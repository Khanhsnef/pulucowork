# PRD — AhaBenefits v2.0
> **Product Requirement Document** | Driver Management → Product  
> Phiên bản: 1.0 | Ngày: 2026-06-23 | Tác giả: Lê Phương Khanh (Driver Management Leader)  
> Tài liệu tham chiếu: `2026-05-ahabenefits-proposal.html` · `2026-05-ahabenefits-points-flow.md` · `2026-05-driver-ranking-params.md`

---

## 0. Mục lục

1. [Problem Statement](#1-problem-statement)
2. [Goals & Success Metrics](#2-goals--success-metrics)
3. [Scope & Phasing](#3-scope--phasing)
4. [Competitor Benchmark](#4-competitor-benchmark)
5. [Module 1 — AhaPoints Engine](#5-module-1--ahapoints-engine)
6. [Module 2 — AhaBenefits Store (Catalog)](#6-module-2--ahabenefits-store-catalog)
7. [Module 3 — Driver App UI/UX](#7-module-3--driver-app-uiux)
8. [Module 4 — Admin Tool (Ops/CS)](#8-module-4--admin-tool-opscs)
9. [Notification System](#9-notification-system)
10. [Open Questions](#10-open-questions)
11. [Timeline & Rollout](#11-timeline--rollout)

---

## 1. Problem Statement

### Situation
Ahamove hiện vận hành đội ngũ tài xế Bike (Instant) quy mô lớn tại SGN và HAN. Driver là tài sản cạnh tranh cốt lõi — thiếu supply trực tiếp ảnh hưởng AR, FR, và SLA với merchant. Các chương trình hỗ trợ như Bảo hiểm, các voucher gotit, các voucher hỗ trợ từ các partnership như MindX, Valvoline, Dat Bike, Selex,... chưa được tích hợp vào một hệ thống, hiện tại vẫn đang thủ công gửi cho Tài xế thông qua noti, sms, khiến tỉ lệ sử dụng voucher thấp, tài xế không biết được những quyền lợi mà mình được hưởng.

### Complication
Mặc dù công ty đã đàm phán được nhiều chương trình hỗ trợ giá trị cao (Bảo hiểm, MindX, Valvoline, Dat Bike, Selex...), nhưng do quy trình phân phối **rời rạc và thủ công** (qua SMS/Noti) kết hợp với mô hình incentive phụ thuộc vào **tiền mặt ngắn hạn**, dẫn đến:

| Vấn đề | Biểu hiện | Hệ quả |
|--------|-----------|--------|
| **Lãng phí giá trị đối tác** | Driver trôi tin nhắn SMS/Noti, tỷ lệ sử dụng voucher cực thấp | Lãng phí nguồn lực đàm phán B2B, không phát huy được lợi thế đối tác |
| **Trải nghiệm phân mảnh** | Thiếu nền tảng tập trung để tài xế tra cứu đặc quyền | Driver không nhận thức được toàn bộ giá trị phúc lợi (Low Perceived Value) |
| **CPO leo thang** | Đốt tiền mặt liên tục để kích supply giờ peak vì hệ thống phúc lợi phi tiền mặt chưa hoạt động hiệu quả | Không bền vững theo mùa, dễ bị đối thủ lôi kéo bằng cash promo |
| **Loyalty thấp** | Driver chạy multi-platform (Grab + Ahamove song song), không có lý do gắn kết ngoài thu nhập | Churn rate cao, đặc biệt ở tập tài xế R1 cốt lõi |

### Resolution
Xây dựng **AhaBenefits v2.0** — một **Hub quyền lợi tập trung in-app** kết hợp cơ chế tích lũy điểm (AhaPoints) tự động gắn chặt với Driver Ranking (R1/R2/R3).
*   **Mục tiêu:** Số hóa và tự động hóa toàn bộ quy trình cấp phát voucher đối tác vào một Cửa hàng đổi thưởng (AhaBenefits Store).
*   **Tác động:** Giúp tài xế dễ dàng truy xuất, sử dụng quyền lợi; nâng cao nhận thức về giá trị phúc lợi; qua đó chuyển dịch từ *mối quan hệ giao dịch (transactional)* sang *hệ sinh thái trung thành (loyalty ecosystem)* và giảm áp lực lên CPO dài hạn.

---

## 2. Goals & Success Metrics

### 2.1 Business Goals

| Goal | Mô tả |
|------|-------|
| **Tăng Loyalty** | Driver R1/R2 có lý do để duy trì hoạt động trên Ahamove |
| **Giảm Churn** | Giảm tỷ lệ rời bỏ R1/R2 bằng quyền lợi gắn với rank |
| **Tối ưu CPO** | Dùng điểm thay thế một phần cash incentive cho driver chất lượng cao |
| **Điều hướng supply** | Dùng multiplier điểm thay tiền để kéo driver vào giờ khó/thời tiết xấu |

### 2.2 Success Metrics

| KPI | Baseline (nay) | Target (6 tháng sau launch) | Đo lường |
|-----|---------------|----------------------------|-----------|
| **Point Burn Rate** | — | > 60% | Điểm đổi / Điểm phát |
| **Redemption Rate** | — | > 80% | Mã voucher dùng thành công / Mã phát |
| **Voucher tab CTR** | — | > 40% weekly active drivers | Click vào AhaBenefits tab / DAD |
| **R1/R2 Churn Rate** | Baseline TBD | Giảm 30% | Driver R1/R2 rời platform / tháng |
| **AR peak hour** | Baseline TBD | +2–3 pp | AR khung giờ 11h–13h, 17h–20h |
| **Avg AhaPoints/Driver/Month** | — | > 1.500 pts (R3) | Tracking ví điểm |
| **DAD (Daily Active Drivers)** | Baseline TBD | +5% | Driver có ít nhất 1 đơn/ngày |

---

## 3. Scope & Phasing

### In Scope
- **Dịch vụ:** Bike Instant (Giao ngay 1H, Siêu tốc, Ghép đơn, 4H) + Enterprise/SME (API Shopee, TikTok Shop)
- **Địa lý:** TP.HCM (SGN) + Hà Nội (HAN) — Phase 1 pilot 500 R1 drivers SGN
- **Driver segment:** R1 Elite, R2 Active, R3 Standard (đã có ranking)
- **Nền tảng:** Driver App (mobile) + Admin tool (web)

### Out of Scope (v2.0)
- Xe tải (Truck) — không thuộc phạm vi DM
- Các tỉnh thành ngoài SGN/HAN — Phase 3 mở rộng
- Transfer/Gift điểm giữa driver — nghiên cứu v3.0
- Driver chưa có rank (Unranked/L6) — chỉ xem catalog, không đổi

---

## 4. Competitor Benchmark

### 4.1 Tổng quan so sánh

| Platform | Tên chương trình | Cơ chế tích điểm | Catalog | Điểm mạnh | Điểm yếu |
|----------|-----------------|------------------|---------|-----------|----------|
| **Grab (VN/MY/SG)** | GrabRewards for Drivers | Điểm theo trip + weekly challenge | Nhiên liệu, bảo hiểm, thiết bị | Tích hợp sâu vào app, UX mượt 
| **Gojek (ID)** | GoPoints | Điểm theo GSV + tier GoClub | F&B, health, data | Ecosystem rộng (GoFood, GoPay) | Leverage internal ecosystem, khó replicate |
| **Uber (US)** | Uber Pro | Điểm theo trips, tier Gold/Platinum/Diamond | Cashback xăng, phí app, học phí | Điểm đổi phí dịch vụ (high perceived value) | Market khác biệt, model không apply trực tiếp |
| **DoorDash (US)** | DoorDash Rewards | Streak bonus, challenge | Voucher Chevron, thiết bị | Streak mechanic hiệu quả | Delivery-only, không phù hợp model Bike VN |
| **Be Delivery (VN)** | beLoyalty *(customer-side only)* | **Driver: không có loyalty points** — chỉ cash bonus theo trips/zone/giờ, thay đổi theo campaign. beLoyalty là chương trình tích bePoint dành cho hành khách, không phải tài xế | — | Agile promo response | Driver retention hoàn toàn bằng tiền mặt ngắn hạn, không tạo switching cost |

> **Nguồn tham khảo:**
> - Grab Driver: [grab.com/vn/driver](https://www.grab.com/vn/driver/) — chính sách tài xế VN
> - Uber Pro: [uber.com/us/en/drive/driver-app/uber-pro](https://www.uber.com/us/en/drive/driver-app/uber-pro/) — tier structure và catalog benefits
> - Gojek GoClub: báo cáo nội bộ DM + [gojek.com/id/driver](https://www.gojek.com/id/driver/) — tier GoRide/GoFood unified
> - DoorDash: [help.doordash.com/dashers/s/article/DoorDash-Rewards-Program](https://help.doordash.com/dashers/s/article/DoorDash-Rewards-Program)
> - Benchmark tổng hợp: `2026-06-global-driver-lifecycle-benchmark.md` (internal, DM team)

### 4.2 Positioning của AhaBenefits

```
                High Perceived Value
                       │
          Uber Pro      │     AhaBenefits v2.0 ◄ Target position
          (fee rebate)  │     (partnership catalog + insurance)
                        │
Low cash cost ──────────┼──────────────────── High cash cost
                        │
          Be/Grab VN    │     Gojek GoClub
          (flash promo) │     (internal ecosystem)
                        │
                Low Perceived Value
```

**Insight chính:** Không có đối thủ nào tại VN đang triển khai loyalty points gắn với Driver Tier một cách hệ thống. AhaBenefits có cơ hội trở thành **first-mover** trong phân khúc Bike logistics tại VN.

---

## 5. Module 1 — AhaPoints Engine

### 5.1 Tổng quan vòng đời điểm

```
[Trip hoàn thành]
      │
      ▼
[Tính điểm: GSV ÷ 5,000 × Layer Multiplier]
      │
      ▼
[PENDING — trong ca, chưa dùng được]
      │
   [Cuối ca — batch job T+1]
      │
   ┌──┴──────────────────────┐
   │ Đủ điều kiện ca         │ Không đủ
   ▼                         ▼
[AVAILABLE + Bonus]    [AVAILABLE — không bonus]
      │
   ┌──┴──────────┐
   │             │
[Đổi thưởng] [Vi phạm/Adjust]
   │             │
[REDEEMED]   [DEDUCTED]   ────── Cuối quý ──► [EXPIRED]
(điểm trừ ngay,
 reward vào "Quà của tôi")
```

> **Nguyên tắc cốt lõi:** Điểm bị trừ **ngay lập tức** khi driver xác nhận đổi thưởng — không chờ partner, không có bước trung gian. Reward xuất hiện trong "Quà của tôi" ngay sau đó. Trạng thái `RESERVED` được loại bỏ khỏi flow.

**4 trạng thái điểm:**

| Trạng thái | Mô tả | Có thể dùng? |
|------------|-------|-------------|
| `PENDING` | Điểm trong ca, chưa validate | Không |
| `AVAILABLE` | Đã credit vào ví, sẵn sàng đổi | Có |
| `REDEEMED` | Đã đổi thành công, điểm trừ ngay | — |
| `EXPIRED` | Hết hạn cuối quý | — |

---

### 5.2 Công thức tính điểm

**Công thức cơ bản:**
```
earned_pts = round( round(trip_GSV ÷ 5,000) × layer_multiplier )
```

**Bước tính chi tiết:**

| Bước | Sự kiện | Hành động hệ thống |
|------|---------|-------------------|
| 1 | Trip auto-complete | Ghi nhận `trip_GSV` (VND) |
| 2 | Xác định layer của đơn (L2–L6) | Lấy `layer_multiplier` từ config |
| 3 | Kiểm tra driver có trong priority layer không | Overflow → multiplier = ×1.0 |
| 4 | `raw_pts = trip_GSV ÷ 5,000` | Giá trị thập phân |
| 5 | `base_pts = round(raw_pts)` | ≥ 0.5 làm tròn lên |
| 6 | `earned_pts = round(base_pts × multiplier)` | Làm tròn sau nhân hệ số |
| 7 | Cộng vào `shift_trip_pts` (PENDING) | Chưa credit vào ví |
| 8 | Cập nhật `shift_gsv_total` | Dùng xét điều kiện bonus ca |

**Ví dụ:**

| GSV | Tính | Kết quả |
|-----|------|---------|
| 14,000đ | 14,000 ÷ 5,000 = 2.8 → round = 3 | **3 pts** |
| 12,000đ | 12,000 ÷ 5,000 = 2.4 → round = 2 | **2 pts** |
| 70,000đ × L2 (×1.5) | 14 × 1.5 = 21.0 → round | **21 pts** |

---

### 5.3 Layer Multiplier Config

| Layer | Driver Rank | Multiplier | Ghi chú |
|-------|-------------|------------|--------|
| L2 Minizone | R1 Elite | ×1.5 | Priority zone tốt nhất |
| L3 Mediumzone | R2 Active | ×1.3 | |
| L4 Bigzone | R3 Standard | ×1.1 | |
| L6 MASS | Unranked | ×1.0 | Không bonus ca |
| Overflow | Bất kỳ | ×1.0 | Đơn overflow từ layer khác |

> **Nguyên tắc:** Điểm tính theo **layer của đơn**, không theo rank của driver.
> R1 nhận đơn overflow từ L3 → multiplier = ×1.3 (layer L3), không phải ×1.5.

**Cần Product quyết định:** Layer của đơn overflow xác định bằng **origin zone** hay **assigned zone**? (→ xem Open Questions #2)

---

### 5.4 Bonus hoàn ca

| Điều kiện | Mô tả |
|-----------|-------|
| ✅ Online in zone | Online trong zone đăng ký ≥ 90% thời lượng ca |
| ✅ Đủ hoạt động | AR và số chuyến tối thiểu trong ca |
| ❌ Offline/ngoài zone | Không bonus, điểm chuyến giữ nguyên |
| ❌ Ca bị force-close | Không bonus, điểm chuyến giữ nguyên |

**Bonus theo layer:**

| Layer | Bonus hoàn ca |
|-------|--------------|
| L2 (R1) | 30 pts/ca |
| L3 (R2) | 25 pts/ca |
| L4 (R3) | 20 pts/ca |
| L6 / Overflow | Không bonus |

> **Open Question #1:** Ngưỡng "online in zone" cụ thể bao nhiêu %? Đề xuất: ≥ 80%.

---

### 5.5 Credit T+1

```
[23:59 ngày N — kết thúc ca]
       │
       ▼
[02:00–04:00 sáng N+1 — batch job validate]
 · Check online_hour_in_zone
 · Check điều kiện hoạt động ca
       │
   ┌───┴──────────────────┐
   │ Đủ điều kiện         │ Không đủ
   ▼                      ▼
shift_trip_pts           shift_trip_pts
+ bonus_pts              (chỉ trip pts)
       │                      │
       └──────────┬───────────┘
                  ▼
   [PENDING → AVAILABLE]
   [Push notification sáng N+1:
    "Ca [tên ca] hôm qua: +X pts
     (Y pts trip + Z pts bonus ca)"]
```

---

### 5.6 Expiry — Điểm hết hạn cuối quý

**Lịch cuối quý:** 31/3 · 30/6 · 30/9 · 31/12 lúc 23:59

| Trạng thái điểm | Xử lý cuối quý |
|-----------------|---------------|
| `AVAILABLE` | Expire toàn bộ |
| `RESERVED` (đang đổi) | Bảo vệ 7 ngày sang quý mới |
| `PENDING` (trong ca) | Credit vào ví rồi expire |

**Reminder notifications:**
- 7 ngày trước cuối quý: "Còn X pts hết hạn ngày [date]"
- 1 ngày trước: nhắc lần 2

---

### 5.7 Point Timeline hàng tháng

```
Ngày 01      Voucher xăng/EV rank entitlement phát tự động (R1, R2)
             Coverage bảo hiểm có hiệu lực (nếu đã đăng ký)

Ngày 01–24   Tích điểm / đổi điểm bình thường

Ngày 25      ⚠️ DEADLINE đăng ký / hủy bảo hiểm tai nạn R1
             (coverage áp dụng từ ngày 01 tháng sau)

Ngày 26–31   Tích điểm / đổi điểm bình thường

Cuối quý     23:59 — Điểm AVAILABLE expire, balance reset về 0
```

---

### 5.8 Adjustment System

**5.8.1 Trừ điểm tự động:**

| Sự kiện | Điểm trừ | Thời điểm | Ghi chú |
|---------|---------|-----------|--------|
| Vi phạm ĐBCL (Đảm bảo Chất lượng) | −50 pts | Ngay khi xác nhận | Ghi log lý do |
| Gian lận / báo cáo giả | −50 pts/lần + review rank | Sau xác minh | CS xử lý thủ công |
| Hủy chuyến không lý do | Không trừ điểm | — | Ảnh hưởng DCR → ảnh hưởng rank |

**5.8.2 Cộng điểm bonus sự kiện:**

| Sự kiện | Điểm thưởng | Trigger |
|---------|------------|--------|
| Streak 7 ngày liên tục | [TBD] pts | Auto detect |
| Campaign đặc biệt (Mega Sales) | [TBD] pts | Campaign config bởi Ops |
| Referral driver mới | [TBD] pts | Sau khi driver mới hoàn thành 10 đơn |

**5.8.3 Manual Adjustment (CS/Ops):**
- Chỉ CS/Ops có quyền, qua Admin tool
- Add points: cần lý do + approval cấp trên
- Deduct points: cần lý do + notification cho driver
- Ghi đầy đủ audit log: ai làm, lúc nào, lý do gì

---

### 5.9 Edge Cases

**Scenario A — Đổi điểm cuối quý (29–31/6):**
```
Điểm trừ ngay khi driver xác nhận → reward vào "Quà của tôi" CLAIMED
Không có partner timeout. Không có hoàn điểm tự động.

Rủi ro: Driver đổi xong nhưng chưa bấm "Sử dụng ngay" → điểm đã mất,
  reward CLAIMED vẫn còn trong "Quà của tôi" (không expire theo điểm).

Rule: Reward (CLAIMED/USED) không bị expire theo quý — chỉ expire theo
  thời hạn của từng reward item (do DM config khi tạo reward).
```

**Scenario B — Driver bị downgrade rank:**
```
R1 → R2 sau kỳ xét rank cuối tháng

Nguyên tắc:
  ✅ Rewards đã REDEEMED → giữ nguyên, dùng đến hết hiệu lực
  ✅ Điểm AVAILABLE → giữ nguyên, không mất
  ❌ Catalog access → xuống tier Vàng (mất quyền đổi R1-only items)
  ❌ Đăng ký bảo hiểm mới → không được kể từ tháng rớt hạng

Notification: "Rank thay đổi Kim Cương → Vàng.
  Rewards đã đổi vẫn hiệu lực. Một số đặc quyền Kim Cương ngừng từ tháng tới."
```

**Scenario C — R1 nhận đơn overflow:**
```
R1 online L2, L2 đầy → cascade → nhận đơn từ L3
Trip income 70,000đ
  → Multiplier = ×1.0 (overflow, không phải ×1.5)
  → Điểm = round(14.0) × 1.0 = 14 pts
```

**Scenario D — Driver đổi sát cuối quý, muốn "giữ điểm":**
```
Không còn scenario này — điểm trừ ngay khi xác nhận đổi.
Driver không thể bị kẹt giữa "đã trừ điểm mà chưa có reward".
Reward CLAIMED luôn an toàn trong "Quà của tôi" dù điểm đã expire.
```

**Scenario E — Ca có cả đơn layer và overflow:**
```
Ca Sáng R2/L3: 5 đơn trong L3 + 2 đơn overflow

5 đơn L3:  ~52,000đ → 10 pts × 1.3 = 13 pts × 5 = 65 pts
2 đơn OFW: ~60,000đ → 12 pts × 1.0 = 12 pts × 2 = 24 pts
Bonus hoàn ca L3:                                  +25 pts
──────────────────────────────────────────────────────────
Tổng ca: 114 pts  (hiển thị breakdown trong app)
```

---

### 5.10 Data Model (gợi ý cho Engineering)

```
PointTransaction
  ├── id
  ├── driver_id
  ├── amount          (+/−)
  ├── type            EARNED | BONUS | REDEEMED | DEDUCTED | EXPIRED | ADJUSTED
  ├── status          PENDING | AVAILABLE | FINAL
  ├── source_ref      trip_id | shift_id | campaign_id | cs_ticket_id
  ├── layer           L2–L6 | OVERFLOW
  ├── multiplier_applied  1.0–1.5
  ├── created_at
  ├── expires_at      (cuối quý)
  └── note            (cho ADJUSTED)

DriverPointWallet
  ├── driver_id
  ├── available_balance
  ├── total_earned_current_quarter
  ├── quarter_expires_at
  └── last_updated_at
```

---

## 6. Module 2 — AhaBenefits Store (Catalog)

### 6.1 Cấu trúc Catalog theo Rank

| Tier | Rank | Màu sắc | Catalog Access |
|------|------|---------|---------------|
| Kim Cương | R1 Elite | 💎 | Full catalog + Insurance |
| Vàng | R2 Active | 🥇 | Advanced catalog |
| Bạc | R3 Standard | 🥈 | Basic catalog |
| Unranked | — | — | Xem không đổi được |

> Kế thừa theo thứ tự: R1 có quyền đổi tất cả items của R2 và R3.

---

### 6.2 Catalog Chi Tiết

**Free Items (Partnership — 0 cash cost cho Ahamove):**

| Danh mục | Sản phẩm | Rank yêu cầu | Điểm cần | Giá trị thực |
|---------|---------|-------------|---------|-------------|
| ⛽ Nhiên liệu | Voucher xăng 30k | R3+ | 170 pts | 30,000đ |
| | Voucher xăng 50k | R2+ | 285 pts | 50,000đ |
| | Voucher xăng 100k | R1 | — (entitlement tháng) | 100,000đ |
| ⚡ EV Charging | Voucher sạc 30k | R3+ | 170 pts | 30,000đ |
| | Voucher sạc 50k | R2+ | 285 pts | 50,000đ |
| 🔧 Bảo dưỡng | Thay nhớt cơ bản | R3+ | 65 pts | ~50,000đ |
| | Gói bảo dưỡng tiêu chuẩn | R2+ | 170 pts | ~150,000đ |
| | Gói bảo dưỡng ưu tiên R1 | R1 | 255 pts | ~250,000đ |
| 🍜 F&B | Voucher cơm/bún 20k | R3+ | 55 pts | 20,000đ |
| | Voucher F&B 50k | R2+ | 140 pts | 50,000đ |
| | Voucher F&B 100k | R1 | 285 pts | 100,000đ |
| 🏥 Sức khỏe | Khám sức khỏe cơ bản | R2+ | 40 pts | — |
| | Gói khám đầy đủ | R1 | 170 pts | — |

**Paid Items (Ahamove-funded):**

| Danh mục | Sản phẩm | Rank yêu cầu | Điểm cần | Chi phí Aha |
|---------|---------|-------------|---------|------------|
| 📱 Data 4G | 5GB (30 ngày) | R3+ | 400 pts | ~50,000đ |
| | 10GB (30 ngày) | R2+ | 700 pts | ~80,000đ |
| | 20GB (30 ngày) | R1 | 1,400 pts | ~150,000đ |
| 🎽 Đồng phục | Áo thun Ahamove | R3+ | 1,400 pts | ~120,000đ |
| | Combo (áo + túi nhiệt) | R2+ | 2,300 pts | ~250,000đ |
| 🛵 Phụ kiện | Bộ phụ kiện xe (gương, đèn) | R2+ | 3,400 pts | ~300,000đ |
| 🛡️ Bảo hiểm | Bảo hiểm tai nạn 10k/tháng | R1 only | 285 pts/tháng | 10,000đ |
| | Bảo hiểm tai nạn 30k/tháng | R1 only | 857 pts/tháng | 30,000đ |

---

### 6.3 Redemption Flow — Happy Path

> **Nguyên tắc:** Điểm bị trừ ngay khi driver xác nhận. Reward xuất hiện trong "Quà của tôi" ngay lập tức. Việc **sử dụng** reward (mang QR ra cửa hàng, bấm dùng mã) là bước tách biệt, xảy ra sau.

```
Driver mở tab AhaBenefits
       │
       ▼
[Hiển thị catalog theo Rank hiện tại]
       │
       ▼
[Driver chọn reward]
       │
       ▼
[Hệ thống kiểm tra 3 điều kiện]
  ├── Balance ≥ điểm yêu cầu?    → No → "Cần thêm X pts"
  ├── Rank đủ điều kiện?          → No → "Cần đạt [rank] để đổi"
  └── Reward còn slot (quantity)?  → No → "Tạm hết — thử lại sau"
       │ All pass
       ▼
[Màn hình xác nhận: tên reward + điểm sẽ trừ]
       │
       ▼
[Driver xác nhận]
       │
       ▼
[Hệ thống xử lý đồng thời — ngay lập tức]
  ├── Trừ điểm: AVAILABLE → REDEEMED
  ├── Giảm quantity reward đi 1
  └── Tạo reward record trong "Quà của tôi" — trạng thái: CLAIMED
       │
       ▼
[Màn hình "Đổi thành công"]
  Hiển thị: tên reward + thông tin sử dụng
  Nút: [Xem Quà của tôi] | [Đóng]
       │
       ▼
[Driver vào "Quà của tôi" → chọn reward → bấm "Sử dụng ngay"]
       │
       ▼
[Hiển thị nội dung reward theo delivery_type]
  (QR / code text / thông báo giao / thông báo cộng tiền)
  Trạng thái reward: CLAIMED → USED
```

**2 trạng thái của Reward trong "Quà của tôi":**

| Trạng thái | Mô tả | Hiển thị |
|------------|-------|---------|
| `CLAIMED` | Đã đổi điểm, chưa bấm sử dụng | "Chưa dùng" — hiển thị nút [Sử dụng ngay] |
| `USED` | Đã bấm sử dụng / đã được ghi nhận | "Đã dùng" — hiển thị lại nội dung (readonly) |

---

### 6.4 Reward Delivery Types — 4 loại phát thưởng

Mỗi reward khi được tạo trên Admin tool phải được chỉ định **một** `delivery_type`. Delivery type quyết định cách hệ thống xử lý sau khi điểm được RESERVED và driver xác nhận đổi.

---

#### Type 1 — VOUCHER_CODE (Mã text/số)

**Mô tả:** Hệ thống assign một mã alphanumeric từ pool do DM upload sẵn. Mã được lưu trong "Quà của tôi" ở trạng thái CLAIMED. Khi driver bấm **"Sử dụng ngay"** thì mã hiện ra và reward chuyển sang USED.

**Ví dụ áp dụng:** Mã giảm giá Urbox, mã nạp data 4G, mã voucher siêu thị.

```
[DM tạo reward — upload pool mã .csv]
  CODE001, CODE002, CODE003…
  Hệ thống lưu vào Code Pool, quantity = số dòng hợp lệ

[Driver đổi thành công — điểm trừ ngay]
  Hệ thống assign 1 mã từ Pool (FIFO) → gắn driver_id
  Quantity reward giảm 1
  Reward vào "Quà của tôi" — trạng thái: CLAIMED (mã chưa hiện)
       │
       ▼
[Driver vào "Quà của tôi" → bấm "Sử dụng ngay"]
       │
       ▼
[Màn hình hiển thị mã]
  Text lớn: "PETRO-CODE001"
  Nút: [Copy mã]
  Trạng thái: CLAIMED → USED
  (Mã vẫn hiển thị được sau khi USED — readonly, để driver xem lại)
       │
       ▼
[Driver đọc/copy mã → nhập tại cửa hàng/app đối tác]
```

**Quy tắc Code Pool:**
- 1 mã chỉ assign cho 1 driver duy nhất — không reuse
- Pool = 0 → reward hiển thị "Tạm hết" trên catalog, không nhận đổi mới
- Pool < 10% hoặc < 50 mã → Admin alert DM upload thêm
- Mã đã ASSIGNED không bị thu hồi kể cả khi driver bị suspend

---

#### Type 2 — QR_CODE (Mã QR tại cửa hàng)

**Mô tả:** Cùng cơ chế pool với VOUCHER_CODE, nhưng mã được render thành QR Code. Driver mang QR đến cửa hàng để nhân viên quét. Khi driver bấm **"Sử dụng ngay"** thì QR mới hiển thị full-screen.

**Ví dụ áp dụng:** Voucher xăng tại trạm Petrolimex, voucher bảo dưỡng tại garage đối tác.

```
[DM tạo reward — upload pool mã .csv, chọn delivery_type = QR_CODE]

[Driver đổi thành công — điểm trừ ngay]
  Assign 1 mã từ Pool → gắn driver_id
  Reward vào "Quà của tôi" — trạng thái: CLAIMED
  (QR chưa hiển thị ở bước này)
       │
       ▼
[Driver đến cửa hàng → vào "Quà của tôi" → bấm "Sử dụng ngay"]
       │
       ▼
[Màn hình QR full-screen]
  QR Code + tên reward + thời hạn
  Trạng thái: CLAIMED → USED
  Nút: [Lưu ảnh QR]
  (QR vẫn hiển thị được sau USED — readonly)
       │
       ▼
[Nhân viên cửa hàng quét QR bằng máy POS/app riêng của đối tác]
```

**Lưu ý:**
- QR phải hoạt động **offline** (render từ mã đã cached) — driver có thể ở vùng sóng yếu
- Thời hạn hiệu lực hiển thị rõ trên màn hình QR
- Cơ chế đối soát với đối tác (portal quét mã) là scope của Partnership team, nằm ngoài v2.0

---

#### Type 3 — PHYSICAL_GIFT (Quà vật lý — DM giao sau)

**Mô tả:** Không phát mã. Khi driver đổi thành công, hệ thống ghi nhận CLAIMED và DM xuất danh sách để xử lý giao quà. Driver bấm **"Sử dụng ngay"** = xác nhận muốn nhận quà, reward chuyển USED và DM thấy trong export list.

**Ví dụ áp dụng:** Áo thun Ahamove, túi nhiệt, phụ kiện xe, quà tặng sự kiện.

```
[Driver đổi thành công — điểm trừ ngay]
  Reward vào "Quà của tôi" — trạng thái: CLAIMED
  Hiển thị: "Nhấn 'Sử dụng ngay' để đăng ký nhận quà"

[Driver bấm "Sử dụng ngay"]
  Màn hình: form xác nhận địa chỉ nhận quà (SĐT, địa chỉ)
  Sau xác nhận: CLAIMED → USED
  Hiển thị: "Đã ghi nhận. Team Ahamove liên hệ trong [X] ngày làm việc."
       │
       ▼
[Ops/DM export danh sách USED từ Admin]
  Bao gồm: driver_id, tên, SĐT, địa chỉ, reward, ngày đổi
       │
       ▼
[DM giao quà offline]
       │
       ▼
[DM cập nhật sub-status trên Admin sau khi giao]
  → App driver cập nhật: "Đang xử lý" → "Đã giao"
  → Push notification: "Quà [tên reward] đã được giao"
```

**Sub-status của PHYSICAL_GIFT (sau khi USED):**

| Sub-status | Hiển thị app | Action |
|------------|-------------|--------|
| `PENDING_FULFILLMENT` | "Đang xử lý" | DM chuẩn bị hàng |
| `SHIPPED` | "Đang giao" | DM update sau khi ship |
| `DELIVERED` | "Đã giao" | Hoàn tất |

---

#### Type 4 — CASH_BONUS (Cột mốc ghi nhận → Cộng tiền sau)

**Mô tả:** Không phát mã. Dùng để tạo cột mốc ghi nhận trên hệ thống khi driver đổi điểm. DM xuất danh sách và cộng thưởng tiền vào tài khoản. Driver bấm **"Sử dụng ngay"** = xác nhận muốn nhận thưởng tiền, chuyển USED.

**Ví dụ áp dụng:** Campaign "Tích đủ X điểm nhận 200k vào tài khoản", thưởng milestone, thưởng cuối năm.

```
[Driver đổi thành công — điểm trừ ngay]
  Reward vào "Quà của tôi" — trạng thái: CLAIMED
  Hiển thị: "Nhấn 'Sử dụng ngay' để nhận [200,000đ] vào tài khoản"

[Driver bấm "Sử dụng ngay"]
  Màn hình xác nhận: số tiền + tài khoản nhận (lấy từ profile)
  Sau xác nhận: CLAIMED → USED
  Hiển thị: "[200,000đ] sẽ được cộng trong [X] ngày làm việc."
       │
       ▼
[Ops/DM export danh sách USED từ Admin]
  Bao gồm: driver_id, tên, SĐT, bank account, số tiền, ngày đổi
       │
       ▼
[DM/Finance cộng tiền qua hệ thống nội bộ]
       │
       ▼
[DM cập nhật "Đã cộng thưởng" trên Admin]
  → App driver: "Chờ cộng thưởng" → "Đã nhận thưởng"
  → Push notification: "Thưởng [200,000đ] đã được cộng vào tài khoản"
```

---

#### Tổng kết 4 Delivery Types

| Type | Điểm trừ khi | Mã hiện khi | Ghi nhận USED khi | Phù hợp cho |
|------|-------------|------------|-------------------|-------------|
| `VOUCHER_CODE` | Xác nhận đổi | Bấm "Sử dụng ngay" | Bấm "Sử dụng ngay" | Urbox, data 4G, siêu thị |
| `QR_CODE` | Xác nhận đổi | Bấm "Sử dụng ngay" | Bấm "Sử dụng ngay" | Xăng, bảo dưỡng, F&B tại điểm |
| `PHYSICAL_GIFT` | Xác nhận đổi | Không có mã | Bấm "Sử dụng ngay" + xác nhận địa chỉ | Áo, túi nhiệt, phụ kiện |
| `CASH_BONUS` | Xác nhận đổi | Không có mã | Bấm "Sử dụng ngay" + xác nhận tài khoản | Thưởng tiền mặt, milestone |

---

#### Admin Tool — Quản lý Code Pool (bổ sung Module 4)

Khi tạo reward có delivery_type = `VOUCHER_CODE` hoặc `QR_CODE`, DM team phải upload code pool:

```
[DM tạo reward mới trên Admin]
  → Điền: tên reward, điểm cần đổi, rank yêu cầu, thời hạn, delivery_type
  → Upload file .csv chứa danh sách mã
  → Hệ thống validate: kiểm tra trùng lặp, format hợp lệ
  → Hiển thị: "X mã hợp lệ / Y mã lỗi" → xác nhận import
  → Reward active khi pool > 0
```

**Monitoring Pool:**
- Dashboard hiển thị: Tổng mã / Đã dùng / Còn lại / % còn
- Alert khi pool < 10% hoặc < 50 mã (tùy config)
- DM có thể upload thêm mã bất kỳ lúc nào (append, không replace pool cũ)
- Export log: ai dùng mã nào, lúc nào (audit trail)

---

### 6.5 Bảo hiểm tai nạn R1 — Special Flow

```
Chỉ dành cho R1, đăng ký trước ngày 25 hàng tháng

Driver vào mục "Bảo hiểm R1"
       │
       ▼
[Chọn gói: 10k (285 pts) hoặc 30k (857 pts)]
       │
       ▼
[Xác nhận: "Coverage có hiệu lực từ 01/[tháng+1]"]
       │
       ▼
[Điểm RESERVED ngay]
       │
       ▼
[Ngày 01 tháng sau → REDEEMED, coverage kích hoạt]
[Gửi số hợp đồng bảo hiểm qua app/SMS]

Hủy (trước ngày 25):
  → Điểm RESERVED → AVAILABLE (hoàn lại)
  → Coverage ngừng cuối tháng hiện tại

Mất R1 mid-month:
  → Không cho đăng ký mới
  → Nếu đã RESERVED: giữ đến hết tháng đã đăng ký
```

---

### 6.6 Acceptance Criteria — Store

| # | Criteria | Delivery Type | Priority |
|---|---------|--------------|---------|
| AC-S1 | Driver thấy catalog đúng tier rank của mình | All | Must Have |
| AC-S2 | Điểm RESERVED ngay khi driver bấm xác nhận | All | Must Have |
| AC-S3 | VOUCHER_CODE: mã text hiển thị trong "Quà của tôi" ≤ 5 giây | VOUCHER_CODE | Must Have |
| AC-S4 | QR_CODE: QR render đúng, hoạt động offline (cached) | QR_CODE | Must Have |
| AC-S5 | PHYSICAL_GIFT: màn hình xác nhận ghi rõ "giao trong X ngày" | PHYSICAL_GIFT | Must Have |
| AC-S6 | CASH_BONUS: màn hình ghi rõ số tiền và thời gian cộng | CASH_BONUS | Must Have |
| AC-S7 | Code Pool = 0 → reward hiển thị "Tạm hết", không hiển thị lỗi kỹ thuật | VOUCHER_CODE / QR_CODE | Must Have |
| AC-S8 | Admin alert khi Code Pool < 10% | VOUCHER_CODE / QR_CODE | Must Have |
| AC-S9 | PHYSICAL_GIFT / CASH_BONUS: trạng thái sub-status cập nhật từ Admin → app ≤ 5 phút | PHYSICAL_GIFT / CASH_BONUS | Should Have |
| AC-S10 | Lịch sử đổi thưởng hiển thị đầy đủ: ngày, reward, điểm trừ, trạng thái | All | Should Have |
| AC-S11 | Insurance R1 hiển thị ngày coverage chính xác | Insurance | Must Have |
| AC-S12 | 1 mã trong pool chỉ được assign cho 1 driver (no reuse) | VOUCHER_CODE / QR_CODE | Must Have |

---

## 7. Module 3 — Driver App UI/UX

### 7.1 Information Architecture

```
Driver App
└── Tab "AhaBenefits" (icon mới)
    ├── AhaBenefits Homepage
    │   ├── Banner Carousel (quảng bá đối tác)
    │   ├── Point Balance Card (AhaPoints hiện tại)
    │   ├── Tier Badge (R1/R2/R3 + progress đến rank tiếp theo)
    │   ├── Quick Actions (Đổi thưởng / Lịch sử / Bảo hiểm)
    │   └── Featured Rewards (gợi ý dựa trên balance)
    │
    ├── Catalog (tab lọc)
    │   ├── Tab: Xăng & EV
    │   ├── Tab: Bảo dưỡng
    │   ├── Tab: Nhu yếu phẩm
    │   ├── Tab: Data & Thiết bị
    │   └── Tab: AhaStore (exclusive)
    │
    ├── Reward Detail
    │   ├── Hình ảnh + Tên reward
    │   ├── Điểm cần đổi
    │   ├── Điều kiện áp dụng + Thời hạn
    │   ├── Địa điểm đối tác (map/danh sách)
    │   └── [Đổi ngay] CTA
    │
    ├── Quà của tôi (My Rewards)
    │   ├── Voucher đang hiệu lực (QR / code)
    │   ├── Voucher đã dùng (lịch sử)
    │   └── Bảo hiểm đang active (số hợp đồng)
    │
    └── Lịch sử Điểm
        ├── Timeline: từng giao dịch +/−
        ├── Filter: Tích / Đổi / Trừ / Hết hạn
        └── Breakdown ca: trip pts + bonus pts
```

---

### 7.2 Màn hình chính — AhaBenefits Homepage

**Components:**
- **Point Balance Card:** Hiển thị to, trung tâm. Số dư AVAILABLE (không tính RESERVED). Badge tier (💎/🥇/🥈).
- **Banner Carousel:** Auto-scroll 3s, tối đa 5 banner, deep link vào catalog category.
- **Progress Bar:** "Cần thêm X pts để đạt R2" — hiển thị cho R3 và R2.
- **Expiry Warning:** Hiển thị nếu balance > 0 và còn ≤ 14 ngày đến cuối quý.

---

### 7.3 Gamification Popup sau chuyến

**Trigger:** Sau mỗi trip auto-complete.

```
┌─────────────────────────────────┐
│  🎉  +21 AhaPoints              │
│  Chuyến vừa hoàn thành          │
│                                 │
│  Tổng ca hôm nay: 87 pts        │
│  Tiến độ bonus ca: ██████░░ 75% │
│                                 │
│  [Xem ví điểm]  [Tiếp tục]      │
└─────────────────────────────────┘
```

**Behavior:**
- Auto-dismiss sau 3 giây nếu không tương tác
- Không hiện nếu driver đang ở màn hình khác (non-intrusive)
- Animation: slide up từ dưới

---

### 7.4 Acceptance Criteria — UI/UX

| # | Criteria | Priority |
|---|---------|---------|
| AC-U1 | Gamification popup sau trip: hiển thị ≤ 2s sau auto-complete | Must Have |
| AC-U2 | Balance sync real-time — không cần refresh thủ công | Must Have |
| AC-U3 | Drop-off tại màn hình voucher detail < 20% | Should Have |
| AC-U4 | QR code trong "Quà của tôi" hoạt động offline (cached) | Must Have |
| AC-U5 | Lịch sử điểm: load ≤ 1.5s, hiển thị 90 ngày gần nhất | Should Have |
| AC-U6 | Expiry countdown hiển thị đúng ngày giờ (timezone HCM/HAN) | Must Have |
| AC-U7 | Catalog filter hoạt động client-side (không gọi API mỗi lần filter) | Nice to Have |

---

## 8. Module 4 — Admin Tool (Ops/CS)

### 8.1 Phân quyền

| Role | Quyền |
|------|-------|
| **Ops Lead** | Cấu hình config (base pts, multiplier, catalog), approve manual adjustment |
| **Ops Member** | Xem báo cáo, không chỉnh config |
| **CS Agent** | Manual adjustment (add/deduct) với lý do, cần Ops Lead approve |
| **Engineering** | Readonly audit log |

---

### 8.2 Config Management

**Points Configuration:**
- Cấu hình `base_divisor` (hiện tại: 5,000)
- Cấu hình `layer_multiplier` theo từng layer (L2–L6)
- Cấu hình `bonus_per_shift` theo layer
- Cấu hình `multiplier theo khung giờ` (peak hour boost — campaign)
- **Audit log mọi thay đổi config:** ai thay đổi, timestamp, giá trị cũ → mới

**Campaign Config:**
- Tạo campaign với: tên, thời gian, điều kiện trigger, điểm thưởng
- Preview tác động (estimated pts budget) trước khi active
- On/Off campaign không ảnh hưởng điểm đã cộng

---

### 8.3 Manual Point Adjustment

```
CS mở ticket → Chọn driver → Nhập adjustment (+ hoặc −) → Nhập lý do
       │
       ▼
[Pending approval]
       │
   ┌───┴─────────────┐
   │ Ops Lead approve │ Reject
   ▼                  ▼
[Credit/Debit áp dụng] [CS nhận thông báo reject + lý do]
[Notification cho driver]
[Log ghi nhận: CS_ticket_id, approver, timestamp]
```

---

### 8.4 Reporting Dashboard (Ops)

| Báo cáo | Nội dung | Frequency |
|---------|---------|-----------|
| Daily Summary | Điểm phát, điểm đổi, active ví, burn rate | Daily |
| Redemption Report | Top items đổi nhiều, drop-off rate, partner fail rate | Weekly |
| Expiry Forecast | Dự báo điểm sắp expire cuối quý | Monthly |
| Fraud Detection | Driver có điểm bất thường (đột biến earned/redeemed) | Real-time alert |

---

### 8.5 Acceptance Criteria — Admin

| # | Criteria | Priority |
|---|---------|---------|
| AC-A1 | Config change có effective_time (không apply ngay) | Must Have |
| AC-A2 | Manual adjustment cần 2-person approval (maker-checker) | Must Have |
| AC-A3 | Audit log immutable — không thể xóa/sửa | Must Have |
| AC-A4 | Daily burn rate hiển thị trên dashboard | Should Have |
| AC-A5 | Alert khi burn rate < 30% sau 2 tuần launch | Should Have |

---

## 9. Notification System

| Trigger | Nội dung | Kênh | Timing |
|---------|---------|------|--------|
| Cuối ca (T+1) | "Ca [tên ca]: +X pts (Y trip + Z bonus)" | Push | Sáng T+1 |
| Đổi thành công | "Đổi [reward] thành công — trừ X pts. Xem QR trong Quà của tôi" | Push + In-app | Ngay |
| Đổi thất bại | "Đổi [reward] thất bại — X pts đã hoàn lại" | Push | Ngay |
| Vi phạm ĐBCL | "Trừ 50 pts do vi phạm chất lượng dịch vụ" | Push + In-app | Ngay |
| Điểm bonus | "Bạn nhận thêm X pts (streak/campaign)" | Push | Ngay |
| Rank thay đổi | "Rank thay đổi: [cũ] → [mới]. Xem quyền lợi mới" | Push + In-app | Sau kỳ xét rank |
| 7 ngày hết quý | "Còn X pts hết hạn ngày [date] — đổi ngay!" | Push | 07:00 |
| 1 ngày hết quý | "Điểm hết hạn ngày mai — X pts còn lại" | Push | 07:00 |
| Reset quý | "Quý mới bắt đầu — bắt đầu tích điểm!" | Push | Ngày đầu quý |
| Deadline bảo hiểm | "Còn X ngày đăng ký bảo hiểm tháng [M+1]" | Push | R1 only, ngày 20–24 |
| Điểm grace period | "Điểm được gia hạn 7 ngày do lỗi đổi thưởng" | Push + In-app | Sau fail |

---

## 10. Open Questions

| # | Câu hỏi | Ảnh hưởng | Owner | Deadline |
|---|---------|-----------|-------|---------|
| 1 | Ngưỡng "online in zone" để nhận bonus ca là bao nhiêu %? | Ảnh hưởng tỷ lệ driver eligible nhận bonus | Product + Ops | Trước design sprint |
| 2 | Layer của đơn overflow xác định bằng origin zone hay assigned zone? | Ảnh hưởng điểm tính cho R1 overflow | Engineering + Ops | Trước dev |
| 3 | Điểm RESERVED có bị expire cuối quý không? | Rule xử lý Scenario A, D | Product | Trước dev |
| 4 | Điểm PENDING trong ca, khi hết quý: credit rồi expire hay expire luôn? | Edge case cuối quý | Product | Trước dev |
| 5 | Driver bị suspend: điểm freeze hay expire? | CS/Policy cần quyết định | CS Lead + Product | Trước launch |
| 6 | Catalog availability theo thành phố (SGN vs HAN) khác nhau không? | Ảnh hưởng partner coverage | Ops + Partnership | Trước Phase 2 |
| 7 | Điều kiện "đủ hoạt động ca" (AR tối thiểu, số chuyến tối thiểu) cụ thể là bao nhiêu? | Cùng câu hỏi #1, cần define cùng lúc | Ops | Trước design sprint |

---

## 11. Timeline & Rollout

### Phase 1 — Q3/2026 (Pilot)
**Mục tiêu:** Validate cơ chế điểm, test partner redemption

| Hạng mục | Timeline | Mô tả |
|---------|---------|-------|
| Design sprint | Tuần 1–2 | Giải quyết Open Questions #1–4, wireframe |
| Engineering | Tuần 3–8 | Backend Points Engine + Admin tool |
| Pilot internal | Tuần 9 | 50 drivers nội bộ + team DM |
| Pilot R1 SGN | Tuần 10–12 | 500 R1 drivers tại TP.HCM |
| **Go/No-go review** | **Cuối Q3** | Đánh giá burn rate, redemption, feedback |

### Phase 2 — Q4/2026 (Full Launch)
**Mục tiêu:** Mở rộng catalog, onboard đối tác chính thức

| Hạng mục | Timeline | Mô tả |
|---------|---------|-------|
| AhaBenefits Store full | Tháng 10 | Catalog đầy đủ, tất cả R1/R2/R3 SGN+HAN |
| Partner agreements | Tháng 10–11 | Xăng, nhớt, F&B, data |
| Insurance R1 | Tháng 11 | Đăng ký bảo hiểm qua app |
| Driver communication | Tháng 10 | Offline event + In-app guide |

### Phase 3 — Q1/2027 (Scale)
**Mục tiêu:** Mở rộng địa lý, tối ưu catalog, EV benefits

| Hạng mục | Timeline | Mô tả |
|---------|---------|-------|
| Mở rộng tỉnh thành | Q1/2027 | Đà Nẵng + 2–3 tỉnh |
| EV Transition Benefits | Q1/2027 | Voucher sạc EV ưu tiên R1 |
| Advanced Analytics | Q1/2027 | Prediction model churn, personalized catalog |

---

## 12. Phụ lục

### A. Giá trị perceived của AhaBenefits với R1 (tháng đủ điều kiện)

| Quyền lợi | Giá trị ước tính |
|-----------|----------------|
| Voucher xăng entitlement | 100,000đ/tháng |
| Điểm tích từ chuyến (est. 1,800 pts × 0.35đ/pt) | ~630,000đ/tháng |
| Bonus hoàn ca (30 pts/ca × 20 ca × 0.35đ) | ~210,000đ/tháng |
| **Tổng perceived value** | **~940,000đ/tháng** |

*Mục tiêu dài hạn: R1 cảm nhận ≥ 1,000,000đ/tháng value từ AhaBenefits.*

### B. Tài liệu liên quan

| File | Mô tả |
|------|-------|
| `2026-05-ahabenefits-proposal.html` | Executive proposal, S-C-R framework, ROI analysis |
| `2026-05-ahabenefits-points-flow.md` | Points flow chi tiết (nguồn gốc tài liệu này) |
| `2026-05-driver-ranking-params.md` | Ranking parameters, Layer definitions |
| `2026-06-driver-journey-milestones.md` | Driver journey milestones tích hợp AhaPoints |
| `2026-06-global-driver-lifecycle-benchmark.md` | Benchmark 15 nền tảng giao hàng toàn cầu |
| `2026-06-AhaBenefits-tech-requests.md` | Tech requests table gửi Engineering |

---

*PRD v1.0 | Driver Management → Product | 2026-06-23*  
*Cập nhật tiếp theo: Sau Design Sprint, khi Open Questions #1–4 được giải quyết*
