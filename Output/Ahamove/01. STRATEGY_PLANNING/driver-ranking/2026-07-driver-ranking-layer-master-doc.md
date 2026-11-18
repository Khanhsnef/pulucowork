# 📊 BÁO CÁO CHIẾN LƯỢC: CHUẨN HÓA HỆ THỐNG XẾP HẠNG ĐỐI TÁC (DRIVER RANKING) & PHÂN LỚP VÙNG (LAYER ALLOCATION) v2.0

> **Cơ quan ban hành:** Driver Management Team & Strategy & Planning (S&P)  
> **Áp dụng:** Toàn hệ thống Ahamove (SGN & HAN) · **Phiên bản:** Final Master Release v2.0 (Tháng 07/2026)  
> **Đối tượng phổ biến:** Stakeholders (Board of Directors, Operations, Product, BI, Strategy & Planning, Partnership)

---

## 1. TÓM TẮT THỰC THI (EXECUTIVE SUMMARY)

### 📊 Executive Summary
Dự án **Driver Ranking & Layer Allocation System v2.0** tái cấu trúc mô hình quản trị nguồn cung của Ahamove. Hệ thống tập trung vào cơ chế **điều phối nguồn cung tự vận hành**:

1. **Phân định rõ Ranh giới Layer vs Rank**:
   - **RANK (Thứ hạng tài xế - 5 Tier):** Quyết định **Hệ số nhân tích điểm AhaPoints** (SUPER $\times 1.5$, PRO $\times 1.3$, SEMI_PRO $\times 1.1$, AMATEUR/UNRANKED $\times 1.0$), **Khung giờ ưu tiên đăng ký ca (Priority Window)**, **Đặc quyền phúc lợi phi tiền mặt** (Voucher Xăng/EV, Bảo hiểm tai nạn, Gói khám sức khỏe), **Ưu tiên cấp phát CCDC (Driver Kit)** và **Tham gia sự kiện Ahamove**.
   - **LAYER (Vùng hoạt động):** Định nghĩa **Bán kính / Phạm vi hoạt động** (L2 $\le 4\text{km}$, L3 $\le 8\text{km}$, L4 Bigzone, L5 Cityzone, L6 MASS), **Sự hỗ trợ của Đội trưởng**, và **Cơ chế Đăng ký ca cắm vùng**.
2. **Cơ chế Ưu tiên Gán Đơn Trong Layer (Intra-Layer Dispatch Priority)**:
   - **LAYER CÓ CA (L2–L5):** Thuật toán **Ưu tiên gán cho Tài xế ĐÃ ĐĂNG KÝ CA tại Layer đó trước** (quét theo Rank trong ca).
   - **LAYER MASS (L6 On-Demand Tự Do):** Do L6 không có đăng ký ca trước, thuật toán **ƯU TIÊN TRỰC TIẾP THEO RANK THỨ HẠNG TÀI XẾ**:
     $$\text{SUPER} \longrightarrow \text{PROFESSIONAL} \longrightarrow \text{SEMI\_PROFESSIONAL} \longrightarrow \text{AMATEUR} \longrightarrow \text{UNRANKED}$$
3. **Mở Đăng Ký Ca Kíp Hàng Tuần Tại Cityzone (L5) & Gợi Ý Zone Thông Minh**:
   - Chấp nhận cho tài xế đăng ký ca kíp hàng tuần (Weekly Shift Registration) tại Cityzone (L5) để tạo thói quen cắm vùng.
   - Tích hợp tính năng **Smart Zone Recommendation** gợi ý khu vực hoạt động tối ưu cho tài xế dựa trên lịch sử chạy, địa điểm cư trú và Demand Heatmap.

### 🎯 Mục tiêu Kinh doanh (Business Objectives)
- **Tối ưu hóa CPO (Cost per Order):** Chuyển dịch toàn bộ chi phí thưởng sang hệ thống tích điểm **AhaPoints biến đổi theo Rank** và phúc lợi đối tác tài trợ.
- **Tự động điều phối cung - cầu:** Tăng tỷ lệ lấp đầy ca làm việc tại L2 Minizone và L3 Mediumzone bằng lực hút nhân điểm Rank và quyền ưu tiên gán đơn cho tài xế cắm ca.

