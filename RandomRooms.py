import operator
from random import randrange
import random
import requests
from Room import Room
from RoomMatrix import RoomMatrix
import RoomUtils

# word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
# response = requests.get(word_site)
# WORDS = response.content.splitlines()

# Read random words from a file
WORDS=[]
f = open ("words.txt", "r")
for line in f:
    WORDS.append(line.replace('\n',''))
f.close()

# Create the 1st room at (0,0), these values are used to
x_pos=0
y_pos=0
# Create a room
room = Room("Start", "salt")
room.create_room(15,(1,15))
# Creates the room matrix with the first room
matrix = RoomMatrix(room)
all_directions=['N','E','S','W']
# iterator
i=0
unique=0
found_again=0
wrong_direction=0
direction = "N"

while (True):
    # Get the list of exits, e.g. NSW (R is appended to show the current map)
    exits = room.show_exits()+"R"

    ##########################################
    # Rules engine
    # Different rules for traversing the rooms
    ##########################################

    # 1 #
    # Get human input
    # direction = input("Enter Direction...")

    # 2 #
    # Get AI input - cycle through directions in turn
    # direction = all_directions[i % len(all_directions)]

    # 3 #
    # Random direction chosen from NESW
    # direction=all_directions[randrange(len(all_directions))]

    # 4 #
    # Only picks from the exit directions available, has to know what exits are available
    # ex = list(room.get_exits())
    # try:
    #     direction = ex[randrange(len(ex))]
    # except:
    #     grid = matrix.get_room_grid()


    # 5 #
    # Never uses the entrance it's just come in from
    # ex = list(room.get_exits())
    # if len(ex) > 1:
    #     ex.remove(RoomUtils.get_opposite_door(direction))
    # direction = ex[randrange(len(ex))]

    # 6 #
    # Weighting of a door that has been used... make the route go through doors it hasn't been through before.
    ex = list(room.get_exits())
    print(room.name)
    door_weight=room.get_door_weight()
    # s = sorted(door_weight, key=operator.itemgetter(0))
    s = sorted(door_weight.items(), key=operator.itemgetter(1))
    print("Weights:", end='')
    print(s)
    # dict_you_want = {your_key: s[your_key] for your_key in ex}
    direction = [item for item in s[0][0]][0]

    room.set_door_weight(direction)

    print("-------------------------------------")
    print("direction = "+direction)
    if(direction.upper() in exits):
        # Increment/decrement the x or y direction depending on the direction travelled.
        if (direction.upper() == "N"):
            from_door=8 # from_door is not used anymore.
            y_pos-=1
        if (direction.upper() == "E"):
            from_door=4
            x_pos+=1
        if (direction.upper() == "S"):
            from_door=2
            y_pos+=1
        if (direction.upper() == "W"):
            from_door=1
            x_pos-=1
        if (direction.upper() == "R"):
            matrix.get_room_grid()

        entry_door = RoomUtils.get_opposite_door(direction)

        try:
            # if the room exists use it
            room =  matrix.getRoom(x_pos,y_pos)
            # increment the number of visits to this room
            room.visits+=1
            # find the door that was entered from and increment it's weight
            room.set_door_weight(entry_door)
            print("************** ROOM FOUND **************")
            print ("You are back in "+room.name+", You can see "+room.description)
            found_again+=1
        except KeyError:
            # Create a new room
            unique+=1
            # Give the room a name and content
            room = Room(random.choice(WORDS), random.choice(WORDS))
            # Find adjacent rooms and any doors that should be created to them
            int_door_ref=RoomUtils.find_neighbours(matrix,x_pos,y_pos)

            # TODO: Change from_door to from_doors for multiple doors that are needed.
            # TODO: Also don't create a room if the neighbour room doesn't have that exit!!!
            room.create_room(randrange(16), int_door_ref)
            room.set_door_weight(entry_door)
            matrix.addRoom((x_pos,y_pos),room)
    else:
        print("Direction not valid")
        wrong_direction+=1

    i+=1
    print(i)
    if i == 10000:
        # This bit also dumps the RoomMatrix to an external binary file.
        grid = matrix.get_room_grid()
        print("New Rooms = "+str(unique))
        print("Revisited = "+str(found_again))
        print("Wrong direction = "+str(wrong_direction))
        break


