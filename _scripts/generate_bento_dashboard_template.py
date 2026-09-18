#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE BENTO GRID EXECUTIVE COMMAND CENTER — BRAND NEW TEMPLATE REDESIGN
===============================================================================
Bố cục lại toàn bộ Dashboard theo phong cách Bento Grid Command Center hiện đại:
- Sidebar Dock Navigation linh hoạt
- Card Kính Nổi (Glassmorphism Bento Cards)
- Biểu đồ tương tác Chart.js đa chiều
- Chế độ Toggle giữa Dashboard Portal và Presentation Slide Mode

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_bento_dashboard():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahamove DM NW Executive Operations Command Center — Bento Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #090D16;
            --bg-sidebar: #111827;
            --bg-card: #1F2937;
            --bg-card-hover: #374151;
            --accent-orange: #FF6B00;
            --accent-orange-glow: rgba(255, 107, 0, 0.3);
            --accent-blue: #3B82F6;
            --accent-emerald: #10B981;
            --accent-purple: #8B5CF6;
            --accent-amber: #F59E0B;
            --accent-rose: #EF4444;
            --text-main: #F9FAFB;
            --text-sub: #9CA3AF;
            --border-color: rgba(255, 255, 255, 0.08);
            --glass: rgba(31, 41, 55, 0.7);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-dark); color: var(--text-main); display: flex; min-height: 100vh; overflow-x: hidden; }

        /* SIDEBAR DOCK NAVIGATION */
        .sidebar {
            width: 280px; background: var(--bg-sidebar); border-right: 1px solid var(--border-color);
            padding: 24px; display: flex; flex-direction: column; gap: 32px; flex-shrink: 0;
            position: sticky; top: 0; height: 100vh;
        }

        .brand-box {
            display: flex; align-items: center; gap: 14px;
        }

        .brand-icon {
            width: 44px; height: 44px; background: linear-gradient(135deg, #FF6B00, #FF8533);
            border-radius: 12px; display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: 900; color: #fff; box-shadow: 0 4px 20px var(--accent-orange-glow);
        }

        .brand-text h2 { font-size: 18px; font-weight: 800; color: #fff; letter-spacing: -0.5px; }
        .brand-text p { font-size: 11px; color: var(--text-sub); }

        .nav-menu { display: flex; flex-direction: column; gap: 8px; list-style: none; }
        .nav-item {
            padding: 12px 16px; border-radius: 10px; font-size: 13px; font-weight: 600;
            color: var(--text-sub); cursor: pointer; display: flex; align-items: center; gap: 12px;
            transition: all 0.2s ease;
        }
        .nav-item:hover, .nav-item.active {
            background: var(--accent-orange); color: #fff; box-shadow: 0 4px 15px var(--accent-orange-glow);
        }

        /* MAIN CONTENT AREA */
        .main-stage { flex: 1; padding: 28px 36px; display: flex; flex-direction: column; gap: 24px; overflow-y: auto; }

        .top-nav {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border-color); padding-bottom: 16px;
        }

        .page-title h1 { font-size: 24px; font-weight: 800; color: #fff; }
        .page-title p { font-size: 13px; color: var(--text-sub); }

        .action-controls { display: flex; gap: 12px; }
        .btn-action {
            background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main);
            padding: 9px 16px; border-radius: 10px; font-size: 12px; font-weight: 700; cursor: pointer;
            transition: all 0.2s; display: flex; align-items: center; gap: 6px;
        }
        .btn-action:hover { background: var(--bg-card-hover); border-color: var(--accent-orange); }
        .btn-action.primary { background: var(--accent-orange); border-color: var(--accent-orange); color: #fff; }

        /* BENTO GRID SYSTEM */
        .bento-grid {
            display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px;
        }

        .bento-card {
            background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 18px;
            padding: 22px; display: flex; flex-direction: column; gap: 14px; position: relative;
            backdrop-filter: blur(12px); transition: transform 0.2s, border-color 0.2s;
        }
        .bento-card:hover { transform: translateY(-2px); border-color: rgba(255, 107, 0, 0.4); }

        /* Span Sizes */
        .col-12 { grid-column: span 12; }
        .col-8 { grid-column: span 8; }
        .col-6 { grid-column: span 6; }
        .col-4 { grid-column: span 4; }
        .col-3 { grid-column: span 3; }

        /* Stat Card Bento Special */
        .stat-card-bento {
            display: flex; flex-direction: column; justify-content: space-between; min-height: 120px;
        }
        .stat-head { display: flex; justify-content: space-between; align-items: center; }
        .stat-label { font-size: 12px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-val { font-size: 36px; font-weight: 900; letter-spacing: -1px; color: #fff; margin: 4px 0; }
        .stat-sub { font-size: 12px; font-weight: 600; color: var(--accent-emerald); display: flex; align-items: center; gap: 4px; }
        .stat-sub.red { color: var(--accent-rose); }

        /* Card Headers */
        .bento-header {
            display: flex; justify-content: space-between; align-items: center;
            padding-bottom: 10px; border-bottom: 1px solid var(--border-color);
        }
        .bento-title { font-size: 15px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 8px; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { text-align: left; padding: 10px 12px; color: var(--text-sub); font-weight: 600; background: rgba(0,0,0,0.3); border-bottom: 1px solid var(--border-color); }
        td { padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.04); color: #E5E7EB; }
        tr:hover td { background: var(--bg-card-hover); }

        .pill { padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; display: inline-block; }
        .pill-green { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .pill-red { background: rgba(239, 68, 68, 0.2); color: #F87171; }
        .pill-yellow { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }

        /* Takeaway Banner */
        .takeaway-banner {
            background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(31, 41, 55, 0.9));
            border: 1px solid rgba(255, 107, 0, 0.4); border-radius: 16px; padding: 20px 24px;
            display: flex; flex-direction: column; gap: 10px;
        }
        .takeaway-title { font-size: 16px; font-weight: 800; color: var(--accent-orange); display: flex; align-items: center; gap: 8px; }

        .chart-box { position: relative; height: 260px; width: 100%; }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- SIDEBAR DOCK NAVIGATION -->
    <div class="sidebar">
        <div class="brand-box">
            <div class="brand-icon">A</div>
            <div class="brand-text">
                <h2>Ahamove Control</h2>
                <p>DM NW Strategy Portal 2026</p>
            </div>
        </div>

        <ul class="nav-menu">
            <li class="nav-item active" onclick="showModule('mod-overview')">📌 1. Overview & Command</li>
            <li class="nav-item" onclick="showModule('mod-regional')">🗺️ 2. Regional & Demand</li>
            <li class="nav-item" onclick="showModule('mod-retention')">🔄 3. Retention & Cohorts</li>
            <li class="nav-item" onclick="showModule('mod-projects')">🚀 4. Projects & Fleets</li>
            <li class="nav-item" onclick="showModule('mod-quality')">🛡️ 5. Quality & Voices</li>
            <li class="nav-item" onclick="showModule('mod-scorecards')">🏆 6. Team Scorecards</li>
        </ul>
    </div>

    <!-- MAIN STAGE -->
    <div class="main-stage">
        
        <!-- TOP NAV HEADER -->
        <div class="top-nav">
            <div class="page-title">
                <h1>Ahamove Driver Management Executive Dashboard</h1>
                <p>Báo Cáo Tổng Hợp Vận Hành Mới Nhất (Meeting 3 & 7 Cards Metabase)</p>
            </div>
            <div class="action-controls">
                <button class="btn-action" onclick="window.print()">🖨️ In Báo Cáo / PDF</button>
                <button class="btn-action primary" onclick="location.href='ahamove_executive_29slides_dashboard.html'">📺 Xem Slide Deck Mode (29 Slides)</button>
            </div>
        </div>

        <!-- TAKEAWAY BANNER -->
        <div class="takeaway-banner">
            <div class="takeaway-title">💡 STRATEGIC EXECUTIVE TAKEAWAYS (MEETING 3 UPDATED)</div>
            <div style="font-size: 13.5px; line-height: 1.6; color: #E5E7EB;">
                <strong>1. Hà Nội Retention Hồi Phục Ấn Tượng (74.17%):</strong> Tỷ lệ giữ chân tài xế $\ge 22$t tại HAN tăng +0.7% MoM, nhóm NLM phục hồi mạnh +3.68% MoM.<br>
                <strong>2. Tỷ Lệ Hủy HAN Hạ Nhiệt (13.04%):</strong> Cancel Rate giảm 0.56% WoW; FT CR giữ ở mốc 9.60%.<br>
                <strong>3. Đội Baga Bulky Đạt 514 Đăng Ký:</strong> Thu hút 336 tx SGN & 178 tx HAN tham gia chuỗi thưởng 3 giai đoạn (15/8 - 30/9).<br>
                <strong>4. Phát Hiện UX CityZone:</strong> 25.6% đơn ngoài ca (401 đơn) vẫn được tài xế giao tốt ➔ Cần Auto-Checkin & push Noti trước 15p.
            </div>
        </div>

        <!-- MODULE 1: OVERVIEW & HERO STATS (DEFAULT ACTIVE) -->
        <div id="mod-overview">
            <div class="bento-grid">
                
                <!-- Hero Stat 1 -->
                <div class="bento-card col-3 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">ACTIVE DRIVERS (WEEKLY)</span>
                        <span class="pill pill-green">NON-ADDITIVE</span>
                    </div>
                    <div class="stat-val">24,121</div>
                    <div class="stat-sub">▲ +3.2% WoW Peak (SGN: 10.8K | HAN: 9.3K)</div>
                </div>

                <!-- Hero Stat 2 -->
                <div class="bento-card col-3 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">HAN RETENTION (>=22t)</span>
                        <span class="pill pill-green">+0.7% MoM</span>
                    </div>
                    <div class="stat-val" style="color:var(--accent-emerald)">74.17%</div>
                    <div class="stat-sub">▲ FT Retention đạt 95.32%</div>
                </div>

                <!-- Hero Stat 3 -->
                <div class="bento-card col-3 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">SGN RETENTION (>=22t)</span>
                        <span class="pill pill-yellow">>75% TARGET</span>
                    </div>
                    <div class="stat-val" style="color:var(--accent-blue)">76.13%</div>
                    <div class="stat-sub">▲ FT Retention đạt 96.46%</div>
                </div>

                <!-- Hero Stat 4 -->
                <div class="bento-card col-3 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">COMPLIANCE CTR</span>
                        <span class="pill pill-green">RECORD HIGH</span>
                    </div>
                    <div class="stat-val" style="color:var(--accent-purple)">77.38%</div>
                    <div class="stat-sub">▲ SGN: 79.91% | HAN: 72.72%</div>
                </div>

                <!-- Bento Chart Row -->
                <div class="bento-card col-8">
                    <div class="bento-header">
                        <div class="bento-title">📈 4-Week Active Driver WoW Trend (Unique Per-Period)</div>
                    </div>
                    <div class="chart-box">
                        <canvas id="bentoActiveChart"></canvas>
                    </div>
                </div>

                <div class="bento-card col-4">
                    <div class="bento-header">
                        <div class="bento-title">📊 Demand & Completed Breakdown</div>
                    </div>
                    <div class="chart-box">
                        <canvas id="bentoDemandChart"></canvas>
                    </div>
                </div>

            </div>
        </div>

        <!-- MODULE 2: REGIONAL PERFORMANCE -->
        <div id="mod-regional" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header">
                    <div class="bento-title">🗺️ Chi Tiết Vận Hành 3 Khu Vực (SGN - HAN - EXP)</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Khu Vực (Region)</th>
                            <th>Nhu Cầu Đơn (Requested)</th>
                            <th>Hoàn Thành (Completed)</th>
                            <th>AR %</th>
                            <th>FR %</th>
                            <th>Surge Rate %</th>
                            <th>RPH</th>
                            <th>Trạng Thái Vận Hành</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>TP.HCM (SGN)</strong></td>
                            <td>379,428</td>
                            <td>328,200</td>
                            <td>95.0%</td>
                            <td><strong style="color:var(--accent-emerald)">86.5%</strong></td>
                            <td>16.8%</td>
                            <td>1.47</td>
                            <td><span class="pill pill-green">🟢 Vận Hành Rất Tốt</span></td>
                        </tr>
                        <tr>
                            <td><strong>Hà Nội (HAN)</strong></td>
                            <td>392,000</td>
                            <td>297,000</td>
                            <td>85.5%</td>
                            <td><strong style="color:var(--accent-rose)">75.8%</strong></td>
                            <td><strong style="color:var(--accent-rose)">48.3%</strong></td>
                            <td>2.07</td>
                            <td><span class="pill pill-red">🔴 Thiếu Cung Ca Cao Điểm</span></td>
                        </tr>
                        <tr>
                            <td><strong>Tỉnh Mở Rộng (EXP)</strong></td>
                            <td>58,863</td>
                            <td>48,486</td>
                            <td>90.5%</td>
                            <td><strong style="color:var(--accent-emerald)">82.4%</strong></td>
                            <td>16.0%</td>
                            <td>1.12</td>
                            <td><span class="pill pill-green">🟢 Đạt SLA</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- MODULE 3: RETENTION & COHORTS -->
        <div id="mod-retention" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header">
                    <div class="bento-title">🔄 Retention Rate Bóc Tách Theo Segment ($\ge 22$ Tuổi)</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Khu Vực & Segment</th>
                            <th>Segment Drivers</th>
                            <th>Active Drivers Realized</th>
                            <th>Retention Rate MTD %</th>
                            <th>Biến Động MoM</th>
                            <th>Biến Động YoY</th>
                            <th>Đánh Giá & Đề Xuất</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>HAN — Full-Time (FT)</strong></td><td>1,260</td><td>1,201</td><td><strong>95.32%</strong></td><td>-0.05%</td><td>-1.95%</td><td><span class="pill pill-green">🟢 Rất bền vững</span></td></tr>
                        <tr><td><strong>HAN — Part-Time (PT)</strong></td><td>7,041</td><td>4,956</td><td><strong>70.39%</strong></td><td>-0.35%</td><td>+0.82%</td><td><span class="pill pill-green">🟢 Ổn định</span></td></tr>
                        <tr><td><strong>HAN — New Last Month (NLM)</strong></td><td>854</td><td>587</td><td><strong>68.74%</strong></td><td><strong>+3.68%</strong></td><td>-6.08%</td><td><span class="pill pill-green">🟢 Hồi phục mạnh</span></td></tr>
                        <tr><td><strong>SGN — Full-Time (FT)</strong></td><td>3,273</td><td>3,157</td><td><strong>96.46%</strong></td><td>-0.52%</td><td>+0.04%</td><td><span class="pill pill-green">🟢 Rất bền vững</span></td></tr>
                        <tr><td><strong>SGN — Part-Time (PT)</strong></td><td>9,937</td><td>6,870</td><td><strong>69.14%</strong></td><td>-2.78%</td><td>-1.64%</td><td><span class="pill pill-yellow">🟡 Cần theo dõi</span></td></tr>
                        <tr><td><strong>SGN — New Last Month (NLM)</strong></td><td>2,060</td><td>1,342</td><td><strong>65.15%</strong></td><td>-5.45%</td><td>-8.41%</td><td><span class="pill pill-red">🔴 Khảo sát churn với GR</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- MODULE 4: PROJECTS & FLEETS -->
        <div id="mod-projects" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header">
                    <div class="bento-title">🚀 Tiến Độ Các Dự Án Vận Hành Trọng Điểm</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Dự Án / Fleet</th>
                            <th>KPI Trọng Tâm Track</th>
                            <th>Kết Quả Thực Tế MTD</th>
                            <th>Kế Hoạch Tiếp Theo</th>
                            <th>Trạng Thái Tiến Độ</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>Trang Bị Baga Bulky</strong></td><td>Số tài xế đăng ký Baga</td><td>514 tài xế (336 SGN, 178 HAN)</td><td>Chạy chuỗi thưởng 3 giai đoạn (15/8 - 30/9)</td><td><span class="pill pill-green">🟢 Bùng nổ vượt target</span></td></tr>
                        <tr><td><strong>Đội Core 2H / Bulky</strong></td><td>Thanh lọc & tuyển mới core</td><td>Thanh lọc 9 tx kém, tuyển thêm 5 tx chính thức</td><td>Tuyển thêm 40 tx/tuần, duy trì 50-70 active/ngày</td><td><span class="pill pill-green">🟢 Đúng tiến độ</span></td></tr>
                        <tr><td><strong>Ân Xá Tài Xế (13/8-14/8)</strong></td><td>Kích hoạt tài xế bị khóa</td><td>220 / 200 tài xế active trở lại</td><td>Loại trừ tx đã active để tránh spam noti</td><td><span class="pill pill-green">🟢 Vượt 110% target</span></td></tr>
                        <tr><td><strong>Xe Điện EV (Datbike/Aizen)</strong></td><td>Lead convert xe điện EV</td><td>Tỷ lệ convert ~25% (964 liên hệ ➔ 165 EV)</td><td>Tách blog riêng truyền thông & quy hoạch luồng lead</td><td><span class="pill pill-yellow">🟡 Cần tăng convert</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- MODULE 5: QUALITY & VOICES -->
        <div id="mod-quality" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header">
                    <div class="bento-title">🛡️ Chất Lượng Tuân Thủ (CTR, GDR) & Phản Hồi Tài Xế</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Hạng Mục</th>
                            <th>TP.HCM (SGN)</th>
                            <th>Hà Nội (HAN)</th>
                            <th>Toàn Quốc (NW)</th>
                            <th>Ghi Chú Vận Hành</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Compliance True Rate (CTR)</td><td>79.91%</td><td>72.72%</td><td><strong>77.38%</strong></td><td><span class="pill pill-green">🟢 Đạt 130% Target KPI</span></td></tr>
                        <tr><td>Good Driver Rate (GDR)</td><td>96.61%</td><td>94.21%</td><td><strong>95.52%</strong></td><td><span class="pill pill-green">🟢 Đạt 120% Target KPI</span></td></tr>
                        <tr><td>Driver Voices (Truy Thu)</td><td colspan="3">20 ca tài xế bị truy thu sai đồng phục ngày 06/08 đã được QM hoàn tiền dứt điểm.</td><td><span class="pill pill-green">✅ Đã xử lý xong</span></td></tr>
                        <tr><td>Sinh Nhật Ahamove 11T</td><td colspan="3">Livestream Sinh nhật ngày 21/08/2026; Minigame online "Chuyển ý tưởng - Ghép tương lai".</td><td><span class="pill pill-purple">🚀 Sự kiện lớn</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- MODULE 6: TEAM SCORECARDS -->
        <div id="mod-scorecards" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header">
                    <div class="bento-title">🏆 Bảng Điểm KPI Trọng Số % Chi Tiết Cho 14 Thành Viên Đội Ngũ</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>STT</th>
                            <th>Họ và Tên</th>
                            <th>Chức Danh</th>
                            <th>Bộ Phận</th>
                            <th>Tổng Điểm Trọng Số KPI</th>
                            <th>Xếp Loại Hoàn Thành</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td><strong>Nguyễn Huy Hoàng</strong></td><td>Executive</td><td>HAN-DM</td><td><strong style="color:var(--accent-emerald)">84.71%</strong></td><td><span class="pill pill-green">🟢 Hoàn thành Xuất sắc</span></td></tr>
                        <tr><td>2</td><td><strong>Nguyễn Thanh Trúc</strong></td><td>Specialist</td><td>SGN-DM</td><td><strong style="color:var(--accent-emerald)">84.71%</strong></td><td><span class="pill pill-green">🟢 Hoàn thành Xuất sắc</span></td></tr>
                        <tr><td>3</td><td><strong>Đào Thị Thu Trang</strong></td><td>Assistant Manager</td><td>Overall</td><td><strong style="color:var(--accent-emerald)">78.17%</strong></td><td><span class="pill pill-green">🟢 Hoàn thành Tốt</span></td></tr>
                        <tr><td>4</td><td><strong>Nguyễn Phương Thuý</strong></td><td>Executive</td><td>HAN-DS</td><td><strong style="color:var(--accent-amber)">70.54%</strong></td><td><span class="pill pill-yellow">🟡 Hoàn thành Khá</span></td></tr>
                        <tr><td>5</td><td><strong>Trần Mỹ Vân</strong></td><td>Specialist</td><td>SGN-DS</td><td><strong style="color:var(--accent-amber)">70.54%</strong></td><td><span class="pill pill-yellow">🟡 Hoàn thành Khá</span></td></tr>
                        <tr><td>6</td><td><strong>Ngô Huỳnh Khoa</strong></td><td>Executive</td><td>SGN-DS</td><td><strong style="color:var(--accent-amber)">70.54%</strong></td><td><span class="pill pill-yellow">🟡 Hoàn thành Khá</span></td></tr>
                        <tr><td>7</td><td><strong>Lê Phương Khanh</strong></td><td>Leader</td><td>SGN</td><td><strong style="color:var(--accent-amber)">70.28%</strong></td><td><span class="pill pill-yellow">🟡 Hoàn thành Khá</span></td></tr>
                        <tr><td>8</td><td><strong>Cáp Minh Hạnh</strong></td><td>Specialist</td><td>DM</td><td><strong style="color:var(--accent-rose)">62.66%</strong></td><td><span class="pill pill-red">🔴 Cần Cải Thiện CR</span></td></tr>
                        <tr><td>9</td><td><strong>Huỳnh Huệ Nhi</strong></td><td>Specialist</td><td>DM</td><td><strong style="color:var(--accent-rose)">62.66%</strong></td><td><span class="pill pill-red">🔴 Cần Cải Thiện CR</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <script>
        function showModule(modId) {
            document.getElementById('mod-overview').classList.add('hidden');
            document.getElementById('mod-regional').classList.add('hidden');
            document.getElementById('mod-retention').classList.add('hidden');
            document.getElementById('mod-projects').classList.add('hidden');
            document.getElementById('mod-quality').classList.add('hidden');
            document.getElementById('mod-scorecards').classList.add('hidden');

            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));

            document.getElementById(modId).classList.remove('hidden');
            event.target.classList.add('active');
        }

        window.onload = function() {
            // Bento Active Line Chart
            const ctx1 = document.getElementById('bentoActiveChart').getContext('2d');
            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: ['Tuần 27/07', 'Tuần 03/08', 'Tuần 10/08', 'Tuần 17/08'],
                    datasets: [
                        { label: 'SGN Active', data: [11092, 11433, 11332, 9630], borderColor: '#3B82F6', fill: false, tension: 0.3 },
                        { label: 'HAN Active', data: [9396, 9672, 9737, 8416], borderColor: '#EF4444', fill: false, tension: 0.3 },
                        { label: 'EXP Active', data: [4169, 4347, 4336, 2925], borderColor: '#10B981', fill: false, tension: 0.3 }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Bento Demand Bar Chart
            const ctx2 = document.getElementById('bentoDemandChart').getContext('2d');
            new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['SGN Demand', 'HAN Demand'],
                    datasets: [
                        { label: 'Requested', data: [379428, 392000], backgroundColor: '#FF6B00' },
                        { label: 'Completed', data: [328200, 297000], backgroundColor: '#10B981' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });
        };
    </script>
</body>
</html>
"""

    out_dir = "Output/Ahamove/04. OPS_METRICS"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ahamove_bento_executive_dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"🎉 Đã xuất thành công Brand New Bento Executive Dashboard tại: {out_path}")

if __name__ == "__main__":
    build_bento_dashboard()
