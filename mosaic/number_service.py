#!/usr/bin/env python3.5

from mosaic import base_service


class NumberService(base_service.BaseService):
    def __init__(self, args=None):
        if args is None:
            args = {'tolle': 'arguments'}
        base_service.BaseService.__init__(self, args)

        # self.init_communication()

    def addition(self, x, y):
        self.set_payload(x, y)
        msg = self.mosaic_message.SerializeToString()
        return self.speak_msg(msg)

if __name__ == '__main__':
    service = NumberService()
    print(service.addition(1, 2))
