# AhaBenefits v2.0 — Points Flow & Product Requirements
> Dành cho Product team. Bao gồm: earning flow, timeline, redemption, cộng/trừ điểm, và các kịch bản edge case.
> Tham chiếu params: `2026-05-driver-ranking-params.md`

---

## 1. Tổng quan Vòng đời Điểm (Point Lifecycle)

```text
[Trip hoàn thành]
       │
       ▼
[Tính điểm chuyến]──────────────────────────────────────────┐
 income ÷ 5.000 × layer multiplier                          │
       │                                                     │
       ▼                                                     │
[Điểm trạng thái: PENDING]                                  │
 Giữ tạm, chưa dùng được                                    │
       │                                                     │
  [Cuối ca]                                                  │
       │                                                     │
       ▼                                                     │
[Hoàn thành ca? ────Yes──→ +Bonus hoàn ca]                  │
       │ No                                                  │
       │ (không bonus)                                       │
       ▼                                                     │
[Điểm trạng thái: AVAILABLE] ◄───────────────────────────── ┘
 Có thể đổi thưởng                                          │
       │                                                     │
  ┌────┴────┐                                                │
  │         │                                                │
[Đổi]   [Vi phạm]                                           │
  │         │                                                │
  ▼         ▼                                                │
[RESERVED] [DEDUCTED -50 pts]                               │
  │                                                          │
[Partner xác nhận]                                          │
  │                                                          │
  ▼                                                          │
[REDEEMED] ─────── Cuối Quý ──────────────► [EXPIRED]
```

---

## 2. Earning Flow — Tích điểm từng chuyến

### 2.1 Công thức & Trigger

| Bước | Sự kiện | Hành động hệ thống |
| --- | --- | --- |
| 1 | Chuyến hoàn thành (auto-complete) | Ghi nhận `trip_GSV` (VND) |
| 2 | Xác định `layer` của đơn hàng (L2–L6) | Lấy `layer_multiplier` từ config |
| 3 | Kiểm tra driver có thuộc priority layer không | Nếu overflow → multiplier = ×1.0, no bonus |
| 4 | Tính `raw_pts = trip_GSV ÷ 5.000` | Giá trị thập phân |
| 5 | Làm tròn: `base_pts = round(raw_pts)` | ≥ 0.5 → làm tròn lên, < 0.5 → làm tròn xuống |
| 6 | Tính `earned_pts = round(base_pts × layer_multiplier)` | Làm tròn sau khi nhân hệ số |
| 7 | Cộng vào `shift_trip_pts` (tạm tính trong ca) | Trạng thái PENDING — chưa credit vào ví |
| 8 | Cập nhật `shift_gsv_total` | Dùng để xét điều kiện bonus hoàn ca |

> **Ví dụ làm tròn:** GSV 14.000đ → 14.000 ÷ 5.000 = 2.8 → **3 pts** · GSV 12.000đ → 12.000 ÷ 5.000 = 2.4 → **2 pts**

> **Lưu ý:** Điểm tính theo **đơn hàng** (dùng GSV của đơn), không theo rank tài xế. R1 nhận đơn overflow từ L3 → multiplier = ×1.3 (hệ số L3), không phải ×1.5.

### 2.2 Bonus hoàn ca

> Không có cơ chế checkout ca. Điều kiện bonus xét dựa trên **online hour in zone** và hoạt động thực tế trong ca.

| Điều kiện | Mô tả | Kết quả |
| --- | --- | --- |
| ✅ Đủ online in zone | Online trong zone đăng ký ≥ ngưỡng tối thiểu của ca ([?] % thời lượng ca — cần Product định nghĩa) | Đủ điều kiện nhận bonus |
| ✅ Đủ điều kiện hoạt động ca | AR, số chuyến hoàn thành tối thiểu trong ca ([?] — cần Product định nghĩa) | Kết hợp với điều kiện trên |
| ❌ Online in zone không đủ | Driver online nhưng ở ngoài zone, hoặc tắt app quá lâu | Không có bonus, điểm chuyến vẫn giữ |
| ❌ Ca bị hủy do hệ thống | Force-close ca | Không có bonus, điểm chuyến vẫn giữ |

