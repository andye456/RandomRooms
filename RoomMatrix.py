# This class holds the rooms in a dictionary once they are created, this array can be saved
import dill as dill
import RoomUtils


class RoomMatrix:
    x_ref = 0
    y_ref = 0

    def __init__(self):
        # initialises the matrix to be empty
        self.room_ref = {}

    # This is used to get the room, using it's coordinates, if it exists when you user travels.
    def getRoom(self, x, y):
        return self.room_ref[(x, y)]

    # add a room at the correct position in the matrix
    def addRoom(self, ref, room):
        self.room_ref[ref] = room

    # returns the room object matrix
    def get_room_matrix(self):
        # Open the serialised data file in read/binary mode
        f = open("rooms.bin", "rb")

        # Load the saved data dictionary.
        room_ref = dill.load(f)

        return room_ref

    def dump_rooms_to_binary(self):
        # dumps the matrix of room to a binary file
        with open("rooms.bin", "wb") as f:
            dill.dump(self.room_ref, f)

    #
    # Figures out what rooms are created and prints an ascii representation of them
    # Also dumps the room matrix to a binary file that can be read by the HTML room finder
    #
    def get_room_grid(self) -> object:
        x = []
        y = []
        for i, j in self.room_ref:
            x.append(i)
            y.append(j)

        x_lim = max(x)
        x_lower = min(x)
        x_tx = 0 - x_lower
        y_lim = max(y)
        y_lower = min(y)
        y_tx = 0 - y_lower
        x_range = x_lim - x_lower + 1
        y_range = y_lim - y_lower + 1
        grid = [[0] * x_range for i in range(y_range)]
        for row in range(len(grid)):
            for elem in range(len(grid[row])):
                try:
                    if self.room_ref[elem - x_tx, row - y_tx] is not None:
                        if self.room_ref[elem - x_tx, row - y_tx].room_name == "Start":
                            print("S", end="")
                        elif self.room_ref[elem - x_tx, row - y_tx].room_name == "Exit":
                            print("E", end="")
                        else:
                            print("X", end="")
                except KeyError:
                    print(" ", end="")
            print()
        return grid
