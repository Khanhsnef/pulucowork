# DRIVER JOURNEY & MILESTONE FRAMEWORK v4.0

## Đề Xuất Hành Trình Tài Xế — Gắn Chặt Với Ranking Params v2.0

> **Ngày:** 02/06/2026 · **Owner:** Driver Management
> **Đối chiếu với:** `2026-05-driver-ranking-params.html` (KPI thresholds, layer, ca, AhaPoints, catalog)
> **Nghiên cứu nền:** `06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md` (15+ nền tảng toàn cầu)

---

## 1. ĐỐI CHIẾU: RANKING PARAMS VS LIFECYCLE — TENSIONS & GAPS

### 1.1 Tóm Tắt Ranking Params Hiện Tại

| Rank | DQS | DCR | Prod (stp/tháng) | Layer | EPH target SGN | EPH target HAN | Full-day Guarantee | AhaPoints × | Voucher xăng | BH |
|:-----|:----|:----|:-----------------|:------|:---------------|:---------------|:-------------------|:------------|:-------------|:---|
| **R1 Kim Cương** | ≥ 80 | ≤ 10% | ≥ 280 | L2 Minizone | 65k/h | 70k/h | 600k · 650k/ngày | ×1.5 +30 | 50k/tháng | Mini (trả bằng pts) |
| **R2 Vàng** | ≥ 75 | ≤ 10% | ≥ 210 | L3 Mediumzone | 60k/h | 65k/h | 550k · 600k/ngày | ×1.3 +25 | 30k/tháng | ❌ |
| **R3 Bạc** | ≥ 75 | ≤ 15% | ≥ 70 | L4 Bigzone | 55k/h | 60k/h | ❌ | ×1.1 +20 | ❌ | ❌ |
| **Unranked** | < 75 | — | — | L6 MASS | — | — | ❌ | ×1.0 | ❌ | ❌ |

**Fleet Target:** R1 15% · R2 35% · R3 35% · Unranked 15% (~10.5k weekly actives SGN+HAN)

### 1.2 Quy Đổi Productivity Sang Hành Vi Hàng Ngày

| Rank | stp/tháng | ÷ 22 ngày làm | ÷ 26 ngày làm | Ý nghĩa |
|:-----|:----------|:-------------|:-------------|:--------|
| **R3** | ≥ 70 | **~3.2 stp/ngày** | ~2.7 stp/ngày | Part-time khả thi — chạy 4-5 đơn/ngày × 4-5 ngày/tuần |
| **R2** | ≥ 210 | **~9.5 stp/ngày** | ~8.1 stp/ngày | Full-time commitment — cần chạy ~10 đơn/ngày × 5-6 ngày/tuần |
| **R1** | ≥ 280 | **~12.7 stp/ngày** | ~10.8 stp/ngày | Chuyên nghiệp — chạy ca full-day ~13 đơn/ngày × 5-6 ngày |

> **Nhận xét:** Khoảng cách R3 → R2 rất lớn (70 → 210 = gấp 3x). Đây là "death zone" — nơi nhiều tài xế sẽ mắc kẹt ở R3 và không thấy đường lên R2. Framework lifecycle cần thiết kế cụ thể cách "leo qua vực" này.

### 1.3 5 Tensions Chính Khi Đối Chiếu

| # | Tension | Chi tiết | Mức nghiêm trọng |
|:--|:--------|:---------|:-----------------|
| **T1** | **"New Unranked" = "Bad Unranked"** | Hệ thống hiện tại không phân biệt tài xế mới đăng ký (chưa có data) với tài xế rớt hạng (performance kém). Cả hai đều ở L6 MASS, không có benefits. Tài xế mới bị "phạt" trước khi có cơ hội chứng minh. | 🔴 Critical |
| **T2** | **Vực R3 → R2 (70 → 210 stp)** | Gấp 3x productivity. Tài xế R3 part-time (~3 stp/ngày) phải nhảy sang full-time (~10 stp/ngày) để lên R2. Không có bậc trung gian. | 🔴 Critical |
| **T3** | **BH chỉ cho R1, trả bằng points** | Nghiên cứu (Swiggy, Deliveroo, XanhSM) cho thấy BH là moat retention mạnh nhất. Hiện tại chỉ R1 được BH mini, phải dùng points. Bỏ lỡ cơ hội tạo switching cost cho R3/R2. | 🟠 High |
| **T4** | **Không có Guarantee cho tài xế mới** | Full-day guarantee chỉ R1+R2. Tài xế mới (Unranked) không có safety net nào. Benchmark: Grab guarantee 14 ngày → D30 retention +32%. | 🟠 High |
| **T5** | **Points expire cuối quý** | Tài xế mới đăng ký gần cuối quý sẽ mất points trước khi tích đủ. Tạo unfairness cảm nhận. | 🟡 Medium |

---

## 2. ĐỀ XUẤT: 5 PHASE DRIVER JOURNEY (THIẾT KẾ LẠI)

### 2.1 Tại Sao 5 Phase Thay Vì 6?

Sau đối chiếu ranking params, tôi đề xuất **gộp Phase 1 + Phase 2 cũ thành 1 phase duy nhất** vì:

