#!/usr/bin/env python3
"""
HTML 16:9 Presentation Renderer Engine (Phase 7).
Transforms SlideJSON into interactive, pixel-perfect 16:9 HTML presentations with Live In-Browser Edit Mode.
"""

import sys
import os
import json


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
    <title>{deck_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Lexend:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-canvas: {bg_canvas};
            --card-bg: {card_bg};
            --card-border: {card_border};
            --font-family: {font_family};
            --primary: {primary_color};
            --accent: {accent_color};
            --text-main: {text_primary};
            --text-muted: {text_muted};
            --positive: {positive_color};
            --negative: {negative_color};
            --warning: {warning_color};
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: #0f172a;
            font-family: var(--font-family);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 0;
            gap: 40px;
        }}

        /* Toolbar controls */
        .toolbar {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 9999;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px 24px;
            border-radius: 999px;
            display: flex;
            gap: 16px;
            align-items: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }}

        .toolbar button {{
            background: var(--accent);
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }}

        .toolbar button:hover {{
            transform: scale(1.05);
            filter: brightness(1.1);
        }}

        /* 16:9 Canvas Container */
        .slide-page {{
            width: 1920px;
            height: 1080px;
            background-color: var(--bg-canvas);
            border-radius: 24px;
            padding: 56px 64px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }}

        /* Header section */
        .slide-header {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .slide-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .takeaway-title {{
            font-size: 32px;
            font-weight: 800;
            color: var(--primary);
            line-height: 1.25;
            letter-spacing: -0.5px;
        }}

        /* Hero KPI Bar */
        .hero-kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 16px;
        }}

        .hero-kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 20px 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            box-shadow: 0 10px 25px -5px rgba(14, 65, 116, 0.06);
            position: relative;
            overflow: hidden;
        }}

        .hero-kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: var(--accent);
        }}

        .hero-kpi-label {{
            font-size: 14px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .hero-kpi-val {{
            font-size: 48px;
            font-weight: 900;
            color: var(--primary);
            line-height: 1.0;
        }}

        .hero-kpi-badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            width: fit-content;
        }}

        .badge-positive {{ background: #ECFDF5; color: var(--positive); }}
        .badge-negative {{ background: #FEF2F2; color: var(--negative); }}
        .badge-neutral {{ background: #EFF6FF; color: var(--primary); }}

        /* Content Body Grid */
        .content-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            flex: 1;
            margin-top: 24px;
        }}

        .glass-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px 28px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            color: var(--primary);
        }}

        .bullet-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .bullet-item {{
            font-size: 15px;
            line-height: 1.5;
            color: var(--text-main);
            position: relative;
            padding-left: 20px;
        }}

        .bullet-item::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: 900;
            font-size: 20px;
            line-height: 1;
        }}

        /* Data Table */
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
            font-size: 14px;
        }}

        .data-table th {{
            background: #F1F5F9;
            color: var(--primary);
            font-weight: 700;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 2px solid var(--card-border);
        }}

        .data-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--card-border);
            color: var(--text-main);
        }}

        /* Slide Footer */
        .slide-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            color: var(--text-muted);
            border-top: 1px solid rgba(226, 232, 240, 0.8);
            padding-top: 16px;
        }}

        /* Editable highlight indicator */
        [contenteditable="true"]:focus {{
            outline: 2px solid var(--accent);
            background: rgba(255, 127, 50, 0.05);
            border-radius: 4px;
        }}

        @media print {{
            body {{ background: none; padding: 0; }}
            .toolbar {{ display: none; }}
            .slide-page {{ page-break-after: always; box-shadow: none; border-radius: 0; }}
        }}
    </style>
</head>
<body>

    <div class="toolbar">
        <span style="color:#fff; font-size:13px; font-weight:600;">⚡ Ahamove 16:9 Presentation</span>
        <button id="editBtn" onclick="toggleEditMode()">✏️ Edit Mode (E)</button>
        <button onclick="window.print()">🖨️ Export PDF</button>
    </div>

    {slides_html}

    <script>
        let isEdit = false;
        function toggleEditMode() {{
            isEdit = !isEdit;
            document.querySelectorAll('.editable').forEach(el => {{
                el.contentEditable = isEdit;
            }});
            const btn = document.getElementById('editBtn');
            btn.innerText = isEdit ? '💾 Save Mode (E)' : '✏️ Edit Mode (E)';
            btn.style.background = isEdit ? '#10B981' : '{accent_color}';
        }}

        document.addEventListener('keydown', (e) => {{
            if (e.key === 'e' || e.key === 'E') {{
                if (document.activeElement.isContentEditable) return;
                toggleEditMode();
            }}
        }});
    </script>
