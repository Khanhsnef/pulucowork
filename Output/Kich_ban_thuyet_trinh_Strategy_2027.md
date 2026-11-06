# 🎤 Kịch bản Thuyết trình – Plan Strategy 2027: Chuyên biệt hóa Tài xế & Moat Vận hành

> **Thời lượng:** ~15 phút trình bày + 5 phút Q&A · **Đối tượng:** Leadership, QM, Product, Legal, SnP
> **Thông điệp xuyên suốt:** *Năng lực tài xế → Moat nhìn thấy được → Nới COD có kiểm soát → Nền chấm điểm tài chính giữ chân tài xế.*

---

# PHẦN 0 · MỞ ĐẦU (1 phút)

**🎯 Câu mở – đi thẳng vào kết luận:**

> "Hôm nay tôi chỉ xin một quyết định: **cho phép chạy pilot 3 việc liên kết nhau trong 2027** – phân tầng tài xế theo năng lực, nới COD Balance cho SC/CN, và đưa hạn mức tín dụng ứng COD vào app – với **vốn trực tiếp của Ahamove gần như bằng 0**."

**Ba ý khóa để khán giả nhớ:**
1. Chúng ta đang **mất GSV** vì tài xế giỏi bị giới hạn COD thấp.
2. Chúng ta đang **gánh rủi ro** vì tài xế yếu vẫn nhận được đơn COD cao.
3. Một giải pháp duy nhất xử lý cả hai, và biến thành **lợi thế thương hiệu**.

➡️ *Chuyển ý:* "Để thấy vì sao, tôi bắt đầu từ vấn đề."

---

# PHẦN 1 · BỐI CẢNH & VẤN ĐỀ (2 phút) – *Slide: Bối cảnh*

**Thoại gợi ý:**

> "Ahamove đang xếp tài xế theo 4 bậc: **SC, CN, BC, CXH**. Nhưng bậc này chỉ phản ánh *mức độ hoạt động chung*, chưa nói được tài xế đó **chở được hàng cồng kềnh không, giữ được tiền COD lớn không**."

**Ba vướng mắc – nói theo nhịp "hệ quả hai chiều":**

| Vấn đề | Hệ quả | Câu nhấn |
| :--- | :--- | :--- |
| COD Balance áp dụng chung | SC/CN tốt bị chặn → **mất GSV**; tài xế highrisk vẫn nhận đơn cao → **rủi ro chiếm dụng vốn** | "Chặn nhầm người tốt, thả nhầm người xấu." |
| Không có kênh tài chính trong ngày | Tài xế tự xoay tiền → ảnh hưởng **Remain rate** | "Tài xế phải ứng tiền túi cho đơn của khách." |
| Thương hiệu không thể hiện thế mạnh | Khách không biết mạng lưới mạnh bulky/COD cao | "Chúng ta mạnh thật, nhưng khách không nhìn thấy." |

**Câu chốt phần:**
> "Ba vướng mắc này thực ra là **một bài toán**: biến năng lực tài xế thành thứ đo được, nhìn thấy được và dùng được."

➡️ *Chuyển ý:* "Bước đầu tiên là định nghĩa năng lực."

---

# PHẦN 2 · CHIẾN LƯỢC CHUYÊN BIỆT HÓA (3 phút) – *Slide: Moat*

**Thoại gợi ý:**

> "Thay vì một con số sao chung chung như đa số nền tảng, chúng ta đo tài xế theo **3 trục không chồng nhau**."

**Giải thích 3 trục (mỗi trục 30 giây):**
1. **Bulky & baga** – tài xế có baga, chuyên đơn cồng kềnh → badge *"Tài xế chuyên chở hàng cồng kềnh"*. Đồng thời là nền cho chiến lược lắp baga sắp tới.
2. **Cash-handling** – đủ tin cậy nhận COD cao và `transfer_COD` → badge *"Tài xế xử lý đơn giá trị cao"*. Ngưỡng: COD Balance ≥ 3M, cancellation true rate < 10%, không chiếm dụng COD 3 tháng.
3. **Độ tin cậy vận hành** – ≥ 6 tháng, AR ≥ 95%, FR ≥ 90%. **Không có badge riêng** – là *điều kiện nền*.

