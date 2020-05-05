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
        return "S";
    if(exit == "E")
        return "W";
    if(exit == "S")
        return "N";
    if(exit == "W")
        return "E";
    return "N";
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
Gets the exits for the given room based on the border widths in the html
UPDATE: Also considers the exits that lead nowhere.
*/
// var get_exits_old = function(x, y) {
//
//     var exits="";
//     if($('#x'+x+'y'+y).css("borderTopWidth") == "1px" && $('#x'+x+'y'+(y-1)).attr('class') == "room") {
//         exits+="N";
//     }
//     if($('#x'+x+'y'+y).css("borderRightWidth") == "1px" && $('#x'+(x+1)+'y'+y).attr('class') == "room" ) {
//         exits+="E";
//     }
//     if($('#x'+x+'y'+y).css("borderBottomWidth") == "1px" && $('#x'+x+'y'+(y+1)).attr('class') == "room") {
//         exits+="S";
//     }
//     if($('#x'+x+'y'+y).css("borderLeftWidth") == "1px" && $('#x'+(x-1)+'y'+y).attr('class') == "room") {
//         exits+="W";
//     }
//
//
//     return exits
// }

// Gets the exits based on the value of data-room-code-int in the HTML that is generated in RoomGenHtml
let get_exits = function(x,y) {
    let exits="";
    if((parseInt($('#x'+x+'y'+y).attr('data-room-code-int')) & 8) >> 3 === 1)
        exits+="N";
    if((parseInt($('#x'+x+'y'+y).attr('data-room-code-int')) & 4) >> 2 === 1)
        exits+="E";
    if((parseInt($('#x'+x+'y'+y).attr('data-room-code-int')) & 2) >> 1 === 1)
        exits+="S";
    if((parseInt($('#x'+x+'y'+y).attr('data-room-code-int')) & 1) >> 0 === 1)
        exits+="W";
    return exits;
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

// Sends an inventory command to the server, parses and displays the result
getInventory = function() {
    des = "";
    $.post("maze.html",'{"command":"I"}')
    .done(function(returnData) {
        console.log(returnData);
        dat = JSON.parse(returnData);
        if(typeof dat.item_data != 'undefined' && Array.isArray(dat.item_data)) {
            $('#dialog').append("<table style='padding:5px; border:5px'>");
            $('#dialog').append("<tr><th colspan='3'>Inventory</th><td>");
            $('#dialog').append("<tr><th>Item</th><th>Value each</th><th>Count</th><td>");

            lookup = {};
            var results = [];
            var items = dat.item_data;
            for(var item, i = 0; item = items[i++];) {
                var n = item.item_object.name;
                if (!(n in lookup)) {
                    lookup[n] = 1;
                    results.push({"name":n, "sell": item.item_object.sell, "count":lookup[n]});
                } else {
                    var index = items.findIndex(obj => obj.item_object.name==n);
                    //results.splice(index,1);
                    lookup[n]+=1
                    results[index] = {"name":n, "sell": item.item_object.sell, "count":lookup[n]};

                }
            }

            results.forEach(function(d){
                $('#dialog').append("<tr style='padding:3px'><td style='padding:3px'>"+d.name+"</td><td>"+d.sell+"</td><td>"+d.count+"</td></tr>");
            });

            $('#dialog').append("</table>");
        } else {
            $('#dialog').append(dat.item_data+"<br/>")
        }
    });
}

function getCharData(x, y) {
    d2 = '{"command": "O", "room_x": ' + x + ',"room_y": ' + y + '}';
    var dat2;
    $.ajax({
        url: "maze.html",
        type:"POST",
        data: d2,
        async: false
    })
    .done(function(returnData) {
        console.log("getCharData: "+returnData);
        dat2 = JSON.parse(returnData);
    });
    return dat2;
};


show_strengths = function(data) {
            if(typeof data['char_data'] != 'undefined') {
            $('#dialog').append("<b>Name: "+data.char_data.name+"</b>");
            $('#dialog').append("<table style='border:5px; padding: 5px'>");
            $('#dialog').append("<tr><td colspan='2'>Hit Points: "+data.char_data.hit_points+"</td></tr>");
            $('#dialog').append("<tr><td colspan='2'>Experience: "+data.char_data.experience+"</td></tr>");
            $('#dialog').append("<tr><th style='padding:5px'>Characteristic</th><th>Power</th><td>");
            for( var key in data.char_data.abilities) {
                if(data.char_data.abilities.hasOwnProperty(key)) {
                    $('#dialog').append("<tr><td>"+key+"</td><td>"+data.char_data.abilities[key]+"</td></tr>");
                }
            }
            $('#dialog').append("</table>");
        }

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
            $('#dialog').append("<p><b>"+dat3.char_data+"</b>");
            if(dat3.char_data == "lose") {
                $('#dialog').append("<p><b> Game Over, return to start to restart.</b>");
                restart();
            }
        }
    });

}

gather = function(x,y) {
    d4 = '{"command":"G", "room_x":'+x+', "room_y":'+y+'}';
    $.post("maze.html",d4)
    .done(function(returnData) {
        console.log(returnData);
        dat4 = JSON.parse(returnData);
        if(typeof dat4.item_data != 'undefined') {
            dat4.item_data.forEach(function(d) {
                $('#dialog').append("You pick up:")
                if(typeof d.item_object != 'undefined')
                    $('#dialog').append(d.item_object.name+"<br/>");
                if(typeof d.potion_object != 'undefined')
                    $('#dialog').append(d.potion_object.name+"<br/>");

            });
        }
    });
}

// This is to consume potions
drink = function(command) {
    d5 = '{"command":"'+command+'"}';
    $.post("maze.html",d5)
    .done(function(returnData) {
        console.log(returnData);
        dat5 = JSON.parse(returnData);
        if(typeof dat5.item_data != 'undefined') {
            $('#dialog').append(dat5.item_data);
        }
    });
}
