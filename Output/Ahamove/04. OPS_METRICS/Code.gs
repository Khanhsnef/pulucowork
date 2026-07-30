/**
 * GOOGLE APPS SCRIPT BACKEND — 3-GATE APPROVAL WORKFLOW + RBAC + SLA
 * Spreadsheet Target ID: 1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4
 *
 * State machine:
 *   Tạo tag mới : PENDING_TEAM_LEAD -> PENDING_DM -> PENDING_QM -> DONE
 *   Add tag     : PENDING_TEAM_LEAD -> PENDING_QM -> DONE  (bỏ qua DM)
 *   Reject bất kỳ gate -> REJECTED (về requester để sửa & re-submit)
 */

/* ============================================================
 *  RBAC — PHÂN QUYỀN (hardcode theo email)
 *  >>> KHANH ĐIỀN EMAIL THẬT VÀO ĐÂY <<<
 *  Vai trò: TEAM_LEAD | DM | QM | REQUESTER (mặc định)
 * ============================================================ */
const ROLE_MAP = {
  // --- DM Lead ---
  'khanh@ahamove.com'   : 'DM',
  // --- Team Leads / Heads ---
  'lead1@ahamove.com'   : 'TEAM_LEAD',
  'lead2@ahamove.com'   : 'TEAM_LEAD',
  // --- QM Specialists ---
  'qm1@ahamove.com'     : 'QM',
  'qm2@ahamove.com'     : 'QM'
};
const DOMAIN_DEFAULT_ROLE = 'REQUESTER'; // mọi user hợp lệ khác = requester

/* ============================================================
 *  TEAM ↔ LEAD — mỗi Team có 1 Lead/Head phụ trách
 *  Lead CHỈ duyệt được request của team mình. DM override tất cả.
 *  >>> KHANH: (1) sửa TÊN TEAM cho khớp TEAM_LIST ở 00_CONFIG_SETTINGS
 *             (2) điền EMAIL lead/head phụ trách từng team.
 *  1 lead có thể nắm nhiều team (trỏ nhiều team về cùng 1 email).
 * ============================================================ */
const TEAM_LEAD_MAP = {
  'Business Operations'      : 'lead1@ahamove.com',   // >>> ĐIỀN EMAIL LEAD <<<
  'Marketing Campaign'       : 'lead1@ahamove.com',   // >>> ĐIỀN EMAIL LEAD <<<
  'Hub Linehaul Operations'  : 'lead2@ahamove.com',   // >>> ĐIỀN EMAIL LEAD <<<
  'Customer Service (CS)'    : 'lead2@ahamove.com',   // >>> ĐIỀN EMAIL LEAD <<<
  'Risk & Fraud Control'     : 'lead2@ahamove.com',   // >>> ĐIỀN EMAIL LEAD <<<
  'Fleet Operations'         : 'lead1@ahamove.com'    // >>> ĐIỀN EMAIL LEAD <<<
};

// Lead `email` có được duyệt request của `team` không? DM luôn = true.
function canLeadApproveTeam(email, team, role) {
  if (role === 'DM') return true;                       // DM override mọi team
  if (role !== 'TEAM_LEAD') return false;
  return (TEAM_LEAD_MAP[team] || '').toLowerCase() === (email || '').toLowerCase();
}

function getUserEmail() {
  try { return (Session.getActiveUser().getEmail() || '').toLowerCase(); }
  catch (e) { return ''; }
}

function getUserRole() {
  const email = getUserEmail();
  if (email && ROLE_MAP[email]) return ROLE_MAP[email];
  return DOMAIN_DEFAULT_ROLE;
}

/* ============================================================
 *  ENTRY POINT
 * ============================================================ */
