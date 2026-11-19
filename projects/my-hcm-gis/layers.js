// Official Live GIS Layers Catalog & Reference Dictionaries
// Source: Sở Tài nguyên & Môi trường TP.HCM GeoServer (OGC WMS 1.1.1 / CORS Enabled)

window.GIS_CONFIG = {
  STNMT_WMS_URL: 'https://geodata-stnmt.tphcm.gov.vn/geoserver/wms',
  DEFAULT_CENTER: [10.7405, 106.6620], // Quận 8 / Trung tâm TP.HCM
  DEFAULT_ZOOM: 16
};

// All live verified WMS layers from geodata-stnmt.tphcm.gov.vn
window.WMS_LAYERS = {
  // 1. Cadastral parcel boundaries (Ranh thửa địa chính toàn TP.HCM)
  CADASTRAL_ALL: {
    id: 'cadastral_all',
    layerName: 'tnmt:v_ranhthua_TPHCM',
    title: 'Ranh thửa địa chính toàn TP.HCM',
    subtitle: 'Hiển thị ranh từng căn nhà, từng thửa đất (rõ nhất ở Zoom ≥ 16)',
    group: 'cadastral',
    defaultOn: true,
    defaultOpacity: 0.9,
    minZoom: 14,
    queryable: true
  },

  // 2. Latest Planning Adjustments + Parcel Overlay (Điều chỉnh QH mới nhất)
  QH_LATEST_ADJ: {
    id: 'qh_latest_adj',
    layerName: 'tnmt:Ranhthua_Quyhoach',
    title: 'Điều chỉnh Quy hoạch Mới Nhất (TP.HCM)',
    subtitle: 'Lớp m_dieuchinh_qh & ranh thửa cập nhật theo quyết định mới nhất',
    group: 'planning',
    defaultOn: true,
    defaultOpacity: 0.55,
    minZoom: 12,
    queryable: true
  },

  // 3. Citywide Land Use Planning (QHSDĐ toàn TP.HCM)
  QHSDD_CITY: {
    id: 'qhsdd_city',
    layerName: 'tnmt:qhsdd2020',
    title: 'Bản đồ Quy hoạch SDĐ toàn TP.HCM',
    subtitle: 'Phủ 100% 22 Quận/Huyện & TP. Thủ Đức (mã màu đất ODT, DGT, CX, TMD...)',
    group: 'planning',
    defaultOn: false,
    defaultOpacity: 0.5,
    minZoom: 10,
    queryable: true
  },

  // 3. 2030 Suburban Planning (Quy hoạch SDĐ đến năm 2030 - 5 Huyện ngoại thành)
  QH_2030_SUBURBS: {
    id: 'qh_2030_suburbs',
    layerName: [
      'thuthap20242025:quyhoachsddhuyen_binhchanh_polygon',
      'thuthap20242025:quyhoachsddhuyen_nhabe_poly',
      'thuthap20242025:quyhoachsddhuyen_hocmon_poly',
      'thuthap20242025:quyhoachsddhuyen_cuchi_poly',
      'thuthap20242025:quyhoachsddhuyen_cangio_poly'
    ].join(','),
    title: 'Quy hoạch SDĐ đến 2030 (5 Huyện)',
    subtitle: 'Bình Chánh, Nhà Bè, Hóc Môn, Củ Chi, Cần Giờ (Cập nhật 2024–2025)',
    group: 'planning',
    defaultOn: true,
    defaultOpacity: 0.65,
    minZoom: 10,
    queryable: true
  },

  // 4. 2030 Road / Infrastructure Line Network (Tuyến đường dự phóng 2030 - 5 Huyện)
  QH_2030_ROADS: {
    id: 'qh_2030_roads',
    layerName: [
      'thuthap20242025:quyhoachsddhuyen_nhabe_line',
      'thuthap20242025:quyhoachsddhuyen_hocmon_line',
      'thuthap20242025:quyhoachsddhuyen_cuchi_line',
      'thuthap20242025:quyhoachsddhuyen_cangio_line',
      'thuthap20242025:huyenbinhchanh_kehoachsddhuyen2024_line',
      'thuthap20242025:thanhphothuduc_kehoachsddhuyen2024_line'
    ].join(','),
    title: 'Mạng lưới đường dự phóng (Dạng tuyến 2024–2030)',
    subtitle: 'Tuyến mở đường mới tại Thủ Đức, Bình Chánh, Nhà Bè, Hóc Môn, Củ Chi, Cần Giờ',
    group: 'planning',
    defaultOn: true,
    defaultOpacity: 0.9,
    minZoom: 11,
    queryable: true
  },

  // 5. 2024-2025 Annual Land Use Plan (Kế hoạch SDĐ 2024-2025 - Các khu dự án & thu hồi mới!)
  KHSDD_2025_ALL: {
    id: 'khsdd_2025',
    layerName: [
      'thuthap20242025:quan1_kehoachsddhuyen2025_polygon',
      'thuthap20242025:quan3_kehoachsddhuyen2025_polygon',
      'thuthap20242025:quan8_kehoachsddhuyen2025_polygon',
      'thuthap20242025:quan12_kehoachsddhuyen2025_polygon',
      'thuthap20242025:quanbinhtan_kehoachsddhuyen2025_polygon',
      'thuthap20242025:quanphunhuan_kehoachsddhuyen2025_polygon',
      'thuthap20242025:huyennhabe_kehoachsddhuyen2025_polygon',
      'thuthap20242025:huyencangio_kehoachsddhuyen2025_polygon',
      'thuthap20242025:thanhphothuduc_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quan4_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quan5_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quan6_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quan7_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quan10_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quan11_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quanbinhthanh_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quangovap_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quantanbinh_kehoachsddhuyen2024_polygon',
      'thuthap20242025:quantanphu_kehoachsddhuyen2024_polygon',
      'thuthap20242025:huyenbinhchanh_kehoachsddhuyen2024_polygon',
      'thuthap20242025:huyenhocmon_kehoachsddhuyen2024_polygon',
      'thuthap20242025:huyencuchi_kehoachsddhuyen2024_polygon'
    ].join(','),
    title: 'Kế hoạch SDĐ 2024–2025 (Dự án & Thu hồi mới)',
    subtitle: 'Toàn bộ 22 Quận/Huyện & TP. Thủ Đức — Vùng có kế hoạch thu hồi / chuyển mục đích',
    group: 'planning',
    defaultOn: false,
    defaultOpacity: 0.75,
    minZoom: 11,
    queryable: true
  },

  // 6. Topographic & Admin Boundaries
  TOPO_2021: {
    id: 'topo_2021',
    layerName: 'tnmt:BDDH_2021',
    title: 'Bản đồ Địa hình & Hẻm TP.HCM',
    subtitle: 'Bản đồ nền địa hình chi tiết, ranh sông rạch, tim đường, địa giới',
    group: 'reference',
    defaultOn: false,
    defaultOpacity: 0.7,
    minZoom: 11,
    queryable: false
  },
  ADMIN_BOUNDARIES: {
    id: 'admin_boundaries',
    layerName: 'tnmt:ranhphuong_pg,tnmt:ranhgioi_quan',
    title: 'Ranh giới Phường / Xã / Quận',
    subtitle: 'Đường phân ranh địa giới hành chính chính thức',
    group: 'reference',
    defaultOn: false,
    defaultOpacity: 0.85,
    minZoom: 10,
    queryable: true
  }
};

