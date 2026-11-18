# Hướng Dẫn Cài Đặt Tự Động 9Router & Bộ Nhớ Agent Trên Windows

Tài liệu này hướng dẫn cách khôi phục toàn bộ cấu hình 9router (Combos, Providers, Flows) và lịch sử/bộ nhớ Agent (Brain, Conversations, settings) từ máy Mac công ty sang máy Windows ở nhà một cách tự động.

## Thành Phần Tự Động Hóa
Hệ thống đã tự động tạo, mã hóa và phân mảnh dữ liệu từ máy Mac của bạn và lưu trữ trong thư mục [9router-backup](file:///Users/ts-1148/Desktop/Pulu-workspace/9router-backup).
Các file tự động chạy trên Windows:
*   [setup-9router.bat](file:///Users/ts-1148/Desktop/Pulu-workspace/setup-9router.bat): File batch nhấp đúp để tự động kích hoạt.
*   [setup-9router.ps1](file:///Users/ts-1148/Desktop/Pulu-workspace/setup-9router.ps1): Script PowerShell chính thực hiện cài đặt.
*   `9router-backup/decrypt.js`: Script giải mã cơ sở dữ liệu SQLite của 9router.
*   `9router-backup/pack-memory.js` và `decrypt.js`/`unpack-memory.js`: Bộ công cụ nén, mã hóa bảo mật dữ liệu bộ nhớ Agent thành các tệp phân mảnh (`chunk.*` dưới 100MB) để lưu trữ thành công trên GitHub.

---

## Yêu Cầu Trước Khi Cài Đặt (Prerequisites)
Đảm bảo máy Windows ở nhà đã cài đặt:
1.  **Node.js LTS** (Tải tại: https://nodejs.org/)
2.  **Git** (Tải tại: https://git-scm.com/)

---

## Các Bước Thực Hiện Trên Máy Windows ở Nhà

1.  **Tải/Pull Workspace Mới Nhất:**
    Mở Terminal trên Windows tại thư mục workspace của bạn và kéo code mới nhất từ GitHub:
    ```bash
    git pull origin main
    ```

2.  **Chạy File Cài Đặt Tự Động:**
    Nhấp đúp chuột vào file:
    👉 **`setup-9router.bat`**

    *Hoặc chạy bằng PowerShell (với quyền Admin hoặc Bypass):*
    ```powershell
    powershell -ExecutionPolicy Bypass -File .\setup-9router.ps1
    ```

3.  **Hệ Thống Sẽ Tự Động Thực Hiện:**
    *   Giải mã database (`data.sqlite`) và các file bảo mật (`jwt-secret`, `machine-id`) và đưa vào thư mục `%APPDATA%\9router`.
    *   Tự động `git clone` mã nguồn 9router từ GitHub và áp dụng các cấu hình registry mới của bạn (Claude Fable/Mythos, esbuild-wasm patch).
    *   Gộp các mảnh (`chunk.*`), giải mã và giải nén bộ nhớ Agent (Brain, Conversations, History) trực tiếp vào thư mục `%USERPROFILE%\.gemini` trên Windows.
    *   Cài đặt thư viện (`npm install`), build ứng dụng, và tạo file khởi động nhanh `start-9router.bat`.

4.  **Khởi Chạy 9Router:**
    Sau khi script chạy xong, một file **`start-9router.bat`** sẽ được tạo ra trong thư mục `9router`.
    *   Nhấp đúp vào `start-9router.bat` để chạy server.
    *   Mở trình duyệt truy cập: **`http://localhost:20128`**
    *   Đăng nhập và sử dụng bình thường.
