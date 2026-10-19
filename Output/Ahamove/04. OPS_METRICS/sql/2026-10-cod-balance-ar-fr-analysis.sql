-- =============================================================================
-- FILE: 2026-10-cod-balance-ar-fr-analysis.sql
-- PURPOSE: Phân tích AR/FR của đơn COD theo COD value block × Driver Ranking
--          Hỗ trợ chiến lược Chuyên biệt hóa Tài xế & COD Champion 2027
-- OWNER: Driver Management (Lê Phương Khanh)
-- CREATED: 2026-10
-- =============================================================================
-- NOTE: Trường cod_amount trong order_raw cần team verify field name thực tế.
--       Giả định field là `stop_cod_amount` (đơn vị VNĐ).
--       Nếu sai, thay thế bằng tên field đúng trong ahamove_raw.order_raw.
-- =============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
-- QUERY 1: AR/FR của đơn COD bị hủy vì tài xế không đủ tiền mặt
--          Phân tích theo COD Value Block × Driver Ranking
-- Context: Phát hiện khoảng tối (dark spot) — đơn nào bị miss do COD Balance
--          áp chung, không phân tầng theo ranking tài xế.
-- ─────────────────────────────────────────────────────────────────────────────

WITH

-- [1a] Lọc raw_performance: đơn xe máy, Bike/Instant, áp condition_kpi chuẩn
base_orders AS (
  SELECT
    r.order_id,
    r.stop_id,
    r.order_date,

    -- unique_id KPI-FR logic (theo spec @vinhnp1)
    CASE
      WHEN LENGTH(r.stop_tracking_number) <= 1
        THEN r.order_id
      WHEN LENGTH(r.stop_tracking_number) <= 4
        THEN CONCAT(r.stop_tracking_number, r.order_date)
      ELSE COALESCE(NULLIF(r.stop_tracking_number, ''), r.stop_id)
    END AS unique_id,

    -- accept_time_kpi: COALESCE(old_supplier_ids từ order_raw, accept_time gốc)
    -- NOTE: old_supplier_ids lấy từ JOIN order_raw ở bước sau
    r.accept_time,
    r.status,
    r.supplier_id,
    r.cancel_by,
    r.cancel_comment,
    r.payment_method,
    r.actual_city_name,
    r.service_id,

    -- Period để join driver_performance_monthly
    FORMAT_DATE('%Y-%m', DATE(r.order_date)) AS period_ym

  FROM `ahamove_raw.raw_performance` r

  WHERE
    -- Lọc Bike/Instant only (loại Truck, Ride, Van, v.v.)
    NOT REGEXP_CONTAINS(r.service_id,
      r'-(INTERCT|TRUCK|RIDE|VAN|PARTNER|TRICYCLE|TEST|PARTNER-BIGC|ASTGROUP|INTERNAL|HUB|BKN|RENT|MASAN)-?')
    -- Loại SaaS services
    AND r.service_id NOT IN (
      SELECT id FROM `ahamove_archive.service_archive`
      WHERE JSON_EXTRACT_SCALAR(_extra_props, '$.is_saas') = 'true'
    )
    -- Loại test accounts
    AND r.user_id NOT IN ('84862151477', '84862151000')
    -- Loại cancel bất thường (cancel trước khi đặt)
    AND (r.cancel_time IS NULL OR r.cancel_time >= r.order_time)
    -- Chỉ đơn COD (payment_method = CASH — buyer trả tiền mặt cho tài xế)
    -- NOTE: Verify giá trị thực tế của payment_method cho đơn COD ứng tiền mặt
    AND LOWER(r.payment_method) IN ('cash', 'cod', 'cash_on_delivery')
    -- Khung thời gian phân tích: 3 tháng gần nhất
    AND r.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
),

