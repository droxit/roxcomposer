#!/usr/bin/env python3.5

from mosaic.communication import service_com_pb2
import uuid
import urllib.parse
import socket
import sys


class BaseService:
    def __init__(self, params=None):
        if params is None:
            params = dict()

        self.mosaic_message = service_com_pb2.MosaicMessage()
        self.pipeline = service_com_pb2.Pipeline()

        self.connection = None
        self.hearing_socket = None
        self.sender_address = None
        self.COMMUNICATION_IP = '127.0.0.1'
        self.COMMUNICATION_PORT = 5001
        self.BUFFER_SIZE = 1024
        self.MSG_RESPONSE_OK = 0

        service = self.pipeline.services.add()
        service.id = 'service-' + uuid.uuid4().hex
        parameter = service.parameters.add()
        parameter.serviceParams = urllib.parse.urlencode(params)

        self.payload = service_com_pb2.Payload()
        # payload.firstNumber = 2
        # payload.secondNumber = 2

        self.mosaic_message.pipeline.CopyFrom(self.pipeline)
        self.mosaic_message.payload.CopyFrom(self.payload)

    def hear_msg(self):
        self.hearing_socket = socket.socket()
        # self.hearing_socket.setblocking(0)
        self.hearing_socket.bind((self.COMMUNICATION_IP, self.COMMUNICATION_PORT))
        self.hearing_socket.listen()

        self.connection, self.sender_address = self.hearing_socket.accept()
        # while 1:
        data = self.connection.recv(self.BUFFER_SIZE)
            # if not data:
            #     break
        print(data)
        self.mosaic_message = service_com_pb2.MosaicMessage()
        self.mosaic_message.MergeFromString(data)
        print(self.get_mosaic_message())
        self.connection.send(self.MSG_RESPONSE_OK.to_bytes(1, sys.byteorder))
        self.connection.close()

    def set_payload(self, first_number, second_number):
        self.payload.firstNumber = first_number
        self.payload.secondNumber = second_number

        self.mosaic_message.payload.CopyFrom(self.payload)

    def get_payload(self):
        return {
            'firstNumber': self.mosaic_message.payload.firstNumber,
            'secondNumber': self.mosaic_message.payload.secondNumber
        }

    def speak_msg(self, msg):
        self.connection = socket.create_connection((self.COMMUNICATION_IP, self.COMMUNICATION_PORT))
        print(self.connection)
        self.connection.send(msg)
        return self.connection.recv(self.BUFFER_SIZE)

    def close_communication(self):
        self.hearing_socket.close()
        # self.connection.close()

    # def register_service(self, service):
    #     if service is not None:
    #         new_service = self.pipeline.services.add()
    #         new_service.id = service.id
    #         new_service.params = service.params
    #
    #         self.mosaic_message.pipeline.MergeFrom(new_service)
    #         return True
    #     else:
    #         print('ERROR - 01')
    #         return False

    def get_mosaic_message(self):
        return self.mosaic_message
