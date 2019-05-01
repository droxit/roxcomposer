# encoding: utf-8
#
# dummy monitoring class - for testing purposes only
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This program is free software: you can redistribute it and/or modify |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#


class DummyMonitor:
    def __init__(self, **kwargs):
        self.arguments = kwargs

    # monitors msg receiving acitvities
    def msg_received(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY RECEIVE \n')
        fh.close()

    # monitors msg dispatching acitvities
    def msg_dispatched(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY DISPATCH \n')
        fh.close()

    # monitors msgs which reached their final destination
    def msg_reached_final_destination(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY DESTINATION \n')
        fh.close()

    def msg_error(self):
        fh = open(self.arguments['filename'], 'a')
        fh.write('DUMMY ERROR \n')
        fh.close()


def not_a_class():
    pass
