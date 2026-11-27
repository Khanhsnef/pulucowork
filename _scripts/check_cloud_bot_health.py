#!/usr/bin/env python3
"""
Daily Cloud Bot Webhook Health Check & Auto-Heal.
Checks Vercel webhook endpoint latency/status and Telegram getWebhookInfo.
If webhook is missing/mismatched, automatically restores it via setWebhook.
"""
import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WEBHOOK_URL = "https://aha-uat-telegram-bot.vercel.app/api/webhook"
DEFAULT_CHAT_ID = "-1001733758627"


def load_env_files() -> dict[str, str]:
    env: dict[str, str] = {}
    for env_path in (ROOT / ".env", ROOT / "projects" / "aha-uat-telegram-bot" / ".env"):
        if env_path.exists():
            for raw in env_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if v})
    return env


def http_get_json(url: str, timeout: int = 12) -> tuple[int, dict[str, Any], int]:
    start = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": "Pulu-CloudBot-HealthCheck/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        latency_ms = int((time.time() - start) * 1000)
        data = json.loads(resp.read().decode("utf-8"))
        return resp.status, data, latency_ms


def check_cloud_bot(webhook_url: str, bot_token: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "webhook_url": webhook_url,
        "endpoint_ok": False,
        "latency_ms": None,
        "bot_configured": False,
        "tg_webhook_ok": False,
        "tg_url": "",
        "pending_updates": 0,
        "last_error": "",
        "auto_healed": False,
        "error": "",
    }

    # 1. Check Vercel endpoint
    try:
        status, data, latency_ms = http_get_json(webhook_url, timeout=15)
        result["latency_ms"] = latency_ms
        result["endpoint_ok"] = status == 200 and bool(data.get("ok"))
        result["bot_configured"] = bool(data.get("bot_configured"))
    except Exception as exc:
        result["error"] = f"Endpoint lỗi: {exc}"

    # 2. Check Telegram getWebhookInfo (+ Auto-Heal if missing)
    if bot_token:
        try:
            _, info, _ = http_get_json(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
            if info.get("ok"):
                wh = info.get("result") or {}
                result["tg_url"] = wh.get("url", "")
                result["pending_updates"] = int(wh.get("pending_update_count", 0) or 0)
                result["last_error"] = wh.get("last_error_message", "") or ""

                if result["tg_url"] != webhook_url and result["endpoint_ok"]:
                    set_url = (
                        f"https://api.telegram.org/bot{bot_token}/setWebhook?"
                        + urllib.parse.urlencode({"url": webhook_url})
                    )
                    _, set_res, _ = http_get_json(set_url)
                    if set_res.get("ok"):
                        result["tg_url"] = webhook_url
                        result["auto_healed"] = True

                result["tg_webhook_ok"] = result["tg_url"] == webhook_url
        except Exception as exc:
            result["error"] = (result["error"] + f" | TG lỗi: {exc}").strip(" |")

    return result


def format_status_message(res: dict[str, Any], now_str: str) -> str:
    healthy = res["endpoint_ok"] and res["tg_webhook_ok"] and not res["last_error"]
    badge = "🟢 ỔN ĐỊNH (24/7)" if healthy else "🟠 CẦN KIỂM TRA"
    if res["auto_healed"]:
        badge = "🟡 ĐÃ TỰ KHÔI PHỤC WEBHOOK"

    endpoint_str = (
        f"Online (`{res['latency_ms']}ms`)" if res["endpoint_ok"] else f"Offline ({res['error'] or 'Lỗi kết nối'})"
    )
    tg_str = "Đang trỏ đúng Vercel" if res["tg_webhook_ok"] else f"Lệch/Trống (`{res['tg_url'] or 'none'}`)"
    err_line = f"\n• Lỗi Telegram gần nhất: `{res['last_error']}`" if res["last_error"] else ""
    heal_line = "\n• Hành động: _Đã tự động gọi lại `setWebhook` thành công._" if res["auto_healed"] else ""

    return (
        f"☁️ *BÁO CÁO SỨC KHỎE CLOUD BOT ({now_str})*\n"
        f"• Trạng thái: *{badge}*\n"
        f"• Vercel Endpoint: {endpoint_str}\n"
        f"• Telegram Webhook: {tg_str}\n"
        f"• Pending updates: `{res['pending_updates']}` | Env Token: `{'OK' if res['bot_configured'] else 'Thiếu'}`"
        f"{err_line}{heal_line}"
    )


def send_telegram_text(token: str, chat_id: str, text: str) -> bool:
    if not token or not chat_id:
        print("⚠️ Missing TELEGRAM_BOT_TOKEN or chat_id; skipping Telegram send.")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status == 200


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Vercel Cloud Bot Webhook health.")
    parser.add_argument("--notify", action="store_true", help="Send report to Telegram health group.")
    args = parser.parse_args()

    env = load_env_files()
    webhook_url = env.get("AHA_WEBHOOK_URL") or DEFAULT_WEBHOOK_URL
    aha_bot_token = env.get("AHA_BOT_TOKEN", "")
    notify_token = env.get("TELEGRAM_BOT_TOKEN", "") or aha_bot_token
    chat_id = env.get("MAC_HEALTH_CHAT_ID") or env.get("TELEGRAM_CHAT_ID") or DEFAULT_CHAT_ID

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    res = check_cloud_bot(webhook_url, aha_bot_token)
    msg = format_status_message(res, now_str)
    print(msg)

    if args.notify:
        ok = send_telegram_text(notify_token, chat_id, msg)
        print(f"Telegram notify sent: {ok} -> {chat_id}")


if __name__ == "__main__":
    main()
