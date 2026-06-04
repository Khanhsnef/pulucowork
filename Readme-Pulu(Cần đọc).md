# 🤖 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG SMART CHAT (PULU)
*Tài liệu này được tạo tự động để lưu trữ các phím tắt và quy tắc chat trên Terminal.*

---

## 1. CÁCH BẮT ĐẦU CHAT NHANH NHẤT
Mỗi khi mở VS Code hoặc Terminal mới, hệ thống đã tự động kích hoạt ngầm. 
Bạn không cần gõ `source ~/.zshrc` nữa.

Chỉ cần gõ 1 trong 2 lệnh sau và nhấn Enter:
- `chat`
- `start`

Lúc này, một giao diện chat (Smart Chat REPL) sẽ hiện ra. Bạn cứ gõ câu hỏi bằng tiếng Việt/Anh bình thường, hệ thống sẽ **tự động phân tích câu hỏi và chọn Model AI phù hợp nhất** để tiết kiệm quota nhưng vẫn đảm bảo độ thông minh tối đa. Nhấn `Ctrl+C` hoặc gõ `exit` để thoát.

---

## 2. AUTO-ROUTING (LUỒNG CHỌN MODEL TỰ ĐỘNG)
Khi bạn gõ câu hỏi trong chế độ `chat` (hoặc nếu gõ thẳng 1 câu hỏi vào terminal), hệ thống quét từ khoá để chọn model:

| Từ khoá thường gặp (Ví dụ) | Model được chọn | Mục đích sử dụng |
| :--- | :--- | :--- |
| `phân tích`, `chiến lược`, `insight`, `p&l`, `okr`, `cung cầu`, `rủi ro` | **🧠 OPUS 4.8** (Cao cấp nhất) | Dùng cho tư duy sâu, chiến lược kinh doanh, lên cấu trúc bài viết, tài liệu quan trọng. |
| `sql`, `code`, `html`, `lark`, `dashboard`, `docx`, `pdf`, `xuất file`, `định dạng` | **💻 SONNET 4.6** | Chuyên gia viết code, lập trình, format tài liệu, chuyển đổi file. |
| `thông báo`, `zalo`, `kịch bản`, `tài xế`, `cạnh tranh` | **⚡ GEMINI PRO** | Ngôn ngữ tự nhiên tốt, viết content, dịch thuật, thông báo cộng đồng. |
| `english`, `proposal`, `hq`, `global` | **🌐 GPT-5.5** | Văn phong chuẩn quốc tế, viết tài liệu cho sếp, báo cáo tiếng Anh. |
| `hỏi nhanh`, `nhanh`, `là gì`, `tính toán` | **💨 DEEPSEEK** (Flash/Miễn phí) | Hỏi đáp siêu tốc, tra cứu nhanh, không tốn quota. |
| *(Không chứa từ khoá nào)* | **🤖 OPUS 4.8** | Mặc định sử dụng model thông minh nhất. |

*(Ví dụ: Bạn gõ "phân tích driver tier" -> Hệ thống tự gọi Opus 4.8. Câu tiếp theo bạn gõ "viết thông báo zalo" -> Hệ thống gọi Gemini Pro nhưng vẫn NHỚ toàn bộ ngữ cảnh câu trước).*

---

## 3. LỐI TẮT BẰNG LỆNH (ONE-SHOT)
Nếu bạn không muốn vào chế độ `chat` mà chỉ muốn hỏi nhanh 1 câu rồi làm việc khác, bạn có thể gõ chữ `ai` kèm theo câu hỏi (để trong ngoặc kép).

Ví dụ: 
```bash
ai "viết cho tôi đoạn code HTML"
ai "phân tích chiến lược Q3"
```
Hệ thống cũng sẽ tự động quét từ khoá giống hệt bảng bên trên.

---

## 4. ÉP BUỘC CHỌN MODEL (MANUAL ALIAS)
Nếu bạn biết chắc mình muốn dùng Model nào và không muốn phụ thuộc vào Auto-routing, hãy dùng các lệnh tắt sau:

- `c-opus` : Mở chat bằng Opus 4.8 (Max brain)
- `c-think` : Mở chat bằng Opus 4.6 Thinking (Chế độ suy nghĩ chậm, logic)
- `c-sonnet`: Mở chat bằng Sonnet 4.6 (Code/Format)
- `c-gemini`: Mở chat bằng Gemini Pro (Viết lách/Dịch thuật)
- `c-gpt`   : Mở chat bằng GPT-5.5 (Tiếng Anh/HQ)
- `c-fast`  : Mở chat bằng DeepSeek (Hỏi nhanh miễn phí)

---

## 5. TÍNH NĂNG "COMMAND NOT FOUND"
Thậm chí, nếu bạn quên mất lệnh `chat` hay `ai`, bạn có thể gõ trực tiếp 1 câu vào terminal (nếu câu đó không trùng với lệnh hệ thống nào).
Ví dụ:
```bash
tính toán CPO nếu tăng 10%
```
Terminal sẽ báo lỗi nhẹ, nhưng ngay lập tức **tự động chuyển câu đó cho AI trả lời** (sẽ gọi DeepSeek hoặc Opus tùy từ khoá).

---

## 6. ⚠️ LƯU Ý QUAN TRỌNG: THANH TIẾN TRÌNH VÀ CHẠY TOOL

Có một sự đánh đổi (Trade-off) về mặt kỹ thuật trên Terminal như sau:

- **Khi dùng lệnh `chat` hoặc `ai`:** Hệ thống có khả năng tự động đổi Model mượt mà ở mỗi câu. Tuy nhiên, nó bị ép chạy ở chế độ ẩn (`-p`), nên **KHÔNG hiển thị được thanh tiến trình (Progress bar) và KHÔNG thể chạy công cụ (như tự viết file, xuất docx)**.
- **Khi muốn chạy Tool (Có thanh tiến trình, tự xuất file, tự code):** Bạn phải sử dụng các lệnh ở Mục 4 kèm theo câu lệnh (Ví dụ: `c-sonnet "xuất docx file báo cáo này"`). Lúc này, giao diện tương tác (Interactive) của Claude sẽ mở ra, hiển thị quá trình chạy Tool và có giao diện hỏi Yes/No để bạn phê duyệt. Nhược điểm là nó sẽ bị khoá vào duy nhất 1 model đó cho tới khi bạn gõ `/exit` để thoát.

**Tóm lại Workflow chuẩn:**
👉 Hỏi đáp, viết nháp, phân tích, dịch thuật -> Dùng lệnh `chat` (Auto-routing).
👉 Tạo file, xuất docx, chạy script tự động -> Dùng lệnh `c-sonnet "nội dung"` (Bật giao diện Tool).
