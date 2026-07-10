# Driver Churn Detection Framework — Data Design

> **Scope**: Bike Instant (MOTORBIKE + EV-BIKE) | **Owner**: Driver Management — Khanh
> **Mục tiêu**: Data layer phục vụ **scoring model** dự báo churn tài xế, tách 2 cohort NEW / OLD.
> **Ngày**: 2026-07-10

---

## 1. Bài toán & Label

**Định nghĩa churn = Activity-gap** (không phụ thuộc `next_ft_segment`):

| Cohort | Định nghĩa cohort | Gap churn |
|---|---|---|
| **NEW** | `driver_life_time IN ('NIM','NLM')` — 2 tháng đầu | ≥ **14 ngày** không có đơn complete |
| **OLD** | `driver_life_time IN ('N2M','OLD')` — từ tháng 3 | ≥ **30 ngày** không có đơn complete |

- **Gran**: `1 dòng = 1 supplier_id × 1 observation_month`.
- **At-risk flag** (early warning cho serving): 7 ngày im lặng đầu tiên → cờ vàng.
- Label được tính **forward-looking**: đứng ở cuối tháng M, nhìn tới ngày complete kế tiếp; nếu khoảng cách từ đơn cuối (trong/đến hết M) tới đơn kế > ngưỡng cohort → `is_churn = 1`.

## 2. Kiến trúc 3 bảng

```text
┌─────────────────────────┐   train    ┌──────────────────────┐
│ churn_feature_mart      │ ─────────▶ │  Scoring Model (DE)  │
│ supplier × month        │            │  NEW model / OLD model│
│ features + is_churn     │            └──────────┬───────────┘
└─────────────────────────┘                       │ serve
                                                   ▼
┌─────────────────────────┐            ┌──────────────────────┐
│ churn_cohort_summary    │ ◀───────── │  churn_score_daily   │
│ monitor churn theo tier │  monitor   │  risk score / driver │
└─────────────────────────┘            └──────────────────────┘
```

| Bảng | Grain | Vai trò |
|---|---|---|
| `churn_feature_mart` | supplier × month | Training set: feature + label. **File SQL kèm theo.** |
| `churn_score_daily` | supplier × day | Serving: điểm rủi ro cập nhật cho ops can thiệp (build sau khi có model) |
| `churn_cohort_summary` | cohort × city × month | Monitor churn rate theo tier/tenure/city |

## 3. Feature Groups (12 features MVP — tất cả từ field có sẵn)

| Nhóm | Feature | Nguồn |
|---|---|---|
| **Engagement** | `online_hours_m`, `online_hours_mom_delta`, `online_hours_3m_slope`, `active_days_m` | `driver_performance_monthly`, `ops_suppliers_online_hours` |
| **Earnings** | `income_m`, `income_mom_pct`, `rph` (income/online_hour) | monthly |
| **Quality** | `ar`, `cr_poc`, `rating_star`, `fr` | `fct_supplier_performance` |
| **Friction** | `noti_timeout_rate`, `sanction_cnt_3m` | `fct`, `supplier_sanction` |
| **Recency** | `days_since_last_order`, `atrisk_flag` | `raw_performance` / `fct` |
| **Static** | `age`, `gender`, `city_id`, `is_ev`, `driver_life_time` | `supplier_raw` |

**Tín hiệu leading mạnh nhất** (ưu tiên monitoring): ↓ `online_hours_3m_slope`, ↓ `income_mom_pct`, ↑ `days_since_last_order`, ↑ `cr_poc`/`noti_timeout_rate`.

## 4. Filter chuẩn (áp dụng xuyên suốt)

```sql
JSON_EXTRACT_SCALAR(extra,'$.vehicle_type') IN ('MOTORBIKE','EV-BIKE')
COALESCE(email,'a')    NOT LIKE '%ahamove_ka_lazada%'
COALESCE(services,'a') NOT LIKE '%VNM-WH-DELIVERY%'
COALESCE(services,'a') NOT LIKE '%VNM-WH-VENDOR%'
COALESCE(tags,'a')     NOT LIKE '%SALESFORCE%'
partitioned_create_time >= '2010-01-01'
-- driver active tháng M: stp_complete > 0, age >= 22
```

## 5. Roadmap

1. **[Bước này]** Build `churn_feature_mart` SQL → verify label distribution (churn rate NEW vs OLD hợp lý ~?).
2. Feature QA: kiểm null, phân phối, correlation với label.
3. DE train model riêng NEW / OLD (logistic/GBT) → validate AUC, precision@k.
4. Build `churn_score_daily` serving + `churn_cohort_summary` monitor.
5. Ops playbook can thiệp theo risk tier.

## ⚠️ Cần verify trước khi chạy production

- Giá trị thực của `driver_life_time`: có đúng `'NIM','NLM','N2M','OLD'` không (đặc biệt `'N2M'`).
- Field `sanction_cnt` từ `supplier_sanction` — tên bảng/field chính xác.
- `active_days` — có field sẵn trong monthly hay phải count từ daily `fct`.
