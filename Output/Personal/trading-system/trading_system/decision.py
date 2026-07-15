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
    chart_data: dict = field(default_factory=dict)   # OHLCV 12 tháng cho web UI (nến + volume)
    price_action: dict = field(default_factory=dict) # PAResult: BOS/CHoCH, OB/FVG, liquidity, tiers, invalidation
    technical_rating: dict = field(default_factory=dict)  # gauge kiểu TV Technicals: votes từng chỉ báo
    technical_rating: dict = field(default_factory=dict) # Kết quả votes của đồng hồ tín hiệu
    insights: list[str] = field(default_factory=list) # Nhận định chuyên sâu về xu hướng và hợp lưu
    volume_pressure: dict = field(default_factory=dict) # Lực mua/bán dựa trên volume nến tăng/giảm trong 14 ngày


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


def _technical_rating(df: pd.DataFrame, feats: pd.DataFrame) -> dict:
    """Đồng hồ tín hiệu kiểu TradingView Technicals: mỗi chỉ báo bỏ 1 phiếu
    MUA/BÁN/TRUNG LẬP, tổng hợp thành rating -1..+1."""
    c = float(df["close"].iloc[-1])
    f = feats.iloc[-1]
    votes: list[dict] = []

    def vote(name, val, sig):
        votes.append({"name": name, "value": val, "signal": sig})

    rsi = float(f["rsi_14"])
    vote("RSI(14)", round(rsi, 1), "MUA" if rsi < 30 else ("BÁN" if rsi > 70 else "TRUNG LẬP"))
    vote("MACD", round(float(f["macd_hist"]), 4),
         "MUA" if f["macd_hist"] > 0 else "BÁN")
    k = float(f["stoch_k"]) if pd.notna(f["stoch_k"]) else 50.0
    vote("Stochastic %K", round(k, 1), "MUA" if k < 20 else ("BÁN" if k > 80 else "TRUNG LẬP"))
    if pd.notna(f["sma_50"]):
        vote("SMA50", round(float(f["sma_50"]), 2), "MUA" if c > f["sma_50"] else "BÁN")
    if pd.notna(f["sma_200"]):
        vote("SMA200", round(float(f["sma_200"]), 2), "MUA" if c > f["sma_200"] else "BÁN")
    if pd.notna(f["bb_mid"]):
        vote("Bollinger mid", round(float(f["bb_mid"]), 2), "MUA" if c > f["bb_mid"] else "BÁN")
    adx = float(f["adx_14"]) if pd.notna(f["adx_14"]) else 0.0
    if adx > 25:
        trend_sig = "MUA" if (pd.notna(f["sma_50"]) and c > f["sma_50"]) else "BÁN"
        vote("ADX(14) trend", round(adx, 1), trend_sig)
    else:
        vote("ADX(14) trend", round(adx, 1), "TRUNG LẬP")
    vote("OBV slope", round(float(f["obv_slope"]), 0) if pd.notna(f["obv_slope"]) else 0,
         "MUA" if f["obv_slope"] > 0 else "BÁN")

    n_buy = sum(1 for v in votes if v["signal"] == "MUA")
    n_sell = sum(1 for v in votes if v["signal"] == "BÁN")
    n_neutral = len(votes) - n_buy - n_sell
    score = (n_buy - n_sell) / max(1, len(votes))   # -1..+1
    label = ("MUA MẠNH" if score >= 0.5 else "MUA" if score >= 0.15 else
             "BÁN MẠNH" if score <= -0.5 else "BÁN" if score <= -0.15 else "TRUNG LẬP")
    return {"score": round(score, 3), "label": label,
            "n_buy": n_buy, "n_sell": n_sell, "n_neutral": n_neutral, "votes": votes}


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

    # Price Action / SMC scan (không chặn pipeline nếu lỗi)
    from dataclasses import asdict as _asdict
    from .price_action import scan_price_action
    try:
        pa = _asdict(scan_price_action(df))
    except Exception as e:
        pa = {"error": f"PA scan failed: {e}"}

    # tín hiệu hiện tại theo best params?
    entry_now = bool(build_entry_signals(feats, df["close"], p).iloc[-1])
    rsi_now = float(feats[f"rsi_{p['rsi_period']}"].iloc[-1])
    near_oversold = rsi_now <= p["rsi_entry"] + 5

    # ── Logic khuyến nghị ────────────────────────────────────────────────
    # MUA: có tín hiệu (hoặc RSI sát vùng mua) + FA pass + OOS win rate >= 50% + đủ mẫu
    # BÁN: đang quá mua (RSI > 70) và trend trung hạn GIẢM
    # còn lại: ĐỨNG NGOÀI
    # Price Action làm bộ lọc xác nhận: cấu trúc cùng chiều → nâng conviction,
    # ngược chiều (CHoCH chống lại lệnh) → hạ conviction một bậc.
    oos_ok = optim.oos_win_rate >= 0.5 and optim.oos_n_trades >= 10
    mid_trend = trends[1].direction
    pa_trend = pa.get("trend")

    if (entry_now or near_oversold) and fa.passed and oos_ok:
        rec = "MUA"
        conviction = "CAO" if (entry_now and optim.stability >= 0.6 and fa.score >= 60) else "TRUNG BÌNH"
        if pa_trend == "down":
            conviction = "THẤP" if conviction == "TRUNG BÌNH" else "TRUNG BÌNH"
        elif pa_trend == "up" and conviction == "TRUNG BÌNH" and optim.stability >= 0.6:
            conviction = "CAO"
    elif rsi_now >= 70 and mid_trend == "GIẢM":
        rec, conviction = "BÁN", "TRUNG BÌNH"
        if pa_trend == "down":
            conviction = "CAO"
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

    # ── Phân tích Chuyên Sâu (Insights & Confluence) ──────────────────────────
    insights = []
    f_last = feats.iloc[-1]
    f_prev = feats.iloc[-2] if len(feats) >= 2 else f_last
    ema9_last, ema21_last = float(f_last.get("ema_9", 0)), float(f_last.get("ema_21", 0))
    ema9_prev, ema21_prev = float(f_prev.get("ema_9", 0)), float(f_prev.get("ema_21", 0))
    
    if ema9_last > ema21_last:
        if ema9_prev <= ema21_prev:
            insights.append("EMA 9 vừa cắt LÊN EMA 21: Tín hiệu đảo chiều tăng ngắn hạn (EMA Golden Cross).")
        else:
            insights.append("Xu hướng ngắn hạn TĂNG: EMA 9 nằm trên EMA 21 duy trì đà tăng giá ngắn hạn.")
    else:
        if ema9_prev >= ema21_prev:
            insights.append("⚠️ EMA 9 vừa cắt XUỐNG EMA 21: Tín hiệu đảo chiều giảm ngắn hạn (EMA Death Cross).")
        else:
            insights.append("Xu hướng ngắn hạn GIẢM: EMA 9 nằm dưới EMA 21 duy trì đà giảm giá ngắn hạn.")
            
    sma200 = float(f_last.get("sma_200", 0)) if pd.notna(f_last.get("sma_200")) else 0
    if sma200 > 0:
        if last > sma200:
            insights.append(f"Bệ đỡ dài hạn: Giá nằm trên SMA 200 ({last:,.2f} > {sma200:,.2f}) xác nhận xu hướng tăng dài hạn vững chắc.")
        else:
            insights.append(f"⚠️ Áp lực dài hạn: Giá nằm dưới SMA 200 ({last:,.2f} < {sma200:,.2f}) cảnh báo xu hướng giảm dài hạn chi phối.")
            
    fib = fibonacci_retracements(df["close"])
    poc = volume_profile_poc(df["close"].iloc[-252:], df["volume"].iloc[-252:])
    
    confluences = []
    for k, v in fib.items():
        if k.startswith("fib_") and abs(v - poc) / poc < 0.012:
            confluences.append(f"{k.replace('fib_', 'Fib ')} ({v:,.2f})")
            
    if confluences:
        insights.append(f"🎯 Vùng hợp lưu mạnh: Mức POC tập trung volume ({poc:,.2f}) hội tụ sát với {', '.join(confluences)}, củng cố vùng hỗ trợ/kháng cự cực kỳ vững chắc.")
    else:
        insights.append(f"Mốc hỗ trợ/kháng cự tĩnh: POC (Point of Control) giao dịch nhiều nhất nằm ở {poc:,.2f}.")
        
    rsi_val = float(f_last.get(f"rsi_{p['rsi_period']}", 50))
    if rsi_val <= p["rsi_entry"]:
        insights.append(f"🔥 Điểm mua hấp dẫn: RSI({p['rsi_period']}) đạt {rsi_val:.1f} đi vào vùng quá bán (oversold), tăng cao xác suất phục hồi.")
    elif rsi_val >= 70:
        insights.append(f"⚠️ Đề phòng rung lắc: RSI({p['rsi_period']}) chạm {rsi_val:.1f} quá mua (overbought), có khả năng xuất hiện nhịp điều chỉnh ngắn hạn.")

    # ── Tính toán Lực Mua / Lực Bán (Volume Pressure) trong 14 ngày ──
    tail_vol = df.tail(14)
    buy_v = 0.0
    sell_v = 0.0
    if len(tail_vol) > 0:
        c_vals = tail_vol["close"].to_numpy()
        o_vals = tail_vol["open"].to_numpy()
        v_vals = tail_vol["volume"].to_numpy()
        for idx in range(len(c_vals)):
            vol_val = float(v_vals[idx]) if pd.notna(v_vals[idx]) else 0.0
            if pd.isna(c_vals[idx]) or pd.isna(o_vals[idx]):
                continue
            if c_vals[idx] > o_vals[idx]:
                buy_v += vol_val
            elif c_vals[idx] < o_vals[idx]:
                sell_v += vol_val
            else:
                buy_v += vol_val * 0.5
                sell_v += vol_val * 0.5
                
    tot_v = buy_v + sell_v
    buy_pct = round(buy_v / tot_v * 100.0, 1) if tot_v > 0 else 50.0
    sell_pct = round(100.0 - buy_pct, 1) if tot_v > 0 else 50.0
    vol_press = {
        "buy_pct": buy_pct,
        "sell_pct": sell_pct,
        "buy_vol": round(buy_v, 1),
        "sell_vol": round(sell_v, 1)
    }

    # Bổ sung insights về cấu trúc thị trường SMC
    if pa and not pa.get("error"):
        pa_trend = pa.get("trend")
        if pa_trend == "up":
            insights.append("Cấu trúc SMC: Xu hướng tăng (Bullish Structure) được duy trì nhờ các cú BOS liên tục.")
        elif pa_trend == "down":
            insights.append("⚠️ Cấu trúc SMC: Xu hướng giảm (Bearish Structure) chi phối với các cấu trúc phá vỡ đi xuống.")
            
        last_ev = pa.get("last_event")
        if last_ev:
            kind = last_ev.get("kind")
            dir_str = "TĂNG" if last_ev.get("direction") == "up" else "GIẢM"
            insights.append(f"Sự kiện SMC gần nhất: Xuất hiện cấu trúc {kind} {dir_str} tại mức giá {float(last_ev.get('level', 0)):,.2f}.")
            
        inv_val = pa.get("invalidation")
        if inv_val:
            insights.append(f"Ngưỡng vô hiệu hóa: Kịch bản hiện tại sẽ bị hủy nếu giá đóng cửa vượt qua mức {inv_val:,.2f}.")

    # Bổ sung insights về volume pressure
    if buy_pct > 58.0:
        insights.append(f"Lượng mua áp đảo: Khối lượng phiên tăng chiếm {buy_pct}% tổng volume 14 ngày qua, thể hiện lực mua chủ động chiếm ưu thế.")
    elif sell_pct > 58.0:
        insights.append(f"⚠️ Áp lực bán lớn: Khối lượng phiên giảm chiếm {sell_pct}% tổng volume 14 ngày qua, thể hiện lực bán chủ động áp đảo.")
    else:
        insights.append(f"Cân bằng cung cầu: Lực mua ({buy_pct}%) và lực bán ({sell_pct}%) dao động trong biên độ cân bằng 14 ngày qua.")

    # tính đồng hồ tín hiệu kỹ thuật
    tech_rating = _technical_rating(df, feats)

    # dữ liệu chart 12 tháng cho web UI — OHLCV đầy đủ để vẽ nến + volume
    tail = df.iloc[-252:]
    tail_feats = feats.iloc[-252:]
    chart_data = {
        "dates": [d.strftime("%Y-%m-%d") for d in tail.index],
        "opens": [round(float(v), 4) for v in tail["open"]],
        "highs": [round(float(v), 4) for v in tail["high"]],
        "lows": [round(float(v), 4) for v in tail["low"]],
        "closes": [round(float(v), 4) for v in tail["close"]],
        "volumes": [round(float(v), 2) for v in tail["volume"]],
        "ma20": [round(float(v), 4) if pd.notna(v) else None for v in tail_feats["sma_20"]],
        "ma50": [round(float(v), 4) if pd.notna(v) else None for v in tail_feats["sma_50"]],
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
        price_action=pa,
        technical_rating=tech_rating,
        insights=insights,
        volume_pressure=vol_press,
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

    pa = d.price_action
    if pa and not pa.get("error"):
        trend_vn = {"up": "TĂNG (bullish structure)", "down": "GIẢM (bearish structure)"}.get(pa.get("trend"), "Chưa rõ")
        lines += ["", "## Price Action & Smart Money Concepts",
                  f"- **Cấu trúc thị trường:** {trend_vn}"]
        if pa.get("last_event"):
            ev = pa["last_event"]
            lines.append(f"- **Sự kiện gần nhất:** {ev['kind']} {'lên' if ev['direction'] == 'up' else 'xuống'} "
                         f"tại mức {ev['level']:,.2f}")
        lines.append(f"- **Order Blocks fresh:** {pa.get('n_fresh_bull_ob', 0)} bull / "
                     f"{pa.get('n_fresh_bear_ob', 0)} bear · **FVG còn mở:** {pa.get('n_open_fvg', 0)}")
        if pa.get("liquidity_above") or pa.get("liquidity_below"):
            la = ", ".join(f"{x:,.2f}" for x in pa.get("liquidity_above", [])) or "—"
            lb = ", ".join(f"{x:,.2f}" for x in pa.get("liquidity_below", [])) or "—"
            lines.append(f"- **Liquidity pools:** trên {la} · dưới {lb}")
        if pa.get("vcp", {}).get("is_vcp"):
            lines.append(f"- **VCP:** đang co thắt, pivot line {pa['vcp']['pivot_line']:,.2f}"
                         + (" — **ĐÃ BREAKOUT**" if pa["vcp"].get("breakout") else ""))
        for pt in pa.get("patterns", []):
            lines.append(f"- **Nến đảo chiều:** {pt['pattern']}"
                         + (" +VSA volume xác nhận" if pt.get("vsa_confirm") else " (volume chưa xác nhận)"))

        if pa.get("tiers"):
            lines += ["", "### Kịch bản hành động phân lớp (Multi-tier Zones)",
                      "| Tier | Hướng | Entry | SL | TP1 | TP2 | R:R | Win rate lịch sử |",
                      "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :--- |"]
            for t in pa["tiers"]:
                wr = f"{t['est_win_rate']:.0%} ({t['n_setups']} setup)" if t.get("est_win_rate") is not None \
                     else f"chưa đủ mẫu ({t.get('n_setups', 0)} setup)"
                lines.append(f"| {t['name']} | {t['side']} | {t['entry']:,.2f} | {t['sl']:,.2f} "
                             f"| {t['tp1']:,.2f} | {t['tp2']:,.2f} | {t['rr_tp2']} | {wr} |")
            for t in pa["tiers"]:
                lines.append(f"- *{t['name']}*: {t['basis']}")
        if pa.get("invalidation"):
            lines += ["", f"⛔ **Invalidation:** {pa['invalidation_note']}"]

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
