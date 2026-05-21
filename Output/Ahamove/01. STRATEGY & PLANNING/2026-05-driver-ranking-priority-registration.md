# Driver Ranking × Priority Registration System

Ahamove Driver Management | 2026-05 | Phiên bản: FINAL 3-Tier

> Hai quy tắc duy nhất:
> **Tier** xác định tài xế được nhìn thấy layer nào.
> **Điểm số** xác định ai được slot trước khi nhiều người cùng đăng ký.

---

## Các quyết định đã xác nhận

| # | Quyết định | Nội dung |
| --- | --- | --- |
| 1 | Số tier | **3-Tier** + tier "Chưa xếp hạng" |
| 2 | Chu kỳ tính Ranking | Hàng tháng — cuối tháng tính, đầu tháng sau áp dụng |
| 3 | Hiển thị điểm | Có — cập nhật mỗi ngày (rolling 30 ngày gần nhất) |
| 4 | Tài xế mới < 1 tháng | Tier "Chưa xếp hạng" — chỉ thấy L6 |
| 5 | Window đăng ký | Mở 7 ngày/chu kỳ, không phân ngày theo tier — tier cao không bao giờ bị đóng |
| 6 | Equipment | Gate tự động tại lúc đăng ký — system check, không xử lý tay |

---

## 1. Công thức Ranking Score

### 1.1 Base Score (0–100 điểm)

| Metric | Weight | Cách tính |
| --- | --- | --- |
| AR (Acceptance Rate) | **37%** | `min(AR / 98%, 1.0) × 100` |
| FR (Fulfillment Rate) | **33%** | `min(FR / 90%, 1.0) × 100` |
| DCR (Cancellation Rate) | **30%** | `max(0, (20% − DCR) / 20%) × 100` |

> DCR đảo chiều: DCR 0% → 100đ / DCR 10% → 50đ / DCR ≥ 20% → 0đ.

`Base Score = AR_score × 37% + FR_score × 33% + DCR_score × 30%`

### 1.2 Prod Bonus (Optional, +0–8 điểm)

> Tie-break khi 2 tài xế cùng Base Score.

| Prod (stp/tháng) | Bonus |
| --- | --- |
| ≥ 150 stp | +8 |
| ≥ 100 stp | +5 |
| ≥ 60 stp | +2 |
| < 60 stp | +0 |

`Final Score = Base Score + Prod Bonus` (capped tại 100)

### 1.3 Ví dụ tính điểm

| Tài xế | AR | FR | DCR | Prod | Final Score | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| A | 98% | 93% | 2% | 140 stp | 100 (capped) | R1 Elite |
| B | 95% | 87% | 8% | 90 stp | 86 | R1 Elite |
| C | 90% | 82% | 12% | 45 stp | 75 | R2 Active |
| D | 82% | 73% | 18% | 20 stp | 63 | R2 Active |
| E | 72% | 65% | 22% | 10 stp | 51 | R3 Standard |
| F | 55% | 50% | 28% | 5 stp | 32 | R3 Standard |

---

## 2. Định nghĩa 3-Tier

| Tier | Tên | Score | Ước tính % driver |
| --- | --- | --- | --- |
| **R1** | Elite | ≥ 78 | ~20% |
| **R2** | Active | 55–77 | ~35% |
| **R3** | Standard | < 55 | ~40% |
| **—** | Chưa xếp hạng | N/A | ~5% |

---

## 3. Tier → Layer Access (Quy tắc 1)

> Tier thấp hơn ngưỡng = **hard block** — không bao giờ thấy layer đó, dù còn slot trống.
> L6 MASS luôn mở cho tất cả.

| Tier | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- |
| R1 Elite | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| R2 Active | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
| R3 Standard | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Chưa xếp hạng | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

**Logic phân bổ:**

| Layer | Phục vụ ai | Supply đến từ |
| --- | --- | --- |
| L1 | KA/MP specialist | R1 độc quyền |
| L2 | Minizone ≤4km | R1 + R2 (R1 điểm cao hơn → fill trước tự nhiên) |
| L3 | Mediumzone 4–7km | R2 + R3 (buffer tốt, không lo thiếu cung) |
| L4 | Bigzone 7–11km | R2 + R3 (buffer tốt) |
| L5 | Cityzone >11km | R3 độc quyền |
| L6 | MASS | Tất cả |

---

## 4. Score → Thứ tự ưu tiên slot (Quy tắc 2)

> Khi nhiều tài xế cùng đăng ký 1 layer trong 7 ngày, slot được cấp theo **điểm số cao → thấp**.
> Không cần time window. Không cần cascade. Hệ thống tự sort.

```text
Ví dụ: L2 có 500 slot, R1+R2 cùng thấy L2

  Hàng đợi L2 được sort tự động:
  #1  R1 — Score 100  → slot #1
  #2  R1 — Score 96   → slot #2
  #3  R2 — Score 88   → slot #3   ← R2 điểm cao vẫn được trước R1 điểm thấp
  #4  R1 — Score 85   → slot #4
  #5  R2 — Score 82   → slot #5
  ...
  #500 → slot cuối cùng
  #501 trở đi → không có slot L2, tự động thấy L6
```

---

## 5. Equipment Gate (Tự động, không cần ops xử lý)

> Equipment check chạy tự động khi tài xế bấm đăng ký.
> Thiếu equipment → hệ thống từ chối, hiện thông báo lý do.

| Layer | Equipment bắt buộc |
| --- | --- |
| L1 | Baga + COD ≥1M + Ký cam kết |
| L2, L3 | EV + Túi giữ nhiệt + COD ≥2M |
| L4, L5 | Baga + COD ≥2M |
| L6 | COD ≥500k |

---

## 6. Layer Hard Requirements (KPI + Thâm niên)

> Ngoài equipment, tài xế phải đạt KPI tối thiểu của layer để đăng ký hợp lệ.
> Áp dụng đồng nhất cho mọi tier đăng ký layer đó.

| Layer | KPI tối thiểu (SGN) | Thâm niên |
| --- | --- | --- |
| L1 | AR ≥96%, FR ≥85%, DCR <10% | ≥3 tháng platform |
| L2, L3 | AR ≥95%, FR ≥85%, DCR <10%, Prod ≥100 stp | ≥1 tháng (FAT) |
| L4, L5 | AR ≥90%, FR ≥80%, DCR <12%, Prod ≥60 stp | ≥1 tháng (FAT) |
| L6 | DCR <20%, Rating ≥4.7 (warning only) | Không yêu cầu |

---

## 7. Upgrade Path

```text
Chưa xếp hạng ──(1 tháng, đủ KPI)──► R3 Standard  →  thấy L3, L4, L5
                                             │
                                     Cải thiện AR/FR/DCR
                                             ▼
                                        R2 Active   →  thấy L2, L3, L4
                                             │
                                     Duy trì KPI cao
                                             ▼
                                        R1 Elite    →  thấy L1, L2
```

> Điểm hiển thị mỗi ngày (rolling 30 ngày).
> Tier chính thức cập nhật 1 lần/tháng — quyết định quyền đăng ký ca tháng tiếp theo.

---

*Trạng thái: FINAL. Sẵn sàng build HTML.*
