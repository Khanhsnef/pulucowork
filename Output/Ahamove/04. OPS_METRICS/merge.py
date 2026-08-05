import re

with open("2026-07-dm-qm-tag-request-manager.html", "r") as f:
    html = f.read()

# 1. Update <title>
html = re.sub(r"<title>.*?</title>", "<title><?= (typeof config !== \"undefined\" && config.APP_TITLE) ? config.APP_TITLE : \"Tag Request Portal\" ?></title>", html)

# 2. Add IS_LOCAL constant at the top of <script>
html = html.replace("<script>", "<script>\n    const IS_LOCAL = typeof google === \"undefined\";\n")

# 3. Add loadDataFromSheet() which replaces mockData() if not IS_LOCAL
load_data_func = """
    // ===== LOAD DATA =====
    function loadDataFromSheet() {
      if (!IS_LOCAL) {
        google.script.run.withSuccessHandler(res => {
          if (res && res.data) {
            requestsData = res.data;
            if (res.role) { CURRENT_ROLE = res.role; CURRENT_EMAIL = res.email || CURRENT_EMAIL; applyRBAC(); }
          } else {
            requestsData = res || [];
          }
          renderAll();
        }).getSheetDataJson();
      } else {
        if (requestsData.length === 0) requestsData = mockData();
        renderAll();
      }
    }
    function applyRBAC() {
       // Since the new UI doesn't have the tab hiding by role in the demo, 
       // but does have updateRolePill(), we just call that.
       updateRolePill();
    }
"""
html = html.replace("document.addEventListener(\"DOMContentLoaded\", () => {", load_data_func + "\n    document.addEventListener(\"DOMContentLoaded\", () => {")
html = html.replace("requestsData = mockData();", "loadDataFromSheet();")

submit_orig = """      const newReq = {
        id: newId, date: timeStr, requestCategory: category,
        team: document.getElementById('req-team').value, name: document.getElementById('req-name').value,
        type: document.getElementById('req-type').value, tagName: document.getElementById('req-tag-name').value,
        driverListSource: isAddTag ? `[${dsType}] ${dsVal}` : '-', reason: document.getElementById('req-reason').value,
        duration: duration, dueDate: document.getElementById('req-deadline').value || '-',
        state:'PENDING_TEAM_LEAD', leadDecision:'PENDING', dmDecision:'PENDING', qmStatus:'HOLD', qmSuccessCount:0, qmRef:'', dmTagCode:'-', breach:''
      };
      requestsData.unshift(newReq);
      renderAll();
      document.getElementById('tag-request-form').reset();
      selectRequestCategory('Tạo tag mới');
      switchTab('tab-master');
      showToast(`Đã gửi ${newId}`, 'Request về Master, đang chờ Lead/Head duyệt. [DEMO]', 'ok');"""
submit_new = """      const newReq = {
        id: newId, date: timeStr, requestCategory: category,
        team: document.getElementById('req-team').value, name: document.getElementById('req-name').value,
        type: document.getElementById('req-type').value, tagName: document.getElementById('req-tag-name').value,
        driverListSource: isAddTag ? `[${dsType}] ${dsVal}` : '-', reason: document.getElementById('req-reason').value,
        duration: duration, dueDate: document.getElementById('req-deadline').value || '-',
        state:'PENDING_TEAM_LEAD', leadDecision:'PENDING', dmDecision:'PENDING', qmStatus:'HOLD', qmSuccessCount:0, qmRef:'', dmTagCode:'-', breach:''
      };
      if (!IS_LOCAL) {
        google.script.run.withSuccessHandler(() => {
          showToast(`Đã gửi ${newId}`, 'Request về Master, đang chờ Lead/Head duyệt.', 'ok');
          loadDataFromSheet();
          document.getElementById('tag-request-form').reset();
          selectRequestCategory('Tạo tag mới');
          switchTab('tab-master');
        }).saveNewRequest(newReq);
      } else {
""" + submit_orig.replace('const newReq = {', 'const _ = {') + "\n      }"
html = html.replace(submit_orig, submit_new)
html = html.replace(submit_orig, submit_new)

# 5. leadApprove
lead_orig = """      r.leadDecision = 'APPROVED'; r.leadApprover = CURRENT_EMAIL; r.breach = '';
      if (r.requestCategory === 'Add tag') { r.state = 'PENDING_QM'; r.dmDecision = 'SKIPPED'; r.qmStatus = 'PENDING_QM'; if (!r.dmTagCode || r.dmTagCode==='-') r.dmTagCode = r.tagName; }
      else { r.state = 'PENDING_DM'; }
      renderAll();
      showToast('Lead đã duyệt ' + id, r.requestCategory === 'Add tag' ? 'Bỏ qua DM → chuyển thẳng QM. [DEMO]' : 'Chuyển sang DM Review. [DEMO]', 'ok');"""
