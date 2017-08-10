#!/usr/bin/env python3.5

from mosaic.communication import service_com_pb2
from google.protobuf import json_format
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
            self.mosaic_msg.MergeFrom(protobuf_msg)

    def add_service(self, ip, port, params):
        pipeline = service_com_pb2.Pipeline()
        service = pipeline.services.add()
        service.id = 'service-' + ip + ':' + str(port)
        parameter = service.parameters.add()
        parameter.serviceParams = urllib.parse.urlencode(params)

        self.mosaic_msg.pipeline.CopyFrom(pipeline)

    def set_content(self, data):
        payload = service_com_pb2.Payload()
        payload.body = data

        self.mosaic_msg.payload.CopyFrom(payload)

    def get_content(self):
        return self.mosaic_msg.payload

    def get_content_as_dict(self):
        return json_format.MessageToDict(self.mosaic_msg.payload)

    def get_protobuf_msg(self):
        return self.mosaic_msg

    def get_protobuf_msg_as_dict(self):
        return json_format.MessageToDict(self.mosaic_msg)
