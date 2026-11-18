# Driver Journey Framework — Ahamove
**Phiên bản:** 1.1 | **Ngày:** 2026-05-28 | **Owner:** Lê Phương Khanh — Driver Management

---

## TL;DR — Luận điểm chính

> **Vấn đề cốt lõi:** Hầu hết tài xế bỏ cuộc trong 120 ngày đầu không phải vì thu nhập thấp, mà vì *không hình thành được thói quen vận hành*, *không cảm nhận được sự tiến bộ*, và *không thuộc về cộng đồng nào*.

> **Giải pháp:** Xây dựng Driver Journey 5 giai đoạn có mục tiêu rõ ràng — mỗi giai đoạn có trigger can thiệp, milestone kích thích tâm lý, và KPI đo lường chặt chẽ. Ưu tiên 60 ngày đầu (cửa sổ hình thành thói quen) như chiến trường quyết định retention dài hạn.

---

## 1. Nền Tảng Nghiên Cứu

### 1.1 Bài học từ các nền tảng toàn cầu

| Nền tảng | Cơ chế cốt lõi | Kết quả đo được |
| :--- | :--- | :--- |
| **Gojek** | AI Income Boost — phân tích pattern hoạt động → gợi ý khu vực/giờ cao điểm cá nhân hoá | Giảm volatility thu nhập → tăng retention |
| **Grab** | Tier Loyalty (Emerald Circle) + Microlearning onboarding (Axonify) | Tỷ lệ kích hoạt onboarding >85% sau cải tổ 2023 |
| **Lyft** | Bảo đảm thu nhập tuần (70% expected fares) + Gamified streaks | Giảm 35% churn trong 30 ngày đầu |
| **DoorDash** | Fast Pay cho dasher mới tuần 1, Milestone Challenge | Tăng activation rate tuần đầu |
| **Uber Eats** | Onboarding bonus + streak bonus 7 ngày đầu | 3× retention 90 ngày với driver hoàn thành 5+ chuyến tuần 1 |

### 1.2 Khoa học hành vi — 3 nền tảng chính

**1. Mô hình BJ Fogg (Tiny Habits):** `Motivation × Ability × Prompt = Behavior`
- Với tài xế mới: Motivation = thu nhập; Ability = app dễ dùng; Prompt = push notification đúng thời điểm
- *Implication:* Không thể dựa vào Motivation (biến động) — phải engineer Ability và Prompt

**2. Self-Determination Theory (SDT) — 3 nhu cầu tâm lý:**
- **Autonomy:** Tự chủ giờ làm, chọn khu vực → tránh cảm giác bị thuật toán kiểm soát
- **Competence:** Tiến bộ có thể nhìn thấy được → tier badge, progress bar, milestone
- **Relatedness:** Thuộc về cộng đồng → WhatsApp group, Driver meetup, Mentor program

**3. Habit Formation (UCL Research — Phillippa Lally):**
- Trung bình **66 ngày** để hình thành thói quen bền vững (range: 18–254 ngày)
- Thói quen đơn giản (check app sáng) hình thành nhanh hơn (3–4 tuần)
- *Implication:* **Ngày 0–60 là cửa sổ chiến lược** — mọi can thiệp phải dồn vào đây

### 1.3 Các mốc churn nguy hiểm (dữ liệu thực tế)

| Cửa sổ nguy hiểm | Xác suất churn | Lý do |
| :--- | :--- | :--- |
| Tuần 1–2 (D7–D14) | Rất cao | Chưa thấy giá trị, chưa đủ thu nhập |
| Ngày 30–60 | Cao | Hết bonus onboarding, không còn "mới lạ" |
| Ngày 90–120 | Trung bình–cao | Milestone kiểm tra tier, quyết định gắn bó dài hạn |
| Sau 120 ngày | Thấp | Driver đã "sống sót" → xác suất gắn bó dài hạn tăng mạnh |

