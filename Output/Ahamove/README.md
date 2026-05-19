# Ahamove — Driver Management Output Index

**Owner:** Lê Phương Khanh | Driver Management Leader  
**Scope:** Xe máy (Instant) — Giao ngay 1H, Siêu tốc, Ghép đơn, 4H

---

## Cấu Trúc Thư Mục

```
Output/Ahamove/
│
├── 01. STRATEGY & PLANNING/        # Chiến lược cung ứng, Tiering, OKR, Roadmap
│   ├── docs/                       # File .docx (PRD, Strategy decks)
│   ├── sql/                        # BigQuery queries dùng cho strategy analysis
│   └── templates/                  # Template tái sử dụng (Ops One-Pager, Brief)
│
├── 02. CAMPAIGNS_PROJECTS/         # Campaign incentive, Mega Sales, Rollout Projects
│   ├── landing-pages/              # HTML landing pages (tuyển dụng, campaign)
│   ├── images/                     # Assets: logo, ảnh tài xế, brand assets
│   ├── briefs/                     # Campaign brief (mục tiêu, budget, target)
│   └── results/                    # Post-campaign analysis (kết quả thực tế vs target)
│
├── 03. DRIVER_COMMUNITY/           # Community engagement, offline/online events
│   ├── events/                     # Kế hoạch event, Run-of-Show, checklist
│   ├── comms/                      # Zalo message, push notification, SMS template
│   └── content/                    # Social post, newsletter, Zalo OA content
│
├── 04. OPS_METRICS/                # Dashboard, SQL, data vận hành hàng ngày
│   ├── sql/                        # BigQuery queries: AR, FR, CPO, SLA
│   ├── dashboards/                 # Dashboard spec, layout, config
│   └── raw-data/                   # CSV export từ Aira / BigQuery
│
├── 05. ANALYSIS & REPORTS/         # Phân tích chuyên sâu, báo cáo định kỳ
│   ├── monthly/                    # Monthly performance report
│   ├── root-cause/                 # RCA: AR drop, supply shock, fraud investigation
│   └── unit-economics/             # CPO breakdown, EPH/RPH, LTV/CAC analysis
│
├── 06. COMPETITIVE_INTEL/          # Thông tin đối thủ (Grab, Be, XanhSM, SPX, GHN)
│   ├── battlecards/                # Battlecard từng đối thủ (strengths, counters)
│   ├── monitoring/                 # Weekly intel snapshot, signal log
│   └── war-gaming/                 # Scenario analysis, competitor response model
│
└── 07. TEAM_MANAGEMENT/            # Quản lý subteam DM, đào tạo, hiệu suất
    ├── training/                   # Training materials, SOP, onboarding
    ├── 1on1/                       # 1:1 notes, coaching logs
    └── performance/                # Performance review, OKR assignment
```

---

## File Index

| File | Folder | Mô tả |
|------|--------|-------|
| `2026-q2-dm-team-okr.md` | 01. STRATEGY | OKR Q2 2026 — DM Team |
| `2026-q2-okr-dm-internal.md` | 01. STRATEGY | OKR Q2 internal (full KR breakdown) |
| `2026-q2-okr-dm-internal.xlsx` | 01. STRATEGY | OKR tracking spreadsheet |
| `OKR Q2-2026 - DM Team (Khanh Le).xlsx` | 01. STRATEGY | OKR gốc từ leadership |
| `Ahamove_FT_Driver_Pool_PRD.docx` | 01. STRATEGY/docs | PRD: Full-time Driver Pool |
| `Supply Strategy 2026 - Internal.docx` | 01. STRATEGY/docs | Supply strategy document |
| `2026-04-ahamove-selex-landing.html` | 02. CAMPAIGNS/landing-pages | Landing page Selex EV campaign |
| `Cancel 12.csv` | 04. OPS_METRICS/raw-data | Raw cancel data tháng 12 |
| `Cancel 2_3.csv` | 04. OPS_METRICS/raw-data | Raw cancel data tháng 2-3 |
| `2026-03-fuel-price-impact-analysis.xlsx` | 05. ANALYSIS | Phân tích tác động giá xăng Q1 |
| `2026-Q2-DM-OKR-assignment.xlsx` | 07. TEAM_MGMT | OKR assignment cho từng member |
| `dm-weekly-review-template.pptx` | 07. TEAM_MGMT | Template weekly review DM team |
| `2026-05-claude-guide-for-team.md` | 07. TEAM_MGMT | Hướng dẫn Claude AI toàn diện cho team (dành cho người chưa biết gì) |
| `2026-05-ev-charging-financial-model.html` | 01. STRATEGY | Financial model EV charging station VN: CAPEX/OPEX/IRR/NPV 3 station types, 4 business models, EVN tariff 2025 |
| `2026-05-ao-khi-campaign-plan.md` | 02. CAMPAIGNS | Kế hoạch truyền thông 990 áo khỉ — 2 track: bán 800 áo 120k (gắn KPI AR/FR) + tặng 190 áo (EV/tuyển dụng). Target 1,500+ đăng ký tạo hiệu ứng khan hiếm. |
| `2026-05-ao-khi-comms-drafts.md` | 02. CAMPAIGNS | Draft nội dung post/push/Lark sẵn sàng gửi — đủ 5 ngày Phase 2, form cấu trúc, message kết quả cá nhân. |
| `2026-05-ao-khi-campaign-tracker.xlsx` | 02. CAMPAIGNS | **Master tracker 6 sheets**: Plan timeline, Nội dung truyền thông copy-paste, Google Form setup, Slot tracking (công thức tự tính), Track B EV gift, Checklist 31 items. |

---

*Last updated: 2026-05-19*
