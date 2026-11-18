with open('projects/hcm-traffic-cams/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update DISTRICT_LIST and DISTRICT_CENTERS
target_start = """    const DISTRICT_LIST = [
      'Quận 1', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 10', 'Quận 11', 'Quận 12',
      'Quận Bình Thạnh', 'Quận Gò Vấp', 'Quận Phú Nhuận', 'Quận Tân Bình', 'Quận Tân Phú', 'Quận Bình Tân',
      'TP Thủ Đức', 'Huyện Bình Chánh', 'Huyện Hóc Môn', 'Huyện Củ Chi', 'Huyện Nhà Bè'
    ];

    const DISTRICT_CENTERS = {
      'Quận 1': [10.78545, 106.69358],
      'Quận 3': [10.78188, 106.68387],
      'Quận 4': [10.76075, 106.7086],
      'Quận 5': [10.75556, 106.6657],
      'Quận 6': [10.75047, 106.64075],
      'Quận 7': [10.73775, 106.71989],
      'Quận 8': [10.72709, 106.65047],
      'Quận 10': [10.77096, 106.66648],
      'Quận 11': [10.76786, 106.64964],
      'Quận 12': [10.85549, 106.65696],
      'Quận Bình Thạnh': [10.8082, 106.71324],
      'Quận Gò Vấp': [10.83165, 106.679],
      'Quận Phú Nhuận': [10.799, 106.67839],
      'Quận Tân Bình': [10.80107, 106.65611],
      'Quận Tân Phú': [10.7832, 106.62518],
      'Quận Bình Tân': [10.76317, 106.59794],
      'TP Thủ Đức': [10.80258, 106.74403],
      'Huyện Bình Chánh': [10.69895, 106.58705],
      'Huyện Hóc Môn': [10.87983, 106.59929],
      'Huyện Củ Chi': [10.98612, 106.57164],
      'Huyện Nhà Bè': [10.70613, 106.73108]
    };"""

replacement_districts = """    const DEFAULT_HCM_DISTRICT_LIST = [
      'Quận 1', 'Quận 3', 'Quận 4', 'Quận 5', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 10', 'Quận 11', 'Quận 12',
      'Quận Bình Thạnh', 'Quận Gò Vấp', 'Quận Phú Nhuận', 'Quận Tân Bình', 'Quận Tân Phú', 'Quận Bình Tân',
      'TP Thủ Đức', 'Huyện Bình Chánh', 'Huyện Hóc Môn', 'Huyện Củ Chi', 'Huyện Nhà Bè'
    ];

    function getActiveDistrictList() {
      const prov = PROVINCES[currentProvince];
      return (prov && prov.districts) ? prov.districts : DEFAULT_HCM_DISTRICT_LIST;
    }

    function getActiveDistrictCenters() {
      const prov = PROVINCES[currentProvince];
      return (prov && prov.centers) ? prov.centers : PROVINCES.HCM.centers;
    }"""

assert target_start in code, "target_start not found"
code = code.replace(target_start, replacement_districts)

# 2. Update fetchLiveRainData
old_fetch_rain = """async function fetchLiveRainData() {
      try {
        const lats = DISTRICT_LIST.map(d => DISTRICT_CENTERS[d][0]).join(',');
        const lons = DISTRICT_LIST.map(d => DISTRICT_CENTERS[d][1]).join(',');
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lats}&longitude=${lons}&current=precipitation,rain,showers,weather_code,temperature_2m&timezone=Asia%2FHo_Chi_Minh`;
        
        const res = await fetch(url);
        const data = await res.json();
        
        let rainCount = 0;
        const results = Array.isArray(data) ? data : [data];
        
        DISTRICT_LIST.forEach((d, idx) => {
          const loc = results[idx] || {};
          const c = loc.current || {};
          const code = c.weather_code || 0;
          const rain = (c.rain || 0) + (c.showers || 0);
          const precip = c.precipitation || 0;
          const isRain = (code >= 51 && code <= 67) || (code >= 80 && code <= 82) || code >= 95 || rain > 0 || precip > 0;
          const rainAmount = Math.max(rain, precip);
          
          districtRainData[d] = {
            isRaining: isRain,
            rainMm: rainAmount,
            temp: c.temperature_2m || 27,
            code: code,
            desc: getWeatherDesc(code, rainAmount)
          };

          if (isRain) rainCount++;
        });

        // Update Header Rain Pill
        const rainPill = document.getElementById('rainStatusText');
        const rainBadge = document.getElementById('rainStatusPill');
        if (rainPill && rainBadge) {
          if (rainCount > 0) {
            rainPill.textContent = `${rainCount}/21 Quận Có Mưa`;
            rainBadge.className = 'flex items-center gap-1.5 text-cyan-300 hover:text-cyan-200 cursor-pointer transition select-none bg-cyan-950/70 px-2.5 py-1 rounded-lg border border-cyan-500/40 shadow-sm shadow-cyan-500/20';
          } else {
            rainPill.textContent = `Toàn TP Tạnh Ráo`;
            rainBadge.className = 'flex items-center gap-1.5 text-slate-300 hover:text-white cursor-pointer transition select-none';
          }
        }

        // Update Option in District Select
        const optionRaining = document.getElementById('optionRainingDistricts');
        if (optionRaining) {
          optionRaining.textContent = `🌧️ Khu Vực Đang Mưa (${rainCount} quận)`;
        }

        // Re-render markers & sidebar with updated rain badges if currently on map
        if (currentTab === 'map') {
          renderMapMarkers();
          renderDistrictQuickViews();
        }
      } catch (err) {
        console.warn('Weather rain fetch error:', err);
      }
    }"""

new_fetch_rain = """async function fetchLiveRainData() {
      try {
        const activeList = getActiveDistrictList();
        const activeCenters = getActiveDistrictCenters();
        const prov = PROVINCES[currentProvince] || PROVINCES.HCM;

        const lats = activeList.map(d => activeCenters[d] ? activeCenters[d][0] : prov.center[0]).join(',');
        const lons = activeList.map(d => activeCenters[d] ? activeCenters[d][1] : prov.center[1]).join(',');
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${lats}&longitude=${lons}&current=precipitation,rain,showers,weather_code,temperature_2m&timezone=Asia%2FHo_Chi_Minh`;
        
        const res = await fetch(url);
        const data = await res.json();
        
        let rainCount = 0;
        const results = Array.isArray(data) ? data : [data];
        
        activeList.forEach((d, idx) => {
          const loc = results[idx] || {};
          const c = loc.current || {};
          const code = c.weather_code || 0;
          const rain = (c.rain || 0) + (c.showers || 0);
          const precip = c.precipitation || 0;
          const isRain = (code >= 51 && code <= 67) || (code >= 80 && code <= 82) || code >= 95 || rain > 0 || precip > 0;
          const rainAmount = Math.max(rain, precip);
          
          districtRainData[d] = {
            isRaining: isRain,
            rainMm: rainAmount,
            temp: c.temperature_2m || 27,
            code: code,
            desc: getWeatherDesc(code, rainAmount)
          };

          if (isRain) rainCount++;
        });

        // Update Header Rain Pill
        const rainPill = document.getElementById('rainStatusText');
        const rainBadge = document.getElementById('rainStatusPill');
        const optionRaining = document.getElementById('optionRainingDistricts');

        if (rainPill && rainBadge) {
          if (rainCount > 0) {
            const rainingNames = activeList.filter(d => districtRainData[d]?.isRaining).join(', ');
            rainPill.textContent = `${prov.shortName}: ${rainCount} khu vực mưa`;
            rainBadge.className = 'flex items-center gap-1.5 text-cyan-300 hover:text-cyan-200 cursor-pointer transition select-none bg-cyan-950/70 px-2.5 py-1 rounded-lg border border-cyan-500/40 shadow-sm shadow-cyan-500/20';
            rainBadge.title = `Các khu vực đang có mưa: ${rainingNames}`;
            if (optionRaining) optionRaining.textContent = `🌧️ Khu Vực Đang Mưa (${rainCount})`;
          } else {
            const sampleTemp = Object.values(districtRainData)[0]?.temp || 28;
            rainPill.textContent = `${prov.shortName}: Trời ráo (${sampleTemp}°C)`;
            rainBadge.className = 'flex items-center gap-1.5 text-slate-300 hover:text-white cursor-pointer transition select-none';
            rainBadge.title = 'Hiện không phát hiện mưa tại các trạm đo';
            if (optionRaining) optionRaining.textContent = '🌧️ Khu Vực Đang Mưa (0)';
          }
        }

        // Re-render markers & sidebar with updated rain badges if currently on map
        if (currentTab === 'map') {
          renderMapMarkers();
          renderDistrictQuickViews();
        }
      } catch (err) {
        console.warn('Weather rain fetch error:', err);
      }
    }"""

assert old_fetch_rain in code, "old_fetch_rain not found"
code = code.replace(old_fetch_rain, new_fetch_rain)

# 3. Update renderDistrictQuickViews
old_render_quick = """      DISTRICT_REPRESENTATIVES.forEach(d => {"""
new_render_quick = """      const activeReps = (currentProvince === 'HCM') ? DISTRICT_REPRESENTATIVES : (PROVINCES_HOTSPOTS[currentProvince] || []).slice(0, 6);
      activeReps.forEach(d => {"""

assert old_render_quick in code, "old_render_quick not found"
code = code.replace(old_render_quick, new_render_quick)

# 4. Update flyToDistrict
old_fly_dist = """function flyToDistrict(distName) {
      const match = Object.keys(DISTRICT_CENTERS).find(k => matchesDistrict(distName, k));
      if (match && DISTRICT_CENTERS[match] && map) {
        map.setView(DISTRICT_CENTERS[match], 14, { animate: true });
        showToast(`Đã di chuyển bản đồ đến: ${distName}`);
      }
    }"""

new_fly_dist = """function flyToDistrict(distName) {
      const activeCenters = getActiveDistrictCenters();
      const match = Object.keys(activeCenters).find(k => matchesDistrict(distName, k));
      if (match && activeCenters[match] && map) {
        map.setView(activeCenters[match], 14, { animate: true });
        showToast(`Đã di chuyển bản đồ đến: ${distName}`);
      }
    }"""

assert old_fly_dist in code, "old_fly_dist not found"
code = code.replace(old_fly_dist, new_fly_dist)

# 5. Update renderMapMarkers grouping
old_render_group = """      // Group cameras by district for sidebar
      const groups = {};
      filtered.forEach(cam => {
        let matchedDist = DISTRICT_LIST.find(d => matchesDistrict(cam.district, d));
        if (!matchedDist) matchedDist = 'Khu Vực Khác';
        if (!groups[matchedDist]) groups[matchedDist] = [];
        groups[matchedDist].push(cam);
      });

      const orderedDistricts = [...DISTRICT_LIST, 'Khu Vực Khác'].filter(d => groups[d] && groups[d].length > 0);"""

new_render_group = """      // Group cameras by district for sidebar
      const activeList = getActiveDistrictList();
      const groups = {};
      filtered.forEach(cam => {
        let matchedDist = activeList.find(d => matchesDistrict(cam.district, d));
        if (!matchedDist) matchedDist = 'Khu Vực Khác';
        if (!groups[matchedDist]) groups[matchedDist] = [];
        groups[matchedDist].push(cam);
      });

      const orderedDistricts = [...activeList, 'Khu Vực Khác'].filter(d => groups[d] && groups[d].length > 0);"""

assert old_render_group in code, "old_render_group not found"
code = code.replace(old_render_group, new_render_group)

# 6. Add province switcher logic
old_init_listeners = """    // Search input
    searchInput.addEventListener('input', (e) => {"""

new_province_code = """    // --- PROVINCE SWITCHER LOGIC ---
    function populateDistrictDropdown(provKey) {
      const prov = PROVINCES[provKey];
      if (!prov) return;
      const select = document.getElementById('districtSelect');
      if (!select) return;
      
      select.innerHTML = '';
      
      const allOpt = document.createElement('option');
      allOpt.value = 'ALL';
      allOpt.textContent = `Toàn ${prov.shortName} (Tất cả)`;
      select.appendChild(allOpt);

      const rainOpt = document.createElement('option');
      rainOpt.value = 'RAINING';
      rainOpt.id = 'optionRainingDistricts';
      rainOpt.className = 'text-cyan-400 font-bold bg-slate-900';
      rainOpt.textContent = '🌧️ Khu Vực Đang Mưa';
      select.appendChild(rainOpt);

      prov.districts.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d;
        opt.textContent = d;
        select.appendChild(opt);
      });
      
      selectedDistrict = 'ALL';
    }

    function switchProvince(provKey) {
      const prov = PROVINCES[provKey];
      if (!prov) return;
      currentProvince = provKey;

      // Update Header Brand
      const titleMobile = document.getElementById('brandTitleMobile');
      const titleDesktop = document.getElementById('brandTitleDesktop');
      const brandSub = document.getElementById('brandSubtitle');
      if (titleMobile) titleMobile.textContent = `${prov.shortName.toUpperCase()} CAMS`;
      if (titleDesktop) titleDesktop.textContent = `${prov.shortName.toUpperCase()} TRAFFIC CAMS`;
      if (brandSub) brandSub.textContent = `Giám sát Giao thông & Điểm nóng Trực tuyến — ${prov.name}`;

      // Update Active Stats Pill
      const statsEl = document.getElementById('activeStats');
      if (statsEl) statsEl.textContent = prov.statsLabel;

      // Update cameras array
      if (provKey === 'HCM') {
        cameras = window.HCM_CAMERAS || [];
      } else {
        cameras = PROVINCES_HOTSPOTS[provKey] || [];
      }

      // Reset search & district
      searchQuery = '';
      if (searchInput) searchInput.value = '';
      if (btnClearSearch) btnClearSearch.classList.add('hidden');
      populateDistrictDropdown(provKey);

      // Update Hotspot Badge count
      const hotspotCount = cameras.filter(c => c.isHotspot).length;
      if (hotspotBadgeCount) hotspotBadgeCount.textContent = hotspotCount;

      // Fly Map to province
      if (map) {
        map.flyTo(prov.center, prov.zoom, { duration: 1.2 });
      }

      // Re-render markers & quick views
      districtRainData = {};
      renderMapMarkers();
      renderDistrictQuickViews();
      fetchLiveRainData();

      // Re-render current tab if wall or hotspots
      if (currentTab === 'wall') renderWallView(true);
      if (currentTab === 'hotspots') renderHotspotsView();
      if (currentTab === 'favorites') renderFavoritesView();

      showToast(`Đã chuyển sang ${prov.icon} ${prov.name}`, 'info');
    }

    const provinceSelect = document.getElementById('provinceSelect');
    if (provinceSelect) {
      provinceSelect.addEventListener('change', (e) => {
        switchProvince(e.target.value);
      });
    }

    // Search input
    searchInput.addEventListener('input', (e) => {"""

assert old_init_listeners in code, "old_init_listeners not found"
code = code.replace(old_init_listeners, new_province_code)

# 7. Update openModal
old_open_modal = """      document.getElementById('modalCamName').textContent = cam.name;
      document.getElementById('modalCamDistrict').textContent = cam.district;
      document.getElementById('modalCamId').textContent = `ID: ${cam.id}`;
      document.getElementById('modalCamCoords').textContent = `GPS: ${cam.lat}, ${cam.lon}`;
      document.getElementById('modalImageTimestamp').textContent = `Cập nhật: ${getTimeString()}`;
      document.getElementById('btnModalGoogleMaps').href = `https://www.google.com/maps?q=${cam.lat},${cam.lon}`;"""

new_open_modal = """      const provName = PROVINCES[currentProvince]?.name || 'Việt Nam';
      document.getElementById('modalCamName').textContent = cam.name;
      document.getElementById('modalCamDistrict').textContent = `${cam.district} • ${provName}`;
      document.getElementById('modalCamId').textContent = `ID: ${cam.id}`;
      document.getElementById('modalCamCoords').textContent = `GPS: ${cam.lat}, ${cam.lon}`;
      document.getElementById('modalImageTimestamp').textContent = cam.isSynthetic ? 'Giám sát trực tiếp qua Google Traffic & Radar Thời Tiết' : `Cập nhật: ${getTimeString()}`;
      document.getElementById('btnModalGoogleMaps').href = `https://www.google.com/maps/search/?api=1&query=${cam.lat},${cam.lon}`;"""

assert old_open_modal in code, "old_open_modal not found"
code = code.replace(old_open_modal, new_open_modal)

with open('projects/hcm-traffic-cams/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("All JavaScript logic successfully applied!")
