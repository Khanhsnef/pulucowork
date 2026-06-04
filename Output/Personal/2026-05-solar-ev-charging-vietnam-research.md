# Solar + EV Charging Integration — Vietnam Market Research
**Date:** 2026-05-07 | **Scope:** Technical + Financial deep-dive cho thị trường Việt Nam

---

## 1. CÁC MÔ HÌNH KỸ THUẬT: SOLAR + EV CHARGING

### 1.1 Grid-Tied (On-Grid) — Không có Battery
- **Cơ chế:** PV → Inverter → AC bus → Charger + Grid. Ban ngày dùng solar, thiếu thì lấy từ lưới, dư thì bán lại (tối đa 20% công suất theo Decree 58/2025).
- **Ưu điểm:** CAPEX thấp nhất, không có tổn thất lưu trữ, ROI tốt nhất ở khu vực có giá điện cao.
- **Nhược điểm:** Phụ thuộc lưới — nếu mất điện lưới thì trạm dừng hoàn toàn. Solar peak (11:00–15:00) không khớp với EV demand peak (17:30–22:30).
- **Phù hợp:** Trạm sạc thương mại có lưới ổn định, diện tích mái đủ lớn, muốn giảm bill điện giờ cao điểm.

### 1.2 Off-Grid — Độc lập hoàn toàn
- **Cơ chế:** PV + Battery Bank → Inverter → Charger. Không kết nối lưới.
- **Ưu điểm:** Hoàn toàn độc lập, không cần hạ tầng điện lưới, phù hợp vùng sâu/hải đảo.
- **Nhược điểm:** CAPEX cực cao ($15,000–$40,000 cho hệ 5–10 kW), phải over-size PV và Battery để đảm bảo dự phòng, LCOE cao nhất ($0.30–$0.35/kWh).
- **Phù hợp:** Trạm sạc xe máy điện tại vùng chưa có điện lưới, islands (Phú Quốc outlying areas, Cô Tô).

### 1.3 Hybrid (Grid-Tied + Battery Storage) — MÔ HÌNH TỐI ƯU
- **Cơ chế:** PV + BESS + Grid. Ba nguồn phối hợp: PV nạp battery ban ngày, battery xả cho charger giờ cao điểm (17:30–22:30), lưới làm backup.
- **Ưu điểm:** Peak shaving tiết kiệm điện giá cao điểm (5,025–5,422 VND/kWh → dùng battery), self-sufficiency cao, không phụ thuộc lưới.
- **Nhược điểm:** CAPEX cao nhất trong 3 mô hình, cần EMS (Energy Management System) phức tạp.
- **Thông số tham chiếu (Delta Thailand case study):** 50 kW PV + 293 kWh storage + 16 chargers (AC+DC) → Giảm 15.64% tổng chi phí điện.
- **Phù hợp:** Trạm sạc đô thị với lưới không ổn định hoặc phí công suất cao, muốn tối ưu TOD tariff.

---

## 2. CẤU TRÚC CHI PHÍ — VIỆT NAM 2024–2025

### 2.1 Chi Phí Tấm Pin Mặt Trời (Solar Panel + System)

| Quy mô hệ thống | Chi phí (VND/kWp) | USD/kWp (tỷ giá 25,000) | Ghi chú |
|---|---|---|---|
| Hộ gia đình (3–10 kWp) | 10,000,000–15,000,000 | $400–$600 | On-grid |
| Thương mại nhỏ (10–100 kWp) | 9,000,000–10,000,000 | $360–$400 | On-grid |
| Thương mại lớn (100–300 kWp) | 8,500,000–9,000,000 | $340–$360 | On-grid |
| Công nghiệp (>300 kWp–1 MWp) | 8,500,000 | $340 | On-grid |
| Hybrid (có lưu trữ) | 12,000,000–15,000,000 | $480–$600 | Bao gồm BESS |

**Chi tiết cấu thành hệ thống on-grid 100 kWp (ước tính):**
- Tấm pin (monocrystalline, ~450W/tấm, 222 tấm): ~$0.20–$0.25/Wp → ~$20,000–$25,000
- Inverter (Sungrow/Huawei, ~$0.05–$0.08/Wp): ~$5,000–$8,000
- Khung giá, cáp, BOS: ~$3,000–$5,000
- Nhân công lắp đặt: ~$2,000–$4,000
- **Tổng ước tính 100 kWp:** ~$30,000–$42,000 (~750–1,050 tr. VND)