1. **Ranking params không có trạng thái trung gian** giữa "vừa đăng ký" và "chưa xếp hạng" — cả hai đều Unranked/L6.
2. **Mốc D3 quá ngắn** để đo lường có ý nghĩa. Grab dùng 14 ngày, Uber dùng 30 ngày, DoorDash dùng 50 đơn. Không có nền tảng nào dùng D3 làm ranh giới phase.
3. **Mục tiêu hành vi D0-D14 là một khối liên tục**: Kích hoạt → Tạo thói quen ban đầu → Chứng minh thu nhập. Chia nhỏ tạo complexity nhưng không tạo action khác biệt.
4. **Gộp lại cho phép "Protected Window" 14 ngày** mạch lạc hơn — tương đương Grab Guarantee 14 ngày.

### 2.2 Framework 5 Phase — Tổng Quan

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                           DRIVER JOURNEY — 5 PHASE                                       │
│                                                                                          │
│  PHASE 1         PHASE 2           PHASE 3           PHASE 4           PHASE 5           │
│  ACTIVATION      HABIT             RANKING           MASTERY           LEGACY             │
│  & FIRST WIN     BUILDING          CLIMB             & OPTIMIZATION    & INFLUENCE        │
│                                                                                          │
│  D0 — D14        D15 — D60         D61 — D150        D151 — D365       D365+              │
│                                                                                          │
│  🟡 Unranked     🔵 Unranked →     🥈 R3 → 🥇 R2    🥇 R2 → 💎 R1    💎 R1 duy trì     │
│  (Protected)     R3 Bạc target                                                           │
│                                                                                          │
│  "Tôi thử xem"  "Tôi quen rồi"   "Tôi leo hạng"   "Tôi tối ưu"     "Tôi dẫn dắt"     │
│                                                                                          │
│  Churn risk:     Churn risk:       Churn risk:       Churn risk:       Churn risk:        │
│  ██████████      ████████          ██████            ███               █                  │
│  RẤT CAO         CAO               TRUNG BÌNH        THẤP             RẤT THẤP           │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Chi Tiết Từng Phase — Gắn Với Ranking Params

---

#### PHASE 1: ACTIVATION & FIRST WIN (D0 → D14)

**Tên gọi:** "Thử Thách Đầu Tiên"
**Trạng thái Ranking:** Unranked — nhưng có **"New Driver" flag** phân biệt với Unranked thông thường
**Layer:** L6 MASS + **Newbie Priority Dispatch** (đơn gần, đơn dễ)

**Mục đích hành vi:** Hoàn thành ≥ 21 đơn trong 14 ngày (benchmark: 21 đơn → D90 retention +58%)

**Tại sao D14 là ranh giới?**
- Grab Guarantee 14 ngày → D30 retention +32%
- Uber: 47% tài xế quit trước 25 đơn
- Behavioral: "21 repetitions" = bắt đầu hình thành habit loop (Lally, 2010)
- DoorDash: "First 50 deliveries" = protected window (Ahamove scale nhỏ hơn → 21 đơn phù hợp)

| Mốc | Ngày | Điều kiện | Cơ chế | Benchmark |
|:----|:-----|:----------|:-------|:----------|
| **M1: First Trip** | D0-D1 | Hoàn thành đơn đầu tiên | First Trip Bonus (declining: 24h > 48h > 72h) + Instant Payout miễn phí | Grab First Trip Bonus +27% activation |
| **M2: Quick 5** | ~D2-D3 | 5 đơn hoàn thành | Cash bonus nhỏ + Progress bar "5/21" hiển thị | DoorDash Progress bar +23% completion |
| **M3: Habit Seed** | ~D7 | 10 đơn hoàn thành | Badge "Tuần Đầu Tiên" + Unlock xem EPH real-time | Uber: transparency → trust |
| **M4: Activation Complete** | D14 | ≥ 21 đơn | **Gateway vào Phase 2** — Unlock đăng ký ca 4h (L4 Bigzone) + Streak system bắt đầu | Benchmark 21-trip threshold |

