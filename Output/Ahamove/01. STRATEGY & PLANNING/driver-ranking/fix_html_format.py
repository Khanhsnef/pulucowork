import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Unranked L5-6 MASS
content = content.replace("<td>L5-6 MASS (slot trống còn lại)</td>", "<td>L5-6 MASS (slot trống còn lại)</td>")
content = content.replace("<td><strong style=\"color:var(--text-sec);\">Ngày 2+</strong></td>", "<td><strong style=\"color:var(--text-sec);\">Ngày 2+</strong></td>")

# Fix target table formatting if the regex messed it up
content = re.sub(r'<tr>\s*<td><span class="rank-pill rp-un">Unranked</span></td>\s*<td class="num" style="color:var\(--[a-z-]+\);">30-40%</td>\s*<td class="num">~4\.000 - 6\.000</td>\s*</tr>', 
                 '<tr>\n              <td><span class="rank-pill rp-un">Unranked</span></td>\n              <td class="num" style="color:var(--text-sec);">30-40%</td>\n              <td class="num">~4.000 - 6.000</td>\n            </tr>', content)

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)

