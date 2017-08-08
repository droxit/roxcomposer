#!/usr/bin/env python3.5

from mosaic import base_service


class NumberService(base_service.BaseService):
    def __init__(self, params=None):
        super().__init__(params)

        # self.init_communication()

    def addition(self, x, y):
        self.set_content({
            'firstNumber': x,
            'secondNumber': y
        })
        return self.send()

if __name__ == '__main__':
    service = NumberService()
    print(service.addition(1, 2))
