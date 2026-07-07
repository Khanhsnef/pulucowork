import re

with open("2026-05-driver-ranking-layer-benefits.html", "r", encoding="utf-8") as f:
    content = f.read()

# Update base pts calculation
content = content.replace("Base : 280k ÷ 5.000 = 56 base pts", "Base : 280k ÷ 1.000 = 280 base pts")
# Since 56 is replaced with 280, we should ensure the next line matches
content = content.replace("Earned: 56 × 1.5 = 84 pts", "Earned: 280 × 1.5 = 420 pts")
content = content.replace("56 base × 1.5 = 84", "280 base × 1.5 = 420")
content = content.replace('<div class="earn-pts">84</div>', '<div class="earn-pts">420</div>')
content = content.replace('<div class="earn-pts">420</div>', '<div class="earn-pts">420</div>') # Ensure idempotency
content = content.replace('<div class="earn-detail">280 base × 1.5 = 420</div>', '<div class="earn-detail">280 base × 1.5 = 420</div>')

# Fix R1 Total expected
content = content.replace("84 × 22 ca = 1.848 pts", "420 × 22 ca = 9.240 pts")
content = content.replace("1.848 pts/tháng", "9.240 pts/tháng")
content = content.replace("5.000 pts (tương đương 50.000đ)", "5.000 pts (tương đương 50.000đ)") # Old logic was 1.000 pts for 50k
content = content.replace("1.000 pts (tương đương 50.000đ)", "5.000 pts (tương đương 50.000đ)")
content = content.replace("dư 848 pts", "dư 4.240 pts")

# Fix catalog in layer benefits
# Since it's unstructured html, I will just do simple text replacements for the point values.
# Wait, this might be fragile. Let's do a targeted replace for this file.
replacements = {
    '<div class="item-pts">600 pts</div>': '<div class="item-pts">3.000 pts</div>',
    '<div class="item-pts">1.000 pts</div>': '<div class="item-pts">5.000 pts</div>',
    '<div class="item-pts">2.400 pts</div>': '<div class="item-pts">12.000 pts</div>',
    '<div class="item-pts">3.000 pts</div>': '<div class="item-pts">15.000 pts</div>',
    '<div class="item-pts">800 pts</div>': '<div class="item-pts">4.000 pts</div>',
    '<div class="item-pts">1.600 pts</div>': '<div class="item-pts">8.000 pts</div>',
    '<div class="item-pts">5.000 pts</div>': '<div class="item-pts">25.000 pts</div>',
    '<div class="item-pts">6.000 pts</div>': '<div class="item-pts">30.000 pts</div>',
    '<div class="item-pts">2.000 pts</div>': '<div class="item-pts">10.000 pts</div>',
    '<div class="item-pts">3.400 pts</div>': '<div class="item-pts">17.000 pts</div>',
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open("2026-05-driver-ranking-layer-benefits.html", "w", encoding="utf-8") as f:
    f.write(content)

