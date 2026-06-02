# PROPOSAL: THIẾT KẾ LẠI DRIVER JOURNEY — 5 PHASE × 25 MILESTONES

> **Trình bày:** Driver Management Team
> **Ngày:** 02/06/2026 · **Phiên bản:** v4.0
> **Scope:** Tài xế 2 bánh (Bike) — SGN + HAN (~10.500 weekly actives)

---

## EXECUTIVE SUMMARY

**Vấn đề:** Hệ thống xếp hạng Ahamove (Ranking v2.0) đã có nền tảng tốt — 4 tier, DQS composite, AhaPoints, layer cascade — nhưng **thiếu lộ trình hành vi** hướng dẫn tài xế đi từ ngày đầu tiên đến trở thành core supply. Khi đối chiếu ranking params với hành vi thực tế và benchmark 15 nền tảng toàn cầu, xuất hiện **5 điểm nghẽn** (tensions) đang làm rò rỉ tài xế ở từng giai đoạn.

**Đề xuất:** Thiết kế **Driver Journey 5 Phase** với **25 mốc hành vi** (milestones) gắn chặt vào hệ thống ranking hiện tại. Mỗi phase có mục đích rõ ràng, mỗi mốc có cơ sở khoa học, và toàn bộ journey tạo **switching cost tích lũy** khiến tài xế càng ở lâu càng khó rời đi.

**Kết quả kỳ vọng:**

| Chỉ số | Hiện trạng ước tính | Target | Benchmark |
|:-------|:--------------------|:-------|:----------|
| D14 Retention | ~55% | **80%** | Grab w/ Guarantee: 85% |
| D30 Retention | ~35% | **72%** | Grab 14d: +32pp |
| D60 Retention (R3 Rate) | ~25% | **55%** | Gojek GoPartner: 60% |
| D150 Retention (R2 Rate) | ~15% | **40%** | Swiggy StepUp: 55% |
| D365 Retention | ~8% | **35%** | Uber Pro active core: 20%, XanhSM: 80% |
| Driver LTV trung bình | ~3.5 tháng | **~12 tháng** | +240% |

---

## PHẦN 1: SITUATION — AHAMOVE ĐÃ CÓ GÌ

### 1.1 Ranking Params v2.0 — Nền Tảng Vững

Hệ thống hiện tại đã có cấu trúc tier rõ ràng:

| Rank | DQS | DCR | Prod (stp/tháng) | Layer | AhaPoints | Earning target | Đặc quyền |
|:-----|:----|:----|:-----------------|:------|:----------|:-------------|:----------|
| **R1 Kim Cương** | ≥ 80 | ≤ 10% | ≥ 280 | L2 Minizone | ×1.5 +30/ca | 65-70k/h | Full-day Guarantee 600-650k, Voucher xăng 50k, BH Mini |
| **R2 Vàng** | ≥ 75 | ≤ 10% | ≥ 210 | L3 Mediumzone | ×1.3 +25/ca | 60-65k/h | Full-day Guarantee 550-600k, Voucher xăng 30k |
| **R3 Bạc** | ≥ 75 | ≤ 15% | ≥ 70 | L4 Bigzone | ×1.1 +20/ca | 55-60k/h | Ca 4h structured, Catalog Bạc |
| **Unranked** | < 75 | — | — | L6 MASS | ×1.0 | — | On-demand, không benefits |

Fleet target: R1 15% (~1.575) · R2 35% (~3.675) · R3 35% (~3.675) · Unranked 15% (~1.575)

**Đánh giá so với toàn cầu:** Hệ thống tier + DQS composite + AhaPoints multiplier + layer cascade đặt Ahamove ngang hàng Uber Pro và DoorDash Dasher Rewards về độ phức tạp, vượt trội Deliveroo/Rappi (không tier), và tiệm cận Grab/Gojek về benefits structure.

### 1.2 Điều Ahamove Chưa Có: Lộ Trình Hành Vi

Ranking params trả lời câu hỏi **"tài xế ở đâu?"** (tier nào, layer nào, bao nhiêu points) — nhưng chưa trả lời **"tài xế nên làm gì tiếp theo?"**

Một tài xế mới đăng ký ngày hôm nay sẽ thấy:
- Mình là "Unranked" — giống hệt tài xế rớt hạng
- Layer L6 MASS — đơn tràn, không ưu tiên, không structured
- Không benefits, không guarantee, không hướng dẫn cụ thể
- Biết cần DQS ≥ 75 và 70 stp để lên R3, nhưng **không biết đường đi**

Đây là vấn đề mà 15 nền tảng toàn cầu đã giải quyết theo những cách khác nhau.

---

## PHẦN 2: COMPLICATION — 5 ĐIỂM NGHẼN TỪ NGHIÊN CỨU TOÀN CẦU & ĐỐI CHIẾU PARAMS

### Nghiên cứu nền

