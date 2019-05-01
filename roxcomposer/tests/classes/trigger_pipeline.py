# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
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

from roxcomposer.communication import roxcomposer_message
import socket

if __name__ == '__main__':
    roxcomposer_msg = roxcomposer_message.Message()
    roxcomposer_msg.add_service('127.0.0.1', 6001)
    roxcomposer_msg.add_service('127.0.0.1', 5001)
    roxcomposer_msg.add_service('127.0.0.1', 4001)
    roxcomposer_msg.add_service('127.0.0.1', 7001)

    address_tuple = ('127.0.0.1', 6001)
    roxcomposer_msg.set_content('Hallöle. Ich bin ein schöner Text. Wenn alles glatt geht, dürfte '
                           'ich am Ende als wunderschöne HTML Datei erscheinen. Ich erweitere den Text auch einfach.'
                           'obwohl die services noch laufen, haha! Und ein Bild: ')

    roxcomposer_msg = roxcomposer_message.Utils.serialize(roxcomposer_msg.get_protobuf_msg())
    wiremsg = struct.pack('>I', len(roxcomposer_msg)) + roxcomposer_msg
    connection = socket.create_connection(address_tuple)
    connection.send(wiremsg)

    # resp = connection.recv(1024)
    connection.close()
