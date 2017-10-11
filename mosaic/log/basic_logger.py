import logging


# This class provided a standard logging feature. It takes arguments like the {'path': './service.log'} to specify
# the logging configuration. If the specified logfile already exists logs will get appended to the file.
class BasicLogger:
    def __init__(self, servicename, **kwargs):
        kwargs['format'] = '[%(asctime)-15s][%(created)s][%(levelname)s] service:' + servicename + ' - %(message)s'
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
