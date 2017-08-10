#!/usr/bin/env python3.5

from mosaic.communication import mosaic_message
import socket
import sys


class BaseService:
    def __init__(self, params=None):
        self.params = params
        if params is None:
            self.params = {
                'ip': '127.0.0.1',
                'port': 5001
            }
        self.BUFFER_SIZE = 1024
        self.MSG_RESPONSE_OK = 0
        self.MSG_RESPONSE_NOK = 1

        self.mosaic_message = mosaic_message.Message()
        self.mosaic_message.add_service(self.params['ip'], self.params['port'], self.params)
        self.payload = None

    def on_message(self, msg):
            pass

    def send(self, ip, port):
        address_tuple = (ip, port)
        self.mosaic_message = mosaic_message.Utils.serialize(self.mosaic_message.get_protobuf_msg())

        connection = socket.create_connection(address_tuple)
        connection.send(self.mosaic_message)

        resp = connection.recv(self.BUFFER_SIZE)
        connection.close()
        return resp

    def recv(self, ip, port):
        s = socket.socket()
        # s.setblocking(0)
        s.bind((ip, port))
        s.listen()

        while 1:
            connection, sender_address = s.accept()
            print('Accepted connection from: ' + sender_address[0] + ':' + str(sender_address[1]))
            data = connection.recv(self.BUFFER_SIZE)
            msg_received = mosaic_message.Utils.deserialize(data)
            self.on_message(mosaic_message.Message(msg_received))
            connection.send(self.MSG_RESPONSE_OK.to_bytes(1, sys.byteorder))
            connection.close()

            if not data:
                break

    def set_content(self, data):
        return mosaic_message.Message.set_content(self.mosaic_message, data)

    def get_content(self):
        return mosaic_message.Message.get_content(self.mosaic_message)

    def get_content_as_dict(self):
        return mosaic_message.Message.get_content_as_dict(self.mosaic_message)

    def get_protobuf_message(self):
        return mosaic_message.Message.get_protobuf_msg(self.mosaic_message)
