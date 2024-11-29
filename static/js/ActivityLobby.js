function confirmLogout(event) {
    event.preventDefault();  // 阻止默认行为，即阻止直接跳转
    const isConfirmed = confirm("Are you sure you want to log out?");
    if (isConfirmed) {
        window.location.href = event.target.href;  // 如果确认，执行登出操作
        document.getElementById("logoutForm").submit();
    }
}

console.log(document.getElementById('show-btn'));

//筛选按钮样式切换
let selectedType = null;
let selectedStatus = null;
function toggleSelection(button, category) {
    const buttons = document.querySelectorAll(`.${category}-btn`);
    //移除选中的样式
    buttons.forEach(btn => { btn.classList.remove('selected'); });
    //切换按钮状态
    if(!button.classList.contains('selected')){     //切换到选中
        button.classList.add('selected');
        if (category === 'type') {
            selectedType = button.value;    //保存用户选择的type
        } else if (category === 'status') {
            selectedStatus = button.value;      //保存用户选择的status
        }
    }else{
        button.classList.remove('selected');
        if(category === 'type'){
            selectedType = null;
        }else if(category === 'status'){
            selectedStatus = null;
        }
    }
    console.log(selectedType,selectedStatus)

}


//点击apply时，将选择的type和status传给后端

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOMContentLoaded event triggered");
    showBtn = document.getElementById('show-btn')
    const form = document.getElementById('filter-form');

    showBtn.addEventListener('click', function(event){
        event.preventDefault();

        const typeInput = document.createElement('input');
        typeInput.type = 'hidden';
        typeInput.name = 'type';
        typeInput.value = selectedType || '';  //没有选择type就传空值
        form.appendChild(typeInput);

        const statusInput = document.createElement('input');
        statusInput.type = 'hidden';
        statusInput.name = 'status';
        statusInput.value = selectedStatus || '';  //没有选择status就传空值
        form.appendChild(statusInput);


        // 获取日期选择器的值并作为隐藏字段传递
        const signupStart = document.getElementById('signup_start').value;
        const signupEnd = document.getElementById('signup_end').value;
        const startTime = document.getElementById('start_time').value;
        const endTime = document.getElementById('end_time').value;

        const signupStartInput = document.createElement('input');
        signupStartInput.type = 'hidden';
        signupStartInput.name = 'signup_start';
        signupStartInput.value = signupStart;
        form.appendChild(signupStartInput);

        const signupEndInput = document.createElement('input');
        signupEndInput.type = 'hidden';
        signupEndInput.name = 'signup_end';
        signupEndInput.value = signupEnd;
        form.appendChild(signupEndInput);

        const startTimeInput = document.createElement('input');
        startTimeInput.type = 'hidden';
        startTimeInput.name = 'start_time';
        startTimeInput.value = startTime;
        form.appendChild(startTimeInput);

        const endTimeInput = document.createElement('input');
        endTimeInput.type = 'hidden';
        endTimeInput.name = 'end_time';
        endTimeInput.value = endTime;
        form.appendChild(endTimeInput);

        //把按钮的值action==apply也传过去
        const actionInput = document.createElement('input');
        actionInput.type = 'hidden';
        actionInput.name = 'action';
        actionInput.value = 'apply';
        form.appendChild(actionInput);

        console.log('Before form submit:', form.innerHTML);
        form.submit();

    });

});
