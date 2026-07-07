import re

with open("2026-07-driver-layer-ranking-present.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace SVG text and labels
content = content.replace("1.500 pts", "1.000 pts")
content = content.replace("2.508", "1.848")
content = content.replace("2.046", "1.496")
content = content.replace("1.606", "1.166")

# Fix Legend
content = content.replace('<rect x="480" y="245" width="10" height="8" fill="#FF7F32" rx="1"/>', '')
content = content.replace('<text x="495" y="252" font-size="7" fill="#4B5563">Bonus ca</text>', '')

# Fix KPI Delta
content = content.replace("+30 pts/ca hoàn tất", "Có Đội trưởng hỗ trợ")
content = content.replace("+25 pts/ca hoàn tất", "Có Đội trưởng hỗ trợ")
content = content.replace("+20 pts/ca hoàn tất", "Có Đội trưởng hỗ trợ")

# Fix Point Economy Text
content = content.replace("Điểm = (Doanh thu thực tế ÷ 5.000) × Hệ số Layer + Điểm thưởng hoàn ca.", "Điểm = (Doanh thu thực tế ÷ 5.000) × Hệ số Layer.")
content = content.replace("tối đa 968 pts/tháng → không chạm mốc đổi quà 50k trong 1 tháng", "tối đa 968 pts/tháng → không đủ điểm đổi thưởng 50k (1.000 pts) trong tháng")

# I will also check for "đảm bảo thu nhập" or other old terms.
content = content.replace("đảm bảo thu nhập", "ưu tiên sự kiện & đặc quyền")
content = content.replace("Đảm bảo thu nhập", "Đặc quyền sinh thái")

with open("2026-07-driver-layer-ranking-present.html", "w", encoding="utf-8") as f:
    f.write(content)
