from roxcomposer.base_service import BaseService

class LogTest(BaseService):
    def __init__(self, params):
        super().__init__(params)

    def logdebug(self, msg, **kwargs):
        self.logger.debug(msg, **kwargs)

    def loginfo(self, msg, **kwargs):
        self.logger.info(msg, **kwargs)

    def logwarn(self, msg, **kwargs):
        self.logger.warn(msg, **kwargs)

    def logerror(self, msg, **kwargs):
        self.logger.error(msg, **kwargs)

    def logcritical(self, msg, **kwargs):
        self.logger.critical(msg, **kwargs)

