function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
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

function showAvatars(){
    // 获取所有class=“avatar”的元素
    const avatars = document.querySelectorAll('.avatar');
    const largeAvatar = document.getElementById('largeAvatar');
    const hiddenInput = document.getElementById('selectedAvatar');

    // Add event listener for each avatar
    avatars.forEach(avatar => {
        avatar.addEventListener('click', function() {
            // Remove 'selected' class from all avatars
            avatars.forEach(item => item.classList.remove('selected'));

            // Add 'selected' class to the clicked avatar
            this.classList.add('selected');

            // Change the large avatar to the selected one
            largeAvatar.src = this.getAttribute('src');
            hiddenInput.value = this.getAttribute('src');
        });
    });
}

