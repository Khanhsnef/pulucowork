-- ============================================================
-- QUERY 2: Driver Monthly Activity — Driver-level grain
-- Source chính: ahamove_archive_ops.fct_supplier_performance
--               + ahamove_archive_ops.driver_performance_monthly
-- Thêm so với query gốc:
--   + supplier_id trong output
--   + driver_life_time (segment), fct_month (NIM cohort)
--   + order_income, reward_income, EPH
--   + Bỏ GROUP BY city để giữ driver-level
-- Output: 1 row = 1 driver × 1 tháng (chỉ active drivers)
-- Dùng cho: EPH analysis, cohort prep, segment performance
-- ============================================================

{{snippet: @yenhm GBQ.date_trunc}}

WITH ranking_monthly AS (
  SELECT
    period,
    city_id,
    supplier_id,
    driver_life_time,
    ft_segment,
    next_driver_life_time,
    next_ft_segment
  FROM ahamove_archive_ops.driver_performance_monthly
  WHERE period >= DATE_SUB(DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon'), INTERVAL 1 MONTH)
    AND period <= DATE(TIMESTAMP({{end_date}}), 'Asia/Saigon')
    -- NOTE: gốc lấy 2 tháng trước, rút xuống 1 tháng trước vì
    --       chỉ cần classify tháng hiện tại
),

cancel_poc AS (
  SELECT
    supplier_id,
    datetrunc_mock(TIMESTAMP(order_date, 'Asia/Saigon'), 'month') AS period,
    COUNT(CASE
      WHEN cancel_comment LIKE '%for supplier%'
        OR cancel_comment LIKE '%Driver ask%'
        OR cancel_comment LIKE '%by Driver%'
        OR cancel_comment LIKE '%by Supplier%'
        OR cancel_comment LIKE '%by supplier%'
        OR cancel_by = 'supplier'
      THEN order_id END)                                          AS driver_cancel,
    COUNT(CASE
      WHEN reason_type = 'poc'
       AND (cancel_comment LIKE '%for supplier%'
         OR cancel_comment LIKE '%Driver ask%'
         OR cancel_comment LIKE '%by Driver%'
         OR cancel_comment LIKE '%by Supplier%'
         OR cancel_comment LIKE '%by supplier%'
         OR cancel_by = 'supplier')
      THEN order_id END)                                          AS cancel_poc
  FROM ahamove_archive_ops.fact_cancellation_detail
  WHERE order_date >= DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon')
    AND order_date <= DATE(TIMESTAMP({{end_date}}),   'Asia/Saigon')
    AND supplier_id IS NOT NULL
  GROUP BY 1, 2
),

-- Performance hàng tháng per driver (dùng 'month' thay vì {{timeview}})
driver_perf_monthly AS (
  SELECT
    datetrunc_mock(TIMESTAMP(p.period, 'Asia/Saigon'), 'month') AS period,
    p.supplier_id,
    datetrunc_mock(s.first_complete_time, 'month')               AS fct_month,
    SUM(p.stp_complete)                                          AS stp_complete,
    SUM(p.reward_income_pit1_5)                                  AS reward_income,
    SUM(p.order_income)                                          AS order_income,
    SUM(p.accept_order)                                          AS accept_order,
    SUM(p.cancel_order)                                          AS cancel_order,
    SUM(p.noti_accept + p.noti_assign)                           AS accept_noti,
    SUM(p.noti_assign + p.noti_accept + p.noti_dismiss
        + p.noti_timeout + p.noti_not_updated)                   AS total_noti,
    SUM(p.rating_5star + p.rating_4star + p.rating_3star
        + p.rating_2star + p.rating_1star)                       AS rating_order,
    SUM(p.rating_5star*5 + p.rating_4star*4 + p.rating_3star*3
        + p.rating_2star*2 + p.rating_1star)                     AS rating_star,
    SUM(p.rating_4star + p.rating_3star + p.rating_2star
        + p.rating_1star)                                        AS bad_rating_order
  FROM ahamove_archive_ops.fct_supplier_performance p
  LEFT JOIN ahamove_supplier_raw.supplier_raw s ON p.supplier_id = s.id
  WHERE p.period >= DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon')
    AND p.period <= DATE(TIMESTAMP({{end_date}}),   'Asia/Saigon')
    AND JSON_EXTRACT_SCALAR(p.extra, '$.vehicle_type') IN ('MOTORBIKE', 'EV-BIKE')
    AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
    AND COALESCE(s.tags,     'a') NOT LIKE '%SALESFORCE%'
    AND s.partitioned_create_time >= '2010-01-01'
  GROUP BY 1, 2, 3
),

online_monthly AS (
  SELECT
    datetrunc_mock(TIMESTAMP(period, 'Asia/Saigon'), 'month') AS period,
    supplier_id,
    SUM(online_hours)                                          AS online_hours
  FROM ahamove_archive.ops_suppliers_online_hours
  WHERE period >= DATE(TIMESTAMP({{start_date}}), 'Asia/Saigon')
    AND period <= DATE(TIMESTAMP({{end_date}}),   'Asia/Saigon')
  GROUP BY 1, 2
)

-- ============================================================
-- OUTPUT: Driver-level × tháng
-- ============================================================
SELECT
  d.period,
  COALESCE(
    m.city_id,
    CASE WHEN sp.city_id IN ('HAN','SGN') THEN sp.city_id ELSE 'EXP' END
  )                                                            AS city_id,
  d.supplier_id,

  -- Segment (từ driver_performance_monthly — đã classify sẵn)
  -- ⚠️ Khanh verify: driver_life_time có giá trị NIM/NLM/FT/PT/Return không?
  m.driver_life_time                                           AS segment,
  m.ft_segment,
  m.next_driver_life_time                                      AS next_segment,   -- dùng cho transition matrix
  d.fct_month,                                                                    -- NIM cohort identifier

  -- Performance
  d.stp_complete,
  d.order_income,
  d.reward_income,
  d.order_income + d.reward_income                             AS gross_income,

  -- Online & productivity
  o.online_hours,
  ROUND(SAFE_DIVIDE(d.stp_complete,  o.online_hours), 2)      AS stp_per_hour,
  ROUND(SAFE_DIVIDE(d.order_income,  o.online_hours), 0)      AS order_income_per_hour,  -- EPH organic
  ROUND(SAFE_DIVIDE(d.order_income + d.reward_income,
                    o.online_hours), 0)                        AS gross_income_per_hour,  -- EPH total
  ROUND(SAFE_DIVIDE(d.reward_income,
                    NULLIF(d.order_income + d.reward_income, 0)),
        3)                                                     AS incentive_ratio,        -- IDI

  -- Acceptance & cancel
  d.accept_order,
  d.cancel_order,
  COALESCE(cp.cancel_poc, 0)                                   AS cancel_poc,
  COALESCE(SAFE_DIVIDE(d.accept_noti, d.total_noti), 1)       AS ar,
  COALESCE(SAFE_DIVIDE(d.cancel_order, d.accept_order), 0)    AS cr,
  COALESCE(SAFE_DIVIDE(d.cancel_order - 0.5 * COALESCE(cp.cancel_poc, 0),
                       d.accept_order), 0)                     AS cr_kpi,

  -- Rating
  d.rating_order,
  COALESCE(SAFE_DIVIDE(d.rating_star, d.rating_order), 5)     AS rating,
  d.bad_rating_order,

  -- Quality flags (để filter nhanh)
  CASE WHEN COALESCE(SAFE_DIVIDE(d.accept_noti, d.total_noti), 1) >= 0.8  THEN 1 ELSE 0 END AS is_hard_driver,
  CASE WHEN COALESCE(SAFE_DIVIDE(d.cancel_order, d.accept_order), 0) <= 0.1 THEN 1 ELSE 0 END AS is_lcd_driver,
  CASE WHEN COALESCE(SAFE_DIVIDE(d.rating_star,  d.rating_order), 5) >= 4.9 THEN 1 ELSE 0 END AS is_gdr_driver

FROM driver_perf_monthly d
LEFT JOIN online_monthly  o  ON o.supplier_id = d.supplier_id AND o.period = d.period
LEFT JOIN ranking_monthly m  ON m.supplier_id = d.supplier_id
                             AND m.period = DATE_TRUNC(DATE(d.period, 'Asia/Saigon'), MONTH)
                             -- d.period là TIMESTAMP → convert DATE trước khi so sánh với m.period (DATE)
LEFT JOIN cancel_poc      cp ON cp.supplier_id = d.supplier_id AND cp.period = d.period
LEFT JOIN ahamove_raw.raw_supplier_profile sp ON sp.id = d.supplier_id

WHERE d.stp_complete > 0   -- chỉ active drivers (có hoàn thành đơn)
ORDER BY d.supplier_id, d.period
