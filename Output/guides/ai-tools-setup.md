# AI Tools — Quick Reference

Cài tại: `~/tools/` | Máy: antigravity (Apple Silicon, macOS)

---

## 1. 9router — AI Proxy Router
**Mục đích:** Route Claude Code / Cursor qua 40+ AI providers, tiết kiệm chi phí API.  
**Port:** `localhost:20128`

```bash
# Lần đầu: chỉnh .env.local
nano ~/tools/9router/.env.local
# Sửa: JWT_SECRET=<chuỗi random dài>  |  INITIAL_PASSWORD=<mật khẩu>

# Chạy:
cd ~/tools/9router && npm run dev

# Kích hoạt cho Claude Code (chạy trong terminal trước khi dùng claude):
export ANTHROPIC_BASE_URL=http://localhost:20128/api/v1
```

**Workflow:**
1. Mở `http://localhost:20128` → Login → Vào Providers
2. Thêm API key (DeepSeek / Kimi / OpenRouter...)
3. Cấu hình model mapping (Opus → DeepSeek R1, Sonnet → DeepSeek V3...)
4. Set env var trên → gõ `claude` như bình thường

---

## 2. local-deep-research — Research Agent
**Mục đích:** Tự động research 20+ nguồn, tổng hợp báo cáo có trích dẫn.  
**Port:** `localhost:5000`

```bash
# Chạy:
~/tools/ldr-env/bin/ldr-web

# Dùng qua MCP (tích hợp Claude Code):
~/tools/ldr-env/bin/ldr-mcp
```

**Workflow:**
1. Mở `http://localhost:5000`
2. Settings → Chọn LLM provider + API key (hoặc Ollama local)
3. New Research → Nhập câu hỏi → Chọn độ sâu (Quick / Detailed / Deep)
4. Đợi agent chạy → Export PDF hoặc Markdown

**Ví dụ use case Ahamove:**
```
"Phân tích chiến lược incentive tài xế của Grab Express tại Việt Nam Q1 2026"
"So sánh mô hình driver tiering của Lalamove vs Ahamove"
```

**Data lưu tại:** `~/Library/Application Support/local-deep-research` (encrypted)

---

## 3. PageIndex — RAG không cần Vector DB
**Mục đích:** Query tài liệu nội bộ (PDF, Markdown) bằng LLM reasoning.  
**Dùng như:** Python library, không có UI.

```bash
# Kích hoạt venv:
source ~/tools/pageindex-env/bin/activate

# Dùng trong Python:
python3
```

```python
from pageindex import PageIndexClient

# Cloud API (cần key từ pageindex.ai):
client = PageIndexClient(api_key="YOUR_KEY")
result = client.query(document="policy.pdf", question="Điều kiện tier 3 là gì?")

# Hoặc self-hosted (xem docs: github.com/VectifyAI/PageIndex)
```

**Tắt venv:**
```bash
deactivate
```

---

## 4. DeepSeek-TUI — Coding Agent trong Terminal
**Mục đích:** Coding agent dùng DeepSeek V3/R1, chạy ngay trong terminal.  
**Cài:** `cargo install --git https://github.com/Hmbown/DeepSeek-TUI` (tự chạy)

```bash
# Chạy:
deepseek-tui
# → Nhập DeepSeek API key lần đầu
# → Chọn model (V3 = nhanh/rẻ, R1 = suy luận sâu)
```

**3 chế độ:**
| Mode | Phím | Mô tả |
|------|------|-------|
| Plan | `p` | Chỉ đọc, lên kế hoạch, không chỉnh file |
| Agent | `a` | Tương tác, hỏi trước khi làm |
| YOLO | `y` | Tự động hoàn toàn, không hỏi |

**Lấy API key:** `platform.deepseek.com` → API Keys → ~$0.14/1M tokens

---

## Aliases đề xuất (thêm vào ~/.zshrc)

```bash
# Rust (bắt buộc nếu dùng DeepSeek-TUI)
source "$HOME/.cargo/env"

# AI Tools shortcuts
alias 9router='cd ~/tools/9router && npm run dev'
alias ldr='~/tools/ldr-env/bin/ldr-web'
alias ldr-mcp='~/tools/ldr-env/bin/ldr-mcp'
alias pageindex='source ~/tools/pageindex-env/bin/activate && python3'
alias dst='deepseek-tui'
```

Sau khi thêm: `source ~/.zshrc`

---

## Port Map (không conflict)

| Tool | Port | Ghi chú |
|------|------|---------|
| 9router | 20128 | Web UI + proxy |
| local-deep-research | 5000 | Web UI |
| PageIndex | — | Library |
| DeepSeek-TUI | — | Terminal app |

---

## Cấu Trúc Thư Mục

```
~/tools/
├── 9router/           # Node.js — npm run dev
├── local-deep-research/  # Source code (ref)
├── ldr-env/           # Python venv — ldr-web chạy từ đây
└── pageindex-env/     # Python venv — PageIndex library
```

---

*Cập nhật: 2026-05-22*
