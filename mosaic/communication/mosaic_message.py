#!/usr/bin/env python3.6

from mosaic.communication import service_com_pb2
from google.protobuf import json_format
import urllib.parse
import json


class Utils:
    @staticmethod
    def serialize(protobuf_msg):
        return service_com_pb2.MosaicMessage.SerializeToString(protobuf_msg)

    @staticmethod
    def deserialize(protobuf_msg_serialized):
        protobuf_msg_received = service_com_pb2.MosaicMessage()
        protobuf_msg_received.MergeFromString(protobuf_msg_serialized)
        return protobuf_msg_received


class Message:
    def __init__(self, protobuf_msg=None):
        if protobuf_msg is None:
            self.protobuf_msg = service_com_pb2.MosaicMessage()
        else:
            self.protobuf_msg = service_com_pb2.MosaicMessage()
            self.protobuf_msg.CopyFrom(protobuf_msg)

        self.pipeline = service_com_pb2.Pipeline()
        self.payload = service_com_pb2.Payload()

    def add_service(self, ip, port, params=None):
        service = self.pipeline.services.add()
        service.id = ip + ':' + str(port)
        if params is not None:
            parameter = service.parameters.add()
            parameter.serviceParams = urllib.parse.urlencode(params)

        self.protobuf_msg.pipeline.MergeFrom(self.pipeline)

    def get_services(self):
        return self.protobuf_msg.pipeline.services

    def get_services_as_dict(self):
        return json_format.MessageToDict(self.protobuf_msg.pipeline)

    def pop_service(self):
        services_as_dict = self.get_services_as_dict()
        me = services_as_dict['services'].pop(0)

        json_format.Parse(json.dumps(services_as_dict), self.protobuf_msg.pipeline)

        return me

    def set_content(self, data):
        payload = service_com_pb2.Payload()
        payload.body = data

        self.protobuf_msg.payload.CopyFrom(payload)

    def get_content(self):
        return self.protobuf_msg.payload

    def get_content_as_dict(self):
        return json_format.MessageToDict(self.protobuf_msg.payload)

    def get_protobuf_msg(self):
        return self.protobuf_msg

    def get_protobuf_msg_as_dict(self):
        return json_format.MessageToDict(self.protobuf_msg)
