#!/usr/bin/env python3
"""
1Office Client & Auto-Auth Engine
Hệ thống kết nối, quản lý session và thao tác với 1Office API (ahamove.1office.vn).
"""

import os
import sys
import logging
import subprocess
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
            "csrf-token-cache": "d4ad167fe49c02a584fa481bdb2d5b57",
        }
        
        self.cookies = {
            "PHPSESSID": "gahs920e058hktvccf5le0e8q3",
            "1office_b9777422e8d99fa2f9b85195e1d2733881519d5duid": "",
            "1office_b9777422e8d99fa2f9b85195e1d2733881519d5dlanguage": "TDI0NXk5Ulo2VEdG",
            "1office_b9777422e8d99fa2f9b85195e1d2733881519d5devent_time": "TDI0Nndjd050aVNHRzFNcGJIRFZIR2dK",
            "_ga": "GA1.1.182590307.1751616266",
        }
        self.username = None
        self.password = None
        self.env_file = os.path.join(os.path.dirname(__file__), ".env.1office")
        self._load_env()

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
                        elif k == "CSRF_TOKEN" and v:
                            self.headers["csrf-token-cache"] = v

        # Đọc trực tiếp từ Environment Variables (ưu tiên cho GitHub Actions / Cloud)
        self.username = os.getenv("ONE_OFFICE_USERNAME") or self.username
        self.password = os.getenv("ONE_OFFICE_PASSWORD") or self.password

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

        phpsessid_updated = False
        uid_updated = False

        for line in lines:
            if line.startswith("PHPSESSID="):
                new_lines.append(f"PHPSESSID={phpsessid_val}\n")
                phpsessid_updated = True
            elif line.startswith("ONE_OFFICE_UID="):
                new_lines.append(f"ONE_OFFICE_UID={uid_val}\n")
                uid_updated = True
            else:
                new_lines.append(line)

        if not phpsessid_updated:
            new_lines.append(f"PHPSESSID={phpsessid_val}\n")
        if not uid_updated:
            new_lines.append(f"ONE_OFFICE_UID={uid_val}\n")

        with open(self.env_file, "w") as f:
            f.writelines(new_lines)
        log.info("Đã cập nhật Cookie mới vào .env.1office")

    def notify(self, title: str, message: str, is_error: bool = False):
        """Hiển thị thông báo macOS Desktop Notification."""
        if sys.platform != "darwin":
            return
        sound = "Basso" if is_error else "Glass"
        subtitle = "FAILED - Cần kiểm tra" if is_error else "Thành công"
        script = f'display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "{sound}"'
        try:
            subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
        except Exception as e:
            log.warning(f"Notification error: {e}")

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Thực hiện đăng nhập lại 1Office để cập nhật Session Cookie."""
        uname = username or self.username
        passwd = password or self.password
        
        if not uname or not passwd:
            log.error("Không có thông tin tài khoản đăng nhập (ONE_OFFICE_USERNAME / ONE_OFFICE_PASSWORD).")
            return False
            
        login_url = f"{self.base_url}/login"
        data = {
            "username": uname,
            "userpwd": passwd,
            "url_login": "",
            "lang": "vi",
            "persistent": "1"
        }
        
        try:
            resp = self.session.post(login_url, data=data, timeout=15)
            if resp.status_code == 200 and "error_login" not in resp.text:
                for k, v in resp.cookies.get_dict().items():
                    self.cookies[k] = v
                self._save_env_cookies()
                log.info("Đăng nhập 1Office thành công! Cập nhật Session Cookie mới.")
                return True
            else:
                log.error("Đăng nhập 1Office thất bại. Kiểm tra lại username/password.")
                return False
        except Exception as e:
            log.error(f"Lỗi kết nối khi đăng nhập 1Office: {e}")
            return False

    def check_session(self, auto_reauth: bool = True) -> Dict[str, Any]:
        """Kiểm tra Session Cookie 1Office hiện tại có khả dụng hay không."""
        test_url = f"{self.base_url}/apps/calendar-room-room?_json=1"
        try:
            resp = self.session.get(test_url, headers=self.headers, cookies=self.cookies, timeout=10)
            if resp.status_code == 200:
                try:
                    res = resp.json()
                    if res.get("error_login"):
                        if auto_reauth and self.username and self.password:
                            log.info("Session hết hạn, tự động đăng nhập lại...")
                            if self.login():
                                return self.check_session(auto_reauth=False)
                        return {"valid": False, "reason": "Session hết hạn (error_login)"}
                    return {"valid": True, "reason": "Session hợp lệ", "data": res}
                except Exception:
                    if "/login" in resp.url or "login" in resp.text.lower():
                        if auto_reauth and self.username and self.password:
                            log.info("Session hết hạn (redirect login), tự động đăng nhập lại...")
                            if self.login():
                                return self.check_session(auto_reauth=False)
                        return {"valid": False, "reason": "Redirect tới login page"}
                    return {"valid": True, "reason": "Session trả về 200"}
            return {"valid": False, "reason": f"HTTP status {resp.status_code}"}
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
                log.warning("Session hết hạn khi gọi API đặt phòng. Thử tự động đăng nhập lại...")
                if self.login():
                    resp = self.session.post(url, data=payload, headers=self.headers, cookies=self.cookies, timeout=15)
                    result = resp.json()
                else:
                    msg = "Session hết hạn - Vui lòng kiểm tra lại thông tin đăng nhập"
                    log.error(f"FAIL: {msg}")
                    self.notify(title="1Office: Session hết hạn", message=msg, is_error=True)
                    return {"success": False, "error": "error_login", "message": msg}

            notice_str = str(result.get("notice") or "").lower()
            if "thành công" in notice_str or result.get("status") == 1:
                log.info(f"OK: {title} | Phòng {room_name} ({date} {time_start}-{time_end})")
                return {"success": True, "notice": result.get("notice"), "room": room_name, "date": date}

            msg = result.get("notice") or result.get("message") or str(result.get("error")) or str(result)
            log.error(f"FAIL: {title} | {msg}")
            self.notify(title=f"1Office FAIL: {title}", message=f"{date} {time_start}-{time_end}\n{msg}", is_error=True)
            return {"success": False, "message": msg}

        except Exception as e:
            msg = str(e)[:120]
            log.error(f"Lỗi khi đặt phòng: {msg}")
            self.notify(title=f"1Office FAIL: {title}", message=f"Lỗi: {msg}", is_error=True)
            return {"success": False, "message": msg}
