#!/usr/bin/env python3.6

import sys
import json
from mosaic import base_service


class FileWriter(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 4001,
                "name": "file_writer",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "DEBUG"
                }
            }
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg):
        self.msg = msg
        self.write_file()

    def write_file(self):
        html_string = self.msg
        f = open('index.html', 'w')
        f.write(html_string)
        f.close()
        return self.dispatch(html_string)


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    #Sservice = FileWriter(params)

    #use service_key
    serv_params = {'service_key':'file_writer.params'}
    service = FileWriter(serv_params)
