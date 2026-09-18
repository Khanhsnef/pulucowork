#!/usr/bin/env python3
"""
Layout Engine & Insight Engine Module (src/layout_engine.py).
Implements the 12 Visual Modules & Layout Primitives for 29-slide generation:
  - Layout A: Executive Summary Dashboard
  - Layout B: KPI Deep Dive
  - Layout C: Regional Comparison (HAN vs SGN)
  - Layout D: Time Series & Trend Analysis
  - Layout E: Driver Funnel & Conversion (Registered -> Active -> Conversion)
  - Layout F: Zone Performance Heatmap & Governance Pulse
  - Layout G: Initiative & Milestone Roadmap Pipeline
  - Layout H: Driver Voice Mechanism (25% Quote | 45% Mechanism | 30% Success Criteria Framework)
  - Layout I: Amnesty & Operational Policy Flowchart
  - Layout J: EV Partnership & Charger Network Breakdown
"""

import re
from typing import Dict, List, Any


def render_layout_f_heatmap(sn: int, title: str, takeaway: str, total_count: int = 29) -> str:
    """Layout F — Zone Performance Heatmap (Slides 12-15)"""
    return f"""
    <div class="slide-page" id="slide-{sn}">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • 02 — ZONE HEATMAP</span>
                <span class="slide-page-num">SLIDE {sn:02d} / {total_count:02d}</span>
            </div>
            <div class="slide-title editable">{title}</div>
            <div class="takeaway-sub editable">Bản đồ nhiệt khu vực: Z6 & Z578 cần can thiệp gấp do Cancel Rate cao và Retention suy giảm</div>
        </div>

        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>🔥 ZONE PERFORMANCE HEATMAP MATRIX</span>
                    <span class="status-pill status-watch">🟡 HEATMAP AUDIT</span>
                </div>
                <table class="dash-table">
                    <thead>
                        <tr>
                            <th>Khu Vực (Zone)</th>
                            <th>Active Drivers</th>
                            <th>Retention Rate</th>
                            <th>Cancel Rate</th>
                            <th>Supply Hours</th>
                            <th>Trạng Thái Hub</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background: #F0FDF4;"><td>Zone 1 (Q.1 - HCM)</td><td>96%</td><td>72%</td><td>10.2%</td><td>98%</td><td><span class="status-pill status-on-track">🟢 ON TRACK</span></td></tr>
                        <tr style="background: #FFFBEB;"><td>Zone 2 (Q.3 - HCM)</td><td>94%</td><td>69%</td><td>12.5%</td><td>95%</td><td><span class="status-pill status-watch">🟡 WATCH</span></td></tr>
                        <tr style="background: #FEF2F2;"><td>Zone 6 (Q.Tân Bình)</td><td>93%</td><td>64%</td><td>15.8%</td><td>91%</td><td><span class="status-pill status-off-track">🔴 OFF TRACK</span></td></tr>
                        <tr style="background: #FEF2F2;"><td>Zone 578 (Long Biên - HN)</td><td>67%</td><td>61%</td><td>18.2%</td><td>85%</td><td><span class="status-pill status-off-track">🔴 OFF TRACK</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text editable">MANAGEMENT ATTENTION: Điều chuyển nhân sự hỗ trợ cắm chốt tại Zone 6 & Zone 578 để hạ Cancel Rate về dưới 12%.</div>
        </div>

        <div class="slide-footer">
            <span class="editable">Ahamove Confidential • Decision Architecture Suite</span>
            <span class="editable">Source: Slide {sn} • Ingested Data Log</span>
        </div>
    </div>
    """


