#!/usr/bin/env python3
"""Capture SGN Ops dashboard sections and send daily Telegram report."""

import argparse
import io
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = ROOT / "Output/Ahamove/04. OPS_METRICS/dashboards/sgn_overview_dashboard.py"
OUT_DIR = ROOT / "Output/Ahamove/04. OPS_METRICS/dashboards/captures"
ENV_PATH = ROOT / ".env"
LOG_PREFIX = "[sgn-daily-report]"

SHEET_ID = "1Nbc4NYg3u8TxEh1acuWvDH-p6_8Nz8bDNF3j4bLGWvM"
SHEET_GID = "743032311"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
REPORT_YEAR = 2026
DAILY_START_COL = 5


def log(msg):
    print(f"{LOG_PREFIX} {msg}", flush=True)


def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")
    env.update({k: v for k, v in os.environ.items() if v})
    return env


def parse_value(value):
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if text in {"", "-", "nan", "None"}:
        return None
    is_percent = "%" in text
    text = text.replace(",", "").replace("%", "").strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number / 100 if is_percent else number


def safe_cell(df, row_idx, col_idx):
    if row_idx is None or col_idx is None or row_idx >= len(df.index) or col_idx >= len(df.columns):
        return ""
    return df.iat[row_idx, col_idx]


def parse_sheet_date(label):
    label = str(label).strip()
    if not label or label.lower() == "nan":
        return None
    try:
        return pd.Timestamp(datetime.strptime(f"{label}-{REPORT_YEAR}", "%d-%b-%Y").date())
    except ValueError:
        return None


def daily_columns(df):
    cols = []
    for col_idx in range(DAILY_START_COL, len(df.columns)):
        date_value = parse_sheet_date(safe_cell(df, 4, col_idx))
        if date_value is not None:
            cols.append((col_idx, date_value))
    return cols


def fmt_num(v, dec=0):
    if v is None or pd.isna(v):
        return "—"
    return f"{v:,.{dec}f}" if dec else f"{v:,.0f}"


def fmt_pct(v):
    if v is None or pd.isna(v):
        return "—"
    return f"{v:.1%}"


def delta_pct(cur, base, is_rate=False):
    if cur is None or base is None or base == 0:
        return None
    return (cur - base) if is_rate else (cur - base) / base


def delta_str(cur, base, is_rate=False):
    d = delta_pct(cur, base, is_rate)
    if d is None:
        return "—"
    arrow = "▲" if d >= 0 else "▼"
    return f"{arrow}{abs(d):.1%}"


