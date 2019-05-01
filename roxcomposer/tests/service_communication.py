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
import socket
import time

from multiprocessing import Process
from roxcomposer import base_service
from roxcomposer.communication import roxcomposer_message


def start_service(serv):
    serv = AppendService(serv['msg'], serv['args'])
    serv.listen()


class AppendService(base_service.BaseService):
    def __init__(self, msg, args):
        self.msg = msg
        super().__init__(args)

    def on_message(self, msg, msg_id, parameters=None):
        self.dispatch(msg + self.msg + parameters[0])


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.services = [
            {
                'msg': 'service 1',
                'args': {
                    'name': 'service1',
                    'ip': '127.0.0.1',
                    'port': 10001,
                    'logging': {
                        'level': 'WARNING',
                        'logpath': '/dev/null'
                    },
                    'monitoring': {
                        'filename': '/dev/null'
                    },
                    'params': ["some/file/path"]
                }
            },
            {
                'msg': 'service 2',
                'args': {
                    'name': 'service1',
                    'ip': '127.0.0.1',
                    'port': 10002,
                    'logging': {
                        'level': 'WARNING',
                        'logpath': '/dev/null'
                    },
                    'monitoring': {
                        'filename': '/dev/null'
                    },
                    'params': ["http://localhost:5000"]
                }
            },
            {
                'msg': 'service 3',
                'args': {
                    'name': 'service1',
                    'ip': '127.0.0.1',
                    'port': 10003,
                    'logging': {
                        'level': 'WARNING',
                        'logpath': '/dev/null'
                    },
                    'monitoring': {
                        'filename': '/dev/null'
                    },
                    'params': ["param"]
                }
            },
        ]

        self.children = []

        for serv in self.services:
            p = Process(target=start_service, args=(serv,))
            p.start()
            self.children.append(p)

    def tearDown(self):
        if len(self.children):
            for p in self.children:
                p.terminate()

    def test_pipeline(self):
        time.sleep(0.5)
        ip = "127.0.0.1"
        port = 10000
        mm = roxcomposer_message.Message()
        payload = "original message" * 1000
        expected_payload = payload
        for serv in self.services:
            expected_payload += serv['msg'] + serv['args']['params'][0]
        for serv in self.services:
            mm.add_service(roxcomposer_message.Service(serv['args']['ip'], serv['args']['port'], serv['args']['params']))
        mm.add_service(roxcomposer_message.Service(ip, port))
        mm.set_payload(payload)
        bin_msg = mm.serialize()

        msg = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ip, port))
            s.listen()

            conn = socket.create_connection((self.services[0]['args']['ip'], self.services[0]['args']['port']))
            conn.sendall(bin_msg)
            # conn.recv(1024)
            conn.close()

            conn, addr = s.accept()
            with conn:
                msg = conn.recv(len(payload) + 1024)

        msg = roxcomposer_message.Message.deserialize(msg)

        # there should not be a pipeline cause it 
        self.assertEqual(msg.payload, expected_payload)


if __name__ == '__main__':
    unittest.main()
