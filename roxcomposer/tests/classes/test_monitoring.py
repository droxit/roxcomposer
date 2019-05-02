# encoding: utf-8
#
# monitor testing class - for testing purposes only
#
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
#


from roxcomposer.base_service import BaseService


class MonitorTest(BaseService):
    def __init__(self, params):
        super().__init__(params)

    def do_receive(self):
        self.monitoring.msg_received()

    def do_dispatch(self):
        self.monitoring.msg_dispatched()

    def do_destination(self):
        self.monitoring.msg_reached_final_destination()

    def do_error(self):
        self.monitoring.msg_error()