**Cơ chế đặc biệt Phase 1:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  🛡️ PROTECTED WINDOW — 14 NGÀY ĐẦU TIÊN                                  │
│                                                                            │
│  1. NEW DRIVER GUARANTEE (thay vì ném vào L6 không có gì):               │
│     → Hoàn thành ≥ 3 đơn/ngày → đảm bảo tối thiểu XXXk/ngày            │
│     → Ahamove bù chênh lệch nếu earning thực < mức đảm bảo             │
│     → Phasing: D1-D7 mức cao, D8-D14 mức thấp hơn 20%                  │
│     → Cost ceiling: chỉ bù khi earning thực thấp hơn. Nếu vượt = $0    │
│     → Benchmark: Grab 14d guarantee → +32% D30 retention                │
│                                                                            │
│  2. NEWBIE PRIORITY DISPATCH:                                             │
│     → Ưu tiên đơn ngắn (<3km), đơn đơn giản (không yêu cầu đặc biệt)  │
│     → Lý do: Giảm friction, tạo trải nghiệm thành công                  │
│                                                                            │
│  3. INSTANT PAYOUT MIỄN PHÍ:                                             │
│     → Nhận tiền sau mỗi đơn hoàn thành (hoặc cuối ngày)                │
│     → Benchmark: 44% tài xế rời đi nếu payout chậm                     │
│                                                                            │
│  4. BUDDY SYSTEM:                                                          │
│     → Gán 1 tài xế R2+/R1 cùng khu vực làm mentor                      │
│     → Buddy được thưởng khi mentee đạt 21 đơn                           │
│     → Kênh Zalo group 5-10 người cùng batch đăng ký                     │
└────────────────────────────────────────────────────────────────────────────┘
```

**KPIs Phase 1:**

| Chỉ số | Target | Alert | Ghi chú |
|:-------|:-------|:------|:--------|
| Activation Rate (≥1 đơn trong 72h) | ≥ 85% | < 60% 🔴 | |
| Time-to-First-Trip | ≤ 24h | > 48h 🔴 | |
| D14 Retention | ≥ 80% | < 65% 🔴 | |
| 21-Trip Achievement Rate | ≥ 65% | < 45% 🔴 | % tài xế đạt 21 đơn trong D14 |
| Guarantee Utilization | ≥ 55% tự vượt | < 40% 🟠 | % tài xế tự earn trên guarantee |

---

#### PHASE 2: HABIT BUILDING (D15 → D60)

**Tên gọi:** "Xây Nền"
**Trạng thái Ranking:** Unranked → **Target R3 Bạc cuối Phase 2**
**Layer:** Chuyển từ L6 sang L4 Bigzone khi đủ điều kiện R3

**Mục đích hành vi:** Hình thành thói quen hoạt động ổn định ≥ 4 ngày/tuần, tích lũy đủ KPI để đạt R3 Bạc

**Tại sao D60 là ranh giới?**
- Lally (2010): Trung bình 66 ngày để hình thành thói quen (range 18-254). D60 ≈ 2 tháng = 2 chu kỳ đánh giá.
- R3 yêu cầu 70 stp/tháng. Tài xế cần **ít nhất 1 tháng đầy đủ** sau Phase 1 để chạm ngưỡng.
- Zwettler (2024): "Newbie Challenge" kéo dài ~D0-D30. "Positioning Challenge" bắt đầu ~D30-D60.
- Thực tế: Tài xế cần ~45-60 ngày để **ổn định pattern** (khu vực, giờ, loại đơn).

**Tính toán con đường lên R3:**

```
R3 yêu cầu: DQS ≥ 75 + DCR ≤ 15% + Prod ≥ 70 stp/tháng

Với tài xế Phase 2 (D15-D60):
  → D15-D30: Đang tìm nhịp, ~3-5 stp/ngày × 15-18 ngày = 45-90 stp
  → D31-D60: Ổn định hơn, ~4-6 stp/ngày × 18-22 ngày = 72-132 stp
  → Tháng thứ 2 (D31-D60): Có khả năng đạt 70 stp → ĐỦ R3

Timeline thực tế: Tài xế sớm nhất có thể đạt R3 vào cuối tháng thứ 2 (~D45-D60)
```

| Mốc | Ngày | Điều kiện | Cơ chế | Gắn với Ranking Params |
|:----|:-----|:----------|:-------|:----------------------|
| **M5: Week 3 Quest** | D15-D21 | Hoàn thành 15 đơn/tuần | Weekly Quest thay Guarantee (bridge mượt) | Preparation cho 70 stp/tháng (R3) |
| **M6: First Month** | D30 | ≥ 60 đơn tổng (tích lũy) | Báo cáo thu nhập tháng đầu tiên + So sánh vs earning target | Calibration: 60 đơn ≈ 2.7 stp/ngày × 22d — gần ngưỡng R3 |
| **M7: Service Unlock** | ~D30 | 30 đơn + DQS ≥ 70 | Unlock Siêu Tốc + Ghép Đơn | Uber: multi-service +19pp retention, zero cost |
| **M8: R3 Qualification** | D45-D60 | DQS ≥ 75, DCR ≤ 15%, Prod ≥ 70 | **RANK UP → R3 Bạc!** Layer L4 Bigzone, AhaPoints ×1.1, Catalog Bạc, Ca 4h structured | Ranking params S1: R3 threshold |
| **M9: Habit Confirmation** | D60 | ≥ 4 ngày/tuần active trong 4 tuần liên tiếp | Badge "Thói Quen Vàng" + Bắt đầu nhận AhaPoints bonus +20/ca | Ranking params S7: L4 bonus |

**Cơ chế đặc biệt Phase 2:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  📈 WEEKLY QUEST SYSTEM (Thay thế Guarantee từ D15)                       │
│                                                                            │
│  Quest Cơ Bản:   15 đơn/tuần → Thưởng nhỏ                                │
│  Quest Nâng Cao: 25 đơn/tuần → Thưởng + Badge                            │
│  Quest Siêu Cấp: 35 đơn/tuần → Thưởng lớn + Unlock tính năng            │
│                                                                            │
│  Progress bar real-time + Countdown deadline                              │
│  So sánh với tài xế cùng khu vực, cùng batch (Social proof)              │
│                                                                            │
│  Mục đích: Bridge từ external motivation (guarantee)                      │
│  → identified motivation (quest = tôi chọn mục tiêu)                     │
│  Benchmark: Uber Quest + DoorDash Challenges (+23% completion)            │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  🔓 PROGRESSIVE SERVICE UNLOCK (Zero-cost retention lever)                │
│                                                                            │
│  Hiện tại (Params): Tất cả dịch vụ mở ngay → không có progression        │
│  Đề xuất: Unlock dần theo milestone                                       │
│                                                                            │
│  21 đơn (D14):  Unlock app full features (EPH tracker, heat map cơ bản)  │
│  30 đơn (~D20): Unlock Siêu Tốc (đơn premium, phí cao hơn)              │
│  50 đơn (~D30): Unlock Ghép Đơn (batch delivery → tăng EPH)              │
│  70 đơn (~D45): Unlock 4H Delivery (scheduled, thu nhập ổn định)         │
│  100 đơn (R3):  Unlock Enterprise/SME API (Shopee, TikTok Shop)          │
│                                                                            │
│  Gắn với Ranking: 100 đơn ≈ R3 territory → Enterprise = R3+ privilege    │
└────────────────────────────────────────────────────────────────────────────┘
```

