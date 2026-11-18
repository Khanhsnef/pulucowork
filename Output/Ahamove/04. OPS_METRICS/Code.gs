/**
 * GOOGLE APPS SCRIPT BACKEND — 3-GATE APPROVAL WORKFLOW + RBAC + SLA
 * Spreadsheet Target ID: 1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4
 *
 * State machine:
 *   Tạo tag mới : PENDING_TEAM_LEAD -> PENDING_DM -> PENDING_QM -> DONE
 *   Add tag     : PENDING_TEAM_LEAD -> PENDING_QM -> DONE  (bỏ qua DM)
 *   Reject bất kỳ gate -> REJECTED (về requester để sửa & re-submit)
 *
 * DEPLOY NOTE: Script này có thể dùng cả dạng standalone lẫn container-bound.
 *   - Nếu standalone: dùng SpreadsheetApp.openById(SS_ID) bên dưới (đã cấu hình).
 *   - Nếu container-bound (tạo từ Extension menu của Sheet): getActiveSpreadsheet() cũng OK.
 *   - Execute as: "User accessing the web app" để RBAC đọc đúng email người dùng.
 *   - Access: "Anyone within ahamove.com" (hoặc Anyone nếu muốn public).
 *   - Sau mỗi lần sửa code PHẢI bấm "New deployment" hoặc test qua URL /dev.
 */

const SS_ID = '1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4';
function getSpreadsheet() {
  try {
    const active = SpreadsheetApp.getActiveSpreadsheet();
    if (active) return active;
  } catch (e) { /* standalone mode — fall through to openById */ }
  return SpreadsheetApp.openById(SS_ID);
}

/* ============================================================
 *  RBAC — PHÂN QUYỀN (hardcode theo email)
 *  >>> KHANH ĐIỀN EMAIL THẬT VÀO ĐÂY <<<
 *  Vai trò: TEAM_LEAD | DM | QM | REQUESTER (mặc định)
 * ============================================================ */
const ROLE_MAP = {
  // --- DM (override mọi team) ---
  'khanhlp@ahamove.com'  : 'DM',
  'trangdtt@ahamove.com' : 'DM',
  // --- Team Leads / Heads (duyệt Gate 1 theo team ở TEAM_LEAD_MAP) ---
  'hant@ahamove.com'     : 'TEAM_LEAD',  // S&P
  'sonnbt@ahamove.com'   : 'TEAM_LEAD',  // Growth
  'luuhtm@ahamove.com'   : 'TEAM_LEAD',  // Growth
  'thaoltn@ahamove.com'  : 'TEAM_LEAD',  // Expansion
  'thinhnh@ahamove.com'  : 'TEAM_LEAD',  // OE + PA
  'taipq@ahamove.com'    : 'TEAM_LEAD',  // OE
  'tuannq@ahamove.com'   : 'TEAM_LEAD',  // OE + PA
  'locnx@ahamove.com'    : 'TEAM_LEAD',  // WH
  // --- QM Specialists (Gate 3 add tag; đồng thời là Lead team QM ở Gate 1) ---
  'phundk@ahamove.com'   : 'QM',
  'vayhc@ahamove.com'    : 'QM'
};
const DOMAIN_DEFAULT_ROLE = 'REQUESTER'; // mọi user hợp lệ khác = requester

/* ============================================================
 *  TEAM ↔ LEAD — mỗi Team có ≥1 Lead/Head phụ trách (mảng email)
 *  Lead CHỈ duyệt được request của team mình. DM override tất cả.
 *  >>> KHANH: (1) sửa TÊN TEAM cho khớp TEAM_LIST ở 00_CONFIG_SETTINGS
 *             (2) điền EMAIL lead/head — thêm nhiều lead cho 1 team bằng cách
 *                 thêm phần tử vào mảng, vd: 'Growth': ['a@','b@'].
 * ============================================================ */
const TEAM_LEAD_MAP = {
  'DM'        : ['khanhlp@ahamove.com', 'trangdtt@ahamove.com'],
  'S&P'       : ['hant@ahamove.com'],
  'Growth'    : ['sonnbt@ahamove.com', 'luuhtm@ahamove.com'],
  'Expansion' : ['thaoltn@ahamove.com'],
  'OE'        : ['thinhnh@ahamove.com', 'taipq@ahamove.com', 'tuannq@ahamove.com'],
  'PA'        : ['thinhnh@ahamove.com', 'tuannq@ahamove.com'],
  'WH'        : ['locnx@ahamove.com'],
  'QM'        : ['phundk@ahamove.com', 'vayhc@ahamove.com']
};

