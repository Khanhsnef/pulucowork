html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Driver Ranking v2.0 - Strategy Presentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0A0A0B;
      --bg-card: #121316;
      --bg-card-hover: #1A1C20;
      --text-prime: #FFFFFF;
      --text-sec: #9CA3AF;
      --orange: #FF7F32;
      --orange-dim: rgba(255, 127, 50, 0.15);
      --yellow: #F59E0B;
      --yellow-dim: rgba(245, 158, 11, 0.15);
      --blue: #3B82F6;
      --blue-dim: rgba(59, 130, 246, 0.15);
      --green: #10B981;
      --green-dim: rgba(16, 185, 129, 0.15);
      --purple: #8B5CF6;
      --purple-dim: rgba(139, 92, 246, 0.15);
      --red: #EF4444;
      --red-dim: rgba(239, 68, 68, 0.15);
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: var(--text-prime); overflow: hidden; }

    .slides-container { width: 100vw; height: 100vh; position: relative; overflow: hidden; }
    .slide {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      display: flex; flex-direction: column; justify-content: center; align-items: center;
      padding: 40px; opacity: 0; transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1);
      transform: translateY(50px) scale(0.95); pointer-events: none;
    }
    .slide.active { opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; }
    .slide.prev { transform: translateY(-50px) scale(0.95); }

    .slide-content { width: 100%; max-width: 1200px; }

    h1 { font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 48px; line-height: 1.2; margin-bottom: 12px; letter-spacing: -0.02em; }
    
    .gradient-text { background: linear-gradient(135deg, var(--orange) 0%, var(--yellow) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-blue { background: linear-gradient(135deg, var(--blue) 0%, #60A5FA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    p.lead { font-size: 20px; color: var(--text-sec); margin-bottom: 32px; max-width: 900px; line-height: 1.5; }

    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    
    .card { background: var(--bg-card); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 24px; position: relative; overflow: hidden; }
    .card-icon { font-size: 32px; margin-bottom: 16px; }
    .card h3 { font-family: 'Montserrat', sans-serif; font-size: 20px; font-weight: 700; margin-bottom: 12px; }
    .card p, .card li { color: var(--text-sec); font-size: 15px; line-height: 1.6; }
    
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .kpi-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 16px; border-radius: 12px; }
    .kpi-label { font-size: 11px; color: var(--text-sec); text-transform: uppercase; font-weight: 600; margin-bottom: 8px; letter-spacing: 0.05em; }
    .kpi-value { font-size: 28px; font-weight: 800; font-family: 'Montserrat', sans-serif; }
    .kpi-delta { font-size: 12px; margin-top: 4px; color: var(--text-sec); }

    .data-table { width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 14px; background: rgba(255,255,255,0.02); border-radius: 12px; overflow: hidden; }
    .data-table th, .data-table td { padding: 14px 16px; border: 1px solid rgba(255,255,255,0.05); text-align: left; }
    .data-table th { background: rgba(255,255,255,0.05); color: #fff; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 0.05em; }
    .data-table td { color: var(--text-sec); }
    .data-table td strong { color: #fff; }
    
    .insight-bar { background: var(--blue-dim); border-left: 4px solid var(--blue); padding: 16px 20px; border-radius: 8px; font-size: 14px; margin-top: 16px; color: #DBEAFE; line-height: 1.6; }
    
    .nav { position: fixed; bottom: 30px; right: 40px; display: flex; gap: 12px; z-index: 100; }
    .nav-btn { background: rgba(255,255,255,0.1); border: none; color: white; width: 48px; height: 48px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }
    .nav-btn:hover { background: rgba(255,255,255,0.2); }
    
    .progress-container { position: fixed; top: 0; left: 0; width: 100%; height: 4px; background: rgba(255,255,255,0.1); z-index: 100; }
    .progress-bar { height: 100%; background: var(--orange); width: 0%; transition: width 0.4s ease; }

    .loop-container { position: relative; width: 100%; max-width: 700px; margin: 0 auto; height: 350px; display: flex; justify-content: center; align-items: center; }
    .loop-node { position: absolute; background: var(--bg-card); border: 1px solid rgba(255,255,255,0.1); padding: 16px 24px; border-radius: 12px; text-align: center; font-weight: 600; width: 220px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); z-index: 2; font-size: 14px;}
    .n-top { top: 0; }
    .n-right { right: 0; top: 50%; transform: translateY(-50%); }
    .n-bottom { bottom: 0; }
    .n-left { left: 0; top: 50%; transform: translateY(-50%); }
    .loop-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none; }
  </style>
</head>
<body>

  <div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>

  <div class="slides-container">
    
    <!-- SLIDE 1 -->
    <div class="slide active">
      <div class="slide-content" style="max-width: 900px; text-align: center;">
        <h1 style="font-size: 64px;">Sự bế tắc của hệ thống <span class="gradient-text-blue">Ranking cũ</span></h1>
        <p class="lead" style="margin: 0 auto 48px;">Vì sao tài xế không còn mặn mà với việc thăng hạng?</p>
        
        <div class="grid-2" style="text-align: left;">
          <div class="card" style="border-top: 4px solid var(--red);">
            <div class="card-icon">🎭</div>
            <h3>Hữu danh vô thực</h3>
            <p>Hệ thống hiện tại <strong>chưa phản ánh đúng chất lượng tài xế</strong>. Không có chỉ số DQS (Driver Quality Score) làm thước đo, dẫn đến việc tài xế chạy nhiều nhưng thái độ kém vẫn hưởng lợi.</p>
          </div>
          <div class="card" style="border-top: 4px solid var(--orange);">
            <div class="card-icon">🌫️</div>
            <h3>Quyền lợi mờ nhạt</h3>
            <p>Khoảng cách đặc quyền giữa các Rank <strong>không đủ rõ ràng</strong>. Tài xế không thấy lợi ích sống còn, dẫn đến mất động lực phấn đấu để thăng hạng hoặc duy trì thứ hạng.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- SLIDE 2 -->
    <div class="slide">
      <div class="slide-content">
        <h1>Giải pháp: Đưa <span class="gradient-text">DQS</span> vào lõi hệ thống</h1>
        <p class="lead">Tái định nghĩa lại Ranking: Chất lượng là vé vào cửa. Thang điểm tích hợp thay thế cho AR/FR đơn lẻ.</p>
        
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-label">Chu kỳ kiểm tra</div>
            <div class="kpi-value" style="color: #fff;">Cuối tháng</div>
            <div class="kpi-delta">Rolling 30 ngày</div>
          </div>
          <div class="kpi-card" style="border-bottom: 3px solid var(--green);">
            <div class="kpi-label">Cập nhật KPI</div>
            <div class="kpi-value" style="color: var(--green);">Mỗi ngày</div>
            <div class="kpi-delta">Realtime live tracking</div>
          </div>
          <div class="kpi-card" style="border-bottom: 3px solid var(--orange);">
            <div class="kpi-label">Ngưỡng R1 DQS</div>
            <div class="kpi-value" style="color: var(--orange);">≥ 80</div>
            <div class="kpi-delta">Kèm Prod ≥ 280 stp</div>
          </div>
          <div class="kpi-card" style="border-bottom: 3px solid var(--yellow);">
            <div class="kpi-label">Ngưỡng R2 DQS</div>
            <div class="kpi-value" style="color: var(--yellow);">≥ 75</div>
            <div class="kpi-delta">Kèm Prod ≥ 210 stp</div>
          </div>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th>KPI Chỉ Số</th>
              <th style="color:var(--orange);">💎 R1 Elite / Kim Cương</th>
              <th style="color:var(--yellow);">🥇 R2 Active / Vàng</th>
              <th style="color:var(--blue);">🥈 R3 Standard / Bạc</th>
              <th>Unranked</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Thang điểm tích hợp (DQS)</strong></td>
              <td style="color:var(--orange); font-weight:700;">≥ 80</td>
              <td style="color:var(--yellow); font-weight:700;">≥ 75</td>
              <td style="color:var(--blue); font-weight:700;">≥ 75</td>
              <td style="color:var(--red);"> < 75 </td>
            </tr>
            <tr>
              <td><strong>Năng suất (Productivity)</strong></td>
              <td>≥ 280 stp/tháng</td>
              <td>≥ 210 stp/tháng</td>
              <td>≥ 70 stp/tháng</td>
              <td>—</td>
            </tr>
            <tr>
              <td><strong>Cấp bậc Layer ưu tiên</strong></td>
              <td>L2 Minizone</td>
              <td>L3 Mediumzone</td>
              <td>L4 Bigzone</td>
              <td>L6 MASS</td>
            </tr>
          </tbody>
        </table>

        <div class="insight-bar">
          <strong>💡 Thay đổi chiến lược:</strong> Việc chuyển dịch sang DQS giúp đồng bộ chất lượng Tài xế, đánh giá toàn diện dựa trên phản hồi khách hàng, tỷ lệ hoàn thành thay vì chỉ đếm số cuốc. Hệ thống xét duyệt tự động từ cao xuống thấp (R1 → R2 → R3), lọc ra nhóm đối tác xuất sắc nhất.
        </div>
      </div>
    </div>

    <!-- SLIDE 3 -->
    <div class="slide">
      <div class="slide-content">
        <h1>Phân quyền & <span class="gradient-text">Lực hút Layer</span></h1>
        <p class="lead">Biến "Ưu tiên đăng ký ca" thành quyền lợi sinh sát. Hệ thống Layer trở thành thỏi nam châm hút tài xế.</p>
        
        <div class="grid-2" style="align-items: center; gap: 40px;">
          <div>
            <div class="kpi-grid" style="grid-template-columns: 1fr 1fr; margin-bottom: 16px;">
              <div class="kpi-card" style="background: rgba(255,127,50,0.1); border-color: rgba(255,127,50,0.3);">
                <div class="kpi-label" style="color: var(--orange);">R1 Mở Cổng</div>
                <div class="kpi-value" style="color: var(--orange);">00:00</div>
                <div class="kpi-delta">Bao trọn khung giờ ngon</div>
              </div>
              <div class="kpi-card" style="background: rgba(245,158,11,0.1); border-color: rgba(245,158,11,0.3);">
                <div class="kpi-label" style="color: var(--yellow);">R2 Mở Cổng</div>
                <div class="kpi-value" style="color: var(--yellow);">10:00</div>
                <div class="kpi-delta">Pick slot sau R1</div>
              </div>
            </div>
            
            <table class="data-table" style="font-size: 13px;">
              <thead>
                <tr>
                  <th>Hạng Tài Xế</th>
                  <th>Phạm vi Layer</th>
                  <th>Cơ chế AhaPoints</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong style="color:var(--orange);">💎 R1 Elite</strong></td>
                  <td>Tất cả L2 - L6</td>
                  <td>L2: <strong style="color:var(--green);">×1.5</strong> | L3: <strong style="color:var(--green);">×1.3</strong></td>
                </tr>
                <tr>
                  <td><strong style="color:var(--yellow);">🥇 R2 Active</strong></td>
                  <td>Tất cả L2 - L6</td>
                  <td>L2: <strong style="color:var(--green);">×1.5</strong> | L3: <strong style="color:var(--green);">×1.3</strong></td>
                </tr>
                <tr>
                  <td><strong style="color:var(--blue);">🥈 R3 Standard</strong></td>
                  <td>Tất cả L2 - L6</td>
                  <td>L4: <strong style="color:var(--green);">×1.1</strong></td>
                </tr>
                <tr>
                  <td><strong style="color:var(--text-sec);">👤 Unranked</strong></td>
                  <td>Chỉ L6 MASS</td>
                  <td>Hệ số ×1.0</td>
                </tr>
              </tbody>
            </table>
            
            <div class="insight-bar" style="margin-top: 0;">
              <strong>💡 Nguyên lý thiết kế:</strong> Tài xế tự do chọn Layer. Tuy nhiên, Layer L2/L3 có hệ số nhân điểm AhaPoints cực cao (x1.5), tạo thành thỏi nam châm thu hút tài xế tập trung phục vụ tại các vùng trung tâm đông đúc, giải bài toán thiếu hụt cung.
            </div>
          </div>

          <!-- Pyramid SVG simplified for dark mode -->
          <div style="background: var(--bg-card); border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
             <svg viewBox="0 0 350 350" width="100%" height="auto">
                <polygon points="175,20 220,100 130,100" fill="url(#grad-r1)" />
                <polygon points="120,110 230,110 260,190 90,190" fill="url(#grad-r2)" />
                <polygon points="80,200 270,200 300,280 50,280" fill="url(#grad-r3)" />
                <polygon points="40,290 310,290 340,340 10,340" fill="url(#grad-un)" />
                
                <text x="175" y="75" fill="#fff" font-size="14" font-weight="800" text-anchor="middle">💎 R1</text>
                <text x="175" y="155" fill="#fff" font-size="14" font-weight="800" text-anchor="middle">🥇 R2</text>
                <text x="175" y="245" fill="#fff" font-size="14" font-weight="800" text-anchor="middle">🥈 R3</text>
                <text x="175" y="320" fill="#fff" font-size="14" font-weight="800" text-anchor="middle">👤 UNRANKED</text>
                
                <defs>
                  <linearGradient id="grad-r1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FF7F32"/><stop offset="100%" stop-color="#D84315"/></linearGradient>
                  <linearGradient id="grad-r2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#F59E0B"/><stop offset="100%" stop-color="#B45309"/></linearGradient>
                  <linearGradient id="grad-r3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3B82F6"/><stop offset="100%" stop-color="#1D4ED8"/></linearGradient>
                  <linearGradient id="grad-un" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4B5563"/><stop offset="100%" stop-color="#1F2937"/></linearGradient>
                </defs>
             </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- SLIDE 4 -->
    <div class="slide">
      <div class="slide-content">
        <h1 style="text-align: center;">Hệ sinh thái <span class="gradient-text">Ràng buộc chặt chẽ</span></h1>
        <p class="lead" style="text-align: center; margin: 0 auto 48px;">Một vòng lặp khép kín khiến tài xế tự vận động trong khuôn khổ của nền tảng.</p>
        
        <div class="loop-container">
          <svg class="loop-svg" viewBox="0 0 700 350" preserveAspectRatio="none">
            <path d="M 350 30 Q 670 30 670 175 Q 670 320 350 320 Q 30 320 30 175 Q 30 30 350 30" fill="none" stroke="var(--blue)" stroke-width="2" stroke-dasharray="8,8" opacity="0.5"/>
          </svg>
          
          <div class="loop-node n-top" style="border-top: 4px solid var(--purple);">
            <div style="font-size: 20px; margin-bottom: 4px;">🎁</div>
            Muốn hưởng<br><strong style="color:var(--purple);">Benefit x1.5 ngon</strong>
          </div>
          <div class="loop-node n-right" style="border-right: 4px solid var(--yellow);">
            <div style="font-size: 20px; margin-bottom: 4px;">📍</div>
            Bắt buộc phải chọn<br><strong style="color:var(--yellow);">Layer L2/L3</strong>
          </div>
          <div class="loop-node n-bottom" style="border-bottom: 4px solid var(--orange);">
            <div style="font-size: 20px; margin-bottom: 4px;">⏰</div>
            Slot ít, phải<br><strong style="color:var(--orange);">Giành mở cổng sớm</strong>
          </div>
          <div class="loop-node n-left" style="border-left: 4px solid var(--green);">
            <div style="font-size: 20px; margin-bottom: 4px;">⭐</div>
            Mở sớm phải có<strong style="color:var(--blue);"> Rank Cao</strong><br>
            <span style="font-size:11px;color:var(--text-sec);">(Duy trì DQS & Năng suất)</span>
          </div>
        </div>
      </div>
    </div>

    <!-- SLIDE 5 -->
    <div class="slide">
      <div class="slide-content">
        <h1>Bản đồ <span class="gradient-text-blue">Hiện thực hóa giá trị</span></h1>
        <p class="lead">Tác động rõ rệt từ sự chuyển dịch mô hình.</p>
        
        <table class="data-table" style="font-size: 15px;">
          <thead>
            <tr>
              <th style="width:25%;">Hiện trạng cũ</th>
              <th style="width:25%;">Giải pháp v2.0</th>
              <th style="width:50%;">Tác động (Business Impact)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Ranking không phản ánh chất lượng, tài xế chỉ cần cày số lượng.</td>
              <td><strong style="color:var(--blue);">TIÊU CHUẨN HÓA</strong><br><span style="font-size:13px;">Đưa DQS làm lõi tiên quyết</span></td>
              <td><strong style="color:var(--green);">Sàng lọc tự nhiên</strong>, triệt tiêu rủi ro gian lận, tăng chất lượng dịch vụ (SLA) toàn hệ thống.</td>
            </tr>
            <tr>
              <td>Quyền lợi các Rank na ná nhau, thiếu sự khác biệt.</td>
              <td><strong style="color:var(--orange);">PHÂN QUYỀN ƯU TIÊN</strong><br><span style="font-size:13px;">Ưu tiên giờ mở cổng theo Rank</span></td>
              <td>Tạo sự phân cấp gay gắt. <strong style="color:var(--green);">Đảm bảo tài xế xuất sắc nhất luôn có việc làm tốt nhất.</strong></td>
            </tr>
            <tr>
              <td>Điều phối cung khó khăn, ép tài xế chạy theo vùng gây ức chế.</td>
              <td><strong style="color:var(--yellow);">LỰC HÚT LAYER</strong><br><span style="font-size:13px;">Hệ số AhaPoints làm mồi nhử</span></td>
              <td><strong style="color:var(--green);">Tài xế tự nguyện đổ về các Layer trọng điểm</strong> (L2/L3), giải bài toán thiếu hụt cung tại Peak-hour.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <div class="nav">
    <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)">❮</button>
    <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">❯</button>
  </div>

  <script>
    const slides = document.querySelectorAll('.slide');
    const progressBar = document.getElementById('progressBar');
    let currentSlide = 0;

    function updateSlide() {
      slides.forEach((slide, index) => {
        slide.className = 'slide';
        if (index === currentSlide) slide.classList.add('active');
        else if (index < currentSlide) slide.classList.add('prev');
      });
      progressBar.style.width = `${((currentSlide) / (slides.length - 1)) * 100}%`;
    }

    function changeSlide(dir) {
      currentSlide = Math.max(0, Math.min(slides.length - 1, currentSlide + dir));
      updateSlide();
    }

    document.addEventListener('keydown', (e) => {
      if (['ArrowRight', 'ArrowDown', ' '].includes(e.key)) changeSlide(1);
      else if (['ArrowLeft', 'ArrowUp'].includes(e.key)) changeSlide(-1);
    });
    updateSlide();
  </script>
</body>
</html>