Đã phân tích 15 nền tảng: **Meituan** (Trung Quốc, 7 triệu riders), **Ele.me** (3.1 triệu), **Grab** (SEA, 5 triệu), **Gojek** (Indonesia/SG, 2.5 triệu), **Uber** (Global, 5 triệu), **DoorDash** (US, 6 triệu), **Deliveroo** (UK/EU), **Swiggy** (India), **Zomato** (India), **Rappi** (LATAM), **iFood** (Brazil, 760k), **Be**, **XanhSM**, **Bolt Food**, **Wolt**. Chi tiết tại `06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md`.

4 mô hình vận hành trên thế giới:

| Mô hình | Đại diện | Churn rate | Đặc điểm |
|:--------|:---------|:-----------|:----------|
| **Pure Gig** (tự do hoàn toàn) | DoorDash, Uber, Deliveroo, Bolt | 60-90%/năm | Linh hoạt tối đa, retention phụ thuộc incentive spend |
| **Structured Gig** (gig có cấu trúc) | Grab, Gojek, Swiggy, **Ahamove** | 30-50%/năm | Tier system + benefits ladder → switching cost cao |
| **Dual-Track** (FT + PT) | Meituan, Ele.me, iFood | 20-40%/năm | Dedicated riders churn thấp, crowdsource churn cao |
| **Employment** (hợp đồng LĐ) | XanhSM, Wolt (DE/FI) | 15-25%/năm | Retention cao nhất, chi phí cố định cao nhất |

Ahamove ở mô hình **Structured Gig** — đúng positioning. Nhưng khi đối chiếu ranking params với benchmark, xuất hiện 5 điểm nghẽn:

---

### Tension 1: "New Unranked" = "Bad Unranked" 🔴

**Vấn đề:** Hệ thống ranking không phân biệt tài xế vừa đăng ký (chưa có data) với tài xế rớt hạng (performance kém). Cả hai đều ở L6 MASS, không benefits, không structured slot.

**Hệ quả:** Tài xế mới bị "phạt" trước khi có cơ hội chứng minh. Trải nghiệm ngày đầu tiên = dispatch tràn, đơn xa, không ưu tiên — chính xác ngược lại với những gì mọi nền tảng thành công đang làm.

**Global benchmark:**
- **DoorDash:** "First 50 deliveries" = protected window — tài xế mới có perks riêng, chưa đánh giá tier
- **Uber:** Tài xế mới bắt đầu ở Blue tier (không phải "dưới Blue"), vẫn có gas cashback 6%
- **Meituan:** Crowdsource riders mới được training + onboarding period trước khi vào hệ thống scoring
- **Gojek:** GoPartner program phân biệt "new" vs "active" vs "dormant"

### Tension 2: Vực R3 → R2 (70 → 210 stp = gấp 3x) 🔴

**Vấn đề:** Quy đổi productivity sang hành vi hàng ngày:

| Rank | stp/tháng | stp/ngày (22 ngày) | Hành vi thực tế |
|:-----|:----------|:-------------------|:---------------|
| **R3 Bạc** | 70 | ~3.2 | Part-time: 4-5 đơn/ngày × 4-5 ngày/tuần |
| **R2 Vàng** | 210 | ~9.5 | Full-time: ~10 đơn/ngày × 5-6 ngày/tuần |
| **Gap** | **3x** | **3x** | **Chuyển hoàn toàn từ part-time sang full-time** |

Không có nền tảng nào trên thế giới yêu cầu bước nhảy 3x giữa 2 tier liền kề mà không có bậc trung gian.

**Hệ quả:** Tài xế mắc kẹt ở R3, không thấy đường lên R2, mất động lực, dần trở thành Drifter/Dormant. Đây là "death zone" lớn nhất trong journey.

**Global benchmark:**
- **Uber Pro:** Blue → Gold → Platinum → Diamond — mỗi bước chỉ tăng ~30-50% points requirement
- **DoorDash:** Silver → Gold → Platinum — composite score tăng dần, không có cliff
- **Gojek GoalBetter:** Classic → Premium → Pro → Elite — trips requirement tăng ~40-70% mỗi bậc
- **Meituan:** Crowdsource Silver (140 đơn) → Gold (200 đơn) = chỉ +43%

### Tension 3: BH Chỉ Cho R1, Trả Bằng Points 🟠

**Vấn đề:** Ranking params hiện tại: BH tai nạn Mini chỉ dành cho R1 Kim Cương, thanh toán bằng AhaPoints (285-857 pts/tháng). R2, R3, Unranked không có bất kỳ BH nào.

**Hệ quả:** Bỏ lỡ cơ chế giữ chân mạnh nhất mà nghiên cứu toàn cầu đã chứng minh. BH là switching cost phi tài chính — tài xế không thể "mang theo" khi chuyển sang Grab/Be.

**Global benchmark:**

