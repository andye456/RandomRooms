from RoomMatrix import RoomMatrix

# Gets N,E,S,W from 0001 etc
def get_direction_from_bin(bin):
    if bin == "1000":
        return "N"
    if bin == "0100":
        return "E"
    if bin == "0010":
        return "S"
    if bin == "0001":
        return "W"

def get_int_from_direction(direction):
    if direction == "N":
        return 8
    if direction == "E":
        return 4
    if direction == "S":
        return 2
    if direction == "W":
        return 1

def get_opposite_door(direction):
    if direction == "N":
        return "S"
    if direction == "E":
        return "W"
    if direction == "S":
        return "N"
    if direction == "W":
        return "E"

def room_gen(room_int_val):
    print(room_int_val)
    if (room_int_val & 8) >> 3 == 1:
        e_n="╔═  ═╗"
    else:
        e_n = "╔════╗"
    if (room_int_val & 4) >> 2 == 1:
        e_e = " "
    else:
        e_e = "║"
    if (room_int_val & 2) >> 1 == 1:
        e_s = "╚═  ═╝"
    else:
        e_s = "╚════╝"
    if (room_int_val & 1) >> 0 == 1:
        e_w = " "
    else:
         e_w = "║"
    print("")
    print(e_n)
    print(e_w+"    "+e_e)
    print(e_s)

# Finds neighbours of the room that is about to be created
# If the North room contains a south exit then create a north exit etc.
def find_neighbours(room_ref,x,y):
    code=0
    try:
        # Check north room and add north to the current room (b1000, 8) if a south exit is present
        if room_ref.getRoom(x,y-1).S == 1:
            code+=2
        if room_ref.getRoom(x, y - 1).S == 0:
            if code > 1:
                code-=2
    except:
        pass
    try:
        # Check south room and add a south to the current room(b0010, 2 if a North exit is present
        if room_ref.getRoom(x ,y + 1).N == 1:
            code+=8
        if room_ref.getRoom(x, y + 1).N == 0 and code > 7:
            code-=8
    except:
        pass
    try:
        # Check west room and add a west to the current room (b0001, 1) if an east exit is present
        if room_ref.getRoom(x-1,y).E == 1:
            code+=4
        if room_ref.getRoom(x - 1, y).E == 0:
            if code > 3:
                code-=4
    except:
        pass
    try:
        # Check east room and add an east to the current room (b0100, 4) if a west exit is present
        if room_ref.getRoom(x+1,y).W == 1:
            code+=1
        if room_ref.getRoom(x + 1, y).W == 0:
            if code > 0:
                code-=1
    except:
        pass # no rooms

    return code

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'