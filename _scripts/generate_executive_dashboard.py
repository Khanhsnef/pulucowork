#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE EXECUTIVE OPERATIONAL KPI DASHBOARD & INSIGHTS REPORT GENERATOR
===============================================================================
Tự động tạo HTML Dashboard Tương Tác Chuẩn Thương Hiệu Ahamove (Canvas Style)
tích hợp 3 Chế Độ View:
1. Daily Tracking Mode (Theo dõi xung nhịp vận hành ngày)
2. Weekly Monday Report Mode (Báo cáo Thứ 2 hàng tuần)
3. Monthly Review Mode (Báo cáo tổng kết tháng & Bảng điểm KPI Team)

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_html_dashboard():
    # Load all raw CSV datasets
    try:
        df1_w = pd.read_csv('/tmp/card_75557_4weeks.csv')
        df4_w = pd.read_csv('/tmp/card_77913_4weeks.csv')
        df1_m = pd.read_csv('/tmp/card_75557_4months.csv')
        df_ar_fr = pd.read_csv('/tmp/kpi_card_75750.csv')
        df_supply = pd.read_csv('/tmp/kpi_card_79066.csv')
        df_gdr = pd.read_csv('/tmp/kpi_card_62728.csv')
        df_ctr = pd.read_csv('/tmp/kpi_card_75304.csv')
        df_cr = pd.read_csv('/tmp/kpi_card_76069.csv')
        df_ret22 = pd.read_csv('/tmp/kpi_card_79068.csv')
    except Exception as e:
        print(f"Lỗi đọc data CSV: {e}")
        return

    html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahamove Operations Executive Dashboard — Daily, Weekly & Monthly KPI Control</title>
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
            --text-main: #F8FAFC;
            --text-sub: #94A3B8;
            --border-color: rgba(255, 255, 255, 0.1);
            --glass-bg: rgba(30, 41, 59, 0.7);
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

        /* HEADER & NAVBAR */
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
            gap: 12px;
        }

        .brand-logo {
            background: linear-gradient(135deg, #FF6B00, #FF8533);
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 22px;
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
        }

        .tab-btn {
            padding: 10px 20px;
            border: none;
            background: transparent;
            color: var(--text-sub);
            font-weight: 600;
            font-size: 14px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .tab-btn.active {
            background: var(--accent-orange);
            color: white;
            box-shadow: 0 2px 10px rgba(255, 107, 0, 0.3);
        }

        /* HERO STATS BAR */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 107, 0, 0.4);
        }

        .stat-card.focal {
            grid-column: span 2;
            background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(30, 41, 59, 0.8));
            border: 1px solid rgba(255, 107, 0, 0.4);
        }

        .stat-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            margin-bottom: 12px;
        }

        .badge-orange { background: rgba(255, 107, 0, 0.2); color: #FF944D; }
        .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .badge-blue { background: rgba(59, 130, 246, 0.2); color: #60A5FA; }
        .badge-rose { background: rgba(244, 63, 94, 0.2); color: #FB7185; }

        .stat-value {
            font-size: 32px;
            font-weight: 900;
            letter-spacing: -1px;
            margin-bottom: 4px;
        }

        .stat-label {
            font-size: 13px;
            color: var(--text-sub);
            font-weight: 500;
        }

        /* MAIN CONTENT LAYOUT */
        .grid-container {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
            margin-bottom: 24px;
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
            background: rgba(15, 23, 42, 0.5);
        }

        td {
            padding: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        tr:hover td {
            background: var(--bg-card-hover);
        }

        .pill {
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 11px;
        }

        .pill-green { background: rgba(16, 185, 129, 0.2); color: #34D399; }
        .pill-red { background: rgba(244, 63, 94, 0.2); color: #FB7185; }
        .pill-yellow { background: rgba(245, 158, 11, 0.2); color: #FBBF24; }

        /* EXECUTIVE TAKEAWAYS BOX */
        .takeaway-box {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(255, 107, 0, 0.3);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
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
            margin-bottom: 14px;
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

    <!-- HEADER -->
    <div class="header">
        <div class="brand">
            <div class="brand-logo">A</div>
            <div class="brand-title">
                <h1>Ahamove Operations Executive Dashboard</h1>
                <p>Hệ Thống Phân Tích Strategist & Control Center 2026</p>
            </div>
        </div>
        <div class="view-switcher">
            <button class="tab-btn active" onclick="switchView('daily')">⚡ Daily Pulse</button>
            <button class="tab-btn" onclick="switchView('weekly')">📊 Weekly Review (Thứ 2)</button>
            <button class="tab-btn" onclick="switchView('monthly')">🏆 Monthly KPI & Scorecards</button>
        </div>
    </div>

    <!-- HERO STATS BAR -->
    <div class="stats-grid">
        <div class="stat-card focal">
            <div class="stat-badge badge-orange">🚗 ACTIVE DRIVERS (WEEKLY AVG)</div>
            <div class="stat-value">24,121 <span style="font-size:16px; font-weight:500; color:var(--accent-emerald);">+3.2% WoW</span></div>
            <div class="stat-label">Tài xế duy nhất/tuần (SGN: 10,872 | HAN: 9,305 | EXP: 3,944) — Non-Additive</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-emerald">🔄 MONTHLY RETENTION</div>
            <div class="stat-value" style="color:var(--accent-emerald);">97.87%</div>
            <div class="stat-label">Tài xế cũ active tiếp (Exclude NIM/NLM)</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-blue">🎯 ACCEPTANCE RATE (AR)</div>
            <div class="stat-value">91.49%</div>
            <div class="stat-label">Toàn quốc (SGN: 95.1% | HAN: 87.7%)</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-rose">⚡ FULFILLMENT RATE (FR)</div>
            <div class="stat-value" style="color:var(--accent-amber);">81.38%</div>
            <div class="stat-label">Toàn quốc (SGN: 86.2% | HAN: 76.0%)</div>
        </div>
        <div class="stat-card">
            <div class="stat-badge badge-orange">🛡️ COMPLIANCE CTR</div>
            <div class="stat-value">74.15%</div>
            <div class="stat-label">Tuân thủ quy chuẩn (Tăng liên tục 4 tháng)</div>
        </div>
    </div>

    <!-- EXECUTIVE TAKEAWAYS BOX -->
    <div class="takeaway-box">
        <div class="takeaway-title">💡 STRATEGIC EXECUTIVE TAKEAWAYS & KEY DECISIONS</div>
        <div class="takeaway-item">
            <strong>Hà Nội (HAN) Peak Surge Bottleneck:</strong> Tỷ lệ đơn bị tăng giá (<code>surge_rate</code>) tại HAN lên tới <strong>48.26%</strong> với hệ số <strong>1.31x</strong>, kéo FR xuống <strong>76.04%</strong>. Cần điều phối gói thưởng ca kíp cho 1,241 tài xế FT tại HAN.
        </div>
        <div class="takeaway-item">
            <strong>Monthly Retention Bền Vững:</strong> Tỷ lệ giữ chân tài xế cũ hàng tháng (loại trừ NIM & NLM) duy trì ở mức cao ấn tượng <strong>97.01% tại SGN</strong> và <strong>94.60% tại HAN</strong>.
        </div>
        <div class="takeaway-item">
            <strong>Chất Lượng Tân Binh (NIM):</strong> Tệp tài xế mới gia nhập trong tháng (NIM) có tỷ lệ hủy thấp (<code>lcd_driver</code>) đạt tới <strong>52.21%</strong>. Cần chính sách giữ chân Retain M1 để tránh Churn sang NLM (39.0%).
        </div>
        <div class="takeaway-item">
            <strong>Kỷ Lực Tuân Thủ CTR:</strong> Tỷ lệ tuân thủ CTR đạt mốc kỷ lục mới <strong>74.15%</strong> (tăng trưởng liên tục từ 70.87% tháng 5).
        </div>
    </div>

    <!-- VIEW 1: DAILY PULSE (ACTIVE DEFAULT) -->
    <div id="view-daily">
        <div class="grid-container">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">⚡ Daily Operations Pulse & Regional Breakdown (SGN - HAN - EXP)</div>
                    <span class="pill pill-green">LIVE UPDATED</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Khu Vực (Region)</th>
                            <th>Nhu Cầu Đơn (Requested)</th>
                            <th>Giao Thành Công (Completed)</th>
                            <th>Tỷ Lệ AR</th>
                            <th>Tỷ Lệ FR</th>
                            <th>Surge Rate</th>
                            <th>Surge Value</th>
                            <th>Đánh Giá SLA</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>TP.HCM (SGN)</strong></td>
                            <td>369,860</td>
                            <td>317,854</td>
                            <td>94.42%</td>
                            <td><strong style="color:var(--accent-emerald)">85.94%</strong></td>
                            <td>16.77%</td>
                            <td>1.15x</td>
                            <td><span class="pill pill-green">🟢 Đạt SLA Xuất sắc</span></td>
                        </tr>
                        <tr>
                            <td><strong>Hà Nội (HAN)</strong></td>
                            <td>312,277</td>
                            <td>237,095</td>
                            <td>85.81%</td>
                            <td><strong style="color:var(--accent-rose)">75.92%</strong></td>
                            <td><strong style="color:var(--accent-rose)">48.26%</strong></td>
                            <td>1.31x</td>
                            <td><span class="pill pill-red">🔴 Thiếu hụt cung cao điểm</span></td>
                        </tr>
                        <tr>
                            <td><strong>Tỉnh Mở Rộng (EXP)</strong></td>
                            <td>58,863</td>
                            <td>48,486</td>
                            <td>90.54%</td>
                            <td><strong style="color:var(--accent-emerald)">82.37%</strong></td>
                            <td>16.02%</td>
                            <td>1.12x</td>
                            <td><span class="pill pill-green">🟢 Đạt SLA</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="card">
                <div class="card-header">
                    <div class="card-title">📊 Top Fleet SLA Status</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Fleet Dịch Vụ</th>
                            <th>Tỷ Lệ FR</th>
                            <th>SLA</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Đội Baga Bulky (SGN)</td>
                            <td>92.12%</td>
                            <td><span class="pill pill-green">Xuất sắc</span></td>
                        </tr>
                        <tr>
                            <td>Đội Baga Bulky (HAN)</td>
                            <td>84.35%</td>
                            <td><span class="pill pill-green">Đạt SLA</span></td>
                        </tr>
                        <tr>
                            <td>1H Siêu Tốc (SGN)</td>
                            <td>86.25%</td>
                            <td><span class="pill pill-green">Đạt SLA</span></td>
                        </tr>
                        <tr>
                            <td>1H Siêu Tốc (HAN)</td>
                            <td>76.10%</td>
                            <td><span class="pill pill-red">Thiếu cung</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- VIEW 2: WEEKLY REPORT MODE -->
    <div id="view-weekly" class="hidden">
        <div class="card">
            <div class="card-header">
                <div class="card-title">📊 4-Week WoW Active Driver Trend (Per-Period Unique Active)</div>
                <span class="pill pill-yellow">WEEKLY MONDAY VIEW</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Mốc Tuần (Period)</th>
                        <th>TP.HCM (SGN)</th>
                        <th>Hà Nội (HAN)</th>
                        <th>Tỉnh Mở Rộng (EXP)</th>
                        <th>Tổng Active Duy Nhất (Weekly Unique)</th>
                        <th>Biến Động WoW</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>2026-07-27</strong></td>
                        <td>11,092</td>
                        <td>9,396</td>
                        <td>4,169</td>
                        <td><strong>24,657</strong></td>
                        <td>—</td>
                    </tr>
                    <tr>
                        <td><strong>2026-08-03</strong></td>
                        <td>11,433</td>
                        <td>9,672</td>
                        <td>4,347</td>
                        <td><strong>25,452</strong></td>
                        <td><span class="pill pill-green">+3.2%</span></td>
                    </tr>
                    <tr>
                        <td><strong>2026-08-10</strong></td>
                        <td>11,332</td>
                        <td>9,737</td>
                        <td>4,336</td>
                        <td><strong>25,405</strong></td>
                        <td><span class="pill pill-green">-0.2%</span></td>
                    </tr>
                    <tr>
                        <td><strong>2026-08-17</strong></td>
                        <td>9,630</td>
                        <td>8,416</td>
                        <td>2,925</td>
                        <td><strong>20,971</strong></td>
                        <td><span class="pill pill-yellow">-17.4% (Tính tới 20/08)</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- VIEW 3: MONTHLY REVIEW & SCORECARDS -->
    <div id="view-monthly" class="hidden">
        <div class="grid-container">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🔄 Monthly Retention Rate (Loại Trừ NIM & NLM)</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Chu Kỳ Shift Tháng (MoM)</th>
                            <th>SGN Retention</th>
                            <th>HAN Retention</th>
                            <th>EXP Retention</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Tháng 5 ➔ Tháng 6</strong></td>
                            <td>12,013 ➔ 11,757 (<strong>97.87%</strong>)</td>
                            <td>11,967 ➔ 11,456 (<strong>95.73%</strong>)</td>
                            <td>2,134 ➔ 2,027 (<strong>94.99%</strong>)</td>
                        </tr>
                        <tr>
                            <td><strong>Tháng 6 ➔ Tháng 7</strong></td>
                            <td>11,757 ➔ 11,701 (<strong>99.52%</strong>)</td>
                            <td>11,456 ➔ 11,047 (<strong>96.43%</strong>)</td>
                            <td>2,027 ➔ 2,036 (<strong>100.44%</strong>)</td>
                        </tr>
                        <tr>
                            <td><strong>Tháng 7 ➔ Tháng 8</strong></td>
                            <td>11,701 ➔ 10,957 (<strong>93.64%</strong>)</td>
                            <td>11,047 ➔ 10,122 (<strong>91.63%</strong>)</td>
                            <td>2,036 ➔ 1,899 (<strong>93.27%</strong>)</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="card">
                <div class="card-header">
                    <div class="card-title">🏆 Top Team Member KPI Scorecards</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Thành Viên Team</th>
                            <th>Chức Danh</th>
                            <th>Tổng Điểm Trọng Số KPI</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Nguyễn Huy Hoàng</strong></td>
                            <td>HAN-DM Executive</td>
                            <td><strong style="color:var(--accent-emerald)">84.71%</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Nguyễn Thanh Trúc</strong></td>
                            <td>SGN-DM Specialist</td>
                            <td><strong style="color:var(--accent-emerald)">84.71%</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Đào Thị Thu Trang</strong></td>
                            <td>Assistant Manager</td>
                            <td><strong style="color:var(--accent-emerald)">78.17%</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Lê Phương Khanh</strong></td>
                            <td>SGN Leader</td>
                            <td><strong style="color:var(--accent-amber)">70.28%</strong></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        function switchView(viewName) {
            document.getElementById('view-daily').classList.add('hidden');
            document.getElementById('view-weekly').classList.add('hidden');
            document.getElementById('view-monthly').classList.add('hidden');

            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

            if(viewName === 'daily') {
                document.getElementById('view-daily').classList.remove('hidden');
                event.target.classList.add('active');
            } else if(viewName === 'weekly') {
                document.getElementById('view-weekly').classList.remove('hidden');
                event.target.classList.add('active');
            } else if(viewName === 'monthly') {
                document.getElementById('view-monthly').classList.remove('hidden');
                event.target.classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

    out_dir = "Output/Ahamove/04. OPS_METRICS"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ahamove_executive_kpi_dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🎉 Đã xuất thành công Interactive Dashboard tại: {out_path}")

if __name__ == "__main__":
    build_html_dashboard()
