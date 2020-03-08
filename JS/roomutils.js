/*
Gets the number of rooms visited and the coverage in %
*/
var find_visited = function() {
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
UPDATE: Also considers the exits that lead nowhere.
*/
var get_exits = function(x, y) {

    var exits="";
    if($('#x'+x+'y'+y).css("borderTopWidth") == "1px" && $('#x'+x+'y'+(y-1)).attr('class') == "room") {
        exits+="N";
    }
    if($('#x'+x+'y'+y).css("borderRightWidth") == "1px" && $('#x'+(x+1)+'y'+y).attr('class') == "room" ) {
        exits+="E";
    }
    if($('#x'+x+'y'+y).css("borderBottomWidth") == "1px" && $('#x'+x+'y'+(y+1)).attr('class') == "room") {
        exits+="S";
    }
    if($('#x'+x+'y'+y).css("borderLeftWidth") == "1px" && $('#x'+(x-1)+'y'+y).attr('class') == "room") {
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

/*
Takes a list of avalable exits and returns the least weighted room or rooms
If more then one room is returned then a random selection is made between them.
*/
var get_least_weighted_room = function(exits,x,y) {

    weights={}

    for(var i = 0; i < exits.length; i++) {
        var heading = exits.charAt(i);
        if(heading == 'N') {
            weights["N"] = parseInt($('#x'+x+'y'+(y-1)).attr('data-weight'));
        }
        if(heading == "E") {
            weights["E"] = parseInt($('#x'+(x+1)+'y'+y).attr('data-weight'));
        }
        if(heading == "S") {
            weights["S"] = parseInt($('#x'+x+'y'+(y+1)).attr('data-weight'));
        }
        if(heading == "W") {
            weights["W"] = parseInt($('#x'+(x-1)+'y'+y).attr('data-weight'));
        }
    }
    console.log(weights);
    // now sort the weights object with the lowest first and only return the directions with the lowest value

    keysSorted = Object.keys(weights).sort(function(a,b){return weights[a]-weights[b]})
    min_weight = weights[keysSorted[0]];

    Object.filter = (obj, predicate) =>
    Object.keys(obj)
          .filter( key => predicate(obj[key]) )
          .reduce( (res, key) => (res[key] = obj[key], res), {} );

    var filtered = Object.filter(weights, score => score == min_weight);
    console.log(filtered);

    return(Object.keys(filtered));

}

addDoors = function(from, exits) {
    $('#north_door').hide();
    $('#east_door').hide();
    $('#south_door').hide();
    $('#west_door').hide();

    if(from == "N") {
        $('#player').css('top', '300px');
        $('#player').css('left', '300px');
    }
    if(from == "E") {
        $('#player').css('top', '300px');
        $('#player').css('left', '300px');
    }
    if(from == "S") {
        $('#player').css('top', '300px');
        $('#player').css('left', '300px');
    }
    if(from == "W") {
        $('#player').css('top', '300px');
        $('#player').css('left', '300px');
    }

    Array.from(exits).forEach(function(item, index) {
        if(item == "N") {
            $('#north_door').show();
        }
        if(item == "E") {
            $('#east_door').show();
        }
        if(item == "S") {
            $('#south_door').show();
        }
        if(item == "W") {
            $('#west_door').show();
        }
    });

}


addDoors_old = function(from, exits) {
    // Show the 3D room

    // Initially sets no exits - a dead-end

    var left_img='./images/left_NO.jpg';
    var right_img='./images/right_NO.jpg';
    var ahead_img='./images/ahead_NO.jpg';

    if(from == "N"){
        Array.from(exits).forEach(function(item, index) {
            if(item == "E")
                left_img='../images/left_OK.jpg';
            if(item == "S")
                ahead_img='../images/ahead_OK.jpg';
            if(item == "W")
                right_img='../images/right_OK.jpg';
        });
        from_north();
    }

    if(from == "E") {
        Array.from(exits).forEach(function(item, index) {
            if(item == "N")
                right_img='../images/right_OK.jpg';
            if(item == "S")
                left_img='../images/left_OK.jpg';
            if(item == "W")
                ahead_img='../images/ahead_OK.jpg';

        });
        from_east();
    }

    if(from == "S") {
        Array.from(exits).forEach(function(item, index) {
            if(item == "N")
                ahead_img='../images/ahead_OK.jpg';
            if(item == "E")
                right_img='../images/right_OK.jpg';
            if(item == "W")
                left_img='../images/left_OK.jpg';
        });
        from_south();
    }

    if(from == "W") {
        Array.from(exits).forEach(function(item, index) {
            if(item == "N")
                left_img='../images/left_OK.jpg';
            if(item == "E")
                ahead_img='../images/ahead_OK.jpg';
            if(item == "S")
                right_img='../images/right_OK.jpg';
        });
        from_west();
    }

//    $('#right').append("<img src='"+right_img+"' style='width:100%'/>");
//    $('#left').append("<img src='"+left_img+"' style='width:100%'/>");
//    $('#up').append("<img src='"+ahead_img+"' style='width:100%'/>");
    $('#right').css({'background':'url('+right_img+')','background-size':'contain','background-repeat': 'no-repeat', 'text-align': 'center'});
    $('#left').css({'background':'url('+left_img+')','background-size':'contain','background-repeat': 'no-repeat', 'text-align': 'center'});
    $('#up').css({'background':'url('+ahead_img+')','background-size':'contain','background-repeat': 'no-repeat', 'text-align': 'center'});

}

// Sends an inventory command to the server, parses and displays the result
getInventory = function() {
    des = "";
    $.post("maze.html",'{"command":"I"}')
    .done(function(returnData) {
        console.log(returnData);
        dat = JSON.parse(returnData);
        if(typeof dat['char_data'] != 'undefined') {
            $('#dialog').append("<table style='pasdding:5px'>");
            $('#dialog').append("<tr><th>Item</th><th>Value</th><td>");
            dat['char_data']['inventory'].forEach(function(d){
                des += d['name']+" ";
                $('#dialog').append("<tr><td>"+d['name']+"</td><td>"+d['sell']+"</td></tr>");
            });
            $('#dialog').append("</table>");
        }
    });
}

fight = function(x,y) {
    d2 = '{"command": "F", "room_x": '+x+',"room_y": '+y+'}';

    $.post("maze.html",d2)
    .done(function(returnData) {
        console.log(returnData);
        dat2 = JSON.parse(returnData);
        if(typeof dat2['char_data'] != 'undefined') {
            $('#dialog').append("<b>"+dat2.char_data.name+"</b>");
            $('#dialog').append("<table style='pasdding:5px'>");
            $('#dialog').append("<tr><th>Characteristic</th><th>Power</th><td>");
            dat2.char_data.abilities.forEach(function(abi){
                $('#dialog').append("<tr><td>"+abi['id']+"</td><td>"+abi['value']+"</td></tr>");
            });
            $('#dialog').append("</table>");
        }
    });
}

trade = function() {
    $.post("maze.html",'{"command":"T"}')
    .done(function(returnData) {
        console.log(returnData);
        dat3 = JSON.parse(returnData);
        if(typeof dat3['char_data'] != 'undefined') {
            $('#dialog').append("<table style='pasdding:5px'>");
            $('#dialog').append("<tr><th>Item </th><th>Value</th><td>");
            dat3['char_data']['inventory'].forEach(function(d){
                $('#dialog').append("<tr><td>"+d['name']+"</td><td>"+d['sell']+"</td></tr>");
            });
            $('#dialog').append("</table>");
        }
    });
}

attack = function(x,y) {
    d3 = '{"command": "A", "room_x": '+x+',"room_y": '+y+'}';
    $.post("maze.html",d3)
    .done(function(returnData) {
        console.log(returnData);
        dat3 = JSON.parse(returnData);
        if(typeof dat3['char_data'] != 'undefined') {
            $('#dialog').append("<p><b> You attack and "+dat3.char_data+"</b>");
        }
    });

}