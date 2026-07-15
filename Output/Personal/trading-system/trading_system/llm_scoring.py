"""Tầng 2 — LLM News Scoring qua Claude Code CLI headless (`claude -p`).

KHÔNG cần API key: dùng chính phiên đăng nhập Claude Code trên máy
(subscription sẵn có). Chỉ chạy on-demand khi user bấm nút trên UI.

Flow:  UI button → POST /api/news/llm/{symbol} → job queue
       → build prompt (tin 7 ngày từ SQLite) → subprocess `claude -p`
       → parse JSON → lưu llm_scores → UI poll và hiển thị.

Fallback model: nếu binary có alias/model mặc định thì dùng nguyên;
truyền --model haiku để rẻ + nhanh (scoring không cần model lớn).
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime

from .news import recent_news, rule_news_score, save_llm_score

CLAUDE_TIMEOUT = 240          # giây — headless lần đầu có thể chậm
MAX_NEWS_FOR_PROMPT = 25
# Máy Khanh route model qua 9Router (prefix cc/) — fallback alias chuẩn nếu fail
LLM_MODELS = ["cc/claude-haiku-4-5-20251001", "haiku"]


def claude_available() -> bool:
    return shutil.which("claude") is not None


PROMPT_TEMPLATE = """Bạn là chuyên gia phân tích tin tức tài chính. Chấm điểm tác động tin tức lên {symbol} ({market_label}).

TIN TỨC 7 NGÀY QUA (mới nhất trước):
{news_block}

ĐIỂM RULE-BASED THAM KHẢO: {rule_score}/100 (50 = trung tính)

Trả về DUY NHẤT một JSON object (không markdown, không giải thích ngoài JSON):
{{
  "score": <int 1-100, 50 là trung tính, cân nhắc trọng số tin trực tiếp về mã cao hơn tin thị trường chung, tin mới quan trọng hơn tin cũ>,
  "confidence": <"cao"|"trung bình"|"thấp" — thấp nếu ít tin trực tiếp>,
  "summary": "<2-3 câu tiếng Việt: động lực chính đang đẩy/kéo mã này từ tin tức>",
  "top_positive": "<tiêu đề tin tích cực quan trọng nhất, hoặc null>",
  "top_negative": "<tiêu đề tin tiêu cực quan trọng nhất, hoặc null>",
  "horizon_impact": {{"short": <-2..2>, "mid": <-2..2>, "long": <-2..2>}}
}}"""


def build_prompt(symbol: str, market: str) -> tuple[str, int, int]:
    """Trả (prompt, n_items, rule_score). Raise nếu không có tin."""
    items = recent_news(symbol, market, days=7, limit=MAX_NEWS_FOR_PROMPT)
    rule = rule_news_score(symbol, market)
    if not items:
        raise ValueError(f"Chưa có tin nào trong DB cho {symbol} — bấm Refresh tin tức trước.")
    lines = []
    for it in items:
        tag = f" [khớp mã, rule {it['rule_score']:+d}]" if it["rule_score"] else ""
        lines.append(f"- ({it['published']}, {it['source']}) {it['title']}{tag}")
    market_label = "cổ phiếu Việt Nam" if market == "vn" else "crypto"
    prompt = PROMPT_TEMPLATE.format(symbol=symbol, market_label=market_label,
                                    news_block="\n".join(lines), rule_score=rule["score"])
    return prompt, len(items), rule["score"]


def _extract_json(text: str) -> dict:
    """Chịu được output lẫn text quanh JSON (headless đôi khi kèm dòng trạng thái)."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"Không tìm thấy JSON trong output: {text[:200]}")
    return json.loads(m.group(0))


def run_llm_scoring(symbol: str, market: str) -> dict:
    """Chạy `claude -p` đồng bộ (gọi từ job thread của server)."""
    if not claude_available():
        raise RuntimeError("Không tìm thấy `claude` CLI trên máy này. Cài Claude Code trước.")

    prompt, n_items, rule_score = build_prompt(symbol, market)
    r = None
    last_err = ""
    for model in LLM_MODELS:
        cmd = ["claude", "-p", prompt, "--output-format", "text", "--model", model]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=CLAUDE_TIMEOUT)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Claude CLI quá {CLAUDE_TIMEOUT}s — thử lại sau.")
        if r.returncode == 0:
            break
        last_err = (r.stderr or r.stdout or "")[:300]
    if r is None or r.returncode != 0:
        raise RuntimeError(f"Claude CLI lỗi: {last_err}")

    data = _extract_json(r.stdout)
    score = int(max(1, min(100, data.get("score", 50))))
    summary = str(data.get("summary", ""))[:500]
    save_llm_score(symbol, score, n_items, summary, json.dumps(data, ensure_ascii=False))
    return {
        "symbol": symbol, "score": score, "rule_score": rule_score,
        "n_items": n_items, "summary": summary,
        "confidence": data.get("confidence"),
        "top_positive": data.get("top_positive"),
        "top_negative": data.get("top_negative"),
        "horizon_impact": data.get("horizon_impact"),
        "scored_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
