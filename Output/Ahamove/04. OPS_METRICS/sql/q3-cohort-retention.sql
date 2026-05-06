-- ============================================================
-- QUERY 3: Cohort Retention Analysis
-- Mục đích: Tính retention rate M+1, M+2, ... M+12 theo NIM cohort
-- Input: Chạy sau khi có output từ Query 2 (hoặc dùng CTE chung)
-- Output: cohort_month × city_id × months_after → retention_rate
-- ============================================================
-- Cách đọc kết quả:
--   cohort_month = tháng NIM (tháng đầu active)
--   months_after = 0 (tháng NIM), 1 (tháng NLM), 2, 3...
--   cohort_size  = số driver NIM trong tháng đó
--   retained     = số còn active (có online hours) tại months_after
--   retention_pct = retained / cohort_size * 100
-- ============================================================

WITH standard AS (
  {{snippet: @yenhm GBQ.date_trunc}}
  {{snippet: @vinhnp1 standard_online_fulltime_driver}}
),

-- Online hours toàn range (mở rộng để cover đủ M+12)
online_all AS (
  SELECT
    datetrunc_mock(TIMESTAMP(r.period, 'Asia/Saigon'), 'month') AS period_month,
    r.supplier_id,
    datetrunc_mock(s.first_complete_time, 'month')              AS first_complete_month,
    r.city_id,
    SUM(r.online_hours)                                         AS online_hours
  FROM ahamove_archive.ops_suppliers_online_hours r
  LEFT JOIN `aha-move`.ahamove_supplier_raw.supplier_raw s ON r.supplier_id = s.id
  WHERE r.period >= DATE_TRUNC(DATE({{start_date}}), MONTH)
    AND r.period <  DATE_ADD(DATE_TRUNC(DATE({{end_date}}), MONTH), INTERVAL 1 MONTH)
    AND COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND s.tags NOT LIKE '%SALESFORCE%'
  GROUP BY 1, 2, 3, 4
),

-- NIM cohort: drivers có first_complete_month trong range
nim_cohorts AS (
  SELECT DISTINCT
    first_complete_month   AS cohort_month,
    supplier_id,
    city_id
  FROM online_all
  WHERE period_month = first_complete_month           -- Tháng đầu tiên active = NIM
    AND first_complete_month >= DATE_TRUNC(DATE({{start_date}}), MONTH)
    AND first_complete_month <= DATE_TRUNC(DATE({{end_date}}),   MONTH)
),

-- Lag steps: M+0 → M+12
lag_steps AS (
  SELECT lag_n
  FROM UNNEST(GENERATE_ARRAY(0, 12)) AS lag_n
),

-- Cross join cohort × lag → kiểm tra còn active không
cohort_retention AS (
  SELECT
    c.cohort_month,
    c.city_id,
    l.lag_n                                  AS months_after,
    c.supplier_id,
    -- Tháng cần kiểm tra active
    DATE_ADD(c.cohort_month, INTERVAL l.lag_n MONTH) AS check_month,
    -- Có online hours tháng đó không?
    CASE WHEN o.online_hours IS NOT NULL THEN 1 ELSE 0 END AS is_active
  FROM nim_cohorts c
  CROSS JOIN lag_steps l
  LEFT JOIN online_all o
    ON  o.supplier_id   = c.supplier_id
    AND o.city_id       = c.city_id
    AND o.period_month  = DATE_ADD(c.cohort_month, INTERVAL l.lag_n MONTH)
  -- Chỉ giữ check_month không vượt quá end_date
  WHERE DATE_ADD(c.cohort_month, INTERVAL l.lag_n MONTH)
          <= DATE_TRUNC(DATE({{end_date}}), MONTH)
)

-- ============================================================
-- OUTPUT: Retention rate per cohort × city × months_after
-- ============================================================
SELECT
  cohort_month,
  city_id,
  months_after,
  check_month,
  COUNT(DISTINCT supplier_id)                                      AS cohort_size,
  COUNT(DISTINCT CASE WHEN is_active = 1 THEN supplier_id END)    AS retained,
  ROUND(
    COUNT(DISTINCT CASE WHEN is_active = 1 THEN supplier_id END)
    * 100.0
    / NULLIF(COUNT(DISTINCT supplier_id), 0),
    1
  )                                                                AS retention_pct,

  -- Breakdown: trong số còn active, bao nhiêu là FT vs PT (M+2 trở đi)
  -- Cần join thêm online_hours để tính segment tại check_month
  -- → Xem query 3b bên dưới nếu cần

FROM cohort_retention
GROUP BY 1, 2, 3, 4
ORDER BY city_id, cohort_month, months_after


-- ============================================================
-- QUERY 3B: Graduation Quality — NIM cohort → FT / PT tại M+2
-- Chạy riêng để biết: trong số NIM còn sống M+2,
--                     bao nhiêu trở thành FT vs PT?
-- ============================================================
/*
WITH standard AS (
  {{snippet: @yenhm GBQ.date_trunc}}
  {{snippet: @vinhnp1 standard_online_fulltime_driver}}
),

online_all AS ( ... ),  -- giống trên

nim_cohorts AS ( ... ), -- giống trên

-- Online hours tại M+2 (tháng thứ 3 của cohort)
online_at_m2 AS (
  SELECT
    c.cohort_month,
    c.supplier_id,
    c.city_id,
    o.online_hours,
    CASE
      WHEN o.online_hours IS NULL THEN 'churned'
      WHEN o.online_hours >= st.standard_hour THEN 'FT'
      ELSE 'PT'
    END AS segment_at_m2
  FROM nim_cohorts c
  LEFT JOIN online_all o
    ON  o.supplier_id  = c.supplier_id
    AND o.city_id      = c.city_id
    AND o.period_month = DATE_ADD(c.cohort_month, INTERVAL 2 MONTH)
  LEFT JOIN standard st
    ON st.time = DATE_ADD(c.cohort_month, INTERVAL 2 MONTH)
)

SELECT
  cohort_month,
  city_id,
  COUNT(DISTINCT supplier_id)                                              AS cohort_size,
  COUNT(DISTINCT CASE WHEN segment_at_m2 = 'FT'      THEN supplier_id END) AS graduated_ft,
  COUNT(DISTINCT CASE WHEN segment_at_m2 = 'PT'      THEN supplier_id END) AS graduated_pt,
  COUNT(DISTINCT CASE WHEN segment_at_m2 = 'churned' THEN supplier_id END) AS churned_at_m2,
  ROUND(COUNT(DISTINCT CASE WHEN segment_at_m2 = 'FT' THEN supplier_id END) * 100.0 / NULLIF(COUNT(DISTINCT supplier_id),0), 1) AS ft_graduation_pct,
  ROUND(COUNT(DISTINCT CASE WHEN segment_at_m2 = 'PT' THEN supplier_id END) * 100.0 / NULLIF(COUNT(DISTINCT supplier_id),0), 1) AS pt_graduation_pct
FROM online_at_m2
GROUP BY 1, 2
ORDER BY city_id, cohort_month
*/
