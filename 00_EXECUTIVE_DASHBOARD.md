---
type: dashboard
title: Executive Cockpit Dashboard
author: Lê Phương Khanh
updated: 2026-08-31
tags:
  - dashboard
  - executive
  - ahamove
---

# 🚀 AHAMOVE DRIVER MANAGEMENT — EXECUTIVE COCKPIT DASHBOARD

> [!IMPORTANT]
> **LEADER:** Lê Phương Khanh — Driver Management Leader | **MỤC TIÊU CỐT LÕI:** Quản trị Nguồn cung Xe máy (Instant 1H, Siêu tốc, 4H, Enterprise) | Tối ưu Mini-Hub | Restructure 4 Tầng Tài xế.

---

## ⚡ 1. QUICK ACTION HUB (KHỞI TẠO NHANH)

| Nút Khởi Tạo Nhanh | Mục Đích Sử Dụng | Template Áp Dụng |
| :--- | :--- | :--- |
| 📅 **Tạo Daily Ops Log** | Ghi chép vận hành ngày, sự cố Mini-Hub, SLA | `[[T_Daily_Ops_Log]]` |
| 📊 **Tạo Strategic Ops Brief** | Đề án chiến lược, One-Pager trình CPO | `[[T_Ahamove_Ops_Brief]]` |
| 🎯 **Tạo Executive Decision Log** | Ghi vết quyết định P&L, trade-offs | `[[T_Decision_Log]]` |
| ⚔️ **Tạo Competitive Intel Brief** | Theo dõi động thái Grab, Be, XanhSM | `[[T_Competitive_Intel]]` |
| 💻 **Tạo SQL Metric Snippet** | Lưu trữ câu lệnh SQL & logic chỉ số | `[[T_SQL_Metric_Snippet]]` |

---

## 📊 2. DANH SÁCH DỰ ÁN & ĐỀ ÁN VẬN HÀNH ĐANG CHẠY (ACTIVE OPS PROJECTS)

```dataview
TABLE date AS "Ngày Cập Nhật", status AS "Trạng Thái", category AS "Mảng Vận Hành"
FROM "Output/Ahamove"
WHERE file.name != "README"
SORT file.mtime DESC
LIMIT 12
```

---

## 🎯 3. EXECUTIVE DECISION LOG (CÁC QUYẾT ĐỊNH ĐANG THEO DÕI)

```dataview
TABLE review_date AS "Mốc Review", status AS "Trạng Thái", impact_level AS "Tác Động P&L"
FROM ""
WHERE type = "decision"
SORT review_date ASC
```

---

## ⚔️ 4. BỨC TRANH CẠNH TRANH THỊ TRƯỜNG (COMPETITIVE INTEL WATCH)

```dataview
TABLE competitor AS "Đối Thủ", threat_level AS "Mức Mối Đe Dọa", date AS "Ngày Ghi Nhận"
FROM ""
WHERE type = "competitive-intel"
SORT date DESC
```

---

## 📋 5. DANH SÁCH VIỆC CẦN XỬ LÝ TRONG TOÀN VAULT (UNCOMPLETED TASKS)

```dataview
TASK
FROM ""
WHERE !completed AND file.name != "00_EXECUTIVE_DASHBOARD"
GROUP BY file.link
```

---

## 🏠 6. GOVERNANCE & PERSONAL CONTROL PANEL

*   👤 **Hồ sơ Cá nhân & Định hướng:** `[[Personal/about-me]]` | `[[Personal/my-rules]]` | `[[Personal/my-voice]]`
*   🥗 **Gia đình & Sức khỏe:** `[[Personal/Menu_Me_Bau_6_Tuan.csv]]`
*   🛠️ **Công cụ & Automation:** `[[AGENTS.md]]` | `[[CLAUDE.md]]` | `[[Readme-Pulu(Cần đọc).md]]`

---
*Last Dashboard System Sync: 2026-08-31 | Developed for Lê Phương Khanh @ Ahamove*
