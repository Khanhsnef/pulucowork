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
    estimate_order_fee,
    normalize_driver_id,
    parse_curl_credentials,
    reverse_geocode_location,
    search_places,
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
        print("🔓 Đã gỡ Webhook cũ để kích hoạt Long Polling.")
    commands = [
        {"command": "menu", "description": "Bảng điều khiển Tạo đơn & Gán đơn"},
        {"command": "tao", "description": "Tạo đơn UAT nhanh theo mẫu"},
        {"command": "new", "description": "Tạo đơn tùy chỉnh (Địa chỉ, Người gửi/nhận, COD...)"},
        {"command": "gan", "description": "Gán đơn XYZ cho tài xế: /gan <MÃ_ĐƠN> [SĐT_TX]"},
        {"command": "taogan", "description": "Tạo đơn mới & Gán ngay: /taogan [SĐT_TX]"},
        {"command": "nap", "description": "Nạp cURL / Token mới"},
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
        "disable_web_page_preview": True,
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
        "💡 <i>Bot tự động làm mới JWT mỗi 5 phút bằng Refresh Token trên Cloud 24/7.</i>"
    )


def format_json_preview(data: Any, limit: int = 700) -> str:
    raw = json.dumps(data, ensure_ascii=False, indent=2)
    if len(raw) > limit:
        raw = raw[:limit] + "\n..."
    return raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _esc(text: Any) -> str:
    return str(text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def is_authorized_chat(chat_id: int, cmd: str = "") -> bool:
    if cmd in ("/chatid", "/bind_group"):
        return True
    store = load_store()
    bound_group = str(store.get("bound_group_id") or "").strip()
    if chat_id > 0:
        return ALLOW_DM
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
    p0 = (payload.get("path") or [{}, {}])[0]
    p1 = (payload.get("path") or [{}, {}])[1]
    cod_amt = p1.get("cod", 0)

    msg = (
        f"✅ <b>Tạo đơn UAT thành công!</b>\n"
        f"• Mã đơn: <code>{order_id}</code>\n"
        f"• Dịch vụ: <code>{payload.get('service_id')}</code>\n"
        f"• 📍 <b>Lấy:</b> {_esc(p0.get('address'))}\n"
        f"  ↳ Người gửi: <b>{_esc(p0.get('name') or 'Mặc định')}</b> ({_esc(p0.get('mobile') or 'Trống')})\n"
        f"• 🏁 <b>Giao:</b> {_esc(p1.get('address'))}\n"
        f"  ↳ Người nhận: <b>{_esc(p1.get('name') or 'Mặc định')}</b> ({_esc(p1.get('mobile') or 'Trống')})\n"
        f"• 💵 COD: <b>{cod_amt:,}đ</b> | 💰 Cước: <b>{payload.get('total_pay', 0):,}đ</b>\n"
        f"• 📝 Ghi chú: <i>{_esc(payload.get('remarks') or 'Không có')}</i>"
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


# ── CUSTOM ORDER WIZARD (/new) ───────────────────────────────────────────────

def _group_reply_hint(chat_id: int) -> str:
    if chat_id < 0:
        return "\n💡 <i>(Trong nhóm: Hãy <b>Reply/Trả lời</b> tin nhắn này khi gõ chữ hoặc gửi ghim Vị trí 📎)</i>"
    return ""


def start_custom_order_flow(chat_id: int, user_id: int) -> None:
    base = build_order_payload()
    p0 = base["path"][0]
    p1 = base["path"][1]
    USER_STATES[(chat_id, user_id)] = {
        "flow": "new_order",
        "step": "service_id",
        "return_to_confirm": False,
        "candidates": [],
        "data": {
            "service_id": base.get("service_id", "SGN-BIKE"),
            "pickup": {
                "address": p0.get("address"),
                "lat": p0.get("lat"),
                "lng": p0.get("lng"),
                "adr_source": p0.get("adr_source", "pelias"),
                "first_label": p0.get("first_label"),
                "second_label": p0.get("second_label"),
            },
            "sender_name": p0.get("name") or "Khanh Lê Phương",
            "sender_mobile": p0.get("mobile") or "0981792046",
            "dropoff": {
                "address": p1.get("address"),
                "lat": p1.get("lat"),
                "lng": p1.get("lng"),
                "adr_source": p1.get("adr_source", "pelias"),
                "first_label": p1.get("first_label"),
                "second_label": p1.get("second_label"),
            },
            "recipient_name": p1.get("name") or "Khanh Lê Phương",
            "recipient_mobile": p1.get("mobile") or "0981792046",
            "cod": p1.get("cod", 0),
            "total_pay": base.get("total_pay", 58000),
            "remarks": base.get("remarks"),
        },
    }
    prompt_service_step(chat_id, user_id)


def prompt_service_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "service_id"
    kb = {
        "inline_keyboard": [
            [
                {"text": "🛵 SGN-BIKE", "callback_data": "new:service:SGN-BIKE"},
                {"text": "⚡ SGN-EXPRESS", "callback_data": "new:service:SGN-EXPRESS"},
            ],
            [
                {"text": "📦 SGN-SAMEDAY", "callback_data": "new:service:SGN-SAMEDAY"},
                {"text": "🚚 SGN-TRUCK-500", "callback_data": "new:service:SGN-TRUCK-500"},
            ],
            [
                {"text": "⏩ Đi thẳng tới Xác nhận đơn", "callback_data": "new:goto:confirm"},
                {"text": "❌ Hủy", "callback_data": "menu:cancel"},
            ],
        ]
    }
    send_msg(
        chat_id,
        "1️⃣ <b>Chọn Dịch vụ (service_id)</b> hoặc gõ mã dịch vụ khác:" + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_pickup_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "pickup_address"
    cur = state["data"]["pickup"]
    kb = {
        "inline_keyboard": [
            [{"text": f"⏭ Giữ: {cur['first_label'][:32]}", "callback_data": "new:pickup:keep"}],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        "2️⃣ 📍 <b>Địa chỉ &amp; Tọa độ Điểm Lấy Hàng (Người gửi)</b>\n"
        f"• Hiện tại: <code>{_esc(cur['address'])}</code> (<code>{cur['lat']}, {cur['lng']}</code>)\n\n"
        "👉 <b>3 cách chọn đúng địa chỉ &amp; tọa độ:</b>\n"
        "1. <b>Gõ tên địa chỉ / tòa nhà / số nhà</b> (VD: <code>Bitexco Quận 1</code> hoặc <code>268 Lý Thường Kiệt Q10</code>) để tìm trên bản đồ Ahamove.\n"
        "2. <b>Bấm nút 📎 (Đính kèm) → Location (Vị trí)</b> trên Telegram điện thoại để kéo ghim trực tiếp trên bản đồ.\n"
        "3. <b>Dán tọa độ</b> <code>lat, lng</code> (VD: <code>10.7721, 106.6983</code>)."
        + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_sender_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "sender_info"
    d = state["data"]
    kb = {
        "inline_keyboard": [
            [
                {
                    "text": f"⏭ Giữ: {d['sender_name']} ({d['sender_mobile']})",
                    "callback_data": "new:sender:keep",
                }
            ],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        "3️⃣ 👤 <b>Thông tin Người gửi (Tên &amp; SĐT)</b>\n"
        f"• Hiện tại: <b>{_esc(d['sender_name'])}</b> — <code>{_esc(d['sender_mobile'])}</code>\n\n"
        "👉 Nhập theo cú pháp <code>Tên | SĐT</code> (VD: <code>Shop Aha | 0981792046</code>) hoặc bấm nút giữ mặc định:"
        + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_dropoff_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "dropoff_address"
    cur = state["data"]["dropoff"]
    kb = {
        "inline_keyboard": [
            [{"text": f"⏭ Giữ: {cur['first_label'][:32]}", "callback_data": "new:dropoff:keep"}],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        "4️⃣ 🏁 <b>Địa chỉ &amp; Tọa độ Điểm Giao Hàng (Người nhận)</b>\n"
        f"• Hiện tại: <code>{_esc(cur['address'])}</code> (<code>{cur['lat']}, {cur['lng']}</code>)\n\n"
        "👉 <b>3 cách chọn đúng địa chỉ &amp; tọa độ:</b>\n"
        "1. <b>Gõ tên địa chỉ / tòa nhà / số nhà</b> (VD: <code>Landmark 81</code> hoặc <code>113 Hồ Học Lãm</code>) để tìm và chọn từ danh sách Ahamove.\n"
        "2. <b>Bấm nút 📎 (Đính kèm) → Location (Vị trí)</b> trên Telegram điện thoại để ghim trên bản đồ.\n"
        "3. <b>Dán tọa độ</b> <code>lat, lng</code>."
        + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_recipient_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "recipient_info"
    d = state["data"]
    kb = {
        "inline_keyboard": [
            [
                {
                    "text": f"⏭ Giữ: {d['recipient_name']} ({d['recipient_mobile']})",
                    "callback_data": "new:recipient:keep",
                }
            ],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        "5️⃣ 📲 <b>Thông tin Người nhận (Tên &amp; SĐT)</b>\n"
        f"• Hiện tại: <b>{_esc(d['recipient_name'])}</b> — <code>{_esc(d['recipient_mobile'])}</code>\n\n"
        "👉 Nhập theo cú pháp <code>Tên | SĐT</code> (VD: <code>Nguyễn Văn A | 0909123456</code>) hoặc bấm giữ mặc định:"
        + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_cod_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "cod"
    kb = {
        "inline_keyboard": [
            [
                {"text": "COD = 0đ", "callback_data": "new:cod:0"},
                {"text": "100,000đ", "callback_data": "new:cod:100000"},
            ],
            [
                {"text": "200,000đ", "callback_data": "new:cod:200000"},
                {"text": "500,000đ", "callback_data": "new:cod:500000"},
            ],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        "6️⃣ 💵 <b>Chọn hoặc nhập tiền thu hộ COD (VNĐ):</b>" + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_total_pay_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "total_pay"
    d = state["data"]
    est = estimate_order_fee(d)
    est_pay = est.get("total_pay", d.get("total_pay", 58000))
    dist = est.get("distance")
    warn = est.get("warning")
    d["estimated_distance"] = dist
    d["total_pay"] = est_pay
    if warn and d.get("cod", 0) > 0:
        d["cod"] = 0

    dist_label = f" ({dist} km)" if dist is not None else ""
    warn_line = f"⚠️ <i>Lưu ý Ahamove UAT: {_esc(warn)} (Đã tự đưa COD về 0đ)</i>\n" if warn else ""
    kb = {
        "inline_keyboard": [
            [
                {
                    "text": f"💰 Dùng giá Ahamove tính: {est_pay:,}đ{dist_label}",
                    "callback_data": f"new:pay:{est_pay}",
                }
            ],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        f"7️⃣ 💰 <b>Cước phí đơn hàng (total_pay)</b>\n"
        + warn_line
        + f"• Hệ thống Ahamove UAT tự tính theo lộ trình: <b>{est_pay:,}đ</b>{dist_label}\n"
        "👉 Bấm nút bên dưới để dùng mức phí chuẩn này hoặc nhập số tiền khác:"
        + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def prompt_remarks_step(chat_id: int, user_id: int) -> None:
    state = USER_STATES[(chat_id, user_id)]
    state["step"] = "remarks"
    kb = {
        "inline_keyboard": [
            [{"text": "⏭ Không ghi chú → Xem tóm tắt đơn", "callback_data": "new:remarks:none"}],
            [{"text": "❌ Hủy", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(
        chat_id,
        "8️⃣ 📝 <b>Nhập ghi chú (remarks) cho tài xế</b> hoặc bấm bỏ qua:" + _group_reply_hint(chat_id),
        reply_markup=kb,
    )


def show_order_confirmation(chat_id: int, user_id: int) -> None:
    state = USER_STATES.get((chat_id, user_id))
    if not state:
        return
    state["step"] = "confirm"
    state["return_to_confirm"] = True
    d = state["data"]

    # Refresh fee estimate whenever addresses/service change
    est = estimate_order_fee(d)
    if est.get("ok"):
        d["total_pay"] = est["total_pay"]
        d["estimated_distance"] = est.get("distance")

    p0 = d["pickup"]
    p1 = d["dropoff"]
    dist_str = f"{d.get('estimated_distance')} km" if d.get("estimated_distance") is not None else "N/A"
    gmap_p0 = f"https://maps.google.com/?q={p0['lat']},{p0['lng']}"
    gmap_p1 = f"https://maps.google.com/?q={p1['lat']},{p1['lng']}"

    store = load_store()
    default_drv = store.get("default_driver_id", "84981792046")

    summary = (
        "📋 <b>XÁC NHẬN ĐƠN HÀNG TÙY CHỈNH (UAT)</b>\n\n"
        f"• 🛵 <b>Dịch vụ:</b> <code>{_esc(d['service_id'])}</code> (Quãng đường: <b>{dist_str}</b>)\n\n"
        f"• 📍 <b>Điểm lấy (Pickup):</b>\n"
        f"  <code>{_esc(p0['address'])}</code>\n"
        f"  🌐 Tọa độ: <a href=\"{gmap_p0}\">{p0['lat']}, {p0['lng']} (Xem bản đồ)</a>\n"
        f"  👤 Người gửi: <b>{_esc(d['sender_name'])}</b> — <code>{_esc(d['sender_mobile'])}</code>\n\n"
        f"• 🏁 <b>Điểm giao (Dropoff):</b>\n"
        f"  <code>{_esc(p1['address'])}</code>\n"
        f"  🌐 Tọa độ: <a href=\"{gmap_p1}\">{p1['lat']}, {p1['lng']} (Xem bản đồ)</a>\n"
        f"  📲 Người nhận: <b>{_esc(d['recipient_name'])}</b> — <code>{_esc(d['recipient_mobile'])}</code>\n\n"
        f"• 💵 <b>Thu hộ COD:</b> <b>{d['cod']:,}đ</b>\n"
        f"• 💰 <b>Cước phí (Total Pay):</b> <b>{d['total_pay']:,}đ</b>\n"
        f"• 📝 <b>Ghi chú:</b> <i>{_esc(d.get('remarks') or 'Không có')}</i>\n\n"
        "👇 <b>Chọn Tạo đơn hoặc bấm vào mục bất kỳ để sửa lại:</b>"
    )

    kb = {
        "inline_keyboard": [
            [
                {"text": "✅ Tạo đơn ngay", "callback_data": "new:submit:create"},
                {"text": f"⚡ Tạo & Gán → {default_drv}", "callback_data": "new:submit:create_assign"},
            ],
            [
                {"text": "📍 Sửa Điểm lấy", "callback_data": "new:edit:pickup"},
                {"text": "👤 Sửa Người gửi", "callback_data": "new:edit:sender"},
            ],
            [
                {"text": "🏁 Sửa Điểm giao", "callback_data": "new:edit:dropoff"},
                {"text": "📲 Sửa Người nhận", "callback_data": "new:edit:recipient"},
            ],
            [
                {"text": "🛵 Sửa Dịch vụ", "callback_data": "new:edit:service"},
                {"text": "💵 Sửa COD/Phí", "callback_data": "new:edit:cod"},
                {"text": "📝 Sửa Ghi chú", "callback_data": "new:edit:remarks"},
            ],
            [{"text": "❌ Hủy đơn", "callback_data": "menu:cancel"}],
        ]
    }
    send_msg(chat_id, summary, reply_markup=kb)


def _parse_contact_input(raw: str, default_name: str, default_mobile: str) -> tuple[str, str]:
    if "|" in raw:
        left, right = raw.split("|", 1)
        return left.strip() or default_name, right.strip() or default_mobile
    cleaned = raw.strip()
    # If user only typed a phone number
    if cleaned.replace("+", "").replace(" ", "").isdigit() and len(cleaned) >= 9:
        return default_name, cleaned
    return cleaned, default_mobile


def _show_place_candidates(chat_id: int, user_id: int, target_key: str, query: str) -> None:
    state = USER_STATES[(chat_id, user_id)]
    candidates = search_places(query, limit=5)
    if not candidates:
        send_msg(
            chat_id,
            f"⚠️ Không tìm thấy địa chỉ nào khớp với <code>{_esc(query)}</code>.\n"
            "👉 Hãy thử gõ rõ hơn (VD: <code>Số nhà, Tên đường, Quận, TP.HCM</code>) hoặc gửi ghim <b>📎 Location (Vị trí)</b> trên Telegram:",
        )
        return

    state["candidates"] = candidates
    buttons: list[list[dict[str, str]]] = []
    lines = [f"🔎 <b>Kết quả tìm địa chỉ cho:</b> <code>{_esc(query)}</code>\n"]
    for idx, cand in enumerate(candidates):
        num = idx + 1
        lines.append(
            f"<b>{num}.</b> {_esc(cand['address'])}\n"
            f"   ↳ Tọa độ: <code>{cand['lat']}, {cand['lng']}</code>"
        )
        short_lbl = f"{num}. {cand['first_label']} ({cand['second_label'][:26]})"
        buttons.append(
            [
                {
                    "text": short_lbl[:60],
                    "callback_data": f"new:pick_addr:{target_key}:{idx}",
                }
            ]
        )

    buttons.append([{"text": "❌ Hủy", "callback_data": "menu:cancel"}])
    lines.append("\n👇 <b>Chạm vào địa chỉ đúng bên dưới (hoặc gõ từ khóa khác để tìm lại):</b>")
    send_msg(chat_id, "\n".join(lines), reply_markup={"inline_keyboard": buttons})


def handle_location_pin(chat_id: int, user_id: int, loc: dict[str, Any], msg_id: int | None = None) -> bool:
    """Handle Telegram native GPS location pin (📎 -> Location) during pickup or dropoff step."""
    state = USER_STATES.get((chat_id, user_id))
    if not state or state.get("flow") != "new_order":
        return False

    step = state.get("step")
    if step not in ("pickup_address", "dropoff_address"):
        return False

    lat = float(loc["latitude"])
    lng = float(loc["longitude"])
    place = reverse_geocode_location(lat, lng)
    target_key = "pickup" if step == "pickup_address" else "dropoff"
    state["data"][target_key] = place

    label_vi = "Điểm lấy hàng" if target_key == "pickup" else "Điểm giao hàng"
    send_msg(
        chat_id,
        f"📍 Đã nhận ghim bản đồ cho <b>{label_vi}</b>:\n"
        f"• Địa chỉ: <code>{_esc(place['address'])}</code>\n"
        f"• Tọa độ: <code>{place['lat']}, {place['lng']}</code>",
        reply_to_message_id=msg_id,
    )

    if state.get("return_to_confirm"):
        show_order_confirmation(chat_id, user_id)
    elif target_key == "pickup":
        prompt_sender_step(chat_id, user_id)
    else:
        prompt_recipient_step(chat_id, user_id)
    return True


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
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_pickup_step(chat_id, user_id)
            return True

        if step == "pickup_address":
            _show_place_candidates(chat_id, user_id, "pickup", text)
            return True

        if step == "sender_info":
            name, mobile = _parse_contact_input(text, data["sender_name"], data["sender_mobile"])
            data["sender_name"] = name
            data["sender_mobile"] = mobile
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_dropoff_step(chat_id, user_id)
            return True

        if step == "dropoff_address":
            _show_place_candidates(chat_id, user_id, "dropoff", text)
            return True

        if step == "recipient_info":
            name, mobile = _parse_contact_input(text, data["recipient_name"], data["recipient_mobile"])
            data["recipient_name"] = name
            data["recipient_mobile"] = mobile
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_cod_step(chat_id, user_id)
            return True

        if step == "cod":
            try:
                data["cod"] = int(text.replace(",", "").replace(".", "").strip())
            except ValueError:
                send_msg(chat_id, "⚠️ Vui lòng nhập số nguyên cho COD (VD: <code>0</code> hoặc <code>150000</code>):")
                return True
            prompt_total_pay_step(chat_id, user_id)
            return True

        if step == "total_pay":
            try:
                data["total_pay"] = int(text.replace(",", "").replace(".", "").strip())
            except ValueError:
                send_msg(chat_id, "⚠️ Vui lòng nhập số nguyên cho cước phí (VD: <code>58000</code>):")
                return True
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_remarks_step(chat_id, user_id)
            return True

        if step == "remarks":
            data["remarks"] = None if text.strip().lower() in ("none", "skip", "không", "-") else text.strip()
            show_order_confirmation(chat_id, user_id)
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

    # Custom order flow callbacks
    elif data.startswith("new:"):
        if (chat_id, user_id) not in USER_STATES:
            start_custom_order_flow(chat_id, user_id)
        state = USER_STATES[(chat_id, user_id)]
        d = state["data"]

        if data == "new:goto:confirm":
            show_order_confirmation(chat_id, user_id)
        elif data.startswith("new:service:"):
            d["service_id"] = data.split(":", 2)[2]
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_pickup_step(chat_id, user_id)
        elif data == "new:pickup:keep":
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_sender_step(chat_id, user_id)
        elif data == "new:sender:keep":
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_dropoff_step(chat_id, user_id)
        elif data == "new:dropoff:keep":
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_recipient_step(chat_id, user_id)
        elif data == "new:recipient:keep":
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_cod_step(chat_id, user_id)
        elif data.startswith("new:pick_addr:"):
            _, _, target_key, idx_str = data.split(":", 3)
            idx = int(idx_str)
            cands = state.get("candidates") or []
            if 0 <= idx < len(cands):
                chosen = cands[idx]
                d[target_key] = chosen
                lbl = "Điểm lấy hàng" if target_key == "pickup" else "Điểm giao hàng"
                send_msg(
                    chat_id,
                    f"✅ Đã chọn <b>{lbl}</b>:\n"
                    f"• <code>{_esc(chosen['address'])}</code>\n"
                    f"• Tọa độ: <code>{chosen['lat']}, {chosen['lng']}</code>",
                )
                if state.get("return_to_confirm"):
                    show_order_confirmation(chat_id, user_id)
                elif target_key == "pickup":
                    prompt_sender_step(chat_id, user_id)
                else:
                    prompt_recipient_step(chat_id, user_id)
        elif data.startswith("new:cod:"):
            d["cod"] = int(data.split(":", 2)[2])
            prompt_total_pay_step(chat_id, user_id)
        elif data.startswith("new:pay:"):
            d["total_pay"] = int(data.split(":", 2)[2])
            if state.get("return_to_confirm"):
                show_order_confirmation(chat_id, user_id)
            else:
                prompt_remarks_step(chat_id, user_id)
        elif data == "new:remarks:none":
            d["remarks"] = None
            show_order_confirmation(chat_id, user_id)
        elif data.startswith("new:edit:"):
            field = data.split(":", 2)[2]
            state["return_to_confirm"] = True
            if field == "service":
                prompt_service_step(chat_id, user_id)
            elif field == "pickup":
                prompt_pickup_step(chat_id, user_id)
            elif field == "sender":
                prompt_sender_step(chat_id, user_id)
            elif field == "dropoff":
                prompt_dropoff_step(chat_id, user_id)
            elif field == "recipient":
                prompt_recipient_step(chat_id, user_id)
            elif field == "cod":
                prompt_cod_step(chat_id, user_id)
            elif field == "remarks":
                prompt_remarks_step(chat_id, user_id)
        elif data == "new:submit:create":
            order_data = USER_STATES.pop((chat_id, user_id))["data"]
            execute_create_order(chat_id, order_data)
        elif data == "new:submit:create_assign":
            order_data = USER_STATES.pop((chat_id, user_id))["data"]
            execute_create_order(chat_id, order_data, auto_assign_driver=default_drv)


def handle_message(message: dict[str, Any]) -> None:
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    user_id = (message.get("from") or {}).get("id") or chat_id
    msg_id = message.get("message_id")
    if not chat_id:
        return

    # Handle Telegram native GPS Location Pin (📎 -> Location)
    if "location" in message and message["location"]:
        if is_authorized_chat(chat_id):
            handle_location_pin(chat_id, user_id, message["location"], msg_id=msg_id)
        return

    text = (message.get("text") or "").strip()
    if not text:
        return

    cmd = text.split()[0].split("@")[0].lower() if text.startswith("/") else ""
    print(f"📩 [chat={chat_id} user={user_id}] {text[:80]}")
    if not is_authorized_chat(chat_id, cmd):
        print(f"⛔ Bỏ qua tin nhắn từ chat_id={chat_id} (chưa được cấp quyền)")
        return

    # 1. Auto-detect cURL or raw JWT in Group or DM
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
                "🚀 <b>Ahamove UAT Group Bot — Tạo đơn &amp; Gán tài xế (24/7 Cloud)</b>\n\n"
                "<b>Lệnh dùng nhanh trên điện thoại:</b>\n"
                "• <code>/tao</code> (hoặc <code>/quick</code>) — Tạo đơn UAT nhanh theo mẫu\n"
                "• <code>/new</code> — Tạo đơn tùy chỉnh (Tìm địa chỉ Ahamove / Ghim GPS 📎, Người gửi, Người nhận, COD, Tự tính phí)\n"
                "• <code>/gan &lt;MÃ_ĐƠN&gt; [SĐT_TX]</code> — Gán đơn XYZ trực tiếp\n"
                "• <code>/taogan [SĐT_TX]</code> — Tạo đơn mới &amp; Gán luôn trong 1 bước\n"
                "• <code>/token</code> — Xem trạng thái Auto-Refresh Token\n"
                "• <code>/bind_group</code> — Khóa Bot vào nhóm hiện tại\n"
                "• <code>/cancel</code> — Hủy thao tác đang nhập"
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
