# Driver Ranking × Priority Registration System

Ahamove Driver Management | 2026-05 | Phiên bản: FINAL 3-Tier

> Hai quy tắc duy nhất:
> **Tier** xác định tài xế được nhìn thấy layer nào.
> **Timestamp** xác định ai được slot trước — first-come-first-served trong mọi layer.

---

## Các quyết định đã xác nhận

| # | Quyết định | Nội dung |
| --- | --- | --- |
| 1 | Số tier | **3-Tier** + tier "Chưa xếp hạng" |
| 2 | Xếp tier bằng cách nào | **Check đủ điều kiện KPI** (AR + FR + DCR + Prod) — pass/fail, không tính điểm |
| 3 | Chu kỳ tính Ranking | Cuối tháng check KPI → kết quả áp dụng từ đầu tháng sau |
| 4 | Thời gian mở đăng ký ca | **Ngày 1–5 hàng tháng** |
| 5 | Hiển thị KPI cho tài xế | Có — cập nhật mỗi ngày (rolling 30 ngày gần nhất) |
| 6 | Tài xế mới < 1 tháng | Tier "Chưa xếp hạng" — chỉ thấy L6 |
| 7 | Slot priority | **FCFS theo timestamp** + **Cascade reveal** — layer mở dần khi layer trước ≥ 80% slot |
| 8 | Equipment gate | Tự động tại lúc đăng ký — COD không check khi đăng ký ca |
| 9 | R1 fallback | R1 thấy thêm L3 khi L2 đạt ≥80% slot — layer dự phòng theo cascade |
| 10 | Auto L6 fallback | Hết ngày 5 chưa đăng ký ca → system tự động xếp vào L6 MASS |

---

## 1. Điều kiện xếp Tier

> Hệ thống check cuối tháng theo thứ tự **R1 → R2 → R3**. Đạt đủ **cả 4 điều kiện** của tier cao nhất → xếp vào tier đó.

### 1.1 SGN

| Tier | AR | FR | DCR | Prod | Thâm niên |
| --- | --- | --- | --- | --- | --- |
| **R1 Elite** | ≥ 95% | ≥ 85% | < 10% | ≥ 100 stp/tháng | ≥ 1 tháng (FAT) |
| **R2 Active** | ≥ 90% | ≥ 80% | < 12% | ≥ 60 stp/tháng | ≥ 1 tháng (FAT) |
| **R3 Standard** | Tài khoản active, DCR < 20%, Rating ≥ 4.7 | | | | ≥ 1 tháng (FAT) |
| **Chưa xếp hạng** | Chưa đủ 1 tháng thâm niên | | | | < 1 tháng |

### 1.2 HAN

| Tier | AR | FR | DCR | Prod | Thâm niên |
| --- | --- | --- | --- | --- | --- |
| **R1 Elite** | ≥ 93% | ≥ 83% | < 12% | ≥ 100 stp/tháng | ≥ 1 tháng (FAT) |
| **R2 Active** | ≥ 88% | ≥ 78% | < 14% | ≥ 60 stp/tháng | ≥ 1 tháng (FAT) |
| **R3 Standard** | Tài khoản active, DCR < 20%, Rating ≥ 4.7 | | | | ≥ 1 tháng (FAT) |
| **Chưa xếp hạng** | Chưa đủ 1 tháng thâm niên | | | | < 1 tháng |

> KPI xếp tier khớp với KPI vào layer tương ứng — tài xế đạt tier nào thì gần như đương nhiên đủ điều kiện vào layer của tier đó.

---

## 2. Tier → Layer Access

> **L1 KA/MP** được assigned trực tiếp — không qua hệ thống đăng ký ca này.
> Hệ thống đăng ký ca áp dụng cho **L2–L5** (+ L6 buffer). Tier thấp hơn = **hard block**.
> ↩ = cascade fallback: mở thêm khi layer ưu tiên đạt ≥80% slot.

