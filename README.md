# RandomRooms

## Concept
### Procedural generation of environment
Random rooms is just that, at set of rooms generated randomly by procedures.
When you leave a room through an exit a new room is generated as follows:

* Assign the door direction to a binary number. i.e. N=1000, E=0100, S=0010, W=0001
* Create a room using a random int between 0 and 15 to create a random combination of the above doors
* There must be an exit back into the room you've just come from
* Any adjacent rooms must have their entrances respected. So if you went North from the current room you would enter a new room, id this room has a room to the west that has an East door then the room must be created with a West door.
* Any adjacent rooms must have their non-exits respected. So in the above scenario the room to the west does not have a door, but the random door generator created an East door, then this door must be removed so a false door is not created.

## Design

### Objects

####Room
This is a class that creates a room with a certain number of exits.
The exits are a combination of N,E,S,W and are created according to the above rules.
The room is given a name and an "item" for the user to see.

####RoomMatrix
This class stores the rooms with their location in the grid. The start - the first room - is always created at 0,0, this is x=0,y=0.
Going North y=y-1, south y=y+1
West x=x-1, East x=x+1

####RoomUtils
Utility functions for room generation or navigation

####RandomRooms
This is the main class and creates rooms and adds them to the Room Matrix. This is also where you assign the rules engine to generate the rooms.
##### Rules Engines for room creation.
* Get human input for the directions to travel
* For every move choose the next direction from NESW in a round-robin fashion
* Random direction chosen from NESW
* Only picks from the exit directions available, has to know what exits are available
* Pick random direcrtion, but never uses the entrance it's just come in from
* Always try and progress to a new room given the directions.

####RoomFinder
This prints out a crude map of the current rooms

####RoomFinderHtml
This renders an html page of the room grid showing the exits

###Other files

####data.bin
This is a python