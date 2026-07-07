import re

with open("2026-07-driver-layer-ranking-present.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update pts in BHTN
content = content.replace("Gói 10k (285 pts) / 30k (857 pts)", "Gói 10k (200 pts) / 30k (600 pts)")

# Add "Sự hỗ trợ" row before "Voucher xăng"
support_row = """          <tr>
            <td>Sự hỗ trợ &amp; Vai trò</td>
            <td class="green-cell">Có Đội trưởng</td>
            <td class="green-cell">Có Đội trưởng</td>
            <td class="green-cell">Có Đội phó</td>
            <td class="red-cell">Không áp dụng</td>
          </tr>
          <tr>
            <td>Voucher xăng/EV hàng tháng</td>"""
content = content.replace("          <tr>\n            <td>Voucher xăng/EV hàng tháng</td>", support_row)

with open("2026-07-driver-layer-ranking-present.html", "w", encoding="utf-8") as f:
    f.write(content)
