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

## 6. Timeline Hàng Tháng

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

## 7. Upgrade Path

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

## 8. Ví dụ minh họa

### 8.1 Xếp tier cuối tháng — 5 profile (SGN)

| Tài xế | AR | FR | DCR | Prod | Kết quả | Lý do |
| --- | --- | --- | --- | --- | --- | --- |
| Anh Hùng | 97% | 88% | 6% | 120 stp | **R1 Elite** | Đạt đủ 4 điều kiện R1 |
| Chị Lan | 92% | 82% | 10% | 75 stp | **R2 Active** | AR 92% < 95% → trượt R1. Đạt đủ R2 |
| Anh Minh | 96% | 87% | 9% | 85 stp | **R2 Active** | Prod 85 < 100 → trượt R1. Đạt đủ R2 |
| Chị Hoa | 85% | 73% | 15% | 40 stp | **R3 Standard** | Không đạt R2 |
| Anh Tuấn | Mới join 2 tuần | — | — | — | **Chưa xếp hạng** | Chưa đủ 1 tháng |

### 8.2 R1 fallback khi L1+L2 hết slot

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

### 8.3 Đăng ký ca L2 — timestamp priority

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

### 8.4 Hành trình thăng hạng — Tài xế Minh (SGN)

| Tháng | AR | FR | DCR | Prod | Tier | Layer thấy | Sự kiện |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T5 | — | — | — | — | Chưa XH | L6 | Mới join |
| T6 | 88% | 77% | 14% | 55 stp | R3 | L3–L5, L6 | Đăng ký L4 |
| T7 | 91% | 81% | 11% | 65 stp | R2 | L2–L4, L6 | Đăng ký L3 |
| T8 | 93% | 84% | 9% | **95 stp** | R2 | L2–L4, L6 | Giữ R2 — Prod chưa đủ 100 |
| T9 | 95% | 86% | 8% | 108 stp | R1 | L1–L3, L6 | Lên R1, đăng ký L2 |
| T10 | 97% | 89% | 6% | 125 stp | R1 | L1–L3, L6 | Duy trì R1, đăng ký L1 |

### 8.5 Equipment không phù hợp

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
