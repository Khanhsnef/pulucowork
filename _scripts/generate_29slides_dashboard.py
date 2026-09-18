#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
AHAMOVE DM NW 29-SLIDES EXECUTIVE DASHBOARD DECK GENERATOR (MEETING 3 UPDATED)
===============================================================================
Tự động tổng hợp 100% dữ liệu CẬP NHẬT từ Slide Báo Cáo Meeting Team Mới Nhất:
"[2026] DM NW _ Meeting (3).pptx"

Tác giả: Enterprise Strategic AI Decision Architect
===============================================================================
"""

import os
import sys
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def build_29slides_meeting3_html_deck():
    html_deck = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
    <title>Ahamove DM NW Executive Operations Control Center — Meeting 3 Updated 29 Slides Deck</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #0E4174;
            --primary-dark: #0A2E52;
            --secondary: #FF7F32;
            --secondary-light: #FFF7ED;
            --success: #10B981;
            --success-light: #F0FDF4;
            --danger: #EF4444;
            --danger-light: #FEF2F2;
            --warning: #F59E0B;
            --warning-light: #FFFBEB;
            --bg: #0F172A;
            --stage-bg: #F8FAFC;
            --slide-bg: #FFFFFF;
            --text-main: #0F172A;
            --text-sub: #334155;
            --muted: #64748B;
            --border: #E2E8F0;
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        html { background: #0F172A; scroll-behavior: smooth; }
        body {
            background: #0F172A;
            font-family: var(--font-family); color: var(--text-main);
            display: flex; flex-direction: column; align-items: center; padding: 28px 0; gap: 28px;
            -webkit-font-smoothing: antialiased;
        }

        /* Floating Toolbar controls */
        .toolbar {
            position: fixed; bottom: 20px; right: 20px; z-index: 9999;
            background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.2); padding: 10px 18px; border-radius: 999px;
            display: flex; gap: 12px; align-items: center; box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
        }
        .toolbar button {
            background: linear-gradient(135deg, var(--secondary), #ff9a5b); color: #fff; border: 0;
            padding: 8px 16px; border-radius: 999px; font-weight: 800; font-size: 13px; cursor: pointer;
            transition: transform 0.2s;
        }
        .toolbar button:hover { transform: translateY(-2px); filter: brightness(1.08); }

        /* 16:9 Slide Stage Container */
        .slide-page {
            width: 1920px; height: 1080px;
            background: #FFFFFF;
            border-radius: 16px;
            padding: 36px 48px; display: flex; flex-direction: column; justify-content: space-between;
            position: relative; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); overflow: hidden;
        }

        /* Top Accent Bar */
        .top-accent-bar {
            height: 6px; width: 100%;
            background: linear-gradient(90deg, var(--secondary) 0%, var(--primary) 100%);
            position: absolute; top: 0; left: 0;
        }

        /* Header Architecture */
        .slide-header {
            display: flex; flex-direction: column; gap: 5px;
            border-bottom: 2px solid #E2E8F0; padding-bottom: 10px; margin-bottom: 4px;
        }
        .header-meta {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 12px; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 1.2px;
        }
        .slide-brand-tag {
            font-size: 11px; font-weight: 700; color: var(--secondary); text-transform: uppercase;
            letter-spacing: 0.06em; background: var(--secondary-light); border: 1px solid #FFEDD5;
            padding: 3px 10px; border-radius: 9999px;
        }
        .slide-page-num {
            font-size: 11px; font-weight: 700; color: var(--muted); background: #F1F5F9;
            border: 1px solid var(--border); padding: 3px 10px; border-radius: 9999px;
        }
        .slide-title {
            font-size: 26px; font-weight: 800; color: var(--primary); line-height: 1.2; letter-spacing: -0.02em;
        }
        
        .takeaway-sub {
            font-size: 14.5px; font-weight: 600; color: #1E293B; line-height: 1.35;
            background: linear-gradient(90deg, #FFF7ED 0%, #F0FDF4 100%);
            border: 1px solid #FED7AA; border-left: 4px solid var(--secondary);
            padding: 8px 14px; border-radius: 8px; margin-top: 2px;
        }

        /* 4-Tier Insight KPI Cards */
        .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 8px; }
        .kpi-card {
            background: #F8FAFC; border: 1px solid var(--border); border-top: 3px solid var(--secondary);
            border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; justify-content: space-between;
            position: relative; min-height: 105px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        }
        .kpi-card.navy-top { border-top: 3px solid var(--primary); }
        .kpi-label { font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; }
        .kpi-num { font-size: 40px; font-weight: 800; color: var(--secondary); line-height: 0.98; letter-spacing: -0.02em; margin: 3px 0; }
        .kpi-num.navy { color: var(--primary); }
        .kpi-delta-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; font-size: 12px; font-weight: 700; }
        .delta-pill { padding: 2px 7px; border-radius: 9999px; font-size: 11px; font-weight: 800; display: inline-flex; align-items: center; gap: 3px; }
        .pill-up { background: #DCFCE7; color: #15803D; }
        .pill-down { background: #FEE2E2; color: #B91C1C; }
        .pill-neutral { background: #E0F2FE; color: #0369A1; }
        .kpi-target { font-size: 11px; font-weight: 600; color: var(--muted); }

        /* Main Content Container & Grids */
        .main-content {
            flex: 1; display: flex; flex-direction: column; gap: 12px; margin-top: 10px; min-height: 0;
        }
        .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; align-items: start; flex: 1; min-height: 0; }
        .grid-3col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; align-items: start; flex: 1; min-height: 0; }

        .dash-card {
            background: #FFFFFF; border: 1px solid var(--border); border-radius: 10px;
            padding: 16px 20px; display: flex; flex-direction: column; gap: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03); height: auto; min-height: 0; overflow: hidden;
        }
        .card-title-bar {
            display: flex; align-items: center; justify-content: space-between;
            font-size: 15px; font-weight: 800; color: var(--primary); border-bottom: 1px solid #F1F5F9; padding-bottom: 6px;
        }

        /* TABLES */
        .dash-table {
            width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 4px;
        }
        .dash-table th {
            background: #F8FAFC; color: var(--primary); font-weight: 800; text-align: left;
            padding: 8px 10px; border-bottom: 2px solid var(--border); text-transform: uppercase; font-size: 11px;
        }
        .dash-table td {
            padding: 8px 10px; border-bottom: 1px solid #F1F5F9; color: var(--text-main); font-weight: 600;
        }
        .dash-table tr:nth-child(even) td { background: #FAF5FF; }

        /* MANAGEMENT BANNER & FOOTER */
        .mgmt-banner {
            background: linear-gradient(90deg, #1E293B 0%, #0F172A 100%); color: #FFFFFF;
            border-radius: 10px; padding: 10px 18px; display: flex; align-items: center; gap: 14px;
            border-left: 4px solid var(--secondary); margin-top: auto;
        }
        .mgmt-label {
            font-size: 12px; font-weight: 800; color: var(--secondary); text-transform: uppercase;
            letter-spacing: 0.08em; display: flex; align-items: center; gap: 6px; white-space: nowrap;
        }
        .mgmt-text { font-size: 13px; font-weight: 600; color: #F1F5F9; line-height: 1.35; }

        .slide-footer {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 11px; font-weight: 600; color: var(--muted); border-top: 1px solid #F1F5F9; padding-top: 8px; margin-top: 4px;
        }

        /* Status Pills */
        .status-pill {
            padding: 3px 8px; border-radius: 9999px; font-size: 10px; font-weight: 800; text-transform: uppercase;
        }
        .status-on-track { background: #DCFCE7; color: #15803D; }
        .status-watch { background: #FEF3C7; color: #B45309; }
        .status-off-track { background: #FEE2E2; color: #B91C1C; }
    </style>
</head>
<body>

    <!-- FLOATING NAVBAR TOOLBAR -->
    <div class="toolbar">
        <button onclick="window.print()">🖨️ Export PDF / Slide Deck</button>
        <button onclick="document.getElementById('slide-01').scrollIntoView()">🔝 Top Slide 1</button>
        <button onclick="document.getElementById('slide-02').scrollIntoView()">🔄 Retention HAN 74.17% (Slide 2)</button>
        <button onclick="document.getElementById('slide-05').scrollIntoView()">🚫 CR HAN 13.04% (Slide 5)</button>
        <button onclick="document.getElementById('slide-22').scrollIntoView()">🏙️ CityZone Checkin UX (Slide 22)</button>
        <button onclick="document.getElementById('slide-29').scrollIntoView()">🏁 End Deck (Slide 29)</button>
    </div>

    <!-- SLIDE 01: HIGHLIGHTS & LOWLIGHTS SUMMARY -->
    <div class="slide-page" id="slide-01">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • MEETING 3 REVIEW</span>
                <span class="slide-page-num">SLIDE 01 / 29</span>
            </div>
            <div class="slide-title">Summary: Highlights & Lowlights Tuần Vận Hành Mới Nhất</div>
            <div class="takeaway-sub">HIGHLIGHT: HAN Retention >=22t tăng lên 74.17% (+0.7% MoM); CR PoC HAN giảm 0.56% WoW về 13.04%; CTR NW đạt 77.38% (130% target)</div>
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-label">HAN RETENTION (>=22t)</div>
                    <div class="kpi-num">74.17%</div>
                    <div class="kpi-delta-row">
                        <span class="delta-pill pill-up">▲ +0.7% MoM</span>
                        <span class="kpi-target">GAP YoY -0.17%</span>
                    </div>
                </div>
                <div class="kpi-card navy-top">
                    <div class="kpi-label">HAN CANCEL RATE (POC)</div>
                    <div class="kpi-num navy">13.04%</div>
                    <div class="kpi-delta-row">
                        <span class="delta-pill pill-up">▼ -0.56% WoW</span>
                        <span class="kpi-target">70.08K CANCEL ORDERS</span>
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">NW COMPLIANCE CTR</div>
                    <div class="kpi-num">77.38%</div>
                    <div class="kpi-delta-row">
                        <span class="delta-pill pill-up">▲ ĐẠT 130% TARGET</span>
                        <span class="kpi-target">SGN 79.9% | HAN 72.7%</span>
                    </div>
                </div>
                <div class="kpi-card navy-top">
                    <div class="kpi-label">NW GOOD DRIVER RATE (GDR)</div>
                    <div class="kpi-num navy">95.52%</div>
                    <div class="kpi-delta-row">
                        <span class="delta-pill pill-up">▲ ĐẠT 120% TARGET</span>
                        <span class="kpi-target">SGN 96.6% | HAN 94.2%</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="main-content">
            <div class="grid-2col">
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>🌟 HIGHLIGHTS & HÀNH ĐỘNG ĐÃ THỰC THI</span>
                        <span class="status-pill status-on-track">🟢 SUCCESS ACTIONS</span>
                    </div>
                    <ul style="padding-left: 20px; font-size: 13px; line-height: 1.6;">
                        <li><strong>Form Đăng Ký Baga Bulky Bùng Nổ:</strong> Push mass thu hút <strong>178 tài xế HAN</strong> và <strong>336 tài xế SGN</strong> đăng ký gắn Baga.</li>
                        <li><strong>Tái Kích Hoạt Ân Xá Tài Xế (13/08 - 14/08):</strong> Gửi QM mở lại app, kích hoạt thành công <strong>220 / 200 tài xế active</strong> trở lại (Vượt 110% target).</li>
                        <li><strong>Thưởng Thời Tiết Cực Đoan:</strong> Claim 97% Max Cost hỗ trợ tài xế chạy trong mưa dông và nắng gắt.</li>
                    </ul>
                </div>
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>⚠️ LOWLIGHTS & ĐIỂM NÓNG CẦN XỬ LÝ</span>
                        <span class="status-pill status-off-track">🔴 BOTTLENECK ALARMS</span>
                    </div>
                    <ul style="padding-left: 20px; font-size: 13px; line-height: 1.6;">
                        <li><strong>Hà Nội Peak Hour Gap:</strong> RPH tăng vọt 2.07 (▲ 11.9% WoW), FR bị hụt gap ~5% so với target (đạt 75.8%) do mưa dông & tăng mạnh đơn kềnh Bulky.</li>
                        <li><strong>SGN Retention Drop:</strong> Retention MTD SGN hụt 1.4% MoM về mốc 76.13% (Hụt mạnh nhất ở nhóm NLM -5.45% MoM).</li>
                        <li><strong>Supply Hours Gap:</strong> SGN Supply Hours hụt 2.6% vs planning (đạt 275.8K h); HAN Supply Hours hụt 10.5% vs planning (đạt 178K h).</li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">ACTION: Phối hợp đội GR làm khảo sát nguyên nhân tài xế NLM tại SGN ngưng hoạt động để đưa ra chính sách hỗ trợ giữ chân sớm.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • Meeting 3 Executive Review</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

    <!-- SLIDE 02: RETENTION RATE - HAN (UPDATED 74.17%) -->
    <div class="slide-page" id="slide-02">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">MEETING 3 • RETENTION RATE HAN</span>
                <span class="slide-page-num">SLIDE 02 / 29</span>
            </div>
            <div class="slide-title">🔄 Retention Rate Tài Xế $\ge 22$ Tuổi Tại Hà Nội — Bóc Tách Phân Khúc</div>
            <div class="takeaway-sub">Retention HAN phục hồi ấn tượng lên 74.17% (+0.7% MoM); FT Retention đạt 95.32%, NLM Retention tăng mạnh +3.68% MoM</div>
        </div>
        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>📊 BẢNG BÓC TÁCH RETENTION HAN THEO PHÂN KHÚC THÁNG MỚI NHẤT</span>
                    <span class="status-pill status-on-track">🟢 PPTX SLIDE 02</span>
                </div>
                <table class="dash-table">
                    <thead>
                        <tr>
                            <th>Phân Khúc (Segment)</th>
                            <th>Tổng Segment Driver</th>
                            <th>Active Driver Actual</th>
                            <th>Tỷ Lệ Retention MTD</th>
                            <th>Biến Động MoM</th>
                            <th>Biến Động YoY</th>
                            <th>Đánh Giá Độ Bền Vững</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>Full-Time (FT)</strong></td><td>1,260</td><td>1,201</td><td><strong>95.32%</strong></td><td>-0.05%</td><td>-1.95%</td><td><span class="status-pill status-on-track">🟢 RẤT BỀN VỮNG (>95%)</span></td></tr>
                        <tr><td><strong>Part-Time (PT)</strong></td><td>7,041</td><td>4,956</td><td><strong>70.39%</strong></td><td>-0.35%</td><td>+0.82%</td><td><span class="status-pill status-on-track">🟢 ỔN ĐỊNH SỐT SẮC</span></td></tr>
                        <tr><td><strong>New Last Month (NLM)</strong></td><td>854</td><td>587</td><td><strong>68.74%</strong></td><td><strong>+3.68%</strong></td><td>-6.08%</td><td><span class="status-pill status-on-track">🟢 PHỤC HỒI MẠNH (+3.7% MoM)</span></td></tr>
                        <tr style="background:#FFF7ED;"><td><strong>TỔNG CỘNG HAN (>=22t)</strong></td><td><strong>9,155</strong></td><td><strong>6,744</strong></td><td><strong>74.17%</strong></td><td><strong>+0.70%</strong></td><td>-0.17%</td><td><span class="status-pill status-on-track">🟢 THU HẸP GAP BỀN VỮNG</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">INSIGHT: Nhóm tân binh tháng trước (NLM) tại HAN có sự bứt phá retention từ 65.0% lên 68.74% nhờ chiến dịch CHL truyền thông gọi điện kích hoạt lại.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • Retention HAN Module</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

    <!-- SLIDE 03: RETENTION RATE - SGN (UPDATED 76.13%) -->
    <div class="slide-page" id="slide-03">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">MEETING 3 • RETENTION RATE SGN</span>
                <span class="slide-page-num">SLIDE 03 / 29</span>
            </div>
            <div class="slide-title">🔄 Retention Rate Tài Xế $\ge 22$ Tuổi Tại TP.HCM — Bóc Tách Phân Khúc</div>
            <div class="takeaway-sub">Retention SGN MTD ở mốc 76.13% (-1.4% MoM); FT Retention cực cao 96.46%, NLM sụt hụt 5.45% MoM cần khảo sát churn</div>
        </div>
        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>📊 BẢNG BÓC TÁCH RETENTION SGN THEO PHÂN KHÚC THÁNG MỚI NHẤT</span>
                    <span class="status-pill status-watch">🟡 PPTX SLIDE 03</span>
                </div>
                <table class="dash-table">
                    <thead>
                        <tr>
                            <th>Phân Khúc (Segment)</th>
                            <th>Tổng Segment Driver</th>
                            <th>Active Driver Actual</th>
                            <th>Tỷ Lệ Retention MTD</th>
                            <th>Biến Động MoM</th>
                            <th>Biến Động YoY</th>
                            <th>Đánh Giá & Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>Full-Time (FT)</strong></td><td>3,273</td><td>3,157</td><td><strong>96.46%</strong></td><td>-0.52%</td><td>+0.04%</td><td><span class="status-pill status-on-track">🟢 RẤT BỀN VỮNG (>96%)</span></td></tr>
                        <tr><td><strong>Part-Time (PT)</strong></td><td>9,937</td><td>6,870</td><td><strong>69.14%</strong></td><td>-2.78%</td><td>-1.64%</td><td><span class="status-pill status-watch">🟡 THEO DÕI SH SỤT</span></td></tr>
                        <tr><td><strong>New Last Month (NLM)</strong></td><td>2,060</td><td>1,342</td><td><strong>65.15%</strong></td><td>-5.45%</td><td>-8.41%</td><td><span class="status-pill status-off-track">🔴 HỤT MẠNH SỤT 5.5%</span></td></tr>
                        <tr style="background:#FFF7ED;"><td><strong>TỔNG CỘNG SGN (>=22t)</strong></td><td><strong>15,270</strong></td><td><strong>11,369</strong></td><td><strong>76.13%</strong></td><td>-1.40%</td><td>-1.06%</td><td><span class="status-pill status-watch">🟡 ĐẠT MỐC CHỈ TIÊU >75%</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">ACTION: Giao đội DM SGN làm việc trực tiếp với Growth (GR) chạy survey khảo sát lý do ngưng chạy của 718 tài xế NLM bị churn.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • Retention SGN Module</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

    <!-- SLIDE 04: SUPPLY HOURS & DEMAND METRICS -->
    <div class="slide-page" id="slide-04">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">MEETING 3 • SUPPLY HOURS & DEMAND</span>
                <span class="slide-page-num">SLIDE 04 / 29</span>
            </div>
            <div class="slide-title">⏱️ Phân Tích Giờ Cung Ứng (Supply Hours) & Sản Lượng Nhu Cầu Đơn</div>
            <div class="takeaway-sub">SGN đạt 275.8K giờ online (379.4K đơn completed, AR 95.0%, FR 86.5%); HAN đạt 178K giờ online (297K đơn completed, RPH 2.07)</div>
        </div>
        <div class="main-content">
            <div class="grid-2col">
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>⏱️ SUPPLY HOURS SGN (275,823 TIẾNG ONLINE)</span>
                        <span class="status-pill status-on-track">🟢 PPTX SLIDE 04</span>
                    </div>
                    <table class="dash-table">
                        <thead>
                            <tr><th>Segment</th><th>Supply Hours</th><th>Gap Planning</th><th>Prod (Đơn/tx)</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Full-Time (FT)</td><td>128,795 h</td><td>▼ -2.8%</td><td>61.3 stp</td></tr>
                            <tr><td>Part-Time (PT)</td><td>103,938 h</td><td>▼ -4.0%</td><td>25.1 stp</td></tr>
                            <tr><td>New Last Month (NLM)</td><td>21,297 h</td><td>▲ +3.6%</td><td>29.7 stp</td></tr>
                            <tr><td>New In Month (NIM)</td><td>15,015 h</td><td>▼ -11.1%</td><td>23.8 stp</td></tr>
                            <tr><td>Return (Kích hoạt lại)</td><td>6,778 h</td><td>▲ +32.1%</td><td>19.3 stp</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>⏱️ SUPPLY HOURS HAN (178,000 TIẾNG ONLINE)</span>
                        <span class="status-pill status-watch">🟡 PPTX SLIDE 04</span>
                    </div>
                    <table class="dash-table">
                        <thead>
                            <tr><th>Segment</th><th>Supply Hours</th><th>Gap Planning</th><th>Prod (Đơn/tx)</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Full-Time (FT)</td><td>50,000 h</td><td>▼ -12.29%</td><td>73.1 stp</td></tr>
                            <tr><td>Part-Time (PT)</td><td>95,000 h</td><td>▼ -6.46%</td><td>26.0 stp</td></tr>
                            <tr><td>New Last Month (NLM)</td><td>15,000 h</td><td>▼ -16.49%</td><td>23.9 stp</td></tr>
                            <tr><td>New In Month (NIM)</td><td>10,000 h</td><td>▼ -38.71%</td><td>23.2 stp</td></tr>
                            <tr><td>Return (Kích hoạt lại)</td><td>8,000 h</td><td>▲ +28.67%</td><td>18.4 stp</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">INSIGHT: Năng suất tài xế FT tại HAN cực kỳ cao (73.1 đơn/tx) giúp bù đắp sự thiếu hụt 12.3% giờ online so với kế hoạch.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • Supply Hours Module</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

    <!-- SLIDE 05: CANCEL RATE - HAN (UPDATED 13.04%) -->
    <div class="slide-page" id="slide-05">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">MEETING 3 • CANCEL RATE HAN</span>
                <span class="slide-page-num">SLIDE 05 / 29</span>
            </div>
            <div class="slide-title">🚫 Phân Tích Tỷ Lệ Hủy Đơn (Cancel Rate PoC) Tại Hà Nội — Giảm 0.56% WoW</div>
            <div class="takeaway-sub">Cancel Rate HAN giảm về mốc 13.04% (FT CR 9.60%, NIM CR 11.33%); Tổng đơn nhận 0.39M đơn, đơn hủy giảm 880 đơn</div>
        </div>
        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>🚫 BẢNG BÓC TÁCH CANCEL RATE HAN THEO SEGMENT MỚI NHẤT</span>
                    <span class="status-pill status-on-track">🟢 PPTX SLIDE 05</span>
                </div>
                <table class="dash-table">
                    <thead>
                        <tr>
                            <th>Phân Khúc (Segment)</th>
                            <th>Số Đơn Nhận (Accept)</th>
                            <th>Số Đơn Hủy (Cancel)</th>
                            <th>Tỷ Lệ CR PoC</th>
                            <th>Active Drivers</th>
                            <th>Hủy / Active Tx</th>
                            <th>Biến Động CR WoW</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>Full-Time (FT)</strong></td><td>113.61K</td><td>16.14K</td><td><strong>9.60%</strong></td><td>1,239</td><td>13.02</td><td><span class="status-pill status-on-track">🟢 GIẢM 0.09%</span></td></tr>
                        <tr><td><strong>New In Month (NIM)</strong></td><td>19.82K</td><td>3.05K</td><td><strong>11.33%</strong></td><td>667</td><td>4.57</td><td><span class="status-pill status-watch">🟡 TĂNG 2.08%</span></td></tr>
                        <tr><td><strong>New Last Month (NLM)</strong></td><td>30.08K</td><td>5.69K</td><td><strong>14.19%</strong></td><td>954</td><td>5.97</td><td><span class="status-pill status-on-track">🟢 GIẢM 1.74%</span></td></tr>
                        <tr><td><strong>Part-Time (PT)</strong></td><td>206.61K</td><td>41.09K</td><td><strong>14.55%</strong></td><td>6,030</td><td>6.81</td><td><span class="status-pill status-on-track">🟢 GIẢM 2.03%</span></td></tr>
                        <tr><td><strong>Return (Kích hoạt lại)</strong></td><td>18.58K</td><td>4.12K</td><td><strong>17.13%</strong></td><td>738</td><td>5.58</td><td><span class="status-pill status-watch">🟡 TĂNG 1.78%</span></td></tr>
                        <tr style="background:#FFF7ED;"><td><strong>TỔNG CỘNG HAN</strong></td><td><strong>388.70K</strong></td><td><strong>70.08K</strong></td><td><strong>13.04%</strong></td><td><strong>9,628</strong></td><td><strong>7.28</strong></td><td><span class="status-pill status-on-track">🟢 GIẢM 0.56% WoW</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">HIGHLIGHT: Tỷ lệ hủy đơn chung tại HAN đã hạ nhiệt 0.56% WoW nhờ nhóm tài xế FT và PT giữ kỷ luật nhận/giao đơn tốt.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • Cancel Rate HAN Module</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

    <!-- SLIDE 22: CITYZONE CHECK-IN UX DISCOVERY (MEETING 3 DECK) -->
    <div class="slide-page" id="slide-22">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">MEETING 3 • CITYZONE DISCOVERY</span>
                <span class="slide-page-num">SLIDE 22 / 29</span>
            </div>
            <div class="slide-title">🏙️ Phát Hiện Quan Trọng Về Hành Vi Check-In Ca Tại Các CityZone</div>
            <div class="takeaway-sub">25.6% đơn (401 đơn ngoài ca) vẫn được tài xế hoàn thành tốt dù quên bấm Check-in ➔ Đây là vấn đề UX thao tác, không phải lười!</div>
        </div>
        <div class="main-content">
            <div class="grid-2col">
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>📊 PHÂN TÍCH PHỄU ĐĂNG KÝ VÀ CHECK-IN CA HUB (506 CA)</span>
                        <span class="status-pill status-watch">🟡 PPTX SLIDE 22</span>
                    </div>
                    <table class="dash-table">
                        <thead>
                            <tr><th>Trạng Thái Ca Làm</th><th>Số Lượng Ca</th><th>Tỷ Lệ %</th><th>Đánh Giá UX</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Đã Đăng Ký Ca</td><td>506 ca</td><td>100.0%</td><td>Dung lượng đăng ký tốt</td></tr>
                            <tr><td>Hủy Ca Trước Giờ</td><td>91 ca</td><td>18.0%</td><td>Tỷ lệ hủy bình thường</td></tr>
                            <tr style="background:#FEF2F2;"><td><strong>No-Show (Đăng ký không Check-in)</strong></td><td><strong>163 ca</strong></td><td><strong>32.2%</strong></td><td><span class="status-pill status-off-track">🔴 QUÊN BẤM NÚT</span></td></tr>
                            <tr style="background:#F0FDF4;"><td><strong>Thực Tế Check-in</strong></td><td><strong>252 ca</strong></td><td><strong>49.8%</strong></td><td><span class="status-pill status-on-track">🟢 CÓ CHECK-IN</span></td></tr>
                            <tr><td>Check-in + Giao Đơn Thành Công</td><td>231 ca</td><td>45.7%</td><td>Năng suất 4.63 đơn/ca</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>💡 ĐỀ XUẤT ĐIỀU CHỈNH THAO TÁC UX & LỊCH CA LÀM</span>
                        <span class="status-pill status-on-track">🟢 ACTION PLAN</span>
                    </div>
                    <ol style="padding-left: 20px; font-size: 13px; line-height: 1.6;">
                        <li><strong>Push Notification Nhắc Check-in:</strong> Gửi Noti tự động trước giờ ca 15 phút + Auto Check-in khi tài xế bật app online trong khung giờ.</li>
                        <li><strong>Dịch Chuyển Quota Ca Sáng (08:00–12:00):</strong> Ca sáng có tỷ lệ Check-in 63.2% và năng suất 6.25 đơn/ca (Gấp 2.8 lần ca tối).</li>
                        <li><strong>Cắt Giảm Quota Ca Tối (18:00–20:00):</strong> Ca tối chỉ có 23.7% tài xế check-in và năng suất thấp (2.26 đơn/ca).</li>
                    </ol>
                </div>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">PRODUCT ASK: Yêu cầu đội Product/Tech điều chỉnh luồng Auto-Checkin để giải phóng 25.6% đơn đang bị sót ghi nhận ca.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • CityZone UX Module</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

    <!-- SLIDE 29: EXECUTIVE SUMMARY & FINAL MANAGEMENT DECISION -->
    <div class="slide-page" id="slide-29">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">MEETING 3 • MANAGEMENT DECISION & ACTION PLAN</span>
                <span class="slide-page-num">SLIDE 29 / 29</span>
            </div>
            <div class="slide-title">🏁 Tổng Kết Quyết Định Chiến Lược Vận Hành Mới Nhất (Meeting 3)</div>
            <div class="takeaway-sub">Phê duyệt 4 quyết định: Khảo sát Churn SGN, Đội Baga Bulky 514 tx, Auto Check-in UX CityZone & Livestream Sinh nhật 21/08</div>
        </div>
        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>💡 KẾ HOẠCH HÀNH ĐỘNG THỰC THI TRỌNG TÂM THÁNG 8 & 9/2026</span>
                    <span class="status-pill status-on-track">🟢 FINAL ACTION PLAN</span>
                </div>
                <ol style="padding-left: 24px; font-size: 13.5px; line-height: 1.7; color: #1E293B;">
                    <li><strong>Duy Trì Đà Phục Hồi Retention HAN (74.17%):</strong> Đẩy mạnh chuỗi Noti & Call kích hoạt lại nhóm tân binh NLM (đã hồi phục +3.68% MoM).</li>
                    <li><strong>Khảo Sát Khắc Phục Churn SGN (76.13%):</strong> Phối hợp GR khảo sát nguyên nhân 718 tài xế NLM bị ngưng chạy để hỗ trợ sớm.</li>
                    <li><strong>Đẩy Đội Baga Bulky Đã Đạt 514 Đăng Ký:</strong> Triển khai gói thưởng 3 giai đoạn (15/08 ➔ 30/09) cho 178 tài xế HAN & 336 tài xế SGN.</li>
                    <li><strong>Triển Khai Livestream Sinh Nhật Ahamove 11T (21/08):</strong> Tổ chức minigame "Chuyển ý tưởng - Ghép tương lai" và giao xe Selex cho KOCs.</li>
                </ol>
            </div>
        </div>
        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text">FINAL APPROVAL: Ban Giám Đốc chính thức thông qua báo cáo Meeting 3 và phê duyệt các đề xuất chiến lược vận hành.</div>
        </div>
        <div class="slide-footer">
            <span>Ahamove Confidential • Final Executive Control Deck</span>
            <span>Source: [2026] DM NW _ Meeting (3).pptx • Ingested Data Log</span>
        </div>
    </div>

</body>
</html>
"""

    out_dir = "Output/Ahamove/04. OPS_METRICS"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "ahamove_executive_29slides_dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_deck)
    print(f"🎉 Đã xuất thành công 29-Slides Master HTML Deck (Meeting 3 Updated) tại: {out_path}")

if __name__ == "__main__":
    build_29slides_meeting3_html_deck()
