with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Layer Multiplier Table (remove Bonus ca, add Hỗ trợ)
# We can find the table header:
content = content.replace("<th>Bonus ca</th>", "<th>Hỗ trợ</th>")
# Now replace the values row by row
content = content.replace('<td><strong style="color:var(--orange);">+30 pts</strong></td>', '<td><strong style="color:var(--orange);">Đội trưởng</strong></td>')
content = content.replace('<td><strong style="color:var(--yellow);">+25 pts</strong></td>', '<td><strong style="color:var(--yellow);">Đội trưởng</strong></td>')
content = content.replace('<td><strong style="color:var(--blue);">+20 pts</strong></td>', '<td><strong style="color:var(--blue);">Đội trưởng</strong></td>')
content = content.replace('<td><strong>—</strong></td>', '<td><strong>Đội trưởng</strong></td>', 1) # for L5
content = content.replace('<td><strong>—</strong></td>', '<td>Không</td>', 2) # for L6 and overflow

# 2. Update Earn Estimate Table
content = content.replace("<th>Bonus ca</th>\n              <th>Tổng/ca</th>", "<th>Tổng/ca</th>")
content = content.replace('<td class="num" style="color:var(--orange);">+30</td>\n              <td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--orange);">114</span>\n              </td>', '<td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--orange);">84</span>\n              </td>')
content = content.replace('<td class="num" style="color:var(--yellow);">+25</td>\n              <td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--yellow);">93</span>\n              </td>', '<td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--yellow);">68</span>\n              </td>')
content = content.replace('<td class="num" style="color:var(--blue);">+20</td>\n              <td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--blue);">73</span>\n              </td>', '<td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--blue);">53</span>\n              </td>')
content = content.replace('<td class="num" style="color:var(--text-sec);">—</td>\n              <td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--text-sec);">44</span>\n              </td>', '<td><span\n                  style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--text-sec);">44</span>\n              </td>')
content = content.replace('<td class="na">—</td>\n              <td><span style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--text-sec);">base</span></td>', '<td><span style="font-family:\'Montserrat\',monospace;font-size:16px;font-weight:800;color:var(--text-sec);">base</span></td>')

# 3. Update Calibration
calib_old = """Pts tích/tháng (avg, 22 ca):
  R1: 114 × 22 = 2.508 pts  (15% fleet)
  R2: 93 × 22 = 2.046 pts  (35% fleet)
  R3: 73 × 22 = 1.606 pts  (35% fleet)
  L6: 44 × 22 = 968 pts  (15% fleet)
  Weighted avg ≈ 1.836 pts/tháng

80% burn → paid reward:  1.836 × 80% = ~1.468 pts ≈ 50.000 VND
  → Paid reward 50k = 1.500 pts (làm tròn)

20% còn lại → free partner:  ~360 pts/tháng
  → Free items giá 40–170 pts → đổi được 2–5 món/tháng"""
calib_new = """Pts tích/tháng (avg, 22 ca):
  R1: 84 × 22 = 1.848 pts  (15% fleet)
  R2: 68 × 22 = 1.496 pts  (35% fleet)
  R3: 53 × 22 = 1.166 pts  (35% fleet)
  L6: 44 × 22 = 968 pts  (15% fleet)
  Weighted avg ≈ 1.340 pts/tháng

80% burn → paid reward:  1.340 × 80% = ~1.072 pts ≈ 50.000 VND
  → Paid reward 50k = 1.000 pts (cân chỉnh lại)

20% còn lại → free partner:  ~268 pts/tháng
  → Free items giá 40–170 pts → đổi được 1–4 món/tháng"""
content = content.replace(calib_old, calib_new)

# Table calibration
content = content.replace("80% → Paid 50k (1.500p)", "80% → Paid 50k (1.000p)")
content = content.replace('<td class="num" style="color:var(--orange);">2.508</td>', '<td class="num" style="color:var(--orange);">1.848</td>')
content = content.replace('✅ 1.500 pts <span style="color:var(--text-muted);font-size:11px;">(dư ~1.008)</span>', '✅ 1.000 pts <span style="color:var(--text-muted);font-size:11px;">(dư ~848)</span>')
content = content.replace('~1.000 pts free', '~800 pts free')

content = content.replace('<td class="num" style="color:var(--yellow);">2.046</td>', '<td class="num" style="color:var(--yellow);">1.496</td>')
content = content.replace('✅ 1.500 pts <span style="color:var(--text-muted);font-size:11px;">(dư ~546)</span>', '✅ 1.000 pts <span style="color:var(--text-muted);font-size:11px;">(dư ~496)</span>')
content = content.replace('~500 pts free', '~400 pts free')

content = content.replace('<td class="num" style="color:var(--blue);">1.606</td>', '<td class="num" style="color:var(--blue);">1.166</td>')
content = content.replace('✅ 1.500 pts <span style="color:var(--text-muted);font-size:11px;">(dư ~106)</span>', '✅ 1.000 pts <span style="color:var(--text-muted);font-size:11px;">(dư ~166)</span>')
content = content.replace('~100 pts free', '~100 pts free') # stays 100

