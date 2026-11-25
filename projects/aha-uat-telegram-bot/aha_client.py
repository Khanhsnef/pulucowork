"""Ahamove UAT API Client with 100% Automatic Token & Cookie Refresh."""

import base64
import copy
import json
import re
import time
from typing import Any

import requests

from config import DEFAULT_ORDER_TEMPLATE, load_store, save_store

CREATE_ORDER_URL = "https://apiuat.ahamove.com/api/v3/private/order/create"
ASSIGN_ORDER_URL_TMPL = "https://adminv3uat.ahamove.com/api/orders/{order_id}/assign/{driver_id}"
USER_REFRESH_URL = "https://apiuat.ahamove.com/api/v3/public/user/token/refresh"
ADMIN_REFRESH_URL = "https://apiuat.ahamove.com/api/v3/public/supplier/token/refresh"
ADMIN_COOKIE_ACTION_ID = "4078ab85377a01afe7dbaaca5adfcf050f1cce6777"

USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 16; Pixel 10) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Mobile Safari/537.36"
)


def normalize_driver_id(raw: str) -> str:
    """Convert 0981792046 or +84981792046 -> 84981792046."""
    digits = re.sub(r"\D", "", raw.strip())
    if digits.startswith("0") and len(digits) >= 9:
        return "84" + digits[1:]
    return digits


def decode_jwt_info(token: str) -> dict[str, Any]:
    """Decode JWT claims and remaining validity time in seconds."""
    if not token:
        return {"valid": False, "reason": "Chưa nạp token"}
    parts = token.strip().split(".")
    if len(parts) != 3:
        return {"valid": False, "reason": "Không đúng định dạng JWT"}
    try:
        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
        exp = payload.get("exp")
        now = int(time.time())
        remaining = int(exp - now) if isinstance(exp, (int, float)) else None
        return {
            "valid": True,
            "typ": payload.get("typ"),
            "role": payload.get("role"),
            "cid": payload.get("cid"),
            "noc": payload.get("noc"),
            "imei": payload.get("imei"),
            "exp": exp,
            "remaining_sec": remaining,
            "expired": remaining is not None and remaining <= 0,
        }
    except Exception as exc:
        return {"valid": False, "reason": f"Lỗi giải mã JWT: {exc}"}


def sync_user_refresh_from_chrome() -> str | None:
    """Read fresh user refresh_token and token from local Chrome cookies if available."""
    try:
        import browser_cookie3

        cj = browser_cookie3.chrome(domain_name="ahamove.com")
        updates: dict[str, Any] = {}
        for c in cj:
            if c.domain in (".ahamove.com", "appuat.ahamove.com"):
                if c.name == "refresh_token" and c.value:
                    updates["user_refresh_token"] = c.value
                elif c.name == "token" and c.value.startswith("eyJ"):
                    info = decode_jwt_info(c.value)
                    if info.get("valid") and info.get("typ") == "user":
                        updates["user_token"] = c.value
                        if info.get("cid"):
                            updates["user_mobile"] = info["cid"]
                        if info.get("imei"):
                            updates["user_imei"] = info["imei"]
        if updates:
            save_store(updates)
            return updates.get("user_refresh_token")
    except Exception:
        pass
    return None