> **Rule of thumb:** Driver hoàn thành 7+ chuyến trong tuần đầu có tỷ lệ retention 90 ngày cao **gấp 3 lần** nhóm còn lại.

---

## 2. Driver Lifetime — 5 Giai Đoạn

```
[Pre-activation] → [KÍCH HOẠT] → [HÌNH THÀNH] → [CAM KẾT] → [CHUYÊN NGHIỆP] → [CỐT LÕI]
       D-7→D0          D1→D7        D8→D60        D61→D120      D121→D180         D181+
```

---

### Giai Đoạn 0 — PRE-ACTIVATION | D-7 → D0
**Mục tiêu:** Đưa tài xế từ đăng ký → sẵn sàng chuyến đầu tiên, không bỏ cuộc giữa chừng

| Yếu tố | Chi tiết |
| :--- | :--- |
| **Trigger vào** | Hoàn thành đăng ký hồ sơ |
| **Trigger ra** | Hoàn thành chuyến đầu tiên (D1) |
| **Rủi ro** | Drop-off trong quá trình nộp giấy tờ / chờ duyệt |
| **Tên nhóm** | **Tân Binh** |

**Các điểm can thiệp:**
- [ ] **D-7:** Gửi checklist onboarding có tiến trình trực quan (5 bước, progress bar)
- [ ] **D-5:** Nhắc nhở tài liệu còn thiếu (auto-detect từ hồ sơ)
- [ ] **D-3:** Preview thu nhập kỳ vọng khu vực tài xế đăng ký ("Tài xế khu vực Q.10 trung bình kiếm X.XXX VNĐ/ngày")
- [ ] **D0:** Push notification kích hoạt + thông báo bonus chuyến đầu tiên

**KPI giai đoạn:**
- `Onboarding Completion Rate` = % tài xế đăng ký hoàn thành đủ hồ sơ → target ≥85%
- `Time-to-First-Trip` = số ngày từ đăng ký → chuyến 1 → target ≤3 ngày

---

### Giai Đoạn 1 — KÍCH HOẠT | D1 → D7
**Mục tiêu:** Tài xế *thực sự trải nghiệm giá trị* — hoàn thành ≥7 chuyến, nhận thu nhập đầu tiên, cài đặt thói quen mở app buổi sáng

| Yếu tố | Chi tiết |
| :--- | :--- |
| **Trigger vào** | Chuyến đầu tiên hoàn thành |
| **Trigger ra** | ≥7 chuyến trong 7 ngày đầu |
| **Rủi ro** | Không đủ đơn → cảm giác nản; thu nhập D1 quá thấp → bỏ cuộc |
| **Tên nhóm** | **Tân Binh** (tiếp tục) |

**Milestone quan trọng:**
```
D1 ──── D3 ──────────── D7
 │       │               │
Chuyến   5 chuyến =      10 chuyến = "Activation
đầu tiên micro-bonus     Complete" badge + Cash reward
(tâm lý neo) (+20k VNĐ)  (+100k–200k VNĐ)
```

**Các điểm can thiệp:**
- **D1 sáng:** "Hôm nay bắt đầu với Ahamove — khu vực bạn có X đơn đang chờ, giờ cao điểm 11h–13h"
- **D3 (nếu <3 chuyến):** Cảnh báo sớm — gửi gợi ý khu vực/giờ cao điểm cá nhân hoá
- **D5 (nếu <5 chuyến):** Điện thoại/chat từ Driver Support: "Bạn cần hỗ trợ gì không?"
- **D7:** Tổng kết tuần — hiển thị thu nhập, số chuyến, tỉ lệ hoàn thành; Mốc 7 chuyến = badge kích hoạt
- **D7 (nếu <5 chuyến):** Flag là **At-Risk** → chuyển vào retention campaign