### 2.2 Chi Phí Battery Storage (BESS) — 2025

| Loại | Chi phí (USD/kWh installed) | VND/kWh | Ghi chú |
|---|---|---|---|
| Cell LiFePO4 (CIF Vietnam, ex-China) | $40–$70/kWh | 1.0–1.75 tr | Cell only |
| C&I containerized system (turnkey) | $180–$300/kWh | 4.5–7.5 tr | Bao gồm PCS, BMS |
| Residential (5–20 kWh) | $250–$450/kWh | 6.25–11.25 tr | Bao gồm hybrid inverter |
| Utility scale (>1 MWh) | $100–$150/kWh | 2.5–3.75 tr | Theo BNEF 2025 |

**Hệ thống hybrid 5kW + 5kWh tại Việt Nam:** 100–130 tr. VND  
**Hệ thống hybrid 10kW + 10kWh tại Việt Nam:** 180–220 tr. VND

### 2.3 Chi Phí Charger EV (tham chiếu)

| Loại Charger | Công suất | Giá nhập (USD) |
|---|---|---|
| AC Level 2 | 7–22 kW | $500–$2,000/unit |
| DC Fast Charger | 30–60 kW | $10,000–$25,000/unit |
| DC Ultra-Fast | 120–150 kW | $30,000–$50,000/unit |

---

## 3. ROI & TÍNH TOÁN TÀI CHÍNH

### 3.1 Thông số cơ bản để tính toán

**Biểu giá điện thương mại EVN (Decision 1279/QĐ-BCT, hiệu lực 10/05/2025, chưa VAT):**

| Khung giờ | Điện áp ≥22 kV | Điện áp 6–22 kV | Điện áp <6 kV |
|---|---|---|---|
| Cao điểm (17:30–22:30 T2–T7) | 5,025 VND/kWh | 5,202 VND/kWh | 5,422 VND/kWh |
| Bình thường | 2,887 VND/kWh | 3,108 VND/kWh | 3,152 VND/kWh |
| Thấp điểm (00:00–06:00) | 1,609 VND/kWh | 1,829 VND/kWh | 1,918 VND/kWh |

**Giá bán điện dư lên lưới (Decree 58/2025 / Decree 135/2024):**
- ~671 VND/kWh (~$0.026/kWh) — cực kỳ thấp, không nên thiết kế để bán điện dư
- Ngưỡng bán tối đa: 20% sản lượng phát (hệ thống 100kW–<1,000kW)

### 3.2 Ví dụ tính LCOE — Hệ Solar 100 kWp tại HCMC (On-grid)

**Thông số đầu vào:**
- CAPEX: 850 tr. VND (~$34,000)
- Peak sun hours HCMC: 4.7 giờ/ngày (trung bình năm)
- Performance ratio: 0.80
- Sản lượng hàng năm: 100 kWp × 4.7 giờ × 365 ngày × 0.80 = **137,240 kWh/năm**
- Tuổi thọ hệ thống: 25 năm
- Tỷ lệ suy giảm công suất: 0.5%/năm
- Chi phí O&M: 0.5%/năm của CAPEX = 4.25 tr. VND/năm
- Discount rate: 8%

**LCOE = [CAPEX + NPV(O&M)] / NPV(Total Generation)**
- Tổng sản lượng 25 năm (chiết khấu 8%, suy giảm 0.5%): ~1,430,000 kWh
- LCOE ≈ 850,000,000 / 1,430,000 ≈ **594 VND/kWh (~$0.024/kWh)**

**So sánh với giá mua điện:**
- Giờ bình thường (2,887 VND/kWh): tiết kiệm **2,293 VND/kWh**
- Giờ cao điểm (5,025 VND/kWh): tiết kiệm **4,431 VND/kWh**

### 3.3 Payback Period — Ví dụ Trạm Sạc EV + Solar

**Cấu hình:** Trạm sạc đô thị HCMC — 4 DC charger 30kW + Solar 120 kWp + BESS 100 kWh

| Hạng mục | Chi phí |
|---|---|
| Solar 120 kWp (9 tr./kWp) | 1,080 tr. VND |
| BESS 100 kWh ($230/kWh → 5.75 tr./kWh) | 575 tr. VND |
| 4 × DC charger 30kW | 320 tr. VND |
| Lắp đặt, EMS, kết nối lưới | 200 tr. VND |
| **Tổng CAPEX** | **~2,175 tr. VND** |

