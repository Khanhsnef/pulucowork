with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("<h2>Timeline Triển Khai (Dự kiến 3 tháng tới)</h2>", "<h2>Timeline Triển Khai (Từ giữa tháng 7/2026)</h2>")

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)
