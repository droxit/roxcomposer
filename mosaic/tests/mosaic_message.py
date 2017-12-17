import unittest
from mosaic.communication import mosaic_message
from mosaic import exceptions
import uuid
import urllib.parse


class TestMosaicMessage(unittest.TestCase):
    def setUp(self):
        self.msg = mosaic_message.Message()
        self.services = [ mosaic_message.Service('127.0.0.1', 5000), mosaic_message.Service('::1', 5001) ]
        self.payload = 'a;sdklfja0eifjq'

        self.msg.set_payload(self.payload)
        for s in self.services:
            self.msg.add_service(s)


    def test_params(self):
        self.assertEqual(self.msg.get_payload(), self.payload)
        self.assertListEqual(self.msg.pipeline, self.services)
        d = {
                'id': self.msg.id,
                'pipline': self.services,
                'payload': self.payload
                }
        self.assertDictEqual(self.msg.get_content_as_dict(), d)
        self.assertEqual(self.msg.pop_service(), self.services[0])
        self.assertListEqual(self.msg.pipeline, [self.services[1]])


#    def test_add_service(self):
#        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
#        dummy_message.add_service('127.0.0.1', 7541)
#
#        add_service = self.pipeline.services.add()
#        add_service.id = '127.0.0.1' + ':' + str(7541)
#
#        self.dummy_protobuf_msg.pipeline.CopyFrom(self.pipeline)
#
#        # test adding service without parameters
#        self.assertDictEqual(dummy_message.get_protobuf_msg_as_dict(),
#                             json_format.MessageToDict(self.dummy_protobuf_msg))
#
#        # params = {
#        #   'ip': '127.0.0.1',
#        #    'port': 7555,
#        #    'name': 'another-fancy-service'
#        # }
#        # dummy_message.add_service('127.0.0.1', 7555, params)
#        # print(dummy_message.get_protobuf_msg_as_dict())
#
#        # add_another_service = self.pipeline.services.add()
#        # add_another_service.id = '127.0.0.1' + ':' + str(7555)
#        # parameter = add_another_service.parameters.add()
#        # parameter.serviceParams = urllib.parse.urlencode(params)
#
#        # self.dummy_protobuf_msg.pipeline.CopyFrom(self.pipeline)
#
#        # print(dummy_message.get_protobuf_msg_as_dict())
#        # print(json_format.MessageToDict(self.dummy_protobuf_msg))
#        # test adding service with parameters
#        # self.assertDictEqual(dummy_message.get_protobuf_msg_as_dict(),
#        #                     json_format.MessageToDict(self.dummy_protobuf_msg))
#
#    def test_get_content_as_dict(self):
#        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
#
#        self.assertTrue(type(dummy_message.get_content_as_dict()) is dict)
#
#        dummy_message.set_content('sollte true sein')
#        self.assertEqual(dummy_message.get_content_as_dict()['body'], 'sollte true sein')
#
#    def test_set_content(self):
#        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
#        dummy_message.set_content('angepasst')
#
#        self.assertEqual(dummy_message.get_content_as_dict()['body'], 'angepasst')
#        self.assertFalse(dummy_message.get_content_as_dict()['body'] is 'yeaaah test')
#
#        # test empty string as input
#        dummy_message.set_content('')
#        self.assertNotIn('body', dummy_message.get_services_as_dict())
#
#    def test_get_content(self):
#        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
#
#        self.assertTrue(type(dummy_message.get_content()) is service_com_pb2.Payload)
#
#        dummy_message.set_content('sollte true sein')
#        self.assertEqual(dummy_message.get_content_as_dict()['body'], 'sollte true sein')
#
#    def test_pop_service(self):
#        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
#        dummy_message.add_service('127.0.0.1', 1234)
#
#        popped_service = dummy_message.pop_service()
#        self.assertTrue(type(popped_service is dict))
#        self.assertEqual(popped_service['id'], '127.0.0.1:6766')
#        self.assertTrue(len(dummy_message.get_services_as_dict()) is 1)
#
#        popped_service = dummy_message.pop_service()
#        self.assertEqual(popped_service['id'], '127.0.0.1:1234')
#        self.assertTrue(len(dummy_message.get_services_as_dict()) is 0)
#
#    def test_is_empty_pipeline(self):
#        dummy_message = mosaic_message.Message(self.dummy_protobuf_msg)
#        dummy_message.add_service('127.0.0.1', 1111)
#
#        self.assertFalse(dummy_message.is_empty_pipeline())
#        self.assertFalse(mosaic_message.Message.is_empty_pipeline(dummy_message))
#
#        # remove dummy services
#        dummy_message.pop_service()
#        dummy_message.pop_service()
#
#        self.assertTrue(dummy_message.is_empty_pipeline())
#        self.assertTrue(mosaic_message.Message.is_empty_pipeline(dummy_message))
#

if __name__ == '__main__':
    unittest.main()