> "Nguyên tắc: **không thể giao bulky hay COD cao cho người chưa chứng minh được sự ổn định**."

**Điểm nhấn khác biệt:**
> "Badge hiển thị ngay trên app khách hàng. Khách chọn Ahamove biết mình được **ghép đúng người cho đúng nhu cầu**, thay vì ghép ngẫu nhiên. Đây là điều Grab, Be, Gojek **chưa làm rõ ra giao diện khách hàng**."

**Việc cần làm ngay:** chốt ngưỡng bằng dữ liệu AR/FR/CR thật (Khanh chủ trì, SnP phối hợp) · thiết kế badge cùng Product · ước tính chi phí và nguồn ngân sách baga.

➡️ *Chuyển ý:* "Khi đã đo được năng lực, ta dùng nó để giải bài toán COD."

---

# PHẦN 3 · ỨNG DỤNG 1 – COD BALANCE THEO RANKING (3 phút) – *Slide: COD Balance*

**Bước 1 – Giải thích cơ chế hiện tại (30 giây):**

> "Đơn cần thu hộ giá trị V được giao cho tài xế có COD Balance ≥ V. Nếu không đủ, hệ thống xét Deposit. Tức là khả năng nhận đơn = **max(COD Balance, Deposit)**."

**Bước 2 – Chỉ ra điểm nghẽn thật:**

> "COD Balance biến thiên liên tục: giảm khi nhận đơn, hồi phục khi nộp tiền. Lúc nó xuống thấp mà Deposit không bù được, tài xế SC/CN giỏi **vẫn bị loại khỏi đơn giá trị cao**. Vấn đề không phải thiếu tài xế đạt chuẩn – mà là **hạn mức chưa phản ánh năng lực**."

**Bước 3 – Đề xuất (nói chậm, dùng bảng):**

> **COD Balance = Base Limit × Hệ số lịch sử × Hệ số thời gian hoạt động**

| Ranking | Base Limit | Điều kiện |
| :--- | :--- | :--- |
| **Siêu Cấp** | **10M** | ≥ 3 tháng không vi phạm; ≥ 35 giờ/tuần |
| **Chuyên Nghiệp** | **5M** | ≥ 3 tháng; ≥ 28 giờ/tuần |
| BC / CXH | Giữ nguyên logic QM / theo ký quỹ | – |

**Câu chốt:** "Nới đúng người, giữ chặt đúng người – **có kiểm soát rủi ro, không nới đại trà**."

➡️ *Chuyển ý:* "Còn khi COD Balance tức thời vẫn thấp thì sao? Đó là vai trò của Deposit."

---

# PHẦN 4 · TĂNG DEPOSIT HIỆU DỤNG (3 phút) – *Slide: Deposit*

**Thoại gợi ý:**

> "Hiện Deposit chỉ tăng khi tài xế nộp thêm tiền túi. Đề xuất: **hợp tác một đối tác tín dụng cấp hạn mức ứng COD 5–20 triệu cho tài xế đủ điều kiện**, dùng thay Deposit."

**Kể luồng vận hành như một câu chuyện 4 bước:**
> "Tài xế nhận đơn → rút hạn mức ứng cho người gửi → giao hàng, thu tiền → **ngay trong ngày** nộp Ahamove và trả lại đối tác → hạn mức được giải phóng."

**Vì sao tài xế có lợi – con số gây ấn tượng:**
- Hiện tài xế ứng tiền túi >2M được trả **0,88%** (cod_fee).
- Quy đổi tương đương trần **~321%/năm**.
- Đối tác chỉ cần lãi **30–60%/năm (~0,08–0,16%/ngày)** vẫn có lãi → **tài xế vẫn lãi ròng**.

> "Tức là đối tác có **dư địa định giá rất lớn** – đây là điểm mạnh nhất để đàm phán."

**Phải nói thẳng rủi ro (tạo niềm tin):**
- ⚠️ Chỉ có lợi khi **tất toán trong ngày**; quá 24h cần cơ chế lãi chuẩn/phí trễ hạn rõ ràng.
- ⚠️ Rủi ro "ôm hàng": cấn trừ qua ví tín dụng của đối tác. **Hợp đồng ba bên phải quy định rõ thứ tự ưu tiên** giữa nợ đối tác và COD Ahamove bị mất.