lead_new = """      if (!IS_LOCAL) {
        google.script.run.withSuccessHandler((res) => {
          if (res && res.status === 'error') { showToast('Không thể lưu', res.message, 'err'); return; }
          showToast('Lead đã duyệt ' + id, r.requestCategory === 'Add tag' ? 'Bỏ qua DM → chuyển thẳng QM.' : 'Chuyển sang DM Review.', 'ok');
          loadDataFromSheet();
        }).saveLeadApproval(id, 'APPROVED', '');
      } else {
""" + lead_orig + "\n      }"
html = html.replace(lead_orig, lead_new)

# 6. submitDMApprove
dm_orig = """      r.dmDecision = 'APPROVED'; r.dmTagCode = tagCode; r.dmNote = document.getElementById('modal-dm-note').value;
      r.state = 'PENDING_QM'; r.qmStatus = 'PENDING_QM'; r.breach = '';
      renderAll(); closeModal('dm-modal');
      showToast('DM đã duyệt ' + r.id, 'Gán mã ' + tagCode + ' → chuyển QM. [DEMO]', 'ok');"""
dm_new = """      const note = document.getElementById('modal-dm-note').value;
      if (!IS_LOCAL) {
        google.script.run.withSuccessHandler((res) => {
          if (res && res.status === 'error') { showToast('Không thể lưu', res.message, 'err'); return; }
          showToast('DM đã duyệt ' + r.id, 'Gán mã ' + tagCode + ' → chuyển QM.', 'ok');
          loadDataFromSheet(); closeModal('dm-modal');
        }).saveDMReview(dmCtx.id, 'APPROVED', note, tagCode);
      } else {
""" + dm_orig + "\n      }"
html = html.replace(dm_orig, dm_new)

# 7. submitReject
rej_orig = """      if (rejectCtx.gate === 'LEAD') { r.leadDecision = 'REJECTED'; r.leadApprover = CURRENT_EMAIL; r.leadNote = note; }
      else { r.dmDecision = 'REJECTED'; r.dmNote = note; }
      r.state = 'REJECTED'; r.qmStatus = 'N/A'; r.breach = '';
      renderAll(); closeModal('reject-modal');
      showToast('Đã từ chối ' + r.id, 'Requester sẽ thấy lý do để chỉnh sửa. [DEMO]', 'warn');"""
rej_new = """      if (!IS_LOCAL) {
        const fn = (rejectCtx.gate === 'LEAD')
          ? (cb) => google.script.run.withSuccessHandler(cb).saveLeadApproval(rejectCtx.id, 'REJECTED', note)
          : (cb) => google.script.run.withSuccessHandler(cb).saveDMReview(rejectCtx.id, 'REJECTED', note, 'N/A');
        fn((res) => {
          if (res && res.status === 'error') { showToast('Không thể lưu', res.message, 'err'); return; }
          showToast('Đã từ chối ' + r.id, 'Requester sẽ thấy lý do để chỉnh sửa.', 'warn');
          loadDataFromSheet(); closeModal('reject-modal');
        });
      } else {
""" + rej_orig + "\n      }"
html = html.replace(rej_orig, rej_new)

# 8. qmSave
qm_orig = """      r.qmStatus = status;
      if (status === 'TAGGED_SUCCESS') { r.state = 'DONE'; r.breach = ''; r.qmSuccessCount = r.count || r.qmSuccessCount || 0; showToast('Hoàn thành ' + id, `Đã đánh dấu DONE. [DEMO]`, 'ok'); }
      else showToast('Đã cập nhật ' + id, 'Trạng thái QM: ' + status + '. [DEMO]', 'ok');
      renderAll();"""
qm_new = """      const count = 0;
      if (!IS_LOCAL) {
        google.script.run.withSuccessHandler((res) => {
          if (res && res.status === 'error') { showToast('Không thể lưu', res.message, 'err'); return; }
          if (status === 'TAGGED_SUCCESS') showToast('Hoàn thành ' + id, `Đã đánh dấu DONE.`, 'ok');
          else showToast('Đã cập nhật ' + id, 'Trạng thái QM: ' + status + '.', 'ok');
          loadDataFromSheet();
        }).saveQMStatus(id, status, count, 'QM Updated');
      } else {
""" + qm_orig + "\n      }"
html = html.replace(qm_orig, qm_new)

# Clean up Demo header banner
html = re.sub(r"<div class=\"demo-banner\">.*?</div>", "", html, flags=re.DOTALL)

with open("Index.html", "w") as f:
    f.write(html)

print("Done")
