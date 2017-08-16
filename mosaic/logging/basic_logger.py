import logging

class BasicLogger():
    def __init__(self, servicename, **kwargs):
        kwargs['format'] = '%(levelname)s:' + servicename + ':(message)s'
        logging.basicConfig(**kwargs)

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg, msg)

    def warn(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def fatal(self, msg):
        logging.fatal(msg)

