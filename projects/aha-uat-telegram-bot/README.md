# Ahamove UAT Group Bot — Thiết lập từ đầu cho Nhóm riêng

Bot hoàn toàn độc lập với bot cũ trong workspace (đọc cấu hình riêng tại `projects/aha-uat-telegram-bot/.env`), được tối ưu cho **Group Chat riêng** + hỗ trợ **nhắn riêng (DM)** để nạp `cURL`/Token kín đáo.

---

## Bước 1: Tạo Bot mới & tắt Privacy Mode trên `@BotFather`
1. Mở Telegram tìm **`@BotFather`** → Gõ `/newbot` → Đặt tên và nhận **`AHA_BOT_TOKEN`**.
2. *(Khuyên dùng cho Group)* Gõ `/setprivacy` trong `@BotFather` → Chọn bot vừa tạo → Chọn **`Disable`** (để bot nhận được lệnh `cURL` khi bạn dán trực tiếp vào nhóm).
3. Thêm Bot vừa tạo vào **Nhóm Telegram riêng** của bạn.

---

## Bước 2: Tạo file `.env` riêng cho Bot
Tạo file `/Users/ts-1148/Desktop/Pulu-workspace/projects/aha-uat-telegram-bot/.env` (hoặc copy từ `.env.example`):

```bash
cp /Users/ts-1148/Desktop/Pulu-workspace/projects/aha-uat-telegram-bot/.env.example \
   /Users/ts-1148/Desktop/Pulu-workspace/projects/aha-uat-telegram-bot/.env
```

Mở file `.env` và điền `AHA_BOT_TOKEN`:
```env
AHA_BOT_TOKEN="1234567890:AAH..."
AHA_GROUP_CHAT_ID=""
AHA_ALLOW_DM="true"
AHA_DEFAULT_DRIVER_ID="84981792046"
```

---

## Bước 3: Khởi chạy Bot & Khóa vào Nhóm riêng
Chạy lệnh sau trên Terminal:
```bash
/Users/ts-1148/Desktop/Pulu-workspace/.venv/bin/python /Users/ts-1148/Desktop/Pulu-workspace/projects/aha-uat-telegram-bot/bot.py
```

1. Vào **Nhóm Telegram riêng**, gõ lệnh:
   ```text
   /bind_group
   ```
   *(Bot sẽ tự động lưu Chat ID của nhóm và từ đó chỉ phục vụ duy nhất nhóm này + DM cá nhân).*
2. Mở **DM riêng với Bot** (hoặc ngay trong nhóm), **dán nguyên 2 đoạn `cURL`** (1 cURL tạo đơn + 1 cURL admin gán đơn). Bot tự bóc tách:
   - `user_token` + `order_template` (từ cURL tạo đơn)
   - `admin_token` + `admin_cookie` (từ cURL gán đơn)

---

## Bước 4: Các lệnh sử dụng trong Nhóm & DM
| Lệnh | Tác dụng & Ví dụ |
| :--- | :--- |
| `/menu` | Mở bảng nút bấm tương tác Tạo đơn, Gán đơn & Huỷ đơn |
| `/help` | Xem hướng dẫn chi tiết toàn bộ câu lệnh & ví dụ |
| `/tao` | Tạo đơn UAT nhanh theo mẫu, trả về mã đơn + nút **🚀 Gán ngay** / **🗑 Huỷ** |
| `/new` | Tạo đơn tùy chỉnh (Tìm địa chỉ Ahamove / Ghim GPS 📎, Người gửi/nhận, COD, Tự tính phí; >50km tự nâng lên `SGN-VAN-500`) |
| `/gan 26I8NU9H 0981792046` | Gán trực tiếp đơn `26I8NU9H` cho tài xế `84981792046` |
| `/taogan [SĐT_TX]` | Tạo đơn mới **và** tự động gán luôn cho tài xế trong 1 bước |
| `/huy 26Y4SFDF Khách hẹn mai` | Huỷ đơn kèm Note huỷ (lưu vào Order Logs) hoặc gõ `/huy <MÃ_ĐƠN>` để chọn lý do chuẩn Ahamove |
| `/add_service [SĐT_TX] [SERVICE]` | Gắn thêm dịch vụ cho tài xế UAT (VD: `/add_service 84981792046 SGN-VAN-500`) |
| `/token` | Kiểm tra thời hạn & trạng thái Auto-Refresh của JWT User/Admin |
| `/nap` | Nạp cURL hoặc JWT mới (hỗ trợ Reply trực tiếp trong nhóm) |
| `/bind_group` | Khóa Bot chỉ phục vụ duy nhất nhóm hiện tại |
| `/cancel` | Hủy thao tác đang nhập dở |
