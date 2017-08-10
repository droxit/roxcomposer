#!/usr/bin/env python3.6

from mosaic import base_service


class SenderService(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                'ip': '127.0.0.1',
                'port': 5001
            }
        super().__init__(params)
        self.recv_pipeline_msg()

    def on_message(self, msg):
        self.mosaic_message = msg
        print(self.input('hallöle'))

    def input(self, payload):
        self.mosaic_message.set_content(payload)
        return self.send()

if __name__ == '__main__':
    service = SenderService()