def refresh_user_token() -> str | None:
    """Refresh user_token using user_refresh_token (or Chrome cookie fallback)."""
    store = load_store()
    rt = store.get("user_refresh_token") or sync_user_refresh_from_chrome()
    if not rt:
        return None

    mobile = store.get("user_mobile") or "84981792046"
    imei = store.get("user_imei") or "lO10z54KkUncGeOyTPYo"

    for attempt in range(2):
        try:
            resp = requests.post(
                USER_REFRESH_URL,
                json={"refresh_token": rt, "mobile": mobile, "type": "web", "imei": imei},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                new_token = data.get("token")
                new_rt = data.get("refresh_token") or rt
                if new_token:
                    save_store({"user_token": new_token, "user_refresh_token": new_rt})
                    return new_token
            # If stored refresh_token expired, try syncing a newer one from Chrome once
            if attempt == 0:
                chrome_rt = sync_user_refresh_from_chrome()
                if chrome_rt and chrome_rt != rt:
                    rt = chrome_rt
                    continue
        except requests.RequestException:
            break
    return None


def ensure_valid_user_token(force_refresh: bool = False) -> str:
    """Return a valid user_token, automatically refreshing if expired or within 30s of expiry."""
    store = load_store()
    token = store.get("user_token", "")
    info = decode_jwt_info(token)
    if not force_refresh and info.get("valid") and (info.get("remaining_sec") or 0) > 30:
        return token
    refreshed = refresh_user_token()
    return refreshed or token


def refresh_admin_token(order_id_hint: str = "26I8NU9H") -> str | None:
    """Refresh admin_token (supplier role=admin) and adminv3uat supplierAuthDataV2 cookie."""
    store = load_store()
    rt = store.get("admin_refresh_token", "")
    if not rt:
        return None

    mobile = store.get("admin_mobile") or "84981792046"
    try:
        resp = requests.post(
            ADMIN_REFRESH_URL,
            json={
                "refresh_token": rt,
                "mobile": mobile,
                "supplier_id": mobile,
                "type": "web",
                "imei": "web",
                "role": "admin",
            },
            timeout=10,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        new_token = data.get("token")
        new_rt = data.get("refresh_token") or rt
        if not new_token:
            return None

        updates: dict[str, Any] = {
            "admin_token": new_token,
            "admin_refresh_token": new_rt,
        }

        # Also refresh supplierAuthDataV2 cookie on adminv3uat via Next-Action
        try:
            r_act = requests.post(
                f"https://adminv3uat.ahamove.com/orders/detail/{order_id_hint}",
                headers={
                    "Next-Action": ADMIN_COOKIE_ACTION_ID,
                    "Content-Type": "text/plain;charset=UTF-8",
                    "Origin": "https://adminv3uat.ahamove.com",
                    "Referer": f"https://adminv3uat.ahamove.com/orders/detail/{order_id_hint}",
                    "User-Agent": USER_AGENT,
                },
                data=json.dumps([new_token]),
                timeout=10,
            )
            cookie_val = r_act.cookies.get("supplierAuthDataV2")
            if cookie_val:
                updates["admin_cookie"] = f"lang=en; supplierAuthDataV2={cookie_val}"
        except requests.RequestException:
            pass

        save_store(updates)
        return new_token
    except requests.RequestException:
        return None


def ensure_valid_admin_token(force_refresh: bool = False, order_id_hint: str = "26I8NU9H") -> str:
    """Return a valid admin_token, automatically refreshing if expired or within 30s of expiry."""
    store = load_store()
    token = store.get("admin_token", "")
    info = decode_jwt_info(token)
    if not force_refresh and info.get("valid") and (info.get("remaining_sec") or 0) > 30:
        return token
    refreshed = refresh_admin_token(order_id_hint=order_id_hint)
    return refreshed or token


def parse_curl_credentials(text: str) -> dict[str, Any]:
    """Extract user_token, admin_token, refresh_token, admin_cookie, and order_template from a cURL or JWT."""
    result: dict[str, Any] = {}
    cleaned = text.strip()

    # Case 1: Raw 32-char hex refresh_token
    if re.fullmatch(r"[0-9a-f]{32}", cleaned):
        result["user_refresh_token"] = cleaned
        return result

    # Case 2: Raw JWT string
    if re.fullmatch(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", cleaned):
        info = decode_jwt_info(cleaned)
        if info.get("typ") == "supplier" or info.get("role") == "admin":
            result["admin_token"] = cleaned
            if info.get("cid"):
                result["admin_mobile"] = info["cid"]
        else:
            result["user_token"] = cleaned
            if info.get("cid"):
                result["user_mobile"] = info["cid"]
            if info.get("imei"):
                result["user_imei"] = info["imei"]
        return result

    # Case 3: cURL command
    auth_match = re.search(r"authorization:\s*Bearer\s+([A-Za-z0-9_.-]+)", cleaned, re.IGNORECASE)
    cookie_match = re.search(r"(?:-b|--cookie)\s+['\"]([^'\"]+)['\"]", cleaned)
    data_match = re.search(r"(?:--data-raw|--data|-d)\s+'(\{.*?\})'", cleaned, re.DOTALL)

    if auth_match:
        token = auth_match.group(1).strip()
        info = decode_jwt_info(token)
        if "adminv3uat.ahamove.com" in cleaned or info.get("typ") == "supplier" or info.get("role") == "admin":
            result["admin_token"] = token
            if info.get("cid"):
                result["admin_mobile"] = info["cid"]
        else:
            result["user_token"] = token
            if info.get("cid"):
                result["user_mobile"] = info["cid"]
            if info.get("imei"):
                result["user_imei"] = info["imei"]

    if cookie_match:
        cookie_str = cookie_match.group(1).strip()
        result["admin_cookie"] = cookie_str
        rt_in_cookie = re.search(r"refresh_token=([0-9a-f]{32})", cookie_str)
        if rt_in_cookie:
            result["user_refresh_token"] = rt_in_cookie.group(1)
        tok_in_cookie = re.search(r"(?:^|;\s*)token=(eyJ[A-Za-z0-9_.-]+)", cookie_str)
        if tok_in_cookie:
            u_tok = tok_in_cookie.group(1)
            u_info = decode_jwt_info(u_tok)
            if u_info.get("typ") == "user":
                result.setdefault("user_token", u_tok)
                if u_info.get("imei"):
                    result["user_imei"] = u_info["imei"]

    if data_match and "order/create" in cleaned:
        try:
            parsed_json = json.loads(data_match.group(1))
            if isinstance(parsed_json, dict) and "path" in parsed_json:
                result["order_template"] = parsed_json
        except json.JSONDecodeError:
            pass

    return result


def build_order_payload(overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build order creation payload from saved template (or default) + overrides."""
    store = load_store()
    base_tmpl = store.get("order_template") or DEFAULT_ORDER_TEMPLATE
    payload = copy.deepcopy(base_tmpl)
    if not overrides:
        return payload

    if overrides.get("service_id"):
        sid = overrides["service_id"].strip().upper()
        payload["service_id"] = sid
        req = [{"_id": "SGN-BIKE-INSURANCE"}] if sid == "SGN-BIKE" else []
        payload["requests"] = req
        payload["service"] = {"_id": sid, "requests": req}

    if overrides.get("cod") is not None:
        payload["path"][1]["cod"] = int(overrides["cod"])

    if overrides.get("total_pay") is not None:
        payload["total_pay"] = int(overrides["total_pay"])

    if "remarks" in overrides:
        payload["remarks"] = overrides["remarks"]

    return payload


def create_order(payload: dict[str, Any], timeout: int = 20) -> dict[str, Any]:
    """POST https://apiuat.ahamove.com/api/v3/private/order/create with automatic token refresh."""
    user_token = ensure_valid_user_token(force_refresh=False)
    if not user_token:
        return {
            "ok": False,
            "status_code": 0,
            "error": "Chưa có User Token hoặc Refresh Token. Hãy dán cURL tạo đơn vào nhóm hoặc DM.",
        }

    for attempt in range(2):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "authorization": f"Bearer {user_token}",
            "content-type": "application/json",
            "origin": "https://appuat.ahamove.com",
            "referer": "https://appuat.ahamove.com/",
            "user-agent": USER_AGENT,
        }
        try:
            resp = requests.post(CREATE_ORDER_URL, headers=headers, json=payload, timeout=timeout)
            if resp.status_code == 401 and attempt == 0:
                new_tok = ensure_valid_user_token(force_refresh=True)
                if new_tok and new_tok != user_token:
                    user_token = new_tok
                    continue

            try:
                body = resp.json()
            except ValueError:
                body = {"raw": resp.text}

            order_id = None
            if isinstance(body, dict):
                order_id = (
                    body.get("_id")
                    or body.get("order_id")
                    or (body.get("order") or {}).get("_id")
                    or (body.get("data") or {}).get("_id")
                )

            return {
                "ok": 200 <= resp.status_code < 300,
                "status_code": resp.status_code,
                "order_id": order_id,
                "body": body,
            }
        except requests.RequestException as exc:
            return {"ok": False, "status_code": 0, "error": str(exc)}

    return {"ok": False, "status_code": 401, "error": "Không thể làm mới User Token"}


def assign_order(order_id: str, driver_id: str, timeout: int = 20) -> dict[str, Any]:
    """PUT https://adminv3uat.ahamove.com/api/orders/{order_id}/assign/{driver_id} with automatic refresh."""
    clean_order_id = order_id.strip().upper()
    clean_driver_id = normalize_driver_id(driver_id)
    admin_token = ensure_valid_admin_token(force_refresh=False, order_id_hint=clean_order_id)
    if not admin_token:
        return {
            "ok": False,
            "status_code": 0,
            "order_id": clean_order_id,
            "driver_id": clean_driver_id,
            "error": "Chưa có Admin Token hoặc Refresh Token. Hãy dán cURL gán đơn vào nhóm hoặc DM.",
        }

    url = ASSIGN_ORDER_URL_TMPL.format(order_id=clean_order_id, driver_id=clean_driver_id)

    for attempt in range(2):
        store = load_store()
        admin_cookie = store.get("admin_cookie", "")
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "authorization": f"Bearer {admin_token}",
            "content-length": "0",
            "origin": "https://adminv3uat.ahamove.com",
            "referer": f"https://adminv3uat.ahamove.com/orders/detail/{clean_order_id}",
            "user-agent": USER_AGENT,
        }
        if admin_cookie:
            headers["cookie"] = admin_cookie

        try:
            resp = requests.put(url, headers=headers, timeout=timeout)
            if resp.status_code in (401, 403) and attempt == 0:
                new_tok = ensure_valid_admin_token(force_refresh=True, order_id_hint=clean_order_id)
                if new_tok:
                    admin_token = new_tok
                    continue

            try:
                body = resp.json()
            except ValueError:
                body = {"raw": resp.text}

            return {
                "ok": 200 <= resp.status_code < 300,
                "status_code": resp.status_code,
                "order_id": clean_order_id,
                "driver_id": clean_driver_id,
                "body": body,
            }
        except requests.RequestException as exc:
            return {
                "ok": False,
                "status_code": 0,
                "order_id": clean_order_id,
                "driver_id": clean_driver_id,
                "error": str(exc),
            }

    return {
        "ok": False,
        "status_code": 401,
        "order_id": clean_order_id,
        "driver_id": clean_driver_id,
        "error": "Không thể làm mới Admin Token",
    }
