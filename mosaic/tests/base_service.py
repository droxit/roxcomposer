import unittest
import os
import json
from tempfile import TemporaryDirectory
from mosaic import base_service
from mosaic import exceptions


class TestBaseService(unittest.TestCase):
    def setUp(self):
        self.test_params_default = {
            'ip': '127.0.0.1',
            'port': 5001,
            'name': 'anonymous-service'
        }

        self.test_params_1 = {
            'ip': '127.0.0.1',
            'port': 6867,
            'name': 'fancy-service'
        }

        self.test_params_2 = {
            'port': 7677,
            'name': 'missing-param-service'
        }

        self.dummy_service_id = '127.0.0.1:1234'

        self.test_sent_mail = {
            "ip": "127.0.0.1",
            "port": 7001,
            "name": "sent_mail",
            "logging": {
                "filename": "pipeline.log",
                "level": "INFO"
            },
            'smtp': {
                'sender': 'mosaic@droxit.de',
                'smtpserver': 'smtp.server.de',
                'smtpusername': 'usernamee',
                'smtppassword': 'XXXXXXXXX',
                'usetls': True
            },
            'mail': {
                'subject': 'Mosaic-Demo: Test',
                'recipient': 'info@droxit.de'
            }
        }

    def test_init(self):
        # test initiatiaton without parameters
        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, None)

        # test initiation with at least 1 param missing
        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, {
            'ip': '127.0.0.1',
            'name': 'fancy-service'
        })

        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, {
            'ip': '127.0.0.1'
        })

        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, self.test_params_2)

        # test initiation with params
        bs_with_params = base_service.BaseService({
            'ip': '127.0.0.1',
            'port': 6867,
            'name': 'fancy-service'
        })
        self.assertDictEqual(bs_with_params.params, self.test_params_1)

        # test initiation with params for a sent_mail service
        sent_mail_with_params = base_service.BaseService({
            "ip": "127.0.0.1",
            "port": 7001,
            "name": "sent_mail",
            "logging": {
                "filename": "pipeline.log",
                "level": "INFO"
            },
            'smtp': {
                'sender': 'mosaic@droxit.de',
                'smtpserver': 'smtp.server.de',
                'smtpusername': 'usernamee',
                'smtppassword': 'XXXXXXXXX',
                'usetls': True
            },
            'mail': {
                'subject': 'Mosaic-Demo: Test',
                'recipient': 'info@droxit.de'
            }
        })
        self.assertDictEqual(sent_mail_with_params.params, self.test_sent_mail)

    def test_get_service_id(self):
        s = base_service.BaseService(params={
            'ip': '127.0.0.1',
            'port': 1234,
            'name': 'dummy-service'
        })
        self.assertEqual(s.get_service_id(), self.dummy_service_id)
