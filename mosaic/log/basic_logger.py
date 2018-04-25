import logging
import os
import time

from mosaic import exceptions

level_map = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

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
        time.tzset()
        # tz = datetime.now(timezone.utc).astimezone().tzinfo
        fmt = None
        if 'format' in kwargs:
            fmt = kwargs['format']
        else:
            fmt = '[%(asctime)-15s.%(msecs)d' + time.strftime('%z') + '][%(created)s][%(levelname)s] service:%(servicename)s %(message_id)s - %(message)s'
        # kwargs['datefmt'] = '%Y-%m-%dT%H:%M:%S.%f%z'
        # %(msecs)
        dtfmt = None
        if 'datefmt' in kwargs:
            dtfmt = kwargs['datefmt']
        else:
            dtfmt = '%Y-%m-%dT%H:%M:%S'
        if 'level' in kwargs:
            if kwargs['level'] in level_map:
                self.logger.setLevel(level_map[kwargs['level']])
            else:
                raise exceptions.ConfigError("can't set log level: {} is invalid".format(kwargs['level']))

        formatter = logging.Formatter(fmt, dtfmt)

        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    # log a message for information
    def info(self, msg, msg_id = None):
        extra = { 'servicename': self.servicename }
        if msg_id is not None:
            extra['message_id'] = 'message_id:{}'.format(msg_id)
        else:
            extra['message_id'] = ''

        self.logger.info(msg, extra=extra)

    # log a message for debug purposes
    def debug(self, msg, msg_id = None):
        extra = { 'servicename': self.servicename }
        if msg_id is not None:
            extra['message_id'] = 'message_id:{}'.format(msg_id)
        else:
            extra['message_id'] = ''
        self.logger.debug(msg, extra=extra)

    # log a message for warning purposes
    def warn(self, msg, msg_id = None):
        extra = { 'servicename': self.servicename }
        if msg_id is not None:
            extra['message_id'] = 'message_id:{}'.format(msg_id)
        else:
            extra['message_id'] = ''
        self.logger.warning(msg, extra=extra)

    # log a message for error issues
    def error(self, msg, msg_id = None):
        extra = { 'servicename': self.servicename }
        if msg_id is not None:
            extra['message_id'] = 'message_id:{}'.format(msg_id)
        else:
            extra['message_id'] = ''
        self.logger.error(msg, extra=extra)

    # log a message for fatal issues
    def critical(self, msg, msg_id = None):
        extra = { 'servicename': self.servicename }
        if msg_id is not None:
            extra['message_id'] = 'message_id:{}'.format(msg_id)
        else:
            extra['message_id'] = ''
        self.logger.critical(msg, extra=extra)

