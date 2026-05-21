# Driver Ranking × Priority Registration System
**Ahamove Driver Management | 2026-05**

> Ranking không chỉ là xếp hạng — mà là cơ chế phân bổ quyền đăng ký ca hoạt động,  
> đảm bảo đúng tài xế chất lượng cao vào đúng layer cần họ nhất.

---

## Các quyết định đã xác nhận

| # | Quyết định | Nội dung |
|---|---|---|
| 1 | Chu kỳ tính lại Ranking | **Hàng tháng** (tính vào cuối tháng, áp dụng cho tháng tiếp theo) |
| 2 | Tài xế mới < 1 tháng | Xếp tier **"Chưa xếp hạng"** — chỉ thấy & đăng ký được L6 |
| 3 | Hiển thị điểm cho tài xế | **Có** — cập nhật mỗi ngày (rolling 30 ngày gần nhất) |
| 4 | Xử lý slot còn trống | **Không đóng window tier cao** — R1 vẫn thấy L1 suốt chu kỳ đăng ký. Tiers thấp hơn bị hard-block (không bao giờ nhìn thấy layer không thuộc quyền hạn của mình) |

---

## 1. Công thức Ranking Score

### 1.1 Base Score (0–100 điểm)

| Metric | Weight | Cách tính |
|---|---|---|
| AR (Acceptance Rate) | **37%** | `min(AR / 98%, 1.0) × 100` |
| FR (Fulfillment Rate) | **33%** | `min(FR / 90%, 1.0) × 100` |
| DCR (Cancellation Rate) | **30%** | `max(0, (20% − DCR) / 20%) × 100` |

> DCR đảo chiều: DCR = 0% → 100đ / DCR = 10% → 50đ / DCR ≥ 20% → 0đ.  
> Rating đã loại khỏi công thức. Benchmark AR 98%, FR 90% = ngưỡng max điểm.

**Base Score = AR_score × 37% + FR_score × 33% + DCR_score × 30%**

### 1.2 Prod Bonus (Optional, +0–8 điểm)

> Dùng để tie-break khi 2 tài xế cùng Base Score. Không bắt buộc trong công thức core.

| Prod (stp/tháng) | Bonus |
|---|---|
| ≥ 150 stp | +8 |
| ≥ 100 stp | +5 |
| ≥ 60 stp | +2 |
| < 60 stp | +0 |

**Final Score = Base Score + Prod Bonus** *(capped tại 100)*

### 1.3 Ví dụ tính điểm

| Tài xế | AR | FR | DCR | Prod | Base Score | Prod Bonus | Final Score |
|---|---|---|---|---|---|---|---|
| A | 98% | 93% | 2% | 140 stp | (100×37% + 100×33% + 90×30%) = **97** | +8 | **100** (capped) |
| B | 95% | 87% | 8% | 90 stp | (96.9×37% + 96.7×33% + 60×30%) = **83.7** | +2 | **86** |
| C | 90% | 82% | 12% | 45 stp | (91.8×37% + 91.1×33% + 40×30%) = **75.2** | +0 | **75** |
| D | 82% | 73% | 18% | 20 stp | (83.7×37% + 81.1×33% + 10×30%) = **62.9** | +0 | **63** |
| E | 72% | 65% | 22% | 10 stp | (73.5×37% + 72.2×33% + 0×30%) = **50.9** | +0 | **51** |

---

## 2. Phương án A — 3-Tier Ranking

### 2.1 Phân tier

| Tier | Tên | Score | Ước tính % driver | Đặc điểm |
|---|---|---|---|---|
| **R1** | 🥇 Elite | ≥ 78 | ~20% | Tài xế chất lượng cao, hoạt động ổn định |
| **R2** | 🥈 Active | 55–77 | ~35% | Tài xế trung bình khá, chạy đều |
| **R3** | 🥉 Standard | < 55 | ~40% | Tài xế vãng lai, chất lượng dao động |
| **—** | ⬜ Chưa xếp hạng | N/A | ~5% | Tài xế mới < 1 tháng |

### 2.2 Tier Eligibility — Ai được thấy layer nào?

> Đây là **hard access control**: tier thấp hơn ngưỡng KHÔNG BAO GIỜ nhìn thấy layer đó,  
> dù layer còn slot trống. Không phải "window delay" — mà là block hoàn toàn.

| Tier | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| 🥇 R1 Elite | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🥈 R2 Active | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🥉 R3 Standard | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| ⬜ Chưa xếp hạng | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### 2.3 Registration Window — Thứ tự mở đăng ký trong chu kỳ

