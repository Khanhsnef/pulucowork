"""Module 3 — Backtest engine + Walk-Forward Optimization (lõi hệ thống).

Engine mô phỏng long-only trên numpy array:
- Vào lệnh tại giá open của bar KẾ TIẾP sau tín hiệu (không look-ahead).
- SL = entry - k*ATR, TP = entry + R*(entry - SL); kiểm tra SL trước TP nếu cùng bar.
- Ràng buộc T+n (VN: không được bán trước khi cổ phiếu về tài khoản).
- Chi phí mua/bán tách riêng (VN có thuế bán 0.1%).

Walk-forward: Train 24 tháng tìm params → Test 6 tháng out-of-sample → trượt.
Chỉ chấp nhận bộ params ổn định qua nhiều fold (chống overfitting).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .config import (
    CostModel,
    MarketConstraints,
    WalkForwardConfig,
    DEFAULT_PARAM_GRID,
)


# ─────────────────────────────────────────────────────────────────────────────
# Kết quả
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class BacktestResult:
    params: dict
    n_trades: int
    win_rate: float          # tỷ lệ lệnh có lãi sau chi phí
    total_return: float      # lợi nhuận gộp trên equity
    sharpe: float            # annualized, trên daily returns của equity
    sortino: float
    max_drawdown: float      # số âm, ví dụ -0.18
    profit_factor: float
    avg_r_multiple: float    # trung bình R thu được mỗi lệnh
    trades: pd.DataFrame | None = None   # chi tiết từng lệnh (entry/exit/lý do)

    def score(self) -> float:
        """Hàm mục tiêu tổng hợp để xếp hạng params.

        Không tối ưu win-rate đơn thuần (dễ ra hệ thống TP nhỏ SL to);
        cân bằng Sharpe + win rate + kiểm soát drawdown, phạt ít mẫu.
        """
        if self.n_trades < 5:
            return -np.inf
        sample_penalty = min(1.0, self.n_trades / 20)
        return (self.sharpe * 0.5 + self.win_rate * 2.0 + self.max_drawdown * 1.0) * sample_penalty


@dataclass
class FoldResult:
    fold_id: int
    train_range: tuple[str, str]
    test_range: tuple[str, str]
    best_train_params: dict
    train_metrics: BacktestResult
    test_metrics: BacktestResult | None   # None nếu test không đủ giao dịch


@dataclass
class OptimResult:
    best_params: dict
    stability: float                 # % folds mà best_params nằm trong top quartile
    folds: list[FoldResult]
    oos_win_rate: float              # win rate gộp TẤT CẢ lệnh out-of-sample
    oos_n_trades: int
    oos_sharpe: float
    full_backtest: BacktestResult    # chạy best_params trên toàn bộ lịch sử (để đếm setup)
    warnings: list[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Sinh tín hiệu vào lệnh từ params
# ─────────────────────────────────────────────────────────────────────────────
def build_entry_signals(feats: pd.DataFrame, close: pd.Series, params: dict) -> pd.Series:
    """Tín hiệu MUA: RSI cắt LÊN ngưỡng quá bán (mean-reversion có xác nhận).

    trend_filter=True → chỉ vào lệnh khi close > SMA200 và ADX > 20
    (mua điều chỉnh trong uptrend, tránh bắt dao rơi trong downtrend).
    """
    r = feats[f"rsi_{params['rsi_period']}"]
    cross_up = (r > params["rsi_entry"]) & (r.shift(1) <= params["rsi_entry"])
    if params.get("trend_filter", False):
        cross_up &= (close > feats["sma_200"]) & (feats["adx_14"] > 20)
    return cross_up.fillna(False)


# ─────────────────────────────────────────────────────────────────────────────
# Engine mô phỏng — numpy loop, một vị thế tại một thời điểm
# ─────────────────────────────────────────────────────────────────────────────
def run_backtest(
    df: pd.DataFrame,
    feats: pd.DataFrame,
    params: dict,
    costs: CostModel,
    constraints: MarketConstraints,
    keep_trades: bool = False,
) -> BacktestResult:
    """Mô phỏng: tín hiệu bar t → vào lệnh giá open bar t+1 → thoát bởi SL/TP/RSI-70.

    Mọi số học trên numpy array để tốc độ đủ nhanh cho grid search
    (~400 combos × 1300 bars < 2s).
    """
    entries = build_entry_signals(feats, df["close"], params).to_numpy()
    o = df["open"].to_numpy(dtype=float)
    h = df["high"].to_numpy(dtype=float)
    l = df["low"].to_numpy(dtype=float)
    c = df["close"].to_numpy(dtype=float)
    atr_arr = feats["atr_14"].to_numpy(dtype=float)
    rsi_exit_arr = feats[f"rsi_{params['rsi_period']}"].to_numpy(dtype=float)

    n = len(df)
    k_sl = params["atr_sl_mult"]
    r_tp = params["tp_r_multiple"]
    t_plus = constraints.settlement_bars

    in_pos = False
    entry_price = sl = tp = 0.0
    entry_i = -1
    equity = 1.0
    equity_curve = np.ones(n)
    trades: list[dict] = []

    i = 0
    while i < n - 1:
        if not in_pos:
            if entries[i] and np.isfinite(atr_arr[i]) and atr_arr[i] > 0:
                # vào lệnh tại open bar kế tiếp
                entry_i = i + 1
                entry_price = o[entry_i] * (1 + costs.buy_cost)
                risk = k_sl * atr_arr[i]
                sl = o[entry_i] - risk
                tp = o[entry_i] + r_tp * risk
                in_pos = True
                i = entry_i
                equity_curve[i] = equity
                i += 1
                continue
        else:
            bars_held = i - entry_i
            exit_price = None
            reason = None
            can_sell = bars_held > t_plus  # VN: bán được từ bar thứ t_plus+1 sau khi mua

            if can_sell:
                if l[i] <= sl:                       # SL ưu tiên trước TP (giả định bảo thủ)
                    exit_price = min(o[i], sl)       # gap-down qua SL → khớp giá mở cửa
                    reason = "SL"
                elif h[i] >= tp:
                    exit_price = max(o[i], tp)       # gap-up qua TP → khớp giá mở cửa
                    reason = "TP"
                elif rsi_exit_arr[i] >= 70:          # thoát kỹ thuật: RSI quá mua
                    exit_price = c[i]
                    reason = "RSI_70"

            if exit_price is not None:
                exit_net = exit_price * (1 - costs.sell_cost)
                ret = exit_net / entry_price - 1
                equity *= (1 + ret)
                risk_pct = (o[entry_i] - sl) / o[entry_i]
                trades.append({
                    "entry_idx": entry_i, "exit_idx": i,
                    "entry_price": entry_price, "exit_price": exit_net,
                    "return": ret, "r_multiple": ret / risk_pct if risk_pct > 0 else 0.0,
                    "bars_held": i - entry_i, "reason": reason,
                })
                in_pos = False

        equity_curve[i] = equity if not in_pos else equity * (c[i] * (1 - costs.sell_cost) / entry_price)
        i += 1

    # đóng vị thế treo cuối kỳ theo giá close cuối
    if in_pos:
        exit_net = c[-1] * (1 - costs.sell_cost)
        ret = exit_net / entry_price - 1
        equity *= (1 + ret)
        risk_pct = (o[entry_i] - sl) / o[entry_i]
        trades.append({
            "entry_idx": entry_i, "exit_idx": n - 1,
            "entry_price": entry_price, "exit_price": exit_net,
            "return": ret, "r_multiple": ret / risk_pct if risk_pct > 0 else 0.0,
            "bars_held": n - 1 - entry_i, "reason": "EOD",
        })
    equity_curve[-1] = equity

    return _metrics(trades, equity_curve, params, df.index, keep_trades)


def _metrics(trades: list[dict], equity_curve: np.ndarray, params: dict,
             index: pd.Index, keep_trades: bool) -> BacktestResult:
    n_trades = len(trades)
    if n_trades == 0:
        return BacktestResult(params, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                              trades=pd.DataFrame() if keep_trades else None)

    rets = np.array([t["return"] for t in trades])
    wins = rets > 0
    gross_profit = rets[wins].sum()
    gross_loss = -rets[~wins].sum()

    daily = pd.Series(equity_curve, index=index).pct_change().dropna()
    ann = np.sqrt(252)
    sharpe = float(daily.mean() / daily.std() * ann) if daily.std() > 0 else 0.0
    downside = daily[daily < 0]
    sortino = float(daily.mean() / downside.std() * ann) if len(downside) > 1 and downside.std() > 0 else 0.0
    peak = np.maximum.accumulate(equity_curve)
    max_dd = float((equity_curve / peak - 1).min())

    trades_df = None
    if keep_trades:
        trades_df = pd.DataFrame(trades)
        trades_df["entry_date"] = index[trades_df["entry_idx"]]
        trades_df["exit_date"] = index[trades_df["exit_idx"]]

    return BacktestResult(
        params=params,
        n_trades=n_trades,
        win_rate=float(wins.mean()),
        total_return=float(equity_curve[-1] - 1),
        sharpe=sharpe,
        sortino=sortino,
        max_drawdown=max_dd,
        profit_factor=float(gross_profit / gross_loss) if gross_loss > 0 else np.inf,
        avg_r_multiple=float(np.mean([t["r_multiple"] for t in trades])),
        trades=trades_df,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Grid search trên một đoạn dữ liệu (train window)
# ─────────────────────────────────────────────────────────────────────────────
def grid_search(
    df: pd.DataFrame,
    feats: pd.DataFrame,
    costs: CostModel,
    constraints: MarketConstraints,
    param_grid: dict[str, list] | None = None,
) -> list[BacktestResult]:
    """Chạy toàn bộ tổ hợp tham số, trả về danh sách kết quả đã sắp theo score giảm dần."""
    grid = param_grid or DEFAULT_PARAM_GRID
    keys = list(grid.keys())
    results = []
    for combo in itertools.product(*grid.values()):
        params = dict(zip(keys, combo))
        results.append(run_backtest(df, feats, params, costs, constraints))
    results.sort(key=lambda r: r.score(), reverse=True)
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Walk-Forward Optimization
# ─────────────────────────────────────────────────────────────────────────────
def walk_forward_optimize(
    df: pd.DataFrame,
    feats: pd.DataFrame,
    costs: CostModel,
    constraints: MarketConstraints,
    param_grid: dict[str, list] | None = None,
    wf: WalkForwardConfig = WalkForwardConfig(),
) -> OptimResult:
    """Quy trình chống overfitting 3 lớp:

    1. Mỗi fold: grid search trên TRAIN → lấy best params → đo trên TEST (out-of-sample).
    2. Bộ params cuối = bộ xuất hiện trong top-quartile TRAIN ở nhiều fold nhất
       (ổn định qua thời gian > tốt nhất một giai đoạn).
    3. OOS win rate gộp mọi lệnh test — con số DUY NHẤT được báo cho user.
    """
    warnings: list[str] = []
    n = len(df)
    if n < constraints.min_history_bars:
        warnings.append(f"Chỉ có {n} bars < {constraints.min_history_bars} — kết quả tham khảo, KHÔNG đủ tin cậy.")

    folds: list[FoldResult] = []
    param_top_counts: dict[tuple, int] = {}
    oos_trades_rets: list[float] = []
    oos_daily_rets: list[pd.Series] = []

    fold_id = 0
    start = 0
    while start + wf.train_bars + wf.test_bars <= n:
        tr_slice = slice(start, start + wf.train_bars)
        te_slice = slice(start + wf.train_bars, start + wf.train_bars + wf.test_bars)
        df_tr, feats_tr = df.iloc[tr_slice], feats.iloc[tr_slice]
        df_te, feats_te = df.iloc[te_slice], feats.iloc[te_slice]

        ranked = grid_search(df_tr, feats_tr, costs, constraints, param_grid)
        valid = [r for r in ranked if r.n_trades >= wf.min_trades_per_fold]
        if not valid:
            start += wf.step_bars
            fold_id += 1
            continue

        best = valid[0]
        # đếm tần suất lọt top-quartile để đo độ ổn định
        q = max(1, len(valid) // 4)
        for r in valid[:q]:
            key = tuple(sorted(r.params.items()))
            param_top_counts[key] = param_top_counts.get(key, 0) + 1

        test_res = run_backtest(df_te, feats_te, best.params, costs, constraints, keep_trades=True)
        if test_res.n_trades > 0 and test_res.trades is not None:
            oos_trades_rets.extend(test_res.trades["return"].tolist())

        folds.append(FoldResult(
            fold_id=fold_id,
            train_range=(str(df_tr.index[0].date()), str(df_tr.index[-1].date())),
            test_range=(str(df_te.index[0].date()), str(df_te.index[-1].date())),
            best_train_params=best.params,
            train_metrics=best,
            test_metrics=test_res if test_res.n_trades >= 1 else None,
        ))
        start += wf.step_bars
        fold_id += 1

    if not folds:
        raise ValueError("Không đủ dữ liệu để chạy walk-forward (cần >= train+test bars).")

    # bộ params ổn định nhất qua các fold
    n_folds_counted = len(folds)
    best_key, best_count = max(param_top_counts.items(), key=lambda kv: kv[1])
    stability = best_count / n_folds_counted
    best_params = dict(best_key)

    if stability < wf.stability_threshold:
        warnings.append(
            f"Params tốt nhất chỉ ổn định ở {stability:.0%} folds "
            f"(< ngưỡng {wf.stability_threshold:.0%}) — thị trường đổi chế độ, giảm tin cậy."
        )

    # OOS gộp
    oos_rets = np.array(oos_trades_rets)
    oos_n = len(oos_rets)
    oos_wr = float((oos_rets > 0).mean()) if oos_n else 0.0
    if oos_n < 10:
        warnings.append(f"Chỉ {oos_n} lệnh out-of-sample — KHÔNG đủ mẫu thống kê (cần >= 10).")

    # sharpe OOS xấp xỉ từ chuỗi return các lệnh test (per-trade, không phải daily)
    oos_sharpe = float(oos_rets.mean() / oos_rets.std() * np.sqrt(max(oos_n, 1))) if oos_n > 1 and oos_rets.std() > 0 else 0.0

    full_bt = run_backtest(df, feats, best_params, costs, constraints, keep_trades=True)

    return OptimResult(
        best_params=best_params,
        stability=stability,
        folds=folds,
        oos_win_rate=oos_wr,
        oos_n_trades=oos_n,
        oos_sharpe=oos_sharpe,
        full_backtest=full_bt,
        warnings=warnings,
    )