**Doanh thu/Tiết kiệm hàng năm:**
- Solar output: 120 kWp × 4.7h × 365 × 0.80 = 164,688 kWh/năm
- Giả định 70% solar dùng giờ bình thường (2,887 VND/kWh), 30% peak shaving từ BESS giờ cao điểm (5,025 VND/kWh):
  - Tiết kiệm từ solar giờ bình thường: 115,282 kWh × (2,887 – 594) VND = **264 tr./năm**
  - Tiết kiệm peak shaving BESS: 49,406 kWh × (5,025 – 1,918) VND = **153 tr./năm**
- **Tổng tiết kiệm: ~417 tr. VND/năm**
- **Payback Period: ~5.2 năm**

**Theo nghiên cứu MDPI (Vietnam-specific):** Payback 5–8 năm, LCOE $0.07–$0.10/kWh cho rooftop PV (tính full system cost).  
**Theo nghiên cứu hybrid EVCS:** Payback 5.66–6.02 năm với LCOE $0.02/kWh (grid-connected optimal scenario).

---

## 4. BỨC XẠ MẶT TRỜI THEO VÙNG VIỆT NAM

| Vùng | GHI (kWh/m²/ngày) | GHI (kWh/m²/năm) | Peak Sun Hours | Đặc điểm mùa |
|---|---|---|---|---|
| **Hà Nội / Bắc Bộ** | 3.4–3.8 | 1,241–1,387 | 3.4–3.8 giờ | Mùa đông (Nov–Feb) GHI thấp; nhiều ngày u ám |
| **Đà Nẵng / Miền Trung** | 4.5–5.0 | 1,643–1,825 | 4.5–5.0 giờ | Mùa khô (Apr–Aug) rất tốt; mưa bão Sep–Nov |
| **Tây Nguyên / Central Highlands** | 4.8–5.2 | 1,752–1,898 | 4.8–5.2 giờ | Cao nhất cả năm; mùa khô kéo dài |
| **HCMC / Đông Nam Bộ** | 4.5–5.0 | 1,581–1,825 | 4.7 giờ (avg) | Feb đỉnh 6.3 kWh/m²/ngày; Jul thấp 3.3 kWh/m²/ngày |
| **ĐBSCL / Mekong** | 4.8–5.5 | 1,752–2,008 | 4.8–5.5 giờ | Tốt nhất toàn quốc; ít mây |

**Ý nghĩa cho sizing:**
- HCMC/ĐBSCL: 1 kWp tạo ra **1,600–1,750 kWh/năm** (PR=0.80)
- Hà Nội: 1 kWp tạo ra **1,080–1,200 kWh/năm** (PR=0.80) — kém ~35%
- ROI tại HCMC cao hơn Hà Nội khoảng **30–40%** cùng cấu hình

---

## 5. CHÍNH SÁCH NET METERING & KHUNG PHÁP LÝ

### 5.1 Tiến trình pháp lý (Timeline)

| Thời điểm | Văn bản | Nội dung chính |
|---|---|---|
| Oct 2024 | **Decree 135/2024/ND-CP** | Cho phép bán điện dư tối đa 20% công suất, giá thị trường. Không có công thức giá cụ thể. |
| Mar 2025 | **Decree 58/2025/ND-CP** | Thay thế Decree 135. Người mua điện dư là đơn vị thành viên EVN (không phải EVN trực tiếp). Giữ nguyên 20% cap. |
| Dec 2025 | **Circular 62/2025/TT-BCT** | Khung giá cho BESS quy mô lớn (≥10 MW, ≥110 kV). IRR trần 12%, hiệu suất charge-discharge 85%. |
| May 2025 | **Decision 1279/QĐ-BCT** | Cập nhật biểu giá điện bán lẻ thương mại. |
| Apr 2026 | **Decision 963/QĐ-BCT** | Tái cấu trúc TOU: bỏ peak sáng, gộp thành peak tối 17:30–22:30 T2–T7. |

### 5.2 Quy định Decree 58/2025 cho Trạm Sạc EV có Solar

