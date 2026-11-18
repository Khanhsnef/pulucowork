import urllib.request
import json
import re

print("1. Fetching data-camera.json...")
req1 = urllib.request.Request(
    "https://raw.githubusercontent.com/ePlus-DEV/camera/main/data-camera.json",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req1) as resp:
    data_cams = json.loads(resp.read().decode("utf-8"))

print("2. Fetching wme-wazevn-traffic-cams-list.js...")
req2 = urllib.request.Request(
    "https://update.greasyfork.org/scripts/497466/wme-wazevn-traffic-cams-list.js",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req2) as resp:
    waze_content = resp.read().decode("utf-8")

m = re.search(r"var\s+trafficCamsData\s*=\s*(\[.*?\]);", waze_content, re.DOTALL)
waze_cams = json.loads(m.group(1)) if m else []

waze_by_id = {}
for w in waze_cams:
    hcmc_url = w.get("url", {}).get("HCMC", "")
    m_id = re.search(r"id=([a-f0-9]{24})", hcmc_url)
    if m_id:
        cid = m_id.group(1)
        waze_by_id[cid] = w

districts_geo = [
    ("Quận 1", 10.765, 10.795, 106.690, 106.715),
    ("Quận 3", 10.770, 10.795, 106.670, 106.695),
    ("Quận 4", 10.750, 10.770, 106.695, 106.720),
    ("Quận 5", 10.745, 10.765, 106.655, 106.680),
    ("Quận 6", 10.735, 10.760, 106.625, 106.655),
    ("Quận 7", 10.715, 10.755, 106.700, 106.755),
    ("Quận 8", 10.710, 10.750, 106.620, 106.690),
    ("Quận 10", 10.760, 10.785, 106.655, 106.675),
    ("Quận 11", 10.755, 10.778, 106.640, 106.660),
    ("Quận 12", 10.830, 10.890, 106.610, 106.710),
    ("Quận Bình Thạnh", 10.790, 10.835, 106.695, 106.735),
    ("Quận Gò Vấp", 10.820, 10.865, 106.650, 106.700),
    ("Quận Phú Nhuận", 10.790, 10.815, 106.670, 106.695),
    ("Quận Tân Bình", 10.785, 10.830, 106.635, 106.675),
    ("Quận Tân Phú", 10.765, 10.805, 106.615, 106.645),
    ("Quận Bình Tân", 10.725, 10.810, 106.575, 106.625),
    ("TP Thủ Đức", 10.760, 10.890, 106.720, 106.850),
    ("Huyện Bình Chánh", 10.630, 10.760, 106.520, 106.630),
    ("Huyện Hóc Môn", 10.850, 10.930, 106.550, 106.640),
    ("Huyện Củ Chi", 10.920, 11.150, 106.400, 106.600),
    ("Huyện Nhà Bè", 10.640, 10.720, 106.700, 106.760),
]

district_centers = {
    "Quận 1": (10.7769, 106.7009),
    "Quận 3": (10.7844, 106.6843),
    "Quận 4": (10.7578, 106.7013),
    "Quận 5": (10.7540, 106.6634),
    "Quận 6": (10.7481, 106.6352),
    "Quận 7": (10.7340, 106.7218),
    "Quận 8": (10.7241, 106.6286),
    "Quận 10": (10.7716, 106.6674),
    "Quận 11": (10.7629, 106.6504),
    "Quận 12": (10.8672, 106.6413),
    "Quận Bình Thạnh": (10.8106, 106.7091),
    "Quận Gò Vấp": (10.8387, 106.6653),
    "Quận Phú Nhuận": (10.7992, 106.6803),
    "Quận Tân Bình": (10.8015, 106.6558),
    "Quận Tân Phú": (10.7901, 106.6281),
    "Quận Bình Tân": (10.7654, 106.6039),
    "TP Thủ Đức": (10.8494, 106.7715),
    "Huyện Bình Chánh": (10.6874, 106.5938),
    "Huyện Hóc Môn": (10.8842, 106.5913),
    "Huyện Củ Chi": (11.0067, 106.5132),
    "Huyện Nhà Bè": (10.6953, 106.7324),
}

