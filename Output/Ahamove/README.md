# Ahamove — Driver Management Output Index

**Owner:** Lê Phương Khanh | Driver Management Leader  
**Scope:** Xe máy (Instant) — Giao ngay 1H, Siêu tốc, Ghép đơn, 4H  
**Last updated:** 2026-06-22

---

## Cấu Trúc Thư Mục

```
Output/Ahamove/
│
├── 01. STRATEGY & PLANNING/        # Chiến lược cung ứng, Tiering, OKR, Roadmap
│   ├── ahabenefits/                # AhaBenefits points flow & proposal
│   ├── driver-journey/             # Driver Journey framework, milestones, proposal
│   ├── driver-ranking/             # Ranking params, layer benefits, priority registration
│   ├── ev-transition/              # EV charging financial model
│   ├── okr/                        # OKR Q2 2026 (md + xlsx)
│   ├── team-restructure/           # Kickoff docs tái cơ cấu team
│   ├── docs/                       # PRD, Strategy decks (.docx)
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

## 📁 File Index — Đầy Đủ

### 01. STRATEGY & PLANNING

#### `ahabenefits/`
| File | Mô tả |
|------|-------|
| `2026-05-ahabenefits-points-flow.md` | Points flow diagram & logic (markdown) |
| `2026-05-ahabenefits-points-flow.html` | Points flow — bản HTML tương tác |
| `2026-05-ahabenefits-proposal.html` | Proposal chính thức AhaBenefits |

#### `driver-journey/`
| File | Mô tả |
|------|-------|
| `2026-05-driver-journey-framework.md` | Framework Driver Journey v3 (markdown) |
| `2026-05-driver-journey-framework.html` | Framework — bản HTML |
| `2026-05-driver-lifecycle-journey.md` | Full lifecycle deep-dive (68KB) |
| `2026-05-driver-lifecycle-journey.html` | Lifecycle — bản HTML tương tác (gồm KPI Nhi, Weekly Health, Execution Roadmap by Milestone) |
| `2026-05-driver-journey-summary.md` | **One-pager tóm tắt** — Journey 2 giai đoạn, KPI Nhi (monthly), Weekly Health, Next Actions theo PIC (Ops/Product/PA) |
| `2026-05-driver-journey-summary.html` | One-pager — bản HTML dark theme (6 section: Vấn đề · Journey · KPI · Weekly Health · Next Actions · Scope) |
| `2026-06-driver-journey-milestones.md` | **Driver Journey v4.0 — 5 Phase × 25 Milestones** gắn Ranking Params v2.0 |
| `2026-06-driver-journey-proposal.md` | **PROPOSAL SCR format** — Situation/Complication/Resolution + Cohort Retention Baseline Jan 2025–Apr 2026 |
| `2026-06-driver-journey-proposal.html` | HTML report tương tác — dark theme, sidebar nav, Timeline SVG, Cohort heatmap |
| `2026-06-driver-journey-presenter-guide.html` | Presenter guide — talking points, objection handling, 3 closing asks |

#### `driver-ranking/`
| File | Mô tả |
|------|-------|
| `2026-05-driver-ranking-params.md` | Ranking params spec (markdown) |
| `2026-05-driver-ranking-params.html` | Ranking params — bản HTML (sheet chi tiết 9 mục) |
| `2026-05-driver-ranking-diagram.html` | Sơ đồ tổng quan 1 trang (card flow) — dùng để present |
| `2026-05-driver-ranking-layer-benefits.html` | Layer benefits visualization |
| `2026-05-driver-ranking-finalized.html` | Finalized ranking system |
| `2026-05-driver-ranking-priority-registration.md` | Priority registration spec |
| `2026-05-driver-ranking-priority-registration.html` | Priority registration — bản HTML |
| `2026-05-driver-ranking-ahabenefits-combined.docx` | Combined ranking + AhaBenefits (.docx) |
| `2-2026-05-driver-ranking-ahabenefits-combined.docx` | Phiên bản v2 combined doc |

#### `ev-transition/`
| File | Mô tả |
|------|-------|
| `2026-05-ev-charging-financial-model.html` | **Financial model EV charging** — CAPEX/OPEX/IRR/NPV, 3 loại trạm, 4 business model, EVN tariff 2025 |

#### `okr/`
| File | Mô tả |
|------|-------|
| `2026-q2-dm-team-okr.md` | OKR Q2 2026 — DM Team (đầy đủ) |
| `2026-q2-okr-dm-internal.md` | OKR Q2 internal — full KR breakdown |
| `2026-q2-okr-dm-internal.xlsx` | OKR tracking spreadsheet |
| `OKR Q2-2026 - DM Team (Khanh Le).xlsx` | OKR gốc từ leadership |

#### `team-restructure/`
| File | Mô tả |
|------|-------|
| `2026-06-driver-restructure-kickoff.md` | Kickoff doc tái cơ cấu (markdown) |
| `2026-06-driver-restructure-kickoff.docx` | Kickoff doc — bản Word full |
| `2026-06-driver-restructure-kickoff_Format_Dep.docx` | Phiên bản format đẹp cho Dep |

#### `docs/`
| File | Mô tả |
|------|-------|
| `Ahamove_FT_Driver_Pool_PRD.docx` | PRD: Full-time Driver Pool |
| `Supply Strategy 2026 - Internal.docx` | Supply strategy document (internal) |

#### Root của `01. STRATEGY & PLANNING/`
| File | Mô tả |
|------|-------|
| `2026-06-driver-journey-milestones.html` | Milestones HTML standalone (77KB) |
| `2026-06-open-source-repos-application.md` | Tài liệu chiến lược ứng dụng open-source repositories vào tối ưu vận hành |

---

### 02. CAMPAIGNS_PROJECTS

#### Root
| File | Mô tả |
|------|-------|
| `2026-04-baga-driver-slides.html` | Baga driver recruitment slides |
| `2026-05-ao-khi-campaign-plan.md` | Kế hoạch truyền thông 990 áo khỉ — 2 track: bán 800 áo 120k + tặng 190 áo |
| `2026-05-ao-khi-comms-drafts.md` | Draft nội dung post/push/Lark sẵn sàng gửi — 5 ngày Phase 2 |
| `2026-05-ao-khi-campaign-tracker.xlsx` | **Master tracker 6 sheets**: Plan, Nội dung, Form, Slot tracking, Track B EV, Checklist 31 items |
| `2026-05-ao-khi-gantt-plan.xlsx` | **Gantt-style plan 3 sheets**: Timeline 4 tuần, Phân tích SC/CN vs TL, Nội dung 5 bài |
| `2026-05-mar-weekly-w20.pptx` | Weekly review W20 presentation |
| `create-form.gs` | Google Apps Script tạo form tự động |

#### `landing-pages/`
| File | Mô tả |
|------|-------|
| `2026-04-ahamove-selex-landing.html` | Landing page Selex EV campaign |
| `index.html` | Landing page index (mirror) |

---

### 04. OPS_METRICS

#### Root
| File | Mô tả |
|------|-------|
| `weekly-ops-dashboard.xlsx` | Dashboard vận hành tuần (master) |
| `copyweekly-ops-dashboard.xlsx` | Copy backup dashboard |
| `daily-ops-report-template.xlsx` | Template báo cáo ops hàng ngày |

#### `dashboards/`
| File | Mô tả |
|------|-------|
| `incentive_simulation_app.py` | App Streamlit giả lập incentive giờ cao điểm & tối ưu nguồn cung |
| `sgn_overview_dashboard.py` | SGN Ops Overview dashboard — live pull từ Google Sheet `SGN Overview` |

#### `sql/`
| File | Mô tả |
|------|-------|
| `q1-active-trend-fixed.sql` | Query active driver trend Q1 |
| `q2-driver-monthly-activity.sql` | Query monthly activity breakdown |
| `q3-cohort-retention.sql` | Query cohort retention analysis |
| `q4-segment-transition.sql` | Query segment transition tracking |

#### `raw-data/`
| File | Mô tả |
|------|-------|
| `Cancel 12.csv` | Raw cancel data tháng 12 |
| `Cancel 2_3.csv` | Raw cancel data tháng 2–3 |
| `active trend.xlsx` | Active driver trend export |
| `Analyze bấy bá - phần 2 - active.csv` | Active data phân tích dispatch (10MB) |
| `Analyze bấy bá - phần 2 - dispatch.csv` | Dispatch data phân tích (1.8MB) |
| `Analyze bấy bá - phần 2 - dispatch 2.csv` | Dispatch data v2 (1.8MB) |

---

### 05. ANALYSIS & REPORTS

#### Root
| File | Mô tả |
|------|-------|
| `2026-03-fuel-price-impact-analysis.xlsx` | Phân tích tác động giá xăng Q1 2026 |
| `2026-05-active-segment-trend.html` | Active driver segment trend analysis |
| `2026-05-analysis-fr-decline-dispatch-impact.html` | FR decline & dispatch impact analysis |
| `2026-05-biweekly-hod-report.md` | Bi-weekly HoD report template |
| `2026-05-fr-decline-all-services-analysis.html` | FR decline — full services breakdown |
| `2026-05-fr-decline-root-cause-analysis.html` | FR decline root cause analysis |
| `2026-06-pulu-smartflow-risk-assessment.md` | **Đánh giá rủi ro & đề xuất bảo mật/hiệu năng** hệ thống PuluSmartFlow |
| `data-spec-driver-analysis.html` | Data spec cho driver analysis queries |

---

### 06. COMPETITIVE_INTEL

#### Root
| File | Mô tả |
|------|-------|
#### `monitoring/`
| File | Mô tả |
|------|-------|
| `2026-06-22-weekly-market-brief.md` | BẢN TIN VẬN HÀNH & THỊ TRƯỜNG ĐẦU TUẦN (16/06 - 22/06/2026) |
| `2026-06-22-weekly-market-brief.html` | Bản HTML tương tác của Bản tin thị trường đầu tuần 22/06 |
| `2026-06-22-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 22/06: ShopeeFood tuyển dụng mạnh, Uber thâu tóm Getir |
| `2026-06-22-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 22/06 |
| `2026-06-21-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 21/06: ShopeeFood campaign siêu sale, Uber liên minh Robotaxi, DoorDash mở rộng Grocery |
| `2026-06-21-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 21/06 |
| `2026-06-20-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 20/06: ShopeeFood siêu sale 21/6, DoorDash tung Summer of DashPass |
| `2026-06-20-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 20/06 |
| `2026-06-19-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 19/06: GSM thay CEO (Nguyễn Văn Thanh rời ghế) & DoorDash gặp sự cố |
| `2026-06-19-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 19/06 |
| `2026-06-18-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 18/06: Uber tập trung Robotaxi & Be kết hợp B2B y tế |
| `2026-06-18-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 18/06 |
| `2026-06-17-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 17/06: GSM ký Taxi Quê Lụa, GrabBenefits & Be Group EV lobby |
| `2026-06-17-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 17/06 |
| `2026-06-16-competitor-intel-report.md` | Báo cáo giám sát cạnh tranh ngày 16/06: GSM thay CEO toàn cầu & Be Group PR campaign |
| `2026-06-16-competitor-intel-report.html` | Bản HTML tương tác của báo cáo giám sát cạnh tranh ngày 16/06 |
| `2026-06-16-weekly-market-brief.md` | Bản tin vận hành & thị trường đầu tuần ngày 16/06: Grab EV, XanhSM thắt chặt P&L, luật ILO mới |
| `2026-06-16-weekly-market-brief.html` | Bản HTML tương tác của bản tin vận hành & thị trường đầu tuần ngày 16/06 |

---

### 07. TEAM_MANAGEMENT

#### Root
| File | Mô tả |
|------|-------|
| `2026-05-claude-guide-for-team.md` | Hướng dẫn Claude AI toàn diện cho team (người chưa biết gì) |
| `2026-05-claude-guide-for-team.pdf` | Bản PDF để share |
| `2026-05-claude-complete-training-guide.html` | Complete training guide — HTML format |
| `2026-05-claude-training-presenter-guide.html` | Presenter guide cho buổi training Claude |
| `2026-05-pulu-workspace-architecture-guide.html` | Hướng dẫn kiến trúc workspace Pulu-workspace |
| `2026-06-dm-org-chart-raci.html` | Org chart & RACI matrix DM team |
| `2026-06-nhi-scope-new-driver.html` | Scope tuyển dụng tài xế mới (Nhi) |
| `2026-06-new-dashboard-sop.md` | SOP quy trình xây dựng Dashboard mới bằng DuckDB & Streamlit |
| `2026-Q2-DM-OKR-assignment.xlsx` | OKR assignment từng member DM team |
| `dm-weekly-review-template.pptx` | Template weekly review DM team |
| `gen_pdf.py` | Script tạo PDF từ markdown |

---

## 🤖 Sub-Agents (`/.claude/agents/`)

| Agent | File | Kích hoạt khi |
|-------|------|---------------|
| SQL Data Analyst | `sql-analyst.md` | Cần query AR, FR, CPO, Active Drivers... |
| Report Writer | `report-writer.md` | Có data → viết báo cáo Lark Docs |
| Competitive Intel | `competitive-intel.md` | Phân tích Grab, Be, XanhSM |
| Driver Comms Writer | `driver-comms.md` | Viết thông báo/script cho tài xế |
| Landing Page Builder | `landing-page-builder.md` | Tạo landing page HTML |
| Content Writer | `content-writer.md` | Caption, blog, LinkedIn, script vlog |
| Event Planner | `event-planner.md` | Lên kế hoạch event offline/online |
| Meeting Prep | `meeting-prep.md` | Chuẩn bị trước cuộc họp quan trọng |
| Weekly Review | `weekly-review.md` | Review cuối tuần + plan tuần tới |

---

## ▶️ Chạy Dashboard Local

```bash
streamlit run "output/Ahamove/04. OPS_METRICS/dashboards/incentive_simulation_app.py" --server.port 8501
```

```bash
streamlit run "output/Ahamove/04. OPS_METRICS/dashboards/sgn_overview_dashboard.py" --server.port 8501
```

---

*Last updated: 2026-06-22 | Scanned by Claude Code*
