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

## Bước 4: Các lệnh sử dụng trong Nhóm
| Lệnh trong Nhóm | Tác dụng |
| :--- | :--- |
| `/menu` | Mở bảng nút bấm tương tác Tạo đơn & Gán đơn |
| `/tao` | Tạo đơn UAT nhanh ngay lập tức, trả về mã đơn + nút **🚀 Gán ngay** |
| `/new` | Tạo đơn tùy chỉnh từng bước (Dịch vụ, COD, Total Pay, Ghi chú) |
| `/gan 26I8NU9H 84981792046` | Gán trực tiếp đơn `26I8NU9H` cho tài xế `84981792046` |
| `/gan 26I8NU9H` | Hiển thị nút bấm 1 chạm gán đơn `26I8NU9H` cho tài xế mặc định hoặc nhập SĐT khác |
| `/taogan` | Tạo đơn mới **và** tự động gán luôn cho tài xế mặc định trong 1 bước |
| `/taogan 0981792046` | Tạo đơn mới **và** gán luôn cho tài xế `84981792046` |
| `/token` | Kiểm tra thời hạn còn lại của JWT User & Admin |
