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

## 3. Layer Access & Priority Registration Window

| Rank | Zone được phép đăng ký | Giờ mở cổng (Ngày 1) | Ghi chú |
|------|------------------------|----------------------|---------|
| R1 Elite | Tất cả (L2 - L6) | **00:00 - 10:00** | Ưu tiên tuyệt đối FCFS |
| R2 Active | Tất cả (L2 - L6) | **10:00 - 14:00** | Ưu tiên sau R1 |
| R3 Standard | Tất cả (L2 - L6) | **14:00 - 24:00** | Ưu tiên sau R2 |
| Unranked | L6 MASS (slot trống còn lại) | **Ngày 2+** | Chỉ đăng ký slot thừa |

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
Điểm/ca = (Thu nhập thực tế ÷ 1.000) × Hệ số Layer
```

> Tỉ lệ quy đổi: **1.000đ thu nhập = 1 điểm base**

### Hệ số Layer & Bonus/ca

| Layer | Hệ số × | Ghi chú |
| --- | --- | --- |
| L2 Minizone | ×1.5 | R1 priority zone |
| L3 Mediumzone | ×1.3 | R2 priority zone |
| L4 Bigzone | ×1.1 | R3 priority zone |
| L5 Cityzone | ×1.0 | |
| L6 MASS | ×1.0 | Unranked |
| **Overflow** | **×1.0** | Đơn tràn ngoài layer hoạt động |

> Hệ số áp theo **đơn hàng**, không theo rank tài xế. Tài xế R1 nhận đơn overflow từ L3 vẫn chỉ được ×1.3 (hệ số L3), không phải ×1.5.

### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng)

| Rank | EPH giả định | Base pts | × Hệ số | Tổng/ca |
| --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 280 | ×1.5 | **420** |
| R2 · L3 | ~65k/h → 260k/ca | 260 | ×1.3 | **338** |
| R3 · L4 | ~60k/h → 240k/ca | 240 | ×1.1 | **264** |
| L6 MASS | ~55k/h → 220k/ca | 220 | ×1.0 | **220** |
| Overflow (any) | — | base | ×1.0 | — | base only |

### Calibration Formula — Mục tiêu đổi điểm/tháng

```text
Pts tích/tháng (avg, 22 ca):
  R1: 420 × 22 = 9.240 pts  (15% fleet)
  R2: 338 × 22 = 7.436 pts  (35% fleet)
  R3: 264 × 22 = 5.808 pts  (35% fleet)
  L6: 220 × 22 = 4.840 pts  (15% fleet)
  Weighted avg ≈ 6.747 pts/tháng

80% burn → paid reward:  6.747 × 80% = ~5.398 pts ≈ 50.000 VND
  → 1 pt ≈ 7đ giá trị (tương đương 0.7% GSV mang về)
  → Paid reward 50k = 7.000 pts (làm tròn)

20% còn lại → free partner:  ~1.350 pts/tháng
  → Free items giá 250–1.500 pts → đổi được 2–5 món/tháng
