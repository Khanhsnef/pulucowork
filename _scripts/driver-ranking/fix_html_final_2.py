import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# 2. Fix base points in "ƯỚC TÍNH PTS/CA" table (using re.DOTALL to match newlines inside span tags)
content = re.sub(r'<td class="num">56</td>\s*<td class="num" style="color:var\(--orange\);">56 × 1\.5 = 84</td>\s*<td><span(.*?)>84</span>',
                 r'<td class="num">280</td>\n              <td class="num" style="color:var(--orange);">280 × 1.5 = 420</td>\n              <td><span\1>420</span>', content, flags=re.DOTALL)

content = re.sub(r'<td class="num">52</td>\s*<td class="num" style="color:var\(--yellow\);">52 × 1\.3 = 68</td>\s*<td><span(.*?)>68</span>',
                 r'<td class="num">260</td>\n              <td class="num" style="color:var(--yellow);">260 × 1.3 = 338</td>\n              <td><span\1>338</span>', content, flags=re.DOTALL)

content = re.sub(r'<td class="num">48</td>\s*<td class="num" style="color:var\(--blue\);">48 × 1\.1 = 53</td>\s*<td><span(.*?)>53</span>',
                 r'<td class="num">240</td>\n              <td class="num" style="color:var(--blue);">240 × 1.1 = 264</td>\n              <td><span\1>264</span>', content, flags=re.DOTALL)

content = re.sub(r'<td class="num">44</td>\s*<td class="num" style="color:var\(--text-sec\);">44 × 1\.0 = 44</td>\s*<td><span(.*?)>44</span>',
                 r'<td class="num">220</td>\n              <td class="num" style="color:var(--text-sec);">220 × 1.0 = 220</td>\n              <td><span\1>220</span>', content, flags=re.DOTALL)

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)
