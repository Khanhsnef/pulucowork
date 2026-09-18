#!/usr/bin/env python3
"""
ChatGPT Canvas Prompt Exporter (TOOLS/chatgpt-exporter/export_chatgpt_prompt.py).
Packages the generated HTML/JSON slide deck into a ready-to-copy Prompt Document for ChatGPT Canvas Redesign.
"""

import sys
import os
import json


def package_chatgpt_prompt(html_path: str, json_path: str, output_prompt_path: str) -> str:
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    with open(html_path, 'r', encoding='utf-8') as f:
        html_code = f.read()

    json_snippet = ""
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as jf:
            json_snippet = jf.read()

    prompt_content = f"""# INSTRUCTION FOR CHATGPT CANVAS / REDESIGN ENGINE

You are an Expert Design Technologist & Modern Web UI Architect.

Below is an existing 16:9 HTML Slide Deck (`real_report.html`) containing 8 operational slides for **Ahamove Driver Management**.

## YOUR TASK:
Redesign the HTML/CSS of this presentation in ChatGPT Canvas to make it look **visually STUNNING, ultra-premium, and modern** (e.g., sleek Dark-mode Glassmorphic Dashboard, Apple/Gemini aesthetic, vibrant gradients, high-contrast visual hierarchy).

## STRICT RULES:
1. **KEEP 100% OF THE DATA**: Do NOT change, alter, or omit any metrics, percentage values, dates, headers, or bullet text.
2. **MAINTAIN 16:9 CANVAS**: Preserve 1920x1080 resolution / aspect ratio for slide pages.
3. **5 VISUAL LAYOUT PRINCIPLES**:
   - Asymmetric Focal Point (Hero KPI / Card 1.5x larger than surrounding context).
   - Floating Glass Cards with 16px border-radius and subtle 1px border stroke.
   - Micro-Visual Anchors (Icon Badges 🎯 ⚡ 💡 🔴 🏆 📊).
   - Giant Numbers (48px - 56px Bold) for key metrics.
   - Dual-Pane 40/60 Balance.
4. **LIVE EDIT MODE**: Keep `contenteditable="true"` or editable classes so the text remains editable in browser.

---

## INPUT HTML SOURCE CODE TO REDESIGN:

```html
{html_code}
```

---

## (OPTIONAL) INPUT SLIDE DATA PAYLOAD (JSON):

```json
{json_snippet}
```
"""

    os.makedirs(os.path.dirname(output_prompt_path), exist_ok=True)
    with open(output_prompt_path, 'w', encoding='utf-8') as out_f:
        out_f.write(prompt_content)

    return output_prompt_path


if __name__ == "__main__":
    html_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/ts-1148/Desktop/Pulu-workspace-v2/AI-REPORT-GENERATOR/OUTPUT/Ahamove_DM_Real_Meeting_Report/real_report.html"
    json_path = sys.argv[2] if len(sys.argv) > 2 else "/Users/ts-1148/Desktop/Pulu-workspace-v2/AI-REPORT-GENERATOR/OUTPUT/Ahamove_DM_Real_Meeting_Report/slide_payload_real.json"
    out_path = sys.argv[3] if len(sys.argv) > 3 else "/Users/ts-1148/Desktop/Pulu-workspace-v2/AI-REPORT-GENERATOR/OUTPUT/Ahamove_DM_Real_Meeting_Report/CHATGPT_CANVAS_PROMPT.md"

    res = package_chatgpt_prompt(html_path, json_path, out_path)
    print(f"✔ ChatGPT Canvas Prompt File Created: {res}")
