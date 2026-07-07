import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

dark_css = """    :root {
      --bg: #0f172a;
      --surface: #1e293b;
      --text-prime: #f8fafc;
      --text-sec: #cbd5e1;
      --text-muted: #94a3b8;
      --border: #334155;
      --blue: #58A6FF;
      --orange: #FF7F32;
      --yellow: #F59E0B;
      --green: #34d399;
      --red: #f87171;
      --purple: #a78bfa;
      --bg-code: #0f172a;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: var(--text-prime); line-height: 1.6; font-size: 14px; padding: 40px 20px; }
    .container { max-width: 900px; margin: 0 auto; background: var(--surface); border-radius: 12px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    h1, h2, h3 { font-family: 'Montserrat', sans-serif; }
    
    .sec-hdr { display: flex; align-items: flex-start; gap: 16px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid var(--border); }
    .sec-num { font-size: 32px; font-weight: 800; color: var(--blue); opacity: 0.2; line-height: 1; }
    .sec-title h2 { font-size: 22px; font-weight: 700; color: var(--blue); margin-bottom: 4px; }
    .sec-title p { font-size: 13px; color: var(--text-sec); font-weight: 500; }
    section { margin-bottom: 48px; }

    .callout { display: flex; gap: 12px; padding: 12px 16px; border-radius: 8px; font-size: 13px; font-weight: 500; }
    .callout.ci { background: rgba(88,166,255,0.1); color: #93c5fd; border-left: 4px solid var(--blue); }
    
    .tw { overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 16px; }
    table { width: 100%; border-collapse: collapse; text-align: left; }
    th { background: rgba(255,255,255,0.05); padding: 12px 16px; font-size: 12px; font-weight: 600; color: var(--text-sec); border-bottom: 1px solid var(--border); }
    td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid var(--border); vertical-align: middle; }
    tr:last-child td { border-bottom: none; }
    
    .rank-r1 { font-weight: 700; color: var(--orange); }
    .rank-r2 { font-weight: 700; color: var(--yellow); }
    .rank-r3 { font-weight: 700; color: var(--blue); }
    .rank-un { font-weight: 600; color: var(--text-muted); }
    
    .kpi-pill { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 600; }
    .kpi-green { background: rgba(52,211,153,0.15); color: #34d399; }
    .kpi-blue { background: rgba(88,166,255,0.15); color: #93c5fd; }
    .kpi-gray { background: rgba(148,163,184,0.15); color: #cbd5e1; }
    
    .layer-badge { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; color: white; }
    .layer-badge.l2 { background: var(--orange); }
    .layer-badge.l3 { background: var(--yellow); }
    .layer-badge.l4 { background: var(--blue); }
    .layer-badge.l5 { background: var(--text-sec); }
    .layer-badge.l6 { background: var(--text-muted); }

    .good { color: var(--green); font-weight: 600; }
    .warn { color: var(--text-muted); font-style: italic; }"""

content = re.sub(r'    :root \{.*?</style>', dark_css + "\n  </style>", content, flags=re.DOTALL)

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)
