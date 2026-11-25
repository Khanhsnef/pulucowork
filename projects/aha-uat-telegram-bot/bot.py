"""Dedicated Group & DM Telegram Bot for Ahamove UAT Order Creation & Driver Assignment."""

import json
import sys
import time
from typing import Any

import requests

from aha_client import (
    assign_order,
    build_order_payload,
    create_order,
    decode_jwt_info,
    ensure_valid_admin_token,
    ensure_valid_user_token,
    normalize_driver_id,
    parse_curl_credentials,
)
from config import ALLOW_DM, BOT_TOKEN, ENV_FILE, GIST_ID, MAX_RUNTIME_SEC, load_store, save_store

SESSION = requests.Session()

# Per-(chat_id, user_id) conversation state so multiple members in a group don't collide
USER_STATES: dict[tuple[int, int], dict[str, Any]] = {}


def tg_url(method: str) -> str:
    return f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"


def tg_call(method: str, payload: dict[str, Any], timeout: int = 30) -> dict[str, Any]:
    try:
        resp = SESSION.post(tg_url(method), json=payload, timeout=timeout)
        return resp.json()
    except Exception as exc:
        print(f"⚠️ Telegram API error ({method}): {exc}")
        return {"ok": False, "description": str(exc)}


def register_bot_commands() -> None:
    """Delete any existing webhook and register slash commands menu in Telegram."""
    wh = tg_call("deleteWebhook", {"drop_pending_updates": False})
    if wh.get("ok"):
        print("🔓 Đã gỡ Webhook cũ (Make.com/n8n) để kích hoạt Long Polling.")
    commands = [
        {"command": "menu", "description": "Bảng điều khiển Tạo đơn & Gán đơn"},
        {"command": "tao", "description": "Tạo đơn UAT nhanh theo mẫu"},
        {"command": "new", "description": "Tạo đơn UAT tùy chỉnh (Dịch vụ, COD, Ghi chú)"},
        {"command": "gan", "description": "Gán đơn XYZ cho tài xế: /gan <MÃ_ĐƠN> [SĐT_TX]"},
        {"command": "taogan", "description": "Tạo đơn mới & Gán ngay: /taogan [SĐT_TX]"},
        {"command": "nap", "description": "Nạp cURL / Token mới (hỗ trợ Group Privacy ON)"},
        {"command": "token", "description": "Kiểm tra thời hạn User/Admin Token"},
        {"command": "bind_group", "description": "Khóa Bot chỉ phục vụ nhóm hiện tại"},
        {"command": "cancel", "description": "Hủy thao tác đang nhập"},
    ]
    tg_call("setMyCommands", {"commands": commands})


