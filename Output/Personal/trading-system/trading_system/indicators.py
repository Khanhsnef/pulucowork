"""Module 2A — TA Engine: tính toàn bộ chỉ báo bằng pandas/numpy thuần.

Không dùng TA-Lib (tránh dependency C); công thức chuẩn Wilder cho RSI/ATR/ADX.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ── Trend ────────────────────────────────────────────────────────────────────
def sma(close: pd.Series, period: int) -> pd.Series:
    return close.rolling(period, min_periods=period).mean()


def ema(close: pd.Series, period: int) -> pd.Series:
    return close.ewm(span=period, adjust=False, min_periods=period).mean()


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame({
        "macd": macd_line,
        "macd_signal": signal_line,
        "macd_hist": macd_line - signal_line,
    })


def adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """Average Directional Index — công thức Wilder."""
    up = high.diff()
    down = -low.diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=high.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=high.index)

    tr = _true_range(high, low, close)
    atr_w = tr.ewm(alpha=1 / period, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_w
    minus_di = 100 * minus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_w
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1 / period, adjust=False).mean()


# ── Momentum ─────────────────────────────────────────────────────────────────
def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """RSI theo smoothing Wilder (ewm alpha=1/n)."""
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    rs = gain / loss.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.fillna(100.0).where(close.notna())  # loss=0 → RSI=100


def stochastic(high: pd.Series, low: pd.Series, close: pd.Series,
               k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    lowest = low.rolling(k_period).min()
    highest = high.rolling(k_period).max()
    k = 100 * (close - lowest) / (highest - lowest).replace(0, np.nan)
    return pd.DataFrame({"stoch_k": k, "stoch_d": k.rolling(d_period).mean()})


# ── Volatility ───────────────────────────────────────────────────────────────
def _true_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    prev_close = close.shift(1)
    return pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    return _true_range(high, low, close).ewm(alpha=1 / period, adjust=False, min_periods=period).mean()


def bollinger(close: pd.Series, period: int = 20, n_std: float = 2.0) -> pd.DataFrame:
    mid = sma(close, period)
    std = close.rolling(period).std(ddof=0)
    return pd.DataFrame({
        "bb_mid": mid,
        "bb_upper": mid + n_std * std,
        "bb_lower": mid - n_std * std,
        "bb_width": (2 * n_std * std) / mid,
    })


# ── Volume ───────────────────────────────────────────────────────────────────
def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    direction = np.sign(close.diff()).fillna(0)
    return (direction * volume).cumsum()


def volume_profile_poc(close: pd.Series, volume: pd.Series, bins: int = 50) -> float:
    """Point of Control — mức giá tập trung volume lớn nhất (hỗ trợ/kháng cự)."""
    hist, edges = np.histogram(close, bins=bins, weights=volume)
    i = int(hist.argmax())
    return float((edges[i] + edges[i + 1]) / 2)


# ── Fibonacci ────────────────────────────────────────────────────────────────
FIB_LEVELS = (0.236, 0.382, 0.5, 0.618, 0.786)


def fibonacci_retracements(close: pd.Series, lookback: int = 252) -> dict[str, float]:
    """Mốc Fibonacci retracement của swing gần nhất (proxy đơn giản cho Elliott/Fib)."""
    window = close.iloc[-lookback:]
    hi, lo = float(window.max()), float(window.min())
    return {f"fib_{lvl}": hi - lvl * (hi - lo) for lvl in FIB_LEVELS} | {"swing_high": hi, "swing_low": lo}


# ── Tổng hợp ─────────────────────────────────────────────────────────────────
def compute_ta_features(df: pd.DataFrame) -> pd.DataFrame:
    """Nhận OHLCV chuẩn (open/high/low/close/volume), trả về bảng feature đầy đủ.

    RSI được tính sẵn cho mọi chu kỳ trong grid để optimizer không phải tính lại.
    """
    h, l, c, v = df["high"], df["low"], df["close"], df["volume"]
    feats = pd.DataFrame(index=df.index)

    for p in (7, 10, 14, 21):
        feats[f"rsi_{p}"] = rsi(c, p)
    feats["atr_14"] = atr(h, l, c, 14)
    feats["sma_50"] = sma(c, 50)
    feats["sma_200"] = sma(c, 200)
    feats["adx_14"] = adx(h, l, c, 14)
    feats = feats.join(macd(c))
    feats = feats.join(bollinger(c))
    feats = feats.join(stochastic(h, l, c))
    feats["obv"] = obv(c, v)
    feats["obv_slope"] = feats["obv"].diff(20)
    return feats
