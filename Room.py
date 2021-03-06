
"""
This is a room, it is created by seeding it with a number, this tells it which exits to create.
There will always be an exit from where the player has just come from, this is the opposite direction
e.g. if in a room you exit north, then the room you enter will have an exit south.
If the number passed to the room does not create that exit, then it is created in addition.
If 0 is passed then this will create a dead-end.
"""
import RoomUtils
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

    visits=0

    # Room attributes
    # An array of any items that are in the room but can't be interacted with
    decorations = []
    # The overall style of the room, e.g. callar, attic, dungeon
    style = ""
    # Monsters that are in the room
    monsters = []

    # Takes name and description for the room
    def __init__(self, room_name, description):
        print("[ROOM] Generated "+room_name)
        self.room_name = room_name
        self.description = description


    # This creates a room, assigning N,E,S,W with 1 or 0
    # if a previous exit is passed then the opposite exit is created in this room
    # N = 1000, S = N >> 2
    # E = 0100, W = E >> 2
    # S = 0010, N = S >> 2
    # W = 0001, E = W >> 2
    # seed is an int in range 0 to 15, 0 = no doors and 15 = all 4 doors
    # from_door is the door that you've just come from - so if you exited north the from_door is North and a door in the new room needs to be created South.
    # from_door needs to be bit rotated right by 2 and ORed with seed
    # no_door - this is a direction that does not need creating as it is an adjacent room with no exit.
    def create_room(self, seed, doors):
        self.door_weights = {}

        save_seed=seed
        print("Seed = "+str(save_seed))
        self.from_door=doors[0]
        # Rotates the from_door right by 2 and updated seed to include new door if not already created
        from_door=doors[0]
        available=doors[1]
        # Addreses the door that has just been entered from
        #inv = (from_door >> 2) | (from_door << 2) & 15
        # Addresses the possible doors that are available.
        #inv2 = (possible >> 2) | (possible << 2) & 15
        seed = seed | from_door
        seed = seed & available
        # This gets a 1 or 0 from the updated seed for each direction
        self.N = (seed & 8)  >> 3
        self.E = (seed & 4)  >> 2
        self.S = (seed & 2)  >> 1
        self.W = (seed & 1)  >> 0

        self.room_code_bin="%d %d %d %d" % (self.N,self.E,self.S,self.W)
        print("room_code_bin = "+str(self.room_code_bin))
        self.room_code_int=seed

        # Initial weighting on the doors, when a door is used this number will be incremented, the bot will always
        # try and go through the door with the lease weight.
        if self.N == 1:
            self.N_weight=0
            self.door_weights["N"] = self.N_weight

        if self.E == 1:
            self.E_weight=0
            self.door_weights["E"] = self.E_weight

        if self.S == 1:
            self.S_weight=0
            self.door_weights["S"] = self.S_weight

        if self.W == 1:
            self.W_weight=0
            self.door_weights["W"] = self.W_weight

    # set the door weight when entering an existing room
    def set_door_weight(self, exit_door):
        if exit_door == 'N':
            self.N_weight+=1
            self.door_weights["N"]=self.N_weight
        if exit_door == 'E':
            self.E_weight+=1
            self.door_weights["E"]=self.E_weight
        if exit_door == 'S':
            self.S_weight+=1
            self.door_weights["S"] = self.S_weight
        if exit_door == 'W':
            self.W_weight+=1
            self.door_weights["W"] = self.W_weight

    # Return the door weights for the current room
    def get_door_weight(self):
        return self.door_weights
        # return {"N":self.N_weight, "E":self.E_weight, "S":self.S_weight, "W":self.W_weight}

    def get_room_code_int(self):
        return self.room_code_int

    def get_room_code_bin(self):
        return "N E S W\n%s" % self.room_code_bin

    def get_exits(self):
        exits = ""
        if self.N == 1:
            exits+="N"
        if self.E == 1:
            exits+="E"
        if self.S == 1:
            exits+="S"
        if self.W == 1:
            exits+="W"
        return exits

    def show_exits(self):
        exits = ""
        print("Exits are: ", end='')
        if self.N == 1:
            print("North ", end='')
            exits+="N"
        if self.E == 1:
            print("East ", end='')
            exits+="E"
        if self.S == 1:
            print("South ", end='')
            exits+="S"
        if self.W == 1:
            print("West ", end='')
            exits+="W"
        # Print an ascii representation of the room
        RoomUtils.room_gen(self.room_code_int)
        return exits


    def show_weights(self):
        print(str(self.door_weights))


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