| Tier | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 Elite | ★ assigned | ✅ | ↩ cascade | ❌ | ❌ | ✅ |
| R2 Active | ★ assigned | ❌ | ✅ | ↩ cascade | ❌ | ✅ |
| R3 Standard | ★ assigned | ❌ | ❌ | ✅ | ↩ cascade | ✅ |
| Chưa xếp hạng | ★ assigned | ❌ | ❌ | ❌ | ❌ | ✅ |

| Layer | Supply đến từ | Ghi chú |
| --- | --- | --- |
| L1 | ★ KA/MP assigned | Không qua đăng ký ca — assigned trực tiếp |
| L2 | R1 ưu tiên | Đăng ký ca, R1 primary layer |
| L3 | R2 ưu tiên · R1 cascade ↩ | R1 fallback khi L2 ≥80% slot |
| L4 | R3 ưu tiên · R2 cascade ↩ | Vùng đệm |
| L5 | R3 cascade ↩ | Long-haul >11km |
| L6 | Tất cả | Buffer co giãn toàn hệ thống |

---

## 3. Slot Priority — Cascade Reveal + FCFS

> **Cascade reveal**: Mỗi tier bắt đầu từ layer ưu tiên cao nhất. Layer tiếp theo chỉ mở khi layer trước đạt **≥ 80% fill-rate**.
> **Timestamp FCFS** áp dụng trong mọi layer đang hiển thị — không ưu tiên theo tier.
> **Auto L6**: Hết ngày 5 chưa đăng ký bất kỳ layer nào → system tự động xếp vào L6.

| Tier | Mở đầu | Khi ≥80% → thêm | Hết ngày 5 |
| --- | --- | --- | --- |
| R1 Elite | L2 | + L3 ↩ | Auto L6 |
| R2 Active | L3 | + L4 ↩ | Auto L6 |
| R3 Standard | L4 | + L5 ↩ | Auto L6 |
| Chưa xếp hạng | L6 | — | L6 |

```text
R1 Anh Hùng — cascade trong ngày 1–5/7:

  Phase 1: L2 mở đầu (R1 primary)
    01/07 08:22 — R1 Anh Hùng → L2 slot #12
    (R2 chạy L3 song song độc lập)

  [02/07] L2 đạt 80% (400/500 slot) → Hệ thống mở L3 ↩ cho R1
  Phase 2: R1 thấy L2 + L3 ↩
    02/07 10:06 — R1 Anh Hùng → L3 slot #88
    02/07 10:09 — R2 Chị Lan  → L3 slot #89
    (FCFS — R1/R2 bình đẳng trong L3)

  Hết 05/07: Tài xế chưa đăng ký → Auto L6
```

---

## 4. Equipment Gate (Tự động)

> System check khi tài xế bấm đăng ký ca. COD **không** check tại bước này.

| Layer | Equipment bắt buộc khi đăng ký ca |
| --- | --- |
| L1 | Baga + Ký cam kết |
| L2, L3 | EV |
| L4, L5 | Baga |
| L6 | Không yêu cầu |

---

## 5. Layer Hard Requirements (KPI + Thâm niên)

> Check tại thời điểm đăng ký. **L1 không áp dụng** (KA/MP assigned). Đồng bộ với rank: L2 = R1 KPI, L3 = R2 KPI, L4–L5 = R3 KPI.

### 5.1 SGN

| Layer | AR | FR | DCR | Prod | Rating | Thâm niên |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | — | — | — | — | — | ★ KA/MP assigned |
| L2 | ≥ 95% | ≥ 85% | < 10% | ≥ 100 stp | — | ≥ 1 tháng |
| L3 | ≥ 90% | ≥ 80% | < 12% | ≥ 60 stp | — | ≥ 1 tháng |
| L4, L5 | — | — | < 20% | — | ≥ 4.7 | ≥ 1 tháng |
| L6 | — | — | < 20% | — | — | — |

### 5.2 HAN

