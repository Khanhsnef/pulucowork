# Templates

CSS chuẩn cho HTML outputs Ahamove — slides và analytics reports. Mỗi file có preview component sẵn sàng copy.

## Analytics Report Template (mới)

| File | Theme | Dùng khi |
|------|-------|----------|
| [analytics-report.html](analytics-report.html) | Light · bg-gray-50 · Lexend + Space Mono | Báo cáo phân tích data dài, deep dive, dashboard cuộn được |

**Components có sẵn** (Ctrl+F theo số `[1]`–`[15]`):
- `[3]` Section block với số thứ tự (01, 02...)
- `[4]` KPI strip 4 metrics + delta badge
- `[7]` Insight box: `.ok` / `.warn` / `.danger` / `.blue`
- `[8]` Data table + badge hệ màu chuẩn
- `[9]` Progress bar (horizontal, 4 màu)
- `[10]` SVG line chart (không cần thư viện)
- `[11]` SVG bar chart ngang
- `[12]` Heatmap table (JS color mapping)
- `[13]` Correlation bar
- `[14]` Grid 2/3/4 col responsive

## Slide Themes

| File | Nền | Vibe | Dùng khi |
|------|-----|------|----------|
| [slide-theme-dark.html](slide-theme-dark.html) | `#080F1D` deep navy | Premium fintech, dark dashboard | Present nội bộ, demo sản phẩm, impact mạnh |
| [slide-theme-navy.html](slide-theme-navy.html) | `#1A2E48` mid navy | Corporate premium, balanced | Báo cáo lãnh đạo, meeting formal |
| [slide-theme-light.html](slide-theme-light.html) | `#F2F4F8` xám nhạt | Consulting, clean, printable | Tài liệu chia sẻ, in ấn, external |

## Cấu trúc mỗi theme

```
slide-theme-XXX.html
├── :root { --variables }   ← Tất cả màu/spacing dưới dạng CSS variables
├── Base styles             ← Body, slide shell, bg, grid, accent-line
├── Header styles           ← eyebrow, title, subtitle, slide-num
├── Card styles             ← .glass (dark/navy) hoặc .card (light)
├── Typography              ← label-xs, num-hero/lg/md, body-sm
├── Components              ← pill, prog-track, sep, hero, survival, actions, footer
└── Preview HTML            ← Mini demo để xem trực tiếp trong browser
```

## Cách dùng

1. Mở file theme muốn dùng, copy toàn bộ `<style>...</style>`
2. Paste vào `<head>` của slide HTML mới
3. Dùng các class: `.card` / `.glass`, `.label-xs`, `.num-lg`, `.pill-warn`, `.pill-ok`, v.v.
4. Tham chiếu màu qua `var(--accent-orange)`, `var(--text-primary)`, v.v.

## Shared layout classes (giống nhau ở cả 3 themes)

```
.s1-body  → grid 3 cột slide 1 (hero + 2 city cards + insight)
.s2-body  → grid 2 cột slide 2 (chart + survival + actions)
.s-header → flex header row
.s-footer → flex footer row
```
