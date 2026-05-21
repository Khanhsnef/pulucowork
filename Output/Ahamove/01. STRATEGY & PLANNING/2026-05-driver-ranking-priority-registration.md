# Driver Ranking × Priority Registration System

Ahamove Driver Management | 2026-05 | Phiên bản: FINAL 3-Tier

> Hai quy tắc duy nhất:
> **Tier** xác định tài xế được nhìn thấy layer nào.
> **Tier cao hơn** được cấp slot trước trong layer chung; cùng tier thì ai đăng ký trước được trước.

---

## Các quyết định đã xác nhận

| # | Quyết định | Nội dung |
| --- | --- | --- |
| 1 | Số tier | **3-Tier** + tier "Chưa xếp hạng" |
| 2 | Xếp tier bằng cách nào | **Check đủ điều kiện KPI** (AR + FR + DCR + Prod) — pass/fail, không tính điểm |
| 3 | Chu kỳ tính Ranking | Hàng tháng — cuối tháng check, đầu tháng sau áp dụng |
| 4 | Hiển thị KPI cho tài xế | Có — cập nhật mỗi ngày (rolling 30 ngày gần nhất) |
| 5 | Tài xế mới < 1 tháng | Tier "Chưa xếp hạng" — chỉ thấy L6 |
| 6 | Slot priority | Tier cao hơn được cấp trước; cùng tier → first-come-first-served |
| 7 | Equipment | Gate tự động tại lúc đăng ký — system check, không xử lý tay |

---

## 1. Điều kiện xếp Tier

> Hệ thống check cuối tháng: tài xế đạt **đủ cả 4 điều kiện** của tier cao nhất mình đạt được → xếp vào tier đó.
> Không đạt R2 → xét R3. Không đạt R3 → Standard mặc định (nếu tài khoản active).

### Điều kiện theo tier (SGN / HAN)

| Tier | AR | FR | DCR | Prod | Thâm niên |
| --- | --- | --- | --- | --- | --- |
| **R1 Elite** | ≥ 95% / ≥ 93% | ≥ 85% / ≥ 83% | < 10% / < 12% | ≥ 100 stp | ≥ 1 tháng (FAT) |
| **R2 Active** | ≥ 90% / ≥ 88% | ≥ 80% / ≥ 78% | < 12% / < 14% | ≥ 60 stp | ≥ 1 tháng (FAT) |
| **R3 Standard** | Tài khoản active, không vi phạm ĐBCL cơ bản (DCR < 20%, Rating ≥ 4.7) | | | | ≥ 1 tháng (FAT) |
| **Chưa xếp hạng** | Tài xế mới — chưa đủ 1 tháng thâm niên | | | | < 1 tháng |

> KPI dùng để xếp tier **khớp với KPI vào layer tương ứng** — tài xế đạt tier nào thì gần như đương nhiên đủ điều kiện vào layer của tier đó, tránh check 2 lần.

---

## 2. Tier → Layer Access

> Tier thấp hơn ngưỡng = **hard block** — không bao giờ thấy layer đó, dù còn slot trống.
> L6 MASS luôn mở cho tất cả.

| Tier | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 Elite | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| R2 Active | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
| R3 Standard | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Chưa xếp hạng | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

**Lý do phân bổ:**

| Layer | Supply đến từ | Ghi chú |
| --- | --- | --- |
| L1 | R1 độc quyền | Chỉ tài xế chất lượng cao nhất phục vụ KA/MP |
| L2 | R1 + R2 | R1 được cấp slot trước; R2 điền phần còn lại |
| L3 | R2 + R3 | Vùng đệm, hai tầng cùng cover → không lo thiếu cung |
| L4 | R2 + R3 | Vùng đệm, hai tầng cùng cover |
| L5 | R3 độc quyền | Long-haul >11km dành cho tài xế phổ thông ổn định |
| L6 | Tất cả | Buffer co giãn toàn hệ thống |

---

## 3. Slot Priority trong Layer chung

> Áp dụng cho L2 (R1+R2 cùng thấy) và L3, L4 (R2+R3 cùng thấy).