// Complete Vietnam Land Use Code Dictionary (Thông tư 08/2024/TT-BTNMT & Luật Đất đai 2024)
window.LAND_CODES = {
  ODT: { name: 'Đất ở tại đô thị', risk: 'safe', riskLabel: 'AN TOÀN — ĐƯỢC XÂY DỰNG', color: '#f472b6', desc: 'Đất ở đô thị hợp pháp, được cấp phép xây dựng nhà ở, chuyển nhượng và thế chấp ngân hàng.' },
  ONT: { name: 'Đất ở tại nông thôn', risk: 'safe', riskLabel: 'AN TOÀN — ĐƯỢC XÂY DỰNG', color: '#fb7185', desc: 'Đất thổ cư khu vực nông thôn/huyện ngoại thành, được cấp phép xây dựng nhà ở.' },
  T:   { name: 'Đất thổ cư (Mã cũ)', risk: 'safe', riskLabel: 'AN TOÀN — ĐẤT Ở', color: '#f472b6', desc: 'Ký hiệu đất thổ cư theo bản đồ địa chính cũ (tương đương ODT/ONT).' },
  TMD: { name: 'Đất thương mại, dịch vụ', risk: 'caution', riskLabel: 'ĐẤT KINH DOANH / CÓ THỜI HẠN', color: '#fb923c', desc: 'Dành cho công trình thương mại, văn phòng, dịch vụ. Kiểm tra thời hạn sử dụng đất (50 năm hay lâu dài).' },
  SKC: { name: 'Đất cơ sở sản xuất phi nông nghiệp', risk: 'caution', riskLabel: 'SẢN XUẤT / KHÔNG Ở LÂU DÀI', color: '#f59e0b', desc: 'Đất nhà xưởng, cơ sở sản xuất kinh doanh ngoài khu công nghiệp.' },
  SKK: { name: 'Đất khu công nghiệp', risk: 'caution', riskLabel: 'KHU CÔNG NGHIỆP', color: '#a855f7', desc: 'Đất dành cho phát triển hạ tầng và nhà máy trong Khu công nghiệp.' },
  SKN: { name: 'Đất cụm công nghiệp', risk: 'caution', riskLabel: 'CỤM CÔNG NGHIỆP', color: '#c084fc', desc: 'Đất cụm công nghiệp, tiểu thủ công nghiệp.' },
  CLN: { name: 'Đất trồng cây lâu năm', risk: 'caution', riskLabel: 'NÔNG NGHIỆP — CHƯA LÊN THỔ CƯ', color: '#eab308', desc: 'Không được xây dựng nhà ở khi chưa chuyển mục đích. Kiểm tra quy hoạch lên ODT/ONT và tính tiền sử dụng đất theo QĐ 79/2024.' },
  BHK: { name: 'Đất trồng cây hàng năm khác', risk: 'caution', riskLabel: 'NÔNG NGHIỆP', color: '#facc15', desc: 'Đất nông nghiệp trồng hoa màu, cây hàng năm.' },
  LUC: { name: 'Đất chuyên trồng lúa nước', risk: 'danger', riskLabel: 'ĐẤT LÚA — HẠN CHẾ CHUYỂN ĐỔI', color: '#fef08a', desc: 'Đất trồng lúa nước được bảo vệ nghiêm ngặt, thủ tục chuyển đổi mục đích rất khó.' },
  LUK: { name: 'Đất trồng lúa nước còn lại', risk: 'danger', riskLabel: 'ĐẤT LÚA', color: '#fef08a', desc: 'Đất trồng lúa, không được phép xây dựng.' },
  NTS: { name: 'Đất nuôi trồng thủy sản', risk: 'danger', riskLabel: 'NÔNG NGHIỆP / THỦY SẢN', color: '#38bdf8', desc: 'Ao hồ, đầm nuôi trồng thủy sản, không được xây nhà.' },
  RSX: { name: 'Đất rừng sản xuất', risk: 'danger', riskLabel: 'ĐẤT RỪNG', color: '#4ade80', desc: 'Đất lâm nghiệp sản xuất, không được xây dựng nhà ở.' },
  RPH: { name: 'Đất rừng phòng hộ', risk: 'danger', riskLabel: 'RỪNG PHÒNG HỘ — CẤM XÂY', color: '#22c55e', desc: 'Đất rừng phòng hộ sinh thái (như Cần Giờ), cấm tuyệt đối xây dựng dân dụng.' },
  DGT: { name: 'Đất giao thông (Lộ giới / Mở đường)', risk: 'danger', riskLabel: 'NGUY CƠ GIẢI TỎA LÀM ĐƯỜNG', color: '#ef4444', desc: 'Thuộc hành lang giao thông, chỉ giới đường đỏ hoặc đường dự phóng mở mới. Sẽ bị thu hồi khi mở đường.' },
  DTL: { name: 'Đất thủy lợi / Hành lang kênh rạch', risk: 'danger', riskLabel: 'HÀNH LANG KÊNH RẠCH — CẤM XÂY', color: '#0ea5e9', desc: 'Hành lang bảo vệ sông rạch, bờ kè, công trình thủy lợi.' },
  DKV: { name: 'Đất khu vui chơi, giải trí công cộng / Công viên', risk: 'danger', riskLabel: 'CÔNG VIÊN CÂY XANH — ĐÓNG BĂNG', color: '#10b981', desc: 'Quy hoạch công viên cây xanh công cộng. Cấm xây mới kiên cố, nguy cơ thu hồi.' },
  CX:  { name: 'Đất cây xanh / Công viên', risk: 'danger', riskLabel: 'CÂY XANH — CẤM XÂY DỰNG', color: '#10b981', desc: 'Đất cây xanh cách ly hoặc công viên công cộng. Không được cấp phép xây dựng nhà ở.' },
  DGD: { name: 'Đất xây dựng cơ sở giáo dục & đào tạo', risk: 'danger', riskLabel: 'ĐẤT TRƯỜNG HỌC — NGUY CƠ THU HỒI', color: '#f97316', desc: 'Quy hoạch xây dựng trường học công lập/dân lập. Hạn chế xây dựng nhà ở.' },
  DYT: { name: 'Đất xây dựng cơ sở y tế', risk: 'danger', riskLabel: 'ĐẤT Y TẾ — NGUY CƠ THU HỒI', color: '#f97316', desc: 'Quy hoạch bệnh viện, trạm y tế.' },
  DVH: { name: 'Đất cơ sở văn hóa', risk: 'danger', riskLabel: 'ĐẤT CÔNG CỘNG', color: '#f97316', desc: 'Đất xây dựng công trình văn hóa công cộng.' },
  DTT: { name: 'Đất cơ sở thể dục thể thao', risk: 'danger', riskLabel: 'ĐẤT THỂ THAO — HẠN CHẾ XÂY', color: '#22c55e', desc: 'Quy hoạch sân bãi, trung tâm thể thao.' },
  TSC: { name: 'Đất trụ sở cơ quan', risk: 'danger', riskLabel: 'TRỤ SỞ CƠ QUAN NHÀ NƯỚC', color: '#dc2626', desc: 'Đất công, trụ sở hành chính.' },
  CQP: { name: 'Đất quốc phòng', risk: 'danger', riskLabel: 'ĐẤT QUỐC PHÒNG — CẤM GIAO DỊCH', color: '#b91c1c', desc: 'Đất an ninh quốc phòng, không được phép mua bán dân sự.' },
  CAN: { name: 'Đất an ninh', risk: 'danger', riskLabel: 'ĐẤT AN NINH', color: '#b91c1c', desc: 'Đất thuộc lực lượng công an, an ninh.' },
  NTD: { name: 'Đất nghĩa trang, nghĩa địa', risk: 'danger', riskLabel: 'ĐẤT NGHĨA TRANG', color: '#64748b', desc: 'Đất nghĩa trang hoặc khu vực chờ di dời giải tỏa.' },
  SON: { name: 'Đất sông, ngòi, kênh, rạch, suối', risk: 'danger', riskLabel: 'MẶT NƯỚC SÔNG RẠCH', color: '#0284c7', desc: 'Mặt nước tự nhiên, tuyệt đối không cấp sổ hay xây dựng.' },
  MNC: { name: 'Đất có mặt nước chuyên dùng', risk: 'danger', riskLabel: 'MẶT NƯỚC CHUYÊN DÙNG', color: '#0369a1', desc: 'Hồ điều tiết, mặt nước chuyên dùng.' },
  DNL: { name: 'Đất công trình năng lượng (Hành lang điện)', risk: 'danger', riskLabel: 'HÀNH LANG AN TOÀN LƯỚI ĐIỆN', color: '#dc2626', desc: 'Hành lang an toàn lưới điện cao thế, bị giới hạn chiều cao hoặc cấm xây dựng.' },
  TON: { name: 'Đất cơ sở tôn giáo', risk: 'caution', riskLabel: 'ĐẤT TÔN GIÁO', color: '#a855f7', desc: 'Chùa, nhà thờ, cơ sở tôn giáo.' },
  DCH: { name: 'Đất chợ', risk: 'caution', riskLabel: 'ĐẤT CHỢ', color: '#f59e0b', desc: 'Quy hoạch chợ truyền thống / thương mại.' }
};

