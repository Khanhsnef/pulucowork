"""Module 2B — FA Filter: cổng lọc cơ bản, ánh xạ thành điểm định lượng.

VN stock : chấm điểm 5 tiêu chí từ BCTC. Crypto: chấm theo thanh khoản/funding.
FA không sinh tín hiệu vào lệnh — chỉ điều chỉnh mức độ tin cậy và có thể
CHẶN khuyến nghị MUA nếu nền tảng quá xấu (score < 40).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import AssetType


@dataclass
class FAGate:
    score: float                 # 0-100
    passed: bool                 # score >= 40 → cho phép khuyến nghị MUA
    details: dict = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)


def score_vn_fundamentals(fund: dict) -> FAGate:
    """Chấm 5 tiêu chí × 20 điểm. Thiếu dữ liệu → 10 điểm trung tính + ghi chú."""
    details, notes = {}, []
    score = 0.0

    def add(name: str, value, points: float, reason: str):
        nonlocal score
        details[name] = {"value": value, "points": points, "reason": reason}
        score += points

    if fund.get("_error"):
        return FAGate(score=50.0, passed=True, details={},
                      notes=[f"Không lấy được FA ({fund['_error']}) — bỏ qua cổng FA, chỉ dùng TA."])

    rg = fund.get("revenue_growth_yoy")
    if rg is None:
        add("revenue_growth", None, 10, "thiếu dữ liệu — trung tính")
    elif rg > 0.15:
        add("revenue_growth", rg, 20, f"doanh thu tăng {rg:.0%} YoY (> 15%)")
    elif rg > 0:
        add("revenue_growth", rg, 12, f"doanh thu tăng nhẹ {rg:.0%}")
    else:
        add("revenue_growth", rg, 0, f"doanh thu giảm {rg:.0%}")

    pg = fund.get("profit_growth_yoy")
    if pg is None:
        add("profit_growth", None, 10, "thiếu dữ liệu — trung tính")
    elif pg > 0.15:
        add("profit_growth", pg, 20, f"lợi nhuận tăng {pg:.0%} YoY")
    elif pg > 0:
        add("profit_growth", pg, 12, f"lợi nhuận tăng nhẹ {pg:.0%}")
    else:
        add("profit_growth", pg, 0, f"lợi nhuận giảm {pg:.0%}")

    roe = fund.get("roe")
    if roe is None:
        add("roe", None, 10, "thiếu dữ liệu")
    else:
        roe_pct = roe if roe > 1 else roe * 100  # vnstock có nguồn trả 15.2, nguồn trả 0.152
        add("roe", roe_pct, 20 if roe_pct > 15 else (12 if roe_pct > 10 else 4),
            f"ROE {roe_pct:.1f}%")

    de = fund.get("debt_to_equity")
    if de is None:
        add("debt_to_equity", None, 10, "thiếu dữ liệu")
    else:
        add("debt_to_equity", de, 20 if de < 1.0 else (10 if de < 2.0 else 0),
            f"Nợ vay/VCSH = {de:.2f}")

    pe = fund.get("pe")
    if pe is None or pe <= 0:
        add("pe", pe, 10, "P/E âm hoặc thiếu — trung tính")
    else:
        add("pe", pe, 20 if pe < 12 else (12 if pe < 20 else 5), f"P/E = {pe:.1f}")

    return FAGate(score=score, passed=score >= 40, details=details, notes=notes)


def score_crypto_context(ctx: dict) -> FAGate:
    """Crypto không có BCTC — chấm theo thanh khoản, funding, orderbook."""
    details, notes = {}, []
    score = 50.0  # nền trung tính

    if ctx.get("_error"):
        return FAGate(score=50.0, passed=True, details={},
                      notes=[f"Không lấy được context ({ctx['_error']}) — chỉ dùng TA."])

    vol = ctx.get("volume_24h_quote")
    if vol is not None:
        if vol > 100_000_000:
            score += 20; details["volume_24h"] = {"value": vol, "points": 20, "reason": "thanh khoản > $100M/24h"}
        elif vol > 10_000_000:
            score += 10; details["volume_24h"] = {"value": vol, "points": 10, "reason": "thanh khoản > $10M/24h"}
        else:
            score -= 20; details["volume_24h"] = {"value": vol, "points": -20, "reason": "thanh khoản mỏng < $10M — rủi ro thao túng"}

    fr = ctx.get("funding_rate")
    if fr is not None:
        if abs(fr) > 0.001:  # |0.1%|/8h — thị trường lệch một phía
            score -= 10
            details["funding_rate"] = {"value": fr, "points": -10,
                                       "reason": f"funding {fr:+.4%} lệch mạnh — đòn bẩy một phía, dễ squeeze"}
        else:
            details["funding_rate"] = {"value": fr, "points": 0, "reason": "funding cân bằng"}

    imb = ctx.get("orderbook_imbalance")
    if imb is not None:
        pts = 10 if imb > 0.1 else (-10 if imb < -0.1 else 0)
        score += pts
        details["orderbook_imbalance"] = {"value": imb, "points": pts,
                                          "reason": f"bid/ask imbalance {imb:+.2f}"}

    score = max(0.0, min(100.0, score))
    return FAGate(score=score, passed=score >= 40, details=details, notes=notes)


def compute_fa_gate(asset: AssetType, symbol: str) -> FAGate:
    if asset == AssetType.VN_STOCK:
        from .data import fetch_vn_fundamentals
        return score_vn_fundamentals(fetch_vn_fundamentals(symbol))
    from .data import fetch_crypto_context
    return score_crypto_context(fetch_crypto_context(symbol))
