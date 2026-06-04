# 🚀 KICK-OFF: Driver Ranking & AhaBenefits v2.0
## Dự Án Tái Cấu Trúc Tài Xế — Ahamove 2026

> **Phân phối:** Driver Management · Product · Engineering · BI/Data · CS · Finance · Legal/Risk  
> **Phiên bản tài liệu gốc:** 2026-05-27 | **Kick-off doc:** 2026-06-04

---

## 📊 EXECUTIVE SUMMARY

Dự án **Driver Ranking & AhaBenefits v2.0** là bước tái thiết toàn diện hệ thống quản lý tài xế, chuyển dịch từ mô hình vận hành rời rạc (AR/FR/Rating riêng lẻ) sang **hệ thống tích hợp đa chiều** dựa trên DQS (Driver Quality Score), kết hợp với cơ chế Dispatch theo Layer và nền kinh tế điểm thưởng (AhaPoints).

### 🎯 Mục Tiêu Kinh Doanh (S-C-R Framework)

| Tình huống (Situation) | Thách thức (Complication) | Kết quả cần đạt (Resolution) |
|:---|:---|:---|
| Fleet 10.500 weekly active drivers, phân bổ không đồng đều | Thiếu hụt cung vào peak-hour, tài xế chất lượng cao không được ưu tiên | Phân tầng rõ ràng 3 rank + Layer cascade → tối ưu cung-cầu |
| Incentive budget phân tán, khó đo ROI | Không có công cụ gắn kết dài hạn cho tài xế chất lượng | AhaBenefits tạo Driver LTV, giảm Churn Rate R1/R2 |
| Hệ thống điểm thưởng chưa tồn tại | Tài xế thiếu động lực nâng cao hiệu suất | Point Economy vận hành theo quý, có expiry tạo urgency |

---

## 📈 IMPORTANT KPIs — Bộ Chỉ Số Đo Lường Thành Công

### 🔷 KPIs Cốt Lõi Vận Hành

| KPI | Định nghĩa | Baseline (ước tính) | Target 3 tháng | Target 6 tháng |
|:---|:---|:---:|:---:|:---:|
| **Active Drivers (Weekly)** | Tài xế hoàn thành ≥1 chuyến/tuần | ~10.500 | Duy trì ≥10.500 | +5% (≥11.025) |
| **Fleet Ratio R1 : R2 : R3** | % phân bổ theo rank trong weekly actives | ❓ TBD | 15% : 35% : 35% : 15% | Ổn định ±3% |
| **Fulfillment Rate (FR)** | % đơn hàng được giao thành công | ❓ TBD | +3pp | +5pp |
| **Acceptance Rate (AR)** | % đơn được tài xế chấp nhận | ❓ TBD | ≥85% (R1+R2) | ≥88% (R1+R2) |
| **Driver Cancellation Rate (DCR)** | % chuyến tài xế hủy sau nhận | R1 mục tiêu ≤10% | Đạt ngưỡng SLA theo rank | 0 vi phạm mass |
| **Capacity Utilization (Peak)** | % slot ca Peak được điền đầy | ❓ TBD | ≥85% | ≥90% |

### 🔷 KPIs Kinh Tế Điểm (Point Economy Health)

| KPI | Định nghĩa | Mức cảnh báo |
|:---|:---|:---|
| **Point Burn Rate** | % điểm được đổi / điểm phát hành trong quý | < 30% → chương trình kém hấp dẫn |
| **Point Expiry Rate** | % điểm hết hạn cuối quý / tổng phát hành | > 40% → tài xế không dùng → lãng phí |
| **Redemption Success Rate** | % lượt đổi thưởng thành công / tổng lượt đổi | < 90% → vấn đề hệ thống/partner |
| **AhaBenefits Adoption Rate** | % tài xế R2+ đã đổi ≥1 reward/quý | < 50% → cần cải thiện UX hoặc catalog |
| **Avg AhaPoints/Driver/Tháng** | Điểm tích lũy bình quân/tài xế/tháng | Cần benchmark sau 1 quý |

### 🔷 KPIs Chất Lượng & Gắn Kết

