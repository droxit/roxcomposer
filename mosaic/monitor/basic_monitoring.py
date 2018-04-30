# encoding: utf-8
#
# This class yields a basic monitoring solution. It offers some functions to monitor service activities in a pipeline.
# The basic version of the monitoring writes every information to one file, which is configurable by defining a para-
# meter in the service parameters.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import time
import json
from mosaic import exceptions


class BasicMonitoring:
    def __init__(self, **kwargs):
        self.arguments = kwargs
        if 'filename' not in kwargs:
            raise exceptions.ParameterMissing("BasicMonitoring needs a filename")
        try:
            fh = open(kwargs['filename'], 'a')
            fh.close()
        except Exception as e:
            ce = exceptions.ConfigError('unable to open monitoring file {} : {}'.format(kwargs['filename'], e))
            raise ce from e

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

    def msg_error(self, **kwargs):
        check_args(kwargs, "service_name", "message_id", "description")
        self.write_to_file("message_error", "error", kwargs)

    def custom_metric(self, **kwargs):
        check_args(kwargs, "service_name", "metric_name", "metric_dictionary")
        self.write_to_file("custom_metric", "information", kwargs)

    # a helper function to write to a file
    def write_to_file(self, event, status, args):
        msg = { "event": event, "status": status, "time": time.time(), "args": args }
        try:
            fh = open(self.arguments['filename'], 'a')
            fh.write(json.dumps(msg) + '\n')
            fh.close()
        except Exception as e:
            re = RuntimeError('unable to commit monitoring message to file: {}'.format(e))
            raise re from e

def check_args(args, *required):
    for r in required:
        if r not in args:
            raise exceptions.ParameterMissing("{} is missing".format(r))


class BasicReporting:
    def __init__(self, **kwargs):
        self.arguments = kwargs
        if 'filename' not in kwargs:
            raise exceptions.ParameterMissing("BasicReporting needs a filename")
        try:
            fh = open(kwargs['filename'], 'a')
            fh.close()
        except Exception as e:
            ce = exceptions.ConfigError('unable to open monitoring file {} : {}'.format(kwargs['filename'], e))
            raise ce from e
            

    # ---- DO NOT USE IN PRODUCTION ---- can be memory intensive and is potentially unsafe because of eval
    def get_msg_history(self, **kwargs):
        check_args(kwargs, "message_id")
        lines = []
        try:
            f = open(self.arguments['filename'])
            lines = f.readlines()
            f.close()
        except Exception as e:
            re = RuntimeError('unable to open monitoring file {} - {}'.format(self.arguments['filename'], e))
            raise re from e

        content = [x for x in map(eval, lines)]
        if len(content):
            def f(x):
                if "message_id" in x['args']:
                    return x['args']['message_id']
                else:
                    return None

            return [x for x in filter(lambda x: f(x) == kwargs['message_id'], content)]
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
