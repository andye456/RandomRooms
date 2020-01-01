maze_solver = function() {
    var rowcount = $('table tr').length
    var colcount = $('table tr:nth-child(1) td').length

    var x=0;
    var y=0;
    var moves = 0;
    for(;true;) {
        if(moves > 10000) break;
        console.log("("+x+","+y+")");
        //    Get the available exits from the room
        var exits = get_exits(x,y);
        var exit = select_exit(exits);
        var coords = move(exit,x,y);
        console.log("new coords: "+coords);
        x=coords[0];
        y=coords[1];

        moves++;
    }

}

var move = function(exit,x,y){

    if(exit == "N") {
        y--;
    }
    if(exit == "E") {
        x++;
    }
    if(exit == "S") {
        y++;
    }
    if(exit == "W") {
        x--;
    }

    console.log("x = "+x+", y = "+y);
    return [x,y]

}

/*
Gets the exits for the given room based on the border widths
*/
var get_exits = function(x, y) {

    var exits="";

    if($('#x'+x+'y'+y).css("borderTopWidth") == "1px") {
        exits+="N";
    }
    if($('#x'+x+'y'+y).css("borderRightWidth") == "1px") {
        exits+="E";
    }
    if($('#x'+x+'y'+y).css("borderBottomWidth") == "1px") {
        exits+="S";
    }
    if($('#x'+x+'y'+y).css("borderLeftWidth") == "1px") {
        exits+="W";
    }

    $('#x'+x+'y'+y).css("background-color","#DDD")
    console.log("exits = "+exits);
    return exits
}

/*
Randomly selects an exit from the available exits.
*/
var select_exit = function(exits) {
    var arr = Array.from(exits);
    var direction = arr[Math.floor(Math.random() * arr.length)];
    console.log("direction = "+direction);
    return direction;
}