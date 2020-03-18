import json
import random

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

# Change this to 0.0.0.0:8060 for AWS
hostName = "localhost"
hostPort = 8080


def adjust_hit_points(const):
    if const < 6:
        return -1
    if 5 < const < 10:
        return 1
    if const > 9:
        return 1


def adjust_dmg(strength):
    if strength < 6:
        return -1
    if 5 < strength < 10:
        return 1
    if strength > 9:
        return 1


def setup():
    print("opening rooms.bin to read matrix")
    f = open("rooms.bin", "rb")
    room_ref = dill.load(f)
    f.close()

    print("opening characters.bin to read characters")
    f = open("characters.bin", "rb")
    character_ref = dill.load(f)
    f.close()

    print("opening items.bin to read items")
    f = open("items.bin", "rb")
    item_ref = dill.load(f)
    f.close()

    return room_ref, character_ref, item_ref


class MyServer(BaseHTTPRequestHandler):
    # initialise the mazes
    room_ref, character_ref, item_ref = setup()

    item_ref[(0, 0)] = []
    idx = 0

    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.request_id = ''
        # Open the serialised data file in read/binary mode

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Serve all pages
    def do_GET(self):
        if self.path.endswith(".jpg"):
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
            val = post_data.decode('utf-8').split("=")[1]
        except:
            pass
        # Generates new room from a request from the web page
        if val != "-1":
            rr = RandomRooms()
            rr.create_rooms(val)
            rf = RoomGenHtml()
            rf.find_rooms_html()
            # Calls  the GET to rerender the page
            self.room_ref, self.character_ref, self.item_ref = setup()
            self.do_GET()
        else:
            resp = json.loads(post_data.decode('utf-8'))
            cmd = ""
            try:
                cmd = resp["command"]
            except KeyError:
                pass
            if cmd == "I":  # Show inventory
                try:
                    # The correct way to stringify an array of objects
                    item_json = json.dumps([ob.__dict__ for ob in self.item_ref[(0, 0)]])
                    item_data = '{"item_data":' + item_json + '}'
                except KeyError:
                    item_data = '{"item_data": "You are carrying nothing"}'
                self.wfile.write(item_data.encode("UTF-8"))
            elif cmd == "P":  # Get strengths
                char_json = json.dumps(self.character_ref[(0, 0)].__dict__)
                char_data = '{"char_data":' + char_json + '}'
                self.wfile.write(char_data.encode("UTF-8"))
            elif cmd == "O":  # Get the characters strengths
                char_json = json.dumps(self.character_ref[(resp['room_x'], resp['room_y'])].__dict__)  # Gets the stats for the character that is in the room
                char_data = '{"char_data":' + char_json + '}'  # make it into a JSON object
                self.wfile.write(char_data.encode("UTF-8"))  # return it to the front end.
            elif cmd == "A":  # attack
                # Get a reference to the monster character object
                them = self.character_ref[(resp['room_x'], resp['room_y'])]
                # get a reference to your character object
                you = self.character_ref[(0, 0)]
                # Get the damage figures from their current weapons
                their_dmg = random.randint(them.weapon['min_damage_large_opponent'],
                                           them.weapon['max_damage_large_opponent'])

                your_dmg = random.randint(you.weapon['min_damage_small_opponent'],
                                          you.weapon['max_damage_small_opponent'])

                # Take their_damage and your damage away from your hit points
                you.hit_points = you.hit_points + adjust_hit_points(you.abilities['constitution'])
                them.hit_points = them.hit_points + adjust_hit_points(them.abilities['constitution'])

                # Adjust the damage according to the strength of the character
                their_total_dmg = their_dmg + adjust_dmg(them.abilities['strength'])
                your_total_dmg = your_dmg + adjust_dmg(you.abilities['strength'])

                you.hit_points -= their_total_dmg
                them.hit_points -= your_total_dmg

                if you.hit_points < 1:
                    char_data = '{"char_data":"lose"}'
                    self.character_ref.pop((0, 0))
                    # self.character_ref.
                elif them.hit_points < 1:
                    char_data = '{"char_data":"win"}'
                    # Increase your experience by one.
                    self.character_ref[(0,0)].experience+=1
                    # ToDo:  Remove the character from the game - change this to have the character die eventually
                    #  when their life gets down to 0 then you can loot them
                    self.character_ref.pop((resp['room_x'], resp['room_y']))
                    # Change the ownership of any items to room
                    for d in self.item_ref[(resp['room_x'], resp['room_y'])]:
                        d.owner = "room"
                else:
                    char_data = '{"char_data":", hit-points remaining.... You: '+str(you.hit_points)+' Them: '+str(them.hit_points)+'"}'
                self.wfile.write(char_data.encode("UTF-8"))  # return it to the front end.

            elif cmd == "G": # Gather items
                # Gets the stats for the character that is in the room
                itm_list = self.item_ref[(resp['room_x'], resp['room_y'])]

                # Check that the items are owned by the room and can be picked up
                item_data = '{"item_data":['
                for i in itm_list:
                    if i.owner == "room":
                        i.owner="Zoran" # my character
                        self.item_ref[(0, 0)].append(i)

                        item_data += json.dumps(i.__dict__)
                        if self.idx < len(itm_list) - 1:
                            item_data += ','
                        self.idx += 1

                item_data += ']}'
                self.wfile.write(item_data.encode("UTF-8"))  # return it to the front end.
            else:
                # {"room_x": 0, "room_y": 0, "room_name": "Start"}

                print("You are in " + self.room_ref[(resp['room_x'], resp['room_y'])].room_name)
                # Convert the response into a JSON object
                room_json = json.dumps(self.room_ref[(resp['room_x'], resp['room_y'])].__dict__)

                room_data = '{"room_data":' + room_json

                try:
                    # _char_ref=self.character_ref[(resp['room_x'],resp['room_y'])]
                    char_json = json.dumps(self.character_ref[(resp['room_x'], resp['room_y'])].__dict__)
                    # Get the friend status of the character
                    fs = FriendStatus.getFriendStatus(self.character_ref[(0, 0)].race,
                                                      self.character_ref[(resp['room_x'], resp['room_y'])].race)
                    char_json += ',"friend_status": "' + fs + '"'
                    room_data += ',"char_data":' + char_json
                except KeyError:
                    _char_ref = {}
                except AttributeError:
                    pass

                try:
                    item_json="["
                    ix=0
                    item_lst = self.item_ref[(resp['room_x'], resp['room_y'])]
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
    server = socketserver.TCPServer((hostName, hostPort), MyServer)
    print("Web Server running on port: 8080")
    server.serve_forever()
except KeyboardInterrupt:
    print(" ^C entered, stopping web server....")
    server.socket.close()
