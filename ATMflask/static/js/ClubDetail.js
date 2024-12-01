// 确认删除社团的功能
function confirmDelete(event, club_id) {
    // 弹出确认框
    if (confirm("Are you sure you want to delete this club? This action cannot be undone.")) {
        // 用户确认后提交删除请求
        window.location.href = "/DeleteClub/" + club_id;
    } else {
        // 用户取消
        event.preventDefault();
    }
}

//保存
// 提交前弹出确认框
function confirmSave(event) {
    event.preventDefault();  // 防止表单默认提交

    // 显示确认框
    var confirmAction = confirm("Are you sure you want to save changes?");

    // 如果用户点击确认，提交表单
    if (confirmAction) {
        document.getElementById('editClubForm').submit();
    }
}
