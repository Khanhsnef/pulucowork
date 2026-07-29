# 🚀 Hướng Dẫn Deploy — Tag Request Portal (3-Gate + RBAC + SLA)

> Áp dụng cho: `Code.gs` (backend) + `Index.html` (Web App UI). File `2026-07-dm-qm-tag-request-manager.html` là **bản DEMO offline**, không cần deploy.

---

## 0. Chuẩn Bị Trước Khi Deploy

| Việc | Chi tiết |
| :--- | :--- |
| ✅ Điền email thật vào `ROLE_MAP` | Mở `Code.gs`, tìm dòng `>>> KHANH ĐIỀN EMAIL THẬT VÀO ĐÂY <<<`. Thay `lead1@`, `lead2@`, `qm1@`, `qm2@`, `khanh@` bằng email `@ahamove.com` thật. |
| ✅ Kiểm tra Spreadsheet Target | ID: `1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4`. Script phải **bound** vào đúng sheet này (mở từ Extensions của chính sheet đó). |

---

## 1. Tạo / Cập Nhật Apps Script Project

1. Mở Google Sheet Target → **Extensions ▸ Apps Script**.
2. Trong editor, tạo/ghi đè 2 file:
   - File `Code.gs` ← dán toàn bộ nội dung `Code.gs`.
   - File `Index.html` (New ▸ HTML) ← dán toàn bộ nội dung `Index.html`.
3. **Ctrl/Cmd + S** để lưu cả 2.

> ⚠️ Tên file HTML phải đúng `Index` (khớp `HtmlService.createTemplateFromFile("Index")` trong `doGet`).

---

## 2. Khởi Tạo Sheet & Cấp Quyền

1. Trong Apps Script, chọn hàm `getMainSheet` ▸ **Run** (lần đầu sẽ hiện popup xin quyền).
2. **Authorize access** → chọn tài khoản `@ahamove.com` → *Advanced ▸ Go to project (unsafe)* → **Allow**.
3. Hàm sẽ tự tạo 2 sheet nếu chưa có:
   - `00_CONFIG_SETTINGS` (config text + SLA keys)
   - `01_ALL_TAG_REQUESTS` (32 cột: 23 gốc + 9 mới)
4. Nếu sheet cũ đã có 23 cột → `getMainSheet()` **tự migrate**, thêm 9 cột mới ở cuối, **không vỡ data cũ**.

---

## 3. Deploy Web App

1. Góc phải trên ▸ **Deploy ▸ New deployment**.
2. **Select type** (bánh răng) ▸ **Web app**.
3. Cấu hình:
   | Trường | Giá trị |
   | :--- | :--- |
   | Description | `Tag Portal v2 - 3 Gate` |
   | Execute as | **Me** (`khanh@ahamove.com`) |
   | Who has access | **Anyone within Ahamove** (để RBAC theo email chạy đúng) |
4. **Deploy** → copy **Web app URL** (dạng `.../exec`) → gửi link cho các team.

> 🔑 **Bắt buộc "Execute as: Me" + "Anyone within org"** thì `Session.getActiveUser().getEmail()` mới trả đúng email người mở → RBAC mới hoạt động. Nếu chọn "Anyone (anonymous)" email sẽ rỗng → mọi người thành REQUESTER.

### Cập nhật code sau này
- Sửa code → **Deploy ▸ Manage deployments ▸ (bút chì) Edit ▸ Version: New version ▸ Deploy**.
- Giữ nguyên URL cũ (không tạo New deployment nếu muốn link không đổi).

---

## 4. Gắn Trigger SLA (`checkSLABreaches`)

1. Apps Script ▸ thanh trái ▸ **Triggers** (biểu tượng đồng hồ) ▸ **+ Add Trigger**.
2. Cấu hình:
   | Trường | Giá trị |
   | :--- | :--- |
   | Function to run | `checkSLABreaches` |
   | Deployment | `Head` |
   | Event source | **Time-driven** |
   | Type | **Hour timer** ▸ **Every 1 hour** (hoặc 2 giờ) |
3. **Save** → authorize thêm quyền gửi mail (`MailApp`) nếu được hỏi.

Trigger sẽ quét mọi request chưa `DONE`/`REJECTED`, so deadline với hiện tại → đánh cờ **`QUÁ HẠN SLA`** (badge đỏ nhấp nháy) + gửi email nhắc đúng nhóm approver (Lead/DM/QM). Chỉ gửi mail **1 lần** cho mỗi request quá hạn.

---

## 5. Test End-to-End (checklist sau deploy)

| # | Kịch bản | Kết quả mong đợi |
| :-- | :--- | :--- |
| 1 | Login bằng email REQUESTER | Chỉ thấy tab **Request** + **Master** |
| 2 | Login TEAM_LEAD | Thấy thêm tab **Lead Approval** |
| 3 | Login DM | Thấy đủ tab + Live UI Editor |
| 4 | Login QM | Thấy tab **QM Add Tags** |
| 5 | Tạo request "Tạo tag mới" | State = `PENDING_TEAM_LEAD`, hiện ở tab Lead |
| 6 | Lead **APPROVE** tag mới | → `PENDING_DM`, hiện ở tab DM |
| 7 | DM **APPROVE** + gán tag code | → `PENDING_QM`, hiện ở tab QM |
| 8 | QM chọn `TAGGED_SUCCESS` | → `DONE`, KPI "Hoàn Thành" +1 |
| 9 | Tạo request **"Add tag"** → Lead APPROVE | Bỏ qua DM, thẳng `PENDING_QM` (DM = SKIPPED) |
| 10 | **REJECT** ở gate Lead (kèm lý do) | → `REJECTED`, requester thấy lý do |
| 11 | Chạy tay `checkSLABreaches()` với 1 request quá deadline | Cột `Cờ Quá Hạn` = `QUÁ HẠN SLA` + nhận email nhắc |
| 12 | Mở lại data cũ (23 cột) | Không vỡ, 9 cột mới rỗng được bổ sung |

---

## 6. Sự Cố Thường Gặp

| Triệu chứng | Nguyên nhân & Cách xử lý |
| :--- | :--- |
| Ai mở cũng là REQUESTER | Deploy sai "Who has access" → sửa thành *Anyone within Ahamove* + *Execute as: Me* |
| Không nhận được email SLA | Chưa gắn trigger `checkSLABreaches`, hoặc chưa authorize quyền `MailApp` |
| Tab không ẩn theo role | Email login không nằm trong `ROLE_MAP` (đang là placeholder) → điền email thật |
| Lỗi "createTemplateFromFile" | File HTML không tên đúng `Index` |
| Data cũ lệch cột | Đừng chèn cột giữa chừng thủ công — để `getMainSheet()` migrate append cuối |

---

*Cập nhật: 2026-07-29 | Ahamove Driver Management*
