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

## 6. 🔥 TÍNH NĂNG ĐỘC QUYỀN: HYBRID MODE (CHẠY TOOL TỰ ĐỘNG MƯỢT MÀ)

Trong lệnh `chat` có một chế độ cực kỳ thông minh gọi là **Hybrid Mode**:

- **Luồng 1 (Hỏi đáp, Phân tích, Viết lách):** Hệ thống tự động đẩy vào chế độ Ẩn (Text Mode). Lúc này chữ sẽ được sinh ra siêu mượt mà, đổi Model ngầm theo nội dung, không có thanh Loading phức tạp cản trở tốc độ.
- **Luồng 2 (Tạo file, Xuất Docx, Viết Code, Chạy Script):** Khi hệ thống quét thấy các từ khóa như `tạo file`, `xuất`, `docx`, `lưu file`... nó sẽ **tự động chuyển sang Chế độ Tool (Tool Mode)**. Màn hình sẽ hiện dòng cảnh báo màu vàng, và toàn bộ Giao diện Gốc của Claude (Thanh tiến trình, Progress Bar, Form hỏi Yes/No cấp quyền) sẽ bung ra để phục vụ bạn.

⚠️ **Lưu ý nhỏ ở Chế độ Tool:** Sau khi tạo file / chạy Tool xong, màn hình sẽ dừng ở dấu nhắc `> `. Bạn chỉ cần gõ `/exit` để thoát khỏi giao diện Tool và trở lại tiếp tục trò chuyện trong lệnh `chat`.

**Tóm lại Workflow Chuẩn nhất:** 
Bạn chỉ cần nhớ 1 chữ duy nhất: gõ `chat`. Mọi việc còn lại (chọn model gì, dùng chế độ nào) hãy để hệ thống tự động lo liệu giúp bạn!
