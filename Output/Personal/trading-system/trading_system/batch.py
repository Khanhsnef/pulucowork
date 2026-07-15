"""Batch scan: chạy analyze() tuần tự trên watchlist, lưu kết quả JSON theo ngày.

Watchlist đọc từ watchlist.json (tạo mặc định nếu chưa có).
Kết quả: reports/daily/YYYY-MM-DD/<symbol>.json + _summary.json (bảng tổng hợp).

CLI:  python -m trading_system.batch            # scan toàn bộ watchlist
      python -m trading_system.batch FPT HPG    # scan các mã chỉ định
"""

from __future__ import annotations

import json
import sys
import traceback
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .decision import Decision
from .main import analyze

ROOT = Path(__file__).resolve().parent.parent
WATCHLIST_PATH = ROOT / "watchlist.json"
DAILY_DIR = ROOT / "reports" / "daily"

DEFAULT_WATCHLIST = {
    "vn_stocks": ["FPT", "HPG", "MWG", "VNM"],
    "crypto": ["BTCUSDT", "ETHUSDT"],
    "lookback_years": 5,
}


def load_watchlist() -> dict:
    if not WATCHLIST_PATH.exists():
        WATCHLIST_PATH.write_text(
            json.dumps(DEFAULT_WATCHLIST, ensure_ascii=False, indent=2), encoding="utf-8")
    return json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))


def save_watchlist(wl: dict) -> None:
    WATCHLIST_PATH.write_text(json.dumps(wl, ensure_ascii=False, indent=2), encoding="utf-8")


def _summary_row(d: Decision) -> dict:
    return {
        "symbol": d.symbol,
        "asset_type": d.asset_type,
        "last_price": d.last_price,
        "recommendation": d.recommendation,
        "conviction": d.conviction,
        "oos_win_rate": d.oos_win_rate,
        "oos_n_trades": d.oos_n_trades,
        "fa_score": d.fa_score,
        "trend_short": d.trends[0].direction,
        "trend_mid": d.trends[1].direction,
        "trend_long": d.trends[2].direction,
        "entry_low": d.zones.entry_low if d.zones else None,
        "entry_high": d.zones.entry_high if d.zones else None,
        "sl": d.zones.sl if d.zones else None,
        "tp1": d.zones.tp1 if d.zones else None,
        "tp2": d.zones.tp2 if d.zones else None,
        "n_warnings": len(d.warnings),
    }


def run_batch(symbols: list[str] | None = None,
              progress: "callable | None" = None) -> dict:
    """Scan tuần tự (vnstock/Binance đều rate-limit — không chạy song song).

    Trả về summary dict; lỗi từng mã không làm gãy cả batch.
    """
    wl = load_watchlist()
    if symbols is None:
        symbols = [s.upper() for s in wl.get("vn_stocks", []) + wl.get("crypto", [])]
    years = int(wl.get("lookback_years", 5))

    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)

    rows, errors = [], []
    t_start = datetime.now()
    for i, sym in enumerate(symbols, 1):
        if progress:
            progress(i, len(symbols), f"[{i}/{len(symbols)}] Đang phân tích {sym}...")
        try:
            d = analyze(sym, lookback_years=years, verbose=False)
            (out_dir / f"{sym}.json").write_text(
                json.dumps(asdict(d), ensure_ascii=False, indent=2, default=str),
                encoding="utf-8")
            rows.append(_summary_row(d))
            print(f"  ✅ {sym}: {d.recommendation} ({d.conviction})", file=sys.stderr)
        except Exception as e:
            errors.append({"symbol": sym, "error": str(e)})
            print(f"  ❌ {sym}: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    # sắp xếp: MUA trước, rồi theo win rate giảm dần
    order = {"MUA": 0, "BÁN": 1, "ĐỨNG NGOÀI": 2}
    rows.sort(key=lambda r: (order.get(r["recommendation"], 9), -r["oos_win_rate"]))

    summary = {
        "date": today,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": round((datetime.now() - t_start).total_seconds(), 1),
        "n_scanned": len(rows),
        "n_errors": len(errors),
        "results": rows,
        "errors": errors,
    }
    (out_dir / "_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def list_batch_dates() -> list[str]:
    if not DAILY_DIR.exists():
        return []
    return sorted((p.name for p in DAILY_DIR.iterdir()
                   if p.is_dir() and (p / "_summary.json").exists()), reverse=True)


def load_batch_summary(date: str) -> dict | None:
    p = DAILY_DIR / date / "_summary.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def load_batch_detail(date: str, symbol: str) -> dict | None:
    p = DAILY_DIR / date / f"{symbol.upper()}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


if __name__ == "__main__":
    args = [a.upper() for a in sys.argv[1:]]
    s = run_batch(args or None)
    print(json.dumps({k: s[k] for k in ("date", "n_scanned", "n_errors", "duration_seconds")},
                     ensure_ascii=False))
    for r in s["results"]:
        print(f"{r['symbol']:10s} {r['recommendation']:12s} win {r['oos_win_rate']:.0%}  "
              f"{r['trend_short']}/{r['trend_mid']}/{r['trend_long']}")
