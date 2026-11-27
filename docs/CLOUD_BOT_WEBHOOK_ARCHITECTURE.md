# Kiến Trúc Chuẩn: Cloud Bot & Workflow Chạy 24/7 (Không Phụ Thuộc Máy Văn Phòng)

> **Mục tiêu:** Mọi Telegram Bot và luồng tự động hóa cá nhân/vận hành đều chạy **24/7 trên Cloud (\$0 phí)**, phản hồi **0 delay**, **không crash/disconnect** khi tắt máy tính văn phòng, và **chỉnh sửa được ngay từ điện thoại**.

---

## 1. Kiến trúc tổng thể (GitHub + Vercel Webhook + Secret Gist)

```text
┌──────────────────┐        HTTPS POST (0 delay)       ┌────────────────────────────────┐
│   Telegram API   │ ─────────────────────────────────▶ │  Vercel Serverless (Python)    │
│  (User / Group)  │ ◀───────────────────────────────── │  /api/webhook (api/webhook.py) │
└──────────────────┘         sendMessage / edit         └───────────────┬────────────────┘
                                                                        │ Read / Write State
┌──────────────────┐      GitHub Mobile / github.dev                    ▼
│  Điện thoại /    │ ───────▶ Git Push ────────┐        ┌────────────────────────────────┐
│  Thiết bị từ xa  │                           ▼        │   GitHub Secret Gist / /tmp    │
└──────────────────┘                  ┌────────────────┐│  (Tokens, USER_STATES, Config) │
                                      │  GitHub Repo   │└────────────────────────────────┘
┌──────────────────┐                  │  (Source Code) │
│  GitHub Actions  │ ◀── Daily Cron ──┴────────────────┘
│ (Health Monitor) │ ──▶ Gửi báo cáo sức khỏe luồng vào Telegram Group mỗi ngày
└──────────────────┘
```

### Tại sao mô hình này tối ưu?
1. **Không dùng Long Polling (`while True: getUpdates`):** Polling bắt máy tính phải mở liên tục, dễ `409 Conflict` hoặc trễ 15–45s lúc bàn giao phiên trên GitHub Actions. **Webhook** để Telegram tự đẩy tin nhắn tới Vercel ngay lập tức (**0 delay**).
2. **\$0 phí & Gần như Unlimited:** Vercel Hobby Plan cho **1.000.000 lượt chạy/tháng** miễn phí, tự cấp HTTPS/SSL, không cần thuê hay bảo trì VPS.
3. **State bền vững khi Serverless tắt/mở:** Mọi token đăng nhập và trạng thái hội thoại nhiều bước (`USER_STATES`) được đồng bộ qua **GitHub Secret Gist** (`config.py`), còn file tạm trên Vercel ghi vào `/tmp`.
4. **Tự động giám sát & tự chữa lành (Auto-Heal):** Mỗi ngày, luồng kiểm tra sức khỏe tự động ping endpoint Vercel, kiểm tra `getWebhookInfo` của Telegram, tự gọi lại `setWebhook` nếu bị mất và báo cáo vào Telegram Group.

---

## 2. Cấu trúc chuẩn cho mọi Bot mới (`template`)

Khi tạo bất kỳ bot Python mới nào trong `projects/<ten-bot>/`, luôn giữ cấu trúc 4 thành phần chuẩn:

```text
projects/<ten-bot>/
├── api/
│   └── webhook.py        # Entrypoint Vercel (BaseHTTPRequestHandler: do_GET + do_POST)
├── bot.py                # Logic xử lý lệnh (handle_message, handle_callback)
├── config.py             # Load .env + sync state qua /tmp (trên Vercel) & Secret Gist
├── pyproject.toml        # Khai báo [tool.vercel] entrypoint = "api.webhook:handler"
├── requirements.txt      # Thư viện Python (VD: requests>=2.31.0)
└── vercel.json           # Cấu hình maxDuration & rewrite "/" -> "/api/webhook"
```

### Quy tắc bắt buộc khi viết code cho mô hình này
* **Filesystem trên Vercel là Read-Only** (trừ `/tmp`): Mọi ghi file tạm phải kiểm tra `os.environ.get("VERCEL")` để chuyển sang `/tmp/...`.
* **Không lưu state dài hạn trong RAM:** Nếu bot có luồng hỏi-đáp nhiều bước (`USER_STATES`), phải đọc/ghi qua `load_store()` / `save_store()` (Gist hoặc DB cloud).
* **Không chạy `deleteWebhook` khi khởi động:** Webhook và Long Polling **không thể chạy song song** trên cùng 1 Bot Token.
* **Luôn trả HTTP `200 OK` cho Telegram:** Trong `do_POST` của `api/webhook.py`, bắt mọi exception và vẫn trả `200` để Telegram không gửi lặp tin nhắn.

---

## 3. Quy trình triển khai 1 Bot mới (từ đầu đến khi chạy)

1. **Tạo bot & lấy Token:** Mở `@BotFather` $\rightarrow$ `/newbot` $\rightarrow$ lưu `BOT_TOKEN`.
2. **Tạo project Vercel:**
   ```bash
   cd projects/<ten-bot>
   vercel link --yes --project <ten-bot>
   ```
3. **Nạp biến môi trường lên Vercel:**
   ```bash
   vercel env add BOT_TOKEN production
   vercel env add GIST_ID production
   vercel env add GIST_TOKEN production
   ```
4. **Deploy Production:**
   ```bash
   vercel deploy --prod --yes
   ```
5. **Gắn Webhook 1 lần duy nhất:**
   ```bash
   curl "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<ten-bot>.vercel.app/api/webhook"
   ```

---

## 4. Cách chỉnh sửa & vận hành khi tắt máy văn phòng

* **Sửa code từ điện thoại:** Mở app **GitHub Mobile** hoặc truy cập `github.dev` trên trình duyệt $\rightarrow$ sửa file $\rightarrow$ Commit. (Nếu đã nối Git trong Vercel Project Settings $\rightarrow$ *Git*, Vercel sẽ tự động deploy lại sau ~15–30 giây).
* **Giám sát hàng ngày:**
  * **08:15 sáng hàng ngày (GitHub Actions - chạy kể cả khi tắt máy):** Script `_scripts/check_cloud_bot_health.py` kiểm tra Vercel endpoint + `getWebhookInfo`, tự khôi phục webhook nếu mất và gửi báo cáo vào nhóm Telegram quản trị.
  * **12:30 trưa hàng ngày (Mac Health Advisor - khi máy bật):** `_scripts/daily_mac_health_advisor.py` báo cáo sức khỏe máy Mac kèm trạng thái Cloud Bot Webhook trong cùng nhóm Telegram.

---

## 5. Tham chiếu triển khai mẫu (`aha-uat-telegram-bot`)
* **Production URL:** `https://aha-uat-telegram-bot.vercel.app`
* **Entrypoint:** `projects/aha-uat-telegram-bot/api/webhook.py`
* **Config & State:** `projects/aha-uat-telegram-bot/config.py`
* **Healthcheck Script:** `_scripts/check_cloud_bot_health.py`
* **Daily Cloud Cron:** `.github/workflows/cloud_bot_health_daily.yml`
