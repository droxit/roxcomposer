# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

import sys
import json
from roxcomposer import base_service


class ImageAdder(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 6001,
                "name": "image_adder",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "DEBUG"
                }
            }
        super().__init__(params)

        self.image = None
        if 'image' in params:
            self.image = params['image']
        self.msg = ''
        self.listen()

    # def on_message(self, msg):
    #     self.msg = msg
    #     self.to_html()

    def on_message_ext(self, extended_msg):
        # access the message's payload
        self.msg = extended_msg.payload
        self.logger.info("received: {} bytes".format(len(extended_msg.payload)))
        self.to_html()

    def to_html(self):
        received_text = self.msg
        html_string = ''
        if self.image is not None:
            html_string = "\n<img src=\"" + self.image + "\">"

        return self.dispatch(received_text + '<br/>' + html_string)


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    # service = ImageAdder(params)
    # use service_key
    serv_params = {'service_key': 'image_adder.params'}
    service = ImageAdder(serv_params)