> **⚠️ Open question cho Product:** Ngưỡng "online in zone" cụ thể là bao nhiêu % thời lượng ca? Đề xuất: ≥ 80% tổng thời gian ca.

### 2.3 Credit điểm vào ví — T+1

```text
Thời điểm credit: Ngày hôm sau (T+1), sau khi hệ thống validate dữ liệu ca

Flow:
  [Kết thúc ca / 23:59 ngày hôm đó]
         │
         ▼
  [Hệ thống batch job chạy (VD: 02:00–04:00 sáng)]
  Validate: online_hour_in_zone + điều kiện hoạt động ca
         │
    ┌────┴────────────────────┐
    │ Đủ điều kiện            │ Không đủ
    ▼                         ▼
  shift_trip_pts              shift_trip_pts
  + bonus_pts                 (không có bonus)
    │                         │
    └──────────┬──────────────┘
               ▼
  [Credit vào ví — PENDING → AVAILABLE]
  [Push notification T+1 sáng:
   "Ca [tên ca] hôm qua — bạn nhận X pts
    (Trong đó: Y pts trip + Z pts bonus ca)"]
```

> Dữ liệu online hour cần được finalize sau khi ca kết thúc → credit T+1 đảm bảo chính xác, tránh sai lệch do data lag.

---

## 3. Point Timeline — Mốc thời gian quan trọng

```text
THÁNG
────────────────────────────────────────────────────────────────────
Ngày 01   │ Voucher xăng/EV rank entitlement được phát tự động (R1, R2)
          │ Coverage bảo hiểm có hiệu lực (nếu đã đăng ký tháng trước)
          │
Ngày 01–24│ Cửa sổ hoạt động bình thường: tích điểm, đổi điểm
          │
Ngày 25   │ ⚠️  DEADLINE đăng ký / huỷ bảo hiểm tai nạn R1
          │     (coverage áp dụng từ ngày 01 tháng sau)
          │
Ngày 26–31│ Tích điểm / đổi điểm bình thường
          │
CUỐI QUÝ (31/3 · 30/6 · 30/9 · 31/12)
────────────────────────────────────────────────────────────────────
23:59     │ ⚠️  ĐIỂM HẾT HẠN — toàn bộ điểm AVAILABLE bị expire
          │     Điểm đang RESERVED (đổi đang xử lý) → giữ nguyên
          │     Điểm đang PENDING (trong ca) → credit rồi expire
          │
Ngày đầu  │ Balance reset về 0. Bắt đầu quý mới.
Quý mới   │ Push notification: "Quý mới bắt đầu — điểm đã reset"
```

---

## 4. Redemption Flow — Đổi điểm

### 4.1 Happy path

```text
Driver mở tab AhaBenefits
       │
       ▼
[Hiển thị catalog theo Rank]
 R3: tier Bạc  │  R2: tier Vàng  │  R1: tier Kim Cương
 (kế thừa theo thứ tự)
       │
       ▼
[Driver chọn reward]
       │
       ▼
[Hệ thống kiểm tra]
 ├── balance ≥ điểm yêu cầu?  → No → Hiện "Chưa đủ điểm, cần thêm X pts"
 ├── rank đủ điều kiện?        → No → Hiện "Cần đạt [rank] để đổi"
 └── reward còn hàng/slot?     → No → Hiện "Tạm hết — thử lại sau"
       │ All pass
       ▼
[Điểm chuyển sang RESERVED]
[Màn hình xác nhận: tóm tắt reward + điểm sẽ trừ]
       │
       ▼
[Driver xác nhận]
       │
       ▼
[Hệ thống gửi yêu cầu đến Partner API]
       │
  ┌────┴────────────┐
  │ Partner confirm  │ Partner timeout/fail
  │ (≤ 30 giây)     │ (> 30 giây)
  ▼                 ▼
[REDEEMED]      [AVAILABLE — hoàn điểm]
[Gửi voucher/   [Thông báo: "Đổi thất bại,
 mã giảm giá]    điểm đã được hoàn lại"]
[Push notif]
```

### 4.2 Bảo hiểm tai nạn R1 (special flow)

