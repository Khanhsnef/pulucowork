const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" x 5.625"
pres.title = "Ahamove MAR-Weekly Delivery W20 2026";

// ── Brand Colors ──────────────────────────────────────────
const C = {
  blue:    "0E4174",
  orange:  "FF7F32",
  green:   "10B981",
  red:     "EF4444",
  white:   "FFFFFF",
  gray50:  "F9FAFB",
  gray100: "F3F4F6",
  gray400: "9CA3AF",
  gray700: "374151",
  blueMid: "1D5A9E",
  blueLight: "EEF3FA",
  orangeLight: "FFF3EC",
};

const ff = { title: "Arial Black", body: "Arial", mono: "Calibri" };

// ── Helpers ───────────────────────────────────────────────
function darkSlide(s) { s.background = { color: C.blue }; }
function lightSlide(s) { s.background = { color: C.gray50 }; }

function sectionTag(slide, label) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.45,
    fill: { color: C.orange }, line: { color: C.orange }
  });
  slide.addText(label, {
    x: 0.35, y: 0, w: 9.3, h: 0.45,
    fontSize: 11, bold: true, color: C.white,
    fontFace: ff.body, valign: "middle", margin: 0
  });
}

function slideTitle(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.4, y: 0.52, w: 9.2, h: 0.55,
    fontSize: 22, bold: true, color: C.blue,
    fontFace: ff.title, margin: 0
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.4, y: 1.06, w: 9.2, h: 0.28,
      fontSize: 10.5, italic: true, color: C.gray400,
      fontFace: ff.body, margin: 0
    });
  }
}

function card(slide, x, y, w, h, opts = {}) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: opts.fill || C.white },
    line: { color: opts.border || "E5E7EB", width: 0.75 },
    shadow: opts.shadow !== false ? { type: "outer", color: "000000", blur: 4, offset: 1, angle: 135, opacity: 0.06 } : undefined
  });
}

function kpiBox(slide, x, y, w, h, label, value, delta, opts = {}) {
  const fillColor = opts.fill || C.white;
  card(slide, x, y, w, h, { fill: fillColor, shadow: false, border: opts.border || "E5E7EB" });
  slide.addText(label, {
    x: x + 0.15, y: y + 0.13, w: w - 0.3, h: 0.22,
    fontSize: 8.5, color: opts.labelColor || C.gray400,
    fontFace: ff.body, bold: false, margin: 0
  });
  slide.addText(value, {
    x: x + 0.1, y: y + 0.34, w: w - 0.2, h: 0.45,
    fontSize: opts.valSize || 22, bold: true, color: opts.valColor || C.blue,
    fontFace: ff.title, margin: 0
  });
  if (delta) {
    const isPos = delta.startsWith("▲") || delta.startsWith("+");
    const isNeg = delta.startsWith("▼") || delta.startsWith("-");
    const dColor = opts.invertDelta
      ? (isPos ? C.red : isNeg ? C.green : C.gray400)
      : (isPos ? C.green : isNeg ? C.red : C.gray400);
    slide.addText(delta, {
      x: x + 0.1, y: y + 0.76, w: w - 0.2, h: 0.22,
      fontSize: 9, color: dColor, bold: true,
      fontFace: ff.body, margin: 0
    });
  }
}