content = content.replace('❌ cần ~1.5 tháng', '❌ cần ~1.1 tháng')
content = content.replace('≈ 35đ', '≈ 50đ')
content = content.replace('1.500 pts', '1.000 pts')

# 4. Update Summary Layer Table (6.2)
layer_sum_old = """            <tr>
              <td style="font-size:12.5px;color:var(--text-sec);">Rank ưu tiên</td>
              <td><span class="rank-r1">R1</span></td>
              <td><span class="rank-r2">R2</span></td>
              <td><span class="rank-r3">R3</span></td>
              <td style="font-size:12px;color:var(--text-sec);">Overflow R3</td>
              <td><span class="rank-un">Unranked</span></td>
            </tr>"""
layer_sum_new = """            <tr>
              <td style="font-size:12.5px;color:var(--text-sec);">Rank ưu tiên</td>
              <td><span class="rank-r1">R1</span></td>
              <td><span class="rank-r2">R2</span></td>
              <td><span class="rank-r3">R3</span></td>
              <td style="font-size:12px;color:var(--text-sec);">Bất kỳ</td>
              <td><span class="rank-un">Unranked</span></td>
            </tr>
            <tr>
              <td style="font-size:12.5px;color:var(--text-sec);">Hỗ trợ</td>
              <td>Đội trưởng</td>
              <td>Đội trưởng</td>
              <td>Đội trưởng</td>
              <td>Đội trưởng</td>
              <td style="font-size:12px;color:var(--text-sec);">Không</td>
            </tr>"""
content = content.replace(layer_sum_old, layer_sum_new)

# Update Catalog formulas
content = content.replace("Điểm = Giá trị thực (VND) ÷ 35", "Điểm = Giá trị thực (VND) ÷ 50")
# I'm not updating the specific catalog table HTML point numbers (e.g. <strong class="num" style="color:var(--blue);">170</strong> to 600) for now unless I use regex because there are a lot of them. Wait, since I'm already using Python, let's just do it so they match.
content = content.replace('<strong class="num" style="color:var(--blue);">170</strong>', '<strong class="num" style="color:var(--blue);">600</strong>')
content = content.replace('<strong class="num" style="color:var(--blue);">65</strong>', '<strong class="num" style="color:var(--blue);">1.000</strong>')
content = content.replace('<strong class="num" style="color:var(--blue);">55</strong>', '<strong class="num" style="color:var(--blue);">400</strong>')
content = content.replace('<strong class="num" style="color:var(--blue);">400</strong>', '<strong class="num" style="color:var(--blue);">1.000</strong>')
content = content.replace('<strong class="num" style="color:var(--blue);">1.400</strong>', '<strong class="num" style="color:var(--blue);">2.400</strong>')

content = content.replace('<strong class="num" style="color:var(--yellow);">285</strong>', '<strong class="num" style="color:var(--yellow);">1.000</strong>')
content = content.replace('<strong class="num" style="color:var(--yellow);">170</strong>', '<strong class="num" style="color:var(--yellow);">3.000</strong>')
content = content.replace('<strong class="num" style="color:var(--yellow);">140</strong>', '<strong class="num" style="color:var(--yellow);">1.000</strong>')
content = content.replace('<strong class="num" style="color:var(--yellow);">40</strong>', '<strong class="num" style="color:var(--yellow);">800</strong>')
content = content.replace('<strong class="num" style="color:var(--yellow);">700</strong>', '<strong class="num" style="color:var(--yellow);">1.600</strong>')
content = content.replace('<strong class="num" style="color:var(--yellow);">2.300</strong>', '<strong class="num" style="color:var(--yellow);">5.000</strong>')
content = content.replace('<strong class="num" style="color:var(--yellow);">3.400</strong>', '<strong class="num" style="color:var(--yellow);">6.000</strong>')

content = content.replace('<strong class="num" style="color:var(--orange);">255</strong>', '<strong class="num" style="color:var(--orange);">5.000</strong>')
content = content.replace('<strong class="num" style="color:var(--orange);">285</strong>', '<strong class="num" style="color:var(--orange);">2.000</strong>')
content = content.replace('<strong class="num" style="color:var(--orange);">170</strong>', '<strong class="num" style="color:var(--orange);">3.400</strong>')
content = content.replace('<strong class="num" style="color:var(--orange);">1.400</strong>', '<strong class="num" style="color:var(--orange);">3.000</strong>')

content = content.replace('<strong class="num" style="color:var(--purple);">285</strong>', '<strong class="num" style="color:var(--purple);">200</strong>')
content = content.replace('<strong class="num" style="color:var(--purple);">857</strong>', '<strong class="num" style="color:var(--purple);">600</strong>')

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)
