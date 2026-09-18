---
type: ops-brief
title: <% tp.file.title %>
date: <% tp.file.creation_date("YYYY-MM-DD") %>
author: Lê Phương Khanh
category: strategy-planning
status: draft
pnl_impact: medium
tags:
  - ahamove
  - ops-brief
  - strategy
---

# 📊 AHAMOVE STRATEGIC OPS BRIEF: <% tp.file.title %>

> [!NOTE]
> **Executive Summary:** Nêu ngắn gọn phát hiện/khuyến nghị cốt lõi nhất (Mô hình Kim Tự Tháp - Pyramid Principle).

---

## 🎯 1. BỐI CẢNH & MỤC TIÊU KINH DOANH (S-C-R FRAMEWORK)

*   **Situation (Bối cảnh):** 
*   **Complication (Thách thức/Điểm nghẽn):** 
*   **Resolution (Giải pháp Đề xuất):** 

---

## 📈 2. CHỈ SỐ KỲ VỌNG & ĐÁNH ĐỔI P&L (UNIT ECONOMICS & TRADE-OFFS)

| Chỉ số (KPI) | Hiện trạng (Baseline) | Mục tiêu (Target) | Tác động P&L / Cost per Order |
| :--- | :--- | :--- | :--- |
| **Active Drivers** | | | |
| **Acceptance Rate** | | | |
| **Fulfillment Rate** | | | |
| **CPO / Incentive** | | | |

---

## ⚙️ 3. SQL EVIDENCE / LOGIC TÍNH TOÁN (SQL-BACKED EVIDENCE)

```sql
-- SQL Query kiểm tra dữ liệu thực tế
SELECT 
    city_id,
    COUNT(DISTINCT driver_id) as active_drivers,
    AVG(acceptance_rate) as avg_acceptance_rate
FROM ahamove_ops.driver_performance_daily
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1;
```

---

## 🚀 4. LỘ TRÌNH THỰC THI (EXECUTION ROADMAP)

- [ ] **Giai đoạn 1 (Pilot):** 
- [ ] **Giai đoạn 2 (Scale Up):** 
- [ ] **Giai đoạn 3 (Post-Mortem Review):** 