**KPI giai đoạn:**
- `First Week Activation Rate` = % đạt ≥7 chuyến trong D1–D7 → target ≥40%
- `D7 Retention Rate` = % còn active ở D7 → target ≥60%
- `First Week Earnings` = thu nhập trung bình tuần 1 → benchmark vs. khu vực

---

### Giai Đoạn 2 — HÌNH THÀNH THÓI QUEN | D8 → D60
**Mục tiêu:** Tài xế hình thành thói quen vận hành ổn định — chủ động mở app, có kế hoạch ca làm việc. Đây là **giai đoạn dài và quan trọng nhất**.

| Yếu tố | Chi tiết |
| :--- | :--- |
| **Trigger vào** | Hoàn thành ≥7 chuyến trong tuần 1 |
| **Trigger ra** | Duy trì active ≥4 ngày/tuần trong 8 tuần (D60) |
| **Rủi ro** | Hết "honeymoon period" → tỉ lệ từ chối đơn tăng; Income volatility cao |
| **Tên nhóm** | **Triển Vọng** |

**Milestone map giai đoạn này:**

| Mốc | Ngày | Điều kiện | Phần thưởng / Ý nghĩa |
| :--- | :--- | :--- | :--- |
| Streak-14 | D14 | Hoạt động 14 ngày liên tiếp | Badge "2 Tuần Kiên Trì" + 150k VNĐ bonus |
| Bước ngoặt 30 ngày | D30 | ≥20 ngày active trong D1–D30 | Lên tier **Triển Vọng** chính thức + kit đồng phục |
| Streak-21 | D21 | 21 ngày hoạt động | Micro-reward + Progress notification ("Bạn đang hình thành thói quen!") |
| Milestone 100 chuyến | ~D40–D50 | 100 chuyến tích luỹ | Badge đặc biệt "100 Chuyến" + Cash reward |
| Milestone 60 ngày | D60 | ≥45 ngày active trong D1–D60 | Badge "Thói Quen Thành Công" — mốc habit formation |

**Cơ chế Streak + Loss Aversion:**
- Streak đếm ngày active liên tiếp (hiển thị trong app, nổi bật)
- Nếu mất streak: hiển thị "Streak của bạn đã đứt — Mở app hôm nay để bắt đầu lại!"
- Streak Protection: 1 lần miễn/tháng (không mất streak nếu nghỉ 1 ngày)
- Demotion warning: "Bạn cần 5 chuyến nữa trong tuần này để giữ hạng Triển Vọng"

**Các điểm can thiệp:**
- **D14 (inactive 7 ngày):** **CRITICAL ALERT** — gọi điện/chat cá nhân + offer bonus re-activation
- **D21:** Review điểm giữa chặng — gửi báo cáo cá nhân (thu nhập, số chuyến, khu vực hiệu quả nhất)
- **D30:** Kết tháng đầu — tổng kết chi tiết + Welcome to "Triển Vọng" tier
- **D45:** Kiểm tra midpoint — nếu churn risk cao: gọi điện từ khu vực staff
- **D60:** Ăn mừng mốc habit — notification đặc biệt + reward xứng đáng

**Cơ chế Autonomy (SDT):**
- Cho phép đặt lịch làm việc ưa thích (giờ cao điểm, khu vực)
- App gợi ý "giờ vàng" dựa theo lịch sử của chính tài xế đó (personalised, không phải chung chung)

**KPI giai đoạn:**
- `D30 Retention Rate` → target ≥45%
- `D60 Retention Rate` → target ≥35%
- `Average Active Days / Month` → target ≥18 ngày
- `Streak Length (avg)` → target ≥10 ngày liên tiếp
- `Inactivity Alert Rate` = % tài xế kích hoạt cảnh báo 7 ngày không hoạt động → intervene trong 24h

---

### Giai Đoạn 3 — CAM KẾT | D67 → D120
**Mục tiêu:** Tài xế *quyết định* gắn bó với Ahamove như nguồn thu nhập chính hoặc bổ sung ổn định. Đây là điểm phân kỳ: driver vượt D120 có xác suất rất cao ở lại dài hạn.

