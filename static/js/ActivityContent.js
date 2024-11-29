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

var idx = 0;
var t = null;
var totalImgs = 0;
var imgPaths = [];

window.onload=function(){
    imgs = document.querySelectorAll(".act-imgs");
    totalImgs = imgs.length;
    imgs.forEach( function(img) {imgPaths.push(img.src);} );
    t = setInterval(carousel,2000);
    //console.log("Total images: " + totalImgs);
   // console.log(imgPaths)
}

function carousel(){
    idx ++;
    if(idx >= totalImgs){ idx = 0;  }
    if(idx < 0){ idx = totalImgs -1; }
    var obj = document.getElementById("act-img");
    obj.src = imgPaths[idx];
}

function stopAndContinue(){
    if(t){
        clearInterval(t);
        t = null;
    }else{
        t = setInterval(carousel,2000);
    }
}

function preimg(){
    idx-=2;
    if (idx < 0) {
        idx = totalImgs - 1;
    }
    carousel();
}
function nextimg(){
    carousel();
}
