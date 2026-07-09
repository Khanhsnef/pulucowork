DECLARE end_date DATE DEFAULT DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY);

-- B1: Tài xế DFD T4/T5/T6
WITH dfd_drivers AS (
    SELECT
        id                                                                      AS supplier_id,
        DATE(first_complete_time, 'Asia/Saigon')                               AS dfd_date,
        DATE_TRUNC(DATE(first_complete_time, 'Asia/Saigon'), MONTH)            AS dfd_month,
        CASE WHEN city_id IN ('HAN','SGN') THEN city_id ELSE 'EXP' END        AS city_id
    FROM ahamove_supplier_raw.supplier_raw
    WHERE DATE_TRUNC(DATE(first_complete_time, 'Asia/Saigon'), MONTH)
              IN ('2026-04-01','2026-05-01','2026-06-01')
        AND JSON_EXTRACT_SCALAR(extra, '$.vehicle_type') IN ('MOTORBIKE','EV-BIKE')
        AND COALESCE(email,    'a') NOT LIKE '%ahamove_ka_lazada%'
        AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-DELIVERY%'
        AND COALESCE(services, 'a') NOT LIKE '%VNM-WH-VENDOR%'
        AND COALESCE(tags,     'a') NOT LIKE '%SALESFORCE%'
        AND partitioned_create_time >= '2010-01-01'
),

-- B2: Online hours theo tuần
online_weekly AS (
    SELECT
        d.supplier_id,
        d.city_id,
        d.dfd_month,
        DATE_TRUNC(o.period, WEEK(MONDAY))                                     AS week,
        DATE_DIFF(
            DATE_TRUNC(o.period, WEEK(MONDAY)),
            DATE_TRUNC(d.dfd_date, WEEK(MONDAY)),
            WEEK
        )                                                                       AS weeks_since_dfd,
        SUM(o.online_hours)                                                     AS online_hours
    FROM dfd_drivers d
    JOIN ahamove_archive.ops_suppliers_online_hours o
        ON  o.supplier_id = d.supplier_id
        AND o.period >= d.dfd_date
        AND o.period <= end_date
    GROUP BY 1,2,3,4,5
),

-- B3: STP, income, rating, cancel từ fct_supplier_performance (daily → group theo tuần)
perf_weekly AS (
    SELECT
        d.supplier_id,
        d.city_id,
        d.dfd_month,
        DATE_TRUNC(p.period, WEEK(MONDAY))                                     AS week,
        DATE_DIFF(
            DATE_TRUNC(p.period, WEEK(MONDAY)),
            DATE_TRUNC(d.dfd_date, WEEK(MONDAY)),
            WEEK
        )                                                                       AS weeks_since_dfd,
        SUM(p.stp_complete)                                                     AS stp_complete,
        COUNT(DISTINCT CASE WHEN p.stp_complete > 0 THEN p.period END)        AS active_day,
        SUM(p.accept_order)                                                     AS accept_order,
        SUM(p.cancel_order)                                                     AS cancel_order,
        SUM(p.order_income)                                                     AS order_income,
        SUM(p.reward_income_pit1_5)                                            AS reward_income,
        SUM(p.rating_star)                                                      AS rating_star,
        SUM(p.rating_order)                                                     AS rating_order
    FROM dfd_drivers d
    JOIN ahamove_archive_ops.fct_supplier_performance p
        ON  p.supplier_id = d.supplier_id
        AND p.period >= d.dfd_date
        AND p.period <= end_date
    GROUP BY 1,2,3,4,5
),

-- B4: cancel_poc từ fact_cancellation_detail theo tuần
cancel_poc_weekly AS (
    SELECT
        d.supplier_id,
        d.dfd_month,
        DATE_TRUNC(c.order_date, WEEK(MONDAY))                                 AS week,
        COUNT(CASE WHEN
                (c.cancel_comment LIKE '%for supplier%'
                OR c.cancel_comment LIKE '%Driver ask%'
                OR c.cancel_comment LIKE '%by Driver%'
                OR c.cancel_comment LIKE '%by Supplier%'
                OR c.cancel_comment LIKE '%by supplier%'
                OR c.cancel_by = 'supplier')
                AND c.reason_type = 'poc'
              THEN c.order_id END)                                             AS cancel_poc
    FROM dfd_drivers d
    JOIN ahamove_archive_ops.fact_cancellation_detail c
        ON  c.supplier_id = d.supplier_id
        AND c.order_date >= d.dfd_date
        AND c.order_date <= end_date
        AND c.supplier_id IS NOT NULL
        AND c.partner != 'tiktokshop'
    GROUP BY 1,2,3
),

