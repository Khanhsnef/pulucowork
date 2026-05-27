# Driver Ranking & AhaBenefits v2.0 — Params Sheet
> File này chứa toàn bộ con số có thể điều chỉnh. Sau khi sửa ở đây → cập nhật vào HTML tương ứng.
> HTML: `2026-05-driver-ranking-layer-benefits.html`

---

## 1. Ranking KPI Thresholds

> Cả 3 rank đều xét bằng **DQS** (Driver Quality Score). Không dùng AR/FR/Rating riêng lẻ.

| Rank | DQS | DCR (%) | Productivity (stp/tháng) |
| --- | --- | --- | --- |
| R1 Elite | ≥ 80 | ≤ 10 | ≥ 280 |
| R2 Active | ≥ 75 | ≤ 10 | ≥ 210 |
| R3 Standard | ≥ 75 | ≤ 15 | ≥ 70 |
| Unranked | < 75 | — | — |

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

## 4. Thu nhập tối đa / giờ (Target Earning)

> Ahamove thiết kế phân bổ đơn & layer để **tối đa hóa thu nhập tài xế lên đến** mức mục tiêu dưới đây.
> Đây là **earning target**, không phải guarantee — Ahamove không bù tiền nếu thực tế thấp hơn.
> Tài xế đạt mức này khi đủ KPI ca + layer hoạt động đúng công suất.

### SGN

| Layer | Thu nhập tối đa/h |
| --- | --- |
| L2 Minizone | lên đến 65.000đ |
| L3 Mediumzone | lên đến 60.000đ |
| L4 Bigzone | lên đến 55.000đ |
| L5 Cityzone | lên đến 55.000đ |

### HAN

| Layer | Thu nhập tối đa/h |
| --- | --- |
| L2 Minizone | lên đến 70.000đ |
| L3 Mediumzone | lên đến 65.000đ |
| L4 Bigzone | lên đến 60.000đ |
| L5 Cityzone | lên đến 60.000đ |

---

## 5. Full-day Guarantee (Đảm bảo ngày — R1 & R2 only)

| Rank | SGN | HAN |
|------|-----|-----|
| R1 💎 Kim Cương | 600.000đ/ngày | 650.000đ/ngày |
| R2 🥇 Vàng | 550.000đ/ngày | 600.000đ/ngày |

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

| Ca | R1 | R2 | R3 |
| --- | --- | --- | --- |
| Ca Sáng (Peak) | 20% | 40% | 40% |
| Ca Chiều (Peak) | 20% | 40% | 40% |
| Ca Tối | 15% | 40% | 45% |
| Ca Full-day | 50% | 50% | — |

> Unranked không có structured slot — nhận đơn on-demand từ khi đơn từ các layer tràn xuống.

---

## 7. AhaBenefits — Point Economy

### Công thức tích điểm
```
Điểm/ca = (Thu nhập thực tế ÷ 5.000) × Hệ số Layer + Bonus hoàn ca
```

> Tỉ lệ quy đổi: **5.000đ thu nhập = 1 điểm base**

### Hệ số Layer & Bonus/ca

| Layer | Hệ số × | Bonus/ca | Ghi chú |
| --- | --- | --- | --- |
| L2 Minizone | ×1.5 | +30 pts | R1 priority zone |
| L3 Mediumzone | ×1.3 | +25 pts | R2 priority zone |
| L4 Bigzone | ×1.1 | +20 pts | R3 priority zone |
| L5 Cityzone | ×1.0 | +20 pts | |
| L6 MASS | ×1.0 | — | Unranked on-demand |
| **Overflow** | **×1.0** | **—** | Đơn L2/L3/L4 cascade ra tài xế ngoài layer → ×1.0, không cộng bonus |

> Hệ số áp theo **đơn hàng**, không theo rank tài xế. Tài xế R1 nhận đơn overflow từ L3 vẫn chỉ được ×1.3 (hệ số L3), không phải ×1.5.

### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng)

| Rank | EPH giả định | Base pts | × Hệ số | + Bonus | Tổng/ca |
| --- | --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 56 | 84 | +30 | **114** |
| R2 · L3 | ~65k/h → 260k/ca | 52 | 68 | +25 | **93** |
| R3 · L4 | ~60k/h → 240k/ca | 48 | 53 | +20 | **73** |
| L6 MASS | ~55k/h → 220k/ca | 44 | 44 | — | **44** |
| Overflow (any) | — | base | ×1.0 | — | base only |

### Calibration Formula — Mục tiêu đổi điểm/tháng

```text
Pts tích/tháng (avg, 22 ca):
  R1: 114 × 22 = 2.508 pts  (15% fleet)
  R2:  93 × 22 = 2.046 pts  (35% fleet)
  R3:  73 × 22 = 1.606 pts  (35% fleet)
  L6:  44 × 22 =   968 pts  (15% fleet)
  Weighted avg ≈ 1.800 pts/tháng

80% burn → paid reward:  1.800 × 80% = ~1.440 pts ≈ 50.000 VND
  → 1 pt ≈ 35đ giá trị (tương đương 0.7% GSV mang về)
  → Paid reward 50k = 1.500 pts (làm tròn)

20% còn lại → free partner:  ~360 pts/tháng
  → Free items giá 50–300 pts → đổi được 2–5 món/tháng
```

| Rank | Pts/tháng | 80% → Paid 50k | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 2.508 | ✅ 1.500 pts (dư ~1.000) | ~1.000 pts free |
| R2 | 2.046 | ✅ 1.500 pts (dư ~550) | ~550 pts free |
| R3 | 1.606 | ✅ 1.500 pts (~1.1 tháng) | ~100 pts free |
| L6 | 968 | ❌ cần ~1.6 tháng | — động lực lên R3 |

### Quy tắc điểm

- Hết hạn: **cuối mỗi Quý** (Q1: 31/3, Q2: 30/6, Q3: 30/9, Q4: 31/12)
- Phạt ĐBCL: **-50 pts** / vi phạm
- Điểm tối thiểu để đổi: xem catalog từng item

---

## 8. AhaBenefits Catalog — Point Costs

> **Công thức giá điểm: Điểm = Giá trị reward (VND) ÷ 35**
> Tương đương 0.7% GSV tài xế mang về (base, ×1.0) hoặc 0.3–0.5% GSV khi có layer multiplier.
> Cột "Giá trị est." là giá trị kinh tế thực của reward với tài xế — cần Finance/partner validate.

### A. Partner Rewards (Ahamove cost = 0đ)

#### ⛽ Nhiên liệu & Sạc EV

| Item | Giá trị est. | Điểm (÷35) | Giới hạn |
| --- | --- | --- | --- |
| Giảm xăng 5% / lần (~đổ 200k) | ~10.000đ | 285 → **300** | Tất cả |
| Giảm xăng 10% / lần | ~20.000đ | 571 → **550** | Tất cả |
| Sạc EV 20% / lần (~sạc 80k) | ~16.000đ | 457 → **450** | Tất cả |
| Combo sạc EV tháng 10% | ~40.000đ | 1.143 → **1.100** | R2+ |

#### 🔧 Bảo dưỡng xe

| Item | Giá trị est. | Điểm (÷35) | Giới hạn |
| --- | --- | --- | --- |
| Giảm 15% dầu nhớt / lọc (~150k) | ~22.500đ | 643 → **650** | Tất cả |
| Giảm 20% bảo dưỡng định kỳ (~250k) | ~50.000đ | 1.429 → **1.400** | Tất cả |
| Giảm 30% vá / thay lốp (~100k) | ~30.000đ | 857 → **850** | Tất cả |
| Gói bảo dưỡng ưu tiên R1 (~300k) | ~90.000đ | 2.571 → **2.550** | R1 only |

