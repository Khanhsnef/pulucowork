# 📁 TEMPLATES — Pulu Workspace

Thư mục này chứa các template dùng lại cho các dự án tương lai.

---

## 🎨 Presentation Dark Slide Template

**File:** `presentation-dark-slide-template.html`
**Nguồn gốc:** Driver Ranking & AhaBenefits v2.0 (2026-07)

### Mô tả
Template slide thuyết trình dạng fullscreen, dark mode cao cấp. Hỗ trợ điều hướng bằng bàn phím (←→ hoặc Space) và thanh progress bar tự động.

### Tính năng
- 🌑 Dark mode glassmorphism, font Montserrat + Inter (Google Fonts)
- ⌨️ Điều hướng bằng phím mũi tên / Space / PageUp/Down
- 📊 Progress bar đầu trang tự động theo dõi vị trí slide
- 🎨 Bảng màu nhất quán: Orange (R1/highlight), Yellow (R2), Blue (R3/accent), Green (positive)
- 📋 Bảng dữ liệu `.data-table` đẹp với hover effect
- 🔲 Grid layout 2 cột `.grid-2` cho so sánh song song
- 📦 KPI cards `.kpi-grid` / `.kpi-card` cho số liệu tổng hợp
- 💡 Insight bar (blue left-border callout)
- 📣 Infobox callout
- 🔷 Timeline boxes `.tl-box` cho lộ trình triển khai
- 🔄 Loop diagram (SVG dashed ellipse + 4 node cards)
- 🔺 Pyramid SVG (3 cấp R1/R2/R3)

### Cách dùng lại
1. Copy file `presentation-dark-slide-template.html` ra thư mục dự án mới
2. Đổi tên theo convention: `YYYY-MM-tên-dự-án-presentation.html`
3. Thay thế nội dung từng slide — giữ nguyên cấu trúc CSS & JS
4. Thêm/bớt slide bằng cách clone block `<div class="slide">...</div>`
5. Số slide trong progress bar tự động cập nhật theo số `<div class="slide">` trong DOM

### CSS Variables (có thể tuỳ chỉnh nhanh)
```css
:root {
  --bg: #0A0A0B;          /* Nền chính */
  --bg-card: #111114;     /* Nền card */
  --orange: #FF7F32;      /* Màu nhấn chính / R1 */
  --yellow: #F59E0B;      /* Màu R2 */
  --blue: #3B82F6;        /* Màu accent / R3 */
  --green: #10B981;       /* Positive */
  --purple: #A855F7;      /* Highlight đặc biệt */
  --red: #EF4444;         /* Negative */
}
```
