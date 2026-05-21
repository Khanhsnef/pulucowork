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

*Trạng thái: FINAL. Sẵn sàng build HTML.*
