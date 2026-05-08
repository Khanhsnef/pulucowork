# Claude AI — Hướng Dẫn Từ Zero Đến Nâng Cao

> **Dành cho:** Thành viên team chưa biết gì về Claude hoặc AI Agent
> **Mục tiêu:** Hiểu rõ cách hoạt động → dùng được ngay → tự cấu hình nâng cao
> **Cập nhật:** 2026-05-08 | Driver Management Team — Ahamove

---

## MỤC LỤC

### PHẦN 1 — NỀN TẢNG (Người mới bắt đầu)

- [AI là gì? Giải thích không cần kỹ thuật](#1-ai-là-gì)
- [Claude là ai? So sánh các AI hiện tại](#2-claude-là-ai)
- [Claude hoạt động như thế nào bên trong?](#3-nguyên-lý-hoạt-động)

### PHẦN 2 — CÁC NỀN TẢNG (Dùng ở đâu, khác gì nhau?)

- [Bản đồ tổng quan các nền tảng Claude](#4-các-nền-tảng-claude)
- [Claude.ai Web — Bắt đầu từ đây](#5-claudeai-web)
- [Claude Desktop — App máy tính](#6-claude-desktop)
- [Claude Code & Cowork — Cấp độ chuyên sâu](#7-claude-code--cowork)

### PHẦN 3 — BẮT ĐẦU THỰC HÀNH (Tạo tài khoản & viết prompt)

- [Tạo tài khoản & giao diện cơ bản](#8-bắt-đầu-dùng-claude)
- [Cách viết Prompt hiệu quả](#9-cách-viết-prompt)
- [Use cases thực tế cho công việc](#10-áp-dụng-vào-công-việc)

### PHẦN 4 — CẤU TRÚC COWORK (Nâng cao)

- [Cowork là gì và tại sao cần?](#11-cowork--cấu-trúc-đầy-đủ)
- [Các file Markdown quan trọng cần tạo](#12-các-markdown-file-quan-trọng)
- [Trình tự Claude Pro hoạt động — từng bước](#13-trình-tự-claude-pro-hoạt-động)
- [Skills — Lệnh tắt thông minh](#14-skills--lệnh-tắt)
- [MCP Tools — Claude kết nối app khác](#15-mcp-tools)

### PHẦN 5 — AN TOÀN & THAM KHẢO (Giới hạn & từ điển)

- [Giới hạn của Claude — Biết để không lạm dụng](#16-giới-hạn-của-claude)
- [Bảo mật & Lưu ý quan trọng](#17-bảo-mật--lưu-ý)
- [Từ điển thuật ngữ](#18-từ-điển-thuật-ngữ)

---

# PHẦN 1 — NỀN TẢNG

## 1. AI Là Gì?

### Giải thích đơn giản nhất

Hãy nghĩ AI như một **nhân viên đã đọc gần như toàn bộ internet** — sách, bài báo, code, Wikipedia, diễn đàn, tài liệu khoa học — rồi học cách **trả lời câu hỏi, viết văn bản, phân tích dữ liệu và lập luận** dựa trên tất cả đó.

Khác với phần mềm thông thường (bạn bấm nút → nó làm đúng 1 việc cố định), AI **hiểu ngôn ngữ tự nhiên** — bạn nói chuyện bình thường với nó như nói chuyện với người.

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

**Anthropic** là công ty AI thành lập 2021 tại Mỹ, tách ra từ OpenAI. Anthropic tập trung vào **AI an toàn và đáng tin cậy**.

**Claude** là sản phẩm AI chính của Anthropic. Hiện tại (2026) đang ở thế hệ **Claude 4** với 3 model:

| Model | Đặc điểm | Khi nào dùng |
|---|---|---|
| **Haiku** | Nhanh, nhẹ, rẻ | Tác vụ đơn giản, lặp nhiều lần |
| **Sonnet** | Cân bằng tốc độ & chất lượng | Công việc hằng ngày (mặc định) |
| **Opus** | Mạnh nhất, chậm hơn | Phân tích phức tạp, chiến lược |

### Claude vs ChatGPT — Khác gì?

| Tiêu chí | Claude (Anthropic) | ChatGPT (OpenAI) |
|---|---|---|
| **Độ trung thực** | Claude hay nói thẳng khi không chắc | Đôi khi trả lời tự tin dù sai |
| **Văn phong** | Tự nhiên, có chiều sâu | Đôi khi cứng, công thức |
| **Tài liệu dài** | Rất mạnh — xử lý ngữ cảnh dài tốt | Tốt nhưng đôi khi lạc đề |
| **Code** | Xuất sắc | Xuất sắc |
| **Giá** | Free / Pro $20/tháng | Free / Plus $20/tháng |

> **Tóm lại:** Claude thường được đánh giá cao hơn về **văn bản chuyên sâu, phân tích, và tính minh bạch** về giới hạn của bản thân.

---

## 3. Nguyên Lý Hoạt Động

### Claude "nghĩ" như thế nào?

```
Quá trình training (học):
  Đọc hàng tỷ tài liệu → học pattern ngôn ngữ
  → Biết "câu A thường được tiếp theo bởi B"
  → Biết "câu hỏi dạng X thường có cấu trúc trả lời Y"

Khi bạn hỏi:
  Bạn gõ câu hỏi
  → Claude dự đoán từng từ tiếp theo theo xác suất cao nhất
  → Kết quả: câu trả lời có nghĩa, giống suy nghĩ người
```

Không có "não bộ" thật sự — nhưng kết quả tạo ra rất giống với tư duy con người vì nó học từ văn bản do con người viết.

### Context Window — "Bộ nhớ làm việc"

**Context window** = lượng văn bản Claude có thể "nhìn thấy" trong 1 lần trò chuyện.

```
Bạn gõ: [Câu hỏi của bạn]
Claude nhìn thấy: [Toàn bộ lịch sử hội thoại từ đầu đến giờ]
→ Trả lời dựa trên TẤT CẢ context đó
```

**Quan trọng:** Khi bạn **đóng tab / mở conversation mới** → Claude quên hết. Mỗi conversation là một trang giấy trắng mới — **trừ khi** dùng Cowork với hệ thống Memory.

### Claude KHÔNG tự động làm được:
- Nhớ bạn sau khi đóng hội thoại (trừ Cowork/Memory)
- Truy cập internet real-time (trừ khi được cài web search tool)
- Lưu file vào máy bạn (trừ Claude Code)
- Tự hành động mà không có lệnh từ bạn

---

# PHẦN 2 — CÁC NỀN TẢNG

## 4. Các Nền Tảng Claude

```
CLAUDE CÓ THỂ DÙNG QUA:
│
├── 🌐 claude.ai (Web)      → Chat trình duyệt — bắt đầu từ đây
├── 🖥️  Claude Desktop       → App cài máy Mac/Windows
├── 💻  Claude Code          → Thao tác file thật, automation
│       ├── CLI (terminal)   → Mạnh nhất
│       ├── claude.ai/code   → Giao diện web của Claude Code
│       └── VS Code / IDE    → Tích hợp IDE cho developer
└── 🏢  Cowork               → Claude Code + Memory + Skills + MCP
```

### Chọn nền tảng nào?

```
❓ Tôi mới dùng lần đầu
   → claude.ai (web) ✅

❓ Tôi dùng hằng ngày, muốn app riêng không lẫn với tab trình duyệt
   → Claude Desktop ✅

❓ Tôi có nhiều chủ đề công việc, muốn lưu context riêng từng mảng
   → claude.ai + Projects ✅

❓ Tôi muốn Claude đọc/ghi file trên máy, chạy script, automation
   → Claude Code (CLI) ✅

❓ Tôi muốn Claude nhớ tôi, kết nối Gmail/Calendar/Drive, chạy task tự động
   → Cowork ✅ (cần setup — liên hệ Khanh)
```

---

## 5. Claude.ai Web

**Truy cập:** Mở trình duyệt → `claude.ai` → đăng nhập

**Làm được gì:**
- Chat hỏi đáp, viết văn bản, phân tích
- Upload file (PDF, Word, Excel, ảnh) để Claude đọc
- Tạo **Projects** — workspace với system prompt & tài liệu cố định
- Dùng mọi thiết bị: laptop, điện thoại, máy tính bảng

**Giới hạn:** Chỉ là chat — không tự động hóa, không thao tác file trên máy bạn.

### Projects trong claude.ai

**Project** = không gian riêng cho từng mảng công việc.

**Cho phép:**
- Đặt **System Prompt** cố định: "Luôn trả lời tiếng Việt, ngắn gọn..."
- Upload **tài liệu nền** (SOP, brand guide, data) → Claude dùng làm tham chiếu mọi lúc
- Tất cả hội thoại trong Project đều kế thừa ngữ cảnh đó

**Ví dụ thực tế:**
```
Project "Driver Ops"
→ Upload: SOP vận hành, quy trình xử lý khiếu nại, bảng KPI
→ Mọi câu hỏi trong project → Claude tự dùng các tài liệu đó trả lời
→ Không cần paste lại SOP mỗi lần hỏi
```

---

## 6. Claude Desktop

**Tải về:** `claude.ai/download` → cài đặt → đăng nhập

| Tiêu chí | Claude.ai Web | Claude Desktop |
|---|---|---|
| Cần mở trình duyệt | ✅ Có | ❌ Không (app độc lập) |
| Giao diện | Giống nhau | Giống nhau |
| Tính năng | Như nhau | Như nhau |
| **MCP Tools** | ❌ Không | ✅ Có thể cài thêm |

> **MCP (Model Context Protocol)** = Chuẩn kết nối cho phép Claude kết nối sang app khác: Google Calendar, Gmail, Notion, Slack... Desktop hỗ trợ cài MCP, web thì không.

---

## 7. Claude Code & Cowork

### Claude Code — Khác gì so với claude.ai?

| claude.ai / Desktop | Claude Code |
|---|---|
| Chat qua giao diện web/app | Chạy trực tiếp trong máy tính (terminal) |
| Claude chỉ trả lời văn bản | Claude **thao tác được file thật** trên máy |
| Không tự chạy lệnh | Tự chạy lệnh, viết code, đọc/sửa file |
| Không nhớ project qua session | Nhớ toàn bộ codebase/thư mục làm việc |
| Dùng tay, từng câu | Có thể chạy task dài tự động |

**Claude Code làm được mà claude.ai KHÔNG làm được:**
- Đọc toàn bộ thư mục file → tổng hợp thành 1 file duy nhất
- Tạo file Excel từ dữ liệu → lưu thẳng vào máy
- Chạy script xử lý 1000 dòng CSV không cần copy-paste từng phần
- Kết nối Gmail → đọc, tóm tắt, soạn draft email

**Claude Code dùng qua 3 cách:**
1. **CLI** — Gõ lệnh `claude` trong terminal (mạnh nhất)
2. **claude.ai/code** — Giao diện web
3. **IDE Extension** — Tích hợp VS Code / JetBrains

---

# PHẦN 3 — BẮT ĐẦU THỰC HÀNH

## 8. Bắt Đầu Dùng Claude

### Bước 1 — Tạo tài khoản

1. Vào **claude.ai** trên trình duyệt bất kỳ
2. Nhấn **Sign Up**
3. Đăng ký bằng email hoặc Google account
4. Chọn gói **Free** để bắt đầu

> **Gói Pro ($20/tháng):** Dùng nhiều hơn, model mạnh hơn (Opus), upload file lớn hơn — nên nâng cấp nếu dùng hằng ngày cho công việc.

### Bước 2 — Giao diện cơ bản

```
┌──────────────────────────────────────────┐
│  Claude                          [+ New] │
│──────────────────────────────────────────│
│  [Danh sách hội thoại cũ]                │
│  [Projects của bạn]                      │
│──────────────────────────────────────────│
│                                          │
│         Khu vực trò chuyện               │
│                                          │
│──────────────────────────────────────────│
│  [📎] [ Gõ câu hỏi của bạn ở đây... ][→]│
└──────────────────────────────────────────┘
```

- **+ New:** Bắt đầu hội thoại mới (Claude quên hết lịch sử cũ)
- **📎 (đính kèm):** Upload PDF, Excel, Word, ảnh để Claude đọc
- **Ô gõ phía dưới:** Gõ yêu cầu → Enter hoặc nhấn nút gửi

### Bước 3 — Thử ngay (5 phút)

```
Gõ thử: "Xin chào! Tôi làm trong lĩnh vực logistics, 
quản lý tài xế giao hàng. Bạn có thể giúp gì cho 
tôi trong công việc hằng ngày không?"
```

---

## 9. Cách Viết Prompt

**Prompt** = Lệnh/câu hỏi bạn gửi cho Claude. Viết tốt → Claude trả lời đúng ý, tiết kiệm thời gian.

### Công thức COAT

| Chữ | Ý nghĩa | Ví dụ |
|---|---|---|
| **C**ontext | Bối cảnh là gì | "Tôi là team leader quản lý 50 tài xế..." |
| **O**bjective | Mục tiêu muốn đạt | "...cần viết email thông báo chính sách mới..." |
| **A**udience | Đối tượng nhận | "...gửi cho tài xế ít học, đọc trên điện thoại..." |
| **T**one/Format | Giọng & định dạng | "...ngắn gọn, dễ hiểu, dưới 100 chữ, tiếng Việt" |

### So sánh Prompt kém vs tốt

**❌ Prompt kém:**
```
viết email
```

**✅ Prompt tốt:**
```
Tôi đang quản lý đội tài xế giao hàng tại TP.HCM.
Viết email thông báo thay đổi chính sách bonus tháng 6:
- Bonus tăng 10% nếu AR ≥ 90%
- Trừ tiền nếu hủy đơn quá 3 lần/tuần
Đối tượng: tài xế, đọc trên điện thoại.
Ngôn ngữ: đơn giản, thân thiện, dưới 120 từ.
```

### Kỹ thuật prompt phổ biến

**1. Giao vai (Role-playing)**
```
Bạn là chuyên gia phân tích dữ liệu vận hành logistics.
Hãy review bảng số liệu này và chỉ ra các điểm bất thường.
```

**2. Cho ví dụ mẫu (Few-shot)**
```
Tóm tắt cuộc họp theo format sau:
- Quyết định: [...]
- Action item: [Ai] làm [gì] trước [ngày]
- Vấn đề còn mở: [...]

Nội dung cuộc họp: [paste vào đây]
```

**3. Yêu cầu step-by-step**
```
Giải thích từng bước cách đọc báo cáo AR/FR 
cho người mới, không dùng thuật ngữ kỹ thuật.
```

**4. Phê bình & cải thiện**
```
Đây là script training tôi vừa viết.
Hãy chỉ ra 3 điểm yếu và đề xuất cải thiện cụ thể:
[paste nội dung vào]
```

**5. Điều chỉnh khi chưa ưng**
```
Câu trả lời trước quá dài. Rút gọn còn 5 bullet point,
mỗi cái tối đa 1 dòng.
```

> **Mẹo:** Claude nhớ toàn bộ hội thoại trong cùng 1 tab. Bạn có thể nói "sửa lại đoạn 2", "thêm ví dụ", "dịch sang tiếng Anh" mà không cần giải thích lại từ đầu.

---

## 10. Áp Dụng Vào Công Việc

### Viết lách & Soạn thảo

| Tác vụ | Prompt mẫu |
|---|---|
| Email | "Viết email [mục đích] gửi [ai], giọng [X], dưới [N] từ" |
| Thông báo nội bộ | "Soạn thông báo về [nội dung], format ngắn dưới 200 từ" |
| JD tuyển dụng | "Viết JD vị trí [tên], yêu cầu [kỹ năng chính], công ty logistics" |
| Tóm tắt tài liệu | Upload PDF/Word + "Tóm tắt thành 5 điểm chính" |

### Phân tích & Báo cáo

| Tác vụ | Prompt mẫu |
|---|---|
| Phân tích số liệu | Upload Excel + "Phân tích xu hướng, top 3 insight quan trọng nhất" |
| Root cause | "[Chỉ số] giảm [X%] trong [thời gian]. Đề xuất 5 nguyên nhân theo thứ tự ưu tiên" |
| Tóm tắt họp | Paste nội dung + "Tóm tắt: Quyết định / Action item / Vấn đề còn mở" |
| Chuẩn bị slide | "Tạo outline slide về [chủ đề], 10 slides, đối tượng [ai]" |

### Use Cases thực tế — Driver Management

| Tình huống | Cách dùng Claude |
|---|---|
| Thông báo chính sách mới cho tài xế | "Viết thông báo [chính sách X] bằng ngôn ngữ đơn giản, tài xế dễ hiểu, dưới 150 chữ" |
| Phân tích báo cáo AR/FR tuần | Upload báo cáo + "Tóm tắt, chỉ ra khu vực nào cần ưu tiên can thiệp" |
| Agenda họp team weekly | "Tạo agenda họp ops tuần, dựa trên các vấn đề: [list]" |
| Script training tài xế mới | "Viết script giải thích [quy trình X] cho tài xế mới, có ví dụ cụ thể" |
| Phân tích feedback tài xế | Paste feedback + "Phân loại theo chủ đề, top 3 vấn đề phổ biến nhất" |

---

# PHẦN 4 — CẤU TRÚC COWORK (NÂNG CAO)

## 11. Cowork — Cấu Trúc Đầy Đủ

### Cowork là gì?

**Cowork** = Claude Code + Memory + Skills + MCP Tools — biến Claude từ "chatbot thông minh" thành **trợ lý làm việc tích hợp thực thụ**.

> Hình dung: `claude.ai` = xe máy đi được.  
> `Cowork` = xe máy đã lắp thêm GPS, hộp đồ, kết nối Bluetooth, camera — cùng động cơ nhưng mạnh hơn nhiều.

### So sánh đầy đủ các nền tảng

| Tính năng | claude.ai | Projects | Claude Desktop | Cowork |
|---|---|---|---|---|
| Chat hỏi đáp | ✅ | ✅ | ✅ | ✅ |
| Upload file để đọc | ✅ | ✅ | ✅ | ✅ |
| Context cố định qua session | ❌ | ✅ (trong project) | ❌ | ✅ (Memory) |
| Đọc/ghi file thật trên máy | ❌ | ❌ | ❌ | ✅ |
| Kết nối Gmail | ❌ | ❌ | Có thể | ✅ |
| Kết nối Google Calendar | ❌ | ❌ | Có thể | ✅ |
| Kết nối Google Drive | ❌ | ❌ | Có thể | ✅ |
| **Memory** (nhớ qua session) | ❌ | ❌ | ❌ | ✅ |
| **Skills** (lệnh tắt) | ❌ | ❌ | ❌ | ✅ |
| Chạy task tự động (schedule) | ❌ | ❌ | ❌ | ✅ |

---

## 12. Các Markdown File Quan Trọng

Đây là phần **khác biệt lớn nhất** của Cowork so với claude.ai. Cowork hoạt động dựa trên một hệ thống **file văn bản** (.md = Markdown) mà Claude đọc mỗi khi bắt đầu session.

### Tổng quan cấu trúc thư mục Cowork

```
Desktop/Cowork/
│
├── CLAUDE.md                    ← ⭐ File quan trọng nhất — "Bản tóm tắt công ty & quy tắc"
│
├── .claude/
│   ├── settings.json            ← Cài đặt permissions, hooks, tools
│   └── commands/                ← Định nghĩa các skill tùy chỉnh
│
├── memory/
│   ├── MEMORY.md                ← ⭐ Index — Danh sách tất cả memory files
│   ├── user_profile.md          ← Bạn là ai, làm gì, mục tiêu
│   ├── user_rules.md            ← Cách Claude nên làm việc với bạn
│   ├── user_voice.md            ← Giọng văn, format ưa thích
│   ├── feedback_*.md            ← Các lần bạn sửa Claude → Claude học lại
│   ├── project_*.md             ← Context các dự án đang chạy
│   └── reference_*.md           ← Link tới tài nguyên bên ngoài
│
└── output/
    └── Ahamove/
        ├── 01. STRATEGY_PLANNING/
        ├── 02. CAMPAIGNS_PROJECTS/
        ├── 03. DRIVER_COMMUNITY/
        ├── 04. OPS_METRICS/
        ├── 05. ANALYSIS_REPORTS/
        ├── 06. COMPETITIVE_INTEL/
        ├── 07. TEAM_MANAGEMENT/
        └── README.md            ← Index tổng hợp (cập nhật sau mỗi file mới)
```

---

### File 1: CLAUDE.md — "Hợp Đồng Ngầm" với Claude

**Đây là file quan trọng nhất.** Claude đọc file này mỗi khi bắt đầu — đây là nơi bạn nói cho Claude biết **bạn là ai, môi trường bạn làm việc, và Claude cần hành xử như thế nào**.

**CLAUDE.md nên chứa:**

```markdown
# CLAUDE.md

## Bối cảnh Công ty & Vai trò
- Tên công ty, lĩnh vực
- Vai trò của bạn (Driver Management Leader)
- Phạm vi quản lý (xe máy, không phải xe tải)
- KPIs quan trọng: AR, FR, CPO, EPH

## Chiến lược & Ưu tiên
- Chiến lược năm hiện tại
- Đối thủ cạnh tranh cần theo dõi

## Brand
- Màu sắc thương hiệu
- Font chữ
- Quy tắc biểu đồ/visualization

## Quy Tắc Đặt Tên & Lưu File
- Cấu trúc thư mục output/
- Quy tắc tên file (lowercase, hyphen, date prefix)

## Quy Tắc Hành Xử của Claude (AI Conventions)
- "Brief before executing" — phác thảo trước
- "Wait for confirmation" — chờ xác nhận
- "Vietnamese Default" — trả lời tiếng Việt
- "Ask when unclear" — không bịa số
```

> **Tại sao quan trọng?** Không có CLAUDE.md, mỗi session bạn phải giải thích lại bối cảnh từ đầu. Với CLAUDE.md tốt, Claude hiểu ngay bạn cần gì mà không cần nhắc nhở.

---

### File 2: memory/MEMORY.md — Index Bộ Nhớ

**MEMORY.md** = Danh sách các file memory Claude cần đọc. Nó không chứa nội dung, chỉ là **mục lục**.

```markdown
# Memory Index

- [user_profile.md](user_profile.md) — Khanh: Driver Management Leader tại Ahamove
- [user_rules.md](user_rules.md) — Rules làm việc: brief trước, SQL first, không bịa data
- [user_voice.md](user_voice.md) — Format: bảng > bullet > văn xuôi; từ vựng chuyên ngành
- [feedback_visualization.md](feedback_visualization.md) — Charts dùng SVG/HTML, không dùng thư viện ngoài
- [project_q2_driver_tiering.md](project_q2_driver_tiering.md) — Dự án restructure tiering Q2/2026
```

> **Quy tắc:** Mỗi file memory có **frontmatter** (header) xác định loại, tên, mô tả. Claude dùng mô tả để quyết định có cần đọc file đó không.

---

### File 3: memory/user_profile.md — Bạn Là Ai

```markdown
---
name: User Profile
description: Khanh - Driver Management Leader tại Ahamove, scope, background, daily metrics
type: user
---

**Tên:** Lê Phương Khanh
**Vai trò:** Driver Management Leader — Ahamove TP.HCM
**Phạm vi quản lý:** Xe máy Instant (Giao ngay 1H, Siêu tốc, Ghép đơn, 4H)
**KPIs theo dõi hằng ngày:** AR (Acceptance Rate), FR (Fulfillment Rate), CPO, EPH
**Không quản lý:** Xe tải, Truck — bỏ qua trong mọi phân tích
**Background:** [kinh nghiệm, kỹ năng đặc biệt...]
```

---

### File 4: memory/user_rules.md — Cách Làm Việc

```markdown
---
name: Working Rules
description: Cách Claude nên hành xử khi làm việc với Khanh
type: feedback
---

1. **Brief before executing** — Phác thảo dàn ý, chờ confirm trước khi viết dài
2. **SQL first** — Khi phân tích metrics, ưu tiên đề xuất SQL query hơn giải thích chung chung
3. **Không bịa số** — Nếu không có data, nói thẳng "cần data X để tính"
4. **Pyramid Principle** — Kết luận trước, lý do sau
5. **Bảng > Bullet > Văn xuôi** — Ưu tiên format bảng cho so sánh
```

---

### File 5: output/Ahamove/README.md — Index Output

```markdown
# Ahamove Output Index

Cập nhật: 2026-05-08

## 01. STRATEGY_PLANNING
- [2026-04-driver-tiering-framework.md] — Framework 4-tier mới, roadmap Q2-Q3
- [2026-05-minihub-analysis.md] — Phân tích ROI Mini-Hub HCM

## 02. CAMPAIGNS_PROJECTS
- [2026-05-mega620-campaign.md] — Kế hoạch campaign 20/6

[... tiếp tục theo folder ...]
```

> **Tại sao cần README.md?** Khi output có hàng chục file, README là "bản đồ" để Claude biết đã làm gì rồi, không tạo file trùng lặp.

---

## 13. Trình Tự Claude Pro Hoạt Động

Đây là điều **ít người hiểu rõ nhất** — cách một session Cowork thực sự diễn ra từng bước.

### Sơ đồ tổng quan

```
┌─────────────────────────────────────────────────────────┐
│                  MỞ SESSION COWORK                       │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 1: LOAD   │  Claude đọc CLAUDE.md
│  CONTEXT        │  → Biết: công ty, role, brand, quy tắc
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 2: LOAD   │  Claude đọc memory/MEMORY.md
│  MEMORY         │  → Biết: bạn là ai, sở thích, dự án đang chạy
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 3: NHẬN   │  Bạn gõ yêu cầu
│  PROMPT         │  "Phân tích AR tuần này, tạo báo cáo"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 4:        │  Claude brief dàn ý
│  PLANNING       │  → Chờ bạn confirm trước khi làm
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 5:        │  Claude dùng tools:
│  EXECUTION      │  - Read (đọc file)
│                 │  - Write/Edit (tạo/sửa file)
│                 │  - Bash (chạy lệnh)
│                 │  - WebSearch (tìm kiếm)
│                 │  - MCP (Gmail/Calendar/Drive)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 6:        │  Tạo file output vào đúng thư mục
│  OUTPUT         │  Cập nhật README.md nếu cần
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BƯỚC 7:        │  Nếu học được điều mới về bạn
│  MEMORY UPDATE  │  → Tự động lưu vào memory/*.md
│  (tự động)      │  → Lần sau không cần nhắc lại
└─────────────────┘
```

### Ví dụ cụ thể — "Tạo báo cáo AR tuần"

```
Bạn gõ: "Tạo báo cáo AR tuần 19, data trong file CSV này"

Claude làm:
1. Đọc CLAUDE.md → biết format báo cáo, màu brand, output folder
2. Đọc memory → biết bạn thích bảng > bullet, cần highlight khu vực thấp
3. Brief: "Tôi sẽ: (1) đọc CSV, (2) tính AR theo zone, (3) tạo file HTML, lưu vào 04.OPS_METRICS"
4. Bạn confirm: "ok đi"
5. Claude:
   - Read file CSV
   - Xử lý dữ liệu
   - Write file 2026-05-ar-week19-report.html
   - Edit README.md thêm entry mới
6. Báo kết quả: "Done. File lưu tại output/Ahamove/04.OPS_METRICS/..."
7. Nếu bạn nói "lần sau thêm cột EPH" → Claude lưu vào feedback memory
```

### Tại sao trình tự này quan trọng?

- **Bước 1-2 (Context loading):** Đây là lý do Cowork "thông minh hơn" claude.ai — nó bắt đầu với đầy đủ bối cảnh thay vì trang trắng
- **Bước 4 (Planning):** Brief trước → tránh Claude làm sai rồi phải làm lại
- **Bước 7 (Memory update):** Claude tự học từ feedback → lần sau không cần nhắc lại

---

## 14. Skills — Lệnh Tắt

**Skills** = Lệnh chuyên dụng được lập trình sẵn. Gõ `/tên-skill` → Claude biết ngay quy trình cần thực hiện.

### Skills hiện có trong Cowork

| Skill | Lệnh | Làm gì | Bối cảnh dùng |
|---|---|---|---|
| **xlsx** | `/xlsx` | Tạo/sửa file Excel chuyên nghiệp | Báo cáo số liệu, financial model |
| **pptx** | `/pptx` | Tạo slide PowerPoint | Presentation, proposal |
| **html** | `/html` | Tạo báo cáo HTML đẹp | Dashboard, report chia sẻ |
| **pdf** | `/pdf` | Đọc, tạo, ghép PDF | Xử lý tài liệu |
| **md** | `/md` | Viết tài liệu Markdown chuẩn | SOP, guide, analysis |
| **okr** | `/okr` | Xây OKR theo chuẩn | Lập kế hoạch quý |
| **plan** | `/plan` | Lập kế hoạch task phức tạp | Dự án nhiều bước |
| **schedule** | `/schedule` | Đặt lịch chạy task tự động | Báo cáo định kỳ |
| **pptx-a** | `/pptx-a` | Slide chuyên nghiệp theo brand | Deck quan trọng |
| **xlsx-a** | `/xlsx-a` | Financial model đầy đủ | Investment case, AOP |

### Cách dùng skill

```
/xlsx Tạo báo cáo AR/FR tuần 19, theo zone, highlight zone < 80%

/pptx Tạo deck 10 slides: "Driver Tiering Strategy Q2 2026"
      Đối tượng: C-level, tông màu Ahamove

/plan Lập kế hoạch rollout tiering mới cho 5000 tài xế HCM
```

### Tự tạo skill (nâng cao)

Skills được lưu trong `.claude/commands/` dưới dạng file Markdown. Nếu muốn tạo skill riêng cho team:

```markdown
# File: .claude/commands/driver-brief.md
---
description: Tạo driver operation brief hằng ngày
---

Tạo brief vận hành ngày hôm nay theo format:
1. Top 3 zone AR thấp nhất (cần action)
2. Alert fraud/anomaly nếu có
3. Recap campaign đang chạy
4. Action items cho ngày mai
```

---

## 15. MCP Tools

**MCP (Model Context Protocol)** = Chuẩn kết nối cho phép Claude "với tay" sang app khác.

### MCP Tools đang kết nối trong Cowork

| Tool | Kết nối với | Làm được gì |
|---|---|---|
| **Gmail** | Email của bạn | Đọc, tóm tắt, soạn draft, gắn label |
| **Google Calendar** | Lịch làm việc | Xem lịch, tạo event, đề xuất giờ họp |
| **Google Drive** | Cloud storage | Tìm file, đọc nội dung, tạo file mới |
| **NotebookLM** | Google NotebookLM | Tạo notebook nghiên cứu, tổng hợp nguồn |
| **Excalidraw** | Vẽ diagram | Tạo sơ đồ, flowchart |

### Ví dụ dùng MCP thực tế

```
"Kiểm tra email hôm nay, tóm tắt những email quan trọng
 liên quan đến driver operations"

"Xem lịch tuần tới, tìm slot 1 tiếng để họp team
 và đề xuất 3 thời điểm phù hợp"

"Tìm trong Drive file 'AR Report March', đọc và
 so sánh với data tuần này tôi vừa paste"
```

---

# PHẦN 5 — AN TOÀN & THAM KHẢO

## 16. Giới Hạn Của Claude

### Claude có thể nói sai — và bạn cần biết điều này

Claude đôi khi **"hallucinate"** — bịa ra thông tin nghe có vẻ đúng nhưng sai. Đặc biệt với:
- Số liệu cụ thể, thống kê (luôn verify)
- Tên người, ngày tháng, sự kiện lịch sử
- Thông tin pháp lý, y tế
- Tin tức sau ngày training cutoff

**Nguyên tắc vàng:** Claude là **assistant thông minh**, không phải **nguồn sự thật**. Luôn verify thông tin quan trọng.

### Nên vs Không nên dùng Claude

| ✅ NÊN dùng Claude | ❌ KHÔNG dùng Claude thay thế |
|---|---|
| Draft văn bản, email, báo cáo | Quyết định chiến lược quan trọng (không verify) |
| Brainstorm ý tưởng | Số liệu tài chính chính xác |
| Tóm tắt tài liệu dài | Tư vấn pháp lý, y tế |
| Giải thích khái niệm | Thay thế judgement của con người |
| Viết code, công thức | Thông tin real-time (giá, tin tức hôm nay) |
| Phân tích pattern từ data | Xác nhận compliance, quy định pháp luật |

---

## 17. Bảo Mật & Lưu Ý

### ⚠️ TUYỆT ĐỐI KHÔNG chia sẻ với Claude (trên cloud):

- **Mật khẩu, tài khoản ngân hàng**
- **Thông tin cá nhân nhạy cảm của tài xế/khách hàng** (CMND, SĐT, địa chỉ nhà)
- **Dữ liệu kinh doanh mật** (doanh thu nội bộ, chiến lược chưa công bố)
- **Hợp đồng, thỏa thuận bảo mật (NDA)**

### Tại sao?

Khi bạn gõ nội dung vào claude.ai, dữ liệu đó được gửi lên server của Anthropic. Mặc dù Anthropic có chính sách bảo mật tốt, **best practice** là không đưa thông tin nhạy cảm lên bất kỳ nền tảng AI cloud nào.

### Cách xử lý data nhạy cảm đúng

```
❌ Sai: "Phân tích tài xế: Nguyễn Văn A - 0901234567 - AR 45%"

✅ Đúng: "Phân tích tài xế (đã ẩn danh):
          Tài xế X - AR 45%, Tài xế Y - AR 62%"
```

**Anonymize trước khi hỏi** — thay tên thật bằng Tài xế A, B, C hoặc dùng ID giả.

---

## 18. Từ Điển Thuật Ngữ

| Thuật ngữ | Giải thích |
|---|---|
| **AI (Artificial Intelligence)** | Trí tuệ nhân tạo — phần mềm xử lý ngôn ngữ và lý luận |
| **LLM (Large Language Model)** | Mô hình ngôn ngữ lớn — loại AI train trên lượng văn bản khổng lồ |
| **Prompt** | Câu lệnh/câu hỏi bạn gửi cho Claude |
| **Context Window** | Lượng text Claude xử lý được trong 1 hội thoại |
| **Hallucination** | Khi AI bịa thông tin sai nhưng trình bày tự tin |
| **Knowledge Cutoff** | Ngày Claude ngừng cập nhật kiến thức mới |
| **Model** | Phiên bản AI: Haiku (nhanh), Sonnet (cân bằng), Opus (mạnh nhất) |
| **Token** | Đơn vị đo văn bản (≈ 3/4 từ tiếng Anh). Giới hạn context tính bằng token |
| **Agent** | Claude được trang bị tools để tự thực hiện tác vụ phức tạp |
| **API** | Cách kết nối Claude vào phần mềm/app khác (dành cho developer) |
| **CLAUDE.md** | File "hợp đồng" chứa bối cảnh công ty, quy tắc — Claude đọc mỗi session |
| **Memory** | Hệ thống file lưu trữ thông tin về bạn xuyên suốt nhiều session |
| **MEMORY.md** | Index — danh sách các file memory, Claude đọc để biết cần load gì |
| **Claude Code** | Phiên bản Claude chạy trong terminal, đọc/ghi file thật trên máy |
| **Claude Desktop** | App cài Mac/Windows, hỗ trợ MCP tools |
| **Cowork** | Môi trường đầy đủ: Claude Code + Memory + Skills + MCP |
| **Projects (Workspace)** | Không gian trong claude.ai — lưu system prompt và tài liệu nền |
| **MCP (Model Context Protocol)** | Chuẩn kết nối Claude sang app khác: Gmail, Calendar, Notion... |
| **Skills** | Lệnh tắt chuyên dụng trong Cowork — gõ `/tên-skill` |
| **System Prompt** | Lệnh nền cài sẵn định hình cách Claude phản hồi |
| **Anthropic** | Công ty tạo ra Claude, thành lập 2021, tập trung AI an toàn |
| **AR (Acceptance Rate)** | Tỷ lệ tài xế chấp nhận đơn hàng |
| **FR (Fulfillment Rate)** | Tỷ lệ hoàn thành đơn hàng thành công |
| **CPO (Cost Per Order)** | Chi phí incentive tính trên mỗi đơn hàng |
| **EPH (Earnings Per Hour)** | Thu nhập trung bình của tài xế theo giờ |

---

## Bắt Đầu Ngay Hôm Nay

### Checklist theo cấp độ

**Người mới (15 phút đầu):**
- [ ] Tạo tài khoản tại **claude.ai**
- [ ] Gửi 1 câu hỏi bất kỳ để làm quen giao diện
- [ ] Thử upload 1 file PDF/Word → hỏi Claude tóm tắt
- [ ] Thử viết 1 email theo COAT formula

**Người dùng thường xuyên (tuần đầu):**
- [ ] Tạo Project riêng cho Driver Ops trong claude.ai
- [ ] Upload SOP vận hành vào Project
- [ ] Thử 3 use case thực tế từ bảng Section 10

**Người dùng nâng cao (cần setup Cowork):**
- [ ] Setup Cowork với Khanh (liên hệ trực tiếp)
- [ ] Hiểu cấu trúc CLAUDE.md + memory/
- [ ] Thử 3 skill: `/xlsx`, `/md`, `/plan`
- [ ] Kết nối Gmail / Google Calendar qua MCP

### Khi nào hỏi Claude vs hỏi đồng nghiệp?

```
Câu hỏi có đáp án rõ ràng, không nhạy cảm  → Hỏi Claude trước (nhanh hơn)
Câu hỏi cần judgement, context nội bộ       → Hỏi đồng nghiệp / quản lý
Câu hỏi quan trọng                          → Claude draft trước → đồng nghiệp review
```

---

*Tài liệu này được soạn bởi Driver Management Team — Ahamove*
*Câu hỏi hoặc góp ý setup Cowork: Khanh — khanhlp@ahamove.com*
*Cập nhật: 2026-05-08*
