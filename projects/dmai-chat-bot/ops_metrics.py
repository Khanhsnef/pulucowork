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
SHEET_67888_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1gUUHLPoeY4pRnUjModVe4fYNmFwiDy_U8dWR38y78Cg/export?format=csv&gid=49583103"
)
SHEET_75557_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1gUUHLPoeY4pRnUjModVe4fYNmFwiDy_U8dWR38y78Cg/export?format=csv&gid=2043805321"
)
GITHUB_74433_URL = (
    "https://raw.githubusercontent.com/Khanhsnef/pulucowork/main/"
    "Output/Ahamove/04.%20OPS_METRICS/card_74433_63d.json"
)
GITHUB_67888_URL = (
    "https://raw.githubusercontent.com/Khanhsnef/pulucowork/main/"
    "Output/Ahamove/04.%20OPS_METRICS/card_67888_63d.json"
)
GITHUB_75557_URL = (
    "https://raw.githubusercontent.com/Khanhsnef/pulucowork/main/"
    "Output/Ahamove/04.%20OPS_METRICS/card_75557_63d.json"
)
CACHE_FILE = "/tmp/card_74433_cache.json"
CACHE_67888_FILE = "/tmp/card_67888_cache.json"
CACHE_75557_FILE = "/tmp/card_75557_cache.json"
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

    # Compact Card 67888 NW/Region KPI line
    kpi_summary = ""
    try:
        rows_67888, _ = fetch_card_67888_rows()
        if rows_67888:
            d6 = sorted({r["period"] for r in rows_67888})[-1]
            kpi_lines = []
            for reg in ("NW", "SGN", "HAN", "EXP"):
                reg_rows = [r for r in rows_67888 if r["period"] == d6 and r["region"] == reg]
                req_s = sum(r["requested"] for r in reg_rows)
                acc_s = sum(r["accept"] for r in reg_rows)
                comp_s = sum(r["completed"] for r in reg_rows)
                if req_s > 0:
                    kpi_lines.append(
                        f"• `{reg}`: Req *{req_s:,}* | Comp *{comp_s:,}* | AR *{acc_s/req_s*100:.1f}%* | FR *{comp_s/req_s*100:.1f}%*"
                    )
            if kpi_lines:
                kpi_summary = f"\n\n📦 *Card 67888 — Orders & KPI ({d6})* _(chi tiết: /kpi)_\n" + "\n".join(kpi_lines)
    except Exception:
        pass

    return (
        f"📊 *Card 74433 — Active Drivers theo Segment ({latest})*\n"
        f"_Nguồn: {source}_ | Tổng Active: *{tot_latest:,}*{dod_str}{wow_str}\n\n"
        + _format_day_table(rows, latest)
        + kpi_summary
        + "\n\n💡 *Insights nhanh*\n"
        + "\n".join(f"• {line}" for line in insights)
    )


def _to_float(v: Any) -> float:
    try:
        return float(v)
    except Exception:
        return 0.0


