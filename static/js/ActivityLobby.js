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
  // 你可以根据选中的活动类型和状态去处理显示相关内容
  console.log(`Selected ${category}: ${activity}`);
}

