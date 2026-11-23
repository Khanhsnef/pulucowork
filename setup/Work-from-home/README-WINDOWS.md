# Hướng Dẫn Đồng Bộ Mac Công Ty → Windows Cá Nhân

Tài liệu này giúp máy **Windows ở nhà** chạy đầy đủ công cụ, skill, hook và AI workflow giống hệt máy **Mac ở công ty**.

---

## Phần 1 — Chuẩn bị trên máy Mac (Trước khi về)

1. **Push toàn bộ code mới nhất lên GitHub:**
   ```bash
   cd ~/Desktop/Pulu-workspace
   git push
   ```
2. **Sao chép an toàn 2 phần không lưu trên GitHub** (qua USB hoặc Google Drive cá nhân):
   * File `.env` (chứa 8 API keys: Telegram, Gemini, Anthropic, Firecrawl, OpenAI, Metabase).
   * Thư mục `~/.9router/` (nếu muốn giữ nguyên provider/combo của 9Router mà không cần login lại).

---

## Phần 2 — Cài đặt trên máy Windows ở nhà (Làm 1 lần)

1. **Bật Developer Mode** trên Windows (*Settings → System → For developers → Developer Mode: On*) để hỗ trợ symlink của `.claude/skills/`.
2. **Cài phần mềm nền tảng** (mở PowerShell):
   ```powershell
   winget install -e --id Git.Git
   winget install -e --id OpenJS.NodeJS.LTS
   winget install -e --id Python.Python.3.14
   winget install -e --id astral-sh.uv
   winget install -e --id GitHub.cli
   ```
3. **Clone repo với symlink bật sẵn:**
   ```powershell
   git config --global core.symlinks true
   git clone --recurse-submodules git@github.com:Khanhsnef/pulucowork.git Pulu-workspace
   cd Pulu-workspace
   git checkout feat/tag-portal-3gate
   ```
4. **Chạy script tự động cài đặt Windows:**
   Nhấp đúp vào [setup-windows.bat](setup-windows.bat) (hoặc chạy trong PowerShell):
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\setup\Work-from-home\setup-windows.ps1
   ```
   Script sẽ tự động:
   * Kiểm tra toàn bộ tool (`git`, `node`, `python`, `uv`, `gh`) và sửa symlink `.claude/skills/*` thành Windows Junction nếu cần.
   * Tạo `.venv` và cài toàn bộ thư viện trong `requirements.txt`.
   * Cài `9router@0.5.123` và `@anthropic-ai/claude-code`.
   * Thiết lập `ANTHROPIC_BASE_URL=http://127.0.0.1:20128/v1`.
5. **Chép `.env` vào thư mục gốc `Pulu-workspace\.env`** và chép `.9router` vào `%USERPROFILE%\.9router` (nếu có).
6. **Mở Antigravity trên Windows:** Đăng nhập cùng Google Account và cài các plugin từ Marketplace (`android-cli-plugin`, `chrome-devtools-plugin`, `firebase`, `google-antigravity-sdk`, `modern-web-guidance-plugin`).

---

## Phần 3 — Sử dụng Hằng ngày trên Windows

* **Bật 9Router:** Nhấp đúp [start-9router.bat](start-9router.bat) → mở `http://localhost:20128`.
* **Bật Claude View:** Nhấp đúp [start-claude-view.bat](start-claude-view.bat) → mở `http://localhost:47892`.
* **Smart Chat (`chat`, `ai`, `c-opus`):** Chạy qua **Git Bash** (đi kèm Git for Windows) với `source _scripts/pulu_smartflow.sh`.
* **Lấy code mới khi chuyển máy:** Luôn chạy `git pull` trước khi làm việc và `git push` (hoặc để Claude `Stop` hook tự sync) khi xong việc.
