# Driver Ranking × Priority Registration System
**Ahamove Driver Management | 2026-05**

> Ranking không chỉ là xếp hạng — mà là cơ chế phân bổ quyền đăng ký ca hoạt động,  
> đảm bảo đúng tài xế chất lượng cao vào đúng layer cần họ nhất.

---

## 1. Công thức Ranking Score

### 1.1 Base Score (0–100 điểm)

| Metric | Weight | Cách tính |
|---|---|---|
| AR (Acceptance Rate) | **37%** | `min(AR / 98%, 1.0) × 100` |
| FR (Fulfillment Rate) | **33%** | `min(FR / 90%, 1.0) × 100` |
| DCR (Cancellation Rate) | **30%** | `max(0, (20% − DCR) / 20%) × 100` |

> DCR được đảo chiều: tài xế DCR = 0% → 100 điểm. DCR = 20% → 0 điểm.  
> Benchmark AR = 98%, FR = 90% là ngưỡng tuyệt đối để đạt max score.

**Base Score = AR_score × 37% + FR_score × 33% + DCR_score × 30%**

---

### 1.2 Prod Bonus (Optional, +0–8 điểm)

> Prod không bắt buộc trong công thức — đây là **bonus** để phân biệt tài xế có cùng base score.  
> Dùng khi cần tie-break hoặc khi muốn khuyến khích tần suất hoạt động cao.

| Prod (stp/tháng) | Bonus |
|---|---|
| ≥ 150 stp | +8 |
| ≥ 100 stp | +5 |
| ≥ 60 stp | +2 |
| < 60 stp | 0 |

**Final Score = Base Score + Prod Bonus** *(capped tại 100)*

---

### 1.3 Ví dụ tính điểm

| Tài xế | AR | FR | DCR | Prod | Base Score | Prod Bonus | Final |
|---|---|---|---|---|---|---|---|
| Tài xế A | 98% | 92% | 3% | 130 stp | 97.7 + 33.0 + 25.5 = **95.3** × weights ≈ **95** | +5 | **100** (capped) |
| Tài xế B | 95% | 87% | 8% | 80 stp | 93.3 + 96.7 + 60.0 → **83.8** | +2 | **86** |
| Tài xế C | 90% | 82% | 12% | 45 stp | 91.8 + 91.1 + 40.0 → **75.2** | 0 | **75** |
| Tài xế D | 85% | 75% | 15% | 30 stp | 86.7 + 83.3 + 25.0 → **66.0** | 0 | **66** |

---

## 2. Phương án A — 3-Tier Ranking

### Phân tier

| Tier | Tên | Score | Ước lượng % driver | Đặc điểm |
|---|---|---|---|---|
| **R1** | 🥇 Elite | ≥ 78 | ~20% | Tài xế chất lượng cao, hoạt động ổn định |
| **R2** | 🥈 Active | 55–77 | ~35% | Tài xế trung bình khá, chạy đều |
| **R3** | 🥉 Standard | < 55 | ~45% | Tài xế vãng lai, chất lượng dao động |

### Priority Registration Matrix — 3 Tier

*(Slot numbers dựa theo SGN demand planning T7/2026)*

| Layer | Slot SGN | Window 1 (72h) | Window 2 (48h) | Window 3 (24h) | Sau đó |
|---|---|---|---|---|---|
| **L1 CORE** | 300 | R1 | — | — | Đóng (chỉ R1 eligible) |
| **L2 Minizone** | 500 | R1 overflow → R2 | R2 tiếp | R3 | Mở tự do |
| **L3 Mediumzone** | 1.000 | R1+R2 overflow → R2 | R3 | Mở tự do | — |
| **L4 Bigzone** | 1.000 | R2 overflow → R3 | Mở tự do | — | — |
| **L5 Citizone** | 1.000 | R3 | Mở tự do | — | — |
| **L6 MASS** | Không giới hạn | Tất cả | — | — | — |

### Ưu điểm / Nhược điểm

| | 3-Tier |
|---|---|
| ✅ | Đơn giản, dễ truyền thông với tài xế ("bạn đang ở nhóm Vàng/Bạc/Đồng") |
| ✅ | Ít phức tạp vận hành, threshold dễ calibrate |
| ✅ | Phù hợp giai đoạn rollout đầu |
| ❌ | Khó phân biệt top 5% với top 20% → cùng nhóm R1, cùng quyền lợi |
| ❌ | Ít động lực cải thiện ở mid-tier (R2 rộng) |

---

## 3. Phương án B — 5-Tier Ranking

### Phân tier

| Tier | Tên | Score | Ước lượng % driver | Đặc điểm |
|---|---|---|---|---|
| **R1** | 💎 Diamond | ≥ 88 | ~8% | Tài xế xuất sắc, hiệu suất vượt chuẩn |
| **R2** | 🥇 Gold | 75–87 | ~17% | Tài xế giỏi, hoạt động đều, ít sự cố |
| **R3** | 🥈 Silver | 60–74 | ~25% | Tài xế ổn định, đủ tiêu chuẩn zone |
| **R4** | 🥉 Bronze | 45–59 | ~25% | Tài xế đang phát triển, cần cải thiện |
| **R5** | ⚪ Basic | < 45 | ~25% | Tài xế mới hoặc chất lượng thấp |

### Priority Registration Matrix — 5 Tier

