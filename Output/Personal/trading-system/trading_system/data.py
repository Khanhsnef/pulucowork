"""Module 1 — Data Ingestion & Cleaning.

VN stock : vnstock (OHLCV + BCTC + chỉ số định giá)
Crypto   : python-binance public API (klines + funding + ticker 24h), không cần API key.
Cache    : Parquet trong data_cache/ — refresh khi file cũ hơn 12h.
"""

from __future__ import annotations

import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

from .config import AssetType

CACHE_DIR = Path(__file__).resolve().parent.parent / "data_cache"
CACHE_TTL_SECONDS = 12 * 3600


# ─────────────────────────────────────────────────────────────────────────────
# Asset Router
# ─────────────────────────────────────────────────────────────────────────────
def route_asset(symbol: str) -> AssetType:
    """'FPT'/'HPG' → VN_STOCK; 'BTCUSDT'/'ETHBTC' → CRYPTO.

    Quy tắc: mã VN là 3 ký tự chữ; mã crypto dài hơn và kết thúc bằng quote phổ biến.
    """
    s = symbol.upper().strip()
    if re.fullmatch(r"[A-Z]{3}", s):
        return AssetType.VN_STOCK
    if re.fullmatch(r"[A-Z0-9]{5,12}", s) and s.endswith(("USDT", "BUSD", "BTC", "ETH", "USDC", "FDUSD")):
        return AssetType.CRYPTO
    raise ValueError(f"Không nhận dạng được '{symbol}' — mã VN (3 chữ cái, vd FPT) hoặc cặp Binance (vd BTCUSDT).")


# ─────────────────────────────────────────────────────────────────────────────
# Ingestion
# ─────────────────────────────────────────────────────────────────────────────
def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{key}.parquet"


def _load_cache(key: str) -> pd.DataFrame | None:
    p = _cache_path(key)
    if p.exists() and (time.time() - p.stat().st_mtime) < CACHE_TTL_SECONDS:
        return pd.read_parquet(p)
    return None


def _save_cache(key: str, df: pd.DataFrame) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    df.to_parquet(_cache_path(key))


def fetch_vn_ohlcv(symbol: str, lookback_years: int = 5) -> pd.DataFrame:
    """OHLCV daily từ vnstock. Giá vnstock đã điều chỉnh (adjusted)."""
    key = f"vn_{symbol}_1D"
    cached = _load_cache(key)
    if cached is not None:
        return cached

    from vnstock import Vnstock
    end = pd.Timestamp.now().strftime("%Y-%m-%d")
    start = (pd.Timestamp.now() - pd.DateOffset(years=lookback_years)).strftime("%Y-%m-%d")
    stock = Vnstock().stock(symbol=symbol, source="VCI")
    df = stock.quote.history(start=start, end=end, interval="1D")
    df = df.rename(columns={"time": "date"})
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    _save_cache(key, df)
    return df


def fetch_vn_fundamentals(symbol: str) -> dict:
    """Chỉ số FA: P/E, P/B, EPS, ROE, tăng trưởng, nợ vay. Trả {} nếu API lỗi."""
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source="VCI")
        ratios = stock.finance.ratio(period="year", lang="en")
        if isinstance(ratios.columns, pd.MultiIndex):
            ratios.columns = [c[-1] for c in ratios.columns]
        latest = ratios.iloc[0] if len(ratios) else pd.Series(dtype=float)

        income = stock.finance.income_statement(period="year", lang="en")
        rev_growth = profit_growth = None
        if len(income) >= 2:
            rev_cols = [c for c in income.columns if "revenue" in str(c).lower()]
            profit_cols = [c for c in income.columns if "profit" in str(c).lower() and "gross" not in str(c).lower()]
            if rev_cols:
                r0, r1 = income[rev_cols[0]].iloc[0], income[rev_cols[0]].iloc[1]
                rev_growth = float(r0 / r1 - 1) if r1 else None
            if profit_cols:
                p0, p1 = income[profit_cols[0]].iloc[0], income[profit_cols[0]].iloc[1]
                profit_growth = float(p0 / p1 - 1) if p1 else None

        def _get(*names):
            for nm in names:
                for col in latest.index:
                    if nm.lower() in str(col).lower():
                        val = latest[col]
                        return float(val) if pd.notna(val) else None
            return None

        return {
            "pe": _get("P/E", "price_to_earning"),
            "pb": _get("P/B", "price_to_book"),
            "eps": _get("EPS", "earning_per_share"),
            "roe": _get("ROE", "return_on_equity"),
            "debt_to_equity": _get("Debt/Equity", "debt_on_equity"),
            "revenue_growth_yoy": rev_growth,
            "profit_growth_yoy": profit_growth,
        }
    except Exception as e:  # API vnstock đổi schema thường xuyên — degrade mềm
        return {"_error": f"FA fetch failed: {e}"}


