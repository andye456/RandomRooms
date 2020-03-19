# RandomRooms

## Concept
### Procedural generation of environment
Random rooms is just that, at set of rooms generated randomly by procedures.
When you leave a room through an exit a new room is generated as follows:

* Assign the door direction to a binary number. i.e. N=1000, E=0100, S=0010, W=0001
* Create a room using a random int between 0 and 15 to create a random combination of the above doors
* There must be an exit back into the room you've just come from
* Any adjacent rooms must have their entrances respected. So if you went North from the current room you would enter a new room, if this room has a room to the west that has an East door then the room must be created with a West door.
* Any adjacent rooms must have their non-exits respected. So in the above scenario the room to the west does not have a door, but the random door generator created an East door, then this door must be removed so a false door is not created.

## Design
Random Rooms is written in Python for portability and fast prototyping.

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

#### data.bin
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

### Manual Navigation
If you select manual navigation then you can only navigate by clicking on the doors in the 3D view.
Your location and direction is shown on the grid.

### 3D view
There is a simple 3D view created using HTML canvas. This will be replaced by some graphics placed in divs that
are made visible when necessary:

Rooms with the following sets of exits (there will always be the exit you came from)
* N, NW, NE, NEW
Room types can be based on the number of times that room was visited during it's creation.
![screen shot](https://github.com/andye456/RandomRooms/blob/master/random_rooms.png)