```text
Trước ngày 25 hàng tháng:

Driver vào mục "Bảo hiểm R1"
       │
       ▼
[Chọn gói: 10k (285 pts) hoặc 30k (857 pts)]
       │
       ▼
[Xác nhận: "Coverage sẽ có hiệu lực từ 01/[tháng+1]"]
       │
       ▼
[Điểm RESERVED ngay]
       │
       ▼
[Ngày 01 tháng sau → điểm REDEEMED, coverage kích hoạt]
[Hệ thống gửi số hợp đồng bảo hiểm qua app/SMS]

Huỷ (trước ngày 25):
  → Điểm RESERVED → AVAILABLE (hoàn lại)
  → Coverage ngừng cuối tháng hiện tại

Mất R1 mid-month:
  → Không cho đăng ký mới
  → Nếu đã RESERVED: giữ reservation đến hết tháng đã đăng ký
```

---

## 5. Cộng / Trừ điểm — Adjustment System

### 5.1 Các sự kiện trừ điểm

| Sự kiện | Điểm trừ | Thời điểm | Ghi chú |
| --- | --- | --- | --- |
| Vi phạm ĐBCL (Đảm bảo Chất lượng) | -50 pts | Ngay khi xác nhận vi phạm | Ghi log lý do |
| Gian lận / báo cáo giả | -50 pts/lần + review rank | Sau xác minh | CS xử lý thủ công |
| Huỷ chuyến không lý do | Không trừ điểm | — | Ảnh hưởng DCR → ảnh hưởng rank |

### 5.2 Các sự kiện cộng điểm bonus

| Sự kiện | Điểm thưởng | Trigger |
| --- | --- | --- |
| Hoàn thành ca đúng giờ | Theo layer (20–30 pts) | Cuối ca |
| Streak 7 ngày liên tục | [TBD] pts | Auto detect |
| Campaign đặc biệt (Mega Sales) | [TBD] pts | Campaign config |

### 5.3 Adjustment thủ công (CS/Ops)

```text
Chỉ CS/Ops có quyền → qua Admin tool
  ├── Add points: cần lý do + approval cấp trên
  ├── Deduct points: cần lý do + notification cho driver
  └── Ghi log đầy đủ: ai làm, lúc nào, lý do gì
```

---

## 6. Kịch bản Edge Case

### Scenario A — Driver đổi điểm cuối quý

```text
Driver R2, balance 1.800 pts, ngày 29/6

Đổi Voucher F&B 50k (1.400 pts) → RESERVED
  ├── Partner confirm trước 30/6 23:59 → REDEEMED ✅
  └── Partner timeout, sau 30/6 00:00 → Điểm expire trước khi hoàn
        → Rule: RESERVED pts không expire, hoàn về sau khi fail
        → Balance = 0 (1.800 - 1.400 đã expire) + 1.400 hoàn = 1.400
        → [⚠️ Edge case cần Product quyết định: hoàn về quý mới hay expire?]
        → Đề xuất: RESERVED pts được bảo vệ khỏi expire 7 ngày
```

### Scenario B — Driver bị downgrade rank

```text
R2 → R3 (sau kỳ xét rank cuối tháng)

Tháng đó: earned 2.046 pts, balance 2.046
  ├── Điểm giữ nguyên, không mất
  ├── Catalog access: xuống tier Bạc (mất quyền đổi R2+ items)
  ├── Items đang RESERVED: giữ, hoàn thành bình thường
  └── Voucher xăng tháng sau: không nhận (đã mất R2)
      [Notification: "Rank của bạn đã thay đổi, một số rewards sẽ không khả dụng"]
```

### Scenario C — Driver R1 nhận đơn overflow

```text
R1 đang online, L2 đầy (≥80% fill) → hệ thống cascade → giao đơn từ L2 ra L3

Trip income: 70.000đ
  ├── Layer của đơn: L2 (đơn xuất phát từ L2)
  ├── Driver là R1 nhưng đang nhận overflow
  └── Điểm = floor(70.000 ÷ 5.000) × 1.0 = 14 pts (×1.0, no bonus)
      [Không phải ×1.5 vì đơn overflow]

[⚠️ Cần Product confirm: layer của đơn xác định bằng origin zone hay assigned zone?]
```