| Yếu tố | Chi tiết |
| :--- | :--- |
| **Trigger vào** | Vượt qua D60 với habit đã hình thành |
| **Trigger ra** | Đạt D120 với consistent activity |
| **Rủi ro** | Income so sánh với đối thủ (Grab, Be); cảm giác "trần kính" về tier |
| **Tên nhóm** | **Thường Trực** |

**Tier chính thức được công nhận tại giai đoạn này:**

| Tier | Điều kiện vào | Quyền lợi |
| :--- | :--- | :--- |
| **Thường Trực** | ≥200 chuyến + D90 active | Base incentive +10%; Priority dispatch trong khung giờ đăng ký; Support ưu tiên |
| **Chuyên Nghiệp** | ≥500 chuyến + ≥20 ngày active/tháng | Incentive +15%; Schedule flexibility; Badge trên profile |

**Milestone quan trọng:**
```
D90 ─────────────── D120
 │                   │
Lên hạng            "Survival Point"
"Thường Trực"        Driver vượt đây có >70%
chính thức           xác suất ở lại 12 tháng
+ vinh danh          (điểm mấu chốt retention)
cộng đồng
```

**Cộng đồng & Relatedness (SDT):**
- D90: Mời tham gia Driver Community chính thức (nhóm Zalo/Facebook theo khu vực)
- D90: Kết đôi với Mentor (driver đã >1 năm) trong 30 ngày
- Tháng đầu đủ điều kiện: bầu chọn "Driver Triển Vọng của Tháng" — hiển thị trong app + fanpage

**KPI giai đoạn:**
- `D90 Retention Rate` → target ≥35%
- `D120 Retention Rate` → target ≥28%
- `Tier Upgrade Rate` = % tài xế đạt Thường Trực trước D90 → target ≥25%
- `Community Join Rate` = % tài xế tham gia cộng đồng → target ≥50%

---

### Giai Đoạn 4 — CHUYÊN NGHIỆP | D121 → D180
**Mục tiêu:** Tài xế *tự nhận diện* mình là tài xế Ahamove chuyên nghiệp — vận hành có chiến lược, thu nhập ổn định, bắt đầu tham gia cộng đồng chủ động.

| Yếu tố | Chi tiết |
| :--- | :--- |
| **Trigger vào** | Vượt D120 active |
| **Trigger ra** | Đạt D180 hoặc 500+ chuyến |
| **Rủi ro** | Burnout; giảm motivation vì không có đỉnh mới để leo |
| **Tên nhóm** | **Chuyên Nghiệp** |

**Bảo đảm thu nhập (Earning Guarantee):**
- Tài xế tier Chuyên Nghiệp trở lên: bảo đảm mức thu nhập sàn tuần (70% expected fares dựa trên lịch sử 4 tuần gần nhất)
- Cơ chế bảo đảm: nếu tuần đó thu nhập thực tế < sàn, Ahamove bù khoảng chênh (có điều kiện số chuyến tối thiểu)
- *Tác động tâm lý:* Giảm anxiety về income volatility → driver cam kết hơn

**Competence (SDT) — Phát triển kỹ năng:**
- Microlearning module: "Tối ưu hoá lộ trình", "Giao tiếp khách hàng 5 sao", "Vận hành giờ cao điểm"
- Chứng chỉ nội bộ: "Tài Xế 5 Sao Ahamove" (nếu duy trì rating ≥4.8 trong 60 ngày)
- Badge kỹ năng hiển thị trên profile driver trong app

**KPI giai đoạn:**
- `D180 Retention Rate` → target ≥22%
- `Average EPH (Earnings Per Hour)` → target đạt mức benchmark khu vực
- `Completion Rate` → target ≥97%
- `Rating Average` → target ≥4.7
- `Skill Certification Rate` = % hoàn thành ít nhất 1 module → target ≥60%