| Layer | Slot SGN | Window 1 (48h) | Window 2 (36h) | Window 3 (24h) | Window 4 (12h) | Sau đó |
|---|---|---|---|---|---|---|
| **L1 CORE** | 300 | R1 | R2 | — | — | Đóng (chỉ R1+R2 eligible) |
| **L2 Minizone** | 500 | R1 overflow → R2 | R2 overflow → R3 | R4 | — | Mở tự do |
| **L3 Mediumzone** | 1.000 | R2 overflow → R3 | R3 overflow → R4 | R5 | Mở tự do | — |
| **L4 Bigzone** | 1.000 | R3 overflow → R4 | R4 overflow → R5 | Mở tự do | — | — |
| **L5 Citizone** | 1.000 | R4 overflow → R5 | Mở tự do | — | — | — |
| **L6 MASS** | Không giới hạn | Tất cả | — | — | — | — |

### Ưu điểm / Nhược điểm

| | 5-Tier |
|---|---|
| ✅ | Gamification rõ ràng hơn — tài xế thấy được lộ trình từ R5 → R1 |
| ✅ | Phân biệt được nhóm top 8% (Diamond) với 17% tiếp theo → quyền lợi L1 chính xác hơn |
| ✅ | Mỗi tier cải thiện ~13-15 điểm là lên tier → khoảng cách khả đạt |
| ❌ | Phức tạp hơn khi communicate 5 nhóm cho tài xế |
| ❌ | Cần calibrate kỹ threshold — nếu phân phối lệch sẽ tier bị rỗng |

---

## 4. Waterfall Logic — Cơ chế Overflow

### Nguyên tắc hoạt động

```
Bước 1: Hệ thống tính Ranking Score tất cả driver → gán Tier (cuối tháng)
Bước 2: Mở đăng ký ca chu kỳ tiếp theo (2 tuần/lần — per kế hoạch vận hành)
Bước 3: Ưu tiên theo thứ tự sau:

  [Mỗi Layer mở window theo Tier]
        │
        ▼
  Window Tier cao nhất (ví dụ R1/Diamond)
        │
        ├── Còn slot? → Driver đăng ký được
        │
        └── Hết slot? → Driver R1 dư → ĐỨng ĐẦU HÀNG ĐỢI Layer kế tiếp
                                         (trước cả Tier thấp hơn)

Bước 4: Window kế tiếp mở → Tier kế tiếp vào, thêm vào SAU overflow tier trên
```

### Ví dụ cụ thể (3-Tier, SGN)

```
R1 = 800 tài xế | L1 = 300 slot | L2 = 500 slot

Window 1 (72h): 800 R1 mở đăng ký L1
  → 300 đăng ký thành công → L1 FULL
  → 500 R1 còn lại → ưu tiên đầu hàng đợi L2

Window 2 (48h): L2 mở đăng ký
  → 500 R1 overflow vào trước
  → L2 có 500 slot → R1 fill hết → L2 FULL (trường hợp này không còn slot cho R2 ở window này)
  → R2 overflow xuống L3, tiếp tục cascade...

Nếu L2 = 500 slot, R1 overflow = 300 (500 R1 chỉ có 300 muốn L2):
  → 300 R1 overflow lấy trước
  → 200 slot còn lại mở cho R2 trong window 2
```

---

## 5. So sánh nhanh: Chọn 3-Tier hay 5-Tier?

| Tiêu chí | 3-Tier | 5-Tier |
|---|---|---|
| **Giai đoạn phù hợp** | Rollout T7/2026 | Sau khi hệ thống ổn định (T10+) |
| **Độ phức tạp vận hành** | Thấp | Trung bình |
| **Động lực tài xế** | Trung bình | Cao |
| **Độ chính xác phân tier** | Đủ dùng | Tốt hơn |
| **Khuyến nghị** | ✅ Bắt đầu với 3-Tier | → Nâng lên 5-Tier sau 3 tháng |

---

## 6. Điều kiện bổ sung khi đăng ký Layer

> Ranking Score xác định **thứ tự ưu tiên** đăng ký.  
> Nhưng tài xế vẫn phải đáp ứng **điều kiện đầu vào** của layer đó (per 2.2 DM FINAL).

| Layer | Điều kiện hard (bắt buộc ngoài Ranking) |
|---|---|
| L1 CORE | Ký cam kết + COD ≥1M + Baga + 3 tháng thâm niên platform |
| L2 Minizone | Có EV + Túi giữ nhiệt + Thâm niên ≥1 tháng (kể từ FAT) |
| L3 Mediumzone | Có EV + Túi giữ nhiệt + Thâm niên ≥1 tháng |
| L4 Bigzone | Có Baga + Thâm niên ≥1 tháng |
| L5 Citizone | Có Baga + Thâm niên ≥1 tháng |
| L6 MASS | COD ≥500k + Không vi phạm ĐBCL cơ bản |

---

## 7. Câu hỏi mở — Cần quyết định trước khi triển khai

| # | Câu hỏi | Tác động |
|---|---|---|
| 1 | Chu kỳ tính lại Ranking: **hàng tháng** hay **rolling 4 tuần**? | Rolling 4 tuần phản ánh gần hơn, nhưng phức tạp hơn |
| 2 | Tài xế mới chưa đủ data (< 1 tháng) xếp tier nào? | Nếu gán R3/R5 mặc định → cần upgrade path rõ |
| 3 | Có cho tài xế **xem điểm Ranking** không? | Transparency tăng động lực nhưng cũng tăng dispute |
| 4 | Nếu layer thiếu driver sau khi đóng window ưu tiên → mở public hay push noti? | Ảnh hưởng fill rate của layer |

---

*Tiếp theo: Chuyển sang HTML interactive khi Khanh confirm phương án tier.*