| Layer | AR | FR | DCR | Prod | Rating | Thâm niên |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | — | — | — | — | — | ★ KA/MP assigned |
| L2 | ≥ 93% | ≥ 83% | < 12% | ≥ 100 stp | — | ≥ 1 tháng |
| L3 | ≥ 88% | ≥ 78% | < 14% | ≥ 60 stp | — | ≥ 1 tháng |
| L4, L5 | — | — | < 20% | — | ≥ 4.7 | ≥ 1 tháng |
| L6 | — | — | < 20% | — | — | — |

---

## 6. Quyền lợi theo Layer & Rank

> Quyền lợi áp dụng khi tài xế **đang hoạt động trong layer** (đã đăng ký ca, duy trì tiêu chuẩn KPI). Các mục `📋 đề xuất` cần validate với team liên quan. Các mục `⏳ pending` đang trong quá trình finalize.

---

### 6.1 Thu nhập đảm bảo (đề xuất cân chỉnh)

> **Nguyên tắc cân chỉnh:** Layer có yêu cầu KPI đầu vào cao hơn → ngưỡng đảm bảo cao hơn để phản ánh đúng giá trị cam kết của tài xế. L2 yêu cầu KPI R1 (cao nhất) → xứng đáng được đảm bảo thu nhập cao nhất. Cần validate với S&P dựa trên data EPH thực tế.

| Layer | Khu vực | SGN (đề xuất) | HAN (đề xuất) | Ghi chú |
| --- | --- | --- | --- | --- |
| **L2 Minizone** | ≤ 4km | **70k/h** | **80k/h** | Ghép 4–5 đơn, KPI R1 → EPH cao nhất |
| **L3 Mediumzone** | 4–7km | **65k/h** | **75k/h** | Ghép 3–4 đơn, KPI R2 |
| **L4 Bigzone** | 7–11km | **60k/h** | **70k/h** | Ghép 2–3 đơn, KPI R3 |
| **L5 Cityzone** | >11km | **60k/h** | **70k/h** | Đơn 2H/4H, zone rộng — giữ nguyên baseline |
| **L6 MASS** | Toàn bộ | Không đảm bảo | Không đảm bảo | Tự do ca, co giãn theo demand |

---

### 6.2 Rewards Points — Hệ thống nhân điểm theo Layer

Tài xế tích lũy điểm trên mỗi đơn hoàn thành. Layer quyết định hệ số nhân. Điểm dùng để đổi ưu đãi từ Ahamove và đối tác.

| Layer | Hệ số nhân | Điểm / đơn (ví dụ base = 10đ) | Tích lũy 100 đơn |
| --- | --- | --- | --- |
| **L2 Minizone** | **×2.0** | 20 điểm | 2.000 điểm |
| **L3 Mediumzone** | **×1.7** | 17 điểm | 1.700 điểm |
| **L4 Bigzone** | **×1.3** | 13 điểm | 1.300 điểm |
| **L5 Cityzone** | **×1.0** | 10 điểm | 1.000 điểm |
| **L6 MASS** | ×1.0 | 10 điểm | 1.000 điểm |

**Điểm có thể dùng để đổi:**

- Voucher nhiên liệu (xăng / sạc điện)
- Voucher bảo dưỡng xe tại garage đối tác
- Thiết bị / CCDC hỗ trợ (túi giữ nhiệt, baga, áo đồng phục)
- Ưu đãi F&B từ merchant đối tác trên Ahamove
- Điểm thưởng tích lũy đổi thẻ quà tặng / tiền mặt (📋 đề xuất — cần check với Product & S&P)

---

### 6.3 Quyền lợi từ đối tác (Partner Benefits)

Ahamove đàm phán gói ưu đãi theo tier — tài xế được access dựa trên layer đang hoạt động.