**KPIs Phase 2:**

| Chỉ số | Target | Alert | Gắn Ranking Params |
|:-------|:-------|:------|:-------------------|
| D30 Retention | ≥ 72% | < 55% 🔴 | |
| D60 Retention | ≥ 62% | < 45% 🔴 | |
| R3 Qualification Rate (cuối D60) | ≥ 55% | < 35% 🔴 | % tài xế đạt R3 Bạc trước D60 |
| Weekly Active Days | ≥ 4 ngày | < 3 ngày 🟠 | R3 cần ~3.2 stp/ngày × 22d |
| Quest Completion Rate | ≥ 55% | < 35% 🟠 | |
| Multi-service Unlock Rate | ≥ 50% (≥2 dịch vụ) | < 30% 🟠 | |

---

#### PHASE 3: RANKING CLIMB (D61 → D150)

**Tên gọi:** "Leo Hạng"
**Trạng thái Ranking:** R3 Bạc → **Target R2 Vàng cuối Phase 3**
**Layer:** L4 Bigzone → L3 Mediumzone

**Mục đích hành vi:** Tăng productivity từ 70 → 210 stp/tháng. Đây là phase khó nhất — "vượt vực".

**Tại sao D150 (5 tháng) là ranh giới?**
- R2 yêu cầu 210 stp/tháng = gấp 3x R3. Cần thời gian ramp-up dần.
- Tài xế cần ít nhất 2-3 chu kỳ đánh giá (2-3 tháng) để tăng dần từ 70 → 140 → 210.
- Swiggy: Insurance tier stabilize sau 2 chu kỳ. Ahamove nên cho ~3 chu kỳ cho bước nhảy lớn này.
- Rusbult Investment Model: Đến D150, tài xế đã đầu tư 5 tháng — switching cost đáng kể.

**Con đường vượt vực R3 → R2:**

```
Vấn đề: R3 = 70 stp/tháng (~3.2/ngày) → R2 = 210 stp/tháng (~9.5/ngày) = GẤP 3X

Giải pháp: RAMP-UP LADDER 3 bậc trong 3 tháng:

  Tháng 3 (D61-D90):   Target 100 stp  (~4.5 stp/ngày)  — "R3 Solid"
  Tháng 4 (D91-D120):  Target 150 stp  (~6.8 stp/ngày)  — "R3 Plus" 
  Tháng 5 (D121-D150): Target 210 stp  (~9.5 stp/ngày)  — "R2 Ready"

Hỗ trợ vượt vực:
  → Multi-service unlock (thêm đơn Ghép, 4H, Enterprise) → tăng tự nhiên stp/ngày
  → Ca 4h structured (L4) → dispatch ổn định hơn on-demand
  → Weekly Quest tăng dần: 20 → 30 → 40 đơn/tuần
  → Income Dashboard: "Bạn đang ở 150 stp. Chỉ cần thêm 60 stp = R2 Vàng!"
```

| Mốc | Ngày | Điều kiện | Cơ chế | Gắn với Ranking Params |
|:----|:-----|:----------|:-------|:----------------------|
| **M10: R3 Solid** | ~D90 | 100 stp trong tháng | Badge "R3 Vững Chắc" + Gợi ý lên ca nhiều hơn | Intermediate target giữa R3(70) và R2(210) |
| **M11: 200 Orders** | ~D90-D100 | 200 đơn tổng | Unlock "Đơn Đặc Biệt" (giá trị cao) + Badge "200 Club" | — |
| **M12: R3 Plus** | ~D120 | 150 stp trong tháng + DQS ≥ 75 | **Unlock đăng ký Ca Full-day thử nghiệm** (1 ngày/tuần, không guarantee) | Bridge: cho R3 "nếm" Ca Full-day trước khi chính thức R2 |
| **M13: R2 Qualification** | D120-D150 | DQS ≥ 75, DCR ≤ 10%, Prod ≥ 210 | **RANK UP → R2 Vàng!** Layer L3, ×1.3, Ca Full-day + Guarantee, Catalog Vàng, Voucher xăng 30k | Ranking params S1: R2 threshold |
| **M14: Insurance Bronze** | Khi đạt R2 | R2 Vàng ≥ 1 chu kỳ | **Mở khóa BH tai nạn cơ bản (Ahamove sponsored, MIỄN PHÍ)** | Gap T3: Mở rộng BH xuống R2 thay vì chỉ R1 |

