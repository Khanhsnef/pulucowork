with open('projects/hcm-traffic-cams/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update PROVINCES with appName, appShortName, appUrl, appDesc
old_prov_hcm = """      HCM: {
        name: 'TP. Hồ Chí Minh',
        shortName: 'TP.HCM',
        icon: '🌟',
        center: [10.7769, 106.7009],
        zoom: 13,
        statsLabel: '835 Camera khả dụng',
        isLiveCctv: true,"""

new_prov_hcm = """      HCM: {
        name: 'TP. Hồ Chí Minh',
        shortName: 'TP.HCM',
        icon: '🌟',
        center: [10.7769, 106.7009],
        zoom: 13,
        statsLabel: '835 Camera khả dụng',
        isLiveCctv: true,
        appName: 'Cổng TT Giao Thông TP.HCM',
        appShortName: 'Sở GTVT',
        appUrl: 'https://giaothong.hochiminhcity.gov.vn/',
        appDesc: 'Hệ thống 835 mắt camera snapshot trực tiếp từ Sở Giao thông Vận tải TP.HCM.',"""

assert old_prov_hcm in code, "old_prov_hcm not found"
code = code.replace(old_prov_hcm, new_prov_hcm)

# Update other provinces in PROVINCES
prov_replacements = [
    (
        """      HN: {
        name: 'Thủ Đô Hà Nội',
        shortName: 'Hà Nội',
        icon: '🏛️',
        center: [21.0285, 105.8542],
        zoom: 12,
        statsLabel: '15 Nút Giao Trọng Điểm',
        isLiveCctv: false,""",
        """      HN: {
        name: 'Thủ Đô Hà Nội',
        shortName: 'Hà Nội',
        icon: '🏛️',
        center: [21.0285, 105.8542],
        zoom: 12,
        statsLabel: '15 Nút Giao Trọng Điểm',
        isLiveCctv: false,
        appName: 'iHanoi (Công Dân Thủ Đô)',
        appShortName: 'iHanoi',
        appUrl: 'https://ihanoi.vn/',
        appDesc: 'Ứng dụng chính thống của UBND & Công an TP Hà Nội với luồng camera giám sát trực tiếp.',"""
    ),
    (
        """      DN: {
        name: 'TP. Đà Nẵng',
        shortName: 'Đà Nẵng',
        icon: '🌊',
        center: [16.0544, 108.2022],
        zoom: 13,
        statsLabel: '8 Cầu & Nút Giao Huyết Mạch',
        isLiveCctv: false,""",
        """      DN: {
        name: 'TP. Đà Nẵng',
        shortName: 'Đà Nẵng',
        icon: '🌊',
        center: [16.0544, 108.2022],
        zoom: 13,
        statsLabel: '8 Cầu & Nút Giao Huyết Mạch',
        isLiveCctv: false,
        appName: 'Danang Smart City',
        appShortName: 'Danang Smart',
        appUrl: 'https://giaothong.danang.gov.vn/',
        appDesc: 'Cổng Giám sát Giao thông TP Đà Nẵng & ứng dụng Danang Smart City.',"""
    ),
    (
        """      BD: {
        name: 'Bình Dương',
        shortName: 'Bình Dương',
        icon: '🏭',
        center: [10.9805, 106.6744],
        zoom: 12,
        statsLabel: '8 Nút Giao Công Nghiệp',
        isLiveCctv: false,""",
        """      BD: {
        name: 'Bình Dương',
        shortName: 'Bình Dương',
        icon: '🏭',
        center: [10.9805, 106.6744],
        zoom: 12,
        statsLabel: '8 Nút Giao Công Nghiệp',
        isLiveCctv: false,
        appName: 'Bình Dương Số (IOC)',
        appShortName: 'Bình Dương Số',
        appUrl: 'https://ioc.binhduong.gov.vn/',
        appDesc: 'Trung tâm Giám sát Điều hành Đô thị Thông minh IOC Bình Dương.',"""
    ),
    (
        """      DNA: {
        name: 'Đồng Nai',
        shortName: 'Đồng Nai',
        icon: '🚛',
        center: [10.9574, 106.8427],
        zoom: 12,
        statsLabel: '8 Cửa Ngõ & Cao Tốc',
        isLiveCctv: false,""",
        """      DNA: {
        name: 'Đồng Nai',
        shortName: 'Đồng Nai',
        icon: '🚛',
        center: [10.9574, 106.8427],
        zoom: 12,
        statsLabel: '8 Cửa Ngõ & Cao Tốc',
        isLiveCctv: false,
        appName: 'Biên Hòa SmartCity',
        appShortName: 'Biên Hòa Smart',
        appUrl: 'https://dongnai.gov.vn/',
        appDesc: 'Trung tâm Điều hành Đô thị Thông minh Đồng Nai & TP. Biên Hòa.',"""
    ),
    (
        """      HP: {
        name: 'Hải Phòng',
        shortName: 'Hải Phòng',
        icon: '⚓',
        center: [20.8449, 106.6881],
        zoom: 12,
        statsLabel: '6 Cầu Cảng & Huyết Mạch',
        isLiveCctv: false,""",
        """      HP: {
        name: 'Hải Phòng',
        shortName: 'Hải Phòng',
        icon: '⚓',
        center: [20.8449, 106.6881],
        zoom: 12,
        statsLabel: '6 Cầu Cảng & Huyết Mạch',
        isLiveCctv: false,
        appName: 'Hải Phòng Smart',
        appShortName: 'HP Smart',
        appUrl: 'https://haiphong.gov.vn/',
        appDesc: 'Cổng điều hành giao thông thông minh TP Hải Phòng.',"""
    ),
    (
        """      CT: {
        name: 'Cần Thơ',
        shortName: 'Cần Thơ',
        icon: '🌾',
        center: [10.0452, 105.7469],
        zoom: 13,
        statsLabel: '6 Nút Giao Tây Nam Bộ',
        isLiveCctv: false,""",
        """      CT: {
        name: 'Cần Thơ',
        shortName: 'Cần Thơ',
        icon: '🌾',
        center: [10.0452, 105.7469],
        zoom: 13,
        statsLabel: '6 Nút Giao Tây Nam Bộ',
        isLiveCctv: false,
        appName: 'Cần Thơ Smart',
        appShortName: 'Cần Thơ Smart',
        appUrl: 'https://cantho.gov.vn/',
        appDesc: 'Cổng giám sát đô thị thông minh TP Cần Thơ.',"""
    ),
    (
        """      DL: {
        name: 'Lâm Đồng (Đà Lạt)',
        shortName: 'Đà Lạt',
        icon: '🌲',
        center: [11.9404, 108.4583],
        zoom: 13,
        statsLabel: '6 Đèo & Cửa Ngõ Du Lịch',
        isLiveCctv: false,""",
        """      DL: {
        name: 'Lâm Đồng (Đà Lạt)',
        shortName: 'Đà Lạt',
        icon: '🌲',
        center: [11.9404, 108.4583],
        zoom: 13,
        statsLabel: '6 Đèo & Cửa Ngõ Du Lịch',
        isLiveCctv: false,
        appName: 'Đà Lạt Trực Tuyến (IOC)',
        appShortName: 'Đà Lạt Online',
        appUrl: 'https://dalat.vn/',
        appDesc: 'Hệ thống Camera Giám sát Đô thị TP. Đà Lạt & IOC Lâm Đồng.',"""
    ),
    (
        """      VT: {
        name: 'Bà Rịa - Vũng Tàu',
        shortName: 'Vũng Tàu',
        icon: '🏖️',
        center: [10.3460, 107.0843],
        zoom: 13,
        statsLabel: '5 Trục Ven Biển & Cảng',
        isLiveCctv: false,""",
        """      VT: {
        name: 'Bà Rịa - Vũng Tàu',
        shortName: 'Vũng Tàu',
        icon: '🏖️',
        center: [10.3460, 107.0843],
        zoom: 13,
        statsLabel: '5 Trục Ven Biển & Cảng',
        isLiveCctv: false,
        appName: 'BR-VT Smart',
        appShortName: 'BR-VT Smart',
        appUrl: 'https://baria-vungtau.gov.vn/',
        appDesc: 'Cổng IOC Giám sát Đô thị Thông minh tỉnh Bà Rịa - Vũng Tàu.',"""
    ),
    (
        """      HUE: {
        name: 'Thừa Thiên Huế',
        shortName: 'Huế',
        icon: '🏯',
        center: [16.4637, 107.5909],
        zoom: 13,
        statsLabel: '6 Cầu Sông Hương & Cửa Ngõ',
        isLiveCctv: false,""",
        """      HUE: {
        name: 'Thừa Thiên Huế',
        shortName: 'Huế',
        icon: '🏯',
        center: [16.4637, 107.5909],
        zoom: 13,
        statsLabel: '6 Cầu Sông Hương & Cửa Ngõ',
        isLiveCctv: false,
        appName: 'Huế-S (IOC Huế)',
        appShortName: 'Huế-S',
        appUrl: 'https://hue-s.vn/',
        appDesc: 'Nền tảng Đô thị Thông minh Huế-S tích hợp camera công cộng Thừa Thiên Huế.',"""
    )
]

for old, new in prov_replacements:
    assert old in code, f"Old prov not found: {old[:30]}"
    code = code.replace(old, new)

# 2. Add Layer 3 banner inside inspectModal
old_modal_footer_anchor = """      <!-- Modal Footer -->
      <div class="px-5 py-3 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">"""

new_modal_app_banner = """      <!-- Layer 3: Official App Verification Bar -->
      <div id="modalAppBanner" class="px-4 sm:px-5 py-3 bg-gradient-to-r from-slate-900 via-slate-850 to-slate-900 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-7 h-7 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0 border border-blue-500/30">
            <i data-lucide="shield-check" class="w-4 h-4"></i>
          </div>
          <div class="min-w-0">
            <span class="text-[10px] uppercase tracking-wider font-bold text-blue-400 block">Lớp 3 • Xác Minh Trực Tiếp</span>
            <p id="modalAppDesc" class="text-xs text-slate-300 truncate">Ứng dụng chính thống của tỉnh/thành với luồng video camera trực tiếp.</p>
          </div>
        </div>
        <div class="flex items-center gap-2 shrink-0 w-full sm:w-auto">
          <a id="btnModalAppDeepLink" href="#" target="_blank" class="flex-1 sm:flex-none px-3.5 py-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-lg shadow-blue-600/30 transition">
            <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
            <span id="btnModalAppText">Mở Camera App</span>
          </a>
          <a id="btnModalGoogleTraffic" href="#" target="_blank" class="flex-1 sm:flex-none px-3 py-1.5 rounded-xl bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 font-semibold text-xs flex items-center justify-center gap-1.5 transition">
            <i data-lucide="navigation" class="w-3.5 h-3.5 text-emerald-400"></i>
            <span>Google Live</span>
          </a>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="px-5 py-3 bg-slate-900 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">"""

assert old_modal_footer_anchor in code, "old_modal_footer_anchor not found"
code = code.replace(old_modal_footer_anchor, new_modal_app_banner)

# 3. Update openModal to populate Layer 3 banner
old_open_modal = """      const provName = PROVINCES[currentProvince]?.name || 'Việt Nam';
      document.getElementById('modalCamName').textContent = cam.name;
      document.getElementById('modalCamDistrict').textContent = `${cam.district} • ${provName}`;
      document.getElementById('modalCamId').textContent = `ID: ${cam.id}`;
      document.getElementById('modalCamCoords').textContent = `GPS: ${cam.lat}, ${cam.lon}`;
      document.getElementById('modalImageTimestamp').textContent = cam.isSynthetic ? 'Giám sát trực tiếp qua Google Traffic & Radar Thời Tiết' : `Cập nhật: ${getTimeString()}`;
      document.getElementById('btnModalGoogleMaps').href = `https://www.google.com/maps/search/?api=1&query=${cam.lat},${cam.lon}`;"""

new_open_modal = """      const prov = PROVINCES[currentProvince] || PROVINCES.HCM;
      const provName = prov.name || 'Việt Nam';
      document.getElementById('modalCamName').textContent = cam.name;
      document.getElementById('modalCamDistrict').textContent = `${cam.district} • ${provName}`;
      document.getElementById('modalCamId').textContent = `ID: ${cam.id}`;
      document.getElementById('modalCamCoords').textContent = `GPS: ${cam.lat}, ${cam.lon}`;
      document.getElementById('modalImageTimestamp').textContent = cam.isSynthetic ? 'Live Traffic & Radar Thời Tiết' : `Cập nhật: ${getTimeString()}`;
      document.getElementById('btnModalGoogleMaps').href = `https://www.google.com/maps/search/?api=1&query=${cam.lat},${cam.lon}`;

      // Layer 3: Wire App Deep-link
      const btnApp = document.getElementById('btnModalAppDeepLink');
      const btnAppText = document.getElementById('btnModalAppText');
      const appDesc = document.getElementById('modalAppDesc');
      const btnGTraffic = document.getElementById('btnModalGoogleTraffic');

      if (btnGTraffic) {
        btnGTraffic.href = `https://www.google.com/maps/search/?api=1&query=${cam.lat},${cam.lon}`;
      }
      if (btnApp && prov.appUrl) {
        btnApp.href = prov.appUrl;
        btnApp.title = `Mở ${prov.appName} để kiểm tra luồng video trực tiếp`;
      }
      if (btnAppText) {
        btnAppText.textContent = `Mở ${prov.appShortName || 'App'}`;
      }
      if (appDesc) {
        appDesc.textContent = prov.appDesc || 'Ứng dụng chính thống của cơ quan quản lý giao thông địa phương.';
      }"""

assert old_open_modal in code, "old_open_modal not found"
code = code.replace(old_open_modal, new_open_modal)

# 4. Update Map Popup in renderMapMarkers to include Layer 3 button
old_popup_footer = """                <div class="mt-3 flex items-center justify-between gap-1 border-t border-slate-800 pt-2">
                  <button onclick="openModal('${cam.id}')" class="px-2.5 py-1 rounded-lg bg-orange-500 hover:bg-orange-600 text-white text-xs font-semibold flex items-center gap-1 transition">
                    <i data-lucide="zoom-in" class="w-3.5 h-3.5"></i> Phóng to
                  </button>
                  <button onclick="toggleFavorite('${cam.id}')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-400 text-xs font-medium flex items-center gap-1 transition">
                    <i data-lucide="star" class="w-3.5 h-3.5"></i> ${isFav(cam.id) ? 'Bỏ lưu' : 'Ghim'}
                  </button>
                  <a href="https://www.google.com/maps?q=${cam.lat},${cam.lon}" target="_blank" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center gap-1 transition">
                    <i data-lucide="navigation" class="w-3.5 h-3.5"></i> Chỉ đường
                  </a>
                </div>"""

new_popup_footer = """                <div class="mt-3 flex items-center justify-between gap-1 border-t border-slate-800 pt-2">
                  <button onclick="openModal('${cam.id}')" class="px-2.5 py-1 rounded-lg bg-orange-500 hover:bg-orange-600 text-white text-xs font-semibold flex items-center gap-1 transition">
                    <i data-lucide="zoom-in" class="w-3.5 h-3.5"></i> Phóng to
                  </button>
                  <button onclick="toggleFavorite('${cam.id}')" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-400 text-xs font-medium flex items-center gap-1 transition">
                    <i data-lucide="star" class="w-3.5 h-3.5"></i> ${isFav(cam.id) ? 'Bỏ lưu' : 'Ghim'}
                  </button>
                  <a href="https://www.google.com/maps?q=${cam.lat},${cam.lon}" target="_blank" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center gap-1 transition">
                    <i data-lucide="navigation" class="w-3.5 h-3.5"></i> Chỉ đường
                  </a>
                </div>
                ${(PROVINCES[currentProvince] && PROVINCES[currentProvince].appUrl) ? `
                  <div class="mt-2 pt-2 border-t border-slate-800/80">
                    <a href="${PROVINCES[currentProvince].appUrl}" target="_blank" class="w-full py-1 px-2 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/40 text-[11px] font-semibold flex items-center justify-center gap-1.5 transition">
                      <i data-lucide="external-link" class="w-3 h-3 text-blue-400"></i>
                      <span>📱 Mở ${PROVINCES[currentProvince].appShortName} (Xem Video Trực Tiếp)</span>
                    </a>
                  </div>
                ` : ''}"""

assert old_popup_footer in code, "old_popup_footer not found"
code = code.replace(old_popup_footer, new_popup_footer)

with open('projects/hcm-traffic-cams/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Layer 3 Deep-link integration applied successfully!")