---

### Giai Đoạn 5 — CỐT LÕI | D181+
**Mục tiêu:** Tài xế trở thành asset chiến lược — nguồn cung tin cậy, đại sứ thương hiệu, mentor cho tài xế mới.

| Yếu tố | Chi tiết |
| :--- | :--- |
| **Trigger vào** | D181 + ≥500 chuyến + rating ≥4.7 |
| **Trigger ra** | N/A — duy trì vô thời hạn |
| **Rủi ro** | Cảm giác bị "bỏ quên" sau khi đã stable; đối thủ săn driver chất lượng cao |
| **Tên nhóm** | **Cốt Lõi** (D181–D365) / **Champion** (D365+) |

**Tier cấp cao:**

| Tier | Điều kiện | Quyền lợi đặc biệt |
| :--- | :--- | :--- |
| **Cốt Lõi** | D181 + ≥500 chuyến | Incentive +20%; Early access tính năng mới; Quarterly Driver Council |
| **Champion** | D365 + ≥1500 chuyến + rating ≥4.8 | Incentive +25%; Mentor program (được trả thêm); Sự kiện exclusive; Quà Anniversary |

**Mentor Program:**
- Driver Champion được assign 3–5 tài xế mới (D0–D30)
- Nhận bonus dựa trên retention của mentee (nếu mentee vượt D30/D90)
- *Tác động kép:* Champion được ghi nhận + Tân Binh được hỗ trợ

**Driver Anniversary:**
- D365: Tặng quà vật lý (áo đặc biệt, phụ kiện xe có logo Ahamove) + Certificate
- D365: Feature trên fanpage/story app: "Hành trình 1 năm của [Tên]"
- D365: Dinner/event exclusive cho Champion cohort

**KPI giai đoạn:**
- `12-Month Retention Rate` → target ≥15–20% của cohort gốc
- `Mentor Program Participation` = % Champion tham gia → target ≥40%
- `Mentee D30 Retention` (do Champion hỗ trợ) → target ≥60%
- `Driver NPS` → target ≥50
- `Referral Rate` = % Cốt Lõi/Champion giới thiệu driver mới → target ≥30%

---

## 3. Ma Trận Phân Nhóm Tài Xế

### 3.1 Phân nhóm theo Vòng Đời × Tần suất

```
                    │  THẤP (<5 trips/ngày)   │  TB (5–12 trips/ngày)  │  CAO (>12 trips/ngày)
────────────────────┼─────────────────────────┼────────────────────────┼──────────────────────
D1–D60              │  ⚠️ Tân Binh at-risk     │  ✅ Tân Binh on-track  │  🚀 Tân Binh fast-track
D61–D120            │  🔴 Đang rời đi          │  🟡 Đang hình thành    │  ✅ Cam kết
D121–D180           │  🔴 High churn risk      │  ✅ Chuyên Nghiệp      │  ⭐ Core candidate
D181+               │  🟡 Casual (giữ nhẹ)    │  ✅ Cốt Lõi            │  🏆 Champion
```

### 3.2 Nhóm Can Thiệp Ưu Tiên

| Nhóm | Định nghĩa | Hành động |
| :--- | :--- | :--- |
| **🚨 At-Risk Mới** | D7–D30 + 7 ngày không active | Gọi điện trong 24h + Re-activation bonus |
| **⚠️ Drift** | D30–D90 + giảm activity >30% so với 2 tuần trước | Push notification + Income projection personalised |
| **🔄 Recovering** | Từng inactive 14+ ngày, đang quay lại | Welcome back campaign + Streak reset bonus |
| **💎 Latent Core** | D120+ + activity cao nhưng chưa upgrade tier | Nhắc tier upgrade + quyền lợi cụ thể |
| **👑 Champion Candidate** | D180+ + rating ≥4.8 + >1000 chuyến | Mời vào Mentor Program + Council |

---

