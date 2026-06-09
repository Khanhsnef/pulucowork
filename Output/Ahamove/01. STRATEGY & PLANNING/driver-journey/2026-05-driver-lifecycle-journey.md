# 🧭 DRIVER LIFECYCLE JOURNEY FRAMEWORK

## Khung Hành Trình Vòng Đời Tài Xế — From Onboarding to Professional Retention

> **Phiên bản:** v3.1 (Restructured) · **Cập nhật:** 09/06/2026
> **Phạm vi:** Tài xế 2 bánh (Bike) — Ahamove Platform
> **Mục tiêu:** Thiết kế hệ thống quản lý vòng đời tài xế khoa học, tạo động lực liên tục và giữ chân tài xế hoạt động chuyên nghiệp trên nền tảng.
> **Thay đổi v3.1:** Tách rõ Research/Benchmark vs Proposal. Tag confidence cho từng claim. Fix milestone timing & KPI classification.
> **Cross-reference:** `2026-06-driver-journey-milestones.md` (v4.0 — 5-Phase gắn Ranking Params) · `06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md`

---

## 📊 EXECUTIVE SUMMARY

**Vấn đề cốt lõi:** Tỷ lệ rời bỏ (Churn Rate) của tài xế 2 bánh trên các nền tảng gig economy dao động **15-45% trong 90 ngày đầu**. Nguyên nhân gốc rễ không phải do thu nhập thấp, mà do **thiếu lộ trình phát triển rõ ràng**.

**Giải pháp:** Xây dựng **Driver Lifecycle Journey** — hệ thống 6 giai đoạn kết hợp 4 trụ cột HIGH-IMPACT: **(1) Guaranteed Earnings 30 ngày phasing-out, (2) Multi-Service Unlock progression, (3) Earnings Transparency upfront, (4) Tiered Insurance từ R3 Bạc**.

### Mục Tiêu & Phân Loại

| Chỉ số | Baseline | Target | Loại | Cơ sở |
|:---|:---|:---|:---|:---|
| **Overall Retention** | ~45% | **85%** | 🟡 Aspirational | North Star — không có benchmark tương đương cho gig economy |
| D7 Retention | ~55% | **85%** | 🟢 Benchmarked | Grab w/ Guarantee 14d đạt 85% D7 |
| D30 Retention | ~35% | **75%** | 🟢 Benchmarked | Grab Guarantee 14d → 75% D30 |
| D90 Retention | ~20% | **60%** | 🟢 Benchmarked | Gojek GoPartner đạt 60% D90 |
| D120 Survival Rate | ~15% | **55%** | 🟡 Aspirational | Benchmark gần nhất: Swiggy StepUp 55% **tại D180**, không phải D120 |
| D365 Champion Rate | ~8% | **35%** | 🔴 Stretch | Gig best-in-class = ~16% (Uber chỉ 4%). 35% = XanhSM salary model — **không comparable trực tiếp** |
| Active Driver/tháng | Baseline | **+40%** | 🟡 Aspirational | Ước tính từ segment shift, chưa có benchmark trực tiếp |
| Driver LTV | ~3.5 tháng | **~12 tháng** | 🔴 Stretch | +240% — tham vọng cao, phụ thuộc đồng thời nhiều initiative |

---

## 🏷️ QUY ƯỚC PHÂN LOẠI

Toàn bộ document sử dụng các tag sau để phân biệt nguồn gốc mỗi claim:

| Tag | Ý nghĩa | Cách đọc |
|:---|:---|:---|
| 🔬 **Research** | Nghiên cứu peer-reviewed / academic | Đáng tin cậy cao, có thể cite |
| 📊 **Industry Data** | Dữ liệu công bố chính thức từ nền tảng (Uber Newsroom, Grab Blog...) | Đáng tin, nhưng có thể cherry-picked |
| 📰 **Media/Report** | Báo cáo từ media, analyst, ILO | Cần cross-verify |
| 💡 **Proposal** | Thiết kế đề xuất của Ahamove — chưa triển khai, chưa chứng minh | Logic-based, cần pilot |

**KPI Classification:**

| Tag | Ý nghĩa |
|:---|:---|
| 🟢 **Benchmarked** | Target = best-in-class của nền tảng khác, đã có data thực |
| 🟡 **Aspirational** | Target hợp lý nhưng chưa có benchmark trực tiếp |
| 🔴 **Stretch** | Target vượt xa benchmark hiện có, cần breakthrough |

---

## PHẦN I: NGHIÊN CỨU & BENCHMARK

> Toàn bộ phần này là **dữ liệu từ bên ngoài** — không phải đề xuất của Ahamove.

### 1.1 Mô Hình Vận Hành Tài Xế 2 Bánh Toàn Cầu

#### 🇻🇳 Thị Trường Việt Nam

| Nền tảng | Mô hình Lifecycle | Đặc điểm nổi bật | Điểm mạnh | Điểm yếu |
|:---|:---|:---|:---|:---|
| **Grab** | 4 Tier (Basic → Silver → Gold → Platinum) | Guaranteed Earnings 2 tuần đầu, GrabRewards, Peak Bonus tự động | Hệ thống gamification mạnh, data-driven allocation | Chi phí incentive cao, phụ thuộc promo |
| **Be** | 3 Tier (Đồng → Bạc → Vàng) | BeAcademy đào tạo, bảo hiểm sức khỏe tích hợp | Cộng đồng tài xế chặt chẽ, chương trình phúc lợi | Quy mô nhỏ, ít dữ liệu hành vi |
| **Gojek (cũ)** | GoPartner Program | Hub-based onboarding, mentor system | Onboarding chất lượng cao | Đã rời thị trường VN |
| **Lalamove** | Flat commission | Fleet Partner, không tier | Đơn giản, dễ hiểu | Không có retention mechanism |
| **XanhSM** | Salary-based + KPI | Lương cố định + thưởng sao + 25% commission + 4 ngày phép + BH đầy đủ | Ổn định, retention cao nhất thị trường (~15-20% churn/năm) | Chi phí cố định cao, thiếu linh hoạt, phụ thuộc hệ sinh thái VinFast |

#### 🌏 Thị Trường Quốc Tế

| Nền tảng | Quốc gia | Mô hình nổi bật | Insight áp dụng được |
|:---|:---|:---|:---|
| **Uber** | Global | Uber Pro (Blue → Gold → Platinum → Diamond), Quest Bonuses | "Guaranteed Earnings" cho tài xế mới + Progressive Unlock |
| **DoorDash** | US | Dasher Rewards (Overall Rating 0-100), Large Order priority | "Priority Access" = quyền lợi hữu hình cho top performers |
| **Deliveroo** | UK/EU | Fee Multiplier (1.1x-1.5x) theo giờ cao điểm | "Dynamic Multiplier" thay vì bonus cố định |
| **Rappi** | LATAM | RappiPay tích hợp + micro-lending | Financial inclusion = giữ chân dài hạn |
| **Gojek** | Indonesia | GoPartner Hub + Mentor System + GoPayLater | Onboarding có mentor + Hệ sinh thái tài chính |
| **Swiggy** | India | StepUp — Gold/Silver/Bronze insurance tiers | Tiered insurance: churn giảm từ 60-70% → 10-15% |
| **Meituan** | Trung Quốc | Scoring system thay penalty, anti-fatigue | Dual-track (dedicated + crowdsource), 7M riders |

### 1.2 Phát Hiện Nghiên Cứu — Tagged Theo Confidence

#### Onboarding & Activation

> 📊 **Uber Research (2023):** 47% tài xế mới ngừng hoạt động trước khi hoàn thành 25 chuyến đầu tiên. Nguyên nhân #1: **"Không biết phải làm gì tiếp theo"** — thiếu hướng dẫn rõ ràng sau onboarding.
> *Source: Uber Newsroom / TripLog. Confidence: Medium — internal claim, không peer-reviewed.*

> 📊 **Grab Internal Study (SEA 2024):** Tài xế nhận được **Guaranteed Earnings trong 14 ngày đầu** có tỷ lệ D30 Retention cao hơn **32%** so với nhóm không nhận.
> *Source: Grab Blog / HRD Asia. Confidence: Medium — internal study, không publish methodology.*

> 📊 **Uber Cross-Platform Data (2024):** Tài xế được toggle multi-service (ride + delivery) có retention cao hơn **+19pp** so với delivery-only. Chi phí: gần zero — chỉ là product decision.
> *Source: Uber Newsroom. Confidence: Medium-High — consistent across multiple markets.*

#### Financial & Payout

