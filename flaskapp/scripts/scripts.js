
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var rect = {};
var drag = false;
var img = null;

function init() {
    img = new Image();
    img.onload = function () {

    // set size proportional to image
    canvas.height = canvas.width * (img.height / img.width);

    // step 1 - resize to 50%
    var oc = document.createElement('canvas'),
        octx = oc.getContext('2d');

    oc.width = img.width * 1;
    oc.height = img.height * 1;
    octx.drawImage(img, 0, 0, oc.width, oc.height);

    // step 2
    octx.drawImage(oc, 0, 0, oc.width * 1, oc.height * 1);

    // step 3, resize to final size
    ctx.drawImage(oc, 0, 0, oc.width * 1, oc.height * 1,
    0, 0, canvas.width, canvas.height);
};
    img.src = '/api/a';
    canvas.addEventListener('mousedown', mouseDown, false);
    canvas.addEventListener('mouseup', mouseUp, false);
    canvas.addEventListener('mousemove', mouseMove, false);
}

function mouseDown(e) {
    rect.startX = e.pageX - this.offsetLeft;
    rect.startY = e.pageY - this.offsetTop;
    drag = true;
}

function mouseUp() { 
    drag = false;
    //myFunction()
    console.log(rect);
     }

function mouseMove(e) {
    if (drag) {
        
        // set size proportional to image
        canvas.height = canvas.width * (img.height / img.width);
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    // step 1 - resize to 50%
        var oc = document.createElement('canvas'),
        octx = oc.getContext('2d');

        oc.width = img.width * 1;
        oc.height = img.height * 1;
        octx.drawImage(img, 0, 0, oc.width, oc.height);

    // step 2
        octx.drawImage(oc, 0, 0, oc.width * 1, oc.height * 1);

    // step 3, resize to final size
        ctx.drawImage(oc, 0, 0, oc.width * 1, oc.height * 1, 0, 0, canvas.width, canvas.height);

        rect.w = (e.pageX - this.offsetLeft) - rect.startX;
        rect.h = (e.pageY - this.offsetTop) - rect.startY;
        ctx.strokeStyle = 'red';
        ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
        
    
    }

}

function myFunction() {
  var Key= prompt("Key:", "");
  var value = prompt("Value:","");
}



init();