// Lead `email` có được duyệt request của `team` không?
// DM luôn = true (override mọi team). Ngoài ra: bất kỳ ai có tên trong TEAM_LEAD_MAP[team]
// đều duyệt được Gate 1 của team đó — kể cả người mang role QM (vd QM team leads).
function canLeadApproveTeam(email, team, role) {
  if (role === 'DM') return true;                       // DM override mọi team
  var owners = (TEAM_LEAD_MAP[team] || []).map(function(e){ return String(e).toLowerCase(); });
  return owners.indexOf((email || '').toLowerCase()) !== -1;
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
  return HtmlService.createHtmlOutputFromFile('Portal')
    .setTitle('Tag Request Portal')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/* ============================================================
 *  CONFIG
 * ============================================================ */
function getAppConfig() {
  const ss = getSpreadsheet();
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
    sheet.appendRow(["TEAM_LIST", "DM, S&P, Growth, Expansion, OE, PA, WH, QM", "Danh sách Team"]);
    sheet.appendRow(["TAG_TYPES", "Driver Segment, Incentive/Challenge, Adhoc, Others", "Danh sách loại Tag"]);
    sheet.appendRow(["SLA_LEAD_HOURS", "4", "SLA giờ chờ Lead duyệt (Gate 1)"]);
    sheet.appendRow(["SLA_DM_HOURS", "8", "SLA giờ chờ DM review (Gate 2)"]);
    sheet.appendRow(["SLA_QM_HOURS", "24", "SLA giờ chờ QM add tag (Gate 3)"]);
    sheet.appendRow(["TELEGRAM_ENABLED", "TRUE", "Bật/Tắt thông báo Telegram (TRUE/FALSE)"]);
    sheet.appendRow(["TELEGRAM_BOT_TOKEN", "8502919754:AAFGjkjrizuZ40ucUjFZ-CXA6TP6W40tXYE", "Telegram Bot Token"]);
    sheet.appendRow(["TELEGRAM_CHAT_ID", "-4601794194", "Telegram Group Chat ID"]);
    sheet.appendRow(["EMAIL_NOTIF_ENABLED", "TRUE", "Bật/Tắt thông báo qua Email (TRUE/FALSE)"]);
    sheet.appendRow(["PORTAL_URL", "https://script.google.com/macros/s/AKfycbyqUdTw-palPPXOyR4OAzrVlsgEF0ospSQl2E47G3lyEv-W1jvINrGmlYxKWjx-RvLMbg/exec", "URL Portal để mở trực tiếp từ thông báo"]);
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
    SLA_LEAD_HOURS: "4", SLA_DM_HOURS: "8", SLA_QM_HOURS: "24",
    TELEGRAM_ENABLED: "TRUE",
    TELEGRAM_BOT_TOKEN: "8502919754:AAFGjkjrizuZ40ucUjFZ-CXA6TP6W40tXYE",
    TELEGRAM_CHAT_ID: "-4601794194",
    EMAIL_NOTIF_ENABLED: "TRUE",
    PORTAL_URL: "https://script.google.com/macros/s/AKfycbyqUdTw-palPPXOyR4OAzrVlsgEF0ospSQl2E47G3lyEv-W1jvINrGmlYxKWjx-RvLMbg/exec"
  };
  for (const k in defaults) { if (!config[k]) config[k] = defaults[k]; }
  // Inject user identity so JS can set role/email without template variables
  config.userEmail = getUserEmail();
  config.userRole  = getUserRole();
  return config;
}

function saveAppConfig(newConfig) {
  const ss = getSpreadsheet();
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
// 23 cột gốc + 11 cột mới (append cuối để không vỡ data cũ)
const BASE_HEADERS = ["Mã Request", "Ngày Tạo", "Hình Thức", "Team Đề Xuất", "Người Đề Xuất", "Loại Tag", "Tên Tag Yêu Cầu", "Nguồn Danh Sách TX", "Số Lượng TX", "Lý Do", "Thời Gian", "DM Reviewer", "Ngày DM Review", "DM Quyết Định", "DM Note", "DM Tag Code", "QM Handover", "QM Specialist", "Ngày QM Nhận", "QM Trạng Thái Add Tag", "Ngày Add Tag Xong", "Số TX Add Thành Công", "Ghi Chú QM"];
const NEW_HEADERS = ["Lead Approver", "Ngày Lead Duyệt", "Lead Quyết Định", "Lead Note", "Trạng Thái Tổng", "Deadline Lead", "Deadline DM", "Deadline QM", "Cờ Quá Hạn", "Cần Add Tag Xong Trước", "Email Người Tạo"];
// Cột (1-based) — vị trí cột mới bắt đầu từ 24
const COL = {
  ID: 1, DATE: 2, CATEGORY: 3, TEAM: 4, NAME: 5, TYPE: 6, TAGNAME: 7,
  SRC: 8, COUNT: 9, REASON: 10, DURATION: 11,
  DM_REVIEWER: 12, DM_DATE: 13, DM_DECISION: 14, DM_NOTE: 15, DM_TAGCODE: 16, QM_HANDOVER: 17,
  QM_SPECIALIST: 18, QM_DATE: 19, QM_STATUS: 20, QM_DONE_DATE: 21, QM_SUCCESS: 22, QM_NOTE: 23,
  LEAD_APPROVER: 24, LEAD_DATE: 25, LEAD_DECISION: 26, LEAD_NOTE: 27,
  STATE: 28, DL_LEAD: 29, DL_DM: 30, DL_QM: 31, BREACH: 32, DUE_DATE: 33,
  SUBMITTER: 34
};

function getMainSheet() {
  const ss = getSpreadsheet();
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
        dueDate: r[COL.DUE_DATE-1] || '-',
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
        breach: r[COL.BREACH-1] || '',
        submitterEmail: (COL.SUBMITTER && r[COL.SUBMITTER-1]) ? r[COL.SUBMITTER-1] : ''
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

  // Generate ID server-side để đảm bảo luôn có ID dù client không truyền
  const lastRow = sheet.getLastRow();
  const seq = String(lastRow).padStart(3, '0');
  const dateTag = Utilities.formatDate(now, "GMT+7", "yyyyMMdd");
  const reqId = 'REQ-' + dateTag + '-' + seq;

  const row = new Array(BASE_HEADERS.length + NEW_HEADERS.length).fill("");
  row[COL.ID-1] = reqId;
  row[COL.DATE-1] = fmt(now);
  row[COL.CATEGORY-1] = data.requestCategory;
  row[COL.TEAM-1] = data.team;
  row[COL.NAME-1] = data.name;
  row[COL.TYPE-1] = data.type;
  row[COL.TAGNAME-1] = data.tagName;
  row[COL.SRC-1] = data.driverListSource || '-';
  row[COL.COUNT-1] = data.count || 0;
  row[COL.REASON-1] = data.reason;
  row[COL.DURATION-1] = data.duration;
  row[COL.DUE_DATE-1] = data.dueDate || '-';
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
  // Ghi email người tạo — ưu tiên từ Session (Apps Script), fallback data.submitterEmail từ client
  const submitterEmail = getUserEmail() || data.submitterEmail || '';
  if (COL.SUBMITTER && submitterEmail) row[COL.SUBMITTER-1] = submitterEmail;
  row[COL.DL_LEAD-1] = fmt(dlLead);
  row[COL.DL_DM-1] = ''; row[COL.DL_QM-1] = '';
  row[COL.BREACH-1] = '';

  sheet.appendRow(row);

  // Gửi thông báo đến Lead và nhóm Telegram
  try {
    notifyWorkflowStep('NEW_REQUEST', {
      id: reqId,
      team: data.team,
      name: data.name,
      submitterEmail: submitterEmail,
      requestCategory: data.requestCategory,
      tagName: data.tagName,
      type: data.type,
      count: data.count || 0,
      reason: data.reason,
      duration: data.duration,
      dueDate: data.dueDate,
      deadlineLead: fmt(dlLead)
    });
  } catch (err) {
    Logger.log('[saveNewRequest] Notification error: ' + err);
  }

  return { status: "success", id: reqId };
}

/* ============================================================
 *  UTILS
 * ============================================================ */
function saveCell(id, colName, value) {
  const ss = getSpreadsheet();
  const sheet = ss.getSheetByName("02_DATA_REQUEST");
  if (!sheet) return { status: 'error', message: 'Không tìm thấy sheet 02_DATA_REQUEST' };

  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const colIndex = headers.indexOf(colName);
  if (colIndex === -1) return { status: 'error', message: 'Không tìm thấy cột ' + colName };

  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === id) {
      sheet.getRange(i + 1, colIndex + 1).setValue(value);
      return { status: 'success' };
    }
  }
  return { status: 'error', message: 'Không tìm thấy ID: ' + id };
}

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/* ============================================================
 *  GATE 1 — LEAD APPROVAL
 * ============================================================ */
