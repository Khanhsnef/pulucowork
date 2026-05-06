-- ============================================================
-- QUERY 1: Active Driver Trend (FIXED + ENHANCED)
-- Fix so với query gốc:
--   BUG 1: Trailing comma trước FROM (syntax error) → đã xóa
--   BUG 2: Condition "period = time" redundant → đã bỏ
-- Thêm: total_stops, avg_stops_per_driver (productivity proxy)
-- Return: giữ nguyên logic gốc (= bất kỳ driver active kỳ này
--         mà KHÔNG có trong segment NIM/NLM/FT/PT = đã từng active,
--         churn ≥1 tháng bất kỳ, rồi quay lại)
-- Output grain: city × order_date × month × week × segment
-- ============================================================

{{snippet: @yenhm GBQ.date_trunc}}

WITH standard AS (
  {{snippet: @vinhnp1 standard_online_fulltime_driver}}
  -- Assumed output columns: (time TIMESTAMP, standard_hour FLOAT)
),

-- [Tháng N-1] Online hours để classify FT / PT / NLM
online_prev_month AS (
  SELECT
    datetrunc_mock(TIMESTAMP(r.period, 'Asia/Saigon'), 'month') AS period,
    r.supplier_id,
    datetrunc_mock(s.first_complete_time, 'month')              AS first_complete_month,
    r.city_id,
    SUM(r.online_hours)                                         AS online_hours
  FROM ahamove_archive.ops_suppliers_online_hours r
  LEFT JOIN `aha-move`.ahamove_supplier_raw.supplier_raw s ON r.supplier_id = s.id
  WHERE r.period >= DATE_SUB(datetrunc_mock(TIMESTAMP({{start_date}}), 'month'), INTERVAL 1 MONTH)
    AND r.period <  datetrunc_mock(TIMESTAMP({{start_date}}), 'month')
    AND COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND s.tags NOT LIKE '%SALESFORCE%'
  GROUP BY 1, 2, 3, 4
),

-- Classify FT / PT / NLM từ online tháng N-1
segment_established AS (
  SELECT
    o.supplier_id,
    o.city_id,
    CASE
      -- NLM: first_complete_month = tháng N-1 → NIM tháng trước → NLM tháng này
      WHEN o.first_complete_month = o.period  THEN 'NLM'
      WHEN o.online_hours >= st.standard_hour THEN 'FT'
      WHEN o.online_hours <  st.standard_hour THEN 'PT'
    END AS segment
  FROM online_prev_month o
  LEFT JOIN standard st ON st.time = o.period
),

-- NIM: first_complete_time nằm trong tháng start_date
nim_drivers AS (
  SELECT
    s.id    AS supplier_id,
    s.city_id,
    'NIM'   AS segment
  FROM `aha-move`.ahamove_supplier_raw.supplier_raw s
  WHERE datetrunc_mock(s.first_complete_time, 'month')
          = datetrunc_mock(TIMESTAMP({{start_date}}), 'month')
    AND COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND s.tags NOT LIKE '%SALESFORCE%'
),

all_segments AS (
  SELECT supplier_id, city_id, segment FROM segment_established
  UNION ALL
  SELECT supplier_id, city_id, segment FROM nim_drivers
),

-- Performance trong kỳ phân tích, đính kèm segment
-- Return = COALESCE(segment, 'Return'):
--   driver complete đơn kỳ này nhưng không có trong all_segments
--   = đã từng active trước đây, inactive ≥1 tháng, nay quay lại
perf AS (
  SELECT
    r.supplier_id,
    r.city_id,
    r.order_date,
    r.stop_id,
    r.service_id,
    r.service_short,
    COALESCE(s.segment, 'Return')                  AS segment
  FROM (
    SELECT
      supplier_id,
      user_id,
      LEFT(service_id, 3)                          AS city_id,
      order_date,
      stop_id,
      service_id,
      RIGHT(service_id, LENGTH(service_id) - 4)    AS service_short,
      status,
      cancel_time,
      order_time,
      payment_method,
      payment_time,
      partner,
      cancel_comment,
      cancel_by_user
    FROM ahamove_raw.raw_performance
  ) r
  LEFT JOIN all_segments s
    ON  s.supplier_id = r.supplier_id
    AND s.city_id     = r.city_id
  WHERE r.order_date >= DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon')
    AND r.order_date <  DATE(TIMESTAMP({{end_date}}),   'Asia/Saigon')
    {{snippet: @vinhnp1 condition_kpi}}
    AND r.status = 'COMPLETED'
    AND r.city_id != 'VNM'
)

