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
| 7 | Slot priority | **First-come-first-served theo timestamp** — không ưu tiên theo tier trong cùng layer |
| 8 | Equipment gate | Tự động tại lúc đăng ký — COD không check khi đăng ký ca |
| 9 | R1 fallback | R1 thấy được L3 — nếu L1+L2 hết slot hoặc không đăng ký kịp vẫn có layer để hoạt động |

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

> Tier thấp hơn ngưỡng = **hard block** — không bao giờ thấy layer đó, dù còn slot trống.
> L6 MASS luôn mở cho tất cả.
> **R1 thấy được L3** để có layer dự phòng nếu L1+L2 hết slot.

| Tier | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 Elite | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| R2 Active | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
| R3 Standard | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Chưa xếp hạng | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

| Layer | Supply đến từ | Ghi chú |
| --- | --- | --- |
| L1 | R1 độc quyền | KA/MP — chỉ tài xế chất lượng cao nhất |
| L2 | R1 + R2 | Timestamp quyết định |
| L3 | **R1 + R2 + R3** | Vùng chung — supply dồi dào, R1 có thể fallback về đây |
| L4 | R2 + R3 | Vùng đệm |
| L5 | R3 độc quyền | Long-haul >11km |
| L6 | Tất cả | Buffer co giãn toàn hệ thống |

---

## 3. Slot Priority

> **First-come-first-served theo timestamp** — không ưu tiên theo tier.
> Tier chỉ quyết định THẤY layer nào, không quyết định ưu tiên slot.

```text
L2 có 500 slot — R1 và R2 cùng đăng ký trong ngày 1–5:

  01/07 08:15 — R2 Chị Lan   → slot #1
  01/07 08:22 — R1 Anh Hùng  → slot #2
  01/07 09:05 — R1 Anh Minh  → slot #3
  01/07 09:40 — R2 Anh Bình  → slot #4
  ...
  03/07 14:30 — slot #500 (cuối) → L2 hết slot

  R1 đăng ký sau 03/07 14:30 → L2 hết → vẫn còn thấy L1 và L3
  R2 đăng ký sau 03/07 14:30 → L2 hết → vẫn còn thấy L3, L4
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

> Check tại thời điểm đăng ký. Áp dụng đồng nhất cho mọi tier.

### 5.1 SGN

| Layer | AR | FR | DCR | Prod | Thâm niên |
| --- | --- | --- | --- | --- | --- |
| L1 | ≥ 96% | ≥ 85% | < 10% | — | ≥ 3 tháng |
| L2, L3 | ≥ 95% | ≥ 85% | < 10% | ≥ 100 stp | ≥ 1 tháng |
| L4, L5 | ≥ 90% | ≥ 80% | < 12% | ≥ 60 stp | ≥ 1 tháng |
| L6 | — | — | < 20% | — | — |

### 5.2 HAN

| Layer | AR | FR | DCR | Prod | Thâm niên |
| --- | --- | --- | --- | --- | --- |
| L1 | ≥ 94% | ≥ 83% | < 12% | — | ≥ 3 tháng |
| L2, L3 | ≥ 93% | ≥ 83% | < 12% | ≥ 100 stp | ≥ 1 tháng |
| L4, L5 | ≥ 88% | ≥ 78% | < 14% | ≥ 60 stp | ≥ 1 tháng |
| L6 | — | — | < 20% | — | — |

---

## 6. Timeline Hàng Tháng

```text
Tuần cuối tháng (T-1)
  └─ Hệ thống tính KPI rolling 30 ngày
  └─ Check điều kiện → gán tier mới cho từng tài xế

Ngày 1–5 tháng T  ←  CỬA SỔ ĐĂNG KÝ CA
  └─ Tài xế thấy layer theo tier mới
  └─ Đăng ký theo timestamp — ai nhanh được slot trước

Ngày 6+ tháng T
  └─ Đóng đăng ký (slot đã phân bổ xong)
  └─ Vận hành theo ca đã đăng ký
```

---

## 7. Upgrade Path

```text
Chưa xếp hạng ──(đủ 1 tháng, đạt KPI R3)──► R3 Standard  →  thấy L3, L4, L5
                                                    │
                                          Đạt KPI R2 trong tháng
                                                    ▼
                                               R2 Active   →  thấy L2, L3, L4
                                                    │
                                          Đạt KPI R1 trong tháng
                                                    ▼
                                               R1 Elite    →  thấy L1, L2, L3
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
