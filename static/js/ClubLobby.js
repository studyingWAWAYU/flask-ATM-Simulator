function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}
// 获取输入框元素
const searchInput = document.getElementById('search-input');
// 监听输入框的焦点事件
searchInput.addEventListener('focus', function() {
    // 当获取焦点时，宽度自动变长
    searchInput.style.width = '300px';
});
// 监听输入框的输入事件
searchInput.addEventListener('input', function() {
    // 如果有输入内容，恢复原始宽度
    if (searchInput.value.length > 0) {
        searchInput.style.width = '400px';  // 可根据输入内容动态调整宽度
    } else {
        searchInput.style.width = '84%';  // 如果输入框为空，则恢复原宽度
    }
});
// 监听失去焦点事件
searchInput.addEventListener('blur', function() {
    // 失去焦点时，恢复原来的宽度
    if (searchInput.value.length === 0) {
        searchInput.style.width = '400px';  // 没有输入内容时恢复
    }
});