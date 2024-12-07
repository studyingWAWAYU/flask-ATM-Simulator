function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}
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

// 加入社团
document.addEventListener("DOMContentLoaded", () => {
    const joinClubButton = document.getElementById('join-club-btn');
    const club_id = joinClubButton.dataset.clubId;

    if (joinClubButton){
        joinClubButton.addEventListener('click', function () {
            // 弹出确认框
            const confirmation = confirm("Do you want to join this club now?");
            if (!confirmation) {
                return;
            }
            fetch(`/joinClub/`+ club_id, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({club_id: club_id}) // 可以扩展传递的数据结构
                })
                .then(response => {
                    // 如果后端返回的是 HTML 页面，则使用 DOM 操作来更新页面内容
                    return response.text();
                })
                .then(html => {
                    // 将返回的 HTML 插入到页面中
                    document.open();
                    document.write(html);
                    document.close();
                })
                .catch(error => {
                alert('There was a problem with your request: ' + error.message);
                });
        });
    }
});

// 退出社团
document.addEventListener("DOMContentLoaded", () => {
    const quitClubButton = document.getElementById('quit-club-btn');
    const club_id = quitClubButton.dataset.clubId;
    if (quitClubButton){
        quitClubButton.addEventListener('click', function () {
            // 弹出确认框
            const confirmation = confirm("Are you sure to quit this club?");
            if (!confirmation) {
                return;
            }
            fetch(`/quitClub/` + club_id, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({club_id: club_id}) // 可以扩展传递的数据结构
                })
                .then(response => {
                    // 如果后端返回的是 HTML 页面，则使用 DOM 操作来更新页面内容
                    return response.text();
                })
                .then(html => {
                    // 将返回的 HTML 插入到页面中
                    document.open();
                    document.write(html);
                    document.close();
                })
                .catch(error => {
                alert('There was a problem with your request: ' + error.message);
                });
        });
    }
});