```

| Rank | Pts/tháng | 80% → Paid 50k | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 9.240 | ✅ 7.000 pts (dư ~2.240) | ~2.240 pts free |
| R2 | 7.436 | ✅ 7.000 pts (dư ~436) | ~436 pts free |
| R3 | 5.808 | ✅ 7.000 pts (~1.2 tháng) | ~500 pts free |
| L6 | 4.840 | ❌ cần ~1.4 tháng | — động lực lên R3 |

### Quy tắc điểm

- Hết hạn: **cuối mỗi Quý** (Q1: 31/3, Q2: 30/6, Q3: 30/9, Q4: 31/12)
- Phạt ĐBCL: **-250 pts** / vi phạm
- Điểm tối thiểu để đổi: xem catalog từng item

---

## 8. AhaBenefits Catalog — Point Costs

> **Công thức giá điểm: Điểm = Giá trị reward (VND) ÷ 7**
> Tương đương 0.7% GSV tài xế mang về (base, ×1.0) hoặc 0.3–0.5% GSV khi có layer multiplier.
> Cột "Giá trị est." là giá trị kinh tế thực của reward với tài xế — cần Finance/partner validate.

### A. Partner Rewards — Phân theo Rank

> Unranked / L6 không có quyền truy cập catalog — tạo động lực đạt R3.

#### 🥈 R3+ Bạc trở lên — Quyền lợi cơ bản

| Danh mục | Item | Giá trị est. | Điểm |
| --- | --- | --- | --- |
| ⛽ Xăng/EV | Giảm xăng 5% / lần (~đổ 200k) | ~10.000đ | **1.500** |
| ⛽ Xăng/EV | Sạc EV 20% / lần (~sạc 80k) | ~16.000đ | **2.250** |
| 🔧 Bảo dưỡng | Giảm 30% vá / thay lốp (~100k) | ~30.000đ | **4.250** |
| 🍜 F&B | Combo bữa trưa tài xế | ~25.000đ | **3.500** |
| 🍜 F&B | Giảm 10% siêu thị (~200k basket) | ~20.000đ | **2.750** |
| 📱 Data | Data 5GB ưu đãi tài xế | ~15.000đ | **2.000** |
| 🏥 Sức khoẻ | Giảm 15% mua thuốc (~100k) | ~15.000đ | **2.000** |

#### 🥇 R2+ Vàng trở lên — Quyền lợi nâng cao

> Bao gồm toàn bộ quyền lợi R3+ và thêm:

| Danh mục | Item | Giá trị est. | Điểm |
| --- | --- | --- | --- |
| ⛽ Xăng/EV | Giảm xăng 10% / lần | ~20.000đ | **2.750** |
| ⛽ Xăng/EV | Combo sạc EV tháng 10% | ~40.000đ | **5.500** |
| 🔧 Bảo dưỡng | Giảm 15% dầu nhớt / lọc (~150k) | ~22.500đ | **3.250** |
| 🔧 Bảo dưỡng | Giảm 20% bảo dưỡng định kỳ (~250k) | ~50.000đ | **7.000** |
| 🎽 CCDC | Túi giữ nhiệt tiêu chuẩn | ~50.000đ | **7.000** |
| 🎽 CCDC | Đồng phục 1 bộ | ~60.000đ | **8.500** |
| 🍜 F&B | Voucher F&B partner 50k | ~50.000đ | **7.000** |
| 📱 Data | Data 10GB ưu đãi tài xế | ~25.000đ | **3.500** |
| 📱 Data | Data 20GB ưu đãi tài xế | ~50.000đ | **7.000** |
| 🏥 Sức khoẻ | Giảm 20% khám tổng quát (~300k) | ~60.000đ | **8.500** |

#### 💎 R1 Kim Cương — Đặc quyền cao nhất

> Bao gồm toàn bộ quyền lợi R2+ và thêm:

| Danh mục | Item | Giá trị est. | Điểm |
| --- | --- | --- | --- |
| ⛽ Xăng/EV | Gói sạc EV ưu tiên tháng (15%) | ~60.000đ | **8.500** |
| 🔧 Bảo dưỡng | Gói bảo dưỡng ưu tiên (~300k) | ~90.000đ | **12.750** |
| 🎽 CCDC | Túi giữ nhiệt cao cấp (XL) | ~80.000đ | **11.500** |
| 🎽 CCDC | Baga / phụ kiện xe | ~120.000đ | **17.000** |
| 🍜 F&B | Voucher F&B partner 100k | ~100.000đ | **14.250** |
| 📱 Data | Gói SIM ưu tiên cao tốc / tháng | ~80.000đ | **11.500** |
| 🛡️ Bảo hiểm | Bảo hiểm tai nạn Mini (đổi điểm để mua) | 10k–30k/tháng | **1.425–4.285** |

---

### B. Rank Entitlements — Đặc quyền theo Rank

| | 💎 R1 Kim Cương | 🥇 R2 Vàng | 🥈 R3 Bạc |
| --- | --- | --- | --- |
| Voucher xăng/EV | 50k/tháng | 30k/tháng | — |
| Bảo hiểm tai nạn Mini | 1.425–4.285 pts/tháng | — | — |
| Cost Ahamove | ~59M/tháng (voucher) + biến phí BH | ~83M/tháng | — |

**Cơ chế Bảo hiểm tai nạn R1:**

- Đăng ký trong app **trước ngày 25**, hiệu lực từ **ngày 01 tháng kế tiếp**
- Thanh toán bằng điểm: 10k/tháng = 1.425 pts · 30k/tháng = 4.285 pts
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
| **Khung giờ đăng ký ca (Ngày 1)** | 00:00 - 10:00 | 10:00 - 14:00 | 14:00 - 24:00 | Ngày 2+ |
| **AhaBenefits** | 💎 Kim Cương | 🥇 Vàng | 🥈 Bạc | ❌ |
| ↳ Hệ số AhaPoints | ×1.5 | ×1.3 | ×1.1 | ×1.0 |
| ↳ Voucher xăng/sạc (tự động) | 50k/tháng | 30k/tháng | — | — |
| ↳ Bảo hiểm tai nạn Mini | ✅ R1 only | ❌ | ❌ | ❌ |
| ↳ Catalog đặc quyền | Kim Cương + Vàng + Bạc | Vàng + Bạc | Bạc only | ❌ |

---

### 9.2 Tổng hợp theo Layer

| | **L2 Minizone** | **L3 Mediumzone** | **L4 Bigzone** | **L5 Cityzone** | **L6 MASS** |
| --- | --- | --- | --- | --- | --- |
| **Hạng ưu tiên** | R1 | R2 | R3 | Bất kỳ | Unranked |
| **AhaBenefits ×** | ×1.5 | ×1.3 | ×1.1 | ×1.0 | ×1.0 |
| **Cơ chế mở cổng** | Mở theo khung giờ | Mở theo khung giờ | Mở theo khung giờ | Mở tự do | Mở tự do |

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
| **Thu nhập target** | Theo Layer | Theo Layer | Theo Layer | Giờ mở R1/R2 |

---

*Cập nhật lần cuối: 2026-05-27 | Driver Management Team*
