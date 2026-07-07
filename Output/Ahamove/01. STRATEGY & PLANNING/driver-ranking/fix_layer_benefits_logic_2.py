import re

with open("2026-05-driver-ranking-layer-benefits.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("× 1.5 : 56 × 1.5 = 84 pts", "× 1.5 : 280 × 1.5 = 420 pts")
content = content.replace("→ Tổng : 84 pts/ca", "→ Tổng : 420 pts/ca")
content = content.replace("56 × 1.5 = 84 pts", "280 × 1.5 = 420 pts")

with open("2026-05-driver-ranking-layer-benefits.html", "w", encoding="utf-8") as f:
    f.write(content)

