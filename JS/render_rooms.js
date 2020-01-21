room_base = function() {
    var room_table = $('<table></table>');
    room_table.css({'border':'1px black solid', 'border-collapse':'collapse'})
    for (var i = 0; i < 30; i++) {
        var tr = $("<tr></tr>")
        for(var j = 0; j < 60; j++) {
            data = $('<td></td>').css({'border':'1px black solid', 'width':'20px', 'height':'20px', 'border-collapse':'collapse'});
            tr.append(data);
        }
        room_table.append(tr)

    }
    room_table.append("</table>");
    $('#roomgraphics').append(room_table);
}