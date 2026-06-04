/**
 * AHAMOVE — Tạo Form Đăng Ký Áo Đồng Phục Đợt 1/2026
 * Hướng dẫn: script.google.com → New project → Paste → Run createAhamoveForm → Authorize → Done
 */
function createAhamoveForm() {

  // ── Tạo form ──────────────────────────────────────────────────────────────
  var form = FormApp.create('[AHAMOVE] Đăng ký mua Áo Đồng Phục Chuyên Gia Giao Hàng — Đợt 1/2026');

  form.setDescription(
    'Ahamove ra mắt đồng phục mới dành riêng cho tài xế — chỉ 800 áo, không sản xuất thêm lần 2.\n\n' +
    'Điền form để đăng ký slot. Kết quả được thông báo ngày 27/05/2026.\n\n' +
    '⚠️ Ưu tiên phân bổ dựa trên hiệu suất vận hành (AR/FR) trong 30 ngày gần nhất.'
  );

  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(
    '✅ Đăng ký thành công!\n\n' +
    'Team DM sẽ thông báo kết quả qua Zalo/SMS vào ngày 27/05/2026.\n\n' +
    'Cảm ơn anh/chị đã tham gia! 🧡'
  );

  // ── Q1: Họ và Tên ─────────────────────────────────────────────────────────
  form.addTextItem()
    .setTitle('Họ và Tên')
    .setHelpText('Nhập họ tên đầy đủ')
    .setRequired(true);

  // ── Q2: Mã tài xế ─────────────────────────────────────────────────────────
  form.addTextItem()
    .setTitle('Mã tài xế (Driver ID)')
    .setHelpText('VD: AHM-123456 — Dùng để xác nhận thông tin vận hành nội bộ')
    .setRequired(true);

  // ── Q3: Số điện thoại ─────────────────────────────────────────────────────
  form.addTextItem()
    .setTitle('Số điện thoại')
    .setHelpText('VD: 0901234567 — Để gửi kết quả qua Zalo/SMS')
    .setRequired(true);

  // ── Q4: Size áo ───────────────────────────────────────────────────────────
  form.addMultipleChoiceItem()
    .setTitle('Size áo')
    .setChoiceValues(['S', 'M', 'L', 'XL', 'XXL'])
    .setRequired(true);

  // ── Q5: Khu vực ───────────────────────────────────────────────────────────
  form.addListItem()
    .setTitle('Khu vực hoạt động chính')
    .setChoiceValues(['TP.HCM', 'Hà Nội', 'Đà Nẵng', 'Tỉnh/Thành phố khác'])
    .setRequired(true);

  // ── Q6: MiniHub ───────────────────────────────────────────────────────────
  form.addTextItem()
    .setTitle('MiniHub gần nhất (điểm nhận áo)')
    .setHelpText('VD: MiniHub Bình Thạnh — Khuyến khích điền để team sắp xếp trước')
    .setRequired(false);

  // ── Q7: Xác nhận điều kiện ────────────────────────────────────────────────
  var confirmItem = form.addCheckboxItem();
  confirmItem
    .setTitle('Xác nhận điều kiện tham gia')
    .setChoices([
      confirmItem.createChoice(
        'Tôi hiểu rằng: (1) slot ưu tiên theo AR/FR; ' +
        '(2) kết quả cuối cùng do Ahamove quyết định; ' +
        '(3) áo nhận tại MiniHub với giá 120,000đ.'
      )
    ])
    .setRequired(true);

  // ── In link ra log ────────────────────────────────────────────────────────
  var publishedUrl = form.getPublishedUrl();
  var editUrl      = form.getEditUrl();

  Logger.log('✅ Form đã tạo thành công!');
  Logger.log('🔗 Link gửi tài xế : ' + publishedUrl);
  Logger.log('✏️  Link chỉnh sửa  : ' + editUrl);

  // Hiện popup kết quả
  var ui = SpreadsheetApp.getUi ? SpreadsheetApp.getUi() : null;
  if (!ui) {
    // Chạy từ Apps Script editor — xem link trong View > Logs
    console.log('Link form: ' + publishedUrl);
  }
}
