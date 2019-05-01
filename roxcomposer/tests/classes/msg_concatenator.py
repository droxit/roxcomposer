# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

import sys
import json
import time
import http.server
from roxcomposer import base_service

class SimpleRHandler(http.server.BaseHTTPRequestHandler):
    def log_request(code, size):
        pass

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

    def on_message(self, msg, msg_id, parameters=None):
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