def render_layout_e_funnel(sn: int, title: str, takeaway: str, total_count: int = 29) -> str:
    """Layout E — Driver Funnel & Conversion Matrix (Slide 17, Recruitment)"""
    return f"""
    <div class="slide-page" id="slide-{sn}">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • 03 — DRIVER FUNNEL</span>
                <span class="slide-page-num">SLIDE {sn:02d} / {total_count:02d}</span>
            </div>
            <div class="slide-title editable">{title}</div>
            <div class="takeaway-sub editable">HAN conversion đạt 90.6% nhưng Z578 bị rò rỉ 33.3% tài xế chưa Active</div>
        </div>

        <div class="main-content">
            <div class="grid-2col">
                <!-- Funnel Stage Card -->
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>🔻 CONVERSION FUNNEL LEAKAGE</span>
                        <span class="status-pill status-watch">🟡 FUNNEL LEAK</span>
                    </div>
                    <div class="funnel-container" style="display: flex; flex-direction: column; gap: 10px; margin-top: 6px;">
                        <div class="funnel-stage" style="background: rgba(14,65,116,0.08); border-left: 4px solid #0E4174; padding: 10px 14px; border-radius: 6px;">
                            <div style="font-size: 11px; font-weight: 800; color: #64748B;">STAGE 1: REGISTERED DRIVERS</div>
                            <div style="font-size: 26px; font-weight: 900; color: #0E4174;">245 TX <span style="font-size: 13px; color: #64748B;">(100%)</span></div>
                        </div>
                        <div style="text-align: center; font-weight: 900; color: #FF7F32; font-size: 15px;">↓ 90.6% Active Rate</div>
                        <div class="funnel-stage" style="background: rgba(16,185,129,0.08); border-left: 4px solid #10B981; padding: 10px 14px; border-radius: 6px;">
                            <div style="font-size: 11px; font-weight: 800; color: #64748B;">STAGE 2: ACTIVE DRIVERS</div>
                            <div style="font-size: 26px; font-weight: 900; color: #10B981;">222 TX <span style="font-size: 13px; color: #10B981;">(ACTIVE)</span></div>
                        </div>
                        <div style="text-align: center; font-weight: 900; color: #EF4444; font-size: 13.5px;">⚠️ 23 TX NOT ACTIVE (Rò Rỉ Nguồn Cung)</div>
                    </div>
                </div>

                <!-- Zone Ranking Matrix -->
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>🎯 ZONE CONVERSION RANKING</span>
                        <span class="status-pill status-on-track">🟢 ZONE RANKING</span>
                    </div>
                    <div class="progress-list" style="margin-top: 4px;">
                        <div class="progress-item">
                            <div class="progress-meta"><span>Z578 (Long Biên)</span><span style="color:#EF4444;">66.7% 🔴</span></div>
                            <div class="progress-track"><div class="progress-fill red" style="width: 66.7%;"></div></div>
                        </div>
                        <div class="progress-item">
                            <div class="progress-meta"><span>Z24 (Bắc Từ Liêm)</span><span style="color:#F59E0B;">78.6% 🟡</span></div>
                            <div class="progress-track"><div class="progress-fill orange" style="width: 78.6%;"></div></div>
                        </div>
                        <div class="progress-item">
                            <div class="progress-meta"><span>TX (Thanh Xuân)</span><span style="color:#10B981;">91.7% 🟢</span></div>
                            <div class="progress-track"><div class="progress-fill green" style="width: 91.7%;"></div></div>
                        </div>
                        <div class="progress-item">
                            <div class="progress-meta"><span>BIGZONE (TP.HCM)</span><span style="color:#10B981;">94.7% 🟢</span></div>
                            <div class="progress-track"><div class="progress-fill green" style="width: 94.7%;"></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text editable">DECISION NEEDED: Tập trung push noti và đội hỗ trợ trực tiếp tại Z578 để xử lý 33.3% tài xế chưa active.</div>
        </div>

        <div class="slide-footer">
            <span class="editable">Ahamove Confidential • Decision Architecture Suite</span>
            <span class="editable">Source: Slide {sn} • Ingested Data Log</span>
        </div>
    </div>
    """


