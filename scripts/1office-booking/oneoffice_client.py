#!/usr/bin/env python3
"""
1Office Client & Auto-Auth Engine
Hệ thống kết nối, quản lý session và thao tác với 1Office API (ahamove.1office.vn).
"""

import os
import sys
import re
import json
import logging
import subprocess
import tempfile
import shutil
import sqlite3
import requests
from typing import Dict, Any, Optional
from datetime import datetime

log = logging.getLogger("oneoffice_client")

ROOM_MAP = {
    "NANGA": "27",
    "DENALI": "25",
}
ROOM_NAME_MAP = {v: k for k, v in ROOM_MAP.items()}

class OneOfficeClient:
    def __init__(self, base_url: str = "https://ahamove.1office.vn"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "origin": self.base_url,
            "referer": f"{self.base_url}/apps/calendar-room-room",
            "csrf-token-cache": "d16209c822ad99e34c8f404b394881ec",
        }
        
        self.cookies = {
            "PHPSESSID": "",
            "1office_b9777422e8d99fa2f9b85195e1d2733881519d5duid": "",
            "1office_b9777422e8d99fa2f9b85195e1d2733881519d5dlanguage": "K7ZHBWKEw-7qUKPOT09C7rG5JiFL8rnWi3XWnIiAGGVqmhiD2A",
            "1office_b9777422e8d99fa2f9b85195e1d2733881519d5devent_time": "Sqxq0jedfHt-0ggwMMR0AlnxS9VuoJswDuOIg5BwVeNiYFqz-iyvq8lJF0iowA",
            "_ga": "GA1.1.182590307.1751616266",
        }
        self.username = None
        self.password = None
        self.env_file = os.path.join(os.path.dirname(__file__), ".env.1office")
        self._load_env()

    def _extract_chrome_cookies(self) -> Dict[str, str]:
        """Tự động trích xuất và giải mã cookies 1Office từ Chrome trên macOS nếu có."""
        if sys.platform != "darwin":
            return {}
        try:
            from Crypto.Cipher import AES
            from Crypto.Protocol.KDF import PBKDF2
            
            pw_out = subprocess.check_output(
                ["security", "find-generic-password", "-s", "Chrome Safe Storage", "-w"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            key = PBKDF2(pw_out.encode("utf-8"), b"saltysalt", 16, 1003)
            
            cookie_file = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cookies")
            if not os.path.exists(cookie_file):
                return {}
                
            tmp = tempfile.mktemp()
            shutil.copy2(cookie_file, tmp)
            conn = sqlite3.connect(tmp)
            cursor = conn.cursor()
            cursor.execute("SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%1office.vn%'")
            res = {}
            for name, enc_val in cursor.fetchall():
                if enc_val.startswith(b"v10"):
                    cipher = AES.new(key, AES.MODE_CBC, IV=b" "*16)
                    decrypted = cipher.decrypt(enc_val[3:])
                    pad_len = decrypted[-1]
                    decrypted = decrypted[:-pad_len]
                    val = decrypted[32:].decode("utf-8", errors="ignore")
                    res[name] = val
            conn.close()
            if os.path.exists(tmp):
                os.remove(tmp)
            return res
        except Exception as e:
            log.warning(f"Không thể trích xuất cookie tự động từ Chrome: {e}")
            return {}

    def _load_env(self):
        """Tải cấu hình từ file .env.1office nếu có."""
        if os.path.exists(self.env_file):
            with open(self.env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip()
                        if k == "BASE_URL" and v:
                            self.base_url = v
                        elif k == "ONE_OFFICE_USERNAME" and v:
                            self.username = v
                        elif k == "ONE_OFFICE_PASSWORD" and v:
                            self.password = v
                        elif k == "PHPSESSID" and v:
                            self.cookies["PHPSESSID"] = v
                        elif k == "ONE_OFFICE_UID" and v:
                            self.cookies["1office_b9777422e8d99fa2f9b85195e1d2733881519d5duid"] = v
                        elif k == "ONE_OFFICE_REMEMBER" and v:
                            self.cookies["1office_b9777422e8d99fa2f9b85195e1d2733881519d5dremember"] = v
                        elif k == "ONE_OFFICE_EVENT_TIME" and v:
                            self.cookies["1office_b9777422e8d99fa2f9b85195e1d2733881519d5devent_time"] = v
                        elif k == "ONE_OFFICE_LANGUAGE" and v:
                            self.cookies["1office_b9777422e8d99fa2f9b85195e1d2733881519d5dlanguage"] = v
                        elif k == "CSRF_TOKEN" and v:
                            self.headers["csrf-token-cache"] = v

        # Đọc trực tiếp từ Environment Variables (ưu tiên cho GitHub Actions / Cloud)
        self.username = os.getenv("ONE_OFFICE_USERNAME") or self.username
        self.password = os.getenv("ONE_OFFICE_PASSWORD") or self.password
        if os.getenv("PHPSESSID"):
            self.cookies["PHPSESSID"] = os.getenv("PHPSESSID")
        if os.getenv("ONE_OFFICE_REMEMBER"):
            self.cookies["1office_b9777422e8d99fa2f9b85195e1d2733881519d5dremember"] = os.getenv("ONE_OFFICE_REMEMBER")
        if os.getenv("CSRF_TOKEN"):
            self.headers["csrf-token-cache"] = os.getenv("CSRF_TOKEN")
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        # Nếu chưa có telegram token, thử đọc từ file .env gốc của workspace
        if not self.telegram_token or not self.telegram_chat_id:
            root_env = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
            if os.path.exists(root_env):
                with open(root_env, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("TELEGRAM_BOT_TOKEN=") and not self.telegram_token:
                            self.telegram_token = line.split("=", 1)[1].strip("\"' ")
                        elif line.startswith("TELEGRAM_CHAT_ID=") and not self.telegram_chat_id:
                            self.telegram_chat_id = line.split("=", 1)[1].strip("\"' ")

    def _save_env_cookies(self):
        """Lưu tự động các Cookie mới thu thập được vào file .env.1office."""
        if not os.path.exists(self.env_file):
            return
        
        lines = []
        with open(self.env_file, "r") as f:
            lines = f.readlines()

        new_lines = []
        phpsessid_val = self.cookies.get("PHPSESSID", "")
        uid_key = "1office_b9777422e8d99fa2f9b85195e1d2733881519d5duid"
        uid_val = self.cookies.get(uid_key, "")
        remember_key = "1office_b9777422e8d99fa2f9b85195e1d2733881519d5dremember"
        remember_val = self.cookies.get(remember_key, "")
        csrf_val = self.headers.get("csrf-token-cache", "")

        phpsessid_updated = False
        remember_updated = False
        csrf_updated = False

        for line in lines:
            if line.startswith("PHPSESSID="):
                new_lines.append(f"PHPSESSID={phpsessid_val}\n")
                phpsessid_updated = True
            elif line.startswith("ONE_OFFICE_REMEMBER="):
                new_lines.append(f"ONE_OFFICE_REMEMBER={remember_val}\n")
                remember_updated = True
            elif line.startswith("CSRF_TOKEN="):
                new_lines.append(f"CSRF_TOKEN={csrf_val}\n")
                csrf_updated = True
            else:
                new_lines.append(line)

        if not phpsessid_updated:
            new_lines.append(f"PHPSESSID={phpsessid_val}\n")
        if not remember_updated and remember_val:
            new_lines.append(f"ONE_OFFICE_REMEMBER={remember_val}\n")
        if not csrf_updated and csrf_val:
            new_lines.append(f"CSRF_TOKEN={csrf_val}\n")

        with open(self.env_file, "w") as f:
            f.writelines(new_lines)
        log.info("Đã cập nhật Cookie mới vào .env.1office")

    def send_telegram(self, message: str) -> bool:
        """Gửi thông báo về Telegram bot nếu có cấu hình."""
        if not self.telegram_token or not self.telegram_chat_id:
            return False
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200 and resp.json().get("ok"):
                log.info("Đã gửi thông báo Telegram thành công.")
                return True
            else:
                log.warning(f"Gửi Telegram thất bại: {resp.text}")
                return False
        except Exception as e:
            log.warning(f"Lỗi gửi Telegram: {e}")
            return False

    def notify(self, title: str, message: str, is_error: bool = False):
        """Hiển thị thông báo macOS Desktop Notification và gửi thông báo Telegram."""
        # 1. Gửi Telegram về điện thoại (hoạt động cả khi chạy trên GitHub Actions hoặc tắt máy Mac)
        icon = "❌" if is_error else "✅"
        tg_text = f"{icon} <b>{title}</b>\n\n{message}"
        self.send_telegram(tg_text)

        # 2. Desktop Notification nếu đang chạy trên macOS
        if sys.platform != "darwin":
            return
        sound = "Basso" if is_error else "Glass"
        subtitle = "FAILED - Cần kiểm tra" if is_error else "Thành công"
        clean_msg = message.replace('"', '\\"')
        script = f'display notification "{clean_msg}" with title "{title}" subtitle "{subtitle}" sound name "{sound}"'
        try:
            subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
        except Exception as e:
            log.warning(f"Notification error: {e}")

    def check_session(self, auto_reauth: bool = True) -> Dict[str, Any]:
        """Kiểm tra Session Cookie 1Office hiện tại có khả dụng hay không."""
        test_url = f"{self.base_url}/apps/calendar-room-room"
        try:
            resp = self.session.get(test_url, headers=self.headers, cookies=self.cookies, timeout=10, allow_redirects=True)
            
            # Kiểm tra nếu bị redirect về trang login hoặc thiếu app.layout
            is_login_page = "/login" in resp.url or "app.layout" not in resp.text
            
            if resp.status_code == 200 and not is_login_page:
                # Trích xuất CSRF Token mới nhất từ trang
                csrf_match = re.search(r'CSRF_TOKEN_CACHE\s*=\s*["\']([a-f0-9]+)["\']', resp.text)
                if csrf_match:
                    self.headers["csrf-token-cache"] = csrf_match.group(1)
                
                # Trích xuất thông tin người dùng
                user_name = "User"
                layout_match = re.search(r"<elem name='app\.layout' data-props='([^']+)'", resp.text)
                if layout_match:
                    try:
                        import html as pyhtml
                        props = json.loads(pyhtml.unescape(layout_match.group(1)))
                        user_name = props.get("username") or user_name
                    except Exception:
                        pass

                return {
                    "valid": True,
                    "reason": f"Session hợp lệ (Tài khoản: {user_name})",
                    "user": user_name,
                    "csrf_token": self.headers.get("csrf-token-cache")
                }

            # Nếu session không hợp lệ, thử fallback lấy cookie từ Chrome trên macOS
            if auto_reauth:
                log.info("Session hiện tại không hợp lệ. Đang kiểm tra phiên đăng nhập từ Chrome...")
                chrome_cookies = self._extract_chrome_cookies()
                if chrome_cookies and "PHPSESSID" in chrome_cookies:
                    for k, v in chrome_cookies.items():
                        self.cookies[k] = v
                    self._save_env_cookies()
                    log.info("Đã cập nhật session từ Chrome! Thử lại...")
                    return self.check_session(auto_reauth=False)

            return {"valid": False, "reason": "Session hết hạn hoặc chưa đăng nhập"}
        except Exception as e:
            return {"valid": False, "reason": f"Lỗi kết nối: {str(e)}"}

    def book_room(self, title: str, room_name_or_id: str, date: str, time_start: str, time_end: str) -> Dict[str, Any]:
        """
        Thực hiện đặt phòng họp trên 1Office.
        """
        room_id = ROOM_MAP.get(room_name_or_id.upper(), room_name_or_id)
        room_name = ROOM_NAME_MAP.get(room_id, room_id)
        
        payload = {
            "meeting_link": "", "object": "", "modify_remind": "1",
            "title": title,
            "calendar_id": "other", "format": "CA_BOTH",
            "time_start": time_start, "date_start": date,
            "time_end": time_end, "date_end": date,
            "meeting_type": "", "total_participate": "",
            "details[0][key]": "ROOM", "details[0][value]": room_id,
            "desc": "", "repeat_interval": "1", "repeat_type": "NONE",
            "repeat_end_type": "FOREVER", "external_emails": "",
            "reminds[1][amount]": "10", "reminds[1][unit]": "MINUTE",
            "reminds[1][by][]": "notify", "inlineLogin": "1",
        }

        try:
            url = f"{self.base_url}/apps/calendar-room-room/add?_json=1"
            resp = self.session.post(url, data=payload, headers=self.headers, cookies=self.cookies, timeout=15)
            result = resp.json()

            if result.get("error_login"):
                log.warning("Session hết hạn khi gọi API đặt phòng. Thử cập nhật từ Chrome...")
                chrome_cookies = self._extract_chrome_cookies()
                if chrome_cookies:
                    for k, v in chrome_cookies.items():
                        self.cookies[k] = v
                    self._save_env_cookies()
                    resp = self.session.post(url, data=payload, headers=self.headers, cookies=self.cookies, timeout=15)
                    result = resp.json()
                else:
                    msg = "Session hết hạn - Vui lòng đăng nhập lại 1Office trên Chrome"
                    log.error(f"FAIL: {msg}")
                    self.notify(title="1Office: Session hết hạn", message=msg, is_error=True)
                    return {"success": False, "error": "error_login", "message": msg}

            notice_str = str(result.get("notice") or "").lower()
            if "thành công" in notice_str or result.get("status") == 1:
                log.info(f"OK: {title} | Phòng {room_name} ({date} {time_start}-{time_end})")
                return {"success": True, "notice": result.get("notice"), "room": room_name, "date": date}

            msg = result.get("notice") or result.get("message") or str(result.get("error")) or str(result)
            
            # Idempotent: Nếu phòng đã được bạn đặt trước đó -> xem như thành công
            lower_msg = msg.lower()
            if "trùng thời gian" in lower_msg and any(name in lower_msg for name in ["khoa", "ngô huỳnh khoa", "khanh", "lê phương khanh"]):
                log.info(f"OK (Đã được đặt trước đó): {title} | Phòng {room_name} ({date} {time_start}-{time_end})")
                return {"success": True, "notice": "Đã được bạn đặt trước đó", "room": room_name, "date": date}

            log.error(f"FAIL: {title} | {msg}")
            self.notify(title=f"1Office FAIL: {title}", message=f"{date} {time_start}-{time_end}\n{msg}", is_error=True)
            return {"success": False, "message": msg}

        except Exception as e:
            msg = str(e)[:120]
            log.error(f"Lỗi khi đặt phòng: {msg}")
            self.notify(title=f"1Office FAIL: {title}", message=f"Lỗi: {msg}", is_error=True)
            return {"success": False, "message": msg}
