#!/usr/bin/env python3.5

from mosaic import base_service


class MathService(base_service.BaseService):
    def __init__(self):
        base_service.BaseService.__init__(self)
        # print(self.mosaic_message)

    def addition(self):
        self.hear_msg()
        payload = self.get_payload()
        return payload['firstNumber'] + payload['secondNumber']

if __name__ == '__main__':
    math_service = MathService()
    print(math_service.addition())
