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

### 3.1 Ưu tiên Đăng ký tại Layer Overlap

Khi nhiều rank cùng được phép đăng ký một layer (spillover + primary), cửa sổ đăng ký mở **sớm hơn 2 tiếng** cho rank cao hơn.

| Layer | Đợt 1 — ưu tiên (mở sớm 2h) | Đợt 2 — còn lại |
|-------|------------------------------|-----------------|
| **L3** | R1 spillover (do L2 ≥ 80% fill) | R2 primary |
| **L4** | R2 spillover (do L3 ≥ 80% fill) | R3 primary |
| **L5** | R3 spillover (do L4 ≥ 80% fill) | Unranked |
| **L2** | R1 only | — |

> **Đánh đổi:** R1 đăng ký spillover tại L3 → hưởng ×1.3 + bonus +25 pts của L3, **không phải** ×1.5 của L2. Muốn giữ ×1.5 + bonus +30 pts: phải chủ động đăng ký L2 trong cửa sổ ưu tiên trước khi L2 fill.

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

### A. Partner Rewards — Phân theo Rank

> Unranked / L6 không có quyền truy cập catalog — tạo động lực đạt R3.

#### 🥈 R3+ Bạc trở lên — Quyền lợi cơ bản

| Danh mục | Item | Giá trị est. | Điểm |
| --- | --- | --- | --- |
| ⛽ Xăng/EV | Giảm xăng 5% / lần (~đổ 200k) | ~10.000đ | **300** |
| ⛽ Xăng/EV | Sạc EV 20% / lần (~sạc 80k) | ~16.000đ | **450** |
| 🔧 Bảo dưỡng | Giảm 30% vá / thay lốp (~100k) | ~30.000đ | **850** |
| 🍜 F&B | Combo bữa trưa tài xế | ~25.000đ | **700** |
| 🍜 F&B | Giảm 10% siêu thị (~200k basket) | ~20.000đ | **550** |
| 📱 Data | Data 5GB ưu đãi tài xế | ~15.000đ | **400** |
| 🏥 Sức khoẻ | Giảm 15% mua thuốc (~100k) | ~15.000đ | **400** |

#### 🥇 R2+ Vàng trở lên — Quyền lợi nâng cao

> Bao gồm toàn bộ quyền lợi R3+ và thêm:

| Danh mục | Item | Giá trị est. | Điểm |
| --- | --- | --- | --- |
| ⛽ Xăng/EV | Giảm xăng 10% / lần | ~20.000đ | **550** |
| ⛽ Xăng/EV | Combo sạc EV tháng 10% | ~40.000đ | **1.100** |
| 🔧 Bảo dưỡng | Giảm 15% dầu nhớt / lọc (~150k) | ~22.500đ | **650** |
| 🔧 Bảo dưỡng | Giảm 20% bảo dưỡng định kỳ (~250k) | ~50.000đ | **1.400** |
| 🎽 CCDC | Túi giữ nhiệt tiêu chuẩn | ~50.000đ | **1.400** |
| 🎽 CCDC | Đồng phục 1 bộ | ~60.000đ | **1.700** |
| 🍜 F&B | Voucher F&B partner 50k | ~50.000đ | **1.400** |
| 📱 Data | Data 10GB ưu đãi tài xế | ~25.000đ | **700** |
| 📱 Data | Data 20GB ưu đãi tài xế | ~50.000đ | **1.400** |
| 🏥 Sức khoẻ | Giảm 20% khám tổng quát (~300k) | ~60.000đ | **1.700** |

#### 💎 R1 Kim Cương — Đặc quyền cao nhất

> Bao gồm toàn bộ quyền lợi R2+ và thêm:

| Danh mục | Item | Giá trị est. | Điểm |
| --- | --- | --- | --- |
| ⛽ Xăng/EV | Gói sạc EV ưu tiên tháng (15%) | ~60.000đ | **1.700** |
| 🔧 Bảo dưỡng | Gói bảo dưỡng ưu tiên (~300k) | ~90.000đ | **2.550** |
| 🎽 CCDC | Túi giữ nhiệt cao cấp (XL) | ~80.000đ | **2.300** |
| 🎽 CCDC | Baga / phụ kiện xe | ~120.000đ | **3.400** |
| 🍜 F&B | Voucher F&B partner 100k | ~100.000đ | **2.850** |
| 📱 Data | Gói SIM ưu tiên cao tốc / tháng | ~80.000đ | **2.300** |
| 🛡️ Bảo hiểm | Bảo hiểm tai nạn Mini (đổi điểm để mua) | 10k–30k/tháng | **285–857** |

---

### B. Rank Entitlements — Đặc quyền theo Rank

