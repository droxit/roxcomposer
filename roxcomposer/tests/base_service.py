# encoding: utf-8
#
# Tests for the base service
#
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
#

import unittest
import os
import json
from tempfile import TemporaryDirectory
from roxcomposer import base_service
from roxcomposer import exceptions
from roxcomposer.communication.roxcomposer_message import Service
from roxcomposer.communication.roxcomposer_message import Message
from multiprocessing import Process
import time


class TestBaseService(unittest.TestCase):
    def setUp(self):
        self.test_params_default = {
            'ip': '127.0.0.1',
            'port': 5001,
            'name': 'anonymous-service',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        }

        self.test_params_1 = {
            'ip': '127.0.0.1',
            'port': 6867,
            'name': 'fancy-service',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
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
                "level": "INFO",
                "logpath": "/dev/null"
            },
            'smtp': {
                'sender': 'roxcomposer@droxit.de',
                'smtpserver': 'smtp.server.de',
                'smtpusername': 'usernamee',
                'smtppassword': 'XXXXXXXXX',
                'usetls': True
            },
            'mail': {
                'subject': 'ROXcomposer-Demo: Test',
                'recipient': 'info@droxit.de'
            }
        }

    def tearDown(self):
        os.remove('monitoring.log')

    def test_init(self):
        # test initiatiaton without parameters
        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, None)

        # test initiation with at least 1 param missing
        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, {
            'ip': '127.0.0.1',
            'name': 'fancy-service',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        })

        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, {
            'ip': '127.0.0.1',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        })

        self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, self.test_params_2)

        # test initiation with params
        bs_with_params = base_service.BaseService({
            'ip': '127.0.0.1',
            'port': 6867,
            'name': 'fancy-service',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        })
        self.assertDictEqual(bs_with_params.params, self.test_params_1)

        # test initiation with params for a sent_mail service
        sent_mail_with_params = base_service.BaseService({
            "ip": "127.0.0.1",
            "port": 7001,
            "name": "sent_mail",
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            },
            'smtp': {
                'sender': 'roxcomposer@droxit.de',
                'smtpserver': 'smtp.server.de',
                'smtpusername': 'usernamee',
                'smtppassword': 'XXXXXXXXX',
                'usetls': True
            },
            'mail': {
                'subject': 'ROXcomposer-Demo: Test',
                'recipient': 'info@droxit.de'
            }
        })
        self.assertDictEqual(sent_mail_with_params.params, self.test_sent_mail)

    def test_get_service_id(self):
        s = base_service.BaseService(params={
            'ip': '127.0.0.1',
            'port': 1234,
            'name': 'dummy-service',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        })
        self.assertEqual(s.get_service_id(), self.dummy_service_id)

    def test_dispatch(self):
        s = base_service.BaseService(params={
            'ip': '127.0.0.1',
            'port': 1234,
            'name': 'dummy-service',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        })

        serv = Service("127.0.0.1", 1330)
        msg = Message()
        msg.set_payload("TEST.")
        msg.add_service(serv)
        s.roxcomposer_message = msg

        # since assertFalse also allows None, we do a assertTrue with the negated statement
        self.assertTrue(not s.dispatch("TEST."))

        s2 = base_service.BaseService(params={
            'ip': '127.0.0.1',
            'port': 1337,
            'name': 'dummy-service2',
            "logging": {
                "level": "INFO",
                "logpath": "/dev/null"
            }
        })

        p = Process(target=s2.listen, args=())
        p.start()
        time.sleep(0.5)

        serv = Service("127.0.0.1", 1337)
        msg = Message()
        msg.set_payload("TEST.")
        msg.add_service(serv)
        s.roxcomposer_message = msg

        self.assertTrue(s.dispatch("TEST."))

        p.terminate()

    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_config_loading(self):
        os.environ['DROXIT_ROXCOMPOSER_CONFIG'] = '/bogus/path/from/hell.json'
        self.assertRaises(exceptions.ConfigError, base_service.BaseService, { "service_key": "nevermind" })

        with TemporaryDirectory() as tdir:
            confname = os.path.join(tdir, "config.json")
            f = open(confname, "w")
            json.dump({"service": {"dummy": self.test_params_1}}, f)
            f.close()
            s = base_service.BaseService({"service_key": "service.dummy", "config_file": confname})

            self.assertDictEqual(s.params, self.test_params_1)

            os.environ['DROXIT_ROXCOMPOSER_CONFIG'] = confname

            self.assertRaises(exceptions.ParameterMissing, base_service.BaseService, { "service_key": "nevermind" })
            s = base_service.BaseService({"service_key": "service.dummy"})
            self.assertDictEqual(s.params, self.test_params_1)

            f = open(confname, "w")
            f.write('this is no proper JSON')
            f.close()
            self.assertRaises(exceptions.ConfigError, base_service.BaseService, { "service_key": "nevermind" })


if __name__ == '__main__':
    unittest.main()
