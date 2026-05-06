-- ============================================================
-- QUERY 1: Active Driver Trend (FIXED + ENHANCED)
-- Sửa: trailing comma, Return definition, redundant condition
-- Thêm: stop counts, Return chính xác (skip exactly 1 month)
-- Output grain: city × date × week × month × segment
-- ============================================================

WITH standard AS (
  {{snippet: @yenhm GBQ.date_trunc}}
  {{snippet: @vinhnp1 standard_online_fulltime_driver}}
  -- Assumed output: (time TIMESTAMP, standard_hour FLOAT)
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

-- [Tháng N-2] Dùng để xác định Return đúng định nghĩa:
-- Return = active tháng N-2, INACTIVE tháng N-1, active tháng N
-- Không có online hours tháng N-2 → không phải Return thực
online_2m_ago AS (
  SELECT DISTINCT r.supplier_id, r.city_id
  FROM ahamove_archive.ops_suppliers_online_hours r
  LEFT JOIN `aha-move`.ahamove_supplier_raw.supplier_raw s ON r.supplier_id = s.id
  WHERE r.period >= DATE_SUB(datetrunc_mock(TIMESTAMP({{start_date}}), 'month'), INTERVAL 2 MONTH)
    AND r.period <  DATE_SUB(datetrunc_mock(TIMESTAMP({{start_date}}), 'month'), INTERVAL 1 MONTH)
    AND COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND s.tags NOT LIKE '%SALESFORCE%'
),

-- Classify FT / PT / NLM từ online tháng N-1
segment_established AS (
  SELECT
    o.supplier_id,
    o.city_id,
    o.online_hours AS prev_online_hours,
    CASE
      -- NLM: first_complete_month = tháng N-1 → họ là NIM tháng trước → NLM tháng này
      WHEN o.first_complete_month = o.period             THEN 'NLM'
      WHEN o.online_hours >= st.standard_hour            THEN 'FT'
      WHEN o.online_hours <  st.standard_hour            THEN 'PT'
    END AS segment
  FROM online_prev_month o
  LEFT JOIN standard st ON st.time = o.period
),

-- NIM: first_complete_time nằm trong tháng start_date
nim_drivers AS (
  SELECT
    s.id         AS supplier_id,
    s.city_id,
    'NIM'        AS segment,
    NULL         AS prev_online_hours
  FROM `aha-move`.ahamove_supplier_raw.supplier_raw s
  WHERE datetrunc_mock(s.first_complete_time, 'month')
          = datetrunc_mock(TIMESTAMP({{start_date}}), 'month')
    AND COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND s.tags NOT LIKE '%SALESFORCE%'
),

all_segments AS (
  SELECT supplier_id, city_id, segment, prev_online_hours FROM segment_established
  UNION ALL
  SELECT supplier_id, city_id, segment, prev_online_hours FROM nim_drivers
),

-- Performance trong kỳ phân tích, đính kèm segment
perf AS (
  SELECT
    r.supplier_id,
    LEFT(r.service_id, 3)                          AS city_id,
    r.order_date,
    r.stop_id,
    r.service_id,
    RIGHT(r.service_id, LENGTH(r.service_id) - 4)  AS service_short,
    CASE
      WHEN s.segment IS NOT NULL     THEN s.segment
      -- Return ĐÚNG: có online tháng N-2, KHÔNG có online tháng N-1
      WHEN two_m.supplier_id IS NOT NULL THEN 'Return'
      -- Long inactive (>1 tháng): không phân loại vào Return
      ELSE 'long_inactive'
    END AS segment
  FROM ahamove_raw.raw_performance r
  LEFT JOIN all_segments   s     ON s.supplier_id   = r.supplier_id
                                 AND s.city_id       = LEFT(r.service_id, 3)
  LEFT JOIN online_2m_ago  two_m ON two_m.supplier_id = r.supplier_id
                                 AND two_m.city_id    = LEFT(r.service_id, 3)
  WHERE r.order_date >= DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon')
    AND r.order_date <  DATE(TIMESTAMP({{end_date}}),   'Asia/Saigon')
    {{snippet: @vinhnp1 condition_kpi}}
    AND r.status = 'COMPLETED'
    AND LEFT(r.service_id, 3) != 'VNM'
)

SELECT
  CASE
    WHEN city_id NOT IN ('SGN','HAN') THEN 'EXP'
    ELSE city_id
  END                                                          AS city_id,
  order_date,
  datetrunc_mock(TIMESTAMP(order_date, 'Asia/Saigon'), 'month') AS month,
  datetrunc_mock(TIMESTAMP(order_date, 'Asia/Saigon'), 'week')  AS week,
  segment                                                        AS tag,

  -- === Active driver count (unique) ===
  COUNT(DISTINCT supplier_id)                                    AS total_active,

  -- By service group
  COUNT(DISTINCT CASE WHEN service_short IN ('BIKE','EXPRESS','ECO','AIBOT','POOL')              THEN supplier_id END) AS active_1h,
  COUNT(DISTINCT CASE WHEN service_short IN ('TMDT','2H','2H-PUBLIC','2H-PUBLIC-BULKY','TMDT-LOW','BULKY') THEN supplier_id END) AS active_2h,
  COUNT(DISTINCT CASE WHEN service_short IN ('SAMEDAY','SAMEPRICE')                              THEN supplier_id END) AS active_4h,

  -- Service detail
  COUNT(DISTINCT CASE WHEN service_short = 'BIKE'                                 THEN supplier_id END) AS bike,
  COUNT(DISTINCT CASE WHEN service_short = 'ECO'                                  THEN supplier_id END) AS eco,
  COUNT(DISTINCT CASE WHEN service_short = 'AIBOT'                                THEN supplier_id END) AS aibot,
  COUNT(DISTINCT CASE WHEN service_short = 'AIFOOD'                               THEN supplier_id END) AS aifood,
  COUNT(DISTINCT CASE WHEN service_short = 'POOL'                                 THEN supplier_id END) AS pool,
  COUNT(DISTINCT CASE WHEN service_short IN ('TMDT','TMDT-LOW')                   THEN supplier_id END) AS tmdt,
  COUNT(DISTINCT CASE WHEN service_short IN ('2H','2H-PUBLIC')                    THEN supplier_id END) AS _2h,
  COUNT(DISTINCT CASE WHEN service_short IN ('BULKY','2H-PUBLIC-BULKY')           THEN supplier_id END) AS _2h_bulky,
  COUNT(DISTINCT CASE WHEN service_short = 'INDAY'                                THEN supplier_id END) AS inday,

  -- === Stoppoints (THÊM MỚI) — proxy cho prod ===
  COUNT(DISTINCT stop_id)                                        AS total_stops,
  COUNT(DISTINCT CASE WHEN service_short IN ('BIKE','EXPRESS','ECO','AIBOT','POOL')              THEN stop_id END) AS stops_1h,
  COUNT(DISTINCT CASE WHEN service_short IN ('TMDT','2H','2H-PUBLIC','2H-PUBLIC-BULKY','TMDT-LOW','BULKY') THEN stop_id END) AS stops_2h,
  COUNT(DISTINCT CASE WHEN service_short IN ('SAMEDAY','SAMEPRICE')                              THEN stop_id END) AS stops_4h,

  -- === Avg stops per active driver (THÊM MỚI) — productivity proxy ===
  ROUND(COUNT(DISTINCT stop_id) / NULLIF(COUNT(DISTINCT supplier_id), 0), 2) AS avg_stops_per_driver

FROM perf
-- Loại long_inactive nếu không muốn show (hoặc giữ để monitor)
-- WHERE segment != 'long_inactive'
GROUP BY 1, 2, 3, 4, 5
ORDER BY 1, 2, 3, 4, 5
