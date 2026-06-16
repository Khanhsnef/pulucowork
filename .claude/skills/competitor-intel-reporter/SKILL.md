---
name: competitor-intel-reporter
description: >-
  Quy trình tự động hóa thu thập tin tức, phân tích động thái đối thủ (Grab, Be, XanhSM) và biên dịch báo cáo MD sang HTML dễ đọc chuẩn thương hiệu Ahamove.
---

# Competitor Intel Reporter

## Overview
Skill này hướng dẫn Agent cách vận hành luồng giám sát cạnh tranh hàng ngày, bao gồm việc quét tin tức đối thủ, chạy phân tích bằng AI, tạo báo cáo markdown, biên dịch sang giao diện HTML tương tác chuẩn thương hiệu và cập nhật danh mục index.

## Prerequisites
*   Thư viện Python: `markdown`
*   Scripts hỗ trợ: `_scripts/crawl_competitor_intel.py` và `_scripts/md_to_html.py`

## Workflow

### 1. Thu thập Tín hiệu Cạnh tranh (Crawl News Signals)
*   Chạy script thu thập thông tin đối thủ bằng cách chạy lệnh:
    ```bash
    python3 _scripts/crawl_competitor_intel.py
    ```
*   Script này sẽ quét tin tức từ Google News RSS cho Grab, Be, và XanhSM, lọc tin trong vòng 3 ngày gần nhất và lưu vào file `output/Ahamove/06. COMPETITIVE_INTEL/monitoring/raw-signals.json`.

### 2. Phân tích Tín hiệu Mới (Analyze Signals)
*   Đọc nội dung file `raw-signals.json`.
*   Sử dụng persona của **Competitive Intelligence Analyst** để đánh giá các động thái mới nhất của đối thủ.
*   Cân nhắc tác động cụ thể lên Driver Acquisition, Driver Retention, Acceptance Rate (AR), Fulfillment Rate (FR), CPO, và Incentive pressure của Ahamove.
*   Tính toán độ tin cậy của thông tin theo khung đánh giá **FAROUT Score (x/60)**.

### 3. Xuất Báo Cáo Markdown (Save Markdown Report)
*   Tạo file báo cáo mới tại thư mục `output/Ahamove/06. COMPETITIVE_INTEL/monitoring/` dưới định dạng tên `YYYY-MM-DD-competitor-intel-report.md`.
*   Cấu trúc báo cáo phải tuân thủ định dạng chuẩn của Lark Docs, bao gồm:
    *   **Executive Summary:** Tóm tắt phát hiện quan trọng nhất.
    *   **Competitor Move:** Chi tiết sự kiện (CONFIRMED / INFERRED / HYPOTHESIS).
    *   **Likely Impact on Ahamove:** Tác động ngắn hạn (< 4 tuần) và dài hạn (> 3 tháng).
    *   **Recommended Response:** Khuyến nghị hành động tức thời, ngắn hạn và chiến lược.
    *   **FAROUT Score:** Đánh giá độ tin cậy.

### 4. Biên dịch sang HTML Dễ Đọc (Compile to Premium HTML)
*   Sau khi tạo xong file Markdown, chạy script biên dịch HTML:
    ```bash
    python3 _scripts/md_to_html.py "output/Ahamove/06. COMPETITIVE_INTEL/monitoring/YYYY-MM-DD-competitor-intel-report.md"
    ```
*   Script sẽ tự động:
    *   Loại bỏ các dòng kẻ trang trí box-drawing (`━`, `=`, `-`) vô nghĩa trong Markdown.
    *   Trích xuất tiêu đề thực tế làm title của browser tab.
    *   Tự động nhúng bảng màu chuẩn Ahamove (`#0E4174` Blue, `#FF7F32` Orange) và font `Lexend`.
    *   Thêm nhãn badge thương hiệu và footer ghi nhận thời gian báo cáo.

### 5. Gửi báo cáo lên Telegram (Push to Telegram Group)
*   Nếu đã cấu hình file `.env` ở thư mục gốc (chứa `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`), hãy gửi thông báo tóm tắt kèm tệp báo cáo HTML đính kèm bằng lệnh:
    ```bash
    python3 _scripts/send_telegram.py "output/Ahamove/06. COMPETITIVE_INTEL/monitoring/YYYY-MM-DD-competitor-intel-report.md" "output/Ahamove/06. COMPETITIVE_INTEL/monitoring/YYYY-MM-DD-competitor-intel-report.html"
    ```
*   Script này sẽ tự động trích xuất nội dung **Executive Summary** làm tin nhắn xem nhanh và đính kèm file HTML báo cáo gốc.

### 6. Cập nhật Index Vận hành (Update Index)
*   Mở file index `output/Ahamove/README.md`.
*   Thêm hai dòng link tới báo cáo Markdown và HTML vừa tạo vào mục `06. COMPETITIVE_INTEL` để các stakeholders dễ dàng theo dõi.

---

## Weekly Market Brief (Bản Tin Đầu Tuần)
Bên cạnh luồng báo cáo hàng ngày từ tin tức Google News RSS, mỗi thứ Hai hàng tuần Agent thực hiện tạo **Bản Tin Vận Hành & Thị Trường Đầu Tuần** (Weekly Market Brief):
1. **Tìm kiếm chuyên sâu:** Thực hiện tìm kiếm web về các chương trình thưởng (incentives), chiết khấu (commission), biểu giá mới của các đối thủ Bike (Grab, Be, XanhSM) và Delivery tương tự (SPX, ShopeeFood) tại Việt Nam trong 7 ngày qua.
2. **Cập nhật toàn cầu:** Quét tin tức nổi bật từ các nền tảng gig economy lớn trên thế giới (Uber, DoorDash, Meituan, Deliveroo) về mô hình vận hành, công nghệ điều phối (dispatch), xe điện (EV fleet) và chính sách lao động.
3. **Cơ cấu báo cáo:** Soạn thảo báo cáo đặt tại `output/Ahamove/06. COMPETITIVE_INTEL/monitoring/YYYY-MM-DD-weekly-market-brief.md` gồm các mục: Executive Summary, Đối thủ nội địa, Xu hướng thế giới, Tác động lên Ahamove, Khuyến nghị Driver Management.
4. **Biên dịch & Đẩy tin:** Biên dịch sang HTML và gửi file đính kèm cùng tin nhắn tóm tắt lên group Telegram.

---

## Common Mistakes
1.  **Thiếu đường dẫn chứa khoảng trắng:** Khi chạy lệnh biên dịch trên Terminal, phải đặt đường dẫn file báo cáo trong dấu ngoặc kép `"..."` do folder chứa khoảng trắng (`06. COMPETITIVE_INTEL`).
2.  **Bỏ quên bước biên dịch HTML:** Luôn chạy script `md_to_html.py` ngay sau khi ghi nhận hoặc cập nhật báo cáo Markdown để tránh lệch pha nội dung giữa 2 phiên bản.
3.  **Không cấu hình biến môi trường Telegram:** Nếu chạy script `send_telegram.py` mà không cấu hình `.env` hoặc truyền biến môi trường tương ứng, script sẽ báo lỗi.
