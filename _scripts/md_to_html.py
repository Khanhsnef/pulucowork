import sys
import os
import markdown

# ── BRAND COLOR PALETTE ───────────────────────────────────────────────────────
BLUE = "#0E4174"
ORANGE = "#FF7F32"
GREEN = "#10B981"
RED = "#EF4444"
BG_LIGHT = "#F8FAFC"
TEXT_DARK = "#1E293B"
BORDER_COLOR = "#E2E8F0"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {blue};
            --secondary: {orange};
            --success: {green};
            --danger: {red};
            --bg: {bg_light};
            --text: {text_dark};
            --border: {border_color};
        }}
        
        body {{
            font-family: 'Lexend', sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
            margin: 0;
            padding: 2rem 1rem;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 2.5rem;
            border-radius: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
            border: 1px solid var(--border);
        }}
        
        .badge {{
            display: inline-block;
            background-color: var(--secondary);
            color: #FFFFFF;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            margin-bottom: 1.5rem;
            letter-spacing: 0.05em;
        }}
        
        h1, h2, h3, h4 {{
            color: var(--primary);
            font-weight: 800;
        }}
        
        h1 {{
            font-size: 2rem;
            border-bottom: 3px solid var(--secondary);
            padding-bottom: 0.5rem;
            margin-top: 0;
        }}
        
        h2 {{
            font-size: 1.4rem;
            margin-top: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.3rem;
        }}
        
        h3 {{
            font-size: 1.15rem;
            color: var(--secondary);
        }}
        
        p, li {{
            font-size: 0.95rem;
            color: #475569;
        }}
        
        hr {{
            border: 0;
            height: 1px;
            background: var(--border);
            margin: 2rem 0;
        }}
        
        blockquote {{
            margin: 1.5rem 0;
            padding: 1rem 1.5rem;
            background: #EFF6FF;
            border-left: 4px solid var(--primary);
            border-radius: 0.5rem;
            color: var(--primary);
            font-style: italic;
        }}
        
        /* Alert styles mapping */
        blockquote.note {{
            background: #F8FAFC;
            border-left-color: #64748B;
            color: #334155;
        }}
        
        blockquote.important {{
            background: #F0FDF4;
            border-left-color: var(--success);
            color: #166534;
        }}
        
        blockquote.warning {{
            background: #FFF9DB;
            border-left-color: #F59E0B;
            color: #92400E;
        }}
        
        /* Table Styles */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.9rem;
        }}
        
        th, td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        th {{
            background-color: var(--primary);
            color: #FFFFFF;
            font-weight: 600;
        }}
        
        tr:nth-child(even) {{
            background-color: #F8FAFC;
        }}
        
        code {{
            background-color: #F1F5F9;
            color: #0F172A;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-family: monospace;
            font-size: 0.85em;
        }}
        
        ul {{
            padding-left: 1.5rem;
        }}
        
        li {{
            margin-bottom: 0.5rem;
        }}
        
        a {{
            color: var(--secondary);
            text-decoration: none;
            font-weight: 600;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            font-size: 0.8rem;
            color: #64748B;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">Ahamove SmartOps Intelligence</div>
        {content}
        <div class="footer">
            Báo cáo được dịch và xuất bản tự động bởi <strong>Antigravity CI Agent</strong> vào lúc {date_generated}
        </div>
    </div>
</body>
</html>
"""

def convert_md_to_html(md_path, html_path=None):
    if not html_path:
        html_path = md_path.replace(".md", ".html")
        
    print(f"Reading markdown from: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    # Pre-process: Clean decorative header lines (e.g., lines with only box-drawing ━, =, -, etc.)
    clean_lines = []
    for line in md_content.splitlines():
        if line.startswith("#"):
            content_part = line.lstrip("#").strip()
            # Skip lines that are purely decorative (have no letters or numbers)
            if not any(c.isalnum() for c in content_part):
                continue
        clean_lines.append(line)
    md_content_clean = "\n".join(clean_lines)
    
    # Extract Title for the tab
    title = "Ahamove Operational Report"
    for line in clean_lines:
        if line.startswith("# "):
            title = line.replace("# ", "").strip()
            break
            
    # Standard Markdown conversion
    html_content = markdown.markdown(
        md_content_clean, 
        extensions=['extra', 'codehilite', 'tables']
    )
    
    # Process custom GitHub alert tags e.g., > [!IMPORTANT]
    html_content = html_content.replace(
        "<blockquote>\n<p>[!IMPORTANT]", 
        '<blockquote class="important">\n<p><strong>💡 CHÚ Ý:</strong>'
    ).replace(
        "<blockquote>\n<p>[!WARNING]", 
        '<blockquote class="warning">\n<p><strong>⚠️ CẢNH BÁO:</strong>'
    ).replace(
        "<blockquote>\n<p>[!NOTE]", 
        '<blockquote class="note">\n<p><strong>📝 GHI CHÚ:</strong>'
    )
    
    # Get current time for footer
    import datetime
    date_generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
    # Wrap in template
    final_html = HTML_TEMPLATE.format(
        title=title,
        content=html_content,
        date_generated=date_generated,
        blue=BLUE,
        orange=ORANGE,
        green=GREEN,
        red=RED,
        bg_light=BG_LIGHT,
        text_dark=TEXT_DARK,
        border_color=BORDER_COLOR
    )
    
    # Save HTML
    print(f"Writing beautiful HTML to: {html_path}")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(final_html)
    print("✅ Conversion successful!")
    return html_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: Missing markdown file argument.")
        print("Usage: python3 md_to_html.py <file.md> [output.html]")
        sys.exit(1)
        
    md_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(md_file):
        print(f"❌ Error: File not found: {md_file}")
        sys.exit(1)
        
    convert_md_to_html(md_file, out_file)
