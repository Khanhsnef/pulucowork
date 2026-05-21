# Driver Ranking × Priority Registration System

Ahamove Driver Management | 2026-05 | Phiên bản: FINAL 3-Tier

> Ranking xác định **thứ tự ưu tiên** đăng ký ca.  
> Equipment xác định **layer nào driver đủ điều kiện** vật lý để hoạt động.  
> Hai điều kiện này kết hợp tạo ra ma trận phân bổ supply chính xác.

---

## Các quyết định đã xác nhận

| # | Quyết định | Nội dung |
| --- | --- | --- |
| 1 | Số tier | **3-Tier**: R1 Elite / R2 Active / R3 Standard + tier "Chưa xếp hạng" |
| 2 | Chu kỳ tính Ranking | **Hàng tháng** — tính cuối tháng, áp dụng tháng tiếp theo |
| 3 | Hiển thị điểm | **Có** — cập nhật mỗi ngày (rolling 30 ngày gần nhất) |
| 4 | Tài xế mới < 1 tháng | Tier **"Chưa xếp hạng"** — chỉ thấy L6, không thể đăng ký zone |
| 5 | Spillover trigger | **Time-based**: Ngày 3 mở spillover, Ngày 4 mở late-access |
| 6 | R3 không có Baga | **Late-access L3** từ Ngày 4 (sau khi R1+R2 đã có 3 ngày ưu tiên L3) |
| 7 | Window của tier cao | **Không đóng** — R1 vẫn thấy L1+L2 suốt chu kỳ đăng ký |

---

## 1. Công thức Ranking Score

### 1.1 Base Score (0–100 điểm)

| Metric | Weight | Cách tính |
| --- | --- | --- |
| AR (Acceptance Rate) | **37%** | `min(AR / 98%, 1.0) × 100` |
| FR (Fulfillment Rate) | **33%** | `min(FR / 90%, 1.0) × 100` |
| DCR (Cancellation Rate) | **30%** | `max(0, (20% − DCR) / 20%) × 100` |

> DCR đảo chiều: DCR 0% → 100đ / DCR 10% → 50đ / DCR ≥ 20% → 0đ.  
> Rating đã loại khỏi công thức.

`Base Score = AR_score × 37% + FR_score × 33% + DCR_score × 30%`

### 1.2 Prod Bonus (Optional, +0–8 điểm)

> Tie-break khi 2 tài xế cùng Base Score. Không bắt buộc trong công thức core.

| Prod (stp/tháng) | Bonus |
| --- | --- |
| ≥ 150 stp | +8 |
| ≥ 100 stp | +5 |
| ≥ 60 stp | +2 |
| < 60 stp | +0 |

**Final Score = Base Score + Prod Bonus** *(capped tại 100)*

### 1.3 Ví dụ tính điểm

| Tài xế | AR | FR | DCR | Prod | Final Score | Tier |
| --- | --- | --- | --- | --- | --- | --- |
| A | 98% | 93% | 2% | 140 stp | **100** (capped) | 🥇 R1 Elite |
| B | 95% | 87% | 8% | 90 stp | **86** | 🥇 R1 Elite |
| C | 90% | 82% | 12% | 45 stp | **75** | 🥈 R2 Active |
| D | 82% | 73% | 18% | 20 stp | **63** | 🥈 R2 Active |
| E | 72% | 65% | 22% | 10 stp | **51** | 🥉 R3 Standard |
| F | 55% | 50% | 28% | 5 stp | **32** | 🥉 R3 Standard |

---

## 2. Định nghĩa 3-Tier

| Tier | Tên | Score | Ước tính % driver | Đặc điểm |
| --- | --- | --- | --- | --- |
| **R1** | 🥇 Elite | ≥ 78 | ~20% | Chất lượng cao, hoạt động ổn định, KPI vượt benchmark |
| **R2** | 🥈 Active | 55–77 | ~35% | Trung bình khá, chạy đều, KPI đạt chuẩn zone |
| **R3** | 🥉 Standard | < 55 | ~40% | Vãng lai, chất lượng dao động, cần cải thiện |
| **—** | ⬜ Chưa xếp hạng | N/A | ~5% | Tài xế mới < 1 tháng, chưa đủ data |

---

