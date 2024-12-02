//增加参与者
document.getElementById('add-participant-btn').addEventListener('click', function() {
        const userId = prompt('Enter User ID:');

        fetch('/addParticipant', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId})
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);  // 显示成功消息
                location.reload();  // 刷新页面
            } else if (data.error) {
                alert(data.error);  // 显示错误消息
            }
        })
    })

// 更新状态
document.addEventListener("DOMContentLoaded", function() {
    // 获取所有的状态选择框
    const statusDropdowns = document.querySelectorAll('.status-dropdown');

    // 循环处理每个状态选择框
    statusDropdowns.forEach(dropdown => {
        const status = dropdown.value;  // 获取当前状态
        const userId = dropdown.dataset.userId;  // 获取用户ID

        // 根据当前状态在选择框中设定默认值
        for (let i = 0; i < dropdown.options.length; i++) {
            if (dropdown.options[i].value === status) {
                dropdown.options[i].selected = true;
                break;
            }
        }

        // 监听状态变化
        dropdown.addEventListener('change', function() {
            const status = this.value;  // 获取选择的新状态

            // 发送POST请求更新状态到后端
            fetch('/updateStatus', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    status: status,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // 状态更新成功，显示提示
                    location.reload();  // 刷新页面
                } else {
                    alert(data.error);  // 如果失败，显示错误信息
                }
            })
        });
    });
});


// 删除参与者
const deleteButtonsNew = document.querySelectorAll('.delete-btn');
    deleteButtonsNew.forEach(button => {
        button.addEventListener('click', function() {
            // 弹出确认框
            const confirmation = confirm("Are you sure you want to delete this participant?");
            if (!confirmation) {
                return;  // 如果管理员取消删除，则返回
            }

            const userId = this.dataset.userId;
            fetch('/deleteParticipant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId })
            })
            .then(response => response.json())
            .then(data => {
            alert(data.message);
            location.reload();
            });
        });
    })
