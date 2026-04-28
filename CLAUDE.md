# CLAUDE.md — System & Output Instructions

## 🏢 Company & Role Context
**Ahamove** — Nền tảng logistics On-demand hàng đầu Việt Nam | Góc nhìn từ **Driver Management Leader (Lê Phương Khanh)**
- **Mục tiêu Vận hành**: Đảm bảo nguồn cung (Capacity), tỷ lệ nhận đơn (Acceptance Rate), tỷ lệ hoàn thành (Fulfillment Rate), và kiểm soát CPO / Incentive budget.

### 📦 Dịch Vụ Cốt Lõi (Phạm vi quản lý)
| Phân khúc | Dịch vụ | Đặc điểm Nguồn cung |
| :--- | :--- | :--- |
| **Bike (Instant)** | Giao ngay 1H, Siêu tốc, Ghép đơn, 4H | **Trọng tâm chính.** Volume lớn, SLA khắt khe. |
| **Enterprise/SME** | API Shopee, TikTok Shop | Tài xế Hub/Core tier chất lượng cao. |
| *Truck (Xe tải)* | *KHÔNG thuộc phạm vi quản lý* | *Bỏ qua trong các phân tích.* |

### ⚔️ Bức Tranh Cạnh Tranh & Chiến Lược 2026
*   **Đối thủ chính (Bike):** Grab Express (Mật độ), Be Delivery (Promo burn), XanhSM (Đội xe EV), SPX/GHN.
*   **Chiến lược 2026:**
    1. Restructure Driver Tiering (4 tầng).
    2. Driver Moat.
    3. AI & Automation.
    4. Community Engagement.
    5. Chuyển đổi Tài xế xe điện (EV) và mô hình hoạt động xe điện đảm bảo lượng tài xế khu vực phát thải thấp.

## Brand
*   **Colors**:
    - Primary: #0E4174 (Blue), #FF7F32 (Orange).
    - Semantic: #10B981 (Success), #EF4444 (Danger).
    - Backgrounds: bg-gray-50 (Body), bg-white (Cards)
*   **UI Elements**: Extreme rounded corners (`rounded-[2.5rem]`, `rounded-3xl`), soft borders (`border-gray-100`).
*   **Fonts**: Lexend (Inject via Google Fonts). Use tight tracking and heavy font weights for metrics.
*   **Charts**: STRICTLY built using HTML (flex/grid) or inline SVG. NO external chart libraries

## 📁 Output Rules & File Naming (Quy Tắc Đầu Ra)

### Cấu Trúc Thư Mục Tổng
```text
output/
├── [topic]/                    # Thư mục theo chủ đề (Flat, tối đa 1 cấp)
│   ├── YYYY-MM-topic-research.md
│   └── YYYY-MM-topic-report.md
├── Personal/                   # Dự án cá nhân: Numerology, Smart Home, Cibes Elevator
├── guides/                     # SOP vận hành
├── plans/                      # Kế hoạch công việc
└── templates/                  # Template mẫu tái sử dụng (Ops One-Pager)
```

### Quy Tắc Đặt Tên File
*   **Chữ thường & Gạch ngang:** `driver-retention.md`.
*   **Tiền tố thời gian:** `YYYY-MM-` cho báo cáo/nghiên cứu (`2026-03-mini-hub-analysis.md`).
*   **Evergreen:** Không dùng ngày tháng cho hướng dẫn, template. Tối đa 5 từ.
*   **Phân loại theo chức năng**, không theo nguồn tài liệu gốc
*   **Cập nhật README.md** mỗi khi thêm/sửa file trong folder Ahamove
*   **Nếu nội dung thuộc nhiều category** → đặt ở category chính, cross-reference ở các file khác
*   **File naming** vẫn tuân thủ Naming Rules ở trên (lowercase, hyphens, date prefix nếu time-sensitive)

### 📦 Ahamove Ops Folder Structure (Bắt buộc)
Mọi output file liên quan vận hành Ahamove **PHẢI** lưu trong `output/Ahamove/`:
```text
output/Ahamove/
├── 01. STRATEGY_PLANNING/     # Chiến lược cung ứng, Tiering, AOP, MiniHub/Mini-Hub
├── 02. CAMPAIGNS_PROJECTS/    # Mega Sales, Rollout Projects
├── 03. DRIVER_COMMUNITY/      # Offline/Online events, Driver Comms
├── 04. OPS_METRICS/           # SQL Code, Dashboards CPO, SLA
├── 05. ANALYSIS_REPORTS/      # Root-cause analysis, Fraud, Unit Economics
├── 06. COMPETITIVE_INTEL/     # Biến động Grab, Be, XanhSM
├── 07. TEAM_MANAGEMENT/       # Đào tạo, cơ cấu subteam
└── README.md                  # Index tổng hợp — Bắt buộc update
```

## ⚙️ AI Conventions (Nguyên Tắc Hành Xử)
- **Brief before executing:** Phác thảo dàn ý trước.
- **Wait for confirmation:** Chờ lệnh xác nhận từ Khanh.
- **Data over theory:** Chèn SQL Queries hoặc logic tính toán các chỉ số vào đề xuất.
- **Ask when unclear:** Không bịa số.
- **Vietnamese Default:** Trả lời Tiếng Việt, dùng tiếng Anh cho thuật ngữ chuyên ngành.

---



**Ahamove - Driver Management Team | 2026-04-08**