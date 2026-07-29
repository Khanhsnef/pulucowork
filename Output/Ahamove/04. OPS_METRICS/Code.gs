/**
 * GOOGLE APPS SCRIPT BACKEND WITH DYNAMIC SPREADSHEET CONFIGURATION
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
    sheet.appendRow(["SUBMIT_BTN_TEXT", "🚀 Gửi Đề Xuất Tới DM Lead", "Tên nút gửi đề xuất"]);
    sheet.appendRow(["TEAM_LIST", "Business Operations, Marketing Campaign, Hub Linehaul Operations, Customer Service (CS), Risk & Fraud Control, Fleet Operations", "Danh sách các Team đề xuất (phân cách bằng dấu phẩy)"]);
    sheet.appendRow(["TAG_TYPES", "Priority Dispatch (Ưu tiên phát đơn), Incentive Campaign (Thưởng/Thách thức), Area Restriction (Giới hạn khu vực), Special Training (Đào tạo dịch vụ VIP), Penalty / Block (Khóa/Tạm dừng)", "Danh sách loại Tag (phân cách bằng dấu phẩy)"]);
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

function getSheetDataJson() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("01_ALL_TAG_REQUESTS");
  if (!sheet) {
    sheet = ss.insertSheet("01_ALL_TAG_REQUESTS");
    sheet.appendRow(["Mã Request", "Ngày Tạo", "Team Đề Xuất", "Người Đề Xuất", "Loại Tag", "Tên Tag Yêu Cầu", "Số Lượng TX", "Lý Do", "Thời Gian", "DM Reviewer", "Ngày DM Review", "DM Quyết Định", "DM Note", "DM Tag Code", "QM Handover", "QM Specialist", "Ngày QM Nhận", "QM Trạng Thái Add Tag", "Ngày Add Tag Xong", "Số TX Add Thành Công", "Ghi Chú QM"]);
  }
  
  const rows = sheet.getDataRange().getValues();
  if (rows.length <= 1) return [];
  
  const cleanData = [];
  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (r[0] && r[0].toString().startsWith("REQ-")) {
      cleanData.push({
        id: r[0], date: r[1], team: r[2], name: r[3], type: r[4], tagName: r[5],
        count: r[6], reason: r[7], duration: r[8], dmReviewer: r[9]||"-", dmReviewDate: r[10]||"-",
        dmDecision: r[11] || 'PENDING', dmNote: r[12] || '', dmTagCode: r[13] || '-',
        qmHandover: r[14]||'HOLD', qmStatus: r[17] || 'PENDING_QM',
        qmSuccessCount: r[19] || 0, qmRef: r[20] || ''
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
    sheet.appendRow(["Mã Request", "Ngày Tạo", "Team Đề Xuất", "Người Đề Xuất", "Loại Tag", "Tên Tag Yêu Cầu", "Số Lượng TX", "Lý Do", "Thời Gian", "DM Reviewer", "Ngày DM Review", "DM Quyết Định", "DM Note", "DM Tag Code", "QM Handover", "QM Specialist", "Ngày QM Nhận", "QM Trạng Thái Add Tag", "Ngày Add Tag Xong", "Số TX Add Thành Công", "Ghi Chú QM"]);
  }
  
  sheet.appendRow([
    data.id, data.date, data.team, data.name, data.type, data.tagName, data.count, data.reason, data.duration,
    "-", "-", data.dmDecision, data.dmNote, data.dmTagCode, data.qmHandover,
    "-", "-", data.qmStatus, "-", data.qmSuccessCount, data.qmRef
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
      sheet.getRange(rowIdx, 10).setValue("Trần Lead DM");
      sheet.getRange(rowIdx, 11).setValue(nowStr);
      sheet.getRange(rowIdx, 12).setValue(decision);
      sheet.getRange(rowIdx, 13).setValue(note);
      sheet.getRange(rowIdx, 14).setValue(tagCode);
      sheet.getRange(rowIdx, 15).setValue(decision === "APPROVED" ? "READY_FOR_QM" : "CANCELLED");
      if (decision === "APPROVED") {
        sheet.getRange(rowIdx, 18).setValue("PROCESSING");
      } else {
        sheet.getRange(rowIdx, 18).setValue("N/A");
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
      sheet.getRange(rowIdx, 16).setValue("QM Specialist");
      if (!sheet.getRange(rowIdx, 17).getValue() || sheet.getRange(rowIdx, 17).getValue() === "-") {
        sheet.getRange(rowIdx, 17).setValue(nowStr);
      }
      sheet.getRange(rowIdx, 18).setValue(status);
      if (status === "TAGGED_SUCCESS") {
        sheet.getRange(rowIdx, 19).setValue(nowStr);
      }
      sheet.getRange(rowIdx, 20).setValue(successCount);
      sheet.getRange(rowIdx, 21).setValue(ref);
      break;
    }
  }
  return { status: "success" };
}