| Nền tảng | BH cho ai | Kết quả |
|:---------|:----------|:--------|
| **Swiggy StepUp** | Gold (gia đình), Silver (cá nhân), Bronze (tai nạn) — theo weekly points | Churn giảm từ **60-70% → 10-15%**. D180 retention +42% |
| **Deliveroo** | Tất cả riders — BH tai nạn + £35/ngày ốm + £1,000 sinh con + £1M liability | Miễn phí, không tier |
| **XanhSM** | Tất cả (hợp đồng LĐ) — BHXH + BHYT + BHTN đầy đủ | Churn **15-20%/năm** — thấp nhất VN |
| **Meituan** | Pilot BH tai nạn lao động — đầu tư 1.4 tỷ CNY | Đang rollout toàn quốc |
| **Ahamove** | Chỉ R1, trả bằng points | **Gap lớn nhất vs đối thủ trực tiếp** |

### Tension 4: Không Có Guarantee Cho Tài Xế Mới 🟠

**Vấn đề:** Full-day guarantee (550-650k/ngày) chỉ áp dụng cho R1 và R2. Tài xế mới (Unranked) tham gia nền tảng không có bất kỳ safety net nào về thu nhập.

**Hệ quả:** Tài xế mới không biết mình sẽ kiếm được bao nhiêu. "Lo lắng về thu nhập" là nguyên nhân #1 khiến tài xế mới rời đi sớm (ILO Gig Economy Report 2024).

**Global benchmark:**

| Nền tảng | Guarantee cho tài xế mới | Kết quả |
|:---------|:------------------------|:--------|
| **Grab** | 14 ngày Guaranteed Earnings | D30 retention **+32%** |
| **Uber** | 30 ngày guarantee (thị trường chọn lọc) | Early churn **-15-20%** |
| **Gojek** | Minimum income program gắn với GoPartner tier | Retention baseline ổn định |
| **Ahamove** | Không có | Tài xế mới = high uncertainty = high churn |

### Tension 5: Points Expire Cuối Quý 🟡

**Vấn đề nhỏ nhưng tạo unfairness:** Tài xế đăng ký giữa tháng 3 (gần cuối Q1) sẽ bị reset points vào 31/3 trước khi tích đủ đổi gì có ý nghĩa. Tài xế đăng ký đầu tháng 1 có 3 tháng tích lũy.

**Giải pháp đơn giản:** Points của tài xế mới (< 60 ngày) không expire trong quý đầu tiên đăng ký. Áp dụng expire bình thường từ quý thứ 2 trở đi.

---

## PHẦN 3: RESOLUTION — DRIVER JOURNEY 5 PHASE

### 3.1 Tại Sao 5 Phase (Không Phải 6 Như v3.0)?

Framework v3.0 trước đây chia 6 phase, tách riêng Activation (D0-D3) và First Win (D4-D14). Sau khi đối chiếu với ranking params và benchmark toàn cầu, tôi đề xuất **gộp thành 5 phase** vì:

1. **Ranking params không có trạng thái trung gian** giữa D0 và D14 — cả hai đều Unranked/L6
2. **Không nền tảng nào dùng D3 làm ranh giới phase** — Grab dùng 14 ngày, DoorDash dùng 50 đơn, Uber dùng 30 ngày
3. **Mục tiêu hành vi D0-D14 là một khối liên tục**: kích hoạt → first win → chứng minh thu nhập
4. **Gộp lại cho phép thiết kế "Protected Window" 14 ngày** mạch lạc — tương đương Grab Guarantee 14 ngày
5. **Thêm 1 phase "Ranking Climb"** (D61-D150) chuyên giải quyết **Tension 2** (vực R3→R2)

### 3.2 Tổng Quan 5 Phase

```
  D0          D14         D60          D150         D365         D365+
  │           │           │            │            │            │
  ●───────────●───────────●────────────●────────────●────────────●──→
  │           │           │            │            │            │
  │  PHASE 1  │  PHASE 2  │  PHASE 3   │  PHASE 4   │  PHASE 5   │
  │  ACTIVATION│ HABIT     │  RANKING   │  MASTERY   │  LEGACY    │
  │  & FIRST  │ BUILDING  │  CLIMB     │            │            │
  │  WIN      │           │            │            │            │
  │           │           │            │            │            │
  │ Unranked  │ Unranked  │ R3 Bạc     │ R2 Vàng    │ R1 Kim     │
  │ (New)     │ → R3      │ → R2 Vàng  │ → R1 KC    │ Cương      │
  │           │           │            │            │ (duy trì)  │
  │ L6 MASS   │ L6 → L4   │ L4 → L3   │ L3 → L2   │ L2         │
  │ +Newbie   │ Bigzone   │ Mediumzone │ Minizone   │ Minizone   │
  │ Priority  │           │            │            │            │
  │           │           │            │            │            │
  │ Churn:    │ Churn:    │ Churn:     │ Churn:     │ Churn:     │
  │ RẤT CAO   │ CAO       │ TRUNG BÌNH │ THẤP       │ RẤT THẤP  │
  │           │           │            │            │            │
  │ "Tôi thử" │ "Tôi quen"│ "Tôi leo"  │ "Tôi tối ưu"│"Tôi dẫn dắt"│
```

### 3.3 Tại Sao Mỗi Ranh Giới Được Chọn?

Mỗi ranh giới phase trùng với **churn cliff point** (thời điểm churn risk tăng đột biến) được xác nhận bởi data toàn cầu, VÀ gắn với **mốc ranking có ý nghĩa** trong params Ahamove:

| Ranh giới | Churn cliff (toàn cầu) | Gắn Ranking Params | Lý do khoa học |
|:----------|:----------------------|:-------------------|:--------------|
| **D14** | Uber: 47% quit trước 25 trips. Grab: Guarantee 14d là turning point | Unranked vẫn, nhưng đã tích lũy 21+ đơn | Fogg Behavioral Model: 21 repetitions = habit loop khởi động |
| **D60** | Lally (2010): 66 ngày trung bình hình thành thói quen. Grab: ~45% churn giai đoạn này | **R3 Bạc đạt được** (70 stp/tháng khả thi ở tháng thứ 2) | SDT: Chuyển từ external motivation → identified motivation |
| **D150** | Rusbult: Investment Model — 5 tháng = switching cost đáng kể | **R2 Vàng đạt được** (ramp 70→210 trong 3 chu kỳ) | Zwettler (2024): "Positioning Challenge" kết thúc ~D120 |
| **D365** | Uber: Chỉ 4% rider survive 1 năm. Ai đến đây = elite | **R1 Kim Cương đạt/duy trì** | Erikson Generativity: Nhu cầu "truyền lại" |

---

### 3.4 Chi Tiết Từng Phase

#### PHASE 1: ACTIVATION & FIRST WIN (D0 → D14)

> **Câu hỏi tài xế:** "Liệu app này có đáng để tôi bỏ thời gian không?"
> **Mục tiêu Ahamove:** Hoàn thành ≥ 21 đơn trong 14 ngày

**Ranking status:** Unranked — nhưng thêm **"New Driver" flag** (giải quyết Tension 1)
**Layer:** L6 MASS + Newbie Priority Dispatch (đơn gần, đơn dễ)

**4 cơ chế đặc biệt (giải quyết Tension 1 + 4):**

| Cơ chế | Chi tiết | Benchmark | Chi phí |
|:-------|:---------|:----------|:-------|
| **New Driver Guarantee 14 ngày** | ≥ 3 đơn/ngày → đảm bảo tối thiểu XXXk/ngày. Ahamove bù chênh lệch. D1-D7 mức cao, D8-D14 mức -20% | Grab 14d → +32% D30 retention | Budget (ceiling on subsidy — cost = 0 nếu tài xế tự vượt) |
| **Newbie Priority Dispatch** | Ưu tiên đơn < 3km, đơn không yêu cầu đặc biệt | Uber: first trip trong 48h → D7 +41% | Algorithm tweak, zero cost |
| **Instant Payout miễn phí** | Nhận tiền sau mỗi đơn/cuối ngày. Miễn phí 30 ngày đầu | 44% tài xế rời đi nếu payout chậm/tốn phí | Transaction fee minimal |
| **Buddy System** | 1 tài xế R2+/R1 cùng khu vực làm mentor. Buddy được thưởng khi mentee đạt 21 đơn | Gojek GoPartner Mentor, Be beAcademy | Buddy bonus nhỏ |

**Milestones Phase 1:**

| Mốc | Thời điểm | Trigger | Reward | Tâm lý tạo ra |
|:----|:----------|:--------|:-------|:-------------|
| **M1** First Trip | D0-D1 | 1 đơn đầu tiên | Cash bonus (declining: 24h > 48h > 72h) | "Tôi làm được!" — Self-efficacy |
| **M2** Quick 5 | D2-D3 | 5 đơn | Cash nhỏ + Progress bar "5/21" | "Tôi đang tiến bộ" — Endowed Progress |
| **M3** Habit Seed | D7 | 10 đơn | Badge "Tuần Đầu Tiên" + Unlock EPH tracker | "Tôi bắt đầu hiểu cách chơi" |
| **M4** Activation Complete | D14 | 21 đơn | **Gateway vào Phase 2:** Đăng ký ca 4h, Streak system bắt đầu | "Tôi đủ tin tưởng để tiếp tục" |

**KPIs:**

| Chỉ số | Target | Alert |
|:-------|:-------|:------|
| Activation Rate (≥ 1 đơn trong 72h) | ≥ 85% | < 60% 🔴 |
| 21-Trip Achievement Rate | ≥ 65% | < 45% 🔴 |
| D14 Retention | ≥ 80% | < 65% 🔴 |
| Guarantee Utilization (% tự vượt) | ≥ 55% | < 40% 🟠 |

---

#### PHASE 2: HABIT BUILDING (D15 → D60)

> **Câu hỏi tài xế:** "Đây có phải nguồn thu nhập ổn định cho tôi không?"
> **Mục tiêu Ahamove:** Tài xế đạt R3 Bạc trước D60

**Ranking status:** Unranked → **R3 Bạc**
**Layer:** L6 → L4 Bigzone (khi đạt R3)

**Tại sao R3 là target đúng ở D60?**
R3 yêu cầu 70 stp/tháng = ~3.2 stp/ngày × 22 ngày = hoàn toàn khả thi với tài xế part-time-to-full-time. Sau Phase 1, tài xế đã hoàn thành ~21 đơn trong 14 ngày (~1.5 stp/ngày). Trong 45 ngày tiếp theo, tăng lên 3-4 stp/ngày là progression tự nhiên.

