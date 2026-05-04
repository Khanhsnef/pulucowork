# Claude AI — Hướng Dẫn Toàn Diện Cho Team
> **Dành cho:** Thành viên team chưa từng dùng AI / Claude
> **Mục tiêu:** Hiểu Claude là gì, dùng được ngay, áp dụng vào công việc thực tế
> **Cập nhật:** 2026-05-04

---

## MỤC LỤC

1. [AI là gì? Giải thích không cần kỹ thuật](#1-ai-là-gì)
2. [Claude là ai? Anthropic là ai?](#2-claude-là-ai)
3. [Claude hoạt động như thế nào?](#3-nguyên-lý-hoạt-động)
4. [Bắt đầu dùng Claude — Step by step](#4-bắt-đầu-dùng-claude)
5. [Cách viết lệnh hiệu quả (Prompt)](#5-cách-viết-prompt)
6. [Áp dụng vào công việc thực tế](#6-áp-dụng-vào-công-việc)
7. [Những điều Claude KHÔNG làm được](#7-giới-hạn-của-claude)
8. [Bảo mật & Lưu ý quan trọng](#8-bảo-mật--lưu-ý)
9. [Từ điển thuật ngữ](#9-từ-điển-thuật-ngữ)

---

## 1. AI Là Gì?

### Giải thích đơn giản nhất

Hãy nghĩ AI (Trí tuệ nhân tạo) như một **nhân viên đã đọc gần như toàn bộ internet** — sách, bài báo, code, tài liệu khoa học, Wikipedia, diễn đàn... — rồi học cách **trả lời câu hỏi, viết văn bản, phân tích dữ liệu và lập luận** dựa trên tất cả kiến thức đó.

Khác với phần mềm thông thường (bạn bấm nút → nó làm đúng 1 việc cố định), AI **hiểu ngôn ngữ tự nhiên** — tức là bạn nói chuyện bình thường với nó như nói chuyện với người.

### AI ≠ Robot trong phim

| Điều nhiều người nghĩ | Thực tế |
|---|---|
| AI có ý thức, cảm xúc như người | AI không có ý thức. Nó xử lý văn bản theo xác suất thống kê |
| AI biết hết mọi thứ | AI chỉ biết những gì đã được học. Có thể sai, có thể bịa |
| AI sẽ thay thế toàn bộ con người | AI thay thế **tác vụ**, không thay thế **tư duy & judgement** |
| Phải biết code mới dùng được | Ai cũng dùng được — chỉ cần biết gõ chữ |

---

## 2. Claude Là Ai?

### Anthropic — Công ty tạo ra Claude

**Anthropic** là công ty AI thành lập năm 2021 tại Mỹ, tách ra từ OpenAI (công ty tạo ChatGPT). Anthropic tập trung vào **AI an toàn và đáng tin cậy** — triết lý của họ là tạo ra AI giúp ích cho con người mà không gây hại.

**Claude** là sản phẩm AI chính của Anthropic, ra mắt năm 2023. Hiện tại (2026) đang ở thế hệ **Claude 4**.

### Claude vs ChatGPT — Khác nhau thế nào?

| Tiêu chí | Claude (Anthropic) | ChatGPT (OpenAI) |
|---|---|---|
| **Độ an toàn** | Thiết kế từ đầu với tiêu chí an toàn | Thêm vào sau |
| **Văn phong** | Tự nhiên, có chiều sâu, ít "robot" hơn | Đôi khi cứng, công thức |
| **Lý luận dài** | Rất mạnh — xử lý tài liệu dài tốt | Tốt nhưng đôi khi lạc đề |
| **Code** | Xuất sắc | Xuất sắc |
| **Phân tích** | Mạnh, có xu hướng trung thực về giới hạn | Tốt |
| **Giá** | Free tier / Pro $20/tháng | Free tier / Plus $20/tháng |

> **Tóm lại:** Cả hai đều mạnh. Claude thường được đánh giá cao hơn về **văn bản chuyên sâu, phân tích, và độ trung thực** (Claude hay nói thẳng khi không chắc, thay vì bịa).

---

## 3. Nguyên Lý Hoạt Động

### Claude "nghĩ" như thế nào? (Không cần biết kỹ thuật)

Hãy tưởng tượng Claude như người đã **đọc hàng tỷ câu văn** trong suốt quá trình training (huấn luyện). Từ đó, Claude học được:
- Khi A thì thường tiếp theo là B
- Câu hỏi dạng X thường được trả lời theo cấu trúc Y
- Văn bản tốt trông như thế nào

Khi bạn gõ câu hỏi, Claude **dự đoán từng từ tiếp theo** theo xác suất cao nhất để tạo ra câu trả lời có nghĩa. Không có "não bộ" thật sự — nhưng kết quả tạo ra rất giống với suy nghĩ con người.

### Context Window — "Bộ nhớ làm việc" của Claude

**Context window** là lượng văn bản Claude có thể "nhìn thấy" và xử lý trong 1 lần trò chuyện.

```
Bạn gõ: [Câu hỏi của bạn]
Claude nhìn thấy: [Toàn bộ lịch sử hội thoại từ đầu đến giờ]
→ Trả lời dựa trên TẤT CẢ context đó
```

**Quan trọng:** Khi bạn **tắt tab / mở cuộc trò chuyện mới** → Claude quên hết. Mỗi conversation là một trang giấy trắng mới.

### Claude KHÔNG có khả năng:
- **Nhớ bạn** sau khi đóng hội thoại (trừ khi dùng tính năng Memory)
- **Truy cập internet real-time** (trừ khi được cài tool tìm kiếm)
- **Lưu file vào máy bạn** tự động
- **Tự hành động** mà không có lệnh từ bạn

---

## 4. Bắt Đầu Dùng Claude

### Bước 1 — Tạo tài khoản

1. Vào **claude.ai** (trên trình duyệt bất kỳ)
2. Nhấn **Sign Up**
3. Đăng ký bằng email hoặc Google account
4. Chọn gói **Free** để bắt đầu (đủ dùng cho hầu hết tác vụ)

> **Gói Pro ($20/tháng):** Dùng nhiều hơn, model mạnh hơn (Opus), upload file lớn hơn — cân nhắc nếu dùng hàng ngày cho công việc.

### Bước 2 — Giao diện cơ bản

```
┌─────────────────────────────────────────┐
│  Claude                          [New]  │
│─────────────────────────────────────────│
│                                         │
│  [Danh sách các cuộc hội thoại cũ]      │
│                                         │
│─────────────────────────────────────────│
│                                         │
│         Khu vực trò chuyện              │
│                                         │
│─────────────────────────────────────────│
│  [ Gõ câu hỏi của bạn ở đây...    ] [→]│
└─────────────────────────────────────────┘
```

- **New conversation:** Bắt đầu hội thoại mới (Claude quên hết lịch sử cũ)
- **Ô gõ phía dưới:** Gõ yêu cầu → Enter hoặc nhấn nút gửi
- **Upload file:** Đính kèm PDF, Excel, Word, ảnh để Claude đọc và phân tích

### Bước 3 — Thử ngay

Gõ thử câu này để làm quen:
```
Xin chào! Tôi vừa mới bắt đầu dùng Claude. 
Bạn có thể giới thiệu ngắn gọn bạn có thể 
giúp gì cho tôi trong công việc văn phòng không?
```

---

## 5. Cách Viết Prompt

**Prompt** = Lệnh/câu hỏi bạn gửi cho Claude.

Viết prompt tốt = Claude trả lời đúng ý hơn, tiết kiệm thời gian hơn.

### Công thức COAT (Dễ nhớ)

| Chữ | Ý nghĩa | Ví dụ |
|---|---|---|
| **C**ontext | Bối cảnh là gì | "Tôi là team leader quản lý 5 người..." |
| **O**bjective | Mục tiêu muốn đạt | "...cần viết email từ chối ứng viên..." |
| **A**udience | Đối tượng nhận | "...gửi cho ứng viên đã phỏng vấn..." |
| **T**one/Format | Giọng & định dạng | "...lịch sự, ngắn gọn dưới 100 từ" |

### So sánh Prompt kém vs tốt

**❌ Prompt kém:**
```
viết email
```
→ Claude không biết email về gì, gửi cho ai, mục đích gì

---

**✅ Prompt tốt:**
```
Tôi đang làm HR tại công ty logistics. Viết email 
từ chối lịch sự cho ứng viên vị trí Operations 
Executive sau vòng phỏng vấn. Lý do: ứng viên 
thiếu kinh nghiệm thực tế. Giọng văn chuyên nghiệp, 
ấm áp, không vượt quá 120 từ. Tiếng Việt.
```

---

### Các kỹ thuật prompt phổ biến

**1. Giao vai (Role-playing)**
```
Bạn là chuyên gia phân tích dữ liệu với 10 năm kinh nghiệm. 
Hãy review bảng số liệu này và chỉ ra các điểm bất thường.
```

**2. Cho ví dụ mẫu**
```
Tóm tắt nội dung cuộc họp theo format sau:
- Quyết định: [...]
- Action item: [Ai] làm [gì] trước [ngày]
- Vấn đề còn mở: [...]

Đây là nội dung cuộc họp: [paste nội dung vào]
```

**3. Yêu cầu step-by-step**
```
Giải thích từng bước cách đọc báo cáo P&L cho người mới, 
không dùng thuật ngữ kỹ thuật phức tạp.
```

**4. Phê bình & cải thiện**
```
Đây là email tôi vừa draft. Hãy chỉ ra 3 điểm yếu 
và đề xuất cải thiện cụ thể:
[paste email vào]
```

**5. Hỏi lại khi chưa ưng**
```
Câu trả lời trước quá dài. Rút gọn còn 5 bullet 
point chính, mỗi cái tối đa 1 dòng.
```

> **Mẹo quan trọng:** Claude nhớ toàn bộ hội thoại trong cùng 1 tab. Bạn có thể nói "sửa lại đoạn 2", "thêm ví dụ", "dịch sang tiếng Anh" mà không cần giải thích lại từ đầu.

---

## 6. Áp Dụng Vào Công Việc

### 6.1 Viết lách & Soạn thảo

| Tác vụ | Prompt mẫu |
|---|---|
| Viết email | "Viết email [mục đích] gửi [ai], giọng [chuyên nghiệp/thân thiện], dưới [X] từ" |
| Soạn thông báo nội bộ | "Soạn thông báo cho toàn team về [nội dung], format ngắn gọn dưới 200 từ" |
| Viết JD tuyển dụng | "Viết JD cho vị trí [tên vị trí], yêu cầu [kỹ năng chính], tại [công ty/ngành]" |
| Tóm tắt tài liệu | Upload file PDF/Word + "Tóm tắt tài liệu này thành 5 điểm chính" |

### 6.2 Phân tích & Báo cáo

| Tác vụ | Prompt mẫu |
|---|---|
| Phân tích số liệu | Upload Excel + "Phân tích xu hướng, chỉ ra top 3 insight quan trọng nhất" |
| Root cause analysis | "Dữ liệu: [chỉ số] giảm [X%] trong [khoảng thời gian]. Đề xuất 5 nguyên nhân tiềm ẩn theo thứ tự ưu tiên" |
| Tóm tắt cuộc họp | Paste nội dung meeting + "Tóm tắt theo format: Quyết định / Action item / Vấn đề còn mở" |
| Chuẩn bị slide | "Tạo outline slide presentation về [chủ đề], 10 slides, đối tượng là [ai]" |

### 6.3 Nghiên cứu & Học tập

| Tác vụ | Prompt mẫu |
|---|---|
| Giải thích khái niệm | "Giải thích [khái niệm] đơn giản như tôi chưa biết gì về lĩnh vực này" |
| So sánh lựa chọn | "So sánh [option A] vs [option B] theo tiêu chí: chi phí, thời gian, rủi ro" |
| Brainstorm ý tưởng | "Brainstorm 10 cách để [mục tiêu]. Sáng tạo, không giới hạn" |
| Chuẩn bị câu hỏi phỏng vấn | "Tạo 20 câu hỏi phỏng vấn cho vị trí [tên vị trí], tập trung vào [kỹ năng X]" |

### 6.4 Use Cases Thực Tế Cho Team Driver Management

| Tình huống | Cách dùng Claude |
|---|---|
| Soạn thông báo chính sách mới cho tài xế | "Viết thông báo chính sách [X] bằng ngôn ngữ đơn giản, tài xế dễ hiểu, dưới 150 chữ" |
| Phân tích báo cáo AR/FR tuần | Upload báo cáo + "Tóm tắt và chỉ ra khu vực nào cần ưu tiên can thiệp" |
| Chuẩn bị nội dung họp team weekly | "Tạo agenda họp team ops tuần, dựa trên các vấn đề sau: [list vấn đề]" |
| Viết script training tài xế mới | "Viết script giải thích quy trình [X] cho tài xế mới, dùng ngôn ngữ đơn giản, có ví dụ cụ thể" |
| Phân tích feedback tài xế | Paste feedback + "Phân loại theo chủ đề, chỉ ra top 3 vấn đề được đề cập nhiều nhất" |

---

## 7. Giới Hạn Của Claude

### Claude có thể nói sai — và bạn cần biết điều này

Claude đôi khi **"hallucinate"** (bịa ra thông tin nghe có vẻ đúng nhưng sai). Đặc biệt với:
- Số liệu cụ thể, thống kê (luôn verify)
- Tên người, ngày tháng, sự kiện lịch sử cụ thể
- Thông tin pháp lý, y tế (không dùng thay cho chuyên gia)
- Thông tin mới sau ngày Claude được training (Claude có knowledge cutoff)

**Nguyên tắc vàng:** Claude là **assistant thông minh**, không phải **nguồn sự thật**. Luôn verify thông tin quan trọng.

### Bảng: Nên vs Không nên dùng Claude

| ✅ NÊN dùng Claude | ❌ KHÔNG dùng Claude thay thế |
|---|---|
| Draft văn bản, email, báo cáo | Quyết định chiến lược quan trọng (không verify) |
| Brainstorm ý tưởng | Số liệu tài chính chính xác (phải kiểm tra) |
| Tóm tắt tài liệu dài | Tư vấn pháp lý, y tế |
| Giải thích khái niệm | Thay thế judgement của con người |
| Viết code, công thức | Thông tin real-time (giá cổ phiếu, tin tức hôm nay) |

---

## 8. Bảo Mật & Lưu Ý

### ⚠️ TUYỆT ĐỐI KHÔNG chia sẻ với Claude:

- **Mật khẩu, tài khoản ngân hàng**
- **Thông tin cá nhân nhạy cảm của tài xế/khách hàng** (CMND, SĐT, địa chỉ nhà)
- **Dữ liệu kinh doanh mật** (doanh thu nội bộ, chiến lược chưa công bố)
- **Hợp đồng, thỏa thuận bảo mật**

### Tại sao?

Khi bạn gõ nội dung vào claude.ai, dữ liệu đó được gửi lên server của Anthropic. Mặc dù Anthropic có chính sách bảo mật tốt, nhưng **best practice** là không đưa thông tin nhạy cảm lên bất kỳ nền tảng AI cloud nào.

### Tips an toàn khi dùng cho công việc:

```
❌ Sai: "Phân tích dữ liệu tài xế của Ahamove:
         Nguyễn Văn A - SĐT 0901234567 - AR 45%..."

✅ Đúng: "Phân tích dữ liệu tài xế ẩn danh:
          Tài xế X - AR 45%, tài xế Y - AR 62%...
          Chỉ ra pattern và đề xuất cải thiện."
```

**Anonymize (ẩn danh hóa) trước khi hỏi** — thay tên thật bằng Tài xế A, B, C hoặc dùng ID giả.

---

## 9. Từ Điển Thuật Ngữ

| Thuật ngữ | Giải thích đơn giản |
|---|---|
| **AI (Artificial Intelligence)** | Trí tuệ nhân tạo — phần mềm có khả năng xử lý ngôn ngữ và lý luận |
| **LLM (Large Language Model)** | "Mô hình ngôn ngữ lớn" — loại AI được train trên lượng văn bản khổng lồ. Claude và ChatGPT đều là LLM |
| **Prompt** | Câu lệnh/câu hỏi bạn gửi cho Claude |
| **Context Window** | "Bộ nhớ làm việc" — lượng text Claude xử lý được trong 1 hội thoại |
| **Hallucination** | Khi AI tự bịa ra thông tin sai nhưng trình bày tự tin như thật |
| **Training / Training Data** | Quá trình "học" của AI — đọc hàng tỷ tài liệu để hiểu ngôn ngữ |
| **Knowledge Cutoff** | Ngày Claude ngừng được cập nhật kiến thức mới (sau đó không biết tin tức mới) |
| **Model** | Phiên bản AI cụ thể. Claude có các model: Haiku (nhanh/nhẹ), Sonnet (cân bằng), Opus (mạnh nhất) |
| **Token** | Đơn vị đo văn bản của AI (≈ 3/4 từ tiếng Anh). Giới hạn context window tính bằng token |
| **Agent** | Claude được trang bị thêm tools (tìm kiếm web, đọc file, chạy code) để tự thực hiện tác vụ phức tạp hơn |
| **API** | Cách kết nối Claude vào phần mềm/app khác (dành cho developer) |
| **Claude Code** | Phiên bản Claude chạy trực tiếp trong terminal/IDE, dùng để hỗ trợ lập trình và thao tác file |
| **Anthropic** | Công ty tạo ra Claude |
| **System Prompt** | Lệnh nền được cài sẵn để định hình cách Claude phản hồi (bạn thường không thấy) |

---

## Bắt Đầu Ngay Hôm Nay

### Checklist 15 phút đầu tiên

- [ ] Tạo tài khoản tại **claude.ai**
- [ ] Gửi 1 câu hỏi bất kỳ để làm quen giao diện
- [ ] Thử upload 1 file PDF/Word và hỏi Claude tóm tắt
- [ ] Thử viết 1 email theo COAT formula
- [ ] Hỏi Claude 1 điều bạn đang thắc mắc trong công việc

### Khi nào thì nên hỏi AI vs hỏi đồng nghiệp?

```
Câu hỏi có đáp án rõ ràng, không nhạy cảm → Hỏi Claude trước
Câu hỏi cần judgement, context nội bộ, quyết định → Hỏi đồng nghiệp/quản lý
Câu hỏi quan trọng → Claude draft trước, đồng nghiệp review sau
```

---

*Tài liệu này được soạn bởi Driver Management Team — Ahamove | 2026-05-04*
*Câu hỏi hoặc góp ý: liên hệ Khanh (khanhlp@ahamove.com)*
