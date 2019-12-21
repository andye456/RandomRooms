
"""
This is a room, it is created by seeding it with a number, this tells it which exits to create.
There will always be an exit from whene the player has just come from, this is the opposite direction
e.g. if in a room you exit north, then the room you enter will have an exit south.
If the number passed to the room does not create that exit, then it is created in addition.
If 0 is passed then this will create a dead-end.
"""
class Room:

    # NESW
    # 1000 0100 0010 0001 (1-15)
    """
     --|N|--
    |       |
    -       -
    W       E
    -       -
    |       |
     --|S|--

    """

    from_door=0

    # Takes name and description for the room
    def __init__(self, name, description):
        print("You are in a place called ["+name+ "] You can see lots of ["+description+"]")
        self.name = name
        self.description = description


    # This creates a room, assigning N,E,S,W with 1 or 0
    # if a previous exit is passed then the opposite exit is created in this room
    # N = 1000, S = N >> 2
    # E = 0100, W = E >> 2
    # S = 0010, N = S >> 2
    # W = 0001, E = W >> 2
    # seed is an int in range 0 to 15, 0 = no doors and 15 = all 4 doors
    # from_door needs to be bit rotated right by 2 and ORed with seed.
    def create_room(self, seed, from_door):
        self.from_door=from_door
        # Rotates the from_door right by 2 and updated seed to include new door if not already created
        inv = (from_door >> 2) | (from_door << 2) & 15
        seed = seed | inv
        # This gets a 1/0 from the updated seed for each direction
        self.N = (seed & 8)  >> 3
        self.E = (seed & 4)  >> 2
        self.S = (seed & 2)  >> 1
        self.W = (seed & 1)  >> 0

        self.room_code_bin="%d %d %d %d" % (self.N,self.E,self.S,self.W)
        self.room_code_int=seed

    def get_room_code_int(self):
        return self.room_code_int

    def get_room_code_bin(self):
        return "N E S W\n%s" % self.room_code_bin

    def show_exits(self):
        exits = ""
        print("Exits are: ", end='')
        if self.N == 1:
            print("North ", end='')
            e_n="╔═  ═╗"
            exits+="N"
        else:
            e_n = "╔════╗"
        if self.E == 1:
            print("East ", end='')
            e_e = " "
            exits+="E"
        else:
            e_e = "║"
        if self.S == 1:
            print("South ", end='')
            e_s="╚═  ═╝"
            exits+="S"
        else:
            e_s="╚════╝"

        if self.W == 1:
            print("West ", end='')
            e_w = " "
            exits+="W"
        else:
            e_w = "║"
        print("")
        print(e_n)
        print(e_w+"    "+e_e)
        print(e_s)

        return exits

# Unit test for this class
if __name__ == "__main__":
    nums = [1,2,4,8]
    for f in nums:
        r1 = Room("Test Room","A room for test %d" % f)
        r1.set_from_door(f)
        for i in range(0,16):
            r1.create_room(i);
            r1.show_exits()
            print(r1.get_room_code_bin())
            print("----------------------------")
        print ("=========================")