// VN-2000 Proj4 Definitions (Exact 7-parameter Bursa-Wolf transform per QĐ 05/2007/QĐ-BTNMT)
// +towgs84=-191.90441429,-39.30318279,-111.45032835,-0.00928836,0.01975479,-0.00427372,0.252906278
window.VN2000_ZONES = {
  hcm: {
    label: 'TP.HCM / Bình Dương / Long An (Kinh tuyến trục 105°45\', Múi 3°)',
    proj4: '+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,-0.00928836,0.01975479,-0.00427372,0.252906278 +units=m +no_defs'
  },
  dongnai: {
    label: 'Đồng Nai / Bà Rịa - Vũng Tàu (Kinh tuyến trục 107°45\', Múi 3°)',
    proj4: '+proj=tmerc +lat_0=0 +lon_0=107.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,-0.00928836,0.01975479,-0.00427372,0.252906278 +units=m +no_defs'
  },
  tayninh: {
    label: 'Tây Ninh (Kinh tuyến trục 105°30\', Múi 3°)',
    proj4: '+proj=tmerc +lat_0=0 +lon_0=105.5 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,-0.00928836,0.01975479,-0.00427372,0.252906278 +units=m +no_defs'
  },
  zone48n: {
    label: 'VN-2000 Múi 6° (Kinh tuyến trục 105°00\')',
    proj4: '+proj=tmerc +lat_0=0 +lon_0=105.0 +k=0.9996 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=-191.90441429,-39.30318279,-111.45032835,-0.00928836,0.01975479,-0.00427372,0.252906278 +units=m +no_defs'
  }
};

