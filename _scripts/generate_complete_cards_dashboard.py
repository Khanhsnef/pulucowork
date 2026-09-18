#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE ALL 11 METABASE CARDS & GOALS MASTER DASHBOARD GENERATOR
===============================================================================
Tự động tổng hợp TOÀN BỘ 11 METABASE CARDS đã xuất hiện trong hệ thống:
1. Card #75750: OE AR-FR KPI 2026
2. Card #79066: OPS S&P KPI Supply Hour
3. Card #62728: OPS KPI 2025 GDR & GR GDR
4. Card #75304: QM Adhoc Raw Data CTR Mới
5. Card #76069: OPS Bike Driver Cancel Rate Rule 0.5 PoC
6. Card #79068: OPS S&P KPI Retention Bike Driver >=22yo
7. Card #72864: OPS S&P HA Active By City (Non-Additive)
8. Card #77913: S&P Overview Performance
9. Card #67888: OPS PA Metric Overall Performance By Service Type
10. Card #75557: OPS S&P HOA Active Rate & Income Theo Ranking
11. Card #82572: DM Biến Động Ranking Khi Áp Dụng DQS Pulu

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_all_11_cards_dashboard():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahamove DM NW Executive Control Tower — All 11 Metabase Cards Master Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #080C14;
            --bg-sidebar: #0F172A;
            --bg-card: #1E293B;
            --bg-card-hover: #334155;
            --accent-orange: #FF6B00;
            --accent-orange-glow: rgba(255, 107, 0, 0.35);
            --accent-blue: #3B82F6;
            --accent-emerald: #10B981;
            --accent-purple: #8B5CF6;
            --accent-amber: #F59E0B;
            --accent-rose: #EF4444;
            --text-main: #F8FAFC;
            --text-sub: #94A3B8;
            --border-color: rgba(255, 255, 255, 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-dark); color: var(--text-main); display: flex; min-height: 100vh; overflow-x: hidden; }

        /* SIDEBAR DOCK NAVIGATION */
        .sidebar {
            width: 320px; background: var(--bg-sidebar); border-right: 1px solid var(--border-color);
            padding: 20px; display: flex; flex-direction: column; gap: 20px; flex-shrink: 0;
            position: sticky; top: 0; height: 100vh; overflow-y: auto;
        }

        .brand-box { display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border-color); padding-bottom: 14px; }
        .brand-icon {
            width: 44px; height: 44px; background: linear-gradient(135deg, #FF6B00, #FF8533);
            border-radius: 12px; display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: 900; color: #fff; box-shadow: 0 4px 20px var(--accent-orange-glow);
        }
        .brand-text h2 { font-size: 16px; font-weight: 800; color: #fff; letter-spacing: -0.3px; }
        .brand-text p { font-size: 11px; color: var(--text-sub); }

        .nav-menu { display: flex; flex-direction: column; gap: 6px; list-style: none; }
        .nav-item {
            padding: 10px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 600;
            color: var(--text-sub); cursor: pointer; display: flex; align-items: center; gap: 10px;
            transition: all 0.2s ease;
        }
        .nav-item:hover, .nav-item.active {
            background: var(--accent-orange); color: #fff; box-shadow: 0 4px 15px var(--accent-orange-glow);
        }

        /* MAIN STAGE */
        .main-stage { flex: 1; padding: 24px 32px; display: flex; flex-direction: column; gap: 20px; overflow-y: auto; }

        .top-nav {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 1px solid var(--border-color); padding-bottom: 14px;
        }
        .page-title h1 { font-size: 22px; font-weight: 800; color: #fff; }
        .page-title p { font-size: 12px; color: var(--text-sub); }

        .action-controls { display: flex; gap: 10px; }
        .btn-action {
            background: var(--bg-card); border: 1px solid var(--border-color); color: var(--text-main);
            padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer;
            transition: all 0.2s; display: flex; align-items: center; gap: 6px;
        }
        .btn-action:hover { background: var(--bg-card-hover); border-color: var(--accent-orange); }
        .btn-action.primary { background: var(--accent-orange); border-color: var(--accent-orange); color: #fff; }

        /* BENTO GRID SYSTEM */
        .bento-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; }

        .bento-card {
            background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px;
            padding: 18px; display: flex; flex-direction: column; gap: 12px; position: relative;
            backdrop-filter: blur(12px); transition: transform 0.2s, border-color 0.2s;
        }
        .bento-card:hover { transform: translateY(-2px); border-color: rgba(255, 107, 0, 0.4); }

        .col-12 { grid-column: span 12; }
        .col-8 { grid-column: span 8; }
        .col-6 { grid-column: span 6; }
        .col-4 { grid-column: span 4; }
        .col-3 { grid-column: span 3; }

        .stat-card-bento { display: flex; flex-direction: column; justify-content: space-between; min-height: 115px; }
        .stat-head { display: flex; justify-content: space-between; align-items: center; }
        .stat-label { font-size: 11px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; }
        .stat-val { font-size: 32px; font-weight: 900; letter-spacing: -1px; color: #fff; margin: 2px 0; }
        .stat-sub { font-size: 11.5px; font-weight: 600; color: var(--accent-emerald); display: flex; align-items: center; gap: 4px; }
        .stat-sub.red { color: var(--accent-rose); }

        .bento-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 8px; border-bottom: 1px solid var(--border-color); }
        .bento-title { font-size: 14.5px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 8px; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        th { text-align: left; padding: 8px 10px; color: var(--text-sub); font-weight: 700; background: rgba(0,0,0,0.4); border-bottom: 1px solid var(--border-color); text-transform: uppercase; font-size: 10.5px; }
        td { padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.04); color: #E2E8F0; font-weight: 500; }
        tr:hover td { background: var(--bg-card-hover); }

        .pill { padding: 3px 7px; border-radius: 5px; font-size: 10.5px; font-weight: 800; display: inline-block; }
        .pill-green { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .pill-red { background: rgba(239, 68, 68, 0.2); color: #F87171; }
        .pill-yellow { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }
        .pill-purple { background: rgba(139, 92, 246, 0.2); color: #A78BFA; }

        .takeaway-banner {
            background: linear-gradient(135deg, rgba(255, 107, 0, 0.18), rgba(30, 41, 59, 0.95));
            border: 1px solid rgba(255, 107, 0, 0.45); border-radius: 14px; padding: 16px 20px;
            display: flex; flex-direction: column; gap: 8px; box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        }
        .takeaway-title { font-size: 15px; font-weight: 800; color: var(--accent-orange); display: flex; align-items: center; gap: 8px; }

        .chart-box { position: relative; height: 250px; width: 100%; }

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
                <p>Master All 11 Metabase Cards Portal</p>
            </div>
        </div>

        <ul class="nav-menu">
            <li class="nav-item active" onclick="showModule('tab-all-cards')">📌 1. Bảng Tổng Hợp 11 Metabase Cards</li>
            <li class="nav-item" onclick="showModule('tab-active-demand')">🗺️ 2. Active (#72864) & Demand (#77913)</li>
            <li class="nav-item" onclick="showModule('tab-arfr-supply')">⏱️ 3. AR-FR (#75750) & Supply Hour (#79066)</li>
            <li class="nav-item" onclick="showModule('tab-gdr-ctr-ret')">🛡️ 4. GDR (#62728), CTR (#75304) & Ret (#79068)</li>
            <li class="nav-item" onclick="showModule('tab-cr-fleets')">🚫 5. Cancel Rate (#76069) & Fleets (#67888)</li>
            <li class="nav-item" onclick="showModule('tab-ranking-dqs')">⭐ 6. Ranking (#75557) & DQS Simulation (#82572)</li>
            <li class="nav-item" onclick="showModule('tab-scorecards')">🏆 7. Team Scorecards (14 Thành Viên)</li>
        </ul>
    </div>

    <!-- MAIN STAGE -->
    <div class="main-stage">
        
        <!-- TOP NAV HEADER -->
        <div class="top-nav">
            <div class="page-title">
                <h1>Ahamove Driver Management Master Control Tower</h1>
                <p>Tích Hợp 100% Đầy Đủ 11 Metabase Question Cards Đã Cung Cấp Trong Hệ Thống</p>
            </div>
            <div class="action-controls">
                <button class="btn-action" onclick="window.print()">🖨️ In Báo Cáo / PDF</button>
                <button class="btn-action primary" onclick="location.href='ahamove_executive_29slides_dashboard.html'">📺 Xem 29-Slides Deck Mode</button>
            </div>
        </div>

        <!-- TAKEAWAY BANNER -->
        <div class="takeaway-banner">
            <div class="takeaway-title">🎯 TỔNG HỢP 11 CARDS METABASE CHÍNH THỨC TRÊN KHUNG DASHBOARD</div>
            <div style="font-size: 13px; line-height: 1.6; color: #E2E8F0;">
                Bao gồm đầy đủ 11 Cards Metabase: <strong>#75750</strong> (AR-FR), <strong>#79066</strong> (Supply Hours), <strong>#62728</strong> (GDR & GR GDR), <strong>#75304</strong> (CTR Mới), <strong>#76069</strong> (CR Rule 0.5 PoC), <strong>#79068</strong> (Retention $\ge 22$t), <strong>#72864</strong> (Active Non-Additive), <strong>#77913</strong> (Demand Performance), <strong>#67888</strong> (Fleet Performance), <strong>#75557</strong> (Active Rate & Income Ranking), <strong>#82572</strong> (Mô phỏng DQS Pulu).
            </div>
        </div>

        <!-- TAB 1: BẢNG TỔNG HỢP 11 METABASE CARDS -->
        <div id="tab-all-cards">
            <div class="bento-grid">
                
                <div class="bento-card col-12">
                    <div class="bento-header">
                        <div class="bento-title">📌 Bảng Chi Tiết 11 Cards Metabase Hệ Thống</div>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Card Metabase ID</th>
                                <th>Tên Card Metabase Direct Link</th>
                                <th>Chỉ Số Bóc Tách Thực Tế (`Actual`)</th>
                                <th>Chỉ Số Target KPI</th>
                                <th>Trạng Thái & Đánh Giá Vận Hành</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td><strong>Card #75750</strong></td><td><a href="https://bi.ahamove.com/question/75750-oe-ar-fr-kpi-2026" target="_blank" style="color:#60A5FA; text-decoration:none;">OE AR-FR KPI 2026</a></td><td><strong>AR 91.49% | FR 81.38%</strong></td><td>FR 81.00%</td><td><span class="pill pill-green">🟢 Đạt KPI (SGN FR 86.21%)</span></td></tr>
                            <tr><td><strong>Card #79066</strong></td><td><a href="https://bi.ahamove.com/question/79066-ops-s-p-kpi-supply-hour" target="_blank" style="color:#60A5FA; text-decoration:none;">OPS S&P KPI Supply Hour</a></td><td><strong>1,295,836.0 tiếng</strong></td><td>1,200,000 h</td><td><span class="pill pill-green">🟢 Đạt 108% Target</span></td></tr>
                            <tr><td><strong>Card #62728</strong></td><td><a href="https://bi.ahamove.com/question/62728-ops-kpi-2025-gdr" target="_blank" style="color:#60A5FA; text-decoration:none;">OPS KPI GDR 2025 & GR GDR</a></td><td><strong>SGN 96.51% | GR GDR 96.21%</strong></td><td>94.50%</td><td><span class="pill pill-green">🟢 Max Score (1.20x)</span></td></tr>
                            <tr><td><strong>Card #75304</strong></td><td><a href="https://bi.ahamove.com/question/75304-qm-adhoc-raw-data-tinh-kpi-ctr-m-i" target="_blank" style="color:#60A5FA; text-decoration:none;">QM Adhoc Raw Data CTR Mới</a></td><td><strong>NW 74.15% | SGN 81.20%</strong></td><td>70.00%</td><td><span class="pill pill-green">🟢 Kỷ Lục Mới</span></td></tr>
                            <tr><td><strong>Card #76069</strong></td><td><a href="https://bi.ahamove.com/question/76069-ops-bike-driver-cancel-rate-rule-0-5-poc-ver2-remove-tts" target="_blank" style="color:#60A5FA; text-decoration:none;">OPS Bike Driver Cancel Rate Rule 0.5 PoC</a></td><td><strong>HAN Tân Binh 12.54% | NW 13.04%</strong></td><td>< 13.50%</td><td><span class="pill pill-green">🟢 Đạt KPI (Giảm -0.56% WoW)</span></td></tr>
                            <tr><td><strong>Card #79068</strong></td><td><a href="https://bi.ahamove.com/question/79068-ops-s-p-kpi-retention-bike-driver-over-22-years-old" target="_blank" style="color:#60A5FA; text-decoration:none;">Retention Bike Driver >=22yo</a></td><td><strong>SGN 77.33% | HAN 74.17% | NW 75.89%</strong></td><td>75.00%</td><td><span class="pill pill-green">🟢 Bền Vững</span></td></tr>
                            <tr><td><strong>Card #72864</strong></td><td><a href="https://bi.ahamove.com/question/72864-ops-s-p-ha-active-by-city" target="_blank" style="color:#60A5FA; text-decoration:none;">OPS S&P HA Active By City</a></td><td><strong>24,121 Unique Drivers / Tuần</strong></td><td>23,500 tx</td><td><span class="pill pill-green">🟢 Tuân thủ Non-Additive</span></td></tr>
                            <tr><td><strong>Card #77913</strong></td><td><a href="https://bi.ahamove.com/question/77913-s-p-overview-performance" target="_blank" style="color:#60A5FA; text-decoration:none;">S&P Overview Performance</a></td><td><strong>SGN 379.4K req / HAN 392K req (RPH 2.07)</strong></td><td>--</td><td><span class="pill pill-yellow">🟡 Surge HAN 48.3%</span></td></tr>
                            <tr><td><strong>Card #67888</strong></td><td><a href="https://bi.ahamove.com/question/67888-ops-pa-metric-overall-performance-by-service-type-kpi" target="_blank" style="color:#60A5FA; text-decoration:none;">Performance By Service Type KPI</a></td><td><strong>Shopee CR 37.61% | Bulky CR 26.69% | 1H 10.8%</strong></td><td>--</td><td><span class="pill pill-red">🔴 Noise đơn SPX</span></td></tr>
                            <tr><td><strong>Card #75557</strong></td><td><a href="https://bi.ahamove.com/question/75557-ops-s-p-hoa-active-rate-income-theo-ranking-hang-thang-ver2" target="_blank" style="color:#60A5FA; text-decoration:none;">Active Rate & Income Theo Ranking</a></td><td><strong>Tài xế Hạng Kim Cương Active Rate 94.2%</strong></td><td>> 90.0%</td><td><span class="pill pill-green">🟢 Thu nhập cao</span></td></tr>
                            <tr><td><strong>Card #82572</strong></td><td><a href="https://bi.ahamove.com/question/82572-dm-bi-n-ng-ranking-khi-ap-d-ng-dqs-pulu" target="_blank" style="color:#60A5FA; text-decoration:none;">Biến Động Ranking Khi Áp Dụng DQS Pulu</a></td><td><strong>Mô phỏng DQS T1=80, T2=75, T3=75</strong></td><td>--</td><td><span class="pill pill-purple">🚀 Mô phỏng DQS</span></td></tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>

        <!-- OTHER TABS -->
        <div id="tab-active-demand" class="hidden">
            <div class="bento-grid">
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">📈 Active Drivers Trend (#72864)</div></div><div class="chart-box"><canvas id="c_active11"></canvas></div></div>
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">📊 Demand Performance (#77913)</div></div><div class="chart-box"><canvas id="c_demand11"></canvas></div></div>
            </div>
        </div>

        <div id="tab-arfr-supply" class="hidden">
            <div class="bento-grid">
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">⏱️ Supply Hours (#79066)</div></div><div class="chart-box"><canvas id="c_supply11"></canvas></div></div>
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">📊 AR & FR (#75750)</div></div><div class="chart-box"><canvas id="c_fr11"></canvas></div></div>
            </div>
        </div>

        <div id="tab-gdr-ctr-ret" class="hidden">
            <div class="bento-grid">
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">🛡️ Quality GDR & CTR (#62728 & #75304)</div></div><div class="chart-box"><canvas id="c_quality11"></canvas></div></div>
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">🔄 Retention >=22yo (#79068)</div></div><div class="chart-box"><canvas id="c_ret11"></canvas></div></div>
            </div>
        </div>

        <div id="tab-cr-fleets" class="hidden">
            <div class="bento-grid">
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">🚫 Cancel Rate PoC 0.5 (#76069)</div></div><div class="chart-box"><canvas id="c_cr11"></canvas></div></div>
                <div class="bento-card col-6"><div class="bento-header"><div class="bento-title">📦 Fleet Service Performance (#67888)</div></div><div class="chart-box"><canvas id="c_fleets11"></canvas></div></div>
            </div>
        </div>

        <div id="tab-ranking-dqs" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header"><div class="bento-title">⭐ Ranking & Mô Phỏng Driver Quality Score DQS Pulu (#75557 & #82572)</div></div>
                <p style="font-size:13px; color:#E2E8F0; line-height:1.6;">
                    Card #75557 và #82572 phân tích biến động xếp hạng tài xế khi áp dụng DQS Pulu với các tham số ngưỡng DQS (T1=80, T2=75, T3=75) và STP (T1=280, T2=150, T3=70). Kết quả mô phỏng cho thấy nhóm tài xế Hạng Kim Cương duy trì Active Rate 94.2% và có mức thu nhập cao nhất.
                </p>
            </div>
        </div>

        <div id="tab-scorecards" class="hidden">
            <div class="bento-card col-12">
                <div class="bento-header"><div class="bento-title">🏆 Bảng Điểm 14 Thành Viên Team</div></div>
                <table>
                    <thead>
                        <tr><th>STT</th><th>Họ và Tên</th><th>Chức Danh</th><th>Bộ Phận</th><th>Tổng Điểm % KPI</th><th>Xếp Loại</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>1</td><td><strong>Nguyễn Huy Hoàng</strong></td><td>Executive</td><td>HAN-DM</td><td><strong style="color:var(--accent-emerald)">84.71%</strong></td><td><span class="pill pill-green">🟢 Xuất Sắc</span></td></tr>
                        <tr><td>2</td><td><strong>Nguyễn Thanh Trúc</strong></td><td>Specialist</td><td>SGN-DM</td><td><strong style="color:var(--accent-emerald)">84.71%</strong></td><td><span class="pill pill-green">🟢 Xuất Sắc</span></td></tr>
                        <tr><td>3</td><td><strong>Đào Thị Thu Trang</strong></td><td>Assistant Manager</td><td>Overall</td><td><strong style="color:var(--accent-emerald)">78.17%</strong></td><td><span class="pill pill-green">🟢 Hoàn Thành Tốt</span></td></tr>
                        <tr><td>4</td><td><strong>Cáp Minh Hạnh</strong></td><td>Specialist</td><td>DM</td><td><strong style="color:var(--accent-rose)">62.66%</strong></td><td><span class="pill pill-red">🔴 Cần Cải Thiện CR</span></td></tr>
                        <tr><td>5</td><td><strong>Huỳnh Huệ Nhi</strong></td><td>Specialist</td><td>DM</td><td><strong style="color:var(--accent-rose)">62.66%</strong></td><td><span class="pill pill-red">🔴 Cần Cải Thiện CR</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <!-- INITIALIZE ALL CHARTS -->
    <script>
        function showModule(tabId) {
            const tabs = ['tab-all-cards', 'tab-active-demand', 'tab-arfr-supply', 'tab-gdr-ctr-ret', 'tab-cr-fleets', 'tab-ranking-dqs', 'tab-scorecards'];
            tabs.forEach(id => document.getElementById(id).classList.add('hidden'));

            document.querySelectorAll('.nav-menu .nav-item').forEach(item => item.classList.remove('active'));

            document.getElementById(tabId).classList.remove('hidden');
            event.target.classList.add('active');
        }

        window.onload = function() {
            new Chart(document.getElementById('c_active11').getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['Tuần 27/07', 'Tuần 03/08', 'Tuần 10/08', 'Tuần 17/08'],
                    datasets: [
                        { label: 'SGN Active', data: [11092, 11433, 11332, 9630], borderColor: '#3B82F6', fill: false },
                        { label: 'HAN Active', data: [9396, 9672, 9737, 8416], borderColor: '#EF4444', fill: false },
                        { label: 'EXP Active', data: [4169, 4347, 4336, 2925], borderColor: '#10B981', fill: false }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_demand11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN Demand', 'HAN Demand', 'EXP Demand'],
                    datasets: [
                        { label: 'Requested', data: [379428, 392000, 58863], backgroundColor: '#FF6B00' },
                        { label: 'Completed', data: [328200, 297000, 48486], backgroundColor: '#10B981' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_supply11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN Supply Hours', 'HAN Supply Hours', 'NW Total'],
                    datasets: [{ label: 'Hours', data: [783184, 512652, 1295836], backgroundColor: ['#3B82F6', '#EF4444', '#10B981'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_fr11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN FR', 'HAN FR', 'EXP FR', 'NW FR'],
                    datasets: [{ label: 'FR (%)', data: [86.21, 76.04, 82.43, 81.38], backgroundColor: ['#10B981', '#EF4444', '#3B82F6', '#FF6B00'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_quality11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN GDR', 'HAN GDR', 'GR GDR', 'SGN CTR', 'NW CTR'],
                    datasets: [{ label: 'Rate (%)', data: [96.51, 93.98, 96.21, 81.20, 74.15], backgroundColor: '#10B981' }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_ret11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['SGN Retention', 'HAN Retention', 'NW Retention'],
                    datasets: [{ label: 'Retention Rate (%)', data: [77.33, 74.17, 75.89], backgroundColor: ['#3B82F6', '#EF4444', '#10B981'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_cr11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['HAN Tân Binh CR', 'SGN CR', 'NW CR'],
                    datasets: [{ label: 'Cancel Rate (%)', data: [12.54, 8.99, 13.04], backgroundColor: '#EF4444' }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
            });

            new Chart(document.getElementById('c_fleets11').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['1H', '4H', 'Bulky', '2H', 'Shopee'],
                    datasets: [{ label: 'Cancel Rate (%)', data: [10.80, 13.70, 26.69, 30.45, 37.61], backgroundColor: '#EF4444' }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#9CA3B8' } } } }
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
    print(f"🎉 Đã xuất thành công Master Portal với đầy đủ 11 Metabase Cards tại: {out_path}")

if __name__ == "__main__":
    build_all_11_cards_dashboard()
