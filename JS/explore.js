/*
Main entry point and setting of common functions etc.
*/
var main = function() {
    // attach the click event to the new content
    $('#x0y0').click(function(){
        var radioValue = $("input[name='rule']:checked").val();
        if(radioValue == "manual"){
            random_room_manual();
        }
        if(radioValue == "random"){
            random();
        }
        if(radioValue == "random_no_ret"){
            random_no_ret();
        }
        if(radioValue == "random_weighted"){
            random_room_weighting();
        }
        if(radioValue == "random_weighted_from"){
            random_room_weighting_from_door();
        }

        });
        // attach the different pointer.
        $('#x0y0').hover(function() {
            $(this).css('cursor','pointer');
        });

        // initialise the canvas
//        init_room();




}
/*
Called from the HTML page when the start room is clicked and random radio is selected.
*/
random = function() {
    var rowcount = $('table tr').length
    var colcount = $('table tr:nth-child(1) td').length


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

var random_room_weighting = function() {
    var rowcount = $('table tr').length
    var colcount = $('table tr:nth-child(1) td').length

    var x=0;
    var y=0;
    var iterations = parseInt($('#count').val());
    // Gets the number of iterations from the text box on HTML page

    var loop = function(value) {

            // increment its visited weighting
        w = parseInt($('#x'+x+'y'+y).attr('data-weight'))+1
        $('#x'+x+'y'+y).attr('data-weight', w);
        // Get the available exits from the room
        var exits = get_exits(x,y);
        console.log("exits = "+exits);
        // gets a list of available exits based on the number of times the adjacent room have been visited
        var weighted = get_least_weighted_room(exits,x,y);



        // select randomly from the list of exits
        var exit = select_exit(weighted);
        console.log("Travelling "+exit);
        var coords = move(exit,x,y);
        x=coords[0];
        y=coords[1];
        // When a room has been visited, change its background color to grey
        $('#x'+x+'y'+y).css("background-color","#FFF");
        if (value < iterations) setTimeout(function () {
            $('#x'+x+'y'+y).css("background-color","#DDD");
            loop(value + 1);
            find_visited();

        }, 30);

    }
    loop(1);
}

var random_room_weighting_from_door = function() {
    var rowcount = $('table tr').length
    var colcount = $('table tr:nth-child(1) td').length

    var x=0;
    var y=0;
    var iterations = parseInt($('#count').val());
    // Gets the number of iterations from the text box on HTML page
    var exit="N";
    $('#x'+x+'y'+y).css("background-color","#DDD");
    var loop = function(value) {
    console.log("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        console.log("[in room] "+$('#x'+x+'y'+y).attr('title'));
        // increment its visited weighting
        var w = parseInt($('#x'+x+'y'+y).attr('data-weight'))+1
        $('#x'+x+'y'+y).attr('data-weight', w);
        // Get the available exits from the room
        var exits = get_exits(x,y);
        console.log("[exits] "+exits);
        // gets a list of available exits based on the number of times the adjacent room have been visited
        var weighted = get_least_weighted_room(exits,x,y);
        // Get door that yoiu have just com in from
        var from = get_from_door(exit);
        console.log("[no return through] "+from);
        // remove from door from the list of exits - as long as it's not the only exit
        if(weighted.length > 1) {
            weighted = jQuery.grep(weighted, function(value) {
                return value != from;
            });
        }


        // select randomly from the list of exits
        exit = select_exit(weighted);
        console.log("[travelling] "+exit);
        coords = move(exit,x,y);
        x=coords[0];
        y=coords[1];

        addDoors(from, exits);

        $('#stop').click(function(){
            console.log("************ STOPPING");
            value=iterations;
        });
        $('#reset').click(function(){
            $( "#tablediv" ).empty();
            $( "#tablediv" ).load( "maze.html #grid" ,function( response, status, xhr ) {
                if ( status == "error" ) {
                    var msg = "Sorry but there was an error: ";
                    $( "#error" ).html( msg + xhr.status + " " + xhr.statusText );
                }
                main();
            });
        });
        // When a room has been visited, change its background color to grey
        $('#x'+x+'y'+y).css("background-color","#F00");
        if (value < iterations) setTimeout(function () {
            $('#x'+x+'y'+y).css("background-color","#DDD");
            loop(value + 1);
            find_visited();

        },0);



    }
    loop(1);
}

var random_room_manual = function() {
    rowcount = $('table tr').length
    colcount = $('table tr:nth-child(1) td').length

    x=0;
    y=0;

    // Call with a non-direction to indicate we're at the start
//    from_south();
    make_move("X");


}

make_move = function(dir) {

    exit=dir;
    exits = get_exits(x,y);
    $('#man').remove();
    if(exits.indexOf(exit) != -1) {

        // Get door that you have just come in from
        from = get_from_door(exit);

        console.log("[travelling] "+exit);
        coords = move(exit,x,y);
        x=coords[0];
        y=coords[1];

        newexits = get_exits(x,y);

        addDoors(from, newexits);



    } else if(dir == "X") {
        // This case is when you are in start
        exit=exits.charAt(0);
        from=get_from_door(exit);
        exits
        addDoors(from, exits);
        $('#x'+x+'y'+y).empty();
    }

    console.log("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
    console.log("[in room] "+$('#x'+x+'y'+y).attr('title'));

    // Get the available exits from the room
//    exits = get_exits(x,y);
    console.log("[exits] "+exits);
    find_visited();
    // When a room has been visited, change its background color to grey
    $('#x'+x+'y'+y).css("background-color","#DDD");
    if(from == "S")
        man="^";
    if(from == "N")
        man="v";
    if(from == "W")
        man=">";
    if(from == "E")
        man="<";
    $('#x'+x+'y'+y).append($("<div id='man'>"+man+"</div>"));
    r_name = $('#x'+x+'y'+y).attr("data-name");
    $('#roomname').text(r_name)
}
