# RandomRooms
![Screenshot of Random Rooms](https://github.com/andye456/RandomRooms/blob/TextBased_ADD_Rules/RR.png)
## Concept
### Procedural generation of environment
Random rooms is just that, at set of rooms generated randomly by procedures.
When you leave a room through an exit a new room is generated as follows:

* Assign the door direction to a binary number. i.e. N=1000, E=0100, S=0010, W=0001
* Create a room using a random int between 0 and 15 to create a random combination of the above doors
* There must be an exit back into the room you've just come from
* Any adjacent rooms must have their entrances respected. So if you went North from the current room you would enter a new room, if this room has a room to the west that has an East door then the room must be created with a West door.
* Any adjacent rooms must have their non-exits respected. So in the above scenario the room to the west does not have a door, but the random door generator created an East door, then this door must be removed so a false door is not created.

To achieve the above the following algorithm was created.

    NOTE: NESW   e.g. N=1000, E=0100, S=0010, W=0001
    move to new room location (x,y)
    required_doors = random number between 0 and 15 (0000b - 1111b)
    ### Doors that are needed
    if room to west (x-1,y) has an east door:
      required door = 0001
    if room to east (x+1,y) has a west door:
      required door =  0100
    if room to north (x, y-1) has a south door:
      required door = 1000
    if room to south has a north door:
      required door = 0010

    e.g.
    west door required 0001
    south door required 0010
    random number = 10 = (1010)
    0001
    0010
    1010
    ---- OR
    1011
    so the new room would potentially have door N,S & W 
    
    If the doors that are not there are to be deleted then you must get the above result and & it with the bitmask
    1011
    0011
    ---- AND
    0011
    So doors required in new room are S,W
    
    

## Design
Random Rooms is written in Python for portability and fast prototyping.

## Latest News
Random Rooms has evolved from a just a procedurally generated maze of rooms, then to to include a 
3D representation of the maze, then the 3D view has been replaced by a
top down view with a wizard character that you can control. The machine solving of the maze in Javascript
was an academic exercise and will not be progrsees, except the techniques may be applied to the movement 
of computer controlled characters.

The direction that this project will follow now is based on the AD&D rules and characters, the maze 
representation will be kept, but any other graphics will be replaced by a test display.

Other characters in the maze will be procedurally generated and will follow the AD&D personas, 
i.e. Race-Class 
e.g. Dwarf-Ranger etc.

The rules, objects, trading system and powers etc. are all derived from from the book:

***Advanced Dungeons and Dragons Players Handbook***

**by Gary Gyrax 1978 - TSR Games**

**ISBN 0-935696-01-6**


### Objects

#### Room
This is a class that defines a room with a certain number of exits.

The exits are defined as a binary number as follows: 

    N = 1000
    E = 0100
    S = 0010
    W = 0001

The exits are created according to the rules described in the section *"Procedural generation of environment"*.

    Attributes:
    name: chosen at random from a dictionary
    description: chosen at random from the same dictionary
    N: 1 or 0 to indicate whether the room has an exit this way
    S: ditto
    E: ditto
    W: ditto
    N_weight: The number of times this door has been used
    S_weight: ditto
    E_weight: ditto
    W_weight: ditto
    door_weights: a dictionary of the above values, e.g. {'N':1, 'E':0. 'S':1, 'W': 1}
    visits: The number of times this room has been visited
    from_door: decimal 1-15 to indicate which door you've come from
    room_code_bin: 0000 to 1111 to indicate the doors
    room_code_int: decimal representation of the above. 
    

#### RoomMatrix
This class stores the rooms with their location in the grid. The start - the first room - is always created at 0,0, this is x=0,y=0.

Going North y=y-1, south y=y+1, West x=x-1, East x=x+1

This class also contains a utility method to print out an ascii representation of the current room matrix.

This method also dumps the RoomMatrix to a binary data file using the python library pickle. 
This means that the whole room matrix can be used and represented by any front end engine. In this example 
RoomFinderHtml.py is used to render the matrix as a set of rooms that can be explored either manually or by an algorithm.
 
#### RoomUtils
Utility functions for room generation or navigation

#### RandomRooms
This is the main class and creates rooms and adds them to the Room Matrix. 
This is also where you assign the rules engine to generate the rooms.

#### RoomFinder
This prints out a crude map of the current rooms

#### RoomFinderHtml
This renders an html page of the room grid showing the exits, the number of times a room has been visited is counted and a colour value is assigned. This creates a "heat-map" that can be used to optimise rules.

### Other files

#### rooms.bin
This is a data file of the dumped RoomMatrix, this uses the python library pickle. This means that any Python
program can be used to render what ever they want from this RoomMatrix object.

## Rules
The programming exercise for Random Rooms is to generate the rooms as efficiently as possible, 
so minimizing the revisits to rooms. The following methods are exp[lored to try and find the most efficient 
way to generate the rooms.
#### Human input
Get human input for the directions to travel, this is the most efficient in terms minimumising revisits, 
but obviously the slowest
#### Round Robin
For every move choose the next direction from NESW in a round-robin fashion
#### Random
Random direction chosen from NESW
#### Limited random
Picks randomly from the exit directions available, has to know what exits are available
#### No return
Pick random direcrtion from the exit directions available, but never uses the entrance it's just come in from
#### Weighted door usage
##### On exit
Every time a door is used to leave a room, the weighting on that door is incremented
##### On entry
Every time a door is used to enter a room, the weighting on that door is incremented, 
this includes initial creation
##### On exit and entry
Every time a door is used to enter or leave a room the weighting on both doors in incremented
#### Use every exit in a room
This will explore every exit a room has

## Navigating the rooms using JQuery

RandomeRoomsHtml renders the random matrix as a set of rooms (the initial intention) on a web page. 
This random matrix of rooms can be used as a "level" or a predefined set of rooms. 
The javascript has been written to use the html as the "game" and the controls to navigate the "level" are
written in javascript.
There are things that aren't known until the full matrix as been created:
* number of visits to each room by the creation algorithm. 
* The exit - this is defined as the last room created.

To make the navigation possible by javascript each table cell that represents a room will be given an 
id of xpos,ypos, e.g. id='x-10y17', this enables the rooms to be easily identified using css selectors in JQuery. 

### Doors
The doors are indicated on the HTML table by making the side of the table cell 1px wide and dashed, non exits are solid 2px wide table cell edges.

If a door does not lead to another room, like at the edge then this exit is treated like a wall.

### Rules
There will be similar navigation rules to the creation rules, the most efficient will be the one that uses an incrementing of the weighting on the doors that have been used.
For simplicity the door used will be chosen at random from the available doors.
#### Selecting a rule
Use the radio buttons to select a rule to use for navigation

#### Iterations
The number of iterations to use when navigating the rooms is set in the text box above the matrix.

#### Starting the room navigation
Click on the start room, indicated with an "S"

### Manual Navigation - deprecated
If you select manual navigation then you can only navigate by clicking on the doors in the 3D view.
Your location and direction is shown on the grid.

### 3D view - deprecated
There is a simple 3D view created using HTML canvas. This will be replaced by some graphics placed in divs that
are made visible when necessary:

Rooms with the following sets of exits (there will always be the exit you came from)
* N, NW, NE, NEW
Room types can be based on the number of times that room was visited during it's creation.

### MVC
The logic will be removed from the Javascript layer and will be handled by the server-side python.
This will be based on the location and other input attributes of the player being POSTed to the 
server every time an action is performed.
There are currently 2 interactive objects to consider
* The room matrix
* The characted matrix

Both have the same size and layout and are referenced by the players X & Y coordinates.

There will always be an exit and eventually a shop or other trasding entities - other characters
can be traded with.

Other layers to consider for inclusion are an object layer to represent objects in the maze that the
characters can use or otherwise interact with.

### Navigation
Navigation will be done by typing in N,S,E,W in the scrolling text interface.
Maybe if a certain spell/magic is used a character can teleport to a certain room.

### Characters
Characters are assigned according to how ofter a room was generated during maze creation. (initially anyway)
The race/class are chosen at random and this will dictate whether they are friend or foe according to the 
"Racial Preference Table" on page 18 of the TSR Handbook.

The player's character will have a level whgich will dictate how goos at things it is all this is in the
TSR Handbook. 
