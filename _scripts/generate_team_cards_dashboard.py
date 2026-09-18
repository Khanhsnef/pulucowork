#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE TEAM CARDS & STRATEGIC GOALS EXECUTIVE DASHBOARD GENERATOR
===============================================================================
Tập trung 100% vào 7 Cards Metabase chính thức do User cung cấp và Bộ Mục Tiêu 
Trọng Tâm của Đội Ngũ Driver Management (14 Thành Viên KPI Weights):
1. Card #75750 (AR-FR KPI 2026)
2. Card #79066 (Supply Hour KPI)
3. Card #62728 (Good Driver Rate - GDR & GR GDR Tân Binh)
4. Card #75304 (Compliance True Rate - CTR)
5. Card #76069 (Bike Driver Cancel Rate Rule 0.5 PoC)
6. Card #79068 (Retention Bike Driver >= 22 Years Old)

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_team_cards_dashboard():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahamove DM NW Executive Control Tower — Cards & Team Goals Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #0B0F19;
            --bg-sidebar: #111827;
            --bg-card: #1F2937;
            --bg-card-hover: #374151;
            --accent-orange: #FF6B00;
            --accent-orange-glow: rgba(255, 107, 0, 0.35);
            --accent-blue: #3B82F6;
            --accent-emerald: #10B981;
            --accent-purple: #8B5CF6;
            --accent-amber: #F59E0B;
            --accent-rose: #EF4444;
            --text-main: #F9FAFB;
            --text-sub: #9CA3AF;
            --border-color: rgba(255, 255, 255, 0.09);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-dark); color: var(--text-main); display: flex; min-height: 100vh; overflow-x: hidden; }

        /* SIDEBAR DOCK NAVIGATION */
        .sidebar {
            width: 310px; background: var(--bg-sidebar); border-right: 1px solid var(--border-color);
            padding: 24px; display: flex; flex-direction: column; gap: 24px; flex-shrink: 0;
            position: sticky; top: 0; height: 100vh; overflow-y: auto;
        }

        .brand-box { display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border-color); padding-bottom: 16px; }
        .brand-icon {
            width: 44px; height: 44px; background: linear-gradient(135deg, #FF6B00, #FF8533);
            border-radius: 12px; display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: 900; color: #fff; box-shadow: 0 4px 20px var(--accent-orange-glow);
        }
        .brand-text h2 { font-size: 16px; font-weight: 800; color: #fff; letter-spacing: -0.3px; }
        .brand-text p { font-size: 11px; color: var(--text-sub); }

        .nav-menu { display: flex; flex-direction: column; gap: 6px; list-style: none; }
        .nav-item {
            padding: 11px 14px; border-radius: 9px; font-size: 13px; font-weight: 600;
            color: var(--text-sub); cursor: pointer; display: flex; align-items: center; gap: 10px;
            transition: all 0.2s ease;
        }
        .nav-item:hover, .nav-item.active {
            background: var(--accent-orange); color: #fff; box-shadow: 0 4px 15px var(--accent-orange-glow);
        }

        /* MAIN STAGE */
        .main-stage { flex: 1; padding: 26px 36px; display: flex; flex-direction: column; gap: 22px; overflow-y: auto; }

        .top-nav {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border-color); padding-bottom: 16px;
        }
        .page-title h1 { font-size: 23px; font-weight: 800; color: #fff; }
        .page-title p { font-size: 12.5px; color: var(--text-sub); }

        .action-controls { display: flex; gap: 10px; }
        .btn-action {
            background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main);
            padding: 8px 15px; border-radius: 9px; font-size: 12px; font-weight: 700; cursor: pointer;
            transition: all 0.2s; display: flex; align-items: center; gap: 6px;
        }
        .btn-action:hover { background: var(--bg-card-hover); border-color: var(--accent-orange); }
        .btn-action.primary { background: var(--accent-orange); border-color: var(--accent-orange); color: #fff; }

        /* BENTO GRID SYSTEM */
        .bento-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 18px; }

        .bento-card {
            background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px;
            padding: 20px; display: flex; flex-direction: column; gap: 14px; position: relative;
            backdrop-filter: blur(12px); transition: transform 0.2s, border-color 0.2s;
        }
        .bento-card:hover { transform: translateY(-2px); border-color: rgba(255, 107, 0, 0.4); }

        .col-12 { grid-column: span 12; }
        .col-8 { grid-column: span 8; }
        .col-6 { grid-column: span 6; }
        .col-4 { grid-column: span 4; }
        .col-3 { grid-column: span 3; }

        .stat-card-bento { display: flex; flex-direction: column; justify-content: space-between; min-height: 120px; }
        .stat-head { display: flex; justify-content: space-between; align-items: center; }
        .stat-label { font-size: 11px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-val { font-size: 34px; font-weight: 900; letter-spacing: -1px; color: #fff; margin: 3px 0; }
        .stat-sub { font-size: 12px; font-weight: 600; color: var(--accent-emerald); display: flex; align-items: center; gap: 4px; }
        .stat-sub.red { color: var(--accent-rose); }

        .bento-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 10px; border-bottom: 1px solid var(--border-color); }
        .bento-title { font-size: 15px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 8px; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
        th { text-align: left; padding: 9px 11px; color: var(--text-sub); font-weight: 700; background: rgba(0,0,0,0.4); border-bottom: 1px solid var(--border-color); text-transform: uppercase; font-size: 10.5px; }
        td { padding: 9px 11px; border-bottom: 1px solid rgba(255,255,255,0.04); color: #E2E8F0; font-weight: 500; }
        tr:hover td { background: var(--bg-card-hover); }

        .pill { padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; display: inline-block; }
        .pill-green { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .pill-red { background: rgba(239, 68, 68, 0.2); color: #F87171; }
        .pill-yellow { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }
        .pill-purple { background: rgba(139, 92, 246, 0.2); color: #A78BFA; }

        .takeaway-banner {
            background: linear-gradient(135deg, rgba(255, 107, 0, 0.18), rgba(31, 41, 55, 0.95));
            border: 1px solid rgba(255, 107, 0, 0.45); border-radius: 16px; padding: 18px 22px;
            display: flex; flex-direction: column; gap: 8px; box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        }
        .takeaway-title { font-size: 15.5px; font-weight: 800; color: var(--accent-orange); display: flex; align-items: center; gap: 8px; }

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
                <p>Official Metabase Cards & Team Goals</p>
            </div>
        </div>

        <ul class="nav-menu">
            <li class="nav-item active" onclick="showModule('tab-cards-hub')">🎯 1. 7 Cards Metabase Control Tower</li>
            <li class="nav-item" onclick="showModule('tab-team-goals')">🏆 2. Team Member Scorecards & Trọng Số</li>
            <li class="nav-item" onclick="showModule('tab-supply-fulfillment')">⏱️ 3. Supply Hours & Fulfillment SLA</li>
            <li class="nav-item" onclick="showModule('tab-quality-retention')">🛡️ 4. Quality (GDR, CTR) & Retention</li>
            <li class="nav-item" onclick="showModule('tab-cancel-gr')">🚫 5. Cancel Rate (PoC 0.5) & Tân Binh</li>
        </ul>
    </div>

    <!-- MAIN STAGE -->
    <div class="main-stage">
        
        <!-- TOP NAV HEADER -->
        <div class="top-nav">
            <div class="page-title">
                <h1>Ahamove DM NW Executive Control Tower</h1>
                <p>Dashboard Chuẩn Hóa Theo 7 Metabase Cards & Mục Tiêu KPI Trọng Tâm Của Đội Ngũ</p>
            </div>
            <div class="action-controls">
                <button class="btn-action" onclick="window.print()">🖨️ In Báo Cáo / PDF</button>
                <button class="btn-action primary" onclick="location.href='ahamove_executive_29slides_dashboard.html'">📺 Xem Slide Deck Mode (29 Slides)</button>
            </div>
        </div>

        <!-- STRATEGIC TAKEAWAY BANNER -->
        <div class="takeaway-banner">
            <div class="takeaway-title">🎯 TỔNG HỢP KẾT QUẢ ĐẠT KPI THEO 7 CARDS METABASE CHÍNH THỨC</div>
            <div style="font-size: 13.5px; line-height: 1.65; color: #E2E8F0;">
                <strong>1. Fulfillment Rate NW (Card #75750):</strong> Đạt <strong>81.38%</strong> (Đạt KPI 81.0%). SGN bứt phá <strong>86.21%</strong> (Vượt xa target 83%).<br>
                <strong>2. Total Supply Hours NW (Card #79066):</strong> Đạt <strong>1,295,836.0 tiếng</strong> online (Vượt 108% target 1.2M tiếng).<br>
                <strong>3. Compliance True Rate NW (Card #75304):</strong> Chạm mốc kỷ lục mới <strong>74.15%</strong> (Vượt xa target 70.0%). SGN CTR đạt 81.20%.<br>
                <strong>4. Good Driver Rate SGN (Card #62728):</strong> Đạt <strong>96.51%</strong> (Hệ số 1.20x max score). GR GDR Tân binh đạt <strong>96.21%</strong>.<br>
                <strong>5. Retention Bike Driver >=22t (Card #79068):</strong> SGN Retention đạt <strong>77.33%</strong> (Vượt target 75%), HAN Retention hồi phục <strong>74.17%</strong> (+0.7% MoM).
            </div>
        </div>

        <!-- TAB 1: 7 CARDS METABASE CONTROL TOWER -->
        <div id="tab-cards-hub">
            <div class="bento-grid">
                
                <!-- Card Stat 1 -->
                <div class="bento-card col-4 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">CARD #75750 — NW FULFILLMENT RATE</span>
                        <span class="pill pill-green">ĐẠT KPI</span>
                    </div>
                    <div class="stat-val" style="color:var(--accent-emerald)">81.38%</div>
                    <div class="stat-sub">▲ Target 81.0% | SGN 86.2% | HAN 76.0%</div>
                </div>

                <!-- Card Stat 2 -->
                <div class="bento-card col-4 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">CARD #79066 — TOTAL SUPPLY HOURS</span>
                        <span class="pill pill-green">108% TARGET</span>
                    </div>
                    <div class="stat-val" style="color:var(--accent-blue)">1.30M h</div>
                    <div class="stat-sub">▲ Actual: 1,295,836 tiếng online</div>
                </div>

                <!-- Card Stat 3 -->
                <div class="bento-card col-4 stat-card-bento">
                    <div class="stat-head">
                        <span class="stat-label">CARD #75304 — COMPLIANCE CTR</span>
                        <span class="pill pill-green">RECORD HIGH</span>
                    </div>
                    <div class="stat-val" style="color:var(--accent-purple)">74.15%</div>
                    <div class="stat-sub">▲ Target 70.0% | SGN 81.2% | HAN 72.7%</div>
                </div>

                <!-- Chart 1: Metabase KPI Achievement Bar -->
                <div class="bento-card col-8">
                    <div class="bento-header">
                        <div class="bento-title">🏆 1. Tỷ Lệ Hoàn Thành Target KPI Theo 7 Cards Metabase Chính Thức</div>
                    </div>
                    <div class="chart-box"><canvas id="c_cards_achievement"></canvas></div>
                </div>

                <!-- Chart 2: Regional SLA Doughnut -->
                <div class="bento-card col-4">
                    <div class="bento-header">
                        <div class="bento-title">🗺️ 2. Phân Bổ Supply Hours 3 Khu Vực</div>
                    </div>
                    <div class="chart-box"><canvas id="c_supply_dist"></canvas></div>
                </div>

                <!-- Detailed Metabase Cards Table -->
                <div class="bento-card col-12">
                    <div class="bento-header">
                        <div class="bento-title">📌 Bảng Chi Tiết 7 Metabase KPI Cards Của Đội Ngũ</div>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Metabase ID</th>
                                <th>Tên Card KPI Chính Thức & URL Metabase</th>
                                <th>Chỉ Số Thực Tế (`Actual`)</th>
                                <th>Chỉ Số Target</th>
                                <th>Hệ Số Score</th>
                                <th>Trạng Thái KPI</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>#75750</strong></td>
                                <td><a href="https://bi.ahamove.com/question/75750-oe-ar-fr-kpi-2026" target="_blank" style="color:#60A5FA; text-decoration:none;">[NW] Fulfillment Rate (AR-FR KPI 2026)</a></td>
                                <td><strong>81.38%</strong></td>
                                <td>81.00%</td>
                                <td>1.00x</td>
                                <td><span class="pill pill-green">🟢 Đạt KPI</span></td>
                            </tr>
                            <tr>
                                <td><strong>#75750</strong></td>
                                <td><a href="https://bi.ahamove.com/question/75750-oe-ar-fr-kpi-2026" target="_blank" style="color:#60A5FA; text-decoration:none;">[SGN] Fulfillment Rate (AR-FR KPI 2026)</a></td>
                                <td><strong>86.21%</strong></td>
                                <td>83.00%</td>
                                <td>1.04x</td>
                                <td><span class="pill pill-green">🟢 Xuất Sắc</span></td>
                            </tr>
                            <tr>
                                <td><strong>#79066</strong></td>
                                <td><a href="https://bi.ahamove.com/question/79066-ops-s-p-kpi-supply-hour" target="_blank" style="color:#60A5FA; text-decoration:none;">[NW] Total Supply Hour (OPS S&P KPI)</a></td>
                                <td><strong>1,295,836 h</strong></td>
                                <td>1,200,000 h</td>
                                <td>1.08x</td>
                                <td><span class="pill pill-green">🟢 Đạt 108%</span></td>
                            </tr>
                            <tr>
                                <td><strong>#62728</strong></td>
                                <td><a href="https://bi.ahamove.com/question/62728-ops-kpi-2025-gdr" target="_blank" style="color:#60A5FA; text-decoration:none;">[SGN] Good Driver Rate (GDR)</a></td>
                                <td><strong>96.51%</strong></td>
                                <td>94.50%</td>
                                <td>1.20x</td>
                                <td><span class="pill pill-green">🟢 Max Score (1.2x)</span></td>
                            </tr>
                            <tr>
                                <td><strong>#75304</strong></td>
                                <td><a href="https://bi.ahamove.com/question/75304-qm-adhoc-raw-data-tinh-kpi-ctr-m-i" target="_blank" style="color:#60A5FA; text-decoration:none;">[NW] Compliance True Rate (CTR)</a></td>
                                <td><strong>74.15%</strong></td>
                                <td>70.00%</td>
                                <td>1.06x</td>
                                <td><span class="pill pill-green">🟢 Kỷ Lục Mới</span></td>
                            </tr>
                            <tr>
                                <td><strong>#76069</strong></td>
                                <td><a href="https://bi.ahamove.com/question/76069-ops-bike-driver-cancel-rate-rule-0-5-poc-ver2-remove-tts" target="_blank" style="color:#60A5FA; text-decoration:none;">[HAN] NEW Bike Driver Cancel Rate (Rule 0.5 PoC)</a></td>
                                <td><strong>12.54%</strong></td>
                                <td>13.50%</td>
                                <td>1.00x</td>
                                <td><span class="pill pill-green">🟢 Giữ Dưới Ngưỡng</span></td>
                            </tr>
                            <tr>
                                <td><strong>#79068</strong></td>
                                <td><a href="https://bi.ahamove.com/question/79068-ops-s-p-kpi-retention-bike-driver-over-22-years-old" target="_blank" style="color:#60A5FA; text-decoration:none;">[SGN] Retention Bike Driver >=22 Years Old</a></td>
                                <td><strong>77.33%</strong></td>
                                <td>75.00%</td>
                                <td>1.03x</td>
                                <td><span class="pill pill-green">🟢 Bền Vững</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>

        <!-- TAB 2: TEAM MEMBER SCORECARDS & TRỌNG SỐ -->
        <div id="tab-team-goals" class="hidden">
            <div class="bento-grid">
                
                <div class="bento-card col-12">
                    <div class="bento-header">
                        <div class="bento-title">🏆 Bảng Điểm Trọng Số KPI 14 Thành Viên Đội Ngũ Driver Management</div>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>STT</th>
                                <th>Họ và Tên</th>
                                <th>Chức Danh</th>
                                <th>Bộ Phận</th>
                                <th>Cơ Cấu Trọng Số KPI Giao Trao</th>
                                <th>Điểm % Hoàn Thành</th>
                                <th>Xếp Loại Khen Thưởng</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="background:rgba(16,185,129,0.1);">
                                <td>1</td><td><strong>Nguyễn Huy Hoàng</strong></td><td>Executive</td><td>HAN-DM</td>
                                <td>Supply Hour (25%) | FR (25%) | CR (20%) | GDR (15%) | Retention (15%)</td>
                                <td><strong style="color:var(--accent-emerald); font-size:14px;">84.71%</strong></td>
                                <td><span class="pill pill-green">🟢 Xuất Sắc (Hạng 1)</span></td>
                            </tr>
                            <tr style="background:rgba(16,185,129,0.1);">
                                <td>2</td><td><strong>Nguyễn Thanh Trúc</strong></td><td>Specialist</td><td>SGN-DM</td>
                                <td>Supply Hour (25%) | FR (25%) | CR (20%) | GDR (15%) | Retention (15%)</td>
                                <td><strong style="color:var(--accent-emerald); font-size:14px;">84.71%</strong></td>
                                <td><span class="pill pill-green">🟢 Xuất Sắc (Hạng 1)</span></td>
                            </tr>
                            <tr>
                                <td>3</td><td><strong>Đào Thị Thu Trang</strong></td><td>Assistant Manager</td><td>Overall</td>
                                <td>Supply Hour (20%) | CR (15%) | GDR (15%) | FR (15%) | Minihub (15%) | Retention (10%)</td>
                                <td><strong style="color:var(--accent-emerald); font-size:14px;">78.17%</strong></td>
                                <td><span class="pill pill-green">🟢 Hoàn Thành Tốt</span></td>
                            </tr>
                            <tr>
                                <td>4</td><td><strong>Nguyễn Phương Thuý</strong></td><td>Executive</td><td>HAN-DS</td>
                                <td>Supply Hour (25%) | FR (25%) | CR (20%) | GDR (15%) | Retention (15%)</td>
                                <td><strong style="color:var(--accent-amber); font-size:14px;">70.54%</strong></td>
                                <td><span class="pill pill-yellow">🟡 Hoàn Thành Khá</span></td>
                            </tr>
                            <tr>
                                <td>5</td><td><strong>Trần Mỹ Vân</strong></td><td>Specialist</td><td>SGN-DS</td>
                                <td>Supply Hour (25%) | FR (25%) | CR (20%) | GDR (15%) | Retention (15%)</td>
                                <td><strong style="color:var(--accent-amber); font-size:14px;">70.54%</strong></td>
                                <td><span class="pill pill-yellow">🟡 Hoàn Thành Khá</span></td>
                            </tr>
                            <tr>
                                <td>6</td><td><strong>Ngô Huỳnh Khoa</strong></td><td>Executive</td><td>SGN-DS</td>
                                <td>Supply Hour (25%) | FR (25%) | CR (20%) | GDR (15%) | Retention (15%)</td>
                                <td><strong style="color:var(--accent-amber); font-size:14px;">70.54%</strong></td>
                                <td><span class="pill pill-yellow">🟡 Hoàn Thành Khá</span></td>
                            </tr>
                            <tr>
                                <td>7</td><td><strong>Lê Phương Khanh</strong></td><td>Leader</td><td>SGN</td>
                                <td>Supply Hour (25%) | FR (25%) | CR (20%) | GDR (15%) | Retention (15%)</td>
                                <td><strong style="color:var(--accent-amber); font-size:14px;">70.28%</strong></td>
                                <td><span class="pill pill-yellow">🟡 Hoàn Thành Khá</span></td>
                            </tr>
                            <tr>
                                <td>8</td><td><strong>Cáp Minh Hạnh</strong></td><td>Specialist</td><td>DM</td>
                                <td><strong>GR GDR (30%) | NEW CR (30%) | Retention (30%) | FR (10%)</strong></td>
                                <td><strong style="color:var(--accent-rose); font-size:14px;">62.66%</strong></td>
                                <td><span class="pill pill-red">🔴 Cần Cải Thiện CR</span></td>
                            </tr>
                            <tr>
                                <td>9</td><td><strong>Huỳnh Huệ Nhi</strong></td><td>Specialist</td><td>DM</td>
                                <td><strong>GR GDR (30%) | NEW CR (30%) | Retention (30%) | FR (10%)</strong></td>
                                <td><strong style="color:var(--accent-rose); font-size:14px;">62.66%</strong></td>
                                <td><span class="pill pill-red">🔴 Cần Cải Thiện CR</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>

        <!-- TAB 3: SUPPLY HOURS & FULFILLMENT SLA -->
        <div id="tab-supply-fulfillment" class="hidden">
            <div class="bento-grid">
                
                <div class="bento-card col-6">
                    <div class="bento-header">
                        <div class="bento-title">⏱️ Supply Hours Distribution (SGN vs HAN)</div>
                    </div>
                    <div class="chart-box"><canvas id="c_supply_bar"></canvas></div>
                </div>

                <div class="bento-card col-6">
                    <div class="bento-header">
                        <div class="bento-title">📊 Fulfillment Rate Comparison Across Regions</div>
                    </div>
                    <div class="chart-box"><canvas id="c_fr_bar"></canvas></div>
                </div>

            </div>
        </div>

        <!-- TAB 4: QUALITY & RETENTION -->
        <div id="tab-quality-retention" class="hidden">
            <div class="bento-grid">
                
                <div class="bento-card col-6">
                    <div class="bento-header">
                        <div class="bento-title">🛡️ Good Driver Rate (GDR) & Compliance CTR Progress</div>
                    </div>
                    <div class="chart-box"><canvas id="c_quality_radar"></canvas></div>
                </div>

                <div class="bento-card col-6">
                    <div class="bento-header">
                        <div class="bento-title">🔄 Retention Rate Bike Driver >= 22 Years Old</div>
                    </div>
                    <div class="chart-box"><canvas id="c_retention_bar"></canvas></div>
                </div>

            </div>
        </div>

        <!-- TAB 5: CANCEL RATE & TÂN BINH -->
        <div id="tab-cancel-gr" class="hidden">
            <div class="bento-grid">
                
                <div class="bento-card col-12">
                    <div class="bento-header">
                        <div class="bento-title">🚫 Cancel Rate PoC Rule 0.5 & GR Good Driver Rate (Tân Binh)</div>
                    </div>
                    <div class="chart-box"><canvas id="c_cr_gr_bar"></canvas></div>
                </div>

            </div>
        </div>

    </div>

    <!-- INITIALIZE ALL CHARTS -->
    <script>
        function showModule(tabId) {
            const tabs = ['tab-cards-hub', 'tab-team-goals', 'tab-supply-fulfillment', 'tab-quality-retention', 'tab-cancel-gr'];
            tabs.forEach(id => document.getElementById(id).classList.add('hidden'));

            document.querySelectorAll('.nav-menu .nav-item').forEach(item => item.classList.remove('active'));

            document.getElementById(tabId).classList.remove('hidden');
            event.target.classList.add('active');
        }

        window.onload = function() {
            // Chart 1: Cards Achievement
            new Chart(document.getElementById('c_cards_achievement').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['FR NW (#75750)', 'FR SGN (#75750)', 'Supply Hours (#79066)', 'GDR SGN (#62728)', 'CTR NW (#75304)', 'CR HAN (#76069)', 'Retention SGN (#79068)'],
                    datasets: [
                        { label: 'Target KPI (%)', data: [81.0, 83.0, 100.0, 94.5, 70.0, 13.5, 75.0], backgroundColor: 'rgba(255, 255, 255, 0.2)' },
                        { label: 'Thực Tế Actual (%)', data: [81.38, 86.21, 108.0, 96.51, 74.15, 12.54, 77.33], backgroundColor: '#FF6B00' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Chart 2: Supply Dist Doughnut
            new Chart(document.getElementById('c_supply_dist').getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['SGN (783.2K h)', 'HAN (512.7K h)'],
                    datasets: [{ data: [783184, 512652], backgroundColor: ['#3B82F6', '#EF4444'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Chart 3: Supply Bar
            new Chart(document.getElementById('c_supply_bar').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN Supply Hours', 'HAN Supply Hours', 'NW Total'],
                    datasets: [{ label: 'Hours', data: [783184, 512652, 1295836], backgroundColor: ['#3B82F6', '#EF4444', '#10B981'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Chart 4: FR Bar
            new Chart(document.getElementById('c_fr_bar').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN FR', 'HAN FR', 'EXP FR', 'NW FR'],
                    datasets: [{ label: 'Fulfillment Rate (%)', data: [86.21, 76.04, 82.43, 81.38], backgroundColor: ['#10B981', '#EF4444', '#3B82F6', '#FF6B00'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Chart 5: Quality Radar
            new Chart(document.getElementById('c_quality_radar').getContext('2d'), {
                type: 'radar',
                data: {
                    labels: ['SGN GDR', 'HAN GDR', 'NW GDR', 'SGN CTR', 'HAN CTR', 'NW CTR'],
                    datasets: [{ label: 'Quality Metrics (%)', data: [96.51, 93.98, 95.52, 81.20, 72.72, 74.15], borderColor: '#10B981', backgroundColor: 'rgba(16,185,129,0.2)' }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Chart 6: Retention Bar
            new Chart(document.getElementById('c_retention_bar').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN Retention', 'HAN Retention', 'NW Retention'],
                    datasets: [{ label: 'Retention Rate (%)', data: [77.33, 74.17, 75.89], backgroundColor: ['#3B82F6', '#EF4444', '#10B981'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3AF' } } } }
            });

            // Chart 7: CR & GR Bar
            new Chart(document.getElementById('c_cr_gr_bar').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['HAN Tân Binh CR', 'SGN CR', 'NW CR', 'GR GDR Tân Binh'],
                    datasets: [{ label: 'Rate (%)', data: [12.54, 8.99, 13.04, 96.21], backgroundColor: ['#10B981', '#3B82F6', '#F59E0B', '#8B5CF6'] }]
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
    print(f"🎉 Đã xuất thành công Official Team Cards & Goals Executive Dashboard tại: {out_path}")

if __name__ == "__main__":
    build_team_cards_dashboard()
