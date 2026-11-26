"""Configuration & Cloud Gist state storage for Ahamove UAT Group Telegram Bot."""

import json
import os
import time
from pathlib import Path
from typing import Any

import requests

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"
STATE_FILE = BASE_DIR / ".tokens.json"
GIST_FILENAME = "aha_uat_tokens.json"

_GIST_CACHE: dict[str, Any] = {"ts": 0.0, "data": None}


def load_local_env() -> None:
    """Load local .env in projects/aha-uat-telegram-bot/.env if present."""
    if not ENV_FILE.exists():
        return
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_local_env()

BOT_TOKEN = os.environ.get("AHA_BOT_TOKEN", "").strip()
GROUP_CHAT_ID = os.environ.get("AHA_GROUP_CHAT_ID", "").strip()
ALLOW_DM = os.environ.get("AHA_ALLOW_DM", "true").strip().lower() in ("1", "true", "yes")
DEFAULT_DRIVER_ID = os.environ.get("AHA_DEFAULT_DRIVER_ID", "84981792046").strip()
GIST_ID = os.environ.get("AHA_GIST_ID", "").strip()
GIST_TOKEN = os.environ.get("AHA_GIST_TOKEN", "").strip()
MAX_RUNTIME_SEC = int(os.environ.get("AHA_MAX_RUNTIME_SEC", "0") or "0")

DEFAULT_ORDER_TEMPLATE: dict[str, Any] = {
    "path": [
        {
            "address": "B Coffee, 7a/3, Thành Thái, Phường 14, Quận 10, Hồ Chí Minh, Việt Nam",
            "lat": 10.769329,
            "lng": 106.663079,
            "cod": 0,
            "adr_source": "pelias",
            "mobile": "",
            "name": "",
            "first_label": "B Coffee",
            "second_label": "7a/3, Thành Thái, Phường 14, Quận 10, Hồ Chí Minh, Việt Nam",
        },
        {
            "address": "113 Hồ Học Lãm, P.An Lạc, TP.Hồ Chí Minh, 70000, Vietnam",
            "lat": 10.715147,
            "lng": 106.615403,
            "cod": 0,
            "adr_source": "grb_AQAEAE0AEKIGmx3B9_7ixEIeShtkVmF2086Ho9X-we0nE6FVDrNbQk-mIYqTKtkve6D950E9KAvPUgczdUAbVVILruC8lMEzS9X0kivdDfkYe0E2lVBQHAwGtMnpzPqzpB3b5GR-UVCf0dWVZUWBPN2NSg",
            "mobile": "0981792046",
            "name": "Khanh Lê Phương",
            "first_label": "113 Hồ Học Lãm",
            "second_label": "P.An Lạc, TP.Hồ Chí Minh, 70000, Vietnam",
        },
    ],
    "requests": [{"_id": "SGN-BIKE-INSURANCE"}],
    "service_id": "SGN-BIKE",
    "service": {"_id": "SGN-BIKE", "requests": [{"_id": "SGN-BIKE-INSURANCE"}]},
    "remarks": None,
    "images": None,
    "order_time": 0,
    "app_source": "web_user",
    "total_pay": 58000,
    "method_id": "LG5Z",
    "method_type": "cash",
    "payment_method": "cash",
    "package_detail": [],
    "package_size": "S",
    "package_weight": 5,
    "item_descriptions": [{"code": "732", "keyword": "Khác", "group": "other"}],
    "reorder_from": "26I8NU9H",
}


def _fetch_from_gist() -> dict[str, Any] | None:
    if not GIST_ID or not GIST_TOKEN:
        return None
    now = time.time()
    if _GIST_CACHE["data"] is not None and (now - _GIST_CACHE["ts"]) < 30:
        return _GIST_CACHE["data"]
    try:
        resp = requests.get(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={
                "Authorization": f"Bearer {GIST_TOKEN}",
                "Accept": "application/vnd.github+json",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            files = resp.json().get("files") or {}
            content = (files.get(GIST_FILENAME) or {}).get("content")
            if content:
                parsed = json.loads(content)
                _GIST_CACHE["ts"] = now
                _GIST_CACHE["data"] = parsed
                STATE_FILE.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
                return parsed
    except Exception as exc:
        print(f"⚠️ Gist read warning: {exc}")
    return None


def _push_to_gist(data: dict[str, Any]) -> None:
    if not GIST_ID or not GIST_TOKEN:
        return
    try:
        resp = requests.patch(
            f"https://api.github.com/gists/{GIST_ID}",
            headers={
                "Authorization": f"Bearer {GIST_TOKEN}",
                "Accept": "application/vnd.github+json",
            },
            json={"files": {GIST_FILENAME: {"content": json.dumps(data, indent=2, ensure_ascii=False)}}},
            timeout=10,
        )
        if resp.status_code == 200:
            _GIST_CACHE["ts"] = time.time()
            _GIST_CACHE["data"] = data
    except Exception as exc:
        print(f"⚠️ Gist write warning: {exc}")


def load_store() -> dict[str, Any]:
    """Load persisted tokens from local file or Cloud Secret Gist."""
    data: dict[str, Any] = {
        "user_token": "",
        "user_refresh_token": "",
        "user_mobile": "84981792046",
        "user_imei": "lO10z54KkUncGeOyTPYo",
        "admin_token": "",
        "admin_refresh_token": "",
        "admin_mobile": "84981792046",
        "admin_cookie": "",
        "adminv2_cookie": "",
        "bound_group_id": GROUP_CHAT_ID,
        "default_driver_id": DEFAULT_DRIVER_ID,
        "order_template": None,
    }
    if not STATE_FILE.exists():
        _fetch_from_gist()
    if STATE_FILE.exists():
        try:
            stored = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            for k in data:
                if stored.get(k):
                    data[k] = stored[k]
        except (json.JSONDecodeError, OSError):
            pass
    elif _GIST_CACHE["data"]:
        for k in data:
            if _GIST_CACHE["data"].get(k):
                data[k] = _GIST_CACHE["data"][k]

    if GROUP_CHAT_ID:
        data["bound_group_id"] = GROUP_CHAT_ID
    return data


def save_store(updates: dict[str, Any]) -> dict[str, Any]:
    """Save updates locally and sync to Cloud Secret Gist."""
    current = load_store()
    changed = False
    for k, v in updates.items():
        if v is not None:
            clean_v = v.strip() if isinstance(v, str) else v
            if current.get(k) != clean_v:
                current[k] = clean_v
                changed = True
    STATE_FILE.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")
    if changed:
        _push_to_gist(current)
    return current
