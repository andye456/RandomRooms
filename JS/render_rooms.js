// Keyboard input with customisable repeat (set to 0 for no key repeat)
//
function KeyboardController(keys, repeat) {
    // Lookup of key codes to timer ID, or null for no repeat
    //
    var timers= {};

    // When key is pressed and we don't already think it's pressed, call the
    // key action callback and set a timer to generate another one after a delay
    //
    document.onkeydown= function(event) {
        var key= (event || window.event).keyCode;
        if (!(key in keys))
            return true;
        if (!(key in timers)) {
            timers[key]= null;
            keys[key]();
            if (repeat!==0)
                timers[key]= setInterval(keys[key], repeat);
        }
        return false;
    };

    // Cancel timeout and mark key as released on keyup
    //
    document.onkeyup= function(event) {
        var key= (event || window.event).keyCode;
        if (key in timers) {
            if (timers[key]!==null)
                clearInterval(timers[key]);
            delete timers[key];
        }
    };

    // When window is unfocused we may not get key events. To prevent this
    // causing a key to 'get stuck down', cancel all held keys
    //
    window.onblur= function() {
        for (key in timers)
            if (timers[key]!==null)
                clearInterval(timers[key]);
        timers= {};
    };
};

init_room = function() {

    var player = '<div id="player"></div>';
    var width = 620;
    var height = 447;
    $('#room').css({"width":width+"px","height":height+"px"});
    $('#room').append(player);

    // Arrow key movement. Repeat key five times a second
    //
    KeyboardController({
        // West
        37: function() {
                position = $('#player').position();

                 // Detect when the door is exited.
                direction="West"
                if(($('#player').offset().top + $('#player').height()) > ($('#west_door').offset().top) && // if the bottom left corner enters the door area
                ($('#player').offset().left) < ($('#west_door').offset().left + 80) &&
                ($('#player').offset().top ) < ($('#west_door').offset().top + $('#west_door').height())) {
                    console.log(direction+" door exited");
                    make_move("W");
                    $('#player').css('left', position.left + 700 +'px');
                    $('#player').css('top', position.top - 0 +'px');
                } else if(position.left > -50) {
                    $('#player').css('left', position.left - 10+'px');
               }
            },
        // North
        38: function() {
                position = $('#player').position();
                 // Detect when the door is exited.
                direction="North"
                if( ($('#player').offset().top ) < ($('#north_door').offset().top + 80) &&
                    ($('#player').offset().left + $('#player').width()) > ($('#north_door').offset().left ) &&
                    ($('#player').offset().left) < ($('#north_door').offset().left + $('#north_door').width()) ) {
                    console.log(direction+" door exited");
                    make_move("N")
//                    $('#player').offset().top = 480;
                    $('#player').css('top', (position.top + 480)+'px');
                }

                else if(position.top > -75) {
                    $('#player').css('top', position.top - 10+'px');
                }
            },
        // East
        39: function() {
            position = $('#player').position();
             // Detect when the door is exited.
            direction = "East";
            if(($('#player').offset().top + $('#player').height()) > ($('#east_door').offset().top) &&
            ($('#player').offset().left) > ($('#east_door').offset().left - 80) &&
            ($('#player').offset().top) < ($('#east_door').offset().top + $('#east_door').height())) {
                console.log(direction+" door exited");
                make_move("E")
                $('#player').css('left', position.left - 700 +'px');
                $('#player').css('top', position.top - 0 +'px');

            } else if(position.left < (width))
                $('#player').css('left', position.left + 10+'px');
            },
        // South
        40: function() {
            position = $('#player').position();
             // Detect when the door is exited.
                direction="South"
                if( ($('#player').offset().top ) > ($('#south_door').offset().top - 75) &&
                    ($('#player').offset().left + $('#player').width()) > ($('#south_door').offset().left) &&
                    ($('#player').offset().left) < ($('#south_door').offset().left + $('#south_door').width()) ) {
                    console.log(direction+" door exited");
                    make_move("S")
                    $('#player').css('top', position.top - 400+'px');
                } else if(position.top < (height ))
                $('#player').css('top', position.top + 10+'px');
            }
    }, 25);
}