**Cơ chế chính:**

| Cơ chế | Chi tiết | Benchmark |
|:-------|:---------|:----------|
| **Weekly Quest** (thay Guarantee từ D15) | Cơ Bản: 15 đơn/tuần. Nâng Cao: 25. Siêu Cấp: 35. Progress bar real-time | Uber Quest + DoorDash Challenges (+23% completion) |
| **Progressive Service Unlock** | 30 đơn: Siêu Tốc. 50 đơn: Ghép Đơn. 70 đơn: 4H Delivery. 100 đơn (R3): Enterprise | Uber: cross-platform +19pp retention, chi phí = 0 |
| **Income Dashboard** | Tích lũy earnings từ D1, so sánh tuần/tuần, đặt mục tiêu cá nhân | DoorDash Earnings Tracker |
| **Cohort Community** | Zalo group 5-10 người cùng batch + Monthly meetup offline 15-20 người/khu vực | Gojek GoFleet, Be beAcademy |

**Milestones Phase 2:**

| Mốc | Thời điểm | Trigger | Reward | Gắn Ranking |
|:----|:----------|:--------|:-------|:------------|
| **M5** Week 3 Quest | D15-D21 | 15 đơn/tuần | Quest reward | Preparation 70 stp (R3) |
| **M6** First Month | D30 | 60 đơn tổng | Báo cáo thu nhập tháng 1 | Calibration gần R3 |
| **M7** Service Unlock | ~D30 | 30 đơn + DQS ≥ 70 | Siêu Tốc + Ghép Đơn | Multi-service → tăng EPH |
| **M8** **R3 Rank Up** | D45-D60 | DQS ≥ 75, DCR ≤ 15%, 70 stp | **L4 Bigzone + ×1.1 + Ca 4h + Catalog Bạc** | Ranking params S1 |
| **M9** Habit Confirm | D60 | 4d/tuần × 4 tuần liên tiếp | Badge "Thói Quen Vàng" | Points +20/ca bắt đầu |

**KPIs:**

| Chỉ số | Target | Alert |
|:-------|:-------|:------|
| D60 Retention | ≥ 62% | < 45% 🔴 |
| R3 Qualification Rate (cuối D60) | ≥ 55% | < 35% 🔴 |
| Weekly Active Days | ≥ 4 ngày | < 3 ngày 🟠 |
| Multi-service Unlock Rate (≥ 2 dịch vụ) | ≥ 50% | < 30% 🟠 |

---

#### PHASE 3: RANKING CLIMB (D61 → D150)

> **Câu hỏi tài xế:** "Tôi muốn lên hạng — nhưng bước nhảy quá lớn?"
> **Mục tiêu Ahamove:** Tài xế vượt vực R3 → R2 Vàng thông qua ramp-up ladder

**Ranking status:** R3 Bạc → **R2 Vàng**
**Layer:** L4 Bigzone → L3 Mediumzone

**Đây là phase quan trọng nhất** — nơi **Tension 2** (vực 3x) cần được giải quyết.

**Giải pháp: Ramp-Up Ladder 3 bậc**

Thay vì yêu cầu nhảy từ 70 → 210 stp (3x) ngay lập tức, thiết kế 3 bậc trung gian:

```
Tháng 3 (D61-D90):   Target 100 stp  (~4.5 stp/ngày)   "R3 Solid"     +43% vs R3
Tháng 4 (D91-D120):  Target 150 stp  (~6.8 stp/ngày)   "R3 Plus"      +50% vs bậc trước
Tháng 5 (D121-D150): Target 210 stp  (~9.5 stp/ngày)   "R2 Ready"     +40% vs bậc trước
```

Mỗi bậc tăng 40-50% — tương đương Uber Pro (Gold→Platinum) và Gojek (Premium→Pro). Không có bậc nào yêu cầu nhảy 3x.

**Cơ chế vượt vực:**

| Cơ chế | Chi tiết | Tại sao hiệu quả |
|:-------|:---------|:-----------------|
| **Sub-milestone Rewards** | 100 stp: Badge "R3 Solid". 150 stp: Badge "R3 Plus" + **unlock Ca Full-day thử nghiệm** 1 ngày/tuần | Chia nhỏ mục tiêu lớn → "small wins" liên tục (Variable Ratio Reinforcement) |
| **Ca Full-day thử cho R3 Plus** | R3 đạt 150 stp → 1 ca Full-day/tuần (không guarantee) | Cho tài xế "nếm" thu nhập R2 trước khi chính thức đạt → motivation boost |
| **BH Bronze khi đạt R2** | R2 mới → BH tai nạn cơ bản, Ahamove sponsor, miễn phí | Loss aversion bắt đầu: "Rớt R2 = mất BH". Swiggy: retention +42% |
| **Grace Period 14 ngày** | Rớt dưới ngưỡng R3/R2 → không rớt hạng ngay, có 14 ngày cứu | Kahneman: Loss aversion gấp 2x. Uber drivers làm chăm hơn để GIỮ tier |

