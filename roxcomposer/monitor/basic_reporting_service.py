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

import json
from roxcomposer import base_service
from roxcomposer.monitor import basic_monitoring

### expects JSON messages in the form {"function": "get_msg_status", "args": {...}}
class BasicReportingService(base_service.BaseService):
    def __init__(self, params):
        super().__init__(params)
        basic_monitoring.check_args(self.params, "filename")
        self.reporter = basic_monitoring.BasicReporting(filename=self.params['filename'])

    def on_message(self, msg, msg_id, parameters=None):
        try:
            m = json.loads(msg)
        except Exception as e:
            errormsg = "unable to parse message, expecting JSON. msg: {}".format(msg)
            self.logger.error(errormsg)
            disp_msg = {'error': errormsg}
            self.dispatch(json.dumps(disp_msg))
            return

        try:
            basic_monitoring.check_args(m, "function", "args")
        except Exception as e:
            errmsg = "missing argument: {}".format(e)
            disp_msg = {'error': errmsg}
            self.dispatch(json.dumps(disp_msg))
            return

        try:
            if m['function'] == "get_msg_status":
                reply = self.reporter.get_msg_status(**m['args'])
            elif m['function'] == "get_msg_history":
                reply = self.reporter.get_msg_history(**m['args'])
            else:
                reply = {"error": "unsupported function: {}".format(m['function'])}
        except Exception as e:
            reply = {"error": str(e)}

        self.dispatch(json.dumps(reply))


