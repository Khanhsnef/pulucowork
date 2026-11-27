"""Multi-sheet Operations & Driver Analytics Engine for @DMAIChat_Bot.

Reads all metrics from Card 74433 (Supply by Segment/Service), Card 67888 (Demand/AR/FR),
Card 75557 (Driver Income/EPH/PPH/Utilization/Quality/LCD/GDR), plus auto-discovers any
new tabs added to the Google Sheet, producing executive reports with DoD/WoW/7d deltas
and cross-sheet diagnostic insights.
"""

from concurrent.futures import ThreadPoolExecutor
import csv
import datetime
import html as html_lib
import io
import json
import os
import re
import time
import urllib.request
from typing import Any

SPREADSHEET_ID = "1gUUHLPoeY4pRnUjModVe4fYNmFwiDy_U8dWR38y78Cg"
METABASE_EXPORT_URL = "https://ws.ahamove.com/ops/trigger/export_to_gs"

SHEET_74433_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=0"
SHEET_67888_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=49583103"
SHEET_75557_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid=2043805321"
SHEET_HTMLVIEW_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/htmlview"

GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/Khanhsnef/pulucowork/main/"
    "Output/Ahamove/04.%20OPS_METRICS"
)
GITHUB_74433_URL = f"{GITHUB_RAW_BASE}/card_74433_63d.json"
GITHUB_67888_URL = f"{GITHUB_RAW_BASE}/card_67888_63d.json"
GITHUB_75557_URL = f"{GITHUB_RAW_BASE}/card_75557_63d.json"

CACHE_74433_FILE = "/tmp/card_74433_cache_v2.json"
CACHE_67888_FILE = "/tmp/card_67888_cache_v2.json"
CACHE_75557_FILE = "/tmp/card_75557_cache_v2.json"
CACHE_EXTRA_FILE = "/tmp/card_extra_tabs_cache.json"
CACHE_TTL_SEC = 300

KNOWN_GIDS = {"0", "49583103", "2043805321"}

SERVICE_COLS_74433 = [
    "total_active", "active_1h", "active_2h", "active_4h",
    "bike", "eco", "aibot", "pool", "aifood", "TMDT", "_2H", "_2HBULKY", "INDAY", "_1HTMDT",
]


def _to_int(v: Any) -> int:
    try:
        s = str(v).replace(",", "").strip()
        return int(float(s)) if s and s.lower() not in ("none", "nan", "-") else 0
    except Exception:
        return 0


def _to_float(v: Any) -> float:
    try:
        s = str(v).replace(",", "").replace("%", "").strip()
        return float(s) if s and s.lower() not in ("none", "nan", "-") else 0.0
    except Exception:
        return 0.0


def _pct_delta(cur: float, base: float, digits: int = 1) -> str:
    if not base:
        return "N/A"
    pct = (cur - base) / abs(base) * 100.0
    arrow = "▲" if pct > 0.05 else ("▼" if pct < -0.05 else "▬")
    return f"{arrow}{pct:+.{digits}f}%"


def _pp_delta(cur_pct: float, base_pct: float, digits: int = 2) -> str:
    if base_pct is None:
        return "N/A"
    diff = cur_pct - base_pct
    arrow = "▲" if diff > 0.02 else ("▼" if diff < -0.02 else "▬")
    return f"{arrow}{diff:+.{digits}f}pp"


def _esc(text: Any) -> str:
    return html_lib.escape(str(text))


# ── METABASE REFRESH (ALL 3 CARDS) ────────────────────────────────────────────
def trigger_metabase_refresh() -> tuple[bool, str]:
    """Trigger Metabase export for all configured cards (74433, 67888, 75557) in parallel."""
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=63)).strftime("%Y-%m-%d")
    jobs = [
        (74433, "0", {"start_date": start_date, "end_date": end_date}),
        (67888, "49583103", {"start_date": start_date, "end_date": end_date, "timeview": "day"}),
        (75557, "2043805321", {"start_date": start_date, "end_date": end_date, "timeview": "day"}),
    ]

    def _post_one(item: tuple[int, str, dict[str, str]]) -> tuple[int, bool, str]:
        cid, gid, flt = item
        payload = {
            "email": "khanhlp@ahamove.com",
            "card_id": cid,
            "source": "metabase",
            "filter": flt,
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit?gid={gid}#gid={gid}",
        }
        req = urllib.request.Request(
            METABASE_EXPORT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "DMAIChat_Bot/2.0"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return cid, resp.status in (200, 201, 202, 204), resp.read().decode("utf-8", errors="ignore")[:80]
        except Exception as exc:
            return cid, False, str(exc)[:80]

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(_post_one, jobs))
    ok_all = all(r[1] for r in results)
    summary = ", ".join(f"{cid}:{'OK' if ok else err}" for cid, ok, err in results)
    return ok_all, summary


# ── DATA FETCHERS (WITH CACHE + GITHUB FALLBACK + PARALLEL LOADING) ───────────
def _normalize_74433(raw: dict[str, Any]) -> dict[str, Any]:
    row: dict[str, Any] = {
        "city_id": str(raw.get("city_id", "")).strip(),
        "month": str(raw.get("month", ""))[:10],
        "week": str(raw.get("week", ""))[:10],
        "order_date": str(raw.get("order_date", ""))[:10],
        "tag": str(raw.get("tag", "")).strip(),
    }
    for col in SERVICE_COLS_74433:
        row[col] = _to_int(raw.get(col, 0))
    return row


def _normalize_67888(r: dict[str, Any]) -> dict[str, Any]:
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


