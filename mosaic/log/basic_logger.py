import logging
from datetime import datetime
from datetime import timezone


# This class provided a standard logging feature. It takes arguments like the {'path': './service.log'} to specify
# the logging configuration. If the specified logfile already exists logs will get appended to the file.
class BasicLogger:
    def __init__(self, servicename, **kwargs):
        tz = datetime.now(timezone.utc).astimezone().tzinfo
        timestamp_iso = datetime.now(tz=tz)
        now = timestamp_iso.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        kwargs['format'] = '[' + now + '][%(created)s][%(levelname)s] service:' + servicename + ' - %(message)s'
        # kwargs['datefmt'] = '%Y-%m-%dT%H:%M:%S%z'
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