def send_msg(
    chat_id: int,
    text: str,
    reply_markup: dict[str, Any] | None = None,
    reply_to_message_id: int | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    res = tg_call("sendMessage", payload)
    if not res.get("ok") and "parse_mode" in payload:
        payload.pop("parse_mode", None)
        res = tg_call("sendMessage", payload)
    return res


def answer_callback(cq_id: str, text: str = "") -> None:
    tg_call("answerCallbackQuery", {"callback_query_id": cq_id, "text": text})


def main_menu_keyboard() -> dict[str, Any]:
    store = load_store()
    drv = store.get("default_driver_id", "84981792046")
    return {
        "inline_keyboard": [
            [
                {"text": "📦 Tạo đơn nhanh (/tao)", "callback_data": "menu:quick"},
                {"text": "📝 Tạo tùy chỉnh (/new)", "callback_data": "menu:new"},
            ],
            [
                {"text": "🚀 Gán đơn XYZ (/gan)", "callback_data": "menu:assign"},
                {"text": f"⚡ Tạo & Gán → {drv}", "callback_data": "menu:create_assign"},
            ],
            [
                {"text": "🔑 Trạng thái Token (/token)", "callback_data": "menu:token"},
                {"text": "📥 Nạp cURL (/nap)", "callback_data": "menu:nap"},
            ],
        ]
    }


def _format_token_line(label: str, token: str) -> str:
    if not token:
        return f"• <b>{label}:</b> ❌ Chưa nạp"
    info = decode_jwt_info(token)
    if not info.get("valid"):
        return f"• <b>{label}:</b> ⚠️ {info.get('reason')}"
    rem = info.get("remaining_sec")
    if rem is None:
        ttl = "không rõ hạn"
    elif rem <= 0:
        ttl = f"🔴 Hết hạn ({abs(rem)}s trước)"
    else:
        mins, secs = divmod(rem, 60)
        ttl = f"🟢 Còn {mins}p {secs}s"
    return f"• <b>{label}:</b> {ttl} (<code>{info.get('cid')}</code> | {info.get('typ')})"


def format_token_status() -> str:
    # Auto-refresh tokens before displaying status so user always sees live state
    ensure_valid_user_token(force_refresh=False)
    ensure_valid_admin_token(force_refresh=False)
    store = load_store()
    u_rt = "✅ Có (Tự động gia hạn)" if store.get("user_refresh_token") else "⚪ Chưa có"
    a_rt = "✅ Có (Tự động gia hạn)" if store.get("admin_refresh_token") else "⚪ Chưa có"
    cookie_ok = "✅ Đã lưu" if store.get("admin_cookie") else "⚪ Chưa có"
    bound_grp = store.get("bound_group_id") or "Chưa khóa (dùng /bind_group trong nhóm)"
    drv = store.get("default_driver_id", "84981792046")
    return (
        "🔑 <b>Trạng thái Cấu hình &amp; Token UAT (Auto-Refresh)</b>\n\n"
        + _format_token_line("User Token (Tạo đơn)", store.get("user_token", ""))
        + f"\n  ↳ <i>User Refresh Token:</i> {u_rt}\n"
        + _format_token_line("Admin Token (Gán đơn)", store.get("admin_token", ""))
        + f"\n  ↳ <i>Admin Refresh Token:</i> {a_rt}"
        + f"\n• <b>Admin Cookie:</b> {cookie_ok}"
        + f"\n• <b>Tài xế mặc định:</b> <code>{drv}</code>"
        + f"\n• <b>Nhóm được phép:</b> <code>{bound_grp}</code>\n\n"
        "💡 <i>Bot đã bật cơ chế tự động làm mới JWT mỗi 5 phút bằng Refresh Token — bạn không cần dán lại cURL thủ công nữa!</i>"
    )


def format_json_preview(data: Any, limit: int = 700) -> str:
    raw = json.dumps(data, ensure_ascii=False, indent=2)
    if len(raw) > limit:
        raw = raw[:limit] + "\n..."
    return raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def is_authorized_chat(chat_id: int, cmd: str = "") -> bool:
    """Verify if message comes from the bound group or allowed DM."""
    if cmd in ("/chatid", "/bind_group"):
        return True
    store = load_store()
    bound_group = str(store.get("bound_group_id") or "").strip()
    is_private = chat_id > 0

    if is_private:
        return ALLOW_DM

    # Group chat (< 0): if bound_group is configured, only allow that exact group
    if bound_group and str(chat_id) != bound_group:
        return False
    return True


def execute_create_order(
    chat_id: int,
    overrides: dict[str, Any] | None = None,
    auto_assign_driver: str | None = None,
    reply_to_msg_id: int | None = None,
) -> None:
    store = load_store()
    default_drv = store.get("default_driver_id", "84981792046")
    payload = build_order_payload(overrides)
    send_msg(chat_id, "⏳ Đang gọi API tạo đơn Ahamove UAT...", reply_to_message_id=reply_to_msg_id)
    res = create_order(payload)

    if not res.get("ok"):
        err = res.get("error") or format_json_preview(res.get("body"))
        send_msg(
            chat_id,
            f"❌ <b>Tạo đơn thất bại</b> (HTTP {res.get('status_code')})\n<pre>{err}</pre>",
            reply_markup=main_menu_keyboard(),
            reply_to_message_id=reply_to_msg_id,
        )
        return

    order_id = res.get("order_id") or "UNKNOWN"
    pickup_addr = (payload.get("path") or [{}, {}])[0].get("first_label", "Điểm lấy")
    drop_addr = (payload.get("path") or [{}, {}])[1].get("first_label", "Điểm giao")
    cod_amt = (payload.get("path") or [{}, {}])[1].get("cod", 0)

    msg = (
        f"✅ <b>Tạo đơn UAT thành công!</b>\n"
        f"• Mã đơn: <code>{order_id}</code>\n"
        f"• Dịch vụ: <code>{payload.get('service_id')}</code>\n"
        f"• Lộ trình: <b>{pickup_addr}</b> → <b>{drop_addr}</b>\n"
        f"• COD: <b>{cod_amt:,}đ</b> | Total Pay: <b>{payload.get('total_pay', 0):,}đ</b>\n"
        f"<pre>{format_json_preview(res.get('body'), 450)}</pre>"
    )

    if auto_assign_driver and order_id != "UNKNOWN":
        send_msg(chat_id, msg, reply_to_message_id=reply_to_msg_id)
        execute_assign_order(chat_id, order_id, auto_assign_driver, reply_to_msg_id=reply_to_msg_id)
        return

    kb = None
    if order_id != "UNKNOWN":
        kb = {
            "inline_keyboard": [
                [
                    {
                        "text": f"🚀 Gán ngay {order_id} → {default_drv}",
                        "callback_data": f"quick_assign:{order_id}:{default_drv}",
                    }
                ],
                [
                    {
                        "text": f"👤 Gán {order_id} cho SĐT khác",
                        "callback_data": f"ask_driver:{order_id}",
                    }
                ],
                [{"text": "🏠 Menu chính", "callback_data": "menu:home"}],
            ]
        }
    send_msg(chat_id, msg, reply_markup=kb, reply_to_message_id=reply_to_msg_id)


def execute_assign_order(
    chat_id: int,
    order_id: str,
    driver_id: str,
    reply_to_msg_id: int | None = None,
) -> None:
    norm_driver = normalize_driver_id(driver_id)
    send_msg(
        chat_id,
        f"⏳ Đang gán đơn <code>{order_id.upper()}</code> cho tài xế <code>{norm_driver}</code>...",
        reply_to_message_id=reply_to_msg_id,
    )
    res = assign_order(order_id, norm_driver)

    if res.get("ok"):
        send_msg(
            chat_id,
            f"🎉 <b>Gán đơn thành công!</b>\n"
            f"• Mã đơn: <code>{res['order_id']}</code>\n"
            f"• Tài xế: <code>{res['driver_id']}</code>\n"
            f"<pre>{format_json_preview(res.get('body'), 450)}</pre>",
            reply_markup=main_menu_keyboard(),
            reply_to_message_id=reply_to_msg_id,
        )
    else:
        err = res.get("error") or format_json_preview(res.get("body"))
        send_msg(
            chat_id,
            f"❌ <b>Gán đơn thất bại</b> (HTTP {res.get('status_code')})\n"
            f"• Mã đơn: <code>{res.get('order_id')}</code>\n"
            f"• Tài xế: <code>{res.get('driver_id')}</code>\n"
            f"<pre>{err}</pre>",
            reply_markup=main_menu_keyboard(),
            reply_to_message_id=reply_to_msg_id,
        )


def start_assign_flow(chat_id: int, user_id: int, prefilled_order_id: str | None = None) -> None:
    store = load_store()
    default_drv = store.get("default_driver_id", "84981792046")
    if prefilled_order_id:
        oid = prefilled_order_id.strip().upper()
        USER_STATES[(chat_id, user_id)] = {
            "flow": "assign",
            "step": "driver_id",
            "data": {"order_id": oid},
        }
        kb = {
            "inline_keyboard": [
                [
                    {
                        "text": f"🚀 Gán luôn cho {default_drv}",
                        "callback_data": f"quick_assign:{oid}:{default_drv}",
                    }
                ],
                [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
            ]
        }
        send_msg(
            chat_id,
            f"👤 Nhập <b>SĐT / Mã tài xế</b> để gán cho đơn <code>{oid}</code> (hoặc bấm nút bên dưới):",
            reply_markup=kb,
        )
    else:
        USER_STATES[(chat_id, user_id)] = {"flow": "assign", "step": "order_id", "data": {}}
        send_msg(
            chat_id,
            "📦 Nhập <b>Mã đơn hàng (VD: 26I8NU9H)</b> cần gán tài xế:\n<i>(Hoặc gõ <code>/gan MÃ_ĐƠN SĐT_TX</code>, gõ /cancel để hủy)</i>",
            reply_markup={"force_reply": True, "selective": True},
        )


def start_custom_order_flow(chat_id: int, user_id: int) -> None:
    USER_STATES[(chat_id, user_id)] = {"flow": "new_order", "step": "service_id", "data": {}}
    kb = {
        "inline_keyboard": [
            [
                {"text": "SGN-BIKE", "callback_data": "new:service:SGN-BIKE"},
                {"text": "SGN-EXPRESS", "callback_data": "new:service:SGN-EXPRESS"},
            ],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(chat_id, "1️⃣ Chọn hoặc nhập <b>service_id</b> (VD: <code>SGN-BIKE</code>):", reply_markup=kb)


def handle_state_input(chat_id: int, user_id: int, text: str, msg_id: int | None = None) -> bool:
    state = USER_STATES.get((chat_id, user_id))
    if not state:
        return False

    flow = state["flow"]
    step = state["step"]
    data = state["data"]

    if flow == "assign":
        if step == "order_id":
            oid = text.strip().upper()
            start_assign_flow(chat_id, user_id, oid)
            return True
        if step == "driver_id":
            oid = data["order_id"]
            USER_STATES.pop((chat_id, user_id), None)
            execute_assign_order(chat_id, oid, text.strip(), reply_to_msg_id=msg_id)
            return True

    if flow == "new_order":
        if step == "service_id":
            data["service_id"] = text.strip().upper()
            state["step"] = "cod"
            kb = {
                "inline_keyboard": [
                    [
                        {"text": "COD = 0đ", "callback_data": "new:cod:0"},
                        {"text": "COD = 100,000đ", "callback_data": "new:cod:100000"},
                    ],
                    [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
                ]
            }
            send_msg(chat_id, "2️⃣ Nhập tiền thu hộ <b>COD</b> (VNĐ):", reply_markup=kb)
            return True

        if step == "cod":
            try:
                data["cod"] = int(text.replace(",", "").replace(".", "").strip())
            except ValueError:
                send_msg(chat_id, "⚠️ Vui lòng nhập số nguyên cho COD (VD: <code>0</code> hoặc <code>50000</code>):")
                return True
            state["step"] = "total_pay"
            kb = {
                "inline_keyboard": [
                    [{"text": "Mặc định (58,000đ)", "callback_data": "new:pay:58000"}],
                    [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
                ]
            }
            send_msg(chat_id, "3️⃣ Nhập <b>total_pay</b> (VNĐ):", reply_markup=kb)
            return True

        if step == "total_pay":
            try:
                data["total_pay"] = int(text.replace(",", "").replace(".", "").strip())
            except ValueError:
                send_msg(chat_id, "⚠️ Vui lòng nhập số nguyên cho total_pay (VD: <code>58000</code>):")
                return True
            state["step"] = "remarks"
            kb = {
                "inline_keyboard": [
                    [{"text": "Bỏ qua ghi chú", "callback_data": "new:remarks:none"}],
                    [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
                ]
            }
            send_msg(chat_id, "4️⃣ Nhập <b>ghi chú (remarks)</b> cho tài xế:", reply_markup=kb)
            return True

        if step == "remarks":
            data["remarks"] = None if text.strip().lower() in ("none", "skip", "không", "-") else text.strip()
            USER_STATES.pop((chat_id, user_id), None)
            execute_create_order(chat_id, data, reply_to_msg_id=msg_id)
            return True

    return False


def handle_callback(cq: dict[str, Any]) -> None:
    cq_id = cq["id"]
    msg = cq.get("message") or {}
    chat_id = (msg.get("chat") or {}).get("id")
    user_id = (cq.get("from") or {}).get("id") or chat_id
    data = cq.get("data", "")
    if not chat_id:
        return

    if not is_authorized_chat(chat_id):
        answer_callback(cq_id, "⛔ Nhóm này chưa được cấp quyền.")
        return

    answer_callback(cq_id)
    store = load_store()
    default_drv = store.get("default_driver_id", "84981792046")

    if data == "menu:home":
        USER_STATES.pop((chat_id, user_id), None)
        send_msg(chat_id, "📋 <b>Bảng điều khiển Ahamove UAT</b>:", reply_markup=main_menu_keyboard())
    elif data == "menu:cancel":
        USER_STATES.pop((chat_id, user_id), None)
        send_msg(chat_id, "🚫 Đã hủy thao tác.", reply_markup=main_menu_keyboard())
    elif data == "menu:quick":
        USER_STATES.pop((chat_id, user_id), None)
        execute_create_order(chat_id)
    elif data == "menu:new":
        start_custom_order_flow(chat_id, user_id)
    elif data == "menu:assign":
        start_assign_flow(chat_id, user_id)
    elif data == "menu:create_assign":
        USER_STATES.pop((chat_id, user_id), None)
        execute_create_order(chat_id, auto_assign_driver=default_drv)
    elif data == "menu:token":
        send_msg(chat_id, format_token_status(), reply_markup=main_menu_keyboard())
    elif data == "menu:nap":
        send_msg(
            chat_id,
            "📥 <b>Hãy Reply (Trả lời) tin nhắn này</b> và dán đoạn <code>cURL</code> hoặc <code>JWT</code> của bạn vào:",
            reply_markup={"force_reply": True, "selective": True},
        )
    elif data.startswith("quick_assign:"):
        _, order_id, driver_id = data.split(":", 2)
        USER_STATES.pop((chat_id, user_id), None)
        execute_assign_order(chat_id, order_id, driver_id)
    elif data.startswith("ask_driver:"):
        _, order_id = data.split(":", 1)
        start_assign_flow(chat_id, user_id, order_id)
    elif data.startswith("new:service:"):
        sid = data.split(":", 2)[2]
        state = USER_STATES.setdefault((chat_id, user_id), {"flow": "new_order", "step": "cod", "data": {}})
        state["data"]["service_id"] = sid
        state["step"] = "cod"
        kb = {
            "inline_keyboard": [
                [
                    {"text": "COD = 0đ", "callback_data": "new:cod:0"},
                    {"text": "COD = 100,000đ", "callback_data": "new:cod:100000"},
                ],
                [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
            ]
        }
        send_msg(chat_id, f"✅ Dịch vụ: <code>{sid}</code>\n2️⃣ Chọn hoặc nhập tiền thu hộ <b>COD</b>:", reply_markup=kb)
    elif data.startswith("new:cod:"):
        cod_val = int(data.split(":", 2)[2])
        state = USER_STATES.setdefault((chat_id, user_id), {"flow": "new_order", "step": "total_pay", "data": {}})
        state["data"]["cod"] = cod_val
        state["step"] = "total_pay"
        kb = {
            "inline_keyboard": [
                [{"text": "Mặc định (58,000đ)", "callback_data": "new:pay:58000"}],
                [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
            ]
        }
        send_msg(chat_id, f"✅ COD: <b>{cod_val:,}đ</b>\n3️⃣ Chọn hoặc nhập <b>total_pay</b>:", reply_markup=kb)
    elif data.startswith("new:pay:"):
        pay_val = int(data.split(":", 2)[2])
        state = USER_STATES.setdefault((chat_id, user_id), {"flow": "new_order", "step": "remarks", "data": {}})
        state["data"]["total_pay"] = pay_val
        state["step"] = "remarks"
        kb = {
            "inline_keyboard": [
                [{"text": "Bỏ qua ghi chú → Tạo đơn ngay", "callback_data": "new:remarks:none"}],
                [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
            ]
        }
        send_msg(
            chat_id,
            f"✅ Total Pay: <b>{pay_val:,}đ</b>\n4️⃣ Nhập <b>ghi chú (remarks)</b> hoặc bấm nút bỏ qua:",
            reply_markup=kb,
        )
    elif data == "new:remarks:none":
        state = USER_STATES.pop((chat_id, user_id), None)
        order_data = (state or {}).get("data", {})
        order_data["remarks"] = None
        execute_create_order(chat_id, order_data)


def handle_message(message: dict[str, Any]) -> None:
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    user_id = (message.get("from") or {}).get("id") or chat_id
    msg_id = message.get("message_id")
    text = (message.get("text") or "").strip()
    if not chat_id or not text:
        return

    cmd = text.split()[0].split("@")[0].lower() if text.startswith("/") else ""
    print(f"📩 [chat={chat_id} user={user_id}] {text[:80]}")
    if not is_authorized_chat(chat_id, cmd):
        print(f"⛔ Bỏ qua tin nhắn từ chat_id={chat_id} (chưa được cấp quyền)")
        return

    # 1. Auto-detect cURL or raw JWT in Group or DM (including "/nap curl ..." or "/token curl ...")
    if ("curl " in text.lower() and "ahamove.com" in text.lower()) or text.startswith("eyJ") or (
        cmd in ("/nap", "/token") and len(text.split()) > 1
    ):
        raw_payload = text.split(None, 1)[1] if cmd in ("/nap", "/token") and len(text.split()) > 1 else text
        parsed = parse_curl_credentials(raw_payload)
        if parsed:
            save_store(parsed)
            updated_keys = ", ".join(parsed.keys())
            send_msg(
                chat_id,
                f"✅ Đã tự động bóc tách &amp; lưu: <code>{updated_keys}</code>\n\n{format_token_status()}",
                reply_markup=main_menu_keyboard(),
                reply_to_message_id=msg_id,
            )
            return

    # 2. Slash Commands
    if text.startswith("/"):
        parts = text.split()
        store = load_store()
        default_drv = store.get("default_driver_id", "84981792046")

        if cmd in ("/chatid", "/bind_group"):
            chat_title = chat.get("title") or "Chat cá nhân (DM)"
            if cmd == "/bind_group" and chat_id < 0:
                save_store({"bound_group_id": str(chat_id)})
                send_msg(
                    chat_id,
                    f"🔒 Đã khóa Bot hoạt động riêng cho nhóm <b>{chat_title}</b> (ID: <code>{chat_id}</code>)!",
                    reply_markup=main_menu_keyboard(),
                    reply_to_message_id=msg_id,
                )
            else:
                send_msg(
                    chat_id,
                    f"📍 <b>Thông tin Chat hiện tại:</b>\n"
                    f"• Tên: <b>{chat_title}</b>\n"
                    f"• Chat ID: <code>{chat_id}</code>\n\n"
                    f"👉 Gõ <code>/bind_group</code> ngay trong nhóm để khóa Bot chỉ phục vụ nhóm này.",
                    reply_to_message_id=msg_id,
                )
            return

        if cmd in ("/start", "/menu", "/help"):
            USER_STATES.pop((chat_id, user_id), None)
            help_text = (
                "🚀 <b>Ahamove UAT Group Bot — Tạo đơn &amp; Gán tài xế</b>\n\n"
                "<b>Lệnh dùng nhanh trong nhóm:</b>\n"
                "• <code>/tao</code> (hoặc <code>/quick</code>) — Tạo đơn UAT nhanh theo mẫu\n"
                "• <code>/new</code> — Tạo đơn tùy chỉnh từng bước\n"
                "• <code>/gan &lt;MÃ_ĐƠN&gt; [SĐT_TX]</code> — Gán đơn XYZ trực tiếp\n"
                "• <code>/taogan [SĐT_TX]</code> — Tạo đơn mới &amp; Gán luôn trong 1 bước\n"
                "• <code>/token</code> — Xem thời hạn JWT User/Admin\n"
                "• <code>/bind_group</code> — Khóa Bot vào nhóm hiện tại\n"
                "• <code>/cancel</code> — Hủy thao tác đang nhập\n\n"
                "💡 <i>Khi hết hạn Token (5 phút), chỉ cần dán lệnh <code>cURL</code> vào nhóm hoặc nhắn riêng (DM) cho Bot.</i>"
            )
            send_msg(chat_id, help_text, reply_markup=main_menu_keyboard(), reply_to_message_id=msg_id)
            return

        if cmd == "/cancel":
            USER_STATES.pop((chat_id, user_id), None)
            send_msg(chat_id, "🚫 Đã hủy thao tác.", reply_markup=main_menu_keyboard(), reply_to_message_id=msg_id)
            return

        if cmd == "/token":
            send_msg(chat_id, format_token_status(), reply_markup=main_menu_keyboard(), reply_to_message_id=msg_id)
            return

        if cmd == "/nap":
            send_msg(
                chat_id,
                "📥 <b>Hãy Reply (Trả lời) tin nhắn này</b> và dán đoạn <code>cURL</code> (tạo đơn hoặc gán đơn) vào đây:\n"
                "<i>(Hoặc gõ <code>/nap &lt;dán_cURL&gt;</code>)</i>",
                reply_markup={"force_reply": True, "selective": True},
                reply_to_message_id=msg_id,
            )
            return

        if cmd in ("/tao", "/quick"):
            USER_STATES.pop((chat_id, user_id), None)
            execute_create_order(chat_id, reply_to_msg_id=msg_id)
            return

        if cmd == "/new":
            start_custom_order_flow(chat_id, user_id)
            return

        if cmd in ("/gan", "/assign"):
            USER_STATES.pop((chat_id, user_id), None)
            if len(parts) >= 3:
                execute_assign_order(chat_id, parts[1], parts[2], reply_to_msg_id=msg_id)
            elif len(parts) == 2:
                # If only order_id is provided: /gan 26I8NU9H -> ask or offer 1-click default driver
                start_assign_flow(chat_id, user_id, parts[1])
            else:
                start_assign_flow(chat_id, user_id)
            return

        if cmd in ("/taogan", "/create_assign"):
            USER_STATES.pop((chat_id, user_id), None)
            drv = parts[1] if len(parts) >= 2 else default_drv
            execute_create_order(chat_id, auto_assign_driver=drv, reply_to_msg_id=msg_id)
            return

        return

    # 3. Active multi-step conversation for this (chat_id, user_id)
    if handle_state_input(chat_id, user_id, text, msg_id=msg_id):
        return

    # 4. In private DM, show menu on unknown message; in Group chat, stay completely silent!
    if chat_id > 0:
        send_msg(chat_id, "Chọn một thao tác bên dưới hoặc gõ /menu:", reply_markup=main_menu_keyboard())


def main() -> None:
    if not BOT_TOKEN or BOT_TOKEN.startswith("DÁN_TOKEN"):
        print(f"❌ Chưa cấu hình AHA_BOT_TOKEN trong file: {ENV_FILE}")
        print("👉 Hãy copy .env.example thành .env và điền AHA_BOT_TOKEN của bot mới.")
        sys.exit(1)

    me = tg_call("getMe", {})
    if not me.get("ok"):
        print(f"❌ AHA_BOT_TOKEN không hợp lệ: {me}")
        sys.exit(1)

    bot_info = me["result"]
    cloud_mode = "☁️ CLOUD 24/7 (GitHub Actions + Secret Gist)" if GIST_ID else "💻 LOCAL"
    print(f"🤖 Bot @{bot_info.get('username')} ({bot_info.get('first_name')}) đã khởi động! [{cloud_mode}]")
    register_bot_commands()

    start_ts = time.time()
    offset: int | None = None
    while True:
        if MAX_RUNTIME_SEC > 0 and (time.time() - start_ts) >= MAX_RUNTIME_SEC:
            print(f"🔄 Đã đạt chu kỳ chạy {MAX_RUNTIME_SEC}s trên Cloud, bàn giao sang phiên kế tiếp...")
            break
        try:
            params: dict[str, Any] = {"timeout": 25}
            if offset is not None:
                params["offset"] = offset
            res = SESSION.get(tg_url("getUpdates"), params=params, timeout=30).json()
            if res.get("ok"):
                for upd in res.get("result", []):
                    offset = upd["update_id"] + 1
                    if "callback_query" in upd:
                        handle_callback(upd["callback_query"])
                    elif "message" in upd:
                        handle_message(upd["message"])
            else:
                print(f"⚠️ getUpdates lỗi: {res}")
                if res.get("error_code") == 409 and "webhook" in str(res.get("description", "")).lower():
                    tg_call("deleteWebhook", {"drop_pending_updates": False})
                time.sleep(2)
        except KeyboardInterrupt:
            print("\n🛑 Bot đã dừng.")
            break
        except Exception as exc:
            print(f"⚠️ Polling error: {exc}")
            time.sleep(3)


if __name__ == "__main__":
    main()
