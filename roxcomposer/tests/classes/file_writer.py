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


class FileWriter(base_service.BaseService):
    def __init__(self, params=None):
        self.filepath = "index.html"
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
        if 'filepath' in params:
            self.filepath = params['filepath']

        self.msg = ''
        self.listen()

    def on_message(self, msg, msg_id, parameters=None):
        self.msg = msg
        self.logger.info("received: {} bytes".format(len(msg)))
        self.write_file()

    def write_file(self):
        html_string = self.msg
        with open(self.filepath, 'w+') as f:
            f.write(html_string)
            f.close()

        return self.dispatch(html_string)


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    service = FileWriter(params)