SELECT
  CASE
    WHEN city_id NOT IN ('SGN','HAN') THEN 'EXP'
    ELSE city_id
  END                                                            AS city_id,
  order_date,
  datetrunc_mock(TIMESTAMP(order_date, 'Asia/Saigon'), 'month') AS month,
  datetrunc_mock(TIMESTAMP(order_date, 'Asia/Saigon'), 'week')  AS week,
  segment                                                        AS tag,

  -- Active driver count (unique)
  COUNT(DISTINCT supplier_id)                                    AS total_active,

  -- By service group
  COUNT(DISTINCT CASE WHEN service_short IN ('BIKE','EXPRESS','ECO','AIBOT','POOL')                        THEN supplier_id END) AS active_1h,
  COUNT(DISTINCT CASE WHEN service_short IN ('TMDT','2H','2H-PUBLIC','2H-PUBLIC-BULKY','TMDT-LOW','BULKY') THEN supplier_id END) AS active_2h,
  COUNT(DISTINCT CASE WHEN service_short IN ('SAMEDAY','SAMEPRICE')                                        THEN supplier_id END) AS active_4h,

  -- Service detail
  COUNT(DISTINCT CASE WHEN service_short = 'BIKE'                          THEN supplier_id END) AS bike,
  COUNT(DISTINCT CASE WHEN service_short = 'ECO'                           THEN supplier_id END) AS eco,
  COUNT(DISTINCT CASE WHEN service_short = 'AIBOT'                         THEN supplier_id END) AS aibot,
  COUNT(DISTINCT CASE WHEN service_short = 'AIFOOD'                        THEN supplier_id END) AS aifood,
  COUNT(DISTINCT CASE WHEN service_short = 'POOL'                          THEN supplier_id END) AS pool,
  COUNT(DISTINCT CASE WHEN service_short IN ('TMDT','TMDT-LOW')            THEN supplier_id END) AS tmdt,
  COUNT(DISTINCT CASE WHEN service_short IN ('2H','2H-PUBLIC')             THEN supplier_id END) AS _2h,
  COUNT(DISTINCT CASE WHEN service_short IN ('BULKY','2H-PUBLIC-BULKY')    THEN supplier_id END) AS _2h_bulky,
  COUNT(DISTINCT CASE WHEN service_short = 'INDAY'                         THEN supplier_id END) AS inday,

  -- Stoppoints (THÊM MỚI — proxy cho prod / avg stoppoints hiện có)
  COUNT(DISTINCT stop_id)                                        AS total_stops,
  COUNT(DISTINCT CASE WHEN service_short IN ('BIKE','EXPRESS','ECO','AIBOT','POOL')                        THEN stop_id END) AS stops_1h,
  COUNT(DISTINCT CASE WHEN service_short IN ('TMDT','2H','2H-PUBLIC','2H-PUBLIC-BULKY','TMDT-LOW','BULKY') THEN stop_id END) AS stops_2h,
  COUNT(DISTINCT CASE WHEN service_short IN ('SAMEDAY','SAMEPRICE')                                        THEN stop_id END) AS stops_4h,

  -- Avg stops per active driver (THÊM MỚI)
  ROUND(
    COUNT(DISTINCT stop_id) / NULLIF(COUNT(DISTINCT supplier_id), 0),
    2
  )                                                              AS avg_stops_per_driver

FROM perf
GROUP BY 1, 2, 3, 4, 5
ORDER BY 1, 2, 3, 4, 5