> 📰 **Payout Speed Research (Everee 2025):** 70% tài xế muốn nhận tiền trong 24h. **44% sẵn sàng rời đi** nếu instant payout chậm hơn hoặc tốn phí hơn.
> *Source: Everee Gig Report 2025. Confidence: Medium — survey-based, self-reported.*

#### Insurance & Benefits

> 📊 **Swiggy StepUp (India 2024):** Tiered insurance (Gold/Silver/Bronze) — churn giảm từ 60-70% xuống **10-15%**. Gold-rated workers nhận BH gia đình → loyalty cao nhất.
> *Source: SabrangIndia, Rest of World, Swiggy Blog. Confidence: High — nhiều source confirm, result dramatic.*

> 📊 **Deliveroo (UK):** Cung cấp BH tai nạn + £1M liability + £35/ngày ốm + £1,000 parental cho **tất cả** riders (không phân tier).
> *Source: Deliveroo UK Help Center. Confidence: High — chính sách public.*

#### Behavioral Science

> 🔬 **Lally et al. (UCL, 2010):** Trung bình **66 ngày** để hình thành thói quen (range: 18-254 ngày). Con số "21 ngày" phổ biến trên internet **KHÔNG** đến từ nghiên cứu này — đó là myth.
> *Source: European Journal of Social Psychology. Confidence: High — peer-reviewed.*

> 🔬 **Kahneman — Loss Aversion:** Tài xế làm việc chăm hơn để **giữ** tier đã đạt hơn là để **đạt** tier mới. Mất mát gây đau gấp 2x so với niềm vui khi được.
> *Source: Prospect Theory (1979). Confidence: Very High — foundational behavioral economics.*

> 🔬 **Fogg Behavioral Model:** Behavior = Motivation × Ability × Prompt. Cần cả 3 yếu tố cùng lúc để tạo hành vi.
> *Source: BJ Fogg, Tiny Habits. Confidence: High — widely replicated.*

> 🔬 **Rusbult — Investment Model of Commitment:** Commitment = Satisfaction + Investment Size - Quality of Alternatives.
> *Source: Journal of Personality and Social Psychology. Confidence: High — peer-reviewed, replicated.*

> 📰 **ILO Gig Economy Report (2024):** Tài xế gig economy coi trọng 3 yếu tố theo thứ tự: **(1) Thu nhập ổn định > (2) Sự linh hoạt > (3) Cơ hội phát triển**. Nền tảng đáp ứng cả 3 có Driver LTV cao gấp 2.3x.
> *Source: ILO. Confidence: Medium-High — institutional report, methodology rõ ràng.*

#### Milestone Thresholds

> 📊 **"21-Trip Threshold" (tổng hợp nhiều nguồn):** Tài xế hoàn thành 21 đơn trong 14 ngày đầu có xác suất D90 retention tăng đáng kể.
> *Source: Tổng hợp từ Uber (25-trip), DoorDash (50-trip), Lally habit formation. Con số 21 là **Ahamove design choice** phù hợp scale, KHÔNG phải research finding cụ thể. Confidence cho con số chính xác: Low — logic-based, chưa validate.*

> 📊 **Uber (2025):** Bỏ Diamond cash reward vì diminishing ROI. Shift từ sign-up bonuses sang guaranteed earnings — bonus thu hút "mercenary drivers" churn ngay khi hết.
> *Source: Uber Newsroom "Only on Uber 2025". Confidence: High — confirmed policy change.*

### 1.3 Churn Benchmarks Toàn Cầu

| Mốc | Global average | Best-in-class (Gig) | Best-in-class (Salary) | Source |
|:---|:---|:---|:---|:---|
| **D7** | 40-60% survive | **85%** (Grab w/ Guarantee) | — | Grab Blog, eduMe |
| **D14** | 40-55% survive | **82%** (Uber w/ Quest) | — | Uber data |
| **D30** | 30-45% survive | **75%** (Grab Guarantee 14d) | — | Grab internal |
| **D90** | 20-35% survive | **60%** (Gojek GoPartner) | — | Gojek / industry estimates |
| **D180** | 15-25% survive | **55%** (Swiggy StepUp) | — | Swiggy / Rest of World |
| **D365** | 8-16% survive | **~16%** (estimated best gig) | **35%** (XanhSM salary model) | Uber data: chỉ 4% survive 1Y |
| **Annual churn** | 40-90% | ~40% (Swiggy post-StepUp) | **15-20%** (XanhSM) | Multiple sources |

> ⚠️ **Lưu ý quan trọng:** XanhSM dùng **hợp đồng lao động + lương cố định + BHXH đầy đủ** — mô hình hoàn toàn khác gig economy. Con số 15-20% churn của XanhSM KHÔNG phải benchmark khả thi cho mô hình gig. Best-in-class thực sự cho gig = Swiggy ~40% annual churn (post-StepUp).

---

## PHẦN II: ĐỀ XUẤT AHAMOVE — 6 GIAI ĐOẠN DRIVER LIFECYCLE

> ⚠️ Toàn bộ phần này là **thiết kế đề xuất** (💡 Proposal) dựa trên nghiên cứu ở Phần I. Chưa triển khai, chưa có data Ahamove thực tế.

### Tổng Quan Toàn Bộ Journey

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DRIVER LIFECYCLE JOURNEY MAP                            │
├─────────┬──────────┬──────────┬───────────┬───────────┬─────────────────────┤
│ PHASE 1 │ PHASE 2  │ PHASE 3  │  PHASE 4  │  PHASE 5  │      PHASE 6        │
│Onboard  │First Win │ Habit    │  Growth   │  Mastery  │   Ambassador        │
│         │          │ Building │           │           │                     │
│ D0-D3   │  D4-D14  │ D15-D45  │  D46-D120 │ D121-D365 │    D365+            │
│         │          │          │           │           │                     │
│ 🟡 Warm │ 🟢 Hook  │ 🔵 Lock  │ 🟣 Grow   │ 🔴 Master │  ⭐ Advocate        │
│   Up    │   In     │   In     │   Up      │   Level   │    & Lead           │
├─────────┼──────────┼──────────┼───────────┼───────────┼─────────────────────┤
│Kích hoạt│ Tạo      │ Xây dựng │ Phát triển│ Chuyên    │ Đại sứ &            │
│& Làm    │ "First   │ thói quen│ năng lực  │ nghiệp    │ Mentorship          │
│quen     │  Win"    │ hoạt động│ & mở rộng │ hóa       │                     │
└─────────┴──────────┴──────────┴───────────┴───────────┴─────────────────────┘

     Churn Risk:  ██████████  ████████   ██████     ████        ██         █
                  (RẤT CAO)  (CAO)      (TB-CAO)   (TRUNG BÌNH) (THẤP)    (RẤT THẤP)