-- [1b] Join order_raw để lấy COD amount thực tế theo từng đơn
-- NOTE: Verify field name: stop_cod_amount là assumption — cần xác nhận với Data team
orders_with_cod_amount AS (
  SELECT
    b.*,
    COALESCE(o.old_supplier_ids, CAST(b.accept_time AS STRING)) AS accept_time_kpi,
    -- NOTE: Thay 'stop_cod_amount' bằng field name thực tế nếu khác
    CAST(o.stop_cod_amount AS FLOAT64) AS cod_amount_vnd
  FROM base_orders b
  LEFT JOIN `ahamove_raw.order_raw` o
    ON b.order_id = o.order_id AND b.stop_id = o.stop_id
),

-- [1c] Join supplier_raw để lọc tài xế xe máy hợp lệ
valid_suppliers AS (
  SELECT DISTINCT supplier_id
  FROM `ahamove_supplier_raw.supplier_raw`
  WHERE
    JSON_EXTRACT_SCALAR(extra, '$.vehicle_type') IN ('MOTORBIKE', 'EV-BIKE')
    AND COALESCE(email, 'a') NOT LIKE '%ahamove_ka_lazada%'
    AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
    AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
    AND COALESCE(tags, 'a') NOT LIKE '%SALESFORCE%'
    AND partitioned_create_time >= '2010-01-01'
),

-- [1d] Join driver_performance_monthly để lấy ranking tháng tương ứng
orders_with_ranking AS (
  SELECT
    o.*,
    COALESCE(d.driver_ranking, 'Un_rank') AS driver_ranking,
    -- COD Value Block (VNĐ)
    CASE
      WHEN o.cod_amount_vnd <= 200000    THEN '1_≤200k'
      WHEN o.cod_amount_vnd <= 500000    THEN '2_200k-500k'
      WHEN o.cod_amount_vnd <= 1000000   THEN '3_500k-1M'
      WHEN o.cod_amount_vnd <= 2000000   THEN '4_1M-2M'
      WHEN o.cod_amount_vnd <= 3000000   THEN '5_2M-3M'
      WHEN o.cod_amount_vnd <= 5000000   THEN '6_3M-5M'
      ELSE                                    '7_>5M'
    END AS cod_block
  FROM orders_with_cod_amount o
  -- Lọc tài xế xe máy hợp lệ
  INNER JOIN valid_suppliers vs ON o.supplier_id = vs.supplier_id
  -- Ranking tháng tương ứng với tháng của đơn hàng
  LEFT JOIN `ahamove_archive_ops.driver_performance_monthly` d
    ON o.supplier_id = d.supplier_id
    AND o.period_ym = d.period
),

-- [1e] Đơn bị hủy do tài xế không đủ tiền mặt COD
cod_cash_cancels AS (
  SELECT *
  FROM orders_with_ranking
  WHERE
    -- Tài xế hủy (không phải khách hủy)
    cancel_by != 'user'
    -- Cancel reason liên quan COD tiền mặt không đủ
    AND (
      LOWER(cancel_comment) LIKE '%cod%'
      OR LOWER(cancel_comment) LIKE '%không đủ tiền ứng trước%'
      OR LOWER(cancel_comment) LIKE '%khong du tien ung truoc%'
      OR LOWER(cancel_comment) LIKE '%thiếu tiền mặt%'
      OR LOWER(cancel_comment) LIKE '%thieu tien mat%'
    )
)

-- [1f] Kết quả cuối: AR/FR theo COD block × Driver Ranking
-- Chú ý: Query này tính AR/FR ở cấp đơn — không phải cấp broadcast
SELECT
  r.cod_block,
  r.driver_ranking,
  COUNT(DISTINCT r.unique_id)                                      AS total_orders,
  COUNT(DISTINCT cc.unique_id)                                     AS cod_cancel_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT cc.unique_id),
    COUNT(DISTINCT r.unique_id)
  ) * 100, 2)                                                      AS cod_cancel_rate_pct,
  COUNT(DISTINCT CASE WHEN r.accept_time_kpi IS NOT NULL
    THEN r.unique_id END)                                          AS accepted_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN r.accept_time_kpi IS NOT NULL
      THEN r.unique_id END),
    COUNT(DISTINCT r.unique_id)
  ) * 100, 2)                                                      AS ar_pct,
  COUNT(DISTINCT CASE WHEN r.status = 'COMPLETED'
    THEN r.unique_id END)                                          AS completed_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN r.status = 'COMPLETED'
      THEN r.unique_id END),
    COUNT(DISTINCT r.unique_id)
  ) * 100, 2)                                                      AS fr_pct

