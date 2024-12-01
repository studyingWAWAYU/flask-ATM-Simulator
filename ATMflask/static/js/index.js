
var index=1;
function carousel(){
    var obj = document.getElementById("alternatePlay");
    index++;
    if(index>4){
        index=1;
        obj.src="../static/img/index/club1.png";
    }else if(index<1) {
        index = 4;
        obj.src = "../static/img/index/club4.png";
    }else {
        obj.src = "../static/img/index/club" + index + ".png";
    }
}
window.onload=function(){
    t = setInterval("carousel()",1700);
}
function stopAndContinue(){
    if(t){
        clearInterval(t);
        t = null;
    }else{
        t = setInterval("carousel()",1700);
    }
}
function preimg(){
    index-=2;
    carousel();
}
function nextimg(){
    carousel();
}

function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}