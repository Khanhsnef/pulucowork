"""Card 74433 (Driver Active by Segment/Tag & Service) fetcher & analyzer for @DMAIChat_Bot."""

import csv
import datetime
import io
import json
import os
import re
import time
import urllib.request
from typing import Any

METABASE_EXPORT_URL = "https://ws.ahamove.com/ops/trigger/export_to_gs"
SHEET_74433_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1BniOS6rJHulyyCLJb13jkc3UWuSRZBraLEmJI6xFNG0/export?format=csv&gid=2008886787"
)
GITHUB_74433_URL = (
    "https://raw.githubusercontent.com/Khanhsnef/pulucowork/main/"
    "Output/Ahamove/04.%20OPS_METRICS/card_74433_63d.json"
)
CACHE_FILE = "/tmp/card_74433_cache.json"
CACHE_TTL_SEC = 300
SERVICE_COLS = [
    "total_active", "active_1h", "active_2h", "active_4h",
    "bike", "eco", "aibot", "pool", "aifood", "TMDT", "_2H", "_2HBULKY", "INDAY", "_1HTMDT",
]


def _to_int(v: Any) -> int:
    try:
        return int(float(str(v).replace(",", "").strip()))
    except Exception:
        return 0


def _normalize_row(raw: dict[str, Any]) -> dict[str, Any]:
    row = {
        "city_id": str(raw.get("city_id", "")).strip(),
        "month": str(raw.get("month", ""))[:10],
        "week": str(raw.get("week", ""))[:10],
        "order_date": str(raw.get("order_date", ""))[:10],
        "tag": str(raw.get("tag", "")).strip(),
    }
    for col in SERVICE_COLS:
        row[col] = _to_int(raw.get(col, 0))
    return row