## 4. Bản Đồ Mốc Thời Gian Tổng Thể

```
D0    D3    D7    D14   D21   D30   D45   D60   D90   D120  D180  D365
│     │     │     │     │     │     │     │     │     │     │     │
●─────●─────●─────●─────●─────●─────●─────●─────●─────●─────●─────●
│     │     │     │     │     │     │     │     │     │     │     │
Chuyến Micro D7   Streak D21  Tháng Mid-  HABIT D90   Survival Prof. Champion
đầu   bonus Act.  badge  badge  1   check  60D   tier  point  tier  Anniv.
            badge  14d         done        BADGE upgrade        unlock Award
```

| Mốc | Ngày | Điều kiện kích hoạt | Loại can thiệp | Mức độ ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| First Trip | D1 | Hoàn thành chuyến đầu | Chúc mừng + Show earnings | 🔴 Critical |
| Micro-win | D3 | 5 chuyến hoàn thành | Bonus nhỏ + Progress notification | 🟠 High |
| Activation Complete | D7 | ≥7 chuyến trong D1–D7 | Badge + Cash reward lớn | 🔴 Critical |
| At-Risk Alert | D7 | <5 chuyến tổng | Outreach cá nhân | 🔴 Critical |
| Streak-14 | D14 | 14 ngày active liên tiếp | Badge + 150k bonus | 🟠 High |
| Inactivity Alert | D8–D66 | 7 ngày không active | Push + Gọi điện | 🔴 Critical |
| Streak-21 | D21 | 21 ngày liên tiếp | Micro-reward | 🟡 Medium |
| Tháng đầu | D30 | ≥20 ngày active | Tier upgrade + Kit | 🔴 Critical |
| 100 Chuyến | ~D40 | 100 chuyến tích luỹ | Badge + Cash | 🟠 High |
| Midpoint check | D45 | Review activity | Personalised report | 🟡 Medium |
| Habit Milestone | D60 | ≥45 ngày active D1–D60 | Special badge + Reward lớn | 🔴 Critical |
| Tier Thường Trực | D90 | ≥200 chuyến + active | Tier badge + Quyền lợi | 🔴 Critical |
| Survival Point | D120 | Active + on-track | Mời Community | 🟠 High |
| Tier Chuyên Nghiệp | D180 | ≥500 chuyến + rating | Tier + Earning guarantee | 🔴 Critical |
| Anniversary | D365 | Active + ≥1500 chuyến | Quà vật lý + Feature trên app | 🟠 High |

---

## 5. Playbook Can Thiệp Theo Tình Huống

### SCENARIO A: Tài xế mới im lặng sau 7 ngày

```
Detect: D7 + <5 chuyến tổng
→ D8 sáng: Push "Khu vực bạn đang có đơn chờ — 50k nếu hoàn thành 3 chuyến hôm nay"
→ D8 chiều (nếu chưa active): SMS/Zalo từ Driver Support cá nhân
→ D10 (vẫn inactive): Gọi điện trực tiếp — tìm hiểu lý do
→ D14 (vẫn inactive): Flag churned, chuyển vào Win-Back flow (campaign riêng)
```

### SCENARIO B: Streak đứt giữa giai đoạn 2

```
Detect: Ngày N — streak đứt sau ≥10 ngày liên tiếp
→ Ngay ngày N+1: Notification "Streak của bạn đã đứt — Dùng Streak Protection hôm nay?"
→ Nếu còn Streak Protection: activate → streak giữ nguyên, protection reset sau 30 ngày
→ D+2 (vẫn inactive): "Bắt đầu lại từ hôm nay — streak mới, cộng thêm 50k nếu đạt 7 ngày"
→ D+7 (vẫn inactive): At-Risk alert — escalate
```

### SCENARIO C: Tài xế tier Triển Vọng đang "trôi"

