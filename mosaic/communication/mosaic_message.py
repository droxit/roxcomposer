from mosaic.communication import service_com_pb2 as proto
from google.protobuf import json_format
import urllib.parse
import uuid
import json
import struct
from mosaic import exceptions

def frame_message(msg):
    return struct.pack('>I', len(msg)) + msg

def unframe_message(msg):
    l = struct.unpack('>I', msg[:4])
    if l + 4 != len(msg):
        raise exceptions.MessageLengthMismatch('Message of length {} does not match frame header {}'.format(len(msg), l))
    return msg[4:]

class Service():
    def __init__(self, ip, port, parameters=[]):
        self.ip = ip
        self.port = port
        self.parameters = parameters

    def encodeId(self):
        return "{}:{}".format(ip, port)

    def decodeId(idstring):
        parts = idstring.split(':')
        if len(parts) < 2:
            errmsg = 'invalid service id: {}'.format(next_service)
            raise exceptions.InvalidServiceId(errmsg)
        self.port = int(next_service_id.pop())
        self.ip = ':'.join(next_service_id)

class Message():
    def __init__(self):
        self.pipeline = []
        self.id = None
        self.payload = None

    def create_id(self):
        self.id = uuid.uuid4()

    def set_payload(self, data):
        self.payload = data

    def get_payload(self):
        return self.payload

    def get_content_as_dict(self):
        return {
                'pipeline': self.pipeline,
                'id': self.id,
                'payload': self.payload
            }

    # raises KeyError if the pipeline is empty
    def pop_service(self):
        return pipeline.pop(0)

    def add_service(self, service):
        self.pipeline.append(service)

    def serializeToProtobuf(self):
        pmsg = proto.MosaicMessage()
        for p in self.pipeline:
            s = proto.Service()
            s.id = p.encodeAdress()
            for para in p.parameters:
                s.parameters.append(para)
            msg.pipeline.services.append(s)

        pmsg.id = self.id
        pmsg.payload.body = self.payload
        binmsg = msg.SerializeToString()

        return struct.pack('>I', len(binmsg)) + binmsg

    @staticmethod
    def deserializeFromProtobuf(binmsg):
        msg = Message()
        pmsg = proto.MosaicMessage()
        pmsg.parseFromString(binmsg)
        msg.set_content(pmsg.payload.string)
        self.id = pmsg.id
        for s in pmsg.pipeline:
            ip, port = Service.decodeId(s.id)
            msg.add_service(Service(ip, port, s.parameters))

        return msg

    def serializeToJson(self):
        msg = {
                'id': self.id,
                'pipeline': [x for x in map(lambda s: { 'id': s.encode(), 'parameters': s.parameters }, self.pipeline)],
                'payload': self.payload
            }

        return json.dumps(msg)

    @staticmethod
    def deserializeFromJson(jsonstring):
        msg = Message()
        d = json.loads(jsonstring)
        msg.set_content(d['payload'])
        msg.id = d['id']
        for s in d['pipeline']:
            ip, port = Service.decodeId(s.id)
            msg.add_service(Service(ip, port, s['parameters']))

        return msg


    def serialize(self):
        return frame_message(self.serializeToProtobuf())

    @staticmethod
    def deserialize(msg):
        return deserializeFromProtobuf(unframe_message(msg))
        