**Cơ chế đặc biệt Phase 3:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  🏔️ GIẢI PHÁP "VƯỢT VỰC" R3 → R2                                        │
│                                                                            │
│  1. SUB-MILESTONE SYSTEM (chia nhỏ mục tiêu lớn):                        │
│     R3 Bạc (70 stp) → R3 Solid (100) → R3 Plus (150) → R2 Vàng (210)   │
│     Mỗi sub-milestone có reward riêng → tạo "small wins" liên tục       │
│                                                                            │
│  2. CA FULL-DAY THỬ NGHIỆM (cho R3 Plus):                               │
│     R3 đạt 150 stp → được đăng ký 1 ca Full-day/tuần (không guarantee)  │
│     Mục đích: Cho tài xế "nếm" thu nhập Full-day → motivation lên R2    │
│     Params hiện tại: Full-day chỉ R1+R2 → Đề xuất mở thử cho R3 Plus   │
│                                                                            │
│  3. BẢO HIỂM MỞ RỘNG XUỐNG R2 (Đề xuất mới):                           │
│     Params hiện tại: BH chỉ R1, trả bằng points                         │
│     Đề xuất: R2 được BH tai nạn cơ bản MIỄN PHÍ (Ahamove sponsor)      │
│     Lý do: Swiggy StepUp → churn 60-70% → 10-15%. Loss aversion cực đại │
│     Cost: ~XX,000đ/người/tháng × 3,675 R2 = cần estimate                │
│                                                                            │
│  4. COMMUNITY ESCALATION:                                                  │
│     D61+: Tham gia Monthly meetup + Peer group khu vực                   │
│     D90+: Eligible làm Buddy Mentor cho tài xế mới (nếu R3+)            │
│     Benchmark: Gojek GoPartner Hub, Be beAcademy                         │
└────────────────────────────────────────────────────────────────────────────┘
```

**KPIs Phase 3:**

| Chỉ số | Target | Alert | Gắn Ranking Params |
|:-------|:-------|:------|:-------------------|
| D90 Retention | ≥ 55% | < 38% 🔴 | |
| D150 Retention | ≥ 45% | < 30% 🔴 | |
| R2 Qualification Rate (cuối D150) | ≥ 40% | < 25% 🔴 | % R3 lên R2 trong 3 chu kỳ |
| Avg Productivity Growth | +30 stp/tháng | < +15 stp 🟠 | Ramp-up 70 → 100 → 150 → 210 |
| Grace Period Recovery Rate | ≥ 60% | < 40% 🟠 | % cứu hạng thành công trong 14 ngày |
| Insurance Enrollment (R2) | ≥ 80% | < 60% 🟠 | Nếu BH mở rộng |

---

#### PHASE 4: MASTERY & OPTIMIZATION (D151 → D365)

**Tên gọi:** "Bậc Thầy"
**Trạng thái Ranking:** R2 Vàng → **Target R1 Kim Cương**
**Layer:** L3 Mediumzone → L2 Minizone

**Mục đích hành vi:** Tối ưu hóa thu nhập, đạt R1 Kim Cương, trở thành core supply đáng tin cậy.

**Tại sao D365 là ranh giới?**
- Uber data: Chỉ 4% rider mới survive 1 năm. Tài xế đến D365 = elite minority.
- R1 yêu cầu 280 stp = ~12.7 stp/ngày. Cần tài xế full-time, committed, chạy Ca Full-day.
- Maslow Self-Actualization: Tài xế giai đoạn này cần **ý nghĩa + công nhận**, không chỉ tiền.

**Con đường R2 → R1:**

```
R2 Vàng (210 stp) → R1 Kim Cương (280 stp) = +33% productivity

Khác với vực R3→R2: Ở đây không phải nhảy productivity mà là tối ưu:
  → Chạy Ca Full-day (08-18h) = 10h active → 12-14 stp/ngày tự nhiên
  → L3 Mediumzone dispatch tốt hơn L4 → ít idle time
  → Multi-service (Enterprise/SME) → đơn giá trị cao, ổn định
  → DQS ≥ 80 (vs 75 cho R2) = cần discipline: AR cao, DCR thấp
  