**Milestones Phase 3:**

| Mốc | Thời điểm | Trigger | Reward | Gắn Ranking |
|:----|:----------|:--------|:-------|:------------|
| **M10** R3 Solid | ~D90 | 100 stp/tháng | Badge + Gợi ý tăng ca | Intermediate target |
| **M11** 200 Orders | ~D100 | 200 đơn tổng | Badge + Đơn Đặc Biệt unlock | — |
| **M12** R3 Plus | ~D120 | 150 stp/tháng | **Ca Full-day thử 1d/tuần** (không guarantee) | Bridge thực tế trước R2 |
| **M13** **R2 Rank Up** | D120-D150 | DQS ≥ 75, DCR ≤ 10%, 210 stp | **L3 + ×1.3 + Full-day Guarantee + Voucher 30k** | Ranking params S1 |
| **M14** Insurance Bronze | R2 ≥ 1 chu kỳ | Duy trì R2 | **BH tai nạn cá nhân (free)** | Giải quyết Tension 3 |

**KPIs:**

| Chỉ số | Target | Alert |
|:-------|:-------|:------|
| D150 Retention | ≥ 45% | < 30% 🔴 |
| R2 Qualification Rate (trong số R3) | ≥ 40% | < 25% 🔴 |
| Avg Productivity Growth | +30 stp/tháng | < +15 stp 🟠 |
| Grace Period Recovery Rate | ≥ 60% | < 40% 🟠 |

---

#### PHASE 4: MASTERY & OPTIMIZATION (D151 → D365)

> **Câu hỏi tài xế:** "Làm sao tối ưu thu nhập và ổn định lâu dài?"
> **Mục tiêu Ahamove:** R2 → R1 Kim Cương + Insurance ladder escalation

**Ranking status:** R2 Vàng → **R1 Kim Cương**
**Layer:** L3 Mediumzone → L2 Minizone

**Khác biệt với Phase 3:** R2 → R1 chỉ tăng +33% (210 → 280 stp) — không phải vực 3x. Tài xế đã chạy Ca Full-day (10h), đã ở L3 Mediumzone (dispatch tốt hơn), đã có multi-service. Bước nhảy này là tối ưu, không phải thay đổi lối sống.

**Cơ chế chính — Insurance Ladder (giải quyết Tension 3):**

| Insurance Tier | Điều kiện | Quyền lợi | Loss Aversion |
|:-------------|:----------|:----------|:-------------|
| **Bronze** | R2 ≥ 1 chu kỳ | BH tai nạn cá nhân cơ bản — **miễn phí** | "Rớt R2 = mất BH" |
| **Silver** | R2 ≥ 2 chu kỳ (~D180) | BH mở rộng: tai nạn + nha khoa + khám sức khỏe — **miễn phí** | "Rớt R2 lâu = mất BH Silver" |
| **Gold** | R1 ≥ 2 chu kỳ | BH Premium: cá nhân + 1 người thân — **miễn phí** | **"Rớt R1 = mất BH cho gia đình"** — loss aversion cực đại |

> **So sánh:** Params hiện tại = BH chỉ R1, trả bằng points (285-857 pts). Đề xuất mới = BH miễn phí từ R2, escalate theo thời gian, cost Ahamove sponsor. Benchmark: Swiggy churn giảm từ 60-70% xuống 10-15% nhờ tiered insurance.

**Milestones Phase 4:**

| Mốc | Thời điểm | Trigger | Reward |
|:----|:----------|:--------|:-------|
| **M15** Insurance Silver | ~D180 | R2 ≥ 2 chu kỳ | BH mở rộng (nha khoa + khám SK) |
| **M16** 500 Orders | ~D200 | 500 đơn tổng | Badge + Mời Beta Testing |
| **M17** **R1 Rank Up** | D180-D300 | DQS ≥ 80, DCR ≤ 10%, 280 stp | **L2 + ×1.5 + Guarantee 600-650k + Full catalog + BH Mini** |
| **M18** Insurance Gold | R1 ≥ 2 chu kỳ | Duy trì R1 | **BH Premium: cá nhân + 1 người thân** |
| **M19** 1000 Orders | ~D300 | 1000 đơn tổng | Badge "Millennium" + Quà vật lý + Feature media |
| **M20** Anniversary | D365 | Active 12 tháng | Celebration + Mời Ambassador Program |

**KPIs:**

| Chỉ số | Target | Alert |
|:-------|:-------|:------|
| D365 Retention | ≥ 35% | < 20% 🔴 |
| R1 Qualification Rate (trong số R2) | ≥ 30% | < 15% 🔴 |
| Insurance Enrollment (R2+) | ≥ 85% | < 60% 🔴 |
| Full-day Utilization (R2+) | ≥ 70% | < 50% 🟠 |

---

#### PHASE 5: LEGACY & INFLUENCE (D365+)

> **Câu hỏi tài xế:** "Tôi còn có thể phát triển gì ở đây?"
> **Mục tiêu Ahamove:** Chuyển tài xế từ "nhận giá trị" → "tạo giá trị"

