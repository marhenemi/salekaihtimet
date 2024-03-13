"""
Created: linre-90/11.3.2024
Updated: 
HOX Raspberry hotspot must have static ip...
HOX This is not very safe...
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from s_settings_parser import parse_data


WAIT_DATA = True
PARSE_ERR = False


class ServerHandler(BaseHTTPRequestHandler):
    """Class for handling GET and post request, both close server."""
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Closing settings server.", "utf-8"))
        global WAIT_DATA
        WAIT_DATA = False
        global PARSE_ERR
        PARSE_ERR = True

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len).decode("utf-8")
        parse_succ = parse_data(post_body)
        global WAIT_DATA
        WAIT_DATA = False

        if parse_succ:
            self.send_response(200)
        else:
            global PARSE_ERR
            PARSE_ERR = True
            self.send_response(400)
        self.end_headers()


def wait_config_file()->bool:
    """Start server on hotspot that accepts post and get request. Returns true if user settings cannot be saved correctly."""
    try:
        server = HTTPServer(("", 8080), ServerHandler)
        server.server_name = "curtain-123456"
        while WAIT_DATA:
            server.handle_request()
        server.server_close()
        return PARSE_ERR
    except:
        return False


if __name__ == "__main__":
    ok = wait_config_file()
    print("Set setup mode to false and continue normal execution")