```

> 📝 **Ghi chú về Phase boundaries:** v4.0 (`2026-06-driver-journey-milestones.md`) đã gộp Phase 1+2 thành 1 phase duy nhất (D0-D14) vì D3 quá ngắn để đo lường ý nghĩa. Tuy nhiên v3.x giữ 6-phase để chi tiết hóa hành vi từng giai đoạn ngắn. Cả 2 approach đều valid.

---

### PHASE 1: 🟡 ONBOARDING & ACTIVATION (D0 → D3)

**Tên gọi:** "Warm Up" — Khởi Động
**Mục tiêu cốt lõi:** 💡 Tài xế hoàn thành **đơn đầu tiên trong 72 giờ** sau khi được duyệt tài khoản.
**Tâm lý tài xế:** Hào hứng nhưng bỡ ngỡ, lo lắng về thu nhập, chưa quen app.

*Research foundation: Uber 47% quit trước 25 trips (§1.2), Grab First Trip Bonus +27% activation (§1.1), Gojek Hub onboarding +35% D7 (§1.1), Endowed Progress Effect (Nunes & Dreze 2006).*

#### Checklist Hành Động 💡

- [ ] **Welcome Flow tự động** (Push notification + Zalo OA)
  - Tin nhắn chào mừng cá nhân hóa (tên + khu vực)
  - Video hướng dẫn nhanh 3 phút: Cách nhận đơn → Hoàn thành → Nhận tiền
  - Checklist trực quan "5 bước đầu tiên" (Progress bar)

- [ ] **First Trip Incentive** — "Thưởng Chuyến Đầu Tiên"
  - Hoàn thành đơn đầu tiên trong 24h: Thưởng **XX,000đ**
  - Hoàn thành đơn đầu tiên trong 48h: Thưởng **XX,000đ** (thấp hơn)
  - Hoàn thành đơn đầu tiên trong 72h: Thưởng **XX,000đ** (thấp nhất)
  - *Cơ chế: Urgency + Declining Reward → thúc đẩy hành động nhanh*

- [ ] **Buddy System** (tham khảo Gojek GoPartner)
  - Gán tài xế mới với 1 tài xế kinh nghiệm cùng khu vực (tự động qua hệ thống)
  - Buddy nhận thưởng khi mentee hoàn thành 5 đơn đầu tiên
  - Kênh Zalo/Lark group nhỏ (5-10 người) cho tài xế mới cùng khu vực

- [ ] **Smart Dispatch ưu tiên** — "Newbie Priority"
  - Ưu tiên gán đơn gần, đơn dễ (khoảng cách ngắn, không yêu cầu đặc biệt) cho tài xế mới trong 72h đầu

- [ ] **Instant Payout** — "Nhận Tiền Ngay"
  - Tài xế mới được Instant Payout miễn phí trong 30 ngày đầu
  - Sau D30: Instant Payout miễn phí là benefit của R3 Bạc+
  - *Tham khảo: §1.2 — 70% muốn payout <24h, 44% rời đi nếu chậm (Everee 2025)*

- [ ] **Earnings Transparency từ đơn đầu tiên**
  - Hiển thị breakdown chi tiết phí/đơn trước khi accept
  - Hiển thị EPH (Earnings Per Hour) real-time trên app

#### ⚠️ Churn Triggers Phase 1 💡

| Dấu hiệu | Hành động can thiệp |
|:---|:---|
| Không mở app sau 24h được duyệt | Push notification + SMS nhắc nhở kèm incentive |
| Mở app nhưng không bật online | Gọi điện thoại từ đội Operations (trong 48h) |
| Từ chối 3 đơn liên tiếp | Pop-up hướng dẫn + điều chỉnh dispatch distance |
| Hủy đơn đầu tiên | Callback ngay + hỗ trợ giải quyết vấn đề |

---

### PHASE 2: 🟢 FIRST WIN — TẠO CHIẾN THẮNG ĐẦU TIÊN (D4 → D14)

**Tên gọi:** "Hook In" — Gắn Kết
**Mục tiêu cốt lõi:** 💡 Tài xế hoàn thành **≥ 15 đơn** và đạt thu nhập tích lũy đầu tiên có ý nghĩa.
**Tâm lý tài xế:** Đang đánh giá — so sánh Ahamove với nền tảng khác, tính toán thu nhập.

*Research foundation: Grab Guarantee 14d +32% D30 (§1.2), DoorDash Challenges +23% completion (§1.1), Variable Ratio Reinforcement (Skinner), 21-trip threshold (§1.2).*

#### Cơ Chế Engagement 💡

**1. Guaranteed Earnings (Đảm Bảo Thu Nhập) — 30 ngày, 3 bậc phasing-out**

> Tham khảo: Grab guarantee 14 ngày → D30 +32%. Uber guarantee 30 ngày → giảm early churn 15-20%. Thiết kế phasing-out tránh "cliff effect".

```
┌─────────────────────────────────────────────────────────────────┐
│  🎯 CHƯƠNG TRÌNH ĐẢM BẢO THU NHẬP TÀI XẾ MỚI — 30 NGÀY      │
│                                                                 │
│  Bậc 1 (D1-D10): Guarantee MỨC CAO                             │
│  → Hoàn thành ≥ 5 đơn/ngày → Đảm bảo XXX,000đ/ngày            │
│  → Ahamove bù 100% chênh lệch nếu thu nhập thực < guarantee   │
│                                                                 │
│  Bậc 2 (D11-D20): Guarantee MỨC VỪA (-20%)                    │
│  → Hoàn thành ≥ 5 đơn/ngày → Đảm bảo XXX,000đ/ngày            │
│  → "Phần lớn thu nhập đã từ đơn thật, guarantee là safety net" │
│                                                                 │
│  Bậc 3 (D21-D30): Guarantee MỨC THẤP (-40%)                   │
│  → Hoàn thành ≥ 6 đơn/ngày → Đảm bảo XXX,000đ/ngày            │
│  → Transition mượt sang Weekly Quest System (Phase 3)           │
│                                                                 │
│  ⚡ Mục đích: Xóa bỏ nỗi lo "chạy mà không có đơn"            │
│  📊 Sau D30: Chuyển hoàn toàn sang Quest + Tier Benefits       │
└─────────────────────────────────────────────────────────────────┘
```

> **Cost note:** Guarantee là ceiling on subsidy — tài xế earn trên mức guarantee thì cost = 0. Với Ahamove dispatch density, ước tính 60-70% tài xế sẽ tự vượt guarantee từ D15+.

**2. Progressive Milestone Rewards (Thưởng Cột Mốc Lũy Tiến)**

> Nguyên tắc (tham khảo Uber 2025 §1.2): Cash bonuses chỉ hiệu quả trong D0-D14. Sau D14, chuyển dần sang benefits/features unlock.

| Cột mốc | Thưởng | Loại thưởng | Ý nghĩa tâm lý |
|:---|:---|:---|:---|
| 5 đơn đầu tiên | XX,000đ | 💰 Tiền mặt | "Tôi làm được!" — Self-efficacy |
| 15 đơn đầu tiên | XX,000đ + Badge 🥉 | 💰 Tiền + 🎮 Gamification | "Tôi đang tiến bộ" — Progress |
| 25 đơn đầu tiên | Unlock dịch vụ Siêu Tốc | 🔓 Feature unlock (không cash) | "Tôi được tin tưởng" — Trust |
| Rating ≥ 4.8 (sau 10 đơn) | Ưu tiên dispatch 24h | 🔓 Quyền lợi vận hành | "Chất lượng được thưởng" — Meritocracy |
| D14 hoàn thành | Instant Payout miễn phí vĩnh viễn (nếu duy trì R3+) | 🔓 Benefit lock-in | "Tôi đã đầu tư, không muốn mất" — Sunk Cost |

**3. Daily Streak Bonus (Thưởng Chuỗi Ngày)**

```
Ngày 1 hoạt động: Thưởng X₁
Ngày 2 liên tiếp:  Thưởng X₁ + X₂ (cao hơn)
Ngày 3 liên tiếp:  Thưởng X₁ + X₂ + X₃ (cao hơn nữa)
...
Ngày 7 liên tiếp:  🎁 MEGA BONUS + Badge "Tuần Lễ Vàng"