**Ranking status:** R1 duy trì (hoặc R2 veteran)
**Layer:** L2 Minizone

**Cơ sở khoa học:** Erikson (1963) — Generativity: người trưởng thành sau khi đạt mastery có nhu cầu "truyền lại" cho thế hệ sau. Tài xế > 1 năm cần **vai trò và trách nhiệm**, không chỉ tiền.

**Milestones Phase 5:**

| Mốc | Trigger | Vai trò | Reward |
|:----|:--------|:--------|:-------|
| **M21** Ambassador Invite | D365 + R2+ + Rating ≥ 4.8 | Đại sứ thương hiệu | Status + Recognition |
| **M22** Mentor Certified | 5 mentee đạt R3 | Certified Mentor | Thưởng per mentee thành công |
| **M23** Area Captain | R1 + NPS nhóm ≥ 40 | Quản lý 20-30 tài xế/khu vực | Thưởng cố định + % performance nhóm |
| **M24** Advisory Board | DM Leadership mời | Cố vấn chính sách | Policy influence |
| **M25** Legacy | 18M, 24M, 36M... | Veteran reward escalation | Certificate + Quà escalating |

**KPIs:**

| Chỉ số | Target |
|:-------|:-------|
| Annual Retention (D365+) | ≥ 85% |
| Referral Rate | ≥ 3 tài xế/quý/Ambassador |
| Mentee D30 Retention | ≥ 80% |
| Ambassador Engagement (≥ 1 activity/tháng) | ≥ 80% |

---

## PHẦN 4: SWITCHING COST TÍCH LŨY — TẠI SAO JOURNEY NÀY GIỮ CHÂN ĐƯỢC

Mỗi phase thêm 1 lớp switching cost. Tài xế càng ở lâu, càng "mất nhiều" nếu rời đi:

```
Phase 1 (D0-D14):    Effort đã bỏ ra (21 đơn, thời gian học app)
                      ↓
Phase 2 (D15-D60):   + Habit hình thành + Points tích lũy + Service unlocked
                      ↓
Phase 3 (D61-D150):  + Tier R3/R2 (mất = rớt layer) + BH Bronze + Ca structured
                      ↓
Phase 4 (D151-D365): + Full-day Guarantee + Voucher xăng + BH Silver/Gold (MẤT = gia đình mất BH)
                      ↓
Phase 5 (D365+):     + Identity ("Tôi là tài xế Ahamove") + Community role + Mentor status
```

**So sánh:**
- Grab/Be: Switching cost chủ yếu là tiền (promo, incentive) → tài xế chạy theo nền tảng nào thưởng hơn
- Ahamove (đề xuất): Switching cost = **tier + BH + community + identity** → tài xế mất nhiều hơn tiền nếu rời đi

Đây chính là định nghĩa của **Driver Moat** — chiến lược #2 trong 2026 Strategy.

---

## PHẦN 5: ĐỀ XUẤT THAY ĐỔI RANKING PARAMS

### 5.1 Cần Thay Đổi (5 Items)

| # | Thay đổi | Hiện tại | Đề xuất | Owner | Effort |
|:--|:---------|:---------|:--------|:------|:-------|
| 1 | **New Driver flag** | Unranked = 1 nhóm | Tách "New Unranked" (< D60) vs "Performance Unranked" | Product | Low |
| 2 | **New Driver Guarantee 14 ngày** | Không | ≥ 3 đơn/ngày → đảm bảo tối thiểu (phasing D1-D7 cao, D8-D14 -20%) | S&P + Finance | Medium |
| 3 | **BH mở rộng R2** | Chỉ R1, trả bằng pts | Bronze (R2 mới, free) → Silver (R2 stable, free) → Gold (R1, free, gia đình) | DM + HR + BH Partner | High |
| 4 | **Sub-milestone R3→R2** | Ngưỡng 70 và 210 | Thêm 100 stp (R3 Solid) và 150 stp (R3 Plus) làm recognition milestones | Product + DM | Low |
| 5 | **Ca Full-day thử cho R3 Plus** | Full-day chỉ R1+R2 | R3 đạt 150 stp → 1 ca Full-day/tuần, không guarantee | Ops + Product | Medium |

### 5.2 Giữ Nguyên

| Params | Lý do |
|:-------|:------|
| KPI thresholds (DQS, DCR, Productivity) | Align global benchmark. R3=70 phù hợp part-time, R1=280 phù hợp elite |
| Fleet ratio 15/35/35/15 | Kim tự tháp hợp lý |
| Layer cascade 80% fill | Dispatch thông minh |
| AhaPoints formula (GSV÷5000 × multiplier + bonus) | Đơn giản, công bằng |
| Ca 4h + Full-day structure | Phù hợp thực tế |

---

## PHẦN 6: LỘ TRÌNH TRIỂN KHAI

