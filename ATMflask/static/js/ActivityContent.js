function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}

function confirmDelete(event){
    event.preventDefault();
    console.log("Delete button clicked");
    var confirmation = confirm("Are you sure to delete this activity? All related data will be removed!")
    if(confirmation){
        document.getElementById('deleteForm').submit();
    }
}