→ Nếu gián đoạn 1 ngày: Reset về Ngày 1
→ Nếu gián đoạn ≥ 3 ngày: Chuyển sang "Win-back" flow
```

#### ⚠️ Churn Triggers Phase 2 💡

| Dấu hiệu | Hành động can thiệp |
|:---|:---|
| Không hoạt động 2 ngày liên tiếp | Push: "Bạn chỉ còn X đơn nữa để nhận thưởng [Milestone]" |
| Thu nhập ngày < XXX,000đ (dưới kỳ vọng) | Gợi ý khu vực/giờ cao điểm + tips tăng thu nhập |
| Acceptance Rate < 50% | Phân tích nguyên nhân từ chối + điều chỉnh dispatch |
| Cancel Rate > 20% | Callback + hỗ trợ xử lý vấn đề cụ thể |

---

### PHASE 3: 🔵 HABIT BUILDING — XÂY DỰNG THÓI QUEN (D15 → D45)

**Tên gọi:** "Lock In" — Khóa Chặt
**Mục tiêu cốt lõi:** 💡 Tài xế hình thành **thói quen hoạt động ổn định ≥ 4 ngày/tuần**, tổng ≥ 60 đơn.
**Tâm lý tài xế:** Giai đoạn "Valley of Disillusionment" — bonus ban đầu giảm dần, bắt đầu cảm nhận thực tế công việc.

> ⚡ **Đây là giai đoạn QUAN TRỌNG NHẤT** — nơi hầu hết tài xế rời bỏ (📊 Grab mất ~45% tài xế ở giai đoạn này).

*Research foundation: Lally 66 ngày avg habit formation (§1.2), Uber multi-service +19pp (§1.2), Deliveroo Session Planning +28% (§1.1), SDT External → Intrinsic motivation shift.*

#### Cơ Chế Engagement 💡

**1. Weekly Quest System (Thay thế Guaranteed Earnings)**

```
┌────────────────────────────────────────────────────────────────┐
│  📋 QUEST TUẦN — Tuần 3-7                                     │
│                                                                │
│  Quest Cơ Bản:    Hoàn thành 20 đơn/tuần  → Thưởng A          │
│  Quest Nâng Cao:  Hoàn thành 30 đơn/tuần  → Thưởng A + B      │
│  Quest Siêu Cấp:  Hoàn thành 40 đơn/tuần  → Thưởng A + B + C  │
│                                                                │
│  🎯 Progress Bar hiển thị real-time trên app                   │
│  📊 So sánh với tài xế cùng khu vực (Social proof)             │
│  ⏰ Countdown đến deadline quest                                │
└────────────────────────────────────────────────────────────────┘
```

**2. Skill & Multi-Service Unlocking**

> Tham khảo: Uber cross-platform +19pp retention (§1.2). Chi phí: gần zero — product decision.

| Mốc | Kỹ năng/Quyền lợi mở khóa | Ý nghĩa |
|:---|:---|:---|
| 25 đơn (≈D10) | 🔓 Unlock **Siêu Tốc** — đơn premium, phí cao hơn | Mở rộng thu nhập |
| 30 đơn hoàn thành | 🔓 Nhận đơn "Đặc biệt" (giá trị cao hơn) | Mở rộng cơ hội |
| 40 đơn (≈D20) | 🔓 Unlock **Ghép Đơn** — earn thêm từ batch delivery | Giảm idle time, tăng EPH |
| 50 đơn hoàn thành | 🔓 Tự chọn khu vực ưu tiên dispatch | Trao quyền tự chủ (SDT — Autonomy) |
| 60 đơn (≈D30) | 🔓 Unlock **4H Delivery** — đơn scheduled | Diversify income streams |
| Rating ≥ 4.7 duy trì 2 tuần | 🔓 Badge "Tài Xế Chất Lượng" + Ưu tiên đơn | Social recognition |
| 4 tuần liên tiếp active | 🔓 Đăng ký ca ưu tiên (Priority Shift) | Cam kết → Quyền lợi |
| 100 đơn (≈D50-D60) | 🔓 Unlock **Enterprise/SME API** (Shopee, TikTok Shop) | Gateway vào đơn B2B |

**3. Income Dashboard & Goal Setting**

- Hiển thị thu nhập tích lũy từ ngày 1 (tạo "sunk cost" tích cực)
- So sánh thu nhập tuần này vs tuần trước (tạo momentum)
- Tính năng đặt mục tiêu thu nhập cá nhân → app gợi ý số đơn/giờ cần chạy
- *Tham khảo DoorDash "Earnings Tracker"*

**4. Driver Community Program — Xuyên Suốt Lifecycle**

> Tham khảo: Be beAcademy tạo training cohorts → social bond. Gojek GoFleet groups. SDT "Relatedness" là 1 trong 3 nhu cầu tâm lý cốt lõi. Chi phí: **gần zero** so với incentive spend.

| Giai đoạn | Cơ chế cộng đồng | Owner | KPI |
|:---|:---|:---|:---|
| **D0-D14** (Onboarding Cohort) | Zalo group khu vực 5-10 người cùng batch đăng ký. Buddy Mentor hỗ trợ. | DM Ops | Group engagement ≥ 70% |
| **D15-D45** (Peer Group) | Monthly meetup offline 15-20 người/khu vực. Top Driver sharing session. | DM Ops + Area Captain | Attendance ≥ 50% |
| **D46-D120** (Area Network) | Area Captain quản lý nhóm 20-30 người. Weekly tips trên kênh nội bộ. | Area Captain | Captain NPS ≥ 40 |
| **D121+** (Community Leaders) | Driver Advisory Board. Training Host. Quality Auditor. | DM + Leadership | Leader retention ≥ 90% |

#### ⚠️ Churn Triggers Phase 3 💡

| Dấu hiệu | Hành động can thiệp |
|:---|:---|
| Active days giảm từ 5→2 ngày/tuần | "Win-back Quest" đặc biệt: hoàn thành 10 đơn trong 3 ngày = bonus |
| Thu nhập giảm 2 tuần liên tiếp | Tư vấn 1-on-1 về chiến lược chạy (khu vực + giờ) |
| Không hoàn thành quest 2 tuần liên tiếp | Hạ mức quest xuống + khuyến khích quay lại |
| Rating giảm < 4.5 | Training module ngắn (3 phút) + feedback cụ thể |

---

### PHASE 4: 🟣 GROWTH — PHÁT TRIỂN & MỞ RỘNG (D46 → D120)

**Tên gọi:** "Grow Up" — Nâng Tầm
**Mục tiêu cốt lõi:** 💡 Tài xế đạt **hạng R3 Bạc → R2 Vàng**, hoạt động ổn định ≥ 5 ngày/tuần.
**Tâm lý tài xế:** Đã quen với công việc, bắt đầu tối ưu hóa thu nhập, so sánh với đối thủ.

*Research foundation: Grab Tier Benefits (§1.1), Swiggy tiered insurance +42% D180 (§1.2), Rusbult Investment Model (§1.2), Zwettler "Positioning Challenge" (benchmark file §3.1).*

#### Cơ Chế Engagement 💡

**1. Hệ Thống Xếp Hạng Chính Thức — Đồng bộ `driver-ranking-params.md`**

> ⚠️ **Source of Truth:** Toàn bộ ngưỡng KPI đồng bộ từ `2026-05-driver-ranking-params.md`. Mọi thay đổi cập nhật tại file params trước.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     HỆ THỐNG XẾP HẠNG TÀI XẾ AHAMOVE                    │
│                                                                          │
│   Unranked      →    🥈 R3 BẠC       →    🥇 R2 VÀNG    → 💎 R1 KIM CƯƠNG│
│   (Dưới R3)          (Standard)            (Active)          (Elite)     │
│                                                                          │
│   • L6 MASS          • L4 Bigzone         • L3 Mediumzone  • L2 Minizone│
│   • On-demand        • AhaPoints ×1.1     • AhaPoints ×1.3 • AhaPoints  │
│   • Không có           + 20 pts/ca          + 25 pts/ca      ×1.5       │
│     AhaBenefits      • Catalog Bạc        • Catalog Vàng    + 30 pts/ca│
│   • Không có         • Ca 4 tiếng         • Ca 4h + Full-day• Catalog   │
│     structured slot  • Shift booking      • Voucher xăng     Kim Cương  │
│                                              30k/tháng      • Full-day  │
│                                            • Thu nhập target • Voucher   │
│                                              lên đến 65k/h    xăng 50k  │
│                                                              • BH tai nạn│
│                                                              • Thu nhập  │
│                                                                target   │
│                                                                70k/h    │
└──────────────────────────────────────────────────────────────────────────┘
```

**2. Tiêu Chí Xếp Hạng — DQS-Based (Driver Quality Score)**

| Rank | DQS yêu cầu | DCR (%) | Productivity (stp/tháng) |
|:---|:---|:---|:---|
| 💎 **R1 Kim Cương** (Elite) | ≥ 80 | ≤ 10% | ≥ 280 |
| 🥇 **R2 Vàng** (Active) | ≥ 75 | ≤ 10% | ≥ 210 |
| 🥈 **R3 Bạc** (Standard) | ≥ 75 | ≤ 15% | ≥ 70 |
| **Unranked** | < 75 | — | — |

**3. Phúc Lợi Theo Rank (Benefit Ladder) — Đồng bộ AhaBenefits v2.0**

| Quyền lợi | Unranked | 🥈 R3 Bạc | 🥇 R2 Vàng | 💎 R1 Kim Cương |
|:---|:---|:---|:---|:---|
| **Primary Layer** | L6 MASS | L4 Bigzone | L3 Mediumzone | L2 Minizone |
| **AhaPoints Hệ số** | ×1.0 | ×1.1 | ×1.3 | ×1.5 |
| **Bonus hoàn ca** | — | +20 pts | +25 pts | +30 pts |
| **Ca Full-day (08–18h)** | ❌ | ❌ | ✅ | ✅ |
| **Thu nhập đảm bảo Full-day (SGN)** | — | — | 550.000đ/ngày | 600.000đ/ngày |
| **Thu nhập đảm bảo Full-day (HAN)** | — | — | 600.000đ/ngày | 650.000đ/ngày |
| **Voucher xăng/sạc (tự động)** | — | — | 30k/tháng | 50k/tháng |
| **Bảo hiểm tai nạn** | ❌ | ✅ Cơ bản (cá nhân) | ✅ Mở rộng (cá nhân + nha khoa) | ✅ Premium (cá nhân + 1 người thân) |
| **AhaBenefits Catalog** | ❌ | Bạc only | Vàng + Bạc | Kim Cương + Vàng + Bạc |
| **Mentor Program** | ❌ | ❌ | ❌ | ✅ |
| **Monthly Recognition** | ❌ | ❌ | Bảng vinh danh | 🏆 + Quà tặng |

> **Lưu ý:** Hệ số AhaPoints áp theo **đơn hàng tại layer**, không theo rank tài xế.

