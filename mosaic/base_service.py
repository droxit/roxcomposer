#!/usr/bin/env python3.6

from mosaic.communication import mosaic_message
from mosaic.logging import basic_logger
import socket
import sys


# The BaseService class yields a full working base microservice, which is able to communicate over mosaic messages
# with other services. To test it out just create a service which inherits from this BaseService class. Simply use the
# send and receive functions to communicate with other services. The direction of the communication is handled over
# a predefined pipeline which gets posted to the first service in the pipeline. The pipeline object ist contained
# in the mosaic message. Check the README.rst for more information.
class BaseService:
    def __init__(self, params=None):
        self.params = params
        if params is None:
            self.params = {
                'ip': '127.0.0.1',
                'port': 5001,
                'name': 'anonymous-service'
            }
        self.BUFFER_SIZE = 1024
        self.MSG_RESPONSE_OK = 0
        self.MSG_RESPONSE_NOK = 1
        logger_params = {}
        if 'logging' in params:
            logger_params = params['logging']
        self.logger = basic_logger.BasicLogger(params['name'], **logger_params)
        self.arguments = {}

        self.mosaic_message = mosaic_message.Message()
        self.payload = None

    # need to be overwritten by inhertied classes.
    def on_message(self, msg):
        pass

    # send a mosaic protobuf message to the next service in the pipeline.
    def send(self):
        me = self.mosaic_message.pop_service()

        if 'services' not in self.mosaic_message.get_services_as_dict():
            return
        elif len(self.mosaic_message.get_services_as_dict()['services']) == 0:
            return

        next_service = self.mosaic_message.get_services_as_dict()['services'][0]
        next_service_id = next_service['id'].split(':')
        address_tuple = (next_service_id[0], next_service_id[1])

        self.mosaic_message = mosaic_message.Utils.serialize(self.mosaic_message.get_protobuf_msg())

        connection = socket.create_connection(address_tuple)
        connection.send(self.mosaic_message)

        resp = connection.recv(self.BUFFER_SIZE)
        connection.close()
        return resp

    # receive mosaic protobuf messages sent to a socket running on the specified ip and port. To handle the received
    # message please implement the on_message funtion in your inherited service.
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
            self.mosaic_message = mosaic_message.Message(msg_received)

            self.on_message(self.mosaic_message)
            connection.send(self.MSG_RESPONSE_OK.to_bytes(1, sys.byteorder))
            connection.close()

            if not data:
                break

    # this function is usually called by services, to receive a message out of the pipeline object posted as part of
    # the mosaic protobuf message.
    def recv_pipeline_msg(self):
        self.recv(self.params['ip'], self.params['port'])

    # set the content of the message currently handled by the service. @data should be a (json) string.
    def set_content(self, data):
        return mosaic_message.Message.set_content(self.mosaic_message, data)

    # get the content of the message currently handled by the service in protobuf format. To get a more usable message
    # use the get_contant_as_dict function.
    def get_content(self):
        return mosaic_message.Message.get_content(self.mosaic_message)

    # get the content of the message curerntly handled by the service as a dicitionary. Remember that the dict only
    # yields a representation of the actual message. So if you actually want to manipulate values in the message you
    # have to set the changed values manually in the protobuf message.
    def get_content_as_dict(self):
        return mosaic_message.Message.get_content_as_dict(self.mosaic_message)

    # get the currently handled message as a protobuf object
    def get_protobuf_message(self):
        return mosaic_message.Message.get_protobuf_msg(self.mosaic_message)
