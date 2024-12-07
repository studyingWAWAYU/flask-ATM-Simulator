function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}

/*删除活动*/
function confirmDelete(event){
    event.preventDefault();
    console.log("Delete button clicked");
    var confirmation = confirm("Are you sure to delete this activity? All related data will be removed!")
    if(confirmation){
        document.getElementById('deleteForm').submit();
    }
}

/*报名*/
document.addEventListener("DOMContentLoaded", function() {
    const signupBtn = document.getElementById("sup-btn");
    if (signupBtn) {
        signupBtn.addEventListener("click", function(event) {
            event.preventDefault();
            const parStatus = signupBtn.textContent.trim();
            if (parStatus === "Registered" || parStatus === "Confirmed" || parStatus === "Present" || parStatus === "Absent") {
                return;
            }

            // 弹出确认框
            const confirmation = confirm("Are you sure you want to sign up for this activity?");
            if (!confirmation) {
                return;  // 如果用户取消报名，直接返回
            }

            // 获取活动 ID 和用户 ID 从页面中的 hidden input 或其他元素
            const activityId = document.getElementById('activity-id').value;  // 获取活动 ID
            const userId = document.getElementById('user-id').value;  // 获取用户 ID

            if (!userId) {
                // 如果用户未登录，提示并跳转到登录页面
                alert("Please log in first to sign up for the activity.");
                window.location.href = "/Login";  // 跳转到登录页面
                return;
            }

            // 向后端发送报名请求
            fetch('/applyAct', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: userId,
                    activityId: activityId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("You have successfully signed up!");
                    signupBtn.textContent = "Registered";  // 更新按钮状态
                    const remainingCount = document.getElementById("rem-participants");
                    remainingCount.textContent = data.remaining;  // 更新剩余名额
                    location.reload();  // 刷新页面
                } else {
                    alert(data.message);  // 显示错误信息
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred. Please try again later.");
            });
        });
    }
});

/*发布签到码*/
document.addEventListener('DOMContentLoaded', function () {
    const postSigninCodeBtn = document.getElementById('post-signin-code-btn');
    const activity_id = postSigninCodeBtn.dataset.activityId;
    if (postSigninCodeBtn) {
        postSigninCodeBtn.addEventListener('click', function(event) {
            event.preventDefault();

            const signinCode = prompt('Enter a 6-digit sign-in code:');

            // Validate if the input is a 6-digit number
            if (!/^\d{6}$/.test(signinCode)) {
                alert('Sign-in code invalid.');
                return;
            }
            fetch('/postSigninCode/'+activity_id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ signin_code: signinCode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // Show success message
                    location.reload();  // Reload the page to reflect changes
                }
            });
        });
    }
});

/*签到*/
document.addEventListener('DOMContentLoaded', function () {
    const SigninBtn = document.getElementById('signin-btn');
    const activity_id = SigninBtn.dataset.activityId;
    if (SigninBtn) {
        SigninBtn.addEventListener('click', function(event) {
            event.preventDefault();
            // 弹出提示框让用户输入签到码
            const signinCode = prompt('Enter a 6-digit sign-in code:');

            // 校验签到码是否是6位数字
            if (!/^\d{6}$/.test(signinCode)) {
                alert('Incorrect sign-in code.');
                return;
            }

            // 发送请求到后端
            fetch('/signin/'+activity_id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ new_signin_code: signinCode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);  // 显示成功消息
                    location.reload();  // 刷新页面
                } else if (data.error) {
                    alert(data.error);  // 显示错误消息
                    location.reload();  // 刷新页面
                }
            });
        });
    }
});


/*活动轮播图*/
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