Timeline: ~2-4 chu kỳ (2-4 tháng) từ R2 stable → R1
```

| Mốc | Ngày | Điều kiện | Cơ chế | Gắn với Ranking Params |
|:----|:-----|:----------|:-------|:----------------------|
| **M15: R2 Stable** | ~D180 | Duy trì R2 ≥ 2 chu kỳ liên tiếp | Unlock **BH mở rộng** (cá nhân + nha khoa) + VIP Order Pool | Gap T3: Insurance Silver tier |
| **M16: 500 Orders** | ~D180-D210 | 500 đơn tổng | Badge "500 Club" + Mời tham gia Beta Testing tính năng mới | — |
| **M17: R1 Qualification** | D180-D300 | DQS ≥ 80, DCR ≤ 10%, Prod ≥ 280 | **RANK UP → R1 Kim Cương!** L2 Minizone, ×1.5, Guarantee 600-650k, Catalog full, BH Mini | Ranking params S1: R1 threshold |
| **M18: Insurance Gold** | Khi R1 ≥ 2 chu kỳ | Duy trì R1 liên tiếp | **BH Premium: cá nhân + 1 người thân** (Ahamove sponsor) | Swiggy Gold tier → loss aversion cực đại |
| **M19: 1000 Orders** | ~D300-D365 | 1000 đơn tổng | Badge "Millennium" + Quà tặng vật lý + Feature trên kênh truyền thông | Emotional milestone |
| **M20: Anniversary** | D365 | Active + ≥ R2 | Celebration event + Quà đặc biệt + Mời vào Ambassador Program | Erikson Generativity |

**Cơ chế đặc biệt Phase 4:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  🛡️ TIERED INSURANCE LADDER (Đề xuất mở rộng vs Params hiện tại)        │
│                                                                            │
│  Params hiện tại:                                                          │
│    R1 only → BH tai nạn Mini → trả bằng points (285-857 pts/tháng)      │
│                                                                            │
│  Đề xuất mới (benchmarked from Swiggy StepUp + Deliveroo):               │
│                                                                            │
│  BRONZE (R2 mới đạt):                                                     │
│    → BH tai nạn cá nhân cơ bản                                           │
│    → Ahamove sponsor (miễn phí cho tài xế)                               │
│    → Mục đích: Tạo switching cost ngay khi lên R2                        │
│                                                                            │
│  SILVER (R2 ≥ 2 chu kỳ, ~D180):                                          │
│    → BH mở rộng: tai nạn + nha khoa + khám sức khỏe định kỳ            │
│    → Ahamove sponsor                                                       │
│    → Loss aversion: "Rớt R2 = mất BH Silver"                             │
│                                                                            │
│  GOLD (R1 ≥ 2 chu kỳ):                                                   │
│    → BH Premium: cá nhân + 1 người thân                                  │
│    → Ahamove sponsor                                                       │
│    → Loss aversion CỰC ĐẠI: "Rớt R1 = mất BH cho gia đình"            │
│    → Swiggy benchmark: Gold family coverage → highest retention           │
│                                                                            │
│  📊 Expected impact: D180 retention +42% (Swiggy actual result)           │
│  💰 Cost estimate: Cần Finance validate. Budget ~47M/tháng (max)         │
│     đã dự trù trong Params S8 — mở rộng thêm Bronze/Silver              │
└────────────────────────────────────────────────────────────────────────────┘
```

**KPIs Phase 4:**

| Chỉ số | Target | Alert | Gắn Ranking Params |
|:-------|:-------|:------|:-------------------|
| D365 Retention | ≥ 35% | < 20% 🔴 | |
| R1 Qualification Rate | ≥ 30% (trong số R2) | < 15% 🔴 | % R2 lên R1 |
| Avg Productivity (R2) | ≥ 210 stp | < 190 stp 🟠 | Ranking params S1 |
| Full-day Utilization | ≥ 70% R2+ dùng Full-day | < 50% 🟠 | Ranking params S6 |
| Insurance Enrollment | ≥ 85% R2+ enrolled | < 60% 🔴 | |
| NPS | ≥ 50 | < 30 🟠 | |

---

#### PHASE 5: LEGACY & INFLUENCE (D365+)

**Tên gọi:** "Di Sản"
**Trạng thái Ranking:** R1 Kim Cương (duy trì) — hoặc R2 Vàng (loyal veteran)
**Layer:** L2 Minizone (R1) hoặc L3 (R2)

**Mục đích hành vi:** Trở thành Đại Sứ, Mentor, Community Leader — chuyển từ "nhận giá trị" sang "tạo giá trị".

| Mốc | Điều kiện | Cơ chế | Giá trị |
|:----|:----------|:-------|:--------|
| **M21: Ambassador Invite** | D365 + R2+ + Rating ≥ 4.8 | Mời chính thức vào Ambassador Program | Status + Recognition |
| **M22: Mentor Certified** | Hoàn thành training + Mentor 5 tài xế thành công (đạt R3) | Badge "Certified Mentor" + Thưởng per mentee | Generativity |
| **M23: Area Captain** | D365+ + R1 + NPS nhóm ≥ 40 | Quản lý nhóm 20-30 tài xế/khu vực. Thưởng theo performance nhóm | Leadership |
| **M24: Advisory Board** | Mời từ DM Leadership | Tham vấn chính sách, beta testing, voice cho cộng đồng | Influence |
| **M25: Legacy Milestones** | 18M, 24M, 36M... | Anniversary reward escalating + Certificate of Excellence | Long-term loyalty |

**KPIs Phase 5:**

| Chỉ số | Target | Gắn Ranking Params |
|:-------|:-------|:-------------------|
| Annual Retention (D365+) | ≥ 85% | R1 duy trì |
| Referral Rate | ≥ 3 tài xế/quý/Ambassador | |
| Mentee D30 Retention | ≥ 80% | Impact on Phase 1 KPI |
| Ambassador Engagement | ≥ 80% tham gia ≥ 1 activity/tháng | |
| Community Leader Ratio | ≥ 50% Ambassador giữ vai trò | |

---

## 3. BẢNG TỔNG HỢP: 25 MILESTONES × RANKING INTEGRATION

