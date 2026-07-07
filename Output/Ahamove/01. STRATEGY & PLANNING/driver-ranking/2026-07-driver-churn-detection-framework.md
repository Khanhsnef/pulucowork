# Driver Churn Detection Framework — Ahamove Bike Instant

**Phiên bản:** 2026-07 | Driver Management Team | Tài liệu chiến lược nội bộ

---

## Executive Summary

Ngưỡng 30 ngày không hoạt động = đã quá muộn để can thiệp. Thay vào đó, framework này cluster tài xế **thuần theo hành vi thực tế** — số ngày hoạt động, tần suất chuyến, pattern giờ online, quỹ đạo thu nhập — không phụ thuộc vào tier R1/R2/R3.

**3 nguyên tắc cốt lõi:**

1. **Behavior beats label.** Tài xế cùng tier R3 có thể thuộc 3 nhóm hành vi hoàn toàn khác nhau — cần can thiệp khác nhau.
2. **Cửa sổ can thiệp tối ưu: ngày 3–7 sau khi gap bắt đầu.** Trước đó = false positive; sau đó = đã muộn.
3. **Chỉ chi budget cho "Persuadables"** — nhóm sẽ churn NẾU không được can thiệp, nhưng vẫn còn receptive.

---

## 1. Định Nghĩa Churn — Behavioral Gap Model

Không dùng ngưỡng cứng 30 ngày. Churn được định nghĩa theo **pattern gap cá nhân hóa**:

```text
Personal Gap Baseline (PGB) = median(gap_days) của tài xế đó trong 60 ngày qua
Churn Signal = gap hiện tại > MAX(PGB × 2.5, 7 ngày)
```

| Trạng thái | Định nghĩa behavioral |
| :--- | :--- |
| **Active** | Có chuyến trong 3 ngày qua; gap ≤ PGB |
| **Cooling** | Gap = PGB × 1.0–1.5 — bắt đầu giảm frequency |
| **At-Risk** | Gap = PGB × 1.5–2.5 — lệch rõ khỏi pattern cá nhân |
| **Churned** | Gap > PGB × 2.5 **hoặc** > 14 ngày tuyệt đối (với tài xế mới < 60 ngày tenure) |
| **Reactivation** | Quay lại sau Churned — track riêng, không nhập chung Active |

> **Tại sao dùng PGB?** Tài xế chạy 1 ngày/tuần sẽ luôn bị flag sai nếu dùng ngưỡng cứng. PGB cá nhân hóa ngưỡng theo thực tế từng người.

---

## 2. Feature Engineering — Behavioral Dimensions

| Feature | Công thức | Ý nghĩa |
| :--- | :--- | :--- |
| `active_days_30d` | Số ngày có ≥1 chuyến trong 30 ngày gần nhất | Mức độ cam kết tổng thể |
| `trips_per_active_day` | Tổng chuyến / active_days_30d | Cường độ khi đã online |
| `online_hours_per_day` | Tổng giờ online / active_days_30d | Thời lượng làm việc |
| `hour_consistency_score` | Std dev của giờ bắt đầu ca trong 30 ngày (thấp = ổn định) | Có pattern giờ cố định không |
| `gap_days_current` | DATEDIFF(today, MAX(last_trip_date)) | Recency — gap đang kéo dài bao lâu |
| `gap_trend` | gap_days_current / PGB − 1 | Lệch bao nhiêu so với pattern cá nhân |
| `eph_trajectory` | EPH(7d) / EPH(30d) − 1 | Thu nhập/giờ đang tăng hay giảm |
| `ar_trajectory` | AR(7d) / AR(30d) − 1 | Mức độ chấp nhận đơn đang thay đổi |
| `tenure_days` | Số ngày kể từ chuyến đầu tiên | Độ gắn bó lịch sử |

---

## 3. Behavioral Clusters — 5 Nhóm Tài Xế

Clustering dựa trên `active_days_30d`, `hour_consistency_score`, `eph_trajectory`, `tenure_days`.

### B1 — Full-timer Ổn định

> **"Cần cơm hàng ngày"**

| Chỉ số | Giá trị điển hình |
| :--- | :--- |
| Active days/tháng | ≥ 20 ngày |
| Online hours/ngày | 6–10h |
| Hour consistency | Thấp (pattern rõ, giờ cố định sáng/chiều) |
| EPH trajectory | Ổn định hoặc tăng nhẹ |
| Gap current | 0–2 ngày |

