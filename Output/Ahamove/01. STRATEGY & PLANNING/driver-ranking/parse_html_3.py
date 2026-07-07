with open("2026-05-driver-ranking-layer-benefits.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Master Table updates
content = content.replace("<th>AhaBenefits (× hệ số + bonus)</th>", "<th>AhaBenefits (× hệ số)</th>")
content = content.replace('<span class="mult m15">×1.5 +30 pts</span>', '<span class="mult m15">×1.5</span>')
content = content.replace('<span class="mult m13">×1.3 +25 pts</span>', '<span class="mult m13">×1.3</span>')
content = content.replace('<span class="mult m11">×1.1 +20 pts</span>', '<span class="mult m11">×1.1</span>')

# 2. AhaBenefits Section (if any mention of + bonus ca)
content = content.replace("Nhân hệ số theo layer + bonus ca.", "Nhân hệ số theo layer.")
content = content.replace('<div style="font-size:12px;font-weight:700;color:var(--orange);">Bonus ca : +30 pts</div>', '')
content = content.replace('<div style="font-size:12px;font-weight:700;color:var(--blue);">Bonus ca : +25 pts</div>', '')
content = content.replace('<div style="font-size:12px;font-weight:700;color:var(--g600);">Bonus ca : +20 pts</div>', '')
content = content.replace('<div style="font-size:12px;font-weight:700;color:var(--g600);">Không có bonus ca</div>', '')

# Earning grids
content = content.replace('<div class="earn-pts">114</div>', '<div class="earn-pts">84</div>')
content = content.replace('<div class="earn-pts">93</div>', '<div class="earn-pts">68</div>')
content = content.replace('<div class="earn-pts">73</div>', '<div class="earn-pts">53</div>')
content = content.replace('<div class="earn-pts">44</div>', '<div class="earn-pts">44</div>')
content = content.replace('~114 pts/ca', '~84 pts/ca')
content = content.replace('~93 pts/ca', '~68 pts/ca')
content = content.replace('~73 pts/ca', '~53 pts/ca')
content = content.replace('56 × 1.5 + 30', '56 × 1.5')
content = content.replace('52 × 1.3 + 25', '52 × 1.3')
content = content.replace('48 × 1.1 + 20', '48 × 1.1')

# Table Bonus ca -> Hỗ trợ
content = content.replace('Hệ số Layer &amp; Bonus/ca', 'Hệ số Layer &amp; Hỗ trợ')
content = content.replace('<th style="padding:8px 10px;text-align:center;font-weight:700;color:var(--g600);font-size:11px;">Bonus ca</th>', '<th style="padding:8px 10px;text-align:center;font-weight:700;color:var(--g600);font-size:11px;">Hỗ trợ</th>')
content = content.replace('<td style="padding:9px 10px;text-align:center;color:var(--orange);font-weight:700;">+30 pts</td>', '<td style="padding:9px 10px;text-align:center;color:var(--orange);font-weight:700;">Đội trưởng</td>')
content = content.replace('<td style="padding:9px 10px;text-align:center;color:var(--blue);font-weight:700;">+25 pts</td>', '<td style="padding:9px 10px;text-align:center;color:var(--blue);font-weight:700;">Đội trưởng</td>')
content = content.replace('<td style="padding:9px 10px;text-align:center;color:var(--g600);font-weight:700;">+20 pts</td>', '<td style="padding:9px 10px;text-align:center;color:var(--g600);font-weight:700;">Đội trưởng</td>')
content = content.replace('<td style="padding:9px 10px;text-align:center;color:var(--g400);">—</td>', '<td style="padding:9px 10px;text-align:center;color:var(--g400);">Đội trưởng</td>', 1)
content = content.replace('<td style="padding:9px 10px;text-align:center;color:var(--g400);">—</td>', '<td style="padding:9px 10px;text-align:center;color:var(--g400);">Không</td>', 1)
content = content.replace('<td style="padding:9px 10px;text-align:center;color:var(--g400);">—</td>', '<td style="padding:9px 10px;text-align:center;color:var(--g400);">Không</td>')

with open("2026-05-driver-ranking-layer-benefits.html", "w", encoding="utf-8") as f:
    f.write(content)
