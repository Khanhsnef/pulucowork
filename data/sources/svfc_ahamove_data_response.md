# 📊 TÓM TẮT THỰC THI (EXECUTIVE SUMMARY — GỘP TP.HCM `SGN` + HÀ NỘI `HAN` & QUY TRÌNH VẬN HÀNH)

*   **Quyết định Chiến lược về Quy trình Thực hiện (Mục 2.1 & 2.2):**
    1.  **Về Quy trình Đăng ký Vay / Phát hành Thẻ (Mục 2.1) $\rightarrow$ CHỌN PHƯƠNG ÁN 1 (Webview do SVFC xây dựng nhúng trên App AhaDriver, có Pre-fill dữ liệu qua API):** Tối ưu thời gian Go-live (Time-to-Market chỉ 2–4 tuần thay vì 3–4 tháng), giảm 80% nguồn lực kỹ thuật (Tech/Product) cho Ahamove, đồng thời đẩy toàn bộ trách nhiệm tuân thủ pháp lý eKYC/Hợp đồng tín dụng về hệ thống chuẩn của SVFC.
    2.  **Về Quy trình Trả nợ / Thu hộ (Mục 2.2) $\rightarrow$ CHỌN OP 2 (Giữ tiền theo chu kỳ 1 tuần dựa trên Practice đối soát hiện tại của Ahamove) kết hợp cơ chế "Khấu trừ từng phần theo ngày/tuần (Micro-withholding Cap $\le$ 25–30% thu nhập tuần)":**
        *   **Bác bỏ Op 1 (Giữ tiền trên Ví tài xế 01 tháng):** Không khả thi về mặt tâm lý hành vi tài xế (Driver Psychology) và vận hành thực địa. Tài xế xe công nghệ cần dòng tiền mặt xoay vòng hàng ngày/hàng tuần để đổ xăng, ăn uống và nộp COD. Nếu giam tiền hoặc trừ cục bộ 1 tháng sẽ gây **sốc thanh khoản**, dẫn đến tài xế **bỏ app (Churn), tắt app chạy hãng khác hoặc rút sạch ví trước ngày chốt**.
        *   **Tối ưu hóa Op 2 (Chu kỳ 1 tuần theo Practice hiện tại):** Khớp 100% với kỳ quyết toán thưởng tuần và đối soát ví thứ Hai/thứ Ba hàng tuần của Ahamove. Khi giới hạn nghĩa vụ trả nợ hàng tháng của SVFC ở mức **$\le$ 50% – 70% thu nhập 1 tuần của tài xế** (tức chỉ tương đương **12% – 18% thu nhập tháng**), cả SVFC và Ahamove đều đảm bảo **Tỷ lệ thu hồi nợ thành công > 95%** mà không làm đứt gãy dòng tiền chạy xe của tài xế.