### 📈 Chỉ số Cốt lõi (Important KPIs)
- **Tiêu chuẩn Rank & Hệ số tích điểm:**
  - **SUPER:** DQS $\ge 80$, $\text{stp} \ge 240$ $\rightarrow$ **Nhân điểm $\times 1.5$**
  - **PROFESSIONAL:** DQS $\ge 75$, $\text{stp} \ge 150$ $\rightarrow$ **Nhân điểm $\times 1.3$**
  - **SEMI_PROFESSIONAL:** DQS $\ge 75$, $\text{stp} \ge 70$ $\rightarrow$ **Nhân điểm $\times 1.1$**
  - **AMATEUR & UNRANKED:** DQS $< 75$ hoặc $\text{stp} < 70$ $\rightarrow$ **Base $\times 1.0$**
- **Fulfillment Rate (FR):** Đạt **≥ 90%** tại **L2 Minizone** và **L3 Mediumzone** vào các khung ca cao điểm.
- **Phân bổ Fleet Target:** **SUPER (10–15%)**, **PROFESSIONAL (15–20%)**, **SEMI_PROFESSIONAL (30–35%)**, **AMATEUR (20–25%)**, **UNRANKED (5-10%)**.

---

## 2. KHUNG PHÂN TÍCH (ANALYSIS FRAMEWORK)

### 2.1 Phân tích Phân Định Rạch Ròi: LAYER vs RANK

Để loại bỏ sự chồng chéo và mập mờ trong chính sách cũ, phiên bản v2.0 thiết lập bảng ma trận phân định chức năng duy nhất:

| Tiêu Chí Phân Định | LAYER (Vùng Hoạt Động L1–L6) | RANK (Thứ Hạng Tài Xế 5 Tier) |
| :--- | :--- | :--- |
| **Bản chất** | Định nghĩa **Không gian & Điều kiện làm việc** | Định nghĩa **Năng lực & Đóng góp của Tài xế** |
| **Hệ số Tích điểm AhaPoints** | Định nghĩa môi trường cắm vùng (bán kính/cự ly) | **QUYẾT ĐỊNH HỆ SỐ NHÂN TÍCH ĐIỂM (`rank_multiplier`)**<br/>• SUPER: **× 1.5**<br/>• PROFESSIONAL: **× 1.3**<br/>• SEMI_PROFESSIONAL: **× 1.1**<br/>• AMATEUR / UNRANKED: **× 1.0** |
| **Hỗ trợ Vận hành** | **Đội trưởng cắm vùng** (L2 & L3) | VIP CSKB Support (Dành riêng cho SUPER) |
| **Quyền Ưu tiên Đăng ký Ca** | Mở slot ca theo khả năng chứa | **QUYẾT ĐỊNH KHUNG GIỜ MỞ CỔNG (Priority Window)**<br/>• SUPER: 00:00 - 10:00 (Mở chọn trước tất cả Zone)<br/>• PRO: 10:00 - 14:00<br/>• SEMI_PRO: 14:00 - 24:00<br/>• AMATEUR/UNRANKED: Ngày 02+ |
| **Cơ chế Gán Đơn trong cùng Layer** | • **L2–L5:** Ưu tiên Tài xế ĐĂNG KÝ CA trước.<br/>• **L6 MASS:** Quét gán đơn trực tiếp theo thứ tự RANK. | **ƯU TIÊN THEO HẠNG RANK (SUPER ➔ PRO ➔ SEMI_PRO)**<br/>Tại L6 MASS: Tài xế Rank SUPER được quét ưu tiên nhận đơn đầu tiên. |
| **Phúc lợi Vật thể & Phi Tiền Mặt** | Cơ sở vật chất tại Hub | **ĐẶC QUYỀN TRỰC TIẾP THEO RANK**<br/>Voucher Xăng/EV cố định, Bảo hiểm tai nạn, Gói khám sức khỏe, Ưu tiên cấp phát Đồng phục/Driver Kit, Ưu tiên mời tham gia Sự kiện/Gala Ahamove |

---

### 2.2 Phân tích Đề xuất Kỹ thuật (Prescriptive Technical Specifications)

---

#### 📌 ĐỀ XUẤT 1: BỘ TIÊU CHÍ XẾP HẠNG (5-TIER DRIVER TAXONOMY) & HỆ SỐ TÍCH ĐIỂM

