init_room = function() {
    var player = '<div id="player"></div>';
    $('#room').append(player);
    $(document).keydown(function(e){
        var position = $('#player').position();
        switch(e.keyCode) {
            // LEFT 37
            case 37:
            $('#player').css('left', position.left - 20+'px');
            break;
            // UP 38
            case 38:
            $('#player').css('top', position.top - 20+'px');
            break;
            // RIGHT 39
            case 39:
            $('#player').css('left', position.left + 20+'px');
            break;
            // DOWN 40
            case 40:
            $('#player').css('top', position.top + 20+'px');
            break;
        }
    });
}