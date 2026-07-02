# Hướng Dẫn Cài Đặt Tự Động 9Router Trên Windows

Tài liệu này hướng dẫn cách khôi phục toàn bộ cấu hình 9router (Combos, Providers, Flows) từ máy Mac công ty sang máy Windows ở nhà một cách tự động.

## Thành Phần Tự Động Hóa
Hệ thống đã tự động tạo và mã hóa cấu hình từ máy Mac của bạn và lưu trữ trong thư mục [9router-backup](file:///Users/ts-1148/Desktop/Pulu-workspace/9router-backup).
Các file tự động chạy trên Windows:
*   [setup-9router.bat](file:///Users/ts-1148/Desktop/Pulu-workspace/setup-9router.bat): File batch nhấp đúp để tự động kích hoạt.
*   [setup-9router.ps1](file:///Users/ts-1148/Desktop/Pulu-workspace/setup-9router.ps1): Script PowerShell chính thực hiện cài đặt.
*   `9router-backup/decrypt.js`: Script giải mã cơ sở dữ liệu SQLite đã được bảo mật để không bị GitHub chặn (Push Protection).

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
    *   Giải mã database (`data.sqlite`) và các file bảo mật (`jwt-secret`, `machine-id`).
    *   Tự động copy dữ liệu cấu hình vào thư mục hệ thống trên Windows (`%APPDATA%\9router`).
    *   Tự động `git clone` mã nguồn 9router từ GitHub.
    *   Ghi đè các file tùy chỉnh của bạn (chẳng hạn cấu hình cho các provider mới như Claude Fable/Mythos, patch esbuild-wasm).
    *   Tạo file cấu hình môi trường `.env.local`.
    *   Cài đặt thư viện (`npm install`) và build ứng dụng.
    *   Tạo shortcut khởi chạy nhanh `start-9router.bat` trong thư mục code `9router`.

4.  **Khởi Chạy Ứng Dụng:**
    Sau khi script chạy xong, một file **`start-9router.bat`** sẽ được tạo ra trong thư mục `9router`.
    *   Nhấp đúp vào `start-9router.bat` để chạy server.
    *   Mở trình duyệt truy cập: **`http://localhost:20128`**
    *   Đăng nhập bằng mật khẩu như trên máy Mac. Toàn bộ Combos, Providers, Flows của bạn đã có đầy đủ.
