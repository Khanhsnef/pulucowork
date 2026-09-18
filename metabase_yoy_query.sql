WITH active_drivers AS (
    SELECT supplier_id
    FROM ahamove_archive_ops.fct_supplier_performance
    WHERE stp_complete > 0
    GROUP BY supplier_id
    HAVING COUNTIF(EXTRACT(YEAR FROM period) = 2025) > 0
       AND COUNTIF(EXTRACT(YEAR FROM period) = 2026) > 0
),

-- Bước 2: Supplier filter chuẩn (SGN, MOTORBIKE/EV-BIKE, loại test/WH/SALESFORCE)
valid_suppliers AS (
    SELECT s.id AS supplier_id
    FROM ahamove_supplier_raw.supplier_raw s
    WHERE JSON_EXTRACT_SCALAR(s.extra, '$.vehicle_type') IN ('MOTORBIKE', 'EV-BIKE')
      AND COALESCE(s.email,    'a') NOT LIKE '%ahamove_ka_lazada%'
      AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
      AND COALESCE(s.services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
      AND COALESCE(s.tags,     'a') NOT LIKE '%SALESFORCE%'
      AND s.partitioned_create_time >= '2010-01-01'
      -- Chỉ SGN (theo supplier profile, không gộp BDG/DNI)
      AND s.city_id = 'SGN'
),

-- Bước 3: Daily performance raw
daily_perf AS (
    SELECT
        p.period,
        DATE_TRUNC(p.period, MONTH)                        AS month,
        EXTRACT(YEAR  FROM p.period)                       AS year,
        EXTRACT(MONTH FROM p.period)                       AS month_num,
        p.supplier_id,
        SUM(p.stp_complete)                                AS stp_complete,
        SUM(p.complete_order)                              AS complete_order,
        SUM(p.accept_order)                                AS accept_order,
        SUM(p.cancel_order)                                AS cancel_order,
        SUM(p.order_income)                                AS order_income,
        SUM(p.reward_income_pit1_5)                        AS reward_income,
        SUM(p.noti_accept + p.noti_assign)                 AS accept_noti,
        SUM(p.noti_assign + p.noti_accept + p.noti_dismiss
            + p.noti_timeout + p.noti_not_updated)         AS total_noti,
        SUM(p.rating_5star + p.rating_4star + p.rating_3star
            + p.rating_2star + p.rating_1star)             AS rating_order,
        SUM(p.rating_5star*5 + p.rating_4star*4
            + p.rating_3star*3 + p.rating_2star*2
            + p.rating_1star)                              AS rating_star
    FROM ahamove_archive_ops.fct_supplier_performance p
    INNER JOIN active_drivers  ad ON p.supplier_id = ad.supplier_id
    INNER JOIN valid_suppliers vs ON p.supplier_id = vs.supplier_id
    WHERE p.period >= DATE('2025-01-01')
      AND p.period <= DATE('2026-09-18')
      AND p.stp_complete > 0
    GROUP BY 1, 2, 3, 4, 5
),

-- Bước 4: Online hours
daily_online AS (
    SELECT
        o.period,
        o.supplier_id,
        SUM(o.online_hours) AS online_hours
    FROM ahamove_archive.ops_suppliers_online_hours o
    INNER JOIN active_drivers  ad ON o.supplier_id = ad.supplier_id
    INNER JOIN valid_suppliers vs ON o.supplier_id = vs.supplier_id
    WHERE o.period >= DATE('2025-01-01')
      AND o.period <= DATE('2026-09-18')
    GROUP BY 1, 2
),

-- Bước 5: Driver cancel POC (daily → aggregate lên month sau)
daily_cancel_poc AS (
    SELECT
        c.supplier_id,
        DATE_TRUNC(DATE(TIMESTAMP(c.order_date), 'Asia/Saigon'), MONTH) AS month,
        COUNT(CASE
            WHEN (c.cancel_comment LIKE '%for supplier%'
               OR c.cancel_comment LIKE '%Driver ask%'
               OR c.cancel_comment LIKE '%by Driver%'
               OR c.cancel_comment LIKE '%by Supplier%'
               OR c.cancel_comment LIKE '%by supplier%'
               OR c.cancel_by = 'supplier')
            THEN c.order_id END)                                         AS driver_cancel,
        COUNT(CASE
            WHEN c.reason_type = 'poc'
             AND (c.cancel_comment LIKE '%for supplier%'
               OR c.cancel_comment LIKE '%Driver ask%'
               OR c.cancel_comment LIKE '%by Driver%'
               OR c.cancel_comment LIKE '%by Supplier%'
               OR c.cancel_comment LIKE '%by supplier%'
               OR c.cancel_by = 'supplier')
            THEN c.order_id END)                                         AS cancel_poc
    FROM ahamove_archive_ops.fact_cancellation_detail c
    INNER JOIN active_drivers  ad ON c.supplier_id = ad.supplier_id
    INNER JOIN valid_suppliers vs ON c.supplier_id = vs.supplier_id
    WHERE c.order_date >= DATE('2025-01-01')
      AND c.order_date <= DATE('2026-09-18')
      AND c.supplier_id IS NOT NULL
    GROUP BY 1, 2
),

-- Bước 6: Merge daily → monthly
monthly_agg AS (
    SELECT
        d.month,
        d.year,
        d.month_num,
        -- Flag tháng chưa full (Sep 2026 chỉ có 18 ngày)
        CASE
            WHEN d.month = DATE_TRUNC(DATE('2026-09-18'), MONTH) THEN TRUE
            ELSE FALSE
        END                                                      AS is_partial_month,
        -- Driver count
        COUNT(DISTINCT d.supplier_id)                            AS driver_count,
        -- Volume
        SUM(d.stp_complete)                                      AS total_stp,
        SUM(d.complete_order)                                    AS total_complete_order,
        -- Income
        SUM(d.order_income)                                      AS total_order_income,
        SUM(d.reward_income)                                     AS total_reward_income,
        SUM(d.order_income + d.reward_income)                    AS total_income,
        -- Hours
        SUM(o.online_hours)                                      AS total_online_hours,
        -- Per-driver averages (monthly)
        AVG(d.order_income + d.reward_income)                    AS avg_income_per_driver,
        AVG(o.online_hours)                                      AS avg_online_hours_per_driver,
        AVG(d.stp_complete)                                      AS avg_stp_per_driver,
        -- Efficiency: EPH & PPH
        SAFE_DIVIDE(
            SUM(d.order_income + d.reward_income),
            SUM(o.online_hours)
        )                                                        AS eph,   -- Earnings Per Hour (VND)
        SAFE_DIVIDE(
            SUM(d.stp_complete),
            SUM(o.online_hours)
        )                                                        AS pph,   -- Packages Per Hour
        -- AR (Acceptance Rate từ notification)
        SAFE_DIVIDE(SUM(d.accept_noti), SUM(d.total_noti))      AS ar_noti,
        -- CR POC (quality cancel rate)
        SAFE_DIVIDE(
            SUM(cp.driver_cancel) - SUM(cp.cancel_poc) * 0.5,
            NULLIF(SUM(d.accept_order), 0)
        )                                                        AS cr_poc,
        -- Rating
        SAFE_DIVIDE(SUM(d.rating_star), NULLIF(SUM(d.rating_order), 0)) AS avg_rating
    FROM daily_perf d
    LEFT JOIN daily_online      o  ON d.period       = o.period
                                   AND d.supplier_id  = o.supplier_id
    LEFT JOIN daily_cancel_poc  cp ON d.month         = cp.month
                                   AND d.supplier_id  = cp.supplier_id
    GROUP BY 1, 2, 3, 4
),

-- Bước 7: YoY so sánh cùng tháng
yoy AS (
    SELECT
        cur.month_num,
        cur.month                                               AS month_2026,
        prev.month                                             AS month_2025,
        cur.is_partial_month,

        -- Driver count
        prev.driver_count                                      AS driver_count_2025,
        cur.driver_count                                       AS driver_count_2026,

        -- EPH (core hypothesis)
        prev.eph                                               AS eph_2025,
        cur.eph                                                AS eph_2026,
        SAFE_DIVIDE(cur.eph - prev.eph, prev.eph)             AS eph_yoy_pct,

        -- PPH
        prev.pph                                               AS pph_2025,
        cur.pph                                                AS pph_2026,
        SAFE_DIVIDE(cur.pph - prev.pph, prev.pph)             AS pph_yoy_pct,

        -- Online hours per driver
        prev.avg_online_hours_per_driver                       AS avg_hours_2025,
        cur.avg_online_hours_per_driver                        AS avg_hours_2026,
        SAFE_DIVIDE(
            cur.avg_online_hours_per_driver - prev.avg_online_hours_per_driver,
            prev.avg_online_hours_per_driver
        )                                                      AS hours_yoy_pct,

        -- Income per driver
        prev.avg_income_per_driver                             AS avg_income_2025,
        cur.avg_income_per_driver                              AS avg_income_2026,
        SAFE_DIVIDE(
            cur.avg_income_per_driver - prev.avg_income_per_driver,
            prev.avg_income_per_driver
        )                                                      AS income_yoy_pct,

        -- STP per driver
        prev.avg_stp_per_driver                                AS avg_stp_2025,
        cur.avg_stp_per_driver                                 AS avg_stp_2026,
        SAFE_DIVIDE(
            cur.avg_stp_per_driver - prev.avg_stp_per_driver,
            prev.avg_stp_per_driver
        )                                                      AS stp_yoy_pct,

        -- Total supply hours (fleet level)
        prev.total_online_hours                                AS total_hours_2025,
        cur.total_online_hours                                 AS total_hours_2026,
        SAFE_DIVIDE(
            cur.total_online_hours - prev.total_online_hours,
            prev.total_online_hours
        )                                                      AS total_hours_yoy_pct,

        -- Quality
        prev.ar_noti                                           AS ar_2025,
        cur.ar_noti                                            AS ar_2026,
        prev.cr_poc                                            AS cr_poc_2025,
        cur.cr_poc                                             AS cr_poc_2026,
        prev.avg_rating                                        AS rating_2025,
        cur.avg_rating                                         AS rating_2026

    FROM monthly_agg cur
    JOIN monthly_agg prev
      ON cur.month_num = prev.month_num
     AND cur.year      = 2026
     AND prev.year     = 2025
)

SELECT *
FROM yoy
ORDER BY month_num ASC;