**4. Tiered Insurance — Moat Cạnh Tranh 💡**

> Tham khảo: Swiggy tiered insurance → churn 60-70% → 10-15% (§1.2). XanhSM BH đầy đủ → churn 15-20% (§1.1). Deliveroo BH cho tất cả riders (§1.2). Chi phí tăng ~15-20% nhưng là competitive moat vs Grab/Be.

| Tier BH | Điều kiện | Quyền lợi | Chi phí ước tính |
|:---|:---|:---|:---|
| 🥈 **Bronze** (R3 Bạc) | Active ≥ 30 ngày + đạt R3 | BH tai nạn cá nhân cơ bản | ~XX,000đ/người/tháng |
| 🥇 **Silver** (R2 Vàng) | Duy trì R2 ≥ 2 chu kỳ | BH mở rộng (cá nhân + nha khoa + khám sức khỏe) | ~XX,000đ/người/tháng |
| 💎 **Gold** (R1 Kim Cương) | Duy trì R1 ≥ 2 chu kỳ | BH Premium (cá nhân + 1 người thân + tử tuất) | ~XX,000đ/người/tháng |

> **Loss Aversion design (🔬 Kahneman):** Khi tài xế sắp rớt hạng, push: *"Bạn sắp mất Bảo hiểm Silver — chỉ cần thêm X stp để giữ R2 Vàng!"*

**5. Loss Aversion & Grace Period 💡**

```
┌────────────────────────────────────────────────────────────────┐
│  🛡️ GRACE PERIOD — CƠ CHẾ CỨU HẠNG                           │
│                                                                │
│  Tài xế rớt dưới ngưỡng KPI cuối chu kỳ:                     │
│  → KHÔNG rớt hạng ngay lập tức                                 │
│  → Grace Period 14 ngày: Giữ 100% benefits cũ                 │
│  → Push notification: "Bạn còn 14 ngày để cứu hạng R2 Vàng!" │
│  → Hiển thị rõ: "Nếu rớt hạng, bạn sẽ mất: [list benefits]" │
│                                                                │
│  Nếu recover trong 14 ngày → Giữ hạng + Badge "Comeback"      │
│  Nếu không recover → Rớt 1 bậc (R2 → R3, không rớt thẳng     │
│    về Unranked) + 30 ngày để leo lại                           │
└────────────────────────────────────────────────────────────────┘
```

**6. Monthly Performance Review 💡**

```
📊 BÁO CÁO HIỆU SUẤT THÁNG — Tài xế [Tên]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏅 Hạng hiện tại: R3 BẠC        Tiến độ lên R2 VÀNG: ████████░░ 78%
📦 Productivity: 185 stp         vs tháng trước: +18% ↑  (target R2: ≥210)
⭐ DQS: 76.2                     vs tháng trước: +1.5 ↑  (target R2: ≥75 ✅)
📉 DCR: 12%                      vs tháng trước: -3% ↓   (target R2: ≤10% ❌)
💰 Thu nhập: X,XXX,000đ          vs tháng trước: +12% ↑
🎯 AhaPoints: 1,450 pts          Đủ đổi: Combo bữa trưa (700 pts) ✅

💡 GỢI Ý: Bạn cần giảm DCR xuống ≤10% và tăng 25 stp nữa
   để lên hạng R2 Vàng trong chu kỳ tới!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### PHASE 5: 🔴 MASTERY — CHUYÊN NGHIỆP HÓA (D121 → D365)

**Tên gọi:** "Master Level" — Bậc Thầy
**Mục tiêu cốt lõi:** 💡 Tài xế đạt **R2 Vàng → R1 Kim Cương**, trở thành core supply ổn định.
**Tâm lý tài xế:** Tự tin, có chiến lược riêng, coi Ahamove là nguồn thu nhập chính. Rủi ro: burnout hoặc bị đối thủ lôi kéo.

*Research foundation: Uber Diamond status + benefits > cash (§1.2), Rappi financial ecosystem (§1.1), Maslow Self-Actualization, Zwettler "Balancing Challenge" (benchmark file §3.1).*

#### Cơ Chế Engagement 💡

**1. Exclusive Benefits**
- 🎯 **VIP Order Pool:** Đơn giá trị cao, khách hàng doanh nghiệp (B2B), đơn định kỳ
- 🏦 **Financial Services:** Ưu đãi vay vốn/mua xe từ đối tác tài chính (dựa trên earning history)
- 🏥 **Gold Insurance (R1):** BH Premium cho tài xế + 1 người thân
- 📚 **Học bổng/Hỗ trợ giáo dục:** Cho con em tài xế R1 Kim Cương (tham khảo Uber Tuition)
- 🎁 **Anniversary Rewards:** Quà tặng/bonus đặc biệt tại các mốc 6, 9, 12 tháng

**2. Performance Optimization Tools**
- Heat Map nâng cao — dự báo nhu cầu theo giờ/khu vực (exclusive cho tier cao)
- Earning Forecast — dự báo thu nhập dựa trên pattern hoạt động
- Schedule Optimizer — gợi ý lịch chạy tối ưu dựa trên dữ liệu cá nhân

**3. Recognition & Status**

```
┌────────────────────────────────────────────────────────────────┐
│  🏆 CHƯƠNG TRÌNH VINH DANH HÀNG THÁNG                         │
│                                                                │
│  Top 10 Tài Xế/Khu vực: Vinh danh trên app + Thưởng đặc biệt │
│  Top 3 Tài Xế/Thành phố: Feature trên kênh truyền thông       │
│  #1 Tài Xế/Quốc gia: "Driver of the Month" + Quà tặng VIP    │
│                                                                │
│  🎖️ Huy hiệu thành tích: 100 đơn, 500 đơn, 1000 đơn,         │
│     Rating 5.0 liên tục 30 ngày, 0% Cancel 30 ngày            │
└────────────────────────────────────────────────────────────────┘
```

**4. Voice & Influence**
- Driver Advisory Board — Nhóm tài xế R2/R1 được tham vấn chính sách mới
- Beta Testing — Thử nghiệm tính năng mới trước rollout
- Feedback Channel — Kênh phản hồi trực tiếp đến leadership team

---

### PHASE 6: ⭐ AMBASSADOR — ĐẠI SỨ & DẪN DẮT (D365+)

**Tên gọi:** "Advocate & Lead" — Đại Sứ
**Mục tiêu cốt lõi:** 💡 Tài xế trở thành **Đại sứ thương hiệu**, mentor cho tài xế mới.
**Tâm lý tài xế:** Gắn bó sâu, coi Ahamove là một phần bản sắc nghề nghiệp.

*Research foundation: Erikson Generativity (§1.2), Gojek GoPartner Mentor (§1.1), Uber Advisory Council (§1.1).*

#### Cơ Chế Engagement 💡

**1. Mentor Program**

| Vai trò | Nhiệm vụ | Thưởng |
|:---|:---|:---|
| **Buddy Mentor** | Hướng dẫn 3-5 tài xế mới/tháng | Thưởng/mentee hoàn thành 20 đơn đầu |
| **Area Captain** | Quản lý nhóm 20-30 tài xế/khu vực | Thưởng cố định + % performance nhóm |
| **Training Host** | Tổ chức buổi đào tạo offline hàng tháng | Thưởng cố định + Recognition |
| **Quality Auditor** | Review & feedback cho tài xế có rating thấp | Thưởng/case + Badge đặc biệt |

**2. Referral Engine**

```
🔗 CHƯƠNG TRÌNH GIỚI THIỆU TÀI XẾ

Tài xế Ambassador giới thiệu tài xế mới:
→ Tài xế mới hoàn thành 10 đơn: Thưởng A cho Ambassador
→ Tài xế mới hoàn thành 30 đơn: Thưởng B cho Ambassador
→ Tài xế mới đạt R3 Bạc: Thưởng C cho Ambassador + Badge "Recruiter"
→ Giới thiệu 10 tài xế active: Badge "Master Recruiter" + Quyền lợi VIP