function saveLeadApproval(reqId, decision, note) {
  const role = getUserRole();
  // QM có thể là Lead của team QM — defer RBAC hoàn toàn sang canLeadApproveTeam bên dưới
  if (role !== 'TEAM_LEAD' && role !== 'DM' && role !== 'QM') {
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

      let nextDeadline = '';
      if (decision === 'APPROVED') {
        if (isAddTag) {
          // Bỏ qua DM -> thẳng QM
          const dlQM = addHours(now, slaHours(config, 'SLA_QM_HOURS', 24));
          nextDeadline = fmt(dlQM);
          sheet.getRange(rowIdx, COL.STATE).setValue('PENDING_QM');
          sheet.getRange(rowIdx, COL.DM_DECISION).setValue('SKIPPED');
          sheet.getRange(rowIdx, COL.DM_NOTE).setValue('Add tag có sẵn — bỏ qua DM review');
          sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue('READY_FOR_QM');
          sheet.getRange(rowIdx, COL.QM_STATUS).setValue('PENDING_QM');
          sheet.getRange(rowIdx, COL.DL_QM).setValue(nextDeadline);
        } else {
          // Tag mới -> DM review
          const dlDM = addHours(now, slaHours(config, 'SLA_DM_HOURS', 8));
          nextDeadline = fmt(dlDM);
          sheet.getRange(rowIdx, COL.STATE).setValue('PENDING_DM');
          sheet.getRange(rowIdx, COL.DM_NOTE).setValue('Đang chờ DM Lead kiểm duyệt');
          sheet.getRange(rowIdx, COL.DL_DM).setValue(nextDeadline);
        }
      } else { // REJECTED
        sheet.getRange(rowIdx, COL.STATE).setValue('REJECTED');
        sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue('CANCELLED');
        sheet.getRange(rowIdx, COL.QM_STATUS).setValue('N/A');
      }
      sheet.getRange(rowIdx, COL.BREACH).setValue(''); // reset cờ quá hạn khi đã xử lý

      // Bắn thông báo Telegram & Email
      try {
        const reqSnapshot = {
          id: reqId,
          team: reqTeam,
          name: rows[i][COL.NAME-1],
          submitterEmail: (COL.SUBMITTER && rows[i][COL.SUBMITTER-1]) ? rows[i][COL.SUBMITTER-1] : '',
          requestCategory: rows[i][COL.CATEGORY-1],
          tagName: rows[i][COL.TAGNAME-1],
          type: rows[i][COL.TYPE-1],
          leadApprover: getUserEmail() || 'Team Lead',
          leadNote: note || '',
          nextDeadline: nextDeadline,
          driverListSource: rows[i][COL.SRC-1],
          count: rows[i][COL.COUNT-1]
        };

        if (decision === 'APPROVED') {
          notifyWorkflowStep(isAddTag ? 'LEAD_APPROVED_ADD_TAG' : 'LEAD_APPROVED_NEW_TAG', reqSnapshot);
        } else {
          notifyWorkflowStep('LEAD_REJECTED', reqSnapshot);
        }
      } catch (err) {
        Logger.log('[saveLeadApproval] Notification error: ' + err);
      }
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

      let nextDeadline = '';
      if (decision === "APPROVED") {
        const dlQM = addHours(now, slaHours(config, 'SLA_QM_HOURS', 24));
        nextDeadline = fmt(dlQM);
        sheet.getRange(rowIdx, COL.STATE).setValue('PENDING_QM');
        sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue("READY_FOR_QM");
        sheet.getRange(rowIdx, COL.QM_STATUS).setValue("PENDING_QM");
        sheet.getRange(rowIdx, COL.DL_QM).setValue(nextDeadline);
      } else {
        sheet.getRange(rowIdx, COL.STATE).setValue('REJECTED');
        sheet.getRange(rowIdx, COL.QM_HANDOVER).setValue("CANCELLED");
        sheet.getRange(rowIdx, COL.QM_STATUS).setValue("N/A");
      }
      sheet.getRange(rowIdx, COL.BREACH).setValue('');

      // Bắn thông báo Telegram & Email
      try {
        const reqSnapshot = {
          id: reqId,
          team: rows[i][COL.TEAM-1],
          name: rows[i][COL.NAME-1],
          submitterEmail: (COL.SUBMITTER && rows[i][COL.SUBMITTER-1]) ? rows[i][COL.SUBMITTER-1] : '',
          requestCategory: rows[i][COL.CATEGORY-1],
          tagName: rows[i][COL.TAGNAME-1],
          dmTagCode: tagCode,
          dmReviewer: getUserEmail() || 'DM Lead',
          dmNote: note || '',
          nextDeadline: nextDeadline,
          driverListSource: rows[i][COL.SRC-1],
          count: rows[i][COL.COUNT-1]
        };

        if (decision === "APPROVED") {
          notifyWorkflowStep('DM_APPROVED', reqSnapshot);
        } else {
          notifyWorkflowStep('DM_REJECTED', reqSnapshot);
        }
      } catch (err) {
        Logger.log('[saveDMReview] Notification error: ' + err);
      }
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

      // Bắn thông báo Telegram & Email khi hoàn thành
      if (status === "TAGGED_SUCCESS") {
        try {
          const reqSnapshot = {
            id: reqId,
            team: rows[i][COL.TEAM-1],
            name: rows[i][COL.NAME-1],
            submitterEmail: (COL.SUBMITTER && rows[i][COL.SUBMITTER-1]) ? rows[i][COL.SUBMITTER-1] : '',
            tagName: rows[i][COL.TAGNAME-1],
            dmTagCode: rows[i][COL.DM_TAGCODE-1] || rows[i][COL.TAGNAME-1],
            qmSpecialist: getUserEmail() || 'QM Specialist',
            successCount: successCount,
            qmRef: ref
          };
          notifyWorkflowStep('QM_DONE', reqSnapshot);
        } catch (err) {
          Logger.log('[saveQMStatus] Notification error: ' + err);
        }
      }
      break;
    }
  }
  return { status: "success" };
}