def render_layout_g_initiative_roadmap(sn: int, title: str, takeaway: str, total_count: int = 29) -> str:
    """Layout G — Milestone Timeline & Project Roadmap (Slide 16 Baga Bulky)"""
    chart_id = f"chart_slide_{sn}"
    return f"""
    <div class="slide-page" id="slide-{sn}">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • 03 — INITIATIVE ROADMAP</span>
                <span class="slide-page-num">SLIDE {sn:02d} / {total_count:02d}</span>
            </div>
            <div class="slide-title editable">{title}</div>
            <div class="takeaway-sub editable">Dự án Baga Bulky Phase 1: 514 tài xế tham gia (HAN 178 TX | SGN 336 TX), đúng tiến độ hoàn ứng 30/8</div>
        </div>

        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>🗓️ PROJECT MILESTONE TIMELINE</span>
                    <span class="status-pill status-done">🔵 ON SCHEDULE</span>
                </div>
                <div class="milestone-timeline">
                    <div class="milestone-box" style="border-top: 3px solid #10B981;">
                        <div class="milestone-date">23 JUL</div>
                        <div class="milestone-title">1. PREP & REGISTRATION</div>
                        <div style="font-size: 11px; color: #64748B;">Mở cổng đăng ký Baga</div>
                    </div>
                    <div class="milestone-box" style="border-top: 3px solid #10B981;">
                        <div class="milestone-date">03 AUG</div>
                        <div class="milestone-title">2. INSTALLATION</div>
                        <div style="font-size: 11px; color: #64748B;">Lắp đặt Baga chuẩn</div>
                    </div>
                    <div class="milestone-box" style="border-top: 3px solid #FF7F32;">
                        <div class="milestone-date">15 AUG</div>
                        <div class="milestone-title">3. LIVE VERIFICATION</div>
                        <div style="font-size: 11px; color: #64748B;">Xác minh ảnh chạy ca</div>
                    </div>
                    <div class="milestone-box" style="border-top: 3px solid #0E4174;">
                        <div class="milestone-date">30 AUG</div>
                        <div class="milestone-title">4. REIMBURSEMENT</div>
                        <div style="font-size: 11px; color: #64748B;">Hoàn ứng chi phí Baga</div>
                    </div>
                </div>
            </div>

            <div class="grid-chart-table">
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>📊 REGIONAL DRIVER ADOPTION</span>
                        <span class="status-pill status-on-track">🟢 514 DRIVERS TOTAL</span>
                    </div>
                    <div class="chart-wrapper"><canvas id="{chart_id}"></canvas></div>
                </div>
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>💡 WHAT WORKED & WHAT'S BLOCKING</span>
                        <span class="status-pill status-watch">🟡 AUDIT</span>
                    </div>
                    <ul class="bullet-list">
                        <li class="bullet-item"><strong>WHAT WORKED:</strong> Truyền thông mass đạt 514 đăng ký (SGN 336 TX, HAN 178 TX).</li>
                        <li class="bullet-item"><strong>WHAT'S BLOCKING:</strong> Tiến độ chụp ảnh xác minh Baga còn chậm ở nhóm PT.</li>
                        <li class="bullet-item"><strong>NEXT 7 DAYS:</strong> Hoàn tất xác minh 100% hồ sơ để chi trả thưởng đúng hạn 30/8.</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text editable">DECISION NEEDED: Phê duyệt quy trình xác minh tự động trên App để tăng tốc hoàn ứng Baga trước 30/8.</div>
        </div>

        <div class="slide-footer">
            <span class="editable">Ahamove Confidential • Decision Architecture Suite</span>
            <span class="editable">Source: Slide {sn} • Ingested Data Log</span>
        </div>
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const ctx = document.getElementById("{chart_id}");
            if (ctx) {{
                new Chart(ctx, {{
                    type: 'bar',
                    data: {{
                        labels: ['SGN (TP.HCM)', 'HAN (Hà Nội)'],
                        datasets: [{{
                            label: 'Tài xế Lắp Baga Bulky',
                            data: [336, 178],
                            backgroundColor: ['#FF7F32', '#0E4174']
                        }}]
                    }},
                    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
                }});
            }}
        }});
    </script>
    """


