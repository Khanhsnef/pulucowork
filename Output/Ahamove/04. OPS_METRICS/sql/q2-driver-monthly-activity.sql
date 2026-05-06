-- ============================================================
-- QUERY 2: Driver Monthly Activity — Driver-level grain
-- Mục đích: Lấy supplier_id × month để làm retention analysis,
--           segment transition matrix, EPH, individual tracking
-- Output: 1 row = 1 driver × 1 tháng (bao gồm tháng inactive)
-- Chạy: {{start_date}} = tháng đầu range, {{end_date}} = tháng cuối range
-- ============================================================

WITH standard AS (
  {{snippet: @yenhm GBQ.date_trunc}}
  {{snippet: @vinhnp1 standard_online_fulltime_driver}}
),

-- Date spine: tất cả các tháng trong range cần phân tích
month_spine AS (
  SELECT month_start
  FROM UNNEST(
    GENERATE_DATE_ARRAY(
      DATE_TRUNC(DATE({{start_date}}), MONTH),
      DATE_TRUNC(DATE({{end_date}}),   MONTH),
      INTERVAL 1 MONTH
    )
  ) AS month_start
),

-- Online hours cho toàn bộ range + 1 tháng trước (để classify segment tháng đầu)
online_all AS (
  SELECT
    datetrunc_mock(TIMESTAMP(r.period, 'Asia/Saigon'), 'month') AS period_month,
    r.supplier_id,
    s.first_complete_time,
    datetrunc_mock(s.first_complete_time, 'month')              AS first_complete_month,
    r.city_id,
    SUM(r.online_hours)                                         AS online_hours
  FROM ahamove_archive.ops_suppliers_online_hours r
  LEFT JOIN `aha-move`.ahamove_supplier_raw.supplier_raw s ON r.supplier_id = s.id
  WHERE r.period >= DATE_SUB(DATE_TRUNC(DATE({{start_date}}), MONTH), INTERVAL 1 MONTH)
    AND r.period <  DATE_ADD(DATE_TRUNC(DATE({{end_date}}), MONTH), INTERVAL 1 MONTH)
    AND COALESCE(s.vehicle_type, 'MOTORBIKE') = 'MOTORBIKE'
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND s.tags NOT LIKE '%SALESFORCE%'
  GROUP BY 1, 2, 3, 4, 5
),

-- Completed stoppoints per driver per month (từ raw_performance)
stops_by_month AS (
  SELECT
    r.supplier_id,
    LEFT(r.service_id, 3)                                          AS city_id,
    datetrunc_mock(TIMESTAMP(r.order_date, 'Asia/Saigon'), 'month') AS period_month,
    COUNT(DISTINCT r.stop_id)                                       AS completed_stops,
    COUNT(DISTINCT r.order_id)                                      AS completed_orders
  FROM ahamove_raw.raw_performance r
  WHERE r.order_date >= DATE({{start_date}})
    AND r.order_date <  DATE_ADD(DATE_TRUNC(DATE({{end_date}}), MONTH), INTERVAL 1 MONTH)
    AND r.status = 'COMPLETED'
    AND LEFT(r.service_id, 3) != 'VNM'
    {{snippet: @vinhnp1 condition_kpi}}
  GROUP BY 1, 2, 3
),

-- Segment mỗi driver × mỗi tháng dựa trên online hours tháng TRƯỚC
-- Logic nhất quán với query gốc:
--   NIM    = first_complete_month = period_month (tháng đầu tiên)
--   NLM    = first_complete_month = period_month - 1 (họ là NIM tháng trước)
--   FT     = active tháng trước, online >= standard
--   PT     = active tháng trước, online < standard
--   Return = active tháng N-2, inactive tháng N-1, active tháng N
--   (inactive hoàn toàn = không có row trong kết quả)
driver_segments AS (
  SELECT
    cur.period_month,
    cur.supplier_id,
    cur.city_id,
    cur.online_hours                         AS cur_online_hours,
    COALESCE(prev.online_hours, 0)           AS prev_online_hours,
    cur.first_complete_month,
    CASE
      WHEN cur.first_complete_month = cur.period_month
        THEN 'NIM'
      WHEN cur.first_complete_month
             = DATE_SUB(cur.period_month, INTERVAL 1 MONTH)
        THEN 'NLM'
      WHEN prev.online_hours IS NOT NULL
       AND prev.online_hours >= st.standard_hour
        THEN 'FT'
      WHEN prev.online_hours IS NOT NULL
       AND prev.online_hours < st.standard_hour
        THEN 'PT'
      -- Return: đã từng active (first_complete_month < period_month),
      --         inactive tháng N-1 (prev.online_hours IS NULL), nay quay lại
      --         Không giới hạn số tháng inactive — churn ≥1 tháng bất kỳ đều là Return
      WHEN prev.online_hours IS NULL
       AND cur.first_complete_month < cur.period_month
        THEN 'Return'
    END AS segment
  FROM online_all cur
  -- Tháng trước (N-1)
  LEFT JOIN online_all prev
    ON  prev.supplier_id    = cur.supplier_id
    AND prev.city_id        = cur.city_id
    AND prev.period_month   = DATE_SUB(cur.period_month, INTERVAL 1 MONTH)
  LEFT JOIN standard st ON st.time = cur.period_month
  -- Chỉ lấy các tháng trong range cần phân tích (bỏ tháng N-1 dùng để classify)
  WHERE cur.period_month >= DATE_TRUNC(DATE({{start_date}}), MONTH)
    AND cur.period_month <= DATE_TRUNC(DATE({{end_date}}),   MONTH)
)

-- ============================================================
-- OUTPUT: 1 row = 1 driver × 1 tháng
-- Dùng để:
--   - Cohort retention (group by first_complete_month)
--   - Segment transition (self-join với lag 1 tháng)
--   - EPH (cần thêm earnings khi có)
--   - Productivity: avg_stops_per_online_hour
-- ============================================================
SELECT
  ds.period_month,
  ds.supplier_id,
  ds.city_id,
  ds.segment,
  ds.first_complete_month,                 -- NIM cohort identifier
  ds.cur_online_hours        AS online_hours,
  ds.prev_online_hours,                    -- Để phân tích downgrade trend

  -- Stoppoints & orders (từ raw_performance)
  COALESCE(sp.completed_stops,  0)         AS completed_stops,
  COALESCE(sp.completed_orders, 0)         AS completed_orders,

  -- Productivity: stops per online hour
  CASE
    WHEN ds.cur_online_hours > 0
    THEN ROUND(COALESCE(sp.completed_stops, 0) / ds.cur_online_hours, 2)
    ELSE NULL
  END                                      AS stops_per_hour,

  -- Flag hữu ích cho transition analysis
  CASE WHEN ds.cur_online_hours >= 150 THEN 1 ELSE 0 END AS is_ft_eligible,

  1                                        AS is_active  -- Tất cả row này đều active

FROM driver_segments ds
LEFT JOIN stops_by_month sp
  ON  sp.supplier_id  = ds.supplier_id
  AND sp.city_id      = ds.city_id
  AND sp.period_month = ds.period_month

-- Loại long_inactive nếu không cần phân tích nhóm này
-- WHERE ds.segment != 'Return'  -- bỏ comment nếu muốn loại Return khỏi output

ORDER BY ds.supplier_id, ds.city_id, ds.period_month
