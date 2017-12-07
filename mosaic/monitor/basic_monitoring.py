import time
import json
from mosaic import exceptions
from mosaic import base_service

def check_args(args, *required):
    for r in required:
        if r not in args:
            raise exceptions.ParameterMissing("{} is missing".format(r))

# This class yields a basic monitoring solution. It offers some functions to monitor service activities in a pipeline.
# The basic version of the monitoring writes every information to one file, which is configurable by defining a para-
# meter in the service parameters.
class BasicMonitoring:
    def __init__(self, **kwargs):
        self.arguments = kwargs
        if 'filename' not in kwargs:
            raise exceptions.ParameterMissing("BasicMonitoring needs a filename")
        fh = open(kwargs['filename'], 'a')
        fh.close()

    # monitors msg receiving acitvities
    def msg_received(self, **kwargs):
        check_args(kwargs, "service_name", "message_id")
        self.write_to_file("message_received", "processing", kwargs)

    # monitors msg dispatching acitvities
    def msg_dispatched(self, **kwargs):
        check_args(kwargs, "service_name", "message_id", "destination")
        self.write_to_file("message_dispatched", "in_transit", kwargs)

    # monitors msgs which reached their final destination
    def msg_reached_final_destination(self, **kwargs):
        check_args(kwargs, "service_name", "message_id")
        self.write_to_file("message_final_destination", "finalized", kwargs)

    # a helper function to write to a file
    def write_to_file(self, event, status, args):
        msg = { "event": event, "status": status, "time": time.time(), "args": args }
        fh = open(self.arguments['filename'], 'a')
        fh.write(repr(msg) + '\n')
        fh.close()


class BasicReporting:
    def __init__(self, **kwargs):
        self.arguments = kwargs
        if 'filename' not in kwargs:
            raise exceptions.ParameterMissing("BasicReporting needs a filename")
        fh = open(kwargs['filename'], 'a')
        fh.close()

    # ---- DO NOT USE IN PRODUCTION ---- can be memory intensive and is potentially unsafe because of eval
    def get_msg_history(self, **kwargs):
        check_args(kwargs, "message_id")
        with open(self.arguments['filename']) as f:
            lines = f.readlines()
            content = [x for x in map(eval, lines)]
        if len(content):
            return [x for x in filter(lambda x: x['args']['message_id'] == kwargs['message_id'], content)]
        else:
            return []

    # ---- DO NOT USE IN PRODUCTION ----
    def get_msg_status(self, **kwargs):
        check_args(kwargs, "message_id")
        history = [x for x in reversed(self.get_msg_history(message_id=kwargs['message_id']))]
        if len(history):
            return history[0]
        else:
            return {"status": "message not found"}

            
### expects JSON messages in the form {"function": "get_msg_status", "args": {...}}
class BasicReportingService(base_service.BaseService):
    def __init__(self, params):
        super().__init__(params)
        check_args(params, "filename")
        self.reporter = BasicReporting(filename=params['filename'])

    def on_message(self, msg):
        try:
            m = json.parse(msg)
        except Exception as e:
            errormsg = "unable to parse message, expecting JSON. msg: {}".format(msg)
            self.logger.error(errormsg)
            self.dispatch('{"error": "{}"}'.format(errormsg))

        check_args(m, "function", "args")
        try:
            if args['function'] == "get_msg_status":
                reply = self.reporter.get_msg_status(m['args'])
            elif args['function'] == "get_msg_history":
                reply = self.reporter.get_msg_history(m['args'])
            else:
                reply = {"error": "unsupported function: {}".format(args['function'])}
        except Exception as e:
            reply = {"error": str(e)}

        dispatch(json.dumps(reply))


        

