import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix L4 Support
content = re.sub(r'(<span class="layer-badge l4">L4</span>.*?</span.*?)<td><strong style="color:var\(--blue\);">Đội trưởng</strong></td>', r'\1<td><span class="warn">Không</span></td>', content, flags=re.DOTALL)
# Fix L5 Support
content = re.sub(r'(<span class="layer-badge l5">L5</span>.*?</span.*?)<td><strong>Đội trưởng</strong></td>', r'\1<td><span class="warn">Không</span></td>', content, flags=re.DOTALL)

# Fix 10-15% targets for R1 and R2
content = re.sub(r'<td>15%</td>(\s*)<td>~1.575</td>', r'<td class="num" style="color:var(--orange);">10-15%</td>\1<td class="num">~1.000 - 1.500</td>', content)
content = re.sub(r'<td>35%</td>(\s*)<td>~3.675</td>', r'<td class="num" style="color:var(--yellow);">10-15%</td>\1<td class="num">~1.000 - 1.500</td>', content, count=1)
content = re.sub(r'<td>35%</td>(\s*)<td>~3.675</td>', r'<td class="num" style="color:var(--blue);">30-40%</td>\1<td class="num">~4.000 - 6.000</td>', content, count=1)

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)

