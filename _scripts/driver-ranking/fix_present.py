import re

with open("2026-07-driver-layer-ranking-present.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace text labels
content = content.replace("1.848", "9.240")
content = content.replace("1.496", "7.436")
content = content.replace("1.166", "5.808")
content = content.replace("968", "4.840")

# Update heights for max 12500 pts instead of 2500 pts.
# Scale = 200px / 12500 = 0.016
# R1: 9240 * 0.016 = 147.84
# R2: 7436 * 0.016 = 118.97
# R3: 5808 * 0.016 = 92.92
# L6: 4840 * 0.016 = 77.44
# 50k Threshold: 5000 * 0.016 = 80 -> y = 220 - 80 = 140

content = re.sub(r'<rect x="18" y="\d+(\.\d+)?" width="44" height="\d+(\.\d+)?" fill="var\(--brand-orange\)" rx="4"/>',
                 '<rect x="18" y="72.16" width="44" height="147.84" fill="var(--brand-orange)" rx="4"/>', content)
content = re.sub(r'<rect x="106" y="\d+(\.\d+)?" width="44" height="\d+(\.\d+)?" fill="var\(--brand-yellow\)" rx="4"/>',
                 '<rect x="106" y="101.03" width="44" height="118.97" fill="var(--brand-yellow)" rx="4"/>', content)
content = re.sub(r'<rect x="194" y="\d+(\.\d+)?" width="44" height="\d+(\.\d+)?" fill="var\(--brand-blue\)" rx="4"/>',
                 '<rect x="194" y="127.08" width="44" height="92.92" fill="var(--brand-blue)" rx="4"/>', content)
content = re.sub(r'<rect x="282" y="\d+(\.\d+)?" width="44" height="\d+(\.\d+)?" fill="#9CA3AF" rx="4"/>',
                 '<rect x="282" y="142.56" width="44" height="77.44" fill="#9CA3AF" rx="4"/>', content)

# Threshold line
content = re.sub(r'<line x1="0" y1="140" x2="360" y2="140"', '<line x1="0" y1="140" x2="360" y2="140"', content)
# Label for threshold
content = content.replace("1.000 pts", "5.000 pts")

# Y axis labels
content = content.replace(">2.500<", ">12.500<")
content = content.replace(">1.250<", ">6.250<")

# Section 5 prices
content = content.replace("600 pts", "3.000 pts")
content = content.replace("400 pts", "2.000 pts")
content = content.replace("1.000 pts", "5.000 pts")
content = content.replace("3.000 pts", "15.000 pts")
content = content.replace("800 pts", "4.000 pts")
content = content.replace("2.000 pts", "10.000 pts")

# Gói BHTN
content = content.replace("Gói 10k (1.000 pts) / 30k (3.000 pts)", "Gói 10k (1.000 pts) / 30k (3.000 pts)")

with open("2026-07-driver-layer-ranking-present.html", "w", encoding="utf-8") as f:
    f.write(content)

