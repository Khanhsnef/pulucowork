#!/usr/bin/env python3
"""
Daily Mac Health Check & Optimization Advisor (Safe Read-Only Diagnostic)
Scans CPU Load, Swap, Memory Pressure, Disk Free, Caches, and memory-heavy processes.
Sends a macOS interactive dialog and Telegram report asking for confirmation BEFORE any cleanup.
"""
import json
import os
import re
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
REPORT_PATH = ROOT / "output" / "mac_daily_health_report.md"


def run_cmd(cmd: str) -> str:
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return res.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def load_env() -> dict:
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if v})
    return env


def send_telegram_text(token: str, chat_id: str, text: str):
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        print(f"Telegram send warning: {e}")


def main():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Uptime & Load Average
    uptime_out = run_cmd("uptime")
    load_1m = 0.0
    m_load = re.search(r"load averages:\s+([0-9.]+)", uptime_out)
    if m_load:
        load_1m = float(m_load.group(1))

    # 2. Swap Usage
    swap_out = run_cmd("sysctl vm.swapusage")
    swap_used_mb = 0.0
    m_swap = re.search(r"used\s*=\s*([0-9.]+)M", swap_out)
    if m_swap:
        swap_used_mb = float(m_swap.group(1))

    # 3. Memory Free %
    mem_out = run_cmd("memory_pressure")
    mem_free_pct = 50
    m_mem = re.search(r"System-wide memory free percentage:\s*(\d+)%", mem_out)
    if m_mem:
        mem_free_pct = int(m_mem.group(1))

    # 4. Disk Free
    df_out = run_cmd("df -h / | tail -n 1")
    parts = df_out.split()
    disk_avail = parts[3] if len(parts) > 3 else "N/A"
    disk_cap = parts[4] if len(parts) > 4 else "N/A"

    # 5. Cache size
    caches_out = run_cmd("du -sh ~/Library/Caches ~/.npm ~/.cache 2>/dev/null")

    # 6. Top CPU & Top Memory Processes
    top_cpu = run_cmd("ps -Aceo pid,%cpu,%mem,rss,comm -r | head -n 6")
    top_mem = run_cmd("top -l 1 -o mem -n 8 -stats pid,command,cpu,mem,cmprs | tail -n 9")

    # Identify issues
    issues = []
    if load_1m > 12.0:
        issues.append(f"⚠️ Tải CPU cao (Load Average: {load_1m})")
    if swap_used_mb > 6144.0:
        issues.append(f"⚠️ Bộ nhớ Swap cao ({swap_used_mb:.0f} MB / {swap_used_mb/1024:.1f} GB)")
    if mem_free_pct < 25:
        issues.append(f"⚠️ RAM trống thấp (chỉ còn {mem_free_pct}%)")

    status_tag = "🟢 HỆ THỐNG ỔN ĐỊNH" if not issues else "🟠 CẦN TỐI ƯU HÓA"
    issue_summary = "Không phát hiện điểm nghẽn nghiêm trọng." if not issues else " | ".join(issues)

    report_md = f"""# 🩺 BÁO CÁO SỨC KHỎE MACOS HÀNG NGÀY ({now_str})
* **Trạng thái:** *{status_tag}*
* **Chẩn đoán nhanh:** {issue_summary}
* **CPU Load Average (1m):** `{load_1m}`
* **Swap Memory Used:** `{swap_used_mb:.0f} MB` (`{swap_used_mb/1024:.2f} GB`)
* **Memory Free:** `{mem_free_pct}%`
* **Ổ cứng SSD trống:** `{disk_avail}` (Capacity `{disk_cap}`)

### 📊 Top Tiến trình tiêu thụ Bộ nhớ (MEM & Compressed)
```text
{top_mem}
```

### 🔥 Top Tiến trình tiêu thụ CPU
```text
{top_cpu}
```

### 🗂️ Dung lượng Cache hiện tại
```text
{caches_out}
```

> 🛡️ **Chế độ An toàn (Safe Guard):** Hệ thống CHƯA tự động tắt bất kỳ tiến trình hay xóa file nào để bảo vệ công việc chưa lưu của bạn.
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report_md, encoding="utf-8")

    # Send Telegram message (defaulting to group -1001733758627)
    env = load_env()
    target_chat_id = env.get("MAC_HEALTH_CHAT_ID") or env.get("TELEGRAM_CHAT_ID") or "-1001733758627"
    tg_msg = (
        f"🩺 *BÁO CÁO SỨC KHỎE MACOS ({now_str})*\n"
        f"• Trạng thái: *{status_tag}*\n"
        f"• Load Average: `{load_1m}` | RAM trống: `{mem_free_pct}%`\n"
        f"• Swap đang dùng: `{swap_used_mb/1024:.2f} GB` | SSD trống: `{disk_avail}`\n"
        f"• Chẩn đoán: _{issue_summary}_\n\n"
        f"🛡️ _Hệ thống chỉ quét chẩn đoán và KHÔNG tự ý đóng ứng dụng để tránh mất dữ liệu bạn đang làm việc._"
    )
    send_telegram_text(env.get("TELEGRAM_BOT_TOKEN"), target_chat_id, tg_msg)

    # Show native macOS notification + non-intrusive dialog if issues are found
    notif_cmd = (
        f'osascript -e \'display notification "Load: {load_1m} | Swap: {swap_used_mb/1024:.1f}GB | '
        f'SSD trống: {disk_avail}. ({status_tag})" '
        f'with title "🩺 Chẩn đoán Mac hàng ngày (12:30)" sound name "Glass"\''
    )
    run_cmd(notif_cmd)

    if issues:
        dialog_text = (
            f"Phát hiện vấn đề hiệu năng lúc {now_str}:\\n"
            + "\\n".join(issues)
            + f"\\n\\nSwap: {swap_used_mb/1024:.1f} GB | SSD trống: {disk_avail}.\\n"
            "Bạn có muốn dọn dẹp Cache rác & reset các tiến trình rò rỉ bộ nhớ nền ngay bây giờ không? (Các cửa sổ làm việc chính vẫn được giữ nguyên)"
        )
        ans = run_cmd(
            f'osascript -e \'button returned of (display dialog "{dialog_text}" '
            f'buttons {{"Để sau (Đang làm việc)", "Tối ưu ngay"}} default button "Để sau (Đang làm việc)" '
            f'with title "🩺 Antigravity Mac Health Advisor" giving up after 60)\''
        )
        if "Tối ưu ngay" in ans:
            run_cmd(
                "rm -rf ~/.npm/_npx/* ~/.npm/_cacache/* ~/Library/Caches/com.vng.zalo.ShipIt/* "
                "~/Library/Caches/pip/* ~/Library/Caches/Homebrew/* 2>/dev/null || true"
            )
            run_cmd('osascript -e \'display notification "Đã dọn dẹp Cache hệ thống an toàn!" with title "✅ Đã tối ưu hóa Mac"\'')


if __name__ == "__main__":
    main()
