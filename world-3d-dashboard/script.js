// ============================================
// WORLD 3D Dashboard — script.js
// ============================================

// --- Service Definitions ---
const SERVICES = [
  { id: 'DAD-AIFOOD',          color: [0, 229, 255],   count: 628, active: true },
  { id: 'DAD-AIFOOD-INTERNAL', color: [255, 87, 34],   count: 517, active: true },
  { id: 'DAD-ECO',             color: [0, 230, 118],   count: 484, active: true },
  { id: 'DAD-BIKE',            color: [255, 214, 0],   count: 188, active: true },
  { id: 'DAD-BULKY',           color: [156, 39, 176],  count: 41,  active: true },
  { id: 'DAD-PARTNER-4PS',     color: [244, 67, 54],   count: 21,  active: true },
  { id: 'DAD-BULKY-INTERNAL',  color: [33, 150, 243],  count: 19,  active: true },
  { id: 'DAD-POOL',            color: [100, 255, 218], count: 5,   active: true },
  { id: 'Other',               color: [158, 158, 158], count: 11,  active: true },
];

const SERVICE_COLOR_MAP = {};
SERVICES.forEach(s => { SERVICE_COLOR_MAP[s.id] = s.color; });

const CUSTOMERS = [
  { name: "AhaFood AI Admin",              count: 628 },
  { name: "AhaMove - Same day",            count: 542 },
  { name: "Công ty Con cưng",              count: 245 },
  { name: "Pharmacity",                    count: 159 },
  { name: "shopeebulky",                   count: 41  },
  { name: "Delivery Pizza4P's",            count: 26  },
  { name: "CellphonesHN",                  count: 16  },
  { name: "Viettel Post (Tài xế gọi điện…",count: 14 },
  { name: "CÔNG TY CỔ PHẦN TRUNG…",       count: 14  },
  { name: "TGDĐ",                          count: 14  },
  { name: "TGDĐ",                          count: 8   },
  { name: "Cty Thế Giới Flan - TX ĐẾN V…",count: 7   },
  { name: "Kho Báo Đen",                   count: 6   },
  { name: "QT1",                           count: 5   },
  { name: "Bếp Bà Hằng",                   count: 4   },
  { name: "Shop Mẹ và Bé",                 count: 3   },
  { name: "Nhà thuốc An Khang",            count: 3   },
  { name: "FPT Shop",                      count: 2   },
  { name: "Gogi House",                    count: 2   },
  { name: "Highlands Coffee",              count: 1   },
];

// Da Nang Center
const CENTER_LNG = 108.2208;
const CENTER_LAT = 16.0544;

// --- Generate Mock Order Data ---
const rawData = [];
SERVICES.forEach(service => {
  for (let i = 0; i < service.count; i++) {
    const u1 = Math.random() || 0.001;
    const u2 = Math.random();
    const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    const z1 = Math.sqrt(-2.0 * Math.log(u1)) * Math.sin(2.0 * Math.PI * u2);

    // Cluster around Da Nang downtown + some coastal spread
    const lng = CENTER_LNG + z0 * 0.018 + (Math.random() > 0.85 ? 0.025 : 0);
    const lat = CENTER_LAT + z1 * 0.015 + (Math.random() > 0.85 ? 0.015 : -0.005);

    rawData.push({
      position: [lng, lat],
      serviceId: service.id,
      color: service.color,
    });
  }
});

// --- Aggregate into Grid Cells ---
// Group nearby points into grid cells to produce tall columns like the reference image
const GRID_SIZE = 0.003; // ~300m grid cells
function aggregateToGrid(points) {
  const cells = {};
  points.forEach(p => {
    const gx = Math.floor(p.position[0] / GRID_SIZE);
    const gy = Math.floor(p.position[1] / GRID_SIZE);
    const key = `${gx}_${gy}`;
    if (!cells[key]) {
      cells[key] = {
        position: [(gx + 0.5) * GRID_SIZE, (gy + 0.5) * GRID_SIZE],
        count: 0,
        serviceCounts: {},
      };
    }
    cells[key].count++;
    cells[key].serviceCounts[p.serviceId] = (cells[key].serviceCounts[p.serviceId] || 0) + 1;
  });

  // Determine dominant service color per cell
  return Object.values(cells).map(cell => {
    let maxSvc = null, maxCnt = 0;
    for (const [svc, cnt] of Object.entries(cell.serviceCounts)) {
      if (cnt > maxCnt) { maxCnt = cnt; maxSvc = svc; }
    }
    const baseColor = SERVICE_COLOR_MAP[maxSvc] || [158, 158, 158];
    return {
      position: cell.position,
      count: cell.count,
      color: [...baseColor, 220], // RGBA
    };
  });
}

let currentHeightScale = 126;

// --- UI Elements ---
const servicesListEl  = document.getElementById('services-list');
const customerListEl  = document.getElementById('customer-list');
const heightSlider    = document.getElementById('height-slider');
const heightValEl     = document.getElementById('height-val');
const btnRotate       = document.getElementById('btn-rotate');
const btnView         = document.getElementById('btn-view');
const btnAll          = document.getElementById('btn-all');
const btnNone         = document.getElementById('btn-none');

