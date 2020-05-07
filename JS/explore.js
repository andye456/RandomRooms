/*
Main entry point and setting of common functions etc.
*/
var main = function () {
    // attach the click event to the new content
    random_room_manual();

};


var random_room_manual = function () {
    // Start by showing the player their character
    show_strengths(getCharData(0, 0));


    rowcount = $('table tr').length;
    colcount = $('table tr:nth-child(1) td').length;

    x = 0;
    y = 0;

    // Make an initial ajax call to attach the maze to the table div
    $('#tablediv').load("../matrix.html", function () {
        // Call with a non-direction to indicate we're at the start
        handle_input("X");
    });

    $('#userinput').click(function () {
        $('#inputline').focus();
    })

    // Get the user command line input
    let keypress = $('#inputline').keypress(function (event) {

        var keycode = (event.keyCode ? event.keyCode : event.which);
        // When enter is pressed - submit the value on the command line
        if (keycode === 13) {
            handle_input($('#inputline').val());
            $('#inputline').val("");
            $('#scrolldiv').animate({scrollTop: $('#scrolldiv')[0].scrollHeight}, 1000);
        }

    });
}
existing = "";
level = 0;
currentexp = 0;
handle_input = function (dir) {

    let exp_data = getCharData(0, 0)
    $('#currenthit').val(exp_data['char_data']['hit_points']);
    $('#currentexp').val(exp_data['char_data']['experience']);


    // work out the targte exp
    $('#targetexp').val((level + 1) * 5)

    // Reads the direction commands to navigate the maze
    if (['N', 'S', 'E', 'W', 'X'].includes(dir.toUpperCase())) {
        exit = dir.toUpperCase();
        exits = get_exits(x, y);
        $('#man').remove();

        console.log("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
        console.log("[in room] " + $('#x' + x + 'y' + y).attr('title'));

        if (exits.indexOf(exit) != -1) {

            // Get door that you have just come in from
            from = get_from_door(exit);

            $('#dialog').append("[travelling] " + exit + "</br>");
            coords = move(exit, x, y);
            x = coords[0];
            y = coords[1];

            newexits = get_exits(x, y);

            //        addDoors(from, newexits);
            $('#dialog').append("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+" + "</br>");
            h = 'Exits are: ' + newexits + "</br>";
            // Get the available exits from the room
            //    exits = get_exits(x,y);
            console.log("[exits] " + newexits);
            $('#dialog').append(h);


        } else if (dir == "X") {
            console.log("At start!");
            // This case is when you are in start
            exit = exits.charAt(0);
            from = get_from_door(exit);
            //        addDoors(from, exits);
            h = 'Exits are: ' + exits + "</br>";
            // Get the available exits from the room
            exits = get_exits(x, y);
            console.log("[exits] " + exits);
            $('#dialog').append(h);


        }
        // Send the room co-ords to the server using the do_POST
        data = {room_x: x, room_y: y};
        d = JSON.stringify(data);

        // Looks up the room data from the serverside using the current position as the key
        // to get the object from the datastore object - the bin file created by the python dill utility
        $.post("maze.html", d)
            .done(function (d2) {
                console.log(d2);
                ht = JSON.parse(d2);
                desc = "You are in a place called " + ht.room_data.room_name + "</br>";
                $('#level').val(level);

                if (ht.room_data.room_name === "Exit") {
                    // if the exit is reached then check the player has the required experience to exit the level
                    c = getCharData(0, 0);
                    if (c.char_data.experience >= $('#targetexp').val()) {
                        // ToDo: Need to write this experience back to the character otherwise it'll be read wrong.
                        currentexp = 0; // reset current experience for the new level.
                        level++;
                        $('#level').val(level);
                        iterations = $('#iter').val();
                        // Generate a new room matrix file by calling the back end.
                        data = {"command": "regenerate", "iterations": iterations, "level": level};
                        d = JSON.stringify(data);
                        $.post("maze.html", d)
                            .done(function (d2) {
                                console.log(d2);
                            });
                        // Loads the room matrix from a file, which has been pre-generated.
                        $('#tablediv').load("../matrix.html", function () {
                            // Set the location to be at the start
                            x = 0;
                            y = 0;
                            // Submit the location to the server, let it return that we are at the start.
                            data = {room_x: x, room_y: y};
                            d = JSON.stringify(data);
                            $.post("maze.html", d)
                                .done(function (d2) {
                                    console.log(d2);
                                    ht = JSON.parse(d2);
                                    desc = "You are in a place called " + ht.room_data.room_name + "</br>";
                                });
                            handle_input("X");
                        });

                    } else {
                        desc += "You need " + $('#targetexp').val() + " experience to exit this level, you have " + c.char_data.experience + "<br>"
                    }
                }
                if (typeof ht['item_data'] != 'undefined') {
                    // Get the items list
                    items = []
                    ht['item_data'].forEach(function (d) {
                        // This is probably too defensive as item_object will not be 'undefined' if it gets to here.
                        if (typeof d.item_object != 'undefined')
                            items += d.item_object.name + " ";
                    });
                }
                if (typeof ht['char_data'] != 'undefined') {

                    if (x == 0 && y == 0) {
                        desc += "&nbsp;Your name is " + ht['char_data']['name'] + "</br>";
                        desc += "&nbsp;a " + ht['char_data']['race'] + "&nbsp" + ht['char_data']['char_class'] + "</br>";
                        if (typeof ht['item_data'] != 'undefined') {
                            desc += "&nbsp;You are carrying: " + items + "</br>";
                        } else {
                            desc += "You are carrying nothing</br>"
                        }
                        desc += "&nbsp;Your current weapon is: " + ht['char_data']['weapon']['name'] + "</br>";
                    } else {
                        friend_status = {
                            "P": "They view you as a friend",
                            "G": "They view you as a friend",
                            "T": "They view you as a friend",
                            "N": "They view you with suspicion",
                            "A": "They view you with mistrust",
                            "H": "They view you with hatred"
                        }
                        desc += "&nbsp;Also here is " + ht['char_data']['name'] + "</br>";
                        desc += "&nbsp;..who is a " + ht['char_data']['race'] + "&nbsp" + ht['char_data']['char_class'] + "</br>";
                        desc += "&nbsp;They are carrying: " + items + "</br>";
                        desc += "&nbsp;Their current weapon is: " + ht['char_data']['weapon']['name'] + "</br>";
                        desc += "&nbsp;Their hit points are: " + ht['char_data']['hit_points'] + "</br>";
                        desc += friend_status[ht.friend_status] + "<br>";
                        if(ht.friend_status == "H") {
                            attack(x,y,false);
                        }
                    }
                } else if (typeof ht.item_data != 'undefined' && ht.item_data.length > 0) {
                    if (ht.item_data[0].owner == "room") {
                        desc += "You can see: " + items + "<br/>";
                    }
                }
                $('#dialog').append(desc);

            });
        from = get_from_door(exit);

        find_visited();
        // When a room has been visited, change its background color to grey
        // Save the old room decorators if there are any
        $('#x' + x + 'y' + y).css("background-color", "#DDD");
        if (from === "S") {
            man = "^";
            $('#x' + x + 'y' + (y + 1)).text(existing);
        }
        if (from === "N") {
            man = "v";
            $('#x' + x + 'y' + (y - 1)).text(existing);
        }
        if (from === "W") {
            man = ">";
            $('#x' + (x - 1) + 'y' + y).text(existing);
        }
        if (from === "E") {
            man = "<";
            $('#x' + (x + 1) + 'y' + y).text(existing);
        }
        existing = $('#x' + x + 'y' + y).html();
        $('#x' + x + 'y' + y).html($("<div id='man'>" + man + "</div>"));
        r_name = $('#x' + x + 'y' + y).attr("data-name");
        $('#roomname').text(r_name)

    } else {
        // This deals with the commands other than movement
        command = dir.toUpperCase();
        if (command == "I")
            getInventory();
        if (command == "O")
            show_strengths(getCharData(x, y));
        if (command == "A")
            attack(x, y, true)
        if (command == "T")
            trade();
        if (command == "P")
            show_strengths(getCharData(0, 0));
        if (command.startsWith("G"))
            gather(x, y);
        if (command.startsWith("D"))
            drink(command);
    }


}