| Loại quyền lợi | L2–L3 (Hạng Vàng) | L4–L5 (Hạng Bạc) | L6 (Cơ bản) |
| --- | --- | --- | --- |
| **Nhiên liệu** | Giảm 5–8% tại trạm đối tác | Giảm 3–5% | — |
| **Sạc điện EV** | Ưu tiên slot + giảm 10% | Giảm 5% | — |
| **Bảo dưỡng xe** | Voucher miễn phí 1 lần/quý | Voucher 1 lần/6 tháng | — |
| **Sức khỏe** | Khám định kỳ 1 lần/năm (phòng khám đối tác) | — | — |
| **Telecom** | Data 30GB/tháng (Viettel / Mobifone) | Data 15GB/tháng | — |
| **F&B / Tiêu dùng** | Discount tại merchant đối tác Ahamove | Discount cơ bản | Standard offers |
| **Bảo hiểm tai nạn** | ⏳ pending — đang đàm phán với PTI / PJICO | ⏳ pending | — |

> Gói "Hạng Vàng" (L2/L3) nhắm đến tài xế chất lượng cao nhất trong hệ thống — giữ chân bằng tổng gói quyền lợi, không chỉ thu nhập. Cần DM phối hợp Partnership để chốt danh sách đối tác cụ thể.

---

### 6.4 Quyền lợi theo Rank

Rank ảnh hưởng trực tiếp đến 4 quyền lợi độc lập ngoài layer access:

#### A. Ưu tiên đăng ký ca (Priority Registration Window)

| Rank | Thời điểm mở đăng ký | Layer được thấy |
| --- | --- | --- |
| **R1 Elite** | Ngày 1 · 00:00 (sớm nhất) | L2 + cascade L3 |
| **R2 Active** | Ngày 1 · 08:00 | L3 + cascade L4 |
| **R3 Standard** | Ngày 1 · 14:00 | L4 + cascade L5 |
| **Chưa xếp hạng** | Ngày 2+ | L6 only |

> R1 có lợi thế đăng ký sớm nhất trong ngày 1 → giảm nguy cơ hết slot ở layer ưu tiên. FCFS timestamp vẫn áp dụng trong cùng window. (📋 đề xuất — cần check với Product về technical feasibility)

#### B. Tier Bonus (Mức thưởng theo Rank)

| Rank | Hệ số bonus trên incentive scheme | Ghi chú |
| --- | --- | --- |
| **R1 Elite** | ×1.3 | Top performer — thưởng cao nhất |
| **R2 Active** | ×1.15 | Active tier — thưởng trung bình |
| **R3 Standard** | ×1.0 | Baseline |
| **Chưa xếp hạng** | ×1.0 | Baseline, không có tier bonus riêng |

> Rank bonus áp dụng nhân thêm trên incentive scheme hiện hành — không thay thế scheme. Chi tiết scheme phối hợp S&P. (📋 đề xuất)

#### C. Ưu tiên sự kiện / hoạt động Ahamove

| Rank | Quyền lợi sự kiện |
| --- | --- |
| **R1 Elite** | Invite VIP · Reserved seating · Vinh danh tại Gala / Community Day · Nhận quà recognition |
| **R2 Active** | Invite ưu tiên · Đảm bảo có slot tham dự |
| **R3 Standard** | Tham dự theo số lượng còn lại |
| **Chưa xếp hạng** | Không ưu tiên |

#### D. Hỗ trợ ưu tiên (Support SLA theo Layer)

| Layer (Rank tương ứng) | Kênh hỗ trợ | SLA phản hồi | Nội dung hỗ trợ |
| --- | --- | --- | --- |
| **L2 (R1)** | Kênh riêng (Hotline / Chat ưu tiên) | < 15 phút | Xử lý tài khoản, khiếu nại đơn, coaching KPI hàng tháng |
| **L3 (R2)** | Priority queue | < 30 phút | Xử lý tài khoản, khiếu nại đơn, check-in quý |
| **L4–L5 (R3)** | Priority queue | < 1 giờ | Xử lý tài khoản, khiếu nại đơn |
| **L6 (Chưa XH)** | Standard CS | Standard SLA | Standard |

> Đội trưởng (Team Leader) phụ trách L2/L3/L4 là đầu mối hỗ trợ trực tiếp tại khu vực — giảm tải CS trung tâm và tăng tốc xử lý vấn đề thực địa.

