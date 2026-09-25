#!/usr/bin/env python3
"""
Automated GitHub Dispatcher for 1Office Booking
Tự động kích hoạt GitHub Actions workflow lúc 15:59:45 ICT Thứ 6 hàng tuần và giám sát kết quả chạy.
"""

import os
import sys
import time
import shutil
import subprocess
import logging
import json
from datetime import datetime, timedelta, timezone

ICT = timezone(timedelta(hours=7))
REPO = "Khanhsnef/pulucowork"
WORKFLOW = "auto_book_1office.yml"

# Tìm binary gh
GH_BIN = shutil.which("gh")
if not GH_BIN:
    for candidate in [
        "/Users/ts-1148/.local/bin/gh",
        "/opt/homebrew/bin/gh",
        "/usr/local/bin/gh",
    ]:
        if os.path.exists(candidate):
            GH_BIN = candidate
            break
GH_BIN = GH_BIN or "gh"

ENV = os.environ.copy()
ENV["PATH"] = f"/Users/ts-1148/.local/bin:/opt/homebrew/bin:/usr/local/bin:{ENV.get('PATH', '')}"

# Cấu hình log
log_dir = os.path.expanduser("~/Library/Logs") if sys.platform == "darwin" else os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "1office-booking.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("github_dispatcher")

def notify(title: str, message: str, is_error: bool = False):
    if sys.platform != "darwin":
        return
    sound = "Basso" if is_error else "Glass"
    subtitle = "FAILED" if is_error else "Thành công"
    script = f'display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "{sound}"'
    try:
        subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
    except Exception:
        pass

def main():
    now_ict = datetime.now(ICT)
    # Kích hoạt trước 16:00:01 đúng 16 giây (15:59:45) để GitHub Actions kịp spin-up runner
    target_ict = now_ict.replace(hour=15, minute=59, second=45, microsecond=0)
    wait_seconds = (target_ict - now_ict).total_seconds()

    if wait_seconds > 0:
        log.info(f"Đang chờ {wait_seconds:.1f}s (~{wait_seconds/60:.1f} phút) tới 15:59:45 ICT để tự động kích hoạt GitHub Actions...")
        time.sleep(wait_seconds)
    else:
        log.info("Thời gian hiện tại đã tới/quá 15:59:45 ICT, kích hoạt GitHub Actions ngay lập tức.")

    log.info(f">>> Đang kích hoạt GitHub Actions workflow: {WORKFLOW} ({REPO})...")
    trigger_cmd = [GH_BIN, "workflow", "run", WORKFLOW, "-R", REPO]
    res = subprocess.run(trigger_cmd, capture_output=True, text=True, env=ENV)
    
    if res.returncode != 0:
        log.error(f"Lỗi khi kích hoạt GitHub Actions: {res.stderr}")
        log.info("Chuyển sang fallback chạy cục bộ ngay lập tức...")
        fallback_cmd = ["python3", "/Users/ts-1148/.1office-booking/book_rooms.py"]
        subprocess.run(fallback_cmd, env=ENV)
        return

    log.info("✅ Đã kích hoạt GitHub Actions workflow thành công!")
    notify("1Office Booking", "Đã kích hoạt GitHub Actions workflow lúc 15:59:45 ICT", is_error=False)

    # Chờ 15s để GitHub tạo run và runner boot up
    time.sleep(15)

    # Lấy run ID mới nhất
    try:
        list_cmd = [GH_BIN, "run", "list", "--workflow", WORKFLOW, "-R", REPO, "-L", "1", "--json", "databaseId,url,status"]
        run_res = subprocess.run(list_cmd, capture_output=True, text=True, env=ENV)
        runs = json.loads(run_res.stdout)
        if runs:
            run_id = str(runs[0]["databaseId"])
            run_url = runs[0]["url"]
            log.info(f"Đang theo dõi GitHub Run #{run_id}: {run_url}")
            
            # Chờ run hoàn thành
            watch_cmd = [GH_BIN, "run", "watch", run_id, "-R", REPO]
            subprocess.run(watch_cmd, env=ENV)

            # Kiểm tra trạng thái cuối cùng
            view_cmd = [GH_BIN, "run", "view", run_id, "-R", REPO, "--json", "conclusion"]
            view_res = subprocess.run(view_cmd, capture_output=True, text=True, env=ENV)
            conclusion = json.loads(view_res.stdout).get("conclusion")
            
            if conclusion == "success":
                log.info(f"🎉 GitHub Actions #{run_id} hoàn tất THÀNH CÔNG!")
                notify("1Office Booking", f"GitHub Actions đã book phòng thành công lúc 16:00:01!\nRun URL: {run_url}", is_error=False)
            else:
                log.error(f"❌ GitHub Actions #{run_id} kết thúc với trạng thái: {conclusion}")
                notify("1Office Booking FAILED", f"GitHub Actions thất bại ({conclusion}). Kích hoạt book cục bộ...", is_error=True)
                fallback_cmd = ["python3", "/Users/ts-1148/.1office-booking/book_rooms.py"]
                subprocess.run(fallback_cmd, env=ENV)
    except Exception as e:
        log.warning(f"Lỗi khi theo dõi GitHub run: {e}")

if __name__ == "__main__":
    main()