def render_layout_i_amnesty_flow(sn: int, title: str, takeaway: str, total_count: int = 29) -> str:
    """Layout I — Amnesty & Operational Policy Flowchart (Slide 19 Ân Xá Policy)"""
    return f"""
    <div class="slide-page" id="slide-{sn}">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • 03 — POLICY FLOWCHART</span>
                <span class="slide-page-num">SLIDE {sn:02d} / {total_count:02d}</span>
            </div>
            <div class="slide-title editable">{title}</div>
            <div class="takeaway-sub editable">Chính sách Ân Xá Tài Xế: Quy trình 4 bước mở lại tài khoản cho 1,250 tài xế vi phạm nhẹ</div>
        </div>

        <div class="main-content">
            <div class="dash-card">
                <div class="card-title-bar">
                    <span>🔄 AMNESTY RE-ACTIVATION FLOWCHART</span>
                    <span class="status-pill status-on-track">🟢 POLICY FLOW</span>
                </div>
                <div class="flowchart-container">
                    <div class="flow-step">
                        <div style="font-size: 11px; font-weight: 800; color: #64748B;">STEP 1</div>
                        <div style="font-size: 13.5px; font-weight: 800; color: #0E4174;">VI PHẠM NHẸ</div>
                        <div style="font-size: 11.5px; color: #64748B;">Khóa dưới 30 ngày</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-step">
                        <div style="font-size: 11px; font-weight: 800; color: #64748B;">STEP 2</div>
                        <div style="font-size: 13.5px; font-weight: 800; color: #0E4174;">ĐƠN ĐỀ NGHỊ</div>
                        <div style="font-size: 11.5px; color: #64748B;">Gửi nguyện vọng Ân xá</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-step">
                        <div style="font-size: 11px; font-weight: 800; color: #64748B;">STEP 3</div>
                        <div style="font-size: 13.5px; font-weight: 800; color: #0E4174;">ĐÀO TẠO LẠI</div>
                        <div style="font-size: 11.5px; color: #64748B;">Học bài Quy chế SLA</div>
                    </div>
                    <div class="flow-arrow">➔</div>
                    <div class="flow-step" style="border-top: 3px solid #10B981; background: #F0FDF4;">
                        <div style="font-size: 11px; font-weight: 800; color: #059669;">STEP 4</div>
                        <div style="font-size: 13.5px; font-weight: 800; color: #047857;">MỞ TÀI KHOẢN</div>
                        <div style="font-size: 11.5px; color: #059669;">Kích hoạt lại dịch vụ</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text editable">MANAGEMENT ATTENTION: Đẩy nhanh công tác truyền thông chính sách Ân Xá qua Zalo OA để phục hồi nguồn cung trước Peak-hour.</div>
        </div>

        <div class="slide-footer">
            <span class="editable">Ahamove Confidential • Decision Architecture Suite</span>
            <span class="editable">Source: Slide {sn} • Ingested Data Log</span>
        </div>
    </div>
    """


