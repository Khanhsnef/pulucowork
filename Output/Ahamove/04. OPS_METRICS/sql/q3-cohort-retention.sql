-- ============================================================
-- QUERY 3A: Cohort Retention — NIM cohort → retention M+1...M+12
-- Source: driver_performance_monthly (đã có segment per driver per month)
--         + fct_supplier_performance (để lấy fct_month = NIM cohort)
-- Output: cohort_month × city_id × months_after → retention_pct
-- ============================================================
-- Cách đọc:
--   months_after = 0 → tháng NIM (100% by definition)
--   months_after = 1 → tháng NLM (% còn active)
--   months_after = 2 → tháng đầu tiên FT/PT
--   months_after = N → retention M+N
-- ============================================================

{{snippet: @yenhm GBQ.date_trunc}}

WITH

-- Lấy fct_month (tháng đầu hoàn thành đơn = NIM cohort) cho từng driver
driver_fct AS (
  SELECT DISTINCT
    p.supplier_id,
    datetrunc_mock(s.first_complete_time, 'month')               AS fct_month,
    s.city_id
  FROM ahamove_archive_ops.fct_supplier_performance p
  LEFT JOIN ahamove_supplier_raw.supplier_raw s ON p.supplier_id = s.id
  WHERE COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
    AND COALESCE(s.tags,     'a') NOT LIKE '%SALESFORCE%'
    AND s.partitioned_create_time >= '2010-01-01'
),

-- NIM cohort: drivers có fct_month trong range phân tích
nim_cohorts AS (
  SELECT
    supplier_id,
    city_id,
    fct_month AS cohort_month
  FROM driver_fct
  WHERE fct_month >= DATE_TRUNC(DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon'), MONTH)
    AND fct_month <= DATE_TRUNC(DATE(TIMESTAMP({{end_date}}), 'Asia/Saigon'), MONTH)
    AND city_id IN ('HAN', 'SGN')   -- bỏ comment nếu muốn cả EXP
),

-- Các tháng driver có active trong driver_performance_monthly
-- (bảng này có row khi driver active = có stp_complete > 0 trong tháng)
active_months AS (
  SELECT
    supplier_id,
    period   -- đã là monthly grain
  FROM ahamove_archive_ops.driver_performance_monthly
  WHERE period >= DATE_TRUNC(DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon'), MONTH)
    AND period <= DATE_ADD(
          DATE_TRUNC(DATE(TIMESTAMP({{end_date}}), 'Asia/Saigon'), MONTH),
          INTERVAL 12 MONTH   -- mở rộng để catch M+12
        )
),

-- Lag steps M+0 → M+12
lag_steps AS (
  SELECT lag_n
  FROM UNNEST(GENERATE_ARRAY(0, 12)) AS lag_n
),

-- Cross join: với mỗi cohort driver × mỗi lag → kiểm tra còn active không
cohort_check AS (
  SELECT
    c.cohort_month,
    c.city_id,
    l.lag_n                                                    AS months_after,
    DATE_ADD(c.cohort_month, INTERVAL l.lag_n MONTH)          AS check_month,
    c.supplier_id,
    CASE WHEN a.supplier_id IS NOT NULL THEN 1 ELSE 0 END     AS is_active
  FROM nim_cohorts c
  CROSS JOIN lag_steps l
  LEFT JOIN active_months a
    ON  a.supplier_id = c.supplier_id
    AND a.period      = DATE_ADD(c.cohort_month, INTERVAL l.lag_n MONTH)
  -- Chỉ giữ check_month không vượt quá end_date + 12 tháng
  WHERE DATE_ADD(c.cohort_month, INTERVAL l.lag_n MONTH)
          <= DATE_ADD(DATE_TRUNC(DATE(TIMESTAMP({{end_date}}), 'Asia/Saigon'), MONTH), INTERVAL 12 MONTH)
)

-- ============================================================
-- OUTPUT A: Retention rate tổng hợp
-- ============================================================
SELECT
  cohort_month,
  city_id,
  months_after,
  check_month,
  COUNT(DISTINCT supplier_id)                                  AS cohort_size,
  COUNT(DISTINCT CASE WHEN is_active = 1 THEN supplier_id END) AS retained,
  ROUND(
    COUNT(DISTINCT CASE WHEN is_active = 1 THEN supplier_id END) * 100.0
    / NULLIF(COUNT(DISTINCT supplier_id), 0),
    1
  )                                                            AS retention_pct
FROM cohort_check
GROUP BY 1, 2, 3, 4
ORDER BY city_id, cohort_month, months_after


-- ============================================================
-- QUERY 3B: Graduation Quality — NIM → FT/PT/Churn tại M+2
-- Bỏ comment query này và chạy riêng khi cần
-- ⚠️ Cần verify giá trị của driver_life_time trước khi dùng
-- ============================================================
/*
WITH nim_cohorts AS ( ... ),  -- giống trên

graduation AS (
  SELECT
    c.cohort_month,
    c.city_id,
    c.supplier_id,
    m.driver_life_time  AS segment_at_m2,   -- ⚠️ verify values: 'FT'/'PT'/NULL?
    m.ft_segment                             -- ⚠️ verify values
  FROM nim_cohorts c
  LEFT JOIN ahamove_archive_ops.driver_performance_monthly m
    ON  m.supplier_id = c.supplier_id
    AND m.period      = DATE_ADD(c.cohort_month, INTERVAL 2 MONTH)
)

SELECT
  cohort_month,
  city_id,
  COUNT(DISTINCT supplier_id)                                        AS cohort_size,
  COUNT(DISTINCT CASE WHEN segment_at_m2 IS NOT NULL THEN supplier_id END) AS survived_m2,
  COUNT(DISTINCT CASE WHEN ft_segment = 'FT'         THEN supplier_id END) AS graduated_ft,
  COUNT(DISTINCT CASE WHEN ft_segment = 'PT'         THEN supplier_id END) AS graduated_pt,
  COUNT(DISTINCT CASE WHEN segment_at_m2 IS NULL     THEN supplier_id END) AS churned_m2,
  ROUND(COUNT(DISTINCT CASE WHEN ft_segment = 'FT' THEN supplier_id END) * 100.0
        / NULLIF(COUNT(DISTINCT supplier_id), 0), 1)                AS ft_graduation_pct,
  ROUND(COUNT(DISTINCT CASE WHEN segment_at_m2 IS NULL THEN supplier_id END) * 100.0
        / NULLIF(COUNT(DISTINCT supplier_id), 0), 1)                AS churn_rate_m2_pct
FROM graduation
GROUP BY 1, 2
ORDER BY city_id, cohort_month
*/
