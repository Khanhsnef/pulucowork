import re

with open("2026-05-driver-ranking-params.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix Section 7: Ước tính pts/ca
old_table = """| Rank | EPH giả định | Base pts | × Hệ số | Tổng/ca |
| --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 56 | 56 × 1.5 = 84 | **84** |
| R2 · L3 | ~65k/h → 260k/ca | 52 | 52 × 1.3 = 68 | **68** |
| R3 · L4 | ~60k/h → 240k/ca | 48 | 48 × 1.1 = 53 | **53** |
| L6 MASS | ~55k/h → 220k/ca | 44 | 44 × 1.0 = 44 | **44** |
| Overflow (any) | — | base | ×1.0 | base only |"""

new_table = """| Rank | EPH giả định | Base pts | × Hệ số | Tổng/ca |
| --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 280 | 280 × 1.5 = 420 | **420** |
| R2 · L3 | ~65k/h → 260k/ca | 260 | 260 × 1.3 = 338 | **338** |
| R3 · L4 | ~60k/h → 240k/ca | 240 | 240 × 1.1 = 264 | **264** |
| L6 MASS | ~55k/h → 220k/ca | 220 | 220 × 1.0 = 220 | **220** |
| Overflow (any) | — | base | ×1.0 | base only |"""
content = content.replace(old_table, new_table)

# Fix Calibration Formula
old_calib = """Pts tích/tháng (avg, 22 ca):
  R1: 84 × 22 = 1.848 pts  (15% fleet)
  R2: 68 × 22 = 1.496 pts  (35% fleet)
  R3: 53 × 22 = 1.166 pts  (35% fleet)
  L6: 44 × 22 = 968 pts  (15% fleet)
  Weighted avg ≈ 1.340 pts/tháng

80% burn → paid reward:  1.340 × 80% = ~1.072 pts ≈ 50.000 VND
  → Paid reward 50k = 1.000 pts (cân chỉnh lại giá trị điểm)

20% còn lại → free partner:  ~268 pts/tháng
  → Free items giá 40–170 pts → đổi được 1–4 món/tháng"""

new_calib = """Pts tích/tháng (avg, 22 ca):
  R1: 420 × 22 = 9.240 pts  (15% fleet)
  R2: 338 × 22 = 7.436 pts  (35% fleet)
  R3: 264 × 22 = 5.808 pts  (35% fleet)
  L6: 220 × 22 = 4.840 pts  (15% fleet)
  Weighted avg ≈ 6.747 pts/tháng

80% burn → paid reward:  6.747 × 80% = ~5.398 pts ≈ 50.000 VND
  → Paid reward 50k = 5.000 pts (cân chỉnh lại giá trị điểm: 1 điểm = 10đ)

20% còn lại → free partner:  ~1.349 pts/tháng
  → Free items giá 200–850 pts → đổi được 1–4 món/tháng"""
content = content.replace(old_calib, new_calib)

old_calib_table = """| Rank | Pts/tháng | 80% → Paid 50k (1.000p) | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 1.848 | ✅ 1.000 pts (dư ~848) | ~800 pts free |
| R2 | 1.496 | ✅ 1.000 pts (dư ~496) | ~400 pts free |
| R3 | 1.166 | ✅ 1.000 pts (dư ~166) | ~100 pts free |
| L6 | 968 | ❌ cần ~1.1 tháng | — động lực lên R3 |"""

new_calib_table = """| Rank | Pts/tháng | 80% → Paid 50k (5.000p) | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 9.240 | ✅ 5.000 pts (dư ~4.240) | ~4.000 pts free |
| R2 | 7.436 | ✅ 5.000 pts (dư ~2.436) | ~2.000 pts free |
| R3 | 5.808 | ✅ 5.000 pts (dư ~808) | ~800 pts free |
| L6 | 4.840 | ❌ cần ~1.1 tháng | — động lực lên R3 |"""
content = content.replace(old_calib_table, new_calib_table)

# Section 8 Catalog
content = content.replace("Công thức giá điểm: Điểm = Giá trị thực (VND) ÷ 50", "Công thức giá điểm: Điểm = Giá trị thực (VND) ÷ 10")

# Prices
content = content.replace("600 pts (Giá trị: 30.000đ)", "3.000 pts (Giá trị: 30.000đ)")
content = content.replace("1.000 pts (Giá trị: ~50.000đ)", "5.000 pts (Giá trị: ~50.000đ)")
content = content.replace("400 pts (Giá trị: 20.000đ)", "2.000 pts (Giá trị: 20.000đ)")
content = content.replace("1.000 pts (Giá trị: 50.000đ)", "5.000 pts (Giá trị: 50.000đ)")
content = content.replace("3.000 pts (Giá trị: ~150.000đ)", "15.000 pts (Giá trị: ~150.000đ)")
content = content.replace("800 pts", "4.000 pts")
content = content.replace("5.000 pts (Giá trị: ~250.000đ)", "25.000 pts (Giá trị: ~250.000đ)")
content = content.replace("2.000 pts (Giá trị: 100.000đ)", "10.000 pts (Giá trị: 100.000đ)")
content = content.replace("3.400 pts", "17.000 pts")

content = content.replace("1.000 pts (Chi phí Aha: ~50.000đ)", "5.000 pts (Chi phí Aha: ~50.000đ)")
content = content.replace("2.400 pts (Chi phí Aha: ~120.000đ)", "12.000 pts (Chi phí Aha: ~120.000đ)")
content = content.replace("1.600 pts (Chi phí Aha: ~80.000đ)", "8.000 pts (Chi phí Aha: ~80.000đ)")
content = content.replace("5.000 pts (Chi phí Aha: ~250.000đ)", "25.000 pts (Chi phí Aha: ~250.000đ)")
content = content.replace("6.000 pts (Chi phí Aha: ~300.000đ)", "30.000 pts (Chi phí Aha: ~300.000đ)")
content = content.replace("3.000 pts (Chi phí Aha: ~150.000đ)", "15.000 pts (Chi phí Aha: ~150.000đ)")

content = content.replace("200 pts/tháng", "1.000 pts/tháng")
content = content.replace("600 pts/tháng", "3.000 pts/tháng")
content = content.replace("285–600 pts/tháng", "1.000–3.000 pts/tháng")
content = content.replace("10k/tháng = 200 pts · 30k/tháng = 600 pts", "10k/tháng = 1.000 pts · 30k/tháng = 3.000 pts")

# Fix 9.2 Layer table
old_92 = """| **Hỗ trợ** | Đội trưởng | Đội trưởng | Đội trưởng | Đội trưởng | Không |"""
new_92 = """| **Hỗ trợ** | Đội trưởng | Đội trưởng | Không | Không | Không |"""
content = content.replace(old_92, new_92)

# Fix 9.1 Rank table
old_91_target = """| **Ca Full-day** | ✅ 08:00–18:00 | ✅ 08:00–18:00 | ❌ | ❌ |"""
new_91_target = """| **Ca Full-day** | ✅ 08:00–18:00 | ✅ 08:00–18:00 | ❌ | ❌ |
| **Slot đăng ký** | Tất cả L2-L6 | Tất cả L2-L6 | Tất cả L2-L6 | L5-6 MASS |"""
content = content.replace(old_91_target, new_91_target)

with open("2026-05-driver-ranking-params.md", "w", encoding="utf-8") as f:
    f.write(content)

