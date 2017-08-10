#!/usr/bin/env python3.5

from mosaic import base_service


class ReceiverService(base_service.BaseService):
    def __init__(self, params=None):
        super().__init__(params)

    def output(self):
        recv = self.recv(self.params['ip'], self.params['port'])
        return recv.get_content_as_dict()

    @staticmethod
    def on_message(msg):
        print(msg.get_protobuf_msg_as_dict())

if __name__ == '__main__':
    math_service = ReceiverService()
    print(math_service.output())
