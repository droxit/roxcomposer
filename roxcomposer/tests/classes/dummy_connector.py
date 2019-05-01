# encoding: utf-8
#
# dummy connector class - for testing purposes only
#
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
#

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

HOST = 'localhost'
PORT = 7475


class SingleRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        data = json.dumps({"json": "test"}).encode()
        if self.path == '/pipelines':
            data = json.dumps({"pipe":{"services":["s1","s2"],"active":True}}).encode()

        self.wfile.write(data)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        request_headers = self.headers
        content_length = request_headers.get("Content-Length")
        length = int(content_length) if content_length else 0

        self._set_headers()
        data = self.rfile.read(length)
        if self.path == '/log_observer':
            d = json.loads(data)
            data = json.dumps({ 'sessionid': "123", "ok": d["services"] }).encode()

        self.wfile.write(data)

    def do_PUT(self):
        request_headers = self.headers
        content_length = request_headers.get("Content-Length")
        length = int(content_length) if content_length else 0

        self._set_headers()
        data = self.rfile.read(length)
        if self.path == '/log_observer':
            d = json.loads(data)
            data = json.dumps({ 'sessionid': "123", "ok": d["services"] }).encode()

        self.wfile.write(data)

    def do_DELETE(self):
        request_headers = self.headers
        content_length = request_headers.get("Content-Length")
        length = int(content_length) if content_length else 0

        self._set_headers()
        data = self.rfile.read(length)
        self.wfile.write(data)

    def log_message(self, format, *args):
        pass


class DummyConnector(HTTPServer, threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        HTTPServer.__init__(self, (HOST, PORT), SingleRequestHandler)

    def run(self):
        self.serve_forever()

    def stop(self):
        self.shutdown()
        self.server_close()