| KPI | Định nghĩa | Target |
|:---|:---|:---|
| **DQS Average by Rank** | Điểm DQS bình quân theo rank | R1 ≥82, R2 ≥77, R3 ≥72 |
| **Driver Churn Rate (R1+R2)** | % tài xế rank cao rời nền tảng/tháng | ≤ 5%/tháng |
| **Driver LTV (Life-Time Value)** | Doanh thu tích lũy theo vòng đời tài xế | Tăng 15% so với cohort hiện tại |
| **Rank Upgrade Rate** | % tài xế R3 lên R2, R2 lên R1/quý | ≥ 10% |
| **Full-day Guarantee Utilization** | % R1+R2 đăng ký ca Full-day | ≥ 60% trong 3 tháng đầu |
| **SLA Drop Rate** | % đơn vi phạm SLA giao hàng | Giảm 15% sau 3 tháng |

---

## 📋 TÓM TẮT CHIẾN LƯỢC — 7 PHẦN CỐT LÕI

### Phần 1 — Hệ Thống Ranking

**3 cấp bậc, đánh giá bằng DQS (tích hợp AR + FR + Rating):**

| Rank | DQS | DCR | Productivity | Fleet Target |
|:---|:---:|:---:|:---:|:---:|
| 💎 R1 Kim Cương | ≥80 | ≤10% | ≥280 stp/tháng | 15% (~1.575 drivers) |
| 🥇 R2 Vàng | ≥75 | ≤10% | ≥210 stp/tháng | 35% (~3.675 drivers) |
| 🥈 R3 Bạc | ≥75 | ≤15% | ≥70 stp/tháng | 35% (~3.675 drivers) |
| Unranked | <75 | — | — | 15% (~1.575 drivers) |

> ⚠️ **Lưu ý thiết kế quan trọng:** Không dùng AR/FR/Rating riêng lẻ — toàn bộ xét qua DQS tích hợp.

### Phần 2 — Dispatch & Layer Cascade

- **L2 → L3 → L4 → L5 → L6** (cascade khi ≥80% fill)
- R1 nhận đơn L2 (Minizone), R2 nhận L3, R3 nhận L4, Unranked vào L6 MASS
- Cửa sổ đăng ký ca mở sớm 2–4h cho rank cao hơn tại layer overlap
- **Full-day Guarantee** (08:00–18:00): R1 nhận 600k/ngày (SGN), R2 nhận 550k/ngày (SGN) — điều kiện: App online ≥95%, AR=100%, FR đạt ngưỡng, không tự hủy chuyến

### Phần 3 — Point Economy

- Điểm tích theo công thức: `round(trip_income ÷ 5.000) × multiplier`
- Multiplier: R1=×1.5 | R2=×1.3 | R3=×1.1 | Unranked=×1.0
- Bonus hoàn ca: R1=+30pts | R2=+25pts | R3=+20pts
- **Vòng đời điểm:** PENDING → AVAILABLE → RESERVED → REDEEMED/EXPIRED
- Reset điểm theo quý (có expiry tạo urgency đổi thưởng)

### Phần 4–5 — AhaBenefits Catalog & Redemption

- **R1 exclusive:** Voucher xăng 50k/tháng, Bảo hiểm tai nạn Mini (auto-activate ngày 01 tháng sau)
- **R2:** Voucher xăng 30k/tháng + catalog Bạc+Vàng
- **R3:** Catalog Bạc only
- Flow đổi thưởng có xử lý fail (hoàn điểm trong 30 giây nếu partner timeout)

### Phần 6 — Edge Cases Quan Trọng (Product cần quyết định)

| Kịch bản | Vấn đề | Đề xuất xử lý |
|:---|:---|:---|
| Đổi điểm cuối quý, partner fail | RESERVED pts có expire không? | Gia hạn 7 ngày bảo vệ RESERVED pts |
| Downgrade rank | Reward đã đổi có bị thu hồi? | Không — thời hạn gắn với reward, không với rank |
| Overflow order | Layer tính điểm theo origin hay assigned zone? | ❓ **Cần Product quyết định** |
| Redemption fail 48h cuối quý | Điểm hoàn nhưng sắp expire | Gia hạn 7 ngày sang quý mới |

---

## ✅ CHECKLIST CROSS-TEAM DEPENDENCIES

> **Mỗi team cần xác nhận danh sách này trước buổi kick-off hoặc trong Sprint 0**

---

### 🔧 PRODUCT TEAM — 7 Open Questions Cần Quyết Định

