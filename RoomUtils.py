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
        e_n = "╔═  ═╗"
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
    print(e_w + "    " + e_e)
    print(e_s)


# Finds neighbours of the room that is about to be created
# If the North room contains a south exit then create a north exit etc.
# from_doors are doors that must be created because they exist in adjacent rooms
# available are doors that can exist, either because an adjacent room has not been created or that the room has no exit to the current room.
"""
rnd     bin     mask    OR then AND     XOR
0       0000    1010    1010   1010 
1       0001            1011   1010
2       0010            1010   1010 
3       0011            1011   
4       0100            1110    
5       0101            1111    
6       0110                    
7       0111                    
8       1000                    
9       1001
10      1010
11      1011
12      1100
13      1101
14      1110
15      1111

When the room is created the from_doors is ORed with the seed (the random number) then ANDed with the available.
This causes unavailable doors to be removed from any possible random door position.
"""
def find_neighbours(room_ref, x, y):
    from_doors = 0
    available = 0
    try:
        # Check north room and add north to the current room (b1000, 8) if a south exit is present
        if room_ref.getRoom(x, y - 1).S == 1:
            from_doors += 8
            available += 8
    except:
        # If the room does not exist to this direction then add a '1' to the bitmask as it can have an exit that way
        available += 8

    try:
        # Check south room and add a south to the current room(b0010, 2 if a North exit is present
        if room_ref.getRoom(x, y + 1).N == 1:
            from_doors += 2
            available += 2
    except:
        available += 2

    try:
        # Check west room and add a west to the current room (b0001, 1) if an east exit is present
        if room_ref.getRoom(x - 1, y).E == 1:
            from_doors += 1
            available += 1
    except:
        available += 1
    try:
        # Check east room and add an east to the current room (b0100, 4) if a west exit is present
        if room_ref.getRoom(x + 1, y).W == 1:
            from_doors += 4
            available += 4
    except:
        available += 4

    return (from_doors,available)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
