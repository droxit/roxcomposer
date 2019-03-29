import logging
import os
import time
import json
from functools import partial
from datetime import datetime, timezone

from roxcomposer import exceptions

level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class JSONFormatter(logging.Formatter):
    def __init__(self):
        pass

    @staticmethod
    def get_attr(record, field):
        return record.__dict__.get(field)

    def format(self, record):
        r = record.__dict__
        out = dict()
        out['level'] = r['levelname']
        out['msg'] = r['msg']
        out['time'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        for k in r['extra']:
            out[k] = r['extra'][k]

        return json.dumps(out)
        #return json.dumps(r)


# This class provided a standard logging feature. It takes arguments like the {'path': './service.log'} to specify
# the logging configuration. If the specified logfile already exists logs will get appended to the file.
class BasicLogger:
    def __init__(self, servicename, **kwargs):
        self.servicename = servicename
        self.logger = logging.getLogger(servicename)
        handler = None
        if 'logpath' in kwargs:
            try:
                logname = kwargs['logpath']
                if os.path.isdir(kwargs['logpath']):
                    logname += servicename + '.log'
                handler = logging.FileHandler(logname, encoding='utf8')

            except Exception as e:
                raise exceptions.ConfigError(
                    'unable to set up file logging: {} - {}'.format(kwargs['logpath'], e)) from e
        else:
            handler = logging.StreamHandler()
        formatter = JSONFormatter()
        handler.setFormatter(formatter)
        
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        if 'level' in kwargs:
            if kwargs['level'] in level_map:
                self.logger.setLevel(level_map[kwargs['level']])
            else:
                raise exceptions.ConfigError("can't set log level: {} is invalid".format(kwargs['level']))

        levels = ['debug', 'info', 'warn', 'error', 'critical']

        for l in levels:
            setattr(self, l, partial(self.do_logging, l))


    def do_logging(self, level, msg, **extra):
        extra['service'] = self.servicename
        getattr(self.logger, level)(msg, extra={'extra': extra})

#
#    # log a message for information
#    def info(self, msg, msg_id = None):
#        extra = { 'servicename': self.servicename }
#        if msg_id is not None:
#            extra['message_id'] = msg_id
#        else:
#            extra['message_id'] = ''
#
#        self.logger.info(msg, extra=extra)