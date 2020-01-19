from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import socketserver
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
        # print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        val = post_data.decode('utf-8').split("=")[1]
        rr = RandomRooms()
        rr.create_rooms(val)
        rf = RoomFinderHtml()
        rf.find_rooms_html()
        # Calls  the GET to rerender the page
        self.do_GET()



try:
    server = socketserver.TCPServer((hostName, hostPort), MyServer)
    print("Web Server running on port: 8080")
    server.serve_forever()
except KeyboardInterrupt:
    print(" ^C entered, stopping web server....")
    server.socket.close()