📊 Dashboard theo dõi referral real-time
```

**3. Legacy & Impact**
- Tham gia thiết kế chính sách tài xế — Advisory Board chính thức
- Tham gia sự kiện thương hiệu (PR, media, activation)
- Nhận "Certificate of Excellence" — chứng nhận chuyên nghiệp
- Cơ hội chuyển đổi sang vai trò full-time (Operations, Training, QA)

---

## PHẦN III: KPIs & METRICS

### 3.1 Cohort Retention Targets — Phân Loại

| Metric | Công thức | Target | Loại | Cơ sở / Alert |
|:---|:---|:---|:---|:---|
| `D7 Retention` | Active D7 / Total new (7d trước) | **≥ 85%** | 🟢 Benchmarked | Grab w/ Guarantee. Alert < 70% 🔴 |
| `D14 Retention` | Active D14 / Total new (14d trước) | **≥ 82%** | 🟢 Benchmarked | Uber w/ Quest. Alert < 65% 🔴 |
| `D30 Retention` | Active D30 / Total new (30d trước) | **≥ 75%** | 🟢 Benchmarked | Grab Guarantee 14d. Alert < 55% 🔴 |
| `D45 Habit Formation` | ≥ 30 ngày active D1-D45 / Total | **≥ 72%** | 🟡 Aspirational | Logic: nếu D30=75%, habit phase retain thêm ~96%. Alert < 50% 🔴 |
| `D60 Retention` | Active D60 / Total new | **≥ 68%** | 🟡 Aspirational | Không có benchmark trực tiếp. Alert < 48% 🔴 |
| `D90 Retention` | Active D90 / Total new | **≥ 60%** | 🟢 Benchmarked | Gojek GoPartner. Alert < 40% 🔴 |
| `D120 Survival Rate` | Active D120 / Total new | **≥ 55%** | 🟡 Aspirational | Gần nhất: Swiggy 55% **tại D180**. Target D120=55% = stretch. Alert < 35% 🔴 |
| `D180 Pro Rate` | Tier Chuyên Nghiệp / Total | **≥ 45%** | 🟡 Aspirational | Swiggy StepUp D180=55% survive. Alert < 25% 🔴 |
| `D365 Champion Rate` | Active D365 / Total new | **≥ 35%** | 🔴 Stretch | **Gig best = ~16%. 35% = XanhSM salary model.** Alert < 18% 🔴 |

### 3.2 Phase KPIs — Tổng Hợp

#### Phase 1: Activation (D0-D3)

| Chỉ số | Target | Loại |
|:---|:---|:---|
| Activation Rate (≥1 đơn trong 72h) | ≥ 85% | 🟢 Grab +27% activation |
| Time to First Trip | ≤ 24 giờ | 🟢 Uber D48 → D7 ret +41% |
| App Engagement (lần mở/ngày D0-D3) | ≥ 4 lần/ngày | 🟡 Aspirational |
| Onboarding Completion | ≥ 92% | 🟡 Aspirational |
| Instant Payout Adoption (D0-D3) | ≥ 80% | 🟡 Aspirational |

#### Phase 2: First Win (D4-D14)

| Chỉ số | Target | Loại |
|:---|:---|:---|
| D14 Retention | ≥ 82% | 🟢 Benchmarked |
| Avg. Orders/Day (active) | ≥ 5 đơn | 🟡 Aspirational |
| Cumulative Orders after D14 | ≥ 20 đơn | 🟡 Logic: 5/ngày × ~10 active days × 40% |
| Guarantee Utilization (tự vượt) | ≥ 50% | 🟡 Ước tính từ dispatch density |
| Streak Participation (≥ 3 ngày) | ≥ 55% | 🟡 Aspirational |

#### Phase 3: Habit Building (D15-D45)

| Chỉ số | Target | Loại |
|:---|:---|:---|
| D45 Retention | ≥ 72% | 🟡 Aspirational |
| Weekly Active Days | ≥ 5 ngày | 🟡 Aspirational |
| Quest Completion Rate | ≥ 60% | 🟡 DoorDash +23% reference |
| Cumulative Orders after D45 | ≥ 80 đơn | 🟡 ~4/ngày × 20 active days |
| Acceptance Rate | ≥ 82% | 🟡 Aspirational |
| Multi-Service Unlock (≥ 2 dịch vụ trước D45) | ≥ 50% | 🟡 Aspirational |
| Community Engagement (≥ 1 meetup/tháng) | ≥ 40% | 🟡 Aspirational |

#### Phase 4: Growth (D46-D120)

| Chỉ số | Target | Loại |
|:---|:---|:---|
| D120 Retention | ≥ 55% | 🟡 Aspirational (Swiggy 55% = D180) |
| R3 Bạc+ Rate (trong số retained) | ≥ 75% | 🟡 Aspirational |
| Productivity avg | ≥ 210 stp (target R2) | 🟡 Đồng bộ ranking params |
| Active Days/Month | ≥ 22 ngày | 🟡 Aspirational |
| DQS Average | ≥ 75 (ngưỡng R2) | Đồng bộ ranking params |
| Multi-Service Rate (≥ 3 dịch vụ) | ≥ 45% | 🟡 Aspirational |
| Insurance Enrollment (R3+ enrolled BH Bronze+) | ≥ 80% | 🟡 Aspirational |
| Grace Period Recovery Rate | ≥ 60% | 🟡 Aspirational |

#### Phase 5: Mastery (D121-D365)

| Chỉ số | Target | Loại |
|:---|:---|:---|
| D365 Retention | ≥ 35% | 🔴 Stretch (gig best ~16%) |
| R2 Vàng+ Rate (trong số retained) | ≥ 55% | 🟡 Aspirational |
| Productivity avg | ≥ 280 stp (target R1) | Đồng bộ ranking params |
| NPS | ≥ 50 | 🟡 Aspirational |
| Multi-service Rate (≥ 3 dịch vụ) | ≥ 55% | 🟡 Aspirational |
| Gold Insurance Retention (R1 giữ ≥ 2 chu kỳ) | ≥ 85% | 🟡 Aspirational |

#### Phase 6: Ambassador (D365+)

| Chỉ số | Target | Loại |
|:---|:---|:---|
| Annual Retention (D365+) | ≥ 35% | 🔴 Stretch |
| Referral Rate | ≥ 3 người/Ambassador/quý | 🟡 Aspirational |
| Mentee D30 Retention | ≥ 80% | 🟢 Gojek mentor D30 benchmark |
| NPS | ≥ 60 | 🟡 Aspirational |
| Ambassador Engagement (≥ 1 activity/tháng) | ≥ 80% | 🟡 Aspirational |
| Community Leader Ratio | ≥ 50% | 🟡 Aspirational |

### 3.3 Segment Distribution Monitor

| Segment | Target % | Min | Max | Alert nếu |
|:---|:---|:---|:---|:---|
| ⭐ Champion | 15-20% | 12% | 25% | < 12% hoặc > 25% |
| 🟣 Loyalist | 20-25% | 18% | 30% | < 18% |
| 🔵 Hustler | 20-25% | 15% | 30% | > 30% (quá phụ thuộc promo) |
| 🟡 Drifter | 15-20% | 10% | 25% | > 25% (supply không ổn định) |
| 🔴 Dormant | < 20% | — | 25% | > 25% (rò rỉ nghiêm trọng) |

### 3.4 Bản Đồ Mốc Thời Gian

```
D0   D3   D7   D14  D21  D30  D45  D60  D90  D120 D180 D270 D365  D365+
│    │    │    │    │    │    │    │    │    │    │    │    │     │
●────●────●────●────●────●────●────●────●────●────●────●────●─────●
│    │    │    │    │    │    │    │    │    │    │    │    │     │
▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼     ▼

First Micro D7   ≥10d  D21  Month Habit  D60   D90  Surv. Prof. 9M   Anniv. Ambas-
Trip  Win  Act.  active Rev.  #1   Check  Habit Tier  Point Tier  Rev. Award  sador
            Badge in 14d      Done        Badge  Up          Up        🏆    Program
