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
This is a class that creates a room with a certain number of exits.
The exits are a combination of N,E,S,W and are created according to the above rules.
The room is given a name and an "item" for the user to see.

#### RoomMatrix
This class stores the rooms with their location in the grid. The start - the first room - is always created at 0,0, this is x=0,y=0.
Going North y=y-1, south y=y+1
West x=x-1, East x=x+1
This class also contains a utility method to print out an ascii representation of the current room matrix.
This method also dumps the RoomMatrix to a binary data file using the python library pickle.

#### RoomUtils
Utility functions for room generation or navigation

#### RandomRooms
This is the main class and creates rooms and adds them to the Room Matrix. This is also where you assign the rules engine to generate the rooms.

#### RoomFinder
This prints out a crude map of the current rooms

#### RoomFinderHtml
This renders an html page of the room grid showing the exits, the number of times a room has been visited is counted and a colour value is assigned. This creates a "heat-map" that can be used to optimise rules.

### Other files

#### data.bin
This is a data file of the dumped RoomMatrix, this uses the python library pickle.

## Rules
The programming exercise for RR is to generate the rooms as efficiently as possible, so minimizing the revisits to rooms.
#### Human input
Get human input for the directions to travel, this is the most efficient in terms minimumising revisits, but obviously the slowest
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
Every time a door is used to enter a room, the weighting on that door is incremented, this includes initial creation
##### On exit and entry
Every time a door is used to enter or leave a room the weighting on both doors in incremented
#### Use every exit in a room
This will explore every exit a room has

## Navigating the rooms

This was an afterthought really, it's actually fairly simple to write a JavaScript function or two to navigate round the maze once it has been created and rendered in HTML.

To make the navigation possible each table cell that represents a room will be given an id of xpos,ypos, e.g. id='x-10y17', this enables the rooms to be easily identified using css selectors in JQuery. 

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