- [ ] **[P1 - CRITICAL]** RESERVED pts có bị expire cuối quý không? → Ảnh hưởng toàn bộ Scenario A
- [ ] **[P1 - CRITICAL]** Layer của đơn overflow xác định bằng **origin zone hay assigned zone**? → Ảnh hưởng tính điểm Scenario C
- [ ] **[P1]** Điểm PENDING (đang trong ca) hết quý → xử lý thế nào? (expire, carry-over, convert?)
- [ ] **[P2]** Có cho phép transfer/gift điểm giữa drivers không? (scope v2.0 hay v3?)
- [ ] **[P2]** Driver bị suspend: điểm freeze hay expire?
- [ ] **[P3]** Cần points history export để phục vụ báo cáo thuế/compliance không?
- [ ] **[P3]** Catalog availability có khác nhau theo thành phố SGN vs HAN không?
- [ ] **[THÊM MỚI]** Streak bonus (7 ngày liên tục) — số điểm thưởng [TBD] cần xác nhận mức cụ thể
- [ ] **[THÊM MỚI]** Campaign Mega Sales bonus — cơ chế cấu hình và approval flow

---

### 🛠️ ENGINEERING TEAM — Deliverables Cần Xây Dựng

**Data Model:**
- [ ] Implement `PointTransaction` table với đủ 12 fields (type, status, source_ref, layer, multiplier_applied, expires_at...)
- [ ] Implement `DriverPointWallet` (available_balance, reserved_balance, quarter_expires_at)
- [ ] Design DQS calculation engine (tích hợp AR + FR + Rating → 1 score)
- [ ] Xây dựng Layer assignment & cascade logic (threshold 80% fill trigger)
- [ ] Shift slot management system (cửa sổ đăng ký mở theo rank)

**Notification System:**
- [ ] Trigger cuối ca: "Bạn vừa nhận X pts"
- [ ] Trigger đổi thưởng: thành công / thất bại
- [ ] Trigger vi phạm ĐBCL: "-50 pts"
- [ ] Trigger 7 ngày + 1 ngày trước hết quý (expiry warning)
- [ ] Trigger thay đổi rank (Push + In-app)
- [ ] Trigger bảo hiểm R1: nhắc đăng ký trước ngày 25

**Admin Tool:**
- [ ] CS/Ops có thể add/deduct điểm thủ công (cần approval flow + audit log)
- [ ] Giao diện xem PointTransaction history theo driver_id

---

### 📊 BI/DATA TEAM — Data Requirements

- [ ] **Cung cấp baseline metrics** (FR, AR, DCR hiện tại theo từng rank/zone)
- [ ] **Build DQS formula** và validate với data lịch sử (back-test 3 tháng)
- [ ] **Dashboard Fleet Ratio** — theo dõi % R1:R2:R3 real-time hàng tuần
- [ ] **Dashboard Point Economy Health**: Burn Rate, Expiry Rate, Redemption Success Rate
- [ ] **Cohort Analysis Driver Churn**: so sánh churn trước/sau khi có AhaBenefits
- [ ] **Driver LTV Model**: xây dựng model dự báo LTV theo rank + tenure
- [ ] **Capacity Forecast (Peak)**: dự báo cung-cầu theo khung giờ, làm cơ sở điều chỉnh slot
- [ ] Cung cấp số lượng tài xế hiện tại đạt ngưỡng từng rank (để validate fleet ratio target 15:35:35:15)

---

### 📞 CUSTOMER SERVICE (CS) TEAM — SOP & Tools

- [ ] Xây dựng **SOP xử lý khiếu nại điểm**: điểm thiếu, sai multiplier, hết hạn
- [ ] SOP xử lý **Bảo hiểm R1**: driver báo không nhận số hợp đồng, claim sự cố
- [ ] SOP xử lý **Điểm trừ vi phạm ĐBCL**: quy trình xác minh trước khi trừ -50pts
- [ ] **Quyền hạn trong Admin Tool**: ai được cộng/trừ điểm thủ công, ai phê duyệt (approval matrix)
- [ ] Chuẩn bị FAQ cho driver: Điểm tính thế nào? Tại sao điểm ít hơn dự kiến? Đổi thưởng fail?
- [ ] Training team CS về hệ thống rank mới và AhaBenefits catalog

---

### 💰 FINANCE TEAM — Budget & Accounting