| # | Milestone | Ngày | Phase | Ranking Status | Điều kiện | Reward chính | Switching Cost tạo thêm |
|:--|:----------|:-----|:------|:-------------|:----------|:-------------|:----------------------|
| M1 | First Trip | D0-D1 | 1 | Unranked (New) | 1 đơn | Cash bonus + Instant Payout | — |
| M2 | Quick 5 | D2-D3 | 1 | Unranked (New) | 5 đơn | Cash + Progress bar | Endowed progress |
| M3 | Habit Seed | D7 | 1 | Unranked (New) | 10 đơn | Badge + EPH unlock | Sunk cost (effort) |
| M4 | Activation | D14 | 1→2 | Unranked → Eligible | 21 đơn | Đăng ký ca + Streak | Feature unlock |
| M5 | Week 3 Quest | D15-D21 | 2 | Unranked | 15 đơn/tuần | Quest reward | Habit formation |
| M6 | First Month | D30 | 2 | Unranked | 60 đơn tổng | Income report | Earnings visibility |
| M7 | Service Unlock | ~D30 | 2 | Unranked | 30 đơn + DQS≥70 | Siêu Tốc + Ghép Đơn | Multi-service lock |
| M8 | **R3 Rank Up** | D45-D60 | 2 | **→ R3 Bạc** | DQS≥75, DCR≤15%, 70stp | L4 + ×1.1 + Catalog Bạc + Ca 4h | **Layer + Points + Benefits** |
| M9 | Habit Confirm | D60 | 2→3 | R3 | 4d/tuần × 4 tuần | Badge + Bonus +20pts/ca | Community entry |
| M10 | R3 Solid | ~D90 | 3 | R3 | 100 stp/tháng | Badge + Gợi ý upgrade | Intermediate target |
| M11 | 200 Orders | ~D100 | 3 | R3 | 200 đơn tổng | Badge + Đơn Đặc Biệt unlock | Order pool access |
| M12 | R3 Plus | ~D120 | 3 | R3 (advanced) | 150 stp/tháng | Full-day thử nghiệm 1d/tuần | Taste of R2 benefits |
| M13 | **R2 Rank Up** | D120-D150 | 3 | **→ R2 Vàng** | DQS≥75, DCR≤10%, 210stp | L3 + ×1.3 + Full-day Guarantee + Voucher 30k | **Guarantee + Voucher + Layer** |
| M14 | Insurance Bronze | R2 mới | 3→4 | R2 | R2 ≥ 1 chu kỳ | BH tai nạn cơ bản (free) | **Insurance = loss aversion** |
| M15 | Insurance Silver | ~D180 | 4 | R2 stable | R2 ≥ 2 chu kỳ | BH mở rộng (cá nhân + nha khoa) | **Insurance escalation** |
| M16 | 500 Orders | ~D200 | 4 | R2 | 500 đơn tổng | Badge + Beta Testing | Status + Influence |
| M17 | **R1 Rank Up** | D180-D300 | 4 | **→ R1 Kim Cương** | DQS≥80, DCR≤10%, 280stp | L2 + ×1.5 + Guarantee 600-650k + Catalog full | **Full switching cost stack** |
| M18 | Insurance Gold | R1 stable | 4 | R1 ≥ 2 chu kỳ | Duy trì R1 | BH Premium (+ 1 người thân) | **Ultimate loss aversion** |
| M19 | 1000 Orders | ~D300 | 4 | R1 | 1000 đơn tổng | Badge + Quà + Feature media | Emotional investment |
| M20 | Anniversary | D365 | 4→5 | R2+/R1 | Active 12 tháng | Celebration + Ambassador invite | Identity attachment |
| M21 | Ambassador | D365+ | 5 | R2+ | Rating ≥ 4.8 | Ambassador Program entry | Role & purpose |
| M22 | Mentor Cert | D365+ | 5 | R1 | 5 mentee thành công | Certified Mentor badge + income | Teaching = deepest lock-in |
| M23 | Area Captain | D365+ | 5 | R1 | NPS nhóm ≥ 40 | Leadership role + group bonus | Responsibility |
| M24 | Advisory Board | Invite | 5 | R1 | DM Leadership mời | Policy influence | Ownership |
| M25 | Legacy | 18M+ | 5 | R1 | Ongoing | Escalating rewards | Time investment |

---

## 4. MAPPING TỔNG THỂ: PHASE × RANKING × BENEFITS × SWITCHING COST

```
Timeline    D0        D14       D60        D150       D365       D365+
            │         │         │          │          │          │
Ranking     │ Unranked │Unranked │ R3 Bạc   │ R2 Vàng  │ R1 Kim   │ R1 duy trì
            │ (New)    │→ R3     │ → R2     │ → R1     │ Cương    │
            │         │         │          │          │          │
Phase       │──PHASE 1──│───PHASE 2────│────PHASE 3────│──────PHASE 4──────│──PHASE 5──
            │Activation │Habit Build  │Ranking Climb  │Mastery & Optimize│Legacy
            │         │         │          │          │          │
Layer       │ L6 MASS  │ L6→L4   │ L4 Big   │ L3 Med   │ L2 Mini  │ L2 Mini
            │(+Newbie  │Bigzone  │→L3 Med   │→L2 Mini  │zone      │zone
            │Priority) │         │          │          │          │
            │         │         │          │          │          │
Earnings    │Guarantee │Quest    │55-60k/h  │60-65k/h  │65-70k/h  │65-70k/h
            │14 ngày   │System   │L4 target │L3 target │L2 target │L2 target
            │         │         │          │Full-day   │Full-day   │
            │         │         │          │550-600k/d │600-650k/d│
            │         │         │          │          │          │
Points      │ ×1.0     │×1.0→×1.1│ ×1.1     │ ×1.3     │ ×1.5     │ ×1.5
            │ no bonus │+20/ca   │ +20/ca   │ +25/ca   │ +30/ca   │ +30/ca
            │         │         │          │          │          │
Insurance   │ —        │ —       │ —        │Bronze→   │Silver→   │Gold
            │         │         │          │Silver    │Gold      │(gia đình)
            │         │         │          │          │          │
Catalog     │ ❌       │ ❌→Bạc  │ Bạc      │ Vàng+Bạc │Full      │Full
            │         │         │          │          │          │
Community   │Buddy     │Zalo     │Monthly   │Mentor    │Area      │Advisory
            │System    │group    │Meetup    │eligible  │Captain   │Board
            │         │         │          │          │          │
Switching   │ Thấp     │ Vừa     │ Cao      │ Rất cao  │Cực cao   │Gần không
Cost tích   │(sunk     │(habit + │(tier +   │(guarantee│(insurance│ thể rời
lũy        │ effort)  │points + │insurance │+insurance│+family   │
            │         │ unlock) │+ catalog)│+catalog) │+identity)│
```

