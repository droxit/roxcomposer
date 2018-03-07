import unittest
from mosaic.communication import mosaic_message
from mosaic import exceptions
import uuid
import urllib.parse


class TestMosaicMessage(unittest.TestCase):
    def setUp(self):
        self.msg = mosaic_message.Message()
        self.services = [ mosaic_message.Service('127.0.0.1', 5000), mosaic_message.Service('::1', 5001, ["blorp", "blub"]) ]
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
        msg2 = mosaic_message.Message.deserialize_from_protobuf(protomsg)
        d1 = self.msg.get_content_as_dict()
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

    def test_json_serialization(self):
        d1 = self.msg.get_content_as_dict()
        jsonmsg = self.msg.serialize_to_json()
        msg2 = mosaic_message.Message.deserialize_from_json(jsonmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

    def test_wire_serialization(self):
        d1 = self.msg.get_content_as_dict()
        binmsg = self.msg.serialize()
        msg2 = mosaic_message.Message.deserialize(binmsg)
        d2 = msg2.get_content_as_dict()
        self.assertEqual(d1, d2)

if __name__ == '__main__':
    unittest.main()