- [ ] **Approve ngân sách Full-day Guarantee**: ước tính số R1+R2 đăng ký × 600k–650k/ngày
- [ ] **Approve ngân sách Voucher xăng/sạc**: ước tính R1 × 50k + R2 × 30k/tháng
- [ ] **Cơ chế hạch toán AhaPoints**: điểm tích lũy được hạch toán khi nào? (EARNED vs REDEEMED)
- [ ] **Liability ước tính**: tổng RESERVED pts chưa đổi = liability bao nhiêu/quý?
- [ ] **Bảo hiểm tai nạn R1**: ký kết đối tác bảo hiểm, phí 10k/285pts và 30k/857pts có hợp lệ?
- [ ] **Partner rewards catalog**: cơ chế thanh toán với các đối tác (F&B voucher, xăng...)
- [ ] Xác định **threshold điểm tối thiểu để đổi** (tránh micro-redemption gây cost cao)

---

### ⚖️ LEGAL/RISK TEAM — Compliance

- [ ] **Điều khoản bảo hiểm tai nạn R1**: review hợp đồng, coverage limit, exclusions
- [ ] **Points không phải tiền tệ**: xác nhận AhaPoints không thuộc phạm vi pháp lý tiền điện tử
- [ ] **GDPR/Data privacy**: PointTransaction logs lưu trữ bao lâu? Ai được access?
- [ ] **Fraud risk**: đánh giá rủi ro tài xế giả mạo chuyến để tích điểm (cần Anti-fraud rule)
- [ ] **Điều khoản sử dụng AhaBenefits**: cần cập nhật T&C với driver

---

### 🤝 PARTNER TEAM (nếu có) — Catalog & Redemption

- [ ] Danh sách đối tác cung cấp rewards trong Catalog (F&B, xăng, bảo dưỡng...)
- [ ] API integration cho redemption flow (partner confirm trong ≤30 giây)
- [ ] SLA đối tác: xử lý timeout, hoàn điểm flow
- [ ] Coverage theo thành phố: đối tác nào có ở SGN, HAN hay toàn quốc?

---

## 📅 TIMELINE ĐỀ XUẤT

| Giai đoạn | Timeline | Mục tiêu chính |
|:---|:---:|:---|
| **Sprint 0 — Kick-off & Alignment** | Tuần 1–2 | Giải quyết 9 Open Questions của Product, confirm budget Finance |
| **Sprint 1–2 — Foundation** | Tuần 3–6 | Data model, DQS engine, Layer cascade logic |
| **Sprint 3–4 — Core Features** | Tuần 7–10 | AhaPoints flow, AhaBenefits catalog, Notification system |
| **Sprint 5 — Edge Cases & Admin** | Tuần 11–12 | Xử lý 5 edge cases, CS Admin tool, SOP training |
| **Beta Launch (R1+R2 only)** | Tuần 13–14 | Pilot với ~5.250 drivers (R1+R2), monitor KPIs |
| **Full Launch** | Tuần 15–16 | Rollout toàn fleet, activate R3 & Unranked tier |

---

## 📊 VALUE REALIZATION — Tác Động Dự Kiến

| Hiện trạng (Current State) | Chuyển đổi | Trạng thái Mục tiêu | Tác động |
|:---|:---:|:---|:---|
| AR/FR/Rating riêng lẻ, không có điểm tổng hợp | → **DQS Engine** | 1 điểm duy nhất phản ánh toàn diện chất lượng tài xế | ***Giảm 60% complexity trong xét rank*** |
| Tài xế chất lượng cao không được ưu tiên nhận đơn | → **Layer Cascade** | R1 nhận đơn L2 Minizone, earn lên đến 65k/h | ***Tăng 35% thu nhập bình quân R1*** |
| Không có cơ chế gắn kết dài hạn cho tài xế | → **AhaBenefits + Point Economy** | Driver LTV tăng, Churn Rate R1/R2 giảm | ***Giảm 20% Churn Rate tài xế chất lượng*** |
| Incentive budget phân tán, khó audit | → **Full-day Guarantee có điều kiện** | Budget gắn với KPI rõ ràng (App online ≥95%, AR=100%) | ***Giảm 30% budget lãng phí do fraud/low-quality*** |
| Thiếu dữ liệu điểm số để ra quyết định | → **PointTransaction + Wallet data model** | Dashboard real-time Fleet Ratio, Point Economy Health | ***100% visibility vận hành điểm thưởng*** |

---

*Driver Management Team · Ahamove · Kick-off Document v1.0 · 2026-06-04*
