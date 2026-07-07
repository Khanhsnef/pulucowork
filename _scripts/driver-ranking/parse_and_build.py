import re

with open("2026-05-driver-ranking-params.md", "r", encoding="utf-8") as f:
    md_content = f.read()

import markdown2
html_content = markdown2.markdown(md_content, extras=["tables", "fenced-code-blocks", "header-ids"])

# Let's assign section classes and structure
# We split by <h2
sections = html_content.split("<h2")
new_html_content = sections[0]
for i in range(1, len(sections)):
    s = "<h2" + sections[i]
    new_html_content += f'\n<section id="s{i}">\n'
    
    # Extract title text
    title_match = re.search(r'>\d+\.\s+(.*?)</h2', s)
    if title_match:
        title = title_match.group(1)
        # Create sec-hdr
        hdr = f"""
      <div class="sec-hdr">
        <div class="sec-num">0{i}</div>
        <div class="sec-title">
          <h2>{title}</h2>
        </div>
      </div>
"""
        s = re.sub(r'<h2.*?>.*?</h2>', hdr, s)
    new_html_content += s + "\n</section>\n"

# Replace blockquotes with callouts
new_html_content = new_html_content.replace("<blockquote>\n  <p>", '<div class="callout ci">\n  <span style="font-size:15px;flex-shrink:0;">ℹ</span>\n  <div class="callout-body">')
new_html_content = new_html_content.replace("</p>\n</blockquote>", '</div>\n</div>')

# Wrap tables with .tw
new_html_content = re.sub(r'(<table>.*?</table>)', r'<div class="tw">\n\1\n</div>', new_html_content, flags=re.DOTALL)

# Add rank pills
new_html_content = new_html_content.replace('💎 R1 Kim Cương', '<span class="rank-pill rp-r1">💎 R1 Kim Cương</span>')
new_html_content = new_html_content.replace('R1 Elite', '<span class="rank-pill rp-r1">💎 R1 Elite</span>')
new_html_content = new_html_content.replace('🥇 R2 Vàng', '<span class="rank-pill rp-r2">🥇 R2 Vàng</span>')
new_html_content = new_html_content.replace('R2 Active', '<span class="rank-pill rp-r2">🥇 R2 Active</span>')
new_html_content = new_html_content.replace('🥈 R3 Bạc', '<span class="rank-pill rp-r3">🥈 R3 Bạc</span>')
new_html_content = new_html_content.replace('R3 Standard', '<span class="rank-pill rp-r3">🥈 R3 Standard</span>')
new_html_content = new_html_content.replace('Unranked', '<span class="rank-pill rp-un">Unranked</span>')

# Add KPI pills
def kpi_pill(match):
    val = match.group(0)
    if '≥' in val or '100%' in val:
        return f'<span class="kpi-pill kpi-green">{val}</span>'
    elif '<' in val:
        return f'<span class="kpi-pill kpi-gray">{val}</span>'
    return val

new_html_content = re.sub(r'≥\s*\d+', kpi_pill, new_html_content)
new_html_content = re.sub(r'<\s*\d+', kpi_pill, new_html_content)

# Use rewrite_dark_theme.py logic to wrap everything
with open("rewrite_dark_theme.py", "r") as f:
    template_script = f.read()

# Extract the template parts
template_match = re.search(r'new_html = f"""(.*?)"""', template_script, re.DOTALL)
if template_match:
    template = template_match.group(1)
    template = template.replace("{content_html}", new_html_content)
    
    with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
        f.write(template)

