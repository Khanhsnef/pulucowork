"""Smoke test trên dữ liệu synthetic — verify engine trước khi dùng dữ liệu thật.

Chạy: python -m tests.test_smoke  (từ thư mục gốc project)
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from trading_system.backtester import grid_search, run_backtest, walk_forward_optimize
from trading_system.config import (
    CRYPTO_CONSTRAINTS,
    CRYPTO_COSTS,
    VN_CONSTRAINTS,
    VN_COSTS,
    WalkForwardConfig,
)
from trading_system.data import clean_ohlcv, route_asset
from trading_system.config import AssetType
from trading_system.indicators import compute_ta_features


def make_synthetic_ohlcv(n: int = 1500, seed: int = 42) -> pd.DataFrame:
    """Random walk có drift nhẹ + chu kỳ, đủ dài cho walk-forward."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2020-01-01", periods=n)
    drift = 0.0003
    cycle = 0.002 * np.sin(np.arange(n) / 40)
    rets = rng.normal(drift, 0.018, n) + cycle
    close = 100 * np.exp(np.cumsum(rets))
    intr = rng.uniform(0.005, 0.02, n)
    open_ = close * (1 + rng.normal(0, 0.004, n))
    high = np.maximum(open_, close) * (1 + intr)
    low = np.minimum(open_, close) * (1 - intr)
    volume = rng.uniform(1e5, 5e6, n)
    return pd.DataFrame({"open": open_, "high": high, "low": low,
                         "close": close, "volume": volume}, index=dates)


def test_router():
    assert route_asset("FPT") == AssetType.VN_STOCK
    assert route_asset("HPG") == AssetType.VN_STOCK
    assert route_asset("BTCUSDT") == AssetType.CRYPTO
    assert route_asset("ETHUSDT") == AssetType.CRYPTO
    try:
        route_asset("INVALID123XYZ")
        raise AssertionError("phải raise ValueError")
    except ValueError:
        pass
    print("✅ router OK")


def test_cleaning():
    df = make_synthetic_ohlcv(600)
    # tiêm lỗi: giá âm, high<low, spike
    df.iloc[10, df.columns.get_loc("close")] = -5
    hi = df.iloc[20]["high"]
    df.iloc[20, df.columns.get_loc("high")] = df.iloc[20]["low"] - 1
    clean, log = clean_ohlcv(df)
    assert (clean[["open", "high", "low", "close"]] > 0).all().all()
    assert (clean["high"] >= clean["low"]).all()
    assert len(log) >= 1
    print(f"✅ cleaning OK — {log}")


def test_backtest_no_lookahead_and_tplus():
    df = make_synthetic_ohlcv()
    feats = compute_ta_features(df)
    params = {"rsi_period": 14, "rsi_entry": 35, "atr_sl_mult": 2.0,
              "tp_r_multiple": 2.0, "trend_filter": False}

    res_vn = run_backtest(df, feats, params, VN_COSTS, VN_CONSTRAINTS, keep_trades=True)
    assert res_vn.n_trades > 0, "phải có giao dịch trên 1500 bars"
    # T+2: mọi lệnh VN phải giữ > 2 bars
    assert (res_vn.trades["bars_held"] > VN_CONSTRAINTS.settlement_bars).all(), \
        "vi phạm T+2!"
    # entry luôn ở bar SAU tín hiệu → không có lệnh entry tại bar 0
    assert (res_vn.trades["entry_idx"] > 0).all()

    res_cx = run_backtest(df, feats, params, CRYPTO_COSTS, CRYPTO_CONSTRAINTS, keep_trades=True)
    assert res_cx.n_trades >= res_vn.n_trades * 0.5, "crypto không bị khóa T+n, số lệnh không thể quá ít"
    print(f"✅ backtest OK — VN: {res_vn.n_trades} lệnh (win {res_vn.win_rate:.0%}), "
          f"Crypto: {res_cx.n_trades} lệnh (win {res_cx.win_rate:.0%})")


