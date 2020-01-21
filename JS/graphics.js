//
//
//init_room = function() {
//    ctx = document.getElementById('viewer').getContext('2d');
//
//}
//
//drawRoom = function() {
//    ctx.fillStyle = '#FFF';
//
//    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
//    // outer view
//
//    ctx.strokeStyle = '#000'
//
//    ctx.strokeRect(0, 0, 400, 400);
//
//    // diagonals
//    ctx.moveTo(0,0);
//    ctx.lineTo(150,150);
//    ctx.stroke();
//
//    ctx.moveTo(400,0);
//    ctx.lineTo(250,150);
//    ctx.stroke();
//
//    ctx.moveTo(400,400);
//    ctx.lineTo(250,250);
//    ctx.stroke();
//
//    ctx.moveTo(0,400);
//    ctx.lineTo(150,250);
//    ctx.stroke();
//
//    // end wall
//    ctx.strokeRect(150,150,100,100);
//
//    // These are the direction divs that are over the doors
//    // remove them so they can be reapplied with the new directions on
//    $('#up').remove();
//    $('#down').remove();
//    $('#left').remove();
//    $('#right').remove();
//    // Always add a back exit to take you to where you 've just come from
//    $('#canvasid').append($("<div id='down' title='Move down' style='position: absolute; left:750; top:525; width:400px; height:50px; cursor:pointer'></div>"));
//
//}
//
//addAhead = function() {
//    ctx.fillStyle = '#000';
//    ctx.fillRect(175,175,50,75);
//
//    $('#canvasid').append($("<div id='up'  title='Move forward' style='position: absolute; left:925; top:350; width:50px; height:75px; cursor:pointer'></div>"));
//
//}
//
//addLeft = function(position) {
//
//    ctx.strokeStyle = '#FFF';
//    // Door top
//    ctx.fillStyle = '#999';
//    ctx.beginPath();
//    ctx.moveTo(50,100);
//    ctx.lineTo(100,150);
//    ctx.lineTo(50,150);
//    ctx.fill();
//    ctx.closePath();
//
//    // main bit
//    ctx.fillStyle = '#CCC';
//    ctx.fillRect(50,150,50,150);
//    $('#canvasid').append($("<div id='left' title='Move left' style='position: absolute; left:800; top:325; width:50px; height:150px; cursor:pointer'></div>"));
//
//    // Door bottom
//    ctx.fillStyle = '#EEE';
//    ctx.strokeStyle = '#FFF '
//    ctx.beginPath();
//    ctx.moveTo(100,300);
//    ctx.lineTo(50,300);
//    ctx.lineTo(50,350);
//    ctx.closePath();
//    ctx.fill();
//
//    ctx.strokeStyle = '#FFF'
//    ctx.moveTo(50,350);
//    ctx.lineTo(100,300);
//    ctx.stroke();
//
//}
//
//addRight = function() {
//
//    // Door top
//    ctx.fillStyle = '#999';
//    ctx.beginPath();
//    ctx.moveTo(350,100);
//    ctx.lineTo(300,150);
//    ctx.lineTo(350,150);
//    ctx.fill();
//
//    // main bit
//    ctx.fillStyle = '#CCC';
//    ctx.fillRect(300,150,50,150);
//    $('#canvasid').append($("<div id='right' title='Move right' style='position: absolute; left:1050; top:325; width:50px; height:150px; cursor:pointer'></div>"));
//
//    // Door bottom
//    ctx.fillStyle = '#EEE';
//    ctx.beginPath();
//    ctx.moveTo(350,300);
//    ctx.lineTo(300,300);
//    ctx.lineTo(350,350);
//    ctx.fill();
//
//    // clear bottom of door
//    ctx.strokeStyle = '#FFF'
//    ctx.moveTo(350,350);
//    ctx.lineTo(300,300);
//    ctx.stroke();
//
//}
//
