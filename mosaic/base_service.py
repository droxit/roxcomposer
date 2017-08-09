#!/usr/bin/env python3.5

from mosaic.communication import mosaic_message


class BaseService:
    def __init__(self, params=None):
        self.params = params
        if params is None:
            self.params = {
                'ip': '127.0.0.1',
                'port': 5001
            }

        self.mosaic_message = mosaic_message.Message()
        self.mosaic_message.add_service(self.params['ip'], self.params['port'], self.params)
        self.payload = None

    def recv(self):
        return self.mosaic_message.recv(self.params['ip'], self.params['port'])

    def set_content(self, data):
        return mosaic_message.Message.set_content(self.mosaic_message, data)

    def get_content(self):
        return mosaic_message.Message.get_content(self.mosaic_message)

    def get_content_as_dict(self):
        return mosaic_message.Message.get_content_as_dict(self.mosaic_message)

    def send(self):
        return self.mosaic_message.send(self.params['ip'], self.params['port'])

    def get_mosaic_message(self):
        return mosaic_message.Message.get_mosaic_msg(self.mosaic_message)
