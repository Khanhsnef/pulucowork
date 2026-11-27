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
    "1gUUHLPoeY4pRnUjModVe4fYNmFwiDy_U8dWR38y78Cg/export?format=csv&gid=0"
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
            "1gUUHLPoeY4pRnUjModVe4fYNmFwiDy_U8dWR38y78Cg/edit?gid=0#gid=0"
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


def _build_insights(rows: list[dict[str, Any]], dates: list[str]) -> list[str]:
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None
    wow_date = dates[-8] if len(dates) >= 8 else None

    cur_rows = [r for r in rows if r["order_date"] == latest]
    prev_rows = [r for r in rows if r["order_date"] == prev] if prev else []
    wow_rows = [r for r in rows if r["order_date"] == wow_date] if wow_date else []

    tot_cur = sum(r["total_active"] for r in cur_rows) or 1
    insights: list[str] = []

    # 1. City DoD & WoW movers
    city_parts = []
    for city in ("SGN", "HAN", "EXP"):
        c_cur = sum(r["total_active"] for r in cur_rows if r["city_id"] == city)
        c_prev = sum(r["total_active"] for r in prev_rows if r["city_id"] == city)
        c_wow = sum(r["total_active"] for r in wow_rows if r["city_id"] == city)
        dod = f"{((c_cur - c_prev) / c_prev * 100):+.1f}%" if c_prev else "N/A"
        wow = f"{((c_cur - c_wow) / c_wow * 100):+.1f}%" if c_wow else "N/A"
        city_parts.append(f"{city} (DoD {dod}, WoW {wow})")
    insights.append("Biến động khu vực: " + " | ".join(city_parts) + ".")

    # 2. Segment mix (Core FT+PT vs Return vs New NIM+NLM)
    ft_pt = sum(r["total_active"] for r in cur_rows if r["tag"] in ("FT", "PT"))
    ret_cur = sum(r["total_active"] for r in cur_rows if r["tag"] == "return")
    ret_prev = sum(r["total_active"] for r in prev_rows if r["tag"] == "return")
    new_cur = sum(r["total_active"] for r in cur_rows if r["tag"] in ("NIM", "NLM"))
    ret_dod = f" ({((ret_cur - ret_prev) / ret_prev * 100):+.1f}% DoD)" if ret_prev else ""
    insights.append(
        f"Cơ cấu lực lượng: Core `FT+PT` chiếm *{ft_pt / tot_cur * 100:.1f}%* ({ft_pt:,} TX), "
        f"`return` đạt *{ret_cur:,}*{ret_dod}, tài xế mới (`NIM+NLM`) đạt *{new_cur:,}* ({new_cur / tot_cur * 100:.1f}%)."
    )

    # 3. Alert on sharpest DoD drop or service highlight
    if prev_rows:
        drops = []
        for city in ("SGN", "HAN", "EXP"):
            for tag in ("FT", "PT", "return", "NIM", "NLM"):
                v1 = sum(r["total_active"] for r in cur_rows if r["city_id"] == city and r["tag"] == tag)
                v0 = sum(r["total_active"] for r in prev_rows if r["city_id"] == city and r["tag"] == tag)
                if v0 >= 50:
                    pct = (v1 - v0) / v0 * 100
                    drops.append((pct, city, tag, v1 - v0))
        drops.sort()
        if drops and drops[0][0] <= -3.0:
            p, c, t, diff = drops[0]
            insights.append(f"Điểm cần chú ý: `{c}-{t}` giảm mạnh nhất (*{p:.1f}%*, {diff:+,} TX so với hôm trước).")
        else:
            insights.append("Ổn định: Không có segment lớn nào giảm sâu (>3%) so với hôm trước.")

    return insights


def fetch_ops_brief(force_refresh: bool = False) -> str:
    """Return formatted Card 74433 summary + insights for the latest available date."""
    rows, source = fetch_card_74433_rows(force_refresh=force_refresh)
    if not rows:
        raise RuntimeError("Chưa có dữ liệu Card 74433.")
    dates = sorted({r["order_date"] for r in rows})
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None
    wow_date = dates[-8] if len(dates) >= 8 else None

    tot_latest = sum(r["total_active"] for r in rows if r["order_date"] == latest)
    dod_str = ""
    if prev:
        tot_prev = sum(r["total_active"] for r in rows if r["order_date"] == prev)
        if tot_prev > 0:
            pct = (tot_latest - tot_prev) / tot_prev * 100
            dod_str = f" | DoD {'+' if pct >= 0 else ''}{pct:.1f}%"
    wow_str = ""
    if wow_date:
        tot_wow = sum(r["total_active"] for r in rows if r["order_date"] == wow_date)
        if tot_wow > 0:
            pct_w = (tot_latest - tot_wow) / tot_wow * 100
            wow_str = f" | WoW {'+' if pct_w >= 0 else ''}{pct_w:.1f}%"

    insights = _build_insights(rows, dates)

    return (
        f"📊 *Card 74433 — Active Drivers theo Segment ({latest})*\n"
        f"_Nguồn: {source}_ | Tổng Active: *{tot_latest:,}*{dod_str}{wow_str}\n\n"
        + _format_day_table(rows, latest)
        + "\n\n💡 *Insights nhanh*\n"
        + "\n".join(f"• {line}" for line in insights)
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