def render_layout_f_governance(sn: int, title: str, takeaway: str, tables: list, total_count: int = 29) -> str:
    """Layout F — Governance Pulse & Strategic Action Tracker (Slide 28)"""
    chart_id = f"chart_slide_{sn}"
    tr_rows = ""
    if tables and len(tables) > 0 and tables[0].get("rows"):
        for row in tables[0]["rows"]:
            cells = "".join([f'<td class="editable">{c}</td>' for c in row[:5]])
            tr_rows += f"<tr>{cells}</tr>"
    
    if not tr_rows:
        tr_rows = """
        <tr><td>Core BigC Long Biên</td><td>Lead đăng ký cắm chốt chưa đạt kỳ vọng</td><td>Mở rộng push noti</td><td>20/8</td><td><span class="status-pill status-watch">🟡 WATCH</span></td></tr>
        <tr><td>Minihub Comms</td><td>Thông tin chưa hệ thống hóa</td><td>Review content & flow</td><td>20/8</td><td><span class="status-pill status-on-track">🟢 ON TRACK</span></td></tr>
        <tr><td>Sinh nhật 11 Tuổi</td><td>Pre-event Minigame đang chạy</td><td>Livestream trực tiếp 21/8</td><td>21/8</td><td><span class="status-pill status-done">🔵 DONE</span></td></tr>
        """
        table_headers = "<th>Hạng Mục</th><th>Bối Cảnh / Nguyên Nhân</th><th>Hành Động Cụ Thể</th><th>Deadline</th><th>Trạng Thái</th>"
    else:
        table_headers = "".join([f"<th>{h}</th>" for h in tables[0]["headers"][:5]])

    return f"""
    <div class="slide-page" id="slide-{sn}">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • 04 — GOVERNANCE PULSE</span>
                <span class="slide-page-num">SLIDE {sn:02d} / {total_count:02d}</span>
            </div>
            <div class="slide-title editable">{title}</div>
            <div class="takeaway-sub editable">Nhịp quản trị: 48% hạng mục On Track, tập trung giải quyết 3 điểm nghẽn ưu tiên trước 21/8</div>
        </div>

        <div class="main-content">
            <div class="grid-gov-asymmetric">
                <!-- 32% Governance Pulse Scorecard -->
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>📊 GOVERNANCE PULSE</span>
                        <span class="status-pill status-on-track">🟢 AUDIT SCORE</span>
                    </div>
                    <div class="gov-pulse-card">
                        <div class="pulse-stat-row green">
                            <span>🟢 48% ON TRACK</span>
                            <span>Healthy</span>
                        </div>
                        <div class="pulse-stat-row yellow">
                            <span>🟠 27% WATCH</span>
                            <span>Attention</span>
                        </div>
                        <div class="pulse-stat-row red">
                            <span>🔴 12% OFF TRACK</span>
                            <span>Escalate</span>
                        </div>
                        <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #CBD5E1; font-size: 11.5px; font-weight: 800; color: #0E4174; display: flex; justify-content: space-between;">
                            <span>NEXT DEADLINE</span>
                            <span>21 AUG (Livestream)</span>
                        </div>
                    </div>
                    <div class="chart-wrapper" style="height: 140px; margin-top: 4px;"><canvas id="{chart_id}"></canvas></div>
                </div>

                <!-- 66% Strategic Action Tracker -->
                <div class="dash-card">
                    <div class="card-title-bar">
                        <span>📋 STRATEGIC ACTION TRACKER</span>
                        <span class="status-pill status-on-track">🟢 EXECUTIVE AUDIT</span>
                    </div>
                    <table class="dash-table">
                        <thead><tr>{table_headers}</tr></thead>
                        <tbody>{tr_rows}</tbody>
                    </table>
                </div>
            </div>
        </div>

        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text editable">MANAGEMENT ATTENTION: Chuẩn bị kỹ thuật cho Livestream Sinh nhật 11 Tuổi ngày 21/8 và đẩy nhanh deal bảo hiểm.</div>
        </div>

        <div class="slide-footer">
            <span class="editable">Ahamove Confidential • Decision Architecture Suite</span>
            <span class="editable">Source: Slide {sn} • Ingested Data Log</span>
        </div>
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const ctx = document.getElementById("{chart_id}");
            if (ctx) {{
                new Chart(ctx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['On Track', 'Watch', 'Off Track', 'Done'],
                        datasets: [{{
                            data: [14, 8, 3, 4],
                            backgroundColor: ['#10B981', '#F59E0B', '#EF4444', '#0284C7']
                        }}]
                    }},
                    options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
                }});
            }}
        }});
    </script>
    """


