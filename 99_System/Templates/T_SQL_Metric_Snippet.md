---
type: sql-snippet
metric_name: <% tp.file.title %>
database: ahamove_production
author: Lê Phương Khanh
updated: <% tp.file.creation_date("YYYY-MM-DD") %>
tags:
  - sql
  - ops-metrics
  - data
---

# 💻 SQL METRIC QUERY: <% tp.file.title %>

> [!NOTE]
> **Mục đích:** Mô tả chỉ số cần tính (VD: Active Drivers, Acceptance Rate, Cancellation True Rate, CPO per District).

---

## ⚙️ 1. CÂU LỆNH SQL STANDARD (PRODUCTION GRADE)

```sql
-- Metric: <% tp.file.title %>
-- Author: Lê Phương Khanh
-- Description: 

SELECT
    DATE_TRUNC('day', order_time) AS order_date,
    city_name,
    service_type,
    COUNT(DISTINCT driver_id) AS active_drivers,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) * 1.0 / COUNT(order_id) AS fulfillment_rate
FROM ahamove_dw.fact_orders
WHERE order_time >= CURRENT_DATE - INTERVAL '30 days'
  AND service_type IN ('BIKE_INSTANT_1H', 'BIKE_EXPRESS', 'BIKE_4H')
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 4 DESC;
```

---

## 📌 2. ĐẦU RA MẪU & CÁCH GIẢI THÍCH CHỈ SỐ (OUTPUT SCHEMA & INTERPRETATION)
*   **Bảng dữ liệu đầu ra:**
*   **Điểm lưu ý khi chạy query:** (Ví dụ: Filter loại trừ xe tải, chỉ lấy Xe máy 2 bánh).