| Thứ Hạng (Rank Key) | Tên Tiếng Việt | Chỉ Số DQS | Năng Suất (stp / tháng) | Hệ Số Điểm Rank (`rank_multiplier`) | Quyền Hạn Đăng Ký Zone & Khung Giờ Mở Cổng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SUPER 💎** | **Siêu cấp** | **DQS ≥ 80** | **stp ≥ 240** | **× 1.5** *(Cao nhất)* | **00:00 – 10:00 (Ngày 01):** Được ưu tiên đăng ký trước vào **TẤT CẢ các Zone (L2 – L6)** |
| **PROFESSIONAL 🥇** | **Chuyên nghiệp** | **DQS ≥ 75** | **stp ≥ 150** | **× 1.3** | **10:00 – 14:00 (Ngày 01):** Được đăng ký vào các slot còn lại của **tất cả các Zone (L2 – L6)** |
| **SEMI_PROFESSIONAL 🥈**| **Bán chuyên** | **DQS ≥ 75** | **stp ≥ 70** | **× 1.1** | **14:00 – 24:00 (Ngày 01):** Được đăng ký vào các slot còn lại của **tất cả các Zone (L2 – L6)** |
| **AMATEUR 🥉** | **Phổ thông** | **DQS < 75** *hoặc* | **stp < 70** | **× 1.0** *(Base)* | **Từ Ngày 02 trở đi:** Chỉ được chọn các slot trống còn lại tại **L5 Cityzone & L6 MASS** |
| **UNRANKED 🆕** | **Chưa xếp hạng** | *Chưa có data* | *Chưa có đơn* | **× 1.0** *(Base)* | **Từ Ngày 02 trở đi:** Chỉ được chọn các slot trống còn lại tại **L5 Cityzone & L6 MASS** |

---

#### 📌 ĐỀ XUẤT 2: THUẬT TOÁN QUÉT GÁN ĐƠN THEO TỪNG LAYER (INTRA-LAYER DISPATCH PRIORITY)

##### 1. Cơ Chế Quét Đơn Từng Layer
Khi một đơn hàng mới phát sinh, thuật toán Matching quét tài xế được phân định theo 2 kịch bản Layer:

- **KỊCH BẢN A: Dành cho các Layer có Đăng ký ca (L2 Minizone, L3 Mediumzone, L4 Bigzone, L5 Cityzone):**
  - **Ưu tiên 1:** Quét nhóm **Tài xế ĐÃ ĐĂNG KÝ CA** tại Zone đó đang trong ca làm việc (`In-Shift SUPER` $\rightarrow$ `In-Shift PRO` $\rightarrow$ `In-Shift SEMI_PRO`).
  - **Ưu tiên 2:** Nếu hết tài xế trong ca mới mở rộng quét nhóm tài xế ngoài ca/vãng lai theo Rank (`Off-Shift SUPER` $\rightarrow$ `Off-Shift PRO` $\rightarrow$ ...).

- **KỊCH BẢN B: Dành riêng cho Layer 6 MASS (On-Demand Tự Do):**
  - Vì Layer 6 MASS không có cơ chế đăng ký ca cố định, hệ thống **ƯU TIÊN TRỰC TIẾP THEO RANK THỨ HẠNG TÀI XẾ**:
    $$\text{SUPER} \longrightarrow \text{PROFESSIONAL} \longrightarrow \text{SEMI\_PROFESSIONAL} \longrightarrow \text{AMATEUR} \longrightarrow \text{UNRANKED}$$
  - Tài xế Rank **SUPER** đang cắm app tự do tại L6 MASS luôn là người đầu tiên được hệ thống gửi đơn match trước các thứ hạng còn lại!

---

#### 📌 ĐỀ XUẤT 3: ĐĂNG KÝ CA KÍP HÀNG TUẦN TẠI CITYZONE (L5) & GỢI Ý ZONE THÔNG MINH

##### 1. Đăng Ký Ca Kíp Hàng Tuần (Weekly Shift Registration in L5 Cityzone)
- **Cơ chế:** Bên cạnh ca tháng, **L5 Cityzone CÓ chấp nhận đăng ký ca kíp theo tuần**. Cổng đăng ký ca tuần mở vào **12:00 Chủ Nhật hàng tuần** cho tuần làm việc tiếp theo.
- **Mục tiêu:** Tạo điều kiện linh hoạt cho nhóm tài xế bán chuyên (SEMI_PROFESSIONAL) và phổ thông (AMATEUR) chủ động lịch trình cá nhân mà vẫn đảm bảo sự cam kết cắm vùng.

