document.addEventListener('DOMContentLoaded',function(){
    var customUpload = document.getElementById('custom_upload')
    var uploadImage = document.getElementById('uploadImg');

    customUpload.addEventListener('click',function(){
        uploadImage.click();
    });
});