def fetch_crypto_ohlcv(symbol: str, interval: str = "1d", lookback_years: int = 5) -> pd.DataFrame:
    """Klines từ Binance public endpoint (không cần key)."""
    key = f"cx_{symbol}_{interval}"
    cached = _load_cache(key)
    if cached is not None:
        return cached

    from binance.client import Client
    client = Client()  # public data
    start_str = (pd.Timestamp.now() - pd.DateOffset(years=lookback_years)).strftime("%d %b, %Y")
    klines = client.get_historical_klines(symbol, interval, start_str)
    cols = ["open_time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "trades", "tbbav", "tbqav", "ignore"]
    df = pd.DataFrame(klines, columns=cols)
    df["date"] = pd.to_datetime(df["open_time"], unit="ms")
    df = df.set_index("date").sort_index()
    df = df[["open", "high", "low", "close", "volume"]].astype(float)
    _save_cache(key, df)
    return df


def fetch_crypto_context(symbol: str) -> dict:
    """FA-proxy cho crypto: 24h volume, funding rate, order-book imbalance."""
    out: dict = {}
    try:
        from binance.client import Client
        client = Client()
        t = client.get_ticker(symbol=symbol)
        out["volume_24h_quote"] = float(t["quoteVolume"])
        out["price_change_24h_pct"] = float(t["priceChangePercent"])

        depth = client.get_order_book(symbol=symbol, limit=100)
        bid_vol = sum(float(q) for _, q in depth["bids"])
        ask_vol = sum(float(q) for _, q in depth["asks"])
        out["orderbook_imbalance"] = (bid_vol - ask_vol) / (bid_vol + ask_vol) if (bid_vol + ask_vol) else 0.0

        try:  # funding chỉ có trên futures — pass nếu cặp không có perp
            fr = client.futures_funding_rate(symbol=symbol, limit=1)
            if fr:
                out["funding_rate"] = float(fr[0]["fundingRate"])
        except Exception:
            pass
    except Exception as e:
        out["_error"] = f"Crypto context fetch failed: {e}"
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Cleaning
# ─────────────────────────────────────────────────────────────────────────────
def clean_ohlcv(df: pd.DataFrame, z_threshold: float = 12.0) -> tuple[pd.DataFrame, list[str]]:
    """Làm sạch OHLCV, trả (df_sạch, log các thao tác đã làm).

    - Bỏ bar trùng index, bar có giá <= 0 hoặc NaN.
    - Sửa bar vi phạm high < low (swap lỗi nguồn).
    - Outlier: |z-score log-return| > threshold VÀ quay đầu ngay bar sau
      (spike lỗi dữ liệu, khác với limit-move thật) → thay bằng nội suy.
    """
    log: list[str] = []
    df = df[~df.index.duplicated(keep="last")].sort_index()

    bad = df[["open", "high", "low", "close"]].le(0).any(axis=1) | df[["open", "high", "low", "close"]].isna().any(axis=1)
    if bad.any():
        log.append(f"Bỏ {int(bad.sum())} bar giá <= 0 / NaN")
        df = df[~bad]

    swapped = df["high"] < df["low"]
    if swapped.any():
        log.append(f"Sửa {int(swapped.sum())} bar high < low")
        hi = df.loc[swapped, "low"].copy()
        df.loc[swapped, "low"] = df.loc[swapped, "high"]
        df.loc[swapped, "high"] = hi

    ret = np.log(df["close"]).diff()
    z = (ret - ret.mean()) / ret.std()
    spike = (z.abs() > z_threshold) & (z.shift(-1) * z < 0)  # spike + đảo chiều ngay
    if spike.any():
        log.append(f"Nội suy {int(spike.sum())} outlier spike (|z| > {z_threshold})")
        cols = ["open", "high", "low", "close"]
        df.loc[spike, cols] = np.nan
        df[cols] = df[cols].interpolate()

    df["volume"] = df["volume"].fillna(0)
    return df, log
