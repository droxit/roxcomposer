import logging
import time

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
        time.tzset()
        # tz = datetime.now(timezone.utc).astimezone().tzinfo
        kwargs['format'] = '[%(asctime)-15s.%(msecs)d' + time.strftime('%z') + '][%(created)s][%(levelname)s] service:' + servicename + ' - %(message)s'
        # kwargs['datefmt'] = '%Y-%m-%dT%H:%M:%S.%f%z'
        # %(msecs)
        kwargs['datefmt'] = '%Y-%m-%dT%H:%M:%S'
        if 'level' in kwargs:
            if kwargs['level'] in level_map:
                kwargs['level'] = level_map[kwargs['level']]
            else:
                del kwargs['level']

        logging.basicConfig(**kwargs)

    # log a message for information
    def info(self, msg):
        logging.info(msg)

    # log a message for debug purposes
    def debug(self, msg):
        logging.debug(msg)

    # log a message for warning purposes
    def warn(self, msg):
        logging.warning(msg)

    # log a message for error issues
    def error(self, msg):
        logging.error(msg)

    # log a message for fatal issues
    def critical(self, msg):
        logging.critical(msg)