function doGet(e) {
  const template = HtmlService.createTemplateFromFile("Index");
  template.config = getAppConfig();
  template.userEmail = getUserEmail();
  template.userRole = getUserRole();
  return template.evaluate()
    .setTitle(template.config.APP_TITLE || "Tag Request Portal")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/* ============================================================
 *  CONFIG
 * ============================================================ */
function getAppConfig() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("00_CONFIG_SETTINGS");
  if (!sheet) {
    sheet = ss.insertSheet("00_CONFIG_SETTINGS", 0);
    sheet.appendRow(["Mã Cấu Hình (Key)", "Nội Dung Hiển Thị (Value)", "Hướng Dẫn"]);
    sheet.appendRow(["APP_TITLE", "Tag Request Portal", "Tiêu đề ứng dụng"]);
    sheet.appendRow(["APP_SUBTITLE", "Spreadsheet Target:", "Dòng phụ dưới tiêu đề"]);
    sheet.appendRow(["SHEET_LINK_TEXT", "Google Sheet Target", "Chữ hiển thị của link sheet"]);
    sheet.appendRow(["FORM_TITLE", "Biểu Mẫu Tạo Yêu Cầu Tag Tài Xế Cho Phía DM", "Tiêu đề biểu mẫu tạo request"]);
    sheet.appendRow(["TAB1_NAME", "📝 Bước 1: Request", "Tên Tab 1"]);
    sheet.appendRow(["TAB2_NAME", "👔 Bước 2: Lead Approval", "Tên Tab 2 (Lead duyệt)"]);
    sheet.appendRow(["TAB3_NAME", "🛡️ Bước 3: DM Review", "Tên Tab 3"]);
    sheet.appendRow(["TAB4_NAME", "⚙️ Bước 4: QM Add Tags", "Tên Tab 4"]);
    sheet.appendRow(["TAB5_NAME", "📊 Master Request Tracker", "Tên Tab 5"]);
    sheet.appendRow(["SUBMIT_BTN_TEXT", "🚀 Gửi Đề Xuất Tới Lead Duyệt", "Tên nút gửi"]);
    sheet.appendRow(["TEAM_LIST", "Business Operations, Marketing Campaign, Hub Linehaul Operations, Customer Service (CS), Risk & Fraud Control, Fleet Operations", "Danh sách Team"]);
    sheet.appendRow(["TAG_TYPES", "Priority Dispatch (Ưu tiên phát đơn), Incentive Campaign (Thưởng/Thách thức), Area Restriction (Giới hạn khu vực), Special Training (Đào tạo dịch vụ VIP), Penalty / Block (Khóa/Tạm dừng)", "Danh sách loại Tag"]);
    sheet.appendRow(["SLA_LEAD_HOURS", "4", "SLA giờ chờ Lead duyệt (Gate 1)"]);
    sheet.appendRow(["SLA_DM_HOURS", "8", "SLA giờ chờ DM review (Gate 2)"]);
    sheet.appendRow(["SLA_QM_HOURS", "24", "SLA giờ chờ QM add tag (Gate 3)"]);
  }

  const rows = sheet.getDataRange().getValues();
  const config = {};
  for (let i = 1; i < rows.length; i++) {
    const key = rows[i][0];
    const val = rows[i][1];
    if (key) config[key] = val;
  }
  // Bổ sung key mới nếu sheet cũ chưa có (không ghi đè giá trị đã chỉnh)
  const defaults = {
    TAB2_NAME: "👔 Bước 2: Lead Approval",
    TAB3_NAME: "🛡️ Bước 3: DM Review",
    TAB4_NAME: "⚙️ Bước 4: QM Add Tags",
    TAB5_NAME: "📊 Master Request Tracker",
    SLA_LEAD_HOURS: "4", SLA_DM_HOURS: "8", SLA_QM_HOURS: "24"
  };
  for (const k in defaults) { if (!config[k]) config[k] = defaults[k]; }
  return config;
}

function saveAppConfig(newConfig) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("00_CONFIG_SETTINGS");
  if (!sheet) {
    getAppConfig();
    sheet = ss.getSheetByName("00_CONFIG_SETTINGS");
  }

  const rows = sheet.getDataRange().getValues();
  for (const key in newConfig) {
    let found = false;
    for (let i = 1; i < rows.length; i++) {
      if (rows[i][0] === key) {
        sheet.getRange(i + 1, 2).setValue(newConfig[key]);
        found = true;
        break;
      }
    }
    if (!found) {
      sheet.appendRow([key, newConfig[key], "Tùy chỉnh từ Live UI Editor"]);
    }
  }
  return { status: "success" };
}

/* ============================================================
 *  SHEET SETUP & HELPERS
 * ============================================================ */
