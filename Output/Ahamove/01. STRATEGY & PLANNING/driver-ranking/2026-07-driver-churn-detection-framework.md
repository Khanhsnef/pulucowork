# Driver Churn Prevention Framework — Ahamove Bike Instant
**Phiên bản:** 2026-07 | Driver Management Team | Tài liệu chiến lược nội bộ

---

## Executive Summary

Ngưỡng churn 30 ngày = đã quá muộn để can thiệp có ý nghĩa. Lyft chứng minh: redefine churn theo gap analysis + uplift modeling tập trung vào nhóm "Persuadables" mang lại ROI retention cao nhất với chi phí thấp nhất. Framework này áp dụng trực tiếp cho Ahamove Bike, dùng data đang có sẵn và tích hợp vào hệ thống AhaBenefits hiện tại.

**3 kết luận then chốt:**
1. Tài xế ở giai đoạn 15-30 ngày active (mới qua học việc, chưa gắn bó) = nhóm dễ churn nhất — cần priority alert riêng.
2. Không chi budget retention vào "Sure Things" (tự ở lại) và "Lost Causes" (đã quyết nghỉ).
3. AhaBenefits + Layer nudge là cơ chế can thiệp tự nhiên — không cần tạo incentive mới.

---

## 1. Định Nghĩa Churn cho Ahamove Bike

Thay ngưỡng cứng 30 ngày bằng hệ thống **Sliding Window Gap**:

| Trạng thái | Định nghĩa | Rank R1/R2 | Rank R3/Unranked |
| :--- | :--- | :--- | :--- |
| **Active** | Có chuyến trong 7 ngày qua | Gap ≤ 5 ngày | Gap ≤ 7 ngày |
| **At-Risk** | Gap tăng bất thường | Gap 5-10 ngày | Gap 7-14 ngày |
| **Slipping** | Không hoạt động kéo dài | Gap 10-15 ngày | Gap 14-21 ngày |
| **Churned** | Chi phí retention > acquisition | Gap > 15 ngày | Gap > 21 ngày |
| **Reactivation** | Quay lại sau churned | Track riêng — reacquisition funnel | Track riêng |

> R1/R2 dùng ngưỡng nghiêm hơn vì mất 1 tài xế R1 = mất capacity L2 Minizone (×1.5 EPH) — tác động trực tiếp đến FR và SLA.

---

## 2. Feature Engineering

| Feature | Công thức tính | Data source |
| :--- | :--- | :--- |
| `gap_days_max_30d` | MAX số ngày liên tiếp không có chuyến trong 30 ngày gần nhất | `trips` table |
| `ar_trend_7d` | AR tuần này / AR tuần trước − 1 (% thay đổi) | `dispatch_logs` |
| `eph_trend_14d` | EPH trung bình 14 ngày / EPH trung bình 30 ngày trước − 1 | `earnings` table |
| `online_time_drop` | Online hours/ngày TB 7 ngày / 30 ngày trước − 1 | `session_logs` |
| `layer_downgrade_count` | Số lần không đăng ký L2/L3 dù đủ điều kiện trong 14 ngày | `layer_registration` |
| `dqs_velocity` | DQS tuần này − DQS 4 tuần trước (delta tuyệt đối) | `quality_score` table |

---

## 3. 4 Behavioral Clusters — Map Ahamove

| Cluster | Tên Ahamove | % Churn ước tính | Đặc điểm hành vi | Rank phổ biến |
| :--- | :--- | :--- | :--- | :--- |
| **C1 — Anchor** | Tài xế Trụ cột | ~[5-10]% | Prod cao ổn định, AR >80%, gap <5 ngày, đang active L2/L3, đổi AhaPoints đều | R1, R2 |
| **C2 — Drifter** | Tài xế Trôi dạt | ~[40-50]% | Prod giảm dần, AR giảm 10-20%, gap tăng lên 10-15 ngày, bắt đầu bỏ đăng ký ca Peak | R3 → Unranked |
| **C3 — Fader** | Tài xế Nhạt dần | ~[65-75]% | Online time giảm >30%, EPH thấp, gap >15 ngày, gần như không đổi điểm | Unranked |
| **C4 — Moonlighter** | Tài xế Thời vụ | ~[15-20]% | Chỉ active cuối tuần/giờ peak, gap trong tuần cao nhưng không rời hẳn | R3, Unranked |

