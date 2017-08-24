#!/usr/bin/env python3.5

import unittest
from mosaic.communication import mosaic_message
from mosaic.communication import service_com_pb2
from google.protobuf import json_format
import urllib.parse


class TestMosaicMessage(unittest.TestCase):
    def setUp(self):
        self.dummy_protobuf_msg = service_com_pb2.MosaicMessage()
        self.pipeline = service_com_pb2.Pipeline()
        self.payload = service_com_pb2.Payload()

        service = self.pipeline.services.add()
        service.id = '127.0.0.1:6766'
        parameter = service.parameters.add()
        params = urllib.parse.urlencode({
            'ip': '127.0.0.1',
            'port': '6766',
            'name': 'service'
        })
        parameter.serviceParams = params
        self.payload.body = 'yeaaah test'
        self.dummy_protobuf_msg.pipeline.CopyFrom(self.pipeline)
        self.dummy_protobuf_msg.payload.CopyFrom(self.payload)

    def test_init(self):
        # test default message initiation
        default_message = mosaic_message.Message()

        self.assertDictEqual(default_message.get_protobuf_msg_as_dict(), {})

        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
        # test dummy protobuf msg initiation
        self.assertDictEqual(dummy_message.get_protobuf_msg_as_dict(),
                             json_format.MessageToDict(self.dummy_protobuf_msg))

    def test_add_service(self):
        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
        dummy_message.add_service('127.0.0.1', 7541)

        add_service = self.pipeline.services.add()
        add_service.id = '127.0.0.1' + ':' + str(7541)

        self.dummy_protobuf_msg.pipeline.CopyFrom(self.pipeline)

        # test adding service without parameters
        self.assertDictEqual(dummy_message.get_protobuf_msg_as_dict(),
                             json_format.MessageToDict(self.dummy_protobuf_msg))

        # params = {
        #   'ip': '127.0.0.1',
        #    'port': 7555,
        #    'name': 'another-fancy-service'
        # }
        # dummy_message.add_service('127.0.0.1', 7555, params)
        # print(dummy_message.get_protobuf_msg_as_dict())

        # add_another_service = self.pipeline.services.add()
        # add_another_service.id = '127.0.0.1' + ':' + str(7555)
        # parameter = add_another_service.parameters.add()
        # parameter.serviceParams = urllib.parse.urlencode(params)

        # self.dummy_protobuf_msg.pipeline.CopyFrom(self.pipeline)

        # print(dummy_message.get_protobuf_msg_as_dict())
        # print(json_format.MessageToDict(self.dummy_protobuf_msg))
        # test adding service with parameters
        # self.assertDictEqual(dummy_message.get_protobuf_msg_as_dict(),
        #                     json_format.MessageToDict(self.dummy_protobuf_msg))

    def test_get_content_as_dict(self):
        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)

        self.assertTrue(type(dummy_message.get_content_as_dict()) is dict)

        dummy_message.set_content('sollte true sein')
        self.assertEqual(dummy_message.get_content_as_dict()['body'], 'sollte true sein')

    def test_set_content(self):
        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
        dummy_message.set_content('angepasst')

        self.assertEqual(dummy_message.get_content_as_dict()['body'], 'angepasst')
        self.assertFalse(dummy_message.get_content_as_dict()['body'] is 'yeaaah test')

        # test empty string as input
        dummy_message.set_content('')
        self.assertNotIn('body', dummy_message.get_services_as_dict())

    def test_get_content(self):
        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)

        self.assertTrue(type(dummy_message.get_content()) is service_com_pb2.Payload)

        dummy_message.set_content('sollte true sein')
        self.assertEqual(dummy_message.get_content_as_dict()['body'], 'sollte true sein')

    def test_pop_service(self):
        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
        dummy_message.add_service('127.0.0.1', 1234)

        popped_service = dummy_message.pop_service()
        self.assertTrue(type(popped_service is dict))
        self.assertEqual(popped_service['id'], '127.0.0.1:6766')
        self.assertTrue(len(dummy_message.get_services_as_dict()) is 1)

        popped_service = dummy_message.pop_service()
        self.assertEqual(popped_service['id'], '127.0.0.1:1234')
        self.assertTrue(len(dummy_message.get_services_as_dict()) is 0)


if __name__ == '__main__':
    unittest.main()
