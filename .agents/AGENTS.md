# AHAMOVE BRAND & OFFICIAL REPORT GUIDELINES

## 🖼️ QUY CHUẨN LOGO AHAMOVE (AHAMOVE LOGO STANDARD)

*   **Logo Chính Thức:** Ahamove Primary Brand Logo (Logo Ahamove dạng chữ kèm biểu tượng chuyển động).
*   **Khoảng Thở (Clear Space):** Luôn duy trì khoảng trống tối thiểu 15px quanh Logo.
*   **Vị Trí Ưu Tiên:** Góc trên bên trái (Top-Left) hoặc Góc trên bên phải (Top-Right) của slide/tài liệu.

---

## 🎨 QUY CHUẨN SLIDE REPORT CHÍNH THỨC (TRÍCH XUẤT TỪ TEMPLATE DOANH NGHIỆP)

Tất cả các báo cáo slide PowerPoint (`.pptx`) của Ahamove phải tuân thủ nghiêm ngặt quy chuẩn từ template `Monthly_Weekly Report Template.pptx`:

### 1. Khung Hình & Phối Màu (Theme & Color Palette)
*   **Tỷ lệ Khung hình:** **16:9 Widescreen** (13.333 inches $\times$ 7.5 inches).
*   **Theme Nền Slide:** **Light Theme Nền Sáng Sang Trọng (`#FFFFFF` / `#F8FAFC`)**.
*   **Màu Nhận Diện Chính:** **Ahamove Primary Orange (`#FF6B00`)** cho Header, Accent Lines, Nút & Bảng.
*   **Màu Chữ:** Title & Headline dùng Slate Dark (`#1E293B`), Subtitle dùng Muted Slate (`#64748B`).
*   **Màu Khối Thẻ (Card Tints):**
    *   Hộp **`KEY TAKEAWAY:`**: Phủ màu Soft Orange Tint (`#FFF3EB`).
    *   Thẻ **Highlights / Success**: Phủ màu Soft Green Tint (`#E8F5EC`) viền `#10B981`.
    *   Thẻ **Lowlights / Warning**: Phủ màu Soft Red Tint (`#FFF1F0`) viền `#EF4444`.
    *   Thẻ **Neutral / Container**: Phủ màu Soft Gray (`#F5F7FA`) viền `#E2E8F0`.

### 2. Cấu Trúc Bắt Buộc Của Slide Báo Cáo
1.  **Cấu trúc Tiêu đề 3 Tầng:**
    *   `Top Category Tag`: Font In hoa 10pt–11pt Bold, màu Cam `#FF6B00`.
    *   `Main Slide Title`: Font 20pt–22pt Extra Bold, màu `#1E293B`.
    *   `Subtitle`: Font 12pt–13pt Regular/Italic, màu `#64748B`.
2.  **Khối `KEY TAKEAWAY:` Nằm Đầu Mỗi Slide:**
    *   Mọi slide báo cáo bắt buộc phải có 1 Hộp `KEY TAKEAWAY:` nằm ngay dưới tiêu đề (Nền `#FFF3EB`), tóm tắt nhận định cốt lõi theo nguyên tắc Kim Tự Tháp.
3.  **Chân Trang Cố Định (Footer Standard):**
    *   `Ahamove — Driver Management | Confidential` góc dưới bên trái.
4.  **Bảng Kế Hoạch Hành Động (Action Plan Table):**
    *   Header màu Cam `#FF6B00`, chữ trắng bold. Cột chuẩn: `HẠNG MỤC` | `NGUYÊN NHÂN/BỐI CẢNH` | `HÀNH ĐỘNG` | `DEADLINE` | `PIC`.

---

## 🔍 QUY TẮC KÍCH HOẠT CLAUDE VIEW DASHBOARD AUTOMATION

*   Bất kỳ khi nào người dùng yêu cầu: `"mở claude view"`, `"open claude view"`, `"bật claude view"`, `"xem claude view"`, `"cv"`, hoặc các cụm từ tương tự:
    1.  Tự động kích hoạt mở URL Dashboard [http://localhost:47892](http://localhost:47892) trên trình duyệt mặc định bằng lệnh `open http://127.0.0.1:47892`.
    2.  Nếu dịch vụ chưa chạy, khởi chạy ngầm bằng `npx claude-view &`.
    3.  Trả về phản hồi kèm đường dẫn truy cập trực tiếp `http://localhost:47892`.
