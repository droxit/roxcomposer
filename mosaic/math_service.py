#!/usr/bin/env python3.5

from mosaic import base_service


class MathService(base_service.BaseService):
    def __init__(self, params=None):
        super().__init__(params)
        # print(self.mosaic_message)

    def addition(self):
        recv = self.recv()
        content = recv.get_content_as_dict()
        return content['firstNumber'] + content['secondNumber']

if __name__ == '__main__':
    math_service = MathService()
    print(math_service.addition())
