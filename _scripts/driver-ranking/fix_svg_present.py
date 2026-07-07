import re

with open("2026-07-driver-layer-ranking-present.html", "r", encoding="utf-8") as f:
    content = f.read()

# Threshold Red Line
content = content.replace('<!-- y = 220 - (1500/2500)*200 = 100 -->', '<!-- y = 220 - (1000/2500)*200 = 140 -->')
content = content.replace('<line x1="50" y1="100" x2="520" y2="100" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,4"/>', '<line x1="50" y1="140" x2="520" y2="140" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="4,4"/>')
content = content.replace('<text x="515" y="95"', '<text x="515" y="135"')

# R1 Stack
content = content.replace('<rect x="90" y="19.4" width="40" height="52.8" fill="#FF7F32" rx="2"/>', '')
content = content.replace('<text x="110" y="15" font-size="8" font-weight="700" fill="#111827" text-anchor="middle">1.848</text>', '<text x="110" y="67" font-size="8" font-weight="700" fill="#111827" text-anchor="middle">1.848</text>')

# R2 Stack
content = content.replace('<!-- R2 (L3): Total 2046 [base 1144 (y: 91.5), multiplier 352 (y: 28.2), bonus 550 (y: 44)] -->', '<!-- R2 (L3): Total 1496 [base 1144 (y: 91.5), multiplier 352 (y: 28.2)] -->')
content = content.replace('<rect x="195" y="100.3" width="40" height="28.2" fill="#0E4174" rx="2"/>', '<rect x="195" y="100.3" width="40" height="28.2" fill="#0E4174" rx="2"/>') # Unchanged visually since 27.5 is close enough to 28.2
content = content.replace('<rect x="195" y="56.3" width="40" height="44" fill="#FF7F32" rx="2"/>', '')
content = content.replace('<text x="215" y="51" font-size="8" font-weight="700" fill="#111827" text-anchor="middle">1.496</text>', '<text x="215" y="96" font-size="8" font-weight="700" fill="#111827" text-anchor="middle">1.496</text>')

# R3 Stack
content = content.replace('<!-- R3 (L4): Total 1606 [base 1056 (y: 84.5), multiplier 110 (y: 8.8), bonus 440 (y: 35.2)] -->', '<!-- R3 (L4): Total 1166 [base 1056 (y: 84.5), multiplier 110 (y: 8.8)] -->')
content = content.replace('<rect x="300" y="91.5" width="40" height="35.2" fill="#FF7F32" rx="2"/>', '')
content = content.replace('<text x="320" y="86" font-size="8" font-weight="700" fill="#111827" text-anchor="middle">1.166</text>', '<text x="320" y="122" font-size="8" font-weight="700" fill="#111827" text-anchor="middle">1.166</text>')

# Add column for Hỗ trợ in 6.1 (if there is a table there)
# Wait, this is a presentation HTML, so there might not be a huge table, just the summary we see.
# I will check if there are other places.

with open("2026-07-driver-layer-ranking-present.html", "w", encoding="utf-8") as f:
    f.write(content)
