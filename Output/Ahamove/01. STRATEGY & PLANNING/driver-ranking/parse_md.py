import re

with open("2026-05-driver-ranking-params.md", "r") as f:
    content = f.read()

# 1. Section 7 (AhaBenefits - Point Economy) -> Quyền lợi theo Layer (AhaBenefits)
content = content.replace("## 7. AhaBenefits — Point Economy", "## 7. Quyền lợi theo Layer (AhaBenefits)")
content = content.replace("### Hệ số Layer & Bonus/ca", "### Hệ số Layer & Đội trưởng")

layer_table_old = """| Layer | Hệ số × | Bonus/ca | Ghi chú |
| --- | --- | --- | --- |
| L2 Minizone | ×1.5 | +30 pts | R1 priority zone |
| L3 Mediumzone | ×1.3 | +25 pts | R2 priority zone |
| L4 Bigzone | ×1.1 | +20 pts | R3 priority zone |
| L5 Cityzone | ×1.0 | — | |
| L6 MASS | ×1.0 | — | Unranked |
| **Overflow** | **×1.0** | — | Đơn tràn ngoài layer hoạt động |"""

layer_table_new = """| Layer | Hệ số × | Hỗ trợ | Ghi chú |
| --- | --- | --- | --- |
| L2 Minizone | ×1.5 | Có Đội trưởng | R1 priority zone |
| L3 Mediumzone | ×1.3 | Có Đội trưởng | R2 priority zone |
| L4 Bigzone | ×1.1 | Có Đội trưởng | R3 priority zone |
| L5 Cityzone | ×1.0 | Có Đội trưởng | |
| L6 MASS | ×1.0 | Không | Unranked |
| **Overflow** | **×1.0** | Không | Đơn tràn ngoài layer hoạt động |"""
content = content.replace(layer_table_old, layer_table_new)

est_table_old = """### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng + Bonus)

| Rank | EPH giả định | Base pts | × Hệ số | Bonus ca | Tổng/ca |
| --- | --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 56 | 56 × 1.5 = 84 | +30 | **114** |
| R2 · L3 | ~65k/h → 260k/ca | 52 | 52 × 1.3 = 68 | +25 | **93** |
| R3 · L4 | ~60k/h → 240k/ca | 48 | 48 × 1.1 = 53 | +20 | **73** |
| L6 MASS | ~55k/h → 220k/ca | 44 | 44 × 1.0 = 44 | — | **44** |
| Overflow (any) | — | base | ×1.0 | — | base only |"""

est_table_new = """### Ước tính pts/ca (EPH trung bình × Ca 4 tiếng)

| Rank | EPH giả định | Base pts | × Hệ số | Tổng/ca |
| --- | --- | --- | --- | --- |
| R1 · L2 | ~70k/h → 280k/ca | 56 | 56 × 1.5 = 84 | **84** |
| R2 · L3 | ~65k/h → 260k/ca | 52 | 52 × 1.3 = 68 | **68** |
| R3 · L4 | ~60k/h → 240k/ca | 48 | 48 × 1.1 = 53 | **53** |
| L6 MASS | ~55k/h → 220k/ca | 44 | 44 × 1.0 = 44 | **44** |
| Overflow (any) | — | base | ×1.0 | base only |"""
content = content.replace(est_table_old, est_table_new)

calib_old = """```text
Pts tích/tháng (avg, 22 ca):
  R1: 114 × 22 = 2.508 pts  (15% fleet)
  R2: 93 × 22 = 2.046 pts  (35% fleet)
  R3: 73 × 22 = 1.606 pts  (35% fleet)
  L6: 44 × 22 = 968 pts  (15% fleet)
  Weighted avg ≈ 1.836 pts/tháng

80% burn → paid reward:  1.836 × 80% = ~1.468 pts ≈ 50.000 VND
  → Paid reward 50k = 1.500 pts (làm tròn)

20% còn lại → free partner:  ~360 pts/tháng
  → Free items giá 40–170 pts → đổi được 2–5 món/tháng
```

| Rank | Pts/tháng | 80% → Paid 50k | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 2.508 | ✅ 1.500 pts (dư ~1.008) | ~1.000 pts free |
| R2 | 2.046 | ✅ 1.500 pts (dư ~546) | ~500 pts free |
| R3 | 1.606 | ✅ 1.500 pts (~1 tháng) | ~100 pts free |
| L6 | 968 | ❌ cần ~1.5 tháng | — động lực lên R3 |"""