// 23 cột gốc + 8 cột mới (append cuối để không vỡ data cũ)
const BASE_HEADERS = ["Mã Request", "Ngày Tạo", "Hình Thức", "Team Đề Xuất", "Người Đề Xuất", "Loại Tag", "Tên Tag Yêu Cầu", "Nguồn Danh Sách TX", "Số Lượng TX", "Lý Do", "Thời Gian", "DM Reviewer", "Ngày DM Review", "DM Quyết Định", "DM Note", "DM Tag Code", "QM Handover", "QM Specialist", "Ngày QM Nhận", "QM Trạng Thái Add Tag", "Ngày Add Tag Xong", "Số TX Add Thành Công", "Ghi Chú QM"];
const NEW_HEADERS = ["Lead Approver", "Ngày Lead Duyệt", "Lead Quyết Định", "Lead Note", "Trạng Thái Tổng", "Deadline Lead", "Deadline DM", "Deadline QM", "Cờ Quá Hạn"];
// Cột (1-based) — vị trí cột mới bắt đầu từ 24
const COL = {
  ID: 1, DATE: 2, CATEGORY: 3, TEAM: 4, NAME: 5, TYPE: 6, TAGNAME: 7,
  SRC: 8, COUNT: 9, REASON: 10, DURATION: 11,
  DM_REVIEWER: 12, DM_DATE: 13, DM_DECISION: 14, DM_NOTE: 15, DM_TAGCODE: 16, QM_HANDOVER: 17,
  QM_SPECIALIST: 18, QM_DATE: 19, QM_STATUS: 20, QM_DONE_DATE: 21, QM_SUCCESS: 22, QM_NOTE: 23,
  LEAD_APPROVER: 24, LEAD_DATE: 25, LEAD_DECISION: 26, LEAD_NOTE: 27,
  STATE: 28, DL_LEAD: 29, DL_DM: 30, DL_QM: 31, BREACH: 32
};

function getMainSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("01_ALL_TAG_REQUESTS");
  if (!sheet) {
    sheet = ss.insertSheet("01_ALL_TAG_REQUESTS");
    sheet.appendRow(BASE_HEADERS.concat(NEW_HEADERS));
    return sheet;
  }
  // Migrate: nếu sheet cũ chỉ có 23 cột -> thêm header cột mới
  const lastCol = sheet.getLastColumn();
  if (lastCol < BASE_HEADERS.length + NEW_HEADERS.length) {
    const startCol = lastCol + 1;
    const missing = (BASE_HEADERS.concat(NEW_HEADERS)).slice(lastCol);
    if (missing.length > 0) {
      sheet.getRange(1, startCol, 1, missing.length).setValues([missing]);
    }
  }
  return sheet;
}

function addHours(date, hours) {
  return new Date(date.getTime() + hours * 3600 * 1000);
}
function fmt(date) {
  return Utilities.formatDate(date, "GMT+7", "yyyy-MM-dd HH:mm");
}
function slaHours(config, key, fallback) {
  const v = parseFloat(config[key]);
  return isNaN(v) ? fallback : v;
}

/* ============================================================
 *  READ
 * ============================================================ */
function getSheetDataJson() {
  const sheet = getMainSheet();
  const rows = sheet.getDataRange().getValues();
  if (rows.length <= 1) return { role: getUserRole(), email: getUserEmail(), data: [] };

  const cleanData = [];
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (r[0] && r[0].toString().startsWith("REQ-")) {
      cleanData.push({
        id: r[COL.ID-1], date: r[COL.DATE-1], requestCategory: r[COL.CATEGORY-1] || 'Tạo tag mới',
        team: r[COL.TEAM-1], name: r[COL.NAME-1], type: r[COL.TYPE-1], tagName: r[COL.TAGNAME-1],
        driverListSource: r[COL.SRC-1] || '-', count: r[COL.COUNT-1], reason: r[COL.REASON-1], duration: r[COL.DURATION-1],
        leadApprover: r[COL.LEAD_APPROVER-1] || '-', leadDate: r[COL.LEAD_DATE-1] || '-',
        leadDecision: r[COL.LEAD_DECISION-1] || 'PENDING', leadNote: r[COL.LEAD_NOTE-1] || '',
        dmReviewer: r[COL.DM_REVIEWER-1] || '-', dmReviewDate: r[COL.DM_DATE-1] || '-',
        dmDecision: r[COL.DM_DECISION-1] || 'PENDING', dmNote: r[COL.DM_NOTE-1] || '', dmTagCode: r[COL.DM_TAGCODE-1] || '-',
        qmHandover: r[COL.QM_HANDOVER-1] || 'HOLD', qmStatus: r[COL.QM_STATUS-1] || 'PENDING_QM',
        qmSpecialist: r[COL.QM_SPECIALIST-1] || '-',
        qmSuccessCount: r[COL.QM_SUCCESS-1] || 0, qmRef: r[COL.QM_NOTE-1] || '',
        state: r[COL.STATE-1] || 'PENDING_TEAM_LEAD',
        deadlineLead: r[COL.DL_LEAD-1] ? fmtCell(r[COL.DL_LEAD-1]) : '',
        deadlineDM: r[COL.DL_DM-1] ? fmtCell(r[COL.DL_DM-1]) : '',
        deadlineQM: r[COL.DL_QM-1] ? fmtCell(r[COL.DL_QM-1]) : '',
        breach: r[COL.BREACH-1] || ''
      });
    }
  }
  return { role: getUserRole(), email: getUserEmail(), data: cleanData };
}

