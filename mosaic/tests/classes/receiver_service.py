#!/usr/bin/env python3.6

from mosaic import base_service


class ReceiverService(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                'ip': '127.0.0.1',
                'port': 4001
            }
        super().__init__(params)

        self.recv_pipeline_msg()

    def on_message(self, msg):
        print('jo')
        print(msg.get_protobuf_msg_as_dict())

if __name__ == '__main__':
    math_service = ReceiverService()
