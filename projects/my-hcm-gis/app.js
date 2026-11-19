(() => {
  'use strict';

  const { STNMT_WMS_URL, DEFAULT_CENTER, DEFAULT_ZOOM } = window.GIS_CONFIG;
  const WATCHLIST_KEY = 'my_hcm_gis_watchlist_v1';

  // --- Utility Helpers ---
  const $ = (id) => document.getElementById(id);
  const esc = (str) => String(str ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));

  let toastTimer = null;
  function showToast(msg) {
    const el = $('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 3200);
  }

  // --- 1. Modern Web Guidance: Dialog Light-Dismiss Fallback ---
  function setupDialogLightDismiss(dialog) {
    if (!dialog || ('closedBy' in HTMLDialogElement.prototype)) return;
    dialog.addEventListener('click', (event) => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      const inside = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      );
      if (!inside) dialog.close();
    });
  }

  const legendDialog = $('legend-dialog');
  const settingsDialog = $('settings-dialog');
  setupDialogLightDismiss(legendDialog);
  setupDialogLightDismiss(settingsDialog);

  $('btn-open-legend').addEventListener('click', () => legendDialog.showModal());
  $('btn-open-settings').addEventListener('click', () => settingsDialog.showModal());

  // --- 2. Modern Web Guidance: 3-State Dark Mode Toggle (Meta + Storage Sync) ---
  const colorSchemeMeta = document.querySelector('meta[name="color-scheme"]');
  const themeSelect = $('theme-select');

  function syncThemeUI() {
    let stored = null;
    try { stored = localStorage.getItem('color-scheme'); } catch {}
    const val = (stored === 'light' || stored === 'dark') ? stored : 'system';
    themeSelect.value = val;
    colorSchemeMeta.content = val === 'system' ? 'light dark' : val;
  }

  themeSelect.addEventListener('change', () => {
    const val = themeSelect.value;
    try {
      if (val === 'system') localStorage.removeItem('color-scheme');
      else localStorage.setItem('color-scheme', val);
    } catch {}
    colorSchemeMeta.content = val === 'system' ? 'light dark' : val;
  });

  window.addEventListener('storage', (e) => {
    if (e.key === 'color-scheme') syncThemeUI();
  });
  syncThemeUI();

  // --- 3. Modern Web Guidance: Accessible Tabs + beforematch + Scroll Fade Fallback ---
  const tablist = $('sidebar-tablist');
  const tabs = Array.from(tablist.querySelectorAll('button'));
  const panels = tabs.map((t) => document.querySelector(`[role="tabpanel"][aria-labelledby="${t.id}"]`));

  function selectTab(targetTab, shouldFocus = false) {
    tabs.forEach((tab, idx) => {
      const active = tab === targetTab;
      tab.ariaSelected = String(active);
      tab.toggleAttribute('focusgroupstart', active);
      const panel = panels[idx];
      if (panel) {
        if (active) {
          panel.removeAttribute('hidden');
          panel.setAttribute('tabindex', '0');
        } else {
          panel.hidden = 'until-found';
          panel.removeAttribute('tabindex');
        }
      }
    });
    targetTab.scrollIntoView({ block: 'nearest', inline: 'nearest', container: 'nearest' });
    if (shouldFocus) targetTab.focus();
  }

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('focus', () => selectTab(tab));
  });

  panels.forEach((panel, idx) => {
    if (!panel) return;
    panel.addEventListener('beforematch', () => selectTab(tabs[idx]));
  });

  // Keyboard arrow navigation fallback when native focusgroup is unsupported
  if (!Object.hasOwn(HTMLElement.prototype, 'focusGroup')) {
    tablist.addEventListener('keydown', (e) => {
      const idx = tabs.indexOf(document.activeElement);
      if (idx === -1) return;
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        selectTab(tabs[(idx + 1) % tabs.length], true);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        selectTab(tabs[(idx - 1 + tabs.length) % tabs.length], true);
      } else if (e.key === 'Home') {
        e.preventDefault();
        selectTab(tabs[0], true);
      } else if (e.key === 'End') {
        e.preventDefault();
        selectTab(tabs[tabs.length - 1], true);
      }
    });
  }

  // Scroll-fade fallback when scroll-driven animations are unsupported
  if (!CSS.supports('animation-timeline', 'scroll()')) {
    const first = tablist.firstElementChild;
    const last = tablist.lastElementChild;
    if (first && last) {
      const obs = new IntersectionObserver((entries) => {
        for (const { target, intersectionRatio } of entries) {
          tablist.classList.toggle(target === first ? 'more-start' : 'more-end', intersectionRatio < 1);
        }
      }, { root: tablist, threshold: 1, rootMargin: '1px' });
      obs.observe(first);
      obs.observe(last);
    }
  }

  // --- 4. Initialize Leaflet Map & Basemaps ---
  const map = L.map('map', {
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
    maxZoom: 21,
    zoomControl: true
  });

  const basemaps = {
    google_hybrid: L.tileLayer('https://mt{s}.google.com/vt/lyrs=y&hl=vi&x={x}&y={y}&z={z}', {
      subdomains: ['0', '1', '2', '3'],
      maxZoom: 21,
      maxNativeZoom: 20,
      attribution: '© Google Satellite'
    }),
    google_road: L.tileLayer('https://mt{s}.google.com/vt/lyrs=m&hl=vi&x={x}&y={y}&z={z}', {
      subdomains: ['0', '1', '2', '3'],
      maxZoom: 21,
      maxNativeZoom: 20,
      attribution: '© Google Maps'
    }),
    osm: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 20,
      maxNativeZoom: 19,
      attribution: '© OpenStreetMap'
    }),
    carto_dark: L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 20,
      attribution: '© CARTO'
    })
  };

  let activeBasemap = basemaps.google_hybrid.addTo(map);

  $('basemap-grid').addEventListener('click', (e) => {
    const btn = e.target.closest('[data-basemap]');
    if (!btn) return;
    const key = btn.dataset.basemap;
    if (!basemaps[key]) return;
    map.removeLayer(activeBasemap);
    activeBasemap = basemaps[key].addTo(map);
    activeBasemap.bringToBack();
    document.querySelectorAll('.basemap-btn').forEach((b) => b.classList.toggle('active', b === btn));
  });

  // --- 5. Live Official WMS Layers (Sở TN&MT TP.HCM) ---
  const wmsInstances = {};
  const wmsListEl = $('wms-layers-list');
  const layerCatalog = Object.values(window.WMS_LAYERS);

  // Add planning layers below cadastral so parcel borders stay crisp on top
  const orderedCatalog = [
    ...layerCatalog.filter((l) => l.group === 'reference'),
    ...layerCatalog.filter((l) => l.group === 'planning'),
    ...layerCatalog.filter((l) => l.group === 'cadastral')
  ];

  orderedCatalog.forEach((cfg, idx) => {
    const wmsLayer = L.tileLayer.wms(STNMT_WMS_URL, {
      layers: cfg.layerName,
      format: 'image/png',
      transparent: true,
      version: '1.1.1',
      uppercase: true,
      opacity: cfg.defaultOpacity,
      minZoom: cfg.minZoom,
      maxZoom: 21,
      zIndex: 200 + idx
    });

    wmsInstances[cfg.id] = { cfg, layer: wmsLayer, active: cfg.defaultOn };
    if (cfg.defaultOn) wmsLayer.addTo(map);
  });

  // Render controls in logical user priority order (Cadastral -> Planning -> Reference)
  layerCatalog.forEach((cfg) => {
    const row = document.createElement('div');
    row.className = 'layer-item';
    const pct = Math.round(cfg.defaultOpacity * 100);
    row.innerHTML = `
      <div class="layer-header">
        <label class="layer-label">
          <input type="checkbox" data-layer-toggle="${cfg.id}" ${cfg.defaultOn ? 'checked' : ''} />
          <span>
            ${esc(cfg.title)}
            <span class="layer-sub">${esc(cfg.subtitle)}</span>
          </span>
        </label>
      </div>
      <div class="opacity-row">
        <span>Độ mờ:</span>
        <input type="range" min="0" max="100" value="${pct}" data-layer-opacity="${cfg.id}" style="--progress:${pct}%" aria-label="Độ mờ lớp ${esc(cfg.title)}" />
        <span class="mono" data-opacity-label="${cfg.id}" style="min-width:34px; text-align:right;">${pct}%</span>
      </div>
    `;
    wmsListEl.appendChild(row);
  });

  wmsListEl.addEventListener('change', (e) => {
    const toggle = e.target.closest('[data-layer-toggle]');
    if (!toggle) return;
    const id = toggle.dataset.layerToggle;
    const entry = wmsInstances[id];
    if (!entry) return;
    entry.active = toggle.checked;
    if (entry.active) entry.layer.addTo(map);
    else map.removeLayer(entry.layer);
  });

  wmsListEl.addEventListener('input', (e) => {
    const range = e.target.closest('[data-layer-opacity]');
    if (!range) return;
    const id = range.dataset.layerOpacity;
    const entry = wmsInstances[id];
    if (!entry) return;
    const val = Number(range.value);
    entry.layer.setOpacity(val / 100);
    range.style.setProperty('--progress', `${val}%`);
    const lbl = wmsListEl.querySelector(`[data-opacity-label="${id}"]`);
    if (lbl) lbl.textContent = `${val}%`;
  });

  // --- 6. Vector Overlay Groups (Highlights, VN-2000, Measure, Custom GeoJSON, Watchlist) ---
  const highlightGroup = L.layerGroup().addTo(map);
  const vn2000Group = L.layerGroup().addTo(map);
  const measureGroup = L.layerGroup().addTo(map);
  const customGeoJsonGroup = L.layerGroup().addTo(map);
  const watchlistMarkersGroup = L.layerGroup().addTo(map);

  // --- 7. Live Coordinate Readout (WGS84 & VN-2000 HCM) ---
  const hcmProj = window.VN2000_ZONES.hcm.proj4;

  function wgsToVn2000(lat, lng, projStr = hcmProj) {
    try {
      const [easting, northing] = proj4('EPSG:4326', projStr, [lng, lat]);
      // Note: On Vietnamese Sổ Hồng, X = Northing (~1,180,000), Y = Easting (~600,000)
      return { x: northing, y: easting };
    } catch {
      return null;
    }
  }

  function vn2000ToWgs(xNorthing, yEasting, projStr = hcmProj) {
    const [lng, lat] = proj4(projStr, 'EPSG:4326', [yEasting, xNorthing]);
    return [lat, lng];
  }

  map.on('mousemove', (e) => {
    const { lat, lng } = e.latlng;
    $('coord-wgs').textContent = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    const vn = wgsToVn2000(lat, lng);
    if (vn) {
      $('coord-vn2000').textContent = `X=${vn.x.toFixed(2)}, Y=${vn.y.toFixed(2)}`;
    }
  });

  map.on('zoomend', () => {
    $('coord-zoom').textContent = String(map.getZoom());
  });

  // --- 8. Quick Jump Selector ---
  const quickSelect = $('quick-jump-select');
  const groupedLocs = {};
  window.QUICK_LOCATIONS.forEach((loc, idx) => {
    if (!groupedLocs[loc.group]) groupedLocs[loc.group] = [];
    groupedLocs[loc.group].push({ ...loc, idx });
  });
  Object.entries(groupedLocs).forEach(([grpName, items]) => {
    const og = document.createElement('optgroup');
    og.label = grpName;
    items.forEach((item) => {
      const opt = document.createElement('option');
      opt.value = String(item.idx);
      opt.textContent = item.name;
      og.appendChild(opt);
    });
    quickSelect.appendChild(og);
  });

  quickSelect.addEventListener('change', () => {
    const loc = window.QUICK_LOCATIONS[Number(quickSelect.value)];
    if (!loc) return;
    map.flyTo([loc.lat, loc.lng], loc.zoom, { duration: 0.7 });
    showToast(`Đã chuyển tới: ${loc.name}`);
  });

  // --- 9. Coordinate Axis Normalizer for GeoServer GeoJSON ---
  // GeoServer sometimes returns [lat, lng] (10.74, 106.66) instead of [lng, lat]
  function toLeafletLatLngs(coords) {
    if (!Array.isArray(coords) || coords.length === 0) return [];
    if (typeof coords[0] === 'number') {
      const a = coords[0], b = coords[1];
      // Vietnam lat is ~8..24, lng is ~102..110
      return (a < 30 && b > 90) ? [a, b] : [b, a];
    }
    return coords.map(toLeafletLatLngs);
  }

  function drawFeatureGeometry(feature, style) {
    if (!feature || !feature.geometry) return null;
    const { type, coordinates } = feature.geometry;
    const latlngs = toLeafletLatLngs(coordinates);
    if (type === 'Polygon' || type === 'MultiPolygon') {
      return L.polygon(latlngs, style).addTo(highlightGroup);
    }
    if (type === 'LineString' || type === 'MultiLineString') {
      return L.polyline(latlngs, style).addTo(highlightGroup);
    }
    return null;
  }

  // --- 10. LIVE WMS GetFeatureInfo Scanner (Batched WAF-Safe Queries + Road Clearance & Price) ---
  let lastInspected = null;

  function pointToSegmentDistMeters(ptLatLng, aCoords, bCoords) {
    // Project to local flat meters around ptLatLng
    const rad = Math.PI / 180;
    const kx = 111320 * Math.cos(ptLatLng.lat * rad);
    const ky = 110540;
    const px = ptLatLng.lng * kx, py = ptLatLng.lat * ky;
    const ax = aCoords[1] * kx, ay = aCoords[0] * ky;
    const bx = bCoords[1] * kx, by = bCoords[0] * ky;
    const dx = bx - ax, dy = by - ay;
    const lenSq = dx * dx + dy * dy;
    let t = lenSq === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / lenSq;
    t = Math.max(0, Math.min(1, t));
    const projX = ax + t * dx;
    const projY = ay + t * dy;
    return Math.hypot(px - projX, py - projY);
  }

  function findNearestRoadClearance(latlng) {
    const list = window.ROAD_CLEARANCE_CORRIDORS || [];
    let best = null;
    let minMeters = Infinity;
    for (const road of list) {
      for (let i = 1; i < road.coords.length; i++) {
        const d = pointToSegmentDistMeters(latlng, road.coords[i - 1], road.coords[i]);
        if (d < minMeters) {
          minMeters = d;
          best = road;
        }
      }
    }
    return best ? { road: best, meters: minMeters } : null;
  }

  function findNearestLandPrice(latlng) {
    const list = window.LAND_PRICES_DATA || [];
    let best = null;
    let minDist = Infinity;
    for (const item of list) {
      const d = latlng.distanceTo(L.latLng(item.lat, item.lng));
      if (d < minDist) {
        minDist = d;
        best = item;
      }
    }
    return best ? { item: best, meters: minDist } : null;
  }

  async function queryWmsBatch(layersCsv, bbox) {
    const params = new URLSearchParams({
      SERVICE: 'WMS',
      VERSION: '1.1.1',
      REQUEST: 'GetFeatureInfo',
      FORMAT: 'image/png',
      TRANSPARENT: 'true',
      QUERY_LAYERS: layersCsv,
      LAYERS: layersCsv,
      INFO_FORMAT: 'application/json',
      FEATURE_COUNT: '10',
      X: '128',
      Y: '128',
      WIDTH: '256',
      HEIGHT: '256',
      SRS: 'EPSG:4326',
      BBOX: bbox
    });
    const resp = await fetch(`${STNMT_WMS_URL}?${params.toString()}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const json = await resp.json();
    return json.features || [];
  }

  async function inspectPoint(latlng) {
    const { lat, lng } = latlng;
    selectTab($('tab-inspect'));
    highlightGroup.clearLayers();
    L.circleMarker([lat, lng], {
      radius: 6,
      color: '#ffffff',
      weight: 2,
      fillColor: '#ff6b00',
      fillOpacity: 1
    }).addTo(highlightGroup);

    $('inspect-coords-badge').textContent = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    $('inspector-content').innerHTML = `
      <div style="padding:14px 0; text-align:center; font-size:12.5px; color:var(--text-muted);">
        ⏳ Đang truy vấn song song Địa chính + Điều chỉnh QH mới nhất + KH SDĐ 2025...
      </div>
    `;

    // Build tight BBOX around clicked point (~40m box at zoom >= 17)
    const delta = map.getZoom() >= 17 ? 0.0004 : 0.0012;
    const bbox = `${lng - delta},${lat - delta},${lng + delta},${lat + delta}`;

    const khAll = window.WMS_LAYERS.KHSDD_2025_ALL.layerName.split(',');
    const batch1 = 'tnmt:v_ranhthua_TPHCM,tnmt:Ranhthua_Quyhoach,tnmt:qhsdd2020,tnmt:ranhphuong_pg';
    const batch2 = window.WMS_LAYERS.QH_2030_SUBURBS.layerName;
    const batch3 = khAll.slice(0, 8).join(',');
    const batch4 = khAll.slice(8, 16).join(',');
    const batch5 = khAll.slice(16).join(',');

    const vn = wgsToVn2000(lat, lng);
    const results = await Promise.allSettled([
      queryWmsBatch(batch1, bbox),
      queryWmsBatch(batch2, bbox),
      queryWmsBatch(batch3, bbox),
      queryWmsBatch(batch4, bbox),
      queryWmsBatch(batch5, bbox)
    ]);

    let features = [];
    let successCount = 0;
    let firstErr = null;
    for (const r of results) {
      if (r.status === 'fulfilled') {
        successCount++;
        features = features.concat(r.value);
      } else if (!firstErr) {
        firstErr = r.reason?.message || 'Lỗi mạng';
      }
    }
    const fetchError = successCount === 0 ? firstErr : null;

    // Categorize returned real features
    const parcelFeat = features.find((f) => f.properties && ('shbando' in f.properties || 'shthua' in f.properties));
    const adjFeat = features.find((f) => (f.id || '').includes('dieuchinh_qh') || (f.properties && 'masdd' in f.properties));
    const qh2030Feat = features.find((f) => (f.id || '').includes('quyhoachsddhuyen_'));
    const kh2025Feat = features.find((f) => (f.id || '').includes('kehoachsddhuyen202'));
    const qhCityFeat = features.find((f) => (f.id || '').includes('quyhoachsdd_') && !(f.id || '').includes('quyhoachsddhuyen_'));
    const adminFeat = features.find((f) => (f.id || '').includes('ranhphuong'));

    // Highlight planning polygon & exact parcel polygon
    const bestPlanHighlight = adjFeat || qh2030Feat || qhCityFeat;
    if (bestPlanHighlight) {
      drawFeatureGeometry(bestPlanHighlight, {
        color: '#f59e0b',
        weight: 2,
        dashArray: '6, 4',
        fillColor: '#f59e0b',
        fillOpacity: 0.14
      });
    }
    if (parcelFeat) {
      drawFeatureGeometry(parcelFeat, {
        color: '#ff2e63',
        weight: 3,
        fillColor: '#ff2e63',
        fillOpacity: 0.25
      });
    }

    const pProps = parcelFeat?.properties || null;
    const planFeat = adjFeat || qh2030Feat || qhCityFeat || null;
    const planProps = planFeat?.properties || null;

    const rawCode = (
      adjFeat?.properties?.masdd ||
      qh2030Feat?.properties?.mucdichsud ||
      qhCityFeat?.properties?.kyhieu ||
      pProps?.kh2003 ||
      pProps?.khloaidat ||
      ''
    ).toString().trim().toUpperCase();

    const nearRoad = findNearestRoadClearance(latlng);
    const nearPrice = findNearestLandPrice(latlng);
    const isNearClearance = nearRoad && nearRoad.meters <= 85;

    const codeMeta = window.LAND_CODES[rawCode] || null;
    const riskLevel = kh2025Feat
      ? 'danger'
      : (isNearClearance && codeMeta?.risk !== 'safe' ? 'danger' : (codeMeta ? codeMeta.risk : 'caution'));
    const riskText = kh2025Feat
      ? '🚨 NẰM TRONG KẾ HOẠCH SDĐ 2024–2025 (CÓ DỰ ÁN / THU HỒI HOẶC CHUYỂN ĐỔI MỚI)'
      : (codeMeta ? codeMeta.riskLabel : (rawCode ? `MÃ ĐẤT: ${rawCode}` : 'NGOÀI PHẠM VI WMS TP.HCM HOẶC CHƯA CÓ MÃ'));

    const wardLabel = adminFeat?.properties
      ? [adminFeat.properties.tenphuong || adminFeat.properties.tenxa || adminFeat.properties.name, adminFeat.properties.tenquan || adminFeat.properties.tenhuyen].filter(Boolean).join(', ')
      : '';

    lastInspected = {
      id: `p_${Date.now()}`,
      lat,
      lng,
      vnX: vn ? Number(vn.x.toFixed(2)) : null,
      vnY: vn ? Number(vn.y.toFixed(2)) : null,
      to: pProps?.shbando ?? null,
      thua: pProps?.shthua ?? null,
      diachi: pProps?.diachi || wardLabel || `${lat.toFixed(5)}, ${lng.toFixed(5)}`,
      dientich: pProps?.dientich || pProps?.dientichpl || null,
      landCode: rawCode || 'N/A',
      landName: planProps?.tenloaidat || planProps?.loaidat || codeMeta?.name || 'Chưa xác định',
      inKh2025: Boolean(kh2025Feat),
      createdAt: new Date().toISOString()
    };

    const sqhktUrl = `https://thongtinquyhoach.hochiminhcity.gov.vn/ban-do-quy-hoach`;
    const streetViewUrl = `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}`;
    const gmapsUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;
    const gulandUrl = `https://guland.vn/soi-quy-hoach/tp-ho-chi-minh`;

    let html = '';
    if (fetchError) {
      html += `<div class="risk-banner risk-caution">Không kết nối được GeoServer Sở TN&MT (${esc(fetchError)}). Vẫn có thể xem tọa độ & mở bản đồ đối chiếu bên dưới.</div>`;
    } else {
      html += `<div class="risk-banner risk-${riskLevel}">${esc(riskText)}</div>`;
    }

    if (isNearClearance) {
      html += `
        <div style="margin-top:8px; padding:9px; border-radius:6px; background:var(--danger-bg); border:1px solid var(--danger); font-size:12px; line-height:1.45;">
          <strong style="color:var(--danger);">🛣️ CẢNH BÁO GIẢI PHÓNG ĐƯỜNG (cách ~${Math.round(nearRoad.meters)}m):</strong><br/>
          <strong>${esc(nearRoad.road.name)}</strong><br/>
          Lộ giới QH: <strong>${esc(nearRoad.road.plannedWidth)}</strong> • ${esc(nearRoad.road.status)}
        </div>
      `;
    }

    if (map.getZoom() < 15) {
      html += `
        <div style="margin-top:8px; display:flex; align-items:center; justify-content:space-between; gap:8px; padding:7px 9px; border-radius:6px; background:var(--accent-bg); font-size:11.5px;">
          <span>Đang ở Zoom ${map.getZoom()} — Zoom ≥ 16 để thấy rõ ranh từng căn nhà.</span>
          <button type="button" class="btn btn-sm btn-primary" id="btn-zoom-parcel">Zoom gần</button>
        </div>
      `;
    }

    if (pProps) {
      html += `
        <div style="margin-top:10px;">
          <div class="section-title" style="margin-bottom:6px;"><span>📄 Thông tin thửa đất (Địa chính thật)</span></div>
          <div class="kv-grid">
            <div class="kv-item">
              <div class="kv-label">Tờ bản đồ / Số thửa</div>
              <div class="kv-val mono">Tờ ${esc(pProps.shbando ?? '—')} • Thửa ${esc(pProps.shthua ?? '—')}</div>
            </div>
            <div class="kv-item">
              <div class="kv-label">Diện tích (m²)</div>
              <div class="kv-val mono">${pProps.dientich ? Number(pProps.dientich).toFixed(1) + ' m²' : '—'}${pProps.dientichpl ? ` (PL: ${Number(pProps.dientichpl).toFixed(1)})` : ''}</div>
            </div>
            <div class="kv-item">
              <div class="kv-label">Loại đất hiện trạng</div>
              <div class="kv-val">${esc(pProps.kh2003 || pProps.khloaidat || '—')}</div>
            </div>
            <div class="kv-item">
              <div class="kv-label">Địa chỉ / Khu vực</div>
              <div class="kv-val">${esc(pProps.diachi || wardLabel || 'Chưa gắn số nhà')}</div>
            </div>
          </div>
        </div>
      `;
    } else if (!fetchError) {
      html += `
        <div style="margin-top:8px; font-size:12px; color:var(--text-muted); line-height:1.5;">
          Không tìm thấy ranh thửa địa chính tại đúng điểm click (có thể điểm nằm trên lòng đường, sông rạch, hoặc ngoài ranh TP.HCM).
        </div>
      `;
    }

    if (planProps) {
      const hex = planProps.color || planProps.mamauhex || codeMeta?.color || '#94a3b8';
      const sourceLabel = adjFeat ? 'Điều chỉnh QH mới nhất' : (qh2030Feat ? 'QH 2030' : 'QH Toàn TP');
      html += `
        <div style="margin-top:10px;">
          <div class="section-title" style="margin-bottom:6px;"><span>🗺️ Quy hoạch sử dụng đất (${sourceLabel})</span></div>
          <div class="kv-grid">
            <div class="kv-item">
              <div class="kv-label">Mã quy hoạch</div>
              <div class="kv-val" style="display:flex; align-items:center; gap:6px;">
                <span class="legend-swatch" style="background:${esc(hex)}"></span>
                <span>${esc(rawCode || '—')}</span>
              </div>
            </div>
            <div class="kv-item">
              <div class="kv-label">Chức năng đất</div>
              <div class="kv-val">${esc(planProps.tenloaidat || planProps.loaidat || codeMeta?.name || '—')}</div>
            </div>
          </div>
          ${planProps.ghichu ? `<div style="margin-top:6px; font-size:12px; color:var(--text-muted);"><strong>Ghi chú Sở TN&MT:</strong> ${esc(planProps.ghichu)}</div>` : ''}
          ${codeMeta?.desc ? `<div style="margin-top:6px; font-size:12px; color:var(--text-muted);">${esc(codeMeta.desc)}</div>` : ''}
        </div>
      `;
    }

    if (kh2025Feat) {
      const khP = kh2025Feat.properties || {};
      const khSummary = Object.entries(khP)
        .filter(([, v]) => v !== null && v !== '' && String(v).length < 140)
        .slice(0, 6)
        .map(([k, v]) => `<code>${esc(k)}</code>: ${esc(v)}`)
        .join(' • ');
      html += `
        <div style="margin-top:10px; padding:9px; border-radius:6px; background:var(--danger-bg); border:1px solid var(--danger); font-size:12px;">
          <strong style="color:var(--danger);">🚨 Phát hiện nằm trong Kế hoạch SDĐ 2024–2025:</strong>
          <div style="margin-top:4px; color:var(--text-main); line-height:1.5;">${khSummary || 'Có dự án/kế hoạch sử dụng đất mới tại khu vực này.'}</div>
        </div>
      `;
    }

    if (nearPrice && nearPrice.meters <= 8000) {
      const lp = nearPrice.item;
      html += `
        <div style="margin-top:10px;">
          <div class="section-title" style="margin-bottom:6px;"><span>💰 Giá đất tham khảo gần nhất (${lp.legalDoc})</span></div>
          <div class="kv-grid">
            <div class="kv-item">
              <div class="kv-label">Bảng giá Nhà nước (VT1)</div>
              <div class="kv-val mono" style="color:var(--caution);">${lp.statePriceV1} tr/m²</div>
            </div>
            <div class="kv-item">
              <div class="kv-label">Giá thị trường (ước tính)</div>
              <div class="kv-val mono" style="color:var(--safe);">${lp.marketRange} tr/m²</div>
            </div>
          </div>
          <div style="margin-top:4px; font-size:11.5px; color:var(--text-muted);">
            Tuyến đối chiếu: <strong>${esc(lp.road)}</strong> (${esc(lp.district)}) • ${esc(lp.yoy)} YoY
          </div>
        </div>
      `;
    }

    html += `
      <div style="margin-top:10px; padding-top:10px; border-top:1px solid var(--border-subtle); display:flex; flex-direction:column; gap:8px;">
        <div class="kv-item">
          <div class="kv-label">Tọa độ thực địa</div>
          <div class="kv-val mono" style="font-size:11.5px;">
            WGS84: ${lat.toFixed(6)}, ${lng.toFixed(6)}<br/>
            VN-2000 (HCM): ${vn ? `X=${vn.x.toFixed(2)} | Y=${vn.y.toFixed(2)}` : '—'}
          </div>
        </div>

        <form id="save-watch-form" style="display:flex; flex-direction:column; gap:6px;">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
            <input type="text" id="watch-price" placeholder="Giá chào (VD: 5.2 tỷ / 85tr/m²)" style="padding:7px 9px; border-radius:6px; border:1px solid var(--border); background:var(--bg-surface); color:var(--text-main); font:inherit; font-size:12px;" />
            <select id="watch-status" style="padding:7px 9px; border-radius:6px; border:1px solid var(--border); background:var(--bg-surface); color:var(--text-main); font:inherit; font-size:12px;">
              <option value="Đang khảo sát">🔎 Đang khảo sát</option>
              <option value="Tiềm năng">✅ Tiềm năng</option>
              <option value="Dính quy hoạch">⚠️ Dính quy hoạch</option>
              <option value="Đã chốt">🏆 Đã chốt</option>
            </select>
          </div>
          <input type="text" id="watch-note" placeholder="Ghi chú riêng (VD: Hẻm 5m, chủ kẹt tiền, lộ giới cắt 2m)..." style="padding:7px 9px; border-radius:6px; border:1px solid var(--border); background:var(--bg-surface); color:var(--text-main); font:inherit; font-size:12px;" />
          <button type="submit" class="btn btn-primary btn-sm">⭐ Lưu thửa đất này vào Sổ tay</button>
        </form>

        <div class="ext-links">
          <a class="ext-link" href="${sqhktUrl}" target="_blank" rel="noopener">🏛️ Sở QH-KT 1/2000</a>
          <a class="ext-link" href="${streetViewUrl}" target="_blank" rel="noopener">👁️ Street View thực tế</a>
          <a class="ext-link" href="${gmapsUrl}" target="_blank" rel="noopener">📍 Google Maps</a>
          <a class="ext-link" href="${gulandUrl}" target="_blank" rel="noopener">🗺️ Mở Guland</a>
        </div>
      </div>
    `;

    $('inspector-content').innerHTML = html;

    const zoomBtn = $('btn-zoom-parcel');
    if (zoomBtn) {
      zoomBtn.addEventListener('click', () => {
        map.flyTo([lat, lng], 17, { duration: 0.6 });
      });
    }

    const saveForm = $('save-watch-form');
    if (saveForm) {
      saveForm.addEventListener('submit', (ev) => {
        ev.preventDefault();
        if (!lastInspected) return;
        const item = {
          ...lastInspected,
          price: $('watch-price').value.trim() || 'Chưa nhập giá',
          status: $('watch-status').value,
          note: $('watch-note').value.trim()
        };
        addToWatchlist(item);
        showToast('Đã lưu thửa đất vào Sổ tay cá nhân!');
      });
    }
  }

  // --- 11. Interactive Map Modes (Inspect / Measure Distance / Measure Area) ---
  let mapMode = 'inspect'; // 'inspect' | 'dist' | 'area'
  let measurePoints = [];

  function setMapMode(mode) {
    mapMode = mode;
    $('tool-inspect').classList.toggle('btn-active', mode === 'inspect');
    $('tool-dist').classList.toggle('btn-active', mode === 'dist');
    $('tool-area').classList.toggle('btn-active', mode === 'area');

    const hud = $('measure-hud');
    if (mode === 'inspect') {
      hud.hidden = true;
      map.getContainer().style.cursor = '';
    } else {
      measurePoints = [];
      measureGroup.clearLayers();
      hud.hidden = false;
      $('measure-mode-label').textContent = mode === 'dist' ? '📏 Đang đo khoảng cách / lộ giới' : '⬛ Đang đo diện tích khu đất';
      $('measure-output').textContent = mode === 'dist' ? '0.0 m' : '0.0 m²';
      map.getContainer().style.cursor = 'crosshair';
    }
  }

  // Spherical polygon area (m²) using Shoelace on Earth sphere
  function computeSphericalArea(latlngs) {
    if (latlngs.length < 3) return 0;
    const R = 6378137;
    const rad = Math.PI / 180;
    let total = 0;
    for (let i = 0; i < latlngs.length; i++) {
      const p1 = latlngs[i];
      const p2 = latlngs[(i + 1) % latlngs.length];
      total += (p2.lng - p1.lng) * rad * (2 + Math.sin(p1.lat * rad) + Math.sin(p2.lat * rad));
    }
    return Math.abs(total * R * R / 2);
  }

  function renderMeasurement() {
    measureGroup.clearLayers();
    if (measurePoints.length === 0) return;

    measurePoints.forEach((pt, idx) => {
      L.circleMarker(pt, {
        radius: 5,
        color: '#ffffff',
        weight: 2,
        fillColor: '#ff6b00',
        fillOpacity: 1
      }).bindTooltip(`Đ${idx + 1}`, { permanent: false }).addTo(measureGroup);
    });

    if (mapMode === 'dist') {
      L.polyline(measurePoints, { color: '#ff6b00', weight: 3, dashArray: '6, 4' }).addTo(measureGroup);
      let totalDist = 0;
      for (let i = 1; i < measurePoints.length; i++) {
        const seg = measurePoints[i - 1].distanceTo(measurePoints[i]);
        totalDist += seg;
        const mid = L.latLng(
          (measurePoints[i - 1].lat + measurePoints[i].lat) / 2,
          (measurePoints[i - 1].lng + measurePoints[i].lng) / 2
        );
        L.tooltip({ permanent: true, direction: 'center', className: 'mono' })
          .setLatLng(mid)
          .setContent(`${seg.toFixed(1)}m`)
          .addTo(measureGroup);
      }
      $('measure-output').textContent = totalDist >= 1000
        ? `${totalDist.toFixed(1)} m (${(totalDist / 1000).toFixed(3)} km)`
        : `${totalDist.toFixed(2)} m`;
    } else if (mapMode === 'area') {
      L.polygon(measurePoints, { color: '#10b981', weight: 2.5, fillColor: '#10b981', fillOpacity: 0.25 }).addTo(measureGroup);
      let perim = 0;
      for (let i = 0; i < measurePoints.length; i++) {
        perim += measurePoints[i].distanceTo(measurePoints[(i + 1) % measurePoints.length]);
      }
      const area = computeSphericalArea(measurePoints);
      $('measure-output').textContent = area >= 10000
        ? `${area.toFixed(1)} m² (${(area / 10000).toFixed(3)} ha) • Chu vi ${perim.toFixed(1)}m`
        : `${area.toFixed(1)} m² • Chu vi ${perim.toFixed(1)}m`;
    }
  }

  map.on('click', (e) => {
    if (mapMode === 'inspect') {
      inspectPoint(e.latlng);
    } else {
      measurePoints.push(e.latlng);
      renderMeasurement();
    }
  });

  $('tool-inspect').addEventListener('click', () => setMapMode('inspect'));
  $('tool-dist').addEventListener('click', () => setMapMode('dist'));
  $('tool-area').addEventListener('click', () => setMapMode('area'));
  $('btn-stop-measure').addEventListener('click', () => setMapMode('inspect'));
  $('tool-clear').addEventListener('click', () => {
    measurePoints = [];
    measureGroup.clearLayers();
    highlightGroup.clearLayers();
    setMapMode('inspect');
    showToast('Đã xóa các nét đo và đánh dấu tạm.');
  });

  $('btn-measure-dist-side').addEventListener('click', () => setMapMode('dist'));
  $('btn-measure-area-side').addEventListener('click', () => setMapMode('area'));
  $('btn-measure-clear-side').addEventListener('click', () => {
    measurePoints = [];
    measureGroup.clearLayers();
    setMapMode('inspect');
  });

  // --- 12. Smart Address & Coordinate Search (WGS84, VN-2000, Local Roads, Nominatim w/ fallback) ---
  async function geocodeNominatim(query) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=vn&viewbox=105.8,11.6,107.6,10.2&q=${encodeURIComponent(query + ', Việt Nam')}`;
    const res = await fetch(url, { headers: { 'Accept-Language': 'vi' } });
    return await res.json();
  }

  $('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const q = $('search-input').value.trim();
    if (!q) return;

    // 1. Direct WGS84 "lat, lng"
    const wgsMatch = q.match(/^\s*(-?\d{1,2}\.\d+)\s*[,;\s]\s*(-?\d{2,3}\.\d+)\s*$/);
    if (wgsMatch) {
      const lat = parseFloat(wgsMatch[1]);
      const lng = parseFloat(wgsMatch[2]);
      map.flyTo([lat, lng], 18, { duration: 0.7 });
      inspectPoint(L.latLng(lat, lng));
      return;
    }

    // 2. Direct VN-2000 "X, Y" (Northing ~ 1100000+, Easting ~ 500000-750000)
    const vnMatch = q.match(/^\s*(\d{6,7}(?:\.\d+)?)\s*[,;\s]\s*(\d{6,7}(?:\.\d+)?)\s*$/);
    if (vnMatch) {
      let a = parseFloat(vnMatch[1]), b = parseFloat(vnMatch[2]);
      let x = a, y = b;
      if (a < 900000 && b > 900000) { x = b; y = a; }
      const [lat, lng] = vn2000ToWgs(x, y);
      map.flyTo([lat, lng], 18, { duration: 0.7 });
      inspectPoint(L.latLng(lat, lng));
      showToast(`Đã chuyển tọa độ VN-2000 tới ${lat.toFixed(5)}, ${lng.toFixed(5)}`);
      return;
    }

    // 3. Instant local match (Land Prices / Quick Locations)
    const qLow = q.toLowerCase();
    const localHit = (window.LAND_PRICES_DATA || []).find((p) =>
      p.road.toLowerCase().includes(qLow) || p.district.toLowerCase().includes(qLow)
    ) || (window.QUICK_LOCATIONS || []).find((l) => l.name.toLowerCase().includes(qLow));

    showToast(`Đang tìm "${q}"...`);
    try {
      let data = await geocodeNominatim(q);
      // Fallback: strip leading house number (e.g. "57/5 Bông Sao Quận 8" -> "Bông Sao Quận 8")
      if (!data.length) {
        const stripped = q.replace(/^\s*\d+[A-Za-z0-9\/\-]*\s+/, '').trim();
        if (stripped && stripped !== q) {
          data = await geocodeNominatim(stripped);
        }
      }
      if (data.length) {
        const lat = parseFloat(data[0].lat);
        const lng = parseFloat(data[0].lon);
        map.flyTo([lat, lng], 17, { duration: 0.8 });
        inspectPoint(L.latLng(lat, lng));
        showToast(`Đã tìm thấy: ${data[0].display_name.split(',').slice(0, 3).join(', ')}`);
        return;
      }
      if (localHit) {
        map.flyTo([localHit.lat, localHit.lng], localHit.zoom || 16, { duration: 0.8 });
        inspectPoint(L.latLng(localHit.lat, localHit.lng));
        showToast(`Đã chuyển tới khu vực: ${localHit.road || localHit.name}`);
        return;
      }
      showToast('Không tìm thấy địa chỉ này. Thử nhập tên đường + Quận/Huyện hoặc tọa độ.');
    } catch {
      if (localHit) {
        map.flyTo([localHit.lat, localHit.lng], localHit.zoom || 16, { duration: 0.8 });
        inspectPoint(L.latLng(localHit.lat, localHit.lng));
      } else {
        showToast('Lỗi kết nối dịch vụ tìm địa chỉ.');
      }
    }
  });

  // --- 13. GPS Geolocation ---
  $('btn-gps').addEventListener('click', () => {
    if (!navigator.geolocation) {
      showToast('Trình duyệt không hỗ trợ GPS.');
      return;
    }
    showToast('Đang xác định vị trí GPS...');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        map.flyTo([latitude, longitude], 18, { duration: 0.8 });
        inspectPoint(L.latLng(latitude, longitude));
        showToast('Đã định vị tới vị trí hiện tại!');
      },
      () => showToast('Không thể lấy vị trí GPS. Kiểm tra quyền truy cập vị trí.')
    );
  });

  // --- 14. VN-2000 Multi-Vertex Sổ Hồng Parcel Plotter ---
  const vnZoneSelect = $('vn2000-zone');
  Object.entries(window.VN2000_ZONES).forEach(([key, val]) => {
    const opt = document.createElement('option');
    opt.value = key;
    opt.textContent = val.label;
    vnZoneSelect.appendChild(opt);
  });

  $('btn-plot-vn2000').addEventListener('click', () => {
    const raw = $('vn2000-input').value.trim();
    if (!raw) {
      showToast('Vui lòng nhập ít nhất 1 cặp tọa độ X Y.');
      return;
    }
    const projStr = window.VN2000_ZONES[vnZoneSelect.value].proj4;
    const lines = raw.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
    const pts = [];

    for (const line of lines) {
      const nums = line.replace(/,/g, ' ').match(/-?\d+(\.\d+)?/g);
      if (!nums || nums.length < 2) continue;
      let a = parseFloat(nums[0]);
      let b = parseFloat(nums[1]);
      // Auto-detect X (Northing ~1,100,000+) vs Y (Easting ~500,000-700,000)
      let x = a, y = b;
      if (a < 900000 && b > 900000) { x = b; y = a; }
      const [lat, lng] = vn2000ToWgs(x, y, projStr);
      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        pts.push(L.latLng(lat, lng));
      }
    }

    if (pts.length === 0) {
      showToast('Định dạng tọa độ VN-2000 không hợp lệ.');
      return;
    }

    vn2000Group.clearLayers();
    if (pts.length === 1) {
      L.marker(pts[0]).bindPopup(`Điểm VN-2000<br/>${pts[0].lat.toFixed(6)}, ${pts[0].lng.toFixed(6)}`).addTo(vn2000Group).openPopup();
      map.flyTo(pts[0], 19, { duration: 0.7 });
      $('vn2000-result').innerHTML = `✅ Đã ghim 1 điểm tọa độ tại <code class="mono">${pts[0].lat.toFixed(6)}, ${pts[0].lng.toFixed(6)}</code>`;
      inspectPoint(pts[0]);
    } else {
      const poly = L.polygon(pts, {
        color: '#06b6d4',
        weight: 3,
        fillColor: '#06b6d4',
        fillOpacity: 0.25
      }).addTo(vn2000Group);

      pts.forEach((pt, idx) => {
        L.circleMarker(pt, { radius: 4, color: '#fff', weight: 1.5, fillColor: '#06b6d4', fillOpacity: 1 })
          .bindTooltip(`Mốc ${idx + 1}`, { permanent: false })
          .addTo(vn2000Group);
      });

      const area = computeSphericalArea(pts);
      let perim = 0;
      for (let i = 0; i < pts.length; i++) {
        perim += pts[i].distanceTo(pts[(i + 1) % pts.length]);
      }
      map.fitBounds(poly.getBounds().pad(0.4), { maxZoom: 19 });
      $('vn2000-result').innerHTML = `
        <div class="risk-banner risk-safe" style="margin-top:6px;">
          ✅ Đã vẽ khung sổ hồng (${pts.length} đỉnh)<br/>
          Diện tích tính toán: <span class="mono">${area.toFixed(1)} m²</span> • Chu vi: <span class="mono">${perim.toFixed(1)} m</span>
        </div>
      `;
      inspectPoint(poly.getBounds().getCenter());
    }
  });

  $('btn-clear-vn2000').addEventListener('click', () => {
    vn2000Group.clearLayers();
    $('vn2000-result').innerHTML = '';
    showToast('Đã xóa khung tọa độ VN-2000.');
  });

  // --- 15. Custom GeoJSON Upload ---
  $('geojson-file-input').addEventListener('change', (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const gj = JSON.parse(reader.result);
        const layer = L.geoJSON(gj, {
          style: { color: '#a855f7', weight: 2.5, fillColor: '#a855f7', fillOpacity: 0.22 },
          onEachFeature: (f, l) => {
            if (f.properties) {
              const rows = Object.entries(f.properties).slice(0, 8).map(([k, v]) => `<b>${esc(k)}</b>: ${esc(v)}`).join('<br/>');
              l.bindPopup(rows);
            }
          }
        }).addTo(customGeoJsonGroup);
        if (layer.getBounds().isValid()) map.fitBounds(layer.getBounds().pad(0.2));
        showToast(`Đã nạp thành công lớp GeoJSON: ${file.name}`);
      } catch {
        showToast('File không phải GeoJSON hợp lệ.');
      }
    };
    reader.readAsText(file);
  });

  $('btn-clear-geojson').addEventListener('click', () => {
    customGeoJsonGroup.clearLayers();
    $('geojson-file-input').value = '';
    showToast('Đã xóa lớp GeoJSON nạp thêm.');
  });

  // --- 16. Personal Watchlist (localStorage + CSV/JSON Export) ---
  function loadWatchlist() {
    try {
      return JSON.parse(localStorage.getItem(WATCHLIST_KEY) || '[]');
    } catch {
      return [];
    }
  }

  function saveWatchlist(list) {
    try { localStorage.setItem(WATCHLIST_KEY, JSON.stringify(list)); } catch {}
    renderWatchlist();
  }

  function addToWatchlist(item) {
    const list = loadWatchlist();
    list.unshift(item);
    saveWatchlist(list);
  }

  function renderWatchlist() {
    const list = loadWatchlist();
    $('watch-count').textContent = String(list.length);
    const container = $('watchlist-items');
    watchlistMarkersGroup.clearLayers();

    if (list.length === 0) {
      container.innerHTML = `<div style="font-size:12px; color:var(--text-muted); padding:8px 0;">Chưa có thửa đất nào được lưu.</div>`;
      return;
    }

    container.innerHTML = list.map((item) => `
      <div class="watch-item">
        <div class="watch-top">
          <div class="watch-title">${esc(item.diachi)}</div>
          <span class="mono" style="font-size:11px; font-weight:700; color:var(--accent);">${esc(item.landCode)}</span>
        </div>
        <div class="watch-meta">
          ${item.to ? `<strong>Tờ ${esc(item.to)} • Thửa ${esc(item.thua)}</strong> | ` : ''}
          ${item.dientich ? `DT: <strong>${Number(item.dientich).toFixed(1)} m²</strong> | ` : ''}
          Giá: <strong>${esc(item.price)}</strong><br/>
          Trạng thái: <strong>${esc(item.status)}</strong>${item.inKh2025 ? ' • <span style="color:var(--danger); font-weight:700;">KH SDĐ 2024-2025</span>' : ''}
          ${item.note ? `<br/>Ghi chú: ${esc(item.note)}` : ''}
        </div>
        <div class="watch-actions">
          <button type="button" class="btn btn-sm" data-watch-fly="${item.id}">📍 Xem trên bản đồ</button>
          <button type="button" class="btn btn-sm" data-watch-del="${item.id}">🗑️ Xóa</button>
        </div>
      </div>
    `).join('');

    list.forEach((item) => {
      L.marker([item.lat, item.lng])
        .bindPopup(`<strong>${esc(item.diachi)}</strong><br/>${esc(item.landCode)} • ${esc(item.price)}<br/>${esc(item.note || '')}`)
        .addTo(watchlistMarkersGroup);
    });
  }

  $('watchlist-items').addEventListener('click', (e) => {
    const flyBtn = e.target.closest('[data-watch-fly]');
    if (flyBtn) {
      const item = loadWatchlist().find((x) => x.id === flyBtn.dataset.watchFly);
      if (item) {
        map.flyTo([item.lat, item.lng], 18, { duration: 0.7 });
        inspectPoint(L.latLng(item.lat, item.lng));
      }
      return;
    }
    const delBtn = e.target.closest('[data-watch-del]');
    if (delBtn) {
      const list = loadWatchlist().filter((x) => x.id !== delBtn.dataset.watchDel);
      saveWatchlist(list);
      showToast('Đã xóa khỏi Sổ tay.');
    }
  });

  function downloadFile(content, filename, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }

  $('btn-export-json').addEventListener('click', () => {
    const list = loadWatchlist();
    if (!list.length) return showToast('Chưa có dữ liệu để xuất.');
    downloadFile(JSON.stringify(list, null, 2), `my-hcm-gis-watchlist-${Date.now()}.json`, 'application/json');
  });

  $('btn-export-csv').addEventListener('click', () => {
    const list = loadWatchlist();
    if (!list.length) return showToast('Chưa có dữ liệu để xuất.');
    const header = ['DiaChi', 'SoTo', 'SoThua', 'DienTich_m2', 'MaDat', 'LoaiDat', 'KHSDD_2025', 'GiaChao', 'TrangThai', 'GhiChu', 'Lat', 'Lng', 'VN2000_X', 'VN2000_Y'];
    const rows = list.map((x) => [
      x.diachi, x.to ?? '', x.thua ?? '', x.dientich ?? '', x.landCode, x.landName, x.inKh2025 ? 'CO' : 'KHONG',
      x.price, x.status, x.note || '', x.lat, x.lng, x.vnX ?? '', x.vnY ?? ''
    ].map((v) => `"${String(v).replace(/"/g, '""')}"`).join(','));
    downloadFile('\uFEFF' + [header.join(','), ...rows].join('\n'), `my-hcm-gis-watchlist-${Date.now()}.csv`, 'text/csv;charset=utf-8');
  });

  // --- 17. Populate Legend Modal ---
  const legendGrid = $('legend-grid');
  Object.entries(window.LAND_CODES).forEach(([code, info]) => {
    const div = document.createElement('div');
    div.className = 'legend-chip';
    div.innerHTML = `
      <span class="legend-swatch" style="background:${esc(info.color)}"></span>
      <div>
        <strong>${esc(code)}</strong> — ${esc(info.name)}
      </div>
    `;
    legendGrid.appendChild(div);
  });

  // --- 18. Sidebar Toggle ---
  $('btn-toggle-sidebar').addEventListener('click', () => {
    $('app-shell').classList.toggle('sidebar-collapsed');
    setTimeout(() => map.invalidateSize(), 200);
  });

  // --- 19. Planned Road Clearance Corridors (2025-2026) ---
  const clearanceRoadsGroup = L.layerGroup().addTo(map);
  const toggleClearanceRoads = $('toggle-clearance-roads');

  function renderClearanceRoadsOnMap() {
    clearanceRoadsGroup.clearLayers();
    if (!toggleClearanceRoads || !toggleClearanceRoads.checked) return;

    (window.ROAD_CLEARANCE_CORRIDORS || []).forEach((road) => {
      const line = L.polyline(road.coords, {
        color: road.color,
        weight: 5,
        dashArray: '8, 6',
        opacity: 0.9
      }).addTo(clearanceRoadsGroup);

      line.bindTooltip(`
        <div style="font-family:'Be Vietnam Pro',sans-serif; font-size:12px; line-height:1.4;">
          <strong style="color:${esc(road.color)};">🛣️ ${esc(road.name)}</strong><br/>
          Lộ giới QH: <strong>${esc(road.plannedWidth)}</strong><br/>
          <span style="color:#64748b;">${esc(road.status)}</span>
        </div>
      `, { sticky: true });

      line.bindPopup(`
        <div style="font-family:'Be Vietnam Pro',sans-serif; font-size:12.5px; max-width:280px; line-height:1.5;">
          <strong style="color:${esc(road.color)};">🛣️ ${esc(road.name)}</strong><br/>
          <strong>Khu vực:</strong> ${esc(road.district)}<br/>
          <strong>Lộ giới QH:</strong> <span style="color:#ef4444; font-weight:700;">${esc(road.plannedWidth)}</span><br/>
          <strong>Hiện hữu:</strong> ${esc(road.existingWidth)}<br/>
          <strong>Tiến độ:</strong> ${esc(road.status)}<br/>
          <strong>Tác động GPMB:</strong> ${esc(road.impact)}
        </div>
      `);
    });
  }

  if (toggleClearanceRoads) {
    toggleClearanceRoads.addEventListener('change', renderClearanceRoadsOnMap);
  }
  renderClearanceRoadsOnMap();

  function renderRoadsList(filter = '') {
    const container = $('roads-list');
    if (!container) return;
    const q = filter.trim().toLowerCase();
    const items = (window.ROAD_CLEARANCE_CORRIDORS || []).filter((r) =>
      !q || r.name.toLowerCase().includes(q) || r.district.toLowerCase().includes(q) || r.status.toLowerCase().includes(q)
    );

    if (!items.length) {
      container.innerHTML = `<div style="font-size:12px; color:var(--text-muted);">Không tìm thấy tuyến đường phù hợp.</div>`;
      return;
    }

    container.innerHTML = items.map((r) => `
      <div class="watch-item">
        <div class="watch-top">
          <div class="watch-title" style="color:${esc(r.color)};">🛣️ ${esc(r.name)}</div>
        </div>
        <div class="watch-meta">
          <strong>${esc(r.district)}</strong> • Lộ giới QH: <strong style="color:var(--danger);">${esc(r.plannedWidth)}</strong><br/>
          Hiện hữu: ${esc(r.existingWidth)}<br/>
          <strong>Tiến độ:</strong> ${esc(r.status)}<br/>
          ${esc(r.impact)}
        </div>
        <div class="watch-actions">
          <button type="button" class="btn btn-sm btn-primary" data-road-fly="${esc(r.id)}">📍 Xem tuyến trên bản đồ</button>
        </div>
      </div>
    `).join('');
  }

  if ($('road-filter-input')) {
    $('road-filter-input').addEventListener('input', (e) => renderRoadsList(e.target.value));
  }
  if ($('roads-list')) {
    $('roads-list').addEventListener('click', (e) => {
      const btn = e.target.closest('[data-road-fly]');
      if (!btn) return;
      const road = (window.ROAD_CLEARANCE_CORRIDORS || []).find((r) => r.id === btn.dataset.roadFly);
      if (!road) return;
      if (toggleClearanceRoads && !toggleClearanceRoads.checked) {
        toggleClearanceRoads.checked = true;
        renderClearanceRoadsOnMap();
      }
      const bounds = L.latLngBounds(road.coords);
      map.fitBounds(bounds.pad(0.25), { maxZoom: 15 });
      showToast(`Đang xem tuyến giải tỏa: ${road.name}`);
    });
  }
  renderRoadsList();

  // --- 20. Land Prices (QD 79/2024) & Land Conversion Tax Calculator ---
  function renderPricesList(filter = '') {
    const container = $('prices-list');
    if (!container) return;
    const q = filter.trim().toLowerCase();
    const items = (window.LAND_PRICES_DATA || []).filter((p) =>
      !q || p.road.toLowerCase().includes(q) || p.district.toLowerCase().includes(q) || p.area.toLowerCase().includes(q)
    );

    if (!items.length) {
      container.innerHTML = `<div style="font-size:12px; color:var(--text-muted);">Không có tuyến đường phù hợp.</div>`;
      return;
    }

    container.innerHTML = items.map((p) => `
      <div class="watch-item">
        <div class="watch-top">
          <div class="watch-title">${esc(p.road)}</div>
          <span class="mono" style="font-size:11px; font-weight:700; color:var(--safe);">${esc(p.yoy)}</span>
        </div>
        <div class="watch-meta">
          <strong>${esc(p.district)}</strong> • ${esc(p.legalDoc)} • Mã: <strong>${esc(p.zoning)}</strong><br/>
          Bảng giá NN (VT1): <strong class="mono" style="color:var(--caution);">${p.statePriceV1} tr/m²</strong> | Thị trường: <strong class="mono" style="color:var(--safe);">${esc(p.marketRange)} tr/m²</strong><br/>
          ${esc(p.note)}
        </div>
        <div class="watch-actions">
          <button type="button" class="btn btn-sm btn-primary" data-price-fly="${esc(p.id)}">📍 Soi vị trí trên bản đồ</button>
        </div>
      </div>
    `).join('');
  }

  if ($('price-filter-input')) {
    $('price-filter-input').addEventListener('input', (e) => renderPricesList(e.target.value));
  }
  if ($('prices-list')) {
    $('prices-list').addEventListener('click', (e) => {
      const btn = e.target.closest('[data-price-fly]');
      if (!btn) return;
      const item = (window.LAND_PRICES_DATA || []).find((p) => p.id === btn.dataset.priceFly);
      if (!item) return;
      map.flyTo([item.lat, item.lng], 16, { duration: 0.7 });
      inspectPoint(L.latLng(item.lat, item.lng));
    });
  }
  renderPricesList();

  const calcRoadSelect = $('calc-road-select');
  const calcAreaInput = $('calc-area');
  const calcPosSelect = $('calc-position');
  const calcOutput = $('calc-output');

  function updateConversionCalc() {
    if (!calcRoadSelect || !calcOutput) return;
    const item = (window.LAND_PRICES_DATA || []).find((p) => p.id === calcRoadSelect.value);
    if (!item) return;
    const area = Math.max(0, Number(calcAreaInput.value) || 0);
    const posFactor = Number(calcPosSelect.value) || 1;
    // Bảng giá đất ở theo vị trí trừ giá đất nông nghiệp ước tính (~1.5 - 2.5 tr/m²)
    const stateUnitPrice = item.statePriceV1 * posFactor;
    const agriDeduct = item.area.includes('Vùng Ven') ? 0.8 : 2.0;
    const diffUnit = Math.max(0, stateUnitPrice - agriDeduct);
    const totalMillions = diffUnit * area;
    const regFee = stateUnitPrice * area * 0.005; // 0.5% lệ phí trước bạ

    calcOutput.innerHTML = `
      <div>Đơn giá Nhà nước áp dụng: <span class="mono">${stateUnitPrice.toFixed(1)} tr/m²</span></div>
      <div>Tiền sử dụng đất lên thổ cư (100% chênh lệch): <span class="mono" style="font-size:14px; color:var(--danger);">${(totalMillions / 1000).toFixed(2)} tỷ VNĐ</span> (${totalMillions.toFixed(0)} tr)</div>
      <div style="font-size:11.5px; color:var(--text-muted); margin-top:3px;">Lệ phí trước bạ (0,5%): ~${regFee.toFixed(1)} tr • Tham khảo theo ${esc(item.legalDoc)}.</div>
    `;
  }

  if (calcRoadSelect) {
    (window.LAND_PRICES_DATA || []).forEach((p) => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = `${p.district} — ${p.road} (${p.statePriceV1} tr/m²)`;
      calcRoadSelect.appendChild(opt);
    });
    calcRoadSelect.addEventListener('change', updateConversionCalc);
    calcAreaInput.addEventListener('input', updateConversionCalc);
    calcPosSelect.addEventListener('change', updateConversionCalc);
    updateConversionCalc();
  }

  // Initial load
  renderWatchlist();
})();