**Hành vi:** Chạy gần như mỗi ngày, có giờ làm cố định, thu nhập từ Ahamove là nguồn chính. Ít churn nhưng **rất nhạy với EPH giảm hoặc zone bị giảm đơn** — nếu kiếm được ít hơn tuần này, tuần sau sẽ thử platform khác.

**Churn risk:** Thấp (~[5-15]%), nhưng khi churn thì mất đột ngột.

---

### B2 — Part-timer Đều Đặn

> **"Chạy có kế hoạch"**

| Chỉ số | Giá trị điển hình |
| :--- | :--- |
| Active days/tháng | 10–19 ngày |
| Online hours/ngày | 3–5h |
| Hour consistency | Trung bình (thường cuối tuần + 1-2 buổi chiều) |
| EPH trajectory | Ổn định |
| Gap current | 2–5 ngày (bình thường) |

**Hành vi:** Coi Ahamove như nguồn thu nhập thứ hai, có việc khác. Chạy đều và chủ động, ít complain. Ổn định nếu giờ peak vẫn kiếm được tốt.

**Churn risk:** Thấp–Trung bình (~[15-25]%). Dễ giữ nếu peak hours accessible.

---

### B3 — Newbie Chưa Gắn Bó

> **"Đang thử xem có ổn không"**

| Chỉ số | Giá trị điển hình |
| :--- | :--- |
| Tenure | < 60 ngày |
| Active days/tháng | Biến động lớn (5–15 ngày, không đều) |
| Hour consistency | Cao (chưa có pattern — giờ random) |
| EPH trajectory | Không rõ xu hướng |
| Gap current | Khó đoán — có thể 0 ngày hoặc 10 ngày |

**Hành vi:** Đây là nhóm **nguy hiểm nhất** — đúng như Lyft phát hiện (15–30 ngày active dễ churn nhất). Mới vượt qua onboarding nhưng chưa hình thành thói quen. Một tuần thu nhập thấp = quyết định bỏ.

**Churn risk:** Cao (~[45-65]%). **Priority alert riêng cho nhóm này.**

---

### B4 — Declining Drifter

> **"Đang dần rút lui"**

| Chỉ số | Giá trị điển hình |
| :--- | :--- |
| Tenure | ≥ 60 ngày (từng active) |
| Active days/tháng | Giảm liên tục 3 tháng gần nhất |
| EPH trajectory | Âm hoặc giảm |
| AR trajectory | Giảm >10% so với 30 ngày trước |
| Gap trend | gap_current / PGB > 1.5 |

**Hành vi:** Từng là Full-timer hoặc Part-timer ổn định, đang dần giảm — có thể do tìm được việc khác, burn out, hoặc platform khác trả hơn. Pattern: giảm từ từ, không bỏ đột ngột.

**Churn risk:** Rất cao (~[60-75]%). **Đây là nhóm "Persuadables" chính — ROI retention cao nhất.**

---

### B5 — Seasonal/Opportunist

> **"Chỉ xuất hiện khi có lợi"**

| Chỉ số | Giá trị điển hình |
| :--- | :--- |
| Active days/tháng | Thấp (3–8 ngày) nhưng **ổn định theo pattern tuần/tháng** |
| Hour consistency | Cao (luôn chạy cuối tuần hoặc ngày lễ) |
| EPH khi active | Cao — chọn giờ peak rất tốt |
| Gap current | Cao tuyệt đối nhưng không lệch PGB |

**Hành vi:** Không phải churn — đây là lựa chọn của họ. Xuất hiện đúng giờ cao điểm, EPH tốt, không cần push. **Push sai giờ tăng CPO vô ích.**

**Churn risk:** Thấp ([10-20]%) nếu đo đúng cách. Không cần retention budget.

---

## 4. Churn Risk Matrix

