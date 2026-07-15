"""Cấu hình hệ thống: cost model, ràng buộc thị trường, lưới tham số tối ưu."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AssetType(str, Enum):
    VN_STOCK = "VN_STOCK"
    CRYPTO = "CRYPTO"


@dataclass(frozen=True)
class CostModel:
    """Chi phí giao dịch một chiều (tỷ lệ trên giá trị lệnh)."""

    commission: float          # phí môi giới / taker fee
    slippage: float            # trượt giá ước tính
    sell_tax: float = 0.0      # thuế bán (VN: 0.1% trên giá trị bán)

    @property
    def buy_cost(self) -> float:
        return self.commission + self.slippage

    @property
    def sell_cost(self) -> float:
        return self.commission + self.slippage + self.sell_tax


@dataclass(frozen=True)
class MarketConstraints:
    """Ràng buộc vi cấu trúc thị trường — hard-code vào backtest để tránh Win Rate ảo."""

    settlement_bars: int = 0        # T+n: số phiên phải giữ tối thiểu sau khi mua (VN: 2)
    daily_price_limit: float | None = None  # biên độ trần/sàn (HOSE: 7%) — None nếu không có
    lot_size: int = 1               # lô giao dịch tối thiểu (HOSE: 100)
    allow_short: bool = False       # VN stock không short được
    min_history_bars: int = 500     # tối thiểu số bar để backtest có ý nghĩa


VN_COSTS = CostModel(commission=0.0015, slippage=0.001, sell_tax=0.001)
CRYPTO_COSTS = CostModel(commission=0.001, slippage=0.0005, sell_tax=0.0)

VN_CONSTRAINTS = MarketConstraints(
    settlement_bars=2,          # T+2.5: cổ phiếu về tài khoản chiều T+2, bán được từ T+3 → giữ tối thiểu 2 bar, bán từ bar thứ 3
    daily_price_limit=0.07,
    lot_size=100,
    allow_short=False,
)
CRYPTO_CONSTRAINTS = MarketConstraints(
    settlement_bars=0,
    daily_price_limit=None,
    lot_size=1,
    allow_short=False,          # phase 1: long-only cho cả hai để so sánh công bằng
)


@dataclass(frozen=True)
class RiskConfig:
    """Khẩu vị rủi ro đã chốt với user: risk 1-2% NAV mỗi lệnh."""

    initial_capital: float = 500_000_000.0   # VND cho VN stock; override 10_000 USDT cho crypto
    risk_per_trade: float = 0.02             # 2% NAV / lệnh
    max_position_pct: float = 0.30           # không dồn quá 30% NAV vào 1 lệnh


# ── Lưới tham số tối ưu hóa (Module 3) ──────────────────────────────────────
# Không gian ~4 tham số, Grid Search đủ nhanh với engine vectorized.
DEFAULT_PARAM_GRID: dict[str, list] = {
    "rsi_period": [7, 10, 14, 21],
    "rsi_entry": [25, 30, 35, 40],           # mua khi RSI cắt lên từ vùng quá bán
    "atr_sl_mult": [1.5, 2.0, 2.5, 3.0],     # SL = entry - k * ATR(14)
    "tp_r_multiple": [1.5, 2.0, 3.0],        # TP = entry + R * (entry - SL)
    "trend_filter": [True, False],           # chỉ vào lệnh khi close > SMA200 & ADX > 20
}

# ── Walk-forward ─────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class WalkForwardConfig:
    train_bars: int = 504      # ~24 tháng phiên giao dịch
    test_bars: int = 126       # ~6 tháng
    step_bars: int = 126       # trượt 6 tháng
    min_trades_per_fold: int = 5     # dưới ngưỡng → fold không đủ mẫu thống kê
    stability_threshold: float = 0.6  # params phải nằm trong top-quartile ở >= 60% folds


def get_cost_model(asset: AssetType) -> CostModel:
    return VN_COSTS if asset == AssetType.VN_STOCK else CRYPTO_COSTS


def get_market_constraints(asset: AssetType) -> MarketConstraints:
    return VN_CONSTRAINTS if asset == AssetType.VN_STOCK else CRYPTO_CONSTRAINTS
