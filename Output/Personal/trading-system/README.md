# Automated Trading Analysis & Optimization System

Hệ thống phân tích & tối ưu hóa giao dịch tự động cho **Chứng khoán VN** (vnstock) và **Crypto Binance** (python-binance).

Pipeline: `Data Ingestion → Cleaning → TA + FA → Walk-Forward Backtest Optimization → Decision (MUA/BÁN/ĐỨNG NGOÀI)`

## Cài đặt

```bash
pip3 install vnstock python-binance pandas numpy pyarrow matplotlib
```

## Sử dụng

**CLI:**
```bash
cd trading-system
python3 -m trading_system.main FPT              # chứng khoán VN
python3 -m trading_system.main BTCUSDT --years 4 # crypto
python3 -m trading_system.main HPG --json --save # xuất JSON, lưu vào reports/
```

**Notebook:** mở `analysis_notebook.ipynb`, đổi biến `SYMBOL`, chạy toàn bộ cells.

**Python API:**
```python
from trading_system.main import analyze
decision = analyze("FPT")
print(decision.recommendation, decision.zones)
```

## Cấu trúc

```
trading-system/
├── trading_system/
│   ├── main.py          # Entry point + CLI (analyze())
│   ├── config.py        # Cost model, ràng buộc T+2/lot/biên độ, param grid, risk config
│   ├── data.py          # Module 1: vnstock + Binance ingestion, cache Parquet, cleaning
│   ├── indicators.py    # Module 2A: RSI/MACD/ADX/ATR/BB/OBV/Stoch/Fibonacci (pandas thuần)
│   ├── fa.py            # Module 2B: FA gate — chấm điểm BCTC (VN) / thanh khoản+funding (crypto)
│   ├── backtester.py    # Module 3: engine mô phỏng + grid search + walk-forward optimization
│   └── decision.py      # Module 4: trend 3 khung + entry/TP/SL zones + render JSON/Markdown
├── tests/test_smoke.py  # Smoke tests trên dữ liệu synthetic (6 tests)
├── analysis_notebook.ipynb
├── reports/             # Báo cáo đã lưu (--save)
└── data_cache/          # Cache Parquet, TTL 12h
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