/* ============================================================
 *  SLA — quét quá hạn + gửi email & Telegram cảnh báo
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
      // Chỉ gửi thông báo 1 lần (nếu chưa từng đánh dấu quá hạn)
      if (already !== 'QUÁ HẠN SLA' && targets.length > 0) {
        try {
          notifyWorkflowStep('SLA_BREACH', {
            id: r[COL.ID-1],
            team: r[COL.TEAM-1],
            tagName: r[COL.TAGNAME-1],
            state: state,
            deadline: deadlineCell,
            targets: targets
          });
        } catch (e) {
          Logger.log('[checkSLABreaches] Alert error: ' + e);
        }
      }
    }
  }
  return { status: "success", breaches: breachCount };
}

/* ============================================================
 *  NOTIFICATION ENGINE (TELEGRAM & EMAIL)
 * ============================================================ */
function getPortalUrl(config) {
  if (config && config.PORTAL_URL && config.PORTAL_URL.trim()) {
    return config.PORTAL_URL.trim();
  }
  try {
    const serviceUrl = ScriptApp.getService().getUrl();
    if (serviceUrl) return serviceUrl;
  } catch (e) {}
  return "https://docs.google.com/spreadsheets/d/" + SS_ID + "/edit";
}

function getLeadEmailsForTeam(team) {
  if (TEAM_LEAD_MAP[team] && TEAM_LEAD_MAP[team].length > 0) {
    return TEAM_LEAD_MAP[team];
  }
  return TEAM_LEAD_MAP['DM'] || ['khanhlp@ahamove.com'];
}

function getDMEmails() {
  return TEAM_LEAD_MAP['DM'] || ['khanhlp@ahamove.com', 'trangdtt@ahamove.com'];
}

function getQMEmails() {
  return TEAM_LEAD_MAP['QM'] || ['phundk@ahamove.com', 'vayhc@ahamove.com'];
}

function sendTelegramNotification(htmlText) {
  try {
    const config = getAppConfig();
    if (String(config.TELEGRAM_ENABLED).toUpperCase() !== 'TRUE') {
      Logger.log('[Telegram] Tắt thông báo qua config.');
      return { success: false, reason: 'disabled' };
    }
    const token = (config.TELEGRAM_BOT_TOKEN || '').trim();
    const chatId = (config.TELEGRAM_CHAT_ID || '').trim();
    if (!token || !chatId) {
      Logger.log('[Telegram] Thiếu BOT_TOKEN hoặc CHAT_ID.');
      return { success: false, reason: 'missing_credentials' };
    }

    const endpoint = 'https://api.telegram.org/bot' + token + '/sendMessage';
    const payload = {
      chat_id: chatId,
      text: htmlText,
      parse_mode: 'HTML',
      disable_web_page_preview: true
    };
    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const resp = UrlFetchApp.fetch(endpoint, options);
    const code = resp.getResponseCode();
    if (code >= 200 && code < 300) {
      Logger.log('[Telegram] Gửi thành công.');
      return { success: true };
    } else {
      Logger.log('[Telegram] Lỗi phản hồi HTTP ' + code + ': ' + resp.getContentText());
      return { success: false, code: code, response: resp.getContentText() };
    }
  } catch (err) {
    Logger.log('[Telegram] Exception: ' + err);
    return { success: false, error: String(err) };
  }
}

