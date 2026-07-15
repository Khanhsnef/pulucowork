"""Web server: FastAPI + scheduler auto-refresh 10:00 sáng.

Chạy:  python -m trading_system.server          # http://127.0.0.1:8899
       python -m trading_system.server --port 8899 --no-scheduler

Job chạy trong ThreadPoolExecutor(1) — phân tích tuần tự, UI poll trạng thái.
Scheduler: thread nền tính giây đến giờ SCHEDULE_HOUR kế tiếp, chạy batch, lặp.
"""

from __future__ import annotations

import argparse
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .batch import (
    list_batch_dates,
    load_batch_detail,
    load_batch_summary,
    load_watchlist,
    run_batch,
    save_watchlist,
)
from .decision import render_markdown, Decision
from .main import analyze

ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT / "static"
SCHEDULE_HOUR = 10  # 10:00 sáng

app = FastAPI(title="Trading Analysis System", docs_url="/api/docs")

# ── Job store (in-memory) ────────────────────────────────────────────────────
_executor = ThreadPoolExecutor(max_workers=1)  # tuần tự: tránh rate-limit API nguồn
_jobs: dict[str, dict] = {}
_jobs_lock = threading.Lock()


def _new_job(kind: str, label: str) -> str:
    job_id = uuid.uuid4().hex[:12]
    with _jobs_lock:
        _jobs[job_id] = {
            "id": job_id, "kind": kind, "label": label,
            "status": "queued", "step": 0, "total": 5, "message": "Đang chờ...",
            "result": None, "error": None,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    return job_id


def _update_job(job_id: str, **kw) -> None:
    with _jobs_lock:
        if job_id in _jobs:
            _jobs[job_id].update(kw)


def _run_analyze_job(job_id: str, symbol: str, years: int) -> None:
    _update_job(job_id, status="running", message=f"Bắt đầu phân tích {symbol}...")
    try:
        def cb(step, total, msg):
            _update_job(job_id, step=step, total=total, message=msg)
        d = analyze(symbol, lookback_years=years, verbose=False, progress=cb)
        _update_job(job_id, status="done", step=5,
                    message="Hoàn thành", result=asdict(d))
    except Exception as e:
        _update_job(job_id, status="error", error=str(e), message=f"Lỗi: {e}")


def _run_batch_job(job_id: str, symbols: list[str] | None) -> None:
    _update_job(job_id, status="running", message="Bắt đầu batch scan...")
    try:
        def cb(i, n, msg):
            _update_job(job_id, step=i, total=n, message=msg)
        summary = run_batch(symbols, progress=cb)
        _update_job(job_id, status="done", message="Hoàn thành", result=summary)
    except Exception as e:
        _update_job(job_id, status="error", error=str(e), message=f"Lỗi: {e}")


# ── API models ───────────────────────────────────────────────────────────────
class AnalyzeReq(BaseModel):
    symbol: str
    years: int = 5


class BatchReq(BaseModel):
    symbols: list[str] | None = None  # None → toàn bộ watchlist


class WatchlistReq(BaseModel):
    vn_stocks: list[str]
    crypto: list[str]
    lookback_years: int = 5


# ── Endpoints ────────────────────────────────────────────────────────────────
@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/analyze")
def api_analyze(req: AnalyzeReq):
    job_id = _new_job("analyze", req.symbol.upper())
    _executor.submit(_run_analyze_job, job_id, req.symbol.upper(), req.years)
    return {"job_id": job_id}


@app.post("/api/batch")
def api_batch(req: BatchReq):
    symbols = [s.upper() for s in req.symbols] if req.symbols else None
    n = len(symbols) if symbols else len(load_watchlist().get("vn_stocks", [])) + len(load_watchlist().get("crypto", []))
    job_id = _new_job("batch", f"Batch scan {n} mã")
    _executor.submit(_run_batch_job, job_id, symbols)
    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
def api_job(job_id: str):
    with _jobs_lock:
        job = _jobs.get(job_id)
    if job is None:
        raise HTTPException(404, "Job không tồn tại")
    return job


@app.get("/api/jobs")
def api_jobs():
    with _jobs_lock:
        return sorted(_jobs.values(), key=lambda j: j["created_at"], reverse=True)[:20]


@app.get("/api/watchlist")
def api_get_watchlist():
    return load_watchlist()


@app.put("/api/watchlist")
def api_put_watchlist(req: WatchlistReq):
    wl = {"vn_stocks": [s.upper() for s in req.vn_stocks],
          "crypto": [s.upper() for s in req.crypto],
          "lookback_years": req.lookback_years}
    save_watchlist(wl)
    return wl


@app.get("/api/history")
def api_history():
    return list_batch_dates()


@app.get("/api/history/{date}")
def api_history_date(date: str):
    s = load_batch_summary(date)
    if s is None:
        raise HTTPException(404, f"Không có batch ngày {date}")
    return s


@app.get("/api/history/{date}/{symbol}")
def api_history_detail(date: str, symbol: str):
    d = load_batch_detail(date, symbol)
    if d is None:
        raise HTTPException(404, f"Không có báo cáo {symbol} ngày {date}")
    return d


@app.get("/api/export/{date}/{symbol}.md")
def api_export_md(date: str, symbol: str):
    raw = load_batch_detail(date, symbol)
    if raw is None:
        raise HTTPException(404, "Không có báo cáo")
    # dựng lại Decision tối thiểu để render markdown từ dict đã lưu
    from .decision import TrendView, PriceZones
    raw["trends"] = [TrendView(**t) for t in raw["trends"]]
    raw["zones"] = PriceZones(**raw["zones"]) if raw.get("zones") else None
    d = Decision(**raw)
    return JSONResponse({"markdown": render_markdown(d)})


@app.get("/api/scheduler")
def api_scheduler_status():
    return {"enabled": _scheduler_enabled, "hour": SCHEDULE_HOUR,
            "next_run": _next_run_at.isoformat(timespec="seconds") if _next_run_at else None}


# ── Scheduler hàng ngày ──────────────────────────────────────────────────────
_scheduler_enabled = False
_next_run_at: datetime | None = None


def _seconds_until(hour: int) -> tuple[float, datetime]:
    now = datetime.now()
    target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return (target - now).total_seconds(), target


def _scheduler_loop():
    global _next_run_at
    while True:
        wait, target = _seconds_until(SCHEDULE_HOUR)
        _next_run_at = target
        time.sleep(wait)
        job_id = _new_job("batch", f"Auto-refresh {SCHEDULE_HOUR}:00")
        _run_batch_job(job_id, None)  # chạy trực tiếp trong thread scheduler


def start_scheduler():
    global _scheduler_enabled
    _scheduler_enabled = True
    threading.Thread(target=_scheduler_loop, daemon=True, name="daily-scheduler").start()


def main():
    import uvicorn
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8899)
    ap.add_argument("--no-scheduler", action="store_true", help="Tắt auto-refresh hàng ngày")
    args = ap.parse_args()

    if not args.no_scheduler:
        start_scheduler()
        print(f"⏰ Auto-refresh bật: batch scan watchlist lúc {SCHEDULE_HOUR}:00 mỗi sáng")
    print(f"🌐 Mở http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