|  | **Tenure thấp (<60 ngày)** | **Tenure cao (≥60 ngày)** |
| :--- | :--- | :--- |
| **Active days giảm** | 🔴 B3 Newbie — CRITICAL | 🔴 B4 Declining — HIGH |
| **Active days ổn định** | 🟡 B3 Newbie (theo dõi) | 🟢 B1/B2 — LOW |
| **Gap >> PGB** | 🔴 CRITICAL — bất kể cluster | 🟠 HIGH — can thiệp ngay |
| **EPH giảm >20%** | 🟠 HIGH | 🟠 HIGH |
| **AR giảm >15%** | 🟡 MEDIUM | 🟡 MEDIUM |

---

## 5. Early Warning SQL — Behavioral Triggers

```sql
-- ==================================================
-- STEP 1: Tính Personal Gap Baseline cho mỗi tài xế
-- ==================================================
WITH driver_gaps AS (
    SELECT
        driver_id,
        completed_at,
        DATEDIFF(completed_at, LAG(completed_at) OVER (
            PARTITION BY driver_id ORDER BY completed_at
        )) AS gap_days
    FROM trips
    WHERE service_type = 'BIKE'
      AND completed_at >= DATE_SUB(CURRENT_DATE, INTERVAL 60 DAY)
),
pgb AS (
    SELECT
        driver_id,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY gap_days) AS personal_gap_baseline
    FROM driver_gaps
    WHERE gap_days IS NOT NULL
    GROUP BY driver_id
),

-- ==================================================
-- STEP 2: Behavioral feature snapshot hiện tại
-- ==================================================
behavioral_snapshot AS (
    SELECT
        t.driver_id,
        COUNT(DISTINCT DATE(t.completed_at))              AS active_days_30d,
        COUNT(*)                                           AS trips_30d,
        DATEDIFF(CURRENT_DATE, MAX(t.completed_at))       AS gap_current,
        STDDEV(HOUR(t.created_at))                        AS hour_consistency_score,
        DATEDIFF(CURRENT_DATE, MIN(t.completed_at))       AS tenure_days
    FROM trips t
    WHERE t.service_type = 'BIKE'
      AND t.completed_at >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    GROUP BY t.driver_id
)

-- ==================================================
-- STEP 3: Gán cluster + churn risk
-- ==================================================
SELECT
    b.driver_id,
    b.active_days_30d,
    b.gap_current,
    p.personal_gap_baseline                               AS pgb,
    b.gap_current / NULLIF(p.personal_gap_baseline, 0)   AS gap_ratio,
    b.tenure_days,
    CASE
        WHEN b.tenure_days < 60 AND b.active_days_30d < 12 THEN 'B3_NEWBIE'
        WHEN b.tenure_days >= 60
             AND b.gap_current > p.personal_gap_baseline * 1.5 THEN 'B4_DECLINING'
        WHEN b.active_days_30d >= 20                           THEN 'B1_FULLTIME'
        WHEN b.active_days_30d BETWEEN 10 AND 19               THEN 'B2_PARTTIME'
        ELSE                                                        'B5_SEASONAL'
    END AS behavior_cluster,
    CASE
        WHEN b.gap_current > GREATEST(p.personal_gap_baseline * 2.5, 7) THEN 'CHURNED'
        WHEN b.gap_current > p.personal_gap_baseline * 1.5               THEN 'AT_RISK'
        WHEN b.gap_current > p.personal_gap_baseline * 1.0               THEN 'COOLING'
        ELSE                                                                   'ACTIVE'
    END AS churn_status
FROM behavioral_snapshot b
JOIN pgb p USING (driver_id)
WHERE b.gap_current > 3  -- chỉ lấy tài xế đang có gap đáng kể
ORDER BY gap_ratio DESC;
```

---

## 6. Intervention Playbook theo Cluster

| Cluster | Churn Status | Hành động | Kênh | Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| **B3 Newbie** | AT_RISK (gap > 7 ngày) | Gọi điện trực tiếp + hỏi barrier (app lỗi? đơn ít? thu nhập thấp hơn kỳ vọng?) | Call/Zalo | 🔴 P0 |
| **B4 Declining** | COOLING → AT_RISK | Earnings comparison: "Tháng trước bạn kiếm [X], tuần này chỉ [Y] — muốn chúng tôi giúp tìm giờ cao điểm tốt hơn?" | App push + Captain | 🔴 P0 |
| **B1 Full-timer** | AT_RISK | Kiểm tra ngay: deactivate? tai nạn? app bug? → Open CS ticket tự động | Auto-CS + SMS | 🟠 P1 |
| **B2 Part-timer** | AT_RISK | Nhẹ hơn — gợi ý ca phù hợp với pattern lịch sử của họ | App push | 🟡 P2 |
| **B5 Seasonal** | Gap cao | **Không làm gì.** Gap cao là bình thường với họ. | — | ⬜ Skip |
| **Bất kỳ** | CHURNED (>14 ngày) | Không tốn budget retention. Offboarding survey ngắn (1 câu): "Lý do chính bạn không chạy Ahamove?" | SMS 1 lần | ⬜ Data only |

