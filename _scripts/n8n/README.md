# n8n Setup — Ahamove Ops Automation

## Quick Start (Docker)

```bash
# 1. Start n8n
docker run -d \
  --name n8n-ahamove \
  --restart unless-stopped \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e GENERIC_TIMEZONE="Asia/Ho_Chi_Minh" \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=khanh \
  -e N8N_BASIC_AUTH_PASSWORD=ahamove2026 \
  n8nio/n8n

# 2. Open UI
open http://localhost:5678
```

## Workflows

| File | Mô tả | Schedule |
|---|---|---|
| `workflow-daily-report.json` | Gửi Telegram report lúc 8AM | Daily 08:00 |
| `workflow-competitor-intel.json` | Crawl tin đối thủ → Telegram alert | Every 6h |
| `workflow-git-sync.json` | Auto-commit & push khi file thay đổi | Every 30min |

## Import Workflow

1. Mở http://localhost:5678
2. New Workflow → **⋮** menu → **Import from file**
3. Chọn file JSON trong folder này
4. Điền credentials (Telegram token, Anthropic API key)
5. **Activate**

## Credentials cần setup

### Telegram Bot
- `TELEGRAM_BOT_TOKEN` — lấy từ @BotFather
- `TELEGRAM_CHAT_ID` — chat ID của group/channel report

### Anthropic (Claude)
- `ANTHROPIC_API_KEY` — dùng để format/summarize report

### Environment Variables trong .env
```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
ANTHROPIC_API_KEY=...
FIRECRAWL_API_KEY=fc-...
```
