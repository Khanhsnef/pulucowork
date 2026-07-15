"""Module Gold — giá vàng thế giới + vàng Việt Nam + chênh lệch quy đổi.

Nguồn (đều free, không cần key riêng):
- Thế giới : Binance PAXG/USDT (Pax Gold — 1 token = 1 troy oz vàng LBMA,
             bám sát XAU spot; có klines lịch sử để vẽ chart)
- Việt Nam : API công khai BTMC (Bảo Tín Minh Châu) — SJC miếng, nhẫn tròn trơn
- Tỷ giá   : open.er-api.com USD/VND

Chênh lệch SJC vs thế giới = (giá SJC/lượng) − (XAU quy đổi VND/lượng).
1 lượng = 37.5g = 1.20565 troy oz. Giá BTMC trả về theo CHỈ → ×10 ra lượng.

Cache in-memory TTL 10 phút (giá vàng VN cập nhật theo phiên, không cần realtime).
"""

from __future__ import annotations

import json
import time
import urllib.request
from datetime import datetime

OZ_PER_LUONG = 1.20565          # 37.5g / 31.1034768g
BTMC_URL = ("http://api.btmc.vn/api/BTMCAPI/getpricebtmc"
            "?key=3kd8ub1llcg9t45hnoh8hmn7t5kc2v")   # key công khai trên site BTMC
UA = {"User-Agent": "TradingSystem/2.0 (personal research)"}

_cache: dict = {"ts": 0.0, "data": None}
CACHE_TTL = 600  # 10 phút


def _get_json(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def fetch_world_gold() -> dict:
    """PAXG/USDT: giá hiện tại + biến động 24h + klines 12 tháng cho chart."""
    t = _get_json("https://api.binance.com/api/v3/ticker/24hr?symbol=PAXGUSDT")
    out = {
        "usd_oz": float(t["lastPrice"]),
        "change_24h_pct": float(t["priceChangePercent"]),
        "high_24h": float(t["highPrice"]),
        "low_24h": float(t["lowPrice"]),
    }
    kl = _get_json("https://api.binance.com/api/v3/klines?symbol=PAXGUSDT&interval=1d&limit=365")
    out["chart"] = {
        "dates": [datetime.fromtimestamp(k[0] / 1000).strftime("%Y-%m-%d") for k in kl],
        "closes": [float(k[4]) for k in kl],
    }
    return out


def fetch_vn_gold() -> dict:
    """BTMC API — lấy SJC miếng + nhẫn tròn trơn. Giá theo chỉ → nhân 10 ra lượng."""
    d = _get_json(BTMC_URL)
    rows = d["DataList"]["Data"]
    out: dict = {"items": [], "updated": None}
    want = [
        ("VÀNG MIẾNG SJC", "SJC miếng"),
        ("NHẪN TRÒN TRƠN", "Nhẫn tròn trơn VRTL"),
        ("VÀNG MIẾNG VRTL", "Vàng miếng VRTL"),
    ]
    for r in rows:
        i = r["@row"]
        name = (r.get(f"@n_{i}") or "").upper()
        for pattern, label in want:
            if pattern in name and not any(x["label"] == label for x in out["items"]):
                buy_chi = float(r.get(f"@pb_{i}") or 0)
                sell_chi = float(r.get(f"@ps_{i}") or 0)
                if buy_chi <= 0:
                    continue
                out["items"].append({
                    "label": label,
                    "buy_luong": buy_chi * 10,       # VND/lượng
                    "sell_luong": sell_chi * 10 if sell_chi > 0 else None,
                })
                out["updated"] = r.get(f"@d_{i}") or out["updated"]
    return out


def fetch_usd_vnd() -> float:
    d = _get_json("https://open.er-api.com/v6/latest/USD")
    return float(d["rates"]["VND"])


def gold_dashboard(force: bool = False) -> dict:
    """Tổng hợp đầy đủ, cache 10 phút. Từng nguồn lỗi thì degrade mềm."""
    now = time.time()
    if not force and _cache["data"] is not None and now - _cache["ts"] < CACHE_TTL:
        return _cache["data"]

    out: dict = {"generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "errors": []}

    world = None
    try:
        world = fetch_world_gold()
        out["world"] = world
    except Exception as e:
        out["errors"].append(f"Vàng thế giới (Binance PAXG): {e}")

    # Phân tích kỹ thuật đầy đủ PAXGUSDT làm proxy cho Vàng
    try:
        from .main import analyze
        from dataclasses import asdict
        analysis_dec = analyze("PAXGUSDT", lookback_years=5, verbose=False)
        out["analysis"] = asdict(analysis_dec)
    except Exception as e:
        out["errors"].append(f"Phân tích kỹ thuật Vàng lỗi: {e}")

    vn = None
    try:
        vn = fetch_vn_gold()
        out["vn"] = vn
    except Exception as e:
        out["errors"].append(f"Vàng VN (BTMC): {e}")

    rate = None
    try:
        rate = fetch_usd_vnd()
        out["usd_vnd"] = rate
    except Exception as e:
        out["errors"].append(f"Tỷ giá USD/VND: {e}")

    # Quy đổi + chênh lệch SJC vs thế giới
    if world and rate:
        world_vnd_luong = world["usd_oz"] * OZ_PER_LUONG * rate
        out["world_vnd_luong"] = world_vnd_luong
        sjc = next((x for x in (vn or {}).get("items", []) if x["label"] == "SJC miếng"), None)
        if sjc and sjc.get("sell_luong"):
            premium = sjc["sell_luong"] - world_vnd_luong
            out["sjc_premium_vnd"] = premium
            out["sjc_premium_pct"] = premium / world_vnd_luong * 100
        if sjc and sjc.get("buy_luong") and sjc.get("sell_luong"):
            out["sjc_spread_vnd"] = sjc["sell_luong"] - sjc["buy_luong"]

    if world or vn:
        _cache["ts"] = now
        _cache["data"] = out
    return out