function sendEmailNotification(recipients, subject, htmlContent) {
  try {
    const config = getAppConfig();
    if (String(config.EMAIL_NOTIF_ENABLED).toUpperCase() !== 'TRUE') {
      Logger.log('[Email] Tắt gửi email qua config.');
      return { success: false, reason: 'disabled' };
    }
    if (!recipients) return { success: false, reason: 'no_recipients' };

    const list = (Array.isArray(recipients) ? recipients : [recipients])
      .map(function(e) { return String(e).trim(); })
      .filter(function(e) { return e && e.indexOf('@') !== -1; });

    if (list.length === 0) return { success: false, reason: 'empty_valid_recipients' };

    MailApp.sendEmail({
      to: list.join(','),
      subject: subject,
      htmlBody: htmlContent
    });
    Logger.log('[Email] Gửi mail thành công tới: ' + list.join(', '));
    return { success: true };
  } catch (err) {
    Logger.log('[Email] Exception: ' + err);
    return { success: false, error: String(err) };
  }
}

function buildEmailTemplate(title, intro, tableRows, ctaUrl) {
  let rowsHtml = '';
  for (let i = 0; i < tableRows.length; i++) {
    const bg = (i % 2 === 0) ? '#F8FAFC' : '#FFFFFF';
    rowsHtml += '<tr style="background-color: ' + bg + ';">'
      + '<td style="padding: 10px 14px; font-weight: 600; color: #475569; width: 35%; border-bottom: 1px solid #E2E8F0;">' + tableRows[i][0] + '</td>'
      + '<td style="padding: 10px 14px; color: #1E293B; border-bottom: 1px solid #E2E8F0;">' + tableRows[i][1] + '</td>'
      + '</tr>';
  }

  return '<div style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Arial, sans-serif; max-width: 620px; margin: 0 auto; padding: 20px; background-color: #F1F5F9;">'
    + '<div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 22px 24px; border-radius: 12px 12px 0 0; border-bottom: 4px solid #FF6B00;">'
    + '  <div style="color: #FF6B00; font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">AHAMOVE DRIVER MANAGEMENT</div>'
    + '  <div style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin-top: 6px;">' + title + '</div>'
    + '</div>'
    + '<div style="background-color: #FFFFFF; padding: 24px; border-radius: 0 0 12px 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">'
    + '  <p style="font-size: 14px; color: #334155; line-height: 1.6; margin: 0 0 18px 0;">' + intro + '</p>'
    + '  <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 24px; border: 1px solid #E2E8F0; border-radius: 8px; overflow: hidden;">'
    +      rowsHtml
    + '  </table>'
    + '  <div style="text-align: center; margin: 28px 0 10px 0;">'
    + '    <a href="' + ctaUrl + '" style="display: inline-block; background-color: #FF6B00; color: #FFFFFF; font-weight: 700; font-size: 14px; text-decoration: none; padding: 12px 28px; border-radius: 6px; box-shadow: 0 4px 10px rgba(255, 107, 0, 0.35);">'
    + '      👉 TRUY CẬP TAG PORTAL ĐỂ XỬ LÝ'
    + '    </a>'
    + '  </div>'
    + '</div>'
    + '<div style="text-align: center; margin-top: 16px; font-size: 11px; color: #94A3B8;">'
    + '  Hệ thống thông báo tự động Tag Request Portal · Ahamove Driver Management'
    + '</div>'
    + '</div>';
}