```text
Bước 1: Hệ thống thu thập đăng ký trong suốt 7 ngày chu kỳ

Bước 2: Phân bổ slot theo thứ tự:
  → Tier cao hơn được xử lý trước
  → Trong cùng tier: ai đăng ký sớm hơn được trước (timestamp)

Ví dụ — L2 có 500 slot, R1 và R2 cùng đăng ký:
  Xử lý R1 trước (bất kể thời điểm đăng ký)
    → R1 đã đăng ký: 120 drivers → lấy 120 slot
  Xử lý R2 tiếp theo theo thứ tự timestamp
    → 380 slot còn lại → R2 đăng ký theo thứ tự thời gian
    → Slot hết → R2 còn lại → chỉ còn L3, L4, L6
```

---

## 4. Equipment Gate (Tự động)

> System check khi tài xế bấm đăng ký. Thiếu equipment → từ chối + hiện lý do.

| Layer | Equipment bắt buộc |
| --- | --- |
| L1 | Baga + COD ≥ 1M + Ký cam kết |
| L2, L3 | EV + Túi giữ nhiệt + COD ≥ 2M |
| L4, L5 | Baga + COD ≥ 2M |
| L6 | COD ≥ 500k |

---

## 5. Layer Hard Requirements (KPI + Thâm niên)

> Check tại thời điểm đăng ký. Áp dụng đồng nhất cho mọi tier.

| Layer | KPI tối thiểu (SGN / HAN) | Thâm niên |
| --- | --- | --- |
| L1 | AR ≥ 96%, FR ≥ 85%, DCR < 10% | ≥ 3 tháng platform |
| L2, L3 | AR ≥ 95% / 93%, FR ≥ 85% / 83%, DCR < 10% / 12%, Prod ≥ 100 stp | ≥ 1 tháng (FAT) |
| L4, L5 | AR ≥ 90% / 88%, FR ≥ 80% / 78%, DCR < 12% / 14%, Prod ≥ 60 stp | ≥ 1 tháng (FAT) |
| L6 | DCR < 20%, Rating ≥ 4.7 (cảnh báo) | Không yêu cầu |

---

## 6. Upgrade Path

```text
Chưa xếp hạng ──(đủ 1 tháng, đạt KPI R3)──► R3 Standard  →  thấy L3, L4, L5
                                                    │
                                          Đạt KPI R2 trong tháng
                                                    ▼
                                               R2 Active   →  thấy L2, L3, L4
                                                    │
                                          Đạt KPI R1 trong tháng
                                                    ▼
                                               R1 Elite    →  thấy L1, L2
```

> KPI hiển thị mỗi ngày (rolling 30 ngày) để tài xế biết mình đang ở đâu so với ngưỡng tier.
> Tier chính thức cập nhật 1 lần/tháng — quyết định quyền đăng ký ca tháng tiếp theo.

---

## 7. Ví dụ minh họa

### 7.1 Xếp tier cuối tháng — 5 profile tài xế

> Hệ thống check 4 điều kiện theo thứ tự R1 → R2 → R3. Đạt đủ cả 4 mới vào tier đó.

| Tài xế | AR | FR | DCR | Prod | Kết quả xếp tier | Lý do |
| --- | --- | --- | --- | --- | --- | --- |
| Anh Hùng | 97% | 88% | 6% | 120 stp | **R1 Elite** | Đạt đủ 4 điều kiện R1 |
| Chị Lan | 92% | 82% | 10% | 75 stp | **R2 Active** | AR 92% < 95% → trượt R1. Đạt đủ R2 |
| Anh Minh | 96% | 87% | 9% | 85 stp | **R2 Active** | Prod 85 < 100 → trượt R1. Đạt đủ R2 |
| Chị Hoa | 85% | 73% | 15% | 40 stp | **R3 Standard** | Không đạt R2 (AR, FR, Prod đều thấp hơn ngưỡng) |
| Anh Tuấn | Mới join 2 tuần | — | — | — | **Chưa xếp hạng** | Chưa đủ 1 tháng thâm niên |

> **Lưu ý anh Minh:** Đạt AR/FR/DCR đủ cho R1 nhưng Prod chỉ 85 stp — thiếu đúng 1 điều kiện → xếp R2, không phải R1. Cả 4 điều kiện phải đạt đồng thời.

---

### 7.2 Đăng ký ca tháng 7 — Layer L2 (500 slot, SGN)

> L2 được nhìn thấy bởi R1 và R2. Slot được cấp cho R1 trước, sau đó R2 theo thứ tự đăng ký sớm.

