from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver
import time
import http.server
import ssl, sys
from os import curdir, sep
from RandomRooms import RandomRooms
from RoomFinderHtml import RoomFinderHtml

hostName = "localhost"
hostPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Serve all pages
    def do_GET(self):
        self._set_response()
        with open(self.path.strip("/"), 'r') as file:
            self.wfile.write(file.read().encode("UTF-8"))  # Read the file and send the contents



    def do_POST(self):
        print("do_POST")
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        val = post_data.decode('utf-8').split("=")[1]
        r = RandomRooms()
        r.create_rooms(val)
        f = RoomFinderHtml()
        f.find_rooms_html()



try:
    server = socketserver.TCPServer((hostName, hostPort), MyServer)
    print("Web Server running on port: 8080")
    server.serve_forever()
except KeyboardInterrupt:
    print(" ^C entered, stopping web server....")
    server.socket.close()
