# Driver Lifecycle Journey — Tóm Tắt & Next Actions

> **One-pager** | Driver Management Team · Ahamove · 2026-06
> Chi tiết đầy đủ: [`2026-05-driver-lifecycle-journey.html`](2026-05-driver-lifecycle-journey.html)

---

## 1. Vấn Đề Cốt Lõi

Ahamove **không** rụng tài xế ở onboarding. Vùng chết nằm ở **Lock In (D15–D60)**.

| Mốc | Baseline | Nhận định |
| :--- | :--- | :--- |
| M+1 (≈D30) | ~78% (HAN 81% / SGN 76%) | ✅ Tốt — giữ chân tuần đầu ổn |
| M+3 (≈D90) | ~43% | 🔴 Rơi **~35pp** chỉ trong 60 ngày |

**→ Trọng tâm framework: chống rụng M+1 → M+3.**

---

## 2. Driver Journey — 2 Giai Đoạn

```
TX MỚI (D0–D60) ──── PIC: Nhi ────►  HANDOVER  ────► TX CŨ (D60+) ──── PIC: Tiên
   Warm Up · Hook In · Lock In         (D60)          Grow Up · Master · Ambassador
```

### TX Mới (D0–D60) — Nhi quản lý toàn bộ (gồm Dormant & Win-back <D60)

| Mốc | Giai đoạn | Sự kiện chính | Incentive (Thưởng Cột Mốc Đơn) |
| :--- | :--- | :--- | :--- |
| **D0** | Warm Up | Nhận handover từ Growth, đơn đầu (DFD) | Thưởng 3 đơn đầu |
| **D3** | Warm Up | Micro Win | Cash mốc 5 đơn |
| **D7** | Hook In | First Win — Badge "Tuần Đầu" | Cash mốc 7 đơn |
| **D14** | Hook In | Fortnight — Unlock 2H-4H-TMDT (≥25 đơn) | Cash mốc 25 đơn |
| **D21** | Lock In | Weekly Quest bắt đầu (20/30/40) | Quest bonus 3 bậc |
| **D30** | Lock In | Review tháng 1 → Weekly policy bình thường | Hết milestone bonus |
| **D60** | Lock In | **Graduation → R3 Bạc** + handover Tiên | Policy R3 + BH Bronze |

> **Nguyên tắc Incentive mới:** Hoàn thành X đơn → nhận Y cash (pay-per-performance).
> **KHÔNG** áp dụng chương trình đảm bảo thu nhập (Guarantee).

---

## 3. KPI Framework cho Nhi (chốt Monthly)

Logic "Cohort Tốt Nghiệp": **mẫu số = TX chạm đúng milestone trong tháng** (vd D60 tháng 8 = DFD từ 3/6→2/7).

| # | KPI | Baseline | Target | Nguồn |
| :--- | :--- | :--- | :--- | :--- |
| 1 ⭐ | **Graduation Rate → R3** | ~35% | **≥45%** | Ranking system (chốt đầu tháng) |
| 2 | D60 Retention | ~52% | ≥62% | ≥1 đơn / 7 ngày gần nhất |
| 3 | D30 Retention | ~78% | ≥83% | Leading indicator |
| 4 | D30→D60 Drop | ~26pp | ≤20pp | Cùng cohort, so 2 mốc |
| 5 | Win-back Rate (<D60) | Chưa đo | ≥40% | Dormant ≥14N quay lại |

> Graduation Rate = North Star. Luôn ≤ D60 Retention (TX active nhưng có thể chưa đủ R3).
> SGN ≥42% · HAN ≥48%.

---

## 4. Weekly Health Check (Nhi theo dõi mỗi tuần)

Đo sức khỏe sớm 4 mốc — leading indicators cho KPI monthly.

| Milestone | Retention = ? | Target | At-Risk = ? |
| :--- | :--- | :--- | :--- |
| **D3** | ≥2 đơn trong 3 ngày đầu | ≥95% | 0 đơn sau DFD |
| **D7** | ≥1 đơn (D5–D7) | ≥90% | Inactive ≥3N |
| **D14** | ≥1 đơn (D12–D14) | ≥88% | Inactive ≥5N |
| **D21** | ≥1 đơn (D17–D21) | ≥85% | Inactive ≥7N |

**Khi dưới target → hành động ngay:** Push/SMS (D3) · Gọi điện (D7) · Zalo + Quest nhỏ (D14) · Buddy call (D21).

---

## 5. Next Actions — theo PIC

Mỗi milestone cần phối hợp 3 bên: **Ops (Nhi)** · **Product (Dev)** · **PA (Payment Analyst)**.

### Ưu tiên P0 (bắt buộc trước rollout)

| Milestone | Ops (Nhi) | Product | PA (Payment Analyst) |
| :--- | :--- | :--- | :--- |
| **D0** | Nhận handover, verify đơn đầu, chào mừng Zalo | Welcome flow, gán Buddy, Smart Dispatch | Thưởng 3 đơn đầu + tính cost/TX |
| **D3** | Flag TX 0 đơn → push/SMS 24h | Trigger noti, progress bar | Thưởng mốc 5 đơn, A/B test cash |
| **D7** | Auto-flag inactive ≥3N → gọi rescue | Push D5, dashboard at-risk, Badge | Cash mốc 7 đơn, tính cost |
| **D30** | Flag inactive ≥7N, review DQS <75 | Income Dashboard, unlock toàn bộ DV | Chuyển Weekly policy, tính CPO |

### Ưu tiên P1

| Milestone | Ops | Product | PA |
| :--- | :--- | :--- | :--- |
| **D14** | Buddy call inactive ≥5N | Badge Fortnight, unlock 2H-4H-TMDT | Cash mốc 25 đơn, policy giá cước |
| **D21** | Rescue inactive ≥7N | Weekly Quest, Progress Bar | Quest bonus 3 bậc |
| **D60** | Check Graduation, handover Tiên, Grace 14d | Ranking chốt, unlock BH Bronze | Policy R3, cost BH Bronze |

### Hạng mục xuyên suốt

| Hạng mục | Pri | Chủ trì |
| :--- | :--- | :--- |
| Cohort Dashboard (theo DFD) | **P0** | Product + BI |
| At-Risk Daily Monitor (SQL) | **P0** | Product → push list cho Nhi |
| Win-back Engine (<D60) | P1 | Product + PA + Nhi |

> **PA cần điền:** mức cash cụ thể vào các ô `XX,000đ` sau khi tính cost từng milestone.

---

## 6. Scope rõ ràng

| Người | Scope | Trách nhiệm |
| :--- | :--- | :--- |
| **Growth** | Đăng ký → Kích hoạt → DFD | Bàn giao TX sau đơn đầu |
| **Nhi** | TX lifetime **<D60** (gồm Dormant & tự win-back) | Onboarding → Graduation R3 |
| **Tiên** | TX **≥D60** | Grow Up → Master → Ambassador |

**Edge case:** TX chạm đúng D60 (calendar) → handover sang Tiên.

---

*Ahamove · Driver Management Team · 2026-06*