```text
Đầu chu kỳ (Ngày 1):
  R1 Elite toàn thành phố đăng ký L2: 120 drivers
  R2 Active toàn thành phố đăng ký L2: 450 drivers

Phân bổ 500 slot L2:
  → Bước 1: 120 R1 nhận slot #1 → #120  (R1 ưu tiên trước)
  → Bước 2: 380 slot còn lại → R2 theo timestamp đăng ký sớm nhất
             R2 đăng ký sớm nhất → slot #121
             ...
             R2 thứ 380 → slot #500  ← slot cuối cùng
             70 R2 còn lại → L2 hết slot

Kết quả cho 70 R2 không có slot L2:
  → Vẫn thấy và đăng ký được L3, L4 (vẫn trong quyền hạn R2)
  → Không thấy L1 (hard block)
```

---

### 7.3 Đăng ký ca tháng 7 — Layer L3 (1.000 slot, SGN)

> L3 được nhìn thấy bởi R2 và R3. R2 ưu tiên trước.

```text
R2 đăng ký L3: 380 drivers (bao gồm 70 R2 vừa trượt L2 + 310 R2 khác chọn L3 ngay)
R3 đăng ký L3: 620 drivers

Phân bổ 1.000 slot L3:
  → Bước 1: 380 R2 nhận slot #1 → #380
  → Bước 2: 620 slot còn lại → R3 theo timestamp
             620 R3 đăng ký sớm → slot #381 → #1.000
             R3 còn lại → L3 hết slot → chuyển sang L4, L5, L6
```

---

### 7.4 Hành trình thăng hạng — Tài xế Minh (6 tháng)

| Tháng | AR | FR | DCR | Prod | Tier | Layer được thấy | Sự kiện |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T5 | — | — | — | — | Chưa xếp hạng | L6 | Mới join, chạy MASS |
| T6 | 88% | 77% | 14% | 55 stp | R3 Standard | L3, L4, L5, L6 | Đạt R3, đăng ký L4 |
| T7 | 91% | 81% | 11% | 65 stp | R2 Active | L2, L3, L4, L6 | Lên R2, đăng ký L3 |
| T8 | 93% | 84% | 9% | 95 stp | R2 Active | L2, L3, L4, L6 | Giữ R2, Prod chưa đủ 100 |
| T9 | 95% | 86% | 8% | 108 stp | R1 Elite | L1, L2, L6 | Lên R1, đăng ký L2 |
| T10 | 97% | 89% | 6% | 125 stp | R1 Elite | L1, L2, L6 | Duy trì R1, đăng ký L1 |

> T8 là ví dụ điển hình: AR/FR/DCR đã đủ R1 nhưng Prod 95 < 100 → giữ R2. Tháng sau cải thiện Prod lên 108 → đủ R1.

---

### 7.5 Tài xế có equipment không phù hợp

```text
Chị Hà — R2 Active, chỉ có EV (không có Baga):

  Thấy được: L2 ✅, L3 ✅, L4 ✅, L6 ✅  (theo tier R2)

  Thử đăng ký L4:
    → System check equipment: L4 yêu cầu Baga
    → Từ chối: "Bạn cần trang bị Baga để đăng ký Bigzone (L4)"

  Chị Hà đăng ký L3 thay thế:
    → System check: L3 yêu cầu EV + Túi giữ nhiệt
    → Chị Hà có EV ✅ + TGN ✅ → Đăng ký thành công
```

---

## 8. Upgrade Path

```text
Chưa xếp hạng ──(đủ 1 tháng, đạt KPI R3)──► R3 Standard  →  thấy L3, L4, L5
                                                    │
                                          Đạt KPI R2 trong tháng
                                                    ▼
                                               R2 Active   →  thấy L2, L3, L4
                                                    │
                                          Đạt KPI R1 trong tháng
                                                    ▼
                                               R1 Elite    →  thấy L1, L2
```

> KPI hiển thị mỗi ngày (rolling 30 ngày) để tài xế biết mình đang ở đâu so với ngưỡng tier.
> Tier chính thức cập nhật 1 lần/tháng — quyết định quyền đăng ký ca tháng tiếp theo.

---

*Trạng thái: FINAL. Sẵn sàng build HTML.*