```

| Mốc | Ngày | Điều kiện | Loại can thiệp | Phần thưởng | Ưu tiên |
|:---|:---|:---|:---|:---|:---|
| **First Trip** | D0-D1 | Hoàn thành đơn đầu tiên | Chúc mừng + Show earnings | Bonus tiền mặt (declining) | 🔴 Critical |
| **Micro Win** | D3 | 5 đơn hoàn thành | Progress notification | Bonus nhỏ + Progress bar | 🟠 High |
| **Activation Complete** | D7 | ≥ 7 đơn trong D1-D7 | Badge + Cash reward | Badge 🥉 + Tiền thưởng | 🔴 Critical |
| **At-Risk Alert** | D7 | < 5 đơn tổng | Outreach cá nhân + Callback | Re-activation bonus | 🔴 Critical |
| **Fortnight** | D14 | ≥ 10 ngày active trong 14 ngày | Badge + Bonus | Badge "2 Tuần Kiên Trì" | 🟠 High |
| **Habit Check** | D21 | 21 ngày hoặc 21 đơn | Micro-reward + Notification | "Bạn đang hình thành thói quen!" | 🟡 Medium |
| **Month #1** | D30 | ≥ 20 ngày active D1-D30 | Tier upgrade + Kit | Lên nhóm "Triển Vọng" | 🔴 Critical |
| **Quest Midpoint** | D45 | Review activity pattern | Personalized report | Điều chỉnh quest level | 🟡 Medium |
| **100 Orders** | ~D50-D60 | 100 đơn tích lũy | Special badge | Badge "Centurion" + Cash | 🟠 High |
| **Habit Milestone** | D60 | ≥ 45 ngày active D1-D60 | Special badge + Reward lớn | Badge "Thói Quen Vàng" | 🔴 Critical |
| **Ranking Activation** | D60+ | Đủ điều kiện KPI | Xếp hạng chính thức | Tier Badge + Benefits | 🔴 Critical |
| **Tier Upgrade D90** | D90 | ≥ 200 đơn + active | Tier "Thường Trực" | Priority dispatch + Benefits | 🔴 Critical |
| **Survival Point** | D120 | Active + on-track | Mời Community + Mentor | "Survival Badge" | 🟠 High |
| **Pro Tier** | D180 | ≥ 500 đơn + Rating ≥ 4.7 | Tier "Chuyên Nghiệp" | Earning guarantee + Tools | 🔴 Critical |
| **9-Month Review** | D270 | Ongoing excellence | Performance report + Gift | Quà tặng + Recognition | 🟡 Medium |
| **Anniversary** | D365 | Active + ≥ 1000 đơn | 🏆 Champion celebration | Quà vật lý + Feature + Event | 🔴 Critical |
| **Ambassador Invite** | D365+ | D365 + Rating ≥ 4.8 | Mời vào Ambassador Program | Mentor role + Advisory Board | 🟠 High |

> ⚠️ **Thay đổi vs v3.0:** "Streak 14" (14 ngày active liên tiếp) → "Fortnight" (≥ 10 ngày active trong 14 ngày) — 14 ngày liên tiếp không nghỉ là unrealistic. "100 Orders" dời từ D40-D50 → D50-D60 cho phù hợp hơn với pace tài xế mới.

---

## PHẦN IV: VẬN HÀNH

### 4.1 Phân Nhóm Tài Xế (Driver Segmentation)

Dựa trên nghiên cứu từ Uber, Grab, và lý thuyết phân khúc hành vi. 5 nhóm chính theo 2 trục: **Tần suất hoạt động** × **Mức độ cam kết**.

```
            Cam kết CAO
                │
    ┌───────────┼───────────┐
    │           │           │
    │  🟣 LOYALIST  │  ⭐ CHAMPION  │
    │  (Trung thành) │  (Nhà vô địch)│
    │           │           │
────┼───────────┼───────────┼────  Tần suất
 THẤP          │          CAO
    │           │           │
    │  🟡 DRIFTER   │  🔵 HUSTLER   │
    │  (Trôi dạt)   │  (Chạy sô)    │
    │           │           │
    └───────────┼───────────┘
                │
            Cam kết THẤP

    + 🔴 DORMANT (Ngủ đông) — Nằm ngoài ma trận (inactive ≥ 14 ngày)
```

#### ⭐ CHAMPION — Nhà Vô Địch (Target: 15-20% driver pool)

| Đặc điểm | Chi tiết |
|:---|:---|
| **Định nghĩa** | ≥ 22 ngày/tháng, ≥ 120 đơn/tháng, Rating ≥ 4.8, Cancel Rate ≤ 5% |
| **Giá trị** | ~15% pool nhưng ~40% tổng đơn |
| **Rủi ro** | Burnout, bị đối thủ lôi kéo |
| **Chiến lược** | Recognition + Exclusive benefits + Financial services + Mentor role |

#### 🟣 LOYALIST — Trung Thành (Target: 20-25%)

| Đặc điểm | Chi tiết |
|:---|:---|
| **Định nghĩa** | 15-21 ngày/tháng, 60-119 đơn/tháng, Rating ≥ 4.5, Cancel Rate ≤ 10% |
| **Giá trị** | Nguồn cung ổn định, tiềm năng upgrade Champion |
| **Chiến lược** | Upgrade path rõ ràng + Tăng benefits gap Silver→Gold + Goal-setting |

#### 🔵 HUSTLER — Chạy Sô (Target: 20-25%)

| Đặc điểm | Chi tiết |
|:---|:---|
| **Định nghĩa** | ≥ 18 ngày/tháng, ≥ 100 đơn/tháng, nhưng multi-platform, Rating 4.3-4.7 |
| **Giá trị** | Volume cao nhưng loyalty thấp |
| **Chiến lược** | Lock-in bằng switching cost (benefits tích lũy), exclusive order pool, streak |

#### 🟡 DRIFTER — Trôi Dạt (Target: 15-20%)

| Đặc điểm | Chi tiết |
|:---|:---|
| **Định nghĩa** | 5-14 ngày/tháng, 20-59 đơn/tháng |
| **Giá trị** | "Supply buffer" cho peak hour |
| **Chiến lược** | Flexible quest + Peak hour incentive + Dễ quay lại |

#### 🔴 DORMANT — Ngủ Đông (Target: < 20%)

| Đặc điểm | Chi tiết |
|:---|:---|
| **Định nghĩa** | Inactive ≥ 14 ngày. **Early Dormant** (< 30 đơn): win-back khó. **Late Dormant** (≥ 30 đơn): khả thi. |
| **Chiến lược** | Win-back phân loại: Early → SMS đơn giản, Late → Callback + Welcome-back bonus |

#### Ma Trận Chuyển Đổi

```
🔴 DORMANT ──win-back──→ 🟡 DRIFTER ──nurture──→ 🟣 LOYALIST ──upgrade──→ ⭐ CHAMPION
                              │                         │
                              ↓                         ↓
                         🔵 HUSTLER ──lock-in──→ 🟣 LOYALIST ──upgrade──→ ⭐ CHAMPION
```

### 4.2 Cơ Chế Win-Back 💡

| Nhóm | Điều kiện | Chiến lược | Budget |
|:---|:---|:---|:---|
| **High-Value Dormant** | ≥ 100 đơn lifetime, Rating ≥ 4.5, inactive 14-60 ngày | Callback cá nhân + Welcome-back bonus mạnh + Fast-track tier restore | 🔴 Cao |
| **Mid-Value Dormant** | 30-99 đơn lifetime, inactive 14-60 ngày | Push + SMS + Moderate bonus | 🟠 TB |
| **Low-Value Dormant** | < 30 đơn lifetime, inactive 14-90 ngày | Push notification đơn giản | 🟡 Thấp |
| **Churned** | Inactive > 90 ngày | Quarterly win-back campaign batch | 🟡 Thấp |

### 4.3 Inactivity Alert Protocol

| Thời gian inactive | Phase 1-2 (D0-D14) | Phase 3-4 (D15-D120) | Phase 5-6 (D121+) |
|:---|:---|:---|:---|
| 2 ngày | Push + Milestone reminder | — | — |
| 3 ngày | SMS/Zalo + Bonus offer | — | — |
| 5 ngày | **Gọi điện trực tiếp** | — | — |
| 7 ngày | Escalate DM Ops | Push + Income projection | — |
| 10 ngày | — | **Gọi điện** + Re-activation quest | Push + "Bạn sắp mất R2 + BH" |
| 14 ngày | Flag "Dormant" | Flag Dormant + Grace Period | **Gọi điện** + "Mất BH!" |
| 21 ngày | Archive | Win-back campaign | Nhắn từ quản lý khu vực |
| 30 ngày | Archive | Archive → Monthly batch | Monthly win-back |

### 4.4 At-Risk Daily Monitor (SQL)

```sql
-- Tài xế cần can thiệp khẩn trong 24h
SELECT
    driver_id, city, register_date,
    DATEDIFF(CURDATE(), register_date) AS driver_age_days,
    last_active_date,
    DATEDIFF(CURDATE(), last_active_date) AS days_inactive,
    total_trips, current_tier, current_segment,
    CASE
        WHEN driver_age_days <= 3 AND days_inactive >= 1
            THEN 'PHASE1_ACTIVATION_RISK'
        WHEN driver_age_days BETWEEN 4 AND 14 AND days_inactive >= 2
            THEN 'PHASE2_FIRST_WIN_RISK'
        WHEN driver_age_days BETWEEN 15 AND 45 AND days_inactive >= 7
            THEN 'PHASE3_HABIT_BREAKING'
        WHEN driver_age_days BETWEEN 46 AND 120 AND days_inactive >= 10
            THEN 'PHASE4_GROWTH_STALLING'
        WHEN driver_age_days BETWEEN 121 AND 365 AND days_inactive >= 14
            THEN 'PHASE5_MASTERY_WAVERING'
        WHEN driver_age_days > 365 AND days_inactive >= 21
            THEN 'PHASE6_AMBASSADOR_DECLINING'
    END AS intervention_type,
    CASE
        WHEN current_segment = 'Champion' THEN 'HIGH_PRIORITY'
        WHEN current_segment = 'Loyalist' THEN 'HIGH_PRIORITY'
        WHEN current_segment = 'Hustler'  THEN 'MEDIUM_PRIORITY'
        WHEN current_segment = 'Drifter'  THEN 'LOW_PRIORITY'
        ELSE 'STANDARD'
    END AS priority_level
