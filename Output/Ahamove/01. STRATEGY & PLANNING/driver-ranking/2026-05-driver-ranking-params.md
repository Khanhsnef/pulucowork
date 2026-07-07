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
earned_pts = round( round(trip_GSV ÷ 5,000) × layer_multiplier )
```

> Tỉ lệ quy đổi: **5.000đ thu nhập = 1 điểm base**

### Hệ số Layer & Bonus/ca

| Layer | Hệ số × | Bonus/ca | Ghi chú |
| --- | --- | --- | --- |
| L2 Minizone | ×1.5 | +30 pts | R1 priority zone |
| L3 Mediumzone | ×1.3 | +25 pts | R2 priority zone |
| L4 Bigzone | ×1.1 | +20 pts | R3 priority zone |
| L5 Cityzone | ×1.0 | — | |
| L6 MASS | ×1.0 | — | Unranked |
| **Overflow** | **×1.0** | — | Đơn tràn ngoài layer hoạt động |

> Hệ số áp theo **đơn hàng**, không theo rank tài xế. Tài xế R1 nhận đơn overflow từ L3 vẫn chỉ được ×1.3 (hệ số L3), không phải ×1.5.

### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng + Bonus)

| Rank | EPH giả định | Base pts | × Hệ số | Bonus ca | Tổng/ca |
| --- | --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 56 | 56 × 1.5 = 84 | +30 | **114** |
| R2 · L3 | ~65k/h → 260k/ca | 52 | 52 × 1.3 = 68 | +25 | **93** |
| R3 · L4 | ~60k/h → 240k/ca | 48 | 48 × 1.1 = 53 | +20 | **73** |
| L6 MASS | ~55k/h → 220k/ca | 44 | 44 × 1.0 = 44 | — | **44** |
| Overflow (any) | — | base | ×1.0 | — | base only |

### Calibration Formula — Mục tiêu đổi điểm/tháng

```text
Pts tích/tháng (avg, 22 ca):
  R1: 114 × 22 = 2.508 pts  (15% fleet)
  R2: 93 × 22 = 2.046 pts  (35% fleet)
  R3: 73 × 22 = 1.606 pts  (35% fleet)
  L6: 44 × 22 = 968 pts  (15% fleet)
  Weighted avg ≈ 1.836 pts/tháng

80% burn → paid reward:  1.836 × 80% = ~1.468 pts ≈ 50.000 VND
  → Paid reward 50k = 1.500 pts (làm tròn)

20% còn lại → free partner:  ~360 pts/tháng
  → Free items giá 40–170 pts → đổi được 2–5 món/tháng
```

| Rank | Pts/tháng | 80% → Paid 50k | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 2.508 | ✅ 1.500 pts (dư ~1.008) | ~1.000 pts free |
| R2 | 2.046 | ✅ 1.500 pts (dư ~546) | ~500 pts free |
| R3 | 1.606 | ✅ 1.500 pts (~1 tháng) | ~100 pts free |
| L6 | 968 | ❌ cần ~1.5 tháng | — động lực lên R3 |

### Quy tắc điểm

- Hết hạn: **cuối mỗi Quý** (Q1: 31/3, Q2: 30/6, Q3: 30/9, Q4: 31/12)
- Phạt ĐBCL: **-50 pts** / vi phạm
- Điểm tối thiểu để đổi: xem catalog từng item

---

## 8. AhaBenefits Catalog — Point Costs

> **Công thức giá điểm: Điểm = Giá trị thực (VND) ÷ 35** (đối với Paid Items)
> Catalog đổi điểm mới chia làm Free Items (Partnership tài trợ) và Paid Items (Ahamove trả tiền).

### A. Partner Rewards — Phân theo Rank

> Unranked / L6 không có quyền truy cập catalog — tạo động lực đạt R3.

#### Free Items (Partnership — 0 cash cost cho Ahamove)

##### 🥈 R3+ Bạc trở lên — Quyền lợi cơ bản
- **Voucher xăng 30k:** 170 pts (Giá trị: 30.000đ)
- **Voucher sạc EV 30k:** 170 pts (Giá trị: 30.000đ)
- **Thay nhớt cơ bản:** 65 pts (Giá trị: ~50.000đ)
- **Voucher cơm/bún 20k:** 55 pts (Giá trị: 20.000đ)

##### 🥇 R2+ Vàng trở lên — Quyền lợi nâng cao
- **Voucher xăng 50k:** 285 pts (Giá trị: 50.000đ)
- **Voucher sạc EV 50k:** 285 pts (Giá trị: 50.000đ)
- **Gói bảo dưỡng tiêu chuẩn:** 170 pts (Giá trị: ~150.000đ)
- **Voucher F&B đối tác 50k:** 140 pts (Giá trị: 50.000đ)
- **Khám sức khỏe cơ bản:** 40 pts

##### 💎 R1 Kim Cương — Đặc quyền cao nhất
- **Gói bảo dưỡng ưu tiên R1:** 255 pts (Giá trị: ~250.000đ)
- **Voucher F&B đối tác 100k:** 285 pts (Giá trị: 100.000đ)
- **Gói khám đầy đủ:** 170 pts

#### Paid Items (Ahamove-funded)

##### 🥈 R3+ Bạc trở lên
- **Data 4G 5GB (30 ngày):** 400 pts (Chi phí Aha: ~50.000đ)
- **Áo thun Ahamove:** 1.400 pts (Chi phí Aha: ~120.000đ)

##### 🥇 R2+ Vàng trở lên
- **Data 4G 10GB (30 ngày):** 700 pts (Chi phí Aha: ~80.000đ)
- **Combo (áo + túi nhiệt):** 2.300 pts (Chi phí Aha: ~250.000đ)
- **Bộ phụ kiện xe (gương, đèn):** 3.400 pts (Chi phí Aha: ~300.000đ)

##### 💎 R1 Kim Cương
- **Data 4G 20GB (30 ngày):** 1.400 pts (Chi phí Aha: ~150.000đ)
- **Bảo hiểm tai nạn 10k/tháng:** 285 pts/tháng
- **Bảo hiểm tai nạn 30k/tháng:** 857 pts/tháng

---

### B. Rank Entitlements — Đặc quyền theo Rank

| | 💎 R1 Kim Cương | 🥇 R2 Vàng | 🥈 R3 Bạc |
| --- | --- | --- | --- |
| Voucher xăng/EV | 50k/tháng | 30k/tháng | — |
| Bảo hiểm tai nạn Mini | 285–857 pts/tháng | — | — |
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
| **Điều kiện xét** | DQS ≥80, DCR <10%, Prod ≥280 | DQS ≥75, DCR <10%, Prod ≥210 | DQS ≥75, DCR ≤15%, Prod ≥70 | Dưới R3 |
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