def test_costs_reduce_returns():
    """Chi phí phải làm giảm lợi nhuận — sanity check dấu."""
    from trading_system.config import CostModel, MarketConstraints
    df = make_synthetic_ohlcv()
    feats = compute_ta_features(df)
    params = {"rsi_period": 14, "rsi_entry": 35, "atr_sl_mult": 2.0,
              "tp_r_multiple": 2.0, "trend_filter": False}
    free = CostModel(commission=0.0, slippage=0.0, sell_tax=0.0)
    nc = MarketConstraints(settlement_bars=0)
    r_free = run_backtest(df, feats, params, free, nc)
    r_cost = run_backtest(df, feats, params, VN_COSTS, nc)
    assert r_free.total_return > r_cost.total_return, "chi phí phải ăn mòn lợi nhuận"
    print(f"✅ cost model OK — free: {r_free.total_return:+.1%} vs có phí: {r_cost.total_return:+.1%}")


def test_grid_and_walkforward():
    df = make_synthetic_ohlcv(1500)
    feats = compute_ta_features(df)
    small_grid = {
        "rsi_period": [10, 14],
        "rsi_entry": [30, 40],
        "atr_sl_mult": [2.0, 3.0],
        "tp_r_multiple": [2.0],
        "trend_filter": [False],
    }
    import time
    t0 = time.time()
    ranked = grid_search(df, feats, VN_COSTS, VN_CONSTRAINTS, small_grid)
    t_grid = time.time() - t0
    assert len(ranked) == 8
    assert ranked[0].score() >= ranked[-1].score()

    t0 = time.time()
    optim = walk_forward_optimize(df, feats, VN_COSTS, VN_CONSTRAINTS, small_grid,
                                  WalkForwardConfig(train_bars=504, test_bars=126, step_bars=126))
    t_wf = time.time() - t0
    assert optim.best_params
    assert len(optim.folds) >= 3
    print(f"✅ grid ({len(ranked)} combos, {t_grid:.1f}s) + walk-forward "
          f"({len(optim.folds)} folds, {t_wf:.1f}s) OK — "
          f"OOS: {optim.oos_n_trades} lệnh, win {optim.oos_win_rate:.0%}, "
          f"stability {optim.stability:.0%}")
    if optim.warnings:
        print(f"   ⚠️ {optim.warnings}")


def test_decision_report():
    from trading_system.decision import make_decision, render_json, render_markdown
    from trading_system.fa import FAGate
    df = make_synthetic_ohlcv(1500)
    feats = compute_ta_features(df)
    small_grid = {"rsi_period": [14], "rsi_entry": [30, 40], "atr_sl_mult": [2.0],
                  "tp_r_multiple": [2.0], "trend_filter": [False]}
    optim = walk_forward_optimize(df, feats, VN_COSTS, VN_CONSTRAINTS, small_grid)
    fa = FAGate(score=65.0, passed=True, details={}, notes=["synthetic test"])
    d = make_decision("TEST", AssetType.VN_STOCK, df, feats, fa, optim)
    md = render_markdown(d)
    js = render_json(d)
    assert d.recommendation in ("MUA", "BÁN", "ĐỨNG NGOÀI")
    assert "Khuyến nghị" in md
    import json as _json
    _json.loads(js)  # JSON hợp lệ
    if d.recommendation == "MUA":
        assert d.zones is not None
        assert d.zones.sl < d.zones.entry_low < d.zones.tp1 <= d.zones.tp2
    print(f"✅ decision OK — {d.recommendation} ({d.conviction}), zones: {d.zones is not None}")


if __name__ == "__main__":
    test_router()
    test_cleaning()
    test_backtest_no_lookahead_and_tplus()
    test_costs_reduce_returns()
    test_grid_and_walkforward()
    test_decision_report()
    print("\n🎉 Tất cả smoke tests PASS")