function notifyWorkflowStep(step, data) {
  const config = getAppConfig();
  const portalUrl = getPortalUrl(config);

  if (step === 'NEW_REQUEST') {
    // 1. Tạo request mới -> Thông báo Lead + DM
    const tgMsg = '🔔 <b>[TAG PORTAL] ĐỀ XUẤT TAG MỚI CẦN DUYỆT (GATE 1)</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team đề xuất:</b> <b>' + data.team + '</b>\n'
      + '👤 <b>Người đề xuất:</b> ' + data.name + (data.submitterEmail ? ' (' + data.submitterEmail + ')' : '') + '\n'
      + '🏷️ <b>Tên Tag:</b> <code>' + data.tagName + '</code> (' + data.type + ')\n'
      + '📦 <b>Hình thức:</b> ' + data.requestCategory + '\n'
      + '👥 <b>Số lượng TX:</b> ' + (data.count || 0) + ' tài xế\n'
      + '🎯 <b>Lý do:</b> ' + (data.reason || '-') + '\n'
      + '⏰ <b>Hạn Lead duyệt (SLA):</b> <b>' + data.deadlineLead + '</b> (≤ 4h)\n\n'
      + '👉 <i>Vui lòng vào Portal để xem xét và duyệt:</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>MỞ TAG PORTAL ĐỂ DUYỆT NGAY</b></a>';

    sendTelegramNotification(tgMsg);

    const emailRows = [
      ['Mã Request', '<b>' + data.id + '</b>'],
      ['Team Đề Xuất', data.team],
      ['Người Tạo', data.name + (data.submitterEmail ? ' (' + data.submitterEmail + ')' : '')],
      ['Hình Thức', data.requestCategory],
      ['Tên Tag Yêu Cầu', '<code>' + data.tagName + '</code> (' + data.type + ')'],
      ['Số Lượng TX', String(data.count || 0)],
      ['Lý Do & Tiêu Chí', data.reason || '-'],
      ['Hạn SLA Duyệt', '<b style="color: #D97706;">' + data.deadlineLead + ' (≤ 4 giờ)</b>']
    ];
    const emailHtml = buildEmailTemplate(
      'Yêu Cầu Duyệt Tag Mới: ' + data.id,
      'Chào Anh/Chị Team Lead, hệ thống vừa nhận được 1 đề xuất Tag tài xế từ team <b>' + data.team + '</b> đang chờ phê duyệt ở Gate 1.',
      emailRows,
      portalUrl
    );
    const leadTargets = getLeadEmailsForTeam(data.team).concat(getDMEmails());
    sendEmailNotification(leadTargets, '[Tag Portal] 🔔 Đề xuất Tag mới cần duyệt: ' + data.id + ' (' + data.team + ')', emailHtml);

  } else if (step === 'LEAD_APPROVED_NEW_TAG') {
    // 2. Lead duyệt Tag Mới -> Chờ DM Review (Gate 2)
    const tgMsg = '🛡️ <b>[TAG PORTAL] LEAD ĐÃ DUYỆT! CHỜ DM THẨM ĐỊNH (GATE 2)</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> <b>' + data.team + '</b>\n'
      + '🏷️ <b>Tên Tag gợi ý:</b> <code>' + data.tagName + '</code>\n'
      + '👤 <b>Lead đã duyệt:</b> ' + data.leadApprover + '\n'
      + '💬 <b>Ghi chú Lead:</b> <i>' + (data.leadNote || '(Không có)') + '</i>\n'
      + '⏰ <b>Hạn DM duyệt (SLA):</b> <b>' + (data.nextDeadline || '≤ 8h') + '</b>\n\n'
      + '👉 <i>Cần DM thẩm định nghiệp vụ & cấp mã Tag Code chuẩn (Taxonomy):</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>MỞ TAG PORTAL ĐỂ GÁN MÃ TAG</b></a>';

    sendTelegramNotification(tgMsg);

    const emailRows = [
      ['Mã Request', '<b>' + data.id + '</b>'],
      ['Team Đề Xuất', data.team],
      ['Tên Tag Yêu Cầu', '<code>' + data.tagName + '</code>'],
      ['Lead Đã Duyệt', data.leadApprover],
      ['Ghi Chú Của Lead', data.leadNote || '(Không có)'],
      ['Hạn SLA DM', '<b style="color: #4F46E5;">' + (data.nextDeadline || '≤ 8 giờ') + '</b>']
    ];
    const emailHtml = buildEmailTemplate(
      'Lead Đã Duyệt! Cần DM Review: ' + data.id,
      'Chào DM Lead, đề xuất Tag từ team <b>' + data.team + '</b> đã được Lead duyệt thành công. Vui lòng thẩm định và gán mã Tag chuẩn cho QM.',
      emailRows,
      portalUrl
    );
    sendEmailNotification(getDMEmails(), '[Tag Portal] 🛡️ Lead đã duyệt ' + data.id + '! Cần DM Review & Gán Tag Code', emailHtml);

  } else if (step === 'LEAD_APPROVED_ADD_TAG') {
    // 3. Lead duyệt Add Tag có sẵn -> Bỏ qua DM, nhảy thẳng QM Queue
    const tgMsg = '⚙️ <b>[TAG PORTAL] YÊU CẦU ADD TAG SẴN CÓ (GATE 3 - QM QUEUE)</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> <b>' + data.team + '</b>\n'
      + '🏷️ <b>Tên Tag:</b> <code>' + data.tagName + '</code>\n'
      + '👤 <b>Lead đã duyệt:</b> ' + data.leadApprover + ' <i>(Bỏ qua bước DM)</i>\n'
      + '📋 <b>Nguồn DS tài xế:</b> ' + (data.driverListSource || '-') + '\n'
      + '👥 <b>Số lượng TX:</b> ' + (data.count || 0) + ' tài xế\n'
      + '⏰ <b>Hạn QM hoàn tất (SLA):</b> <b>' + (data.nextDeadline || '≤ 24h') + '</b>\n\n'
      + '👉 <i>Cần QM vào hàng đợi để gắn tag cho đối tác:</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>MỞ TAG PORTAL ĐỂ XỬ LÝ</b></a>';

    sendTelegramNotification(tgMsg);

    const emailRows = [
      ['Mã Request', '<b>' + data.id + '</b>'],
      ['Team Đề Xuất', data.team],
      ['Tên Tag Gán', '<code>' + data.tagName + '</code>'],
      ['Lead Phê Duyệt', data.leadApprover],
      ['Nguồn Danh Sách TX', data.driverListSource || '-'],
      ['Số Lượng TX', String(data.count || 0)],
      ['Hạn SLA QM', '<b style="color: #059669;">' + (data.nextDeadline || '≤ 24 giờ') + '</b>']
    ];
    const emailHtml = buildEmailTemplate(
      'Hàng Đợi QM: Yêu Cầu Add Tag ' + data.id,
      'Chào QM Team, đề xuất Add Tag có sẵn đã được Lead duyệt và sẵn sàng trong hàng đợi để gắn tag trên hệ thống.',
      emailRows,
      portalUrl
    );
    sendEmailNotification(getQMEmails(), '[Tag Portal] ⚙️ Hàng đợi QM: Đề xuất Add Tag ' + data.id + ' (' + data.team + ')', emailHtml);

  } else if (step === 'LEAD_REJECTED') {
    // 4. Lead từ chối
    const tgMsg = '❌ <b>[TAG PORTAL] ĐỀ XUẤT BỊ TỪ CHỐI TẠI GATE 1</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> ' + data.team + ' | <b>Tag:</b> <code>' + data.tagName + '</code>\n'
      + '👤 <b>Người từ chối:</b> Lead (' + data.leadApprover + ')\n'
      + '💬 <b>Lý do từ chối:</b> <i>' + (data.leadNote || 'Không đạt tiêu chí') + '</i>\n\n'
      + '👉 <i>Requester vui lòng kiểm tra lại lý do trên Portal:</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>XEM CHI TIẾT TRÊN PORTAL</b></a>';

    sendTelegramNotification(tgMsg);

    if (data.submitterEmail) {
      const emailRows = [
        ['Mã Request', '<b>' + data.id + '</b>'],
        ['Người Từ Chối', data.leadApprover],
        ['Lý Do Từ Chối', '<span style="color:#EF4444; font-weight:600;">' + (data.leadNote || 'Không đạt yêu cầu') + '</span>']
      ];
      const emailHtml = buildEmailTemplate(
        'Đề Xuất Bị Từ Chối: ' + data.id,
        'Chào bạn, đề xuất Tag của bạn vừa bị từ chối bởi Team Lead ở Gate 1. Vui lòng xem lý do để điều chỉnh đề xuất mới.',
        emailRows,
        portalUrl
      );
      sendEmailNotification([data.submitterEmail], '[Tag Portal] ❌ Đề xuất ' + data.id + ' đã bị Từ chối bởi Lead', emailHtml);
    }

  } else if (step === 'DM_APPROVED') {
    // 5. DM duyệt & gán Tag Code -> Giao QM
    const tgMsg = '⚙️ <b>[TAG PORTAL] DM ĐÃ CẤP MÃ TAG! CHỜ QM GẮN TAG (GATE 3)</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> <b>' + data.team + '</b>\n'
      + '🏷️ <b>Mã Tag chuẩn (Taxonomy):</b> <code>' + data.dmTagCode + '</code>\n'
      + '👤 <b>DM Reviewer:</b> ' + data.dmReviewer + '\n'
      + '💬 <b>Ghi chú DM:</b> <i>' + (data.dmNote || '(Không có)') + '</i>\n'
      + '📋 <b>Nguồn DS tài xế:</b> ' + (data.driverListSource || '-') + '\n'
      + '👥 <b>Số lượng TX:</b> ' + (data.count || 0) + ' tài xế\n'
      + '⏰ <b>Hạn QM hoàn tất (SLA):</b> <b>' + (data.nextDeadline || '≤ 24h') + '</b>\n\n'
      + '👉 <i>Cần QM vào hàng đợi để gắn tag cho đối tác:</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>MỞ TAG PORTAL ĐỂ CẬP NHẬT QM</b></a>';

    sendTelegramNotification(tgMsg);

    const emailRows = [
      ['Mã Request', '<b>' + data.id + '</b>'],
      ['Team Đề Xuất', data.team],
      ['Mã Tag Chuẩn Cấp Phép', '<b style="color: #0D9488; font-size: 14px;">' + data.dmTagCode + '</b>'],
      ['DM Reviewer', data.dmReviewer],
      ['Ghi Chú Của DM', data.dmNote || '(Không có)'],
      ['Hạn SLA QM', '<b style="color: #059669;">' + (data.nextDeadline || '≤ 24 giờ') + '</b>']
    ];
    const emailHtml = buildEmailTemplate(
      'DM Đã Cấp Mã Tag! Chờ QM Xử Lý: ' + data.id,
      'Chào QM Team, đề xuất Tag đã được DM thẩm định và chính thức cấp mã Tag chuẩn <b>' + data.dmTagCode + '</b>. Vui lòng tiến hành add tag cho tài xế.',
      emailRows,
      portalUrl
    );
    const qmTargets = getQMEmails().concat(data.submitterEmail ? [data.submitterEmail] : []);
    sendEmailNotification(qmTargets, '[Tag Portal] ⚙️ DM đã duyệt & cấp Tag Code ' + data.dmTagCode + ': ' + data.id + ' (Chờ QM)', emailHtml);

  } else if (step === 'DM_REJECTED') {
    // 6. DM từ chối
    const tgMsg = '❌ <b>[TAG PORTAL] ĐỀ XUẤT BỊ TỪ CHỐI BỞI DM</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> ' + data.team + ' | <b>Tag:</b> <code>' + data.tagName + '</code>\n'
      + '👤 <b>Người từ chối:</b> DM Lead (' + data.dmReviewer + ')\n'
      + '💬 <b>Lý do từ chối:</b> <i>' + (data.dmNote || 'Không phù hợp taxonomy/chính sách') + '</i>\n\n'
      + '👉 <i>Requester & Lead vui lòng xem lại lý do trên Portal:</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>XEM CHI TIẾT TRÊN PORTAL</b></a>';

    sendTelegramNotification(tgMsg);

    const rejectTargets = (data.submitterEmail ? [data.submitterEmail] : []).concat(getLeadEmailsForTeam(data.team));
    if (rejectTargets.length > 0) {
      const emailRows = [
        ['Mã Request', '<b>' + data.id + '</b>'],
        ['Người Từ Chối', data.dmReviewer],
        ['Lý Do Từ Chối', '<span style="color:#EF4444; font-weight:600;">' + (data.dmNote || 'Không đạt tiêu chí taxonomy') + '</span>']
      ];
      const emailHtml = buildEmailTemplate(
        'DM Đã Từ Chối Đề Xuất: ' + data.id,
        'Chào bạn và Team Lead, đề xuất Tag đã bị từ chối ở bước thẩm định của DM. Vui lòng xem lý do để có hướng điều chỉnh phù hợp.',
        emailRows,
        portalUrl
      );
      sendEmailNotification(rejectTargets, '[Tag Portal] ❌ Đề xuất ' + data.id + ' đã bị Từ chối bởi DM', emailHtml);
    }

  } else if (step === 'QM_DONE') {
    // 7. QM hoàn tất gắn tag
    const tgMsg = '🎉 <b>[TAG PORTAL] ĐÃ HOÀN TẤT GẮN TAG TÀI XẾ (DONE)</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> <b>' + data.team + '</b>\n'
      + '🏷️ <b>Mã Tag:</b> <code>' + data.dmTagCode + '</code>\n'
      + '👤 <b>QM Specialist:</b> ' + data.qmSpecialist + '\n'
      + '✅ <b>Số lượng TX gắn thành công:</b> <b>' + data.successCount + '</b> tài xế\n'
      + '📝 <b>Batch Ref / Ghi chú:</b> <i>' + (data.qmRef || '-') + '</i>\n\n'
      + '👉 <i>Tag đã sẵn sàng vận hành trên hệ thống!</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>MỞ TAG PORTAL ĐỂ XEM</b></a>';

    sendTelegramNotification(tgMsg);

    const targets = (data.submitterEmail ? [data.submitterEmail] : [])
      .concat(getLeadEmailsForTeam(data.team))
      .concat(getDMEmails());

    const emailRows = [
      ['Mã Request', '<b>' + data.id + '</b>'],
      ['Team Đề Xuất', data.team],
      ['Mã Tag Đã Gắn', '<b style="color: #059669; font-size: 14px;">' + data.dmTagCode + '</b>'],
      ['QM Phụ Trách', data.qmSpecialist],
      ['Số Lượng TX Thành Công', '<b style="color: #059669;">' + data.successCount + ' tài xế</b>'],
      ['Batch / Ghi Chú QM', data.qmRef || '-']
    ];
    const emailHtml = buildEmailTemplate(
      'Hoàn Tất Gắn Tag Tài Xế: ' + data.id,
      'Xin chúc mừng! Đề xuất Tag tài xế từ team <b>' + data.team + '</b> đã được bộ phận QM add thành công vào hệ thống.',
      emailRows,
      portalUrl
    );
    sendEmailNotification(targets, '[Tag Portal] 🎉 Hoàn tất gắn Tag ' + data.dmTagCode + ': ' + data.id + ' (' + data.successCount + ' TX)', emailHtml);

  } else if (step === 'SLA_BREACH') {
    // 8. Cảnh báo quá hạn SLA
    const tgMsg = '⚠️ <b>[TAG PORTAL CẢNH BÁO] REQUEST QUÁ HẠN SLA!</b>\n\n'
      + '📌 <b>Mã Request:</b> <code>' + data.id + '</code>\n'
      + '🏢 <b>Team:</b> <b>' + data.team + '</b> | <b>Tag:</b> <code>' + data.tagName + '</code>\n'
      + '🚦 <b>Trạng thái đang nghẽn:</b> <b>' + data.state + '</b>\n'
      + '⏰ <b>Hạn SLA đã quá:</b> <b>' + data.deadline + '</b>\n\n'
      + '👉 <i>Đề nghị Approver phụ trách vào xử lý khẩn cấp:</i>\n'
      + '🔗 <a href="' + portalUrl + '"><b>TRUY CẬP PORTAL XỬ LÝ NGAY</b></a>';

    sendTelegramNotification(tgMsg);

    const emailRows = [
      ['Mã Request', '<b>' + data.id + '</b>'],
      ['Team Đề Xuất', data.team],
      ['Tên Tag', data.tagName],
      ['Trạng Thái Nghẽn', '<b style="color:#EF4444;">' + data.state + '</b>'],
      ['Hạn SLA Ban Đầu', '<b style="color:#EF4444;">' + data.deadline + '</b>']
    ];
    const emailHtml = buildEmailTemplate(
      '⚠️ Cảnh Báo Request Quá Hạn SLA: ' + data.id,
      'Cảnh báo: Request <b>' + data.id + '</b> đang bị quá hạn so với cam kết SLA dịch vụ nội bộ. Vui lòng kiểm tra và xử lý ngay.',
      emailRows,
      portalUrl
    );
    sendEmailNotification(data.targets, '[Tag Request Portal] ⚠️ Cảnh báo quá hạn SLA: ' + data.id + ' (' + data.state + ')', emailHtml);
  }
}

/**
 * Hàm kiểm thử hệ thống thông báo Telegram & Email (Chạy từ Apps Script Run)
 */
function testNotificationWorkflow() {
  const sample = {
    id: "REQ-TEST-" + Utilities.formatDate(new Date(), "GMT+7", "HHmm"),
    team: "S&P",
    name: "Khánh LP (Test)",
    submitterEmail: "khanhlp@ahamove.com",
    requestCategory: "Tạo tag mới",
    tagName: "TAG_TEST_NOTIFICATION_BOT",
    type: "Priority Dispatch",
    count: 100,
    reason: "Kiểm thử hệ thống thông báo tự động đa kênh Telegram & Email",
    duration: "2026-11-10",
    dueDate: "2026-11-15",
    deadlineLead: fmt(addHours(new Date(), 4))
  };

  Logger.log("--- BẮT ĐẦU KIỂM THỬ THÔNG BÁO ---");
  notifyWorkflowStep('NEW_REQUEST', sample);
  Logger.log("--- HOÀN TẤT KIỂM THỬ ---");
  return { status: "success", message: "Đã gửi bản tin kiểm thử đến Telegram và Email!" };
}
