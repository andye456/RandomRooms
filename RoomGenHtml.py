"""
RoomFinder will load a previously created matrix of rooms and using various algorithms traverse the maze in the least moves

"""
import dill

class RoomGenHtml:

    def find_rooms_html(self):
        html="""
        <html>
            <head>
                <link rel="icon" href="data:,">
                <style>
                    body {padding:20px;}
                    td {
                        padding:5px;
                        text-align:center;
                        height:25px; 
                        width:25px;
                    }
                    
                    th {
                        padding: 5px;
                        text-align: center;
                    }
            
                    .direction {
                        cursor: pointer;
                        color: rgb(195, 8, 8);
                    } 
                    #tablediv {
                        width:100%;
                        height:100%;
                    }
                    table {
                        margin: 0 auto; /* or margin: 0 auto 0 auto */
                    }
                    #images {
                        table-layout: fixed;
                        width:500px;
                        border-collapse: collapse;
                    }
                    #left,#right,#up {
                        height:532px;
                        cursor: pointer;
                        color: rgb(195, 8, 8);
                        background-size:100% 100%;
                    }
                    #down {
                        cursor: pointer;
                        color: rgb(195, 8, 8);
                        background-size:100% 100%;
                    }
                </style>
                <script type="text/javascript" src="JS/roomutils.js"></script>
                <script type="text/javascript" src="JS/render_rooms.js"></script>
                <script type="text/javascript" src="JS/explore.js"></script>
                <script type="text/javascript" src="JS/jquery/jquery-341.js"></script>
                <script type="text/javascript" src="JS/bootstrap-4.4.1-dist/js/bootstrap.min.js"></script>
                <link rel="stylesheet" href="JS/bootstrap-4.4.1-dist/css/bootstrap.min.css">
                <link rel="stylesheet" href="css/room.css">
                <script>
                    $(document).ready(function () {       
                        main();            
                    });
        
                </script>
            </head>
            <body>
                <div class="container-fluid">
                    <div class="row"> <!-- row 1 -->
                        <div class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 1 -->
                            <form method="POST" target="maze.html">
                                <table>
                                <tr><td>Create iterations:</td><td><input type="text" name="iter" value="100"></td>
                                <tr><td>Click to generate:</td><td><input type="submit" value="start"></td></tr>
                                </table>
                            </form>
                        </div>
                
                        <div id="playerstatus" class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 2 -->
                            <table style='width:100%'>
                            <tr><td>I</td><td>Your inventory</td></tr>
                            <tr><td>O</td><td>Opponent's hit points and characteristics</td></tr>
                            <tr><td>P</td><td>Player's hit points and characteristics</td></tr>
                            <tr><td>A</td><td>Attack opponent</td></tr>
                            <tr><td>D</td><td>Drink potion</td></tr>
                            <tr><td>G</td><td>gather &lt;item&gt;/td></tr>
                            <tr><td>X</td><td>Show room info;/td></tr>
                            </table>
                        </div>
                
                        <div  id="userinput" class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 3 -->
                            $>User Input
                            <input type="text" id="inputline" autofocus></text>
                        </div>
                
                        <div id="characterstatus" class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 4 -->

                        </div>
                
                    </div>
                    
                    <div class="row" style="height:700px"> <!-- row 2 -->
                        <div class="col border border-primary rounded overflow-auto" id='tablediv'> <!-- Row 2 Col 1 -->
                            <table id='grid' style='border:0px black solid; border-collapse:collapse;'>
        """
        color=""
        # Open the serialised data file in read/binary mode
        f = open("rooms.bin", "rb")

        x = []
        y = []
        # Load the saved data dictionary.
        room_ref=dill.load(f)

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
            max_num=room_ref[i].visits
            if max_num>new_max:
                new_max=max_num
        oldrange=new_max
        newrange=255 #this is FF
        print(new_max)
        # Now loop through the html grid and check if each square corresponds to a room that has beed created.
        for row in range(len(grid)):
            html+="<tr>"
            for elem in range(len(grid[row])):
                try:
                    # If a room is found then make the borders of the td match the exits that the room has
                    if room_ref[elem - x_tx, row - y_tx] is not None:
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

                        color = "border-color:black"
                        if room_ref[elem - x_tx, row - y_tx].room_name == "Start":
                            color="border-color:red"
                            text="S"
                        if room_ref[elem - x_tx, row - y_tx].room_name == "Exit":
                            color="border-color:Green"
                            text="E"
                        v=(newrange/oldrange)*room_ref[elem - x_tx, row - y_tx].visits

                        xref=elem - x_tx
                        yref=row - y_tx
                        heat_color=format(255-int(v),'02x')
                        html+="<td class='room' id='x"+str(xref)+"y"+str(yref)+"' data-weight='0' data-name='"+str(room_ref[elem - x_tx, row - y_tx].room_name)+"' title='"+str(room_ref[elem - x_tx, row - y_tx].visits)+" "+str(room_ref[elem - x_tx, row - y_tx].room_name)+"'style='"+style_n+";"+style_e+";"+style_s+";"+style_w+";" \
                              +color+"; background-color:#FF"+ heat_color+"FF; font-size:12px; text-align: center'>"
                        # html+=str(room_ref[elem - x_tx, row - y_tx].visits)
                        html+=text
                except KeyError:
                    html += "<td class='blank' style='background-color:#ffffff'>"
                print(".", end='')
        html += """
                                    </td>
                                </tr>
                            </table>
                        </div>
                        
                        <div id="scrolldiv" class="col border border-primary rounded overflow-auto"> <!-- Row 2 Col 2 -->
                            <div id="dialog" style="height:700px"></div>
                        </div>
                    </div> <!-- END row 2 -->
                </div> <!-- END container -->
             </body>
        </html>"""
        f.close()
        with open("maze.html","w") as h:
            h.write(html)

if __name__ == "__main__":
    rf = RoomGenHtml()
    rf.find_rooms_html()