hotspot_keywords = [
    "Hàng Xanh", "Dân Chủ", "Lăng Cha Cả", "Cộng Hòa", "Trường Chinh", 
    "Sài Gòn", "Thủ Thiêm", "Rạch Chiếc", "Phù Đổng", "Cây Gõ", 
    "An Sương", "Phú Lâm", "Võ Văn Kiệt", "Mai Chí Thọ", "Điện Biên Phủ",
    "Phạm Văn Đồng", "Nam Kỳ Khởi Nghĩa", "Nguyễn Văn Trỗi", "Xô Viết Nghệ Tĩnh",
    "Nguyễn Hữu Cảnh", "Bạch Đằng", "Đinh Bộ Lĩnh", "Quốc Lộ 1", "Quốc Lộ 13",
    "Cầu Kênh Tẻ", "Cầu Chữ Y", "Cầu Nguyễn Văn Cừ", "Ngã tư Bảy Hiền", "Ngã 6 Gò Vấp",
    "Kinh Dương Vương", "An Lạc", "Hồ Học Lãm", "Tên Lửa", "Quốc Lộ 1A", "Mã Lò", 
    "Bà Hom", "Hương Lộ 2", "Bốn Xã", "Bình Phước", "Trạm 2", "Suối Tiên",
    "Cách Mạng Tháng", "Lý Thái Tổ", "Ba Tháng Hai", "Hai Bà Trưng", "Nguyễn Thị Minh Khai",
    "Pasteur", "Hoàng Văn Thụ", "Phan Đăng Lưu", "Đinh Tiên Hoàng", "Xa Lộ Hà Nội",
    "Nguyễn Tri Phương", "Ngô Gia Tự", "Lê Văn Việt", "Hoàng Diệu", "Nguyễn Tất Thành",
    "Quang Trung", "Phan Văn Trị", "Nguyễn Kiệm", "Nguyễn Oanh", "Nguyễn Văn Linh", 
    "Nguyễn Thị Thập", "Huỳnh Tấn Phát", "Phạm Hùng", "Dương Bá Trạc", "Tạ Quang Bửu", 
    "Lê Văn Lương", "Nguyễn Hữu Thọ", "Tân Sơn Nhất", "Tô Ký", "Quốc Lộ 22",
    "Hùng Vương", "An Dương Vương", "Lý Thường Kiệt", "Hoàng Sa", "Trường Sa"
]

def normalize_district(raw_dist, lat, lon):
    if raw_dist in ["TP. Thủ Đức", "Quận 2", "Quận 9", "Quận Thủ Đức"]:
        return "TP Thủ Đức"
    if raw_dist in district_centers:
        return raw_dist
    if lat and lon:
        for dname, min_lat, max_lat, min_lon, max_lon in districts_geo:
            if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
                return dname
    return raw_dist if raw_dist not in ["N/A", "false", "2", None, "Trung tâm TP.HCM"] else "Quận 1"

processed_cameras = []
seen_ids = set()

for cam in data_cams:
    cid = cam.get("CamId")
    if not cid or cid in seen_ids:
        continue
    seen_ids.add(cid)

    name = cam.get("CamName", "Camera giao thông")
    raw_dist = cam.get("Disctrict", "TP. Hồ Chí Minh")

    lat, lon = None, None
    if cid in waze_by_id:
        w_cam = waze_by_id[cid]
        lat = float(w_cam["lat"])
        lon = float(w_cam["lon"])
        if w_cam.get("desc") and (name.startswith("TTH") or name.startswith("ITS") or len(name) < 8):
            name = f"{w_cam['desc']} ({name})"

    has_exact_coords = lat is not None and lon is not None
    if not has_exact_coords:
        coords = district_centers.get(raw_dist, (10.7769, 106.7009))
        import hashlib
        h = int(hashlib.md5(cid.encode()).hexdigest(), 16)
        lat = coords[0] + ((h % 100) - 50) * 0.0003
        lon = coords[1] + (((h >> 8) % 100) - 50) * 0.0003

    district = normalize_district(raw_dist, lat, lon)
    is_hotspot = any(kw.lower() in name.lower() for kw in hotspot_keywords)
    snapshot_url = f"https://camera.thongtingiaothong.vn/api/snapshot/{cid}"

    processed_cameras.append({
        "id": cid,
        "name": name,
        "district": district,
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "hasExactCoords": has_exact_coords,
        "isHotspot": is_hotspot,
        "snapshotUrl": snapshot_url
    })

for cid, w_cam in waze_by_id.items():
    if cid not in seen_ids:
        seen_ids.add(cid)
        name = w_cam.get("desc", f"Camera {cid[:8]}")
        lat = float(w_cam["lat"])
        lon = float(w_cam["lon"])
        district = normalize_district("TP. Hồ Chí Minh", lat, lon)
        is_hotspot = any(kw.lower() in name.lower() for kw in hotspot_keywords)
        snapshot_url = f"https://camera.thongtingiaothong.vn/api/snapshot/{cid}"

        processed_cameras.append({
            "id": cid,
            "name": name,
            "district": district,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "hasExactCoords": True,
            "isHotspot": is_hotspot,
            "snapshotUrl": snapshot_url
        })

print(f"Total processed cameras: {len(processed_cameras)}")
hotspots_count = sum(1 for c in processed_cameras if c["isHotspot"])
print(f"Hotspot cameras: {hotspots_count}")

with open("hcm-traffic-cams/cameras.json", "w", encoding="utf-8") as f:
    json.dump(processed_cameras, f, ensure_ascii=False, indent=2)

with open("hcm-traffic-cams/cameras-data.js", "w", encoding="utf-8") as f:
    f.write("window.HCM_CAMERAS = ")
    json.dump(processed_cameras, f, ensure_ascii=False)
    f.write(";\n")

print("Saved cameras.json and cameras-data.js successfully!")