def build_brief():
    """Refresh data source directly from Google Sheet and summarize yesterday."""
    response = requests.get(SHEET_CSV_URL, timeout=30)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text), header=None, dtype=str, keep_default_na=False)
    cols = daily_columns(df)
    if len(cols) < 3:
        raise RuntimeError("Not enough daily columns to build brief")

    col_today, date_today = cols[0]
    col_y, date_y = cols[1]
    col_dod, date_dod = cols[2]
    col_lw = col_y + 7
    date_lw = parse_sheet_date(safe_cell(df, 4, col_lw))

    def val(row, col):
        return parse_value(safe_cell(df, row, col))

    request_y = val(21, col_y)
    demand_y = val(28, col_y)
    fr_y = val(180, col_y)
    active_y = val(50, col_y)
    sh_y = val(66, col_y)
    prod_y = val(74, col_y)

    request_dod = delta_str(request_y, val(21, col_dod))
    request_wow = delta_str(request_y, val(21, col_lw))
    demand_dod = delta_str(demand_y, val(28, col_dod))
    fr_dod = delta_str(fr_y, val(180, col_dod), is_rate=True)
    active_dod = delta_str(active_y, val(50, col_dod))
    sh_dod = delta_str(sh_y, val(66, col_dod))
    prod_dod = delta_str(prod_y, val(74, col_dod))

    # Quick diagnosis rules, no fabricated target except dashboard default FR 81%.
    notes = []
    if fr_y is not None:
        notes.append("FR đạt ngưỡng 81%" if fr_y >= 0.81 else "FR dưới ngưỡng 81%, cần soi channel/segment kéo tụt")
    if request_y is not None and demand_y is not None:
        notes.append("Demand bám Request tốt" if demand_y / request_y >= 0.80 else "Demand/Request còn thấp, ưu tiên xử lý fulfillment")
    if active_y is not None and sh_y is not None:
        notes.append("Supply pool ổn định hơn hôm trước" if (delta_pct(active_y, val(50, col_dod)) or 0) >= 0 and (delta_pct(sh_y, val(66, col_dod)) or 0) >= 0 else "Theo dõi supply/online hours vì có tín hiệu giảm DoD")

    brief = (
        f"🚀 *SGN Ops Daily Pulse — {date_y.strftime('%d-%b-%Y')}*\n\n"
        f"*Tóm tắt nhanh hôm qua*\n"
        f"• Request: *{fmt_num(request_y)}* | DoD {request_dod} | WoW {request_wow}\n"
        f"• Demand: *{fmt_num(demand_y)}* | DoD {demand_dod}\n"
        f"• FR: *{fmt_pct(fr_y)}* | DoD {fr_dod}\n"
        f"• Active: *{fmt_num(active_y)}* | DoD {active_dod}\n"
        f"• Supply Hours: *{fmt_num(sh_y)}* | DoD {sh_dod}\n"
        f"• Productivity: *{fmt_num(prod_y, 1)}* | DoD {prod_dod}\n\n"
        f"*Nhận định ngắn*\n" + "\n".join(f"• {n}" for n in notes)
    )
    return brief


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_url(url, timeout=90):
    started = time.time()
    while time.time() - started < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            res = json.loads(response.read().decode())
            if not res.get("ok"):
                raise RuntimeError(res)
            return res
    except Exception:
        payload.pop("parse_mode", None)
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode())


def send_telegram_photo(token, chat_id, photo_path, caption=""):
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    boundary = "Boundary-SGN-Daily-Photo"
    file_name = Path(photo_path).name
    file_content = Path(photo_path).read_bytes()
    fields = [("chat_id", str(chat_id))]
    if caption:
        fields.append(("caption", caption[:1024]))

    body = b""
    for name, value in fields:
        body += f"--{boundary}\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode("utf-8")
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="photo"; filename="{file_name}"\r\n'.encode()
    body += b"Content-Type: image/png\r\n\r\n" + file_content + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": str(len(body))},
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        res = json.loads(response.read().decode())
        if not res.get("ok"):
            raise RuntimeError(res)
        return res