---

## 7. Cohort Survival — Ưu Tiên Theo Tenure

Dựa trên Lyft survival analysis, **2 giai đoạn nguy hiểm nhất:**

```text
Tuần 2–4   (tenure 8–28 ngày)  → Newbie chưa hình thành thói quen
Tháng 3–4  (tenure 60–120 ngày) → Honeymoon period kết thúc, so sánh với platform khác
```

**Cohort alert tự động cần setup:**
- D+7 sau chuyến đầu tiên: onboarding check-in ("bạn đã kiếm được [X] trong tuần đầu")
- D+30: earnings summary + gợi ý giờ peak tốt nhất theo zone của họ
- D+90: loyalty nudge — "Bạn đã hoàn thành [X] chuyến, cách [Y] chuyến để đổi [benefit]"

---

## 8. Revenue Impact Formula

```text
GSV recovered/tháng =
    N_persuadables_at_risk × retention_rate_uplift × avg_trips_per_driver × avg_GSV_per_trip

Trong đó:
    N_persuadables_at_risk = B3 + B4 có churn_status = AT_RISK trong tháng
    retention_rate_uplift  = % tăng retention sau intervention (cần A/B test — target: +[X]%)
    avg_trips_per_driver   = [X] chuyến/tháng (pull từ cohort B3/B4 trước khi AT_RISK)
    avg_GSV_per_trip        = [X] VND (Bike Instant)
```

| Tham số | Placeholder | Nguồn |
| :--- | :--- | :--- |
| N B3 AT_RISK / tháng | [X] tài xế | `behavioral_snapshot` + cohort |
| N B4 AT_RISK / tháng | [X] tài xế | `behavioral_snapshot` + cohort |
| Avg trips trước churn — B3 | [X] chuyến | `trips` history 30d trước churn date |
| Avg trips trước churn — B4 | [X] chuyến | `trips` history 30d trước churn date |
| Avg GSV/trip Bike Instant | [X] VND | `trip_revenue` |
| Retention uplift target | [X]% | A/B test Phase 3 |

---

## 9. Implementation Roadmap

| Phase | Timeline | Hành động | Output |
| :--- | :--- | :--- | :--- |
| **1 — Baseline** | T1–T2 | Pull PGB distribution cho toàn fleet. Validate 5 clusters bằng 6 tháng cohort. Đo churn rate thực tế từng cluster. | Cluster baseline report + validated thresholds |
| **2 — Detect** | T3–T4 | Deploy SQL pipeline vào DWH. Dashboard "At-Risk by Cluster" trên Metabase. Pilot Captain alert cho B3/B4 tại 2–3 zone. | Daily at-risk feed; heatmap theo zone |
| **3 — Act** | T5–T6 | A/B test intervention: B3 (call script) vs B4 (earnings nudge). Đo Δactive_days, ΔGDR, ΔGSV sau 30 ngày. | Uplift validated. Playbook v1 chính thức. |

---

## Risks

| Rủi ro | Mức | Mitigation |
| :--- | :--- | :--- |
| PGB sai với tài xế mới (<30 ngày data) | Cao | Dùng fleet median làm fallback PGB cho tenure <30 ngày |
| B5 Seasonal bị flag sai là AT_RISK | Trung bình | Thêm điều kiện `hour_consistency_score` thấp vào filter B5 |
| Alert fatigue cho Captain nếu volume B3/B4 quá lớn | Trung bình | Cap alert tối đa 20 drivers/Captain/ngày; ưu tiên gap_ratio cao nhất |
| Không phân biệt tự-churn vs deactivated | Cao | Thêm `churn_reason` field vào offboarding trước Phase 1 |

---

---

_Driver Management Team | 2026-07 | Review định kỳ: Quý hoặc sau Mega Sales event_
