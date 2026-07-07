# Driver Ranking & AhaBenefits v2.0 — Params Sheet
> File này chứa toàn bộ con số có thể điều chỉnh. Sau khi sửa ở đây → cập nhật vào HTML tương ứng.
> HTML: `2026-05-driver-ranking-layer-benefits.html`

---

## 1. Ranking KPI Thresholds

> Cả 3 rank đều xét bằng **DQS** (Driver Quality Score). Không dùng AR/FR/Rating riêng lẻ.

| Rank | DQS | Productivity (stp/tháng) |
| --- | --- | --- |
| R1 Elite | ≥ 80 | ≥ 280 |
| R2 Active | ≥ 75 | ≥ 210 |
| R3 Standard | ≥ 75 | ≥ 70 |
| Unranked | < 75 | — |

---

## 2. Fleet Target Ratio (% of monthly actives)

| Rank | Target % | Số lượng |
|------|----------|--------------------------|
| R1 💎 Kim Cương | 10-15% | ~1.000 - 1.500 |
| R2 🥇 Vàng | 10-15% | ~1.000 - 1.500 |
| R3 🥈 Bạc | 30-40% | ~4.000 - 6.000 |
| Unranked | 30-40% | ~4.000 - 6.000 |

---

## 3. Layer Access & Priority Registration Window

| Rank | Zone được phép đăng ký | Giờ mở cổng (Ngày 1) | Ghi chú |
|------|------------------------|----------------------|---------|
| R1 Elite | Tất cả (L2 - L6) | **00:00 - 10:00** | Ưu tiên tuyệt đối FCFS |
| R2 Active | Tất cả (L2 - L6) | **10:00 - 14:00** | Ưu tiên sau R1 |
| R3 Standard | Tất cả (L2 - L6) | **14:00 - 24:00** | Ưu tiên sau R2 |
| Unranked | L5-6 MASS (slot trống còn lại) | **Ngày 2+** | Chỉ đăng ký slot thừa |

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

---

## 7. Quyền lợi theo Layer (AhaBenefits)

### Công thức tích điểm
```
earned_pts = round( round(trip_GSV ÷ 1,000) × layer_multiplier )
```

> Tỉ lệ quy đổi: **1.000đ thu nhập = 1 điểm base**

### Hệ số Layer & Đội trưởng

| Layer | Hệ số × | Hỗ trợ | Ghi chú |
| --- | --- | --- | --- |
| L2 Minizone | ×1.5 | Có Đội trưởng hỗ trợ | R1 priority zone |
| L3 Mediumzone | ×1.3 | Có Đội trưởng hỗ trợ | R2 priority zone |
| L4 Bigzone | ×1.1 | Không | R3 priority zone |
| L5 Cityzone | ×1.0 | Không | |
| L6 MASS | ×1.0 | Không | Unranked |
| **Overflow** | **×1.0** | Không | Đơn tràn ngoài layer hoạt động |

> Hệ số áp theo **đơn hàng** và tài xế Layer, không theo rank tài xế. Tài xế R1 đăng ký ca L3 và nhận đơn overflow từ L3 vẫn chỉ được ×1.3 (hệ số L3), không phải ×1.5. Khi Tài xế không đăng ký hoặc không trong ca hoạt động thì thì hệ số nhân điểm của đơn hàng đó là 1.0. 

### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng)

| Rank | EPH giả định | Base pts | × Hệ số | Tổng/ca |
| --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 280 | 280 × 1.5 = 420 | **420** |
| R2 · L3 | ~65k/h → 260k/ca | 260 | 260 × 1.3 = 338 | **338** |
| R3 · L4 | ~60k/h → 240k/ca | 240 | 240 × 1.1 = 264 | **264** |
| L6 MASS | ~55k/h → 220k/ca | 220 | 220 × 1.0 = 220 | **220** |
| Overflow (any) | — | base | ×1.0 | base only |

### Calibration Formula — Mục tiêu đổi điểm/tháng

```text
Pts tích/tháng (avg, 22 ca):
  R1: 420 × 22 = 9.240 pts  (15% fleet)
  R2: 338 × 22 = 7.436 pts  (35% fleet)
  R3: 264 × 22 = 5.808 pts  (35% fleet)
  L6: 220 × 22 = 4.840 pts  (15% fleet)
  Weighted avg ≈ 6.747 pts/tháng

80% burn → paid reward:  6.747 × 80% = ~5.398 pts ≈ 50.000 VND
  → Paid reward 50k = 5.000 pts (cân chỉnh lại giá trị điểm: 1 điểm = 10đ)

20% còn lại → free partner:  ~1.349 pts/tháng
  → Free items giá 200–850 pts → đổi được 1–4 món/tháng
```

| Rank | Pts/tháng | 80% → Paid 50k (5.000p) | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 9.240 | ✅ 5.000 pts (dư ~4.240) | ~4.000 pts free |
| R2 | 7.436 | ✅ 5.000 pts (dư ~2.436) | ~2.000 pts free |
| R3 | 5.808 | ✅ 5.000 pts (dư ~808) | ~4.000 pts free |
| L6 | 4.840 | ❌ cần ~1.1 tháng | — động lực lên R3 |

### Quy tắc điểm

