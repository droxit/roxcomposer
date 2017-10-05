from mosaic.base_service import BaseService

class LogTest(BaseService):
    def __init__(self, params):
        super().__init__(params)

    def logdebug(self, msg):
        self.logger.debug(msg)

    def loginfo(self, msg):
        self.logger.info(msg)

    def logwarn(self, msg):
        self.logger.warn(msg)

    def logerror(self, msg):
        self.logger.error(msg)

    def logcritical(self, msg):
        self.logger.critical(msg)

