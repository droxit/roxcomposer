import unittest
import socket
import time
import http.client

from multiprocessing import Process
import threading
from roxcomposer.tests.classes import msg_concatenator
from roxcomposer import base_service
from roxcomposer.communication import roxcomposer_message


def start_service(serv):
    serv = msg_concatenator.MsgConcatenator(serv['args'])
    serv.listen_thread()
    serv.http.serve_forever()


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.services = [
            {
                'args': {
                    'name': 'service1',
                    'ip': '127.0.0.1',
                    'port': 10001,
                    'http_address': ("127.0.0.1", 11001),
                    'logging': {
                        'level': 'WARNING'
                    }
                }
            },
            {
                'args': {
                    'name': 'service1',
                    'ip': '127.0.0.1',
                    'port': 10002,
                    'http_address': ("127.0.0.1", 11002),
                    'logging': {
                        'level': 'WARNING'
                    }
                }
            }
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

        payloads = [ "afas0df9a0sdfij", "flk3j2323rf2f0-29f#!$!@#$pe+ü++", "asdlfkj23,dv   aefkdjflkj   " ]
        expected_payload = "".join(payloads).encode()

        for p in payloads:
            mm = roxcomposer_message.Message()
            for serv in self.services:
                 mm.add_service(roxcomposer_message.Service(serv['args']['ip'], serv['args']['port']))
            mm.set_payload(p)
            bin_msg = mm.serialize()

            msg = ""
            conn = socket.create_connection((self.services[0]['args']['ip'], self.services[0]['args']['port']))
            conn.sendall(bin_msg)
            conn.close()

            time.sleep(0.1)

        c = http.client.HTTPConnection('127.0.0.1', 11001)
        c.request('GET', '/')
        resp = c.getresponse().read()
        self.assertEqual(resp, expected_payload)

        c = http.client.HTTPConnection('127.0.0.1', 11002)
        c.request('GET', '/')
        resp = c.getresponse().read()
        self.assertEqual(resp, expected_payload)

if __name__ == '__main__':
    unittest.main()
