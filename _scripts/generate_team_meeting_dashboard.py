#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE TEAM MEETING CUSTOM EXECUTIVE DASHBOARD GENERATOR
===============================================================================
Tự động xuất HTML Dashboard Tương Tác Chuẩn Thương Hiệu Ahamove (Canvas Style)
dựa trên 100% dữ liệu bóc tách từ Slide Báo Cáo Meeting Team:
"[2026] DM NW _ Meeting (2).pptx"

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_team_meeting_html_dashboard():
    html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahamove DM NW Team Meeting — Weekly Review & Strategic Focus Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-primary: #0F172A;
            --bg-card: #1E293B;
            --bg-card-hover: #334155;
            --accent-orange: #FF6B00;
            --accent-orange-light: #FF8533;
            --accent-blue: #3B82F6;
            --accent-emerald: #10B981;
            --accent-amber: #F59E0B;
            --accent-rose: #F43F5E;
            --accent-purple: #8B5CF6;
            --text-main: #F8FAFC;
            --text-sub: #94A3B8;
            --border-color: rgba(255, 255, 255, 0.1);
            --glass-bg: rgba(30, 41, 59, 0.8);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }

        /* HEADER & BRANDING */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .brand-logo {
            background: linear-gradient(135deg, #FF6B00, #FF8533);
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 24px;
            color: white;
            box-shadow: 0 4px 20px rgba(255, 107, 0, 0.4);
        }

        .brand-title h1 {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #FFFFFF, #94A3B8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-title p {
            font-size: 13px;
            color: var(--text-sub);
        }

        .view-switcher {
            display: flex;
            background: var(--bg-card);
            padding: 4px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            gap: 4px;
        }

        .tab-btn {
            padding: 10px 18px;
            border: none;
            background: transparent;
            color: var(--text-sub);
            font-weight: 600;
            font-size: 13px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .tab-btn.active {
            background: var(--accent-orange);
            color: white;
            box-shadow: 0 2px 10px rgba(255, 107, 0, 0.3);
        }

        /* HERO STATS GRID */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        .stat-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 107, 0, 0.4);
        }

        .stat-card.focal {
            grid-column: span 2;
            background: linear-gradient(135deg, rgba(255, 107, 0, 0.18), rgba(30, 41, 59, 0.9));
            border: 1px solid rgba(255, 107, 0, 0.5);
        }

        .stat-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            margin-bottom: 12px;
            text-transform: uppercase;
        }

        .badge-orange { background: rgba(255, 107, 0, 0.2); color: #FF944D; }
        .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .badge-blue { background: rgba(59, 130, 246, 0.2); color: #60A5FA; }
        .badge-rose { background: rgba(244, 63, 94, 0.2); color: #FB7185; }
        .badge-purple { background: rgba(139, 92, 246, 0.2); color: #A78BFA; }

        .stat-value {
            font-size: 32px;
            font-weight: 900;
            letter-spacing: -1px;
            margin-bottom: 4px;
        }

        .stat-label {
            font-size: 12px;
            color: var(--text-sub);
        }

        /* GRID LAYOUT & CHARTS */
        .grid-container {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }

        .chart-container {
            position: relative;
            height: 270px;
            width: 100%;
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }

        .card-title {
            font-size: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* TABLES */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th {
            text-align: left;
            padding: 12px;
            color: var(--text-sub);
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            background: rgba(15, 23, 42, 0.6);
        }

        td {
            padding: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        tr:hover td {
            background: var(--bg-card-hover);
        }

        .pill {
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 11px;
            display: inline-block;
        }

        .pill-green { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .pill-red { background: rgba(244, 63, 94, 0.2); color: #FB7185; }
        .pill-yellow { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }

        /* EXECUTIVE TAKEAWAYS BOX */
        .takeaway-box {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98));
            border: 1px solid rgba(255, 107, 0, 0.35);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
        }

        .takeaway-title {
            font-size: 18px;
            font-weight: 800;
            color: var(--accent-orange);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .takeaway-item {
            margin-bottom: 12px;
            padding-left: 20px;
            position: relative;
            font-size: 14px;
            color: #E2E8F0;
        }

        .takeaway-item::before {
            content: "➔";
            position: absolute;
            left: 0;
            color: var(--accent-orange);
            font-weight: 900;
        }

        .hidden { display: none !important; }
    </style>
</head>
<body>

    <!-- HEADER & BRANDING -->
    <div class="header">
        <div class="brand">
            <div class="brand-logo">A</div>
            <div class="brand-title">
                <h1>Ahamove Driver Management (DM NW) Team Meeting Control Center</h1>
                <p>Báo Cáo Đánh Giá Vận Hành Tuần 33 & Định Hướng Trọng Tâm Chiến Lược (Tháng 8/2026)</p>
            </div>
        </div>
        <div class="view-switcher">
            <button class="tab-btn active" onclick="switchView('campaign')">🔥 Campaign 8.8 Review</button>
            <button class="tab-btn" onclick="switchView('retention')">🔄 Retention & Supply Hours</button>
            <button class="tab-btn" onclick="switchView('projects')">🚀 Projects & Fleets (Bulky/MiniHub/EV)</button>
            <button class="tab-btn" onclick="switchView('quality')">🛡️ Quality, Comms & Voices</button>
        </div>
    </div>

    <!-- HERO STATS BAR -->
    <div class="stats-grid">
        <div class="stat-card focal">
            <div class="stat-badge badge-orange">🔥 CAMPAIGN 8.8 ACTIVE DRIVERS</div>
            <div class="stat-value">12,043 <span style="font-size:15px; font-weight:600; color:var(--accent-emerald);">SGN: 6,917 | HAN: 5,126</span></div>
            <div class="stat-label">Năng suất trung bình: SGN 10.16 stp (+0.5) | HAN 8.95 stp (+0.22)</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-emerald">🔄 RETENTION RATE (>=22t)</div>
            <div class="stat-value" style="color:var(--accent-emerald)">72.19% <span style="font-size:13px; color:var(--text-sub)">SGN</span></div>
            <div class="stat-label">HAN: 69.76% (FT Retention đạt 96.18%)</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-blue">📦 CORE 2H & BULKY FLEET</div>
            <div class="stat-value">57 <span style="font-size:14px; font-weight:500;">Tài xế gia nhập</span></div>
            <div class="stat-label">Thanh lọc 28-29 tx kém; Tuyển thêm 40 tx/tuần</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-purple">⚡ EV BIKE TRANSITION</div>
            <div class="stat-value" style="color:var(--accent-purple)">135% <span style="font-size:13px;">SGN Active MTD</span></div>
            <div class="stat-label">HAN Active MTD: 94% (504/535 tài xế)</div>
        </div>
    </div>

    <!-- EXECUTIVE TAKEAWAYS BOX -->
    <div class="takeaway-box">
        <div class="takeaway-title">💡 TEAM MEETING STRATEGIC INSIGHTS & FOCUS ROADMAP</div>
        <div class="takeaway-item">
            <strong>Tối Ưu Năng Suất Campaign Mega Sales 8.8:</strong> SGN hoàn thành <strong>98.66% Capacity Target</strong> (66,334 đơn hoàn thành), năng suất tăng lên <strong>10.16 đơn/tx</strong> và thu nhập đạt <strong>52.7k/h (+6.1k/h)</strong>. HAN hoàn thành <strong>98.13% Capacity Target</strong> với 45,636 đơn.
        </div>
        <div class="takeaway-item">
            <strong>Bóc Tách Retention & Giải Pháp CHL:</strong> Retention tài xế $\ge 22$t tại HAN sụt hụt MoM 0.33% về <strong>69.76%</strong> (Nhóm NLM hụt 2.85%). Chiến dịch CHL đợt 2 đã kích hoạt thành công 71 tài xế HAN và 98 tài xế SGN quay lại hoạt động.
        </div>
        <div class="takeaway-item">
            <strong>Thanh Lọc & Mở Rộng Đội Core 2H/Bulky:</strong> Tiến hành lọc 28 tài xế hiệu suất thấp, phỏng vấn 82 tài xế mới và bổ sung chính thức <strong>57 tài xế chất lượng cao</strong>. Đặt mục tiêu nạp thêm 40 tài xế/tuần.
        </div>
        <div class="takeaway-item">
            <strong>Xử Lý Phản Hồi Driver Voices & Truy Thu Đồng Phục:</strong> Giải quyết dứt điểm 20 ca tài xế bị truy thu sai đồng phục do luồng xác thực ngày 06/08 (đã hoàn tiền và bổ sung thông báo Noti hướng dẫn).
        </div>
    </div>

    <!-- VIEW 1: CAMPAIGN 8.8 REVIEW (ACTIVE DEFAULT) -->
    <div id="view-campaign">
        <div class="grid-container">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🔥 Campaign 8.8 Supply Capacity & Fulfillment (SGN vs HAN)</div>
                    <span class="pill pill-green">CAMPAIGN 8.8 REVIEW</span>
                </div>
                <div class="chart-container">
                    <canvas id="campaignChart"></canvas>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <div class="card-title">💰 Driver Income & Productivity</div>
                </div>
                <div class="chart-container">
                    <canvas id="incomeChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">📋 Chi Tiết Phân Khúc Tài Xế Tham Gia Campaign 8.8</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Khu Vực & Phân Khúc</th>
                        <th>Active Actual</th>
                        <th>Active Target %</th>
                        <th>Năng Suất (Prod)</th>
                        <th>Prod Target %</th>
                        <th>Capacity (Sản lượng)</th>
                        <th>Capacity Target %</th>
                        <th>Đánh Giá Mức Độ Đạt Target</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>SGN — Full Time (FT)</strong></td>
                        <td>2,559</td>
                        <td>96.72%</td>
                        <td>13.43 đơn/tx</td>
                        <td>99.48%</td>
                        <td>34,367 đơn</td>
                        <td>96.22%</td>
                        <td><span class="pill pill-green">🟢 Đạt Target xuất sắc</span></td>
                    </tr>
                    <tr>
                        <td><strong>SGN — Part Time (PT)</strong></td>
                        <td>3,265</td>
                        <td>90.88%</td>
                        <td>7.95 đơn/tx</td>
                        <td>106.00%</td>
                        <td>25,957 đơn</td>
                        <td>96.33%</td>
                        <td><span class="pill pill-green">🟢 Vượt năng suất target</span></td>
                    </tr>
                    <tr>
                        <td><strong>SGN — New Last Month (NLM)</strong></td>
                        <td>629</td>
                        <td>111.89%</td>
                        <td>9.28 đơn/tx</td>
                        <td>97.68%</td>
                        <td>5,837 đơn</td>
                        <td>109.30%</td>
                        <td><span class="pill pill-green">🟢 Vượt target active</span></td>
                    </tr>
                    <tr>
                        <td><strong>HAN — Full Time (FT)</strong></td>
                        <td>999</td>
                        <td>96.99%</td>
                        <td>14.36 đơn/tx</td>
                        <td>105.11%</td>
                        <td>14,346 đơn</td>
                        <td>101.94%</td>
                        <td><span class="pill pill-green">🟢 Vượt target sản lượng</span></td>
                    </tr>
                    <tr>
                        <td><strong>HAN — Part Time (PT)</strong></td>
                        <td>3,175</td>
                        <td>86.37%</td>
                        <td>7.66 đơn/tx</td>
                        <td>109.30%</td>
                        <td>24,321 đơn</td>
                        <td>94.41%</td>
                        <td><span class="pill pill-yellow">🟡 Năng suất gánh active</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- VIEW 2: RETENTION & SUPPLY HOURS -->
    <div id="view-retention" class="hidden">
        <div class="grid-container">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🔄 Retention Rate Bóc Tách Theo Segment (SGN vs HAN)</div>
                </div>
                <div class="chart-container">
                    <canvas id="retentionSegmentChart"></canvas>
                </div>
            </div>
            <div class="card">
                <div class="card-header">
                    <div class="card-title">⏱️ Supply Hours Breakdown</div>
                </div>
                <div class="chart-container">
                    <canvas id="supplyHoursChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">📊 Chi Tiết Retention Tài Xế >=22 Tuổi Theo Segment</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Region & Segment</th>
                        <th>Tổng Segment Driver</th>
                        <th>Active Driver Realized</th>
                        <th>Tỷ Lệ Retention MTD</th>
                        <th>Biến Động MoM</th>
                        <th>Biến Động YoY</th>
                        <th>Đánh Giá Độ Bền Vững</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>HAN — Full-Time (FT)</strong></td>
                        <td>1,230</td>
                        <td>1,183</td>
                        <td><strong>96.18%</strong></td>
                        <td>-2.45%</td>
                        <td>-1.33%</td>
                        <td><span class="pill pill-green">🟢 Giữ chân cực bền vững</span></td>
                    </tr>
                    <tr>
                        <td><strong>HAN — Part-Time (PT)</strong></td>
                        <td>7,174</td>
                        <td>5,352</td>
                        <td><strong>74.60%</strong></td>
                        <td>-0.28%</td>
                        <td>-0.60%</td>
                        <td><span class="pill pill-green">🟢 Ổn định</span></td>
                    </tr>
                    <tr>
                        <td><strong>HAN — New Last Month (NLM)</strong></td>
                        <td>867</td>
                        <td>590</td>
                        <td><strong>68.05%</strong></td>
                        <td>-2.85%</td>
                        <td>-4.71%</td>
                        <td><span class="pill pill-yellow">🟡 Cần kích hoạt lại (CHL)</span></td>
                    </tr>
                    <tr>
                        <td><strong>SGN — Full-Time (FT)</strong></td>
                        <td>3,274</td>
                        <td>3,125</td>
                        <td><strong>95.45%</strong></td>
                        <td>-0.82%</td>
                        <td>-0.35%</td>
                        <td><span class="pill pill-green">🟢 Giữ chân cực bền vững</span></td>
                    </tr>
                    <tr>
                        <td><strong>SGN — Part-Time (PT)</strong></td>
                        <td>9,937</td>
                        <td>6,357</td>
                        <td><strong>63.97%</strong></td>
                        <td>-2.43%</td>
                        <td>-2.26%</td>
                        <td><span class="pill pill-yellow">🟡 Cần theo dõi</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- VIEW 3: PROJECTS & FLEETS -->
    <div id="view-projects" class="hidden">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🚀 Tình Hình Các Dự Án Vận Hành Trọng Điểm (Baga / MiniHub / EV Bike)</div>
                <span class="pill pill-purple">PROJECT SPOTLIGHT</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Dự Án / Fleet</th>
                        <th>Chỉ Số Trọng Tâm Track</th>
                        <th>Kết Quả Thực Tế MTD</th>
                        <th>Kế Hoạch & Action Tiếp Theo</th>
                        <th>Trạng Thái Tiến Độ</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Đội Core 2H / Bulky</strong></td>
                        <td>Số lượng tài xế gia nhập đội core</td>
                        <td>57 tài xế mới gia nhập chính thức (lọc 29 tx kém)</td>
                        <td>Tuyển bổ sung 40 tài xế/tuần, theo dõi năng suất sau thanh lọc</td>
                        <td><span class="pill pill-green">🟢 Đang chạy tốt</span></td>
                    </tr>
                    <tr>
                        <td><strong>Project Trang Bị Baga Bulky</strong></td>
                        <td>Số tài xế đăng ký & trang bị baga</td>
                        <td>Đã duyệt plan thưởng 3 giai đoạn (15/8 - 30/9)</td>
                        <td>Phối hợp DS đẩy truyền thông branding lợi ích gắn baga</td>
                        <td><span class="pill pill-green">🟢 Đúng timeline</span></td>
                    </tr>
                    <tr>
                        <td><strong>Xe Điện EV (AIZEN / Dat Bike / Tailg)</strong></td>
                        <td>Tài xế active MTD xe điện</td>
                        <td>SGN: 656/475 (135%) | HAN: 504/535 (94%)</td>
                        <td>Tỷ lệ convert lead ~25% (964 liên hệ ➔ 165 EV). Quy hoạch lại luồng lead</td>
                        <td><span class="pill pill-yellow">🟡 Cần đẩy mạnh convert</span></td>
                    </tr>
                    <tr>
                        <td><strong>MiniHub & Captain Operations</strong></td>
                        <td>Checkin rate & Online rate các Zone</td>
                        <td>Checkin rate >92%, Online rate >92% (Z2&4 tăng active)</td>
                        <td>Duy trì online rate, loại TX kém, cải thiện Shift hour Z136</td>
                        <td><span class="pill pill-green">🟢 Đạt chuẩn KPI</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- VIEW 4: QUALITY, COMMS & VOICES -->
    <div id="view-quality" class="hidden">
        <div class="card">
            <div class="card-header">
                <div class="card-title">🛡️ Đánh Giá Tỷ Lệ Tuân Thủ CTR, GDR & Driver Voices</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Chỉ Số / Hạng Mục</th>
                        <th>TP.HCM (SGN)</th>
                        <th>Hà Nội (HAN)</th>
                        <th>Toàn Quốc (NW)</th>
                        <th>Đánh Giá & Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Compliance True Rate (CTR)</strong></td>
                        <td><strong>81.20%</strong></td>
                        <td><strong>70.86%</strong></td>
                        <td><strong>78.49%</strong></td>
                        <td><span class="pill pill-green">🟢 Đạt 130% Target KPI</span></td>
                    </tr>
                    <tr>
                        <td><strong>Good Driver Rate (GDR)</strong></td>
                        <td><strong>97.30%</strong></td>
                        <td><strong>95.57%</strong></td>
                        <td><strong>96.53%</strong></td>
                        <td><span class="pill pill-green">🟢 Đạt 120% Target KPI</span></td>
                    </tr>
                    <tr>
                        <td><strong>Driver Voices (Phản hồi Tx)</strong></td>
                        <td colspan="3">20 ca tài xế bị truy thu đồng phục sai luồng xác thực ngày 6/8. Team đã làm việc với QM check case by case và hoàn tiền.</td>
                        <td><span class="pill pill-green">✅ Đã giải quyết xong</span></td>
                    </tr>
                    <tr>
                        <td><strong>Sự Kiện Sinh Nhật AHM 11T</strong></td>
                        <td colspan="3">Triển khai minigame online "Chuyển ý tưởng - Ghép tương lai", bàn giao xe KOC (3 Camel 1, 1 Camel 2).</td>
                        <td><span class="pill pill-purple">🚀 Pre-event bùng nổ</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function switchView(viewName) {
            document.getElementById('view-campaign').classList.add('hidden');
            document.getElementById('view-retention').classList.add('hidden');
            document.getElementById('view-projects').classList.add('hidden');
            document.getElementById('view-quality').classList.add('hidden');

            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

            if(viewName === 'campaign') {
                document.getElementById('view-campaign').classList.remove('hidden');
                event.target.classList.add('active');
            } else if(viewName === 'retention') {
                document.getElementById('view-retention').classList.remove('hidden');
                event.target.classList.add('active');
            } else if(viewName === 'projects') {
                document.getElementById('view-projects').classList.remove('hidden');
                event.target.classList.add('active');
            } else if(viewName === 'quality') {
                document.getElementById('view-quality').classList.remove('hidden');
                event.target.classList.add('active');
            }
        }

        window.onload = function() {
            // Chart 1: Campaign Capacity vs Demand
            const ctx1 = document.getElementById('campaignChart').getContext('2d');
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['SGN Campaign 8.8', 'HAN Campaign 8.8'],
                    datasets: [
                        { label: 'Capacity Actual (Đơn)', data: [66334, 45636], backgroundColor: '#FF6B00' },
                        { label: 'Demand Requested (Đơn)', data: [77506, 60142], backgroundColor: '#3B82F6' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#F8FAFC' } } } }
            });

            // Chart 2: Driver Income & Prod
            const ctx2 = document.getElementById('incomeChart').getContext('2d');
            new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['SGN CP 8.8', 'HAN CP 8.8'],
                    datasets: [
                        { label: 'Thu Nhập / Giờ (VNĐ)', data: [52700, 58000], backgroundColor: '#10B981' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#F8FAFC' } } } }
            });

            // Chart 3: Retention Segment
            const ctx3 = document.getElementById('retentionSegmentChart').getContext('2d');
            new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: ['FT Retention', 'PT Retention', 'NLM Retention'],
                    datasets: [
                        { label: 'HAN Retention (%)', data: [96.18, 74.60, 68.05], backgroundColor: '#F43F5E' },
                        { label: 'SGN Retention (%)', data: [95.45, 63.97, 60.73], backgroundColor: '#3B82F6' }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#F8FAFC' } } } }
            });

            // Chart 4: Supply Hours
            const ctx4 = document.getElementById('supplyHoursChart').getContext('2d');
            new Chart(ctx4, {
                type: 'doughnut',
                data: {
                    labels: ['SGN Supply Hours (283.4K h)', 'HAN Supply Hours (182K h)'],
                    datasets: [{ data: [283394, 182000], backgroundColor: ['#FF6B00', '#8B5CF6'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#F8FAFC' } } } }
            });
        };
    </script>
</body>
</html>
"""

    out_dir = "Output/Ahamove/04. OPS_METRICS"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ahamove_team_meeting_dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🎉 Đã xuất thành công Custom Team Meeting Dashboard tại: {out_path}")

if __name__ == "__main__":
    build_team_meeting_html_dashboard()