#### 🎽 CCDC & Trang thiết bị

| Item | Giá trị est. | Điểm (÷35) | Giới hạn |
| --- | --- | --- | --- |
| Túi giữ nhiệt tiêu chuẩn | ~50.000đ | 1.429 → **1.400** | Tất cả |
| Túi giữ nhiệt cao cấp (XL) | ~80.000đ | 2.286 → **2.300** | Tất cả |
| Baga / phụ kiện xe | ~120.000đ | 3.429 → **3.400** | Tất cả |
| Đồng phục 1 bộ | ~60.000đ | 1.714 → **1.700** | Tất cả |

#### 🍜 F&B / Tiêu dùng

| Item | Giá trị est. | Điểm (÷35) | Giới hạn |
| --- | --- | --- | --- |
| Voucher F&B partner 50k | 50.000đ | 1.429 → **1.400** | Tất cả |
| Voucher F&B partner 100k | 100.000đ | 2.857 → **2.850** | Tất cả |
| Giảm 10% siêu thị (~200k basket) | ~20.000đ | 571 → **550** | Tất cả |
| Combo bữa trưa tài xế | ~25.000đ | 714 → **700** | Tất cả |

#### 📱 Data SIM & Viễn thông

| Item | Giá trị est. | Điểm (÷35) | Giới hạn |
| --- | --- | --- | --- |
| Data 5GB ưu đãi tài xế | ~15.000đ | 429 → **400** | Tất cả |
| Data 10GB ưu đãi tài xế | ~25.000đ | 714 → **700** | Tất cả |
| Data 20GB ưu đãi tài xế | ~50.000đ | 1.429 → **1.400** | Tất cả |
| Gói SIM ưu tiên cao tốc / tháng | ~80.000đ | 2.286 → **2.300** | R2+ |

#### 🏥 Sức khoẻ & Bảo vệ

| Item | Giá trị est. | Điểm (÷35) | Giới hạn |
| --- | --- | --- | --- |
| Giảm 20% khám tổng quát (~300k) | ~60.000đ | 1.714 → **1.700** | Tất cả |
| Giảm 15% mua thuốc (~100k) | ~15.000đ | 429 → **400** | Tất cả |

---

### B. Rank Entitlements — Tự động & Đặc quyền theo Rank

#### 💎 R1 Exclusive — Mua bảo hiểm tai nạn theo tháng

> **Đặc quyền mua**, không tự động cấp — Ahamove đàm phán group rate, R1 được quyền đăng ký.

| Cơ chế | Chi tiết |
| --- | --- |
| Đối tượng | R1 Elite (💎 Kim Cương) only |
| Cách mua | Đăng ký trong app trước ngày 25 hàng tháng |
| Hiệu lực | Từ ngày 01 tháng kế tiếp |
| Phí | 10.000đ – 30.000đ/tháng (gói Mini, group rate) |
| Thanh toán | Trừ thẳng vào ví tài xế |
| Huỷ | Có thể huỷ trước ngày 25, ngừng hiệu lực cuối tháng |
| Mất R1 | Không được gia hạn tháng tiếp — coverage tháng đã mua vẫn giữ đến hết tháng |

> Cost Ahamove = 0đ. Driver tự trả phí, Ahamove chỉ là aggregator để có group rate tốt hơn.

#### 💰 Paid Entitlements (Ahamove chi — nằm trong 200M budget)

| Rank | Item | Giá trị | Chi phí Ahamove | Số lượng | ~Cost/tháng |
| --- | --- | --- | --- | --- | --- |
| 💎 Kim Cương | Voucher xăng/EV | 50k/tháng | ~37.5k (75% giá) | ~1.575 | ~59M |
| 🥇 Vàng | Voucher xăng/EV | 30k/tháng | ~22.5k (75% giá) | ~3.675 | ~83M |
| **Tổng** | | | | | **~142M** |
| **Buffer** | | | | | **~58M vs 200M** |

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
