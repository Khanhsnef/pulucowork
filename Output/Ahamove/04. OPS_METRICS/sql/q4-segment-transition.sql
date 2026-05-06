-- ============================================================
-- QUERY 4: Segment Transition Matrix
-- Source: ahamove_archive_ops.driver_performance_monthly
--         (đã có driver_life_time + next_driver_life_time sẵn)
-- Output: from_segment × to_segment × count + performance KPIs
-- Dùng cho: Tìm điểm rò rỉ — FT → PT bao nhiêu? PT → Churn bao nhiêu?
-- ============================================================
-- ⚠️ Cần verify giá trị driver_life_time và next_driver_life_time:
--    Ví dụ: 'NIM', 'NLM', 'FT', 'PT', 'Return', 'Churn'?
--    Chạy SELECT DISTINCT driver_life_time FROM driver_performance_monthly LIMIT 50
--    để xác nhận trước khi dùng query này
-- ============================================================

{{snippet: @yenhm GBQ.date_trunc}}

WITH

transition_raw AS (
  SELECT
    m.period,
    m.city_id,
    m.supplier_id,
    m.driver_life_time                           AS from_segment,
    m.ft_segment                                 AS from_ft_segment,
    -- next_driver_life_time = segment tháng sau của driver này
    -- NULL = driver churn (không active tháng sau)
    COALESCE(m.next_driver_life_time, 'Churn')   AS to_segment,
    COALESCE(m.next_ft_segment, 'Churn')         AS to_ft_segment
  FROM ahamove_archive_ops.driver_performance_monthly m
  WHERE m.period >= DATE_TRUNC(DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon'), MONTH)
    AND m.period <= DATE_TRUNC(DATE(TIMESTAMP({{end_date}}), 'Asia/Saigon'), MONTH)
    AND m.city_id IN ('HAN', 'SGN')   -- bỏ comment nếu muốn EXP
)

-- ============================================================
-- OUTPUT A: Transition count + % theo from_segment
-- ============================================================
SELECT
  city_id,
  from_segment,
  to_segment,
  COUNT(DISTINCT supplier_id)                    AS driver_count,

  -- % trong số drivers từ segment đó đi về đâu
  ROUND(
    COUNT(DISTINCT supplier_id) * 100.0
    / NULLIF(SUM(COUNT(DISTINCT supplier_id)) OVER (
        PARTITION BY city_id, from_segment
      ), 0),
    1
  )                                              AS pct_of_from_segment

FROM transition_raw
GROUP BY 1, 2, 3
ORDER BY city_id, from_segment, driver_count DESC


-- ============================================================
-- OUTPUT B (chạy riêng): Transition theo từng tháng — thấy xu hướng thay đổi
-- ============================================================
/*
SELECT
  period,
  city_id,
  from_segment,
  to_segment,
  COUNT(DISTINCT supplier_id) AS driver_count
FROM transition_raw
GROUP BY 1, 2, 3, 4
ORDER BY period, city_id, from_segment, driver_count DESC
*/


-- ============================================================
-- OUTPUT C (chạy riêng): FT churn vs downgrade — câu hỏi cốt lõi
-- Điều kiện: from_segment = 'FT' (hoặc ft_segment = 'FT')
-- ============================================================
-- driver_life_time dùng 'OLD' (không phân biệt FT/PT) → phải dùng ft_segment/next_ft_segment
SELECT
  period,
  city_id,
  COUNT(DISTINCT CASE WHEN to_ft_segment = 'FT'    THEN supplier_id END) AS retained_ft,
  COUNT(DISTINCT CASE WHEN to_ft_segment = 'PT'    THEN supplier_id END) AS downgraded_to_pt,
  COUNT(DISTINCT CASE WHEN to_ft_segment = 'Churn' THEN supplier_id END) AS churned,
  COUNT(DISTINCT CASE WHEN to_segment    = 'Return'THEN supplier_id END) AS went_return,
  COUNT(DISTINCT supplier_id)                                             AS total_ft,

  ROUND(COUNT(DISTINCT CASE WHEN to_ft_segment = 'PT'    THEN supplier_id END) * 100.0
        / NULLIF(COUNT(DISTINCT supplier_id), 0), 1) AS downgrade_pct,
  ROUND(COUNT(DISTINCT CASE WHEN to_ft_segment = 'Churn' THEN supplier_id END) * 100.0
        / NULLIF(COUNT(DISTINCT supplier_id), 0), 1) AS churn_pct

FROM transition_raw
WHERE from_ft_segment = 'FT'
GROUP BY 1, 2
ORDER BY period, city_id
