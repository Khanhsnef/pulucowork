import re

with open("2026-05-driver-ranking-layer-benefits.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix L4 Support
content = re.sub(r'(<td class="zone-name">L4 Bigzone</td>.*?)<td class="support">Đội trưởng</td>', r'\1<td class="support">Không</td>', content, flags=re.DOTALL)
content = re.sub(r'(<td class="zone-name">L5 Cityzone</td>.*?)<td class="support">Đội trưởng</td>', r'\1<td class="support">Không</td>', content, flags=re.DOTALL)

content = content.replace("Unranked / L6 không có quyền truy cập catalog", "Unranked / L6 không có quyền truy cập catalog, chỉ truy cập được các rewards mass")
content = content.replace("Unranked không có structured slot — nhận đơn on-demand từ khi đơn từ các layer tràn xuống.", "")

with open("2026-05-driver-ranking-layer-benefits.html", "w", encoding="utf-8") as f:
    f.write(content)

