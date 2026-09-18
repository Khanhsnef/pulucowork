# INSTRUCTION FOR CHATGPT CANVAS / REDESIGN ENGINE

You are an Expert Design Technologist & Modern Web UI Architect.

Below is an existing 16:9 HTML Slide Deck (`real_report.html`) containing 8 operational slides for **Ahamove Driver Management**.

## YOUR TASK:
Redesign the HTML/CSS of this presentation in ChatGPT Canvas to make it look **visually STUNNING, ultra-premium, and modern** (e.g., sleek Dark-mode Glassmorphic Dashboard, Apple/Gemini aesthetic, vibrant gradients, high-contrast visual hierarchy).

## STRICT RULES:
1. **KEEP 100% OF THE DATA**: Do NOT change, alter, or omit any metrics, percentage values, dates, headers, or bullet text.
2. **MAINTAIN 16:9 CANVAS**: Preserve 1920x1080 resolution / aspect ratio for slide pages.
3. **5 VISUAL LAYOUT PRINCIPLES**:
   - Asymmetric Focal Point (Hero KPI / Card 1.5x larger than surrounding context).
   - Floating Glass Cards with 16px border-radius and subtle 1px border stroke.
   - Micro-Visual Anchors (Icon Badges 🎯 ⚡ 💡 🔴 🏆 📊).
   - Giant Numbers (48px - 56px Bold) for key metrics.
   - Dual-Pane 40/60 Balance.
4. **LIVE EDIT MODE**: Keep `contenteditable="true"` or editable classes so the text remains editable in browser.

---

## INPUT HTML SOURCE CODE TO REDESIGN:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
    <title>Ahamove DM NW Executive Meeting Report 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Lexend:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-canvas: #F8FAFC;
            --card-bg: #FFFFFF;
            --card-border: rgba(226, 232, 240, 0.8);
            --font-family: Lexend, Inter, sans-serif;
            --primary: #0E4174;
            --accent: #FF7F32;
            --text-main: #0F172A;
            --text-muted: #475569;
            --positive: #10B981;
            --negative: #EF4444;
            --warning: #F59E0B;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #0f172a;
            font-family: var(--font-family);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 0;
            gap: 40px;
        }

        /* Toolbar controls */
        .toolbar {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 9999;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px 24px;
            border-radius: 999px;
            display: flex;
            gap: 16px;
            align-items: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }

        .toolbar button {
            background: var(--accent);
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 14px;
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }

        .toolbar button:hover {
            transform: scale(1.05);
            filter: brightness(1.1);
        }

        /* 16:9 Canvas Container */
        .slide-page {
            width: 1920px;
            height: 1080px;
            background-color: var(--bg-canvas);
            border-radius: 24px;
            padding: 56px 64px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            overflow: hidden;
        }

        /* Header section */
        .slide-header {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .slide-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .takeaway-title {
            font-size: 32px;
            font-weight: 800;
            color: var(--primary);
            line-height: 1.25;
            letter-spacing: -0.5px;
        }

        /* Hero KPI Bar */
        .hero-kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 16px;
        }

        .hero-kpi-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 20px 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            box-shadow: 0 10px 25px -5px rgba(14, 65, 116, 0.06);
            position: relative;
            overflow: hidden;
        }

        .hero-kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 6px;
            height: 100%;
            background: var(--accent);
        }

        .hero-kpi-label {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
        }

        .hero-kpi-val {
            font-size: 48px;
            font-weight: 900;
            color: var(--primary);
            line-height: 1.0;
        }

        .hero-kpi-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            width: fit-content;
        }

        .badge-positive { background: #ECFDF5; color: var(--positive); }
        .badge-negative { background: #FEF2F2; color: var(--negative); }
        .badge-neutral { background: #EFF6FF; color: var(--primary); }

        /* Content Body Grid */
        .content-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            flex: 1;
            margin-top: 24px;
        }

        .glass-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px 28px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
        }

        .card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 700;
            color: var(--primary);
        }

        .bullet-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .bullet-item {
            font-size: 15px;
            line-height: 1.5;
            color: var(--text-main);
            position: relative;
            padding-left: 20px;
        }

        .bullet-item::before {
            content: '•';
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: 900;
            font-size: 20px;
            line-height: 1;
        }

        /* Data Table */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
            font-size: 14px;
        }

        .data-table th {
            background: #F1F5F9;
            color: var(--primary);
            font-weight: 700;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 2px solid var(--card-border);
        }

        .data-table td {
            padding: 12px 16px;
            border-bottom: 1px solid var(--card-border);
            color: var(--text-main);
        }

        /* Slide Footer */
        .slide-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 13px;
            color: var(--text-muted);
            border-top: 1px solid rgba(226, 232, 240, 0.8);
            padding-top: 16px;
        }

        /* Editable highlight indicator */
        [contenteditable="true"]:focus {
            outline: 2px solid var(--accent);
            background: rgba(255, 127, 50, 0.05);
            border-radius: 4px;
        }

        @media print {
            body { background: none; padding: 0; }
            .toolbar { display: none; }
            .slide-page { page-break-after: always; box-shadow: none; border-radius: 0; }
        }
    </style>