> "Kết quả: Ahamove **chuyển phần lớn rủi ro tín dụng sang đối tác**, chỉ giữ rủi ro vận hành."

**Ước tính tác động:** ΔGSV = đơn transfer_COD bị từ chối do Deposit (2026) × giá trị TB × % tài xế được duyệt. *(Số liệu sẽ được xác thực trước khi QM duyệt.)*

➡️ *Chuyển ý:* "Đối tác này đến từ đâu, và pháp lý ra sao?"

---

# PHẦN 5 · ỨNG DỤNG 2 – GIẢI PHÁP TÀI CHÍNH TRONG NGÀY (2 phút) – *Slide: Tài chính*

**Benchmark thị trường (30 giây):**
- **Grab Partner Cash Advance:** chấm điểm bằng dữ liệu hoạt động nội bộ, hạn mức 500–15.000 SGD, phí xử lý tối đa ~2%, thu hồi tự động hàng tuần.
- **GIMO, Vui App × Visa:** ứng lương, tích hợp payroll – gần Việt Nam nhất nhưng chưa phục vụ lao động tự do.

> "Cả hai đều chấm điểm bằng dữ liệu nền tảng, không dùng CIC. Ahamove **đã có sẵn** dữ liệu AR/FR/CR/thâm niên – chính là 3 trục ta vừa định nghĩa."

**Chọn phương án – bảng so sánh:**

| | **A. Hợp tác phân phối** | **B. Tự vận hành sandbox P2P** |
| :--- | :--- | :--- |
| Tốc độ | **Nhanh, trong 2027** | Chậm: xin phép NHNN (NĐ 94/2025) |
| Giấy phép | Không cần | Cần pháp nhân, hạ tầng, nhân sự tài chính |
| Rủi ro tín dụng | Đối tác chịu | **Ahamove tự chịu** |
| Biên lợi nhuận | Thấp (hoa hồng) | Cao hơn về dài hạn |

> "**Khuyến nghị: Phương án A cho 2027.** B là mục tiêu 2028+, chỉ khi quy mô ứng COD đủ lớn để biện minh chi phí cấp phép."

**Lưu ý pháp lý (nói ngắn):** trần 20%/năm của BLDS chỉ áp dụng cá nhân–cá nhân; tổ chức tín dụng thỏa thuận theo Luật TCTD 2024. Mức % thực tế sẽ xác minh với đối tác. Cần Legal xác nhận việc chia sẻ dữ liệu tài xế (có đồng ý).

➡️ *Chuyển ý:* "Vậy triển khai như thế nào?"

---

# PHẦN 6 · LỘ TRÌNH 2027 (1,5 phút) – *Slide: Roadmap*

> "Ba luồng chạy song song, **cùng một pilot, hai góc nhìn**."

| Quý | Cột mốc quyết định |
| :--- | :--- |
| **Q1** | Chốt 3 trục và ngưỡng; chốt ngưỡng COD; shortlist đối tác; align QM |
| **Q2** | Ra badge; thí điểm baga 1 Mini-Hub (zone 2, nhiều vol TMĐT); **pilot hạn mức 5M** nhóm Siêu Cấp tại 1 city; ký 1 đối tác |
| **Q3** | Đánh giá badge (GSV bulky/COD cao); mở rộng 2–3 Mini-Hub; mở rộng toàn quốc |
| **Q4** | Hạn mức lên **20M** cho nhóm đạt chuẩn; chuẩn hóa chính sách; cân nhắc đối tác thứ 2 / Phương án B |

> "Nguyên tắc: **pilot nhỏ, đo hàng tuần, mở rộng khi tỷ lệ tất toán đúng ngày đạt chuẩn.**"

---

# PHẦN 7 · GIÁ TRỊ & RỦI RO (1,5 phút) – *Slide: Value + Risk*