function badge(slide, x, y, w, label, value, isGood) {
  const fill = isGood ? "E6F9F3" : "FEF2F2";
  const textColor = isGood ? "065F46" : "991B1B";
  const borderColor = isGood ? C.green : C.red;
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h: 0.3,
    fill: { color: fill }, line: { color: borderColor, width: 0.75 }
  });
  slide.addText(`${label}  ${value}`, {
    x, y, w, h: 0.3,
    fontSize: 8.5, bold: true, color: textColor,
    fontFace: ff.body, align: "center", valign: "middle", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 1 — COVER
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  darkSlide(s);

  // Orange accent stripe top
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.18,
    fill: { color: C.orange }, line: { color: C.orange }
  });

  // Logo text area
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 0.32, w: 2.2, h: 0.4,
    fill: { color: C.white }, line: { color: C.white }
  });
  s.addText("Ahamove", {
    x: 0.4, y: 0.32, w: 2.2, h: 0.4,
    fontSize: 16, bold: true, color: C.blue,
    fontFace: ff.title, align: "center", valign: "middle", margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 2.72, y: 0.32, w: 1.5, h: 0.4,
    fill: { color: C.orange }, line: { color: C.orange }
  });
  s.addText("MAR-WEEKLY", {
    x: 2.72, y: 0.32, w: 1.5, h: 0.4,
    fontSize: 10, bold: true, color: C.white,
    fontFace: ff.body, align: "center", valign: "middle", margin: 0
  });

  // Main title
  s.addText("DELIVERY", {
    x: 0.5, y: 1.3, w: 9, h: 1.4,
    fontSize: 80, bold: true, color: C.white,
    fontFace: ff.title, align: "center", charSpacing: 10, margin: 0
  });
  s.addText("2026", {
    x: 0.5, y: 2.7, w: 9, h: 1.1,
    fontSize: 80, bold: true, color: C.orange,
    fontFace: ff.title, align: "center", margin: 0
  });

  // Meta info
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 4.95, w: 10, h: 0.675,
    fill: { color: "0A2E5A" }, line: { color: "0A2E5A" }
  });
  s.addText("Supply Ops Weekly Review  ·  W20 2026  ·  18/05/2026", {
    x: 0.5, y: 4.95, w: 9, h: 0.675,
    fontSize: 13, color: C.gray400,
    fontFace: ff.body, align: "center", valign: "middle", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 2 — EXECUTIVE SUMMARY
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "EXECUTIVE SUMMARY  ·  W20 — 12/05 → 18/05/2026");
  slideTitle(s, "Tuần W20: Cầu ổn định — Cung giảm nhẹ — CR tăng đáng chú ý");

  // ── Left: Highlights ──
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 1.42, w: 0.06, h: 3.0,
    fill: { color: C.green }, line: { color: C.green }
  });
  s.addText("HIGHLIGHTS", {
    x: 0.5, y: 1.42, w: 2.2, h: 0.3,
    fontSize: 10, bold: true, color: C.green,
    fontFace: ff.body, margin: 0
  });

  const highlights = [
    "CTR NW vượt 130% Target",
    "GDR NEW & MASS vượt Target ở cả 3 vùng",
    "Supply Hour SGN vượt 110% Target",
    "Active EV SGN đạt 127% Target",
    "MiniHub HAN: PPH 110%, Online Rate 120%",
  ];
  highlights.forEach((h, i) => {
    s.addShape(pres.shapes.OVAL, {
      x: 0.5, y: 1.82 + i * 0.52, w: 0.14, h: 0.14,
      fill: { color: C.green }, line: { color: C.green }
    });
    s.addText(h, {
      x: 0.72, y: 1.79 + i * 0.52, w: 3.9, h: 0.28,
      fontSize: 11, color: C.gray700,
      fontFace: ff.body, valign: "middle", margin: 0
    });
  });

  // ── Right: Lowlights ──
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 1.42, w: 0.06, h: 3.0,
    fill: { color: C.red }, line: { color: C.red }
  });
  s.addText("LOWLIGHTS / CẦN XỬ LÝ", {
    x: 5.35, y: 1.42, w: 4.3, h: 0.3,
    fontSize: 10, bold: true, color: C.red,
    fontFace: ff.body, margin: 0
  });

  const lowlights = [
    "FR hụt target 95% ở cả 3 khu vực (NW: 82.35%)",
    "Retention hụt 2 main city (HAN 76.9%, SGN 80.2%)",
    "CR tăng 0.44% WoW — Driver not ready top 4 tuần liên tiếp",
    "Active EV HAN chỉ đạt 57.6% target (hụt mạnh ở tập NEW)",
    "MiniHub HAN Volume chỉ 71% target",
  ];
  lowlights.forEach((l, i) => {
    s.addShape(pres.shapes.OVAL, {
      x: 5.35, y: 1.82 + i * 0.52, w: 0.14, h: 0.14,
      fill: { color: C.red }, line: { color: C.red }
    });
    s.addText(l, {
      x: 5.57, y: 1.79 + i * 0.52, w: 4.08, h: 0.28,
      fontSize: 11, color: C.gray700,
      fontFace: ff.body, valign: "middle", margin: 0
    });
  });

  // Divider
  s.addShape(pres.shapes.LINE, {
    x: 4.75, y: 1.42, w: 0, h: 3.7,
    line: { color: "E5E7EB", width: 1 }
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 3 — SERVICE PERFORMANCE: AR/FR TREND
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 2  ·  CẦU & DỊCH VỤ");
  slideTitle(s, "Service Performance — AR/FR Trend 5 Tuần", "Request ổn định, FR giảm do Supply Hour giảm & thời tiết HAN");

  const weeks = ["04/20", "04/27", "05/04", "05/11", "05/18"];
  const ar = [91.96, 88.90, 92.07, 92.01, 89.97];
  const fr = [82.79, 79.75, 83.25, 83.03, 80.99];
  const req = [893.6, 664.6, 918.4, 882.9, 888.8];

  // Bar chart (requested)
  s.addChart(pres.charts.BAR, [
    { name: "Requested (K)", labels: weeks, values: req }
  ], {
    x: 0.4, y: 1.42, w: 5.8, h: 3.6,
    barDir: "col",
    chartColors: [C.blueLight, "C7D6F5", "A4BBF0", "8AAEE9", C.blue],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.gray400,
    valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 },
    catGridLine: { style: "none" },
    showValue: true,
    dataLabelColor: C.gray700,
    dataLabelFontSize: 9,
    showLegend: false,
    valAxisMinVal: 0,
    valAxisMaxVal: 1000,
  });

  // Line chart overlay — AR & FR as separate chart
  s.addChart(pres.charts.LINE, [
    { name: "AR (%)", labels: weeks, values: ar },
    { name: "FR (%)", labels: weeks, values: fr },
  ], {
    x: 0.4, y: 1.42, w: 5.8, h: 3.6,
    chartColors: [C.orange, C.blue],
    chartArea: { fill: { color: "FFFFFF", transparency: 100 } },
    catAxisLabelColor: "FFFFFF",
    valAxisHidden: true,
    catAxisHidden: true,
    valGridLine: { style: "none" },
    catGridLine: { style: "none" },
    showLegend: true,
    legendPos: "t",
    legendColor: C.gray700,
    legendFontSize: 9,
    lineSize: 2.5,
    lineSmooth: false,
    showValue: true,
    dataLabelColor: C.gray700,
    dataLabelFontSize: 8.5,
    valAxisMinVal: 60,
    valAxisMaxVal: 100,
  });

  // Right side: Key stats + summary
  card(s, 6.45, 1.42, 3.2, 3.6);

  s.addText("W20 vs W19", {
    x: 6.6, y: 1.55, w: 2.9, h: 0.28,
    fontSize: 11, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const statRows = [
    ["Request NW", "+0.67% WoW", true],
    ["Completed NW", "▼ 1.8% WoW", false],
    ["FR NW", "80.99% (▼2.04%)", false],
    ["AR NW", "89.97% (▼2.04%)", false],
    ["FR HAN", "77.02% (▼3.44%)", false],
    ["FR SGN", "84.49% (▼0.86%)", false],
  ];
  statRows.forEach(([label, val, good], i) => {
    s.addText(label, {
      x: 6.6, y: 1.95 + i * 0.49, w: 1.65, h: 0.28,
      fontSize: 10, color: C.gray400, fontFace: ff.body, margin: 0
    });
    s.addText(val, {
      x: 8.25, y: 1.95 + i * 0.49, w: 1.3, h: 0.28,
      fontSize: 10, bold: true, color: good ? C.green : C.red,
      fontFace: ff.body, align: "right", margin: 0
    });
    if (i < statRows.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x: 6.6, y: 2.18 + i * 0.49, w: 2.9, h: 0,
        line: { color: "F3F4F6", width: 0.5 }
      });
    }
  });

  // Root cause note
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.45, y: 5.02, w: 3.2, h: 0.5,
    fill: { color: "FFF3EC" }, line: { color: C.orange, width: 0.75 }
  });
  s.addText("Root cause HAN: thời tiết mưa 3 ngày + nắng gắt cuối tuần → SH FT/PT giảm 5-7%", {
    x: 6.55, y: 5.04, w: 3.0, h: 0.46,
    fontSize: 8.5, color: "92400E", fontFace: ff.body, valign: "middle", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 4 — FR DEEP DIVE: REGION + SERVICE
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 2  ·  CẦU & DỊCH VỤ");
  slideTitle(s, "FR Deep Dive — Theo Khu Vực & Dịch Vụ (W20)", "FR hụt chủ yếu ở 1H, 2H và 4H — HAN giảm mạnh nhất 3.44% WoW");

  // Left: FR by region - grouped bar
  s.addText("FR by Region (%)", {
    x: 0.4, y: 1.38, w: 4.5, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  s.addChart(pres.charts.BAR, [
    { name: "EXP", labels: ["04/20","04/27","05/04","05/11","05/18"], values: [84.58,80.38,82.35,82.26,81.18] },
    { name: "HAN", labels: ["04/20","04/27","05/04","05/11","05/18"], values: [79.93,74.31,81.89,80.46,77.02] },
    { name: "SGN", labels: ["04/20","04/27","05/04","05/11","05/18"], values: [84.99,83.89,84.46,85.35,84.49] },
  ], {
    x: 0.35, y: 1.68, w: 5.0, h: 3.3,
    barDir: "col",
    barGrouping: "clustered",
    chartColors: [C.orange, C.blue, C.green],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400,
    valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 9, legendColor: C.gray700,
    valAxisMinVal: 70, valAxisMaxVal: 90,
    showValue: false,
  });

  // Right: FR by service
  s.addText("FR by Dịch Vụ — W20 (05/18)", {
    x: 5.6, y: 1.38, w: 4.0, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const services = ["1H", "2H", "4H", "BULKY"];
  const frService = [80.53, 81.22, 76.54, 93.10];
  const frWoW =    [-2.02, -3.16, -1.85,  0.75];

  services.forEach((svc, i) => {
    const good = frWoW[i] > 0;
    const yPos = 1.7 + i * 0.84;
    card(s, 5.55, yPos, 4.0, 0.72, { shadow: false });
    s.addText(svc, {
      x: 5.7, y: yPos + 0.08, w: 0.8, h: 0.28,
      fontSize: 12, bold: true, color: C.blue, fontFace: ff.title, margin: 0
    });
    s.addText(`${frService[i]}%`, {
      x: 6.55, y: yPos + 0.08, w: 1.5, h: 0.28,
      fontSize: 16, bold: true, color: good ? C.green : C.gray700,
      fontFace: ff.title, margin: 0
    });
    s.addText(`WoW: ${frWoW[i] > 0 ? "+" : ""}${frWoW[i]}%`, {
      x: 6.55, y: yPos + 0.38, w: 1.5, h: 0.24,
      fontSize: 9.5, color: good ? C.green : C.red, bold: true,
      fontFace: ff.body, margin: 0
    });
    // Bar indicator
    const barW = Math.min((frService[i] / 100) * 1.5, 1.5);
    s.addShape(pres.shapes.RECTANGLE, {
      x: 8.15, y: yPos + 0.18, w: 1.5, h: 0.2,
      fill: { color: "E5E7EB" }, line: { color: "E5E7EB" }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 8.15, y: yPos + 0.18, w: barW, h: 0.2,
      fill: { color: good ? C.green : C.blue }, line: { color: good ? C.green : C.blue }
    });
    s.addText(`${frService[i]}%`, {
      x: 8.15, y: yPos + 0.4, w: 1.5, h: 0.2,
      fontSize: 8, color: C.gray400, fontFace: ff.body, margin: 0
    });
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 5 — ACTIVE DRIVER & SUPPLY HOUR
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 3  ·  NGUỒN CUNG (SUPPLY CAPACITY)");
  slideTitle(s, "Active Driver & Supply Hour — W20", "Active giảm nhẹ 1.4% NW; Supply Hour giảm 1-2% cả 3 khu vực");

  // KPI row
  const kpis = [
    { label: "Active NW", val: "23,515", delta: "▼ 1.4% WoW", inv: true },
    { label: "Active HAN", val: "10,595", delta: "▼ 1.69% WoW", inv: true },
    { label: "Active SGN", val: "11,059", delta: "▼ 1.92% WoW", inv: true },
    { label: "Active EXP", val: "1,861", delta: "▲ 3.97% WoW", inv: false },
  ];
  kpis.forEach((k, i) => {
    kpiBox(s, 0.35 + i * 2.32, 1.35, 2.15, 1.12,
      k.label, k.val, k.delta, { invertDelta: k.inv, valSize: 18 });
  });

  // Supply Hour bar chart
  s.addText("Supply Hour (K) by Region", {
    x: 0.4, y: 2.62, w: 5.4, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const weeks = ["04/20","04/27","05/04","05/11","05/18"];
  s.addChart(pres.charts.BAR, [
    { name: "EXP", labels: weeks, values: [42.8,34.7,41.5,41.7,41.2] },
    { name: "HAN", labels: weeks, values: [204.0,127.4,205.2,202.7,199.8] },
    { name: "SGN", labels: weeks, values: [292.5,213.1,291.6,287.9,282.7] },
  ], {
    x: 0.35, y: 2.92, w: 5.4, h: 2.5,
    barDir: "col", barGrouping: "stacked",
    chartColors: [C.orange, C.blueMid, C.blue],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400, valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "b", legendFontSize: 9, legendColor: C.gray700,
    valAxisMinVal: 0, valAxisMaxVal: 620,
    showValue: false,
  });

  // Right: Retention MTD + Productivity
  card(s, 5.95, 1.35, 3.7, 2.2);
  s.addText("Retention Rate MTD — May 2026", {
    x: 6.1, y: 1.47, w: 3.4, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });
  const retRows = [
    ["NW",  "77.82%", "+4.55% MoM", "-1.52% YoY"],
    ["HAN", "76.73%", "+7.36% MoM", "-0.98% YoY"],
    ["SGN", "80.17%", "+2.55% MoM", "-1.25% YoY"],
    ["EXP", "71.32%", "-1.42% MoM", "-5.40% YoY"],
  ];
  retRows.forEach(([area, rr, mom, yoy], i) => {
    s.addText(area, { x: 6.1, y: 1.82 + i * 0.36, w: 0.5, h: 0.28, fontSize: 9.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0 });
    s.addText(rr, { x: 6.65, y: 1.82 + i * 0.36, w: 0.8, h: 0.28, fontSize: 11, bold: true, color: C.gray700, fontFace: ff.title, margin: 0 });
    s.addText(mom, { x: 7.5, y: 1.82 + i * 0.36, w: 1.0, h: 0.28, fontSize: 8.5, color: C.green, fontFace: ff.body, margin: 0 });
    s.addText(yoy, { x: 8.55, y: 1.82 + i * 0.36, w: 1.0, h: 0.28, fontSize: 8.5, color: C.red, fontFace: ff.body, margin: 0 });
  });

  // Productivity mini table
  card(s, 5.95, 3.7, 3.7, 1.72, { shadow: false });
  s.addText("Online per Driver (giờ/TX)", {
    x: 6.1, y: 3.78, w: 3.4, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });
  const prodRows = [
    ["", "FT", "PT", "NLM", "Return"],
    ["SGN 05/18", "44.2", "18.5", "21.4", "14.4"],
    ["HAN 05/18", "42.7", "15.8", "15.4", "13.2"],
  ];
  s.addTable(prodRows.map((row, ri) =>
    row.map((cell, ci) => ({
      text: cell,
      options: {
        fontSize: 9,
        bold: ri === 0 || ci === 0,
        color: ri === 0 ? C.white : ci === 0 ? C.blue : C.gray700,
        fill: ri === 0 ? { color: C.blue } : ci === 0 ? { color: C.blueLight } : { color: C.white },
        align: ci === 0 ? "left" : "center",
        valign: "middle",
      }
    }))
  ), { x: 5.95, y: 4.1, w: 3.7, h: 1.2, border: { pt: 0.5, color: "E5E7EB" } });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 6 — RPH & UTILIZATION
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 3  ·  NGUỒN CUNG (SUPPLY CAPACITY)");
  slideTitle(s, "RPH & Utilization Rate — W20", "Hiệu quả cung cải thiện: RPH tăng 2.3%, Utilization tăng 0.92% WoW");

  // RPH KPIs
  const rphData = [
    ["RPH NW", "1.70", "▲ 2.31%"],
    ["RPH HAN", "1.93", "▲ 3.97%"],
    ["RPH SGN", "1.53", "▲ 0.80%"],
    ["RPH EXP", "1.74", "▲ 2.42%"],
  ];
  rphData.forEach(([label, val, delta], i) => {
    kpiBox(s, 0.35 + i * 2.32, 1.35, 2.15, 1.0, label, val, delta, { valSize: 22 });
  });

  // Utilization line chart
  s.addText("Utilization Rate (%) — 5 Tuần", {
    x: 0.4, y: 2.5, w: 5.2, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const weeks = ["04/20","04/27","05/04","05/11","05/18"];
  s.addChart(pres.charts.LINE, [
    { name: "EXP", labels: weeks, values: [54.1,56.5,57.5,54.0,54.4] },
    { name: "HAN", labels: weeks, values: [82.1,81.7,82.4,81.3,82.3] },
    { name: "SGN", labels: weeks, values: [73.9,74.1,78.6,75.5,76.4] },
    { name: "NW",  labels: weeks, values: [75.4,75.1,78.4,76.0,76.9] },
  ], {
    x: 0.35, y: 2.8, w: 5.5, h: 2.6,
    chartColors: [C.orange, C.blue, C.green, "888888"],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400, valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 9, legendColor: C.gray700,
    lineSize: 2, lineSmooth: true,
    showValue: true, dataLabelFontSize: 8, dataLabelColor: C.gray700,
    valAxisMinVal: 45, valAxisMaxVal: 90,
  });

  // Right: Utilization by segment table
  card(s, 6.0, 1.35, 3.65, 4.05);
  s.addText("Utilization by Segment (05/18)", {
    x: 6.15, y: 1.48, w: 3.3, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const utilTable = [
    ["",          "FT",     "NIM",    "NLM",    "PT",     "Return"],
    ["SGN 05/18", "76.3%",  "79.8%",  "80.6%",  "75.5%",  "76.0%"],
    ["SGN 05/11", "75.3%",  "79.1%",  "80.1%",  "74.8%",  "73.6%"],
    ["HAN 05/18", "83.9%",  "81.9%",  "83.8%",  "81.3%",  "81.6%"],
    ["HAN 05/11", "82.7%",  "81.3%",  "83.8%",  "80.2%",  "80.3%"],
  ];
  s.addTable(utilTable.map((row, ri) =>
    row.map((cell, ci) => ({
      text: cell,
      options: {
        fontSize: 9,
        bold: ri === 0 || ci === 0,
        color: ri === 0 ? C.white : ci === 0 ? C.blue : C.gray700,
        fill: ri === 0 ? { color: C.blue } : ri % 2 === 1 ? { color: C.white } : { color: C.gray100 },
        align: ci === 0 ? "left" : "center",
        valign: "middle",
      }
    }))
  ), { x: 6.0, y: 1.85, w: 3.65, h: 2.8, border: { pt: 0.5, color: "E5E7EB" } });

  // Insight note
  s.addShape(pres.shapes.RECTANGLE, {
    x: 6.0, y: 4.75, w: 3.65, h: 0.52,
    fill: { color: C.blueLight }, line: { color: C.blue, width: 0.75 }
  });
  s.addText("Insight: RPH tăng do request tăng (+0.7%) trong khi supply hour giảm (-1.6%) → cùng lượng tài xế giao nhiều hơn/giờ", {
    x: 6.1, y: 4.77, w: 3.45, h: 0.48,
    fontSize: 8.5, color: C.blue, fontFace: ff.body, valign: "middle", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 7 — EARNING (EPH)
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 4  ·  THU NHẬP TÀI XẾ");
  slideTitle(s, "Earning per Hour (EPH) — W20", "NW EPH đạt 47.2k/h (+0.9k WoW) — HAN tăng mạnh 2-3k/h tất cả các tập");

  // Top KPIs
  kpiBox(s, 0.35, 1.35, 2.0, 1.05, "EPH NW", "47,223", "▲ +0.9k WoW", { valSize: 18 });
  kpiBox(s, 2.5, 1.35, 2.0, 1.05, "EPH HAN", "52,887", "▲ +2.6k WoW", { valSize: 18 });
  kpiBox(s, 4.65, 1.35, 2.0, 1.05, "EPH SGN", "45,336", "▼ -0.07k WoW", { valSize: 18, invertDelta: true });

  // EPH by segment — HAN
  s.addText("HAN — EPH by Segment (đ/h)", {
    x: 0.35, y: 2.55, w: 4.7, h: 0.28,
    fontSize: 10.5, bold: true, color: C.orange, fontFace: ff.body, margin: 0
  });

  const segLabels = ["FT", "PT", "NLM", "NIM", "Return"];
  const hanEph = [
    [54512, 49584, 45596, 40532, 44734],
    [54753, 49845, 45926, 41268, 45917],
    [57917, 52717, 48148, 43675, 48253],
  ];
  s.addChart(pres.charts.BAR, [
    { name: "05/04", labels: segLabels, values: hanEph[0] },
    { name: "05/11", labels: segLabels, values: hanEph[1] },
    { name: "05/18", labels: segLabels, values: hanEph[2] },
  ], {
    x: 0.35, y: 2.85, w: 4.6, h: 2.55,
    barDir: "col", barGrouping: "clustered",
    chartColors: ["C7D6F5", C.blueMid, C.orange],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400, valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 9, legendColor: C.gray700,
    valAxisMinVal: 35000, valAxisMaxVal: 65000,
    showValue: false,
  });

  // SGN EPH
  s.addText("SGN — EPH by Segment (đ/h)", {
    x: 5.15, y: 2.55, w: 4.5, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const sgnEph = [
    [49407, 46463, 43588, 37766, 42952],
    [47563, 44231, 42852, 38494, 40556],
    [47510, 44289, 43248, 39222, 41169],
  ];
  s.addChart(pres.charts.BAR, [
    { name: "05/04", labels: segLabels, values: sgnEph[0] },
    { name: "05/11", labels: segLabels, values: sgnEph[1] },
    { name: "05/18", labels: segLabels, values: sgnEph[2] },
  ], {
    x: 5.1, y: 2.85, w: 4.55, h: 2.55,
    barDir: "col", barGrouping: "clustered",
    chartColors: ["C7D6F5", C.blueMid, C.blue],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400, valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 9, legendColor: C.gray700,
    valAxisMinVal: 30000, valAxisMaxVal: 60000,
    showValue: false,
  });

  // Note box
  card(s, 6.8, 1.35, 2.85, 1.05, { shadow: false });
  s.addText([
    { text: "HAN: ", options: { bold: true, color: C.orange } },
    { text: "FT tăng mạnh +3.2k → 57.9k\n", options: { color: C.gray700 } },
    { text: "SGN: ", options: { bold: true, color: C.blue } },
    { text: "EPH ổn định, dao động nhẹ", options: { color: C.gray700 } },
  ], {
    x: 6.9, y: 1.4, w: 2.65, h: 0.95,
    fontSize: 10, fontFace: ff.body, valign: "middle", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 8 — RETENTION RATE (HAN + SGN)
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 5  ·  CHẤT LƯỢNG TÀI XẾ");
  slideTitle(s, "Retention Rate — HAN & SGN (May 2026)", "MoM cải thiện mạnh nhưng cả 2 thành phố vẫn hụt Target 80% và YoY");

  // HAN section
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 1.38, w: 0.06, h: 3.72,
    fill: { color: C.orange }, line: { color: C.orange }
  });
  s.addText("HAN", {
    x: 0.5, y: 1.38, w: 1.5, h: 0.32,
    fontSize: 13, bold: true, color: C.orange, fontFace: ff.title, margin: 0
  });

  kpiBox(s, 0.5, 1.75, 1.7, 1.0, "Overall RR", "76.93%", "▲ +7.4% MoM", { valSize: 16 });
  kpiBox(s, 2.3, 1.75, 1.7, 1.0, "vs Target", "hụt 80%", "▼ -0.74% YoY", { valSize: 13, invertDelta: true });

  const hanSeg = [
    ["FT",  "97.30%", "▼ -1.23%", "▲ +0.67%"],
    ["PT",  "75.08%", "▲ +8.29%", "▲ +0.90%"],
    ["NLM", "72.70%", "▼ -4.32%", "▼ -8.01%"],
  ];
  const hdrs = [["Segment","RR","MoM","YoY"]];
  s.addTable([
    hdrs[0].map(h => ({ text: h, options: { fontSize: 9, bold: true, color: C.white, fill: { color: C.orange }, align: "center", valign: "middle" } })),
    ...hanSeg.map(([seg, rr, mom, yoy]) => [
      { text: seg, options: { fontSize: 10, bold: true, color: C.orange, fill: { color: C.white }, valign: "middle" } },
      { text: rr,  options: { fontSize: 10, bold: true, color: C.gray700, fill: { color: C.white }, align: "center", valign: "middle" } },
      { text: mom, options: { fontSize: 9, color: mom.includes("▲") ? C.green : C.red, fill: { color: C.white }, align: "center", valign: "middle", bold: true } },
      { text: yoy, options: { fontSize: 9, color: yoy.includes("▲") ? C.green : C.red, fill: { color: C.white }, align: "center", valign: "middle", bold: true } },
    ])
  ], { x: 0.5, y: 2.85, w: 3.5, h: 1.5, border: { pt: 0.5, color: "E5E7EB" } });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 4.45, w: 3.5, h: 0.55,
    fill: { color: "FEF2F2" }, line: { color: C.red, width: 0.75 }
  });
  s.addText("NLM: RR thấp nhất, gap -8% YoY — cần ưu tiên action giữ chân", {
    x: 0.6, y: 4.47, w: 3.3, h: 0.51,
    fontSize: 8.5, color: "991B1B", fontFace: ff.body, valign: "middle", margin: 0
  });

  // Divider
  s.addShape(pres.shapes.LINE, {
    x: 4.85, y: 1.35, w: 0, h: 3.9,
    line: { color: "E5E7EB", width: 1.5 }
  });

  // SGN section
  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.0, y: 1.38, w: 0.06, h: 3.72,
    fill: { color: C.blue }, line: { color: C.blue }
  });
  s.addText("SGN", {
    x: 5.15, y: 1.38, w: 1.5, h: 0.32,
    fontSize: 13, bold: true, color: C.blue, fontFace: ff.title, margin: 0
  });

  kpiBox(s, 5.15, 1.75, 1.7, 1.0, "Overall RR", "80.17%", "▲ +2.55% MoM", { valSize: 16 });
  kpiBox(s, 6.95, 1.75, 1.7, 1.0, "vs Target", "đạt 80%", "▼ -1.25% YoY", { valSize: 13, invertDelta: true });

  const sgnSeg = [
    ["FT",  "98.43%", "+0.3%", "+0.7%"],
    ["PT",  "74.86%", "+2.2%", "-0.5%"],
    ["NLM", "80.34%", "+5.0%", "+3.0%"],
  ];
  s.addTable([
    hdrs[0].map(h => ({ text: h, options: { fontSize: 9, bold: true, color: C.white, fill: { color: C.blue }, align: "center", valign: "middle" } })),
    ...sgnSeg.map(([seg, rr, mom, yoy]) => [
      { text: seg, options: { fontSize: 10, bold: true, color: C.blue, fill: { color: C.white }, valign: "middle" } },
      { text: rr,  options: { fontSize: 10, bold: true, color: C.gray700, fill: { color: C.white }, align: "center", valign: "middle" } },
      { text: mom, options: { fontSize: 9, color: mom.includes("-") ? C.red : C.green, fill: { color: C.white }, align: "center", valign: "middle", bold: true } },
      { text: yoy, options: { fontSize: 9, color: yoy.includes("-") ? C.red : C.green, fill: { color: C.white }, align: "center", valign: "middle", bold: true } },
    ])
  ], { x: 5.15, y: 2.85, w: 3.5, h: 1.5, border: { pt: 0.5, color: "E5E7EB" } });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.15, y: 4.45, w: 3.5, h: 0.55,
    fill: { color: "E6F9F3" }, line: { color: C.green, width: 0.75 }
  });
  s.addText("NLM SGN tháng 5 tốt, vượt 80% MTD — PT cần action do hụt YoY", {
    x: 5.25, y: 4.47, w: 3.3, h: 0.51,
    fontSize: 8.5, color: "065F46", fontFace: ff.body, valign: "middle", margin: 0
  });

  // New driver W1 callout
  card(s, 8.75, 1.75, 0.9, 1.0, { fill: C.blueLight, shadow: false });
  s.addText("New W1\nHAN\n72.7%", {
    x: 8.78, y: 1.8, w: 0.84, h: 0.9,
    fontSize: 9.5, bold: true, color: C.blue,
    fontFace: ff.body, align: "center", valign: "middle", margin: 0
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 9 — CANCELLATION RATE OVERVIEW
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 5  ·  CHẤT LƯỢNG TÀI XẾ");
  slideTitle(s, "Cancellation Rate — NW Overview (W20)", "CR tăng 0.44% WoW — 2H tăng mạnh nhất; Driver not ready top reason 4 tuần liên tiếp");

  // NW CR trend
  s.addText("NW CR (Rule PoC) — 5 Tuần", {
    x: 0.35, y: 1.38, w: 5.0, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const weeks = ["04/20","04/27","05/04","05/11","05/18"];
  s.addChart(pres.charts.LINE, [
    { name: "EXP", labels: weeks, values: [5.8,6.1,6.1,6.1,6.3] },
    { name: "HAN", labels: weeks, values: [13.9,14.0,13.6,12.9,13.4] },
    { name: "SGN", labels: weeks, values: [10.8,11.4,11.3,11.1,11.5] },
    { name: "NW",  labels: weeks, values: [11.7,11.9,11.9,11.5,12.0] },
  ], {
    x: 0.35, y: 1.68, w: 5.5, h: 2.7,
    chartColors: [C.orange, C.red, C.blue, "888888"],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400, valAxisLabelColor: C.gray400,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 9, legendColor: C.gray700,
    lineSize: 2.5, lineSmooth: false,
    showValue: true, dataLabelFontSize: 8, dataLabelColor: C.gray700,
    valAxisMinVal: 0, valAxisMaxVal: 20,
  });

  // CR by service
  s.addText("CR by Dịch Vụ (W20)", {
    x: 0.35, y: 4.48, w: 5.5, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });
  const svcCR = [
    ["DV",    "1H",     "2H",     "4H",     "Bulky",  "Shopee", "TikTok"],
    ["HAN",   "11.29%", "27.83%", "11.06%", "17.97%", "24.45%", "21.34%"],
    ["WoW",   "0.0%",   "+5.9%",  "+0.5%",  "-0.7%",  "+3.3%",  "+0.69%"],
    ["SGN",   "9.64%",  "16.71%", "7.74%",  "12.06%", "21.88%", "19.49%"],
    ["WoW",   "0.0%",   "-0.5%",  "-0.5%",  "0.0%",   "-2.0%",  "-0.1%"],
  ];
  s.addTable(svcCR.map((row, ri) =>
    row.map((cell, ci) => {
      const isWoW = row[0] === "WoW";
      const isIncrease = cell.startsWith("+") || parseFloat(cell) > 20;
      const isHeader = ri === 0;
      const isLabel = ci === 0;
      return {
        text: cell,
        options: {
          fontSize: 8.5,
          bold: isHeader || isLabel,
          color: isHeader ? C.white
            : isLabel ? (isWoW ? C.gray400 : C.blue)
            : isWoW ? (cell.startsWith("+") ? C.red : cell.startsWith("-") ? C.green : C.gray400)
            : C.gray700,
          fill: isHeader ? { color: C.blue } : isWoW ? { color: C.gray100 } : { color: C.white },
          align: ci === 0 ? "left" : "center",
          valign: "middle",
        }
      };
    })
  ), { x: 0.35, y: 4.78, w: 5.5, h: 0.72, border: { pt: 0.5, color: "E5E7EB" } });

  // Right: Top cancel reasons
  card(s, 6.05, 1.38, 3.6, 3.95);
  s.addText("Top Cancel Reasons — SGN (W20)", {
    x: 6.2, y: 1.5, w: 3.3, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const reasons = [
    ["Driver not ready", "22,720", "🔴 #1 × 4 tuần"],
    ["Recipient cannot be reached", "21,224", ""],
    ["Rescheduled delivery", "14,963", ""],
    ["Recipient cancel booking", "9,528", ""],
    ["Sender cancel booking", "4,787", ""],
    ["Sender cannot be reached", "3,524", ""],
  ];
  reasons.forEach(([reason, count, note], i) => {
    const isTop = i === 0;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 6.05, y: 1.88 + i * 0.51, w: 3.6, h: 0.45,
      fill: { color: isTop ? "FEF2F2" : C.white },
      line: { color: isTop ? C.red : "F3F4F6", width: 0.5 }
    });
    s.addText(`${i + 1}. ${reason}`, {
      x: 6.15, y: 1.91 + i * 0.51, w: 2.3, h: 0.2,
      fontSize: 8.5, bold: isTop, color: isTop ? "991B1B" : C.gray700,
      fontFace: ff.body, margin: 0
    });
    s.addText(count, {
      x: 8.5, y: 1.91 + i * 0.51, w: 1.1, h: 0.2,
      fontSize: 8.5, bold: true, color: isTop ? C.red : C.gray400,
      fontFace: ff.mono, align: "right", margin: 0
    });
    if (note) {
      s.addText(note, {
        x: 6.15, y: 2.1 + i * 0.51, w: 3.4, h: 0.18,
        fontSize: 7.5, color: C.red, fontFace: ff.body, margin: 0
      });
    }
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 10 — CR ROOT CAUSE: DRIVER NOT READY
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 5  ·  CHẤT LƯỢNG TÀI XẾ");
  slideTitle(s, "Root Cause — \"Driver Not Ready\" (Survey 50 TX SGN)", "Hủy chủ quan tập trung khung giờ chiều tối — Chat AI/tổng đài là bottleneck chính");

  // Survey results (left)
  s.addText("Lý Do Hủy Chủ Quan (n=50 TX được call out)", {
    x: 0.35, y: 1.38, w: 5.0, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const surveyData = [
    ["Hệ thống tự gán đơn không phù hợp", 27, C.red],
    ["Chat AI / Tổng đài hỗ trợ hủy chậm", 22, C.orange],
    ["Chọn sai lý do để hủy nhanh", 17, "F59E0B"],
    ["Khách hàng KNM / thuê bao", 12, C.gray400],
    ["Định vị sai / địa chỉ không chính xác", 10, C.gray400],
    ["Lý do cá nhân / thời gian biểu", 12, C.gray400],
  ];

  surveyData.forEach(([label, pct, color], i) => {
    const yPos = 1.75 + i * 0.51;
    s.addText(label, {
      x: 0.4, y: yPos, w: 3.2, h: 0.24,
      fontSize: 9.5, color: C.gray700, fontFace: ff.body, margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: yPos + 0.26, w: 3.2, h: 0.16,
      fill: { color: "E5E7EB" }, line: { color: "E5E7EB" }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.4, y: yPos + 0.26, w: (pct / 100) * 3.2, h: 0.16,
      fill: { color: color }, line: { color: color }
    });
    s.addText(`${pct}%`, {
      x: 3.65, y: yPos + 0.22, w: 0.6, h: 0.22,
      fontSize: 9.5, bold: true, color: color, fontFace: ff.body, margin: 0
    });
  });

  // Divider
  s.addShape(pres.shapes.LINE, {
    x: 4.6, y: 1.35, w: 0, h: 4.0,
    line: { color: "E5E7EB", width: 1 }
  });

  // Right: Hourly CR subjective rate
  s.addText("% Hủy Chủ Quan theo Giờ", {
    x: 4.8, y: 1.38, w: 4.8, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const hourlyData = [
    ["16:00-17:00", 45.3, 33.8],
    ["17:00-18:00", 46.8, 35.1],
    ["18:00-19:00", 46.5, 36.4],
    ["19:00-20:00", 45.9, 37.0],
    ["20:00-21:00", 50.2, 42.5],
    ["21:00-22:00", 54.7, 49.9],
    ["22:00-23:00", 56.3, 50.0],
    ["23:00-00:00", 51.2, 41.9],
  ];

  s.addChart(pres.charts.BAR, [
    { name: "HAN % Chủ Quan", labels: hourlyData.map(r => r[0]), values: hourlyData.map(r => r[1]) },
    { name: "SGN % Chủ Quan", labels: hourlyData.map(r => r[0]), values: hourlyData.map(r => r[2]) },
  ], {
    x: 4.75, y: 1.68, w: 4.9, h: 2.9,
    barDir: "col", barGrouping: "clustered",
    chartColors: [C.orange, C.blue],
    chartArea: { fill: { color: C.white } },
    catAxisLabelColor: C.gray400, valAxisLabelColor: C.gray400,
    catAxisLabelRotate: 30,
    valGridLine: { color: "E5E7EB", size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "t", legendFontSize: 9, legendColor: C.gray700,
    valAxisMinVal: 0, valAxisMaxVal: 65,
    showValue: false,
  });

  // Key insight boxes
  const insightBoxes = [
    { x: 4.75, text: "HAN: 45-56% chủ quan vào chiều tối (vs 37-43% khung khác)", color: C.orange },
    { x: 7.3, text: "SGN: 35-50% chủ quan vào chiều tối (vs 25-33% khung khác)", color: C.blue },
  ];
  insightBoxes.forEach(({ x, text, color }) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.68, w: 2.45, h: 0.62,
      fill: { color: C.white }, line: { color, width: 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.68, w: 0.06, h: 0.62,
      fill: { color }, line: { color }
    });
    s.addText(text, {
      x: x + 0.12, y: 4.7, w: 2.28, h: 0.58,
      fontSize: 8.5, color: C.gray700, fontFace: ff.body, valign: "middle", margin: 0
    });
  });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 11 — PROJECT KPIs: EV + MINIHUB
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 6  ·  PROJECT KPIs");
  slideTitle(s, "EV Project & MiniHub — W20 vs Target", "EV SGN vượt target; MiniHub HAN cần đẩy volume & chuyển đổi tài xế mới");

  // EV section header
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 1.38, w: 0.06, h: 2.05,
    fill: { color: C.green }, line: { color: C.green }
  });
  s.addText("⚡ EV PROJECT", {
    x: 0.5, y: 1.38, w: 2.5, h: 0.32,
    fontSize: 12, bold: true, color: C.green, fontFace: ff.body, margin: 0
  });

  const evKpis = [
    { area: "NW",  label: "Total Active EV", val: "520", pct: "80.4%", good: false },
    { area: "HAN", label: "Total Active EV", val: "250", pct: "57.6%", good: false },
    { area: "SGN", label: "Total Active EV", val: "270", pct: "126.8%", good: true },
  ];
  evKpis.forEach((k, i) => {
    const fillColor = k.good ? "E6F9F3" : "FEF2F2";
    const pctColor = k.good ? C.green : C.red;
    card(s, 0.5 + i * 3.1, 1.78, 2.9, 1.5, { fill: fillColor, border: k.good ? C.green : C.red, shadow: false });
    s.addText(k.area, { x: 0.65 + i * 3.1, y: 1.88, w: 1.5, h: 0.28, fontSize: 13, bold: true, color: k.good ? "065F46" : "991B1B", fontFace: ff.title, margin: 0 });
    s.addText(k.val, { x: 0.65 + i * 3.1, y: 2.18, w: 1.2, h: 0.42, fontSize: 24, bold: true, color: k.good ? "065F46" : "991B1B", fontFace: ff.title, margin: 0 });
    s.addText("active EV", { x: 1.9 + i * 3.1, y: 2.28, w: 1.4, h: 0.28, fontSize: 9, color: C.gray400, fontFace: ff.body, margin: 0 });
    s.addText(`Đạt ${k.pct} target`, { x: 0.65 + i * 3.1, y: 2.62, w: 2.6, h: 0.28, fontSize: 10, bold: true, color: pctColor, fontFace: ff.body, margin: 0 });
  });

  // MiniHub section
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.35, y: 3.45, w: 0.06, h: 1.9,
    fill: { color: C.blue }, line: { color: C.blue }
  });
  s.addText("🏪 MINIHUB PROJECT", {
    x: 0.5, y: 3.45, w: 3.0, h: 0.32,
    fontSize: 12, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });

  const mhTable = [
    ["Metric",             "NW",       "% Target", "HAN",     "% Target", "SGN",      "% Target"],
    ["MiniHub Volume",     "122,981",  "90%",      "38,482",  "71%",      "84,499",   "103%"],
    ["MiniHub PPH",        "3.02",     "100%",     "3.42",    "110%",     "2.87",     "99%"],
    ["Online Rate",        "81.11%",   "95%",      "89.14%",  "120%",     "78.41%",   "95%"],
  ];

  const pctGood = (cell, ri, ci) => {
    if (ri === 0 || ci === 0 || !cell.endsWith("%")) return null;
    const v = parseFloat(cell);
    if (v >= 100) return true;
    if (v < 90) return false;
    return null;
  };

  s.addTable(mhTable.map((row, ri) =>
    row.map((cell, ci) => {
      const pg = pctGood(cell, ri, ci);
      return {
        text: cell,
        options: {
          fontSize: 9,
          bold: ri === 0 || ci === 0,
          color: ri === 0 ? C.white
            : pg === true ? "065F46"
            : pg === false ? "991B1B"
            : ci === 0 ? C.blue : C.gray700,
          fill: ri === 0 ? { color: C.blue }
            : pg === true ? { color: "E6F9F3" }
            : pg === false ? { color: "FEF2F2" }
            : ri % 2 === 0 ? { color: C.gray100 } : { color: C.white },
          align: ci === 0 ? "left" : "center",
          valign: "middle",
        }
      };
    })
  ), { x: 0.5, y: 3.82, w: 9.15, h: 1.35, border: { pt: 0.5, color: "E5E7EB" } });
}

// ═══════════════════════════════════════════════════════════
// SLIDE 12 — DRIVER VOICES & NEXT ACTIONS
// ═══════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  lightSlide(s);
  sectionTag(s, "ACT 7  ·  CỘNG ĐỒNG TÀI XẾ & NEXT ACTIONS");
  slideTitle(s, "Driver's Voices & Engagement — NW (W20)", "5 issues được ghi nhận từ community — 4/5 đã xử lý");

  const issues = [
    { no: "01", title: "Lỗi điều hướng",       desc: "Đơn gán không đúng điều hướng, tổng đài không hủy giúp",        status: "Đã gửi OE",          done: true },
    { no: "02", title: "Giảm thời gian chờ",   desc: "Viral post đề xuất giảm từ 15p → 10p",                          status: "Apply từ 26/5",       done: true },
    { no: "03", title: "Lỗi chi tiền",          desc: "Lỗi giao dịch 7/5 & 11/5 — TX bức xúc",                       status: "Tắt Vietinbank → Momo", done: true },
    { no: "04", title: "Cắt thưởng Hoàn TNhập", desc: "TX phản ứng tiêu cực với cắt thưởng",                         status: "Đã truyền thông CT mới", done: true },
    { no: "05", title: "Thắc mắc EV & CTT",    desc: "TX hỏi về chương trình EV & CTT",                              status: "Seeding + Góc giải đáp", done: true },
  ];

  issues.forEach((item, i) => {
    const yPos = 1.42 + i * 0.71;
    const fillColor = item.done ? "E6F9F3" : "FEF2F2";
    const borderColor = item.done ? C.green : C.red;
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.35, y: yPos, w: 6.8, h: 0.63,
      fill: { color: fillColor }, line: { color: borderColor, width: 0.75 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.35, y: yPos, w: 0.06, h: 0.63,
      fill: { color: borderColor }, line: { color: borderColor }
    });
    s.addText(item.no, {
      x: 0.48, y: yPos + 0.08, w: 0.4, h: 0.2,
      fontSize: 9, bold: true, color: borderColor, fontFace: ff.body, margin: 0
    });
    s.addText(item.title, {
      x: 0.92, y: yPos + 0.06, w: 3.4, h: 0.24,
      fontSize: 10.5, bold: true, color: C.gray700, fontFace: ff.body, margin: 0
    });
    s.addText(item.desc, {
      x: 0.92, y: yPos + 0.31, w: 3.4, h: 0.24,
      fontSize: 8.5, color: C.gray400, fontFace: ff.body, margin: 0
    });
    // Status badge
    s.addShape(pres.shapes.RECTANGLE, {
      x: 4.4, y: yPos + 0.16, w: 2.65, h: 0.3,
      fill: { color: item.done ? "065F46" : "991B1B" }, line: { color: item.done ? C.green : C.red }
    });
    s.addText(`✓ ${item.status}`, {
      x: 4.4, y: yPos + 0.16, w: 2.65, h: 0.3,
      fontSize: 9, bold: true, color: C.white,
      fontFace: ff.body, align: "center", valign: "middle", margin: 0
    });
  });

  // Right: Upcoming
  card(s, 7.3, 1.42, 2.35, 4.05);
  s.addText("Upcoming Events", {
    x: 7.42, y: 1.54, w: 2.1, h: 0.28,
    fontSize: 10.5, bold: true, color: C.blue, fontFace: ff.body, margin: 0
  });
  const upcoming = [
    "🏆 Leaderboard Đua top đơn 5 sao",
    "💧 Chương trình tiếp nước xuyên suốt hè",
    "🎁 Rewards cho tài xế",
    "🔍 Góc giải đáp thắc mắc EV",
  ];
  upcoming.forEach((item, i) => {
    s.addText(item, {
      x: 7.45, y: 1.92 + i * 0.7, w: 2.05, h: 0.55,
      fontSize: 10, color: C.gray700, fontFace: ff.body,
      valign: "middle", margin: 0
    });
    if (i < upcoming.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x: 7.45, y: 2.45 + i * 0.7, w: 2.05, h: 0,
        line: { color: "E5E7EB", width: 0.5 }
      });
    }
  });
}

// ── Write file ─────────────────────────────────────────────
const outPath = "/Users/ts-1148/Desktop/Cowork/output/Ahamove/02. CAMPAIGNS_PROJECTS/2026-05-mar-weekly-w20.pptx";
pres.writeFile({ fileName: outPath }).then(() => {
  console.log("✅ Written:", outPath);
}).catch(err => {
  console.error("❌ Error:", err);
});
