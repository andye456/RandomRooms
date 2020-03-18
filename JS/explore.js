/*
Main entry point and setting of common functions etc.
*/
var main = function() {
    // attach the click event to the new content
    random_room_manual();

}



var random_room_manual = function() {
    rowcount = $('table tr').length
    colcount = $('table tr:nth-child(1) td').length

    x=0;
    y=0;

    // Call with a non-direction to indicate we're at the start
    handle_input("X");

    // Get the user command line input
    $('#inputline').keypress(function(event){

        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            handle_input($('#inputline').val());
            $('#inputline').val("");
            $('#scrolldiv').animate({scrollTop:$('#scrolldiv')[0].scrollHeight}, 1000);
        }

    });


}

handle_input = function(dir) {
    // Reads the direction commands to navigate the maze
    if(['N','S','E','W','X'].includes(dir.toUpperCase())) {
        exit=dir.toUpperCase();
        exits = get_exits(x,y);
        $('#man').remove();

        console.log("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        console.log("[in room] "+$('#x'+x+'y'+y).attr('title'));

        if(exits.indexOf(exit) != -1) {

            // Get door that you have just come in from
            from = get_from_door(exit);

            $('#dialog').append("[travelling] "+exit+"</br>");
            coords = move(exit,x,y);
            x=coords[0];
            y=coords[1];

            newexits = get_exits(x,y);

    //        addDoors(from, newexits);
            $('#dialog').append("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"+"</br>");
            h='Exits are: '+newexits+"</br>";
            // Get the available exits from the room
            //    exits = get_exits(x,y);
            console.log("[exits] "+newexits);
            $('#dialog').append(h);


        } else if(dir == "X") {
            console.log("At start!");
            // This case is when you are in start
            exit=exits.charAt(0);
            from=get_from_door(exit);
    //        addDoors(from, exits);
            h='Exits are: '+exits+"</br>";
            // Get the available exits from the room
            exits = get_exits(x,y);
            console.log("[exits] "+exits);
            $('#dialog').append(h);


        }
        // Send the room co-ords to the server using the do_POST
        data={room_x: x, room_y: y};
        d = JSON.stringify(data);

        // Looks up the room data from the serverside using the current position as the key
        // to get the object from the datastore object - the bin file created by the python dill utility
        $.post("maze.html",d)
            .done(function(d2) {
            console.log(d2);
            ht = JSON.parse(d2);
            desc= "You are in a place called "+ht['room_data']['room_name']+"</br>";
            if(typeof ht['item_data'] != 'undefined') {
                // Get the items list
                items=[]
                ht['item_data'].forEach(function(d){
                   items+=d.item_object.name+" ";
                });
            }
            if(typeof ht['char_data'] != 'undefined') {

                if(x == 0 && y == 0) {
                    desc+= "&nbsp;Your name is "+ht['char_data']['name']+"</br>";
                    desc+= "&nbsp;a "+ht['char_data']['race']+"&nbsp"+ht['char_data']['char_class']+"</br>";
                    if(typeof ht['item_data'] != 'undefined') {
                        desc+= "&nbsp;You are carrying: "+items+"</br>";
                    } else {
                        desc+= "You are carrying nothing</br>"
                    }
                    desc+= "&nbsp;Your current weapon is: "+ht['char_data']['weapon']['name']+"</br>";
                } else {
                    friend_status={"P":"They view you as a friend",
                    "G":"They view you as a friend",
                    "T":"They view you as a friend",
                    "N":"They view you with suspicion",
                    "A":"They view you with mistrust",
                    "H":"They view you with hatred"}
                    desc+= "&nbsp;Also here is "+ht['char_data']['name']+"</br>";
                    desc+= "&nbsp;..who is a "+ht['char_data']['race']+"&nbsp"+ht['char_data']['char_class']+"</br>";
                    desc+= "&nbsp;They are carrying: "+items+"</br>";
                    desc+= "&nbsp;Their current weapon is: "+ht['char_data']['weapon']['name']+"</br>";
                    desc+= friend_status[ht.friend_status]+"<br>";
                }
            } else if(typeof ht.item_data != 'undefined' && ht.item_data[0].owner == "room") {
                desc+="You can see: "+items+"<br/>";
            }
            $('#dialog').append(desc);

        });
        from=get_from_door(exit);

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
    } else {
        // This deals with the commands other than movement
        command=dir.toUpperCase();
        if(command == "I")
            getInventory();
        if(command == "O")
            strengths(x,y);
        if(command == "A")
            attack(x,y)
        if(command == "T")
            trade();
        if(command == "P")
            strengths(0,0);
        if(command == "G")
            gather(x,y);
    }


}
