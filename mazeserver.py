import json
import dill
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver
from RandomRooms import RandomRooms
from RoomFinderHtml import RoomFinderHtml
from RoomMatrix import RoomMatrix

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
        # print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n" %
        #       (str(self.path), str(self.headers), post_data.decode('utf-8')))
        print ("Body: %s"%post_data.decode('utf-8'))
        self._set_response()
        val = "-1"
        try:
            val = post_data.decode('utf-8').split("=")[1]
        except:
            pass
        if val != "-1":
            rr = RandomRooms()
            rr.create_rooms(val)
            rf = RoomFinderHtml()
            rf.find_rooms_html()
            # Calls  the GET to rerender the page
            self.do_GET()
        else:
            resp = json.loads(post_data.decode('utf-8'))
            # {"room_x": 0, "room_y": 0, "room_name": "Start"}

            print("You are in "+self.room_ref[(resp['room_x'],resp['room_y'])].name)
            # COnvert the response into a JSON object
            _room_ref=self.room_ref[(resp['room_x'],resp['room_y'])]
            room_name = _room_ref.name
            exit_N = str(_room_ref.N)
            exit_E = str(_room_ref.E)
            exit_S = str(_room_ref.S)
            exit_W = str(_room_ref.W)
            name = _room_ref.name

            room_data = '{"room_data":{"room_name":"' + room_name + '","exit_N":' + exit_N + ', "exit_E":' + exit_E + ', "exit_S":' + exit_S + ', "exit_W":' + exit_W + '}'
            try:
                _char_ref=self.character_ref[(resp['room_x'],resp['room_y'])]
                room_data += ',"char_data":{"race":"' + str(_char_ref._char_race) + '","class":"' + str(_char_ref._char_class) + '","name":"'+str(_char_ref._name)+'"}'
            except KeyError:
                _char_ref={}
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