---

### 6.5 Tổng hợp so sánh ngang — Rank

| Quyền lợi | R1 Elite | R2 Active | R3 Standard | Chưa XH |
| --- | --- | --- | --- | --- |
| Layer ưu tiên | L2 (Minizone) | L3 (Medium) | L4 (Bigzone) | L6 only |
| Thu nhập đảm bảo | 70k/h SGN · 80k/h HAN | 65k/h SGN · 75k/h HAN | 60k/h SGN · 70k/h HAN | Không |
| Rewards multiplier | ×2.0 | ×1.7 | ×1.3 | ×1.0 |
| Partner benefits | Hạng Vàng | Hạng Vàng | Hạng Bạc | — |
| Tier bonus | ×1.3 | ×1.15 | ×1.0 | ×1.0 |
| Đăng ký ca sớm | Ngày 1 · 00:00 | Ngày 1 · 08:00 | Ngày 1 · 14:00 | Ngày 2+ |
| Sự kiện Ahamove | VIP + vinh danh | Ưu tiên | Theo slot | Không ưu tiên |
| Hỗ trợ SLA | < 15 phút | < 30 phút | < 1 giờ | Standard |
| BH sức khỏe | ⏳ pending | ⏳ pending | ⏳ pending | — |

---

### 6.6 Pending finalize

| Mục | Trạng thái | Team phụ trách |
| --- | --- | --- |
| Thu nhập đảm bảo L2/L3 (70k/65k SGN) | Validate với S&P — đối chiếu EPH P50 thực tế | DM + S&P |
| Bảo hiểm sức khỏe (L2–L5) | Check điều kiện (đề xuất: cam kết ≥ 1 năm) | DM + HR |
| Gói đối tác Hạng Vàng / Bạc | Đàm phán danh sách đối tác cụ thể | DM + Partnership |
| Bảo hiểm tai nạn (L2–L3) | Đàm phán với PTI / PJICO | DM + HR |
| Priority registration window (time-based) | Check technical feasibility với Product | DM + Product |
| Tier bonus multiplier (×1.3 / ×1.15) | Xây scheme chi tiết | DM + S&P |
| Rewards points system (base point, redemption catalog) | Thiết kế product feature | DM + Product |

---

## 7. Timeline Hàng Tháng

```text
Tuần cuối tháng (T-1)
  └─ Hệ thống tính KPI rolling 30 ngày
  └─ Check điều kiện → gán tier mới cho từng tài xế

Ngày 1–5 tháng T  ←  CỬA SỔ ĐĂNG KÝ CA
  └─ Mỗi tier thấy layer ưu tiên trước (cascade reveal)
  └─ Layer tiếp theo mở khi layer trước ≥ 80% slot
  └─ Timestamp FCFS trong mọi layer đang mở

Ngày 6+ tháng T
  └─ Đóng đăng ký (slot đã phân bổ xong)
  └─ Tài xế chưa đăng ký → đã được auto gán L6
  └─ Vận hành theo ca đã đăng ký
```

### Cascade đăng ký — Mở dần theo fill-rate

| Tier | Mở đầu | Khi ≥80% → thêm | Hết ngày 5 chưa ĐK |
| --- | --- | --- | --- |
| R1 Elite | L2 | + L3 ↩ | Auto L6 |
| R2 Active | L3 | + L4 ↩ | Auto L6 |
| R3 Standard | L4 | + L5 ↩ | Auto L6 |
| Chưa xếp hạng | L6 | — | L6 |

---

## 8. Upgrade Path

```text
Chưa xếp hạng ──(đủ 1 tháng, đạt KPI R3)──► R3 Standard  →  đăng ký L4, L5 ↩
                                                    │
                                          Đạt KPI R2 trong tháng
                                                    ▼
                                               R2 Active   →  đăng ký L3, L4 ↩
                                                    │
                                          Đạt KPI R1 trong tháng
                                                    ▼
                                               R1 Elite    →  đăng ký L2, L3 ↩

★ L1 KA/MP = assigned trực tiếp, không qua đăng ký ca
↩ = cascade fallback khi layer ưu tiên ≥80% slot
```

