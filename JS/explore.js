/*
TODO: Get some readout of p3ercentage coverage that has been explored
TODO: Implement weighted doors
*/

/*
Called from the HTML page when the start room is clicked and random radio is selected.
*/
random = function() {
    var rowcount = $('table tr').length
    var colcount = $('table tr:nth-child(1) td').length

    console.log("rows: "+rowcount+" cols: "+colcount+" total: "+(rowcount*colcount));

    var x=0;
    var y=0;
    var iterations = parseInt($('#count').val());
    // Gets the number of iterations from the text box on HTML page
    for(var i = 0; i < iterations; i++) {
        //    Get the available exits from the room
        var exits = get_exits(x,y);
        var exit = select_exit(exits);
        var coords = move(exit,x,y);
        x=coords[0];
        y=coords[1];
        // When a room has been visited, change its background color to grey
        $('#x'+x+'y'+y).css("background-color","#DDD")

    }
    find_visited()

}
/*
Called from the HTML page when the start room is clicked and random_no_ret radio is selected.
*/
random_no_ret = function() {
    var rowcount = $('table tr').length
    var colcount = $('table tr:nth-child(1) td').length

    var x=0;
    var y=0;
    var iterations = parseInt($('#count').val());
    // Gets the number of iterations from the text box on HTML page
    for(var i = 0; i < iterations; i++) {
        //    Get the available exits from the room
        var exits = get_exits(x,y);
        var from = get_from_door(exit);
        // remove from door from the list of exits - as long as it's not the only exit
        if(exits.length > 1) {
            exits = jQuery.grep(exits, function(value) {
                return value != from;
            });
        }
        var exit = select_exit(exits);
        var coords = move(exit,x,y);
        x=coords[0];
        y=coords[1];
        // When a room has been visited, change its background color to grey
        $('#x'+x+'y'+y).css("background-color","#DDD")

    }
    find_visited()

}

find_visited = function() {
    var visited = $('td').filter(function(){
        return $(this).css('background-color') == 'rgb(221, 221, 221)';
    }).length;

    var total = $('.room').length;


    console.log("visited = "+visited+" total = "+total );

    coverage = (visited/total) * 100;

    console.log(coverage+"%");

    $('#room_count').text(total);
    $('#visited').text(visited);
    $('#coverage').text(coverage)

}

/*
Gets the door that you have just come in from - this will be the opposite from "exit"
*/
var get_from_door = function(exit) {
    if(exit == "N")
        return "S"
    if(exit == "E")
        return "W"
    if(exit == "S")
        return "N"
    if(exit == "W")
        return "E"
}

/*
Takes the value for the move, N, S, E, W and changes the co-ordinates of the current location
*/
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
    if(exit == "X") {
    }

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

    return exits
}

/*
Randomly selects an exit from the available exits.
*/
var select_exit = function(exits) {
    var arr = Array.from(exits);
    var direction = arr[Math.floor(Math.random() * arr.length)];
    return direction;
}