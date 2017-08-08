#!/usr/bin/env python3.5

from mosaic.communication import mosaic_message


class BaseService:
    def __init__(self, params=None):
        self.params = params
        if params is None:
            self.params = {
                'ip': '127.0.0.1',
                'port': 5001
            }

        self.mosaic_message = mosaic_message.Message()
        self.mosaic_message.set_pipeline(self.params['ip'], self.params['port'], self.params)
        # self.pipeline = service_com_pb2.Pipeline()
        self.payload = None
        #
        # self.connection = None
        # self.hearing_socket = None
        # self.sender_address = None
        # self.COMMUNICATION_IP = '127.0.0.1'
        # self.COMMUNICATION_PORT = 5001
        # self.BUFFER_SIZE = 1024
        # self.MSG_RESPONSE_OK = 0

        # service = self.pipeline.services.add()
        # service.id = 'service-' + params['ip'] + ':' + params['port']
        # parameter = service.parameters.add()
        # parameter.serviceParams = urllib.parse.urlencode(params)

        # self.mosaic_message.pipeline.CopyFrom(self.pipeline)

    def recv(self):
        return mosaic_message.Message.recv(self.mosaic_message, self.params['ip'], self.params['port'])

        # self.hearing_socket = socket.socket()
        # # self.hearing_socket.setblocking(0)
        # self.hearing_socket.bind((self.COMMUNICATION_IP, self.COMMUNICATION_PORT))
        # self.hearing_socket.listen()
        #
        # self.connection, self.sender_address = self.hearing_socket.accept()
        # # while 1:
        # data = self.connection.recv(self.BUFFER_SIZE)
        #     # if not data:
        #     #     break
        # print(data)
        # self.mosaic_message = service_com_pb2.MosaicMessage()
        # self.mosaic_message.MergeFromString(data)
        # print(self.get_mosaic_message())
        # self.connection.send(self.MSG_RESPONSE_OK.to_bytes(1, sys.byteorder))
        # self.connection.close()

    # def set_payload(self, first_number, second_number):
    #     self.payload.firstNumber = first_number
    #     self.payload.secondNumber = second_number
    #
    #     self.mosaic_message.payload.CopyFrom(self.payload)

    def set_content(self, data):
        return mosaic_message.Message.set_content(self.mosaic_message, data)

    def get_content(self):
        return mosaic_message.Message.get_content(self.mosaic_message)

    def get_content_as_dict(self):
        return mosaic_message.Message.get_content_as_dict(self.mosaic_message)

    def send(self):
        # self.connection = socket.create_connection((self.COMMUNICATION_IP, self.COMMUNICATION_PORT))
        # print(self.connection)
        # self.connection.send(msg)
        # return self.connection.recv(self.BUFFER_SIZE)
        self.mosaic_message = mosaic_message.Utils.serialize(self.mosaic_message)
        return mosaic_message.Message.send(self.mosaic_message, self.params['ip'], self.params['port'])

    def get_mosaic_message(self):
        return mosaic_message.Message.get_mosaic_msg(self.mosaic_message)
