---
name: auto-ops-dashboard-builder
description: >-
  Tự động xây dựng và triển khai dashboard Streamlit + DuckDB từ các nguồn dữ liệu thô đa dạng (Text, Ảnh, Google Sheets, Excel, CSV) với giao diện chuẩn thương hiệu Ahamove.
---

# Auto Ops Dashboard Builder

## Overview
Skill này hướng dẫn Agent tự động trích xuất dữ liệu thô, thiết kế cấu trúc database DuckDB và lập trình ứng dụng Streamlit hoàn chỉnh để hiển thị thông tin vận hành và hỗ trợ giả lập các chỉ số CPO, FR, AR cho Ahamove Driver Management.

## Dependencies
*   `modern-web-guidance` (Dùng để tối ưu hóa thiết kế giao diện)
*   Thư viện Python: `streamlit`, `duckdb`, `pandas`, `openpyxl`

## Quick Start
Khi người dùng yêu cầu: *"Tạo cho tôi một dashboard từ [nguồn dữ liệu]"*, Agent thực hiện theo quy trình 5 bước bên dưới mà không cần hỏi lại trừ khi xảy ra lỗi nghiêm trọng.

## Workflow

### 1. Phân tích & Trích xuất Dữ liệu Đầu vào (Data Ingestion)
*   **Trường hợp CSV/Excel:** Đọc trực tiếp schema bằng Python để hiểu các cột.
*   **Trường hợp Google Sheets:** Yêu cầu link công khai hoặc file tải về dạng CSV.
*   **Trường hợp Văn bản (Text) hoặc Ảnh chụp (Image):**
    *   Sử dụng khả năng đa phương thức (Multimodal/OCR) để trích xuất toàn bộ dữ liệu số dưới dạng bảng.
    *   **GIAO THỨC LỖI:** Nếu ảnh quá mờ hoặc thiếu quyền truy cập Sheets, **BẮT BUỘC** dừng lại và hỏi người dùng cung cấp thông tin sạch (lựa chọn a).

### 2. Thiết kế Cơ sở Dữ liệu với DuckDB
*   Đặt file dữ liệu phẳng vào `output/Ahamove/04. OPS_METRICS/raw-data/`.
*   Tạo Temp View bằng DuckDB:
    ```python
    import duckdb
    db = duckdb.connect(database=':memory:')
    ```
*   **Xử lý dữ liệu thô (Calibrate):** Ép kiểu thủ công các cột số có chứa dấu phẩy phân tách hàng nghìn sang `VARCHAR` rồi dùng `CAST(REPLACE(col, ',', '') AS INTEGER)` để tránh lỗi `ConversionException`.

### 3. Thiết kế Giao diện Streamlit chuẩn Brand Ahamove
Mọi Dashboard tạo ra phải tuân thủ nghiêm ngặt hệ thống màu sắc và kiểu chữ của Ahamove:
*   **Bảng màu:**
    *   Primary Blue: `#0E4174` (Tiêu đề, nút bấm chính)
    *   Primary Orange: `#FF7F32` (Điểm nhấn, các chỉ số quan trọng)
    *   Semantic: `#10B981` (Thành công/FR đạt target), `#EF4444` (Nguy hiểm/SLA sụt giảm)
*   **Typography:** Inject font `Lexend` bằng CSS Markdown:
    ```python
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Lexend', sans-serif; }
    </style>
    """, unsafe_allow_html=True)
    ```
*   **Bố cục (Layout):**
    *   Sử dụng `st.sidebar` để gom tất cả các bộ lọc (chọn thành phố, phân tầng tài xế, thanh trượt tham số giả lập).
    *   Dùng `st.columns` và custom HTML để tạo các thẻ Metrics Card đẹp ở trên cùng.
    *   Hiển thị biểu đồ so sánh tương tác bằng `st.line_chart` hoặc `st.bar_chart`.

### 4. Triển khai & Xác thực (Deployment & Validation)
*   Tạo file code dashboard tại thư mục: `output/Ahamove/04. OPS_METRICS/dashboards/[tên-file-viết-thường].py`.
*   Cập nhật index file vào `output/Ahamove/README.md`.
*   Chạy thử ứng dụng trong terminal:
    ```bash
    streamlit run output/Ahamove/04. OPS_METRICS/dashboards/[tên-file].py --server.headless true
    ```
*   Dùng browser subagent để truy cập `localhost:8501`, chụp ảnh màn hình xác nhận giao diện hiển thị đúng, không lỗi.

## Common Mistakes
1.  **Lỗi Ép kiểu DuckDB:** Quên cấu hình `types={'column': 'VARCHAR'}` khi đọc CSV dẫn đến crash giữa chừng khi gặp số lớn có dấu phẩy.
2.  **Thiếu Font & CSS:** Dùng giao diện Streamlit thô mặc định (không có font Lexend và bo góc metrics card) làm giảm tính premium của tài liệu.
3.  **Lỗi đường dẫn BASE_DIR:** Sử dụng `dirname(__file__)` quá nhiều cấp dẫn đến trỏ sai thư mục `raw-data`. Hãy mặc định sử dụng đường dẫn tuyệt đối `/Users/ts-1148/Desktop/Pulu-workspace`.
