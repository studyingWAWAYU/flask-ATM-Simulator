function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}
function showActivities(activity, category) {
  // 根据类别选择按钮：`type` 或 `status`
  let buttons;
  if (category === 'type') {
    buttons = document.querySelectorAll('.type-btn');
  } else if (category === 'status') {
    buttons = document.querySelectorAll('.status-btn');
  }
  // 移除所有按钮的选中状态
  buttons.forEach(function(button) {
    button.classList.remove('selected');
  });
  // 为点击的按钮添加选中状态
  event.target.classList.add('selected');
  // 可以根据选中的活动类型和状态去处理显示相关内容
  console.log(`Selected ${category}: ${activity}`);
}