def render_layout_h_driver_voice(sn: int, title: str, takeaway: str, total_count: int = 29) -> str:
    """Layout H — Driver Voice Mechanism (Slide 29 VOC: 25% Quote | 45% Mechanism | 30% Success Criteria Framework)"""
    return f"""
    <div class="slide-page" id="slide-{sn}">
        <div class="top-accent-bar"></div>
        <div class="slide-header">
            <div class="header-meta">
                <span class="slide-brand-tag">DRIVER MANAGEMENT • 03 — DRIVER VOICE & VOC</span>
                <span class="slide-page-num">SLIDE {sn:02d} / {total_count:02d}</span>
            </div>
            <div class="slide-title editable">{title}</div>
            <div class="takeaway-sub editable">Lắng nghe tài xế: Điều kiện Online >80% tạo rào cản UX làm giảm 25.6% tỷ lệ nhận thưởng ca</div>
        </div>

        <div class="main-content">
            <!-- Asymmetrical Grid: 25% Quote | 45% Mechanism | 30% Success Criteria -->
            <div class="grid-voc-asymmetric">
                <!-- 25% Driver Quote -->
                <div class="dash-card" style="border-top: 3px solid #EF4444; background: #FEF2F2;">
                    <div class="card-title-bar"><span style="color:#B91C1C;">💬 DRIVER VOICE</span></div>
                    <div style="font-size: 13.5px; font-weight: 600; font-style: italic; color: #7F1D1D; line-height: 1.45;">
                        "Tôi chạy đủ ca nhưng hệ thống không ghi nhận Check-in vì phải di chuyển ngoài Zone trả đơn!"
                    </div>
                </div>

                <!-- 45% Operational Mechanism & Evidence -->
                <div class="dash-card" style="border-top: 3px solid #F59E0B;">
                    <div class="card-title-bar"><span>⚙️ OPERATIONAL MECHANISM & EVIDENCE</span></div>
                    <ul class="bullet-list">
                        <li class="bullet-item">Điều kiện Online >80% áp dụng toàn ca gây ma sát cho tài xế di chuyển xa.</li>
                        <li class="bullet-item">Tài xế di chuyển trả đơn ngoài Zone $\rightarrow$ không được tính thời gian Online.</li>
                        <li class="bullet-item">Bị loại khỏi danh sách thưởng ca tự động dù đã giao nhận đủ đơn.</li>
                    </ul>
                </div>

                <!-- 30% Success Criteria & Measurement Framework -->
                <div class="dash-card" style="border-top: 3px solid #10B981; background: #F0FDF4;">
                    <div class="card-title-bar"><span style="color:#047857;">🎯 SUCCESS CRITERIA FRAMEWORK</span></div>
                    <div class="success-criteria-card">
                        <div style="font-size: 11.5px; font-weight: 800; color: #0E4174;">MEASUREMENT FRAMEWORK</div>
                        <div style="font-size: 12.5px; font-weight: 700; color: #1E293B;">
                            Online Threshold: 80% ➔ 75%
                        </div>
                        <div style="font-size: 12px; color: #059669; font-weight: 700;">
                            ↓ Giảm Ma Sát UX
                        </div>
                        <div style="font-size: 12.5px; font-weight: 700; color: #1E293B;">
                            Reward Participation: 25.6% ↓ ➔ Target Recovery
                        </div>
                        <div style="font-size: 11.5px; font-weight: 800; color: #FF7F32; margin-top: 4px;">
                            Auto Check-in: Launch &lt; 25/8
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="mgmt-banner">
            <div class="mgmt-label"><span>💡</span> <span>Management Decision / Ask</span></div>
            <div class="mgmt-text editable">DECISION NEEDED: Phê duyệt điều chỉnh ngưỡng Online requirement từ 80% xuống 75% cho nhóm chạy ca liên tỉnh/xa zone.</div>
        </div>

        <div class="slide-footer">
            <span class="editable">Ahamove Confidential • Decision Architecture Suite</span>
            <span class="editable">Source: Slide {sn} • Ingested Data Log</span>
        </div>
    </div>
    """
