# Driver Ranking & AhaBenefits v2.0 — Params Sheet
> File này chứa toàn bộ con số có thể điều chỉnh. Sau khi sửa ở đây → cập nhật vào HTML tương ứng.
> HTML: `2026-05-driver-ranking-layer-benefits.html`

---

## 1. Ranking KPI Thresholds

> Cả 3 rank đều xét bằng **DQS** (Driver Quality Score). Không dùng AR/FR/Rating riêng lẻ.

| Rank | DQS | DCR (%) | Productivity (stp/tháng) |
| --- | --- | --- | --- |
| R1 Elite | ≥ 80 | < 10 | ≥ 280 |
| R2 Active | ≥ 75 | < 10 | ≥ 210 |
| R3 Standard | ≥ 70 | — | ≥ 70 |
| Unranked | < 70 | — | — |

> DQS scale & công thức: cần confirm với Data team trước khi go-live.

---

## 2. Fleet Target Ratio (% of weekly actives)

| Rank | Target % | Số lượng (~10.5k weekly) |
|------|----------|--------------------------|
| R1 💎 Kim Cương | 15% | ~1.575 |
| R2 🥇 Vàng | 35% | ~3.675 |
| R3 🥈 Bạc | 35% | ~3.675 |
| Unranked | 15% | ~1.575 |

---

## 3. Layer Access & Cascade

| Rank | Primary Layer | Fallback |
|------|--------------|----------|
| R1 Elite | L2 Minizone | → L3 khi L2 ≥ 80% fill |
| R2 Active | L3 Mediumzone | → L4 khi L3 ≥ 80% fill |
| R3 Standard | L4 Bigzone | → L5 khi L4 ≥ 80% fill |
| Unranked | L6 MASS | — |

> Ngưỡng cascade: **80%** slot fill → mở layer kế tiếp

---

## 4. Hourly Income Guarantee (Đảm bảo theo giờ)

> Chỉ áp dụng khi tài xế đủ điều kiện KPI ca. Tách biệt hoàn toàn với budget 200M AhaBenefits.

### SGN
| Layer | Guarantee/h |
|-------|------------|
| L2 Minizone | 65.000đ |
| L3 Mediumzone | 60.000đ |
| L4 Bigzone | 55.000đ |
| L5 Cityzone | 55.000đ |

### HAN
| Layer | Guarantee/h |
|-------|------------|
| L2 Minizone | 70.000đ |
| L3 Mediumzone | 65.000đ |
| L4 Bigzone | 60.000đ |
| L5 Cityzone | 60.000đ |

---

## 5. Full-day Guarantee (Đảm bảo ngày — R1 & R2 only)

| Rank | SGN | HAN |
|------|-----|-----|
| R1 💎 Kim Cương | 600.000đ/ngày | 800.000đ/ngày |
| R2 🥇 Vàng | 500.000đ/ngày | 750.000đ/ngày |

**Điều kiện nhận:**
1. Đăng ký ca Full-day (08:00–18:00)
2. App online ≥ 95% + AR = 100%
3. FR ≥ ngưỡng Rank, DCR ≤ ngưỡng Rank
4. Không tự huỷ chuyến

**Điều kiện mất:**
- Fail điều kiện 2 lần/tuần → mất tiền đảm bảo cả tuần đó

---

## 6. Ca Làm Việc (Shifts)

| Ca | Giờ | Loại | Ghi chú |
|----|-----|------|---------|
| Ca Sáng | 08:00 – 12:00 | Ca 4 tiếng ⚡ Peak | Peak sáng |
| Ca Chiều | 13:00 – 17:00 | Ca 4 tiếng ⚡ Peak | Peak chiều |
| Ca Tối | 17:00 – 21:00 | Ca 4 tiếng | Bình thường |
| Ca Full-day | 08:00 – 18:00 | Ca 10 tiếng | R1 + R2 only |

### Slot allocation (% / tổng slot mỗi ca)
| Ca | R1 | R2 | R3 | Unranked |
|----|----|----|----|----------|
| Ca Sáng (Peak) | 20% | 40% | 30% | 10% |
| Ca Chiều (Peak) | 20% | 40% | 30% | 10% |
| Ca Tối | 15% | 35% | 35% | 15% |
| Ca Full-day | 50% R1 / 50% R2 | — | — | — |

---

## 7. AhaBenefits — Point Economy

### Công thức tích điểm
```
Điểm/ca = (Thu nhập thực tế ÷ 5.000) × Hệ số Layer + Bonus hoàn ca
```

> Tỉ lệ quy đổi: **5.000đ thu nhập = 1 điểm base**

### Hệ số Layer & Bonus/ca
| Layer | Hệ số × | Bonus/ca |
|-------|---------|----------|
| L2 Minizone | ×2.0 | +60 pts |
| L3 Mediumzone | ×1.7 | +55 pts |
| L4 Bigzone | ×1.3 | +50 pts |
| L5 Cityzone | ×1.0 | +50 pts |
| L6 MASS | ×1.0 | — |

### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng)
| Rank | EPH giả định | Base pts | × Hệ số | + Bonus | Tổng/ca |
|------|-------------|----------|---------|---------|---------|
| R1 · L2 | ~200k/h | 160 | 320 | +60 | **380** |
| R2 · L3 | ~170k/h | 136 | 231 | +55 | **286** |
| R3 · L4 | ~140k/h | 112 | 146 | +50 | **196** |
| L6 MASS | ~110k/h | 88 | 88 | — | **88** |

### Quy tắc điểm
- Hết hạn: **cuối mỗi Quý** (Q1: 31/3, Q2: 30/6, Q3: 30/9, Q4: 31/12)
- Phạt ĐBCL: **-200 pts** / vi phạm
- Điểm tối thiểu để đổi: xem catalog từng item

---

## 8. AhaBenefits Catalog — Point Costs

### A. Partner Rewards (Ahamove cost = 0đ)

#### ⛽ Nhiên liệu & Sạc EV
| Item | Điểm | Giới hạn |
|------|------|----------|
| Giảm giá xăng 5% / lần | 600 | Tất cả |
| Giảm giá xăng 10% / lần | 1.100 | Tất cả |
| Giảm giá sạc EV 20% / lần | 800 | Tất cả |
| Combo sạc EV tháng (10%) | 2.000 | R2+ |

#### 🔧 Bảo dưỡng xe
| Item | Điểm | Giới hạn |
|------|------|----------|
| Giảm 15% dầu nhớt / lọc | 900 | Tất cả |
| Giảm 20% bảo dưỡng định kỳ | 1.800 | Tất cả |
| Giảm 30% vá/thay lốp | 1.200 | Tất cả |
| Gói bảo dưỡng ưu tiên | 3.000 | R1 only |

#### 🎽 CCDC & Trang thiết bị
| Item | Điểm | Giới hạn |
|------|------|----------|
| Túi giữ nhiệt tiêu chuẩn | 800 | Tất cả |
| Túi giữ nhiệt cao cấp (XL) | 1.400 | Tất cả |
| Baga / phụ kiện xe | 1.500 | Tất cả |
| Đồng phục 1 bộ | 700 | Tất cả |

#### 🍜 F&B / Tiêu dùng
| Item | Điểm | Giới hạn |
|------|------|----------|
| Voucher F&B partner 50k | 500 | Tất cả |
| Voucher F&B partner 100k | 950 | Tất cả |
| Giảm 10% chuỗi siêu thị | 600 | Tất cả |
| Combo bữa trưa tài xế | 400 | Tất cả |

#### 📱 Data SIM & Viễn thông
| Item | Điểm | Giới hạn |
|------|------|----------|
| Data 5GB ưu đãi tài xế | 450 | Tất cả |
| Data 10GB ưu đãi tài xế | 800 | Tất cả |
| Data 20GB ưu đãi tài xế | 1.500 | Tất cả |
| Gói SIM ưu tiên cao tốc | 2.200 | R2+ |

#### 🏥 Sức khoẻ & Bảo vệ
| Item | Điểm | Giới hạn |
|------|------|----------|
| Giảm 20% khám tổng quát | 1.500 | Tất cả |
| Giảm 15% mua thuốc tại nhà thuốc | 600 | Tất cả |
| Bảo hiểm tai nạn 1 tháng | 2.500 | R2+ |
| Bảo hiểm tai nạn 3 tháng | 6.000 | R1 only |

---

### B. Rank Entitlements — Tự động theo Rank (nằm trong 200M budget)

| Rank | Item | Giá trị | Chi phí Ahamove | Số lượng | ~Cost/tháng |
|------|------|---------|----------------|----------|-------------|
| 💎 Kim Cương | Voucher xăng/EV | 50k/tháng | ~37.5k (75% giá) | ~1.575 | ~59M |
| 💎 Kim Cương | Khám sức khoẻ | 1 lần/năm | ~21k/tháng (250k÷12) | ~1.575 | ~33M |
| 🥇 Vàng | Voucher xăng/EV | 30k/tháng | ~22.5k (75% giá) | ~3.675 | ~83M |
| **Tổng** | | | | | **~175M** |
| **Buffer** | | | | | **~25M vs 200M** |

---

## 9. Budget Summary

| Hạng mục | Chi phí/tháng | Ghi chú |
|----------|--------------|---------|
| AhaBenefits paid rewards | ~175M | Xem bảng trên |
| Hourly guarantee | TBD | Tách biệt, cần EPH data |
| Full-day guarantee | TBD | Tách biệt, cần EPH data |
| **AhaBenefits budget** | **≤ 200M** | Buffer ~25M |

---

*Cập nhật lần cuối: 2026-05-27 | Driver Management Team*
