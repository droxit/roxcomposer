from roxcomposer.base_service import BaseService

class LogTest(BaseService):
    def __init__(self, params):
        super().__init__(params)

    def logdebug(self, msg, msg_id = None):
        self.logger.debug(msg, msg_id)

    def loginfo(self, msg, msg_id = None):
        self.logger.info(msg, msg_id)

    def logwarn(self, msg, msg_id = None):
        self.logger.warn(msg, msg_id)

    def logerror(self, msg, msg_id = None):
        self.logger.error(msg, msg_id)

    def logcritical(self, msg, msg_id = None):
        self.logger.critical(msg, msg_id)

