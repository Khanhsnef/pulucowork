# 🚦 Hệ Thống Giám Sát Camera & Giao Thông Trực Tuyến Toàn Quốc (Nationwide Traffic Portal)

Ứng dụng web trực quan hóa tình trạng giao thông theo thời gian thực trên toàn quốc với trọng tâm là **TP. Hồ Chí Minh (835 camera giao thông công cộng)** kết hợp cùng **9 tỉnh thành phố trọng điểm** (Hà Nội, Đà Nẵng, Bình Dương, Đồng Nai, Hải Phòng, Cần Thơ, Lâm Đồng/Đà Lạt, Bà Rịa - Vũng Tàu, Thừa Thiên Huế).

---

## 🌟 Tính Năng Nổi Bật

1. **🌐 Đa Tỉnh / Thành Phố Toàn Quốc (Nationwide Multi-Province Switcher):**
   - Hỗ trợ chuyển đổi nhanh 10 tỉnh thành phố trọng điểm ngay trên Header:
     - 🌟 **TP. Hồ Chí Minh:** Toàn bộ 835 mắt camera live snapshot, 21 thẻ Quick-view đại diện quận/huyện.
     - 🏛️ **Hà Nội:** 15 nút giao & cầu huyết mạch (Ngã Tư Sở, Vành Đai 3, Cầu Giấy, Cầu Chương Dương, Cầu Vĩnh Tuy, Cầu Nhật Tân, Ngã Tư Vọng, v.v.).
     - 🌊 **Đà Nẵng:** Cầu Rồng, Cầu Sông Hàn, Cầu Trần Thị Lý, Hầm chui Điện Biên Phủ, v.v.
     - 🏭 **Bình Dương:** Vòng xoay An Phú, Ngã tư 550, QL13, Miếu Ông Cù, Sóng Thần, v.v.
     - 🚛 **Đồng Nai:** Ngã 4 Vũng Tàu, Cầu Đồng Nai, Tam Hiệp, Cổng 11, Sân bay Long Thành, v.v.
     - ⚓ **Hải Phòng:** Cầu Hoàng Văn Thụ, Cầu Rào, Cầu Bạch Đằng, Cảng Đình Vũ, v.v.
     - 🌾 **Cần Thơ:** Cầu Cần Thơ, Bến Ninh Kiều, Nút giao IC3, Cầu Hưng Lợi, v.v.
     - 🌲 **Lâm Đồng (Đà Lạt):** Đèo Prenn, Đèo Mimosa, Chợ Đà Lạt, Đèo Bảo Lộc, v.v.
     - 🏖️ **Bà Rịa - Vũng Tàu:** Vòng xoay Tượng Đài, Thùy Vân Bãi Sau, Cụm cảng Cái Mép - Thị Vải, v.v.
     - 🏯 **Thừa Thiên Huế:** Cầu Trường Tiền, Cầu Phú Xuân, Ngã 6 Hùng Vương, Cửa Ngõ Đại Nội, v.v.
   - Bản đồ tự động lướt mượt mà (`flyTo`) đến trung tâm từng tỉnh thành kèm cập nhật bộ lọc Quận/Huyện đặc thù.

2. **🚦 Tích Hợp Lớp Dữ Liệu Google Live Traffic Toàn Diện:**
   - Hiển thị trực tiếp vạch lưu lượng xe thời gian thực của Google: Xanh lá (Thông thoáng), Cam (Đông đúc), Đỏ / Đỏ thẫm (Ùn tắc / Kẹt xe) trên khắp mọi nẻo đường Việt Nam.

3. **🌧️ Radar Mưa Doppler & Cảnh Báo Mưa Thời Gian Thực:**
   - Quét dữ liệu thời tiết live từ Open-Meteo & RainViewer Doppler Radar.
   - Thẻ thông tin trên Header cảnh báo tức thời số lượng quận/huyện đang có mưa.
   - Bộ lọc `🌧️ Khu Vực Đang Mưa` cho phép 1 chạm lọc ngay những nơi đang mưa ngập để cảnh báo tài xế.

4. **📱 Tối Ưu Hóa Trải Nghiệm Thiết Bị Di Động (Mobile First):**
   - Thanh điều hướng ngón tay cái đáy màn hình (Bottom Navigation Bar) chuẩn App di động.
   - Header 2 tầng gọn gàng, chống tràn ngang màn hình, nút bấm cảm ứng lớn tối thiểu 44px.
   - Xem camera toàn màn hình mượt mà trên iPhone, Android.

5. **🔍 Zoom Tự Động Bật Camera & Quick View Đại Diện:**
   - Khi phóng to bản đồ vào bất kỳ giao lộ nào, camera gần nhất tự động mở popup.
   - Thẻ Quick-view ảnh live ghim sẵn trên bản đồ giúp nhìn lướt nhanh tình hình mà không cần click từng điểm.

---

## 🚀 Cách Sử Dụng

### Cách 1: Mở trực tiếp (Standalone File)
Chỉ cần nhấp đúp file `index.html` hoặc mở bằng trình duyệt (Chrome, Safari, Edge):
```bash
open index.html
```

### Cách 2: Triển khai Local Server
```bash
python3 server.py
# Hoặc
npx serve .
```

### Cách 3: Tải file Zip triển khai Hosting / Pages nội bộ
Toàn bộ source code được đóng gói trong `hcm-traffic-cams.zip` sẵn sàng upload lên Nginx, Apache, Netlify, Cloudflare Pages hoặc `pages.ahamove.com`.