// Quick Jump Locations across HCMC & Neighboring Provinces
window.QUICK_LOCATIONS = [
  { group: 'TP.HCM — Nội Thành', name: 'Quận 8 (Tạ Quang Bửu / Kênh Đôi)', lat: 10.7405, lng: 106.6620, zoom: 17 },
  { group: 'TP.HCM — Nội Thành', name: 'Quận 1 (Nguyễn Huệ / Bến Thành)', lat: 10.7740, lng: 106.7010, zoom: 17 },
  { group: 'TP.HCM — Nội Thành', name: 'TP. Thủ Đức — Thủ Thiêm', lat: 10.7715, lng: 106.7215, zoom: 16 },
  { group: 'TP.HCM — Nội Thành', name: 'TP. Thủ Đức — TOD Trường Thọ', lat: 10.8355, lng: 106.7590, zoom: 16 },
  { group: 'TP.HCM — Nội Thành', name: 'TP. Thủ Đức — Long Bình (VĐ3)', lat: 10.8440, lng: 106.8320, zoom: 15 },
  { group: 'TP.HCM — Nội Thành', name: 'Quận 7 — Phú Mỹ Hưng', lat: 10.7295, lng: 106.7195, zoom: 16 },
  { group: 'TP.HCM — Nội Thành', name: 'Quận Bình Tân — Tên Lửa', lat: 10.7480, lng: 106.6120, zoom: 16 },
  { group: 'TP.HCM — 5 Huyện (Có QH 2030)', name: 'Bình Chánh — Tân Kiên / VĐ2', lat: 10.7200, lng: 106.5980, zoom: 15 },
  { group: 'TP.HCM — 5 Huyện (Có QH 2030)', name: 'Nhà Bè — Nguyễn Hữu Thọ', lat: 10.6780, lng: 106.7160, zoom: 15 },
  { group: 'TP.HCM — 5 Huyện (Có QH 2030)', name: 'Hóc Môn — Song Hành QL22', lat: 10.8830, lng: 106.5950, zoom: 15 },
  { group: 'TP.HCM — 5 Huyện (Có QH 2030)', name: 'Củ Chi — Thị trấn Củ Chi', lat: 10.9735, lng: 106.4940, zoom: 15 },
  { group: 'TP.HCM — 5 Huyện (Có QH 2030)', name: 'Cần Giờ — Khu Lấn Biển Cần Thạnh', lat: 10.4080, lng: 106.9550, zoom: 14 },
  { group: 'Vùng Ven (Bình Dương / Đồng Nai / Long An / BR-VT)', name: 'Bình Dương — TP. Dĩ An (Nút Tân Vạn)', lat: 10.8960, lng: 106.8090, zoom: 15 },
  { group: 'Vùng Ven (Bình Dương / Đồng Nai / Long An / BR-VT)', name: 'Bình Dương — TP. Thuận An (QL13)', lat: 10.9250, lng: 106.7120, zoom: 15 },
  { group: 'Vùng Ven (Bình Dương / Đồng Nai / Long An / BR-VT)', name: 'Đồng Nai — Sân Bay Long Thành', lat: 10.8080, lng: 107.0750, zoom: 14 },
  { group: 'Vùng Ven (Bình Dương / Đồng Nai / Long An / BR-VT)', name: 'Đồng Nai — Nhơn Trạch (Cầu VĐ3)', lat: 10.7680, lng: 106.8780, zoom: 14 },
  { group: 'Vùng Ven (Bình Dương / Đồng Nai / Long An / BR-VT)', name: 'Long An — Bến Lức (Lương Hòa / VĐ3)', lat: 10.6750, lng: 106.4950, zoom: 14 },
  { group: 'Vùng Ven (Bình Dương / Đồng Nai / Long An / BR-VT)', name: 'BR-VT — TP. Cảng Phú Mỹ', lat: 10.5920, lng: 107.0520, zoom: 14 }
];
