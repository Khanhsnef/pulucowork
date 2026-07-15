# Automated Trading Analysis & Optimization System

Hệ thống phân tích & tối ưu hóa giao dịch tự động cho **Chứng khoán VN** (vnstock) và **Crypto Binance** (python-binance), có **Web UI**, **batch scan** và **auto-refresh 10:00 sáng**.

Pipeline: `Data Ingestion → Cleaning → TA + FA → Walk-Forward Backtest Optimization → Decision (MUA/BÁN/ĐỨNG NGOÀI)`

## 🚀 Chạy nhanh (Windows — máy nhà)

```text
1. Cài Python 3.10+ từ python.org (tick "Add Python to PATH")
2. git clone https://github.com/Khanhsnef/pulucowork.git
   (hoặc git pull nếu đã clone)
3. Vào folder Output/Personal/trading-system/
4. Double-click run.bat
   → Lần đầu tự tạo venv + cài thư viện (~2-3 phút)
   → Browser tự mở http://127.0.0.1:8899
```

## 🚀 Chạy nhanh (macOS)

```bash
cd Output/Personal/trading-system && ./run.sh
```

## Web UI — 4 tab

| Tab | Chức năng |
| :--- | :--- |
| 🔍 **Phân tích 1 mã** | Nhập mã → progress 5 bước real-time → báo cáo đầy đủ: khuyến nghị, chart SVG 12 tháng có vẽ Entry/TP/SL, trend 3 khung, fold table |
| 📊 **Batch Scan** | Quét toàn bộ watchlist tuần tự, bảng tổng hợp xếp hạng MUA trước, click từng dòng xem chi tiết |
| 🗓 **Lịch sử** | Xem lại mọi batch đã chạy theo ngày (đọc từ `reports/daily/`) — không cần chạy lại |
| ⭐ **Watchlist** | Sửa danh sách mã theo dõi ngay trên UI, lưu vào `watchlist.json` |

**Auto-refresh:** server bật scheduler mặc định — **10:00 sáng mỗi ngày** tự batch scan toàn bộ watchlist và lưu vào `reports/daily/YYYY-MM-DD/`. Chỉ cần để server chạy (hoặc mở `run.bat` trước giờ đó). Tắt bằng `--no-scheduler`.

## Sử dụng khác

**CLI:**

```bash
python3 -m trading_system.main FPT               # 1 mã, in Markdown
python3 -m trading_system.main BTCUSDT --years 4 --json --save
python3 -m trading_system.batch                  # batch toàn watchlist
python3 -m trading_system.batch FPT HPG          # batch mã chỉ định
python3 -m trading_system.server --port 8899     # web UI
```

**Notebook:** mở `analysis_notebook.ipynb`, đổi biến `SYMBOL`, chạy toàn bộ cells.

**Python API:**

```python
from trading_system.main import analyze
decision = analyze("FPT")
print(decision.recommendation, decision.zones)
```

## Cấu trúc

```text
trading-system/
├── trading_system/
│   ├── main.py          # Entry point + CLI (analyze() với progress callback)
│   ├── config.py        # Cost model, ràng buộc T+2/lot/biên độ, param grid, risk config
│   ├── data.py          # Module 1: vnstock + Binance ingestion, cache Parquet, cleaning
│   ├── indicators.py    # Module 2A: RSI/MACD/ADX/ATR/BB/OBV/Stoch/Fibonacci (pandas thuần)
│   ├── fa.py            # Module 2B: FA gate — chấm điểm BCTC (VN) / thanh khoản+funding (crypto)
│   ├── backtester.py    # Module 3: engine mô phỏng + grid search + walk-forward optimization
│   ├── decision.py      # Module 4: trend 3 khung + entry/TP/SL zones + render JSON/Markdown
│   ├── batch.py         # Batch scan watchlist → reports/daily/YYYY-MM-DD/
│   └── server.py        # FastAPI web server + scheduler auto-refresh 10:00
├── static/index.html    # Web UI (Lexend, SVG charts thuần, 4 tabs)
├── tests/test_smoke.py  # Smoke tests trên dữ liệu synthetic (6 tests)
├── analysis_notebook.ipynb
├── watchlist.json       # Danh sách mã theo dõi (sửa được trên UI)
├── run.bat / run.sh     # Launcher Windows / macOS: tự tạo venv + cài deps + mở browser
├── requirements.txt
├── reports/daily/       # Báo cáo batch theo ngày (gitignored)
└── data_cache/          # Cache Parquet, TTL 12h (gitignored)
```

## Thiết kế chống Win Rate ảo

| Cơ chế | Chi tiết |
| :--- | :--- |
| Không look-ahead | Tín hiệu bar t → vào lệnh giá **open bar t+1** |
| T+2.5 (VN) | Không cho bán trước khi hàng về tài khoản (`settlement_bars=2`) |
| Chi phí thật | VN: 0.15% phí + 0.1% slippage + 0.1% thuế bán; Crypto: 0.1% taker + 0.05% slippage |
| SL ưu tiên TP | Cùng bar chạm cả SL và TP → tính là SL (giả định bảo thủ) |
| Gap handling | Gap qua SL/TP → khớp giá mở cửa, không khớp giá SL/TP lý tưởng |
| Walk-forward | Train 24 tháng → Test 6 tháng out-of-sample, trượt 6 tháng |
| Stability filter | Params phải lọt top-quartile ở ≥ 60% folds, không lấy best 1 giai đoạn |
| Sample guard | < 10 lệnh OOS hoặc < 5 lệnh/fold → cảnh báo "không đủ mẫu thống kê" |
| Score đa mục tiêu | Sharpe + win rate + drawdown (không tối ưu win rate đơn thuần) |

## Khẩu vị rủi ro (đã chốt)

- Risk 2% NAV/lệnh, position size tính ngược từ khoảng SL, cap 30% NAV/vị thế
- SL = entry − k×ATR(14), k ∈ [1.5, 3.0] do optimizer chọn — không dùng % cố định
- TP1 chốt 50% vị thế, TP2 theo R-multiple tối ưu

## Ghi chú

- vnstock 4.x hiện warning deprecation (API `Vnstock()` cũ) — vẫn hoạt động; khi nào gãy thì migrate sang `vnstock.api.quote.Quote`.
- Binance dùng public endpoint, không cần API key cho dữ liệu lịch sử.
- Timeframe: VN = 1D (không có intraday tin cậy miễn phí); Crypto = 1D mặc định, đổi được qua `fetch_crypto_ohlcv(interval="4h")`.
- Kết quả smoke test và 2 lần chạy thật (BTCUSDT, FPT) đều pass — xem `tests/test_smoke.py`.

---
*Hệ thống hỗ trợ quyết định — không phải khuyến nghị đầu tư. Win rate quá khứ không đảm bảo kết quả tương lai.*
