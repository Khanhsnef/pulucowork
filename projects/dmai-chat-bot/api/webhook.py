"""Vercel Serverless Webhook entrypoint for @DMAIChat_Bot."""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import bot_core  # noqa: E402
import ops_metrics  # noqa: E402


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
        if cmd in ("/ops", "/kpi", "/sgn"):
            refresh_note = ""
            force_refresh = arg == "refresh"
            if force_refresh:
                ok, info = ops_metrics.trigger_metabase_refresh()
                refresh_note = "✅ Đã kích hoạt Metabase export mới.\n\n" if ok else f"⚠️ Metabase refresh cảnh báo: `{info}`\n\n"
            try:
                brief = ops_metrics.fetch_ops_brief(force_refresh=force_refresh)
                bot_core.send_telegram_msg(chat_id, refresh_note + brief, reply_to_message_id=msg_id)
            except Exception as exc:
                bot_core.send_telegram_msg(chat_id, f"⚠️ Không lấy được chỉ số Ops: `{exc}`", reply_to_message_id=msg_id)
            return
        if cmd in ("/mac", "/health", "/mac_clean") and os.environ.get("VERCEL"):
            bot_core.send_telegram_msg(
                chat_id,
                "💻 Lệnh `/mac` chỉ quét được phần cứng khi máy Mac đang bật.\n"
                "☁️ Hiện tại `@DMAIChat_Bot` đang chạy **24/7 trên Vercel Cloud** — bạn có thể chat AI hoặc dùng `/status`, `/chatid`, `/help` bình thường kể cả khi tắt máy.",
                reply_to_message_id=msg_id,
            )
            return
        if cmd == "/ask":
            query = text.partition(" ")[2].strip()
            if query:
                bot_core.handle_natural_message(chat_id, f"@DMAIChat_Bot {query}", msg_id, message)
            else:
                bot_core.send_telegram_msg(
                    chat_id,
                    "💡 Dùng `/ask <câu hỏi>` hoặc tag `@DMAIChat_Bot <câu hỏi>` / reply tin nhắn của bot để trao đổi trong bất kỳ group nào.",
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
