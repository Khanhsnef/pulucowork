/**
 * GOOGLE APPS SCRIPT BACKEND WITH AUTOMATIC DM BYPASS FOR ADD TAG REQUESTS
 * Spreadsheet Target ID: 1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4
 */

function doGet(e) {
  const template = HtmlService.createTemplateFromFile("Index");
  template.config = getAppConfig();
  return template.evaluate()
    .setTitle(template.config.APP_TITLE || "Tag Request Portal")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getAppConfig() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("00_CONFIG_SETTINGS");
  if (!sheet) {
    sheet = ss.insertSheet("00_CONFIG_SETTINGS", 0);
    sheet.appendRow(["Mã Cấu Hình (Key)", "Nội Dung Hiển Thị (Value)", "Hướng Dẫn"]);
    sheet.appendRow(["APP_TITLE", "Tag Request Portal", "Tiêu đề ứng dụng"]);
    sheet.appendRow(["FORM_TITLE", "Biểu Mẫu Tạo Yêu Cầu Tag Tài Xế Cho Phía DM", "Tiêu đề biểu mẫu tạo request"]);
    sheet.appendRow(["TAB1_NAME", "📝 Bước 1: Request", "Tên Tab 1"]);
    sheet.appendRow(["TAB2_NAME", "🛡️ Bước 2: DM Review", "Tên Tab 2"]);
    sheet.appendRow(["TAB3_NAME", "⚙️ Bước 3: QM Add Tags", "Tên Tab 3"]);
    sheet.appendRow(["TAB4_NAME", "📊 Master Request Tracker", "Tên Tab 4"]);
    sheet.appendRow(["SUBMIT_BTN_TEXT", "🚀 Gửi Đề Xuất Tới DM Lead", "Tên nút gửi"]);
    sheet.appendRow(["TEAM_LIST", "Business Operations, Marketing Campaign, Hub Linehaul Operations, Customer Service (CS), Risk & Fraud Control, Fleet Operations", "Danh sách Team"]);
    sheet.appendRow(["TAG_TYPES", "Priority Dispatch (Ưu tiên phát đơn), Incentive Campaign (Thưởng/Thách thức), Area Restriction (Giới hạn khu vực), Special Training (Đào tạo dịch vụ VIP), Penalty / Block (Khóa/Tạm dừng)", "Danh sách loại Tag"]);
  }
  
  const rows = sheet.getDataRange().getValues();
  const config = {};
  for (let i = 1; i < rows.length; i++) {
    const key = rows[i][0];
    const val = rows[i][1];
    if (key) config[key] = val;
  }
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

function getSheetDataJson() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("01_ALL_TAG_REQUESTS");
  if (!sheet) {
    sheet = ss.insertSheet("01_ALL_TAG_REQUESTS");
    sheet.appendRow(["Mã Request", "Ngày Tạo", "Hình Thức", "Team Đề Xuất", "Người Đề Xuất", "Loại Tag", "Tên Tag Yêu Cầu", "Nguồn Danh Sách TX", "Số Lượng TX", "Lý Do", "Thời Gian", "DM Reviewer", "Ngày DM Review", "DM Quyết Định", "DM Note", "DM Tag Code", "QM Handover", "QM Specialist", "Ngày QM Nhận", "QM Trạng Thái Add Tag", "Ngày Add Tag Xong", "Số TX Add Thành Công", "Ghi Chú QM"]);
  }
  
  const rows = sheet.getDataRange().getValues();
  if (rows.length <= 1) return [];
  
  const cleanData = [];
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (r[0] && r[0].toString().startsWith("REQ-")) {
      cleanData.push({
        id: r[0], date: r[1], requestCategory: r[2] || 'Tạo tag mới',
        team: r[3], name: r[4], type: r[5], tagName: r[6],
        driverListSource: r[7] || '-', count: r[8], reason: r[9], duration: r[10],
        dmReviewer: r[11]||"-", dmReviewDate: r[12]||"-",
        dmDecision: r[13] || 'PENDING', dmNote: r[14] || '', dmTagCode: r[15] || '-',
        qmHandover: r[16]||'HOLD', qmStatus: r[19] || 'PENDING_QM',
        qmSuccessCount: r[21] || 0, qmRef: r[22] || ''
      });
    }
  }
  return cleanData;
}

