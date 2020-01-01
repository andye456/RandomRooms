"""
RoomFinder will load a previously created matrix of rooms and using various algorithms traverse the maze in the least moves

"""
from Room import Room
from RoomMatrix import RoomMatrix
import pickle
import RoomUtils

html="<html><head>"
html+="<style>"

html+="td {height:15px; width:10px;}"
html+="</style>"
html+="""
<script type="text/javascript" src="JS/jquery/jquery-341.js"></script>
<script type="text/javascript" src="JS/explore.js"></script>
"""
html+="<script>"
html+=""" 
$(document).ready(function () {
    $('#x0y0').click(function(){
        maze_solver();
    });
});
"""
html+="</script>"
html+="</head><body>"
html+="""
<table>
<tr><td></td><td>&#8679</td><td></td></tr>
<tr><td>&#8678</td><td></td><td>&#8680</td></tr>
<tr><td></td><td>&#8681</td><td></td></tr>
</table>
"""
html+="<table id='grid' style='border:1px black solid; border-collapse:separate; width: max-content'>"

color=""
# Open the serialised data file in read/binary mode
f = open("data.bin", "rb")

x = []
y = []
# Load the saved data dictionary.
room_ref=pickle.load(f)

# Iterate through the rooms in the dictionary
for i, j in room_ref:
    x.append(i)
    y.append(j)

# gets the x,y dimensions using the range of the axis, e.g. -5 to 5 gives a range of 11
x_lim = max(x)
x_lower = min(x)
# x_tx is the transform amount to apply to the grid positions to get the actual values in the room grid.
x_tx = 0 - x_lower
y_lim = max(y)
y_lower = min(y)
y_tx = 0 - y_lower
x_range = x_lim - x_lower + 1
y_range = y_lim - y_lower + 1
grid = [[0] * x_range for i in range(y_range)]
# Get the max visits for any room
new_max=0
for i in room_ref:
    max=room_ref[i].visits
    if max>new_max:
        new_max=max
oldrange=new_max
newrange=255 #this is FF
print(new_max)
# Now loop through the html grid and check if each square corresponds to a room that has beed created.
for row in range(len(grid)):
    html+="<tr>"
    for elem in range(len(grid[row])):
        try:
            # If a room is found then make the borders of the td match the exits that the room has
            if (room_ref[elem - x_tx, row - y_tx] is not None):
                val = room_ref[elem - x_tx, row - y_tx].room_code_int
                if (val & 8) >> 3 == 1:
                    style_n='border-top:dashed 1px black'
                else:
                    style_n='border-top:2px black solid'
                text=""
                if (val & 4) >> 2 == 1:
                    style_e='border-right:dashed 1px black'
                else:
                    style_e='border-right:2px black solid'
                if (val & 2) >> 1:
                    style_s = 'border-bottom:dashed 1px black'
                else:
                    style_s = 'border-bottom:2px black solid'
                if (val & 1) >> 0 == 1:
                    style_w = 'border-left:dashed 1px black'
                else:
                    style_w = 'border-left:2px black solid'
                if room_ref[elem - x_tx, row - y_tx].name == "Start":
                    color="border-color:red"
                    text="S"
                else:
                    color = "border-color:black"
                    v=(newrange/oldrange)*room_ref[elem - x_tx, row - y_tx].visits

                xref=elem - x_tx
                yref=row - y_tx
                heat_color=format(255-int(v),'02x')
                html+="<td id='x"+str(xref)+"y"+str(yref)+"' title='"+str(room_ref[elem - x_tx, row - y_tx].visits)+" "+str(room_ref[elem - x_tx, row - y_tx].name)+"'style='"+style_n+";"+style_e+";"+style_s+";"+style_w+";"\
                      +color+"; background-color:#FF"+ heat_color+"FF; font-size:12px; text-align: center'>"
                # html+=str(room_ref[elem - x_tx, row - y_tx].visits)
                html+=text
        except KeyError:
            html+="<td background-color:#000000>"
        html+="</td>"
    print(".", end='')
    html+="</tr>"
html+="</table></body></html>"
f.close()
with open("maze.html","w") as h:
    h.write(html)