---

## 5. ĐỀ XUẤT THAY ĐỔI VỚI RANKING PARAMS HIỆN TẠI

### 5.1 Thay Đổi Cần Thiết (Cần Update Params)

| # | Thay đổi | Params hiện tại | Đề xuất | Lý do | Impact |
|:--|:---------|:---------------|:--------|:------|:-------|
| 1 | **New Driver flag** | Unranked = 1 nhóm duy nhất | Tách "New Unranked" (< D60, < 100 đơn) vs "Performance Unranked" | Tài xế mới không nên bị đối xử như tài xế rớt hạng | Product change |
| 2 | **New Driver Guarantee** | Không có guarantee cho Unranked | 14 ngày guarantee (D0-D14) cho New Unranked | Grab: +32% D30 retention | Budget impact |
| 3 | **BH mở rộng xuống R2** | BH chỉ R1, trả bằng points | Bronze (R2 mới) + Silver (R2 stable) miễn phí | Swiggy: churn 60-70% → 10-15% | Budget impact |
| 4 | **Sub-milestone R3→R2** | Chỉ có 2 ngưỡng: 70 và 210 | Thêm target trung gian: 100 (R3 Solid), 150 (R3 Plus) | Vực 3x quá lớn, cần chia nhỏ | Product + Ops |
| 5 | **Ca Full-day thử cho R3 Plus** | Full-day chỉ R1+R2 | R3 đạt 150 stp → 1 ca Full-day/tuần (không guarantee) | Taste of benefits = motivation | Slot allocation |

### 5.2 Giữ Nguyên (Params Tốt, Không Cần Đổi)

| Params | Lý do giữ |
|:-------|:---------|
| KPI thresholds (DQS, DCR, Productivity) | Đã align với global benchmark. R3=70 phù hợp part-time entry, R1=280 phù hợp elite. |
| Fleet ratio 15/35/35/15 | Hợp lý — tạo kim tự tháp có đủ R1/R2 cho supply quality |
| Layer cascade (80% fill trigger) | Cơ chế dispatch thông minh, đảm bảo utilization |
| AhaPoints formula (GSV÷5000 × multiplier + bonus) | Đơn giản, công bằng, gắn với layer |
| Points expire cuối quý | Tạo urgency tiêu điểm → engagement with catalog |
| Ca 4h + Full-day structure | Phù hợp thực tế. Thêm thử nghiệm Full-day cho R3 Plus là đủ |

---

## 6. INACTIVITY PROTOCOL — GẮN VỚI PHASE & RANKING

| Inactive | Phase 1 (D0-D14) | Phase 2 (D15-D60) | Phase 3 (D61-D150) | Phase 4 (D151-D365) | Phase 5 (D365+) |
|:---------|:-----------------|:-----------------|:-------------------|:-------------------|:---------------|
| **2 ngày** | Push + Milestone reminder | — | — | — | — |
| **3 ngày** | SMS + Bonus offer | Push + Quest reminder | — | — | — |
| **5 ngày** | **Gọi điện** | Push + Income projection | — | — | — |
| **7 ngày** | Escalate DM Ops | **Quest win-back đặc biệt** | Push + "Bạn sắp mất R3" | — | — |
| **10 ngày** | — | **Gọi điện** + Re-activation | Push + Grace Period warning | Push + "Bạn sắp mất R2 + BH" | — |
| **14 ngày** | Flag Dormant | Flag Dormant | **Gọi điện** + Grace Period | **Gọi điện** + "Mất BH Silver!" | Push + Quản lý khu vực nhắn |
| **21 ngày** | Archive | Win-back campaign | Win-back (Mid-value) | Win-back (High-value) | **Gọi điện** + Exit survey |
| **30 ngày** | Archive | Archive | Monthly win-back batch | Monthly win-back (priority) | Monthly win-back |

> **Nguyên tắc:** Phase càng cao + Rank càng cao = can thiệp càng mạnh và càng sớm. R1 inactive 7 ngày = R3 inactive 14 ngày về mức ưu tiên.

---

## 7. CROSS-REFERENCE

| File | Nội dung liên quan |
|:-----|:-------------------|
| `01. STRATEGY/2026-05-driver-ranking-params.html` | Source of truth cho KPI thresholds, layer, ca, AhaPoints, catalog |
| `01. STRATEGY/2026-05-driver-lifecycle-journey.md` | Framework v3.0 (6 phase) — phiên bản trước, chi tiết từng phase |
| `06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md` | Nghiên cứu 15+ nền tảng toàn cầu, benchmark, behavioral science |

---

*Driver Management Team | Ahamove | 02/06/2026*
*Phiên bản: v4.0 — 5-Phase Journey gắn chặt Ranking Params v2.0*