FROM orders_with_ranking r
LEFT JOIN cod_cash_cancels cc USING (unique_id)

GROUP BY 1, 2
ORDER BY r.cod_block, r.driver_ranking;


-- =============================================================================
-- QUERY 2: AR/FR của đơn Transfer COD theo COD Value Block × Driver Ranking
--          Transfer COD = người mua chuyển khoản vào tài khoản tài xế,
--          tài xế cần đủ COD Balance để fulfil đơn
-- =============================================================================

WITH

-- [2a] Base: đơn transfer_COD — condition_kpi chuẩn
transfer_cod_base AS (
  SELECT
    r.order_id,
    r.stop_id,
    r.order_date,
    CASE
      WHEN LENGTH(r.stop_tracking_number) <= 1
        THEN r.order_id
      WHEN LENGTH(r.stop_tracking_number) <= 4
        THEN CONCAT(r.stop_tracking_number, r.order_date)
      ELSE COALESCE(NULLIF(r.stop_tracking_number, ''), r.stop_id)
    END AS unique_id,
    r.accept_time,
    r.status,
    r.supplier_id,
    r.cancel_by,
    r.cancel_comment,
    r.payment_method,
    r.actual_city_name,
    FORMAT_DATE('%Y-%m', DATE(r.order_date)) AS period_ym

  FROM `ahamove_raw.raw_performance` r

  WHERE
    NOT REGEXP_CONTAINS(r.service_id,
      r'-(INTERCT|TRUCK|RIDE|VAN|PARTNER|TRICYCLE|TEST|PARTNER-BIGC|ASTGROUP|INTERNAL|HUB|BKN|RENT|MASAN)-?')
    AND r.service_id NOT IN (
      SELECT id FROM `ahamove_archive.service_archive`
      WHERE JSON_EXTRACT_SCALAR(_extra_props, '$.is_saas') = 'true'
    )
    AND r.user_id NOT IN ('84862151477', '84862151000')
    AND (r.cancel_time IS NULL OR r.cancel_time >= r.order_time)
    -- Chỉ đơn Transfer COD
    -- NOTE: Verify giá trị thực tế: 'TRANSFER_COD', 'transfer_cod', 'TCOD', v.v.
    AND LOWER(r.payment_method) IN ('transfer_cod', 'tcod', 'transfer cod')
    AND r.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
),

-- [2b] Enrich với COD amount và accept_time_kpi từ order_raw
tcod_with_amount AS (
  SELECT
    b.*,
    COALESCE(o.old_supplier_ids, CAST(b.accept_time AS STRING)) AS accept_time_kpi,
    CAST(o.stop_cod_amount AS FLOAT64) AS cod_amount_vnd
  FROM transfer_cod_base b
  LEFT JOIN `ahamove_raw.order_raw` o
    ON b.order_id = o.order_id AND b.stop_id = o.stop_id
),