*   **Quy chuẩn Quy mô Tập Đối tác Cốt lõi (`SC` + `CN` = 27,734 tài xế/tháng tại `SGN` + `HAN`):**
    *   Gộp [svfc.xlsx](file:///Users/ts-1148/Desktop/Pulu-workspace/data/sources/svfc.xlsx) (`SGN`) và [svfc HAN.xlsx](file:///Users/ts-1148/Desktop/Pulu-workspace/data/sources/svfc%20HAN.xlsx) (`HAN`), tập đối tác hoạt động ổn định có lịch sử vận hành tốt (**`SC` + `CN`**) đạt trung bình **27,734 tài xế/tháng** (**`SC`: 14,616 TX** – thu nhập TB **15.99 triệu/tháng**; **`CN`: 13,118 TX** – thu nhập TB **10.62 triệu/tháng**), trên tổng **MAU toàn hệ thống đạt 98,442 tài xế/tháng**. Toàn bộ bảng tính động đã được lưu tại [svfc_ahamove_summary.xlsx](file:///Users/ts-1148/Desktop/Pulu-workspace/data/sources/svfc_ahamove_summary.xlsx).

---

# ⚖️ PHÂN TÍCH CHUYÊN SÂU MỤC 2: QUY TRÌNH VAY & TRẢ NỢ (DECISION NAVIGATOR)

## 1. Đánh giá Mục 2.1: Quy trình Vay / Phát hành Thẻ tín dụng (`Phương án 1` vs `Phương án 2`)

| Tiêu chí Đánh giá | Phương án 1: Nhúng Webview SVFC trên App AhaDriver *(ĐỀ XUẤT CHỌN)* | Phương án 2: Ahamove tự xây UI/Flow đăng ký Native trên App Driver |
| :--- | :--- | :--- |
| **Thời gian Triển khai (Time-to-Market)** | **Rất nhanh (2 – 4 tuần):** Chỉ cần mở Banner/Icon trên App AhaDriver, gọi SSO/Token truyền `driver_id` + gói dữ liệu API sang Webview SVFC. | **Chậm (3 – 4 tháng):** Phải thiết kế UI/UX, code Native iOS/Android, chờ duyệt bản cập nhật App Store / Google Play mỗi khi SVFC đổi quy trình. |
| **Chi phí Kỹ thuật & Vận hành (Tech & Ops Cost)** | **Tối thiểu cho Ahamove:** SVFC tự chủ động cập nhật biểu mẫu, lãi suất, điều khoản hợp đồng trên Webview mà không cần Ahamove sửa code App. | **Rất cao:** Đội Product/Tech Ahamove phải duy trì, fix bug luồng eKYC, OTP, upload CCCD, ký hợp đồng điện tử. |
| **Rủi ro Pháp lý & Bảo mật Dữ liệu (Compliance)** | **An toàn tuyệt đối cho Ahamove:** Tài xế thao tác eKYC, VNeID và ký Hợp đồng tín dụng trực tiếp trên môi trường của tổ chức tín dụng (SVFC). | **Rủi ro cao:** Ahamove phải lưu trữ/trung chuyển hồ sơ nhạy cảm (ảnh CCCD, sinh trắc học, hợp đồng vay) qua server trung gian. |
| **Trải nghiệm Tài xế (Driver UX)** | **Liền mạch nếu kết hợp API Pre-fill:** Ahamove truyền sẵn Họ tên, SĐT, CCCD, Hạng tài xế, Thu nhập qua API để Webview SVFC tự điền sẵn (Auto-fill), tài xế chỉ cần xác nhận. | Mượt về giao diện nhưng dễ phát sinh lỗi đồng bộ trạng thái hồ sơ giữa 2 hệ thống. |

---

## 2. Đánh giá Mục 2.2: Quy trình Trả nợ (`Op 1: Giữ 01 tháng` vs `Op 2: Giữ 01 tuần theo Practice hiện tại`)

> [!WARNING]
> **Rủi ro Cốt tử của Op 1 (Giữ tiền trên Ví tài xế 01 tháng):**
> Trong vận hành thực tế của ngành Ride-hailing / On-demand Delivery (Ahamove, Grab, Be), khoảng **65% – 75% doanh thu chuyến xe là Tiền mặt (Cash/COD)** tài xế thu trực tiếp từ khách hàng, và phần tiền trong **Ví Tài Xế (Cước trả trước qua thẻ/ví điện tử + Tiền thưởng tuần)** được tài xế dùng để **khấu trừ phí chiết khấu (Commission) hàng ngày** hoặc **rút ra hàng tuần** để chi tiêu/xoay vòng vốn COD.
> *   Nếu áp dụng **Op 1 (Giam/giữ tiền trên Ví tài xế suốt 01 tháng)**: Tài xế sẽ cảm thấy bị "đóng băng thu nhập", dẫn đến **phản ứng tiêu cực trên cộng đồng tài xế, rút sạch tiền khỏi ví ngay khi có thể, hoặc ngừng nhận đơn (Churn)** sang ứng dụng khác để có tiền mặt tiêu dùng hàng ngày.
> *   Nếu chỉ thực hiện **1 lệnh trừ cục bộ toàn bộ tiền gốc + lãi vào đúng 1 ngày cuối tháng**: Xác suất rất cao tại ngày đó số dư Ví Tài Xế **không đủ** để trừ một cục 1.5 – 3 triệu VNĐ, làm phát sinh nợ quá hạn kỹ thuật.

### So sánh Lợi ích — Rủi ro & Điểm Cân bằng Tối ưu giữa `Op 1` và `Op 2`

| Góc độ Đánh giá | Op 1: Giữ lại trên Ví tài xế 01 tháng | Op 2: Giữ lại trên Ví tài xế 01 tuần theo Practice hiện tại *(ĐỀ XUẤT CHỌN)* |
| :--- | :--- | :--- |
| **Đối với Tài xế (Driver Psychology & Cashflow)** | ❌ **Áp lực dòng tiền lớn:** Bị giữ tiền cả tháng hoặc bị trừ một khoản lớn đột ngột làm thiếu tiền mặt đổ xăng/ứng COD hàng ngày. | ✅ **Nhẹ nhàng, không gây sốc thanh khoản:** Khớp với chu kỳ nhận thưởng tuần hiện tại của tài xế. Tài xế vẫn rút được phần dư thu nhập hàng tuần để sinh hoạt. |
| **Đối với Ahamove (Driver Retention & Ops SLA)** | ❌ **Rủi ro mất nguồn cung (Driver Churn):** Tài xế sợ bị giam tiền ví nên giảm giờ online hoặc bỏ sang hãng khác vào tuần cuối tháng. Phải sửa sâu logic Ví Tài Xế. | ✅ **Giữ chân tài xế & Tận dụng sẵn hạ tầng:** Tận dụng nguyên vẹn luồng đối soát/quyết toán ví hàng tuần hiện hữu của Ahamove, không làm giảm tỷ lệ Active/Fulfillment. |
| **Đối với SVFC (Credit Risk & Collection Rate)** | ❌ **Rủi ro thu hồi nợ thấp (All-or-Nothing):** Đợi cả tháng mới chốt giữ tiền dễ gặp rủi ro tài xế nghỉ chạy ở tuần thứ 3–4, ví bằng 0đ vào ngày thanh toán. | ✅ **Kiểm soát rủi ro sớm (Early Warning):** Gọi API đối soát hàng ngày/hàng tuần; tiền trả nợ được khóa/thu gọn ngay trong kỳ thu nhập tuần gần nhất trước ngày đến hạn (`01, 05, 10, 16`). |

### 💡 Thiết kế Cơ chế Vận hành Tối ưu cho `Op 2` (Win – Win cho cả Ahamove & SVFC)

Để **Op 2** vận hành trơn tru nhất, Ahamove đề xuất với SVFC công thức định lượng cụ thể cho dấu `...%` trong đề bài của SVFC như sau:

1.  **Ngưỡng Trần Khấu trừ Tuần (Weekly Repayment Cap = Tối đa `50% – 70%` thu nhập thanh toán của 1 tuần, hoặc chia đều `20% – 25%` mỗi tuần):**
    *   *Theo ví dụ của SVFC:* Tài xế nhóm `CN`/`SC` có thu nhập **12 triệu VNĐ/tháng** ($\approx$ **3 triệu VNĐ/tuần**).
    *   Với khoản vay tiêu dùng **20 – 30 triệu VNĐ** (hoặc thẻ tín dụng 15 triệu VNĐ), số tiền gốc + lãi phải trả hàng tháng cho SVFC chỉ rơi vào khoảng **1,2 – 1,8 triệu VNĐ/tháng**.
    *   Như vậy, tổng số tiền phải trả hàng tháng cho SVFC chỉ chiếm **40% – 60% thu nhập của 1 tuần duy nhất** (nhỏ hơn nhiều so với mức 3 triệu VNĐ/tuần của tài xế).
    *   **Đề xuất điền vào dấu `...%` của SVFC:** *"Số tiền phải trả hàng tháng cho SVFC không vượt quá **70% số tiền bình quân được thanh toán định kỳ hàng tuần** (tương đương không quá **18% – 20% tổng thu nhập tháng** của tài xế)"*.
2.  **Hai tùy chọn Kỹ thuật thực thi Op 2 cho Ahamove & SVFC:**
    *   **Cách 2A — Giữ tiền trong Tuần liền kề trước Ngày Thanh toán (`01, 05, 10, 16`):** SVFC gửi API báo số tiền đến hạn trước 7 ngày $\rightarrow$ Trong chu kỳ 1 tuần trước ngày thanh toán, hệ thống Ví Ahamove tự động tạm giữ (Hold/Freeze) khoản tiền trả nợ từ doanh thu ví/thưởng tuần của tài xế (tối đa không quá 70% thu nhập tuần đó) và chuyển sang SVFC vào đúng ngày thanh toán.
    *   **Cách 2B — Tích lũy theo Tuần / Ngày (Smooth Weekly Auto-Save):** Chia khoản trả góp tháng làm 4 phần nhỏ mỗi tuần (ví dụ: phải trả 1.6 triệu/tháng $\rightarrow$ mỗi kỳ đối soát tuần giữ lại 400.000đ). Cách này giúp tài xế hầu như không cảm thấy áp lực bị trừ tiền, tỷ lệ thu hồi của SVFC đạt gần như tuyệt đối **100%**.

---

# 📧 BẢN NHÁP EMAIL PHẢN HỒI TOÀN DIỆN CHO SVFC (BAO GỒM DATA SGN+HAN & MỤC 2.1, 2.2)

> [!TIP]
> Bản nháp dưới đây đã tích hợp **cả Phần 1 (Bảng tiêu chí + Data SGN & HAN)** và **Phần 2 (Phản hồi lựa chọn Phương án Quy trình Vay 2.1 & Quy trình Trả nợ 2.2)** để bạn copy gửi trực tiếp cho SVFC.

**Tiêu đề (Subject):** Re: [AHAMOVE x SVFC] Phản hồi dữ liệu Đối tác Tài xế (TP.HCM & Hà Nội) và Đề xuất Quy trình Vay & Trả nợ tối ưu

**Nội dung (Body):**

Kính gửi Anh/Chị Đại diện **SVFC** *(Shinhan Finance)*,

Cảm ơn Quý Đối tác đã gửi khung tiêu chí sản phẩm **Gói ứng tiền nhanh**, **Gói vay tiêu dùng** cùng đề xuất **Quy trình thực hiện (Mục 2.1 & 2.2)** dành cho Đối tác Tài xế Ahamove.

Tiếp nối thông tin đã trao đổi về lực lượng **~25.000 – 35.000 đối tác tài xế hoạt động ổn định, có lịch sử vận hành tốt (nhóm Siêu cấp `SC` & Chuyên nghiệp `CN`)**, Ahamove xin gửi phản hồi chi tiết bao gồm: **(I) Bảng thông tin sản phẩm & dữ liệu thực tế tại TP.HCM (`SGN`) + Hà Nội (`HAN`)**, và **(II) Đánh giá & Đề xuất của Ahamove đối với Quy trình vay / phát hành thẻ (2.1) và Quy trình trả nợ (2.2)** như sau:

---

### PHẦN 1. BẢNG PHẢN HỒI TIÊU CHÍ SẢN PHẨM & SỐ LIỆU TÀI XẾ (TP.HCM & HÀ NỘI)

#### 1.1. Bảng Phản hồi theo Khung Tiêu chí của SVFC

| Tiêu chí | Gói ứng tiền nhanh | Gói vay tiêu dùng | Thông tin AHAMOVE bổ sung & Đề xuất (Số liệu SGN + HAN) |
| :--- | :--- | :--- | :--- |
| **Đối tượng** | Khách hàng là tài xế của AHAMOVE | Khách hàng là tài xế của AHAMOVE | **1. Quy mô MAU / DAU trên App AhaDriver (TP.HCM & Hà Nội):**<br>• **MAU (Active Drivers hàng tháng):** Đạt trung bình **98.442 tài xế/tháng** (T08: 99.246 \| T09: 95.712 \| T10: 103.430 \| T11: 95.378), trong đó khu vực **TP.HCM (`SGN`) chiếm 59,57% (58.645 TX)** và **Hà Nội (`HAN`) chiếm 40,43% (39.797 TX)**.<br>• **DAU (Active hàng ngày):** Đạt **~45.000 – 58.000 tài xế/ngày** (thời gian online trung bình toàn hệ thống đạt **112,6 giờ/tháng/tài xế**, riêng nhóm Full-time đạt **210,7 giờ/tháng**).<br>**2. Tỷ lệ duy trì hoạt động (Retention) & Tập đối tác cốt lõi (`SC` – `CN`):**<br>• **Tập đối tác hoạt động ổn định có lịch sử vận hành tốt (`SC` + `CN`):** Đạt trung bình **27.734 tài xế/tháng (28,17% MAU)**, khớp với quy mô **25.000 – 35.000 đối tác cốt lõi** đã trao đổi. Khi mở rộng thêm nhóm Bán chuyên (`BC`: **23.121 tài xế/tháng**), tổng quy mô phễu khách hàng mục tiêu đạt **50.855 tài xế/tháng (51,66% MAU)**.<br>• **Tỷ lệ duy trì hoạt động (Retention Rate):** Nhóm tài xế cũ hoạt động liên tục từ tháng trước (`OLD` + `NLM`) đạt **85,30% MAU** (riêng nhóm `OLD` chiếm **77,15%**). Nếu tính cả nhóm tài xế cũ quay lại (`Return`: **5,97%**), tổng tỷ lệ tài xế gắn bó đạt **91,27% MAU** (T11/2026 đạt **93,02%**).<br>**3. Khả năng hỗ trợ Digital Selling & Tăng tỷ lệ chuyển đổi:**<br>• **In-app Banner / Placement:** Hiển thị tại Trang chủ App AhaDriver, màn hình **Ví Tài Xế** (điểm chạm có tần suất truy cập cao nhất mỗi ngày) và mục Đặc quyền Tài xế.<br>• **Push Notification & In-app Message:** Gửi thông báo cá nhân hóa tới từng phân khúc.<br>• **Segment Targeting:** Phân nhóm tự động theo Hạng tài xế (`SC`, `CN`, `BC`), Khu vực (`SGN`, `HAN`), Thâm niên và Thu nhập thực tế để hiển thị gói vay phù hợp. |
| **Mục đích vay vốn** | Tài xế có nhu cầu ứng tiền nhanh | Tài xế có nhu cầu tiêu dùng trung dài hạn | Phù hợp với nhu cầu thanh khoản ngắn hạn (xăng xe, bảo dưỡng phương tiện, sinh hoạt phí) và tiêu dùng trung dài hạn (mua/nâng cấp xe máy, điện thoại, học phí gia đình). |
| **Số tiền cho vay** | Hạn mức tối đa 10-15 triệu đồng | Tối đa 10-30 triệu đồng | **Đề xuất phân tầng hạn mức theo Hạng tài xế (Ranking):**<br>• **Nhóm Siêu cấp (`SC` – 14.616 TX, thu nhập TB ~15,99 triệu):** Ứng nhanh **15 triệu** \| Vay tiêu dùng **20 – 30 triệu**.<br>• **Nhóm Chuyên nghiệp (`CN` – 13.118 TX, thu nhập TB ~10,62 triệu):** Ứng nhanh **10 – 15 triệu** \| Vay tiêu dùng **15 – 25 triệu**.<br>• **Nhóm Bán chuyên (`BC` – 23.121 TX, thu nhập TB ~6,06 triệu):** Ứng nhanh **10 triệu** \| Vay tiêu dùng **10 – 15 triệu**. |
| **Thời gian cho vay** | Thời hạn hạn mức | Tối đa 60 tháng | Thống nhất theo chính sách sản phẩm của SVFC. |
| **Hình thức cho vay** | Thẻ tín dụng ảo có tính năng rút tiền mặt tại quầy VPB “MIỄN PHÍ” trong 30 ngày đầu mở thẻ | Cho vay trung dài hạn | Ahamove hỗ trợ truyền thông điểm nhấn **“MIỄN PHÍ rút tiền mặt tại quầy VPB trong 30 ngày đầu”** ngay trên luồng đăng ký In-app để tối đa hóa tỷ lệ kích hoạt thẻ. |
| **Độ tuổi khách hàng** | Từ 21 tuổi đến độ tuổi nghỉ hưu theo quy định Pháp luật | Từ 21 tuổi đến độ tuổi nghỉ hưu theo quy định Pháp luật | **100% tài xế trong danh mục từ 21 tuổi trở lên (trong đó > 69% từ 26 tuổi trở lên):**<br>• Nhóm 21 – 22 tuổi: **22.761 TX (23,12%)**<br>• Nhóm 23 – 25 tuổi: **7.085 TX (7,20%)**<br>• Nhóm 26 – 30 tuổi: **12.342 TX (12,54%)**<br>• Nhóm 31 – 40 tuổi: **30.173 TX (30,65%)**<br>• Nhóm > 40 tuổi: **26.082 TX (26,49%)** |
| **Thời gian làm việc** | Đề xuất: **Từ 3 – 6 tháng trở lên** | Đề xuất: **Từ 6 tháng trở lên** | **Xem chi tiết tại Bảng 1.2 bên dưới.** Nhóm có thâm niên **$\ge$ 6 tháng** đạt **65.854 TX/tháng (66,90% MAU)**; nhóm **$\ge$ 12 tháng** đạt **52.024 TX/tháng (52,85% MAU)**. |
| **Thu nhập tối thiểu** | Đề xuất: **Từ 5 – 6 triệu đồng/tháng** | Đề xuất: **Từ 6 – 8 triệu đồng/tháng** | **Xem chi tiết tại Bảng 1.3 bên dưới.** Nhóm có thu nhập bình quân qua ứng dụng **$\ge$ 6 triệu đồng/tháng** đạt **37.689 TX/tháng (38,29% MAU)**, trong đó nhóm **$\ge$ 10 triệu đồng/tháng** đạt **24.710 TX/tháng (25,10% MAU)**. |
| **Điều kiện KH** | Thỏa mãn tiêu chí chọn lọc khách hàng:<br>+ Nhóm siêu cấp (`SC`)<br>+ Nhóm chuyên dụng (`CN`)<br>+ Nhóm bán chuyên (`BC`) / Full-time (`FT`) | Thỏa mãn tiêu chí chọn lọc khách hàng:<br>+ Nhóm siêu cấp (`SC`)<br>+ Nhóm chuyên dụng (`CN`)<br>+ Nhóm bán chuyên (`BC`) / Full-time (`FT`) | **Xem chi tiết chân dung từng nhóm tại Bảng 1.4 bên dưới.** |
| **Lịch sử tín dụng** | Không có nợ quá hạn và nợ xấu theo quy định SVFC | Không có nợ quá hạn và nợ xấu theo quy định SVFC | SVFC kiểm tra CIC/PCB theo quy định. Ahamove hỗ trợ lọc trước (Pre-screening) các tài xế có lịch sử vận hành tốt, không vi phạm quy chế/gian lận trên nền tảng. |
| **Ngày thanh toán** | • Ngày chốt sao kê: 5, 10, 20 hàng tháng<br>• Ngày thanh toán: +15 ngày kể từ ngày sao kê<br>• Thanh toán tối thiểu 2% hoặc toàn bộ dư nợ | Ngày thanh toán thuộc một trong các ngày: 01, 05, 10 hoặc 16 hàng tháng | Hoàn toàn khớp với chu kỳ đối soát ví hàng tuần của Ahamove (chi tiết tại Mục 2.2 bên dưới). |
| **Lãi suất và Phí** | Lãi suất & Phí ưu đãi | Lãi suất & Phí ưu đãi | Đề xuất SVFC áp dụng biểu lãi suất ưu đãi đặc quyền cho tập **~27.734 tài xế nhóm `SC` & `CN`** để tăng tỷ lệ chuyển đổi. |
| **Thời gian xử lý hồ sơ** | Phê duyệt nhanh | Phê duyệt nhanh | Tích hợp luồng eKYC & truyền dữ liệu qua API giúp phê duyệt nhanh ngay trên ứng dụng AhaDriver. |
| **Thủ tục** | Online 100% | Online 100% | Triển khai 100% Online Journey qua Webview SVFC trên ứng dụng AhaDriver. |
| **Hồ sơ** | • Căn cước công dân, VNeID<br>• Thông tin API từ AHAMOVE | • Căn cước công dân, VNeID<br>• Thông tin API từ AHAMOVE | **Các trường thông tin Ahamove có thể cung cấp qua API (khi có sự đồng ý chia sẻ dữ liệu của Tài xế - User Consent theo NĐ 13/2023/NĐ-CP):**<br>1. **Định danh & Trạng thái:** Mã tài xế (`Driver ID`), Họ tên, SĐT đăng ký, Số CCCD đã xác thực, Nhóm độ tuổi, Khu vực hoạt động (`SGN` / `HAN`), Trạng thái tài khoản (`Active`).<br>2. **Thâm niên & Gắn bó:** Ngày kích hoạt tài khoản, Nhóm thâm niên (`fct_tenure_group`), Nhóm duy trì hoạt động (`OLD` / `Return` / `NLM` / `NIM`).<br>3. **Xếp hạng & Hiệu suất (3 – 6 tháng gần nhất):** Hạng tài xế (`SC` / `CN` / `BC` / `Un_rank`), Nhóm làm việc (`FT` / `PT`), Số đơn hoàn thành TB/tháng (`productivity`), Số giờ online TB/tháng (`online_hours`).<br>4. **Thu nhập:** Thu nhập bình quân tháng qua nền tảng Ahamove (`avg_income` / `income_bracket`). |

#### 1.2. Bảng Phân bổ theo Thời gian làm việc (Gộp SGN + HAN)

| Thời gian làm việc | Số lượng tài xế (TB 4 tháng) | % Tỷ trọng | Số lượng tài xế (T11/2026) | Đơn TB/tháng | Thu nhập TB/tháng (VNĐ) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **< 6 tháng** | **32.588** | **33,10%** | 30.422 | 142,9 | 4.226.113 |
| **6-12 tháng** | **13.830** | **14,05%** | 13.670 | 197,2 | 5.718.592 |
| **12-24 tháng** | **16.848** | **17,11%** | 15.752 | 232,6 | 7.145.538 |
| **24 -36 tháng** | **11.874** | **12,06%** | 12.096 | 271,7 | 8.044.829 |
| **Trên 36 tháng** | **23.303** | **23,67%** | 23.438 | 303,6 | 8.205.626 |
| **Tổng cộng** | **98.442** | **100,00%** | **95.378** | **219,4** | **6.338.043** |

#### 1.3. Bảng Phân bổ theo Mức Thu nhập Bình quân Tháng (Gộp SGN + HAN)

| Thu nhập / tháng | Số lượng tài xế (TB 4 tháng) | % Tỷ trọng | Số lượng tài xế (T11/2026) | Ghi chú Nhóm đối tượng |
| :--- | :---: | :---: | :---: | :--- |
| **< 6 triệu** | **60.753** | **61,71%** | 62.720 | Chủ yếu là tài xế Part-time (`PT`) / Chưa xếp hạng (`Un_rank`) chạy kiếm thêm |
| **6-10 triệu** | **12.980** | **13,18%** | 13.046 | Tài xế Bán chuyên (`BC`) & Chuyên nghiệp (`CN`) hoạt động đều đặn |
| **10-13 triệu** | **9.157** | **9,30%** | 9.688 | Tài xế Full-time (`FT`) hạng Chuyên nghiệp (`CN`) & Siêu cấp (`SC`) |
| **13 -17 triệu** | **11.565** | **11,75%** | 7.758 | Tài xế Chủ lực hạng Siêu cấp (`SC`), năng suất > 480 đơn/tháng |
| **17 -22 triệu** | **3.235** | **3,29%** | 2.142 | Nhóm Cao cấp hạng Siêu cấp (`SC`), năng suất 600 – 750 đơn/tháng |
| **>22 triệu** | **754** | **0,77%** | 24 | Nhóm Đỉnh cao hạng Siêu cấp (`SC`), năng suất > 750 đơn/tháng |
| **Tổng cộng** | **98.442** | **100,00%** | **95.378** | **Tổng nhóm thu nhập $\ge$ 6 triệu/tháng đạt 37.689 TX/tháng (38,29% MAU)** |

#### 1.4. Chân dung Chi tiết các Nhóm Phân hạng Khách hàng (Gộp SGN + HAN)

| Phân hạng Tài xế | Số lượng TX (TB 4 tháng) | % Tỷ trọng | Năng suất TB (Đơn/tháng) | Giờ Online TB (Giờ/tháng) | Thu nhập TB/tháng (VNĐ) | Đặc điểm Vận hành & Đề xuất Phê duyệt (Whitelist) |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Nhóm Siêu cấp (`SC`)** | **14.616** | **14,85%** | **585,9 đơn** | **248,7 giờ** | **15.987.882** | **Lực lượng nòng cốt nhất (100% Full-time):** Online > 8,2 giờ/ngày, thu nhập rất cao và ổn định. Đề xuất duyệt hạn mức tối đa cho cả 2 gói vay. |
| **2. Nhóm Chuyên nghiệp / Chuyên dụng (`CN`)** | **13.118** | **13,33%** | **397,2 đơn** | **177,9 giờ** | **10.616.472** | **Lực lượng chuyên nghiệp ổn định:** Online ~6 giờ/ngày, thu nhập TB > 10,6 triệu/tháng. Kết hợp cùng nhóm `SC` tạo thành tập **27.734 đối tác cốt lõi (28,17% MAU)**. |
| **3. Nhóm Bán chuyên (`BC`)** | **23.121** | **23,49%** | **201,6 đơn** | **116,0 giờ** | **6.062.778** | **Lực lượng bán chuyên thường xuyên:** Online ~4 giờ/ngày, thu nhập TB > 6 triệu/tháng. Phù hợp với **Gói Ứng Tiền Nhanh (10 – 15 triệu)** và Gói Vay Tiêu Dùng (thâm niên $\ge$ 6 tháng). |
| **4. Nhóm Phổ thông (`Un_rank`)** | **47.587** | **48,34%** | **66,6 đơn** | **51,2 giờ** | **2.328.547** | Tài xế chạy bán thời gian linh hoạt hoặc mới gia nhập. Chỉ xét cấp hạn mức nhỏ đối với các tài xế có thâm niên gắn bó > 12 tháng. |
| **Tổng cộng / TB Gia quyền** | **98.442** | **100,00%** | **219,4 đơn** | **112,6 giờ** | **6.338.043** | *(Nếu phân theo hình thức làm việc: Nhóm **Full-time `FT`** đạt **34.969 TX – 35,52% MAU**, năng suất **451,8 đơn/tháng**, thu nhập TB **12.652.078 VNĐ/tháng**).* |

---

### PHẦN 2. PHẢN HỒI CỦA AHAMOVE VỀ QUY TRÌNH THỰC HIỆN (MỤC 2.1 & 2.2)

#### 2.1. Về Quy trình Vay / Phát hành Thẻ tín dụng
👉 **Ahamove thống nhất lựa chọn Phương án 1 (Điều hướng sang luồng đăng ký Webview do SVFC xây dựng ngay trên App AhaDriver), kết hợp truyền dữ liệu tự động qua API (API Pre-fill):**
*   **Lý do lựa chọn:**
    1.  **Tối ưu tốc độ triển khai (Time-to-Market):** Giảm thiểu thời gian phát triển Native UI và không bị phụ thuộc vào chu kỳ duyệt bản cập nhật của App Store / Google Play khi SVFC cần điều chỉnh biểu mẫu, điều khoản hay chương trình ưu đãi.
    2.  **Chuẩn hóa Pháp lý & Bảo mật:** Toàn bộ bước xác thực eKYC, đối chiếu VNeID/CCCD và ký Hợp đồng tín dụng được thực hiện trực tiếp trên hệ thống đạt chuẩn bảo mật của SVFC.
    3.  **Tối ưu Trải nghiệm Tài xế (Auto-fill UX):** Khi tài xế bấm đăng ký trên App AhaDriver và xác nhận đồng ý chia sẻ dữ liệu (e-Consent), Ahamove sẽ truyền ngầm qua API các thông tin định danh và chấm điểm (`Driver ID`, Họ tên, SĐT, CCCD, Hạng tài xế `SC/CN/BC`, Thâm niên, Thu nhập bình quân) sang SVFC để **tự động điền sẵn (Pre-fill)** trên Webview, giúp tài xế hoàn tất hồ sơ chỉ trong 2 – 3 phút.

#### 2.2. Về Quy trình Trả nợ (Thu hộ qua Ví Tài xế)
👉 **Ahamove đề xuất lựa chọn `Op 2` (SVFC API Daily $\rightarrow$ Ahamove giữ lại trên Ví tài xế theo chu kỳ 01 tuần dựa trên Practice hiện tại $\rightarrow$ Thanh toán cho SVFC vào ngày thanh toán định kỳ) và tối ưu hóa như sau:**
*   **Lý do không chọn `Op 1` (Giữ tiền trên Ví 01 tháng):**
    *   Đặc thù của tài xế công nghệ là cần dòng tiền mặt luân chuyển hàng ngày/hàng tuần để chi trả xăng xe, sinh hoạt phí và ứng tiền mặt (COD) cho các đơn hàng giao nhận. Việc giữ tiền trên Ví kéo dài 01 tháng sẽ gây áp lực thanh khoản lớn cho tài xế, dễ dẫn đến tâm lý ngừng nhận đơn hoặc chuyển sang nền tảng khác vào cuối tháng, làm tăng rủi ro cho cả Ahamove và SVFC.
*   **Cơ chế vận hành hiệu quả & cân đối nhất theo `Op 2` (Chu kỳ 01 tuần):**
    1.  **Tương thích 100% với hạ tầng đối soát hiện tại của Ahamove:** Hiện tại Ahamove đang thực hiện đối soát và thanh toán tiền thưởng/ví theo chu kỳ hàng tuần. Việc giữ tiền trong khung 01 tuần hoàn toàn khớp với luồng dòng tiền hiện hữu.
    2.  **Định lượng ngưỡng an toàn (`...%` trong đề xuất của SVFC):**
        *   Với nhóm khách hàng mục tiêu `SC` và `CN` (thu nhập bình quân từ **10,6 – 16,0 triệu VNĐ/tháng**, tương đương **~2,6 – 4,0 triệu VNĐ/tuần**), khoản trả góp hàng tháng cho gói vay 10 – 30 triệu VNĐ chỉ rơi vào khoảng **1,0 – 2,0 triệu VNĐ/tháng**.
        *   Do đó, Ahamove đề xuất quy định: **"Số tiền phải trả hàng tháng cho SVFC không vượt quá `70%` số tiền bình quân được thanh toán định kỳ hàng tuần của tài xế (tương đương không vượt quá `18% – 20%` thu nhập hàng tháng)"**.
    3.  **Linh hoạt kỹ thuật để bảo đảm tỷ lệ thu hồi nợ tối đa cho SVFC:**
        *   **Phương thức chuẩn (Theo tuần đến hạn):** Trong vòng **07 ngày trước ngày thanh toán định kỳ** (`01, 05, 10, 16` hoặc ngày đến hạn sao kê), SVFC gửi yêu cầu thu hộ qua API Daily; hệ thống Ví Ahamove sẽ tự động giữ lại (Hold) số tiền cần thanh toán từ doanh thu ví/thưởng tuần đó của tài xế để chuyển trả SVFC.
        *   **Phương thức nâng cao (Chia nhỏ tích lũy hàng tuần - Weekly Micro-withholding):** Để giảm nhẹ hơn nữa áp lực trả nợ một lần trong tháng, hai bên có thể cấu hình tự động giữ lại **25% nghĩa vụ trả nợ tháng vào mỗi tuần** (4 tuần/tháng) hoặc khấu trừ một tỷ lệ nhỏ trên doanh thu ví hàng ngày cho đến khi đủ số tiền kỳ hạn của tháng đó.

---

Ahamove gửi đính kèm file Excel tổng hợp chi tiết (**`svfc_ahamove_summary.xlsx`**) bao gồm đầy đủ bảng phản hồi và số liệu phân tích theo từng tháng (T08 – T11/2026) tại cả TP.HCM và Hà Nội.

Rất mong nhận được phản hồi từ đội ngũ SVFC để hai bên tiến hành bước thống nhất tài liệu đặc tả kỹ thuật API (API Specification) cho luồng **Phương án 1 (Mục 2.1)** và **Op 2 (Mục 2.2)**.

Trân trọng,
**[Tên của bạn]**
**[Chức danh / Bộ phận — Ahamove]**
