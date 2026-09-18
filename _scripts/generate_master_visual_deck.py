import os
import json

html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Driver Operations Performance Report — Ahamove DM NW</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #0E4174;
            --primary-dark: #0A2E52;
            --secondary: #FF7F32;
            --secondary-light: #FFF7ED;
            --success: #10B981;
            --success-light: #ECFDF5;
            --warning: #F59E0B;
            --warning-light: #FFFBEB;
            --danger: #EF4444;
            --danger-light: #FEF2F2;
            --bg-dark: #0F172A;
            --card-bg: #FFFFFF;
            --text-dark: #0F172A;
            --text-muted: #64748B;
            --border-light: #E2E8F0;
            --radius-lg: 16px;
            --radius-md: 10px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-dark);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
            -webkit-font-smoothing: antialiased;
        }

        /* 16:9 Stage Wrapper */
        .stage-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100vw;
            height: 100vh;
            padding: 1.5rem;
        }

        .stage {
            width: 1280px;
            height: 720px;
            position: relative;
            background: #F8FAFC;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
            border-radius: 20px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .slide {
            display: none;
            width: 100%;
            height: 100%;
            padding: 2.2rem 3rem;
            background: #F8FAFC;
            flex-direction: column;
            justify-content: space-between;
            position: absolute;
            top: 0;
            left: 0;
            box-sizing: border-box;
            overflow: hidden;
        }

        .slide.active {
            display: flex;
        }

        /* Header Bar */
        .slide-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border-light);
            padding-bottom: 0.8rem;
            margin-bottom: 1.2rem;
        }

        .slide-header h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.65rem;
            font-weight: 800;
            color: var(--primary);
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        .brand-tag {
            background: rgba(14, 65, 116, 0.08);
            color: var(--primary);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.3rem 0.8rem;
            border-radius: 99px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Slide Content Area */
        .slide-body {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            overflow: hidden;
        }

        /* Grid Layouts */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; height: 100%; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
        .grid-2-1 { display: grid; grid-template-columns: 2fr 1fr; gap: 1.2rem; height: 100%; }
        .grid-1-2 { display: grid; grid-template-columns: 1fr 2fr; gap: 1.2rem; height: 100%; }

        /* Bento Cards */
        .bento-card {
            background: var(--card-bg);
            border-radius: var(--radius-lg);
            padding: 1.25rem 1.5rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
        }

        .bento-card.highlight {
            border-left: 5px solid var(--secondary);
        }

        .bento-card.danger-border {
            border-left: 5px solid var(--danger);
        }

        .bento-card.success-border {
            border-left: 5px solid var(--success);
        }

        /* Giant KPI Callout */
        .kpi-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.3rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .kpi-number {
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1;
            margin: 0.4rem 0;
        }

        .kpi-number.success { color: var(--success); }
        .kpi-number.warning { color: var(--warning); }
        .kpi-number.danger { color: var(--danger); }
        .kpi-number.primary { color: var(--primary); }

        .kpi-subtext {
            font-size: 0.82rem;
            color: var(--text-muted);
            line-height: 1.4;
        }

        /* Status Pills */
        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: 99px;
        }

        .status-pill.success { background: var(--success-light); color: var(--success); }
        .status-pill.warning { background: var(--warning-light); color: var(--warning); }
        .status-pill.danger { background: var(--danger-light); color: var(--danger); }

        /* Tables */
        table.ops-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        table.ops-table th {
            background: #F1F5F9;
            color: var(--primary);
            font-weight: 700;
            text-align: left;
            padding: 0.6rem 0.8rem;
            border-bottom: 2px solid var(--border-light);
        }

        table.ops-table td {
            padding: 0.65rem 0.8rem;
            border-bottom: 1px solid var(--border-light);
            color: var(--text-dark);
            line-height: 1.4;
        }

        table.ops-table tr:hover {
            background: #F8FAFC;
        }

        /* Timeline & Steps */
        .step-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .step-item {
            display: flex;
            gap: 0.8rem;
            align-items: flex-start;
            background: #F8FAFC;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--primary);
        }

        .step-num {
            background: var(--primary);
            color: #FFF;
            font-weight: 800;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            flex-shrink: 0;
        }

        /* Title Slide Custom */
        .slide.title-slide {
            background: linear-gradient(135deg, #0A2E52 0%, #0E4174 60%, #1E293B 100%);
            color: #FFF;
            padding: 4rem;
            justify-content: center;
            position: relative;
        }

        .title-slide h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 1rem;
            color: #FFFFFF;
        }

        .title-slide .hero-tag {
            display: inline-block;
            background: rgba(255, 127, 50, 0.2);
            border: 1px solid #FF7F32;
            color: #FF9D66;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 0.4rem 1rem;
            border-radius: 99px;
            margin-bottom: 1.5rem;
        }

        /* Footer Bar */
        .slide-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--border-light);
            padding-top: 0.6rem;
            margin-top: 0.8rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        /* Control Panel Floating */
        .controls {
            position: absolute;
            bottom: 1rem;
            right: 2rem;
            display: flex;
            gap: 0.5rem;
            z-index: 100;
            background: rgba(15, 23, 42, 0.8);
            padding: 0.4rem 0.8rem;
            border-radius: 99px;
            backdrop-filter: blur(8px);
        }

        .btn-ctrl {
            background: #334155;
            color: #FFF;
            border: none;
            padding: 0.4rem 0.8rem;
            border-radius: 99px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-ctrl:hover {
            background: var(--secondary);
        }

        /* Chart Canvas Container */
        .chart-box {
            position: relative;
            width: 100%;
            height: 220px;
        }
    </style>
</head>
<body>

    <div class="stage-wrapper">
        <div class="stage" id="stage">

            <!-- SLIDE 1: COVER -->
            <div class="slide title-slide active">
                <span class="hero-tag">AHAMOVE DRIVER MANAGEMENT NETWORK</span>
                <h1>MASTER DRIVER OPERATIONS PERFORMANCE REPORT</h1>
                <p style="font-size: 1.1rem; color: #94A3B8; max-width: 800px; line-height: 1.6;">
                    Comprehensive Diagnostic & Strategy Framework (WHAT → WHERE → WHO → IMPACT → WHY → ACTION → EXPECTED RECOVERY)
                </p>
                <div style="margin-top: 2.5rem; display: flex; gap: 2rem; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 1.2rem;">
                    <div>
                        <span style="font-size: 0.75rem; color: #64748B; text-transform: uppercase;">Lead Author</span>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #FFF;">Strategy & BI Operations Team</div>
                    </div>
                    <div>
                        <span style="font-size: 0.75rem; color: #64748B; text-transform: uppercase;">Scope</span>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #FF9D66;">DM NW Performance & Quality Diagnostic</div>
                    </div>
                    <div>
                        <span style="font-size: 0.75rem; color: #64748B; text-transform: uppercase;">Data Source</span>
                        <div style="font-size: 0.95rem; font-weight: 700; color: #FFF;">Metabase 11 Cards Audit</div>
                    </div>
                </div>
            </div>

            <!-- SLIDE 2: KPI HEALTH OVERVIEW -->
            <div class="slide">
                <div class="slide-header">
                    <h2>📊 1.1. KPI Health Overview Dashboard</h2>
                    <span class="brand-tag">EXECUTIVE SUMMARY</span>
                </div>
                <div class="slide-body">
                    <div class="grid-4">
                        <div class="bento-card success-border">
                            <div class="kpi-title">🟢 Compliance True Rate</div>
                            <div class="kpi-number success">74.15%</div>
                            <div class="kpi-subtext">▲ Kỷ lục mới toàn quốc.<br>Đảm bảo tuân thủ tiêu chuẩn vận hành.</div>
                        </div>
                        <div class="bento-card warning-border">
                            <div class="kpi-title">🟡 Fulfillment Rate (FR NW)</div>
                            <div class="kpi-number warning">81.38%</div>
                            <div class="kpi-subtext">SGN bứt phá <strong>86.2%</strong><br>HAN sụt giảm còn <strong>75.8%</strong></div>
                        </div>
                        <div class="bento-card warning-border">
                            <div class="kpi-title">🟡 SGN Retention NLM</div>
                            <div class="kpi-number warning">65.15%</div>
                            <div class="kpi-subtext">▼ -5.45% MoM (Sụt 718 tx).<br>Cần can thiệp nhóm Tân binh.</div>
                        </div>
                        <div class="bento-card danger-border">
                            <div class="kpi-title">🔴 CityZone Checkin No-Show</div>
                            <div class="kpi-number danger">32.2%</div>
                            <div class="kpi-subtext">163 ca No-show (39% ca ảo vẫn hoàn thành 401 đơn).</div>
                        </div>
                    </div>

                    <div class="grid-2-1" style="margin-top: 0.5rem;">
                        <div class="bento-card">
                            <div class="kpi-title">📈 Mức Độ Biến Động Fulfillment Rate Theo Khu Vực</div>
                            <div class="chart-box">
                                <canvas id="frChart"></canvas>
                            </div>
                        </div>
                        <div class="bento-card highlight">
                            <div class="kpi-title">🏆 Key Takeaways</div>
                            <ul style="font-size: 0.82rem; line-height: 1.5; color: var(--text-dark); padding-left: 1rem;">
                                <li><strong>Hà Nội nghẽn cung ca cao điểm:</strong> FR HAN chạm mốc đáy 75.8%, Surge vọt 48.3%.</li>
                                <li><strong>Chất lượng SGN duy trì đỉnh:</strong> Good Driver Rate SGN đạt 96.51% (Max score 1.20x).</li>
                                <li><strong>Sự cố UX CityZone Hub:</strong> Lỗi quên bấm Check-in ca làm ảnh hưởng 25.6% đơn hàng.</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 2 / 8</span>
                </div>
            </div>

            <!-- SLIDE 3: TOP 3 PROBLEM STATEMENTS -->
            <div class="slide">
                <div class="slide-header">
                    <h2>🎯 1.2. Top 3 Problem Statements (Prioritization P0 / P1)</h2>
                    <span class="brand-tag">PROBLEM PRIORITIZATION</span>
                </div>
                <div class="slide-body">
                    <div class="grid-3">
                        <div class="bento-card danger-border">
                            <div>
                                <span class="status-pill danger">PRIORITY P0</span>
                                <h3 style="font-size: 1.1rem; font-weight: 800; color: var(--primary); margin: 0.6rem 0 0.4rem 0;">PROB-01: FR HAN Sụt Ca Cao Điểm</h3>
                                <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">
                                    Fulfillment Rate Hà Nội sụt về <strong>75.8%</strong> trong ca trưa (11h-13h) và ca chiều (17h-19h). Surge Rate vọt 48.3% (Hệ số 1.31x), RPH 2.07.
                                </p>
                            </div>
                            <div style="background: var(--danger-light); padding: 0.6rem; border-radius: 8px; margin-top: 0.8rem;">
                                <span style="font-size: 0.75rem; font-weight: 700; color: var(--danger);">TÁC ĐỘNG KINH DOANH:</span>
                                <div style="font-size: 0.85rem; font-weight: 800; color: var(--danger);">Thất thoát ~95,000 đơn/tháng</div>
                            </div>
                        </div>

                        <div class="bento-card danger-border">
                            <div>
                                <span class="status-pill danger">PRIORITY P0</span>
                                <h3 style="font-size: 1.1rem; font-weight: 800; color: var(--primary); margin: 0.6rem 0 0.4rem 0;">PROB-02: UX CityZone Check-in Sót Đơn</h3>
                                <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">
                                    163 ca No-show (32.2% ca). Tuy nhiên 39% số ca No-show đó (99 ca) <strong>vẫn hoàn thành 401 đơn</strong> do tài xế quên bấm Check-in.
                                </p>
                            </div>
                            <div style="background: var(--danger-light); padding: 0.6rem; border-radius: 8px; margin-top: 0.8rem;">
                                <span style="font-size: 0.75rem; font-weight: 700; color: var(--danger);">TÁC ĐỘNG KINH DOANH:</span>
                                <div style="font-size: 0.85rem; font-weight: 800; color: var(--danger);">Sót đơn tính thưởng & khiếu nại +50%</div>
                            </div>
                        </div>

                        <div class="bento-card warning-border">
                            <div>
                                <span class="status-pill warning">PRIORITY P1</span>
                                <h3 style="font-size: 1.1rem; font-weight: 800; color: var(--primary); margin: 0.6rem 0 0.4rem 0;">PROB-03: Shopee Reverse Cancel Rate Vọt</h3>
                                <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">
                                    Tỷ lệ hủy đơn dịch vụ Shopee Reverse tăng lên mốc <strong>37.61%</strong> do quy trình gán đơn đổi trả phức tạp và thông tin địa chỉ lấy hàng nhiễu.
                                </p>
                            </div>
                            <div style="background: var(--warning-light); padding: 0.6rem; border-radius: 8px; margin-top: 0.8rem;">
                                <span style="font-size: 0.75rem; font-weight: 700; color: var(--warning);">TÁC ĐỘNG KINH DOANH:</span>
                                <div style="font-size: 0.85rem; font-weight: 800; color: var(--warning);">Tăng 3.5x tỷ lệ hủy & sụt SLA SPX</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 3 / 8</span>
                </div>
            </div>

            <!-- SLIDE 4: CHURN & LOCALIZATION ANALYSIS -->
            <div class="slide">
                <div class="slide-header">
                    <h2>🌳 2.2. Localization & Contribution Analysis</h2>
                    <span class="brand-tag">DEEP DIAGNOSTICS</span>
                </div>
                <div class="slide-body">
                    <div class="grid-2">
                        <div class="bento-card">
                            <div class="kpi-title">📉 Phân Rã Lý Do Sụt Giảm Tân Binh (NLM SGN: 718 TX)</div>
                            <div class="chart-box">
                                <canvas id="churnChart"></canvas>
                            </div>
                        </div>

                        <div class="bento-card">
                            <div class="kpi-title">📍 Phân Phối Ca Check-in CityZone Hub (506 Ca)</div>
                            <div class="chart-box">
                                <canvas id="cityzoneChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 4 / 8</span>
                </div>
            </div>

            <!-- SLIDE 5: 5 WHYS ROOT CAUSE -->
            <div class="slide">
                <div class="slide-header">
                    <h2>🔍 3.1. 5 Whys Root Cause Diagnosis</h2>
                    <span class="brand-tag">ROOT CAUSE AUDIT</span>
                </div>
                <div class="slide-body">
                    <div class="step-list">
                        <div class="step-item">
                            <div class="step-num">1</div>
                            <div>
                                <strong style="font-size: 0.9rem; color: var(--primary);">Why #1: Tại sao FR HAN bị sụt về 75.8%?</strong>
                                <div style="font-size: 0.82rem; color: var(--text-muted);">Vì tỷ lệ tăng giá (Surge Rate) vọt 48.3% (Hệ số 1.31x) và RPH chạm mốc 2.07 đơn/giờ gây nghẽn mạng lưới.</div>
                            </div>
                        </div>

                        <div class="step-item">
                            <div class="step-num">2</div>
                            <div>
                                <strong style="font-size: 0.9rem; color: var(--primary);">Why #2: Tại sao Surge Rate và RPH vọt cao?</strong>
                                <div style="font-size: 0.82rem; color: var(--text-muted);">Vì nguồn cung giờ online của tài xế thiếu hụt -15.4% so với nhu cầu ca cao điểm (11h-13h & 17h-19h).</div>
                            </div>
                        </div>

                        <div class="step-item">
                            <div class="step-num">3</div>
                            <div>
                                <strong style="font-size: 0.9rem; color: var(--primary);">Why #3: Tại sao giờ online tài xế ca cao điểm bị sụt hụt?</strong>
                                <div style="font-size: 0.82rem; color: var(--text-muted);">Tài xế Part-time (PT) giảm -6.46% giờ online và Tân binh (NIM) giảm -38.71% do thời tiết mưa nắng cực đoan.</div>
                            </div>
                        </div>

                        <div class="step-item" style="background: #FEF2F2; border-left-color: var(--danger);">
                            <div class="step-num" style="background: var(--danger);">★</div>
                            <div>
                                <strong style="font-size: 0.9rem; color: var(--danger);">ROOT CAUSE XÁC MINH (CONFIRMED):</strong>
                                <div style="font-size: 0.85rem; font-weight: 700; color: var(--danger);">
                                    Hạn chế trang bị Baga/Áo mưa tiêu chuẩn và rào cản hạn mức COD Balance (10M) khiến tài xế PT/NIM không đủ điều kiện gánh đơn Bulky ca cao điểm.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 5 / 8</span>
                </div>
            </div>

            <!-- SLIDE 6: EXECUTION ROADMAP -->
            <div class="slide">
                <div class="slide-header">
                    <h2>🎯 4.1. Execution Roadmap & Action Matrix</h2>
                    <span class="brand-tag">ACTION PLAN</span>
                </div>
                <div class="slide-body">
                    <table class="ops-table">
                        <thead>
                            <tr>
                                <th>Mã Action</th>
                                <th>Tên Giải Pháp Chi Tiết</th>
                                <th>Nhóm Ưu Tiên</th>
                                <th>PIC Đảm Nhận</th>
                                <th>Thời Gian Triển Khai</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>ACT-01</strong></td>
                                <td>Tự động hóa Geofencing Check-in qua vị trí GPS cho CityZone Hub</td>
                                <td><span class="status-pill danger">P0 High</span></td>
                                <td>Product & Operations</td>
                                <td>Tuần 1 - Tuần 2</td>
                            </tr>
                            <tr>
                                <td><strong>ACT-02</strong></td>
                                <td>Tăng hạn mức COD linh hoạt từ 10M lên 15M cho tài xế Tân binh đủ điểm tín nhiệm</td>
                                <td><span class="status-pill danger">P0 High</span></td>
                                <td>Risk & DM Lead</td>
                                <td>Tuần 2</td>
                            </tr>
                            <tr>
                                <td><strong>ACT-03</strong></td>
                                <td>Tài trợ 50% chi phí Baga Bulky & Áo mưa cao cấp cho 500 tài xế PT Hà Nội</td>
                                <td><span class="status-pill warning">P1 Med</span></td>
                                <td>Driver Comms & Ops</td>
                                <td>Tuần 2 - Tuần 3</td>
                            </tr>
                            <tr>
                                <td><strong>ACT-04</strong></td>
                                <td>Tối ưu UI gán đơn Shopee Reverse kèm bản đồ định vị chính xác</td>
                                <td><span class="status-pill warning">P1 Med</span></td>
                                <td>Product & SPX Lead</td>
                                <td>Tuần 3</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 6 / 8</span>
                </div>
            </div>

            <!-- SLIDE 7: VALUE REALIZATION -->
            <div class="slide">
                <div class="slide-header">
                    <h2>📈 5.1. Value Realization & ROI Transformation</h2>
                    <span class="brand-tag">EXPECTED IMPACT</span>
                </div>
                <div class="slide-body">
                    <table class="ops-table">
                        <thead>
                            <tr>
                                <th>Chỉ Số Vận Hành (KPI)</th>
                                <th>Hiện Trạng (Current)</th>
                                <th>Mục Tiêu Sau Chuyển Đổi</th>
                                <th>Tác Động Kinh Doanh (Business Impact)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Fulfillment Rate (HAN)</strong></td>
                                <td>75.8% (Surge 48.3%)</td>
                                <td><strong style="color: var(--success);">83.5% (Surge < 25%)</strong></td>
                                <td>Khôi phục +15,000 đơn hoàn thành/tháng tại Hà Nội.</td>
                            </tr>
                            <tr>
                                <td><strong>Tỷ lệ No-show CityZone</strong></td>
                                <td>32.2% (163 ca)</td>
                                <td><strong style="color: var(--success);">< 5.0% (Tự động Checkin)</strong></td>
                                <td>Triệt tiêu 100% khiếu nại sót đơn tính thưởng của tài xế.</td>
                            </tr>
                            <tr>
                                <td><strong>Retention Tân Binh NLM SGN</strong></td>
                                <td>65.15% (Sụt 718 tx)</td>
                                <td><strong style="color: var(--success);">72.0% (+6.85% MoM)</strong></td>
                                <td>Giữ chân +500 tài xế active, giảm chi phí tuyển dụng mới.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 7 / 8</span>
                </div>
            </div>

            <!-- SLIDE 8: 60-SEC EXECUTIVE STORYLINE -->
            <div class="slide">
                <div class="slide-header">
                    <h2>🎙️ 60-Second BOD Executive Storyline</h2>
                    <span class="brand-tag">MANAGEMENT BRIEF</span>
                </div>
                <div class="slide-body">
                    <div class="bento-card highlight" style="height: 100%;">
                        <div class="kpi-title">🏆 TÓM TẮT DÀNH CHO BAN GIÁM ĐỐC (PYRAMID PRINCIPLE)</div>
                        <div style="font-size: 0.95rem; line-height: 1.6; color: var(--text-dark); display: flex; flex-direction: column; gap: 1rem; margin-top: 0.5rem;">
                            <div>
                                <strong>1. Điểm Khởi Sắc:</strong> Tuân thủ tiêu chuẩn vận hành toàn quốc (Compliance True Rate) đạt kỷ lục mới <strong>74.15%</strong>; SGN giữ vững chất lượng dịch vụ ở mức tối đa (Good Driver Rate 96.51%).
                            </div>
                            <div>
                                <strong>2. Điểm Nghẽn Cốt Lõi:</strong> Nguồn cung Hà Nội trong ca cao điểm thiếu hụt làm FR sụt về <strong>75.8%</strong>; sự cố thao tác Check-in thủ công tại CityZone Hub gây lãng phí 25.6% lượng đơn.
                            </div>
                            <div>
                                <strong>3. Quyết Định Đề Xuất:</strong> Phê duyệt ngay giải pháp <strong>Geofencing Auto-Checkin</strong> cho Hub và mở rộng <strong>hạn mức COD linh hoạt 15M</strong> cho tài xế Tân binh trong tuần tới.
                            </div>
                        </div>
                    </div>
                </div>
                <div class="slide-footer">
                    <span>Ahamove Operations Report 2026</span>
                    <span>Slide 8 / 8</span>
                </div>
            </div>

        </div>
    </div>

    <!-- Floating Navigation Controls -->
    <div class="controls">
        <button class="btn-ctrl" onclick="prevSlide()">◀ Trước</button>
        <span id="slideIndicator" style="color: #FFF; font-size: 0.8rem; display: flex; align-items: center; font-weight: 700;">1 / 8</span>
        <button class="btn-ctrl" onclick="nextSlide()">Sau ▶</button>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const indicator = document.getElementById('slideIndicator');

        function showSlide(index) {
            slides.forEach((s, i) => {
                s.classList.toggle('active', i === index);
            });
            currentSlide = index;
            indicator.textContent = `${currentSlide + 1} / ${slides.length}`;
        }

        function nextSlide() {
            if (currentSlide < slides.length - 1) showSlide(currentSlide + 1);
        }

        function prevSlide() {
            if (currentSlide > 0) showSlide(currentSlide - 1);
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        });

        // Initialize Charts when DOM loaded
        window.addEventListener('load', () => {
            // Chart 1: FR Chart
            const ctx1 = document.getElementById('frChart').getContext('2d');
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['SGN', 'Toàn Quốc (NW)', 'Chỉ Tiêu Target', 'HAN Ca Cao Điểm'],
                    datasets: [{
                        label: 'Fulfillment Rate (%)',
                        data: [86.2, 81.38, 85.0, 75.8],
                        backgroundColor: ['#10B981', '#0E4174', '#94A3B8', '#EF4444'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { min: 60, max: 100 } }
                }
            });

            // Chart 2: Churn Chart
            const ctx2 = document.getElementById('churnChart').getContext('2d');
            new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: ['Chi phí xăng/Thu nhập (44%)', 'Lỗi App/Chưa quen COD (31%)', 'Chuyển sang đối thủ (25%)'],
                    datasets: [{
                        data: [316, 222, 180],
                        backgroundColor: ['#EF4444', '#F59E0B', '#64748B']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } } }
                }
            });

            // Chart 3: CityZone Chart
            const ctx3 = document.getElementById('cityzoneChart').getContext('2d');
            new Chart(ctx3, {
                type: 'pie',
                data: {
                    labels: ['Check-in hợp lệ (67.8%)', 'No-show thực sự (19.6%)', 'No-show ẢO (Vẫn chạy đơn: 12.6%)'],
                    datasets: [{
                        data: [343, 99, 64],
                        backgroundColor: ['#10B981', '#EF4444', '#FF7F32']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } } }
                }
            });
        });
    </script>
</body>
</html>
"""

output_path = "/Users/ts-1148/Desktop/Pulu-workspace/Output/Ahamove/04. OPS_METRICS/ahamove_master_ops_performance_report-169-slides.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully created Master Visual Slide Deck at: {output_path}")
