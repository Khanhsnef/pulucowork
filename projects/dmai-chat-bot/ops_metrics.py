"""Pure-stdlib SGN Ops daily metrics fetcher & Metabase refresh trigger for @DMAIChat_Bot."""

import csv
import datetime
import io
import json
import os
import time
import urllib.request
from typing import Any

SHEET_ID = "1Nbc4NYg3u8TxEh1acuWvDH-p6_8Nz8bDNF3j4bLGWvM"
SHEET_GID = "743032311"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"
GITHUB_PULSE_URL = "https://raw.githubusercontent.com/Khanhsnef/pulucowork/main/Output/Ahamove/04.%20OPS_METRICS/latest_ops_pulse.md"
METABASE_EXPORT_URL = "https://ws.ahamove.com/ops/trigger/export_to_gs"
REPORT_YEAR = 2026
DAILY_START_COL = 5
CACHE_FILE = "/tmp/sgn_ops_brief_cache.json"
CACHE_TTL_SEC = 300


def _parse_value(value: Any) -> float | None:
    if value is None:
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
    return number / 100.0 if is_percent else number


def _safe_cell(rows: list[list[str]], row_idx: int, col_idx: int) -> str:
    if row_idx < len(rows) and col_idx < len(rows[row_idx]):
        return rows[row_idx][col_idx]
    return ""


def _parse_sheet_date(label: str) -> datetime.datetime | None:
    text = str(label or "").strip()
    if not text or text in {"-", "nan", "None"}:
        return None
    for fmt in ("%d-%b-%Y", "%d-%b"):
        try:
            dt = datetime.datetime.strptime(text, fmt)
            return dt.replace(year=REPORT_YEAR) if fmt == "%d-%b" else dt
        except ValueError:
            continue
    return None


def _fmt_num(v: float | None, dec: int = 0) -> str:
    if v is None:
        return "N/A"
    return f"{v:,.0f}" if dec == 0 else f"{v:,.{dec}f}"


def _fmt_pct(v: float | None) -> str:
    return "N/A" if v is None else f"{v * 100:.2f}%"


def _delta_pct(cur: float | None, base: float | None) -> float | None:
    if cur is None or base in (None, 0):
        return None
    return (cur - base) / abs(base)


def _delta_str(cur: float | None, base: float | None, is_rate: bool = False) -> str:
    if cur is None or base is None:
        return "N/A"
    if is_rate:
        diff_pp = (cur - base) * 100
        return f"{'+' if diff_pp >= 0 else ''}{diff_pp:.2f}pp"
    pct = _delta_pct(cur, base)
    if pct is None:
        return "N/A"
    return f"{'+' if pct >= 0 else ''}{pct * 100:.1f}%"


def trigger_metabase_refresh() -> tuple[bool, str]:
    """Trigger Metabase export to Google Sheets."""
    req = urllib.request.Request(
        METABASE_EXPORT_URL,
        data=json.dumps({}).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "DMAIChat_Bot/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            return resp.status == 200, body[:200]
    except Exception as exc:
        return False, str(exc)


def fetch_ops_brief(force_refresh: bool = False) -> str:
    """Fetch latest SGN Ops Pulse from GitHub snapshot (fast <200ms) with 5-min /tmp cache."""
    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            cached = json.loads(open(CACHE_FILE, encoding="utf-8").read())
            if time.time() - float(cached.get("ts", 0)) < CACHE_TTL_SEC and cached.get("brief"):
                return cached["brief"]
        except Exception:
            pass

    req = urllib.request.Request(GITHUB_PULSE_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        brief = resp.read().decode("utf-8", errors="replace").strip()
    if not brief:
        raise RuntimeError("Chưa có dữ liệu Ops Pulse trên GitHub.")
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "brief": brief}, f, ensure_ascii=False)
    except Exception:
        pass
    return brief


def build_ops_brief_from_sheet() -> str:
    """Fetch heavy SGN Ops Google Sheet CSV (120s timeout, for GitHub Actions) and build brief."""
    req = urllib.request.Request(SHEET_CSV_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        csv_text = resp.read().decode("utf-8", errors="replace")

    rows = list(csv.reader(io.StringIO(csv_text)))
    if len(rows) <= 180:
        raise RuntimeError("Dữ liệu Google Sheet chưa đầy đủ.")

    cols: list[tuple[int, datetime.datetime]] = []
    max_cols = len(rows[4]) if len(rows) > 4 else 0
    for c in range(DAILY_START_COL, max_cols):
        dt = _parse_sheet_date(_safe_cell(rows, 4, c))
        if dt:
            cols.append((c, dt))

    if len(cols) < 3:
        raise RuntimeError("Không đủ cột ngày để tổng hợp chỉ số.")

    _, _ = cols[0]
    col_y, date_y = cols[1]
    col_dod, _ = cols[2]
    col_lw = col_y + 7

    def val(row: int, col: int) -> float | None:
        return _parse_value(_safe_cell(rows, row, col))

    request_y = val(21, col_y)
    demand_y = val(28, col_y)
    fr_y = val(180, col_y)
    active_y = val(50, col_y)
    sh_y = val(66, col_y)
    prod_y = val(74, col_y)

    request_dod = _delta_str(request_y, val(21, col_dod))
    request_wow = _delta_str(request_y, val(21, col_lw))
    demand_dod = _delta_str(demand_y, val(28, col_dod))
    fr_dod = _delta_str(fr_y, val(180, col_dod), is_rate=True)
    active_dod = _delta_str(active_y, val(50, col_dod))
    sh_dod = _delta_str(sh_y, val(66, col_dod))
    prod_dod = _delta_str(prod_y, val(74, col_dod))

    notes = []
    if fr_y is not None:
        notes.append("FR đạt ngưỡng 81%" if fr_y >= 0.81 else "FR dưới ngưỡng 81%, cần soi channel/segment kéo tụt")
    if request_y is not None and demand_y is not None and request_y > 0:
        notes.append("Demand bám Request tốt" if demand_y / request_y >= 0.80 else "Demand/Request còn thấp, ưu tiên xử lý fulfillment")
    if active_y is not None and sh_y is not None:
        d_act = _delta_pct(active_y, val(50, col_dod)) or 0
        d_sh = _delta_pct(sh_y, val(66, col_dod)) or 0
        notes.append(
            "Supply pool ổn định hơn hôm trước"
            if d_act >= 0 and d_sh >= 0
            else "Theo dõi supply/online hours vì có tín hiệu giảm DoD"
        )

    brief = (
        f"🚀 *SGN Ops Daily Pulse — {date_y.strftime('%d-%b-%Y')}*\n\n"
        f"*Tóm tắt nhanh hôm qua*\n"
        f"• Request: *{_fmt_num(request_y)}* | DoD {request_dod} | WoW {request_wow}\n"
        f"• Demand: *{_fmt_num(demand_y)}* | DoD {demand_dod}\n"
        f"• FR: *{_fmt_pct(fr_y)}* | DoD {fr_dod}\n"
        f"• Active: *{_fmt_num(active_y)}* | DoD {active_dod}\n"
        f"• Supply Hours: *{_fmt_num(sh_y)}* | DoD {sh_dod}\n"
        f"• Productivity: *{_fmt_num(prod_y, 1)}* | DoD {prod_dod}\n\n"
        f"*Nhận định ngắn*\n" + "\n".join(f"• {n}" for n in notes)
    )
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "brief": brief}, f, ensure_ascii=False)
    except Exception:
        pass
    return brief
