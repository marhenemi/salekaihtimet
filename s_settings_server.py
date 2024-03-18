"""
Created: linre-90/11.3.2024
Updated: linre-90/18.03.2024
HOX Raspberry hotspot must have static ip...
HOX This is not very safe...
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from s_settings_parser import parse_data
from s_logger import s_dev_Log
from threading import Thread

SERVER = None

class ServerHandler(BaseHTTPRequestHandler):
    """Class for handling GET and post request, both close server."""

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode("utf-8")
        parse_succ = parse_data(post_body)

        if parse_succ:
            self.send_response(200)
        else:
            self.send_response(400)
        self.end_headers()


def server_close(callback)->None:
    """Close settings server and stop listening uploads. Callback is some function that is wanted run on close."""
    global SERVER
    if SERVER != None:
        SERVER.shutdown()
        SERVER.server_close()
        SERVER = None
    callback()


def server_start()->None:
    """Start server on hotspot that accepts post and get request. Returns true if user settings cannot be saved correctly."""
    global SERVER
    SERVER = HTTPServer(("", 8080), ServerHandler)
    SERVER.server_name = "curtain-123456"
    thread = Thread(target = SERVER.serve_forever)
    thread.start()


if __name__ == "__main__":
    ok = server_start()
    print("Set setup mode to false and continue normal execution")
