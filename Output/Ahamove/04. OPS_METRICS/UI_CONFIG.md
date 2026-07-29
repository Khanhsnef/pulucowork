# 🏷️ Tag Request Portal - Visual & Content UI Configuration

Anh/Chị có thể sửa trực tiếp bất kỳ nội dung text, tiêu đề, tên nút bấm hoặc danh sách lựa chọn trong file Markdown này. Khi sửa xong, chỉ cần gõ vào khung chat: *"Cập nhật code từ file UI_CONFIG.md giúp tôi"*, AI sẽ tự động đồng bộ sang tệp `Index.html`, `2026-07-dm-qm-tag-request-manager.html` và `Code.gs`!

---

## 1. Thông Tin Chung & Header
- **App Title**: Tag Request Portal
- **Link Target Text**: Google Sheet Target
- **Google Sheet URL**: https://docs.google.com/spreadsheets/d/1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4/edit#gid=407438001

---

## 2. Thẻ Thống Kê KPI (Summary Cards)
- **Card 1 Title**: Tổng Yêu Cầu (All Requests)
- **Card 1 Subtitle**: Ghi nhận trên hệ thống

- **Card 2 Title**: Chờ DM Review (Pending)
- **Card 2 Subtitle**: SLA phản hồi: ≤ 4h

- **Card 3 Title**: DM Đã Duyệt (Approved)
- **Card 3 Subtitle**: Đã chuyển luồng QM

- **Card 4 Title**: Chờ QM Add Tags
- **Card 4 Subtitle**: Yêu cầu DM đã duyệt

---

## 3. Tên Các Tab Điều Hướng (Navigation Tabs)
- **Tab 1 Name**: 📝 Bước 1: Request
- **Tab 2 Name**: 🛡️ Bước 2: DM Review
- **Tab 3 Name**: ⚙️ Bước 3: QM Add Tags
- **Tab 4 Name**: 📊 Master Request Tracker

---

## 4. Bước 1: Biểu Mẫu Gửi Yêu Cầu (Request Form)
- **Form Section Header**: 📝 Biểu Mẫu Tạo Yêu Cầu Tag Tài Xế Cho Phía DM
- **Field 1 Label**: Team Đề Xuất *
- **Field 2 Label**: Họ Tên Người Yêu Cầu *
- **Field 3 Label**: Loại Tag Mong Muốn *
- **Field 4 Label**: Tên Tag Gợi Ý / Mục Tiêu *
- **Field 5 Label**: Thời Gian Áp Dụng *
- **Field 6 Label**: Lý Do Kinh Doanh & Tiêu Chí Chọn Tài Xế *
- **Submit Button Text**: 🚀 Gửi Đề Xuất Tới DM Lead

### Danh Sách Các Team Đề Xuất (Dropdown)
1. Business Operations
2. Marketing Campaign
3. Hub Linehaul Operations
4. Customer Service (CS)
5. Risk & Fraud Control
6. Fleet Operations

### Danh Sách Loại Tag Mong Muốn (Dropdown)
1. Priority Dispatch (Ưu tiên phát đơn)
2. Incentive Campaign (Thưởng/Thách thức)
3. Area Restriction (Giới hạn khu vực)
4. Special Training (Đào tạo dịch vụ VIP)
5. Penalty / Block (Khóa/Tạm dừng)

---

## 5. Bước 2: Bàn Tròn DM Review (DM Review Console)
- **Section Header**: 🛡️ Bàn Tròn Thẩm Định Của DM Lead (DM Review Console)
- **Modal Header**: 🛡️ Thẩm Định Request

---

## 6. Bước 3: Hàng Đợi QM Add Tag (QM Add Tag Queue)
- **Section Header**: ⚙️ Hàng Đợi QM Tiếp Nhận & Add Tag

---

## 7. Bước 4: Master Request Tracker
- **Section Header**: 📊 Master Request Tracker
