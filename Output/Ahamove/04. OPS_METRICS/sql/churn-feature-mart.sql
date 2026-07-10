-- ============================================================
-- CHURN FEATURE MART — training set cho Driver Churn Scoring Model
-- Grain: 1 dòng = 1 supplier_id × 1 observation_month
-- Label: activity-gap (NEW ≥14 ngày, OLD ≥30 ngày không có đơn complete)
-- Cohort: NEW = NIM+NLM | OLD = N2M+OLD → train 2 model riêng
-- Scope: Bike Instant (MOTORBIKE + EV-BIKE)
-- ------------------------------------------------------------
-- ⚠️ VERIFY trước khi chạy prod:
--   • driver_life_time values: 'NIM','NLM','N2M','OLD' (đặc biệt N2M)
--   • active_days: đang count từ daily fct — đổi nếu monthly có sẵn
--   • sanction_cnt: nối supplier_sanction khi đã confirm tên field
-- ============================================================

{{snippet: @yenhm GBQ.date_trunc}}

DECLARE start_month DATE DEFAULT '2026-01-01';   -- tháng quan sát đầu
DECLARE end_month   DATE DEFAULT DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY), MONTH);

-- ------------------------------------------------------------
-- B0: Supplier hợp lệ (filter chuẩn Bike Instant)
-- ------------------------------------------------------------
WITH base_supplier AS (
  SELECT
    id                                                          AS supplier_id,
    CASE WHEN city_id IN ('HAN','SGN') THEN city_id ELSE 'EXP' END AS city_id,
    JSON_EXTRACT_SCALAR(extra,'$.vehicle_type')                 AS vehicle_type,
    CASE WHEN JSON_EXTRACT_SCALAR(extra,'$.vehicle_type')='EV-BIKE'
         THEN 1 ELSE 0 END                                      AS is_ev,
    JSON_EXTRACT_SCALAR(extra,'$.gender')                       AS gender,
    SAFE_CAST(RIGHT(JSON_EXTRACT_SCALAR(extra,'$.date_of_birth'),4) AS INT64) AS birth_year,
    first_complete_time
  FROM ahamove_supplier_raw.supplier_raw
  WHERE JSON_EXTRACT_SCALAR(extra,'$.vehicle_type') IN ('MOTORBIKE','EV-BIKE')
    AND COALESCE(email,    'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
    AND COALESCE(tags,     'a') NOT LIKE '%SALESFORCE%'
    AND partitioned_create_time >= '2010-01-01'
),

-- ------------------------------------------------------------
-- B1: Observation grid — mỗi driver active × mỗi tháng quan sát
--     driver_performance_monthly có row khi active (stp_complete>0)
-- ------------------------------------------------------------
obs AS (
  SELECT
    m.supplier_id,
    m.period                                                    AS obs_month,
    m.driver_life_time,
    -- Cohort NEW vs OLD
    CASE
      WHEN m.driver_life_time IN ('NIM','NLM') THEN 'NEW'
      WHEN m.driver_life_time IN ('N2M','OLD') THEN 'OLD'
      ELSE 'OLD'                                                -- fallback an toàn
    END                                                         AS cohort,
    CASE WHEN m.driver_life_time IN ('NIM','NLM') THEN 14 ELSE 30 END AS gap_threshold_days
  FROM ahamove_archive_ops.driver_performance_monthly m
  WHERE m.period BETWEEN start_month AND end_month
    AND m.stp_complete > 0
),

-- ------------------------------------------------------------
-- B2: Đơn complete (daily) — dùng cho label activity-gap + recency
--     Filter đơn chuẩn (bike, non-GHN/truck/test)
-- ------------------------------------------------------------
completed_orders AS (
  SELECT
    supplier_id,
    DATE(order_time, 'Asia/Saigon')                            AS order_date
  FROM ahamove_order_raw.order_raw
  WHERE status = 'COMPLETED'
    AND seq = 0
    AND user_id NOT IN ('84862151477','84862151000')
    AND NOT REGEXP_CONTAINS(service_id,
        '-(INTERCT|TRUCK|RIDE|VAN|PARTNER|TRICYCLE|TEST|PARTNER-BIGC|ASTGROUP|INTERNAL|HUB|BKN|RENT|MASAN)-?')
    AND COALESCE(partner,'ahamove') NOT IN ('ghn','ghnlastmile')
    AND DATE(order_time,'Asia/Saigon') BETWEEN DATE_SUB(start_month, INTERVAL 2 MONTH)
                                           AND LAST_DAY(end_month)
),

-- ------------------------------------------------------------
-- B3: LABEL — activity-gap forward-looking
--     Với mỗi (driver, obs_month): tìm đơn complete cuối ≤ hết obs_month,
--     và đơn complete kế tiếp sau đó. Gap > ngưỡng cohort → churn.
-- ------------------------------------------------------------
label AS (
  SELECT
    o.supplier_id,
    o.obs_month,
    o.gap_threshold_days,
    -- đơn cuối trong/đến hết obs_month
    MAX(CASE WHEN c.order_date <= LAST_DAY(o.obs_month) THEN c.order_date END) AS last_order_in_obs,
    -- đơn kế tiếp đầu tiên SAU obs_month
    MIN(CASE WHEN c.order_date  > LAST_DAY(o.obs_month) THEN c.order_date END) AS next_order_after
  FROM obs o
  LEFT JOIN completed_orders c ON c.supplier_id = o.supplier_id
  GROUP BY 1,2,3
),

label_final AS (
  SELECT
    supplier_id,
    obs_month,
    gap_threshold_days,
    last_order_in_obs,
    next_order_after,
    -- Gap ngày: nếu không có đơn kế → tính tới cuối tháng end_month (censor)
    DATE_DIFF(
      COALESCE(next_order_after, LAST_DAY(end_month)),
      last_order_in_obs, DAY
    )                                                           AS gap_days,
    CASE
      WHEN last_order_in_obs IS NULL THEN NULL                 -- không active thật → loại
      WHEN DATE_DIFF(COALESCE(next_order_after, LAST_DAY(end_month)),
                     last_order_in_obs, DAY) >= gap_threshold_days
        THEN 1 ELSE 0
    END                                                         AS is_churn
  FROM label
),

-- ------------------------------------------------------------
-- B4: FEATURE — Engagement + Earnings + Quality (từ monthly + fct)
-- ------------------------------------------------------------
perf_month AS (
  SELECT
    m.supplier_id,
    m.period                                                    AS obs_month,
    m.online_hours                                              AS online_hours_m,
    m.order_income                                              AS income_m,
    SAFE_DIVIDE(m.order_income, NULLIF(m.online_hours,0))       AS rph,
    -- MoM delta (window theo driver)
    m.online_hours - LAG(m.online_hours) OVER w                 AS online_hours_mom_delta,
    SAFE_DIVIDE(m.order_income - LAG(m.order_income) OVER w,
                NULLIF(LAG(m.order_income) OVER w,0))           AS income_mom_pct,
    -- 3M slope thô = (M - M-2)/2
    SAFE_DIVIDE(m.online_hours - LAG(m.online_hours,2) OVER w, 2) AS online_hours_3m_slope
  FROM ahamove_archive_ops.driver_performance_monthly m
  WHERE m.period BETWEEN DATE_SUB(start_month, INTERVAL 2 MONTH) AND end_month
    AND m.stp_complete > 0
  WINDOW w AS (PARTITION BY m.supplier_id ORDER BY m.period)
),

-- Quality + active_days từ daily fct (gộp theo tháng)
quality_month AS (
  SELECT
    supplier_id,
    DATE_TRUNC(DATE(first_complete_time,'Asia/Saigon'), MONTH)  AS obs_month,  -- ⚠️ dùng period của fct
    COUNT(DISTINCT DATE(first_complete_time,'Asia/Saigon'))     AS active_days_m,
    SAFE_DIVIDE(SUM(stp_success), NULLIF(SUM(stp_complete),0))  AS fr_proxy,
    SAFE_DIVIDE(
      SUM(rating_5star*5 + rating_4star*4 + rating_3star*3 + rating_2star*2 + rating_1star),
      NULLIF(SUM(rating_5star+rating_4star+rating_3star+rating_2star+rating_1star),0)
    )                                                           AS rating_star,
    SAFE_DIVIDE(SUM(noti_timeout), NULLIF(SUM(noti_assign),0))  AS noti_timeout_rate
  FROM ahamove_archive_ops.fct_supplier_performance
  GROUP BY 1,2
)

-- ============================================================
-- OUTPUT: churn_feature_mart
-- ============================================================
SELECT
  o.supplier_id,
  o.obs_month,
  o.cohort,
  o.driver_life_time,
  -- Static
  b.city_id,
  b.is_ev,
  b.gender,
  EXTRACT(YEAR FROM o.obs_month) - b.birth_year                AS age,
  -- Engagement
  p.online_hours_m,
  p.online_hours_mom_delta,
  p.online_hours_3m_slope,
  q.active_days_m,
  -- Earnings
  p.income_m,
  p.income_mom_pct,
  p.rph,
  -- Quality / Friction
  q.fr_proxy,
  q.rating_star,
  q.noti_timeout_rate,
  -- Recency
  lf.gap_days                                                  AS days_since_last_order,
  CASE WHEN lf.gap_days >= 7 AND lf.is_churn = 0 THEN 1 ELSE 0 END AS atrisk_flag,
  -- LABEL
  lf.is_churn
FROM obs o
JOIN base_supplier b   ON b.supplier_id = o.supplier_id
JOIN label_final  lf   ON lf.supplier_id = o.supplier_id AND lf.obs_month = o.obs_month
LEFT JOIN perf_month p ON p.supplier_id = o.supplier_id AND p.obs_month = o.obs_month
LEFT JOIN quality_month q ON q.supplier_id = o.supplier_id AND q.obs_month = o.obs_month
WHERE lf.is_churn IS NOT NULL
  AND (EXTRACT(YEAR FROM o.obs_month) - b.birth_year) >= 22    -- đồng bộ Retention KPI
ORDER BY o.cohort, o.obs_month, o.supplier_id

-- ============================================================
-- QA nhanh sau khi chạy: churn rate theo cohort có hợp lý không
-- ============================================================
/*
SELECT cohort, obs_month,
  COUNT(*) AS drivers,
  ROUND(AVG(is_churn)*100,1) AS churn_rate_pct,
  ROUND(AVG(days_since_last_order),1) AS avg_gap
FROM churn_feature_mart
GROUP BY 1,2 ORDER BY 1,2;
*/