- Hết hạn: **cuối mỗi Quý** (Q1: 31/3, Q2: 30/6, Q3: 30/9, Q4: 31/12)
- Phạt ĐBCL: **-50 pts** / vi phạm
- Điểm tối thiểu để đổi: xem catalog từng item

---

## 8. AhaBenefits Catalog — Point Costs

> **Công thức giá điểm: Điểm = Giá trị thực (VND) ÷ 10** (đối với Paid Items)
> Catalog đổi điểm mới chia làm Free Items (Partnership tài trợ) và Paid Items (Ahamove trả tiền).

### A. Partner Rewards — Phân theo Rank

> Unranked / L6 không có quyền truy cập catalog, chỉ truy cập được các rewards mass — tạo động lực đạt R3.

#### Free Items (Partnership — 0 cash cost cho Ahamove)

##### 🥈 R3+ Bạc trở lên — Quyền lợi cơ bản
- **Voucher xăng 30k:** 3.000 pts (Giá trị: 30.000đ)
- **Voucher sạc EV 30k:** 3.000 pts (Giá trị: 30.000đ)
- **Thay nhớt cơ bản:** 5.000 pts (Giá trị: ~50.000đ)
- **Voucher cơm/bún 20k:** 2.000 pts (Giá trị: 20.000đ)

##### 🥇 R2+ Vàng trở lên — Quyền lợi nâng cao
- **Voucher xăng 50k:** 5.000 pts (Giá trị: 50.000đ)
- **Voucher sạc EV 50k:** 5.000 pts (Giá trị: 50.000đ)
- **Gói bảo dưỡng tiêu chuẩn:** 15.000 pts (Giá trị: ~150.000đ)
- **Voucher F&B đối tác 50k:** 5.000 pts (Giá trị: 50.000đ)
- **Khám sức khỏe cơ bản:** 4.000 pts

##### 💎 R1 Kim Cương — Đặc quyền cao nhất
- **Gói bảo dưỡng ưu tiên R1:** 25.000 pts (Giá trị: ~250.000đ)
- **Voucher F&B đối tác 100k:** 10.000 pts (Giá trị: 100.000đ)
- **Gói khám đầy đủ:** 17.000 pts

#### Paid Items (Ahamove-funded)

##### 🥈 R3+ Bạc trở lên
- **Data 4G 5GB (30 ngày):** 5.000 pts (Chi phí Aha: ~50.000đ)
- **Áo thun Ahamove:** 12.000 pts (Chi phí Aha: ~120.000đ)

##### 🥇 R2+ Vàng trở lên
- **Data 4G 10GB (30 ngày):** 8.000 pts (Chi phí Aha: ~80.000đ)
- **Combo (áo + túi nhiệt):** 25.000 pts (Chi phí Aha: ~250.000đ)
- **Bộ phụ kiện xe (gương, đèn):** 30.000 pts (Chi phí Aha: ~300.000đ)

##### 💎 R1 Kim Cương
- **Data 4G 20GB (30 ngày):** 15.000 pts (Chi phí Aha: ~150.000đ)
- **Bảo hiểm tai nạn 10k/tháng:** 1.000 pts/tháng
- **Bảo hiểm tai nạn 30k/tháng:** 3.000 pts/tháng

---

### B. Rank Entitlements — Đặc quyền theo Rank

| | 💎 R1 Kim Cương | 🥇 R2 Vàng | 🥈 R3 Bạc |
| --- | --- | --- | --- |
| Voucher xăng/EV | 50k/tháng | 30k/tháng | — |
| Bảo hiểm tai nạn Mini | 1.000–3.000 pts/tháng | — | — |
| Cost Ahamove | ~59M/tháng (voucher) + biến phí BH | ~83M/tháng | — |

**Cơ chế Bảo hiểm tai nạn R1:**

- Đăng ký trong app **trước ngày 25**, hiệu lực từ **ngày 01 tháng kế tiếp**
- Thanh toán bằng điểm: 10k/tháng = 1.000 pts · 30k/tháng = 3.000 pts
- Huỷ trước ngày 25 → ngừng hiệu lực cuối tháng; mất R1 → không gia hạn được

> Budget 200M: Voucher xăng R1+R2 = **~142M** · Buffer ~58M. BH tai nạn là biến phí ngoài budget, cần duyệt riêng (tối đa ~47M nếu 100% R1 đăng ký gói 30k).

---

## 9. Bảng Tổng Hợp Benefits — Theo Rank & Layer

### 9.1 Tổng hợp theo Rank

| Benefit | 💎 R1 Kim Cương | 🥇 R2 Vàng | 🥈 R3 Bạc | Unranked |
| --- | --- | --- | --- | --- |
| **Điều kiện xét** | DQS ≥80, Prod ≥280 | DQS ≥75, Prod ≥210 | DQS ≥75, Prod ≥70 | Dưới R3 |
| **Primary Layer** | L2 Minizone | L3 Mediumzone | L4 Bigzone | L6 MASS |
| **Ca Full-day** | ✅ 08:00–18:00 | ✅ 08:00–18:00 | ❌ | ❌ |
| **Slot đăng ký** | Tất cả L2-L6 | Tất cả L2-L6 | Tất cả L2-L6 | L5-6 MASS |
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
| **Hỗ trợ** | Đội trưởng | Đội trưởng | Không | Không | Không |
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