| | 💎 R1 Kim Cương | 🥇 R2 Vàng | 🥈 R3 Bạc |
| --- | --- | --- | --- |
| Voucher xăng/EV | 50k/tháng | 30k/tháng | — |
| Bảo hiểm tai nạn Mini | 10k–30k/tháng · đổi điểm | — | — |
| Cost Ahamove | ~59M/tháng (voucher) + biến phí BH | ~83M/tháng | — |

**Cơ chế Bảo hiểm tai nạn R1:**

- Đăng ký trong app **trước ngày 25**, hiệu lực từ **ngày 01 tháng kế tiếp**
- Thanh toán bằng điểm: 10k/tháng = 285 pts · 30k/tháng = 857 pts
- Huỷ trước ngày 25 → ngừng hiệu lực cuối tháng; mất R1 → không gia hạn được

> Budget 200M: Voucher xăng R1+R2 = **~142M** · Buffer ~58M. BH tai nạn là biến phí ngoài budget, cần duyệt riêng (tối đa ~47M nếu 100% R1 đăng ký gói 30k).

---

## 9. Bảng Tổng Hợp Benefits — Theo Rank & Layer

### 9.1 Tổng hợp theo Rank

| Benefit | 💎 R1 Kim Cương | 🥇 R2 Vàng | 🥈 R3 Bạc | Unranked |
| --- | --- | --- | --- | --- |
| **Điều kiện xét** | DQS ≥80, DCR <10%, Prod ≥280 | DQS ≥75, DCR <10%, Prod ≥210 | DQS ≥70, DCR ≤15%, Prod ≥70 | Dưới R3 |
| **Primary Layer** | L2 Minizone | L3 Mediumzone | L4 Bigzone | L6 MASS |
| **Ca Full-day** | ✅ 08:00–18:00 | ✅ 08:00–18:00 | ❌ | ❌ |
| **Thu nhập target Full-day** | SGN 600k · HAN 650k | SGN 550k · HAN 600k | — | — |
| **Slot ưu tiên Ca Peak** | 20% | 40% | 40% | on-demand |
| **AhaBenefits** | 💎 Kim Cương | 🥇 Vàng | 🥈 Bạc | ❌ |
| ↳ Hệ số AhaPoints | ×1.5 | ×1.3 | ×1.1 | ×1.0 |
| ↳ Bonus hoàn ca | +30 pts | +25 pts | +20 pts | — |
| ↳ Voucher xăng/sạc (tự động) | 50k/tháng | 30k/tháng | — | — |
| ↳ Bảo hiểm tai nạn Mini | ✅ R1 only | ❌ | ❌ | ❌ |
| ↳ Catalog đặc quyền | Kim Cương + Vàng + Bạc | Vàng + Bạc | Bạc only | ❌ |

---

### 9.2 Tổng hợp theo Layer

| | **L2 Minizone** | **L3 Mediumzone** | **L4 Bigzone** | **L5 Cityzone** | **L6 MASS** |
| --- | --- | --- | --- | --- | --- |
| **Rank ưu tiên** | R1 | R2 | R3 | Overflow R3 | Unranked |
| **AhaBenefits ×** | ×1.5 | ×1.3 | ×1.1 | ×1.0 | ×1.0 |
| **Bonus/ca** | +30 pts | +25 pts | +20 pts | +20 pts | — |
| **Overflow** | ×1.0, no bonus | ×1.0, no bonus | ×1.0, no bonus | — | — |
| **Thu nhập mục tiêu SGN** | lên đến 65k/h | lên đến 60k/h | lên đến 55k/h | lên đến 55k/h | — |
| **Thu nhập mục tiêu HAN** | lên đến 70k/h | lên đến 65k/h | lên đến 60k/h | lên đến 60k/h | — |
| **Cascade mở khi** | L2 ≥80% fill | L3 ≥80% fill | L4 ≥80% fill | — | luôn mở |

---

### 9.3 Tổng hợp Ca làm việc

| | **Ca Sáng** | **Ca Chiều** | **Ca Tối** | **Ca Full-day** |
| --- | --- | --- | --- | --- |
| **Giờ** | 08:00–12:00 | 13:00–17:00 | 17:00–21:00 | 08:00–18:00 |
| **Loại** | 4 tiếng ⚡ Peak | 4 tiếng ⚡ Peak | 4 tiếng | 10 tiếng |
| **Slot R1** | 20% | 20% | 15% | 50% |
| **Slot R2** | 40% | 40% | 40% | 50% |
| **Slot R3** | 40% | 40% | 45% | — |
| **Unranked** | on-demand | on-demand | on-demand | ❌ |
| **Thu nhập target** | Theo Layer | Theo Layer | Theo Layer | R1: 600–650k · R2: 550–600k |

---

*Cập nhật lần cuối: 2026-05-27 | Driver Management Team*