function saveNewRequest(data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("01_ALL_TAG_REQUESTS");
  if (!sheet) {
    sheet = ss.insertSheet("01_ALL_TAG_REQUESTS");
    sheet.appendRow(["Mã Request", "Ngày Tạo", "Hình Thức", "Team Đề Xuất", "Người Đề Xuất", "Loại Tag", "Tên Tag Yêu Cầu", "Nguồn Danh Sách TX", "Số Lượng TX", "Lý Do", "Thời Gian", "DM Reviewer", "Ngày DM Review", "DM Quyết Định", "DM Note", "DM Tag Code", "QM Handover", "QM Specialist", "Ngày QM Nhận", "QM Trạng Thái Add Tag", "Ngày Add Tag Xong", "Số TX Add Thành Công", "Ghi Chú QM"]);
  }

  // Luồng xử lý: Nếu "Add tag" -> Tự động Bypass DM Review, chuyển thẳng cho QM
  let isAddTag = (data.requestCategory === 'Add tag');
  let dmDec = isAddTag ? 'AUTO_BYPASS' : 'PENDING';
  let dmNote = isAddTag ? 'Tự động duyệt (Add Tag trực tiếp chuyển QM)' : 'Đang chờ DM Lead kiểm duyệt';
  let dmCode = isAddTag ? (data.tagName || 'DM_ADD_TAG_DIRECT') : '-';
  let qmHandover = isAddTag ? 'READY_FOR_QM' : 'HOLD';
  let qmStatus = isAddTag ? 'PENDING_QM' : 'HOLD';

  sheet.appendRow([
    data.id, data.date, data.requestCategory, data.team, data.name, data.type, data.tagName,
    data.driverListSource, data.count, data.reason, data.duration,
    isAddTag ? "System (Auto)" : "-", isAddTag ? data.date : "-",
    dmDec, dmNote, dmCode, qmHandover,
    "-", "-", qmStatus, "-", 0, isAddTag ? `Nguồn TX: ${data.driverListSource}` : "Chờ DM duyệt"
  ]);
  return { status: "success" };
}

function saveDMReview(reqId, decision, note, tagCode) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("01_ALL_TAG_REQUESTS");
  const rows = sheet.getDataRange().getValues();
  const nowStr = Utilities.formatDate(new Date(), "GMT+7", "yyyy-MM-dd HH:mm");
  
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === reqId) {
      const rowIdx = i + 1;
      sheet.getRange(rowIdx, 12).setValue("Trần Lead DM");
      sheet.getRange(rowIdx, 13).setValue(nowStr);
      sheet.getRange(rowIdx, 14).setValue(decision);
      sheet.getRange(rowIdx, 15).setValue(note);
      sheet.getRange(rowIdx, 16).setValue(tagCode);
      sheet.getRange(rowIdx, 17).setValue(decision === "APPROVED" ? "READY_FOR_QM" : "CANCELLED");
      if (decision === "APPROVED") {
        sheet.getRange(rowIdx, 20).setValue("PENDING_QM");
      } else {
        sheet.getRange(rowIdx, 20).setValue("N/A");
      }
      break;
    }
  }
  return { status: "success" };
}

function saveQMStatus(reqId, status, successCount, ref) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("01_ALL_TAG_REQUESTS");
  const rows = sheet.getDataRange().getValues();
  const nowStr = Utilities.formatDate(new Date(), "GMT+7", "yyyy-MM-dd HH:mm");
  
  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] === reqId) {
      const rowIdx = i + 1;
      sheet.getRange(rowIdx, 18).setValue("QM Specialist");
      if (!sheet.getRange(rowIdx, 19).getValue() || sheet.getRange(rowIdx, 19).getValue() === "-") {
        sheet.getRange(rowIdx, 19).setValue(nowStr);
      }
      sheet.getRange(rowIdx, 20).setValue(status);
      if (status === "TAGGED_SUCCESS") {
        sheet.getRange(rowIdx, 21).setValue(nowStr);
      }
      sheet.getRange(rowIdx, 22).setValue(successCount);
      sheet.getRange(rowIdx, 23).setValue(ref);
      break;
    }
  }
  return { status: "success" };
}