function fmtCell(v) {
  if (v instanceof Date) return fmt(v);
  return v.toString();
}

/* ============================================================
 *  CREATE — mọi request mới bắt đầu ở PENDING_TEAM_LEAD
 * ============================================================ */
function saveNewRequest(data) {
  const sheet = getMainSheet();
  const config = getAppConfig();
  const now = new Date();
  const dlLead = addHours(now, slaHours(config, 'SLA_LEAD_HOURS', 4));

  const row = new Array(BASE_HEADERS.length + NEW_HEADERS.length).fill("");
  row[COL.ID-1] = data.id;
  row[COL.DATE-1] = data.date;
  row[COL.CATEGORY-1] = data.requestCategory;
  row[COL.TEAM-1] = data.team;
  row[COL.NAME-1] = data.name;
  row[COL.TYPE-1] = data.type;
  row[COL.TAGNAME-1] = data.tagName;
  row[COL.SRC-1] = data.driverListSource || '-';
  row[COL.COUNT-1] = data.count || 0;
  row[COL.REASON-1] = data.reason;
  row[COL.DURATION-1] = data.duration;
  // Các gate sau chưa xử lý
  row[COL.DM_REVIEWER-1] = '-'; row[COL.DM_DATE-1] = '-';
  row[COL.DM_DECISION-1] = 'PENDING'; row[COL.DM_NOTE-1] = 'Chờ Lead duyệt trước'; row[COL.DM_TAGCODE-1] = '-';
  row[COL.QM_HANDOVER-1] = 'HOLD';
  row[COL.QM_SPECIALIST-1] = '-'; row[COL.QM_DATE-1] = '-'; row[COL.QM_STATUS-1] = 'HOLD';
  row[COL.QM_DONE_DATE-1] = '-'; row[COL.QM_SUCCESS-1] = 0; row[COL.QM_NOTE-1] = 'Chờ Lead duyệt';
  // Gate 1 - Lead
  row[COL.LEAD_APPROVER-1] = '-'; row[COL.LEAD_DATE-1] = '-';
  row[COL.LEAD_DECISION-1] = 'PENDING'; row[COL.LEAD_NOTE-1] = '';
  row[COL.STATE-1] = 'PENDING_TEAM_LEAD';
  row[COL.DL_LEAD-1] = fmt(dlLead);
  row[COL.DL_DM-1] = ''; row[COL.DL_QM-1] = '';
  row[COL.BREACH-1] = '';

  sheet.appendRow(row);
  return { status: "success" };
}

/* ============================================================
 *  GATE 1 — LEAD APPROVAL
 * ============================================================ */
