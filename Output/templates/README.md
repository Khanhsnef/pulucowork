# Slide Templates

3 theme CSS chuẩn cho HTML slides Ahamove. Mỗi file có preview component + toàn bộ CSS variables sẵn sàng copy.

## Themes

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
