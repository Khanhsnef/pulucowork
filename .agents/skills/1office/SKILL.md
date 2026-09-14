---
name: 1office
description: Tích hợp và tự động hóa thao tác trên nền tảng quản trị doanh nghiệp 1Office (ahamove.1office.vn). Hỗ trợ tự động đặt phòng họp, tra cứu phòng trống, kiểm tra lịch họp và quản lý session cookie tự động.
---

# 1Office Automation & Integration Skill

Skill này hướng dẫn Antigravity IDE (và các sub-agents) thao tác với nền tảng **1Office (`ahamove.1office.vn`)**.

---

## 🎯 Năng Lực & Tính Năng Của Skill

1. **Đặt Phòng Họp Tự Động (Meeting Room Booking):**
   - Đặt phòng họp NANGA (ID: 27), DENALI (ID: 25) và các phòng họp khác trên 1Office.
   - Hỗ trợ đặt theo lịch cố định tuần hoặc đặt phòng tức thời theo thời gian được chỉ định.

2. **Tra Cứu Lịch Phòng Họp (Room Schedule & Availability):**
   - Kiểm tra phòng nào đang trống / đã có người đặt trong khoảng thời gian cụ thể.

3. **Quản Lý Phiên Đăng Nhập (Session Management):**
   - Tự động duy trì và kiểm tra tính hợp lệ của Session Cookie (`PHPSESSID`, `uid`).
   - Tự động fallback đăng nhập lại khi Session bị hết hạn (nếu được cấu hình credentials).

---

## 🛠️ Hướng Dẫn Sử Dụng Căn Bản (Usage Rules)

Khi người dùng yêu cầu liên quan đến **1Office** (VD: "đặt phòng họp Nanga thứ 2", "kiểm tra phòng họp trống", "kiểm tra kết nối 1office"):

### 1. Kiểm tra trạng thái phiên kết nối 1Office
Chạy lệnh CLI:
```bash
python3 scripts/1office-booking/cli.py status
```

### 2. Tra cứu lịch phòng họp trong ngày
Chạy lệnh CLI:
```bash
python3 scripts/1office-booking/cli.py check-rooms --date DD/MM/YYYY
```

### 3. Đặt phòng họp linh hoạt
Chạy lệnh CLI với thông số tương ứng:
```bash
python3 scripts/1office-booking/cli.py book --room NANGA --date DD/MM/YYYY --start HH:MM --end HH:MM --title "Tên Buổi Họp"
```

---

## 📁 Cấu Trúc Các File Liên Quan

- `scripts/1office-booking/1office_client.py`: Module xử lý API, Auth & Cookie 1Office.
- `scripts/1office-booking/cli.py`: Tool CLI cho Antigravity Agent thực thi trực tiếp.
- `scripts/1office-booking/book_rooms.py`: Script chạy tự động hàng tuần (kết hợp LaunchAgent `com.ahamove.book-meeting-rooms`).
- `scripts/1office-booking/.env.1office`: Nơi lưu trữ thông tin cấu hình Cookie / Credentials an toàn.
