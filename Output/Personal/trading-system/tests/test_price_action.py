"""Tests cho Price Action module — synthetic patterns có kết quả biết trước.

Chạy: python3 -m tests.test_price_action
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from trading_system.price_action import (
    PAParams,
    detect_structure,
    extract_fvgs,
    find_liquidity_pools,
    find_pivots,
    scan_price_action,
    _walk_trade,
)


def _mk_df(closes, spread=0.5, vol=None):
    c = np.asarray(closes, dtype=float)
    n = len(c)
    o = np.concatenate([[c[0]], c[:-1]])
    h = np.maximum(o, c) + spread
    l = np.minimum(o, c) - spread
    v = np.asarray(vol, dtype=float) if vol is not None else np.full(n, 1e6)
    idx = pd.bdate_range("2023-01-02", periods=n)
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": v}, index=idx)


def test_pivots_no_lookahead():
    """Pivot chỉ được confirm sau k bar — confirmed_at > index."""
    rng = np.random.default_rng(7)
    c = 100 + np.cumsum(rng.normal(0, 1, 300))
    df = _mk_df(c)
    piv = find_pivots(df["high"].to_numpy(), df["low"].to_numpy(), k=3)
    assert len(piv) > 5
    assert all(p.confirmed_at == p.index + 3 for p in piv)
    print(f"✅ pivots OK — {len(piv)} pivots, tất cả confirm trễ k=3 bar")


def test_structure_uptrend_bos():
    """Chuỗi higher-highs/higher-lows rõ ràng → BOS hướng lên, không có CHoCH."""
    # zigzag đi lên: 100→110→105→115→110→120→115→125...
    legs = []
    base = 100.0
    for i in range(6):
        legs += list(np.linspace(base, base + 10, 8))       # sóng lên
        legs += list(np.linspace(base + 10, base + 5, 6))   # điều chỉnh nông
        base += 5
    df = _mk_df(legs, spread=0.2)
    piv = find_pivots(df["high"].to_numpy(), df["low"].to_numpy(), 3)
    events = detect_structure(df["close"].to_numpy(), piv)
    assert len(events) >= 2, "phải phát hiện được structure break"
    ups = [e for e in events if e.direction == "up"]
    assert len(ups) >= 2
    assert events[-1].direction == "up"
    print(f"✅ structure OK — {len(events)} events, "
          f"{sum(1 for e in events if e.kind == 'BOS')} BOS / "
          f"{sum(1 for e in events if e.kind == 'CHoCH')} CHoCH, trend cuối: up")


def test_choch_on_reversal():
    """Uptrend rồi sập mạnh → phải có CHoCH direction=down."""
    legs = []
    base = 100.0
    for i in range(4):
        legs += list(np.linspace(base, base + 10, 8))
        legs += list(np.linspace(base + 10, base + 5, 6))
        base += 5
    legs += list(np.linspace(base, base - 30, 25))          # sập xuyên swing lows
    df = _mk_df(legs, spread=0.2)
    piv = find_pivots(df["high"].to_numpy(), df["low"].to_numpy(), 3)
    events = detect_structure(df["close"].to_numpy(), piv)
    downs = [e for e in events if e.direction == "down"]
    assert downs, "phải có structure break xuống"
    assert downs[0].kind == "CHoCH", f"break xuống đầu tiên phải là CHoCH, got {downs[0].kind}"
    print(f"✅ CHoCH OK — đảo chiều được đánh dấu CHoCH đúng")


def test_fvg_detection():
    """Gap 3 nến rõ ràng → FVG bull."""
    c = list(np.linspace(100, 102, 30))
    c += [110, 111, 112]           # gap mạnh lên
    c += list(np.linspace(112, 113, 30))
    df = _mk_df(c, spread=0.3)
    atr = np.full(len(c), 1.0)
    fvgs = extract_fvgs(df["high"].to_numpy(), df["low"].to_numpy(), atr, PAParams())
    bulls = [z for z in fvgs if z.direction == "bull"]
    assert bulls, "phải phát hiện FVG bull sau gap"
    print(f"✅ FVG OK — {len(bulls)} bull FVG")


def test_equal_lows_liquidity():
    """Hai đáy bằng nhau → sell-side liquidity pool phía dưới."""
    c = (list(np.linspace(100, 90, 15)) + list(np.linspace(90, 100, 15))
         + list(np.linspace(100, 90.2, 15)) + list(np.linspace(90.2, 105, 20)))
    df = _mk_df(c, spread=0.2)
    piv = find_pivots(df["high"].to_numpy(), df["low"].to_numpy(), 3)
    atr = np.full(len(c), 2.0)
    pools = find_liquidity_pools(piv, atr, df["high"].to_numpy(), df["low"].to_numpy(),
                                 PAParams())
    below = [p for p in pools if p.side == "below"]
    assert below, "phải phát hiện equal lows"
    assert below[0].n_touches >= 2
    print(f"✅ liquidity OK — pool dưới @ {below[0].level:.1f} ({below[0].n_touches} chạm)")


def test_walk_trade_sl_first():
    """Bar chạm cả SL lẫn TP → tính SL (bảo thủ)."""
    o = np.array([100.0, 100, 100, 100])
    h = np.array([101.0, 101, 120, 101])   # bar 2 chạm TP
    l = np.array([99.0, 95, 94, 99])       # bar 1&2 chạm entry, bar 2 chạm cả SL
    c = np.array([100.0, 96, 100, 100])
    r = _walk_trade(o, h, l, c, start=1, entry=96, sl=94.5, tp=110, max_hold=10, side="long")
    assert r is False, "bar chạm cả SL và TP phải tính là loss"
    print("✅ walk_trade OK — SL ưu tiên trước TP")


def test_full_scan_real_shape():
    """Scan end-to-end trên random walk — không crash, JSON-able, cấu trúc đủ field."""
    rng = np.random.default_rng(11)
    rets = rng.normal(0.0005, 0.02, 800)
    c = 100 * np.exp(np.cumsum(rets))
    vol = rng.uniform(5e5, 5e6, 800)
    df = _mk_df(c, spread=0.4, vol=vol)
    res = scan_price_action(df)
    import json
    from dataclasses import asdict
    js = json.dumps(asdict(res), ensure_ascii=False)  # phải serialize được
    assert res.trend in ("up", "down", None)
    assert isinstance(res.setup_stats, dict) and "ob_retest_bull" in res.setup_stats
    for t in res.tiers:
        if t["side"] == "LONG":
            assert t["sl"] < t["entry"], "LONG: SL phải dưới entry"
            assert t["tp2"] > t["entry"], "LONG: TP phải trên entry"
    print(f"✅ full scan OK — trend={res.trend}, {len(res.tiers)} tiers, "
          f"OB fresh: {res.n_fresh_bull_ob}B/{res.n_fresh_bear_ob}S, "
          f"stats: { {k: v for k, v in res.setup_stats.items()} }")


if __name__ == "__main__":
    test_pivots_no_lookahead()
    test_structure_uptrend_bos()
    test_choch_on_reversal()
    test_fvg_detection()
    test_equal_lows_liquidity()
    test_walk_trade_sl_first()
    test_full_scan_real_shape()
    print("\n🎉 Price Action tests PASS")