</body>
</html>
"""


def render_slide_to_html(slide_json_path: str, output_html_path: str, theme_path: str = None, template_path: str = None) -> str:
    with open(slide_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Check if custom HTML template file exists
    if not template_path:
        default_tpl = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "TEMPLATES", "dark-glassmorphism", "template.html")
        if os.path.exists(default_tpl):
            template_path = default_tpl

    if template_path and os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as tpl_f:
            template_code = tpl_f.read()
    else:
        template_code = HTML_TEMPLATE

    # Default styling tokens
    theme = {
        "bg_canvas": "#F8FAFC",
        "card_bg": "#FFFFFF",
        "card_border": "rgba(226, 232, 240, 0.8)",
        "font_family": "Lexend, Inter, sans-serif",
        "primary_color": "#0E4174",
        "accent_color": "#FF7F32",
        "text_primary": "#0F172A",
        "text_muted": "#475569",
        "positive_color": "#10B981",
        "negative_color": "#EF4444",
        "warning_color": "#F59E0B"
    }

    if theme_path and os.path.exists(theme_path):
        with open(theme_path, 'r', encoding='utf-8') as tf:
            theme.update(json.load(tf))

    slides_html_blocks = []
    deck_title = data.get("deck_title", "Executive Report")

    for slide in data.get("slides", []):
        slide_id = slide.get("slide_id", 1)
        header_text = slide.get("takeaway_header", "Executive Summary")
        hero_kpis = slide.get("hero_kpis", [])
        cards = slide.get("cards", [])
        data_table = slide.get("data_table")
        source_slides = slide.get("source_slides", [])
        source_trace = f"Source: Slide {', '.join(map(str, source_slides))}" if source_slides else "Source: Data Analytics Engine"

        # Build Hero KPI block
        hero_kpi_html = ""
        if hero_kpis:
            kpi_items = ""
            for kpi in hero_kpis:
                status = kpi.get("badge_status", "neutral")
                badge_class = f"badge-{status}"
                delta_html = f'<span class="hero-kpi-badge {badge_class}">{kpi.get("delta")}</span>' if kpi.get("delta") else ""
                kpi_items += f"""
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">{kpi.get("label")}</div>
                    <div class="hero-kpi-val editable">{kpi.get("value")}</div>
                    {delta_html}
                </div>
                """
            hero_kpi_html = f'<div class="hero-kpi-grid">{kpi_items}</div>'

        # Build Content Cards grid
        cards_html = ""
        for card in cards:
            bullets_html = ""
            for bullet in card.get("bullets", []):
                bullets_html += f'<li class="bullet-item editable">{bullet}</li>'

            cards_html += f"""
            <div class="glass-card">
                <div class="card-header">
                    <span>{card.get("icon_badge", "💡")}</span>
                    <span class="editable">{card.get("title")}</span>
                </div>
                <ul class="bullet-list">{bullets_html}</ul>
            </div>
            """

        # Table block if available
        table_html = ""
        if data_table and data_table.get("headers"):
            th_html = "".join([f'<th class="editable">{h}</th>' for h in data_table["headers"]])
            tr_html = ""
            for row in data_table.get("rows", []):
                td_html = "".join([f'<td class="editable">{cell}</td>' for cell in row])
                tr_html += f'<tr>{td_html}</tr>'
            table_html = f"""
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr>{th_html}</tr></thead>
                    <tbody>{tr_html}</tbody>
                </table>
            </div>
            """

        # Executive Comment / Analyst Insight block if present
        exec_comment = slide.get("executive_comment")
        comment_html = ""
        if exec_comment:
            comment_html = f"""
            <div class="executive-comment-card">
                <div class="comment-header">
                    <span>💡</span>
                    <span>Góc Nhìn Quản Trị & Đánh Giá Vận Hành (Executive Comment)</span>
                </div>
                <div class="comment-body editable">{exec_comment}</div>
            </div>
            """

        slide_block = f"""
        <div class="slide-page" id="slide-{slide_id}">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide {slide_id}</span>
                </div>
                <div class="takeaway-title editable">{header_text}</div>
                {hero_kpi_html}
            </div>

            <div class="content-grid">
                {cards_html}
                {table_html}
            </div>

            {comment_html}

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">{source_trace}</span>
            </div>
        </div>
        """

        slides_html_blocks.append(slide_block)

    full_html = template_code.format(
        deck_title=deck_title,
        bg_canvas=theme.get("bg_canvas", "#F8FAFC"),
        card_bg=theme.get("card_bg", "#FFFFFF"),
        card_border=theme.get("card_border", "rgba(226, 232, 240, 0.8)"),
        font_family=theme.get("font_family", "Lexend, Inter, sans-serif"),
        primary_color=theme.get("primary_color", "#0E4174"),
        accent_color=theme.get("accent_color", "#FF7F32"),
        text_primary=theme.get("text_primary", "#0F172A"),
        text_muted=theme.get("text_muted", "#475569"),
        positive_color=theme.get("positive_color", "#10B981"),
        negative_color=theme.get("negative_color", "#EF4444"),
        warning_color=theme.get("warning_color", "#F59E0B"),
        slides_html="\n".join(slides_html_blocks)
    )

    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    return output_html_path



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_html.py <slide_json_path> <output_html_path> [theme_json_path]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_path = sys.argv[2]
    theme_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    res = render_slide_to_html(json_path, output_path, theme_path)
    print(f"Rendered 16:9 HTML Presentation: {res}")