-- [2c] Supplier + Ranking enrich
tcod_enriched AS (
  SELECT
    t.*,
    COALESCE(d.driver_ranking, 'Un_rank') AS driver_ranking,
    CASE
      WHEN t.cod_amount_vnd <= 200000    THEN '1_≤200k'
      WHEN t.cod_amount_vnd <= 500000    THEN '2_200k-500k'
      WHEN t.cod_amount_vnd <= 1000000   THEN '3_500k-1M'
      WHEN t.cod_amount_vnd <= 2000000   THEN '4_1M-2M'
      WHEN t.cod_amount_vnd <= 3000000   THEN '5_2M-3M'
      WHEN t.cod_amount_vnd <= 5000000   THEN '6_3M-5M'
      ELSE                                    '7_>5M'
    END AS cod_block,
    -- Flag đơn bị hủy vì COD balance không đủ
    CASE
      WHEN t.cancel_by != 'user'
        AND (
          LOWER(t.cancel_comment) LIKE '%cod%'
          OR LOWER(t.cancel_comment) LIKE '%số dư%'
          OR LOWER(t.cancel_comment) LIKE '%so du%'
          OR LOWER(t.cancel_comment) LIKE '%balance%'
          OR LOWER(t.cancel_comment) LIKE '%không đủ tiền%'
          OR LOWER(t.cancel_comment) LIKE '%khong du tien%'
        )
      THEN 1 ELSE 0
    END AS is_cod_balance_cancel

  FROM tcod_with_amount t
  INNER JOIN (
    SELECT DISTINCT supplier_id
    FROM `ahamove_supplier_raw.supplier_raw`
    WHERE
      JSON_EXTRACT_SCALAR(extra, '$.vehicle_type') IN ('MOTORBIKE', 'EV-BIKE')
      AND COALESCE(email, 'a') NOT LIKE '%ahamove_ka_lazada%'
      AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
      AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
      AND COALESCE(tags, 'a') NOT LIKE '%SALESFORCE%'
      AND partitioned_create_time >= '2010-01-01'
  ) vs ON t.supplier_id = vs.supplier_id
  LEFT JOIN `ahamove_archive_ops.driver_performance_monthly` d
    ON t.supplier_id = d.supplier_id
    AND t.period_ym = d.period
)

-- [2d] Output: AR/FR/COD Balance Cancel Rate theo block × ranking
SELECT
  cod_block,
  driver_ranking,
  COUNT(DISTINCT unique_id)                                        AS total_tcod_orders,
  SUM(is_cod_balance_cancel)                                       AS cod_balance_cancel_orders,
  ROUND(SAFE_DIVIDE(
    SUM(is_cod_balance_cancel),
    COUNT(DISTINCT unique_id)
  ) * 100, 2)                                                      AS cod_balance_cancel_rate_pct,
  COUNT(DISTINCT CASE WHEN accept_time_kpi IS NOT NULL
    THEN unique_id END)                                            AS accepted_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN accept_time_kpi IS NOT NULL
      THEN unique_id END),
    COUNT(DISTINCT unique_id)
  ) * 100, 2)                                                      AS ar_pct,
  COUNT(DISTINCT CASE WHEN status = 'COMPLETED'
    THEN unique_id END)                                            AS completed_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN status = 'COMPLETED'
      THEN unique_id END),
    COUNT(DISTINCT unique_id)
  ) * 100, 2)                                                      AS fr_pct

FROM tcod_enriched

GROUP BY 1, 2
ORDER BY cod_block, driver_ranking;


-- =============================================================================
-- QUERY 3: Baseline AR/FR/CR theo Driver Ranking — validate threshold chiến lược
--          Target: SC ≥ 95% AR, CN ≥ 90% AR; CR (cancel rate) SC ≤ 5%
--          Phân tích trên toàn bộ đơn Bike/Instant (không lọc COD)
--          Dùng để đặt ngưỡng tham chiếu cho COD Overdraft eligibility
-- =============================================================================

WITH

-- [3a] Base: toàn bộ đơn Bike/Instant, condition_kpi chuẩn, 3 tháng gần nhất
all_bike_orders AS (
  SELECT
    r.order_id,
    r.stop_id,
    r.order_date,
    CASE
      WHEN LENGTH(r.stop_tracking_number) <= 1
        THEN r.order_id
      WHEN LENGTH(r.stop_tracking_number) <= 4
        THEN CONCAT(r.stop_tracking_number, r.order_date)
      ELSE COALESCE(NULLIF(r.stop_tracking_number, ''), r.stop_id)
    END AS unique_id,
    COALESCE(o.old_supplier_ids, CAST(r.accept_time AS STRING)) AS accept_time_kpi,
    r.status,
    r.supplier_id,
    r.cancel_by,
    r.actual_city_name,
    FORMAT_DATE('%Y-%m', DATE(r.order_date)) AS period_ym

  FROM `ahamove_raw.raw_performance` r
  LEFT JOIN `ahamove_raw.order_raw` o
    ON r.order_id = o.order_id AND r.stop_id = o.stop_id

  WHERE
    NOT REGEXP_CONTAINS(r.service_id,
      r'-(INTERCT|TRUCK|RIDE|VAN|PARTNER|TRICYCLE|TEST|PARTNER-BIGC|ASTGROUP|INTERNAL|HUB|BKN|RENT|MASAN)-?')
    AND r.service_id NOT IN (
      SELECT id FROM `ahamove_archive.service_archive`
      WHERE JSON_EXTRACT_SCALAR(_extra_props, '$.is_saas') = 'true'
    )
    AND r.user_id NOT IN ('84862151477', '84862151000')
    AND (r.cancel_time IS NULL OR r.cancel_time >= r.order_time)
    AND r.order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)
),

