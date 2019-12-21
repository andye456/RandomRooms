# This class holds the rooms in a dictionary once they are created, this array can be saved
class RoomMatrix:

    x_ref = 0
    y_ref = 0
    room_ref={}
    def __init__(self, room):
        self.addRoom(0,room)
        pass

    # This is used to get the room, using it's coordinates, if it exists when you user travels.
    def getRoom(self, x, y):
        return self.room_ref[(x,y)]

    # add a room at the correct position in the matrix
    def addRoom(self, entered_from, room):
        if entered_from == "N": self.y_ref+=1
        if entered_from == "S": self.y_ref-=1
        if entered_from == "E": self.x_ref+=1
        if entered_from == "W": self.x_ref-=1
        self.room_ref[(self.x_ref,self.y_ref)]=room
        # print(self.room_ref)

    def get_room_grid(self):
        x=[]
        y=[]
        for i,j in self.room_ref:
            x.append(i)
            y.append(j)
            # print(i,j)
            # print("x=",)
            # print(x)
            # print("y=",)
            # print(y)
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
                # print(grid[row][elem], end=' ')
                try:
                    if(self.room_ref[elem-x_tx,row-y_tx] is not None):
                        grid[row][elem]="1"
                        print("X", end="")
                except KeyError:
                    grid[row][elem]="0"
                    print(" ",end="")
            print()
        for i in reversed(grid):
            for j in range(len(grid[i])):
                if grid[i][j] == "1":
                    print("X", end="")
                else:
                    print(" ", end="")
            print()
            #print(grid[row])