**Giá trị – BEFORE → AFTER:**
- COD chung → **COD nới theo ranking** → ↑ GSV đơn giá trị cao, ↓ rủi ro từ tài xế highrisk.
- Deposit tiền túi → **hạn mức đối tác 5–20M** → vốn Ahamove ≈ 0.
- Ghép ngẫu nhiên → **badge năng lực** → moat hữu hình so với Grab/Be/Gojek.

**3 nhóm rủi ro không chồng nhau:**
| Nhóm | Rủi ro | Biện pháp |
| :--- | :--- | :--- |
| Vận hành | Gian lận badge/ranking (mượn tài khoản) | Audit định kỳ |
| Tài chính | Default tăng khi mở rộng nhanh | Giới hạn tốc độ pilot; theo dõi risk exposure **theo tuần** |
| Pháp lý/Đối tác | NHNN đổi chính sách; đối tác rút lui | Chọn **≥ 2 đối tác** |

---

# PHẦN 8 · KẾT & ĐỀ NGHỊ QUYẾT ĐỊNH (1 phút)

> "Tóm lại: **một bài toán, ba đòn bẩy** – Badge tạo moat, COD theo ranking mở GSV, hạn mức đối tác giữ chân tài xế mà không tốn vốn."

**🔔 Xin quyết định hôm nay:**
1. ✅ Thông qua khung 3 trục và giao Khanh + SnP chốt ngưỡng số trong Q1.
2. ✅ Cho phép QM review đề xuất COD Balance (SC 10M / CN 5M) và Deposit qua hạn mức đối tác.
3. ✅ Cho phép Legal và BD bắt đầu shortlist 3–5 đối tác tài chính.

> "Cảm ơn mọi người. Tôi sẵn sàng trả lời câu hỏi."

---

# ❓ CHUẨN BỊ Q&A

| Câu hỏi dự kiến | Gợi ý trả lời |
| :--- | :--- |
| *Nới COD có làm tăng rủi ro mất tiền không?* | Chỉ nới cho SC/CN có ≥3 tháng không vi phạm; BC/CXH giữ nguyên; theo dõi risk exposure theo tuần; rủi ro tín dụng chuyển sang đối tác. |
| *Nếu tài xế không nộp tiền thì sao?* | Cấn trừ qua ví tín dụng đối tác; hợp đồng ba bên quy định thứ tự ưu tiên. Rủi ro còn lại = đơn bị ôm × giá trị × xác suất cấn trừ không đủ. |
| *Vì sao tài xế dùng hạn mức đối tác thay vì tiền túi?* | Lãi trong ngày (~0,08–0,16%) thấp hơn 0,88% cod_fee; không cần có sẵn tiền mặt. |
| *Đối tác có chịu lãi thấp như vậy không?* | Trần quy đổi 321%/năm cho dư địa lớn; lãi 30–60%/năm vẫn hấp dẫn; cần xác minh mức thật khi đàm phán. |
| *Sao không tự làm P2P lending?* | Cần sandbox NHNN, pháp nhân, nhân sự tài chính, tự chịu rủi ro. Phương án B là 2028+. |
| *Badge có thật sự tăng GSV?* | Đo ở Q3: GSV đơn bulky/COD cao tại Mini-Hub có badge so với nhóm đối chứng. |
| *Số liệu ΔGSV là bao nhiêu?* | Đang trích xuất đơn bị từ chối do Deposit (2026) tách theo ranking – hoàn tất Q1 trước khi QM duyệt. |
| *Grocery thì sao?* | Có benefits, quyền lợi, công cụ và system quản lý riêng – thiết kế tách biệt khỏi mạng lưới chung. |

---

## 💡 Mẹo trình bày mượt

- **Nói kết luận trước, giải thích sau** (Pyramid Principle) ở mỗi phần.
- **Chậm lại ở 3 con số:** `10M / 5M`, `0,88% ≈ 321%/năm`, `5–20M`.
- Dùng cụm chuyển ý cuối mỗi phần để mạch câu chuyện liền: *vấn đề → năng lực → COD → Deposit → tài chính → lộ trình → quyết định*.
- Mở file HTML ở chế độ toàn màn hình, cuộn theo thanh điều hướng trên cùng ứng với từng phần.
