import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# If the file starts with "<!DOC\n    <section", we know the head is missing.
if content.startswith("<!DOC\n    <section"):
    head_css = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Driver Ranking Params — Ahamove</title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #F4F7F9;
      --surface: #FFFFFF;
      --text-prime: #111827;
      --text-sec: #4B5563;
      --text-muted: #9CA3AF;
      --border: #E5E7EB;
      --blue: #0E4174;
      --orange: #FF7F32;
      --yellow: #F59E0B;
      --green: #10B981;
      --red: #EF4444;
      --purple: #8B5CF6;
      --bg-code: #1F2937;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: var(--text-prime); line-height: 1.6; font-size: 14px; padding: 40px 20px; }
    .container { max-width: 900px; margin: 0 auto; background: var(--surface); border-radius: 12px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
    h1, h2, h3 { font-family: 'Montserrat', sans-serif; }
    
    .sec-hdr { display: flex; align-items: flex-start; gap: 16px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid var(--border); }
    .sec-num { font-size: 32px; font-weight: 800; color: var(--blue); opacity: 0.2; line-height: 1; }
    .sec-title h2 { font-size: 22px; font-weight: 700; color: var(--blue); margin-bottom: 4px; }
    .sec-title p { font-size: 13px; color: var(--text-sec); font-weight: 500; }
    section { margin-bottom: 48px; }

    .callout { display: flex; gap: 12px; padding: 12px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; }
    .callout.ci { background: #E0F2FE; color: #0369A1; border-left: 4px solid #0EA5E9; }
    
    .tw { overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 16px; }
    table { width: 100%; border-collapse: collapse; text-align: left; }
    th { background: #F9FAFB; padding: 12px 16px; font-size: 12px; font-weight: 600; color: var(--text-sec); border-bottom: 1px solid var(--border); }
    td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid var(--border); vertical-align: middle; }
    tr:last-child td { border-bottom: none; }
    
    .rank-r1 { font-weight: 700; color: var(--orange); }
    .rank-r2 { font-weight: 700; color: var(--yellow); }
    .rank-r3 { font-weight: 700; color: var(--blue); }
    .rank-un { font-weight: 600; color: var(--text-muted); }
    
    .kpi-pill { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; }
    .kpi-green { background: #D1FAE5; color: #065F46; }
    .kpi-blue { background: #DBEAFE; color: #1E40AF; }
    .kpi-gray { background: #F3F4F6; color: #4B5563; }
    
    .layer-badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; color: white; }
    .layer-badge.l2 { background: var(--orange); }
    .layer-badge.l3 { background: var(--yellow); }
    .layer-badge.l4 { background: var(--blue); }
    .layer-badge.l5 { background: var(--text-sec); }
    .layer-badge.l6 { background: var(--text-muted); }

    .good { color: var(--green); font-weight: 600; }
    .warn { color: var(--text-muted); font-style: italic; }
  </style>
</head>
<body>
  <div class="container">
"""
    content = content.replace("<!DOC\n", head_css, 1)
    content = content + "\n  </div>\n</body>\n</html>"

    with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed HTML formatting.")
else:
    print("HTML already seems to have a valid head.")