| Công suất hệ thống | Yêu cầu thủ tục | Điều kiện bán điện dư |
|---|---|---|
| < 100 kW (hộ gia đình) | Thông báo DOIT + PCCC. Không cần phép. | Không giới hạn 20% |
| 100 kW – < 1,000 kW | Thông báo EVN. Cần xác nhận capacity còn trong quy hoạch tỉnh/thành. | Tối đa 20% sản lượng phát |
| ≥ 1,000 kW | Đăng ký DOIT, xin giấy phép hoạt động điện lực nếu bán điện. | Theo quy hoạch |

**Lưu ý quan trọng cho thiết kế:** Với hệ thống EV charging thương mại muốn bán điện dư, giá mua lại ~671 VND/kWh ($0.026/kWh) **cực kỳ thấp** (thấp hơn 4× so với giá mua điện giờ bình thường). Chiến lược tối ưu: **maximize self-consumption**, thiết kế solar + BESS để dùng hết nội bộ, không tối ưu hóa bán lưới.

### 5.3 Ưu đãi Thuế
- Miễn thuế nhập khẩu cho thiết bị solar/BESS không sản xuất được trong nước
- Miễn thuế thu nhập doanh nghiệp 4 năm đầu, giảm 50% trong 9 năm tiếp theo (theo Luật Đầu tư)

---

## 6. THIẾT KẾ TỐI ƯU SOLAR + EV CHARGING STATION

### 6.1 Sizing Rationale (Nguyên lý định cỡ)

**Nguyên tắc cơ bản:**
- 1 kW charger AC cần ~1.2–1.5 kWp solar để tự cấp điện trong giờ nắng
- 1 DC fast charger 30 kW cần ~36–45 kWp solar
- Thêm BESS để giải quyết mismatch solar noon vs. EV peak evening

**Sizing Công Thức:**
```
Solar PV Required (kWp) = 
  [Daily EV Energy Demand (kWh)] / [Peak Sun Hours × Performance Ratio]

Battery Capacity (kWh) = 
  [Peak Charger Power (kW)] × [Peak Duration (h)] / [DoD (0.8)]
```

**Ví dụ: Trạm sạc 6 × AC 22kW (suburban, HCMC)**
- Daily demand: 6 chargers × 22kW × 4 sessions × 1h = 528 kWh/ngày
- Solar needed: 528 / (4.7 × 0.80) = **140 kWp**
- BESS cho peak shaving (17:30–22:30 = 5h): 6 × 22kW × 5h × 0.7 utilization / 0.8 DoD = **578 kWh**
- Thực tế: tối ưu BESS ở 200–300 kWh (cân bằng CAPEX vs. savings)

### 6.2 Cấu hình tham chiếu theo quy mô

| Quy mô trạm | Charger | Solar | BESS | CAPEX ước tính |
|---|---|---|---|---|
| Mini (xe máy/e-scooter) | 10 × 3.3kW AC | 15 kWp | 30 kWh | ~350 tr. VND |
| Nhỏ (suburban) | 4 × 22kW AC | 50 kWp | 100 kWh | ~1,200 tr. VND |
| Vừa (urban hub) | 4 × 30kW DC | 120 kWp | 200 kWh | ~2,500 tr. VND |
| Lớn (highway/commercial) | 4 × 60kW DC + 4 × 22kW AC | 300 kWp | 400 kWh | ~6,000 tr. VND |

### 6.3 Hướng tối ưu thiết kế
- **Solar canopy** thay vì mái nhà → tạo bóng mát cho xe, marketing value cao
- **East-West orientation** (thay vì Nam) → trải đều sản lượng 08:00–17:00, giảm peak solar congestion
- **Tích hợp V2G** (Vehicle-to-Grid) trong tương lai khi EVN cho phép — pin EV có thể xả lại lưới giờ cao điểm

---

## 7. CASE STUDIES

### 7.1 Delta Europe HQ Solar EV Charging (Tham chiếu áp dụng cho Việt Nam)
- **Cấu hình:** 50 kW rooftop PV + 293 kWh BESS + 16 chargers (AC+DC)
- **Kết quả:** Giảm 15.64% tổng chi phí điện, zero power overload
- **Công cụ:** DeltaGrid® EVM — quản lý PV + BESS + charger trên 1 platform

### 7.2 V-Green Vietnam (Hệ thống đang triển khai 2025–2026)
- **Quy mô:** 99 fast-charging stations, đầu tư 10 nghìn tỷ VND (~$404 triệu)
- **Công nghệ:** Wind + solar + BESS (VinFast-manufactured)
- **Model:** Franchise model, landowner tham gia đầu tư trạm sạc