def capture_sections(url, out_dir):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Missing dependency: playwright. Install with `python3 -m pip install playwright && python3 -m playwright install chromium`.") from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    date_stamp = datetime.now().strftime("%Y%m%d-%H%M")
    images = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 2000, "height": 1400}, device_scale_factor=1)
        page.goto(url, wait_until="networkidle", timeout=90000)

        # Refresh Streamlit cache/data source before capture.
        try:
            page.get_by_role("button", name="🔄 Refresh data").click(timeout=10000)
            page.wait_for_load_state("networkidle", timeout=90000)
            page.wait_for_timeout(8000)
        except Exception as exc:
            log(f"Refresh button click skipped/failed, continuing after direct sheet refresh: {exc}")

        def screenshot_locator(locator, name, caption):
            locator.scroll_into_view_if_needed(timeout=30000)
            page.wait_for_timeout(1200)
            path = out_dir / f"{date_stamp}-{name}.png"
            locator.screenshot(path=str(path), timeout=30000)
            images.append((path, caption))

        # Executive Summary cards: from section title through monthly card row.
        exec_title = page.locator("text=Executive Summary").first
        exec_box = exec_title.bounding_box(timeout=30000)
        daily_table_title = page.locator("text=Daily Operating Cockpit").first
        next_box = daily_table_title.bounding_box(timeout=30000)
        exec_clip = {"x": 0, "y": max(0, exec_box["y"] - 10), "width": 2000, "height": max(360, next_box["y"] - exec_box["y"] - 18)}
        exec_path = out_dir / f"{date_stamp}-executive-summary.png"
        page.screenshot(path=str(exec_path), clip=exec_clip)
        images.append((exec_path, "Executive Summary — KPI Pulse"))

        # Daily cockpit table: crop left daily block only, not MTD.
        daily_title_box = daily_table_title.bounding_box(timeout=30000)
        table = page.locator("table.cockpit-table").first
        table.scroll_into_view_if_needed(timeout=30000)
        page.wait_for_timeout(1000)
        table_box = table.bounding_box(timeout=30000)
        # Label + 8 daily cols out of label + 8 daily + 5 MTD cols.
        daily_width = table_box["width"] * (9 / 14)
        daily_path = out_dir / f"{date_stamp}-daily-cockpit-daily-only.png"
        page.screenshot(
            path=str(daily_path),
            clip={"x": table_box["x"], "y": max(0, daily_title_box["y"] - 8), "width": daily_width, "height": min(980, table_box["height"] + (table_box["y"] - daily_title_box["y"]) + 12)},
        )
        images.append((daily_path, "Daily Operating Cockpit — Daily view only"))

        # FR% by User Group table.
        page.locator('[role="tab"]').filter(has_text="User Group FR").click(timeout=30000)
        page.wait_for_timeout(1500)
        fr_table = page.locator("table.fr-matrix-table").first
        screenshot_locator(fr_table, "fr-user-group", "FR% by User Group")

        # Supply tables under Active Driver Trend.
        page.locator('[role="tab"]').filter(has_text="Active Driver Trend").click(timeout=30000)
        page.wait_for_timeout(1500)
        supply_heading = page.locator("text=Supply Hours — DoD / WoW / WTD / MTD").first
        supply_table = supply_heading.locator("xpath=following::table[1]")
        screenshot_locator(supply_table, "supply-hours-detail", "Supply Hours — DoD / WoW / WTD / MTD")

        # Segment Efficiency table.
        page.locator('[role="tab"]').filter(has_text="Segment Efficiency").click(timeout=30000)
        page.wait_for_timeout(1500)
        seg_table = page.locator("text=Segment").locator("xpath=ancestor::table[1]").first
        screenshot_locator(seg_table, "segment-efficiency", "Segment Efficiency")

        browser.close()
    return images


def run_report(send=True):
    env = load_env()
    token = env.get("TELEGRAM_BOT_TOKEN")
    chat_id = env.get("TELEGRAM_CHAT_ID")
    if send and (not token or not chat_id):
        raise RuntimeError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must exist in .env or environment")

    brief = build_brief()
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    log(f"Starting Streamlit on {url}")
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(DASHBOARD_PATH),
            "--server.address",
            "127.0.0.1",
            "--server.port",
            str(port),
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env={**os.environ, **env},
        preexec_fn=os.setsid if hasattr(os, "setsid") else None,
    )
    try:
        if not wait_for_url(url, timeout=100):
            raise RuntimeError("Streamlit did not become ready in time")
        images = capture_sections(url, OUT_DIR)
        if send:
            log("Sending Telegram brief")
            send_telegram_message(token, chat_id, brief)
            for path, caption in images:
                log(f"Sending {path.name}")
                send_telegram_photo(token, chat_id, path, caption=caption)
        else:
            log("Dry run complete; not sending Telegram")
            print(brief)
            for path, caption in images:
                print(caption, path)
    finally:
        log("Stopping Streamlit")
        try:
            if hasattr(os, "killpg"):
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            else:
                proc.terminate()
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Capture images and print brief without sending Telegram")
    args = parser.parse_args()
    run_report(send=not args.dry_run)


if __name__ == "__main__":
    main()
