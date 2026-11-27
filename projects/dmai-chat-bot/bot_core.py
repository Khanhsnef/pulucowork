import os
import sys
import time
import urllib.request
import urllib.parse
import json
import glob
import datetime
import re

# ── LOAD ENV CONFIG ──────────────────────────────────────────────────────────
TOKEN = None
CHAT_ID = None
GEMINI_API_KEY = None
OPENAI_API_KEY = None
ANTHROPIC_API_KEY = None

# Try loading from environment or .env file
env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith("#") and "=" in line:
                key, val = line.strip().split("=", 1)
                k = key.strip()
                v = val.strip().strip('"').strip("'")
                if k == "TELEGRAM_BOT_TOKEN":
                    TOKEN = v
                elif k == "TELEGRAM_CHAT_ID":
                    CHAT_ID = v
                elif k == "GEMINI_API_KEY":
                    GEMINI_API_KEY = v
                elif k == "OPENAI_API_KEY":
                    OPENAI_API_KEY = v
                elif k == "ANTHROPIC_API_KEY":
                    ANTHROPIC_API_KEY = v

# Override with environment variables if present
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", TOKEN)
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", CHAT_ID)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", OPENAI_API_KEY)
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", ANTHROPIC_API_KEY)

if not TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN is not set.")
    sys.exit(1)

MONITOR_DIR = "Output/Ahamove/06. COMPETITIVE_INTEL/monitoring"

# ── HELPER FUNCTIONS ──────────────────────────────────────────────────────────
def _split_lines_safely(text, max_len=3800):
    if not text or len(text) <= max_len:
        return [text] if text else []
    chunks = []
    cur = ""
    for line in text.splitlines(keepends=True):
        if len(cur) + len(line) > max_len:
            if cur:
                chunks.append(cur.rstrip("\n"))
            cur = line
        else:
            cur += line
    if cur:
        chunks.append(cur.rstrip("\n"))
    return chunks


def markdown_to_telegram_html(md_text):
    """Convert LLM Markdown (**bold**, `code`, ### headers, bullets) into clean Telegram HTML."""
    import html as _html
    if not md_text:
        return ""
    lines = md_text.splitlines()
    out_lines = []
    in_code_block = False
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            out_lines.append("<pre>" if in_code_block else "</pre>")
            continue
        if in_code_block:
            out_lines.append(_html.escape(raw_line))
            continue

        line = _html.escape(raw_line)
        # Headings ### Title -> <b>Title</b>
        m_hd = re.match(r"^\s*#{1,4}\s+(.+)$", line)
        if m_hd:
            hdr = re.sub(r"\*\*(.+?)\*\*", r"\1", m_hd.group(1).strip())
            out_lines.append(f"\n<b>{hdr}</b>")
            continue

        # Normalize bullet markers "*   " or "-   " -> "• "
        line = re.sub(r"^(\s*)[\*\-]\s+", r"\1• ", line)
        # Inline `code`
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
        # Bold **text**
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        # Italic *text* (single asterisk not adjacent to space)
        line = re.sub(r"(?<!\*)\*([^\*\n]+?)\*(?!\*)", r"<i>\1</i>", line)
        out_lines.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out_lines)).strip()


