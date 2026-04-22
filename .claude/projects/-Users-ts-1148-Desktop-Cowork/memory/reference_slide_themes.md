---
name: slide-themes
description: 3 CSS theme presets cho HTML slides Ahamove — dark/navy/light, với preview và CSS variables
type: reference
---

Ba theme HTML slide đã build sẵn, lưu tại `output/templates/`:

| Theme | File | Nền | Đặc điểm |
|-------|------|-----|----------|
| **DARK** | `output/templates/slide-theme-dark.html` | `#080F1D` | Glassmorphism `.glass`, text trắng opacity thấp, glow effects |
| **NAVY** | `output/templates/slide-theme-navy.html` | `#1A2E48` | Glassmorphism `.glass`, text trắng opacity cao, contrast tốt hơn dark |
| **LIGHT** | `output/templates/slide-theme-light.html` | `#F2F4F8` | White `.card` + shadow, text tối `#0A1828`, printable |

**How to apply:** Copy `<style>` block từ file theme vào slide HTML mới. Mọi màu sắc đều là CSS `--variables` trong `:root`.

**Shared components (cả 3 themes):**
- `.label-xs`, `.num-hero`, `.num-lg`, `.num-md`, `.body-sm`
- `.pill-warn`, `.pill-ok`, `.pill-info`, `.pill-blue`
- `.prog-track` / `.prog-fill`, `.sep`
- `.surv-block.han` / `.surv-block.sgn` — survival rate blocks
- `.act-item`, `.act-num`, `.act-txt` — action items
- `.s-header`, `.s-footer`, `.s-eyebrow`, `.eyebrow-dot`

**Slide size:** 1280×720px (16:9). Accent line ở top. Grid lines ở bg.
