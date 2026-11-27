"""Vercel Serverless Webhook entrypoint for @DMAIChat_Bot."""

import json
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import bot_core  # noqa: E402
import ops_metrics  # noqa: E402


def _send_typing(chat_id: Any) -> None:
    try:
        url = f"https://api.telegram.org/bot{bot_core.TOKEN}/sendChatAction"
        req = urllib.request.Request(
            url,
            data=json.dumps({"chat_id": chat_id, "action": "typing"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass


def process_update(update: dict[str, Any]) -> None:
    """Process a single Telegram update in DM or any Group chat."""
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text") or message.get("caption") or ""
    msg_id = message.get("message_id")
    if not chat_id or not text:
        return

    if text.startswith("/"):
        cmd = text.split()[0].split("@")[0].lower()
        arg = text.partition(" ")[2].strip().lower()
        force_refresh = arg == "refresh"

        if cmd in ("/report", "/ops", "/sgn"):
            _send_typing(chat_id)
            if arg in ("week", "weekly", "tuan", "tuần"):
                try:
                    report_html = ops_metrics.fetch_period_report("week")
                    bot_core.send_telegram_html(chat_id, report_html, reply_to_message_id=msg_id)
                except Exception as exc:
                    bot_core.send_telegram_msg(chat_id, f"⚠️ Không tạo được báo cáo tuần: `{exc}`", reply_to_message_id=msg_id)
                return
            if arg in ("month", "monthly", "thang", "tháng"):
                try:
                    report_html = ops_metrics.fetch_period_report("month")
                    bot_core.send_telegram_html(chat_id, report_html, reply_to_message_id=msg_id)
                except Exception as exc:
                    bot_core.send_telegram_msg(chat_id, f"⚠️ Không tạo được báo cáo tháng: `{exc}`", reply_to_message_id=msg_id)
                return
            refresh_note = ""
            if force_refresh:
                ok, info = ops_metrics.trigger_metabase_refresh()
                refresh_note = (
                    "✅ <i>Đã kích hoạt đồng bộ Metabase mới cho cả 3 Card (74433, 67888, 75557).</i>\n\n"
                    if ok
                    else f"⚠️ <i>Metabase refresh cảnh báo:</i> <code>{ops_metrics._esc(info)}</code>\n\n"
                )
            try:
                report_html = ops_metrics.fetch_full_executive_report(force_refresh=force_refresh)
                bot_core.send_telegram_html(chat_id, refresh_note + report_html, reply_to_message_id=msg_id)
            except Exception as exc:
                bot_core.send_telegram_msg(chat_id, f"⚠️ Không tạo được báo cáo tổng hợp: `{exc}`", reply_to_message_id=msg_id)
            return

        if cmd in ("/supply", "/active"):
            _send_typing(chat_id)
            try:
                brief = ops_metrics.fetch_supply_brief(force_refresh=force_refresh)
                bot_core.send_telegram_html(chat_id, brief, reply_to_message_id=msg_id)
            except Exception as exc:
                bot_core.send_telegram_msg(chat_id, f"⚠️ Không lấy được chỉ số Nguồn cung (Card 74433): `{exc}`", reply_to_message_id=msg_id)
            return

        if cmd in ("/kpi", "/orders", "/perf"):
            _send_typing(chat_id)
            try:
                brief = ops_metrics.fetch_kpi_brief(force_refresh=force_refresh)
                bot_core.send_telegram_html(chat_id, brief, reply_to_message_id=msg_id)
            except Exception as exc:
                bot_core.send_telegram_msg(chat_id, f"⚠️ Không lấy được chỉ số KPI (Card 67888): `{exc}`", reply_to_message_id=msg_id)
            return

        if cmd in ("/driver", "/income"):
            _send_typing(chat_id)
            try:
                brief = ops_metrics.fetch_driver_brief(force_refresh=force_refresh)
                bot_core.send_telegram_html(chat_id, brief, reply_to_message_id=msg_id)
            except Exception as exc:
                bot_core.send_telegram_msg(chat_id, f"⚠️ Không lấy được chỉ số Driver (Card 75557): `{exc}`", reply_to_message_id=msg_id)
            return

        if cmd in ("/mac", "/health", "/mac_clean") and os.environ.get("VERCEL"):
            bot_core.send_telegram_html(
                chat_id,
                "💻 Lệnh <code>/mac</code> chỉ quét được phần cứng khi máy Mac đang bật.\n"
                "☁️ Hiện tại <code>@DMAIChat_Bot</code> đang chạy <b>24/7 trên Vercel Cloud</b> — "
                "gõ <code>/report</code>, <code>/ops</code>, <code>/kpi</code>, <code>/supply</code>, <code>/driver</code> để xem báo cáo vận hành.",
                reply_to_message_id=msg_id,
            )
            return

        if cmd == "/ask":
            query = text.partition(" ")[2].strip()
            if query:
                bot_core.handle_natural_message(chat_id, f"@DMAIChat_Bot {query}", msg_id, message)
            else:
                bot_core.send_telegram_html(
                    chat_id,
                    "💡 Dùng <code>/ask &lt;câu hỏi&gt;</code> hoặc tag <code>@DMAIChat_Bot &lt;câu hỏi&gt;</code> / reply tin nhắn của bot để phân tích chuyên sâu.",
                    reply_to_message_id=msg_id,
                )
            return

        bot_core.handle_command(chat_id, text, msg_id)
    else:
        bot_core.handle_natural_message(chat_id, text, msg_id, message)


class handler(BaseHTTPRequestHandler):
    """Vercel Python Serverless Function handler for @DMAIChat_Bot."""

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self._send_json(
            200,
            {
                "ok": True,
                "service": "dmai-chat-bot",
                "bot": "@DMAIChat_Bot",
                "version": "2.0-multi-sheet-executive",
                "mode": "vercel-webhook",
                "bot_configured": bool(bot_core.TOKEN),
                "ai_configured": bool(
                    bot_core.GEMINI_API_KEY or bot_core.OPENAI_API_KEY or bot_core.ANTHROPIC_API_KEY
                ),
            },
        )

    def do_POST(self) -> None:
        try:
            content_length = int(self.headers.get("Content-Length", "0") or "0")
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            update = json.loads(raw_body.decode("utf-8"))
        except Exception as exc:
            self._send_json(400, {"ok": False, "error": f"Invalid JSON: {exc}"})
            return

        try:
            process_update(update)
        except Exception as exc:
            print(f"⚠️ @DMAIChat_Bot webhook error: {exc}")

        self._send_json(200, {"ok": True})
