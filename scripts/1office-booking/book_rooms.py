#!/usr/bin/env python3
"""
1Office Room Booking - Auto Weekly
Chạy lúc 16:00:01 Thứ 6 -> book 2 phòng NANGA & 1 phòng DENALI cho Thứ 2 & Thứ 6 tuần sau
"""

import os
import sys
import time
import logging
from datetime import datetime, timedelta, timezone
from oneoffice_client import OneOfficeClient

ICT = timezone(timedelta(hours=7))

# Tự động tạo thư mục log phù hợp trên macOS hoặc Linux (GitHub Actions)
log_dir = os.path.expanduser("~/Library/Logs") if sys.platform == "darwin" else os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "1office-booking.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger(__name__)

MEETINGS = [
    {
        "title": "[Supply] Weekly Meeting",
        "room": "NANGA",
        "time_start": "14:02",
        "time_end": "15:59",
        "day": "monday",
    },
    {
        "title": "[DM] Catchup",
        "room": "NANGA",
        "time_start": "16:02",
        "time_end": "16:59",
        "day": "monday",
    },
    {
        "title": "[DM] Catchup",
        "room": "DENALI",
        "time_start": "16:02",
        "time_end": "18:00",
        "day": "friday",
    },
]

DAY_MAP = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}

def next_weekday(day: str) -> str:
    """Tính ngày weekday kế tiếp (tuần sau), VD: 'monday', 'friday' theo giờ ICT."""
    target = DAY_MAP[day]
    today = datetime.now(ICT)
    days = (target - today.weekday()) % 7 or 7
    return (today + timedelta(days=days)).strftime("%d/%m/%Y")


def main():
    # Chờ tới đúng 16:00:01 (ICT) (Bỏ qua nếu SKIP_SLEEP=1)
    if not os.getenv("SKIP_SLEEP"):
        now = datetime.now(ICT)
        target = now.replace(hour=16, minute=0, second=1, microsecond=0)
        wait_seconds = (target - now).total_seconds()
        if wait_seconds > 0:
            log.info(f"Hiện tại: {now.strftime('%H:%M:%S')} (ICT). Đang chờ {wait_seconds:.1f}s để tới đúng 16:00:01...")
            time.sleep(wait_seconds)
        else:
            log.info(f"Hiện tại: {now.strftime('%H:%M:%S')} (ICT) (đã quá 16:00:01), thực thi ngay lập tức.")

    log.info("=== 1Office Auto Booking Starting ===")
    client = OneOfficeClient()

    results = []
    for meeting in MEETINGS:
        date = next_weekday(meeting["day"])
        res = client.book_room(
            title=meeting["title"],
            room_name_or_id=meeting["room"],
            date=date,
            time_start=meeting["time_start"],
            time_end=meeting["time_end"],
        )
        ok = res["success"]
        results.append((meeting, date, ok))

    success = sum(1 for _, _, ok in results if ok)
    total = len(results)

    if success == total:
        lines = "\n".join(
            f"{m['title']} ({m['room']}) {m['time_start']}-{m['time_end']} ({d})" for m, d, _ in results
        )
        client.notify(
            title="1Office: Đã book phòng họp thành công",
            message=lines,
            is_error=False,
        )
        log.info(f"=== Done: {success}/{total} OK ===")
        sys.exit(0)
    else:
        failed = [m["title"] for m, _, ok in results if not ok]
        client.notify(
            title="1Office: Đặt phòng THẤT BẠI",
            message=f"Chỉ đặt được {success}/{total} phòng.\nPhòng lỗi: {', '.join(failed)}",
            is_error=True
        )
        log.error(f"=== Done: {success}/{total} OK | FAIL: {failed} ===")
        sys.exit(1)


if __name__ == "__main__":
    main()