### Scenario D — Đổi điểm thất bại, sắp hết quý

```text
Driver đổi ngày 30/12, partner fail → điểm hoàn về ngày 31/12 23:58
  → 2 phút sau: điểm expire cuối quý

Rule đề xuất: Nếu redemption fail trong vòng 48h cuối quý
  → Điểm hoàn về nhưng được gia hạn 7 ngày sang quý mới
  → Gửi notification: "Điểm được gia hạn thêm 7 ngày do lỗi đổi thưởng"
```

### Scenario E — Driver tích điểm trên cùng 1 ca có cả đơn trong layer và overflow

```text
Ca Sáng R2/L3: 5 đơn trong L3 + 2 đơn overflow từ L2

5 đơn L3:  mỗi đơn ~52.000đ → 10 base pts × 1.3 = 13 pts/đơn × 5 = 65 pts
2 đơn OFW: mỗi đơn ~60.000đ → 12 base pts × 1.0 = 12 pts/đơn × 2 = 24 pts
Bonus hoàn ca (L3): +25 pts
─────────────────────────────────────────────────────
Tổng ca: 65 + 24 + 25 = 114 pts

[Hiển thị chi tiết trong app: breakdown by trip type]
```

---

## 7. Data Model gợi ý (cho Engineering)

```text
PointTransaction
  ├── id
  ├── driver_id
  ├── amount (+ hoặc -)
  ├── type: EARNED | BONUS | REDEEMED | DEDUCTED | EXPIRED | REFUNDED | ADJUSTED
  ├── status: PENDING | AVAILABLE | RESERVED | FINAL
  ├── source_ref: trip_id | shift_id | campaign_id | cs_ticket_id
  ├── layer: L2–L6 | OVERFLOW
  ├── multiplier_applied: 1.0–1.5
  ├── created_at
  ├── expires_at (cuối quý)
  └── note (cho ADJUSTED)

DriverPointWallet
  ├── driver_id
  ├── available_balance
  ├── reserved_balance
  ├── total_earned_current_quarter
  ├── quarter_expires_at
  └── last_updated_at
```

---

## 8. Notifications cần thiết

| Trigger | Nội dung | Kênh |
| --- | --- | --- |
| Cuối ca | "Bạn vừa nhận X pts — Tổng: Y pts" | Push |
| Đổi thành công | "Đổi [reward] thành công — trừ X pts" | Push + In-app |
| Đổi thất bại | "Đổi thất bại — X pts đã hoàn lại" | Push |
| Vi phạm ĐBCL | "Trừ 50 pts do vi phạm chất lượng" | Push + In-app |
| 7 ngày trước hết quý | "Còn X pts sẽ hết hạn ngày [date] — đổi ngay!" | Push |
| 1 ngày trước hết quý | "Điểm hết hạn ngày mai — X pts còn lại" | Push |
| Sau reset | "Quý mới bắt đầu — tích điểm để đổi thưởng!" | Push |
| Trước ngày 25 | "Còn [X ngày] để đăng ký bảo hiểm tháng [M+1]" | Push (R1 only) |
| Rank thay đổi | "Rank của bạn thay đổi — xem quyền lợi mới" | Push + In-app |

---

## 9. Open Questions cho Product

| # | Câu hỏi | Ảnh hưởng |
| --- | --- | --- |
| 1 | RESERVED pts có bị expire cuối quý không? | Scenario A — cần rule rõ |
| 2 | Layer của đơn overflow xác định bằng origin zone hay assigned zone? | Scenario C — ảnh hưởng pts tính |
| 3 | Điểm PENDING (trong ca) hết quý thì xử lý thế nào? | End-of-quarter edge case |
| 4 | Có cho phép transfer/gift điểm giữa drivers không? | Scope v2.0 hay v3? |
| 5 | Driver bị suspend: điểm freeze hay expire? | CS/policy cần quyết định |
| 6 | Có cần points history export (thuế/báo cáo)? | Compliance |
| 7 | Catalog availability theo thành phố (SGN vs HAN) có khác không? | Partner coverage |

---

*Cập nhật: 2026-05-27 | Driver Management → Product handoff*
