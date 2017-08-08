#!/usr/bin/env python3.5

from mosaic.communication import service_com_pb2
from google.protobuf import json_format
import socket
import sys
import urllib.parse


class Utils:
    @staticmethod
    def serialize(mosaic_msg):
        return service_com_pb2.MosaicMessage.SerializeToString(mosaic_msg)

    @staticmethod
    def deserialize(mosaic_msg_serialized):
        mosaic_msg_received = service_com_pb2.MosaicMessage()
        mosaic_msg_received.MergeFromString(mosaic_msg_serialized)
        return mosaic_msg_received


class Message:
    def __init__(self, protobuf_msg=None):
        if protobuf_msg is None:
            self.mosaic_msg = service_com_pb2.MosaicMessage()
        else:
            self.mosaic_msg = service_com_pb2.MosaicMessage()
            self.mosaic_msg.CopyFrom(protobuf_msg)
        self.BUFFER_SIZE = 1024
        self.MSG_RESPONSE_OK = 0
        self.MSG_RESPONSE_NOK = 1

    def send(self, ip, port):
        address_tuple = (ip, port)
        self.mosaic_msg = Utils.serialize(self.mosaic_msg)

        connection = socket.create_connection(address_tuple)
        connection.send(self.mosaic_msg)

        resp = connection.recv(self.BUFFER_SIZE)
        connection.close()
        return resp

    def recv(self, ip, port):
        s = socket.socket()
        # s.setblocking(0)
        s.bind((ip, port))
        s.listen()

        connection, sender_address = s.accept()
        # while 1:
        data = connection.recv(self.BUFFER_SIZE)
        msg_received = Utils.deserialize(data)
        # if not data:
        #     break
        connection.send(self.MSG_RESPONSE_OK.to_bytes(1, sys.byteorder))
        connection.close()

        return Message(msg_received)

    def add_service(self, ip, port, params):
        pipeline = service_com_pb2.Pipeline()
        service = pipeline.services.add()
        service.id = 'service-' + ip + ':' + str(port)
        parameter = service.parameters.add()
        parameter.serviceParams = urllib.parse.urlencode(params)

        self.mosaic_msg.pipeline.CopyFrom(pipeline)

    def set_content(self, data):
        payload = service_com_pb2.Payload()
        payload.firstNumber = data['firstNumber']
        payload.secondNumber = data['secondNumber']

        self.mosaic_msg.payload.CopyFrom(payload)

    def get_content(self):
        return self.mosaic_msg.payload

    def get_content_as_dict(self):
        return json_format.MessageToDict(self.mosaic_msg.payload)

    def get_mosaic_msg(self):
        return self.mosaic_msg

    def get_mosaic_msg_as_dict(self):
        return json_format.MessageToDict(self.mosaic_msg)
