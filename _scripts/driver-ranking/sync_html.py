import re
import glob

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Section 2: Fleet Target Ratio
    content = content.replace("15%", "10-15%", 1) # Only first few? No, replace specific
    content = content.replace("<td>15%</td>\n              <td>~1.575</td>", "<td>10-15%</td>\n              <td>~1.000 - 1.500</td>")
    content = content.replace("<td>35%</td>\n              <td>~3.675</td>", "<td>10-15%</td>\n              <td>~1.000 - 1.500</td>", 1) # R2
    content = content.replace("<td>35%</td>\n              <td>~3.675</td>", "<td>30-40%</td>\n              <td>~4.000 - 6.000</td>") # R3
    content = content.replace("<td>15%</td>\n              <td>~1.575</td>", "<td>30-40%</td>\n              <td>~4.000 - 6.000</td>") # Unranked

    # Section 3: Layer Access
    content = content.replace("L6 MASS (slot trống còn lại)", "L5-6 MASS (slot trống còn lại)")

    # Formulas & multipliers
    content = content.replace("trip_GSV ÷ 5,000", "trip_GSV ÷ 1,000")
    content = content.replace("trip_GSV ÷ 5.000", "trip_GSV ÷ 1.000")
    content = content.replace("5.000đ thu nhập = 1 điểm base", "1.000đ thu nhập = 1 điểm base")
    
    # Layer Support (L4, L5)
    content = content.replace("<td><span class=\"layer-badge l4\">L4 Bigzone</span></td>\n              <td><span class=\"kpi-pill kpi-gray\">×1.1</span></td>\n              <td class=\"good\">Có Đội trưởng</td>", "<td><span class=\"layer-badge l4\">L4 Bigzone</span></td>\n              <td><span class=\"kpi-pill kpi-gray\">×1.1</span></td>\n              <td class=\"warn\">Không</td>")
    content = content.replace("<td><span class=\"layer-badge l5\">L5 Cityzone</span></td>\n              <td><span class=\"kpi-pill kpi-gray\">×1.0</span></td>\n              <td class=\"good\">Có Đội trưởng</td>", "<td><span class=\"layer-badge l5\">L5 Cityzone</span></td>\n              <td><span class=\"kpi-pill kpi-gray\">×1.0</span></td>\n              <td class=\"warn\">Không</td>")
    # In layer-benefits it might be different structure
    content = content.replace("<td>L4 Bigzone</td>\n              <td>×1.1</td>\n              <td class=\"good\">Có Đội trưởng</td>", "<td>L4 Bigzone</td>\n              <td>×1.1</td>\n              <td class=\"warn\">Không</td>")
    content = content.replace("<td>L5 Cityzone</td>\n              <td>×1.0</td>\n              <td class=\"good\">Có Đội trưởng</td>", "<td>L5 Cityzone</td>\n              <td>×1.0</td>\n              <td class=\"warn\">Không</td>")

    content = content.replace("Hệ số áp theo <strong>đơn hàng</strong>, không theo rank tài xế. Tài xế R1 nhận đơn overflow từ L3 vẫn chỉ được ×1.3 (hệ số L3), không phải ×1.5.", "Hệ số áp theo <strong>đơn hàng</strong> và tài xế Layer, không theo rank tài xế. Tài xế R1 đăng ký ca L3 và nhận đơn overflow từ L3 vẫn chỉ được ×1.3 (hệ số L3), không phải ×1.5. Khi Tài xế không đăng ký hoặc không trong ca hoạt động thì thì hệ số nhân điểm của đơn hàng đó là 1.0.")

    # Base Pts
    content = content.replace("<td>56</td>\n              <td>56 × 1.5 = 84</td>\n              <td><strong>84</strong></td>", "<td>280</td>\n              <td>280 × 1.5 = 420</td>\n              <td><strong>420</strong></td>")
    content = content.replace("<td>52</td>\n              <td>52 × 1.3 = 68</td>\n              <td><strong>68</strong></td>", "<td>260</td>\n              <td>260 × 1.3 = 338</td>\n              <td><strong>338</strong></td>")
    content = content.replace("<td>48</td>\n              <td>48 × 1.1 = 53</td>\n              <td><strong>53</strong></td>", "<td>240</td>\n              <td>240 × 1.1 = 264</td>\n              <td><strong>264</strong></td>")
    content = content.replace("<td>44</td>\n              <td>44 × 1.0 = 44</td>\n              <td><strong>44</strong></td>", "<td>220</td>\n              <td>220 × 1.0 = 220</td>\n              <td><strong>220</strong></td>")
    
    # Calibration
    content = content.replace("84 × 22 = 1.848 pts", "420 × 22 = 9.240 pts")
    content = content.replace("68 × 22 = 1.496 pts", "338 × 22 = 7.436 pts")
    content = content.replace("53 × 22 = 1.166 pts", "264 × 22 = 5.808 pts")
    content = content.replace("44 × 22 = 968 pts", "220 × 22 = 4.840 pts")
    content = content.replace("1.340 pts/tháng", "6.747 pts/tháng")
    content = content.replace("1.340 × 80% = ~1.072 pts", "6.747 × 80% = ~5.398 pts")
    content = content.replace("Paid reward 50k = 1.000 pts (cân chỉnh lại giá trị điểm)", "Paid reward 50k = 5.000 pts (cân chỉnh lại giá trị điểm: 1 điểm = 10đ)")
    content = content.replace("~268 pts/tháng", "~1.349 pts/tháng")
    content = content.replace("40–170 pts", "200–850 pts")

    content = content.replace("<td>1.848</td>\n              <td class=\"good\">✅ 1.000 pts (dư ~848)</td>\n              <td>~800 pts free</td>", "<td>9.240</td>\n              <td class=\"good\">✅ 5.000 pts (dư ~4.240)</td>\n              <td>~4.000 pts free</td>")
    content = content.replace("<td>1.496</td>\n              <td class=\"good\">✅ 1.000 pts (dư ~496)</td>\n              <td>~400 pts free</td>", "<td>7.436</td>\n              <td class=\"good\">✅ 5.000 pts (dư ~2.436)</td>\n              <td>~2.000 pts free</td>")
    content = content.replace("<td>1.166</td>\n              <td class=\"good\">✅ 1.000 pts (dư ~166)</td>\n              <td>~100 pts free</td>", "<td>5.808</td>\n              <td class=\"good\">✅ 5.000 pts (dư ~808)</td>\n              <td>~800 pts free</td>")
    content = content.replace("<td>968</td>", "<td>4.840</td>")

    # Catalog
    content = content.replace("Giá trị thực (VND) ÷ 50", "Giá trị thực (VND) ÷ 10")
    content = content.replace("600 pts (Giá", "3.000 pts (Giá")
    content = content.replace("1.000 pts (Giá", "5.000 pts (Giá")
    content = content.replace("400 pts (Giá", "2.000 pts (Giá")
    content = content.replace("3.000 pts (Giá", "15.000 pts (Giá")
    content = content.replace("800 pts</li>", "4.000 pts</li>")
    content = content.replace("5.000 pts (Giá", "25.000 pts (Giá")
    content = content.replace("2.000 pts (Giá", "10.000 pts (Giá")
    content = content.replace("3.400 pts</li>", "17.000 pts</li>")
    
    content = content.replace("1.000 pts (Chi", "5.000 pts (Chi")
    content = content.replace("2.400 pts (Chi", "12.000 pts (Chi")
    content = content.replace("1.600 pts (Chi", "8.000 pts (Chi")
    content = content.replace("5.000 pts (Chi", "25.000 pts (Chi")
    content = content.replace("6.000 pts (Chi", "30.000 pts (Chi")
    content = content.replace("3.000 pts (Chi", "15.000 pts (Chi")
    content = content.replace("200 pts/tháng", "1.000 pts/tháng")
    content = content.replace("600 pts/tháng", "3.000 pts/tháng")
    content = content.replace("285–600 pts", "1.000–3.000 pts")
    content = content.replace("10k/tháng = 200 pts · 30k/tháng = 600 pts", "10k/tháng = 1.000 pts · 30k/tháng = 3.000 pts")

    # Add slot dang ky
    if "<td>✅ 08:00–18:00</td>" in content and "Slot đăng ký" not in content:
        content = content.replace("<tr>\n              <td><strong>Khung giờ đăng ký ca (Ngày 1)</strong></td>", "<tr>\n              <td><strong>Slot đăng ký</strong></td>\n              <td>Tất cả L2-L6</td>\n              <td>Tất cả L2-L6</td>\n              <td>Tất cả L2-L6</td>\n              <td>L5-6 MASS</td>\n            </tr>\n            <tr>\n              <td><strong>Khung giờ đăng ký ca (Ngày 1)</strong></td>")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

process_file("2026-05-driver-ranking-params.html")
process_file("2026-05-driver-ranking-layer-benefits.html")