</head>
<body>

    <div class="toolbar">
        <span style="color:#fff; font-size:13px; font-weight:600;">⚡ Ahamove 16:9 Presentation</span>
        <button id="editBtn" onclick="toggleEditMode()">✏️ Edit Mode (E)</button>
        <button onclick="window.print()">🖨️ Export PDF</button>
    </div>

    
        <div class="slide-page" id="slide-1">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 1</span>
                </div>
                <div class="takeaway-title editable">Báo Cáo Vận Hành DM NW: CTR Đạt 77.38% & GDR Đạt 95.52%, Phát Hiện Vấn Đề UX Check-in Cityzone & Đẩy Mạnh EV Partnership</div>
                <div class="hero-kpi-grid">
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">[NW] Overall CTR</div>
                    <div class="hero-kpi-val editable">77.38%</div>
                    <span class="hero-kpi-badge badge-negative">-1.11% WoW</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">[NW] Overall GDR</div>
                    <div class="hero-kpi-val editable">95.52%</div>
                    <span class="hero-kpi-badge badge-neutral">-0.04% WoW</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">SGN GDR (HCM)</div>
                    <div class="hero-kpi-val editable">96.61%</div>
                    <span class="hero-kpi-badge badge-positive">-0.69% WoW</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">HAN GDR (HN)</div>
                    <div class="hero-kpi-val editable">94.21%</div>
                    <span class="hero-kpi-badge badge-warning">-1.36% WoW</span>
                </div>
                </div>
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>🏆</span>
                    <span class="editable">Key Highlights Vận Hành Tuần</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Tuyển dụng Core: Đã đủ lead đăng ký cho Fuji, Ajinomoto, Baga & chuỗi push active CP 15.8 (2-3 noti/ngày).</li><li class="bullet-item editable">CityZone Funnel: Quy mô tăng trưởng x3.5 lần (112 -> 394 ca đăng ký, 47 -> 197 tài xế tham gia).</li><li class="bullet-item editable">Partnership EV: Đã publish Landing Page policy mới, review xong hợp đồng mượn xe Dat Bike & Selex KOC.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>🎯</span>
                    <span class="editable">Trọng Tâm & Điểm Nghẽn Cần Xử Lý Immediate</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Phát hiện UX Check-in CityZone: 25.6% tổng đơn thuộc nhóm tài xế chạy ca nhưng quên bấm Check-in.</li><li class="bullet-item editable">Tuyển Core BigC Long Biên (HAN): Lead đăng ký cắm chốt chưa đạt kỳ vọng.</li><li class="bullet-item editable">Sự cố ngày 14/8: Tự động bật dịch vụ 2H-4H làm tài xế bức xúc trên hội nhóm (Đã fix trong ngày).</li></ul>
            </div>
            
                
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 22, 24, 26, 27, 28, 29</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-2">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 2</span>
                </div>
                <div class="takeaway-title editable">Chỉ Số Tuân Thủ CTR & GDR: SGN Giữ Vững GDR 96.61%, HAN CTR Cần Tăng Cường Push Noti Nhắc Nhở</div>
                <div class="hero-kpi-grid">
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">HAN CTR (HN)</div>
                    <div class="hero-kpi-val editable">72.72%</div>
                    <span class="hero-kpi-badge badge-negative">Target: 130%</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">HAN GDR (HN)</div>
                    <div class="hero-kpi-val editable">94.21%</div>
                    <span class="hero-kpi-badge badge-warning">Target: 120%</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">SGN CTR (HCM)</div>
                    <div class="hero-kpi-val editable">79.91%</div>
                    <span class="hero-kpi-badge badge-neutral">Target: 130%</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">SGN GDR (HCM)</div>
                    <div class="hero-kpi-val editable">96.61%</div>
                    <span class="hero-kpi-badge badge-positive">Target: 120%</span>
                </div>
                </div>
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>📊</span>
                    <span class="editable">Phân Tích Chi Tiết CTR (Compliance True Rate)</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">HAN CTR đứng ở mức 72.72% (-1.86% WoW), khoảng cách lớn so với Target 130%.</li><li class="bullet-item editable">SGN CTR đạt 79.91% (-1.29% WoW), duy trì lượng tài xế tuân thủ quy trình giao nhận tốt hơn.</li><li class="bullet-item editable">Hành động: Tăng tần suất Noti & SMS nhắc mở lại dịch vụ đối với nhóm tài xế tại Hà Nội.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>📊</span>
                    <span class="editable">Phân Tích Chi Tiết GDR (Good Driver Rate)</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">SGN GDR đạt 96.61%, chứng minh chất lượng dịch vụ đội ngũ tài xế phía Nam được duy trì xuất sắc.</li><li class="bullet-item editable">HAN GDR đạt 94.21% (-1.36% WoW), cần rà soát lại các điểm vi phạm thái độ và thời gian giao.</li><li class="bullet-item editable">Chuẩn hóa lại bộ Content & flow truyền thông ngay tại các điểm chạm Mini-hub.</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">Khu Vực (Region)</th><th class="editable">CTR Thực Tế</th><th class="editable">Target CTR</th><th class="editable">GDR Thực Tế</th><th class="editable">Target GDR</th><th class="editable">Đánh Giá SLA</th></tr></thead>
                    <tbody><tr><td class="editable">Hà Nội (HAN)</td><td class="editable">72.72%</td><td class="editable">130%</td><td class="editable">94.21%</td><td class="editable">120%</td><td class="editable">⚠️ Cần Push Noti Tần Suất Cao</td></tr><tr><td class="editable">TP.HCM (SGN)</td><td class="editable">79.91%</td><td class="editable">130%</td><td class="editable">96.61%</td><td class="editable">120%</td><td class="editable">✔ GDR Đạt Chất Lượng Tốt</td></tr><tr><td class="editable">Toàn Mạng (NW)</td><td class="editable">77.38%</td><td class="editable">130%</td><td class="editable">95.52%</td><td class="editable">120%</td><td class="editable">🏆 Đạt Chuẩn Vận Hành Toàn Mạng</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 26</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-3">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 3</span>
                </div>
                <div class="takeaway-title editable">CityZone Hub Funnel: 25.6% Đơn Hàng Thuộc Nhóm Tài Xế Chạy Ca Quên Check-in — Vấn Đề UX Thao Tác</div>
                <div class="hero-kpi-grid">
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Registered Hub</div>
                    <div class="hero-kpi-val editable">770</div>
                    <span class="hero-kpi-badge badge-neutral">100% Funnel</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Check-in Rate</div>
                    <div class="hero-kpi-val editable">49.8%</div>
                    <span class="hero-kpi-badge badge-warning">252 ca</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Chưa Check-in Lần Nào</div>
                    <div class="hero-kpi-val editable">55%</div>
                    <span class="hero-kpi-badge badge-negative">128 / 232 TX</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Đơn Ngoài Ca Quên Check-in</div>
                    <div class="hero-kpi-val editable">25.6%</div>
                    <span class="hero-kpi-badge badge-negative">401 đơn</span>
                </div>
                </div>
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>💡</span>
                    <span class="editable">Phát Hiện Quan Trọng Về Thao Tác Check-In</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">39% số ca no-show/hủy (99/254 ca) VẪN CÓ ĐƠN HOÀN THÀNH trong đúng khung giờ ca đó (401 đơn).</li><li class="bullet-item editable">Năng suất nhóm quên check-in đạt 4.05 đơn/ca (xấp xỉ nhóm check-in chuẩn 4.63 đơn/ca).</li><li class="bullet-item editable">Kết luận: Đây KHÔNG PHẢI tài xế lười, mà là vấn đề UX nhận biết thao tác check-in trên App.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>⚡</span>
                    <span class="editable">Chi Tiết Phễu Chuyển Đổi Active Hub</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Tổng ca đăng ký: 506 ca (100%). Hủy ca: 91 ca (18.0%).</li><li class="bullet-item editable">No-show (đăng ký nhưng không check-in): 163 ca (32.2%).</li><li class="bullet-item editable">Check-in thực tế: 252 ca (49.8%). Check-in + có đơn hoàn thành: 231 ca (45.7%).</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">Trạng Thái Phễu Hub</th><th class="editable">Số Ca</th><th class="editable">% Tỷ Lệ</th><th class="editable">Đánh Giá Vận Hành</th></tr></thead>
                    <tbody><tr><td class="editable">Đăng ký ca</td><td class="editable">506</td><td class="editable">100.0%</td><td class="editable">Nhu cầu tham gia cao</td></tr><tr><td class="editable">Hủy ca</td><td class="editable">91</td><td class="editable">18.0%</td><td class="editable">Mức hủy bình thường</td></tr><tr><td class="editable">No-show (Không Check-in)</td><td class="editable">163</td><td class="editable">32.2%</td><td class="editable">⚠️ Vấn đề UX thao tác Check-in</td></tr><tr><td class="editable">Check-in thành công</td><td class="editable">252</td><td class="editable">49.8%</td><td class="editable">Cần cải thiện lên >70%</td></tr><tr><td class="editable">Check-in + Hoàn thành đơn</td><td class="editable">231</td><td class="editable">45.7%</td><td class="editable">Tỷ lệ có đơn hiệu quả high (91.6%)</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 22</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-4">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 4</span>
                </div>
                <div class="takeaway-title editable">Tối Ưu Khung Giờ Ca Hub: Ca Sáng 08:00-12:00 Đạt Năng Suất 6.25 Đơn/Ca (Gấp 2.8 Lần Ca Tối 18:00-20:00)</div>
                <div class="hero-kpi-grid">
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Ca Sáng 08-12h Check-in</div>
                    <div class="hero-kpi-val editable">63.2%</div>
                    <span class="hero-kpi-badge badge-positive">6.25 đơn/ca</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Ca Tối 18-20h Check-in</div>
                    <div class="hero-kpi-val editable">35.0%</div>
                    <span class="hero-kpi-badge badge-negative">2.26 đơn/ca</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Năng Suất Ca 4H</div>
                    <div class="hero-kpi-val editable">6.25</div>
                    <span class="hero-kpi-badge badge-positive">2.06 đơn/giờ</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Năng Suất Ca 2H</div>
                    <div class="hero-kpi-val editable">3.62</div>
                    <span class="hero-kpi-badge badge-neutral">1.93 đơn/giờ</span>
                </div>
                </div>
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>📈</span>
                    <span class="editable">Khung Giờ Hiệu Quả Nhất (08:00 – 12:00)</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Đạt tỷ lệ Check-in cao nhất (63.2%), sản lượng trung bình 6.25 đơn/ca (2.06 đơn/giờ).</li><li class="bullet-item editable">Các ca 14:00-17:00 (54.9% check-in, 4.84 đơn/ca) và 15:00-17:00 (64.3% check-in) cũng đạt hiệu quả cao.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>📉</span>
                    <span class="editable">Khung Giờ Kém Hiệu Quả (18:00 – 20:00)</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Thu hút 19.2% đăng ký (97 ca) nhưng chỉ có 23.7% check-in thực tế.</li><li class="bullet-item editable">Năng suất thấp nhất: Chỉ 2.26 đơn/ca (1.71 đơn/giờ). Đề xuất giảm bớt quota ca tối để đẩy sang ca sáng.</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">Khung Giờ Ca</th><th class="editable">Ca Đăng Ký</th><th class="editable">% Check-in</th><th class="editable">Đơn / Ca</th><th class="editable">Đơn / Giờ</th></tr></thead>
                    <tbody><tr><td class="editable">08:00 – 12:00 (4h)</td><td class="editable">95 (18.8%)</td><td class="editable">63.20%</td><td class="editable">6.25</td><td class="editable">2.06 🏆 Best Slot</td></tr><tr><td class="editable">14:00 – 17:00 (3h)</td><td class="editable">113 (22.3%)</td><td class="editable">54.90%</td><td class="editable">4.84</td><td class="editable">2.07</td></tr><tr><td class="editable">15:00 – 17:00 (2h)</td><td class="editable">28 (5.5%)</td><td class="editable">64.30%</td><td class="editable">4.44</td><td class="editable">2.41</td></tr><tr><td class="editable">18:00 – 20:00 (2h)</td><td class="editable">97 (19.2%)</td><td class="editable">23.70%</td><td class="editable">2.26</td><td class="editable">1.71 ⚠️ Kém Hiệu Quả</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 23</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-5">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 5</span>
                </div>
                <div class="takeaway-title editable">Tăng Trưởng Quy Mô Hub: Số Ca Đăng Ký Tăng Tốc x3.5 Lần (T1 -> T2), Cần Giải Quyết 55.8% Tài Xế Rời Bỏ Sau Ca Đầu</div>
                <div class="hero-kpi-grid">
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Tăng Trưởng Ca T1->T2</div>
                    <div class="hero-kpi-val editable">x3.5</div>
                    <span class="hero-kpi-badge badge-positive">112 -> 394 ca</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Tăng Trưởng TX T1->T2</div>
                    <div class="hero-kpi-val editable">x4.2</div>
                    <span class="hero-kpi-badge badge-positive">47 -> 197 TX</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Chạy 1 Ca Rồi Thôi</div>
                    <div class="hero-kpi-val editable">55.8%</div>
                    <span class="hero-kpi-badge badge-negative">58 tài xế</span>
                </div>
                
                <div class="hero-kpi-card">
                    <div class="hero-kpi-label editable">Quay Lại ≥ 2 Ngày</div>
                    <div class="hero-kpi-val editable">39.4%</div>
                    <span class="hero-kpi-badge badge-positive">41 tài xế</span>
                </div>
                </div>
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>🚀</span>
                    <span class="editable">Tăng Trưởng Quy Mô 2 Tuần Liên Tiếp</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Số ca đăng ký tăng 3.5 lần (từ 112 lên 394 ca), số tài xế tham gia tăng 4.2 lần (từ 47 lên 197 tài xế).</li><li class="bullet-item editable">Fill rate tăng từ 79.7% lên 84.1% (+4.4%), cho thấy nhu cầu đơn hàng Hub được đáp ứng tốt hơn.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>🔄</span>
                    <span class="editable">Thách Thức Retention & Gắn Kết Mới</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">55.8% tài xế (58 TX) chỉ chạy đúng 1 ca rồi ngừng -> Cần tạo điểm chạm training & hướng dẫn chạy Hub lần đầu.</li><li class="bullet-item editable">44.2% tài xế quay lại chạy >= 2 ca; 17.3% tài xế (18 TX) trung thành quay lại >= 3 ngày khác nhau.</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">Chỉ Số Retention Hub</th><th class="editable">Tuần 1 (4-9/8)</th><th class="editable">Tuần 2 (10-16/8)</th><th class="editable">Mức Thay Đổi</th></tr></thead>
                    <tbody><tr><td class="editable">Ca đăng ký</td><td class="editable">112</td><td class="editable">394</td><td class="editable">×3.5 🚀 Tăng nhanh</td></tr><tr><td class="editable">Tài xế tham gia</td><td class="editable">47</td><td class="editable">197</td><td class="editable">×4.2 🚀 Tăng nhanh</td></tr><tr><td class="editable">Check-in rate</td><td class="editable">50.9%</td><td class="editable">49.5%</td><td class="editable">≈ Ổn định</td></tr><tr><td class="editable">Năng suất (đơn/giờ)</td><td class="editable">1.96</td><td class="editable">2.01</td><td class="editable">≈ Ổn định</td></tr><tr><td class="editable">Fill rate</td><td class="editable">79.7%</td><td class="editable">84.1%</td><td class="editable">+4.4% 📈 Cải thiện</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 24</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-6">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 6</span>
                </div>
                <div class="takeaway-title editable">Truyền Thông & Tuyển Đội Core: Đạt Kế Hoạch Fuji & Ajinomoto, Tập Trung Tháo Gỡ Core BigC Long Biên</div>
                
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>🏆</span>
                    <span class="editable">Communications Highlights</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Thưởng baga & Tuyển Core Fuji, Ajinomoto: Đã thu thập đủ lead đăng ký theo kế hoạch.</li><li class="bullet-item editable">Thông báo mở lại dịch vụ tại HAN: Đã phát Noti + SMS với tần suất cao.</li><li class="bullet-item editable">Campaign 15.8: Setup popup, bản tin lượng đơn + chuỗi content thưởng điểm nóng, push active 2-3 tin/ngày.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>🔴</span>
                    <span class="editable">Lowlights & Kế Hoạch Khắc Phục</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Tuyển Core BigC Long Biên chưa đạt kỳ vọng -> Tăng tần suất + mở rộng danh sách push noti (Deadline 20/8, PIC Hoa).</li><li class="bullet-item editable">Thông tin truyền thông Mini-hub chưa được hệ thống -> Review content & tạo flow comms chuẩn (Deadline 20/8, PIC Hoa/Khoa/Vân).</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">Hạng Mục Comms</th><th class="editable">Bối Cảnh / Nguyên Nhân</th><th class="editable">Hành Động Khắc Phục</th><th class="editable">Deadline</th><th class="editable">PIC</th></tr></thead>
                    <tbody><tr><td class="editable">Tuyển Core BigC</td><td class="editable">Lead cắm chốt Long Biên chưa đạt kỳ vọng</td><td class="editable">Mở rộng danh sách push noti</td><td class="editable">20/8</td><td class="editable">Hoa</td></tr><tr><td class="editable">Minihub Comms</td><td class="editable">Thông tin chưa hệ thống hóa</td><td class="editable">Tạo content & flow theo cycle</td><td class="editable">20/8</td><td class="editable">Hoa / Khoa / Vân</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 27</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-7">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 7</span>
                </div>
                <div class="takeaway-title editable">Hợp Tác EV & Sự Kiện 11 Tuổi: Hoàn Tất Hợp Đồng Dat Bike, Đẩy Mạnh Gói Thuê Xe Aizen Tại SGN</div>
                
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>⚡</span>
                    <span class="editable">Tình Hình Chuyển Đổi Phương Tiện EV</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Nhu cầu tài xế quan tâm đến EV tăng từ tháng 8, tập trung mạnh nhất tại khu vực TP.HCM.</li><li class="bullet-item editable">Done review hợp đồng mượn xe Dat Bike; bàn giao xe Selex cho KOC mượn tư vấn tài xế NW.</li><li class="bullet-item editable">Gói thuê xe AIZEN: Tách blog riêng truyền thông & seeding bài viết cho tài xế SGN (Deadline 21/8, PIC Khoa/Vân).</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>🎉</span>
                    <span class="editable">Pre-event Sinh Nhật Ahamove 11 Tuổi</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Triển khai hoạt động CHL & minigame online 'Chuyển ý tưởng - Ghép tương lai'.</li><li class="bullet-item editable">Tổ chức chính thức Livestream Sinh nhật Ahamove vào ngày 21/8 (PIC Khoa/Vân/Thúy, Support DM/GR Team).</li><li class="bullet-item editable">Lowlight: Tiến độ đàm phán deal quyền lợi Bảo hiểm cho tài xế còn chậm.</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">Hạng Mục Partnership</th><th class="editable">Trạng Thái Bối Cảnh</th><th class="editable">Kế Hoạch Tiếp Theo</th><th class="editable">Deadline</th><th class="editable">PIC</th></tr></thead>
                    <tbody><tr><td class="editable">Dat Bike</td><td class="editable">Review xong hợp đồng</td><td class="editable">Triển khai mượn xe cho TX</td><td class="editable">Hoàn thành</td><td class="editable">Partnership Team</td></tr><tr><td class="editable">Selex EV</td><td class="editable">Đã bàn giao xe KOC</td><td class="editable">KOC tư vấn tài xế quan tâm NW</td><td class="editable">Đang chạy</td><td class="editable">Partnership Team</td></tr><tr><td class="editable">Thuê xe AIZEN</td><td class="editable">Cần tài xế SGN hiểu rõ gói thuê</td><td class="editable">Tách blog & seeding truyền thông</td><td class="editable">21/8</td><td class="editable">Khoa / Vân</td></tr><tr><td class="editable">Sinh nhật 11 Tuổi</td><td class="editable">Pre-event Minigame đang chạy</td><td class="editable">Livestream trực tiếp 21/8</td><td class="editable">21/8</td><td class="editable">Khoa / Vân / Thúy</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 25, 28</span>
            </div>
        </div>
        

        <div class="slide-page" id="slide-8">
            <div class="slide-header">
                <div class="slide-meta">
                    <span>Ahamove Driver Management • Executive Brief</span>
                    <span>Slide 8</span>
                </div>
                <div class="takeaway-title editable">Lộ Trình Hành Động 3 Bước: Sửa Thao Tác Check-In UX, Điều Chuyển Quota Ca Sáng & Tháo Gỡ Sự Cố 2H-4H</div>
                
            </div>

            <div class="content-grid">
                
            <div class="glass-card">
                <div class="card-header">
                    <span>📋</span>
                    <span class="editable">Bước 1: Fix UX Check-In & Auto Check-In</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Thêm Push Notification trước giờ ca 15 phút nhắc bấm Check-in.</li><li class="bullet-item editable">Cấu hình Auto Check-in nếu tài xế Online và di chuyển trong phạm vi Hub đúng khung giờ ca.</li></ul>
            </div>
            
            <div class="glass-card">
                <div class="card-header">
                    <span>📋</span>
                    <span class="editable">Bước 2: Điều Chuyển Quota Ca Tối Sang Ca Sáng 4H</span>
                </div>
                <ul class="bullet-list"><li class="bullet-item editable">Cắt/giảm ca tối 18:00-20:00 (chỉ 2.26 đơn/ca), dịch chuyển quota sang ca sáng 08:00-12:00 (6.25 đơn/ca).</li><li class="bullet-item editable">Xây dựng điểm chạm hướng dẫn chạy Hub lần đầu để giảm tỷ lệ 55.8% tài xế bỏ sau ca 1.</li></ul>
            </div>
            
                
            <div class="glass-card" style="grid-column: span 2;">
                <table class="data-table">
                    <thead><tr><th class="editable">STT</th><th class="editable">Hành Động Cốt Lõi</th><th class="editable">Mục Tiêu Kỳ Vọng</th><th class="editable">Thời Gian</th><th class="editable">PIC Lead</th></tr></thead>
                    <tbody><tr><td class="editable">1</td><td class="editable">Thêm Push Noti 15p & Auto Check-in</td><td class="editable">Khắc phục 25.6% đơn chạy ngoài ca quên check-in</td><td class="editable">25/8</td><td class="editable">Product / DM Team</td></tr><tr><td class="editable">2</td><td class="editable">Dịch chuyển quota ca 18-20h sang ca 08-12h</td><td class="editable">Tăng năng suất toàn phễu Hub lên >5 đơn/ca</td><td class="editable">22/8</td><td class="editable">Ops Hub Team</td></tr><tr><td class="editable">3</td><td class="editable">Tập huấn & Seeding gói thuê xe AIZEN SGN</td><td class="editable">Tăng nhận thức & tỷ lệ chuyển đổi xe điện EV</td><td class="editable">21/8</td><td class="editable">Khoa / Vân</td></tr><tr><td class="editable">4</td><td class="editable">Tăng push noti tuyển Core BigC Long Biên</td><td class="editable">Đảm bảo đủ lead cắm chốt Long Biên</td><td class="editable">20/8</td><td class="editable">Hoa</td></tr></tbody>
                </table>
            </div>
            
            </div>

            <div class="slide-footer">
                <span class="editable">Confidential • For Internal Decision Architecture Only</span>
                <span class="editable">Source: Slide 24, 27, 28, 29</span>
            </div>
        </div>
        

    <script>
        let isEdit = false;
        function toggleEditMode() {
            isEdit = !isEdit;
            document.querySelectorAll('.editable').forEach(el => {
                el.contentEditable = isEdit;
            });
            const btn = document.getElementById('editBtn');
            btn.innerText = isEdit ? '💾 Save Mode (E)' : '✏️ Edit Mode (E)';
            btn.style.background = isEdit ? '#10B981' : '#FF7F32';
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'e' || e.key === 'E') {
                if (document.activeElement.isContentEditable) return;
                toggleEditMode();
            }
        });
    </script>
