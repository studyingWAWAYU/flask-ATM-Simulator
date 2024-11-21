function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}
document.addEventListener('DOMContentLoaded',function(){
    var customUpload = document.getElementById('custom_upload')
    var uploadImage = document.getElementById('uploadImg');

    customUpload.addEventListener('click',function(){
        uploadImage.click();
    });
});