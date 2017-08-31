#!/usr/bin/env python3.6

from mosaic import base_service


class FileWriter(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                'ip': '127.0.0.1',
                'port': 4001
            }
        super().__init__(params)

        self.recv_pipeline_msg()

    def on_message(self, msg):
        self.mosaic_message = msg
        print(self.mosaic_message.get_protobuf_msg_as_dict())
        self.write_file()

    def write_file(self):
        html_string = self.mosaic_message.get_content_as_dict()['body']
        f = open('index.html', 'w')
        f.write(html_string)
        f.close()


if __name__ == '__main__':
    math_service = FileWriter()
