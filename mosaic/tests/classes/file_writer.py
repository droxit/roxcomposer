#!/usr/bin/env python3.6

from mosaic import base_service


class FileWriter(base_service.BaseService):
    def __init__(self, params=None):
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg):
        self.msg = msg
        self.logger.info('msg received: ' + msg)
        self.write_file()

    def write_file(self):
        html_string = self.msg
        f = open('index.html', 'w')
        f.write(html_string)
        f.close()


if __name__ == '__main__':
    fw = FileWriter()