function saveLeadApproval(reqId, decision, note) {
  const role = getUserRole();
  if (role !== 'TEAM_LEAD' && role !== 'DM') {
    return { status: "error", message: "Bạn không có quyền duyệt ở bước Lead." };
  }
  const sheet = getMainSheet();
  const config = getAppConfig();
  const rows = sheet.getDataRange().getValues();
  const now = new Date();

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][COL.ID-1] === reqId) {
      const rowIdx = i + 1;
      const state = rows[i][COL.STATE-1];
      if (state !== 'PENDING_TEAM_LEAD') {
        return { status: "error", message: "Request không ở trạng thái chờ Lead duyệt." };
      }
      // RBAC theo team: Lead chỉ duyệt request của team mình; DM override tất cả.
      const reqTeam = rows[i][COL.TEAM-1];
      if (!canLeadApproveTeam(getUserEmail(), reqTeam, role)) {
        return { status: "error", message: "Bạn không phụ trách team \"" + reqTeam + "\". Chỉ Lead của team này (hoặc DM) mới được duyệt." };
      }
      const isAddTag = (rows[i][COL.CATEGORY-1] === 'Add tag');

      sheet.getRange(rowIdx, COL.LEAD_APPROVER).setValue(getUserEmail() || 'Team Lead');
      sheet.getRange(rowIdx, COL.LEAD_DATE).setValue(fmt(now));
      sheet.getRange(rowIdx, COL.LEAD_DECISION).setValue(decision);
      sheet.getRange(rowIdx, COL.LEAD_NOTE).setValue(note || '');

      if (decision === 'APPROVED') {
        if (isAddTag) {
          // Bỏ qua DM -> thẳng QM
          sheet.getRange(rowIdx, COL.STATE).setValue('PENDING_QM');
          sheet.getRange(rowIdx, COL.DM_DECISION).setValue('SKIPPED');
          sheet.getRange(rowIdx, COL.DM_NOTE).setValue('Add tag có sẵn — bỏ qua DM review');
          sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue('READY_FOR_QM');
          sheet.getRange(rowIdx, COL.QM_STATUS).setValue('PENDING_QM');
          sheet.getRange(rowIdx, COL.DL_QM).setValue(fmt(addHours(now, slaHours(config, 'SLA_QM_HOURS', 24))));
        } else {
          // Tag mới -> DM review
          sheet.getRange(rowIdx, COL.STATE).setValue('PENDING_DM');
          sheet.getRange(rowIdx, COL.DM_NOTE).setValue('Đang chờ DM Lead kiểm duyệt');
          sheet.getRange(rowIdx, COL.DL_DM).setValue(fmt(addHours(now, slaHours(config, 'SLA_DM_HOURS', 8))));
        }
      } else { // REJECTED
        sheet.getRange(rowIdx, COL.STATE).setValue('REJECTED');
        sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue('CANCELLED');
        sheet.getRange(rowIdx, COL.QM_STATUS).setValue('N/A');
      }
      sheet.getRange(rowIdx, COL.BREACH).setValue(''); // reset cờ quá hạn khi đã xử lý
      break;
    }
  }
  return { status: "success" };
}

/* ============================================================
 *  GATE 2 — DM REVIEW (chỉ xử lý khi PENDING_DM)
 * ============================================================ */
function saveDMReview(reqId, decision, note, tagCode) {
  const role = getUserRole();
  if (role !== 'DM') {
    return { status: "error", message: "Chỉ DM Lead mới được review ở bước này." };
  }
  const sheet = getMainSheet();
  const config = getAppConfig();
  const rows = sheet.getDataRange().getValues();
  const now = new Date();

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][COL.ID-1] === reqId) {
      const rowIdx = i + 1;
      if (rows[i][COL.STATE-1] !== 'PENDING_DM') {
        return { status: "error", message: "Request không ở trạng thái chờ DM review." };
      }
      sheet.getRange(rowIdx, COL.DM_REVIEWER).setValue(getUserEmail() || 'DM Lead');
      sheet.getRange(rowIdx, COL.DM_DATE).setValue(fmt(now));
      sheet.getRange(rowIdx, COL.DM_DECISION).setValue(decision);
      sheet.getRange(rowIdx, COL.DM_NOTE).setValue(note);
      sheet.getRange(rowIdx, COL.DM_TAGCODE).setValue(tagCode);

      if (decision === "APPROVED") {
        sheet.getRange(rowIdx, COL.STATE).setValue('PENDING_QM');
        sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue("READY_FOR_QM");
        sheet.getRange(rowIdx, COL.QM_STATUS).setValue("PENDING_QM");
        sheet.getRange(rowIdx, COL.DL_QM).setValue(fmt(addHours(now, slaHours(config, 'SLA_QM_HOURS', 24))));
      } else {
        sheet.getRange(rowIdx, COL.STATE).setValue('REJECTED');
        sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue("CANCELLED");
        sheet.getRange(rowIdx, COL.QM_STATUS).setValue("N/A");
      }
      sheet.getRange(rowIdx, COL.BREACH).setValue('');
      break;
    }
  }
  return { status: "success" };
}

/* ============================================================
 *  GATE 3 — QM ADD TAG (TAGGED_SUCCESS -> DONE)
 * ============================================================ */
