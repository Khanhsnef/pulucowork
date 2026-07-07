import re

with open("2026-05-driver-ranking-params.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Sidebar
sidebar_new = """      <ul>
        <li><a href="#s1">01. Ranking KPI Thresholds</a></li>
        <li><a href="#s2">02. Layer Access & Priority</a></li>
        <li><a href="#s3">03. Quyền lợi theo Rank</a></li>
        <li><a href="#s4">04. Quyền lợi theo Layer</a></li>
        <li><a href="#s5">05. AhaBenefits Catalog</a></li>
        <li><a href="#s6">06. Bảng Tổng Hợp</a></li>
        <li><a href="#s7">07. Timeline Triển Khai</a></li>
      </ul>"""

content = re.sub(r'<ul>.*?</ul>', sidebar_new, content, flags=re.DOTALL, count=1)

# 2. Extract sections
sections_raw = re.findall(r'(<section id="s\d+">.*?</section>)', content, re.DOTALL)
s_kpi = sections_raw[0]
s_layer = sections_raw[2]
s_rank_ben = sections_raw[3]
s_layer_ben = sections_raw[5]
s_catalog = sections_raw[6]
s_summary = sections_raw[7]

# 3. Modify S2: Layer Access (old S3)
s_layer = re.sub(r'<section id="s\d+">', '<section id="s2">', s_layer)
s_layer = re.sub(r'<div class="sec-num">.*?</div>', '<div class="sec-num">02</div>', s_layer)
s_layer = re.sub(r'<h2>Layer Access & Priority</h2>\s*<p>.*?</p>', 
                 '<h2>Layer Access & Priority</h2>\n          <p>Tài xế mọi Rank đều được đăng ký vào tất cả các zone — ưu tiên theo khung giờ</p>', s_layer)

# Replace table in Layer Access with the new table from MD
layer_table = """
      <div class="tw" style="margin-bottom:16px;">
        <table>
          <thead>
            <tr>
              <th style="min-width:130px;">Rank</th>
              <th>Zone được phép đăng ký</th>
              <th style="color:var(--purple);">Giờ mở cổng (Ngày 1)</th>
              <th>Ghi chú ưu tiên</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="rank-r1">💎 R1 Elite</span></td>
              <td>Tất cả (L2 - L6)</td>
              <td><strong style="color:var(--orange);">00:00 - 10:00</strong></td>
              <td class="good">Ưu tiên tuyệt đối FCFS</td>
            </tr>
            <tr>
              <td><span class="rank-r2">🥇 R2 Active</span></td>
              <td>Tất cả (L2 - L6)</td>
              <td><strong style="color:var(--yellow);">10:00 - 14:00</strong></td>
              <td class="good">Ưu tiên sau R1</td>
            </tr>
            <tr>
              <td><span class="rank-r3">🥈 R3 Standard</span></td>
              <td>Tất cả (L2 - L6)</td>
              <td><strong style="color:var(--blue);">14:00 - 24:00</strong></td>
              <td class="good">Ưu tiên sau R2</td>
            </tr>
            <tr>
              <td><span class="rank-un">Unranked</span></td>
              <td>L6 MASS (slot trống còn lại)</td>
              <td><strong style="color:var(--text-sec);">Ngày 2+</strong></td>
              <td class="warn">Chỉ đăng ký slot thừa</td>
            </tr>
          </tbody>
        </table>
      </div>
"""
s_layer = re.sub(r'<div class="tw".*?</table>\s*</div>', layer_table, s_layer, flags=re.DOTALL)


# 4. Modify S3: Quyền lợi theo Rank (old S4/S5)
s_rank_ben = re.sub(r'<section id="s\d+">', '<section id="s3">', s_rank_ben)
s_rank_ben = re.sub(r'<div class="sec-num">.*?</div>', '<div class="sec-num">03</div>', s_rank_ben)


# 5. Modify S4: Quyền lợi theo Layer (old S6/S7)
s_layer_ben = re.sub(r'<section id="s\d+">', '<section id="s4">', s_layer_ben)
s_layer_ben = re.sub(r'<div class="sec-num">.*?</div>', '<div class="sec-num">04</div>', s_layer_ben)
s_layer_ben = re.sub(r'<h2>.*?</h2>', '<h2>Quyền lợi theo Layer (AhaBenefits)</h2>', s_layer_ben)


# 6. Modify S5: AhaBenefits Catalog (old S7/S8)
s_catalog = re.sub(r'<section id="s\d+">', '<section id="s5">', s_catalog)
s_catalog = re.sub(r'<div class="sec-num">.*?</div>', '<div class="sec-num">05</div>', s_catalog)


# 7. Modify S6: Bảng Tổng Hợp (old S8/S9)
s_summary = re.sub(r'<section id="s\d+">', '<section id="s6">', s_summary)
s_summary = re.sub(r'<div class="sec-num">.*?</div>', '<div class="sec-num">06</div>', s_summary)
# Rename the internal subtitles 9.1 -> 6.1, 9.2 -> 6.2, 9.3 -> 6.3
s_summary = s_summary.replace("9.1 Theo Rank", "6.1 Theo Rank")
s_summary = s_summary.replace("9.2 Theo Layer", "6.2 Theo Layer")
s_summary = s_summary.replace("9.3 Theo Ca làm việc", "6.3 Theo Ca làm việc (Reference)")


# 8. Create S7: Timeline Triển Khai
s_timeline = """
    <!-- ── S7: TIMELINE ── -->
    <section id="s7">
      <div class="sec-hdr">
        <div class="sec-num">07</div>
        <div class="sec-title">
          <h2>Timeline Triển Khai (Dự kiến 3 tháng tới)</h2>
          <p>Lộ trình áp dụng Ranking & Benefits v2.0</p>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:16px;">
        
        <!-- Tháng 1 -->
        <div style="background:var(--bg-card);border-left:4px solid var(--blue);border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.2);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:16px;font-weight:700;color:var(--text-prime);">Tháng 1: Truyền thông & Đào tạo</div>
            <div style="font-size:12px;font-weight:600;color:var(--blue);background:var(--blue-dim);padding:4px 8px;border-radius:4px;">Tháng 5/2026</div>
          </div>
          <ul style="margin:0;padding-left:20px;font-size:13px;color:var(--text-sec);line-height:1.6;">
            <li>Công bố bộ tiêu chí Ranking mới (Chuyển sang dùng <strong>DQS</strong> thay vì bộ chỉ số cũ).</li>
            <li>Đào tạo tài xế về hệ thống điểm AhaPoints và Catalog đặc quyền.</li>
            <li>Thu thập feedback và tinh chỉnh UI/UX trên app.</li>
          </ul>
        </div>

        <!-- Tháng 2 -->
        <div style="background:var(--bg-card);border-left:4px solid var(--yellow);border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.2);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:16px;font-weight:700;color:var(--text-prime);">Tháng 2: Shadow Mode (Chạy ngầm)</div>
            <div style="font-size:12px;font-weight:600;color:var(--yellow);background:var(--yellow-dim);padding:4px 8px;border-radius:4px;">Tháng 6/2026</div>
          </div>
          <ul style="margin:0;padding-left:20px;font-size:13px;color:var(--text-sec);line-height:1.6;">
            <li>Hệ thống tính điểm DQS chạy thực tế, hiển thị Rank dự kiến trên app nhưng <strong>chưa áp dụng chặn đăng ký Layer</strong>.</li>
            <li>Tài xế làm quen với cơ chế ưu tiên theo khung giờ (Priority Registration Window).</li>
            <li>Bắt đầu phát sinh AhaPoints (nhưng chưa cho phép đổi quà thực tế).</li>
          </ul>
        </div>

        <!-- Tháng 3 -->
        <div style="background:var(--bg-card);border-left:4px solid var(--orange);border-radius:8px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.2);">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-size:16px;font-weight:700;color:var(--text-prime);">Tháng 3: Triển khai Chính thức</div>
            <div style="font-size:12px;font-weight:600;color:var(--orange);background:var(--orange-dim);padding:4px 8px;border-radius:4px;">Tháng 7/2026</div>
          </div>
          <ul style="margin:0;padding-left:20px;font-size:13px;color:var(--text-sec);line-height:1.6;">
            <li>Áp dụng hoàn toàn cơ chế: R1 mở cổng đăng ký từ 00:00, R2 từ 10:00, R3 từ 14:00.</li>
            <li>Kích hoạt <strong>AhaBenefits Catalog</strong>, cho phép tài xế đổi AhaPoints lấy Voucher, Data, Bảo hiểm...</li>
            <li>Bắt đầu chu kỳ đánh giá và hết hạn điểm theo Quý.</li>
          </ul>
        </div>

      </div>
    </section>
"""

# Reconstruct Main
main_start = content.find('<main>') + 6
main_end = content.find('</main>')

new_main = f"\n    {s_kpi}\n\n    {s_layer}\n\n    {s_rank_ben}\n\n    {s_layer_ben}\n\n    {s_catalog}\n\n    {s_summary}\n\n{s_timeline}\n  "
content = content[:main_start] + new_main + content[main_end:]

with open("2026-05-driver-ranking-params.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Done parsing and rewriting!")
