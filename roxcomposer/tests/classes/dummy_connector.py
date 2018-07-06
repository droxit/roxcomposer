# encoding: utf-8
#
# dummy connector class - for testing purposes only
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
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
