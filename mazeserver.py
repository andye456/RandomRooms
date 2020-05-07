import json
import random
import sys
import traceback
from urllib import parse

import dill
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver

from CharacterMatrix import CharacterMatrix
from RandomRooms import RandomRooms
from RoomGenHtml import RoomGenHtml
from RoomMatrix import RoomMatrix
from characters import Items
from characters import Weapons
from characters.Character import Character
from characters.CharacterAbilities import CharacterAbilities
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

from characters import FriendStatus

from utils.serverutils import attack, adjust_hit_points

# Change this to 0.0.0.0:8060 for AWS
hostName = "localhost"
hostPort = 8090



def setup():
    print("opening rooms.bin to read matrix")
    f = open("rooms.bin", "rb")
    r_ref = dill.load(f)
    f.close()

    print("opening characters.bin to read characters")
    f = open("characters.bin", "rb")
    c_ref = dill.load(f)
    f.close()

    print("opening items.bin to read items")
    f = open("items.bin", "rb")
    i_ref = dill.load(f)
    f.close()

    # Add the player and other game data
    classes = ['Assassin', 'Druid', 'Illusionist', 'Monk', 'Paladin', 'Ranger']
    races = ['Dwarf','Elf','Gnome','Half_Elf','Half_Orc','Halfling','Human']
    # classes = ['Assassin']
    # races = ['Half_Orc']
    char_race = random.choice(races)
    char_class = random.choice(classes)
    weapon = Weapons.Cane
    abilities = CharacterAbilities(char_race, char_class)
    c_ref[(0, 0)] = Character("Zoran", 25, random.randint(10, 15), char_race, char_class, 0, 0, weapon, abilities.getAbilities())
    i_ref[(0, 0)] = [];

    return r_ref, c_ref, i_ref

# Adds the players game data on top of the data that has been randomly generated.
def add_game_data():
    pass

