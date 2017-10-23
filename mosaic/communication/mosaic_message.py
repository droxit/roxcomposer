#!/usr/bin/env python3.6

from mosaic.communication import service_com_pb2
from google.protobuf import json_format
import urllib.parse
import uuid
import json
from mosaic import exceptions


# This class offers serialization and deserialization functions to parse a protobuf message directly after it has been
# sent or received.
class Utils:
    @staticmethod
    def serialize(protobuf_msg):
        return service_com_pb2.MosaicMessage.SerializeToString(protobuf_msg)

    @staticmethod
    def deserialize(protobuf_msg_serialized):
        protobuf_msg_received = service_com_pb2.MosaicMessage()
        protobuf_msg_received.MergeFromString(protobuf_msg_serialized)
        return protobuf_msg_received


# The Message class offers an easier handling of protobuf messages used for communication. Therefor services don't need
# to use the protobuf classes and methods.
class Message:
    def __init__(self, protobuf_msg=None):
        # the messag can be set up either as a new message or an existing protobuf msg
        if protobuf_msg is None:
            try:
                self.protobuf_msg = service_com_pb2.MosaicMessage()
                self.protobuf_msg.id = str(uuid.uuid4())
            except Exception:
                raise exceptions.InvalidMosaicMessage('Message.__init__() - failed at creating a new MosaicMessage.')
        else:
            try:
                self.protobuf_msg = service_com_pb2.MosaicMessage()
                self.protobuf_msg.CopyFrom(protobuf_msg)
            except TypeError:
                raise exceptions.InvalidMosaicMessage('Message.__init__() - ' + str(protobuf_msg) + ' is not a valid '
                                                                                                    'MosaicMessage.')

        self.pipeline = self.protobuf_msg.pipeline
        self.payload = self.protobuf_msg.payload
        self.id = self.protobuf_msg.id

    # add a service to the currently processed pipeline
    def add_service(self, ip, port, params=None):
        service = self.pipeline.services.add()
        service.id = ip + ':' + str(port)
        if params is not None:
            parameter = service.parameters.add()
            parameter.serviceParams = urllib.parse.urlencode(params)

    # get services out of the current message as protobuf Service objects
    def get_services(self):
        return self.protobuf_msg.pipeline.services

    # get services out of the current message as dictionary objects
    def get_services_as_dict(self):
        return json_format.MessageToDict(self.protobuf_msg.pipeline)

    # pop out the first service of the pipeline
    def pop_service(self):
        services_as_dict = self.get_services_as_dict()
        me = services_as_dict['services'].pop(0)

        json_format.Parse(json.dumps(services_as_dict), self.protobuf_msg.pipeline)

        return me

    # set the content @data of the current message
    def set_content(self, data):
        payload = service_com_pb2.Payload()
        payload.body = data

        self.protobuf_msg.payload.CopyFrom(payload)

    # get the content out of the current message as a protobuf Payload object
    def get_content(self):
        return self.protobuf_msg.payload

    # get the content out of the current message as a dictionary
    def get_content_as_dict(self):
        return json_format.MessageToDict(self.protobuf_msg.payload)

    # get the current message as a protobuf MosaicMessage object
    def get_protobuf_msg(self):
        return self.protobuf_msg

    # get the current message as a dictionary
    def get_protobuf_msg_as_dict(self):
        return json_format.MessageToDict(self.protobuf_msg)

    # get current message id
    def get_message_id(self):
        return self.id

    # this function returns true, if the pipeline is empty, which means if there is no other services except itself in
    # the pipeline
    def is_empty_pipeline(self, mosaic_msg=None):
        if mosaic_msg is None:
            if self.get_services_as_dict().get('services') is None:
                return True
            elif len(self.get_services_as_dict()['services']) == 1:
                return True
            else:
                return False
        else:
            if mosaic_msg.get_services_as_dict().get('services') is None:
                return True
            elif len(mosaic_msg.get_services_as_dict()['services']) == 1:
                return True
            else:
                return False

    # override str method, to get a string representaion of the message
    def __str__(self):
        return str(self.get_protobuf_msg_as_dict())
