/**
 * GOOGLE APPS SCRIPT BACKEND FOR DM & QM TAG MANAGEMENT WEB APP
 * Spreadsheet Target ID: 1tsoIAEisTLiIkeqCJ7NMwrpNRhlXRbYrWpN3mb6xrE4
 */

function doGet(e) {
  return HtmlService.createTemplateFromFile("Index")
    .evaluate()
    .setTitle("Hệ Thống Quản Lý & Đề Xuất Tag Tài Xế | DM & QM Portal")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
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
      sheet.getRange(rowIdx, 10).setValue("Trần Lead DM"); // DM Reviewer
      sheet.getRange(rowIdx, 11).setValue(nowStr);        // Review Date
      sheet.getRange(rowIdx, 12).setValue(decision);      // DM Decision
      sheet.getRange(rowIdx, 13).setValue(note);          // DM Note
      sheet.getRange(rowIdx, 14).setValue(tagCode);       // DM Tag Code
      sheet.getRange(rowIdx, 15).setValue(decision === "APPROVED" ? "READY_FOR_QM" : "CANCELLED"); // QM Handover
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
      sheet.getRange(rowIdx, 16).setValue("QM Specialist"); // QM User
      if (!sheet.getRange(rowIdx, 17).getValue() || sheet.getRange(rowIdx, 17).getValue() === "-") {
        sheet.getRange(rowIdx, 17).setValue(nowStr); // QM Received Date
      }
      sheet.getRange(rowIdx, 18).setValue(status);
      if (status === "TAGGED_SUCCESS") {
        sheet.getRange(rowIdx, 19).setValue(nowStr); // Finish Date
      }
      sheet.getRange(rowIdx, 20).setValue(successCount);
      sheet.getRange(rowIdx, 21).setValue(ref);
      break;
    }
  }
  return { status: "success" };
}