// --- Render Services List ---
function renderServices() {
  servicesListEl.innerHTML = '';
  SERVICES.forEach(svc => {
    const el = document.createElement('div');
    el.className = 'service-item' + (svc.active ? '' : ' disabled');
    el.innerHTML = `
      <div class="service-left">
        <div class="service-color" style="background:rgb(${svc.color.join(',')});color:rgb(${svc.color.join(',')})"></div>
        <div class="service-name">${svc.id}</div>
      </div>
      <div class="service-count">${svc.count}</div>
    `;
    el.addEventListener('click', () => {
      svc.active = !svc.active;
      renderServices();
      updateMap();
    });
    servicesListEl.appendChild(el);
  });
}
renderServices();

// --- Render Customers List ---
CUSTOMERS.forEach((c, i) => {
  const el = document.createElement('li');
  el.className = 'customer-item';
  el.innerHTML = `
    <span>${i + 1}</span>
    <span class="customer-name" title="${c.name}">${c.name}</span>
    <span class="customer-count">${c.count}</span>
  `;
  customerListEl.appendChild(el);
});

// --- Buttons ---
btnAll.addEventListener('click', () => {
  SERVICES.forEach(s => s.active = true);
  renderServices();
  updateMap();
});
btnNone.addEventListener('click', () => {
  SERVICES.forEach(s => s.active = false);
  renderServices();
  updateMap();
});
heightSlider.addEventListener('input', e => {
  currentHeightScale = parseInt(e.target.value);
  heightValEl.textContent = currentHeightScale + 'x';
  updateMap();
});

// --- AI Panel Minimize Toggle ---
document.querySelector('.btn-minimize').addEventListener('click', function () {
  const content = document.querySelector('.ai-content');
  if (content.style.display === 'none') {
    content.style.display = 'block';
    this.textContent = '-';
  } else {
    content.style.display = 'none';
    this.textContent = '+';
  }
});

// ============================================
// Initialize Deck.gl + MapLibre
// ============================================
const INITIAL_VIEW_STATE = {
  longitude: CENTER_LNG,
  latitude: CENTER_LAT,
  zoom: 12.5,
  minZoom: 10,
  maxZoom: 16,
  pitch: 55,
  bearing: -25,
};

const deckgl = new deck.DeckGL({
  container: 'map',
  mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
  initialViewState: INITIAL_VIEW_STATE,
  controller: true,
  getTooltip: ({ object }) => {
    if (!object) return null;
    return {
      html: `<div style="font-family:Inter,sans-serif;font-size:12px;padding:4px 8px"><b>${object.count} đơn</b></div>`,
      style: { background: 'rgba(0,0,0,0.8)', color: '#fff', borderRadius: '6px' },
    };
  },
});

// --- Get Active (filtered) Data ---
function getActiveData() {
  const activeIds = new Set(SERVICES.filter(s => s.active).map(s => s.id));
  return rawData.filter(d => activeIds.has(d.serviceId));
}

// --- Update Map Layers ---
function updateMap() {
  const activePoints = getActiveData();
  const gridData = aggregateToGrid(activePoints);

  // Update UI stats
  document.getElementById('val-orders').textContent = activePoints.length.toLocaleString();
  document.getElementById('val-zones').textContent = gridData.length.toLocaleString();

  const layer = new deck.ColumnLayer({
    id: 'order-columns',
    data: gridData,
    diskResolution: 6,
    radius: 120,
    extruded: true,
    pickable: true,
    elevationScale: currentHeightScale,
    getPosition: d => d.position,
    getFillColor: d => d.color,
    getElevation: d => d.count,
    material: {
      ambient: 0.6,
      diffuse: 0.6,
      shininess: 40,
      specularColor: [60, 64, 70],
    },
    transitions: {
      elevationScale: { duration: 400 },
    },
  });

  deckgl.setProps({ layers: [layer] });
}

// Initial render
updateMap();

// ============================================
// Auto-Rotate
// ============================================
let isRotating = false;
let rotateRAF = null;
let currentBearing = INITIAL_VIEW_STATE.bearing;

function rotateStep() {
  if (!isRotating) return;
  currentBearing += 0.3;
  deckgl.setProps({
    initialViewState: {
      ...INITIAL_VIEW_STATE,
      bearing: currentBearing,
      transitionDuration: 0,
    },
  });
  rotateRAF = requestAnimationFrame(rotateStep);
}

btnRotate.addEventListener('click', () => {
  isRotating = !isRotating;
  if (isRotating) {
    btnRotate.textContent = '⏸ Dừng quay';
    btnRotate.classList.add('active');
    rotateStep();
  } else {
    btnRotate.textContent = '▶ Đang quay';
    btnRotate.classList.remove('active');
    if (rotateRAF) cancelAnimationFrame(rotateRAF);
  }
});

// ============================================
// Top-Down View
// ============================================
btnView.addEventListener('click', () => {
  isRotating = false;
  btnRotate.textContent = '▶ Đang quay';
  btnRotate.classList.remove('active');
  if (rotateRAF) cancelAnimationFrame(rotateRAF);

  deckgl.setProps({
    initialViewState: {
      longitude: CENTER_LNG,
      latitude: CENTER_LAT,
      zoom: 12.5,
      pitch: 0,
      bearing: 0,
      transitionDuration: 1200,
    },
  });
});
