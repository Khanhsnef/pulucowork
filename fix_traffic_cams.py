with open('projects/hcm-traffic-cams/index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add getTrafficTileUrl and update getSnapshotUrl
old_snapshot_fn = """function getSnapshotUrl(camId) {
      const cam = cameras.find(c => c.id === camId) || (window.HCM_CAMERAS && window.HCM_CAMERAS.find(c => c.id === camId));
      if (cam && cam.isSynthetic) {
        return getNodeSvgBanner(cam.name, cam.district, cam.isHotspot);
      }
      return `https://camera.thongtingiaothong.vn/api/snapshot/${camId}?t=${Date.now()}`;
    }"""

new_snapshot_fn = """function getTrafficTileUrl(lat, lon, zoom = 16) {
      const x = Math.floor((lon + 180) / 360 * Math.pow(2, zoom));
      const latRad = lat * Math.PI / 180;
      const y = Math.floor((1 - Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI) / 2 * Math.pow(2, zoom));
      // Google Road Map with Live Traffic overlay tile
      return `https://mt1.google.com/vt/lyrs=m,traffic&x=${x}&y=${y}&z=${zoom}`;
    }

    function getSnapshotUrl(camId) {
      const cam = cameras.find(c => c.id === camId) || (window.HCM_CAMERAS && window.HCM_CAMERAS.find(c => c.id === camId));
      if (cam && (cam.isSynthetic || currentProvince !== 'HCM')) {
        if (cam.lat && cam.lon) {
          return getTrafficTileUrl(cam.lat, cam.lon, 16);
        }
      }
      return `https://camera.thongtingiaothong.vn/api/snapshot/${camId}?t=${Date.now()}`;
    }"""

assert old_snapshot_fn in code, "old_snapshot_fn not found"
code = code.replace(old_snapshot_fn, new_snapshot_fn)

# 2. Update refreshAllImages to not break synthetic/non-HCM nodes
old_refresh = """    function refreshAllImages() {
      const now = Date.now();
      
      // Refresh visible camera cards on wall
      document.querySelectorAll('img[id^="wall_img_"]').forEach(img => {
        const id = img.id.replace('wall_img_', '');
        img.src = `https://camera.thongtingiaothong.vn/api/snapshot/${id}?t=${now}`;
      });

      // Refresh open modal if active
      if (currentModalCam) {
        document.getElementById('modalCamImage').src = `https://camera.thongtingiaothong.vn/api/snapshot/${currentModalCam.id}?t=${now}`;
        document.getElementById('modalImageTimestamp').textContent = `Cập nhật: ${getTimeString()}`;
      }

      // Refresh open popups
      document.querySelectorAll('img[id^="popup_img_"]').forEach(img => {
        const id = img.id.replace('popup_img_', '');
        img.src = `https://camera.thongtingiaothong.vn/api/snapshot/${id}?t=${now}`;
      });

      // Refresh district quick cards on map
      document.querySelectorAll('img[id^="quick_card_"]').forEach(img => {
        const id = img.id.replace('quick_card_', '');
        img.src = `https://camera.thongtingiaothong.vn/api/snapshot/${id}?t=${now}`;
      });
    }"""

new_refresh = """    function refreshAllImages() {
      const now = Date.now();
      
      // Refresh visible camera cards on wall
      document.querySelectorAll('img[id^="wall_img_"]').forEach(img => {
        const id = img.id.replace('wall_img_', '');
        const cam = cameras.find(c => c.id === id);
        if (cam && (cam.isSynthetic || currentProvince !== 'HCM')) {
          // Keep live tile or refresh tile
          img.src = getSnapshotUrl(id);
        } else {
          img.src = `https://camera.thongtingiaothong.vn/api/snapshot/${id}?t=${now}`;
        }
      });

      // Refresh open modal if active
      if (currentModalCam) {
        if (currentModalCam.isSynthetic || currentProvince !== 'HCM') {
          document.getElementById('modalCamImage').src = getSnapshotUrl(currentModalCam.id);
          document.getElementById('modalImageTimestamp').textContent = `Cập nhật Live Traffic: ${getTimeString()}`;
        } else {
          document.getElementById('modalCamImage').src = `https://camera.thongtingiaothong.vn/api/snapshot/${currentModalCam.id}?t=${now}`;
          document.getElementById('modalImageTimestamp').textContent = `Cập nhật: ${getTimeString()}`;
        }
      }

      // Refresh open popups
      document.querySelectorAll('img[id^="popup_img_"]').forEach(img => {
        const id = img.id.replace('popup_img_', '');
        const cam = cameras.find(c => c.id === id);
        if (cam && (cam.isSynthetic || currentProvince !== 'HCM')) {
          img.src = getSnapshotUrl(id);
        } else {
          img.src = `https://camera.thongtingiaothong.vn/api/snapshot/${id}?t=${now}`;
        }
      });

      // Refresh district quick cards on map
      document.querySelectorAll('img[id^="quick_card_"]').forEach(img => {
        const id = img.id.replace('quick_card_', '');
        const cam = cameras.find(c => c.id === id);
        if (cam && (cam.isSynthetic || currentProvince !== 'HCM')) {
          img.src = getSnapshotUrl(id);
        } else {
          img.src = `https://camera.thongtingiaothong.vn/api/snapshot/${id}?t=${now}`;
        }
      });
    }"""

assert old_refresh in code, "old_refresh not found"
code = code.replace(old_refresh, new_refresh)

# 3. Update quick card badge label to reflect CCTV vs Live Traffic
old_quick_badge = """              <img id="quick_card_${d.id}" src="${getSnapshotUrl(d.id)}" alt="${d.name}" class="w-full h-full object-cover">
              <span class="absolute bottom-1 right-1 px-1 py-0.2 rounded text-[7px] sm:text-[8px] font-mono bg-slate-900/90 text-emerald-400 font-bold border border-emerald-500/30">LIVE</span>"""

new_quick_badge = """              <img id="quick_card_${d.id}" src="${getSnapshotUrl(d.id)}" alt="${d.name}" class="w-full h-full object-cover" onerror="this.onerror=null; this.src='https://cartodb-basemaps-a.global.ssl.fastly.net/rastertiles/voyager/15/26015/14428.png'">
              <span class="absolute bottom-1 right-1 px-1 py-0.2 rounded text-[7px] sm:text-[8px] font-mono bg-slate-900/90 text-emerald-400 font-bold border border-emerald-500/30">
                ${(currentProvince === 'HCM') ? 'LIVE CCTV' : 'TRAFFIC'}
              </span>"""

assert old_quick_badge in code, "old_quick_badge not found"
code = code.replace(old_quick_badge, new_quick_badge)

with open('projects/hcm-traffic-cams/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Traffic cams fix applied successfully!")