```
Detect: D60–D90 + activity giảm >30% so với 4 tuần trước
→ Gửi Income Projection: "Nếu duy trì tốc độ hiện tại, tháng này bạn thiếu ~X đơn để lên Thường Trực"
→ Personalised suggestion: "Giờ 17h–19h thứ 3–5 khu vực Q.7 có surge cao nhất lịch sử của bạn"
→ Nếu D90 không đạt tier: "Bạn cần thêm Y chuyến trong X ngày — chúng tôi sẽ cộng thêm 10% mỗi chuyến"
```

### SCENARIO D: Champion trở nên nhàm chán (giảm activity sau D365)

```
Detect: D365+ + activity giảm >40% trong 4 tuần
→ Nhắn thẳng từ quản lý khu vực: ghi nhận đóng góp, hỏi thăm
→ Mời tham gia Mentor Program (nếu chưa) — tạo mục đích mới
→ Offer exclusive: tham gia Driver Council, góp ý sản phẩm
→ Nếu vẫn giảm: exit survey — tìm hiểu lý do để cải thiện hệ thống
```

---

## 6. Dashboard Quản Lý — KPI Tổng Hợp

### 6.1 Cohort Health Dashboard (theo dõi hàng tuần)

| Metric | Công thức | Target | Alert Level |
| :--- | :--- | :--- | :--- |
| `D7 Activation Rate` | Drivers với ≥7 trips D1–D7 / Total new drivers | ≥40% | <25% |
| `D30 Retention` | Drivers active D30 / Total new D1 (30 ngày trước) | ≥45% | <30% |
| `D60 Habit Formation` | Drivers active ≥45 ngày trong D1–D60 / Total | ≥35% | <20% |
| `D90 Retention` | Drivers active D90 / Total new D1 (90 ngày trước) | ≥35% | <20% |
| `D120 Survival Rate` | Drivers still active D120 / Total new D1 | ≥28% | <15% |
| `D180 Pro Rate` | Drivers đạt tier Chuyên Nghiệp / Total new D1 | ≥20% | <10% |
| `12M Retention` | Drivers still active M12 / Total new D1 | ≥15% | <8% |

### 6.2 At-Risk Monitoring (theo dõi hàng ngày)

```sql
-- Tài xế cần can thiệp khẩn trong 24h
SELECT
    driver_id,
    city,
    register_date,
    DATEDIFF(CURDATE(), register_date) AS driver_age_days,
    last_active_date,
    DATEDIFF(CURDATE(), last_active_date) AS days_inactive,
    total_trips,
    current_tier,
    CASE
        WHEN driver_age_days BETWEEN 1 AND 7
             AND total_trips < 5
             AND days_inactive >= 2          THEN 'CRITICAL_NEW_INACTIVE'
        WHEN driver_age_days BETWEEN 8 AND 30
             AND days_inactive BETWEEN 7 AND 14 THEN 'HABIT_WINDOW_AT_RISK'
        WHEN driver_age_days BETWEEN 31 AND 60
             AND days_inactive >= 7           THEN 'HABIT_FORMING_DROPOUT'
        WHEN driver_age_days BETWEEN 61 AND 120
             AND days_inactive >= 14          THEN 'COMMITMENT_WAVERING'
        ELSE NULL
    END AS intervention_type
FROM drivers
WHERE register_date >= CURDATE() - INTERVAL 180 DAY
  AND (
      (DATEDIFF(CURDATE(), register_date) BETWEEN 1 AND 7 AND total_trips < 5)
   OR (DATEDIFF(CURDATE(), last_active_date) BETWEEN 7 AND 14
       AND DATEDIFF(CURDATE(), register_date) BETWEEN 8 AND 120)
  )
ORDER BY intervention_type, days_inactive DESC;
```

### 6.3 Tier Transition Tracker

