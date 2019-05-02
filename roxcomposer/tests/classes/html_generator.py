# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

import sys
import json
from roxcomposer import base_service


class HtmlGenerator(base_service.BaseService):
    def __init__(self, params=None):
        if params is None:
            params = {
                "ip": "127.0.0.1",
                "port": 5001,
                "name": "html_generator",
                "logging": {
                    "filename": "pipeline.log",
                    "level": "DEBUG"
                }
            }
        super().__init__(params)

        self.msg = ''
        self.listen()

    def on_message(self, msg, msg_id, parameters=None):
        self.msg = msg
        self.logger.info("received: {} bytes".format(len(msg)))
        self.to_html()

    def to_html(self):
        received_text = self.msg
        html_string = """
            <!doctype html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <title>droxIT - roxcomposer</title>
                        <style>
                            body {margin: 3em;}
                            header {background: #eee; padding: 1em;}
                            article {padding: 2em;}
                        </style>
                    <body>
                        <header><h1>ROXCOMPOSER - DEMO</h1></header>
                        <article>
                            """ + received_text + """
                        </article>
                    </body>
                </html>
        """

        return self.dispatch(html_string)


if __name__ == '__main__':
    params = None
    if len(sys.argv) > 1:
        params = json.loads(sys.argv[1])

    #service = HtmlGenerator('html_generator.params')

    #use service_key
#    serv_params = {'service_key':'html_generator.params'}
#    service = HtmlGenerator(serv_params)
    service = HtmlGenerator(params)
