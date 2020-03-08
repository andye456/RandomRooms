import json
import random

import dill
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver

import jsonpickle as jsonpickle

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
hostName = "localhost"
hostPort = 8080


class MyServer(BaseHTTPRequestHandler):
    print("opening rooms.bin to read matrix")
    f = open("rooms.bin", "rb")
    room_ref = dill.load(f)
    f.close()

    f = open("characters.bin", "rb")
    character_ref = dill.load(f)
    f.close()

    # This bit adds you as a Human, with random class and gives you a few basic items to start
    classes=['Assassin','Druid','Illusionist','Monk','Paladin','Ranger']
    char_race="Human"
    char_class=random.choice(classes)
    items=[Items.Sack,Items.Candle]
    weapon=Weapons.Cane
    abilities=CharacterAbilities(char_race, char_class)
    my_char = Character("Pweter", 25, 200, char_race, char_class, items, 0, 0,weapon, abilities.getAbilities())
    character_ref[(0, 0)] = my_char

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
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        print ("Body: %s"%post_data.decode('utf-8'))
        self._set_response()
        val = "-1"
        try:
            val = post_data.decode('utf-8').split("=")[1]
        except:
            pass
        # Generates new room from a request from the web page # not implemented
        if val != "-1":
            rr = RandomRooms()
            rr.create_rooms(val)
            rf = RoomGenHtml()
            rf.find_rooms_html()
            # Calls  the GET to rerender the page
            self.do_GET()
        else:
            resp = json.loads(post_data.decode('utf-8'))
            cmd = ""
            try:
                cmd=resp["command"]
            except KeyError:
                pass
            if cmd == "I": # Show inventory
                char_json = json.dumps(self.character_ref[(0, 0)].__dict__)
                char_data = '{"char_data":'+char_json+'}'
                self.wfile.write(char_data.encode("UTF-8"))
            elif cmd == "F": # Friend status
                char_json = json.dumps(self.character_ref[(resp['room_x'],resp['room_y'])].__dict__) # Gets the stats for the character that is in the room
                char_data = '{"char_data":' + char_json + '}' # make it intom a JSON object
                self.wfile.write(char_data.encode("UTF-8")) # return it to the front end.
            elif cmd == "A": # attack
                them = self.character_ref[(resp['room_x'], resp['room_y'])]
                their_dmg = random.randint(them.weapon['min_damage_large_opponent'],them.weapon['max_damage_large_opponent'])
                your_dmg = random.randint(self.character_ref[(0, 0)].weapon['min_damage_small_opponent'],self.character_ref[(0, 0)].weapon['max_damage_small_opponent'])

                if your_dmg > their_dmg:
                    char_data = '{"char_data":"win"}'
                    # ToDo:  Remove the character from the game - change this to have the character die eventually when their life gets down to 0 then you can loot them
                    self.character_ref.pop((resp['room_x'], resp['room_y']))
                else:
                    char_data = '{"char_data":"lose"}'
                self.wfile.write(char_data.encode("UTF-8"))  # return it to the front end.

            elif cmd == "T":
                pass
            else:
                # {"room_x": 0, "room_y": 0, "room_name": "Start"}

                print("You are in "+self.room_ref[(resp['room_x'],resp['room_y'])].room_name)
                # Convert the response into a JSON object
                room_json = json.dumps(self.room_ref[(resp['room_x'],resp['room_y'])].__dict__)

                room_data = '{"room_data":'+room_json

                try:
                    # _char_ref=self.character_ref[(resp['room_x'],resp['room_y'])]
                    char_json = json.dumps(self.character_ref[(resp['room_x'], resp['room_y'])].__dict__)
                    # Get the friend status of the character
                    fs = FriendStatus.getFriendStatus(self.character_ref[(0, 0)].race,self.character_ref[(resp['room_x'], resp['room_y'])].race)
                    char_json += ',"friend_status": "'+fs+'"'
                    room_data += ',"char_data":'+char_json
                except KeyError:
                    _char_ref={}
                except AttributeError:
                    pass

                room_data+='}'

                # TODO: Establish your class, using the FriendStatus lookup decide whether the character in the room is an enemy

                # Returns the JSON to the html page.
                self.wfile.write(room_data.encode("UTF-8"))





try:
    server = socketserver.TCPServer((hostName, hostPort), MyServer)
    print("Web Server running on port: 8080")
    server.serve_forever()
except KeyboardInterrupt:
    print(" ^C entered, stopping web server....")
    server.socket.close()
