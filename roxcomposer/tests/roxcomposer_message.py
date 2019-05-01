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

import unittest
from roxcomposer.communication import roxcomposer_message
from roxcomposer import exceptions
import uuid
import urllib.parse


class TestROXcomposerMessage(unittest.TestCase):
    def setUp(self):
        self.msg = roxcomposer_message.Message()
        self.services = [ roxcomposer_message.Service('127.0.0.1', 5000), roxcomposer_message.Service('::1', 5001, ["blorp", "blub"]) ]
        self.payload = 'a;sdklfja0eifjq'

        self.msg.set_payload(self.payload)
        for s in self.services:
            self.msg.add_service(s)


    def test_params(self):
        self.assertEqual(self.msg.get_payload(), self.payload)
        self.assertListEqual(self.msg.pipeline, self.services)
        d = {
                'id': self.msg.id,
                'pipeline': self.services,
                'payload': self.payload
                }
        self.assertDictEqual(self.msg.get_content_as_dict(), d)
        self.assertEqual(self.msg.pop_service(), self.services[0])
        self.assertListEqual(self.msg.pipeline, [self.services[1]])


    def test_protobuf_serialization(self):
        protomsg = self.msg.serialize_to_protobuf()
        msg2 = roxcomposer_message.Message.deserialize_from_protobuf(protomsg)
        d1 = self.msg.get_content_as_dict()
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

    def test_json_serialization(self):
        d1 = self.msg.get_content_as_dict()
        jsonmsg = self.msg.serialize_to_json()
        msg2 = roxcomposer_message.Message.deserialize_from_json(jsonmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

    def test_wire_serialization(self):
        d1 = self.msg.get_content_as_dict()
        binmsg = self.msg.serialize()
        msg2 = roxcomposer_message.Message.deserialize(binmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

if __name__ == '__main__':
    unittest.main()