function saveQMStatus(reqId, status, successCount, ref) {
  const role = getUserRole();
  if (role !== 'QM' && role !== 'DM') {
    return { status: "error", message: "Chỉ QM mới được cập nhật ở bước này." };
  }
  const sheet = getMainSheet();
  const rows = sheet.getDataRange().getValues();
  const now = new Date();

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][COL.ID-1] === reqId) {
      const rowIdx = i + 1;
      if (rows[i][COL.STATE-1] !== 'PENDING_QM') {
        return { status: "error", message: "Request không ở trạng thái chờ QM xử lý." };
      }
      sheet.getRange(rowIdx, COL.QM_SPECIALIST).setValue(getUserEmail() || 'QM Specialist');
      const curDate = sheet.getRange(rowIdx, COL.QM_DATE).getValue();
      if (!curDate || curDate === "-") {
        sheet.getRange(rowIdx, COL.QM_DATE).setValue(fmt(now));
      }
      sheet.getRange(rowIdx, COL.QM_STATUS).setValue(status);
      if (status === "TAGGED_SUCCESS") {
        sheet.getRange(rowIdx, COL.QM_DONE_DATE).setValue(fmt(now));
        sheet.getRange(rowIdx, COL.STATE).setValue('DONE');
        sheet.getRange(rowIdx, COL.BREACH).setValue('');
      }
      sheet.getRange(rowIdx, COL.QM_SUCCESS).setValue(successCount);
      sheet.getRange(rowIdx, COL.QM_NOTE).setValue(ref);
      break;
    }
  }
  return { status: "success" };
}

/* ============================================================
 *  SLA — quét quá hạn + gửi email nhắc/escalate
 *  Gắn trigger: Edit > Triggers > checkSLABreaches, time-driven, mỗi 1-2h
 * ============================================================ */
function checkSLABreaches() {
  const sheet = getMainSheet();
  const rows = sheet.getDataRange().getValues();
  const now = new Date();
  let breachCount = 0;

  // Danh sách email approver theo role để nhắc
  const leadEmails = [], dmEmails = [], qmEmails = [];
  for (const em in ROLE_MAP) {
    if (ROLE_MAP[em] === 'TEAM_LEAD') leadEmails.push(em);
    else if (ROLE_MAP[em] === 'DM') dmEmails.push(em);
    else if (ROLE_MAP[em] === 'QM') qmEmails.push(em);
  }

  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (!r[COL.ID-1] || !r[COL.ID-1].toString().startsWith("REQ-")) continue;
    const state = r[COL.STATE-1];
    if (state === 'DONE' || state === 'REJECTED') continue;

    let deadlineCell = '', targets = [];
    if (state === 'PENDING_TEAM_LEAD') { deadlineCell = r[COL.DL_LEAD-1]; targets = leadEmails; }
    else if (state === 'PENDING_DM')   { deadlineCell = r[COL.DL_DM-1];   targets = dmEmails; }
    else if (state === 'PENDING_QM')   { deadlineCell = r[COL.DL_QM-1];   targets = qmEmails; }
    if (!deadlineCell) continue;

    const deadline = (deadlineCell instanceof Date) ? deadlineCell : new Date(deadlineCell.toString().replace(' ', 'T') + ':00+07:00');
    if (isNaN(deadline.getTime())) continue;

    if (now > deadline) {
      const rowIdx = i + 1;
      const already = r[COL.BREACH-1];
      sheet.getRange(rowIdx, COL.BREACH).setValue('QUÁ HẠN SLA');
      breachCount++;
      // Chỉ gửi email 1 lần (nếu chưa từng đánh dấu quá hạn)
      if (already !== 'QUÁ HẠN SLA' && targets.length > 0) {
        try {
          MailApp.sendEmail({
            to: targets.join(','),
            subject: '[Tag Request Portal] ⚠️ Request quá hạn SLA: ' + r[COL.ID-1],
            body: 'Request ' + r[COL.ID-1] + ' (' + r[COL.TEAM-1] + ' — ' + r[COL.TAGNAME-1] + ')'
                + ' đang ở trạng thái ' + state + ' và đã QUÁ HẠN SLA (deadline: ' + deadlineCell + ').'
                + '\nVui lòng xử lý sớm.'
          });
        } catch (e) { /* bỏ qua lỗi gửi mail */ }
      }
    }
  }
  return { status: "success", breaches: breachCount };
}