> **Window không đóng lại đối với tier đã được mở.**  
> R1 đăng ký L1 ở Window 1 → R2 mở L2 ở Window 2 → R1 vẫn còn thấy & đăng ký được L1.

| Layer | Slot SGN | Window 1 (Ngày 1–3) | Window 2 (Ngày 4–5) | Window 3 (Ngày 6–7) |
|---|---|---|---|---|
| **L1** | 300 | 🥇 R1 mở | *(R1 vẫn tiếp tục)* | *(R1 vẫn tiếp tục)* |
| **L2** | 500 | 🥇 R1 mở | 🥈 R2 mở thêm | *(R1+R2 tiếp tục)* |
| **L3** | 1.000 | 🥇 R1 mở | 🥈 R2 mở thêm | 🥉 R3 mở thêm |
| **L4** | 1.000 | 🥇 R1 mở | 🥈 R2 mở thêm | 🥉 R3 mở thêm |
| **L5** | 1.000 | 🥇 R1 mở | 🥈 R2 mở thêm | 🥉 R3 mở thêm |
| **L6** | Không giới hạn | Tất cả mở ngay | — | — |

### 2.4 Ưu / Nhược điểm

| ✅ Ưu điểm | ❌ Nhược điểm |
|---|---|
| Đơn giản, dễ communicate với tài xế | Không phân biệt top 5% vs top 20% trong R1 |
| Ít phức tạp vận hành, threshold dễ calibrate | Mid-tier R2 rộng → ít động lực cải thiện dần |
| Phù hợp rollout T7/2026 | — |

---

## 3. Phương án B — 5-Tier Ranking

### 3.1 Phân tier

| Tier | Tên | Score | Ước tính % driver | Đặc điểm |
|---|---|---|---|---|
| **R1** | 💎 Diamond | ≥ 88 | ~8% | Xuất sắc, vượt benchmark tất cả KPI |
| **R2** | 🥇 Gold | 75–87 | ~17% | Giỏi, hoạt động đều, ít sự cố |
| **R3** | 🥈 Silver | 60–74 | ~25% | Ổn định, đủ tiêu chuẩn zone |
| **R4** | 🥉 Bronze | 45–59 | ~25% | Đang phát triển, cần cải thiện |
| **R5** | ⚪ Basic | < 45 | ~20% | Tài xế chất lượng thấp / thiếu hoạt động |
| **—** | ⬜ Chưa xếp hạng | N/A | ~5% | Tài xế mới < 1 tháng |

### 3.2 Tier Eligibility — Ai được thấy layer nào?

| Tier | L1 | L2 | L3 | L4 | L5 | L6 |
|---|---|---|---|---|---|---|
| 💎 R1 Diamond | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🥇 R2 Gold | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 🥈 R3 Silver | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| 🥉 R4 Bronze | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| ⚪ R5 Basic | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| ⬜ Chưa xếp hạng | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### 3.3 Registration Window — Thứ tự mở đăng ký

| Layer | Slot SGN | Window 1 (Ngày 1–2) | Window 2 (Ngày 3) | Window 3 (Ngày 4) | Window 4 (Ngày 5) | Window 5 (Ngày 6–7) |
| --- | --- | --- | --- | --- | --- | --- |
| **L1** | 300 | 💎 R1 mở | *(R1 tiếp tục)* | *(R1 tiếp tục)* | *(R1 tiếp tục)* | *(R1 tiếp tục)* |
| **L2** | 500 | 💎 R1 mở | 🥇 R2 mở thêm | *(R1+R2 tiếp tục)* | *(R1+R2 tiếp tục)* | *(R1+R2 tiếp tục)* |
| **L3** | 1.000 | 💎 R1 mở | 🥇 R2 mở thêm | 🥈 R3 mở thêm | *(tiếp tục)* | *(tiếp tục)* |
| **L4** | 1.000 | 💎 R1 mở | 🥇 R2 mở thêm | 🥈 R3 mở thêm | 🥉 R4 mở thêm | *(tiếp tục)* |
| **L5** | 1.000 | 💎 R1 mở | 🥇 R2 mở thêm | 🥈 R3 mở thêm | 🥉 R4 mở thêm | ⚪ R5 mở thêm |
| **L6** | Không giới hạn | Tất cả mở ngay | — | — | — | — |

### 3.4 Ưu / Nhược điểm

