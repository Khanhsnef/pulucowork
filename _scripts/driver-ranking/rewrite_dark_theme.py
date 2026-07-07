import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    html = f.read()

# Extract sections 1 to 7
sections = re.findall(r'(<section id="s\d+".*?</section>)', html, flags=re.DOTALL)
if not sections:
    print("Could not find sections!")
    exit(1)

content_html = "\n\n".join(sections)

# The new HTML structure
new_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Driver Ranking Params — Ahamove</title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-main: #0B0E14;
      --bg-side: #151921;
      --card-bg: #1A1F26;
      --border: #2A2F38;
      --orange: #FF6A00;
      --orange-dim: rgba(255,106,0,0.15);
      --text-prime: #F3F4F6;
      --text-sec: #9CA3AF;
      --blue: #3B82F6;
      --blue-dim: rgba(59,130,246,0.15);
      --green: #10B981;
      --green-dim: rgba(16,185,129,0.15);
      --yellow: #F59E0B;
      --yellow-dim: rgba(245,158,11,0.15);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-main);
      color: var(--text-prime);
      line-height: 1.6;
      font-size: 14px;
      display: flex;
      min-height: 100vh;
    }}
    
    /* SIDEBAR */
    .sidebar {{
      width: 260px;
      background-color: var(--bg-side);
      border-right: 1px solid var(--border);
      padding: 24px 0;
      flex-shrink: 0;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }}
    .sb-header {{ padding: 0 24px 20px; border-bottom: 1px solid var(--border); margin-bottom: 20px; }}
    .sb-tag {{ font-size: 10px; font-weight: 700; color: var(--orange); background: var(--orange-dim); padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 12px; }}
    .sb-title {{ font-family: 'Montserrat', sans-serif; font-size: 15px; font-weight: 700; line-height: 1.3; margin-bottom: 4px; }}
    .sb-sub {{ font-size: 11px; color: var(--text-sec); }}
    
    .nav-group {{ margin-bottom: 24px; }}
    .nav-head {{ font-size: 10px; font-weight: 700; color: var(--text-sec); letter-spacing: 1px; padding: 0 24px; margin-bottom: 8px; text-transform: uppercase; }}
    .sidebar ul {{ list-style: none; }}
    .sidebar li a {{
      display: block;
      padding: 8px 24px;
      color: var(--text-sec);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      transition: all 0.2s;
    }}
    .sidebar li a:hover {{ background: rgba(255,255,255,0.05); color: #fff; }}
    .sidebar li a .n {{ opacity: 0.5; margin-right: 8px; font-family: monospace; }}

    /* MAIN CONTENT */
    .main {{
      flex: 1;
      padding: 40px 60px;
      max-width: 1000px;
    }}
    
    /* HEADER CARD */
    .hero-card {{
      background: linear-gradient(145deg, #1A1F26 0%, #151921 100%);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 32px;
      margin-bottom: 48px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    .hero-tag {{ border: 1px solid var(--orange); color: var(--orange); font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 999px; display: inline-block; margin-bottom: 16px; letter-spacing: 1px; }}
    .hero-card h1 {{ font-family: 'Montserrat', sans-serif; font-size: 26px; font-weight: 800; margin-bottom: 8px; }}
    .hero-card h1 span {{ color: var(--orange); }}
    .hero-card p {{ color: var(--text-sec); font-size: 14px; margin-bottom: 24px; }}
    .hero-meta {{ display: flex; gap: 40px; border-top: 1px solid var(--border); padding-top: 20px; }}
    .hm-item {{ display: flex; flex-direction: column; }}
    .hm-label {{ font-size: 10px; font-weight: 600; color: var(--text-sec); text-transform: uppercase; margin-bottom: 4px; }}
    .hm-val {{ font-size: 13px; font-weight: 500; color: #fff; }}
    .hm-val.org {{ color: var(--orange); }}

    /* SECTION HEADER */
    .sec-hdr {{ display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }}
    .sec-num {{ background: var(--orange); color: #fff; width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 800; font-family: 'Montserrat'; }}
    .sec-title h2 {{ font-size: 20px; font-weight: 700; margin-bottom: 2px; }}
    .sec-title p {{ font-size: 13px; color: var(--text-sec); font-weight: 500; }}
    section {{ margin-bottom: 56px; }}

    /* CALLOUT */
    .callout {{ background: var(--blue-dim); border-left: 3px solid var(--blue); padding: 12px 16px; border-radius: 4px 8px 8px 4px; font-size: 13px; font-weight: 500; display: flex; gap: 12px; align-items: center; margin-bottom: 24px; color: #93C5FD; }}
    
    /* TABLES */
    .tw {{ background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border); overflow: hidden; }}
    table {{ width: 100%; border-collapse: collapse; text-align: left; }}
    thead {{ border-bottom: 1px solid var(--orange); }}
    th {{ padding: 14px 20px; font-size: 11px; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 0.5px; }}
    td {{ padding: 14px 20px; border-bottom: 1px solid var(--border); font-size: 13px; }}
    tr:last-child td {{ border-bottom: none; }}
    
    /* PILLS & BADGES */
    .rank-pill {{ display: inline-flex; align-items: center; padding: 4px 12px; border-radius: 999px; border: 1px solid; font-size: 12px; font-weight: 700; background: rgba(0,0,0,0.2); }}
    .rp-r1 {{ border-color: var(--orange); color: var(--orange); }}
    .rp-r2 {{ border-color: var(--yellow); color: var(--yellow); }}
    .rp-r3 {{ border-color: var(--blue); color: var(--blue); }}
    .rp-un {{ border-color: var(--text-sec); color: var(--text-sec); }}
    
    .kpi-pill {{ display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; }}
    .kpi-green {{ background: var(--green-dim); color: var(--green); }}
    .kpi-blue {{ background: var(--blue-dim); color: var(--blue); }}
    .kpi-gray {{ background: rgba(255,255,255,0.05); color: var(--text-sec); }}
    
    .layer-badge {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; color: white; }}
    .layer-badge.l2 {{ background: var(--orange); }}
    .layer-badge.l3 {{ background: var(--yellow); }}
    .layer-badge.l4 {{ background: var(--blue); }}
    .layer-badge.l5 {{ background: var(--text-sec); }}
    .layer-badge.l6 {{ background: #4B5563; }}

    .good {{ color: var(--green); font-weight: 600; }}
    .warn {{ color: var(--text-sec); font-style: italic; }}
    
    a {{ color: var(--blue); text-decoration: none; }}
  </style>
</head>
<body>

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="sb-header">
      <span class="sb-tag">PARAMS SHEET</span>
      <div class="sb-title">Driver Ranking &<br>AhaBenefits v2.0</div>
      <div class="sb-sub">Driver Management · 2026</div>
    </div>
    
    <div class="nav-group">
      <div class="nav-head">RANKING</div>
      <ul>
        <li><a href="#s1"><span class="n">01</span> KPI Thresholds</a></li>
        <li><a href="#s2"><span class="n">02</span> Layer Access</a></li>
        <li><a href="#s3"><span class="n">03</span> Quyền lợi theo Rank</a></li>
      </ul>
    </div>
    
    <div class="nav-group">
      <div class="nav-head">AHABENEFITS</div>
      <ul>
        <li><a href="#s4"><span class="n">04</span> Quyền lợi Layer</a></li>
        <li><a href="#s5"><span class="n">05</span> Catalog</a></li>
      </ul>
    </div>
    
    <div class="nav-group">
      <div class="nav-head">SUMMARY</div>
      <ul>
        <li><a href="#s6"><span class="n">06</span> Bảng Tổng Hợp</a></li>
        <li><a href="#s7"><span class="n">07</span> Timeline Triển Khai</a></li>
      </ul>
    </div>
    
    <div class="nav-group" style="margin-top:40px; border-top:1px solid var(--border); padding-top:20px;">
      <div class="nav-head">Tham chiếu</div>
      <ul>
        <li><a href="2026-05-driver-ranking-layer-benefits.html" style="font-size:11px; line-height:1.4;">2026-05-driver-ranking-layer-benefits.html</a></li>
        <li><a href="2026-05-driver-ranking-diagram.html" style="font-size:11px; line-height:1.4;">2026-05-driver-ranking-diagram.html</a></li>
      </ul>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main">
    
    <div class="hero-card">
      <div class="hero-tag">⚡ EDITABLE PARAMS</div>
      <h1>Driver Ranking & <span>AhaBenefits v2.0</span><br>Params Sheet</h1>
      <p>Toàn bộ con số có thể điều chỉnh. Sau khi sửa → cập nhật vào HTML tương ứng.</p>
      <div class="hero-meta">
        <div class="hm-item">
          <span class="hm-label">CẬP NHẬT</span>
          <span class="hm-val">2026-07-07</span>
        </div>
        <div class="hm-item">
          <span class="hm-label">OWNER</span>
          <span class="hm-val">Driver Management</span>
        </div>
        <div class="hm-item">
          <span class="hm-label">SCOPE</span>
          <span class="hm-val">SGN + HAN - Bike</span>
        </div>
        <div class="hm-item">
          <span class="hm-label">VERSION</span>
          <span class="hm-val org">v2.0</span>
        </div>
      </div>
    </div>

    {content_html}

  </main>

</body>
</html>
"""

# Now we need to modify the sections inside new_html to match the pill styles
new_html = new_html.replace('<span class="rank-r1">💎 R1 Elite</span>', '<span class="rank-pill rp-r1">💎 R1 Elite</span>')
new_html = new_html.replace('<span class="rank-r2">🥇 R2 Active</span>', '<span class="rank-pill rp-r2">🥇 R2 Active</span>')
new_html = new_html.replace('<span class="rank-r3">🥈 R3 Standard</span>', '<span class="rank-pill rp-r3">🥈 R3 Standard</span>')
new_html = new_html.replace('<span class="rank-un">Unranked</span>', '<span class="rank-pill rp-un">Unranked</span>')

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(new_html)

