---
type: decision
title: <% tp.file.title %>
date: <% tp.file.creation_date("YYYY-MM-DD") %>
decider: Lê Phương Khanh
stakeholders: [Operations, BI, Product, Finance]
status: pending-review
review_date: <% tp.date.now("YYYY-MM-DD", 14) %>
impact_level: high
tags:
  - decision-log
  - executive
---

# 🎯 EXECUTIVE DECISION LOG: <% tp.file.title %>

> [!IMPORTANT]
> **Quyết định Cốt lõi:** Ghi rõ phát biểu quyết định trong 1-2 câu trực diện.

---

## 🔍 1. BỐI CẢNH & GIẢ ĐỊNH DỮ LIỆU (CONTEXT & ASSUMPTIONS)
*   **Vấn đề cần giải quyết:** 
*   **Bằng chứng dữ liệu (SQL/BI):** 
*   **Giả định chính (Key Assumptions):** 

---

## ⚖️ 2. MA TRẬN ĐÁNH ĐỔI PHƯƠNG ÁN (TRADE-OFF MATRIX)

| Phương án (Options) | Ưu điểm (Pros) | Nhược điểm (Cons) | Tác động CPO / SLA | Rủi ro (Risks) |
| :--- | :--- | :--- | :--- | :--- |
| **Option A (Đề xuất)** | | | | |
| **Option B (Phương án 2)**| | | | |
| **Option C (Do Nothing)** | | | | |

---

## 📌 3. LÝ DO CHỌN & CHỈ SỐ XÁC THỰC (RATIONALE & VALIDATION METRICS)
*   **Lý do lựa chọn Option A:** 
*   **Chỉ số xác thực thành công (Success Metrics):** 
*   **Cột mốc Đánh giá lại (Review Date):** `[[<% tp.date.now("YYYY-MM-DD", 14) %>]]`

---

## 📋 4. KẾ HOẠCH BÀN GIAO & TRUYỀN THÔNG (COMMUNICATION PLAN)
- [ ] Thông báo bộ phận Ops Mini-Hub
- [ ] Truyền thông Đối tác Tài xế qua Zalo/App
- [ ] Cập nhật SQL Dashboard theo dõi
