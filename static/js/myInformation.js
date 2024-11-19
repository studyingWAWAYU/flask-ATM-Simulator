function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}
function confirmChange(event) {
    var confirmation = confirm("Are you sure you want to submit changes?");
    if (confirmation) {
        event.target.form.submit();
    } else {
        event.preventDefault();
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var currentGender = document.getElementById("currentGender").value;
    var genderSelect = document.getElementById("gender");
    for (var i = 0; i < genderSelect.options.length; i++) {
        if (genderSelect.options[i].value === currentGender) {
            genderSelect.options[i].selected = true;
            break;
        }
    }
});