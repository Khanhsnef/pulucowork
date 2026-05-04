# Claude AI — Hướng Dẫn Toàn Diện Cho Team
> **Dành cho:** Thành viên team chưa từng dùng AI / Claude
> **Mục tiêu:** Hiểu Claude là gì, dùng được ngay, áp dụng vào công việc thực tế
> **Cập nhật:** 2026-05-04

---

## MỤC LỤC

1. [AI là gì? Giải thích không cần kỹ thuật](#1-ai-là-gì)
2. [Claude là ai? Anthropic là ai?](#2-claude-là-ai)
3. [Claude hoạt động như thế nào?](#3-nguyên-lý-hoạt-động)
4. [Các nền tảng Claude — Dùng ở đâu, khác gì nhau?](#4-các-nền-tảng-claude)
5. [Bắt đầu dùng Claude — Step by step](#5-bắt-đầu-dùng-claude)
6. [Cách viết lệnh hiệu quả (Prompt)](#6-cách-viết-prompt)
7. [Áp dụng vào công việc thực tế](#7-áp-dụng-vào-công-việc)
8. [Những điều Claude KHÔNG làm được](#8-giới-hạn-của-claude)
9. [Bảo mật & Lưu ý quan trọng](#9-bảo-mật--lưu-ý)
10. [Từ điển thuật ngữ](#10-từ-điển-thuật-ngữ)

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

## 4. Các Nền Tảng Claude

Claude không chỉ có một cách dùng — có nhiều "cửa vào" khác nhau, phù hợp với nhu cầu khác nhau. Phần này giải thích rõ từng nền tảng để bạn chọn đúng công cụ cho đúng việc.

---

### Bản đồ tổng quan

```
CLAUDE CÓ THỂ DÙNG QUA:
│
├── 🌐 claude.ai          → Trình duyệt web (ai cũng dùng được, không cài gì)
├── 🖥️  Claude Desktop     → App cài trên máy Mac/Windows
├── 💻  Claude Code        → Công cụ cho lập trình viên (chạy trong terminal)
│       ├── CLI (terminal)
│       ├── Web: claude.ai/code
│       └── IDE Extension (VS Code, JetBrains)
└── 🏢  Cowork            → Môi trường làm việc đầy đủ xây trên Claude Code
```

---

### 🌐 Claude.ai (Web)

**Là gì:** Trang web tại **claude.ai** — cách đơn giản nhất để dùng Claude.

**Cách truy cập:** Mở trình duyệt → gõ claude.ai → đăng nhập

**Ai nên dùng:** Tất cả mọi người, đặc biệt người mới bắt đầu.

**Làm được gì:**
- Chat hỏi đáp, viết văn bản, phân tích
- Upload file (PDF, Word, Excel, ảnh) để Claude đọc
- Tạo **Projects** (workspace) để lưu ngữ cảnh tái sử dụng
- Dùng trên mọi thiết bị: laptop, điện thoại, máy tính bảng

**Giới hạn:** Chỉ là chat — không thể tự động hóa, không kết nối sâu với email/lịch, không thao tác file trên máy bạn.

---

### 🖥️ Claude Desktop (App máy tính)

**Là gì:** Ứng dụng cài đặt trên máy tính (Mac hoặc Windows), giao diện giống claude.ai nhưng chạy như một app riêng.

**Cách truy cập:** Tải về tại claude.ai/download → cài đặt → đăng nhập

**Khác gì claude.ai web?**

| Tiêu chí | Claude.ai Web | Claude Desktop |
|---|---|---|
| Cần mở trình duyệt | ✅ Có | ❌ Không (app độc lập) |
| Giao diện | Giống nhau | Giống nhau |
| Tính năng | Như nhau | Như nhau + tích hợp MCP |
| Offline | ❌ Không | ❌ Không (vẫn cần internet) |
| **MCP Tools** | ❌ Không | ✅ Có thể cài thêm |

> **MCP (Model Context Protocol)** = Chuẩn kết nối cho phép Claude "với tay" sang các app khác: Google Calendar, Gmail, Notion, Slack... Desktop cho phép cài thêm các kết nối này, còn web thì không.

**Ai nên dùng:** Người dùng thường xuyên, muốn Claude là app riêng không lẫn với các tab trình duyệt.

---

### 💻 Claude Code (Dành cho lập trình & công việc chuyên sâu)

**Là gì:** Phiên bản Claude chạy **trong terminal (cửa sổ dòng lệnh)** của máy tính — không phải chat web thông thường.

**Khác biệt lớn nhất so với claude.ai:**

| claude.ai / Desktop | Claude Code |
|---|---|
| Chat qua giao diện web/app | Chạy trực tiếp trong máy tính |
| Claude chỉ trả lời văn bản | Claude **thao tác được file thật** trên máy bạn |
| Không tự chạy lệnh | Tự chạy lệnh, viết code, đọc/sửa file |
| Không nhớ project qua session | Nhớ toàn bộ codebase/project |
| Dùng tay, từng câu | Có thể chạy task dài tự động |

**Ví dụ Claude Code làm được mà claude.ai không làm được:**
- Đọc toàn bộ thư mục file báo cáo của bạn → tổng hợp thành 1 file duy nhất
- Tự động tạo file Excel từ dữ liệu bạn cung cấp → lưu thẳng vào máy
- Chạy script xử lý 1000 dòng CSV mà không cần bạn copy-paste từng phần

**Ai nên dùng:** Developer, data analyst, hoặc người dùng nâng cao muốn tự động hóa công việc.

**Claude Code có thể dùng qua 3 cách:**
1. **CLI** — Gõ lệnh `claude` trong terminal (mạnh nhất)
2. **claude.ai/code** — Giao diện web của Claude Code
3. **IDE Extension** — Tích hợp thẳng vào VS Code hoặc JetBrains (cho developer)

---

### 🏢 Cowork — Môi Trường Làm Việc Đầy Đủ

**Là gì:** Cowork là một **bộ cấu hình và mở rộng** xây trên nền Claude Code, biến Claude từ "chatbot thông minh" thành một **trợ lý làm việc thực thụ** được kết nối với toàn bộ công cụ văn phòng.

> Hình dung đơn giản: claude.ai = xe máy đi được. Cowork = xe máy đã được lắp thêm GPS, hộp chứa đồ, kết nối Bluetooth, camera hành trình, tích hợp app giao hàng — cùng một "động cơ" nhưng mạnh hơn nhiều.

#### Cowork có gì thêm so với Claude thông thường?

| Tính năng | claude.ai | Claude Desktop | Cowork |
|---|---|---|---|
| Chat hỏi đáp | ✅ | ✅ | ✅ |
| Đọc/viết file trên máy | ❌ | ❌ | ✅ |
| Kết nối Gmail | ❌ | Có thể | ✅ |
| Kết nối Google Calendar | ❌ | Có thể | ✅ |
| Kết nối Google Drive | ❌ | Có thể | ✅ |
| Kết nối NotebookLM | ❌ | ❌ | ✅ |
| **Memory** (nhớ qua session) | ❌ | ❌ | ✅ |
| **Skills** (lệnh tắt chuyên dụng) | ❌ | ❌ | ✅ |
| Cấu hình theo công ty/team | Giới hạn | Giới hạn | ✅ |
| Chạy task tự động (cron/schedule) | ❌ | ❌ | ✅ |

#### Memory trong Cowork — Claude "nhớ" bạn

Khi dùng Cowork, Claude có hệ thống **memory file** — mỗi lần làm việc, Claude học thêm về bạn, lưu lại:
- Bạn là ai, làm gì, cần gì
- Feedback và sở thích làm việc
- Các dự án đang chạy
- Nguồn tài liệu tham khảo

→ Lần sau mở lại, Claude không cần bạn giải thích lại từ đầu.

#### Skills trong Cowork — Lệnh tắt thông minh

**Skills** là các "lệnh chuyên dụng" được lập trình sẵn để làm những việc phức tạp với 1 lệnh ngắn. Gõ `/tên-skill` là Claude tự biết cần làm gì.

Ví dụ các skill đang có trong Cowork của Khanh:

| Skill | Lệnh | Làm gì |
|---|---|---|
| **xlsx** | `/xlsx` | Tạo/sửa file Excel chuyên nghiệp |
| **pptx** | `/pptx` | Tạo slide PowerPoint |
| **html** | `/html` | Tạo báo cáo HTML đẹp |
| **pdf** | `/pdf` | Đọc, tạo, ghép file PDF |
| **md** | `/md` | Viết tài liệu Markdown chuẩn |
| **okr** | `/okr` | Xây OKR theo chuẩn |
| **plan** | `/plan` | Lập kế hoạch task phức tạp |
| **schedule** | `/schedule` | Đặt lịch chạy task tự động |

---

### 🗂️ Projects / Workspace trong claude.ai

Bên trong claude.ai, bạn có thể tạo **Projects** (trước đây gọi là Workspaces) — một không gian riêng cho từng mảng công việc.

**Project cho phép:**
- Đặt **System Prompt** cố định (ví dụ: "Luôn trả lời tiếng Việt, ngắn gọn")
- Upload **tài liệu nền** (SOP, brand guide, data) để Claude dùng làm tham chiếu
- Tất cả hội thoại trong Project đều kế thừa ngữ cảnh đó

**Ví dụ dùng thực tế:**
```
Project "Driver Ops" → Upload SOP vận hành, quy trình xử lý khiếu nại
→ Mọi câu hỏi trong project này, Claude tự dùng SOP đó để trả lời
→ Không cần paste lại SOP mỗi lần hỏi
```

#### Projects vs Cowork — Khác gì?

| Tiêu chí | Projects (claude.ai) | Cowork |
|---|---|---|
| **Bản chất** | Không gian chat có ngữ cảnh cố định | Môi trường làm việc tích hợp đầy đủ |
| **Memory** | Trong project đó thôi | Xuyên suốt mọi session |
| **Tools** | Chỉ chat + upload file | Kết nối Gmail, Calendar, Drive, tự động hóa |
| **Skills** | Không có | Có sẵn hàng chục skill |
| **Tự động hóa** | Không | Có (schedule, cron) |
| **Thao tác file** | Claude đọc file bạn upload | Claude đọc/ghi file thẳng trên máy bạn |
| **Độ phức tạp** | Đơn giản, dùng ngay | Cần setup, nhưng mạnh hơn nhiều |

> **Tóm lại:** Projects là **nâng cấp nhỏ** của claude.ai thông thường. Cowork là **bước nhảy vọt** — từ chatbot thành trợ lý làm việc tích hợp thực sự.

---

### Chọn nền tảng nào?

```
Tôi mới dùng lần đầu
→ claude.ai (web) ✅

Tôi dùng Claude mỗi ngày, muốn app riêng
→ Claude Desktop ✅

Tôi có nhiều chủ đề/mảng công việc khác nhau, muốn lưu context
→ claude.ai + Projects ✅

Tôi là developer hoặc muốn Claude thao tác file trực tiếp trên máy
→ Claude Code (CLI) ✅

Tôi muốn Claude kết nối Gmail/Calendar/Drive, nhớ tôi, chạy task tự động
→ Cowork ✅ (yêu cầu setup — liên hệ Khanh để được hướng dẫn)
```

---

## 5. Bắt Đầu Dùng Claude

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

## 6. Cách Viết Prompt

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

## 7. Áp Dụng Vào Công Việc

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

## 8. Giới Hạn Của Claude

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

## 9. Bảo Mật & Lưu Ý

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

## 10. Từ Điển Thuật Ngữ

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
| **Claude Code** | Phiên bản Claude chạy trực tiếp trong terminal/IDE, có thể đọc/ghi file thật trên máy tính, thao tác codebase |
| **Claude Desktop** | App cài đặt trên máy Mac/Windows, giao diện như claude.ai nhưng hỗ trợ kết nối MCP |
| **Cowork** | Môi trường làm việc đầy đủ xây trên Claude Code — có Memory, Skills, kết nối Gmail/Calendar/Drive |
| **Projects (Workspace)** | Không gian làm việc trong claude.ai — lưu system prompt và tài liệu nền để dùng lại nhiều lần |
| **MCP (Model Context Protocol)** | Chuẩn kết nối cho phép Claude "với tay" sang app khác: Google Workspace, Notion, Slack... |
| **Skills** | Lệnh tắt chuyên dụng trong Cowork — gõ `/tên-skill` để Claude thực hiện task phức tạp theo quy trình định sẵn |
| **Memory** | Hệ thống lưu trữ thông tin qua nhiều session trong Cowork — Claude nhớ bạn là ai, sở thích, dự án đang chạy |
| **Anthropic** | Công ty tạo ra Claude, thành lập 2021 tại Mỹ, tập trung vào AI an toàn |
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