def send_telegram_html(chat_id, html_text, reply_to_message_id=None):
    """Send rich HTML-formatted Telegram message with safe line chunking & plain fallback."""
    chunks = _split_lines_safely(html_text, max_len=3800)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    last_res = None
    for idx, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        if reply_to_message_id and idx == 0:
            payload["reply_to_message_id"] = reply_to_message_id
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                last_res = json.loads(response.read().decode())
        except Exception as e:
            print(f"⚠️ HTML send warning: {e}. Retrying plain...")
            plain = re.sub(r"<[^>]+>", "", chunk)
            payload_fb = {"chat_id": chat_id, "text": plain}
            if reply_to_message_id and idx == 0:
                payload_fb["reply_to_message_id"] = reply_to_message_id
            req_fb = urllib.request.Request(
                url,
                data=json.dumps(payload_fb).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(req_fb, timeout=12) as response:
                    last_res = json.loads(response.read().decode())
            except Exception as fb_err:
                print(f"⚠️ Plain fallback failed: {fb_err}")
    return last_res


def send_telegram_msg(chat_id, text, reply_to_message_id=None):
    chunks = _split_lines_safely(text, max_len=3800)
    if len(chunks) > 1:
        last_res = None
        for idx, ch in enumerate(chunks):
            last_res = send_telegram_msg(chat_id, ch, reply_to_message_id if idx == 0 else None)
        return last_res

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ Error sending message with Markdown: {e}. Retrying as plain text...")
        if "parse_mode" in payload:
            del payload["parse_mode"]
        req_fallback = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req_fallback, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as fallback_err:
            print(f"⚠️ Fallback sending failed: {fallback_err}")
            return None

def send_telegram_doc(chat_id, doc_path, reply_to_message_id=None):
    if not os.path.exists(doc_path):
        return None
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    boundary = "Boundary-TelegramSendDocument"
    file_name = os.path.basename(doc_path)
    with open(doc_path, 'rb') as f:
        file_content = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
        f'{chat_id}\r\n'
    ).encode('utf-8')
    
    if reply_to_message_id:
        body += (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reply_to_message_id"\r\n\r\n'
            f'{reply_to_message_id}\r\n'
        ).encode('utf-8')

    body += (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="document"; filename="{file_name}"\r\n'
        f'Content-Type: text/html\r\n\r\n'
    ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': len(body)
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"⚠️ Error sending document: {e}")
        return None

def get_latest_report(pattern):
    files = glob.glob(os.path.join(MONITOR_DIR, pattern))
    if files:
        latest_md = max(files, key=os.path.getmtime)
        latest_html = latest_md.replace(".md", ".html")
        if not os.path.exists(latest_html):
            latest_html = None
        return latest_md, latest_html

    # Cloud fallback (Vercel): fetch latest matching report from GitHub repo
    try:
        import fnmatch
        api_url = (
            "https://api.github.com/repos/Khanhsnef/pulucowork/contents/"
            "Output/Ahamove/06.%20COMPETITIVE_INTEL/monitoring"
        )
        req = urllib.request.Request(api_url, headers={"User-Agent": "DMAIChat_Bot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode("utf-8"))
        matches = [it for it in items if fnmatch.fnmatch(it.get("name", ""), pattern)]
        if not matches:
            return None, None
        latest_item = max(matches, key=lambda x: x["name"])
        md_name = latest_item["name"]
        md_tmp = os.path.join("/tmp", md_name)
        urllib.request.urlretrieve(latest_item["download_url"], md_tmp)

        html_name = md_name.replace(".md", ".html")
        html_item = next((it for it in items if it.get("name") == html_name), None)
        html_tmp = None
        if html_item and html_item.get("download_url"):
            html_tmp = os.path.join("/tmp", html_name)
            urllib.request.urlretrieve(html_item["download_url"], html_tmp)
        return md_tmp, html_tmp
    except Exception as exc:
        print(f"⚠️ GitHub report fetch error: {exc}")
        return None, None

def parse_summary(md_path):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return "Không thể đọc nội dung báo cáo.", "Báo cáo"

    title = "Báo cáo giám sát cạnh tranh"
    exec_summary = ""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# ") and not any(c in line for c in ["━", "=", "-"]):
            title = line.replace("# ", "").strip()
        if "Executive Summary" in line or "Tóm Tắt Thực Thi" in line or "📊 Executive Summary" in line:
            summary_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith("#") or next_line == "---":
                    break
                if next_line:
                    summary_lines.append(lines[j])
            exec_summary = "\n".join(summary_lines)
            
    return exec_summary, title

# ── AI API CALLERS ────────────────────────────────────────────────────────────
def call_gemini_api(user_message, system_context, api_key, use_search=True):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": f"System Context:\n{system_context}\n\nUser Question:\n{user_message}"}]
        }],
        "generationConfig": {
            "maxOutputTokens": 8192,
            "temperature": 0.4,
            "thinkingConfig": {"thinkingBudget": 512}
        }
    }
    if use_search:
        payload["tools"] = [{"googleSearch": {}}]
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            res = json.loads(response.read().decode())
            candidates = res.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                parts = candidates[0]["content"]["parts"]
                text_parts = [p.get("text", "") for p in parts if not p.get("thought") and p.get("text")]
                return "".join(text_parts) or parts[0].get("text", "Tôi chưa xử lý được câu hỏi này.")
            return "Tôi chưa xử lý được câu hỏi này."
    except Exception as e:
        print(f"⚠️ Gemini API Error: {e}")
        return None