-- [3b] Enrich với driver ranking
orders_ranked AS (
  SELECT
    o.*,
    COALESCE(d.driver_ranking, 'Un_rank') AS driver_ranking
  FROM all_bike_orders o
  INNER JOIN (
    SELECT DISTINCT supplier_id
    FROM `ahamove_supplier_raw.supplier_raw`
    WHERE
      JSON_EXTRACT_SCALAR(extra, '$.vehicle_type') IN ('MOTORBIKE', 'EV-BIKE')
      AND COALESCE(email, 'a') NOT LIKE '%ahamove_ka_lazada%'
      AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
      AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
      AND COALESCE(tags, 'a') NOT LIKE '%SALESFORCE%'
      AND partitioned_create_time >= '2010-01-01'
  ) vs ON o.supplier_id = vs.supplier_id
  LEFT JOIN `ahamove_archive_ops.driver_performance_monthly` d
    ON o.supplier_id = d.supplier_id
    AND o.period_ym = d.period
)

-- [3c] Baseline AR/FR/CR by Ranking — validate strategic thresholds
SELECT
  driver_ranking,
  -- Tier order cho sort dễ đọc
  CASE driver_ranking
    WHEN 'SC'      THEN 1
    WHEN 'CN'      THEN 2
    WHEN 'BC'      THEN 3
    WHEN 'Un_rank' THEN 4
    ELSE 5
  END AS tier_order,

  COUNT(DISTINCT unique_id)                                        AS total_orders,
  COUNT(DISTINCT supplier_id)                                      AS unique_drivers,

  -- AR: % đơn được tài xế accept / tổng đơn
  COUNT(DISTINCT CASE WHEN accept_time_kpi IS NOT NULL
    THEN unique_id END)                                            AS accepted_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN accept_time_kpi IS NOT NULL
      THEN unique_id END),
    COUNT(DISTINCT unique_id)
  ) * 100, 2)                                                      AS ar_pct,

  -- FR: % đơn completed / tổng đơn
  COUNT(DISTINCT CASE WHEN status = 'COMPLETED'
    THEN unique_id END)                                            AS completed_orders,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN status = 'COMPLETED'
      THEN unique_id END),
    COUNT(DISTINCT unique_id)
  ) * 100, 2)                                                      AS fr_pct,

  -- CR (Cancel Rate): % đơn tài xế hủy sau khi đã nhận / tổng đơn đã nhận
  COUNT(DISTINCT CASE WHEN cancel_by != 'user' AND accept_time_kpi IS NOT NULL
    THEN unique_id END)                                            AS driver_cancel_after_accept,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN cancel_by != 'user' AND accept_time_kpi IS NOT NULL
      THEN unique_id END),
    COUNT(DISTINCT CASE WHEN accept_time_kpi IS NOT NULL
      THEN unique_id END)
  ) * 100, 2)                                                      AS cr_after_accept_pct,

  -- Gap vs threshold: dương = đạt, âm = thiếu
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN accept_time_kpi IS NOT NULL
      THEN unique_id END),
    COUNT(DISTINCT unique_id)
  ) * 100, 2)
  - CASE driver_ranking WHEN 'SC' THEN 95 WHEN 'CN' THEN 90 ELSE NULL END
                                                                   AS ar_gap_vs_threshold

FROM orders_ranked

GROUP BY 1, 2
ORDER BY 2;
