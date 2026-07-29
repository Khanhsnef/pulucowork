# 🏷️ Tag Request Portal - Visual & Content UI Configuration

Anh/Chị có thể sửa trực tiếp bất kỳ nội dung text, tiêu đề, tên nút bấm hoặc danh sách lựa chọn trong file Markdown này. Khi sửa xong, chỉ cần gõ vào khung chat: *"Cập nhật code từ file UI_CONFIG.md giúp tôi"*, AI sẽ tự động đồng bộ sang tệp `Index.html`, `2026-07-dm-qm-tag-request-manager.html` và `Code.gs`!

> ⚡ **Lưu ý (v2 — 3-Gate Workflow):** Từ bản này tool đã nâng lên **luồng phê duyệt đa tầng** (Lead → DM → QM) + **phân quyền RBAC theo email** + **SLA đếm giờ**. Xem mục 8, 9, 10 bên dưới.

---

## 1. Thông Tin Chung & Header
- **App Title**: Tag Request Portal
- **Link Target Text**: Google Sheet Target
- **Google Sheet URL**: https://docs.google.com/spreadsheets/d/1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4/edit#gid=407438001

---

## 2. Thẻ Thống Kê KPI (Summary Cards)
- **Card 1 Title**: Tổng Yêu Cầu · **Subtitle**: Ghi nhận trên hệ thống
- **Card 2 Title**: Chờ Lead Duyệt · **Subtitle**: SLA: ≤ 4h
- **Card 3 Title**: Chờ DM Review · **Subtitle**: SLA: ≤ 8h
- **Card 4 Title**: Chờ QM Add Tags · **Subtitle**: SLA: ≤ 24h
- **Card 5 Title**: Hoàn Thành (Done) · **Subtitle**: Đã add tag thành công

---

## 3. Tên Các Tab Điều Hướng (Navigation Tabs) — 5 Tab
- **Tab 1 Name**: 📝 Bước 1: Request
- **Tab 2 Name**: 👔 Bước 2: Lead Approval
- **Tab 3 Name**: 🛡️ Bước 3: DM Review
- **Tab 4 Name**: ⚙️ Bước 4: QM Add Tags
- **Tab 5 Name**: 📊 Master Request Tracker

---

## 4. Bước 1: Biểu Mẫu Gửi Yêu Cầu (Request Form)
- **Form Section Header**: 📝 Biểu Mẫu Tạo Yêu Cầu Tag Tài Xế Cho Phía DM
- **Field 1 Label**: Team Đề Xuất *
- **Field 2 Label**: Họ Tên Người Yêu Cầu *
- **Field 3 Label**: Loại Tag Mong Muốn *
- **Field 4 Label**: Tên Tag Gợi Ý / Mục Tiêu *
- **Field 5 Label**: Thời Gian Áp Dụng *
- **Field 6 Label**: Lý Do Kinh Doanh & Tiêu Chí Chọn Tài Xế *
- **Submit Button Text**: 🚀 Gửi Đề Xuất Tới Lead Duyệt

### Danh Sách Các Team Đề Xuất (Dropdown)
1. Business Operations
2. Marketing Campaign
3. Hub Linehaul Operations
4. Customer Service (CS)
5. Risk & Fraud Control
6. Fleet Operations

### Danh Sách Loại Tag Mong Muốn (Dropdown)
1. Priority Dispatch (Ưu tiên phát đơn)
2. Incentive Campaign (Thưởng/Thách thức)
3. Area Restriction (Giới hạn khu vực)
4. Special Training (Đào tạo dịch vụ VIP)
5. Penalty / Block (Khóa/Tạm dừng)

---

## 5. Bước 2: Bàn Duyệt Của Lead / Head (Lead Approval — Gate 1) 🆕
- **Section Header**: 👔 Bàn Duyệt Của Lead / Head Team (Gate 1)
- **Modal Header**: 👔 Duyệt Cấp Lead
- Lead/Head duyệt request của team → APPROVED (chuyển tiếp) hoặc REJECTED (trả requester kèm lý do).

---

## 6. Bước 3: Bàn Tròn DM Review (DM Review Console — Gate 2)
- **Section Header**: 🛡️ Bàn Tròn Thẩm Định Của DM Lead (Gate 2)
- **Modal Header**: 🛡️ Thẩm Định Request
- Chỉ áp dụng cho **Tạo tag mới**. Add tag có sẵn sẽ bỏ qua bước này.

---

## 7. Bước 4: Hàng Đợi QM Add Tag (QM Add Tag Queue — Gate 3)
- **Section Header**: ⚙️ Hàng Đợi QM Tiếp Nhận & Add Tag (Gate 3)
- QM cập nhật trạng thái: PENDING_QM → PROCESSING → TAGGED_SUCCESS (→ DONE) / FAILED.

---

## 8. State Machine — Trạng Thái Tổng (cột `Trạng Thái Tổng`)

```text
              ┌──────── REJECT (kèm lý do → trả requester) ────────┐
              ▼                                                    │
[PENDING_TEAM_LEAD] → [PENDING_DM] → [PENDING_QM] → [DONE]
     (Gate 1)     │     (Gate 2)        (Gate 3)
                  └── nếu "Add tag" (tag có sẵn) → bỏ qua DM → [PENDING_QM]
```

| Hình thức | Luồng | Số gate |
| :--- | :--- | :--- |
| **Tạo tag mới** | PENDING_TEAM_LEAD → PENDING_DM → PENDING_QM → DONE | 3 gate |
| **Add tag có sẵn** | PENDING_TEAM_LEAD → PENDING_QM → DONE (DM = SKIPPED) | 2 gate |
| **Reject bất kỳ gate** | → REJECTED (hiển thị lý do cho requester để sửa & re-submit) | — |

---

## 9. Phân Quyền RBAC (Hardcode trong `Code.gs` → `ROLE_MAP`)

> ⚠️ **Cần Khanh điền email thật** vào `ROLE_MAP` trong `Code.gs` (hiện đang để placeholder `lead1@`, `qm1@`...).

| Vai trò | Quyền xem Tab | Hành động được phép |
| :--- | :--- | :--- |
| **REQUESTER** (mặc định) | Request, Master | Tạo request |
| **TEAM_LEAD** | + Lead Approval | Duyệt/Từ chối Gate 1 |
| **DM** | + Lead Approval, DM Review, QM, Live Editor | Duyệt Gate 1 & 2, chỉnh QM, sửa config |
| **QM** | + QM Add Tags | Add tag, cập nhật Gate 3 |

- Backend enforce thật qua `getUserRole()` trước mỗi lần ghi (không chỉ ẩn UI).
- Frontend ẩn/hiện tab theo `TAB_ACCESS` để gọn giao diện.

---

## 10. SLA Config (chỉnh qua Live UI Editor → lưu về `00_CONFIG_SETTINGS`)

| Key | Mặc định | Ý nghĩa |
| :--- | :--- | :--- |
| `SLA_LEAD_HOURS` | 4 | Giờ chờ tối đa ở Gate 1 (Lead) |
| `SLA_DM_HOURS` | 8 | Giờ chờ tối đa ở Gate 2 (DM) |
| `SLA_QM_HOURS` | 24 | Giờ chờ tối đa ở Gate 3 (QM) |

- Hàm `checkSLABreaches()` quét sheet, đánh cờ **`QUÁ HẠN SLA`** (badge đỏ nhấp nháy) + gửi email nhắc đúng nhóm approver.
- **Gắn trigger:** Apps Script → *Triggers* → `checkSLABreaches`, time-driven, mỗi 1–2h.
