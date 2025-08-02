from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pi import *
import urllib.request
import os
import random

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case '/':
                now = datetime.utcnow()
                response_string = now.strftime("The time is %-I:%M %p, UTC.")
                self.respond_with(200, response_string)
            case '/healthz':
                self.respond_with(200, "Healthy")
            case '/readyz':
                dependencies_connected = True
                
                if dependencies_connected:
                    self.respond_with(200, "Ready")
                else:
                    self.respond_with(503, "Not Ready")
            case '/pi':
                pi = leibniz_pi(1000000)
                self.respond_with(200, str(pi))
            case '/avatar':
                url = os.environ['AVATAR_ENDPOINT'] + "/" + str(random.randint(0, 100))
                try:
                    with urllib.request.urlopen(url) as f:
                        data = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'image/png')
                        self.end_headers()
                        self.wfile.write(data)
                except urllib.error.URLError as e:
                    self.respond_with(500, e.reason)
            case _:
                self.respond_with(404, "Not Found")
        

    def respond_with(self, status_code: int, content: str) -> None:
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

def startServer():
    try:
        server = ThreadingHTTPServer(('', 80), RequestHandler)
        print("Listening on " + ":".join(map(str, server.server_address)))
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    startServer()