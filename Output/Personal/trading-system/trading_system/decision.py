"""Module 4 — Decision Engine & Report Generator.

Tổng hợp TA + FA + kết quả walk-forward thành khuyến nghị hành động:
MUA / BÁN / ĐỨNG NGOÀI + Entry Zone + TP1/TP2 + SL (ATR-based) + Win Rate lịch sử.
Xuất JSON và Markdown.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime

import pandas as pd

from .backtester import OptimResult, build_entry_signals
from .config import AssetType, RiskConfig
from .fa import FAGate
from .indicators import fibonacci_retracements, volume_profile_poc


@dataclass
class TrendView:
    horizon: str        # "1-2 tuần" | "1-3 tháng" | "3-12 tháng"
    direction: str      # TĂNG | GIẢM | ĐI NGANG
    evidence: list[str]


@dataclass
class PriceZones:
    entry_low: float
    entry_high: float
    tp1: float
    tp2: float
    sl: float
    sl_basis: str       # diễn giải "entry - k×ATR(14)"
    position_size_pct: float   # % NAV theo risk 2%/lệnh


@dataclass
class Decision:
    symbol: str
    asset_type: str
    generated_at: str
    last_price: float
    recommendation: str          # MUA | BÁN | ĐỨNG NGOÀI
    conviction: str              # CAO | TRUNG BÌNH | THẤP
    trends: list[TrendView]
    zones: PriceZones | None     # None nếu ĐỨNG NGOÀI
    win_rate_statement: str      # "Setup xuất hiện X lần trong N năm, thắng Y%"
    oos_win_rate: float
    oos_n_trades: int
    best_params: dict
    fa_score: float
    fa_notes: list[str]
    warnings: list[str]
    fold_summary: list[dict] = field(default_factory=list)
    chart_data: dict = field(default_factory=dict)   # {dates: [...], closes: [...]} 12 tháng cho web UI


# ─────────────────────────────────────────────────────────────────────────────
def _assess_trends(df: pd.DataFrame, feats: pd.DataFrame) -> list[TrendView]:
    c = df["close"]
    last = float(c.iloc[-1])
    f = feats.iloc[-1]
    views = []

    # Ngắn hạn 1-2 tuần: MACD hist + RSI14 + vị trí so với BB mid
    ev = []
    short_score = 0
    if f["macd_hist"] > 0: short_score += 1; ev.append("MACD histogram dương")
    else: short_score -= 1; ev.append("MACD histogram âm")
    if f["rsi_14"] > 50: short_score += 1; ev.append(f"RSI14 = {f['rsi_14']:.0f} > 50")
    else: short_score -= 1; ev.append(f"RSI14 = {f['rsi_14']:.0f} < 50")
    if last > f["bb_mid"]: short_score += 1; ev.append("giá trên BB middle")
    else: short_score -= 1; ev.append("giá dưới BB middle")
    views.append(TrendView("Ngắn hạn (1-2 tuần)",
                           "TĂNG" if short_score >= 2 else ("GIẢM" if short_score <= -2 else "ĐI NGANG"), ev))

    # Trung hạn 1-3 tháng: SMA50 + ADX + OBV slope
    ev = []
    mid_score = 0
    if last > f["sma_50"]: mid_score += 1; ev.append("giá trên SMA50")
    else: mid_score -= 1; ev.append("giá dưới SMA50")
    if f["adx_14"] > 25:
        trending_up = last > f["sma_50"]
        mid_score += 1 if trending_up else -1
        ev.append(f"ADX = {f['adx_14']:.0f} — trend mạnh")
    else:
        ev.append(f"ADX = {f['adx_14']:.0f} — trend yếu")
    if f["obv_slope"] > 0: mid_score += 1; ev.append("OBV tăng 20 phiên (dòng tiền vào)")
    else: mid_score -= 1; ev.append("OBV giảm 20 phiên (dòng tiền ra)")
    views.append(TrendView("Trung hạn (1-3 tháng)",
                           "TĂNG" if mid_score >= 2 else ("GIẢM" if mid_score <= -2 else "ĐI NGANG"), ev))

    # Dài hạn 3-12 tháng: SMA200 + cấu trúc swing
    ev = []
    long_score = 0
    if pd.notna(f["sma_200"]):
        if last > f["sma_200"]: long_score += 2; ev.append("giá trên SMA200")
        else: long_score -= 2; ev.append("giá dưới SMA200")
    else:
        ev.append("chưa đủ 200 phiên dữ liệu")
    ret_12m = float(c.iloc[-1] / c.iloc[-min(252, len(c))] - 1)
    if ret_12m > 0.10: long_score += 1; ev.append(f"hiệu suất 12 tháng {ret_12m:+.0%}")
    elif ret_12m < -0.10: long_score -= 1; ev.append(f"hiệu suất 12 tháng {ret_12m:+.0%}")
    views.append(TrendView("Dài hạn (3-12 tháng)",
                           "TĂNG" if long_score >= 2 else ("GIẢM" if long_score <= -2 else "ĐI NGANG"), ev))
    return views


def _count_similar_setups(optim: OptimResult, df: pd.DataFrame) -> tuple[str, int, float]:
    """Đếm setup giống hệt trong toàn bộ lịch sử từ full backtest — trả về câu phát biểu."""
    bt = optim.full_backtest
    years = max(1, round((df.index[-1] - df.index[0]).days / 365))
    if bt.n_trades == 0:
        return ("Setup chưa từng xuất hiện đủ điều kiện trong lịch sử — không có thống kê.", 0, 0.0)
    stmt = (f"Setup này xuất hiện {bt.n_trades} lần trong {years} năm qua, "
            f"tỷ lệ thắng {bt.win_rate:.0%} (avg {bt.avg_r_multiple:+.2f}R/lệnh). "
            f"Out-of-sample: {optim.oos_n_trades} lệnh, thắng {optim.oos_win_rate:.0%}.")
    return stmt, bt.n_trades, bt.win_rate


def make_decision(
    symbol: str,
    asset: AssetType,
    df: pd.DataFrame,
    feats: pd.DataFrame,
    fa: FAGate,
    optim: OptimResult,
    risk: RiskConfig = RiskConfig(),
) -> Decision:
    last = float(df["close"].iloc[-1])
    atr14 = float(feats["atr_14"].iloc[-1])
    p = optim.best_params
    trends = _assess_trends(df, feats)
    wr_stmt, _, _ = _count_similar_setups(optim, df)

    # tín hiệu hiện tại theo best params?
    entry_now = bool(build_entry_signals(feats, df["close"], p).iloc[-1])
    rsi_now = float(feats[f"rsi_{p['rsi_period']}"].iloc[-1])
    near_oversold = rsi_now <= p["rsi_entry"] + 5

    # ── Logic khuyến nghị ────────────────────────────────────────────────
    # MUA: có tín hiệu (hoặc RSI sát vùng mua) + FA pass + OOS win rate >= 50% + đủ mẫu
    # BÁN: đang quá mua (RSI > 70) và trend trung hạn GIẢM
    # còn lại: ĐỨNG NGOÀI
    oos_ok = optim.oos_win_rate >= 0.5 and optim.oos_n_trades >= 10
    mid_trend = trends[1].direction

    if (entry_now or near_oversold) and fa.passed and oos_ok:
        rec = "MUA"
        conviction = "CAO" if (entry_now and optim.stability >= 0.6 and fa.score >= 60) else "TRUNG BÌNH"
    elif rsi_now >= 70 and mid_trend == "GIẢM":
        rec, conviction = "BÁN", "TRUNG BÌNH"
    else:
        rec, conviction = "ĐỨNG NGOÀI", "CAO" if not oos_ok else "TRUNG BÌNH"

    # ── Price zones (chỉ khi MUA) ────────────────────────────────────────
    zones = None
    if rec == "MUA":
        fib = fibonacci_retracements(df["close"])
        poc = volume_profile_poc(df["close"].iloc[-252:], df["volume"].iloc[-252:])
        # Entry zone: quanh giá hiện tại, neo xuống hỗ trợ gần nhất (fib/POC dưới giá)
        supports = [v for k, v in fib.items() if k.startswith("fib_") and v < last] + ([poc] if poc < last else [])
        entry_low = max(supports) if supports else last - 0.5 * atr14
        entry_low = min(entry_low, last)  # không cao hơn giá hiện tại
        entry_high = last * 1.005
        risk_amount = p["atr_sl_mult"] * atr14
        sl = entry_low - risk_amount
        tp1 = entry_high + p["tp_r_multiple"] * risk_amount * 0.5
        tp2 = entry_high + p["tp_r_multiple"] * risk_amount
        sl_pct = (entry_high - sl) / entry_high
        pos_pct = min(risk.risk_per_trade / sl_pct, risk.max_position_pct)
        zones = PriceZones(
            entry_low=round(entry_low, 2), entry_high=round(entry_high, 2),
            tp1=round(tp1, 2), tp2=round(tp2, 2), sl=round(sl, 2),
            sl_basis=f"entry − {p['atr_sl_mult']}×ATR(14) = −{risk_amount:.2f} ({sl_pct:.1%} dưới entry)",
            position_size_pct=round(pos_pct, 4),
        )

    # dữ liệu chart 12 tháng cho web UI (downsample còn ~250 điểm)
    tail = df.iloc[-252:]
    chart_data = {
        "dates": [d.strftime("%Y-%m-%d") for d in tail.index],
        "closes": [round(float(v), 4) for v in tail["close"]],
    }

    fold_summary = [
        {
            "fold": f.fold_id,
            "test_range": f"{f.test_range[0]} → {f.test_range[1]}",
            "test_trades": f.test_metrics.n_trades if f.test_metrics else 0,
            "test_win_rate": round(f.test_metrics.win_rate, 3) if f.test_metrics else None,
        }
        for f in optim.folds
    ]

    return Decision(
        symbol=symbol,
        asset_type=asset.value,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        last_price=last,
        recommendation=rec,
        conviction=conviction,
        trends=trends,
        zones=zones,
        win_rate_statement=wr_stmt,
        oos_win_rate=round(optim.oos_win_rate, 4),
        oos_n_trades=optim.oos_n_trades,
        best_params=p,
        fa_score=fa.score,
        fa_notes=fa.notes + [d.get("reason", "") for d in fa.details.values() if isinstance(d, dict)],
        warnings=optim.warnings,
        fold_summary=fold_summary,
        chart_data=chart_data,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Render
# ─────────────────────────────────────────────────────────────────────────────
def render_json(d: Decision) -> str:
    return json.dumps(asdict(d), ensure_ascii=False, indent=2, default=str)


def render_markdown(d: Decision) -> str:
    lines = [
        f"# Báo cáo Phân tích: {d.symbol} ({d.asset_type})",
        f"*Tạo lúc: {d.generated_at} — Giá hiện tại: {d.last_price:,.2f}*",
        "",
        f"## 🎯 Khuyến nghị: **{d.recommendation}** (độ tin cậy: {d.conviction})",
        "",
        f"> {d.win_rate_statement}",
        "",
        "## Nhận định Xu hướng",
        "| Khung | Xu hướng | Bằng chứng |",
        "| :--- | :--- | :--- |",
    ]
    for t in d.trends:
        lines.append(f"| {t.horizon} | **{t.direction}** | {'; '.join(t.evidence)} |")

    if d.zones:
        z = d.zones
        lines += [
            "",
            "## Mốc Giá Hành Động",
            "| Mốc | Giá | Ghi chú |",
            "| :--- | ---: | :--- |",
            f"| Entry Zone | {z.entry_low:,.2f} – {z.entry_high:,.2f} | neo theo Fib/POC hỗ trợ gần nhất |",
            f"| TP 1 | {z.tp1:,.2f} | chốt 50% vị thế |",
            f"| TP 2 | {z.tp2:,.2f} | chốt phần còn lại |",
            f"| **SL bắt buộc** | **{z.sl:,.2f}** | {z.sl_basis} |",
            f"| Position size | {z.position_size_pct:.1%} NAV | risk 2%/lệnh theo khoảng SL |",
        ]

    lines += [
        "",
        "## Tham số Tối ưu (Walk-Forward)",
        f"- Bộ tham số: `{d.best_params}`",
        f"- Out-of-sample: **{d.oos_n_trades} lệnh, win rate {d.oos_win_rate:.0%}**",
        f"- FA score: {d.fa_score:.0f}/100",
    ]
    if d.fold_summary:
        lines += ["", "### Kết quả từng fold (out-of-sample)",
                  "| Fold | Giai đoạn test | Số lệnh | Win rate |", "| ---: | :--- | ---: | ---: |"]
        for f in d.fold_summary:
            wr = f"{f['test_win_rate']:.0%}" if f["test_win_rate"] is not None else "—"
            lines.append(f"| {f['fold']} | {f['test_range']} | {f['test_trades']} | {wr} |")

    if d.warnings:
        lines += ["", "## ⚠️ Cảnh báo"] + [f"- {w}" for w in d.warnings]

    lines += ["", "---", "*Hệ thống hỗ trợ quyết định — không phải khuyến nghị đầu tư. "
              "Win rate quá khứ không đảm bảo kết quả tương lai.*"]
    return "\n".join(lines)