def _normalize_75557(r: dict[str, Any]) -> dict[str, Any]:
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
        "cancel_order": _to_int(r.get("cancel_order", 0)),
        "cancel_poc": _to_int(r.get("cancel_poc", 0)),
        "accept_noti": _to_int(r.get("accept_noti", 0)),
        "total_noti": _to_int(r.get("total_noti", 0)),
        "rating_order": _to_int(r.get("rating_order", 0)),
        "rating_star": _to_int(r.get("rating_star", 0)),
        "bad_rating_order": _to_int(r.get("bad_rating_order", 0)),
        "total_aa_driver": _to_int(r.get("total_aa_driver", 0)),
        "hard_driver": _to_int(r.get("hard_driver", 0)),
        "lcd_driver": _to_int(r.get("lcd_driver", 0)),
        "lcd_driver_kpi": _to_int(r.get("lcd_driver_kpi", 0)),
        "gdr_driver": _to_int(r.get("gdr_driver", 0)),
    }


def _fetch_dataset(
    sheet_url: str,
    github_url: str,
    cache_file: str,
    date_key: str,
    normalizer: Any,
    label: str,
    force_refresh: bool = False,
) -> tuple[list[dict[str, Any]], str]:
    if not force_refresh and os.path.exists(cache_file):
        try:
            cached = json.loads(open(cache_file, encoding="utf-8").read())
            if time.time() - float(cached.get("ts", 0)) < CACHE_TTL_SEC and cached.get("rows"):
                return cached["rows"], cached.get("source", f"Cache ({label})")
        except Exception:
            pass

    rows: list[dict[str, Any]] = []
    source = ""
    try:
        req = urllib.request.Request(sheet_url, headers={"User-Agent": "DMAIChat_Bot/2.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        if text and not text.lstrip().startswith("<"):
            parsed = [normalizer(r) for r in csv.DictReader(io.StringIO(text)) if r.get(date_key)]
            if parsed:
                rows = parsed
                source = f"Sheet Live ({label})"
    except Exception:
        pass

    if not rows:
        req = urllib.request.Request(github_url, headers={"User-Agent": "DMAIChat_Bot/2.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw_list = json.loads(resp.read().decode("utf-8"))
        rows = [normalizer(r) for r in raw_list if r.get(date_key)]
        source = f"GitHub Snapshot ({label})"

    if rows:
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"ts": time.time(), "source": source, "rows": rows}, f, ensure_ascii=False)
        except Exception:
            pass
    return rows, source


def fetch_card_74433_rows(force_refresh: bool = False) -> tuple[list[dict[str, Any]], str]:
    return _fetch_dataset(
        SHEET_74433_CSV_URL, GITHUB_74433_URL, CACHE_FILE_74433, "order_date", _normalize_74433, "74433", force_refresh
    )


CACHE_FILE_74433 = CACHE_74433_FILE


def fetch_card_67888_rows(force_refresh: bool = False) -> tuple[list[dict[str, Any]], str]:
    return _fetch_dataset(
        SHEET_67888_CSV_URL, GITHUB_67888_URL, CACHE_67888_FILE, "period", _normalize_67888, "67888", force_refresh
    )


def fetch_card_75557_rows(force_refresh: bool = False) -> tuple[list[dict[str, Any]], str]:
    return _fetch_dataset(
        SHEET_75557_CSV_URL, GITHUB_75557_URL, CACHE_75557_FILE, "period", _normalize_75557, "75557", force_refresh
    )


def fetch_extra_tabs(force_refresh: bool = False) -> list[dict[str, Any]]:
    """Auto-discover and read any additional tabs added to the Google Sheet."""
    if not force_refresh and os.path.exists(CACHE_EXTRA_FILE):
        try:
            cached = json.loads(open(CACHE_EXTRA_FILE, encoding="utf-8").read())
            if time.time() - float(cached.get("ts", 0)) < CACHE_TTL_SEC:
                return cached.get("tabs", [])
        except Exception:
            pass

    extra_tabs: list[dict[str, Any]] = []
    try:
        req = urllib.request.Request(SHEET_HTMLVIEW_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            html_text = resp.read().decode("utf-8", errors="ignore")
        tabs = re.findall(r'name:\s*"([^"]+)".*?gid:\s*"(\d+)"', html_text)
        for name, gid in tabs:
            if gid in KNOWN_GIDS:
                continue
            csv_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={gid}"
            try:
                with urllib.request.urlopen(
                    urllib.request.Request(csv_url, headers={"User-Agent": "DMAIChat_Bot/2.0"}), timeout=6
                ) as c_resp:
                    c_txt = c_resp.read().decode("utf-8", errors="replace")
                if c_txt and not c_txt.lstrip().startswith("<"):
                    r_list = list(csv.DictReader(io.StringIO(c_txt)))
                    if r_list:
                        extra_tabs.append({
                            "name": name,
                            "gid": gid,
                            "row_count": len(r_list),
                            "columns": list(r_list[0].keys()),
                            "sample_latest": r_list[-10:],
                        })
            except Exception:
                continue
        with open(CACHE_EXTRA_FILE, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "tabs": extra_tabs}, f, ensure_ascii=False)
    except Exception:
        pass
    return extra_tabs


def fetch_all_sheets_parallel(force_refresh: bool = False) -> dict[str, Any]:
    """Fetch all 3 core sheets + any extra tabs in parallel."""
    with ThreadPoolExecutor(max_workers=4) as pool:
        f74 = pool.submit(fetch_card_74433_rows, force_refresh)
        f67 = pool.submit(fetch_card_67888_rows, force_refresh)
        f75 = pool.submit(fetch_card_75557_rows, force_refresh)
        fex = pool.submit(fetch_extra_tabs, force_refresh)
        r74, s74 = f74.result()
        r67, s67 = f67.result()
        r75, s75 = f75.result()
        extra = fex.result()
    return {
        "74433": r74, "src_74433": s74,
        "67888": r67, "src_67888": s67,
        "75557": r75, "src_75557": s75,
        "extra_tabs": extra,
    }


# ── AGGREGATION HELPERS ───────────────────────────────────────────────────────
def _agg_67888(sub: list[dict[str, Any]]) -> dict[str, float]:
    rq = sum(x["requested"] for x in sub)
    ac = sum(x["accept"] for x in sub)
    cp = sum(x["completed"] for x in sub)
    unful = rq - cp
    drop_after_acc = max(0, ac - cp)
    return {
        "req": rq,
        "acc": ac,
        "comp": cp,
        "unful": unful,
        "drop": drop_after_acc,
        "ar": (ac / rq * 100.0) if rq else 0.0,
        "fr": (cp / rq * 100.0) if rq else 0.0,
        "drop_rate": (drop_after_acc / ac * 100.0) if ac else 0.0,
    }


def _agg_74433(sub: list[dict[str, Any]]) -> dict[str, int]:
    out = {c: sum(x[c] for x in sub) for c in SERVICE_COLS_74433}
    for seg in ("FT", "PT", "return", "NIM", "NLM"):
        out[f"seg_{seg}"] = sum(x["total_active"] for x in sub if x["tag"].lower() == seg.lower())
    return out


def _agg_75557(sub: list[dict[str, Any]]) -> dict[str, float]:
    drv = sum(x["total_driver"] for x in sub)
    rnk = sum(x["ranking_driver"] for x in sub if x["ranking_driver"] > 0)
    drv_with_rnk = sum(x["total_driver"] for x in sub if x["ranking_driver"] > 0)
    stp = sum(x["total_stp"] for x in sub)
    o_inc = sum(x["order_income"] for x in sub)
    r_inc = sum(x["reward_income"] for x in sub)
    inc = o_inc + r_inc
    onl = sum(x["online_hours"] for x in sub)
    bsy = sum(x["busy_hours"] for x in sub)
    acc = sum(x["accept_order"] for x in sub)
    canc = sum(x["cancel_order"] for x in sub)
    cpoc = sum(x["cancel_poc"] for x in sub)
    anoti = sum(x["accept_noti"] for x in sub)
    tnoti = sum(x["total_noti"] for x in sub)
    r_ord = sum(x["rating_order"] for x in sub)
    r_star = sum(x["rating_star"] for x in sub)
    bad_r = sum(x["bad_rating_order"] for x in sub)
    aa = sum(x["total_aa_driver"] for x in sub)
    hard = sum(x["hard_driver"] for x in sub)
    lcd = sum(x["lcd_driver"] for x in sub)
    lcd_kpi = sum(x["lcd_driver_kpi"] for x in sub)
    gdr = sum(x["gdr_driver"] for x in sub)
    return {
        "drv": drv,
        "rnk": rnk,
        "active_rate": (drv_with_rnk / rnk * 100.0) if rnk else 0.0,
        "stp": stp,
        "stp_per_drv": (stp / drv) if drv else 0.0,
        "hrs_per_drv": (onl / drv) if drv else 0.0,
        "inc": inc,
        "rew": r_inc,
        "inc_per_drv": (inc / drv) if drv else 0.0,
        "rew_per_stp": (r_inc / stp) if stp else 0.0,
        "rew_pct": (r_inc / inc * 100.0) if inc else 0.0,
        "eph": (inc / onl) if onl else 0.0,
        "pph": (stp / onl) if onl else 0.0,
        "util": (bsy / onl * 100.0) if onl else 0.0,
        "aa_pct": (aa / drv * 100.0) if drv else 0.0,
        "hard_pct": (hard / drv * 100.0) if drv else 0.0,
        "lcd": lcd,
        "lcd_kpi": lcd_kpi,
        "lcd_pct": (lcd / drv * 100.0) if drv else 0.0,
        "gdr_pct": (gdr / drv * 100.0) if drv else 0.0,
        "ar_noti": (anoti / tnoti * 100.0) if tnoti else 0.0,
        "cr_total": (canc / acc * 100.0) if acc else 0.0,
        "cr_poc": (cpoc / acc * 100.0) if acc else 0.0,
        "cpoc_cnt": cpoc,
        "canc_cnt": canc,
        "rating": (r_star / r_ord) if r_ord else 0.0,
        "bad_rating": bad_r,
        "bad_pct": (bad_r / r_ord * 100.0) if r_ord else 0.0,
    }


# ── MASTER FULL CROSS-SHEET EXECUTIVE REPORT (HTML) ───────────────────────────
def fetch_full_executive_report(force_refresh: bool = False) -> str:
    """Read ALL metrics across ALL sheets and produce a rich, scannable HTML Executive Report."""
    bundle = fetch_all_sheets_parallel(force_refresh=force_refresh)
    r74, r67, r75 = bundle["74433"], bundle["67888"], bundle["75557"]
    if not r74 and not r67 and not r75:
        raise RuntimeError("Chưa tải được dữ liệu từ các sheet.")

    dates_all = sorted(
        {r["order_date"] for r in r74} | {r["period"] for r in r67} | {r["period"] for r in r75}
    )
    latest = dates_all[-1]
    prev = dates_all[-2] if len(dates_all) >= 2 else None
    wow = dates_all[-8] if len(dates_all) >= 8 else None
    last7_dates = set(dates_all[-8:-1]) if len(dates_all) >= 8 else set(dates_all[:-1])

    def _slice(dataset: list[dict[str, Any]], d_key: str, dt: str | None, c_key: str | None = None, c_val: str | None = None) -> list[dict[str, Any]]:
        if not dt:
            return []
        return [
            x for x in dataset
            if x[d_key] == dt and (c_val is None or x[c_key] == c_val)
        ]

    # Pre-aggregate NW & Regions (compact 1-message Executive Report)
    out: list[str] = []
    out.append(f"🏛️ <b>OPS EXECUTIVE REPORT — {latest}</b>")
    out.append(f"<i>DoD vs {prev or 'N/A'} | WoW vs {wow or 'N/A'} | 3 Sheets Live</i>")
    out.append("━━━━━━━━━━━━━━━━━━━━")

    for reg in ("NW", "SGN", "HAN", "EXP"):
        reg_icon = {"NW": "🌐", "SGN": "🏙️", "HAN": "🏛️", "EXP": "🧭"}[reg]
        reg_title = "NW (Toàn Quốc)" if reg == "NW" else reg

        d_cur = _agg_67888(_slice(r67, "period", latest, "region", reg))
        d_prv = _agg_67888(_slice(r67, "period", prev, "region", reg))
        d_wow = _agg_67888(_slice(r67, "period", wow, "region", reg))

        c_filter = None if reg == "NW" else reg
        s_cur = _agg_74433(_slice(r74, "order_date", latest, "city_id", c_filter))
        s_prv = _agg_74433(_slice(r74, "order_date", prev, "city_id", c_filter))
        s_wow = _agg_74433(_slice(r74, "order_date", wow, "city_id", c_filter))

        e_cur = _agg_75557(_slice(r75, "period", latest, "city_id", c_filter))
        e_prv = _agg_75557(_slice(r75, "period", prev, "city_id", c_filter))

        fr_badge = "🟢" if d_cur["fr"] >= 84.0 else ("🟡" if d_cur["fr"] >= 81.0 else "🔴")
        out.append(f"\n{reg_icon} <b>{reg_title}</b> {fr_badge}")

        if d_cur["req"] > 0:
            svcs = [x for x in _slice(r67, "period", latest, "region", reg) if x["requested"] >= 100]
            weak = min(svcs, key=lambda x: x["fr"]) if svcs else None
            weak_s = f" | Thấp nhất: <code>{_esc(weak['service_type'])}</code> {weak['fr']*100:.1f}%" if weak else ""
            out.append(
                f"• <b>Demand:</b> <b>{int(d_cur['req']):,}</b> ({_pct_delta(d_cur['req'], d_prv['req'])} DoD, {_pct_delta(d_cur['req'], d_wow['req'])} WoW) | "
                f"AR <b>{d_cur['ar']:.1f}%</b> | FR <b>{d_cur['fr']:.1f}%</b> ({_pp_delta(d_cur['fr'], d_prv['fr'], 1)}){weak_s}"
            )

        if s_cur["total_active"] > 0:
            tot_s = s_cur["total_active"]
            ft_pt_pct = (s_cur["seg_FT"] + s_cur["seg_PT"]) / tot_s * 100
            new_cnt = s_cur["seg_NIM"] + s_cur["seg_NLM"]
            out.append(
                f"• <b>Supply:</b> <b>{tot_s:,}</b> TX ({_pct_delta(tot_s, s_prv['total_active'])} DoD, {_pct_delta(tot_s, s_wow['total_active'])} WoW) | "
                f"Core {ft_pt_pct:.0f}% • Ret {s_cur['seg_return']:,} • New {new_cnt:,}"
            )

        if e_cur["drv"] > 0:
            out.append(
                f"• <b>Driver:</b> <b>{e_cur['inc_per_drv']/1000:,.0f}k/TX</b> ({_pct_delta(e_cur['inc_per_drv'], e_prv['inc_per_drv'])}) | "
                f"EPH <b>{e_cur['eph']/1000:,.1f}k</b> | PPH <b>{e_cur['pph']:.2f}</b> | Util {e_cur['util']:.0f}% | "
                f"AA {e_cur['aa_pct']:.0f}% | LCD {e_cur['lcd_pct']:.0f}% | CR {e_cur['cr_poc']:.1f}%"
            )

    if bundle["extra_tabs"]:
        names = ", ".join(f"<code>{_esc(tb['name'])}</code>" for tb in bundle["extra_tabs"])
        out.append(f"\n📑 <i>Tab mở rộng:</i> {names}")

    out.append("\n━━━━━━━━━━━━━━━━━━━━")
    out.append("🧠 <b>INSIGHTS CHÍNH</b>")
    for bullet in _build_cross_sheet_insights(r74, r67, r75, latest, prev, wow):
        out.append(f"• {bullet}")
    out.append("\n<i>Chi tiết từng bảng: /kpi • /supply • /driver</i>")

    return "\n".join(out)


def _build_cross_sheet_insights(
    r74: list[dict[str, Any]],
    r67: list[dict[str, Any]],
    r75: list[dict[str, Any]],
    latest: str,
    prev: str | None,
    wow: str | None,
) -> list[str]:
    insights: list[str] = []

    cur67 = [x for x in r67 if x["period"] == latest]
    prv67 = [x for x in r67 if x["period"] == prev] if prev else []
    wow67 = [x for x in r67 if x["period"] == wow] if wow else []

    cur74 = [x for x in r74 if x["order_date"] == latest]
    prv74 = [x for x in r74 if x["order_date"] == prev] if prev else []

    cur75 = [x for x in r75 if x["period"] == latest]
    prv75 = [x for x in r75 if x["period"] == prev] if prev else []

    # 1. Supply vs Demand Growth Balance (NW & Cities)
    nw_d_cur = _agg_67888([x for x in cur67 if x["region"] == "NW"])
    nw_d_prv = _agg_67888([x for x in prv67 if x["region"] == "NW"])
    nw_s_cur = sum(x["total_active"] for x in cur74)
    nw_s_prv = sum(x["total_active"] for x in prv74)
    if nw_d_prv["req"] and nw_s_prv:
        req_chg = (nw_d_cur["req"] - nw_d_prv["req"]) / nw_d_prv["req"] * 100
        sup_chg = (nw_s_cur - nw_s_prv) / nw_s_prv * 100
        gap = req_chg - sup_chg
        balance_msg = (
            "Demand tăng nhanh hơn Active Driver (áp lực thiếu supply giờ cao điểm)"
            if gap > 2.0
            else ("Nguồn Supply giữ nhịp tốt hơn đà giảm của Demand (giúp FR cải thiện)" if gap < -1.5 else "Supply - Demand biến động cân bằng")
        )
        insights.append(
            f"<b>Cân bằng Supply - Demand (NW):</b> Demand (Volume) biến động <b>{req_chg:+.1f}%</b> DoD trong khi Active Driver biến động "
            f"<b>{sup_chg:+.1f}%</b> DoD → <i>{balance_msg}</i> (FR đạt <b>{nw_d_cur['fr']:.2f}%</b>, "
            f"{_pp_delta(nw_d_cur['fr'], nw_d_prv['fr'])})."
        )

    # 2. Bottleneck Service & Auto-Accept Correlation across SGN vs HAN
    sgn_75 = _agg_75557([x for x in cur75 if x["city_id"] == "SGN"])
    han_75 = _agg_75557([x for x in cur75 if x["city_id"] == "HAN"])
    sgn_67 = _agg_67888([x for x in cur67 if x["region"] == "SGN"])
    han_67 = _agg_67888([x for x in cur67 if x["region"] == "HAN"])
    if sgn_67["req"] and han_67["req"]:
        weak_svcs = [x for x in cur67 if x["region"] in ("SGN", "HAN", "EXP") and x["requested"] >= 300]
        worst_svc = min(weak_svcs, key=lambda x: x["fr"]) if weak_svcs else None
        svc_clause = (
            f"; điểm nghẽn lớn nhất là <code>{worst_svc['region']}-{worst_svc['service_type']}</code> "
            f"(FR chỉ <b>{worst_svc['fr']*100:.1f}%</b>, AR <b>{worst_svc['ar']*100:.1f}%</b> trên {worst_svc['requested']:,} đơn)"
            if worst_svc else ""
        )
        insights.append(
            f"<b>Tương quan Auto-Accept &amp; SLA:</b> SGN duy trì FR <b>{sgn_67['fr']:.1f}%</b> nhờ tỷ lệ AA cao "
            f"(<b>{sgn_75['aa_pct']:.1f}%</b>), trong khi HAN có AA thấp (<b>{han_75['aa_pct']:.1f}%</b>) dẫn tới AR/FR thấp hơn "
            f"(AR <b>{han_67['ar']:.1f}%</b>, FR <b>{han_67['fr']:.1f}%</b>){svc_clause}."
        )

    # 3. Post-Accept Cancellation Leakage (CR POC vs Unfulfilled)
    high_cr_segs = [x for x in cur75 if x["accept_order"] >= 300]
    if high_cr_segs and nw_d_cur["unful"] > 0:
        worst_cr = max(high_cr_segs, key=lambda x: x["cancel_poc"] / x["accept_order"])
        w_rate = worst_cr["cancel_poc"] / worst_cr["accept_order"] * 100
        drop_share = (nw_d_cur["drop"] / nw_d_cur["unful"] * 100) if nw_d_cur["unful"] else 0
        insights.append(
            f"<b>Rò rỉ đơn sau nhận (Cancel Leakage):</b> Toàn mạng lưới mất <b>{int(nw_d_cur['drop']):,}</b> đơn hủy sau khi TX đã nhận "
            f"(chiếm <b>{drop_share:.1f}%</b> tổng đơn rớt). Nóng nhất ở <code>{worst_cr['city_id']}-{worst_cr['driver_segment']}</code> "
            f"với CR POC <b>{w_rate:.1f}%</b> ({worst_cr['cancel_poc']:,} đơn hủy)."
        )

    # 4. Driver Unit Economics & LCD Quality (EPH, Utilization, Low Cancellation Rate Driver)
    tot_75 = _agg_75557(cur75)
    prv_75 = _agg_75557(prv75) if prv75 else {}
    if tot_75["drv"] > 0:
        eph_chg = _pct_delta(tot_75["eph"], prv_75.get("eph", 0))
        inc_chg = _pct_delta(tot_75["inc_per_drv"], prv_75.get("inc_per_drv", 0))
        # LCD = Low Cancellation Rate Driver (higher is better -> flag lowest LCD% segment)
        lcd_segs = [x for x in cur75 if x["total_driver"] >= 100]
        low_lcd = min(lcd_segs, key=lambda x: x["lcd_driver"] / x["total_driver"]) if lcd_segs else None
        lcd_clause = (
            f"; tỷ lệ LCD (TX hủy thấp) đạt <b>{tot_75['lcd_pct']:.1f}%</b> NW, thấp nhất ở "
            f"<code>{low_lcd['city_id']}-{low_lcd['driver_segment']}</code> "
            f"(<b>{low_lcd['lcd_driver']/low_lcd['total_driver']*100:.1f}%</b> ~ {low_lcd['lcd_driver']:,}/{low_lcd['total_driver']:,} TX)"
            if low_lcd else ""
        )
        insights.append(
            f"<b>Thu nhập &amp; Chất lượng Supply:</b> Thu nhập TB đạt <b>{tot_75['inc_per_drv']/1000:,.0f}k/TX</b> ({inc_chg} DoD), "
            f"EPH đạt <b>{tot_75['eph']/1000:,.1f}k/h</b> ({eph_chg} DoD), Utilization <b>{tot_75['util']:.1f}%</b>{lcd_clause}."
        )

    # 5. Biggest Segment / Service Movers (DoD & WoW)
    movers = []
    for c in ("SGN", "HAN", "EXP"):
        for t in ("FT", "PT", "return", "NIM", "NLM"):
            v1 = sum(x["total_active"] for x in cur74 if x["city_id"] == c and x["tag"] == t)
            v0 = sum(x["total_active"] for x in prv74 if x["city_id"] == c and x["tag"] == t)
            if v0 >= 50:
                movers.append(((v1 - v0) / v0 * 100.0, f"{c}-{t}", v1, v1 - v0))
    if movers:
        movers.sort()
        worst_m = movers[0]
        best_m = movers[-1]
        insights.append(
            f"<b>Biến động Segment mạnh nhất (DoD):</b> Tăng tốt nhất <code>{best_m[1]}</code> "
            f"(<b>{best_m[0]:+.1f}%</b>, {best_m[3]:+,} TX) | Giảm mạnh nhất <code>{worst_m[1]}</code> "
            f"(<b>{worst_m[0]:+.1f}%</b>, {worst_m[3]:+,} TX)."
        )

    return insights


# ── SPECIALIZED SINGLE-SHEET REPORTS (ENHANCED HTML + % DELTAS) ───────────────
def fetch_ops_brief(force_refresh: bool = False) -> str:
    """Alias /ops to the upgraded Full Cross-Sheet Executive Report."""
    return fetch_full_executive_report(force_refresh=force_refresh)


def fetch_supply_brief(force_refresh: bool = False) -> str:
    """Detailed Card 74433 Supply by Segment & All 14 Service Columns + DoD/WoW."""
    rows, source = fetch_card_74433_rows(force_refresh=force_refresh)
    if not rows:
        raise RuntimeError("Chưa có dữ liệu Card 74433.")
    dates = sorted({r["order_date"] for r in rows})
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None
    wow = dates[-8] if len(dates) >= 8 else None

    cur = [r for r in rows if r["order_date"] == latest]
    prv = [r for r in rows if r["order_date"] == prev] if prev else []
    wov = [r for r in rows if r["order_date"] == wow] if wow else []

    tot_c = sum(x["total_active"] for x in cur)
    tot_p = sum(x["total_active"] for x in prv)
    tot_w = sum(x["total_active"] for x in wov)

    lines = [
        f"🛵 <b>CHI TIẾT ACTIVE DRIVER / SUPPLY CARD 74433 — {latest}</b>",
        f"<i>{source}</i> | NW Active: <b>{tot_c:,}</b> ({_pct_delta(tot_c, tot_p)} DoD | {_pct_delta(tot_c, tot_w)} WoW)",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    for city in ("SGN", "HAN", "EXP"):
        c_cur = sorted([r for r in cur if r["city_id"] == city], key=lambda x: -x["total_active"])
        c_prv = {r["tag"]: r for r in prv if r["city_id"] == city}
        c_wov = {r["tag"]: r for r in wov if r["city_id"] == city}
        cs_c = sum(x["total_active"] for x in c_cur)
        cs_p = sum(x["total_active"] for x in c_prv.values())
        cs_w = sum(x["total_active"] for x in c_wov.values())
        lines.append(
            f"\n📍 <b>{city}</b> — Tổng: <b>{cs_c:,}</b> ({_pct_delta(cs_c, cs_p)} DoD | {_pct_delta(cs_c, cs_w)} WoW)"
        )
        for r in c_cur:
            rp = c_prv.get(r["tag"], {})
            rw = c_wov.get(r["tag"], {})
            lines.append(
                f"• <code>{r['tag']}</code>: <b>{r['total_active']:,}</b> "
                f"({_pct_delta(r['total_active'], rp.get('total_active', 0))} DoD, {_pct_delta(r['total_active'], rw.get('total_active', 0))} WoW)\n"
                f"  <i>1h:{r['active_1h']:,} • 2h:{r['active_2h']:,} • 4h:{r['active_4h']:,} | "
                f"bike:{r['bike']:,} • eco:{r['eco']:,} • 2H:{r['_2H']:,} • bulky:{r['_2HBULKY']:,} • "
                f"pool:{r['pool']:,} • food:{r['aifood']:,} • TMDT:{r['TMDT']:,} • inday:{r['INDAY']:,}</i>"
            )
    return "\n".join(lines)


def fetch_kpi_brief(force_refresh: bool = False) -> str:
    """Detailed Card 67888 Orders, AR, FR, Unfulfilled & All Service Types + DoD/WoW."""
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

    nw_c = _agg_67888([r for r in cur if r["region"] == "NW"])
    nw_p = _agg_67888([r for r in prv if r["region"] == "NW"])
    nw_w = _agg_67888([r for r in wov if r["region"] == "NW"])

    lines = [
        f"📦 <b>CHI TIẾT ĐƠN &amp; SLA CARD 67888 — {latest}</b>",
        f"<i>{source}</i> | NW Req: <b>{int(nw_c['req']):,}</b> ({_pct_delta(nw_c['req'], nw_p['req'])} DoD | {_pct_delta(nw_c['req'], nw_w['req'])} WoW) | "
        f"FR: <b>{nw_c['fr']:.2f}%</b> ({_pp_delta(nw_c['fr'], nw_p['fr'])} DoD)",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    for reg in ("NW", "SGN", "HAN", "EXP"):
        rc = _agg_67888([r for r in cur if r["region"] == reg])
        rp = _agg_67888([r for r in prv if r["region"] == reg])
        rw = _agg_67888([r for r in wov if r["region"] == reg])
        if rc["req"] == 0:
            continue
        lines.append(
            f"\n🌐 <b>{reg}</b> — Req: <b>{int(rc['req']):,}</b> ({_pct_delta(rc['req'], rp['req'])} DoD, {_pct_delta(rc['req'], rw['req'])} WoW)\n"
            f"  Acc: <b>{int(rc['acc']):,}</b> | Comp: <b>{int(rc['comp']):,}</b> | Rớt: <b>{int(rc['unful']):,}</b> | "
            f"AR: <b>{rc['ar']:.1f}%</b> ({_pp_delta(rc['ar'], rp['ar'], 1)}) | FR: <b>{rc['fr']:.1f}%</b> ({_pp_delta(rc['fr'], rp['fr'], 1)})"
        )
        p_map = {x["service_type"]: x for x in prv if x["region"] == reg}
        for s in sorted([r for r in cur if r["region"] == reg], key=lambda x: -x["requested"])[:7]:
            sp = p_map.get(s["service_type"])
            rq_d = _pct_delta(s["requested"], sp["requested"], 1) if sp else "N/A"
            fr_d = _pp_delta(s["fr"] * 100, sp["fr"] * 100, 1) if sp else "N/A"
            lines.append(
                f"  • <code>{_esc(s['service_type'])}</code>: Req <b>{s['requested']:,}</b> ({rq_d}) | "
                f"Comp {s['completed']:,} | AR <b>{s['ar']*100:.1f}%</b> | FR <b>{s['fr']*100:.1f}%</b> ({fr_d})"
            )
    return "\n".join(lines)


def fetch_driver_brief(force_refresh: bool = False) -> str:
    """Detailed Card 75557 Driver Income, EPH, PPH, Util, AA, Hard, LCD, GDR, CR, Rating + DoD/WoW."""
    rows, source = fetch_card_75557_rows(force_refresh=force_refresh)
    if not rows:
        raise RuntimeError("Chưa có dữ liệu Card 75557.")
    dates = sorted({r["period"] for r in rows})
    latest = dates[-1]
    prev = dates[-2] if len(dates) >= 2 else None
    wow = dates[-8] if len(dates) >= 8 else None

    cur = [r for r in rows if r["period"] == latest]
    prv = [r for r in rows if r["period"] == prev] if prev else []
    wov = [r for r in rows if r["period"] == wow] if wow else []

    tc = _agg_75557(cur)
    tp = _agg_75557(prv)
    tw = _agg_75557(wov)

    lines = [
        f"💰 <b>CHI TIẾT THU NHẬP &amp; CHẤT LƯỢNG TX CARD 75557 — {latest}</b>",
        f"<i>{source}</i> | NW TX: <b>{int(tc['drv']):,}</b> | TB/TX: <b>{tc['inc_per_drv']/1000:,.0f}k</b> "
        f"({_pct_delta(tc['inc_per_drv'], tp['inc_per_drv'])} DoD | {_pct_delta(tc['inc_per_drv'], tw['inc_per_drv'])} WoW) | "
        f"EPH: <b>{tc['eph']/1000:,.1f}k</b> ({_pct_delta(tc['eph'], tp['eph'])})",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    for city in ("SGN", "HAN", "EXP"):
        c_rows = sorted([r for r in cur if r["city_id"] == city], key=lambda x: -x["total_driver"])
        if not c_rows:
            continue
        ca = _agg_75557(c_rows)
        cp = _agg_75557([r for r in prv if r["city_id"] == city])
        cw = _agg_75557([r for r in wov if r["city_id"] == city])
        p_map = {r["driver_segment"]: r for r in prv if r["city_id"] == city}
        lines.append(
            f"\n🏙️ <b>{city}</b> — TX: <b>{int(ca['drv']):,}</b> ({_pct_delta(ca['drv'], cp['drv'])} DoD, {_pct_delta(ca['drv'], cw['drv'])} WoW) | "
            f"Active/Rank: <b>{ca['active_rate']:.1f}%</b>\n"
            f"  TB/TX: <b>{ca['inc_per_drv']/1000:,.0f}k</b> ({_pct_delta(ca['inc_per_drv'], cp['inc_per_drv'])}) | "
            f"EPH: <b>{ca['eph']/1000:,.1f}k</b> | PPH: <b>{ca['pph']:.2f}</b> | Util: <b>{ca['util']:.1f}%</b> | "
            f"Thưởng: <b>{ca['rew_pct']:.2f}%</b>\n"
            f"  AA: <b>{ca['aa_pct']:.1f}%</b> • Hard: <b>{ca['hard_pct']:.1f}%</b> • LCD: <b>{int(ca['lcd']):,}</b> ({ca['lcd_pct']:.1f}%) • "
            f"GDR: <b>{ca['gdr_pct']:.1f}%</b> • AR Noti: <b>{ca['ar_noti']:.1f}%</b> • CR POC: <b>{ca['cr_poc']:.2f}%</b> • ⭐<b>{ca['rating']:.2f}</b>"
        )
        for r in c_rows:
            sa = _agg_75557([r])
            sp = _agg_75557([p_map[r["driver_segment"]]]) if r["driver_segment"] in p_map else {}
            inc_d = _pct_delta(sa["inc_per_drv"], sp.get("inc_per_drv", 0), 1) if sp else "N/A"
            lines.append(
                f"  • <code>{r['driver_segment']}</code>: <b>{r['total_driver']:,}</b> TX | "
                f"<b>{sa['inc_per_drv']/1000:,.0f}k</b> ({inc_d}) | EPH {sa['eph']/1000:,.1f}k | PPH {sa['pph']:.2f} | "
                f"Util {sa['util']:.0f}% | AA {sa['aa_pct']:.0f}% | LCD {int(sa['lcd'])} | CR {sa['cr_poc']:.1f}%"
            )
    return "\n".join(lines)


# ── AI CONTEXT BUILDER (ALL SHEETS + PRE-COMPUTED DELTAS & TRENDS) ────────────
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
    """Build comprehensive multi-sheet context with pre-computed DoD/WoW/WTD/MTD metrics for AI."""
    bundle = fetch_all_sheets_parallel()
    r74, r67, r75 = bundle["74433"], bundle["67888"], bundle["75557"]
    if not r74 and not r67 and not r75:
        return ""

    dates = sorted({r["order_date"] for r in r74} | {r["period"] for r in r67} | {r["period"] for r in r75})
    req_dates = _extract_requested_dates(user_message, dates)
    msg_low = user_message.lower()
    wants_week = any(k in msg_low for k in ("tuần", "week", "đầu tuần", "7 ngày", "trend"))

    if req_dates:
        target_dates = req_dates
    elif wants_week:
        target_dates = dates[-7:]
    else:
        # Include latest, prev (DoD), and 7-days-ago (WoW) so AI always has exact % deltas!
        picks = [dates[-1]]
        if len(dates) >= 2:
            picks.append(dates[-2])
        if len(dates) >= 8:
            picks.append(dates[-8])
        target_dates = sorted(set(picks))

    parts: list[str] = [
        f"Khoảng dữ liệu khả dụng: {dates[0]} -> {dates[-1]} | Ngày mới nhất: {dates[-1]}",
        "BẢN TÓM TẮT EXECUTIVE ĐÃ TÍNH SẴN (% DoD, % WoW, Insights chéo):",
        re.sub(r"<[^>]+>", "", fetch_full_executive_report()),
    ]

    # Detailed slices for requested/recent dates across all 3 cards
    if r74:
        parts.append("\n=== CHI TIẾT CARD 74433 (TÀI XẾ ACTIVE THEO TAG & 14 CỘT DỊCH VỤ) ===")
        for dt in target_dates:
            day_r = [x for x in r74 if x["order_date"] == dt]
            if not day_r:
                continue
            tot_all = sum(x["total_active"] for x in day_r)
            city_sums = " | ".join(f"{c}={sum(x['total_active'] for x in day_r if x['city_id'] == c):,}" for c in ("SGN", "HAN", "EXP"))
            parts.append(f"[Ngày {dt}] TỔNG TX ACTIVE NW={tot_all:,} | {city_sums}")
            for r in sorted(day_r, key=lambda x: (x["city_id"], x["tag"])):
                parts.append(
                    f"  {r['city_id']}|{r['tag']}: active={r['total_active']} (1h={r['active_1h']},2h={r['active_2h']},4h={r['active_4h']} | "
                    f"bike={r['bike']},eco={r['eco']},pool={r['pool']},food={r['aifood']},2H={r['_2H']},bulky={r['_2HBULKY']},TMDT={r['TMDT']},inday={r['INDAY']})"
                )

    if r67:
        parts.append("\n=== CHI TIẾT CARD 67888 (ĐƠN REQUESTED, ACCEPT, COMPLETED, AR, FR) ===")
        for dt in target_dates:
            d6_r = [x for x in r67 if x["period"] == dt]
            if not d6_r:
                continue
            parts.append(f"[Ngày {dt}]")
            for r in sorted(d6_r, key=lambda x: (x["region"], -x["requested"])):
                parts.append(
                    f"  {r['region']}|{r['service_type']}: req={r['requested']},acc={r['accept']},comp={r['completed']},unful={r['requested']-r['completed']}|AR={r['ar']*100:.2f}%,FR={r['fr']*100:.2f}%"
                )

    if r75:
        parts.append("\n=== CHI TIẾT CARD 75557 (THU NHẬP, EPH, PPH, UTIL, AA, HARD, LCD, GDR, CR, RATING) ===")
        for dt in target_dates:
            d7_r = [x for x in r75 if x["period"] == dt]
            if not d7_r:
                continue
            tot7 = sum(x["total_driver"] for x in d7_r)
            c7_s = " | ".join(f"{c}={sum(x['total_driver'] for x in d7_r if x['city_id'] == c):,}" for c in ("SGN", "HAN", "EXP"))
            parts.append(f"[Ngày {dt}] TỔNG TX={tot7:,} | {c7_s}")
            for r in sorted(d7_r, key=lambda x: (x["city_id"], x["driver_segment"])):
                sa = _agg_75557([r])
                parts.append(
                    f"  {r['city_id']}|{r['driver_segment']}: rank={r['ranking_driver']},active={r['total_driver']}({sa['active_rate']:.1f}%),hard={r['hard_driver']},aa={r['total_aa_driver']}({sa['aa_pct']:.0f}%),lcd={r['lcd_driver']},gdr={r['gdr_driver']} | "
                    f"inc/drv={sa['inc_per_drv']:,.0f},rew%={sa['rew_pct']:.2f}%,EPH={sa['eph']:,.0f},PPH={sa['pph']:.2f},Util={sa['util']:.1f}%,hrs/drv={sa['hrs_per_drv']:.1f} | "
                    f"AR_noti={sa['ar_noti']:.1f}%,CR_tot={sa['cr_total']:.1f}%,CR_poc={sa['cr_poc']:.2f}%({r['cancel_poc']}),Rating={sa['rating']:.2f},bad={r['bad_rating_order']}"
                )

    # Weekly & Monthly multi-sheet trends
    if r67 and r75:
        parts.append("\n=== XU HƯỚNG THEO THÁNG & 7 NGÀY GẦN NHẤT (TỔNG HỢP 3 SHEETS) ===")
        months = sorted({r["period"][:7] for r in r67})
        for m in months:
            m67 = [r for r in r67 if r["period"].startswith(m)]
            m75 = [r for r in r75 if r["period"].startswith(m)]
            n_d = len({r["period"] for r in m67}) or 1
            a67 = _agg_67888([r for r in m67 if r["region"] == "NW"])
            a75 = _agg_75557(m75)
            parts.append(
                f"Tháng {m} ({n_d} ngày): NW Req={int(a67['req']):,} ({int(a67['req'])//n_d:,}/ng), Comp={int(a67['comp']):,}, "
                f"AR={a67['ar']:.2f}%, FR={a67['fr']:.2f}% | TB TX/ng={int(a75['drv'])//n_d:,}, EPH={a75['eph']:,.0f}, PPH={a75['pph']:.2f}, Util={a75['util']:.1f}%, CR_poc={a75['cr_poc']:.2f}%"
            )

    if bundle["extra_tabs"]:
        parts.append("\n=== DỮ LIỆU CÁC TAB MỞ RỘNG TRÊN GOOGLE SHEET ===")
        for tb in bundle["extra_tabs"]:
            parts.append(f"Tab {tb['name']} ({tb['row_count']} dòng): {json.dumps(tb['sample_latest'], ensure_ascii=False)}")

    return "\n".join(parts)
