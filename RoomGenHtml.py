"""
RoomFinder will load a previously created matrix of rooms and using various algorithms traverse the maze in the least moves

"""
import dill

class RoomGenHtml:

    def generate_page(self):
        html = """
        <html>
            <head>
                <link rel="icon" href="data:,">
                <style>
                    body {padding:20px;}
                    td {
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
                            <form method="POST" target="maze.html" id="reset">
                                <table>
                                <tr><td>Create iterations:</td><td><input type="text" name="iter" id="iter" value="100"></td>
                                <tr><td>Target Experience:</td><td><input type="text" name="targetexp" id="targetexp" readonly></td></tr>
                                <tr><td>Current Experience:</td><td><input type="text" name="currentexp" id="currentexp" readonly></td></tr>
                                <tr><td>Current Hit Points:</td><td><input type="text" name="currenthit" id="currenthit" readonly></td></tr>                                
                                <tr><td>Current Level:</td><td><input type="text" name="level" id="level" readonly></td></tr>
                                <tr><td>Click to regenerate:</td><td><input type="submit" value="reset"></td></tr>
                                </table>
                            </form>
                        </div>

                        <div id="playerstatus" class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 2 -->
                            <table style='width:100%'>
                            <tr><td>i</td><td>Your inventory</td></tr>
                            <tr><td>o</td><td>Opponent's hit points and characteristics</td></tr>
                            <tr><td>p</td><td>Player's hit points and characteristics</td></tr>
                            <tr><td>a</td><td>Attack opponent</td></tr>
                            <tr><td>d</td><td>Drink potion</td></tr>
                            <tr><td>g</td><td>gather &lt;item&gt;</td></tr>
                            <tr><td>x</td><td>Show room info</td></tr>
                            </table>
                        </div>

                        <div  id="userinput" class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 3 -->
                            $>User Input
                            <input type="text" id="inputline" autofocus></text>
                        </div>

                        <div id="characterstatus" class="col-3 col-md-offset-2 border border-primary rounded"> <!-- Row 1 Col 4 -->
                            <h6>Objectives</h6>
                            <p>Simple - get to the highest level!<br>
                            Navigate the maze using n,s,e,w typed in to the User Input box<br>
                            The numbers in the rooms are the strength of the healing potions<br>
                            You must be at that level to use that strength potion.<br>
                            You need a certain amount of experience to exit the maze, this target is shown on left.<br>
                            Battle monsters to steal their items & trade with allies.<br>
                            If you get stuck or defeated hit "reset" - back to beginning!
                            
                        </div>

                    </div>

                    <div class="row" style="height:700px"> <!-- row 2 -->
                        <div class="col border border-primary rounded overflow-auto" id='tablediv'> <!-- Row 2 Col 1 -->
                        </div>
                        
                        <div id="scrolldiv" class="col border border-primary rounded overflow-auto"> <!-- Row 2 Col 2 -->
                            <div id="dialog" style="height:700px"></div>
                        </div>
                    </div> <!-- END row 2 -->
                </div> <!-- END container -->
             </body>
        </html>"""
        with open("maze.html","w") as h:
            h.write(html)



    def find_rooms_html(self):
        table = """
        <table id='grid' style='border:0px black solid; border-collapse:collapse;'>
        """
        color=""
        # Open the serialised data file in read/binary mode
        f = open("rooms.bin", "rb")

        x = []
        y = []
        # Load the saved data dictionary.
        room_ref=dill.load(f)
        f.close()
        f = open("items.bin", "rb")
        item_ref=dill.load(f)
        f.close()

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
        # Now loop through the html grid and check if each square corresponds to a room that has been created.
        for row in range(len(grid)):
            table+="<tr>"
            for elem in range(len(grid[row])):
                try:
                    # Get the room code (no. of doors) - if the neighbour NESW is blank then subtract that val
                    if room_ref[elem - x_tx, row - y_tx] is not None:
                        val = room_ref[elem - x_tx, row - y_tx].room_code_int

                        # make adjustment for neighbouring room being blank
                        # Remove the door if the dor exists and it leads nowhere
                        if (val & 8) >> 3 == 1 and room_ref.get((elem - x_tx, row - y_tx-1)) is None:
                            val -= 8
                        if (val & 4) >> 2 == 1 and room_ref.get((elem - x_tx+1, row - y_tx)) is None:
                            val -= 4
                        if (val & 2) >> 1 == 1 and room_ref.get((elem - x_tx, row - y_tx+1)) is None:
                            val -= 2
                        if (val & 1) >> 0 == 1 and room_ref.get((elem - x_tx-1, row - y_tx)) is None:
                            val -= 1

                        if val == 15:
                            room_style='background-image:url(./images/1x/nesw.png); background-size:contain;'
                        elif val == 14:
                            room_style = 'background-image:url(./images/1x/nes.png); background-size:contain;'
                        elif val == 13:
                            room_style='background-image:url(./images/1x/new.png); background-size:contain;'
                        elif val == 12:
                            room_style = 'background-image:url(./images/1x/ne.png); background-size:contain;'
                        elif val == 11:
                            room_style = 'background-image:url(./images/1x/nsw.png); background-size:contain;'
                        elif val == 10:
                            room_style = 'background-image:url(./images/1x/ns.png); background-size:contain;'
                        elif val == 9:
                            room_style = 'background-image:url(./images/1x/nw.png); background-size:contain;'
                        elif val == 8:
                            room_style = 'background-image:url(./images/1x/n.png); background-size:contain;'
                        elif val == 7:
                            room_style = 'background-image:url(./images/1x/esw.png); background-size:contain;'
                        elif val == 6:
                            room_style = 'background-image:url(./images/1x/es.png); background-size:contain;'
                        elif val == 5:
                            room_style = 'background-image:url(./images/1x/ew.png); background-size:contain;'
                        elif val == 4:
                            room_style = 'background-image:url(./images/1x/e.png); background-size:contain;'
                        elif val == 3:
                            room_style = 'background-image:url(./images/1x/sw.png); background-size:contain;'
                        elif val == 2:
                            room_style = 'background-image:url(./images/1x/s.png); background-size:contain;'
                        elif val == 1:
                            room_style = 'background-image:url(./images/1x/w.png); background-size:contain;'
                        text=""

                        color = "border-color:black"

                        if (elem - x_tx, row - y_tx) in item_ref.keys():
                            for itm in item_ref[elem - x_tx, row - y_tx]:
                                if 'power' in itm.item_object.keys():
                                    text=str(itm.item_object['power'])
                                else:
                                    text="*"

                        if room_ref[elem - x_tx, row - y_tx].room_name == "Start":
                            color="border-color:red"
                            text="S"
                        if room_ref[elem - x_tx, row - y_tx].room_name == "Exit":
                            color="border-color:Green"
                            text="E"
                        if oldrange > 0:
                            v=(newrange/oldrange)*room_ref[elem - x_tx, row - y_tx].visits
                        else:
                            v=0

                        xref=elem - x_tx
                        yref=row - y_tx
                        heat_color=format(255-int(v),'02x')

                        # Puts the right room image in.
                        table+="<td class='room' id='x"+str(xref)+"y"+str(yref)+"' data-weight='0' data-name='" \
                              +str(room_ref[elem - x_tx, row - y_tx].room_name)+ \
                              "' data-room-code-int='"+str(val)+ \
                              "' title='"+str(room_ref[elem - x_tx, row - y_tx].visits)+" "+str(room_ref[elem - x_tx, row - y_tx].room_name) \
                              +"'style='"+room_style+";" \
                              +color+"; background-color:#FF"+ heat_color+"FF; font-size:12px; text-align: center'>"

                        # Puts the number of visits during generation in the room
                        # html+=str(room_ref[elem - x_tx, row - y_tx].visits)
                        table+=text
                except KeyError as ke:
                    table += "<td class='blank' style='background-color:#ffffff'>"
                print(".", end='')
        table += """
                                    </td>
                                </tr>
                            </table>
        """
        with open("matrix.html","w") as h:
            h.write(table)

if __name__ == "__main__":
    rf = RoomGenHtml()
    rf.find_rooms_html()
    rf.generate_page()