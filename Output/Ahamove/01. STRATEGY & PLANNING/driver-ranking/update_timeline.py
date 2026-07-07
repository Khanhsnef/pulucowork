import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

new_timeline = """<!-- Giai đoạn 1 -->
        <div style="background:var(--bg-card);border-left:4px solid var(--blue);border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.2);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:16px;font-weight:700;color:var(--text-prime);">Giai đoạn 1: Chuẩn bị & Phát triển</div>
            <div style="font-size:12px;font-weight:600;color:var(--blue);background:var(--blue-dim);padding:4px 8px;border-radius:4px;">Giữa Tháng 7/2026</div>
          </div>
          <ul style="margin:0;padding-left:20px;font-size:13px;color:var(--text-sec);line-height:1.6;">
            <li>Điều chỉnh ranking, apply <strong>DQS</strong>, truyền thông, đào tạo, chỉnh sửa các document.</li>
            <li>Xây dựng <strong>AhaBenefits</strong> song song, xây dựng cơ chế ưu tiên đăng ký/tự động mở ca.</li>
          </ul>
        </div>

        <!-- Giai đoạn 2 -->
        <div style="background:var(--bg-card);border-left:4px solid var(--yellow);border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.2);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:16px;font-weight:700;color:var(--text-prime);">Giai đoạn 2: Shadow Mode (Chạy ngầm)</div>
            <div style="font-size:12px;font-weight:600;color:var(--yellow);background:var(--yellow-dim);padding:4px 8px;border-radius:4px;">Tháng 8/2026</div>
          </div>
          <ul style="margin:0;padding-left:20px;font-size:13px;color:var(--text-sec);line-height:1.6;">
            <li>Hệ thống tính điểm DQS chạy thực tế, hiển thị Rank dự kiến trên app nhưng chưa áp dụng chặn đăng ký Layer.</li>
            <li>Chạy test ở <strong>HAN</strong> trước, sau đó triển khai mở rộng ở <strong>SGN</strong>.</li>
          </ul>
        </div>

        <!-- Giai đoạn 3 -->
        <div style="background:var(--bg-card);border-left:4px solid var(--orange);border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.2);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:16px;font-weight:700;color:var(--text-prime);">Giai đoạn 3: Triển khai Chính thức</div>
            <div style="font-size:12px;font-weight:600;color:var(--orange);background:var(--orange-dim);padding:4px 8px;border-radius:4px;">Tháng 9/2026</div>
          </div>
          <ul style="margin:0;padding-left:20px;font-size:13px;color:var(--text-sec);line-height:1.6;">
            <li>Triển khai Chính thức, đồng bộ áp dụng <strong>AhaBenefits</strong>.</li>
            <li>Kích hoạt cổng đổi điểm lấy Voucher, Data, Bảo hiểm, Công cụ dụng cụ...</li>
          </ul>
        </div>"""

content = re.sub(r'<!-- Tháng 1 -->.*<!-- Tháng 3 -->.*?</ul>\s*</div>', new_timeline, content, flags=re.DOTALL)

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)