def call_openai_api(user_message, system_context, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 2048,
        "temperature": 0.4
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            res = json.loads(response.read().decode())
            choices = res.get("choices", [])
            if choices and choices[0].get("message", {}).get("content"):
                return choices[0]["message"]["content"]
            return "Tôi chưa xử lý được câu hỏi này."
    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return None

def call_anthropic_api(user_message, system_context, api_key):
    url = "https://api.anthropic.com/v1/messages"
    payload = {
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 512,
        "system": system_context,
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode())
            content = res.get("content", [])
            if content and content[0].get("type") == "text":
                return content[0]["text"]
            return "Tôi chưa xử lý được câu hỏi này."
    except Exception as e:
        print(f"⚠️ Anthropic API Error: {e}")
        return None

def get_system_context(user_message=""):
    msg_low = user_message.lower()
    intel_keywords = ("đối thủ", "grab", "be", "xanhsm", "thị trường", "bản tin", "intel", "competitor", "chiến dịch")
    is_ops_only = any(k in msg_low for k in (
        "ops", "kpi", "sgn", "han", "exp", "nw", "tài xế", "driver", "active", "ar", "fr", "eph", "pph", "thu nhập", "vận hành", "đơn"
    )) and not any(k in msg_low for k in intel_keywords)

    md_file_daily, _ = (None, None) if is_ops_only else get_latest_report("*-report.md")
    md_file_weekly, _ = (None, None) if is_ops_only else get_latest_report("*-weekly-market-brief.md")
    
    context = (
        "Bạn là Chuyên gia Phân tích Vận hành & Chiến lược Tài xế (Senior Ops & Driver Strategy Analyst) của Ahamove.\n"
        "Nhiệm vụ của bạn là phân tích sâu dữ liệu vận hành từ tất cả các bảng dữ liệu (Supply, Demand/SLA, Driver Income/Quality), "
        "thị trường, đối thủ (Grab, Be, XanhSM, SPX, ShopeeFood), OKRs và chính sách phân hạng tài xế.\n\n"
        "Phong cách trình bày: Trực diện (Lead with the answer), sắc bén, dẫn chứng bằng con số tuyệt đối kèm tỷ lệ % tăng/giảm (▲/▼ DoD, WoW, ±pp), "
        "bố cục phân tách rõ ràng bằng tiêu đề & gạch đầu dòng dễ đọc trên điện thoại. "
        "Với câu hỏi xã giao đơn giản thì trả lời ngắn gọn; với câu hỏi báo cáo/vận hành/phân tích thì lập báo cáo đầy đủ, sâu sắc, nhiều insights.\n\n"
    )
    
    loaded_files = []
    
    if md_file_daily:
        try:
            with open(md_file_daily, 'r', encoding='utf-8') as f:
                context += f"### BÁO CÁO NGÀY MỚI NHẤT ({os.path.basename(md_file_daily)}):\n" + f.read() + "\n\n"
                loaded_files.append(os.path.basename(md_file_daily))
        except Exception:
            pass
            
    if md_file_weekly:
        try:
            with open(md_file_weekly, 'r', encoding='utf-8') as f:
                context += f"### BẢN TIN TUẦN MỚI NHẤT ({os.path.basename(md_file_weekly)}):\n" + f.read() + "\n\n"
                loaded_files.append(os.path.basename(md_file_weekly))
        except Exception:
            pass

    # 2. Dynamic RAG based on keyword matching
    # Map keywords to relative paths of documents from Output/Ahamove/
    rag_map = {
        ("okr", "kr", "mục tiêu", "target"): [
            "Output/Ahamove/01. STRATEGY_PLANNING/okr/2026-q2-dm-team-okr.md",
            "Output/Ahamove/01. STRATEGY_PLANNING/okr/2026-q2-okr-dm-internal.md"
        ],
        ("journey", "lifecycle", "vòng đời", "trải nghiệm", "hành trình"): [
            "Output/Ahamove/01. STRATEGY_PLANNING/driver-journey/2026-05-driver-journey-summary.md",
            "Output/Ahamove/01. STRATEGY_PLANNING/driver-journey/2026-06-driver-journey-milestones.md",
            "Output/Ahamove/01. STRATEGY_PLANNING/driver-journey/2026-06-driver-journey-proposal.md",
            "Output/Ahamove/06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md"
        ],
        ("benchmark", "toàn cầu", "thế giới", "nước ngoài", "uber", "meituan", "doordash", "swiggy", "gojek", "deliveroo", "rappi", "ifood"): [
            "Output/Ahamove/06. COMPETITIVE_INTEL/2026-06-global-driver-lifecycle-benchmark.md"
        ],
        ("ranking", "phân hạng", "params", "level", "benefits", "ahabenefits", "quyền lợi", "thưởng điểm"): [
            "Output/Ahamove/01. STRATEGY_PLANNING/ahabenefits/2026-05-ahabenefits-points-flow.md",
            "Output/Ahamove/01. STRATEGY_PLANNING/driver-ranking/2026-05-driver-ranking-params.md",
            "Output/Ahamove/01. STRATEGY_PLANNING/driver-ranking/2026-05-driver-ranking-priority-registration.md"
        ],
        ("restructure", "tái cơ cấu", "cơ cấu", "org", "raci"): [
            "Output/Ahamove/01. STRATEGY_PLANNING/team-restructure/2026-06-driver-restructure-kickoff.md"
        ],
        ("open-source", "mã nguồn mở", "github", "git"): [
            "Output/Ahamove/01. STRATEGY_PLANNING/2026-06-open-source-repos-application.md"
        ],
        ("áo khỉ", "monkey", "campaign", "chiến dịch"): [
            "Output/Ahamove/02. CAMPAIGNS_PROJECTS/2026-05-ao-khi-campaign-plan.md",
            "Output/Ahamove/02. CAMPAIGNS_PROJECTS/2026-05-ao-khi-comms-drafts.md"
        ],
        ("pulu", "smartflow", "risk", "bảo mật", "hiệu năng"): [
            "Output/Ahamove/05. ANALYSIS_REPORTS/2026-06-pulu-smartflow-risk-assessment.md"
        ],
        ("dashboard", "sop", "duckdb", "streamlit"): [
            "Output/Ahamove/07. TEAM_MANAGEMENT/2026-06-new-dashboard-sop.md"
        ],
        ("claude", "ai", "training", "đào tạo"): [
            "Output/Ahamove/07. TEAM_MANAGEMENT/2026-05-claude-guide-for-team.md"
        ]
    }

    user_msg_lower = user_message.lower()
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for keys, paths in rag_map.items():
        if any(k in user_msg_lower for k in keys):
            for rel_path in paths:
                full_path = os.path.join(root_dir, rel_path)
                filename = os.path.basename(rel_path)
                if filename not in loaded_files and os.path.exists(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            context += f"### TÀI LIỆU LIÊN QUAN: {filename} ({rel_path})\n" + f.read() + "\n\n"
                            loaded_files.append(filename)
                    except Exception:
                        pass
                        
    if loaded_files:
        print(f"📚 Loaded dynamic context files for query '{user_message}': {loaded_files}")
        
    ops_keywords = (
        "ops", "kpi", "sgn", "han", "exp", "nw", "nationwide", "đơn", "tài xế", "driver", "active",
        "segment", "tag", "ft", "pt", "nim", "nlm", "return", "bike", "eco",
        "pool", "aifood", "aibot", "tmdt", "2h", "4h", "bulky", "inday", "vận hành",
        "chỉ số", "hôm qua", "tuần", "tháng", "trend", "ngày", "74433", "67888", "75557",
        "requested", "accept", "accepted", "completed", "ar", "fr", "fulfillment", "acceptance", "service",
        "income", "thu nhập", "thưởng", "reward", "eph", "pph", "utilization", "auto-accept",
        "hard", "lcd", "gdr", "rating", "cancel", "cr", "ranking",
    )
    if any(k in user_message.lower() for k in ops_keywords):
        try:
            import ops_metrics
            ops_ctx = ops_metrics.build_query_context(user_message)
            if ops_ctx:
                context += (
                    "### QUY TẮC LẬP BÁO CÁO & INSIGHTS VẬN HÀNH (BẮT BUỘC TUÂN THỦ):\n"
                    "1. Đọc và kết hợp ĐẦY ĐỦ tất cả chỉ số từ cả 3 bảng: "
                    "Card 67888 (Đơn hàng: Requested, Accept, Completed, Đơn rớt, AR, FR theo dịch vụ) + "
                    "Card 74433 (Nguồn cung Tài xế Active theo Segment FT/PT/return/NIM/NLM & kênh dịch vụ) + "
                    "Card 75557 (Thu nhập TB/TX, EPH, PPH, Utilization, Tỷ trọng thưởng, Active/Ranking, Auto-Accept %, Hard %, LCD, GDR, AR Noti, CR POC, Rating).\n"
                    "2. Mọi chỉ số quan trọng PHẢI đi kèm **tỷ lệ tăng/giảm** (`▲/▼ +x.x% DoD`, `WoW`, hoặc `±x.xx pp`).\n"
                    "3. Trình bày theo cấu trúc chuẩn dễ đọc:\n"
                    "   - **📊 TÓM TẮT ĐIỀU HÀNH (Executive Summary):** 2-3 câu kết luận quan trọng nhất toàn mạng lưới.\n"
                    "   - **🌐 1. NW (Toàn Quốc)** | **🏙️ 2. SGN** | **🏛️ 3. HAN** | **🧭 4. EXP**: Mỗi khu vực nêu rõ Cầu & SLA, Nguồn cung, Thu nhập & Chất lượng.\n"
                    "   - **🧠 INSIGHTS CHÉO & ĐỀ XUẤT HÀNH ĐỘNG:** Chỉ rõ nguyên nhân gốc rễ (VD: tương quan giữa AA%/CR POC với FR, biến động Cung vs Cầu, cảnh báo nhóm LCD hoặc dịch vụ kéo tụt SLA) và hành động ưu tiên.\n"
                    "4. Tuyệt đối KHÔNG gọi số tài xế ở Card 74433/75557 là 'đơn hàng'.\n\n"
                    f"### DỮ LIỆU OPS ĐA CHIỀU (ALL SHEETS):\n{ops_ctx}\n\n"
                )
        except Exception as exc:
            print(f"⚠️ Ops metrics context error: {exc}")

    return context

# ── COMMAND & MESSAGE HANDLERS ────────────────────────────────────────────────
def handle_command(chat_id, text, msg_id):
    raw_cmd = text.split()[0].lower()
    cmd = raw_cmd.split("@")[0] if "@" in raw_cmd else raw_cmd

    if cmd in ["/start", "/help"]:
        help_text = (
            "🤖 <b>HƯỚNG DẪN SỬ DỤNG AHAMOVE OPS ANALYST BOT</b> (<code>@DMAIChat_Bot</code>)\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>1. Báo cáo Vận hành Đa chiều (Live Google Sheets — 3+ Cards):</b>\n"
            "• <code>/report</code> hoặc <code>/ops</code> — <b>Báo cáo Tổng hợp Điều hành</b> (đọc toàn bộ Sheet 67888 + 74433 + 75557, tách riêng NW/SGN/HAN/EXP kèm % DoD, % WoW &amp; Insights chéo).\n"
            "• <code>/ops refresh</code> — Kích hoạt đồng bộ mới từ Metabase cho cả 3 Card rồi xuất báo cáo.\n"
            "• <code>/kpi</code> — Chi tiết Đơn hàng, Đơn rớt, AR &amp; FR theo từng <code>service_type</code> (Card 67888).\n"
            "• <code>/supply</code> — Chi tiết Nguồn cung Tài xế theo Segment &amp; 14 kênh dịch vụ (Card 74433).\n"
            "• <code>/driver</code> — Chi tiết Thu nhập, EPH, PPH, Utilization, AA%, Hard%, LCD, GDR, CR POC &amp; Rating (Card 75557).\n\n"
            "📰 <b>2. Báo cáo Thị trường &amp; Đối thủ:</b>\n"
            "• <code>/latest</code> — Báo cáo giám sát đối thủ mới nhất trong ngày.\n"
            "• <code>/weekly</code> — Bản tin tổng hợp thị trường &amp; đối thủ đầu tuần.\n\n"
            "💬 <b>3. Phân tích Chuyên sâu với AI trong mọi Group:</b>\n"
            "• Tag <code>@DMAIChat_Bot &lt;câu hỏi&gt;</code>, gõ <code>/ask &lt;câu hỏi&gt;</code>, hoặc <b>Reply</b> tin nhắn của Bot để yêu cầu phân tích xu hướng tuần/tháng, so sánh ngày cụ thể, chẩn đoán nguyên nhân &amp; đề xuất hành động."
        )
        send_telegram_html(chat_id, help_text, reply_to_message_id=msg_id)

    elif cmd == "/chatid":
        send_telegram_msg(
            chat_id,
            f"🆔 *Chat ID của hội thoại này:* `{chat_id}`",
            reply_to_message_id=msg_id,
        )

    elif cmd in ["/mac", "/health"]:
        send_telegram_msg(chat_id, "⏳ _Đang quét thông số sức khỏe máy Mac (Chế độ Chỉ Đọc an toàn)..._", reply_to_message_id=msg_id)
        try:
            import subprocess
            uptime_out = subprocess.getoutput("uptime").strip()
            swap_out = subprocess.getoutput("sysctl vm.swapusage").strip()
            df_out = subprocess.getoutput("df -h / | tail -n 1").split()
            disk_avail = df_out[3] if len(df_out) > 3 else "N/A"
            disk_cap = df_out[4] if len(df_out) > 4 else "N/A"
            top_mem = subprocess.getoutput("top -l 1 -o mem -n 6 -stats pid,command,cpu,mem,cmprs | tail -n 7").strip()
            msg = (
                "🩺 *CHẨN ĐOÁN SỨC KHỎE MACOS TỨC THÌ*\n"
                f"• *Uptime & Load:* `{uptime_out}`\n"
                f"• *Swap Memory:* `{swap_out}`\n"
                f"• *Ổ cứng SSD trống:* `{disk_avail}` (Đã dùng `{disk_cap}`)\n\n"
                f"📊 *Top tiến trình tiêu thụ RAM/Swap:*\n```\n{top_mem}\n```\n"
                "💡 _Gõ `/mac_clean` nếu bạn muốn dọn Cache rác an toàn mà không đóng ứng dụng đang làm việc._"
            )
            send_telegram_msg(chat_id, msg, reply_to_message_id=msg_id)
        except Exception as e:
            send_telegram_msg(chat_id, f"⚠️ Không thể quét thông số: `{e}`", reply_to_message_id=msg_id)

    elif cmd == "/mac_clean":
        try:
            import subprocess
            subprocess.run(
                "rm -rf ~/.npm/_npx/* ~/.npm/_cacache/* ~/Library/Caches/com.vng.zalo.ShipIt/* "
                "~/Library/Caches/pip/* ~/Library/Caches/Homebrew/* 2>/dev/null || true",
                shell=True,
                timeout=20,
            )
            df_out = subprocess.getoutput("df -h / | tail -n 1").split()
            disk_avail = df_out[3] if len(df_out) > 3 else "N/A"
            swap_out = subprocess.getoutput("sysctl vm.swapusage").strip()
            send_telegram_msg(
                chat_id,
                "✅ *Đã dọn dẹp Cache rác an toàn!*\n"
                f"• *Ổ cứng SSD trống hiện tại:* `{disk_avail}`\n"
                f"• *Swap hiện tại:* `{swap_out}`\n"
                "🛡️ _Toàn bộ cửa sổ làm việc và tài liệu của bạn được giữ nguyên._",
                reply_to_message_id=msg_id,
            )
        except Exception as e:
            send_telegram_msg(chat_id, f"⚠️ Lỗi khi dọn cache: `{e}`", reply_to_message_id=msg_id)

    elif cmd == "/latest":
        md_file, html_file = get_latest_report("*-report.md")
        if not md_file:
            send_telegram_msg(chat_id, "⚠️ Hiện chưa có báo cáo giám sát ngày nào trong hệ thống.", reply_to_message_id=msg_id)
            return

        summary, title = parse_summary(md_file)
        message = f"🔔 *BÁO CÁO MỚI NHẤT: {title}*\n\n"
        if summary:
            message += f"📊 *Tóm tắt thực thi:*\n{summary}\n\n"
        message += "📎 _Báo cáo chi tiết dạng HTML được đính kèm bên dưới._"
        
        send_telegram_msg(chat_id, message, reply_to_message_id=msg_id)
        if html_file:
            send_telegram_doc(chat_id, html_file, reply_to_message_id=msg_id)

    elif cmd == "/weekly":
        md_file, html_file = get_latest_report("*-weekly-market-brief.md")
        if not md_file:
            send_telegram_msg(chat_id, "⚠️ Hiện chưa có bản tin đầu tuần nào trong hệ thống.", reply_to_message_id=msg_id)
            return

        summary, title = parse_summary(md_file)
        message = f"📰 *BẢN TIN ĐẦU TUẦN: {title}*\n\n"
        if summary:
            message += f"📊 *Tóm tắt thực thi:*\n{summary}\n\n"
        message += "📎 _Bản tin chi tiết dạng HTML được đính kèm bên dưới._"
        
        send_telegram_msg(chat_id, message, reply_to_message_id=msg_id)
        if html_file:
            send_telegram_doc(chat_id, html_file, reply_to_message_id=msg_id)

    elif cmd == "/status":
        streamlit_status = "⚠️ Ngoại tuyến (Offline)"
        try:
            with urllib.request.urlopen("http://localhost:8501", timeout=2) as response:
                if response.status == 200:
                    streamlit_status = "✅ Trực tuyến (http://localhost:8501)"
        except Exception:
            pass

        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_text = (
            "💻 *Trạng thái Hệ thống Ahamove SmartOps:*\n\n"
            f"- *Daily Crawler & Monitor:* ✅ Sẵn sàng (chạy lúc 9:00 AM)\n"
            f"- *Weekly Brief Scheduler:* ✅ Sẵn sàng (chạy lúc 8:30 AM thứ Hai)\n"
            f"- *Simulator Dashboard (Streamlit):* {streamlit_status}\n"
            f"- *Thời gian hệ thống:* `{now_str}`"
        )
        send_telegram_msg(chat_id, status_text, reply_to_message_id=msg_id)

def handle_natural_message(chat_id, text, msg_id, message):
    is_private = int(chat_id) > 0
    
    # Check if bot is mentioned or replied to
    is_reply_to_bot = False
    reply_to = message.get("reply_to_message")
    if reply_to:
        reply_from = reply_to.get("from", {})
        # Ensure it is replying to our specific bot username
        if reply_from.get("is_bot") and reply_from.get("username") == "DMAIChat_Bot":
            is_reply_to_bot = True
            
    # Match only explicit username handle or the exact phrase "bot ơi" / "bot oi" with word boundaries
    text_lower = text.lower()
    mentioned = False
    if "@dmaichat_bot" in text_lower:
        mentioned = True
    elif re.search(r'\bbot\s+ơi\b', text_lower) or re.search(r'\bbot\s+oi\b', text_lower):
        mentioned = True
    
    # Only respond in group if it's a private chat, a direct reply, or explicitly mentioned
    if not is_private and not is_reply_to_bot and not mentioned:
        return
        
    print(f"💬 Handling natural message: '{text}' in Chat ID: {chat_id}")
    
    # Send typing action
    try:
        url_action = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
        payload = {"chat_id": chat_id, "action": "typing"}
        req_action = urllib.request.Request(
            url_action,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req_action, timeout=3)
    except Exception:
        pass
        
    context = get_system_context(text)
    
    # Try calling configured API Keys in sequence
    reply_text = None
    
    # Let's try Gemini first (disable googleSearch when internal Ops data is already in context)
    use_search = "DỮ LIỆU OPS ĐA CHIỀU" not in context
    if GEMINI_API_KEY and not reply_text:
        reply_text = call_gemini_api(text, context, GEMINI_API_KEY, use_search=use_search)
        
    # Then try OpenAI
    if OPENAI_API_KEY and not reply_text:
        reply_text = call_openai_api(text, context, OPENAI_API_KEY)
        
    # Finally try Anthropic (making sure key starts with sk-ant)
    if ANTHROPIC_API_KEY and not reply_text:
        if ANTHROPIC_API_KEY.startswith("sk-ant"):
            reply_text = call_anthropic_api(text, context, ANTHROPIC_API_KEY)
        else:
            # Stale or misconfigured key in env
            print("⚠️ System ANTHROPIC_API_KEY does not start with 'sk-ant'. Skipping.")
            
    if not reply_text:
        has_any_key = bool(GEMINI_API_KEY or OPENAI_API_KEY or (ANTHROPIC_API_KEY and ANTHROPIC_API_KEY.startswith("sk-ant")))
        if has_any_key:
            reply_text = "⚠️ *Hệ thống AI tạm thời phản hồi chậm hoặc quá tải.* Vui lòng thử gửi lại sau vài giây (hoặc dùng `/ops`, `/kpi`, `/driver` để lấy số liệu tức thì)."
        else:
            reply_text = (
                "⚠️ *Trợ lý AI chưa được cấu hình khóa kết nối.*\n\n"
                "Vui lòng điền một trong các API Key sau vào file `.env` của bạn để bắt đầu trò chuyện:\n"
                "- `GEMINI_API_KEY`=\"key_của_bạn\" (khuyên dùng)\n"
                "- `OPENAI_API_KEY`=\"key_của_bạn\"\n"
                "- `ANTHROPIC_API_KEY`=\"key_của_bạn\""
            )
        
    send_telegram_html(chat_id, markdown_to_telegram_html(reply_text), reply_to_message_id=msg_id)

# ── MAIN LOOP (POLLING) ───────────────────────────────────────────────────────
def register_bot_commands():
    commands = [
        {"command": "report", "description": "Báo cáo vận hành tổng hợp (3 Sheets + Insights chéo)"},
        {"command": "ops", "description": "Báo cáo tổng hợp điều hành (/ops refresh để đồng bộ mới)"},
        {"command": "kpi", "description": "Chi tiết Đơn hàng, AR & FR theo dịch vụ (Card 67888)"},
        {"command": "supply", "description": "Chi tiết Nguồn cung Tài xế theo Segment (Card 74433)"},
        {"command": "driver", "description": "Chi tiết Thu nhập, EPH, PPH, AA, LCD, CR (Card 75557)"},
        {"command": "ask", "description": "Hỏi chuyên sâu AI Analyst trong nhóm"},
        {"command": "latest", "description": "Xem báo cáo giám sát đối thủ mới nhất trong ngày"},
        {"command": "weekly", "description": "Xem bản tin thị trường & đối thủ đầu tuần"},
        {"command": "help", "description": "Xem hướng dẫn sử dụng đầy đủ của Bot"},
    ]
    scopes = [
        {"type": "default"},
        {"type": "all_private_chats"},
        {"type": "all_group_chats"},
        {"type": "all_chat_administrators"},
    ]
    for scope in scopes:
        for lang in ("", "vi", "en"):
            payload = {"commands": commands, "scope": scope}
            if lang:
                payload["language_code"] = lang
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{TOKEN}/setMyCommands",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            try:
                urllib.request.urlopen(req, timeout=10)
            except Exception as e:
                print(f"⚠️ Warning registering commands for {scope}: {e}")


def main():
    print("🤖 Starting Ahamove SmartOps Telegram Bot Listener (AI-enabled Polling)...")
    register_bot_commands()
    offset = None
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {"timeout": 20}
            if offset:
                params["offset"] = offset
            
            data = urllib.parse.urlencode(params).encode('utf-8')
            req = urllib.request.Request(url, data=data)
            
            with urllib.request.urlopen(req, timeout=25) as response:
                res = json.loads(response.read().decode())
                
                if res.get("ok") and res.get("result"):
                    for update in res["result"]:
                        offset = update["update_id"] + 1
                        
                        message = update.get("message")
                        if not message:
                            continue
                            
                        chat = message.get("chat")
                        text = message.get("text")
                        msg_id = message.get("message_id")
                        
                        if chat and text:
                            chat_id = chat["id"]
                            if text.startswith("/"):
                                print(f"📩 Received command: '{text}' from Chat ID: {chat_id}")
                                handle_command(chat_id, text, msg_id)
                            else:
                                handle_natural_message(chat_id, text, msg_id, message)
                            
        except KeyboardInterrupt:
            print("\n🤖 Bot listener stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Connection error or API limit: {e}")
            time.sleep(5)
            
        time.sleep(1)

if __name__ == "__main__":
    main()
