import operator
import random
from enum import Enum
from random import randrange

import RoomUtils
from CharacterMatrix import CharacterMatrix
from ItemMatrix import ItemMatrix
from Room import Room
from RoomMatrix import RoomMatrix
from characters import Weapons
from characters.Character import Character
import characters.Items as Items
from characters.CharacterAbilities import CharacterAbilities
from characters.Item import Item

from characters.classes.Ranger import Ranger
from characters.classes.Druid import Druid
from characters.classes.Illusionist import Illusionist
from characters.classes.Monk import Monk
from characters.classes.Paladin import Paladin
from characters.classes.Assassin import Assassin

from characters.race.Gnome import Gnome
from characters.race.Elf import Elf
from characters.race.Half_Orc import Half_Orc
from characters.race.Half_Elf import Half_Elf
from characters.race.Halfling import Halfling
from characters.race.Human import Human
from characters.race.Dwarf import Dwarf


class RandomRooms():
    CHAR_CLASS = Enum('char_class', 'Druid Paladin Ranger Illusionist Assassin Monk')

    CHAR_RACE = Enum('char_race', 'Elf Gnome Dwarf Half_Elf Halfling Half_Orc Human')

    character_matrix = CharacterMatrix()
    item_matrix = ItemMatrix()

    def create_rooms(self, iterroom):

        print("Creating " + str(iterroom) + " rooms!")
        # Read random words from a file
        WORDS = []
        f = open("words.txt", "r")
        for line in f:
            WORDS.append(line.replace('\n', '').replace('\'', ''))
        f.close()

        # Create the 1st room at (0,0), these values are used to
        x_pos = 0
        y_pos = 0
        # Create a room
        room = Room("Start", "salt")
        room.create_room(15, (1, 15))
        # Creates the room matrix with the first room
        room_matrix = RoomMatrix()
        room_matrix.addRoom((0, 0), room)

        # self.character_matrix = CharacterMatrix()

        # iterator
        i = 0
        unique = 0
        found_again = 0
        wrong_direction = 0
        direction = "N"

        while True:
            # Get the list of exits, e.g. NSW (R is appended to show the current map)
            exits = room.show_exits() + "R"

            # Weighting of a door that has been used... make the route go through doors it hasn't been through before.
            ex = list(room.get_exits())
            print(room.room_name)
            door_weight = room.get_door_weight()
            # s = sorted(door_weight, key=operator.itemgetter(0))
            s = sorted(door_weight.items(), key=operator.itemgetter(1))
            print("Weights:", end='')
            print(s)
            # dict_you_want = {your_key: s[your_key] for your_key in ex}
            direction = [item for item in s[0][0]][0]

            room.set_door_weight(direction)

            print("-------------------------------------")
            print("direction = " + direction)
            if direction.upper() in exits:
                # Increment/decrement the x or y direction depending on the direction travelled.
                if direction.upper() == "N":
                    from_door = 8  # from_door is not used anymore.
                    y_pos -= 1
                if direction.upper() == "E":
                    from_door = 4
                    x_pos += 1
                if direction.upper() == "S":
                    from_door = 2
                    y_pos += 1
                if direction.upper() == "W":
                    from_door = 1
                    x_pos -= 1
                if direction.upper() == "R":
                    room_matrix.get_room_grid()

                entry_door = RoomUtils.get_opposite_door(direction)

                try:
                    character = None
                    # if the room exists use it
                    room = room_matrix.getRoom(x_pos, y_pos)
                    # increment the number of visits to this room
                    room.visits += 1
                    # find the door that was entered from and increment it's weight
                    room.set_door_weight(entry_door)
                    print("************** ROOM FOUND **************")
                    print("You are back in " + room.room_name + ", You can see " + room.description)
                    found_again += 1

                    # Add a character if the room already exists and the number of visits is over a certain amount (experimental)
                    #
                    # NOTE: To add new Class items to a character race or class: add a class variable to the race or class file
                    # To make this accessible from the HTML then add it to room_data in mazeserver.py,
                    # this will then pass JSON objects back to the javascript on the web page and can be accessed.
                    #
                    # Not sure how to change/access the individual "instace" variables of the P objects that are created in the CharacterMatrix
                    #
                    if found_again > 1:
                        print("+_+_+_+__+_+_ Adding character")
                        # Randomly selects a class and race from the available Enums

                        char_class = random.choice(list(self.CHAR_CLASS)).name
                        char_race = random.choice(list(self.CHAR_RACE)).name

                        # Dynamically creates a character type in a certain room
                        # Get some random items
                        items = Items.getRandomItems()
                        # define the characters abilities based on its race/class
                        ab = CharacterAbilities(char_race, char_class)
                        # Create the character
                        abilities = ab.getAbilities()
                        character = Character(random.choice(WORDS).capitalize(),  # its name
                                              random.randint(40, 300),  # age
                                              random.randint(3, 16),  # This sets the initial hit points for the monster
                                              char_race,
                                              char_class,
                                              items,
                                              x_pos,
                                              y_pos,
                                              Weapons.Club,
                                              abilities)
                        # Add the character to the character matrix
                        self.character_matrix.addCharacter((x_pos, y_pos), character)
                    if found_again > 0:
                        I=[]
                        # If the character exists in this room then associate this item with the character
                        if character is not None:
                            c = character.name
                        else:
                            c = ""
                        for itm in Items.getRandomItems():
                            I.append(Item(itm,c))
                            self.item_matrix.addItem((x_pos, y_pos),I)


                except KeyError:
                    # Create a new room
                    unique += 1
                    # Give the room a name and content
                    room = Room(random.choice(WORDS), random.choice(WORDS))
                    # Find adjacent rooms and any doors that should be created to them
                    int_door_ref = RoomUtils.find_neighbours(room_matrix, x_pos, y_pos)

                    # TODO: Change from_door to from_doors for multiple doors that are needed.
                    # TODO: Also don't create a room if the neighbour room doesn't have that exit!!!
                    room.create_room(randrange(16), int_door_ref)
                    room.set_door_weight(entry_door)
                    room_matrix.addRoom((x_pos, y_pos), room)

            else:
                print("Direction not valid")
                wrong_direction += 1

            i += 1
            print("Iteration: " + str(i))
            # When all the iterations are done
            if i == int(iterroom):
                room = room_matrix.getRoom(x_pos, y_pos)
                room.room_name = "Exit"
                room.description = "The way out"
                # Prints out an ascii representation of the matrix
                room_matrix.get_room_grid()

                # dumps the RoomMatrix to an external binary file.
                room_matrix.dump_rooms_to_binary()

                # dumps the characters to a binary file.
                self.character_matrix.dump_chars_to_binary()

                # dump the items to a file
                self.item_matrix.dump_items_to_binary()

                # Prints some stats
                print("New Rooms = " + str(unique))
                print("Revisited = " + str(found_again))
                print("Wrong direction = " + str(wrong_direction))
                break


if __name__ == "__main__":
    r = RandomRooms()
    r.create_rooms(100)