##### 2. Tính Năng Gợi Ý Zone Thông Minh (Smart Zone Recommendation System)
Hệ thống AI/ML trên App Tài xế tự động phân tích và đưa ra **Top 3 Zone Gợi Ý** cho tài xế đăng ký ca/hoạt động lại dựa trên 4 tiêu chí:
1. **Lịch sử khu vực hoạt động hiệu suất cao nhất** của tài xế trong 30 ngày gần nhất.
2. **Vị trí địa lý cư trú** (home location) để giảm quãng đường di chuyển rỗng đến ca.
3. **Bản đồ Nhiệt Nguồn Cung - Nhu Cầu (Demand Heatmap)** dự báo cho tuần tới.
4. **Hạng tài xế (Rank):** Gợi ý các Zone phù hợp nhất với khung giờ ưu tiên của tài xế.

---

#### 📌 ĐỀ XUẤT 4: HỆ THỐNG PHÂN LỚP VÙNG (LAYER L1–L6)

| Layer | Tên Layer | Bán kính / Phạm vi | Đội Trưởng Hỗ Trợ | Cơ chế Đăng ký & Quy tắc Gán đơn |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | **KA / MP** | Gán trực tiếp kho KA | ❌ | Gán trực tiếp (Assigned) cho đối tác KA |
| **L2** | **Minizone** | Bán kính ngắn **≤ 4km** | ✅ **Đội trưởng + VIP Support** | Đăng ký ca tháng · **Ưu tiên Ca ➔ Rank** |
| **L3** | **Mediumzone**| Bán kính trung bình **≤ 8km**| ✅ **Đội trưởng hỗ trợ** | Đăng ký ca tháng · **Ưu tiên Ca ➔ Rank** |
| **L4** | **Bigzone** | Vùng Quận / Huyện | ❌ (CSKB tiêu chuẩn) | Đăng ký ca tháng · **Ưu tiên Ca ➔ Rank** |
| **L5** | **Cityzone** | Toàn Thành phố | ❌ | Đăng ký ca tuần & ca tháng · **Ưu tiên Ca ➔ Rank** |
| **L6** | **MASS** | Toàn hệ thống | ❌ | On-demand tự do · **ƯU TIÊN THUẦN RANK (SUPER ➔ PRO ➔ SEMI_PRO)** |

---

#### 📌 ĐỀ XUẤT 5: BẢNG TỔNG HỢP ĐẶC QUYỀN PHÚC LỢI THEO RANK (RANK ENTITLEMENTS)

| Danh Mục Quyền Lợi | SUPER 💎 (Siêu cấp) | PROFESSIONAL 🥇 (Chuyên nghiệp) | SEMI_PROFESSIONAL 🥈 (Bán chuyên) | AMATEUR 🥉 & UNRANKED 🆕 |
| :--- | :--- | :--- | :--- | :--- |
| **Hệ số Tích điểm AhaPoints** | **× 1.5** *(Cao nhất)* | **× 1.3** | **× 1.1** | × 1.0 (Base) |
| **Ưu tiên Gán đơn L6 MASS** | **Ưu tiên 1 (Số 1)** | **Ưu tiên 2** | **Ưu tiên 3** | Baseline FCFS |
| **Khung giờ mở đăng ký ca (Priority Window)** | **00:00 – 10:00** *(Sớm nhất, chọn mọi Zone)* | **10:00 – 14:00** *(Chọn mọi Zone)* | **14:00 – 24:00** *(Chọn mọi Zone)* | Ngày 02 trở đi *(Chỉ L5 & L6)* |
| **Voucher Xăng Petrolimex / Sạc EV VinFast** | **50.000 VNĐ / tháng** *(Cố định)* | **30.000 VNĐ / tháng** *(Cố định)* | Đổi bằng điểm AhaPoints | Không hỗ trợ |
| **Bảo hiểm Tai nạn Cá nhân Mini** | **Hỗ trợ 100%** *(Đăng ký gói 1k/3k pts)* | — | — | — |
| **Ưu tiên Cấp phát CCDC (Driver Kit)** | **Ưu tiên 1** *(Tặng Combo Áo + Túi)* | **Ưu tiên 2** *(Giảm 50% giá CCDC)* | Đổi bằng điểm AhaPoints | Mua giá niêm yết |
| **Ưu tiên Tham gia Sự kiện Ahamove** | **Vé VIP Gala & Sự kiện Vinh danh** | **Ưu tiên Mời tham dự** | Đăng ký theo slot tự do | — |
| **Bảo dưỡng Xe & Khám sức khỏe** | Gói Bảo dưỡng + Khám tổng quát | Gói Bảo dưỡng tiêu chuẩn | Đổi bằng điểm AhaPoints | — |

