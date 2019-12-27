# This class holds the rooms in a dictionary once they are created, this array can be saved
import pickle
import RoomUtils
class RoomMatrix:

    x_ref = 0
    y_ref = 0
    room_ref={}

    def __init__(self):
        pass

    # Creates the first room at 0,0
    def __init__(self, room):
        self.addRoom((0,0),room)

    # This is used to get the room, using it's coordinates, if it exists when you user travels.
    def getRoom(self, x, y):
        return self.room_ref[(x,y)]

    # add a room at the correct position in the matrix
    def addRoom(self, ref, room):
        self.room_ref[ref]=room

    #
    # Figures out what rooms are created and prints an ascii representation of them
    #
    def get_room_grid(self):
        x=[]
        y=[]
        for i,j in self.room_ref:
            x.append(i)
            y.append(j)
        # dumps the matrix of room to a binary file
        with open("data.bin","wb") as f:
            pickle.dump(self.room_ref, f)

        x_lim=max(x)
        x_lower=min(x)
        x_tx=0-x_lower
        y_lim=max(y)
        y_lower=min(y)
        y_tx=0-y_lower
        x_range=x_lim-x_lower+1
        y_range=y_lim-y_lower+1
        grid=[[0] * x_range for i in range(y_range)]
        for row in range(len(grid)):
            for elem in range(len(grid[row])):
                try:
                    if(self.room_ref[elem-x_tx,row-y_tx] is not None):
                        if(self.room_ref[elem-x_tx,row-y_tx].name == "Start"):
                            # print("S", end="")
                            print(f"{RoomUtils.bcolors.FAIL}S{RoomUtils.bcolors.ENDC}", end="")
                        else:
                            # print("X", end="")
                            print(f"{RoomUtils.bcolors.OKBLUE}X{RoomUtils.bcolors.ENDC}", end="")
                except KeyError:
                    print(" ",end="")
            print()
        return grid


