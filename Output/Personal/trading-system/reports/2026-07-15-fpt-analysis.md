# Báo cáo Phân tích: FPT (VN_STOCK)
*Tạo lúc: 2026-07-15 10:24 — Giá hiện tại: 69.40*

## 🎯 Khuyến nghị: **ĐỨNG NGOÀI** (độ tin cậy: CAO)

> Setup này xuất hiện 52 lần trong 5 năm qua, tỷ lệ thắng 54% (avg +0.08R/lệnh). Out-of-sample: 29 lệnh, thắng 45%.

## Nhận định Xu hướng
| Khung | Xu hướng | Bằng chứng |
| :--- | :--- | :--- |
| Ngắn hạn (1-2 tuần) | **GIẢM** | MACD histogram âm; RSI14 = 36 < 50; giá dưới BB middle |
| Trung hạn (1-3 tháng) | **GIẢM** | giá dưới SMA50; ADX = 12 — trend yếu; OBV giảm 20 phiên (dòng tiền ra) |
| Dài hạn (3-12 tháng) | **GIẢM** | giá dưới SMA200; hiệu suất 12 tháng -35% |

## Tham số Tối ưu (Walk-Forward)
- Bộ tham số: `{'atr_sl_mult': 1.5, 'rsi_entry': 40, 'rsi_period': 7, 'tp_r_multiple': 1.5, 'trend_filter': False}`
- Out-of-sample: **29 lệnh, win rate 45%**
- FA score: 50/100

### Kết quả từng fold (out-of-sample)
| Fold | Giai đoạn test | Số lệnh | Win rate |
| ---: | :--- | ---: | ---: |
| 0 | 2023-04-25 → 2023-10-24 | 3 | 67% |
| 1 | 2023-10-25 → 2024-04-26 | 4 | 75% |
| 2 | 2024-05-02 → 2024-10-28 | 4 | 50% |
| 3 | 2024-10-29 → 2025-05-06 | 7 | 43% |
| 4 | 2025-05-07 → 2025-10-31 | 5 | 40% |
| 5 | 2025-11-03 → 2026-05-11 | 6 | 17% |

---
*Hệ thống hỗ trợ quyết định — không phải khuyến nghị đầu tư. Win rate quá khứ không đảm bảo kết quả tương lai.*