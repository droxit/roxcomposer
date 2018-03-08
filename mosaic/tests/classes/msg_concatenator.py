import sys
import json
import time
import http.server
from mosaic import base_service

class SimpleRHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        self.wfile.write(self.server.cumulated_message.encode())

class MyHTTPServer(http.server.HTTPServer):
    def __init__(self, address, rhandler):
        super().__init__(address, rhandler)
        self.cumulated_message = ''

    def set_msg(self, msg):
        self.cumulated_message = msg


class MsgConcatenator(base_service.BaseService):
    def __init__(self, params=None):
        super().__init__(params)

        self.msgs = ''
        self.http = MyHTTPServer(params['http_address'], SimpleRHandler)

    def on_message(self, msg):
        self.msgs += msg
        self.http.set_msg(self.msgs)
        self.dispatch(msg)

if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    service = MsgConcatenator(params)
    service.listen_thread()
    service.http.serve_forever()