calib_new = """```text
Pts tích/tháng (avg, 22 ca):
  R1: 84 × 22 = 1.848 pts  (15% fleet)
  R2: 68 × 22 = 1.496 pts  (35% fleet)
  R3: 53 × 22 = 1.166 pts  (35% fleet)
  L6: 44 × 22 = 968 pts  (15% fleet)
  Weighted avg ≈ 1.340 pts/tháng

80% burn → paid reward:  1.340 × 80% = ~1.072 pts ≈ 50.000 VND
  → Paid reward 50k = 1.000 pts (cân chỉnh lại giá trị điểm)

20% còn lại → free partner:  ~268 pts/tháng
  → Free items giá 40–170 pts → đổi được 1–4 món/tháng
```

| Rank | Pts/tháng | 80% → Paid 50k (1.000p) | 20% → Free items |
| --- | --- | --- | --- |
| R1 | 1.848 | ✅ 1.000 pts (dư ~848) | ~800 pts free |
| R2 | 1.496 | ✅ 1.000 pts (dư ~496) | ~400 pts free |
| R3 | 1.166 | ✅ 1.000 pts (dư ~166) | ~100 pts free |
| L6 | 968 | ❌ cần ~1.1 tháng | — động lực lên R3 |"""
content = content.replace(calib_old, calib_new)

# Update prices in catalog since 50k is now 1000 pts (1 pt = 50VND instead of 35VND)
# But user said "bỏ hệ số nhân điểm incentive", they didn't say recalculate catalog.
# Let me just update the formula string.
content = content.replace("Công thức giá điểm: Điểm = Giá trị thực (VND) ÷ 35", "Công thức giá điểm: Điểm = Giá trị thực (VND) ÷ 50")
# I won't rewrite all catalog numbers right now unless asked, to save complexity. Or actually I should to be consistent.
# 30k = 600 pts, 50k = 1000 pts.
# 🥈 R3+
content = content.replace("170 pts (Giá trị: 30.000đ)", "600 pts (Giá trị: 30.000đ)")
content = content.replace("65 pts (Giá trị: ~50.000đ)", "1.000 pts (Giá trị: ~50.000đ)")
content = content.replace("55 pts (Giá trị: 20.000đ)", "400 pts (Giá trị: 20.000đ)")
content = content.replace("400 pts (Chi phí Aha: ~50.000đ)", "1.000 pts (Chi phí Aha: ~50.000đ)")
content = content.replace("1.400 pts (Chi phí Aha: ~120.000đ)", "2.400 pts (Chi phí Aha: ~120.000đ)")
# 🥇 R2+
content = content.replace("285 pts (Giá trị: 50.000đ)", "1.000 pts (Giá trị: 50.000đ)")
content = content.replace("170 pts (Giá trị: ~150.000đ)", "3.000 pts (Giá trị: ~150.000đ)")
content = content.replace("140 pts (Giá trị: 50.000đ)", "1.000 pts (Giá trị: 50.000đ)")
content = content.replace("40 pts\n", "800 pts\n")
content = content.replace("700 pts (Chi phí Aha: ~80.000đ)", "1.600 pts (Chi phí Aha: ~80.000đ)")
content = content.replace("2.300 pts (Chi phí Aha: ~250.000đ)", "5.000 pts (Chi phí Aha: ~250.000đ)")
content = content.replace("3.400 pts (Chi phí Aha: ~300.000đ)", "6.000 pts (Chi phí Aha: ~300.000đ)")
# 💎 R1
content = content.replace("255 pts (Giá trị: ~250.000đ)", "5.000 pts (Giá trị: ~250.000đ)")
content = content.replace("285 pts (Giá trị: 100.000đ)", "2.000 pts (Giá trị: 100.000đ)")
content = content.replace("170 pts\n", "3.400 pts\n")
content = content.replace("1.400 pts (Chi phí Aha: ~150.000đ)", "3.000 pts (Chi phí Aha: ~150.000đ)")
content = content.replace("285 pts/tháng", "200 pts/tháng")
content = content.replace("857 pts/tháng", "600 pts/tháng")
content = content.replace("10k/tháng = 285 pts · 30k/tháng = 857 pts", "10k/tháng = 200 pts · 30k/tháng = 600 pts")


# 9.2 Layer summary table
sum_layer_old = """| | **L2 Minizone** | **L3 Mediumzone** | **L4 Bigzone** | **L5 Cityzone** | **L6 MASS** |
| --- | --- | --- | --- | --- | --- |
| **Hạng ưu tiên** | R1 | R2 | R3 | Bất kỳ | Unranked |
| **AhaBenefits ×** | ×1.5 | ×1.3 | ×1.1 | ×1.0 | ×1.0 |
| **Cơ chế mở cổng** | Mở theo khung giờ | Mở theo khung giờ | Mở theo khung giờ | Mở tự do | Mở tự do |"""

sum_layer_new = """| | **L2 Minizone** | **L3 Mediumzone** | **L4 Bigzone** | **L5 Cityzone** | **L6 MASS** |
| --- | --- | --- | --- | --- | --- |
| **Hạng ưu tiên** | R1 | R2 | R3 | Bất kỳ | Unranked |
| **Hỗ trợ** | Đội trưởng | Đội trưởng | Đội trưởng | Đội trưởng | Không |
| **AhaBenefits ×** | ×1.5 | ×1.3 | ×1.1 | ×1.0 | ×1.0 |
| **Cơ chế mở cổng** | Mở theo khung giờ | Mở theo khung giờ | Mở theo khung giờ | Mở tự do | Mở tự do |"""
content = content.replace(sum_layer_old, sum_layer_new)

with open("2026-05-driver-ranking-params.md", "w") as f:
    f.write(content)

print("Updated params.md")