### 7.3 Solar PV Carport — Taiwan (Kaohsiung, subtropical = gần Việt Nam)
- **Cấu hình:** 286 tấm pin × 50 kW, 525.6 m², góc nghiêng 20°
- **Sản lượng:** 140 MWh/năm → phục vụ >3,000 xe/tháng (mỗi xe sạc 1 giờ)
- **Phát thải:** Thấp hơn 94% so với điện lưới thông thường

### 7.4 HOMER Analysis — Grid-Connected Hybrid EVCS (SEA region)
- **Cấu hình tối ưu:** 136 kW PV + Biomass backup + Grid (không BESS)
- **LCOE:** $0.0215/kWh (cực kỳ cạnh tranh)
- **CAPEX:** $1.13 triệu
- **Payback:** 5.98 năm
- **Renewable fraction:** 81.3%

---

## 8. KINH TẾ BATTERY STORAGE — PEAK SHAVING

### 8.1 Business Case cho BESS tại Trạm Sạc

**Cơ hội tiết kiệm từ TOD tariff (Điện áp <6kV):**
- Sạc BESS giờ thấp điểm: 1,918 VND/kWh
- Xả BESS giờ cao điểm: tránh mua 5,422 VND/kWh
- **Delta spread: 3,504 VND/kWh (~$0.14/kWh)**

**Ví dụ 100 kWh BESS, 1 chu kỳ/ngày:**
- Tiết kiệm/ngày: 100 kWh × 0.85 (hiệu suất) × 3,504 VND = **297,840 VND/ngày**
- Tiết kiệm/năm: **~108 tr. VND/năm**
- Chi phí BESS 100 kWh ($230/kWh → ~575 tr. VND)
- **Payback chỉ từ BESS:** ~5.3 năm (không tính solar savings)

### 8.2 Sizing BESS cho EV Charging Station

| Cấu hình Charger | BESS tối thiểu | BESS khuyến nghị | Use Case |
|---|---|---|---|
| 4 × 22 kW AC | 50 kWh | 100 kWh | Bãi đỗ xe nhỏ |
| 2 × 150 kW DC | 300 kWh | 400 kWh | Urban fast-charge hub |
| 4 × 30 kW DC | 100 kWh | 200 kWh | Suburban station |

**Lưu ý:** Oversizing BESS làm tăng chi phí 30%; undersizing không đủ peak shaving.

---

## 9. SOLAR vs. EV LOAD PROFILE — MISMATCH ANALYSIS

### 9.1 Đặc điểm Load Profile EV tại Việt Nam

**Xe máy điện (e-2W — chiếm đa số):**
- Pin: 1.2–3.0 kWh (thường dùng)
- Thời gian sạc tại nhà: 4–8 giờ (qua đêm, 22:00–06:00)
- Thời gian sạc nhanh (swap): 2–3 phút/pin
- Peak demand từ sạc: không tập trung nếu sạc ở nhà

**Xe ô tô điện:**
- Pin: 30–80 kWh (VinFast VF8 là 75.8 kWh)
- Sạc DC fast (30–60 kW): 60–150 phút
- Hành vi: sau giờ làm (17:00–21:00) và ban đêm

### 9.2 Mismatch Map

```
SOLAR GENERATION PROFILE (HCMC, ví dụ ngày điển hình):
 0         6          12          18         24
 |---------|##########||##########|----------|
           07:00     12:00     17:30
           Solar     Peak      Sunset
           rises     (5.0 kWh  (EV peak
                     /m²)      starts)

EV DEMAND PROFILE (Urban Charging Station):
 0         6          12          18         24
 |-------|__|__________|##########|###|------|
         07:30       16:00     18:00  22:30
         Morning     Lunch      Evening
         commute     top-up     Peak
         charge
```

**Kết luận mismatch:**
- **Solar peak:** 09:00–15:00 (overlap thấp với EV demand)
- **EV demand peak:** 17:30–22:30 (sau khi solar đã tắt)
- **Overlap zone:** 09:00–12:00 (commuters quay lại, một số sạc buổi trưa) — **chỉ ~20–30% overlap**
- **Gap cần BESS lấp đầy:** ~5 giờ cao điểm tối (17:30–22:30)