> Số % churn là ước tính tham khảo Lyft — cần validate bằng 6 tháng cohort data Ahamove Bike.

---

## 4. Early Warning Signals — SQL Trigger Logic

```sql
-- TRIGGER 1: Gap Alert (At-Risk detection)
SELECT
    driver_id,
    DATEDIFF(CURRENT_DATE, MAX(completed_at)) AS gap_days,
    rank_current,
    layer_current
FROM trips
WHERE service_type = 'BIKE'
GROUP BY driver_id, rank_current, layer_current
HAVING gap_days BETWEEN 7 AND 14        -- R3/Unranked threshold
    OR (gap_days BETWEEN 5 AND 10 AND rank_current IN ('R1','R2'));
-- Tag: AT_RISK | Priority: CRITICAL nếu R1/R2

-- TRIGGER 2: AR Drop Alert (Disengagement signal)
SELECT
    driver_id,
    ar_7d / NULLIF(ar_prev_7d, 0) - 1 AS ar_pct_change,
    rank_current
FROM driver_weekly_metrics
WHERE ar_7d / NULLIF(ar_prev_7d, 0) - 1 < -0.15  -- AR giảm >15%
  AND trips_7d > 0                                 -- vẫn còn active
  AND service_type = 'BIKE';
-- Tag: AR_DEGRADING | Kết hợp gap_days → composite risk

-- TRIGGER 3: EPH Drop Alert (Earning fatigue)
SELECT
    driver_id,
    eph_14d / NULLIF(eph_30d_lag, 0) - 1 AS eph_pct_change,
    layer_current
FROM driver_earnings_trend
WHERE eph_14d / NULLIF(eph_30d_lag, 0) - 1 < -0.20  -- EPH giảm >20%
  AND service_type = 'BIKE';
-- Tag: EARNING_FATIGUE | Risk cao nhất nhóm Fader

-- COMPOSITE RISK SCORE (0-1 scale)
-- risk_score = (gap_norm × 0.40) + (ar_drop × 0.35) + (eph_drop × 0.25)
-- Threshold: > 0.60 = HIGH_RISK → đưa vào Intervention queue
```

---

## 5. Intervention Matrix

| Nhóm | Cluster map | Chiến lược | Công cụ AhaBenefits | Chi phí |
| :--- | :--- | :--- | :--- | :--- |
| **Sure Things** | C1 Anchor | Duy trì — không can thiệp thêm. Đảm bảo benefit flows ổn định. | Voucher xăng tự động R1/R2, ưu tiên slot L2/L3 đăng ký sớm | Thấp — nhúng sẵn |
| **Persuadables** | C2 Drifter (gap 7-14 ngày, AR đang giảm) | Can thiệp có mục tiêu. **Đây là nhóm ROI cao nhất.** | AhaPoints nudge ("bạn cách [X] pts để đổi voucher xăng 50k"), Captain outreach, suggest shift sang Ca Peak | Trung bình — tập trung toàn bộ retention budget |
| **Lost Causes** | C3 Fader (gap >21 ngày) | Không tốn budget. Offboarding survey. | Không trigger thêm benefit | Rất thấp |
| **Sleeping Dogs** | C4 Moonlighter | Không push thêm — sẽ tự active vào peak. Push sai giờ tăng CPO không cần thiết. | Monitor passively, offer Weekend Layer slot ưu tiên | Gần 0 |

**Playbook Persuadables — Chi tiết can thiệp:**

