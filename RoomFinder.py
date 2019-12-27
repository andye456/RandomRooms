"""
RoomFinder will load a previously created matrix of rooms and using various algorithms traverse the maze in the least moves

"""
from Room import Room
from RoomMatrix import RoomMatrix
import pickle
import RoomUtils


# Open the serialised data file in read/binary mode
f = open("data.bin", "rb")

x = []
y = []
# Load the saved data dictionary.
room_ref=pickle.load(f)

# Iterate through the rooms in the dictionary
for i, j in room_ref:
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

            if (room_ref[elem - x_tx, row - y_tx].name == "Start"):
                print("S", end="")
                # print(f"{RoomUtils.bcolors.FAIL}S{RoomUtils.bcolors.ENDC}", end="")
            else:
                print("X", end="")
                # print(f"{RoomUtils.bcolors.OKBLUE}X{RoomUtils.bcolors.ENDC}", end="")
        except KeyError:
            print(" ", end="")
    print()
f.close()

