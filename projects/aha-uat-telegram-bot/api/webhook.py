"""Vercel Serverless Webhook entrypoint for Ahamove UAT Telegram Bot."""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import bot  # noqa: E402
from config import BOT_TOKEN, load_store, save_store  # noqa: E402

WEBHOOK_SECRET = os.environ.get("AHA_WEBHOOK_SECRET", "").strip()


def _hydrate_user_states() -> str:
    """Load persisted multi-step USER_STATES from store into bot.USER_STATES."""
    store = load_store()
    raw_states = store.get("user_states") or {}
    bot.USER_STATES.clear()
    for key, val in raw_states.items():
        if ":" in key and isinstance(val, dict):
            chat_str, user_str = key.split(":", 1)
            try:
                bot.USER_STATES[(int(chat_str), int(user_str))] = val
            except ValueError:
                continue
    return json.dumps(raw_states, sort_keys=True, ensure_ascii=False)


def _persist_user_states(before_snapshot: str) -> None:
    """Persist bot.USER_STATES back to store only if it changed."""
    serialized = {
        f"{chat_id}:{user_id}": val
        for (chat_id, user_id), val in bot.USER_STATES.items()
    }
    after_snapshot = json.dumps(serialized, sort_keys=True, ensure_ascii=False)
    if after_snapshot != before_snapshot:
        save_store({"user_states": serialized})


def process_telegram_update(update: dict[str, Any]) -> None:
    """Dispatch a single Telegram update through bot handlers with state sync."""
    before_snapshot = _hydrate_user_states()
    try:
        if "callback_query" in update:
            bot.handle_callback(update["callback_query"])
        elif "message" in update:
            bot.handle_message(update["message"])
    finally:
        _persist_user_states(before_snapshot)


class handler(BaseHTTPRequestHandler):
    """Vercel Python Serverless Function handler."""

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
                "service": "aha-uat-telegram-bot",
                "mode": "vercel-webhook",
                "bot_configured": bool(BOT_TOKEN),
            },
        )

    def do_POST(self) -> None:
        if WEBHOOK_SECRET:
            header_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
            if header_secret != WEBHOOK_SECRET:
                self._send_json(403, {"ok": False, "error": "Invalid webhook secret"})
                return

        try:
            content_length = int(self.headers.get("Content-Length", "0") or "0")
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            update = json.loads(raw_body.decode("utf-8"))
        except Exception as exc:
            self._send_json(400, {"ok": False, "error": f"Invalid JSON: {exc}"})
            return

        try:
            process_telegram_update(update)
        except Exception as exc:
            # Always return 200 to Telegram so it doesn't spam retries on app errors
            print(f"⚠️ Webhook processing error: {exc}")

        self._send_json(200, {"ok": True})