def fetch_card_67888_rows(force_refresh: bool = False) -> tuple[list[dict[str, Any]], str]:
    """Fetch Card 67888 rows from live Google Sheet CSV (tab 67888) or GitHub snapshot."""
    if not force_refresh and os.path.exists(CACHE_67888_FILE):
        try:
            cached = json.loads(open(CACHE_67888_FILE, encoding="utf-8").read())
            if time.time() - float(cached.get("ts", 0)) < CACHE_TTL_SEC and cached.get("rows"):
                return cached["rows"], cached.get("source", "cache")
        except Exception:
            pass

    def _norm6(r: dict[str, Any]) -> dict[str, Any]:
        return {
            "period": str(r.get("period", ""))[:10],
            "region": str(r.get("region", "")).strip(),
            "service_type": str(r.get("service_type", "")).strip(),
            "requested": _to_int(r.get("requested", 0)),
            "accept": _to_int(r.get("accept", 0)),
            "completed": _to_int(r.get("completed", 0)),
            "ar": _to_float(r.get("ar", 0)),
            "fr": _to_float(r.get("fr", 0)),
        }

    rows: list[dict[str, Any]] = []
    source = ""
    try:
        req = urllib.request.Request(SHEET_67888_CSV_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        if text and not text.lstrip().startswith("<"):
            parsed = [_norm6(r) for r in csv.DictReader(io.StringIO(text)) if r.get("period")]
            if parsed:
                rows = parsed
                source = "Google Sheet Live (67888)"
    except Exception:
        pass

    if not rows:
        req = urllib.request.Request(GITHUB_67888_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw_list = json.loads(resp.read().decode("utf-8"))
        rows = [_norm6(r) for r in raw_list if r.get("period")]
        source = "GitHub Snapshot (Card 67888)"

    if rows:
        try:
            with open(CACHE_67888_FILE, "w", encoding="utf-8") as f:
                json.dump({"ts": time.time(), "source": source, "rows": rows}, f, ensure_ascii=False)
        except Exception:
            pass
    return rows, source


def fetch_kpi_brief(force_refresh: bool = False) -> str:
    """Return formatted Card 67888 summary (Requested, Accept, Completed, AR, FR) + insights."""
    rows, source = fetch_card_67888_rows(force_refresh=force_refresh)
    if not rows:
        raise RuntimeError("Chưa có dữ liệu Card 67888.")
    dates = sorted({r["period"] for r in rows})
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None
    wow = dates[-8] if len(dates) >= 8 else None

    cur = [r for r in rows if r["period"] == latest]
    prv = [r for r in rows if r["period"] == prev] if prev else []
    wov = [r for r in rows if r["period"] == wow] if wow else []

    def agg(sub: list[dict[str, Any]]) -> tuple[int, int, int, float, float]:
        rq = sum(x["requested"] for x in sub)
        ac = sum(x["accept"] for x in sub)
        cp = sum(x["completed"] for x in sub)
        return rq, ac, cp, (ac / rq * 100 if rq else 0.0), (cp / rq * 100 if rq else 0.0)

    nw_rq, nw_ac, nw_cp, nw_ar, nw_fr = agg([r for r in cur if r["region"] == "NW"])
    p_rq, _, p_cp, _, p_fr = agg([r for r in prv if r["region"] == "NW"])
    w_rq, _, _, _, w_fr = agg([r for r in wov if r["region"] == "NW"])

    dod_rq = f" ({(nw_rq - p_rq) / p_rq * 100:+.1f}% DoD)" if p_rq else ""
    wow_rq = f" | {(nw_rq - w_rq) / w_rq * 100:+.1f}% WoW" if w_rq else ""
    dod_fr = f" ({nw_fr - p_fr:+.2f}pp DoD)" if p_rq else ""

    lines = [
        f"📦 *Card 67888 — Orders & KPI theo Service Type ({latest})*",
        f"_Nguồn: {source}_ | NW Requested: *{nw_rq:,}*{dod_rq}{wow_rq} | FR: *{nw_fr:.2f}%*{dod_fr}\n",
    ]
    for reg in ("NW", "SGN", "HAN", "EXP"):
        r_rows = [r for r in cur if r["region"] == reg]
        rq, ac, cp, ar, fr = agg(r_rows)
        if rq == 0:
            continue
        lines.append(f"*{reg}* — Req: *{rq:,}* | Acc: *{ac:,}* | Comp: *{cp:,}* | AR: *{ar:.1f}%* | FR: *{fr:.1f}%*")
        top_svc = sorted(r_rows, key=lambda x: -x["requested"])[:5]
        for s in top_svc:
            lines.append(
                f"• `{s['service_type']}`: Req {s['requested']:,}, Acc {s['accept']:,}, "
                f"Comp {s['completed']:,} | AR *{s['ar']*100:.1f}%* | FR *{s['fr']*100:.1f}%*"
            )
        lines.append("")

    # Insights
    insights = []
    if p_rq:
        insights.append(f"Nationwide (NW) đạt *{nw_cp:,}/{nw_rq:,}* đơn hoàn thành (FR *{nw_fr:.2f}%*, AR *{nw_ar:.2f}%*, {nw_fr - p_fr:+.2f}pp DoD).")
    reg_frs = []
    for reg in ("SGN", "HAN", "EXP"):
        rq, _, _, _, fr = agg([r for r in cur if r["region"] == reg])
        if rq > 0:
            reg_frs.append((fr, reg, rq))
    if reg_frs:
        reg_frs.sort()
        low_fr, low_reg, _ = reg_frs[0]
        high_fr, high_reg, _ = reg_frs[-1]
        insights.append(f"Khu vực FR cao nhất: `{high_reg}` (*{high_fr:.1f}%*) | Thấp nhất: `{low_reg}` (*{low_fr:.1f}%*).")
    nw_svcs = [r for r in cur if r["region"] == "NW" and r["requested"] >= 100]
    if nw_svcs:
        weak_svc = min(nw_svcs, key=lambda x: x["fr"])
        insights.append(
            f"Dịch vụ cần chú ý (NW >=100 req): `{weak_svc['service_type']}` có FR thấp nhất (*{weak_svc['fr']*100:.1f}%*, AR *{weak_svc['ar']*100:.1f}%*, {weak_svc['requested']:,} req)."
        )
    if w_rq:
        insights.append(f"So với tuần trước (WoW): NW Requested *{(nw_rq - w_rq) / w_rq * 100:+.1f}%*, FR *{nw_fr - w_fr:+.2f}pp*.")

    return "\n".join(lines).strip() + "\n\n💡 *Insights nhanh*\n" + "\n".join(f"• {x}" for x in insights)


def fetch_card_75557_rows(force_refresh: bool = False) -> tuple[list[dict[str, Any]], str]:
    """Fetch Card 75557 rows from live Google Sheet CSV (tab 75557) or GitHub snapshot."""
    if not force_refresh and os.path.exists(CACHE_75557_FILE):
        try:
            cached = json.loads(open(CACHE_75557_FILE, encoding="utf-8").read())
            if time.time() - float(cached.get("ts", 0)) < CACHE_TTL_SEC and cached.get("rows"):
                return cached["rows"], cached.get("source", "cache")
        except Exception:
            pass

    def _norm7(r: dict[str, Any]) -> dict[str, Any]:
        return {
            "period": str(r.get("period", ""))[:10],
            "city_id": str(r.get("city_id", "")).strip(),
            "driver_segment": str(r.get("driver_segment", "")).strip(),
            "ranking_driver": _to_int(r.get("ranking_driver", 0)),
            "total_driver": _to_int(r.get("total_driver", 0)),
            "total_stp": _to_int(r.get("total_stp", 0)),
            "order_income": _to_float(r.get("order_income", 0)),
            "reward_income": _to_float(r.get("reward_income", 0)),
            "online_hours": _to_float(r.get("online_hours", 0)),
            "busy_hours": _to_float(r.get("busy_hours", 0)),
            "accept_order": _to_int(r.get("accept_order", 0)),
            "cancel_poc": _to_int(r.get("cancel_poc", 0)),
            "accept_noti": _to_int(r.get("accept_noti", 0)),
            "total_noti": _to_int(r.get("total_noti", 0)),
            "rating_order": _to_int(r.get("rating_order", 0)),
            "rating_star": _to_int(r.get("rating_star", 0)),
            "bad_rating_order": _to_int(r.get("bad_rating_order", 0)),
            "total_aa_driver": _to_int(r.get("total_aa_driver", 0)),
            "hard_driver": _to_int(r.get("hard_driver", 0)),
            "lcd_driver": _to_int(r.get("lcd_driver", 0)),
            "gdr_driver": _to_int(r.get("gdr_driver", 0)),
        }

    rows: list[dict[str, Any]] = []
    source = ""
    try:
        req = urllib.request.Request(SHEET_75557_CSV_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        if text and not text.lstrip().startswith("<"):
            parsed = [_norm7(r) for r in csv.DictReader(io.StringIO(text)) if r.get("period")]
            if parsed:
                rows = parsed
                source = "Google Sheet Live (75557)"
    except Exception:
        pass

    if not rows:
        req = urllib.request.Request(GITHUB_75557_URL, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw_list = json.loads(resp.read().decode("utf-8"))
        rows = [_norm7(r) for r in raw_list if r.get("period")]
        source = "GitHub Snapshot (Card 75557)"

    if rows:
        try:
            with open(CACHE_75557_FILE, "w", encoding="utf-8") as f:
                json.dump({"ts": time.time(), "source": source, "rows": rows}, f, ensure_ascii=False)
        except Exception:
            pass
    return rows, source


def fetch_driver_brief(force_refresh: bool = False) -> str:
    """Return formatted Card 75557 summary (Driver Income, EPH, PPH, Util, AA, CR POC) + insights."""
    rows, source = fetch_card_75557_rows(force_refresh=force_refresh)
    if not rows:
        raise RuntimeError("Chưa có dữ liệu Card 75557.")
    dates = sorted({r["period"] for r in rows})
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None
    cur = [r for r in rows if r["period"] == latest]
    prv = [r for r in rows if r["period"] == prev] if prev else []

    def agg(sub: list[dict[str, Any]]) -> dict[str, float]:
        drv = sum(x["total_driver"] for x in sub)
        stp = sum(x["total_stp"] for x in sub)
        inc = sum(x["order_income"] + x["reward_income"] for x in sub)
        rew = sum(x["reward_income"] for x in sub)
        onl = sum(x["online_hours"] for x in sub)
        bsy = sum(x["busy_hours"] for x in sub)
        aa = sum(x["total_aa_driver"] for x in sub)
        acc = sum(x["accept_order"] for x in sub)
        cpoc = sum(x["cancel_poc"] for x in sub)
        anoti = sum(x["accept_noti"] for x in sub)
        tnoti = sum(x["total_noti"] for x in sub)
        return {
            "drv": drv,
            "inc_per_drv": inc / drv if drv else 0.0,
            "eph": inc / onl if onl else 0.0,
            "pph": stp / onl if onl else 0.0,
            "util": bsy / onl * 100 if onl else 0.0,
            "aa_pct": aa / drv * 100 if drv else 0.0,
            "cr_poc": cpoc / acc * 100 if acc else 0.0,
            "ar_noti": anoti / tnoti * 100 if tnoti else 0.0,
            "rew_pct": rew / inc * 100 if inc else 0.0,
        }

    tot = agg(cur)
    tot_p = agg(prv) if prv else {}
    inc_dod = f" ({(tot['inc_per_drv'] - tot_p['inc_per_drv']) / tot_p['inc_per_drv'] * 100:+.1f}% DoD)" if tot_p.get("inc_per_drv") else ""

    lines = [
        f"🛵 *Card 75557 — Driver Income & Efficiency ({latest})*",
        f"_Nguồn: {source}_ | TB Thu nhập/TX: *{tot['inc_per_drv']/1000:,.0f}k*{inc_dod} | EPH: *{tot['eph']/1000:,.1f}k* | PPH: *{tot['pph']:.2f}*\n",
    ]
    for city in ("SGN", "HAN", "EXP"):
        c_rows = sorted([r for r in cur if r["city_id"] == city], key=lambda x: -x["total_driver"])
        if not c_rows:
            continue
        ca = agg(c_rows)
        lines.append(
            f"*{city}* — TX: *{int(ca['drv']):,}* | TB/TX: *{ca['inc_per_drv']/1000:,.0f}k* | "
            f"EPH: *{ca['eph']/1000:,.1f}k* | PPH: *{ca['pph']:.2f}* | Util: *{ca['util']:.1f}%* | AA: *{ca['aa_pct']:.1f}%*"
        )
        for r in c_rows:
            sa = agg([r])
            lines.append(
                f"• `{r['driver_segment']}`: {r['total_driver']:,} TX | {sa['inc_per_drv']/1000:,.0f}k/TX | "
                f"EPH {sa['eph']/1000:,.1f}k | PPH {sa['pph']:.2f} | AA {sa['aa_pct']:.0f}% | CR {sa['cr_poc']:.1f}%"
            )
        lines.append("")

    insights = [
        f"Toàn quốc: Utilization *{tot['util']:.1f}%*, Auto-Accept *{tot['aa_pct']:.1f}%*, AR Noti *{tot['ar_noti']:.1f}%*, CR POC *{tot['cr_poc']:.2f}%*.",
        f"Tỷ trọng thưởng chiếm *{tot['rew_pct']:.2f}%* tổng thu nhập tài xế.",
    ]
    high_cr = [r for r in cur if r["accept_order"] >= 200]
    if high_cr:
        worst = max(high_cr, key=lambda x: x["cancel_poc"] / x["accept_order"])
        insights.append(
            f"Segment CR POC cao nhất: `{worst['city_id']}-{worst['driver_segment']}` "
            f"(*{worst['cancel_poc']/worst['accept_order']*100:.1f}%*, {worst['cancel_poc']:,} đơn hủy)."
        )

    return "\n".join(lines).strip() + "\n\n💡 *Insights nhanh*\n" + "\n".join(f"• {x}" for x in insights)


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
        day_r = [x for x in rows if x["order_date"] == dt]
        tot_all = sum(x["total_active"] for x in day_r)
        city_sums = " | ".join(
            f"{c}={sum(x['total_active'] for x in day_r if x['city_id'] == c):,}"
            for c in ("SGN", "HAN", "EXP")
        )
        parts.append(f"--- CHI TIẾT NGÀY {dt} (TỔNG ACTIVE TOÀN QUỐC={tot_all:,} | {city_sums}) ---")
        for r in sorted(day_r, key=lambda x: (x["city_id"], x["tag"])):
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

    # Monthly trend (Card 74433)
    months = sorted({r["month"] for r in rows if r["month"]})
    parts.append("--- TREND THÁNG CARD 74433 (TB ngày theo tháng/city/tag) ---")
    for m in months:
        m_rows = [r for r in rows if r["month"] == m]
        n_days = len({r["order_date"] for r in m_rows}) or 1
        by_ct = {}
        for r in m_rows:
            k = (r["city_id"], r["tag"])
            by_ct[k] = by_ct.get(k, 0) + r["total_active"]
        summary = ", ".join(f"{c}-{t}:{v//n_days}/ng" for (c, t), v in sorted(by_ct.items()))
        parts.append(f"Tháng {m[:7]} ({n_days} ngày): {summary}")

    # Card 67888 context (Requested, Accept, Completed, AR, FR by region & service_type)
    try:
        rows_67888, src_67888 = fetch_card_67888_rows()
        if rows_67888:
            d6_list = sorted({r["period"] for r in rows_67888})
            t_dates6 = _extract_requested_dates(user_message, d6_list) or (d6_list[-2:] if len(d6_list) >= 2 else d6_list[-1:])
            parts.append(f"\n=== CARD 67888 ({src_67888}: {d6_list[0]} -> {d6_list[-1]}) ===")
            for dt in t_dates6:
                parts.append(f"--- CHI TIẾT ĐƠN/KPI NGÀY {dt} ---")
                for r in sorted([x for x in rows_67888 if x["period"] == dt], key=lambda x: (x["region"], -x["requested"])):
                    parts.append(
                        f"{r['region']} | {r['service_type']} | req={r['requested']} acc={r['accept']} "
                        f"comp={r['completed']} | AR={r['ar']*100:.2f}% FR={r['fr']*100:.2f}%"
                    )
            # Monthly & last-7-days region summary
            parts.append("--- TỔNG HỢP 7 NGÀY GẦN NHẤT & THEO THÁNG (CARD 67888) ---")
            for label, cond in [("7d gần nhất", set(d6_list[-7:])), ("Tháng 11", {d for d in d6_list if d.startswith("2026-11")}), ("Tháng 10", {d for d in d6_list if d.startswith("2026-10")})]:
                sub_all = [r for r in rows_67888 if r["period"] in cond]
                if not sub_all:
                    continue
                reg_parts = []
                for reg in ("NW", "SGN", "HAN", "EXP"):
                    sr = [r for r in sub_all if r["region"] == reg]
                    rq = sum(x["requested"] for x in sr)
                    ac = sum(x["accept"] for x in sr)
                    cp = sum(x["completed"] for x in sr)
                    if rq:
                        reg_parts.append(f"{reg}(req={rq:,},acc={ac:,},comp={cp:,},AR={ac/rq*100:.1f}%,FR={cp/rq*100:.1f}%)")
                if reg_parts:
                    parts.append(f"{label}: " + " | ".join(reg_parts))
    except Exception as exc:
        print(f"⚠️ Card 67888 context error: {exc}")

    # Card 75557 context (Driver Income, EPH, PPH, Util, AA, CR POC, Rating)
    try:
        rows_75557, src_75557 = fetch_card_75557_rows()
        if rows_75557:
            d7_list = sorted({r["period"] for r in rows_75557})
            t_dates7 = _extract_requested_dates(user_message, d7_list) or (d7_list[-2:] if len(d7_list) >= 2 else d7_list[-1:])
            parts.append(f"\n=== CARD 75557 ({src_75557}: {d7_list[0]} -> {d7_list[-1]}) ===")
            for dt in t_dates7:
                d7_rows = [x for x in rows_75557 if x["period"] == dt]
                tot7_all = sum(x["total_driver"] for x in d7_rows)
                c7_sums = " | ".join(
                    f"{c}={sum(x['total_driver'] for x in d7_rows if x['city_id'] == c):,}"
                    for c in ("SGN", "HAN", "EXP")
                )
                parts.append(f"--- DRIVER INCOME & QUALITY NGÀY {dt} (TỔNG TX={tot7_all:,} | {c7_sums}) ---")
                for r in sorted(d7_rows, key=lambda x: (x["city_id"], x["driver_segment"])):
                    inc = r["order_income"] + r["reward_income"]
                    drv = r["total_driver"] or 1
                    onl = r["online_hours"] or 1
                    acc = r["accept_order"] or 1
                    tnoti = r["total_noti"] or 1
                    rord = r["rating_order"] or 1
                    parts.append(
                        f"{r['city_id']} | {r['driver_segment']} | rank_drv={r['ranking_driver']} active={r['total_driver']} "
                        f"hard={r['hard_driver']} aa={r['total_aa_driver']} lcd={r['lcd_driver']} gdr={r['gdr_driver']} | "
                        f"inc/drv={inc/drv:,.0f} rew={r['reward_income']:,.0f} EPH={inc/onl:,.0f} PPH={r['total_stp']/onl:.2f} "
                        f"Util={r['busy_hours']/onl*100:.1f}% AR_noti={r['accept_noti']/tnoti*100:.1f}% "
                        f"CR_poc={r['cancel_poc']/acc*100:.2f}% Rating={r['rating_star']/rord:.2f}"
                    )
    except Exception as exc:
        print(f"⚠️ Card 75557 context error: {exc}")

    return "\n".join(parts)