> KPI hiển thị mỗi ngày (rolling 30 ngày). Tier chính thức cập nhật 1 lần/tháng.

---

## 9. Ví dụ minh họa

### 9.1 Xếp tier cuối tháng — 5 profile (SGN)

| Tài xế | AR | FR | DCR | Prod | Kết quả | Lý do |
| --- | --- | --- | --- | --- | --- | --- |
| Anh Hùng | 97% | 88% | 6% | 120 stp | **R1 Elite** | Đạt đủ 4 điều kiện R1 |
| Chị Lan | 92% | 82% | 10% | 75 stp | **R2 Active** | AR 92% < 95% → trượt R1. Đạt đủ R2 |
| Anh Minh | 96% | 87% | 9% | 85 stp | **R2 Active** | Prod 85 < 100 → trượt R1. Đạt đủ R2 |
| Chị Hoa | 85% | 73% | 15% | 40 stp | **R3 Standard** | Không đạt R2 |
| Anh Tuấn | Mới join 2 tuần | — | — | — | **Chưa xếp hạng** | Chưa đủ 1 tháng |

### 9.2 R1 fallback khi L1+L2 hết slot

```text
Anh Hùng — R1 Elite, đăng ký ca ngày 4/7 (muộn):

  Mở app ngày 04/07:
    L1: 300/300 slot → HẾT
    L2: 500/500 slot → HẾT
    L3: 650/1000 slot → Còn 350 slot  ← R1 thấy được nhờ fallback
    L6: Mở (không giới hạn)

  Anh Hùng chọn L3 → System check equipment: L3 yêu cầu EV ✅
  → Đăng ký L3 thành công
  → Không phải xuống L6 MASS
```

### 9.3 Đăng ký ca L2 — timestamp priority

```text
L2 có 500 slot, R1 và R2 cùng đăng ký ngày 1–5/7:

  01/07 08:15 — R2 Chị Lan   → slot #1
  01/07 08:22 — R1 Anh Hùng  → slot #2
  01/07 09:40 — R2 Anh Bình  → slot #3
  ...
  03/07 14:30 → slot #500 → L2 HẾT

  R2 đăng ký sau → L2 hết → chuyển L3, L4
  R1 đăng ký sau → L2 hết → chuyển L1 hoặc L3
```

### 9.4 Hành trình thăng hạng — Tài xế Minh (SGN)

| Tháng | AR | FR | DCR | Prod | Tier | Layer thấy | Sự kiện |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T5 | — | — | — | — | Chưa XH | L6 | Mới join |
| T6 | 88% | 77% | 14% | 55 stp | R3 | L3–L5, L6 | Đăng ký L4 |
| T7 | 91% | 81% | 11% | 65 stp | R2 | L2–L4, L6 | Đăng ký L3 |
| T8 | 93% | 84% | 9% | **95 stp** | R2 | L2–L4, L6 | Giữ R2 — Prod chưa đủ 100 |
| T9 | 95% | 86% | 8% | 108 stp | R1 | L1–L3, L6 | Lên R1, đăng ký L2 |
| T10 | 97% | 89% | 6% | 125 stp | R1 | L1–L3, L6 | Duy trì R1, đăng ký L1 |

### 9.5 Equipment không phù hợp

```text
Chị Hà — R2 Active, chỉ có EV (không có Baga):

  Thấy được: L2 ✅  L3 ✅  L4 ✅  L6 ✅

  Đăng ký L4 → System check: L4 yêu cầu Baga
    → Từ chối: "Cần trang bị Baga để đăng ký Bigzone (L4)"

  Đăng ký L3 → System check: L3 yêu cầu EV ✅
    → Đăng ký thành công
```

---

*Trạng thái: FINAL.*