| Trigger | Hành động | Kênh | SLA |
| :--- | :--- | :--- | :--- |
| Gap = 7 ngày | Push "Bạn đang bỏ lỡ [X] pts hôm nay" + EPH estimate nếu online giờ này | App notification | 24h |
| Gap = 10 ngày | Captain/Đội trưởng liên hệ trực tiếp tài xế trong zone | Zalo / Call | 48h |
| AR drop >15% | Auto-check: deactivate? app lỗi? → Support ticket tự động mở | In-app + CS | 4h |
| EPH drop >20% | Suggest chuyển sang Ca Sáng/Ca Chiều (Peak) + show EPH estimate so sánh | App push | 24h |

---

## 6. Revenue Impact Formula

```
GSV recovered/tháng =
    N_churned_persuadables × Churn_reduction_rate × Avg_trips_per_driver × Avg_GSV_per_trip

CPO impact =
    Drivers_retained × AR_improvement_delta × Trips_recovered / Total_dispatches
    → FR tăng → ít re-dispatch → CPO giảm
```

**Bảng tham số (cần validate):**

| Tham số | Placeholder | Nguồn data cần lấy |
| :--- | :--- | :--- |
| N tài xế Persuadables rời/tháng | [X] tài xế | `driver_activity` cohort 6 tháng |
| Avg trips/driver/month — nhóm Drifter | [X] chuyến | `trips` history |
| Avg GSV/trip — Bike Instant | [X] VND | `pricing` / `trip_revenue` table |
| Churn reduction target (sau intervention) | [X]% | A/B test result |
| **Tổng GSV recovered ước tính** | **[X]M VND/tháng** | Tổng hợp trên |

---

## 7. Implementation Roadmap

| Giai đoạn | Timeline | Hành động chính | Output | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 — Define** | T1-T2 | Validate churn definition với 6 tháng cohort. Build bảng `driver_churn_signals` trong DWH. Xác định baseline churn rate theo Rank/Layer. | Churn baseline report | Data Eng + DM |
| **Phase 2 — Detect** | T3-T4 | Deploy 3 SQL triggers. Tích hợp composite risk score vào Metabase dashboard. Pilot alert flow với Captain team tại 2-3 zone thí điểm. | "At-Risk heatmap" theo zone, daily refresh | DM Ops + DE |
| **Phase 3 — Act** | T5-T6 | A/B test: intervention group vs control trên Persuadables. Đo ΔAR, ΔGDR, ΔGSV sau 30 ngày. Calibrate AhaPoints nudge messaging. Chính thức hóa playbook. | Uplift model validated. Intervention playbook v1 chính thức | DM + Product |

---

## Risks & Next Checks

| Rủi ro | Mức độ | Mitigation |
| :--- | :--- | :--- |
| Gap threshold quá nhạy → false positive → alert fatigue cho Captain | Trung bình | Calibrate theo seasonality: Tết, mưa lớn, mega sales — điều chỉnh ngưỡng tạm thời |
| Push Sleeping Dogs sai giờ → CPO tăng, dispatch lệch zone | Cao | Chỉ trigger trong Ca Peak; không push tài xế Moonlighter giờ thường |
| AhaPoints nudge kém hiệu quả nếu catalog không đủ hấp dẫn | Trung bình | A/B test variant: "X pts = voucher xăng 50k" vs "hoàn thành [X] chuyến hôm nay" |
| Không tách được tự-churn vs bị-deactivate trong data | Cao | Thêm field `churn_reason` vào offboarding flow trước Phase 1 |

**Data cần validate trước Phase 1:**
- Tỷ lệ churn thực tế theo Rank/Layer — 6 tháng gần nhất
- Phân phối `gap_days` thực tế của fleet Bike Instant
- Avg GSV/trip và Avg trips/month theo từng cluster tương đương
- Tỷ lệ tự churn vs bị deactivate — cần tách riêng để không sai target nhóm can thiệp

---

*Driver Management Team | 2026-07 | Review định kỳ: Quý hoặc sau mỗi Mega Sales event*
