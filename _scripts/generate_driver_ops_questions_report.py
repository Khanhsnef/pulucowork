#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE DM NW STRATEGIC DRIVER OPERATIONS DIAGNOSTIC QUESTIONS REPORT
===============================================================================
Xây dựng Bộ Câu Hỏi Chuyên Sâu Xoay Quanh Vận Hành Tài Xế (Driver Operations):
1. Quản Trị Tuyển Nạp & Kích Hoạt Ca Đầu (Acquisition & Activation — NIM)
2. Duy Trì, Giữ Chân & Quản Trị Churn (Retention & Engagement — NLM & >=22yo)
3. Năng Suất, Phân Bổ Ca & Giờ Online (Productivity & Supply Hours — FT vs PT)
4. Kỷ Luật Tuân Thủ & Chất Lượng Phục Vụ (Quality & Compliance — GDR & CTR)
5. Hành Vi Từ Chối / Hủy Đơn Theo Nhánh Dịch Vụ (Driver Behavior & Cancel Rate)
6. Kích Hoạt Tài Xế Ngưng Chạy & Động Lực Thu Nhập (Reactivation & Income Economics)

Tác giả: Strategy & BI Operations — Driver Management Network
===============================================================================
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_driver_ops_questions_report():
    report_content = """# 🛵 BỘ CÂU HỎI PHÂN TÍCH CHUYÊN SÂU XOAY QUANH VẬN HÀNH TÀI XẾ (DRIVER OPERATIONS DIAGNOSTIC FRAMEWORK)

> **Báo cáo Khung Phân Tích & Chẩn Đoán Vận Hành Tài Xế (Driver Operations Diagnostic Report)**  
> **Đơn vị thực hiện:** Strategy & BI Operations Team — Driver Management Network (DM NW)  
> **Phương pháp tiếp cận:** Phân rã 6 Trụ Cột Vòng Đời & Hành Vi Tài Xế dựa trên 10 Metabase Cards Thực Tế (Metabase Card #75750, #79066, #62728, #75304, #76069, #79068, #72864, #77913, #67888, #75557).

---

## 📌 BẢNG TỔNG HỢP CÁC CHỈ SỐ METABASE VỀ TÀI XẾ (DRIVER METRICS OVERVIEW)

| Metabase Card ID | Tên Chỉ Số Vận Hành Tài Xế Metabase | Phạm Vi | Chỉ Số Thực Tế (`Actual`) | Ý Nghĩa Trong Vận Hành Tài Xế |
| :---: | :--- | :---: | :---: | :--- |
| **Card #72864** | Active Drivers Weekly (Non-Additive) | NW / SGN / HAN / EXP | **24,121 Unique Drivers / Tuần** | Quy mô lực lượng tài xế thực tế hoạt động hàng tuần |
| **Card #79066** | Total Supply Hours | NW / SGN / HAN | **1,295,836.0 Giờ Online** | Dung lượng thời gian online tích lũy của tài xế |
| **Card #75557** | Active Rate & Income theo Segment | FT / PT / Return / NIM / NLM | **FT Active 94.2% \| Thu nhập 18.5M** | Phân khúc năng suất, giờ online, busy rate & thu nhập |
| **Card #79068** | Retention Bike Driver $\ge 22$t | SGN / HAN | **SGN 77.33% \| HAN 74.17%** | Tỷ lệ giữ chân tài xế nạp tháng trước (NLM HAN `68.74%`) |
| **Card #76069** | Cancel Rate PoC | HAN / SGN / NW | **HAN Tân Binh CR 12.54%** | Tỷ lệ hủy đơn của nhóm tài xế mới vs toàn mạng lưới |
| **Card #75304** | Compliance True Rate (CTR) | NW / SGN / HAN | **NW CTR 74.15% \| SGN 81.20%** | Kỷ luật tuân thủ đồng phục & quy chuẩn thương hiệu |
| **Card #62728** | Good Driver Rate (GDR) | SGN / HAN / GR | **SGN GDR 96.51% \| GR 96.21%** | Tỷ lệ tài xế đạt chuẩn chất lượng phục vụ 5 sao |
| **Card #67888** | Cancel Rate Theo Service Type | Nhánh Dịch Vụ | **Shopee CR 37.61% \| 1H CR 10.80%** | Mức độ từ chối / hủy đơn của tài xế theo từng loại đơn |
| **Card #77913** | Surge Rate & RPH | SGN / HAN / EXP | **HAN Surge 48.3% \| RPH 2.07** | Áp lực gánh đơn ca cao điểm & mật độ đơn/giờ tài xế |

---

## 🔍 6 TRỤ CỘT CÂU HỎI VẬN HÀNH TÀI XẾ CHIẾN LƯỢC (DRIVER OPERATIONS QUESTIONS)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   6 PILLARS OF DRIVER OPERATIONS DIAGNOSTICS                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│ [PILLAR 1] Tuyển Nạp & Kích Hoạt Ca Đầu (Acquisition & Activation — NIM)        │
│ [PILLAR 2] Giữ Chân, Duy Trì & Quản Trị Churn (Retention & Engagement — NLM)     │
│ [PILLAR 3] Năng Suất, Phân Bổ Ca & Giờ Online (Productivity & Supply Hours)      │
│ [PILLAR 4] Kỷ Luật Tuân Thủ & Chất Lượng Phục Vụ (Discipline & Compliance — QM)   │
│ [PILLAR 5] Phản Ứng Từ Chối / Hủy Đơn (Driver Behavior by Fleet & Cancel Rate)  │
│ [PILLAR 6] Kích Hoạt Tài Xế Ngưng Chạy & Thu Nhập (Reactivation & Income)        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

### 🛵 TRỤ CỘT 1: QUẢN TRỊ TUYỂN NẠP & KÍCH HOẠT CA ĐẦU (ACQUISITION & ACTIVATION — NIM)

1. **Phễu Kích Hoạt Tân Binh (First Order Activation Rate):**
   - Trong số tài xế mới nạp trong tháng (**NIM** - Active Rate hiện tại `55.4%`), có bao nhiêu % tài xế hoàn thành đơn hàng đầu tiên trong vòng **24h** và **72h** sau khi kích hoạt tài khoản?
   - Rào cản kỹ thuật hoặc điểm gãy (drop-off point) chính khiến 44.6% tân binh còn lại chưa phát sinh đơn chạy ca đầu là gì (Do chưa quen giao diện app, ngại nạp tiền balance, hay lo lắng quy trình thu COD)?

2. **Chi Phí Onboarding & Tuân Thủ Đầu Vào:**
   - Thời gian trung bình từ lúc tài xế hoàn thành đăng ký hồ sơ đến khi hoàn tất mua trang bị đồng phục, nạp tiền deposit balance và chính thức bật online phát sinh đơn đầu tiên là bao nhiêu ngày?
   - Việc đơn giản hóa quy trình xác thực hồ sơ online qua app có giúp tăng tỷ lệ kích hoạt tân binh NIM thêm +10-15% hay không?

---

### 🛵 TRỤ CỘT 2: GIỮ CHÂN, DUY TRÌ & QUẢN TRỊ CHURN (RETENTION & ENGAGEMENT — NLM & >=22YO)

3. **Phân Tích Churn MoM Nhóm Tân Binh Tháng Trước (NLM Cohort Churn):**
   - Yếu tố cốt lõi nào giúp chỉ số Retention nhóm tân binh NLM tại Hà Nội bứt phá **`+3.68% MoM`** (đạt `68.74%`), trong khi TP.HCM lại bị sụt sút **`-5.45% MoM`** (xuống `65.15%`)?
   - Thu nhập bình quân/giờ của tân binh NLM tại TP.HCM có bị sụt giảm hơn so với Hà Nội trong 14 ngày chạy đầu tiên hay không? Tỷ lệ rời bỏ (churn) diễn ra nhiều nhất ở tuần thứ 1 hay tuần thứ 3?

4. **Phân Rã Giữ Chân Theo Loại Xe & Độ Tuổi (Fleet & Age Cohort Retention):**
   - Chỉ số Retention của nhóm tài xế $\ge 22$ tuổi (`77.33%` SGN, `74.17%` HAN - Card #79068) có sự chênh lệch ra sao giữa **Tài xế xe máy xăng truyền thống** và **Tài xế chuyển đổi Xe điện (EV)**?
   - Tài xế Xe điện EV có tỷ lệ gắn kết bền vững hơn (Retention cao hơn) nhờ chi phí vận hành xăng/bảo dưỡng thấp hơn hay không?

---

### 🛵 TRỤ CỘT 3: NĂNG SUẤT, PHÂN BỔ CA & GIỜ ONLINE (PRODUCTIVITY & SUPPLY HOURS — FT vs PT)

5. **Giải Mã Điểm Nghẽn Nguồn Cung Ca Cao Điểm (Peak Hour Supply Deficit):**
   - Tại sao tổng số giờ online tại Hà Nội (**512,652 giờ**) lại thấp hơn TP.HCM (**783,184 giờ**) tới **35.2%**, dẫn đến RPH đẩy lên cao **`2.07 đơn/giờ`** và Tỷ lệ đơn Surge Pricing vọt lên **`48.3%`** (Card #77913)?
   - Nguồn cung giờ online tại Hà Nội bị hụt chính ở lực lượng **Part-time (PT)** hay **Full-time (FT)**? Sự thiếu hụt này tập trung vào ca trưa (11h-13h) hay ca chiều (17h-19h)?

6. **Mật Độ Giờ Bận (Busy Rate) & Ngưỡng Áp Lực Mệt Mỏi (Driver Fatigue Threshold):**
   - Tỷ lệ giờ bận (Busy Rate) của tài xế **Full-time (FT)** đạt **`71.5%`** (với `185h online/tháng`) so với **Part-time (PT)** là **`62.0%`** (với `125h online/tháng` - Card #75557).
   - Tỷ lệ bận `71.5%` này đã tối ưu hiệu suất thu nhập chưa, hay đang chạm ngưỡng quá tải khiến tài xế kiệt sức (Driver Fatigue) dẫn đến tỷ lệ từ chối/hủy đơn tăng đột ngột vào cuối ca?

---

### 🛵 TRỤ CỘT 4: KỶ LUẬT TUÂN THỦ & CHẤT LƯỢNG PHỤC VỤ (DISCIPLINE & COMPLIANCE — GDR & CTR)

7. **Kỷ Luật Tuân Thủ Đồng Phục & Nhận Diện Thương Hiệu (Compliance True Rate — CTR):**
   - Động lực chính giúp chỉ số CTR toàn quốc tăng 4 tháng liên tiếp chạm mốc kỷ lục **`74.15%`** (TP.HCM đạt `81.20%` - Card #75304) là gì?
   - Giữa nhóm tài xế mới nạp (NIM/NLM) và nhóm tài xế chạy lâu năm (FT), nhóm nào có tỷ lệ vi phạm quy chuẩn QM (không mặc áo khoác/không mang túi chuẩn) cao hơn khi bị kiểm tra thực địa?

8. **Chất Lượng Phục Vụ & Good Driver Rate (GDR Optimization):**
   - Chỉ số GDR tại TP.HCM giữ mốc xuất sắc **`96.51%`** (đạt max score 1.20x). Nhóm tài xế có GDR thấp (<90%) rơi vào những lỗi vi phạm nào phổ biến nhất (Thái độ phục vụ, thu tiền quá cước, hay giao hàng chậm lead-time)?
   - Cơ chế thưởng Good Driver hiện tại đã đủ sức giữ chân 10% tài xế xuất sắc nhất mạng lưới chưa?

---

### 🛵 TRỤ CỘT 5: PHẢN ỨNG TỪ CHỐI / HỦY ĐƠN THEO NHÁNH DỊCH VỤ (DRIVER CANCEL BEHAVIOR)

9. **Tâm Lý Từ Chối Đơn Đổi Trả Shopee Reverse (Cancel Rate 37.61%):**
   - Vì sao tỷ lệ hủy đơn dịch vụ Shopee Reverse vọt lên **`37.61%`** (cao gấp 3.5 lần so với gói Siêu Tốc 1H `10.80%` - Card #67888)?
   - Tài xế hủy đơn do gặp khó khăn khi tìm kiếm hàng tại kho SPX, khoảng cách di chuyển quá xa, hay do lo ngại rủi ro đền bù khi xảy ra thất lạc hàng đổi trả?

10. **Tâm Lý Nhận Đơn Bulky & Ghép Đơn 2H (Bulky CR 26.69% & 2H CR 30.45%):**
    - Rào cản về **hạn mức tiền mặt COD balance**, kích thước hàng hóa kềnh hay thời gian chờ ghép đơn quá lâu là nguyên nhân chính làm 26% - 30% đơn Bulky và 2H bị tài xế hủy bỏ sau khi nhận gán?
    - Việc trang bị Baga tiêu chuẩn và hỗ trợ nâng hạn mức COD balance có giúp giảm tỷ lệ hủy đơn Bulky xuống dưới mốc <18% không?

---

### 🛵 TRỤ CỘT 6: KÍCH HOẠT TÀI XẾ NGƯNG CHẠY & ĐỘNG LỰC THU NHẬP (REACTIVATION & ECONOMICS)

11. **Phục Hồi Nguồn Cung Tài Xế Quay Lại (Return / Reactivation Rate):**
    - Tỷ lệ active của nhóm tài xế quay lại (**Return**) đạt **`74.6%`** với thu nhập trung bình **`6.8M – 8.5M VNĐ/tháng`** (Card #75557).
    - Đâu là đòn bẩy hiệu quả nhất (Cuộc gọi chăm sóc CHL, Notification cá nhân hóa, hay gói thưởng chào mừng) giúp kích hoạt tài xế ngưng chạy trên 30 ngày quay trở lại app?

12. **Cân Bằng Thu Nhập Bình Quân & Cạnh Tranh Thị Trường (Driver Unit Economics):**
    - Mức thu nhập trung bình/tháng của tài xế **Full-time (18.5 triệu VNĐ)** và **Part-time (10.5 triệu VNĐ)** trên hệ thống Ahamove có đủ sức cạnh tranh và chống chảy máu nguồn cung sang các đối thủ cạnh tranh trên thị trường (Grab, Lalamove, Be, XanhSM) hay không?

---

> [!IMPORTANT]
> **Tài liệu Bộ Câu Hỏi Phân Tích Vận Hành Tài Xế đã được lưu trữ tại:**  
> 🔗 [`Output/Ahamove/04. OPS_METRICS/ahamove_driver_ops_questions_report.md`](file:///Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/04.%20OPS_METRICS/ahamove_driver_ops_questions_report.md)
"""

    out_dir = "Output/Ahamove/04. OPS_METRICS"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ahamove_driver_ops_questions_report.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"🎉 Đã xuất thành công Master Driver Operations Diagnostic Questions Report tại: {out_path}")

if __name__ == "__main__":
    build_driver_ops_questions_report()
