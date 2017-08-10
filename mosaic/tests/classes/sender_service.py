#!/usr/bin/env python3.6

from mosaic import base_service


class SenderService(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                'ip': '127.0.0.1',
                'port': 5002
            }
        super().__init__(params)
        self.recv_pipeline_msg()

    def recv_pipeline_msg(self):
        self.recv(self.params['ip'], self.params['port'])

    def on_message(self, msg):
        self.mosaic_message = msg
        self.input('hallöle')

    def input(self, data):
        print(self.mosaic_message.pop_service())

        exit()
        self.mosaic_message.set_content(data)
        return self.send('127.0.0.1', 5001)

if __name__ == '__main__':
    service = SenderService()