## 3. Tier Eligibility — Ma trận Tier × Layer × Equipment

### 3.1 Logic tổng thể

```text
Điều kiện truy cập layer = RANKING tier + EQUIPMENT

  R1 hoặc R2 → xem layer có eligible không?
    └─ Eligible = tier đúng + có equipment phù hợp (EV, Baga...)
         └─ Nếu đủ → thấy và đăng ký được
         └─ Nếu thiếu equipment → không đăng ký được dù tier đủ

  R3 Standard có 2 sub-case:
    • R3 + Baga → Primary L4+L5
    • R3 + EV only (không Baga) → Không có primary zone
                                 → Late-access L3 từ Ngày 4
```

### 3.2 Ma trận đầy đủ

| Tier | Equipment | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 🥇 R1 Elite | Baga *(L1 yêu cầu)* | ✅ D1 | ✅ D1 | ✅ D3+ | ✅ D3+ | ✅ D4+ | ✅ |
| 🥈 R2 Active | EV/TGN hoặc Baga | ❌ | ✅ D1 | ✅ D1 | ✅ D3+ | ✅ D3+ | ✅ |
| 🥉 R3 Standard | Baga | ❌ | ❌ | ❌ | ✅ D1 | ✅ D1 | ✅ |
| 🥉 R3 Standard | EV only (không Baga) | ❌ | ❌ | ✅ D4+ | ❌ | ❌ | ✅ |
| ⬜ Chưa xếp hạng | Bất kỳ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

> **D1** = Thấy từ Ngày 1 (primary).  
> **D3+** = Mở thêm từ Ngày 3 (spillover).  
> **D4+** = Mở thêm từ Ngày 4 (late-access).  
> ❌ = Hard block — không bao giờ thấy, dù còn slot trống.

---

## 4. Registration Window Schedule

> Chu kỳ đăng ký: **7 ngày** mỗi 2 tuần (per kế hoạch vận hành).  
> Ngày 1 = ngày mở đăng ký của chu kỳ.

### 4.1 Timeline mở layer theo ngày

```text
Ngày 1–2  ──────────────────────────────────────────────────────
  R1: Thấy L1 + L2
  R2: Thấy L2 + L3
  R3 Baga: Thấy L4 + L5
  R3 EV: Thấy L6 (chờ D4)
  Tất cả: Thấy L6

Ngày 3  ─────────────────────────────────── SPILLOVER UNLOCK ──
  R1: Mở thêm L3 + L4  (L1, L2 vẫn còn mở cho R1)
  R2: Mở thêm L4 + L5  (L2, L3 vẫn còn mở cho R2)
  R3 Baga: L4+L5 vẫn mở, thêm vào hàng đợi R2 spillover

Ngày 4  ─────────────────────────────────── LATE ACCESS ───────
  R3 EV: Mở L3 (với điều kiện EV + TGN)
  R1: Mở thêm L5  (nếu muốn đăng ký L5)

Ngày 5–7  ──────────────────────────────── FILL REMAINING ─────
  Tất cả tiers giữ nguyên quyền truy cập đã unlock
  Slot nào còn trống → tier eligible vẫn có thể vào
```

### 4.2 Bảng tóm tắt — Layer thấy được theo từng Ngày

| Layer | Ngày 1–2 | + Ngày 3 | + Ngày 4 |
| --- | --- | --- | --- |
| **L1** | R1 | *(R1 tiếp tục)* | *(R1 tiếp tục)* |
| **L2** | R1, R2 | *(R1+R2 tiếp tục)* | *(R1+R2 tiếp tục)* |
| **L3** | R2 | + R1 spillover | + R3 EV late |
| **L4** | R3 Baga | + R1 spillover, R2 spillover | *(tiếp tục)* |
| **L5** | R3 Baga | + R2 spillover | + R1 late |
| **L6** | Tất cả | *(tiếp tục)* | *(tiếp tục)* |

---

## 5. Waterfall Spillover — Nguyên tắc ưu tiên khi nhiều tiers cùng thấy 1 layer

> Khi 2+ tiers cùng eligible cho 1 layer (ví dụ L3 từ Ngày 3 có cả R1 spillover + R2 primary),  
> **R1 luôn được xử lý trước R2, R2 trước R3** — theo thứ tự ranking điểm số cao → thấp.