def trigger_metabase_refresh() -> tuple[bool, str]:
    """Trigger Metabase Card 74433 export to Google Sheets."""
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=63)).strftime("%Y-%m-%d")
    payload = {
        "email": "khanhlp@ahamove.com",
        "card_id": 74433,
        "source": "metabase",
        "filter": {"start_date": start_date, "end_date": end_date},
        "spreadsheet_url": (
            "https://docs.google.com/spreadsheets/d/"
            "1BniOS6rJHulyyCLJb13jkc3UWuSRZBraLEmJI6xFNG0/edit?gid=2008886787#gid=2008886787"
        ),
    }
    req = urllib.request.Request(
        METABASE_EXPORT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "DMAIChat_Bot/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return resp.status in (200, 201, 202, 204), resp.read().decode("utf-8", errors="ignore")[:200]
    except Exception as exc:
        return False, str(exc)


def fetch_card_74433_rows(force_refresh: bool = False) -> tuple[list[dict[str, Any]], str]:
    """Fetch Card 74433 rows from live Google Sheet CSV (if public) or GitHub JSON snapshot."""
    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            cached = json.loads(open(CACHE_FILE, encoding="utf-8").read())
            if time.time() - float(cached.get("ts", 0)) < CACHE_TTL_SEC and cached.get("rows"):
                return cached["rows"], cached.get("source", "cache")
        except Exception:
            pass

    rows: list[dict[str, Any]] = []
    source = ""

    # 1. Try live Google Sheet CSV (works if sheet is shared "Anyone with the link -> Viewer")
    try:
        req = urllib.request.Request(SHEET_74433_CSV_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        if text and not text.lstrip().startswith("<"):
            reader = csv.DictReader(io.StringIO(text))
            parsed = [_normalize_row(r) for r in reader if r.get("order_date")]
            if parsed:
                rows = parsed
                source = "Google Sheet Live"
    except Exception:
        pass

    # 2. Fallback to GitHub snapshot (fast <200ms)
    if not rows:
        req = urllib.request.Request(GITHUB_74433_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw_list = json.loads(resp.read().decode("utf-8"))
        rows = [_normalize_row(r) for r in raw_list if r.get("order_date")]
        source = "GitHub Snapshot (Card 74433)"

    if rows:
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"ts": time.time(), "source": source, "rows": rows}, f, ensure_ascii=False)
        except Exception:
            pass
    return rows, source


def _format_day_table(rows: list[dict[str, Any]], target_date: str) -> str:
    day_rows = [r for r in rows if r["order_date"] == target_date]
    if not day_rows:
        return f"Không có dữ liệu cho ngày `{target_date}`."
    day_rows.sort(key=lambda r: (r["city_id"], -r["total_active"]))
    lines = []
    cur_city = None
    for r in day_rows:
        if r["city_id"] != cur_city:
            cur_city = r["city_id"]
            city_sum = sum(x["total_active"] for x in day_rows if x["city_id"] == cur_city)
            lines.append(f"\n*{cur_city}* (Tổng active: *{city_sum:,}*)")
        lines.append(
            f"• `{r['tag']}`: *{r['total_active']:,}* "
            f"(bike {r['bike']:,}, eco {r['eco']:,}, pool {r['pool']:,}, "
            f"food {r['aifood']:,}, 2H {r['_2H']:,}, bulky {r['_2HBULKY']:,}, tmdt {r['TMDT']:,})"
        )
    return "\n".join(lines).strip()


def fetch_ops_brief(force_refresh: bool = False) -> str:
    """Return formatted Card 74433 summary for the latest available date."""
    rows, source = fetch_card_74433_rows(force_refresh=force_refresh)
    if not rows:
        raise RuntimeError("Chưa có dữ liệu Card 74433.")
    dates = sorted({r["order_date"] for r in rows})
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None

    tot_latest = sum(r["total_active"] for r in rows if r["order_date"] == latest)
    dod_str = ""
    if prev:
        tot_prev = sum(r["total_active"] for r in rows if r["order_date"] == prev)
        if tot_prev > 0:
            pct = (tot_latest - tot_prev) / tot_prev * 100
            dod_str = f" | DoD {'+' if pct >= 0 else ''}{pct:.1f}%"

    return (
        f"📊 *Card 74433 — Active Drivers theo Segment ({latest})*\n"
        f"_Nguồn: {source} | Tổng Active: *{tot_latest:,}*{dod_str}_\n\n"
        + _format_day_table(rows, latest)
    )


def _extract_requested_dates(text: str, available_dates: list[str]) -> list[str]:
    found: list[str] = []
    for m in re.findall(r"(20\d{2}-\d{2}-\d{2})", text):
        if m in available_dates and m not in found:
            found.append(m)
    for d_m in re.findall(r"\b(\d{1,2})[/-](\d{1,2})(?:[/-](20\d{2}))?\b", text):
        dd, mm, yyyy = int(d_m[0]), int(d_m[1]), d_m[2] or "2026"
        cand = f"{yyyy}-{mm:02d}-{dd:02d}"
        if cand in available_dates and cand not in found:
            found.append(cand)
    return found


def build_query_context(user_message: str) -> str:
    """Build compact Card 74433 context (specific day, latest day, weekly & monthly trends) for AI."""
    rows, source = fetch_card_74433_rows()
    if not rows:
        return ""

    dates = sorted({r["order_date"] for r in rows})
    target_dates = _extract_requested_dates(user_message, dates)
    if not target_dates:
        target_dates = dates[-2:] if len(dates) >= 2 else dates[-1:]

    parts = [f"Nguồn: {source} | Khoảng dữ liệu: {dates[0]} đến {dates[-1]} (945 dòng)"]

    for dt in target_dates:
        parts.append(f"--- CHI TIẾT NGÀY {dt} ---")
        for r in sorted([x for x in rows if x["order_date"] == dt], key=lambda x: (x["city_id"], x["tag"])):
            parts.append(
                f"{r['city_id']} | {r['tag']} | total={r['total_active']} | "
                f"1h={r['active_1h']} 2h={r['active_2h']} 4h={r['active_4h']} | "
                f"bike={r['bike']} eco={r['eco']} aibot={r['aibot']} pool={r['pool']} "
                f"aifood={r['aifood']} TMDT={r['TMDT']} 2H={r['_2H']} 2HBULKY={r['_2HBULKY']} "
                f"INDAY={r['INDAY']} 1HTMDT={r['_1HTMDT']}"
            )

    # Weekly trend (average daily active per week by city & tag)
    weeks = sorted({r["week"] for r in rows if r["week"]})[-6:]
    parts.append("--- TREND TUẦN (Tổng & TB ngày theo tuần/city/tag, 6 tuần gần nhất) ---")
    for w in weeks:
        w_rows = [r for r in rows if r["week"] == w]
        n_days = len({r["order_date"] for r in w_rows}) or 1
        by_ct: dict[tuple[str, str], int] = {}
        for r in w_rows:
            k = (r["city_id"], r["tag"])
            by_ct[k] = by_ct.get(k, 0) + r["total_active"]
        summary = ", ".join(f"{c}-{t}:{v//n_days}/ng" for (c, t), v in sorted(by_ct.items()))
        parts.append(f"Tuần {w} ({n_days} ngày): {summary}")

    # Monthly trend
    months = sorted({r["month"] for r in rows if r["month"]})
    parts.append("--- TREND THÁNG (TB ngày theo tháng/city/tag) ---")
    for m in months:
        m_rows = [r for r in rows if r["month"] == m]
        n_days = len({r["order_date"] for r in m_rows}) or 1
        by_ct = {}
        for r in m_rows:
            k = (r["city_id"], r["tag"])
            by_ct[k] = by_ct.get(k, 0) + r["total_active"]
        summary = ", ".join(f"{c}-{t}:{v//n_days}/ng" for (c, t), v in sorted(by_ct.items()))
        parts.append(f"Tháng {m[:7]} ({n_days} ngày): {summary}")

    return "\n".join(parts)
