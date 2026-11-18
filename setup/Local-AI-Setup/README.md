# 🛠️ Bộ Công Cụ Tự Động Thiết Lập Local AI (Forge + Flux.1)

Thư mục này được chuẩn bị sẵn để giúp bạn tự động thiết lập và chạy mô hình tạo ảnh AI Flux.1 cục bộ trên máy tính cá nhân ở nhà có card đồ họa Nvidia RTX 3060 Ti.

## 📋 Yêu cầu trước khi chạy
Đảm bảo máy tính ở nhà của bạn đã cài đặt:
1. **[Git for Windows](https://git-scm.com/)**
2. **[Python 3.10.x](https://www.python.org/downloads/release/python-3106/)** (Vui lòng chọn tích vào ô **"Add Python to PATH"** lúc cài đặt).

## 🚀 Hướng dẫn khởi chạy tại nhà

1. Mở Terminal / Command Prompt hoặc Git Bash tại nhà.
2. Kéo toàn bộ code mới nhất từ GitHub về máy:
   ```bash
   git pull origin main
   ```
3. Truy cập thư mục `Local-AI-Setup` và double-click chuột chạy tệp:
   ```text
   setup_and_run.bat
   ```
4. **Tệp lệnh sẽ tự động:**
   * Kiểm tra phiên bản Git và Python trên máy của bạn.
   * Tự động clone mã nguồn **WebUI Forge** nếu chưa có.
   * Tự động tải xuống mô hình lượng tử hóa **Flux.1-Dev NF4** (~6.3 GB) từ Hugging Face trực tiếp vào đúng thư mục cần thiết.
   * Tự động kích hoạt và mở WebUI trên trình duyệt của bạn (`http://127.0.0.1:7860`).

---
*Lưu ý: Thư mục sinh ra trong quá trình thiết lập (`stable-diffusion-webui-forge`) đã được thêm vào `.gitignore` để tránh đẩy hàng chục GB mô hình và mã nguồn AI lên kho lưu trữ GitHub chung.*
