import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix "ƯỚC TÍNH PTS/CA" table header alignment
# The header has "<th>Hỗ trợ</th>", which needs to be removed.
content = re.sub(r'<th>Hỗ trợ</th>\s*<th>Tổng/ca</th>', r'<th>Tổng/ca</th>', content)

# 2. Fix base points in "ƯỚC TÍNH PTS/CA" table
content = re.sub(r'<td class="num">56</td>\s*<td class="num" style="color:var\(--orange\);">56 × 1\.5 = 84</td>\s*<td><span(.*?)>84</span>',
                 r'<td class="num">280</td>\n              <td class="num" style="color:var(--orange);">280 × 1.5 = 420</td>\n              <td><span\1>420</span>', content)

content = re.sub(r'<td class="num">52</td>\s*<td class="num" style="color:var\(--yellow\);">52 × 1\.3 = 68</td>\s*<td><span(.*?)>68</span>',
                 r'<td class="num">260</td>\n              <td class="num" style="color:var(--yellow);">260 × 1.3 = 338</td>\n              <td><span\1>338</span>', content)

content = re.sub(r'<td class="num">48</td>\s*<td class="num" style="color:var\(--blue\);">48 × 1\.1 = 53</td>\s*<td><span(.*?)>53</span>',
                 r'<td class="num">240</td>\n              <td class="num" style="color:var(--blue);">240 × 1.1 = 264</td>\n              <td><span\1>264</span>', content)

content = re.sub(r'<td class="num">44</td>\s*<td class="num" style="color:var\(--text-sec\);">44 × 1\.0 = 44</td>\s*<td><span(.*?)>44</span>',
                 r'<td class="num">220</td>\n              <td class="num" style="color:var(--text-sec);">220 × 1.0 = 220</td>\n              <td><span\1>220</span>', content)

# 3. Fix Calibration table
content = re.sub(r'<td class="num" style="color:var\(--orange\);">1\.848</td>\s*<td class="good">✅ 1\.000 pts <span(.*?)>\(dư ~848\)</span></td>\s*<td(.*?)>~800 pts free</td>',
                 r'<td class="num" style="color:var(--orange);">9.240</td>\n              <td class="good">✅ 5.000 pts <span\1>(dư ~4.240)</span></td>\n              <td\2>~4.000 pts free</td>', content)

content = re.sub(r'<td class="num" style="color:var\(--yellow\);">1\.496</td>\s*<td class="good">✅ 1\.000 pts <span(.*?)>\(dư ~496\)</span></td>\s*<td(.*?)>~400 pts free</td>',
                 r'<td class="num" style="color:var(--yellow);">7.436</td>\n              <td class="good">✅ 5.000 pts <span\1>(dư ~2.436)</span></td>\n              <td\2>~2.000 pts free</td>', content)

content = re.sub(r'<td class="num" style="color:var\(--blue\);">1\.166</td>\s*<td class="warn">✅ 1\.000 pts <span(.*?)>\(dư ~166\)</span>\s*</td>\s*<td(.*?)>~100 pts free</td>',
                 r'<td class="num" style="color:var(--blue);">5.808</td>\n              <td class="warn">✅ 5.000 pts <span\1>(dư ~808)</span>\n              </td>\n              <td\2>~800 pts free</td>', content)

content = re.sub(r'<td class="num">968</td>', r'<td class="num">4.840</td>', content)

# 4. Fix Catalog Prices (The points column)
# Section 5 prices
content = re.sub(r'<strong class="num" style="color:var\(--blue\);">600</strong>', r'<strong class="num" style="color:var(--blue);">3.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--blue\);">1\.000</strong>', r'<strong class="num" style="color:var(--blue);">5.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--blue\);">2\.400</strong>', r'<strong class="num" style="color:var(--blue);">12.000</strong>', content)

content = re.sub(r'<strong class="num" style="color:var\(--yellow\);">1\.000</strong>', r'<strong class="num" style="color:var(--yellow);">5.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--yellow\);">3\.000</strong>', r'<strong class="num" style="color:var(--yellow);">15.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--yellow\);">800</strong>', r'<strong class="num" style="color:var(--yellow);">4.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--yellow\);">1\.600</strong>', r'<strong class="num" style="color:var(--yellow);">8.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--yellow\);">5\.000</strong>', r'<strong class="num" style="color:var(--yellow);">25.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--yellow\);">6\.000</strong>', r'<strong class="num" style="color:var(--yellow);">30.000</strong>', content)

content = re.sub(r'<strong class="num" style="color:var\(--orange\);">5\.000</strong>', r'<strong class="num" style="color:var(--orange);">25.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--orange\);">2\.000</strong>', r'<strong class="num" style="color:var(--orange);">10.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--orange\);">3\.400</strong>', r'<strong class="num" style="color:var(--orange);">17.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--orange\);">3\.000</strong>', r'<strong class="num" style="color:var(--orange);">15.000</strong>', content)
content = re.sub(r'<strong class="num" style="color:var\(--orange\);">200</strong>', r'<strong class="num" style="color:var(--orange);">1.000</strong>', content)
# Ensure 600 pts/thang for R1 is replaced properly
content = re.sub(r'<strong class="num" style="color:var\(--orange\);">600</strong>', r'<strong class="num" style="color:var(--orange);">3.000</strong>', content)
# 285-600 -> 1000-3000 in text
content = content.replace("285–600", "1.000–3.000")

# Fix 9.2 Layer table equivalent (In params.html it's 6.2 Theo Layer)
content = re.sub(r'<tr>\s*<td><strong>Hỗ trợ</strong></td>\s*<td class="good">Đội trưởng</td>\s*<td class="good">Đội trưởng</td>\s*<td class="good">Đội trưởng</td>\s*<td class="good">Đội trưởng</td>\s*<td class="warn">Không</td>\s*</tr>',
                 r'<tr>\n              <td><strong>Hỗ trợ</strong></td>\n              <td class="good">Đội trưởng</td>\n              <td class="good">Đội trưởng</td>\n              <td class="warn">Không</td>\n              <td class="warn">Không</td>\n              <td class="warn">Không</td>\n            </tr>', content)

# Ensure "Slot đăng ký" row in 6.1 Bảng Tổng Hợp is aligned. The screenshot doesn't show "Slot đăng ký" but has "Ưu tiên đăng ký Layer". 
# Wait, "Ưu tiên đăng ký Layer" is the "Khung giờ đăng ký ca (Ngày 1)" in the markdown? No, it's just what it is in the HTML.
# My script sync_html.py did:
# content = content.replace("<tr>\n              <td><strong>Khung giờ đăng ký ca (Ngày 1)</strong></td>", "<tr>\n              <td><strong>Slot đăng ký</strong></td>\n              <td>Tất cả L2-L6</td>\n              <td>Tất cả L2-L6</td>\n              <td>Tất cả L2-L6</td>\n              <td>L5-6 MASS</td>\n            </tr>\n            <tr>\n              <td><strong>Khung giờ đăng ký ca (Ngày 1)</strong></td>")
# This might have worked but caused an issue? Actually, "Khung giờ đăng ký ca (Ngày 1)" has 5 columns, including the row header.
# Let's remove the "Slot đăng ký" row entirely to revert to original format.
content = re.sub(r'<tr>\s*<td><strong>Slot đăng ký</strong></td>.*?</tr>\s*(<tr>\s*<td><strong>Khung giờ đăng ký ca \(Ngày 1\))', r'\1', content, flags=re.DOTALL)


# Write back
with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)