FROM drivers
WHERE intervention_type IS NOT NULL
ORDER BY priority_level, days_inactive DESC;
```

---

## PHẦN V: TÍCH HỢP & TRIỂN KHAI

### 5.1 Mapping: Journey Phase → Ranking System

| Journey Phase | Thâm niên | Ranking Tier | Layer Access |
|:---|:---|:---|:---|
| Phase 1-2 (D0-D14) | < 1 tháng | Chưa xếp hạng | L6 MASS |
| Phase 3 (D15-D45) | ≈ 1 tháng | R3 Standard (nếu đủ KPI) | L4 Bigzone |
| Phase 4 (D46-D120) | 1-4 tháng | R3 → R2 Active | L4 → L3 Mediumzone |
| Phase 5 (D121-D365) | 4-12 tháng | R2 → R1 Elite | L3 → L2 Minizone |
| Phase 6 (D365+) | 12+ tháng | R1 Elite (duy trì) | L2 Minizone + L1 KA/MP |

### 5.2 Mapping: Segment → AhaBenefits

| Segment | AhaBenefits Tier | Hệ số Points | Catalog Access |
|:---|:---|:---|:---|
| ⭐ Champion | 💎 Kim Cương | ×1.5 | Full catalog + BH tai nạn |
| 🟣 Loyalist | 🥇 Vàng | ×1.3 | Vàng + Bạc |
| 🔵 Hustler | 🥈 Bạc (hoặc Vàng nếu đủ KPI) | ×1.1 - ×1.3 | Bạc (+ Vàng nếu upgrade) |
| 🟡 Drifter | 🥈 Bạc (hoặc không) | ×1.0 - ×1.1 | Bạc basic |
| 🔴 Dormant | Đóng băng | — | Không truy cập |

### 5.3 Value Realization (BEFORE → AFTER)

| Hiện trạng | Chuyển đổi | Target State | Impact | Loại |
|:---|:---|:---|:---|:---|
| Tài xế mới không có hướng dẫn → 45% churn D30 | 6-Phase Journey + Guarantee 30D | Lộ trình rõ + Guaranteed Earnings + Instant Payout | D30 retention 75% | 🟢 Benchmarked |
| Chỉ chạy 1 dịch vụ → EPH thấp | Multi-Service Unlock | Progressive unlock 5 dịch vụ | +19pp retention | 🟢 Benchmarked (Uber) |
| Không phân biệt tài xế mới vs cũ | Segment-Based Ops | 5 nhóm × chiến lược riêng | +40% Active Driver | 🟡 Aspirational |
| Không có BH → thua XanhSM | Tiered Insurance | Bronze → Silver → Gold | D180 ret +42% | 🟢 Benchmarked (Swiggy) |
| Tài xế lâu năm không có role → burnout | Ambassador + Community | Mentor + Captain + Advisory Board | LTV 3.5 → 12 tháng | 🔴 Stretch |
| Phát hiện churn chậm | Predictive Alerts + Grace Period | Cảnh báo sớm + 14 ngày cứu hạng | Giảm 50% Dormant | 🟡 Aspirational |
| Win-back không phân loại | Tiered Win-Back | High/Mid/Low value flow | Win-back 10% → 35% | 🟡 Aspirational |

### 5.4 Lộ Trình Triển Khai

| Giai đoạn | Timeline | Ưu tiên | Owner |
|:---|:---|:---|:---|
| **Phase A — Foundation** | T6-T7/2026 | Cohort Dashboard · Inactivity Alert · Guaranteed Earnings 30d · Instant Payout D0-D30 · Earnings Transparency · Buddy System pilot (SGN → HAN) | DM + BI + Product + Finance |
| **Phase B — Gamification** | T7-T8/2026 | Streak System + Milestone Rewards · Weekly Quest · Multi-Service Unlock progression · Progress Bar & Tier Badge · Income Dashboard + Goal Setting | Product + S&P |
| **Phase C — Segmentation & Insurance** | T8-T9/2026 | 5-segment model deploy · Segment-based automation · Tiered Insurance pilot Bronze (R3 SGN) · Grace Period + Loss Aversion · Win-back flow · Community Program | BI + DM + HR + Đối tác BH |
| **Phase D — Advanced** | T9-T12/2026 | Insurance Silver (R2) + Gold (R1) rollout · Ambassador & Mentor Program · Driver Advisory Board · Churn Prediction ML · Performance Optimization Tools | DM + HR + Finance + BI + DS |

---

## 📚 NGUỒN THAM KHẢO

### Nền Tảng & Dữ Liệu Thị Trường (📊 Industry Data)

- **Uber:** Uber Pro tier system, Quest Bonuses, Guaranteed Earnings 30-day, Upfront Pricing, Diamond cash reward removal (2025), Cross-platform retention (+19pp)
- **Grab SEA:** 4-Tier GrabBenefits, Guaranteed Earnings 14-day (+32% D30), 90% quarterly retention Q2/2023
- **Gojek:** GoPartner Hub, GoFleet, GoalBetter (Classic/Premium/Pro/Elite), GoPayLater
- **DoorDash:** Dasher Rewards (replaced Top Dasher), Large Order Program, Overall Dasher Rating (composite 0-100)
- **Deliveroo:** Fee Multiplier 1.1x-1.5x, Session Planning (+28%), Rider Insurance (accident + £1M liability + £35/day + £1,000 parental)
- **Swiggy:** StepUp — Gold/Silver/Bronze tiered insurance → churn giảm 60-70% → 10-15%
- **Rappi:** RappiPay (ví + thẻ tín dụng + tiết kiệm + micro-lending)
- **Meituan:** Scoring system thay penalty (2024-2025), anti-fatigue, BH tai nạn lao động 1.4 tỷ CNY
- **Be Vietnam:** beAcademy, 3-tier (Đồng/Bạc/Vàng)
- **XanhSM Vietnam:** Salary + KPI hybrid — lương cố định + 25% commission + BHXH/BHYT/BHTN
- **iFood Brazil:** Dual model (75% gig + 25% subcontracted), Support Points, 45K EV plan

### Nghiên Cứu Khoa Học (🔬 Peer-Reviewed)

- Lally, P. et al. (2010) "How are habits formed" — UCL, European Journal of Social Psychology. **66 ngày avg (18-254 range)**
- Zwettler et al. (2024) "Kicking off a Gig Work Career: Career Learning Cycle" — SAGE, Journal of Career Assessment
- Selcuk & Gokpinar (2025) "Incentivizing Flexible Workers" — SAGE, M&SOM
- Allon et al. (2019) "Impact of Behavioral and Economic Drivers on Gig Economy Workers" — Wharton/Mack Institute
- Deci, E.L. & Ryan, R.M. — Self-Determination Theory (Autonomy, Competence, Relatedness)
- Fogg, B.J. — Tiny Habits (Motivation × Ability × Prompt)
- Rusbult, C.E. — Investment Model of Commitment (Satisfaction + Investment - Alternatives)
- Kahneman, D. — Prospect Theory: Loss Aversion (mất gây đau gấp 2x)
- Nunes, J.C. & Dreze, X. (2006) — Endowed Progress Effect
- Erikson, E. — Generativity in Adult Development

### Báo Cáo & Media (📰 Reports)

- ILO Gig Economy Report (2024): Thu nhập ổn định > Linh hoạt > Cơ hội phát triển. LTV 2.3x nếu đáp ứng cả 3
- Everee 2025 Gig Driver Report: 70% muốn payout <24h, 44% rời đi nếu chậm
- eduMe: Activation Rates in the Gig Economy
- Abraham et al. (2024) "Driving the Gig Economy" — NBER Working Paper

### Ahamove Internal

- Cohort retention data (Q1-Q2/2026)
- Segment transition analysis
- Driver ranking v2.0 parameters (`2026-05-driver-ranking-params.md`)

---

*Driver Management Team | Ahamove | Cập nhật: 09/06/2026*
*Phiên bản: v3.1 — Restructured: Research/Benchmark tách khỏi Proposal, KPIs classified (Benchmarked / Aspirational / Stretch)*
