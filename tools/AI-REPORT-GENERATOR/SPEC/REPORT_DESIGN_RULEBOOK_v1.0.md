# 📘 AHAMOVE DRIVER MANAGEMENT — REPORT DESIGN RULEBOOK v1.0

> **Mục tiêu hệ thống:** Giữ nguyên nhận diện thương hiệu hiện tại, nhưng chuyển đổi report từ *"tập hợp các thẻ (collection of cards)"* thành **"Báo cáo vận hành định hướng ra quyết định (Decision-Oriented Operating Report)"**.

---

## 📑 MỤC LỤC
1. [I. DESIGN PHILOSOPHY](#i-design-philosophy)
2. [II. CANVAS RULES](#ii-canvas-rules)
3. [III. CONTENT DENSITY](#iii-content-density)
4. [IV. INFORMATION HIERARCHY](#iv-information-hierarchy)
5. [V. KPI RULES](#v-kpi-rules)
6. [VI. LAYOUT RULES (8 Layout Archetypes)](#vi-layout-rules)
7. [VII. GRID RULES](#vii-grid-rules)
8. [VIII. CARD RULES](#viii-card-rules)
9. [IX. TEXT RULES](#ix-text-rules)
10. [X. INSIGHT ENGINE RULES](#x-insight-engine-rules)
11. [XI. INSIGHT STRUCTURE](#xi-insight-structure)
12. [XII. DRIVER VOICE RULES](#xii-driver-voice-rules)
13. [XIII. CHART RULES](#xiii-chart-rules)
14. [XIV. TABLE RULES](#xiv-table-rules)
15. [XV. GOVERNANCE RULES](#xv-governance-rules)
16. [XVI. ACTION RULES](#xvi-action-rules)
17. [XVII. MANAGEMENT TAKEAWAY RULES](#xvii-management-takeaway-rules)
18. [XVIII. AUTO-BALANCE ENGINE](#xviii-auto-balance-engine)
19. [XIX. AUTO-FILL MODULE RULES](#xix-auto-fill-module-rules)
20. [XX. VISUAL RHYTHM RULES](#xx-visual-rhythm-rules)
21. [XXI. COLOR RULES](#xxi-color-rules)
22. [XXII. TYPOGRAPHY RULES](#xxii-typography-rules)
23. [XXIII. CONTENT PRIORITY](#xxiii-content-priority)
24. [XXIV. DATA INTEGRITY RULES](#xxiv-data-integrity-rules)
25. [XXV. QUALITY CONTROL](#xxv-quality-control)
26. [XXVI. SLIDE SCORE (100pt Matrix)](#xxvi-slide-score)
27. [XXVII. AUTOMATIC SLIDE TYPE DETECTION](#xxvii-automatic-slide-type-detection)
28. [XXVIII. INFORMATION GAIN RULE](#xxviii-information-gain-rule)
29. [XXIX. RULE RIÊNG CHO PAGE VOC VÀ GOVERNANCE](#xxix-rule-rieng-cho-page-voc-va-governance)
30. [XXX. QUY TẮC TỐI CAO & KIẾN TRÚC 4 TẦNG](#xxx-quy-tac-toi-cao--kien-truc-4-tang)

---

## I. DESIGN PHILOSOPHY

### Rule 01 — Không redesign nhận diện thương hiệu
Tuyệt đối giữ nguyên hệ thống nhận diện:
- Font chữ: `Inter`, `-apple-system`, `sans-serif`.
- Bảng màu: Navy (`#0E4174`), Orange (`#FF7F32`), Green (`#10B981`), Red (`#EF4444`), Yellow (`#F59E0B`), Blue (`#0284C7`).
- Border radius, Card language, 16:9 canvas, Header, Footer, Status pills, Editable HTML.
- Không tạo ra visual language hoàn toàn mới.

### Rule 02 — Thay đổi "composition", không thay đổi "identity"
Hai slide có thể dùng chung font, màu sắc, viền, bóng đổ và khoảng cách nhưng **không bắt buộc phải cùng layout**:
- **Retention:** `KPI + Trend + Segment Breakdown`
- **Driver Voice (VOC):** `Quote + Journey + Operational Impact + Action`
- **Governance:** `Status Pulse + Priority Actions + Strategic Tracker`
- **Initiative:** `Timeline + Progress Pipeline + Impact`

---

## II. CANVAS RULES

### Rule 03 — Canvas cố định
- Định dạng 16:9 chuẩn `1920px × 1080px` logical canvas.
- Tất cả các component phải responsive bên trong khung canvas này.

### Rule 04 — Thiết lập vùng an toàn (Safe Margins)
- Top: `24–32px` | Left: `32px` | Right: `32px` | Bottom: `24px`.
- Không có bất kỳ component nào được phép chạm dính mép viền.

### Rule 05 — Header không được chiếm quá nhiều
- Header tối đa: `10–12%` chiều cao slide.
- Cấu trúc: `[Section Tag] ➔ TITLE ➔ Takeaway Subtitle`.
- Không để title và takeaway thành một block văn bản quá cao.

---

## III. CONTENT DENSITY

### Rule 06 — Không stretch card theo slide
- **CẤM:** `height: 100%;` hoặc `min-height: 600px;` nếu nội dung thực tế không yêu cầu.
- Card phải: `height: auto; min-height: 0; align-self: start;` để ôm vừa vặn nội dung.

### Rule 07 — Content density target
- Mỗi slide thông thường phải sử dụng khoảng **70–90% usable canvas** (không tính header, footer và margin).

### Rule 08 — Hero slide được phép sparse
- Nếu slide là cover, major milestone, key message hoặc section divider $\rightarrow$ có thể dùng **40–70% canvas**. Không cố lấp đầy rỗng.

### Rule 09 — Sparse slide detector
Tự động tính mật độ: `density = actualContentHeight / usableContentHeight`
| Density | Trạng Thái |
| :--- | :--- |
| `<30%` | 🔴 Too Sparse |
| `30–50%` | 🟠 Sparse |
| `50–70%` | 🟡 Acceptable |
| `70–90%` | 🟢 Optimal |
| `90–100%` | 🟠 Dense |
| `>100%` | 🔴 Overflow |

### Rule 10 — Sparse không được giải quyết bằng thêm chữ
- Nếu `density < 50%`, **tuyệt đối không tự động thêm paragraph text**.
- Ưu tiên bổ sung Visual Modules: Chart, Ranking, KPI Strip, Funnel, Timeline, Journey, Comparison, Insight Card, Action Framework, Evidence.

---

## IV. INFORMATION HIERARCHY

### Rule 11 — Mỗi slide chỉ có 1 Primary Message
- Ví dụ: *"SGN Retention giảm 5.4pp MoM"*. Không để 3 headline ngang hàng gây nhiễu.

### Rule 12 — Mỗi slide tối đa 3 supporting insights
- Cấu trúc: `PRIMARY MESSAGE ➔ Insight 1 ➔ Insight 2 ➔ Insight 3 ➔ ACTION`.

### Rule 13 — Mỗi slide phải trả lời 3 câu hỏi
- **WHAT?** (Điều gì xảy ra?)
- **WHY?** (Tại sao?)
- **SO WHAT / ACTION?** (Cần làm gì?)

### Rule 14 — Không lặp lại cùng một insight
- Loại bỏ hoàn toàn sự lặp lại giữa block Highlight và Lowlight.

---

## V. KPI RULES

### Rule 15 — KPI chỉ dùng khi có ý nghĩa
- Không tạo KPI card chỉ để lấp khoảng trống. Mỗi KPI phải có ít nhất 1 yếu tố: Target, Delta, Benchmark, Status, Trend, hoặc Comparison.

### Rule 16 — KPI card chuẩn 4 tầng
- `LABEL` (11px Bold) $\rightarrow$ `VALUE` (42-48px Bold) $\rightarrow$ `DELTA` (▲ +0.7% MoM) $\rightarrow$ `TARGET / GAP` (Target 75.0% | Gap -0.8pp).

### Rule 17 — KPI value không quá dài
- Ưu tiên: `74.2%`, `+5.4pp`, `96.6%`, `13.0%`. Không để số lẻ rườm rà như `74.173829%`.

### Rule 18 — Tối đa 5 hero KPIs
- Thông thường `3–4 KPI` là tối ưu. 5 KPI chỉ dùng cho Executive Summary.

### Rule 19 — Không lặp delta
- Nếu tất cả KPI có cùng delta (VD: `▲ +0.7% MoM`), đúc kết thành `Overall: +0.7% MoM` ở header thay vì lặp 4 lần.

### Rule 20 — KPI phải có semantic direction (Metric Polarity)
- Retention ↑ = Tốt (Xanh) | Cancel Rate ↑ = Xấu (Đỏ). Engine phải nhận diện đúng hướng tích cực/tiêu cực của từng chỉ số.

---

## VI. LAYOUT RULES (8 Layout Archetypes)

- **Rule 21 — Layout A (Executive Dashboard):** Header + KPI Strip + Main Chart + Insight Matrix.
- **Rule 22 — Layout B (Trend Layout):** KPI + Trend Line Chart + Driver/Segment Breakdown + Action.
- **Rule 23 — Layout C (Comparison Layout):** So sánh đối đầu HAN vs SGN / Zone kèm Gap Indicators.
- **Rule 24 — Layout D (Funnel Layout):** Phễu chuyển đổi `REGISTERED ➔ ACTIVE ➔ RETAINED ➔ PRODUCTIVE`.
- **Rule 25 — Layout E (Heatmap Layout):** Ma trận bản đồ nhiệt phủ màu tint (`🟢 ON TRACK`, `🟡 WATCH`, `🔴 OFF TRACK`).
- **Rule 26 — Layout F (Initiative Layout):** Progress Pipeline (`PREP ➔ REGISTER ➔ LIVE ➔ VERIFY ➔ CLOSE`) + Impact Matrix.
- **Rule 27 — Layout G (Driver Voice Layout):** `QUOTE ➔ MECHANISM ➔ IMPACT ➔ SOLUTION ➔ SUCCESS METRIC`.
- **Rule 28 — Layout H (Governance Layout):** `STATUS PULSE ➔ PRIORITY ACTIONS ➔ DEADLINE ➔ ESCALATION`.

---

## VII. GRID RULES & ASYMMETRICAL RATIOS

### Rule 29 — Không mặc định 3 equal columns (Chống lặp 33% | 33% | 33%)
Áp dụng tỷ lệ bất đối xứng linh hoạt: `25 | 45 | 30`, `35 | 65`, `40 | 60`, `32 | 66`.

### Rule 30 — Grid phải content-aware
Điều chỉnh độ rộng cột dựa trên độ dài nội dung (Quote: 25%, Mechanism: 45%, Action/Framework: 30%).

### Rule 31 — Empty card không tồn tại
Nếu card có `< 3` phần tử có nghĩa, không cho phép card đó chiếm toàn bộ chiều cao.

---

## VIII. CARD RULES

### Rule 32 — Card không phải container để chứa khoảng trắng
Card chỉ tồn tại để nhóm thông tin, tạo visual hierarchy, highlight status và hỗ trợ comparison.

### Rule 33 — Card padding
Khuyến nghị `16–24px`. Tuyệt đối không để padding quá lớn làm loãng thông tin.

### Rule 34 — Card header tối đa 1 dòng
Rút gọn tiêu đề dài: ❌ *"Góc Nhìn Quản Trị & Đánh Giá Vận Hành"* $\rightarrow$ ✅ *"MANAGEMENT VIEW"*.

### Rule 35 — Không dùng icon chỉ để trang trí
Icon phải có ý nghĩa biểu đạt: 📊 Data | 🎯 Target | ⚠️ Risk | ✓ Done | 💡 Insight | 🚨 Escalation.

---

## IX. TEXT RULES

### Rule 36 — Không dùng paragraph dài
Một đoạn insight chỉ từ `1–2 câu`.

### Rule 37 — Bullet tối đa 3–5 items/card
Nếu trên 5 items $\rightarrow$ bắt buộc chuyển sang grouping hoặc ranking.

### Rule 38 — Một bullet chỉ chứa 1 ý
Tách đoạn văn thành từng dòng ngắn có điểm nhấn.

### Rule 39 — Highlight / Lowlight / Action phải tách thành modules độc lập
Không viết chung Highlight, Action và Driver Voice vào cùng 1 bullet card.

---

## X. INSIGHT ENGINE RULES (Business Logic)

- **Rule 40 — Biggest Gap:** `gap = actual - target`
- **Rule 41 — Biggest Improvement:** `max(delta)`
- **Rule 42 — Biggest Deterioration:** `min(delta)`
- **Rule 43 — Weakest Segment:** `min(segment_metric)`
- **Rule 44 — Best Segment:** `max(segment_metric)`
- **Rule 45 — Largest Gap Between Segments:** `max - min` (VD: FT 95.3% vs NLM 68.7% $\rightarrow$ Gap 26.6pp).
- **Rule 46 — Anomaly Detection:** Nếu `abs(delta) > historical_threshold` $\rightarrow$ cờ báo `⚠️ ANOMALY`.
- **Rule 47 — Concentration Mix Shift:** Phát hiện phân khúc chiếm >X% tổng sản lượng.

---

## XI. INSIGHT STRUCTURE

### Rule 48 — Insight phải có 4 tầng
`OBSERVATION ➔ DIAGNOSIS ➔ IMPLICATION ➔ ACTION`

### Rule 49 — Observation không được giả làm diagnosis
Chỉ kết luận nguyên nhân khi data chứng minh rõ ràng. Nếu chưa đủ bằng chứng, ghi: *"Potential driver: NLM churn — cần validate"*.

### Rule 50 — Confidence Level Rating
- **CONFIRMED:** Có data trực tiếp.
- **SUPPORTED:** Có nhiều chỉ báo hỗ trợ.
- **HYPOTHESIS:** Cần validation thêm.

---

## XII. DRIVER VOICE RULES (VOC)

- **Rule 51 — Quote phải giữ nguyên meaning:** Không paraphrase làm biến đổi thông điệp của tài xế.
- **Rule 52 — Quote phải có context:** Luôn đính kèm Segment tài xế và bối cảnh xảy ra.
- **Rule 53 — Quote phải chuyển thành Operational Mechanism:**
  `DRIVER SAYS ➔ SYSTEM ISSUE ➔ REWARD IMPACT ➔ BEHAVIOR IMPACT`
- **Rule 54 — VOC không được đứng một mình:** Slide VOC bắt buộc chứa: `Quote ➔ Mechanism ➔ Impact ➔ Action ➔ Success Criteria`.

---

## XIII. CHART RULES

- **Rule 55 — Chart phải trả lời 1 câu hỏi:** Không vẽ biểu đồ chỉ vì sẵn data.
- **Rule 56 — Chọn chart theo data type:**
  - Trend $\rightarrow$ Line Chart
  - Comparison $\rightarrow$ Bar Chart
  - Composition / Distribution $\rightarrow$ Donut Chart
  - Funnel $\rightarrow$ Funnel Matrix
  - Target $\rightarrow$ Progress Bar
  - Zone x KPI $\rightarrow$ Heatmap Matrix
  - Timeline $\rightarrow$ Pipeline Step Flow
- **Rule 57 — Donut chart chỉ dùng cho composition:** Donut không được chiếm >50% slide chỉ vì container cao.
- **Rule 58 — Chart size proportional to information:** Ít data points $\rightarrow$ Visual nhỏ/vừa.
- **Rule 59 — Không có chart nào không có Key Takeaway.**

---

## XIV. TABLE RULES

- **Rule 60 — Table chỉ dùng khi cần scan nhiều dimensions.** (Nếu chỉ có 2-3 dòng $\rightarrow$ chuyển thành Action Cards).
- **Rule 61 — Table không chứa paragraph:** Mỗi cell lý tưởng từ 1-2 dòng.
- **Rule 62 — Action table ưu tiên 5 columns:** `ITEM | WHY | ACTION | DEADLINE | PIC`.
- **Rule 63 — Status pills trực quan:** `🟢 ON TRACK`, `🟡 WATCH`, `🔴 OFF TRACK`, `🔵 DONE`.
- **Rule 64 — Sort action table theo urgency:** `OFF TRACK ➔ WATCH ➔ Deadline gần ➔ ON TRACK ➔ DONE`.

---

## XV. GOVERNANCE RULES

- **Rule 65 — Governance slide phải trả lời 4 câu:**
  1. *How healthy are we?*
  2. *What needs attention?*
  3. *Who owns it?*
  4. *When is deadline?*
- **Rule 66 — Status distribution không phải main story:** Donut chart chỉ là chỉ báo sức khỏe. Main story phải là **Priority Actions / Escalation Matrix**.
- **Rule 67 — Action tracker phải highlight deadline:** Làm nổi bật các mốc `TODAY`, `21 AUG`, `OVERDUE`.

---

## XVI. ACTION RULES

- **Rule 68 — Mỗi action phải có owner (PIC).** Nếu thiếu $\rightarrow$ gán `OWNER NEEDED`.
- **Rule 69 — Mỗi action phải có deadline.** Nếu thiếu $\rightarrow$ gán `TBD`.
- **Rule 70 — Action phải bắt đầu bằng động từ:**
  ❌ *"Push noti"* $\rightarrow$ ✅ *"Increase Push Noti frequency"*.
  ❌ *"Auto Check-in"* $\rightarrow$ ✅ *"Launch Auto Check-in feature"*.
- **Rule 71 — Action phải liên kết với insight:** `Problem ➔ Action ➔ Owner ➔ Deadline ➔ Success Metric`.

---

## XVII. MANAGEMENT TAKEAWAY RULES

- **Rule 72 — Mỗi slide có tối đa 1 Management Takeaway Banner.**
- **Rule 73 — Takeaway phải actionable:** ❌ *"Cần theo dõi sát sao"* $\rightarrow$ ✅ *"Ưu tiên xử lý NLM churn trong tuần này"*.
- **Rule 74 — 3 loại Management Banners:**
  - `INFORMATION:` *"SGN GDR duy trì 96.6%."*
  - `MANAGEMENT ATTENTION:` *"SGN Retention giảm 5.4pp MoM."*
  - `DECISION NEEDED:` *"Phê duyệt triển khai Auto Check-in trước 25/8."*

---

## XVIII. AUTO-BALANCE ENGINE

- **Rule 75 — Engine đo đạc actual bounding boxes:** Đo `contentHeight`, `availableHeight`, `freeSpace`.
- **Rule 76 — Nếu free space > 25%:** Tự động chèn Secondary Module theo thứ tự ưu tiên: `Insight ➔ Comparison ➔ Trend ➔ Ranking ➔ Flow ➔ KPI ➔ Timeline`.
- **Rule 77 — Nếu free space 10–25%:** Tự động scale vừa vặn chart, KPI, và spacing.
- **Rule 78 — Nếu free space < 10%:** Trạng thái Balanced, giữ nguyên.
- **Rule 79 — Nếu overflow:** Thứ tự xử lý: `Remove duplicate ➔ Shorten labels ➔ Convert paragraph to bullets ➔ Convert bullets to visual ➔ Reduce padding ➔ Reduce chart height ➔ Slightly reduce font`.

---

## XIX. AUTO-FILL MODULE RULES

Nếu slide bị sparse, engine tự chọn module phụ phù hợp với chủ đề:
- **Driver Voice:** `Journey ➔ Impact ➔ Success Metric`
- **KPI / Retention:** `Trend ➔ Segment Ranking ➔ Target Gap`
- **Governance:** `Governance Pulse ➔ Status Scorecard ➔ Deadline`
- **Initiative:** `Progress Pipeline ➔ Timeline ➔ Impact Matrix`
- **Zone:** `Heatmap Matrix ➔ Best/Worst Ranking`

---

## XX. VISUAL RHYTHM RULES

- **Rule 80 — Không quá 3 slide liên tiếp cùng composition.**
- **Rule 81 — Sau chart-heavy slide nên đổi sang visual khác** (Funnel, Heatmap, Action Tracker).
- **Rule 82 — Không dùng cùng 1 dominant visual liên tục.**

---

## XXI. COLOR RULES

- **Rule 83 — Không thêm palette mới:** Chỉ dùng Navy, Orange, Green, Red, Yellow, Blue.
- **Rule 84 — Màu phải có semantic:** Navy = Neutral/Primary | Orange = Attention/Highlight | Green = Healthy | Yellow = Watch | Red = Risk | Blue = Done.
- **Rule 85 — Không dùng màu chỉ để trang trí.**

---

## XXII. TYPOGRAPHY RULES

- **Rule 86 — Giữ nguyên font family (`Inter`).**
- **Rule 87 — Typography hierarchy cố định:** Slide title (26px) > Section title (16px) > Card title (15px) > Body (13px) > Meta (11px).
- **Rule 88 — Tối đa 3 font sizes trong 1 card:** `Label | Value | Supporting`.

---

## XXIII. CONTENT PRIORITY

Khi diện tích canvas không đủ, tuân thủ thứ tự ưu tiên:
- **KEEP:** `1. Primary KPI | 2. Primary Insight | 3. Root Cause | 4. Action | 5. Deadline / PIC`
- **REMOVE FIRST:** `1. Generic explanation | 2. Duplicate text | 3. Decorative labels | 4. Secondary commentary | 5. Long prose`

---

## XXIV. DATA INTEGRITY RULES

- **Rule 89 — Không tự bịa số liệu:** Insight Engine chỉ tính toán dựa trên data thực tế.
- **Rule 90 — Không tự biến correlation thành causation:** Đánh dấu *"Possible driver"* nếu chưa có bằng chứng xác thực.
- **Rule 91 — Không sửa data source silently:** Flag `⚠️ DATA CHECK` nếu phát hiện bất thường.
- **Rule 92 — Target phải có nguồn:** Không tự tạo Target Gap nếu không có chỉ tiêu AOP.

---

## XXV. QUALITY CONTROL & CHECKS

Trước khi xuất bản slide final, chạy tự động 5 bước QA:
- **Rule 93 — No overflow:** `scrollHeight <= clientHeight`
- **Rule 94 — No empty oversized cards:** Flag nếu `contentHeight / cardHeight < 25%`.
- **Rule 95 — No duplicate insight:** Loại bỏ trùng lặp giữa Highlight và Lowlight.
- **Rule 96 — No orphan chart:** Chart phải có Title, Data và Takeaway.
- **Rule 97 — No orphan action:** Action phải có Owner và Deadline.
- **Rule 98 — No slide without takeaway banner.**

---

## XXVI. SLIDE SCORE (100pt Matrix)

Mỗi slide tự động chấm điểm trên thang 100:
- Content Accuracy: **20pt**
- Density Optimization: **20pt**
- Hierarchy & Layout: **15pt**
- Insight Quality: **20pt**
- Actionability: **15pt**
- Visual Aesthetics: **10pt**

| Total Score | Trạng Thái |
| :--- | :--- |
| `90–100` | 🟢 Excellent |
| `75–89` | 🟢 Good |
| `60–74` | 🟡 Review Required |
| `<60` | 🔴 Redesign Mandatory |

---

## XXVII. AUTOMATIC SLIDE TYPE DETECTION

```javascript
if (hasTrend && hasTarget) return "trend";
if (hasSegments && hasTwoRegions) return "comparison";
if (hasRegistered && hasActive) return "funnel";
if (hasZoneMatrix) return "heatmap";
if (hasQuote) return "driver-voice";
if (hasDeadline && hasPIC) return "governance";
```

---

## XXVIII. INFORMATION GAIN RULE

Ưu tiên các Visual Module giúp ra quyết định nhanh nhất theo thứ tự:
`Problem Identification ➔ Root Cause ➔ Comparison ➔ Trend ➔ Action ➔ Supporting Detail`.

---

## XXIX. RULE RIÊNG CHO PAGE VOC VÀ GOVERNANCE

### Page 29 (VOC / Driver Voice):
Bắt buộc cấu trúc 3 cột bất đối ứng:
- **25% Driver Quote:** Cụm trích dẫn trực tiếp từ tài xế.
- **45% Operational Mechanism & Evidence:** Phân tích cơ chế kỹ thuật & ảnh hưởng thu nhập.
- **30% Success Criteria Framework:** Khung đo lường phục hồi (`Threshold 80% ➔ 75% | Reward Participation Recovery | Auto Check-in < 25/8`).

### Page 28 (Governance & Action Tracker):
Bắt buộc cấu trúc 2 cột bất đối ứng:
- **32% Governance Pulse Scorecard:** Sức khỏe vận hành (`🟢 48% ON TRACK | 🟠 27% WATCH | 🔴 12% OFF TRACK | NEXT DEADLINE: 21 AUG`).
- **66% Strategic Action Tracker Table:** Bảng hành động chiến lược xếp theo thứ tự ưu tiên cấp bách.

---

## XXX. QUY TẮC TỐI CAO & KIẾN TRÚC 4 TẦNG

### 🔟 10 LUẬT BẤT BIẾN TỐI CAO:
1. **One slide = one primary message.**
2. **WHAT ➔ WHY ➔ SO WHAT.**
3. **Card height follows content, not canvas.**
4. **Target density = 70–90%.**
5. **Whitespace > 25% ➔ Add meaningful visual/insight, never filler text.**
6. **No duplicate information.**
7. **Every KPI needs context: target / delta / benchmark / status.**
8. **Every insight must lead toward an action or implication.**
9. **Same brand system, different composition.**
10. **The report exists to support decisions, not to display all available data.**

---

### 🏗️ KIẾN TRÚC 4 TẦNG HỆ THỐNG (SYSTEM ARCHITECTURE):

```
┌──────────────────────────────────────────────────────────────┐
│                       DATA LAYER                             │
│   KPI / Table / Driver Voice / Event / Zone Performance Log  │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                     INSIGHT ENGINE                           │
│   Gap / Trend / Rank / Anomaly / VOC Mechanism / Density     │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                     LAYOUT ENGINE                            │
│   Dashboard / Trend / Funnel / VOC / Heatmap / Governance    │
└──────────────────────────────┬───────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│                     RENDER ENGINE                            │
│   Typography / Color / Card Auto-height / Density / QA       │
└──────────────────────────────┬───────────────────────────────┘
```

---

## XXXI. KNAFLIC STORYTELLING WITH DATA SUPREME LAWS

### Rule 99 — The Big Idea Mandate (Chapter 1)
- Slide 1 (Executive Summary) bắt buộc phải hiển thị **The Big Idea** thành một khối nổi bật (Focus Card):
  - 1 câu duy nhất kết hợp: (1) Góc nhìn chiến lược + (2) Rủi ro/Đánh đổi + (3) Hành động khuyến nghị.
  - Phải đi kèm **3-Minute Story Payload** cho sếp.

### Rule 100 — Chart Selection Taxonomy & Anti-Pattern Red Lines (Chapter 2)
- Chỉ sử dụng 12 dạng hiển thị trực quan tiêu chuẩn (Simple Text, Table, Heatmap, Scatterplot, Line Graph, Slopegraph, Bar Charts).
- **CẤM TỰ NÂNG NẤC VẼ KHÔNG CHUẨN:**
  - 🚫 **Tuyệt đối cấm Pie / Donut Charts**: Thay bằng Bar Chart sắp xếp giảm dần hoặc Slopegraph.
  - 🚫 **Tuyệt đối cấm 3D Charts**: Không dùng hiệu ứng 3D bóp méo thị giác.
  - 🚫 **Tuyệt đối cấm Trục Y kép (Dual Y-Axis)**: Thay bằng direct labeling hoặc chia làm 2 panel xếp chồng.

### Rule 101 — Decluttering & Gestalt Principles Enforcement (Chapter 3)
- Xóa bỏ 100% khung viền ô chart nặng nề (Chart borders).
- Làm nhạt gridlines về tông xám nhạt (`#F1F5F9` hoặc `#E2E8F0`).
- Xóa bỏ legends riêng lẻ ➔ Thay bằng **Direct Labeling** ngay tại điểm cuối của data series.

### Rule 102 — 90% Gray + Single Accent Color Rule (Chapter 4)
- **Màu nền baseline:** 90% các yếu tố phụ, baseline data series phải dùng màu xám trung tính (`#94A3B8`, `#64748B`, `#F1F5F9`).
- **Màu nhấn điểm tụ (Accent Focus):** Chỉ sử dụng 1 màu accent nổi bật (Orange `#FF7F32` hoặc Blue `#0E4174`) cho đúng 1 data series/metric quan trọng nhất cần thu hút mắt người xem.

### Rule 103 — Design Affordances & Visual Hierarchy (Chapter 5)
- Thẻ quan trọng nhất (Hero Card / Primary Recommendation) bắt buộc có **Focus Border** (`2px solid #FF7F32`) và nền sáng nhẹ (`#FFF7ED`).
- Thẻ phụ/ít ưu tiên giảm độ rực màu (opacity 0.75-0.85).

### Rule 104 — Horizontal & Vertical Logic (Chapter 7)
- **Horizontal Logic:** Đọc riêng danh sách Tiêu đề của các slide phải tạo thành một câu chuyện chiến lược hoàn chỉnh theo mạch (Plot ➔ Conflict ➔ Resolution ➔ Action).
- **Vertical Logic:** Nội dung chi tiết trong slide phải chứng minh trực tiếp cho Tiêu đề khẳng định phía trên.

---
*Tài liệu quy chuẩn AHAMOVE DRIVER MANAGEMENT — REPORT DESIGN RULEBOOK v1.0 được lưu trữ chính thức tại `AI-REPORT-GENERATOR/SPEC/REPORT_DESIGN_RULEBOOK_v1.0.md`.*