| ✅ Ưu điểm | ❌ Nhược điểm |
|---|---|
| Gamification rõ ràng — tài xế thấy lộ trình R5 → R1 | Phức tạp hơn khi communicate 5 nhóm + Chưa xếp hạng |
| Phân tách chính xác nhóm top 8% (Diamond) riêng | Cần calibrate threshold kỹ — tránh tier bị rỗng |
| Mỗi bước tăng ~13–15 điểm → khoảng cách khả đạt | — |
| Gắn chặt với Layer access: mỗi tier = 1 layer tương ứng | — |

---

## 4. Waterfall Logic — Cơ chế Spillover khi hết slot

### Nguyên tắc

```text
RULE 1 — Hard block:
  Tier thấp hơn threshold KHÔNG BAO GIỜ thấy layer đó.
  (R2 mở L2 window không ảnh hưởng gì đến L1 của R1)

RULE 2 — Windows không đóng:
  Khi window của tier kế tiếp mở ra,
  tier cũ VẪN GIỮ quyền truy cập layer của mình.

RULE 3 — Spillover xuống layer kế:
  R1 đăng ký L1 → L1 FULL → R1 còn lại:
    → Tự động thấy và có thể đăng ký L2
    → Được xếp TRƯỚC R2 trong hàng đợi L2
    (vì R1 > R2 về ranking)

RULE 4 — Slot hết vs. Window đóng (khác nhau):
  Slot hết = layer đó không nhận thêm đăng ký (bất kể tier nào)
  Window đóng = KHÔNG XẢY RA trong thiết kế này
```

### Ví dụ minh họa (3-Tier, SGN, Ngày 4 của chu kỳ đăng ký)

```text
Tình huống:
  R1 = 900 tài xế | L1 = 300 slot | L2 = 500 slot
  Ngày 1–3: R1 có thể đăng ký L1 + L2 + L3 + L4 + L5
  Ngày 4: R2 mở đăng ký (L2, L3, L4, L5)

Kết quả sau 3 ngày R1 hoạt động:
  L1: 300/300 slot → FULL (280 R1 đã đăng ký, 20 slot cuối fill bởi R1 khác)
  L2: 180/500 slot → còn 320 slot trống
  Còn lại 620 R1 chưa đăng ký ca nào

Ngày 4 — R2 mở đăng ký L2:
  Hàng đợi L2 = [620 R1 chưa đăng ký] → [R2 vào sau]
  → 320 slot trống: R1 lấy trước → sau đó R2 tiếp
  → R1 fill thêm 200 slot → còn 120 cho R2
  → R2 đăng ký 120 slot → L2 FULL

Kết quả: R1 luôn được ưu tiên trong mọi layer họ eligible.
```

---

## 5. So sánh & Khuyến nghị

| Tiêu chí | 3-Tier | 5-Tier |
|---|---|---|
| **Giai đoạn phù hợp** | ✅ Rollout T7/2026 | T10/2026 trở đi |
| **Độ phức tạp vận hành** | Thấp | Trung bình |
| **Động lực tài xế** | Trung bình | Cao (lộ trình rõ) |
| **Khớp với số layer** | 3 tier / 5 layer → hơi lệch | 5 tier / 5 layer → khớp đẹp |
| **Khuyến nghị** | Bắt đầu đây | Nâng cấp sau 3 tháng vận hành |

> **Lộ trình đề xuất:** Triển khai 3-Tier T7/2026 → Thu thập data phân phối thực tế → Calibrate threshold 5-Tier → Migrate T10/2026.

---

## 6. Layer Hard Requirements (ngoài Ranking)

> Ranking xác định **thứ tự ưu tiên**. Tài xế vẫn phải đáp ứng điều kiện đầu vào của layer.  
> Nếu không đủ hard requirement → không thể đăng ký dù có ranking cao.

| Layer | Hard Requirements (per 2.2 DM FINAL) |
|---|---|
| **L1 CORE** | Ký cam kết + COD ≥1M + Baga + ≥3 tháng thâm niên platform |
| **L2 Minizone** | EV + Túi giữ nhiệt + ≥1 tháng thâm niên (kể từ FAT) |
| **L3 Mediumzone** | EV + Túi giữ nhiệt + ≥1 tháng thâm niên |
| **L4 Bigzone** | Baga + ≥1 tháng thâm niên |
| **L5 Citizone** | Baga + ≥1 tháng thâm niên |
| **L6 MASS** | COD ≥500k + Không vi phạm ĐBCL cơ bản |
| **Chưa xếp hạng** | COD ≥500k (chỉ L6) |

---

*Trạng thái: Đã xác nhận 4/4 quyết định vận hành. Sẵn sàng chuyển sang HTML.*
