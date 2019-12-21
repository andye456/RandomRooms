from random import randrange
import random
import requests
from Room import Room
from RoomMatrix import RoomMatrix

word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(word_site)
WORDS = response.content.splitlines()
x_pos=0
y_pos=0
position=(x_pos,y_pos) # this is a tuple that holds the co-ordinates of the room
room = Room("Start", "This room is large")
room.create_room(15,1)
matrix = RoomMatrix(room) # Creates the room matrix with the first room
while (True):
    exits = room.show_exits()+"R"
    direction = input("Enter Direction...")
    print("-------------------------------------")

    if(direction.upper() in exits):
        if (direction.upper() == "N"):
            from_door=8
            y_pos+=1
        if (direction.upper() == "E"):
            from_door=4
            x_pos+=1
        if (direction.upper() == "S"):
            from_door=2
            y_pos-=1
        if (direction.upper() == "W"):
            from_door=1
            x_pos-=1
        if (direction.upper() == "R"):
            matrix.get_room_grid();
        try:
            # if the room exists use it
            room =  matrix.getRoom(x_pos,y_pos)
            print ("You are in "+room.name+", You can see "+room.description)
        except KeyError:
            # Create a new room
            room = Room(random.choice(WORDS).decode('utf-8'), random.choice(WORDS).decode('utf-8'))
            room.create_room(randrange(16), from_door)
            matrix.addRoom(direction.upper(),room)
    else:
        print("Direction not valid")