### 9.3 Tác động đến thiết kế
- **Không có BESS:** Solar chỉ tự cấp ~20–30% nhu cầu EV charging (phần overlap)
- **Có BESS 4h:** Solar tích lũy ban ngày → xả cao điểm tối → tự cấp 60–75% nhu cầu EV
- **BESS sizing rule of thumb:** BESS capacity (kWh) ≈ Solar PV (kWp) × Peak sun hours × 0.6

---

## 10. TÓM TẮT SO SÁNH MÔ HÌNH

| Tiêu chí | Grid-Tied | Hybrid (PV+BESS) | Off-Grid |
|---|---|---|---|
| CAPEX (100kWp ref.) | ~850 tr. VND | ~1,425 tr. VND | ~2,000+ tr. VND |
| LCOE | ~$0.024/kWh | ~$0.035–0.05/kWh | ~$0.25–$0.35/kWh |
| Payback | 3–5 năm | 5–7 năm | 10–15 năm |
| Solar self-consumption | 20–40% | 60–80% | 100% |
| Phụ thuộc lưới | Cao | Thấp | Không |
| Phù hợp VN | Đô thị, lưới ổn | Đô thị, TOD cao | Vùng xa/hải đảo |

**Khuyến nghị cho EV Charging tại đô thị VN:** Hybrid (PV + BESS + Grid), ưu tiên hóa self-consumption, tận dụng peak shaving spread VND 3,500/kWh giờ cao điểm vs. thấp điểm.

---

## Nguồn Tham Khảo

- [Decree 135/2024 — Dentons LuatViet](https://www.dentonsluatviet.com/en/insights/alerts/2024/october/29/vietnam-new-decree-no-135-2024-on-onsite-self-consumption-rooftop-solar-power-development)
- [Decree 58/2025 — Duane Morris](https://blogs.duanemorris.com/vietnam/2025/08/27/vietnam-decree-58-on-development-of-renewable-energy-power-mechanisms-and-policies-for-self-production-and-self-consumption-rooftop-solar-power-systems/)
- [Vietnam TOU Tariff — Arcus Energy](https://arcusenergyasia.com/resources/tariffs/business)
- [Solar Installation Costs Vietnam 2025 — Dat Solar](https://datsolar.com/en/solar-panel-installer/)
- [Solar Installation Costs Vietnam 2025 — Quanganh](https://quanganhcons.com/solar-panel-installation-costs-vietnam-2025/)
- [BESS Pricing Circular 62/2025 — Vietnam Briefing](https://www.vietnam-briefing.com/news/examining-vietnams-first-bess-pricing-framework-circular-62.html)
- [BESS Costs 2025 — GSL Energy](https://www.gsl-energy.com/the-real-cost-of-commercial-battery-energy-storage-in-2025-what-you-need-to-know.html)
- [Solar Irradiance Vietnam — Energypedia](https://energypedia.info/wiki/Solar_Energy_Country_Analysis_Vietnam)
- [V-Green EV Charging — Electrive](https://www.electrive.com/2026/03/20/v-green-to-build-99-fast-charging-stations-in-vietnam/)
- [Net Metering Tariff $0.026/kWh — PV Magazine](https://pv-magazine.com/2024/07/16/vietnam-sets-0-026-kwh-tariff-for-net-metered-solar-power/)
- [Solar EV Charging EVCS Hybrid — PMC/Scientific Reports](https://pmc.ncbi.nlm.nih.gov/articles/PMC11794887/)
- [Technical Economic Analysis PV-EVCS Vietnam — MDPI](https://www.mdpi.com/2071-1050/13/6/3528)
- [Solar Carport Canopy EV Charging — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9902566/)
- [Delta Thailand Smart EV Charging](https://www.deltathailand.com/en/blog-detail/5/90/Smart-EV-Charging-Infrastructure-Solution-in-Thailand)
- [Battery Sizing for EV Stations — ACE Battery](https://www.acebattery.com/blogs/how-to-size-a-battery-storage-system-for-your-ev-charging-station)
- [Solar EV Charging Cost Breakdown — Max Power](https://www.mxpcharger.com/solar-ev-charging-station-cost-breakdown/)
- [UNDP Net Zero Transport Vietnam](https://www.undp.org/sites/g/files/zskgke326/files/2024-12/main_report_to_drvn_en_29.11.2024.pdf)
