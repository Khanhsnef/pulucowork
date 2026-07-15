"""Module 2C — Price Action & Smart Money Concepts (SMC).

Quét không look-ahead (pivot chỉ được tính sau k bar xác nhận):
- Market Structure: swing pivots → BOS (Break of Structure) / CHoCH (Change of Character)
- Order Blocks: nến ngược chiều cuối cùng trước cú break, lọc volume (VSA)
- Fair Value Gaps: khoảng mất cân bằng 3 nến, kích thước tối thiểu theo ATR
- Liquidity Pools: cụm đỉnh/đáy bằng nhau (equal highs/lows) — bẫy thanh khoản
- Nến đảo chiều: Pinbar / Engulfing tại key level + xác nhận volume
- VCP (Volatility Contraction Pattern) cho cổ phiếu

Phân tầng vùng giá (multi-tier zones):
- Tier 1 An toàn : retest Order Block (+confluence FVG) thuận cấu trúc
- Tier 2 Tấn công: mua tại vùng quét thanh khoản (liquidity sweep & reclaim)
- Invalidation  : swing được bảo vệ của cấu trúc — đóng cửa qua là hủy kịch bản

Win rate mỗi loại setup được ĐẾM THẬT bằng replay lịch sử (mini-backtest
cùng quy tắc SL-trước-TP như backtester chính), không ước lượng.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

import numpy as np
import pandas as pd

from .indicators import atr as atr_fn


# ─────────────────────────────────────────────────────────────────────────────
# Tham số (phase sau sẽ đưa vào lưới walk-forward optimization)
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class PAParams:
    pivot_k: int = 3            # số bar xác nhận mỗi bên của swing pivot
    fvg_min_atr: float = 0.30   # FVG tối thiểu = 0.3 × ATR14
    ob_vol_mult: float = 1.20   # volume OB/break bar phải > 1.2 × SMA20 volume
    eq_tol_atr: float = 0.15    # dung sai "bằng nhau" của equal highs/lows
    sl_buf_atr: float = 0.50    # đệm SL dưới zone
    tp_r: float = 2.0           # TP mặc định khi replay setup
    max_hold: int = 60          # số bar tối đa giữ 1 setup khi replay
    vcp_contraction: float = 0.75  # mỗi sóng co lại còn <= 75% sóng trước


# ─────────────────────────────────────────────────────────────────────────────
# Cấu trúc dữ liệu
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Pivot:
    index: int
    confirmed_at: int
    price: float
    kind: str               # 'H' | 'L'


@dataclass
class StructureEvent:
    index: int              # bar mà close phá level (thời điểm biết được tín hiệu)
    kind: str               # 'BOS' | 'CHoCH'
    direction: str          # 'up' | 'down'
    level: float            # giá pivot bị phá
    origin_index: int       # index swing gốc của con sóng (protected swing)
    origin_level: float | None


@dataclass
class Zone:
    kind: str               # 'OB' | 'FVG'
    direction: str          # 'bull' | 'bear'
    top: float
    bottom: float
    created_at: int
    volume_ok: bool = True
    mitigated_at: int | None = None    # giá đã quay lại chạm zone
    invalidated_at: int | None = None  # close xuyên thủng zone


@dataclass
class LiquidityPool:
    side: str               # 'above' (buy-side, equal highs) | 'below' (sell-side, equal lows)
    level: float
    n_touches: int
    formed_at: int          # bar xác nhận thành viên cuối
    swept_at: int | None = None


@dataclass
class TierZone:
    name: str               # 'Tier 1 — An toàn' | 'Tier 2 — Tấn công'
    side: str               # 'LONG' | 'SHORT'
    entry: float
    sl: float
    tp1: float
    tp2: float
    rr_tp2: float
    est_win_rate: float | None   # từ replay lịch sử; None nếu không đủ mẫu
    n_setups: int
    basis: str              # diễn giải setup


@dataclass
class PAResult:
    trend: str | None                    # 'up' | 'down' | None
    last_event: dict | None
    events_recent: list[dict]
    n_fresh_bull_ob: int
    n_fresh_bear_ob: int
    n_open_fvg: int
    liquidity_above: list[float]
    liquidity_below: list[float]
    patterns: list[dict]                 # pinbar/engulfing gần đây tại key level
    vcp: dict
    tiers: list[dict]
    invalidation: float | None
    invalidation_note: str
    setup_stats: dict                    # win rate replay từng loại setup
    notes: list[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Swing pivots — xác nhận trễ k bar, không look-ahead
# ─────────────────────────────────────────────────────────────────────────────
def find_pivots(high: np.ndarray, low: np.ndarray, k: int) -> list[Pivot]:
    """Fractal chuẩn: strict hơn mọi bar bên trái, >= mọi bar bên phải.

    Cho phép tie bên phải vì open bar sau thường bằng close bar trước
    (dữ liệu thật lẫn synthetic đều có), strict cả hai phía sẽ bỏ sót pivot.
    """
    n = len(high)
    pivots: list[Pivot] = []
    for i in range(k, n - k):
        if high[i] > high[i - k: i].max() and high[i] >= high[i + 1: i + k + 1].max():
            pivots.append(Pivot(i, i + k, float(high[i]), "H"))
        if low[i] < low[i - k: i].min() and low[i] <= low[i + 1: i + k + 1].min():
            pivots.append(Pivot(i, i + k, float(low[i]), "L"))
    pivots.sort(key=lambda p: (p.confirmed_at, p.index))
    return pivots


# ─────────────────────────────────────────────────────────────────────────────
# Market Structure: BOS / CHoCH
# ─────────────────────────────────────────────────────────────────────────────
def detect_structure(close: np.ndarray, pivots: list[Pivot]) -> list[StructureEvent]:
    """Máy trạng thái chạy tuần tự theo bar — mọi quyết định tại bar i chỉ dùng
    thông tin <= i (pivot phải được xác nhận xong mới tham gia)."""
    by_confirm: dict[int, list[Pivot]] = {}
    for p in pivots:
        by_confirm.setdefault(p.confirmed_at, []).append(p)

    events: list[StructureEvent] = []
    trend: str | None = None
    ref_h: Pivot | None = None   # swing high tham chiếu đang chờ bị phá
    ref_l: Pivot | None = None

    for i in range(len(close)):
        for p in by_confirm.get(i, []):
            if p.kind == "H":
                if ref_h is None or p.index > ref_h.index:
                    ref_h = p
            else:
                if ref_l is None or p.index > ref_l.index:
                    ref_l = p

        c = close[i]
        if ref_h is not None and c > ref_h.price:
            kind = "BOS" if trend in ("up", None) else "CHoCH"
            events.append(StructureEvent(
                index=i, kind=kind, direction="up", level=ref_h.price,
                origin_index=ref_l.index if ref_l else -1,
                origin_level=ref_l.price if ref_l else None))
            trend = "up"
            ref_h = None            # đã tiêu thụ — chờ swing high mới
        elif ref_l is not None and c < ref_l.price:
            kind = "BOS" if trend in ("down", None) else "CHoCH"
            events.append(StructureEvent(
                index=i, kind=kind, direction="down", level=ref_l.price,
                origin_index=ref_h.index if ref_h else -1,
                origin_level=ref_h.price if ref_h else None))
            trend = "down"
            ref_l = None
    return events


# ─────────────────────────────────────────────────────────────────────────────
# Order Blocks & FVG
# ─────────────────────────────────────────────────────────────────────────────
def extract_order_blocks(df_o: np.ndarray, df_h: np.ndarray, df_l: np.ndarray,
                         df_c: np.ndarray, vol: np.ndarray, vol_sma: np.ndarray,
                         events: list[StructureEvent], p: PAParams) -> list[Zone]:
    """OB = nến ngược chiều cuối cùng trước cú break structure."""
    zones: list[Zone] = []
    for ev in events:
        lo_search = max(ev.origin_index, 0) if ev.origin_index >= 0 else max(ev.index - 20, 0)
        found = None
        for j in range(ev.index - 1, lo_search - 1, -1):
            bearish = df_c[j] < df_o[j]
            if (ev.direction == "up" and bearish) or (ev.direction == "down" and not bearish):
                found = j
                break
        if found is None:
            continue
        vsma = vol_sma[found]
        vol_ok = bool(np.isfinite(vsma) and (
            vol[found] >= p.ob_vol_mult * vsma or vol[ev.index] >= p.ob_vol_mult * vol_sma[ev.index]))
        zones.append(Zone(
            kind="OB", direction="bull" if ev.direction == "up" else "bear",
            top=float(df_h[found]), bottom=float(df_l[found]),
            created_at=ev.index, volume_ok=vol_ok))
    return zones


def extract_fvgs(df_h: np.ndarray, df_l: np.ndarray, atr: np.ndarray, p: PAParams) -> list[Zone]:
    zones: list[Zone] = []
    for i in range(2, len(df_h)):
        if not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        gap_up = df_l[i] - df_h[i - 2]
        gap_dn = df_l[i - 2] - df_h[i]
        if gap_up >= p.fvg_min_atr * atr[i]:
            zones.append(Zone("FVG", "bull", float(df_l[i]), float(df_h[i - 2]), i))
        elif gap_dn >= p.fvg_min_atr * atr[i]:
            zones.append(Zone("FVG", "bear", float(df_l[i - 2]), float(df_h[i]), i))
    return zones


def track_zone_status(zones: list[Zone], df_h: np.ndarray, df_l: np.ndarray,
                      df_c: np.ndarray) -> None:
    """Đánh dấu mitigated (giá chạm lại) / invalidated (close xuyên thủng)."""
    n = len(df_c)
    for z in zones:
        for i in range(z.created_at + 1, n):
            if z.direction == "bull":
                if z.mitigated_at is None and df_l[i] <= z.top:
                    z.mitigated_at = i
                if df_c[i] < z.bottom:
                    z.invalidated_at = i
                    break
            else:
                if z.mitigated_at is None and df_h[i] >= z.bottom:
                    z.mitigated_at = i
                if df_c[i] > z.top:
                    z.invalidated_at = i
                    break


# ─────────────────────────────────────────────────────────────────────────────
# Liquidity Pools — equal highs / equal lows
# ─────────────────────────────────────────────────────────────────────────────
def find_liquidity_pools(pivots: list[Pivot], atr: np.ndarray,
                         df_h: np.ndarray, df_l: np.ndarray, p: PAParams) -> list[LiquidityPool]:
    pools: list[LiquidityPool] = []
    for kind, side in (("H", "above"), ("L", "below")):
        ps = [x for x in pivots if x.kind == kind]
        i = 0
        while i < len(ps) - 1:
            cluster = [ps[i]]
            j = i + 1
            while j < len(ps) and ps[j].index - cluster[-1].index <= 60:
                a = atr[ps[j].index] if np.isfinite(atr[ps[j].index]) else 0
                if a > 0 and abs(ps[j].price - cluster[0].price) <= p.eq_tol_atr * a:
                    cluster.append(ps[j])
                j += 1
            if len(cluster) >= 2:
                level = max(x.price for x in cluster) if kind == "H" else min(x.price for x in cluster)
                formed = max(x.confirmed_at for x in cluster)
                pool = LiquidityPool(side=side, level=float(level),
                                     n_touches=len(cluster), formed_at=formed)
                arr = df_h if kind == "H" else df_l
                for t in range(formed + 1, len(arr)):
                    if (kind == "H" and arr[t] > level) or (kind == "L" and arr[t] < level):
                        pool.swept_at = t
                        break
                pools.append(pool)
                i += len(cluster)
            else:
                i += 1
    return pools


# ─────────────────────────────────────────────────────────────────────────────
# Nến đảo chiều tại key level + VSA
# ─────────────────────────────────────────────────────────────────────────────
def detect_reversal_patterns(df_o, df_h, df_l, df_c, vol, vol_sma,
                             key_levels: list[float], atr: np.ndarray,
                             lookback: int = 5) -> list[dict]:
    out = []
    n = len(df_c)
    for i in range(max(1, n - lookback), n):
        a = atr[i] if np.isfinite(atr[i]) else 0
        if a <= 0:
            continue
        near_key = any(abs(df_l[i] - kl) <= 0.5 * a or abs(df_h[i] - kl) <= 0.5 * a
                       for kl in key_levels)
        if not near_key:
            continue
        vsa_ok = bool(np.isfinite(vol_sma[i]) and vol[i] >= 1.5 * vol_sma[i])
        body = abs(df_c[i] - df_o[i])
        rng = df_h[i] - df_l[i]
        if rng <= 0:
            continue
        lower_tail = min(df_o[i], df_c[i]) - df_l[i]
        upper_tail = df_h[i] - max(df_o[i], df_c[i])
        if body <= rng * 0.33 and lower_tail >= 2 * body:
            out.append({"bar": i, "pattern": "Pinbar bull", "vsa_confirm": vsa_ok})
        elif body <= rng * 0.33 and upper_tail >= 2 * body:
            out.append({"bar": i, "pattern": "Pinbar bear", "vsa_confirm": vsa_ok})
        prev_body_hi = max(df_o[i - 1], df_c[i - 1])
        prev_body_lo = min(df_o[i - 1], df_c[i - 1])
        if df_c[i] > df_o[i] and df_o[i] <= prev_body_lo and df_c[i] >= prev_body_hi:
            out.append({"bar": i, "pattern": "Bullish Engulfing", "vsa_confirm": vsa_ok})
        elif df_c[i] < df_o[i] and df_o[i] >= prev_body_hi and df_c[i] <= prev_body_lo:
            out.append({"bar": i, "pattern": "Bearish Engulfing", "vsa_confirm": vsa_ok})
    return out


# ─────────────────────────────────────────────────────────────────────────────
# VCP — Volatility Contraction Pattern
# ─────────────────────────────────────────────────────────────────────────────
def detect_vcp(pivots: list[Pivot], df_c: np.ndarray, vol: np.ndarray, p: PAParams) -> dict:
    ps = sorted(pivots, key=lambda x: x.index)[-8:]
    if len(ps) < 4:
        return {"is_vcp": False}
    swings = []
    for a, b in zip(ps[:-1], ps[1:]):
        if a.kind != b.kind:
            swings.append({"range": abs(b.price - a.price),
                           "vol": float(np.mean(vol[a.index:b.index + 1]))})
    if len(swings) < 3:
        return {"is_vcp": False}
    last3 = swings[-3:]
    contracting = all(last3[k + 1]["range"] <= p.vcp_contraction * last3[k]["range"]
                      for k in range(2))
    vol_declining = last3[-1]["vol"] < last3[0]["vol"]
    pivot_line = max(x.price for x in ps if x.kind == "H")
    near_pivot = df_c[-1] >= 0.93 * pivot_line
    is_vcp = bool(contracting and vol_declining and near_pivot)
    return {"is_vcp": is_vcp, "pivot_line": float(pivot_line) if is_vcp else None,
            "n_contractions": 3 if is_vcp else 0,
            "breakout": bool(is_vcp and df_c[-1] > pivot_line)}


# ─────────────────────────────────────────────────────────────────────────────
# Replay setup lịch sử → win rate thật
# ─────────────────────────────────────────────────────────────────────────────
def _walk_trade(df_o, df_h, df_l, df_c, start: int, entry: float, sl: float,
                tp: float, max_hold: int, side: str = "long") -> bool | None:
    """Trả True=win, False=loss, None=không khớp lệnh. SL ưu tiên trước TP."""
    n = len(df_c)
    filled_at = None
    for i in range(start, min(start + max_hold, n)):
        if side == "long":
            if df_l[i] <= entry:
                filled_at = i
                fill = min(entry, df_o[i])
                break
        else:
            if df_h[i] >= entry:
                filled_at = i
                fill = max(entry, df_o[i])
                break
    if filled_at is None:
        return None
    for i in range(filled_at, min(filled_at + max_hold, n)):
        if side == "long":
            if df_l[i] <= sl:
                return False
            if df_h[i] >= tp:
                return True
        else:
            if df_h[i] >= sl:
                return False
            if df_l[i] <= tp:
                return True
    exit_c = df_c[min(filled_at + max_hold, n) - 1]
    return (exit_c > fill) if side == "long" else (exit_c < fill)


def replay_ob_retest(df_o, df_h, df_l, df_c, obs: list[Zone], atr: np.ndarray,
                     p: PAParams, direction: str) -> tuple[int, float | None]:
    outcomes = []
    for z in obs:
        if z.direction != direction or not z.volume_ok:
            continue
        a = atr[z.created_at] if np.isfinite(atr[z.created_at]) else 0
        if a <= 0:
            continue
        if direction == "bull":
            entry, sl = z.top, z.bottom - p.sl_buf_atr * a
            tp = entry + p.tp_r * (entry - sl)
            r = _walk_trade(df_o, df_h, df_l, df_c, z.created_at + 1, entry, sl, tp,
                            p.max_hold, "long")
        else:
            entry, sl = z.bottom, z.top + p.sl_buf_atr * a
            tp = entry - p.tp_r * (sl - entry)
            r = _walk_trade(df_o, df_h, df_l, df_c, z.created_at + 1, entry, sl, tp,
                            p.max_hold, "short")
        if r is not None:
            outcomes.append(r)
    n = len(outcomes)
    return n, (sum(outcomes) / n if n else None)


def replay_sweep_reclaim(df_o, df_h, df_l, df_c, pools: list[LiquidityPool],
                         atr: np.ndarray, p: PAParams, side: str) -> tuple[int, float | None]:
    """side='below' → long sau khi quét equal lows; side='above' → short sau khi quét equal highs."""
    outcomes = []
    n = len(df_c)
    for pool in pools:
        if pool.side != side or pool.swept_at is None:
            continue
        j = pool.swept_at
        a = atr[j] if np.isfinite(atr[j]) else 0
        if a <= 0 or j + 1 >= n:
            continue
        if side == "below" and df_c[j] > pool.level:          # sweep & reclaim
            entry = df_o[j + 1]
            sl = df_l[j] - 0.25 * a
            if entry <= sl:
                continue
            tp = entry + p.tp_r * (entry - sl)
            r = _walk_trade(df_o, df_h, df_l, df_c, j + 1, entry, sl, tp, p.max_hold, "long")
        elif side == "above" and df_c[j] < pool.level:
            entry = df_o[j + 1]
            sl = df_h[j] + 0.25 * a
            if sl <= entry:
                continue
            tp = entry - p.tp_r * (sl - entry)
            r = _walk_trade(df_o, df_h, df_l, df_c, j + 1, entry, sl, tp, p.max_hold, "short")
        else:
            continue
        if r is not None:
            outcomes.append(r)
    m = len(outcomes)
    return m, (sum(outcomes) / m if m else None)


# ─────────────────────────────────────────────────────────────────────────────
# Phân tầng vùng giá
# ─────────────────────────────────────────────────────────────────────────────
def _build_tiers(df_c, atr_last: float, trend: str | None, last_close: float,
                 fresh_obs: list[Zone], open_fvgs: list[Zone],
                 pools: list[LiquidityPool], protected: float | None,
                 stats: dict, p: PAParams) -> list[TierZone]:
    tiers: list[TierZone] = []
    if trend not in ("up", "down") or atr_last <= 0:
        return tiers
    side = "LONG" if trend == "up" else "SHORT"

    if trend == "up":
        cands = [z for z in fresh_obs if z.direction == "bull" and z.top < last_close]
        cands.sort(key=lambda z: -z.top)   # zone gần giá nhất
        tps_above = sorted([x.level for x in pools if x.side == "above"
                            and x.swept_at is None and x.level > last_close])
        tp1_default = tps_above[0] if tps_above else last_close + 2 * atr_last
        if cands:
            z = cands[0]
            confl = any(f.direction == "bull" and f.invalidated_at is None
                        and not (f.top < z.bottom - 0.3 * atr_last or f.bottom > z.top + 0.3 * atr_last)
                        for f in open_fvgs)
            entry = z.top
            sl = min(z.bottom, protected if protected is not None else z.bottom) - p.sl_buf_atr * atr_last
            tp2 = max(entry + p.tp_r * (entry - sl), tp1_default)
            n, wr = stats.get("ob_retest_bull", (0, None))
            tiers.append(TierZone(
                name="Tier 1 — An toàn", side=side, entry=round(entry, 4),
                sl=round(sl, 4), tp1=round(tp1_default, 4), tp2=round(tp2, 4),
                rr_tp2=round((tp2 - entry) / (entry - sl), 2) if entry > sl else 0.0,
                est_win_rate=wr, n_setups=n,
                basis="Retest Order Block bull" + (" + confluence FVG" if confl else "") + " thuận BOS"))
        pool_below = sorted([x for x in pools if x.side == "below" and x.swept_at is None
                             and x.level < last_close], key=lambda x: -x.level)
        if pool_below:
            lv = pool_below[0].level
            entry = lv - 0.05 * atr_last
            sl = entry - 0.75 * atr_last
            tp2 = max(entry + p.tp_r * (entry - sl), tp1_default)
            n, wr = stats.get("sweep_reclaim_long", (0, None))
            tiers.append(TierZone(
                name="Tier 2 — Tấn công", side=side, entry=round(entry, 4),
                sl=round(sl, 4), tp1=round(tp1_default, 4), tp2=round(tp2, 4),
                rr_tp2=round((tp2 - entry) / (entry - sl), 2),
                est_win_rate=wr, n_setups=n,
                basis=f"Sweep thanh khoản equal lows @ {lv:.2f} rồi reclaim"))
    else:  # downtrend — zones cho SHORT (crypto) / tín hiệu thoát với VN stock
        cands = [z for z in fresh_obs if z.direction == "bear" and z.bottom > last_close]
        cands.sort(key=lambda z: z.bottom)
        tps_below = sorted([x.level for x in pools if x.side == "below"
                            and x.swept_at is None and x.level < last_close], reverse=True)
        tp1_default = tps_below[0] if tps_below else last_close - 2 * atr_last
        if cands:
            z = cands[0]
            entry = z.bottom
            sl = max(z.top, protected if protected is not None else z.top) + p.sl_buf_atr * atr_last
            tp2 = min(entry - p.tp_r * (sl - entry), tp1_default)
            n, wr = stats.get("ob_retest_bear", (0, None))
            tiers.append(TierZone(
                name="Tier 1 — An toàn", side=side, entry=round(entry, 4),
                sl=round(sl, 4), tp1=round(tp1_default, 4), tp2=round(tp2, 4),
                rr_tp2=round((entry - tp2) / (sl - entry), 2) if sl > entry else 0.0,
                est_win_rate=wr, n_setups=n,
                basis="Retest Order Block bear thuận BOS xuống"))
    return tiers


# ─────────────────────────────────────────────────────────────────────────────
# API chính
# ─────────────────────────────────────────────────────────────────────────────
def scan_price_action(df: pd.DataFrame, params: PAParams = PAParams()) -> PAResult:
    """Quét toàn bộ Price Action/SMC trên OHLCV daily. Trả PAResult JSON-able."""
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    l = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    v = df["volume"].to_numpy(float)
    atr = atr_fn(df["high"], df["low"], df["close"], 14).to_numpy(float)
    vol_sma = pd.Series(v).rolling(20).mean().to_numpy(float)
    n = len(c)
    notes: list[str] = []

    pivots = find_pivots(h, l, params.pivot_k)
    events = detect_structure(c, pivots)
    trend = events[-1].direction if events else None
    protected = events[-1].origin_level if events else None

    obs = extract_order_blocks(o, h, l, c, v, vol_sma, events, params)
    fvgs = extract_fvgs(h, l, atr, params)
    track_zone_status(obs, h, l, c)
    track_zone_status(fvgs, h, l, c)
    pools = find_liquidity_pools(pivots, atr, h, l, params)

    fresh_obs = [z for z in obs if z.invalidated_at is None and z.mitigated_at is None]
    open_fvgs = [z for z in fvgs if z.invalidated_at is None]

    key_levels = ([z.top for z in fresh_obs] + [z.bottom for z in fresh_obs]
                  + [x.level for x in pools if x.swept_at is None]
                  + ([protected] if protected else []))
    patterns = detect_reversal_patterns(o, h, l, c, v, vol_sma, key_levels, atr)
    vcp = detect_vcp(pivots, c, v, params)

    # Replay lịch sử → win rate thật cho từng loại setup
    stats = {
        "ob_retest_bull": replay_ob_retest(o, h, l, c, obs, atr, params, "bull"),
        "ob_retest_bear": replay_ob_retest(o, h, l, c, obs, atr, params, "bear"),
        "sweep_reclaim_long": replay_sweep_reclaim(o, h, l, c, pools, atr, params, "below"),
        "sweep_reclaim_short": replay_sweep_reclaim(o, h, l, c, pools, atr, params, "above"),
    }

    atr_last = float(atr[-1]) if np.isfinite(atr[-1]) else 0.0
    tiers = _build_tiers(c, atr_last, trend, float(c[-1]), fresh_obs, open_fvgs,
                         pools, protected, stats, params)
    if not tiers and trend:
        notes.append("Không có zone fresh phù hợp gần giá — chờ pullback về OB/FVG mới.")

    if trend == "up":
        inv_note = (f"Đóng cửa dưới {protected:.2f} → cấu trúc tăng bị phá (CHoCH), hủy mọi kịch bản LONG."
                    if protected else "Chưa xác định được swing bảo vệ.")
    elif trend == "down":
        inv_note = (f"Đóng cửa trên {protected:.2f} → cấu trúc giảm bị phá (CHoCH), hủy kịch bản SHORT/đứng ngoài."
                    if protected else "Chưa xác định được swing bảo vệ.")
    else:
        inv_note = "Chưa đủ dữ liệu cấu trúc."

    ev_recent = [asdict(e) for e in events[-6:]]
    last_ev = asdict(events[-1]) if events else None

    return PAResult(
        trend=trend,
        last_event=last_ev,
        events_recent=ev_recent,
        n_fresh_bull_ob=sum(1 for z in fresh_obs if z.direction == "bull"),
        n_fresh_bear_ob=sum(1 for z in fresh_obs if z.direction == "bear"),
        n_open_fvg=len(open_fvgs),
        liquidity_above=[round(x.level, 4) for x in pools
                         if x.side == "above" and x.swept_at is None][:5],
        liquidity_below=[round(x.level, 4) for x in pools
                         if x.side == "below" and x.swept_at is None][:5],
        patterns=patterns,
        vcp=vcp,
        tiers=[asdict(t) for t in tiers],
        invalidation=round(protected, 4) if protected else None,
        invalidation_note=inv_note,
        setup_stats={k: {"n": s[0], "win_rate": round(s[1], 4) if s[1] is not None else None}
                     for k, s in stats.items()},
        notes=notes,
    )
