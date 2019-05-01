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


import json
import requests

roxconnector = 'localhost:7475'
service_file_dir = 'services'
logobs_session = None
logobs_session_timeout = 3600

f = {
  "classpath": "roxcomposer.tests.classes.delay_service.DelayService",
  "params": {
    "ip": "127.0.0.1",
    "port": 4007,
    "name": "delay_service"
  }
}


headers = {'Content-Type': 'application/json'}
r = requests.post('http://{}/start_service'.format(roxconnector), json=f, headers=headers)


d = {'name': "pipe1", 'services': [{'service': 'delay_service', 'params':{'param1':'someparam'}}]}
r = requests.post('http://{}/set_pipeline'.format(roxconnector), data=json.dumps(d), headers=headers)
print(r.text)