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
