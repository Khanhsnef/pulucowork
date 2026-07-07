import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'<strong class="num" style="color:var\(--purple\);">200</strong>', r'<strong class="num" style="color:var(--purple);">1.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--purple\);">600</strong>', r'<strong class="num" style="color:var(--purple);">3.000</strong>', content)

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)

