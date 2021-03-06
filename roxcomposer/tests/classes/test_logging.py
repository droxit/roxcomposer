# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

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