```text
Ví dụ: L3 vào Ngày 3 — Hàng đợi đăng ký L3:
  Vị trí 1–N: R1 spillover (đăng ký theo điểm cao → thấp)
  Vị trí N+1: R2 primary (đăng ký theo điểm cao → thấp)

  Khi slot L3 hết → các driver còn lại trong hàng đợi không đăng ký được nữa
```

### Ví dụ đầy đủ (SGN, Ngày 5 của chu kỳ)

```text
Setup:
  R1 = 700 drivers | L1 = 300 slot | L2 = 500 slot
  R2 = 1.225 drivers | L3 = 1.000 slot
  R3 Baga = 1.000 drivers | L4 = 1.000 slot | L5 = 1.000 slot

Ngày 1–2 kết quả:
  L1: 300/300 → FULL (R1 đăng ký hết)
  L2: 400/500 → còn 100 slot (R1 đăng ký 400, chờ R2 điền nốt)
  L3: 800/1.000 → còn 200 slot (R2 đăng ký 800)
  L4: 700/1.000 → còn 300 slot (R3 Baga đăng ký 700)
  L5: 300/1.000 → còn 700 slot (R3 Baga đăng ký 300)

Ngày 3 — Spillover mở:
  R1 spillover → thấy L3+L4:
    → R1 còn 0 driver chưa đăng ký (đã fill hết L1+L2)
    → Không có R1 spillover thực tế trong ví dụ này ✓
  R2 spillover → thấy L4+L5:
    → R2 còn ~425 drivers chưa đăng ký
    → 425 R2 đổ vào L4(300 slot trống) + L5(700 slot trống)
    → L4 FULL | L5 còn 275 slot

Ngày 4 kết quả:
  L5: R3 Baga còn + R2 spillover còn → fill nốt 275 slot → FULL
  L3: R3 EV late-access → điền slot L3 nếu còn (trong ví dụ L3 còn 200 slot)
```

---

## 6. Layer Hard Requirements (Độc lập với Ranking)

> Ranking = thứ tự ưu tiên trong hàng đợi.  
> Hard requirement = điều kiện **bắt buộc** để slot đó valid. Thiếu 1 điều kiện → không đăng ký được.

| Layer | KPI tối thiểu (per 2.2 DM FINAL — SGN) | Equipment | Thâm niên |
| --- | --- | --- | --- |
| **L1 CORE** | AR ≥96%, FR ≥85%, DCR <10% | Baga + Ký cam kết + COD ≥1M | ≥3 tháng |
| **L2 Minizone** | AR ≥95%, FR ≥85%, DCR <10%, Prod ≥100 stp | EV + TGN | ≥1 tháng (FAT) |
| **L3 Mediumzone** | AR ≥95%, FR ≥85%, DCR <10%, Prod ≥100 stp | EV + TGN | ≥1 tháng (FAT) |
| **L4 Bigzone** | AR ≥90%, FR ≥80%, DCR <12%, Prod ≥60 stp | Baga | ≥1 tháng (FAT) |
| **L5 Citizone** | AR ≥90%, FR ≥80%, DCR <12%, Prod ≥60 stp | Baga | ≥1 tháng (FAT) |
| **L6 MASS** | DCR <20%, Rating ≥4.7 (warning only) | Không yêu cầu | Không yêu cầu |

---

## 7. Upgrade Path — Lộ trình phát triển cho tài xế

```text
Chưa xếp hạng ──(1 tháng + đủ KPI)──► R3 Standard
                                             │
                                   Cải thiện AR/FR/DCR
                                             │
                                             ▼
                                       R2 Active (Score 55–77)
                                             │
                                   Duy trì KPI cao liên tục
                                             │
                                             ▼
                                       R1 Elite (Score ≥78)
                                             │
                                   Đăng ký được L1 (KA/MP)
```

> **Ranking cập nhật hàng ngày (rolling 30 ngày)** → tài xế thấy được điểm tiến triển theo thời gian thực.  
> **Tier chính thức** (quyết định quyền đăng ký ca) cập nhật **1 lần/tháng** vào đầu tháng.

---

*Trạng thái: FINAL. Sẵn sàng build HTML.*
