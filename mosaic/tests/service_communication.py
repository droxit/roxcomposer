#!/usr/bin/env python3.5

import unittest
import os
import socket
import signal
import time
from mosaic import base_service
from mosaic.communication import mosaic_message

class AppendService(base_service.BaseService):
    def __init__(self, msg, args):
        self.msg = msg
        super().__init__(args)
        self.listen()

    def on_message(self, msg):
        print(self.mosaic_message.get_protobuf_msg_as_dict())
        self.dispatch(msg + self.msg)


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.services = [
            {'msg': 'service 1', 'args': {'name': 'service1', 'ip': '127.0.0.1', 'port': 10001}},
            {'msg': 'service 2', 'args': {'name': 'service2', 'ip': '127.0.0.1', 'port': 10002}},
            {'msg': 'service 3', 'args': {'name': 'service3', 'ip': '127.0.0.1', 'port': 10003}}
        ]

        self.children = []

        for serv in self.services:
            pid = os.fork()
            if pid:
                self.children.append(pid)
            else:
                serv = AppendService(serv['msg'], serv['args'])

    def tearDown(self):
        if len(self.children):
            for pid in self.children:
                os.kill(pid, signal.SIGINT)

    def test_pipeline(self):
        time.sleep(0.5)
        ip = "127.0.0.1"
        port = 10000
        mm = mosaic_message.Message()
        payload = "original message"
        expected_payload = payload
        for serv in self.services:
            expected_payload += serv['msg']
            mm.add_service(serv['args']['ip'], serv['args']['port'])
        mm.add_service(ip, port)
        mm.set_content(payload)
        bin_msg = mosaic_message.Utils.serialize(mm.get_protobuf_msg())

        sock = socket.socket()
        sock.bind((ip,port))

        sock.connect((self.services[0]['args']['ip'], self.services[0]['args']['port']))
        sock.sendall(bin_msg)
        resp = sock.recv(2048)
        print(resp)

        sock.listen()
        conn, addr = sock.accept()
        recv_msg = conn.recv(2048)
        recv_msg = mosaic_message.Utils.deserialize(recv_msg)
        recv_msg = mosaic_message.Message(recv_msg)

        # there should not be a pipeline cause it 
        self.assertEqual(recv_msg.get_content(), expected_payload)
        

if __name__ == '__main__':
    unittest.main()
