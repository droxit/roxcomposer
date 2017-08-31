#!/usr/bin/env python3.5

import unittest
import os
import socket
import signal
import time
from multiprocessing import Process
from mosaic import base_service
from mosaic.communication import mosaic_message

def sigint_handler(signum, frame):
    exit(0)

def start_service(serv):
    serv = AppendService(serv['msg'], serv['args'])
    serv.listen()


class AppendService(base_service.BaseService):
    def __init__(self, msg, args):
        self.msg = msg
        super().__init__(args)

    def on_message(self, msg):
        print(self.mosaic_message.get_protobuf_msg_as_dict())
        self.dispatch(msg + self.msg)


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.services = [
            {'msg': 'service 1', 'args': {'name': 'service1', 'ip': '127.0.0.1', 'port': 10001, 'logging': {'level': 'DEBUG'}}},
            {'msg': 'service 2', 'args': {'name': 'service1', 'ip': '127.0.0.1', 'port': 10002, 'logging': {'level': 'DEBUG'}}},
            {'msg': 'service 3', 'args': {'name': 'service1', 'ip': '127.0.0.1', 'port': 10003, 'logging': {'level': 'DEBUG'}}},
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
        mm = mosaic_message.Message()
        payload = "original message"
        expected_payload = payload
        for serv in self.services:
            expected_payload += serv['msg']
            mm.add_service(serv['args']['ip'], serv['args']['port'])
        mm.add_service(ip, port)
        mm.set_content(payload)
        bin_msg = mosaic_message.Utils.serialize(mm.get_protobuf_msg())



        msg = ""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ip,port))
            s.listen()

            conn = socket.create_connection((self.services[0]['args']['ip'], self.services[0]['args']['port']))
            conn.sendall(bin_msg)
            #conn.recv(1024)
            conn.close()

            conn, addr = s.accept()
            with conn:
                msg = conn.recv(2048)
                conn.send(b'OK')

        msg = mosaic_message.Utils.deserialize(msg)
        msg = mosaic_message.Message(msg)

        # there should not be a pipeline cause it 
        self.assertEqual(msg.get_content().body, expected_payload)
        

if __name__ == '__main__':
    unittest.main()