| Giai đoạn | Timeline | Deliverables | Owner |
|:----------|:---------|:-------------|:------|
| **A. Quick Wins** | T7/2026 | New Driver flag (product) + Newbie Priority Dispatch + Instant Payout miễn phí 30 ngày + Buddy System pilot SGN + Sub-milestone badges (100/150 stp) | Product + DM Ops |
| **B. Foundation** | T7-T8/2026 | New Driver Guarantee 14 ngày + Weekly Quest System + Progressive Service Unlock + EPH Dashboard + Streak System + Community cohort groups | Product + S&P + Finance |
| **C. Insurance Pilot** | T8-T9/2026 | BH Bronze (R2) pilot SGN + Ca Full-day thử cho R3 Plus + Grace Period notifications + Churn alert system theo phase | DM + HR + BH Partner |
| **D. Scale** | T10-T12/2026 | BH Silver (R2 stable) + Gold (R1) rollout + Ambassador & Mentor Program + Performance Optimization Tools + Churn Prediction ML model | DM + Product + BI + DS |

---

## PHẦN 7: NGUỒN THAM KHẢO

### Nền Tảng (15 platforms analyzed)
- **Meituan** — Scoring system thay penalty (2024-2025), 7M riders, Silver/Gold tier. [China Daily](https://www.chinadaily.com.cn/a/202505/28/WS68366831a310a04af22c1eb0.html), [TechNode](https://technode.com/2024/12/30/meituan-addresses-rider-conditions-with-pledge-to-end-delivery-time-penalties-before-2026/)
- **Uber Pro** — Blue/Gold/Platinum/Diamond, +5% fare, tuition, Costco. [Uber.com](https://www.uber.com/us/en/drive/uber-pro/), [Gridwise](https://gridwise.io/blog/uber-pro/uber-pro-what-should-uber-drivers-know/)
- **DoorDash** — Dasher Rewards, Overall Rating composite (0-100), 50-trip onboarding. [DoorDash Blog](https://about.doordash.com/en-us/news/making-dashing-even-better-2024-2025), [Help Center](https://help.doordash.com/dashers/s/article/Overall-Dasher-Rating)
- **Swiggy StepUp** — Tiered insurance Bronze/Silver/Gold, churn 60-70% → 10-15%. [Rest of World](https://restofworld.org/2024/swiggy-health-insurance-quotas/), [SabrangIndia](https://sabrangindia.in/swiggys-tiered-insurance-scheme-for-delivery-fleet-the-inherent-nature-of-the-gig-economy/)
- **Grab** — GrabBenefits 2.0, 14-day Guarantee, Diamond/Sapphire/Ruby/Emerald. [Grab SG](https://www.grab.com/sg/grabdriverbenefits/), [HRD Asia](https://www.hcamag.com/asia/specialisation/benefits/grab-expands-benefits-to-support-drivers-welfare/508617)
- **Gojek** — GoalBetter (SG) Classic/Premium/Pro/Elite, GoPartner (ID), fuel rebate 37%. [Gojek SG](https://www.gojek.com/sg/blog/goalbetter-tier-2025)
- **Deliveroo** — BH tai nạn miễn phí tất cả riders, pay floor £12.30+/h. [Deliveroo UK](https://rider.deliveroo.co.uk/support/insurance/what-is-covered-by-deliveroo-insurance)
- **Rappi** — RappiPay wallet + credit card + savings + micro-lending. [Contrary Research](https://research.contrary.com/company/rappi)
- **iFood** — Support Points (trạm nghỉ), 760K riders, 45K e-bikes 2027. [Harvard D3](https://d3.harvard.edu/platform-digit/submission/ifood-delivers-great-results-in-brazil-going-beyond-connecting-restaurants-with-customers/)

### Nghiên Cứu Hàn Lâm
- Zwettler et al. (2024) — [Career Learning Cycle of Gig Workers](https://journals.sagepub.com/doi/10.1177/10690727231212188), Journal of Career Assessment, SAGE
- Selcuk & Gokpinar (2025) — [Incentivizing Flexible Workers](https://journals.sagepub.com/doi/10.1177/10591478251403250), M&SOM, SAGE
- Allon et al. (2019) — [Behavioral and Economic Drivers](https://mackinstitute.wharton.upenn.edu/wp-content/uploads/2020/11/FP0438_WP_2019Oct.pdf), Wharton/Mack Institute
- Abraham et al. (2024) — [Driving the Gig Economy](https://www.nber.org/system/files/working_papers/w32766/w32766.pdf), NBER
- Lally et al. (2010) — How are habits formed, UCL (66-day average)
- Deci & Ryan — Self-Determination Theory (Autonomy, Competence, Relatedness)
- Fogg — Tiny Habits (Motivation × Ability × Prompt)
- Rusbult — Investment Model of Commitment
- Kahneman — Loss Aversion (mất gây đau 2x)
- Erikson — Generativity in adult development

---

*Driver Management Team | Ahamove | 02/06/2026*
*Proposal: Driver Journey v4.0 — 5 Phase × 25 Milestones*
*Cross-reference: `2026-05-driver-ranking-params.html` · `2026-06-global-driver-lifecycle-benchmark.md` · `2026-06-driver-journey-milestones.md`*
