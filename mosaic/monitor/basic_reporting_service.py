import json
from mosaic import base_service
from mosaic.monitor import basic_monitoring

### expects JSON messages in the form {"function": "get_msg_status", "args": {...}}
class BasicReportingService(base_service.BaseService):
    def __init__(self, params):
        super().__init__(params)
        basic_monitoring.check_args(self.params, "filename")
        self.reporter = basic_monitoring.BasicReporting(filename=self.params['filename'])

    def on_message(self, msg):
        try:
            m = json.loads(msg)
        except Exception as e:
            errormsg = "unable to parse message, expecting JSON. msg: {}".format(msg)
            self.logger.error(errormsg)
            self.dispatch('{"error": "{}"}'.format(errormsg))

        basic_monitoring.check_args(m, "function", "args")
        try:
            if args['function'] == "get_msg_status":
                reply = self.reporter.get_msg_status(m['args'])
            elif args['function'] == "get_msg_history":
                reply = self.reporter.get_msg_history(m['args'])
            else:
                reply = {"error": "unsupported function: {}".format(args['function'])}
        except Exception as e:
            reply = {"error": str(e)}

        self.dispatch(json.dumps(reply))


