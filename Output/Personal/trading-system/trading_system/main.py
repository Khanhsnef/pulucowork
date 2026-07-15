"""Entry point: analyze('FPT') hoặc analyze('BTCUSDT') → báo cáo đầy đủ.

CLI:  python -m trading_system.main FPT
      python -m trading_system.main BTCUSDT --years 4 --json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .backtester import walk_forward_optimize
from .config import (
    AssetType,
    RiskConfig,
    get_cost_model,
    get_market_constraints,
)
from .data import clean_ohlcv, fetch_crypto_ohlcv, fetch_vn_ohlcv, route_asset
from .decision import Decision, make_decision, render_json, render_markdown
from .fa import compute_fa_gate
from .indicators import compute_ta_features

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def analyze(
    symbol: str,
    lookback_years: int = 5,
    verbose: bool = True,
    progress: "callable | None" = None,
) -> Decision:
    """Pipeline đầy đủ: route → ingest → clean → TA + FA → walk-forward → decision.

    progress: callback (step:int, total:int, message:str) — dùng cho web UI/batch.
    """
    def log(msg: str, step: int = 0):
        if verbose:
            print(msg, file=sys.stderr)
        if progress is not None:
            progress(step, 5, msg)

    asset = route_asset(symbol)
    log(f"[1/5] {symbol} → {asset.value}. Đang tải dữ liệu ({lookback_years} năm)...", 1)

    if asset == AssetType.VN_STOCK:
        raw = fetch_vn_ohlcv(symbol, lookback_years)
    else:
        raw = fetch_crypto_ohlcv(symbol, "1d", lookback_years)

    df, clean_log = clean_ohlcv(raw)
    log(f"[2/5] {len(df)} bars sạch." + (f" Cleaning: {'; '.join(clean_log)}" if clean_log else ""), 2)

    feats = compute_ta_features(df)
    log("[3/5] TA features xong. Đang lấy FA...", 3)
    fa = compute_fa_gate(asset, symbol)
    log(f"      FA score: {fa.score:.0f}/100 ({'PASS' if fa.passed else 'FAIL'})", 3)

    log("[4/5] Walk-forward optimization (grid search từng fold — mất 1-3 phút)...", 4)
    optim = walk_forward_optimize(
        df, feats,
        costs=get_cost_model(asset),
        constraints=get_market_constraints(asset),
    )
    log(f"      Best params: {optim.best_params} | stability {optim.stability:.0%} "
        f"| OOS: {optim.oos_n_trades} lệnh, win {optim.oos_win_rate:.0%}", 4)

    log("[5/5] Sinh khuyến nghị...", 5)
    risk = RiskConfig() if asset == AssetType.VN_STOCK else RiskConfig(initial_capital=10_000.0)
    return make_decision(symbol, asset, df, feats, fa, optim, risk)


def main():
    ap = argparse.ArgumentParser(description="Automated Trading Analysis & Optimization System")
    ap.add_argument("symbol", help="Mã VN (FPT, HPG) hoặc cặp Binance (BTCUSDT)")
    ap.add_argument("--years", type=int, default=5, help="Số năm dữ liệu lịch sử (mặc định 5)")
    ap.add_argument("--json", action="store_true", help="In JSON thay vì Markdown")
    ap.add_argument("--save", action="store_true", help="Lưu báo cáo vào reports/")
    args = ap.parse_args()

    decision = analyze(args.symbol.upper(), lookback_years=args.years)
    output = render_json(decision) if args.json else render_markdown(decision)
    print(output)

    if args.save:
        REPORTS_DIR.mkdir(exist_ok=True)
        from datetime import datetime
        stamp = datetime.now().strftime("%Y-%m-%d")
        ext = "json" if args.json else "md"
        path = REPORTS_DIR / f"{stamp}-{args.symbol.lower()}-analysis.{ext}"
        path.write_text(output, encoding="utf-8")
        print(f"\n💾 Đã lưu: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
