import logging
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
        self.logger = logging.getLogger(servicename)
        handler = None
        if 'filename' in kwargs:
            try:
                handler = logging.FileHandler(kwargs['filename'], encoding='utf8')
            except Exception as e:
                raise exceptions.ConfigError('unable to set up file logging: {} - {}'.format(kwargs['filename'],e)) from e
        else:
            handler = logging.StreamHandler()
        time.tzset()
        # tz = datetime.now(timezone.utc).astimezone().tzinfo
        fmt = None
        if 'format' in kwargs:
            fmt = kwargs['format']
        else:
            fmt = '[%(asctime)-15s.%(msecs)d' + time.strftime('%z') + '][%(created)s][%(levelname)s] service:' + servicename + ' - %(message)s'
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
    def info(self, msg):
        self.logger.info(msg)

    # log a message for debug purposes
    def debug(self, msg):
        self.logger.debug(msg)

    # log a message for warning purposes
    def warn(self, msg):
        self.logger.warning(msg)

    # log a message for error issues
    def error(self, msg):
        self.logger.error(msg)

    # log a message for fatal issues
    def critical(self, msg):
        self.logger.critical(msg)

