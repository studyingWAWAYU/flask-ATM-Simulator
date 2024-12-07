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

document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('uploadImg');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    let selectedFiles = [];

    // 处理文件选择并显示预览
    imageInput.addEventListener('change', function(event) {
        const files = event.target.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();

                // 读取文件并显示预览
                reader.onload = function(e) {
                    const imgElement = document.createElement('img');
                    imgElement.src = e.target.result;
                    imgElement.width = 100;

                    const deleteBtn = document.createElement('button');
                    deleteBtn.textContent = '❌';

                    deleteBtn.onclick = function() {
                        removeFile(i);
                    };

                    const previewDiv = document.createElement('div');
                    previewDiv.classList.add('image-preview');
                    previewDiv.appendChild(imgElement);
                    previewDiv.appendChild(deleteBtn);

                    imagePreviewContainer.appendChild(previewDiv);
                };

                reader.readAsDataURL(file);
                selectedFiles.push(file);
            }
        }
    });


    // 删除文件
    function removeFile(index) {
        // 从 selectedFiles 中删除文件
        selectedFiles.splice(index, 1);

        // 删除对应的预览元素
        const previewDivs = imagePreviewContainer.getElementsByClassName('image-preview');
        if (previewDivs[index]) {
            previewDivs[index].remove(); // 删除对应的预览图
        }
        updatePreviews();
    }

    // 更新预览容器中的图片
    function updatePreviews() {
        imagePreviewContainer.innerHTML = ''; // 清空容器

        // 重新渲染预览
        selectedFiles.forEach((file, i) => {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgElement = document.createElement('img');
                imgElement.src = e.target.result;
                imgElement.width = 100;

                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = '❌';

                deleteBtn.onclick = function() {
                    removeFile(i);
                };

                const previewDiv = document.createElement('div');
                previewDiv.classList.add('image-preview');
                previewDiv.appendChild(imgElement);
                previewDiv.appendChild(deleteBtn);

                imagePreviewContainer.appendChild(previewDiv);
            };
            reader.readAsDataURL(file);
        });
    }

    // 提交表单时，上传选择的文件
    document.getElementById('form').addEventListener('submit', function(event) {
        // 获取表单中的其他字段
        const formData = new FormData(event.target);

        console.log(selectedFiles);
        // 如果用户选择了图片，添加图片文件

        formData.delete('photo[]');
        for (let i = 0; i < selectedFiles.length; i++) {
        formData.append('photo[]', selectedFiles[i]); // 使用 selectedFiles 替代默认的文件列表
        }

        console.log('photo[]')


        // 使用 fetch API 提交表单数据
        event.preventDefault(); // 阻止表单默认提交行为

        fetch('/AddActivity', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            // 如果后端返回的是 HTML 页面，则使用 DOM 操作来更新页面内容
            return response.text();
        })
        .then(html => {
            // 将返回的 HTML 插入到页面中
            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => {
            console.error('Error submitting form:', error);
        });
    });
});