-- B5: AR/FR từ raw_performance theo tuần
demand_weekly AS (
    SELECT
        d.supplier_id,
        d.city_id,
        d.dfd_month,
        DATE_TRUNC(r.order_date, WEEK(MONDAY))                                 AS week,
        DATE_DIFF(
            DATE_TRUNC(r.order_date, WEEK(MONDAY)),
            DATE_TRUNC(d.dfd_date, WEEK(MONDAY)),
            WEEK
        )                                                                       AS weeks_since_dfd,
        COUNT(DISTINCT
            CASE WHEN LENGTH(r.stop_tracking_number) <= 1 THEN r.order_id
                 WHEN LENGTH(r.stop_tracking_number) <= 4 THEN CONCAT(r.stop_tracking_number, CAST(r.order_date AS STRING))
                 ELSE COALESCE(NULLIF(r.stop_tracking_number,''), r.stop_id)
            END
        )                                                                       AS total_request,
        COUNT(DISTINCT
            CASE WHEN r.accept_time IS NOT NULL THEN
                CASE WHEN LENGTH(r.stop_tracking_number) <= 1 THEN r.order_id
                     WHEN LENGTH(r.stop_tracking_number) <= 4 THEN CONCAT(r.stop_tracking_number, CAST(r.order_date AS STRING))
                     ELSE COALESCE(NULLIF(r.stop_tracking_number,''), r.stop_id)
                END END
        )                                                                       AS accepted_request,
        COUNT(DISTINCT
            CASE WHEN r.status = 'COMPLETED' THEN
                CASE WHEN LENGTH(r.stop_tracking_number) <= 1 THEN r.order_id
                     WHEN LENGTH(r.stop_tracking_number) <= 4 THEN CONCAT(r.stop_tracking_number, CAST(r.order_date AS STRING))
                     ELSE COALESCE(NULLIF(r.stop_tracking_number,''), r.stop_id)
                END END
        )                                                                       AS completed_request
    FROM dfd_drivers d
    JOIN ahamove_raw.raw_performance r
        ON  r.supplier_id = d.supplier_id
        AND r.order_date >= d.dfd_date
        AND r.order_date <= end_date
    WHERE r.status IN ('CANCELLED','COMPLETED')
        AND r.seq <> 0
        AND r.user_id NOT IN ('84862151477','84862151000')
        AND NOT REGEXP_CONTAINS(r.service_id, '-(INTERCT|TRUCK|RIDE|VAN|PARTNER|TRICYCLE|TEST|PARTNER-BIGC|ASTGROUP|INTERNAL|HUB|BKN|RENT|MASAN)-?')
        AND (r.cancel_time IS NULL OR r.cancel_time >= r.order_time)
        AND (r.cancel_comment IS NULL OR LOWER(r.cancel_comment) NOT LIKE '%user not pay%')
    GROUP BY 1,2,3,4,5
)

-- Final: aggregate theo cohort × city × tuần thứ N
SELECT
    p.dfd_month,
    p.city_id,
    p.weeks_since_dfd,
    p.week,

    -- Volume & Activity
    COUNT(DISTINCT p.supplier_id)                                               AS active_driver,
    SUM(p.active_day)                                                           AS active_day,
    SUM(p.stp_complete)                                                         AS stp_complete,

    -- Online & Productivity
    ROUND(SUM(o.online_hours), 1)                                               AS online_hours,
    ROUND(SAFE_DIVIDE(SUM(o.online_hours), COUNT(DISTINCT p.supplier_id)), 1)  AS avg_online_per_driver,
    ROUND(SAFE_DIVIDE(SUM(p.stp_complete), SUM(o.online_hours)), 2)            AS productivity,

    -- Income
    ROUND(SUM(p.order_income), 0)                                               AS order_income,
    ROUND(SUM(p.reward_income), 0)                                              AS reward_income,
    ROUND(SAFE_DIVIDE(SUM(p.order_income + p.reward_income), COUNT(DISTINCT p.supplier_id)), 0) AS avg_income_per_driver,

    -- AR / FR
    SUM(d.total_request)                                                        AS total_request,
    ROUND(SAFE_DIVIDE(SUM(d.accepted_request),  SUM(d.total_request)) * 100, 1) AS ar_pct,
    ROUND(SAFE_DIVIDE(SUM(d.completed_request), SUM(d.total_request)) * 100, 1) AS fr_pct,

    -- CR POC (loại TikTok)
    ROUND(SAFE_DIVIDE(SUM(p.cancel_order), SUM(p.accept_order)) * 100, 1)     AS cr_pct,
    ROUND(SAFE_DIVIDE(
        SUM(p.cancel_order) - SUM(COALESCE(cp.cancel_poc, 0)) * 0.5,
        SUM(p.accept_order)
    ) * 100, 1)                                                                 AS cr_poc_pct,

    -- Rating
    ROUND(SAFE_DIVIDE(SUM(p.rating_star), NULLIF(SUM(p.rating_order), 0)), 2) AS avg_rating

FROM perf_weekly p
LEFT JOIN online_weekly   o  ON  p.supplier_id = o.supplier_id
                             AND p.week        = o.week
LEFT JOIN demand_weekly   d  ON  p.supplier_id = d.supplier_id
                             AND p.week        = d.week
LEFT JOIN cancel_poc_weekly cp ON p.supplier_id = cp.supplier_id
                              AND p.week        = cp.week

WHERE p.city_id != 'EXP'
GROUP BY 1,2,3,4
ORDER BY 1,2,3
