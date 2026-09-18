"""
analyzer.py — Gọi claude CLI (không cần API key) để analyze + tạo storyline
"""
import os
import json
import subprocess
import tempfile


def analyze_slides(
    slides: list[dict],
    report_type: str = "Management Report",
    compression: str = "Medium",
    language: str = "auto",
    style: str = "Modern Corporate",
) -> dict:
    """
    Gọi `claude -p` qua subprocess để analyze slides.
    Không cần ANTHROPIC_API_KEY — dùng session đang login sẵn.
    """
    print(f"\n[analyze] Phân tích {len(slides)} slides với Claude CLI...")
    print(f"[analyze] Mode: {report_type} | Compression: {compression}")

    slides_text = _build_slides_text(slides)
    prompt = _build_analysis_prompt(slides_text, report_type, compression, language, style, len(slides))

    # Ghi prompt ra temp file để tránh shell escaping issues
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["claude", "-p", f"$(cat {tmp_path})"],
            capture_output=True, text=True, timeout=300,
            shell=False,
        )
        # shell=False + cat workaround → dùng shell=True thay
        result = subprocess.run(
            f'claude -p "$(cat {tmp_path})" --model cc/claude-sonnet-4-6',
            capture_output=True, text=True, timeout=300,
            shell=True,
        )
        raw = result.stdout.strip()
        if not raw and result.stderr:
            raise RuntimeError(f"claude CLI error:\n{result.stderr[:500]}")
    finally:
        os.unlink(tmp_path)

    analysis = _parse_json_response(raw)
    print(f"[analyze] Done → {len(analysis.get('output_slides', []))} output slides")
    return analysis


# ─── Prompt builders ──────────────────────────────────────────────────────────

def _build_slides_text(slides: list[dict]) -> str:
    parts = []
    for s in slides:
        part = [f"=== SLIDE {s['slide_num']} ==="]
        if s.get("title"):
            part.append(f"TITLE: {s['title']}")
        if s.get("texts"):
            part.append("CONTENT:\n" + "\n".join(s["texts"]))
        if s.get("bullet_points"):
            bullets = "\n".join(
                f"{'  ' * b['level']}- {b['text']}" for b in s["bullet_points"]
            )
            part.append(f"BULLETS:\n{bullets}")
        if s.get("tables"):
            for t in s["tables"]:
                rows = "\n".join(" | ".join(row) for row in t)
                part.append(f"TABLE:\n{rows}")
        if s.get("notes"):
            part.append(f"NOTES: {s['notes']}")
        parts.append("\n".join(part))
    return "\n\n".join(parts)


def _build_analysis_prompt(
    slides_text: str,
    report_type: str,
    compression: str,
    language: str,
    style: str,
    total_slides: int,
) -> str:
    compression_guide = {
        "Light": "Keep most information. Merge only clear duplicates.",
        "Medium": "Prioritize insights and key data. Merge related slides. Target ~40% reduction.",
        "Aggressive": "Keep only key message + key numbers + actions per topic. Target 60-70% reduction.",
    }.get(compression, "Medium")

    lang_instruction = "Match the input language exactly" if language == "auto" else f"Use {language}"

    return f"""You are an expert business analyst and management consultant.
Analyze the following presentation slides and rebuild them as a concise executive report.

RULES:
- NEVER invent data or numbers. Only use what is in the slides.
- ALWAYS prioritize insight over volume.
- Think like a McKinsey consultant building a board-level report deck.
- {lang_instruction}

REPORT TYPE: {report_type}
COMPRESSION: {compression} — {compression_guide}
OUTPUT STYLE: {style}

---
INPUT SLIDES ({total_slides} slides):
{slides_text}
---

YOUR TASK:
1. Analyze each slide: topic, key message, key numbers, insights, issues, actions.
2. Group slides by theme.
3. Build an executive storyline: Executive Summary → Highlights → Lowlights → Insights → Next Actions (only sections relevant to content).
4. For each output slide define: slide_title (message-driven headline, NOT topic label), layout_type, key_message, content, image_needed, image_prompt, source_slides.

Layout types available: kpi_cards, highlights_lowlights, problem_solution, action_table, executive_summary, section_divider, ranking, process_flow, timeline, strategy_framework

Return ONLY valid JSON with NO markdown fences, NO explanation:

{{
  "report_title": "...",
  "report_type": "{report_type}",
  "total_input_slides": {total_slides},
  "analysis_summary": [
    {{"input_slides": "1-3", "topic": "...", "key_insight": "...", "output_slide": 1}}
  ],
  "output_slides": [
    {{
      "slide_num": 1,
      "slide_title": "...",
      "layout_type": "executive_summary",
      "key_message": "...",
      "content": {{}},
      "image_needed": false,
      "image_prompt": "",
      "source_slides": [1, 2]
    }}
  ]
}}"""


def _parse_json_response(raw: str) -> dict:
    """Extract JSON từ Claude response."""
    # Strip markdown fences nếu có
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]

    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"Không tìm thấy JSON trong response:\n{raw[:500]}")
    return json.loads(raw[start:end])


def save_analysis(result: dict, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[analyze] Saved: {output_path}")