</body>
</html>

```

---

## (OPTIONAL) INPUT SLIDE DATA PAYLOAD (JSON):

```json
{
  "deck_title": "Ahamove DM NW Executive Meeting Report 2026",
  "style_theme": "operations",
  "slides": [
    {
      "slide_id": 1,
      "layout_template": "executive-summary",
      "takeaway_header": "Báo Cáo Vận Hành DM NW: CTR Đạt 77.38% & GDR Đạt 95.52%, Phát Hiện Vấn Đề UX Check-in Cityzone & Đẩy Mạnh EV Partnership",
      "hero_kpis": [
        {
          "label": "[NW] Overall CTR",
          "value": "77.38%",
          "delta": "-1.11% WoW",
          "badge_status": "negative"
        },
        {
          "label": "[NW] Overall GDR",
          "value": "95.52%",
          "delta": "-0.04% WoW",
          "badge_status": "neutral"
        },
        {
          "label": "SGN GDR (HCM)",
          "value": "96.61%",
          "delta": "-0.69% WoW",
          "badge_status": "positive"
        },
        {
          "label": "HAN GDR (HN)",
          "value": "94.21%",
          "delta": "-1.36% WoW",
          "badge_status": "warning"
        }
      ],
      "cards": [
        {
          "card_id": "c1",
          "icon_badge": "🏆",
          "title": "Key Highlights Vận Hành Tuần",
          "bullets": [
            "Tuyển dụng Core: Đã đủ lead đăng ký cho Fuji, Ajinomoto, Baga & chuỗi push active CP 15.8 (2-3 noti/ngày).",
            "CityZone Funnel: Quy mô tăng trưởng x3.5 lần (112 -> 394 ca đăng ký, 47 -> 197 tài xế tham gia).",
            "Partnership EV: Đã publish Landing Page policy mới, review xong hợp đồng mượn xe Dat Bike & Selex KOC."
          ]
        },
        {
          "card_id": "c2",
          "icon_badge": "🎯",
          "title": "Trọng Tâm & Điểm Nghẽn Cần Xử Lý Immediate",
          "bullets": [
            "Phát hiện UX Check-in CityZone: 25.6% tổng đơn thuộc nhóm tài xế chạy ca nhưng quên bấm Check-in.",
            "Tuyển Core BigC Long Biên (HAN): Lead đăng ký cắm chốt chưa đạt kỳ vọng.",
            "Sự cố ngày 14/8: Tự động bật dịch vụ 2H-4H làm tài xế bức xúc trên hội nhóm (Đã fix trong ngày)."
          ]
        }
      ],
      "data_table": null,
      "source_slides": [
        22,
        24,
        26,
        27,
        28,
        29
      ]
    },
    {
      "slide_id": 2,
      "layout_template": "kpi-dashboard",
      "takeaway_header": "Chỉ Số Tuân Thủ CTR & GDR: SGN Giữ Vững GDR 96.61%, HAN CTR Cần Tăng Cường Push Noti Nhắc Nhở",
      "hero_kpis": [
        {
          "label": "HAN CTR (HN)",
          "value": "72.72%",
          "delta": "Target: 130%",
          "badge_status": "negative"
        },
        {
          "label": "HAN GDR (HN)",
          "value": "94.21%",
          "delta": "Target: 120%",
          "badge_status": "warning"
        },
        {
          "label": "SGN CTR (HCM)",
          "value": "79.91%",
          "delta": "Target: 130%",
          "badge_status": "neutral"
        },
        {
          "label": "SGN GDR (HCM)",
          "value": "96.61%",
          "delta": "Target: 120%",
          "badge_status": "positive"
        }
      ],
      "cards": [
        {
          "card_id": "c3",
          "icon_badge": "📊",
          "title": "Phân Tích Chi Tiết CTR (Compliance True Rate)",
          "bullets": [
            "HAN CTR đứng ở mức 72.72% (-1.86% WoW), khoảng cách lớn so với Target 130%.",
            "SGN CTR đạt 79.91% (-1.29% WoW), duy trì lượng tài xế tuân thủ quy trình giao nhận tốt hơn.",
            "Hành động: Tăng tần suất Noti & SMS nhắc mở lại dịch vụ đối với nhóm tài xế tại Hà Nội."
          ]
        },
        {
          "card_id": "c4",
          "icon_badge": "📊",
          "title": "Phân Tích Chi Tiết GDR (Good Driver Rate)",
          "bullets": [
            "SGN GDR đạt 96.61%, chứng minh chất lượng dịch vụ đội ngũ tài xế phía Nam được duy trì xuất sắc.",
            "HAN GDR đạt 94.21% (-1.36% WoW), cần rà soát lại các điểm vi phạm thái độ và thời gian giao.",
            "Chuẩn hóa lại bộ Content & flow truyền thông ngay tại các điểm chạm Mini-hub."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "Khu Vực (Region)",
          "CTR Thực Tế",
          "Target CTR",
          "GDR Thực Tế",
          "Target GDR",
          "Đánh Giá SLA"
        ],
        "rows": [
          [
            "Hà Nội (HAN)",
            "72.72%",
            "130%",
            "94.21%",
            "120%",
            "⚠️ Cần Push Noti Tần Suất Cao"
          ],
          [
            "TP.HCM (SGN)",
            "79.91%",
            "130%",
            "96.61%",
            "120%",
            "✔ GDR Đạt Chất Lượng Tốt"
          ],
          [
            "Toàn Mạng (NW)",
            "77.38%",
            "130%",
            "95.52%",
            "120%",
            "🏆 Đạt Chuẩn Vận Hành Toàn Mạng"
          ]
        ]
      },
      "source_slides": [
        26
      ]
    },
    {
      "slide_id": 3,
      "layout_template": "kpi-dashboard",
      "takeaway_header": "CityZone Hub Funnel: 25.6% Đơn Hàng Thuộc Nhóm Tài Xế Chạy Ca Quên Check-in — Vấn Đề UX Thao Tác",
      "hero_kpis": [
        {
          "label": "Registered Hub",
          "value": "770",
          "delta": "100% Funnel",
          "badge_status": "neutral"
        },
        {
          "label": "Check-in Rate",
          "value": "49.8%",
          "delta": "252 ca",
          "badge_status": "warning"
        },
        {
          "label": "Chưa Check-in Lần Nào",
          "value": "55%",
          "delta": "128 / 232 TX",
          "badge_status": "negative"
        },
        {
          "label": "Đơn Ngoài Ca Quên Check-in",
          "value": "25.6%",
          "delta": "401 đơn",
          "badge_status": "negative"
        }
      ],
      "cards": [
        {
          "card_id": "c5",
          "icon_badge": "💡",
          "title": "Phát Hiện Quan Trọng Về Thao Tác Check-In",
          "bullets": [
            "39% số ca no-show/hủy (99/254 ca) VẪN CÓ ĐƠN HOÀN THÀNH trong đúng khung giờ ca đó (401 đơn).",
            "Năng suất nhóm quên check-in đạt 4.05 đơn/ca (xấp xỉ nhóm check-in chuẩn 4.63 đơn/ca).",
            "Kết luận: Đây KHÔNG PHẢI tài xế lười, mà là vấn đề UX nhận biết thao tác check-in trên App."
          ]
        },
        {
          "card_id": "c6",
          "icon_badge": "⚡",
          "title": "Chi Tiết Phễu Chuyển Đổi Active Hub",
          "bullets": [
            "Tổng ca đăng ký: 506 ca (100%). Hủy ca: 91 ca (18.0%).",
            "No-show (đăng ký nhưng không check-in): 163 ca (32.2%).",
            "Check-in thực tế: 252 ca (49.8%). Check-in + có đơn hoàn thành: 231 ca (45.7%)."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "Trạng Thái Phễu Hub",
          "Số Ca",
          "% Tỷ Lệ",
          "Đánh Giá Vận Hành"
        ],
        "rows": [
          [
            "Đăng ký ca",
            "506",
            "100.0%",
            "Nhu cầu tham gia cao"
          ],
          [
            "Hủy ca",
            "91",
            "18.0%",
            "Mức hủy bình thường"
          ],
          [
            "No-show (Không Check-in)",
            "163",
            "32.2%",
            "⚠️ Vấn đề UX thao tác Check-in"
          ],
          [
            "Check-in thành công",
            "252",
            "49.8%",
            "Cần cải thiện lên >70%"
          ],
          [
            "Check-in + Hoàn thành đơn",
            "231",
            "45.7%",
            "Tỷ lệ có đơn hiệu quả high (91.6%)"
          ]
        ]
      },
      "source_slides": [
        22
      ]
    },
    {
      "slide_id": 4,
      "layout_template": "comparison",
      "takeaway_header": "Tối Ưu Khung Giờ Ca Hub: Ca Sáng 08:00-12:00 Đạt Năng Suất 6.25 Đơn/Ca (Gấp 2.8 Lần Ca Tối 18:00-20:00)",
      "hero_kpis": [
        {
          "label": "Ca Sáng 08-12h Check-in",
          "value": "63.2%",
          "delta": "6.25 đơn/ca",
          "badge_status": "positive"
        },
        {
          "label": "Ca Tối 18-20h Check-in",
          "value": "35.0%",
          "delta": "2.26 đơn/ca",
          "badge_status": "negative"
        },
        {
          "label": "Năng Suất Ca 4H",
          "value": "6.25",
          "delta": "2.06 đơn/giờ",
          "badge_status": "positive"
        },
        {
          "label": "Năng Suất Ca 2H",
          "value": "3.62",
          "delta": "1.93 đơn/giờ",
          "badge_status": "neutral"
        }
      ],
      "cards": [
        {
          "card_id": "c7",
          "icon_badge": "📈",
          "title": "Khung Giờ Hiệu Quả Nhất (08:00 – 12:00)",
          "bullets": [
            "Đạt tỷ lệ Check-in cao nhất (63.2%), sản lượng trung bình 6.25 đơn/ca (2.06 đơn/giờ).",
            "Các ca 14:00-17:00 (54.9% check-in, 4.84 đơn/ca) và 15:00-17:00 (64.3% check-in) cũng đạt hiệu quả cao."
          ]
        },
        {
          "card_id": "c8",
          "icon_badge": "📉",
          "title": "Khung Giờ Kém Hiệu Quả (18:00 – 20:00)",
          "bullets": [
            "Thu hút 19.2% đăng ký (97 ca) nhưng chỉ có 23.7% check-in thực tế.",
            "Năng suất thấp nhất: Chỉ 2.26 đơn/ca (1.71 đơn/giờ). Đề xuất giảm bớt quota ca tối để đẩy sang ca sáng."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "Khung Giờ Ca",
          "Ca Đăng Ký",
          "% Check-in",
          "Đơn / Ca",
          "Đơn / Giờ"
        ],
        "rows": [
          [
            "08:00 – 12:00 (4h)",
            "95 (18.8%)",
            "63.20%",
            "6.25",
            "2.06 🏆 Best Slot"
          ],
          [
            "14:00 – 17:00 (3h)",
            "113 (22.3%)",
            "54.90%",
            "4.84",
            "2.07"
          ],
          [
            "15:00 – 17:00 (2h)",
            "28 (5.5%)",
            "64.30%",
            "4.44",
            "2.41"
          ],
          [
            "18:00 – 20:00 (2h)",
            "97 (19.2%)",
            "23.70%",
            "2.26",
            "1.71 ⚠️ Kém Hiệu Quả"
          ]
        ]
      },
      "source_slides": [
        23
      ]
    },
    {
      "slide_id": 5,
      "layout_template": "trend",
      "takeaway_header": "Tăng Trưởng Quy Mô Hub: Số Ca Đăng Ký Tăng Tốc x3.5 Lần (T1 -> T2), Cần Giải Quyết 55.8% Tài Xế Rời Bỏ Sau Ca Đầu",
      "hero_kpis": [
        {
          "label": "Tăng Trưởng Ca T1->T2",
          "value": "x3.5",
          "delta": "112 -> 394 ca",
          "badge_status": "positive"
        },
        {
          "label": "Tăng Trưởng TX T1->T2",
          "value": "x4.2",
          "delta": "47 -> 197 TX",
          "badge_status": "positive"
        },
        {
          "label": "Chạy 1 Ca Rồi Thôi",
          "value": "55.8%",
          "delta": "58 tài xế",
          "badge_status": "negative"
        },
        {
          "label": "Quay Lại ≥ 2 Ngày",
          "value": "39.4%",
          "delta": "41 tài xế",
          "badge_status": "positive"
        }
      ],
      "cards": [
        {
          "card_id": "c9",
          "icon_badge": "🚀",
          "title": "Tăng Trưởng Quy Mô 2 Tuần Liên Tiếp",
          "bullets": [
            "Số ca đăng ký tăng 3.5 lần (từ 112 lên 394 ca), số tài xế tham gia tăng 4.2 lần (từ 47 lên 197 tài xế).",
            "Fill rate tăng từ 79.7% lên 84.1% (+4.4%), cho thấy nhu cầu đơn hàng Hub được đáp ứng tốt hơn."
          ]
        },
        {
          "card_id": "c10",
          "icon_badge": "🔄",
          "title": "Thách Thức Retention & Gắn Kết Mới",
          "bullets": [
            "55.8% tài xế (58 TX) chỉ chạy đúng 1 ca rồi ngừng -> Cần tạo điểm chạm training & hướng dẫn chạy Hub lần đầu.",
            "44.2% tài xế quay lại chạy >= 2 ca; 17.3% tài xế (18 TX) trung thành quay lại >= 3 ngày khác nhau."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "Chỉ Số Retention Hub",
          "Tuần 1 (4-9/8)",
          "Tuần 2 (10-16/8)",
          "Mức Thay Đổi"
        ],
        "rows": [
          [
            "Ca đăng ký",
            "112",
            "394",
            "×3.5 🚀 Tăng nhanh"
          ],
          [
            "Tài xế tham gia",
            "47",
            "197",
            "×4.2 🚀 Tăng nhanh"
          ],
          [
            "Check-in rate",
            "50.9%",
            "49.5%",
            "≈ Ổn định"
          ],
          [
            "Năng suất (đơn/giờ)",
            "1.96",
            "2.01",
            "≈ Ổn định"
          ],
          [
            "Fill rate",
            "79.7%",
            "84.1%",
            "+4.4% 📈 Cải thiện"
          ]
        ]
      },
      "source_slides": [
        24
      ]
    },
    {
      "slide_id": 6,
      "layout_template": "kpi-dashboard",
      "takeaway_header": "Truyền Thông & Tuyển Đội Core: Đạt Kế Hoạch Fuji & Ajinomoto, Tập Trung Tháo Gỡ Core BigC Long Biên",
      "hero_kpis": [],
      "cards": [
        {
          "card_id": "c11",
          "icon_badge": "🏆",
          "title": "Communications Highlights",
          "bullets": [
            "Thưởng baga & Tuyển Core Fuji, Ajinomoto: Đã thu thập đủ lead đăng ký theo kế hoạch.",
            "Thông báo mở lại dịch vụ tại HAN: Đã phát Noti + SMS với tần suất cao.",
            "Campaign 15.8: Setup popup, bản tin lượng đơn + chuỗi content thưởng điểm nóng, push active 2-3 tin/ngày."
          ]
        },
        {
          "card_id": "c12",
          "icon_badge": "🔴",
          "title": "Lowlights & Kế Hoạch Khắc Phục",
          "bullets": [
            "Tuyển Core BigC Long Biên chưa đạt kỳ vọng -> Tăng tần suất + mở rộng danh sách push noti (Deadline 20/8, PIC Hoa).",
            "Thông tin truyền thông Mini-hub chưa được hệ thống -> Review content & tạo flow comms chuẩn (Deadline 20/8, PIC Hoa/Khoa/Vân)."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "Hạng Mục Comms",
          "Bối Cảnh / Nguyên Nhân",
          "Hành Động Khắc Phục",
          "Deadline",
          "PIC"
        ],
        "rows": [
          [
            "Tuyển Core BigC",
            "Lead cắm chốt Long Biên chưa đạt kỳ vọng",
            "Mở rộng danh sách push noti",
            "20/8",
            "Hoa"
          ],
          [
            "Minihub Comms",
            "Thông tin chưa hệ thống hóa",
            "Tạo content & flow theo cycle",
            "20/8",
            "Hoa / Khoa / Vân"
          ]
        ]
      },
      "source_slides": [
        27
      ]
    },
    {
      "slide_id": 7,
      "layout_template": "trend",
      "takeaway_header": "Hợp Tác EV & Sự Kiện 11 Tuổi: Hoàn Tất Hợp Đồng Dat Bike, Đẩy Mạnh Gói Thuê Xe Aizen Tại SGN",
      "hero_kpis": [],
      "cards": [
        {
          "card_id": "c13",
          "icon_badge": "⚡",
          "title": "Tình Hình Chuyển Đổi Phương Tiện EV",
          "bullets": [
            "Nhu cầu tài xế quan tâm đến EV tăng từ tháng 8, tập trung mạnh nhất tại khu vực TP.HCM.",
            "Done review hợp đồng mượn xe Dat Bike; bàn giao xe Selex cho KOC mượn tư vấn tài xế NW.",
            "Gói thuê xe AIZEN: Tách blog riêng truyền thông & seeding bài viết cho tài xế SGN (Deadline 21/8, PIC Khoa/Vân)."
          ]
        },
        {
          "card_id": "c14",
          "icon_badge": "🎉",
          "title": "Pre-event Sinh Nhật Ahamove 11 Tuổi",
          "bullets": [
            "Triển khai hoạt động CHL & minigame online 'Chuyển ý tưởng - Ghép tương lai'.",
            "Tổ chức chính thức Livestream Sinh nhật Ahamove vào ngày 21/8 (PIC Khoa/Vân/Thúy, Support DM/GR Team).",
            "Lowlight: Tiến độ đàm phán deal quyền lợi Bảo hiểm cho tài xế còn chậm."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "Hạng Mục Partnership",
          "Trạng Thái Bối Cảnh",
          "Kế Hoạch Tiếp Theo",
          "Deadline",
          "PIC"
        ],
        "rows": [
          [
            "Dat Bike",
            "Review xong hợp đồng",
            "Triển khai mượn xe cho TX",
            "Hoàn thành",
            "Partnership Team"
          ],
          [
            "Selex EV",
            "Đã bàn giao xe KOC",
            "KOC tư vấn tài xế quan tâm NW",
            "Đang chạy",
            "Partnership Team"
          ],
          [
            "Thuê xe AIZEN",
            "Cần tài xế SGN hiểu rõ gói thuê",
            "Tách blog & seeding truyền thông",
            "21/8",
            "Khoa / Vân"
          ],
          [
            "Sinh nhật 11 Tuổi",
            "Pre-event Minigame đang chạy",
            "Livestream trực tiếp 21/8",
            "21/8",
            "Khoa / Vân / Thúy"
          ]
        ]
      },
      "source_slides": [
        25,
        28
      ]
    },
    {
      "slide_id": 8,
      "layout_template": "action-plan",
      "takeaway_header": "Lộ Trình Hành Động 3 Bước: Sửa Thao Tác Check-In UX, Điều Chuyển Quota Ca Sáng & Tháo Gỡ Sự Cố 2H-4H",
      "hero_kpis": [],
      "cards": [
        {
          "card_id": "c15",
          "icon_badge": "📋",
          "title": "Bước 1: Fix UX Check-In & Auto Check-In",
          "bullets": [
            "Thêm Push Notification trước giờ ca 15 phút nhắc bấm Check-in.",
            "Cấu hình Auto Check-in nếu tài xế Online và di chuyển trong phạm vi Hub đúng khung giờ ca."
          ]
        },
        {
          "card_id": "c16",
          "icon_badge": "📋",
          "title": "Bước 2: Điều Chuyển Quota Ca Tối Sang Ca Sáng 4H",
          "bullets": [
            "Cắt/giảm ca tối 18:00-20:00 (chỉ 2.26 đơn/ca), dịch chuyển quota sang ca sáng 08:00-12:00 (6.25 đơn/ca).",
            "Xây dựng điểm chạm hướng dẫn chạy Hub lần đầu để giảm tỷ lệ 55.8% tài xế bỏ sau ca 1."
          ]
        }
      ],
      "data_table": {
        "headers": [
          "STT",
          "Hành Động Cốt Lõi",
          "Mục Tiêu Kỳ Vọng",
          "Thời Gian",
          "PIC Lead"
        ],
        "rows": [
          [
            "1",
            "Thêm Push Noti 15p & Auto Check-in",
            "Khắc phục 25.6% đơn chạy ngoài ca quên check-in",
            "25/8",
            "Product / DM Team"
          ],
          [
            "2",
            "Dịch chuyển quota ca 18-20h sang ca 08-12h",
            "Tăng năng suất toàn phễu Hub lên >5 đơn/ca",
            "22/8",
            "Ops Hub Team"
          ],
          [
            "3",
            "Tập huấn & Seeding gói thuê xe AIZEN SGN",
            "Tăng nhận thức & tỷ lệ chuyển đổi xe điện EV",
            "21/8",
            "Khoa / Vân"
          ],
          [
            "4",
            "Tăng push noti tuyển Core BigC Long Biên",
            "Đảm bảo đủ lead cắm chốt Long Biên",
            "20/8",
            "Hoa"
          ]
        ]
      },
      "source_slides": [
        24,
        27,
        28,
        29
      ]
    }
  ]
}
```