```sql
-- Tiến trình lên tier — phát hiện driver "gần tier"
SELECT
    driver_id,
    current_tier,
    total_trips,
    active_days_last_30,
    avg_rating_last_60d,
    CASE
        WHEN current_tier = 'Tan_Binh'      AND total_trips >= 150 THEN 'Ready → Trieu_Vong'
        WHEN current_tier = 'Trieu_Vong'    AND total_trips >= 180 THEN 'Ready → Thuong_Truc'
        WHEN current_tier = 'Thuong_Truc'   AND total_trips >= 450 THEN 'Ready → Chuyen_Nghiep'
        WHEN current_tier = 'Chuyen_Nghiep' AND total_trips >= 1300 THEN 'Ready → Cot_Loi'
        ELSE NULL
    END AS upgrade_status,
    CASE
        WHEN current_tier = 'Tan_Binh'      THEN 200 - total_trips
        WHEN current_tier = 'Trieu_Vong'    THEN 200 - total_trips  -- threshold Thuong_Truc
        WHEN current_tier = 'Thuong_Truc'   THEN 500 - total_trips
        WHEN current_tier = 'Chuyen_Nghiep' THEN 1500 - total_trips
        ELSE 0
    END AS trips_to_next_tier
FROM drivers
WHERE upgrade_status IS NOT NULL
ORDER BY trips_to_next_tier ASC;
```

---

## 7. Tóm Tắt Tier System

| Tier | Giai đoạn | Điều kiện tích luỹ | Quyền lợi chính | Badge |
| :--- | :--- | :--- | :--- | :--- |
| **Tân Binh** | D0–D29 | Mới đăng ký | Onboarding bonus, Mentor hỗ trợ | 🔵 |
| **Triển Vọng** | D30–D89 | ≥200 trips + ≥20 ngày active/tháng | +10% incentive, Priority support | 🟢 |
| **Thường Trực** | D90–D179 | ≥500 trips + rating ≥4.6 | +15% incentive, Community access, Schedule flex | 🟡 |
| **Chuyên Nghiệp** | D180–D364 | ≥1000 trips + rating ≥4.7 | +20% incentive, Earning guarantee, Skill cert | 🟠 |
| **Cốt Lõi** | D365+ | ≥1500 trips + rating ≥4.8 | +25% incentive, Mentor bonus, Driver Council | 🔴 |
| **Champion** | D365+ (elite) | ≥3000 trips + sustained excellence | +30% incentive, Product feedback loop, Anniversary | 🏆 |

> *Lưu ý:* Tier dựa trên tích luỹ chuyến ĐÃ HOÀN THÀNH (không tính chuyến huỷ). Rating tính trung bình 60 ngày gần nhất. Tier có thể bị hạ nếu rating <4.3 trong 30 ngày liên tiếp hoặc inactive >21 ngày.

---

## 8. Lộ Trình Triển Khai

| Giai đoạn | Timeline | Ưu tiên |
| :--- | :--- | :--- |
| **Phase 1 — Foundation** | T6–T7/2026 | Thiết lập cohort dashboard (D7/D30/D90 tracking); Inactivity alert system (7/14 ngày); Milestone bonus D7 + D30 |
| **Phase 2 — Gamification** | T7–T8/2026 | Streak system trong app; Tier badge hiển thị; Progress bar "X chuyến đến tier tiếp theo" |
| **Phase 3 — Community** | T8–T9/2026 | Driver Community Zalo/Facebook theo khu vực; Mentor Program (Champion → Tân Binh); Driver of the Month |
| **Phase 4 — Advanced** | T9–T12/2026 | Earning guarantee cho Chuyên Nghiệp+; Personalised income projection; Churn prediction ML model; Driver Council |

---

*Tài liệu này tổng hợp từ nghiên cứu: Gojek Engineering Blog, Grab Driver Operations (APRN 2025), Lyft Churn Reduction Case Study, UCL Habit Formation Study (Lally et al.), Self-Determination Theory (Deci & Ryan), BJ Fogg Tiny Habits, Amplitude Retention Research, và dữ liệu vận hành ngành gig economy 2024–2026.*