class MyServer(BaseHTTPRequestHandler):
    # Open the serialised data file in read/binary mode
    # initialise the mazes
    # NOTE If these are set here it means that they are Class attributes and must be accessed using the class name MyServer.
    # If they are accessed with self then this is fine, but changing self will not change these Class attributes.
    room_ref, character_ref, item_ref = setup()
    run = False
    rr = RandomRooms()
    rf = RoomGenHtml()
    idx = 0
    level_factor = 0
    # This is called once per GET request so can't put init code in here.
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.request_id = ''

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Serve all pages
    def do_GET(self):
        if self.path.endswith(".png"):
            f = open(self.path.strip("/"), 'rb')
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(self.path.strip("/"), 'r') as file:
                self.wfile.write(file.read().encode("UTF-8"))  # Read the file and send the contents

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        print("Body: %s" % post_data.decode('utf-8'))
        self._set_response()
        val = "-1"
        try:
            # if val is a number then generate this number of rooms
            # if it is a letter then handle this as a command
            # query_str = post_data.decode('utf-8').split("&")
            # val = query_str[0].split("=")[1]
            # MyServer.level_factor=query_str[4].split("=")[1]

            q = parse.parse_qs(post_data.decode('utf-8'))
            query_str = {k: v[0] for k, v in q.items()}
            if "iter" in query_str.keys():
                val = query_str['iter']
                MyServer.level_factor = query_str['level']

        except:
            pass
        # Generates new room matrix from a request from the web page
        # this is only called from the reset button on the form.
        # When the exit is reached the maze is regenerated but in an ajax call  - handled further down.
        if val != "-1":
            self.rr.create_rooms(val, MyServer.level_factor) # val iterations to run the room generator for.
            self.rf.generate_page()
            self.rf.find_rooms_html()
            MyServer.room_ref, MyServer.character_ref, MyServer.item_ref = setup()
            # MyServer.level_factor = 0
            MyServer.item_ref[(0, 0)] = []
            self.idx = 0
            # Calls  the GET to rerender the page
            self.do_GET()
            print("You are on level "+str(MyServer.level_factor))
        else:
            resp = json.loads(post_data.decode('utf-8'))
            cmd = ""
            try:
                cmd = resp["command"]
                print("Command entered: "+cmd)
            except KeyError:
                print("Command not recognised: "+cmd)

            ###### Show inventory ######
            if cmd == "I":
                try:
                    # The correct way to stringify an array of objects
                    item_json = json.dumps([ob.__dict__ for ob in MyServer.item_ref[(0, 0)]])
                    item_data = '{"item_data":' + item_json + '}'
                except KeyError:
                    item_data = '{"item_data": "You are carrying nothing"}'
                self.wfile.write(item_data.encode("UTF-8"))

            ##### Get the abilities of either the player or opponent
            elif cmd == "O":  # Get the characters or players strengths - this is also called when user enters "P" for their own abilities, with (0,0)
                try:
                    if resp['room_x'] != 0 and resp['room_y'] != 0:
                        MyServer.character_ref[(resp['room_x'], resp['room_y'])].hit_points + MyServer.character_ref[(resp['room_x'], resp['room_y'])].abilities['constitution']
                    char_json = json.dumps(MyServer.character_ref[(resp['room_x'], resp['room_y'])].__dict__)  # Gets the stats for the character that is in the room
                    char_data = '{"char_data":' + char_json + '}'  # make it into a JSON object
                    self.wfile.write(char_data.encode("UTF-8"))  # return it to the front end.
                except KeyError as e:
                    print("The character no longer exists")

            ###### ATTACK ######
            elif cmd == "A":
                char_data = attack((resp['room_x'], resp['room_y']), MyServer.character_ref, MyServer.item_ref, resp['you_first']);
                self.wfile.write(char_data.encode("UTF-8"))  # return it to the front end.

            ###### Gather Items ######
            elif cmd == "G" or (len(cmd) > 1 and cmd.split(" ")[0] == "G"):
                itm_list = MyServer.item_ref[(resp['room_x'], resp['room_y'])]
                # Check that the items are owned by the room and can be picked up
                item_data = '{"item_data":['
                for i in itm_list:
                    if i.owner == "room":
                        i.owner="Zoran" # my character
                        # Moves the item to your home location (0,0)
                        MyServer.item_ref[(0, 0)].append(i)
                        itm_list.remove(i)
                        item_data += json.dumps(i.__dict__)
                        if self.idx < len(itm_list) - 1:
                            item_data += ','
                        self.idx += 1

                item_data += ']}'
                self.wfile.write(item_data.encode("UTF-8"))  # return it to the front end.
            ##### Drink potions ####
            elif cmd == "D" or (len(cmd) > 1 and cmd.split(" ")[0] == "D"):
                try:
                    potion = cmd.split(" ")[1]

                    def handle_potion(potion_name, points):
                        r = "Hit Points increased by "+str(points)+"<br>"
                        idx=0
                        # Loop through the items in my room as these belong to me
                        for items in MyServer.item_ref[(0, 0)]:
                            # if any of the items match the potion name I am requesting
                            if items.item_object['name'].upper() == potion_name.upper():
                                # inform player how may uses the potion has
                                r+=potion_name+" has "+str(MyServer.item_ref[(0, 0)][idx].item_object['uses']-1)+" more uses<br>"
                                if MyServer.item_ref[(0, 0)][idx].item_object['uses'] > 0:
                                    # boost my hit points by the required amount.
                                    MyServer.character_ref[(0, 0)].hit_points += points
                                    # reduce the number of uses the potion has
                                    MyServer.item_ref[(0, 0)][idx].item_object['uses'] -= 1
                                    if MyServer.item_ref[(0, 0)][idx].item_object['uses'] <= 0:
                                        r += "You have finished " + potion_name + "<br>"
                                        del MyServer.item_ref[(0, 0)][idx]
                            idx+=1
                        return r

                    for i in MyServer.item_ref[(0, 0)]:
                        if i.item_object['name'].upper() == potion:
                            inc = int(MyServer.level_factor) + 1
                            if potion == "HEALING1" and MyServer.character_ref[(0,0)].experience >= 1 * inc:
                                ret_str=handle_potion(potion, 1)
                            elif potion == "HEALING2" and MyServer.character_ref[(0,0)].experience >= 2 * inc:
                                ret_str=handle_potion(potion,2)
                            elif potion == "HEALING3" and MyServer.character_ref[(0,0)].experience >= 3 * inc:
                                ret_str=handle_potion(potion,3)
                            elif potion == "HEALING4" and MyServer.character_ref[(0,0)].experience >= 4 * inc:
                                ret_str=handle_potion(potion,4)
                            elif potion == "HEALING5" and MyServer.character_ref[(0,0)].experience >= 5 * inc:
                                ret_str=handle_potion(potion,5)
                            else:
                                ret_str="potion has no effect as you don't have enough experience to use it.<br>You need "+str(inc)+" times level 0 exp"
                            item_data = '{"item_data": "'+ret_str+'","hit_points":"'+str(MyServer.character_ref[(0, 0)].hit_points)+'"}'
                    self.wfile.write(item_data.encode("UTF-8"))  # return it to the front end.
                except Exception as e:
                    print(e)
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

                    ret_str="what? <br>"
                    item_data = '{"item_data": "' + ret_str + '","hit_points":"'+str(MyServer.character_ref[(0, 0)].hit_points)+'"}'
                    self.wfile.write(item_data.encode("UTF-8"))
            ##### REGENERATE #####
            elif cmd == "regenerate":
                # Save existing data
                player = MyServer.character_ref[(0,0)]
                player_items = MyServer.item_ref[(0,0)]

                # Remove the old dict
                MyServer.room_ref.clear()
                MyServer.level_factor = resp['level']
                val = resp["iterations"]
                self.rr.create_rooms(val, MyServer.level_factor)  # val iterations to run the room generator for.
                self.rf.find_rooms_html()
                MyServer.room_ref,MyServer.character_ref,MyServer.item_ref = setup()

                MyServer.item_ref[(0,0)] = player_items
                self.idx = 0
                MyServer.character_ref[(0,0)] = player
                # Set the experience back to zero.
                MyServer.character_ref[(0, 0)].experience=0;
                # Calls  the GET to rerender the page
                # self.do_GET()
                print("You are on level " + str(MyServer.level_factor))
                print("Room generated at (0,-1) is: "+MyServer.room_ref[(0,-1)].room_name)

            # Deal with the new room reference
            # If the response from the web page is {"room_x": -2, "room_y": 4}
            ####### MOVEMENT #######
            else:
                # {"room_x": 0, "room_y": 0, "room_name": "Start"}

                print("You are in " + MyServer.room_ref[(resp['room_x'], resp['room_y'])].room_name)
                # print("[Visiting] MyServer.room_ref.id() = "+MyServer.room_ref.id())

                # Convert the response into a JSON object
                room_json = json.dumps(MyServer.room_ref[(resp['room_x'], resp['room_y'])].__dict__)

                room_data = '{"room_data":' + room_json

                try:
                    # _char_ref=MyServer.character_ref[(resp['room_x'],resp['room_y'])]
                    char_json = json.dumps(MyServer.character_ref[(resp['room_x'], resp['room_y'])].__dict__)
                    # Get the friend status of the character
                    fs = FriendStatus.getFriendStatus(MyServer.character_ref[(0, 0)].race, MyServer.character_ref[(resp['room_x'], resp['room_y'])].race)
                    # set the characters adjusted hit points according to their constitution
                    #MyServer.character_ref[(resp['room_x'], resp['room_y'])].hit_points += MyServer.character_ref[(resp['room_x'], resp['room_y'])].abilities['constitution']

                    char_json += ',"friend_status": "' + fs + '"'
                    room_data += ',"char_data":' + char_json

                    # If friend status is hatred then they will attack unprovoked
                    # if fs == "H":
                    #     char_json += attack((resp['room_x'], resp['room_y']), MyServer.character_ref, MyServer.item_ref, your_turn=False);

                except KeyError:
                    _char_ref = {}
                except AttributeError:
                    pass

                try:
                    item_json="["
                    ix=0
                    item_lst = MyServer.item_ref[(resp['room_x'], resp['room_y'])]
                    for i in item_lst:
                        item_json+=json.dumps(i.__dict__ )
                        if ix<len(item_lst)-1:
                            item_json+=','
                        ix+=1
                    item_json+=']'
                    room_data += ',"item_data":'+item_json
                except KeyError:
                    _char_ref = {}
                except AttributeError:
                    pass
                room_data += '}'
                print(room_data)
                # TODO: Establish your class, using the FriendStatus lookup decide whether the character in the room
                #  is an enemy

                # Returns the JSON to the html page.
                self.wfile.write(room_data.encode("UTF-8"))


try:
    svr = socketserver.TCPServer((hostName, hostPort), MyServer)
    print("Web Server running on port:"+str(hostPort))
    svr.serve_forever()
except KeyboardInterrupt:
    print(" ^C entered, stopping web server....")
    svr.socket.close()