---

### 2.3 Lộ Trình Triển Khai Thực Tế (Realistic Execution Roadmap)

```text
📌 LỘ TRÌNH TRIỂN KHAI THỰC TẾ (REALISTIC EXECUTION ROADMAP):

• Giai đoạn 1: Hiện tại (Tháng 07/2026) — Chuẩn Hóa Phân Hạng Ranking 5-Tier
  - Áp dụng đổi trước tiêu chuẩn phân hạng Ranking 5-Tier (SUPER, PROFESSIONAL, SEMI_PRO, AMATEUR, UNRANKED) dựa trên DQS & Năng suất (stp).

• Giai đoạn 2: Dự kiến Tháng 08 – 09/2026 — Triển Khai Hệ Số Tích Điểm Theo Rank
  - Triển khai thuật toán tính điểm AhaPoints theo hệ số nhân Rank (SUPER x1.5, PRO x1.3, SEMI_PRO x1.1, AMATEUR/UNRANKED x1.0).

• Giai đoạn 3: Trong Quý 3 (Tháng 09/2026) — Backend AhaPoints & UI/UX App
  - Triển khai hệ thống tính toán AhaPoints backend và hoàn thiện giao diện UI/UX hiển thị điểm/hạng trên App Tài xế.

• Giai đoạn 4: Kế Hoạch Phúc Lợi Phi Tiền Mặt (In Planning / Partnership)
  - Hoàn thiện kế hoạch & đàm phán thương lượng với đối tác (Petrolimex, VinFast EV, PTI) để phát hành Voucher Xăng/EV & Bảo hiểm tai nạn.
```

---

## 3. 📈 HIỆN THỰC HÓA GIÁ TRỊ (VALUE REALIZATION)

### Bảng Đo Lường Tác Động Kinh Doanh (Measurable Business Impact)

| Hiện trạng (Current State) | Chuyển đổi (Transformation) | Trạng thái Mục tiêu (Target State) | Tác động Kinh doanh (Measurable Impact) |
| :--- | :--- | :--- | :--- |
| Duy trì chi phí cố định không hiệu quả. | ↓ **CHUYỂN DỊCH SANG AHAPOINTS VÀ QUÀ TÀI TRỢ** ↓ | Chuyển 100% thưởng sang tích điểm **AhaPoints biến đổi theo Rank** & đối tác tài trợ. | ***Tối ưu hóa tổng chi phí CPO thực tế.*** |
| Nhầm lẫn giữa quyền lợi Hạng tài xế và đặc tính Vùng hoạt động. | ↓ **PHÂN ĐỊNH RẠCH RÒI LAYER VS RANK** ↓ | Rank quyết định **Hệ số nhân điểm (SUPER: x1.5)** & Phúc lợi; Layer quyết định **Bán kính & Đăng ký ca**. | ***Minh bạch hóa 100% chính sách vận hành; loại bỏ tranh chấp quyền lợi của đối tác.*** |
| Tài xế Rank cao chạy tại L6 MASS bị cào bằng quyền lợi gán đơn với tài xế mới. | ↓ **GÁN ĐƠN L6 MASS THUẦN THEO RANK** ↓ | Tại L6 MASS, gán đơn ưu tiên trực tiếp theo thứ tự Rank: **SUPER ➔ PRO ➔ SEMI_PRO**. | ***Tăng 35% hài lòng & giữ chân 80% tài xế Rank cao khi chạy tự do.*** |

---
*Tài liệu Final Master này đã được làm sạch và hoàn thiện chuẩn mực để trình duyệt cấp Board of Directors và triển khai đồng bộ cho các Stakeholders.*
