# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

from roxcomposer.communication import service_com_pb2 as proto
import uuid
import json
import struct
import time
from roxcomposer import exceptions


def get_packet_len(msg):
    if len(msg) >= 4:
        return struct.unpack('>I', msg[:4])[0]
    raise exceptions.InvalidArgument('the provided string was too short: {}'.format(msg))


# prefixes msg with it's length as a 32bit big endian integer
def frame_message(msg):
    return struct.pack('>I', len(msg)) + msg


# remove the length prefix (see frame_message) from msg
# throws an exception if len(msg) does not match the prefixed length
def unframe_message(msg):
    l = struct.unpack('>I', msg[:4])[0]
    if l + 4 != len(msg):
        raise exceptions.MessageLengthMismatch(
            'Message of length {} does not match frame header {}'.format(len(msg), l))
    return msg[4:]


class Service:
    def __init__(self, ip, port, parameters=None):
        self.ip = ip
        self.port = port
        if parameters == None:
            self.parameters = []
        else:
            self.parameters = parameters

    def encodeId(self):
        return "{}:{}".format(self.ip, self.port)

    @staticmethod
    def decodeId(idstring):
        parts = idstring.split(':')
        if len(parts) < 2:
            errmsg = 'invalid service id: {}'.format(idstring)
            raise exceptions.InvalidServiceId(errmsg)
        port = int(parts.pop())
        ip = ':'.join(parts)
        return (ip, port)

    def __str__(self):
        return str({'ip': self.ip, 'port': self.port, 'parameters': self.parameters})

    def __repr__(self):
        return '<Service ' + str(self) + '>'

    def __eq__(self, other):
        return repr(self) == repr(other)


class Message:
    def __init__(self):
        self.pipeline = []
        self.id = None
        self.payload = None
        self.create_id()
        self.created = int(time.time() * 1000)

    def create_id(self):
        self.id = str(uuid.uuid4())

    def set_payload(self, data):
        self.payload = data

    def get_payload(self):
        return self.payload

    def get_content_as_dict(self):
        return {
            'id': self.id,
            'pipeline': self.pipeline,
            'payload': self.payload
        }

    # raises KeyError if the pipeline is empty
    def pop_service(self):
        return self.pipeline.pop(0)

    # raises KeyError if the pipeline is empty
    def peek_service(self):
        return self.pipeline[0]

    def add_service(self, service):
        self.pipeline.append(service)

    def has_empty_pipeline(self):
        return len(self.pipeline) == 0

    def serialize_to_protobuf(self):
        pmsg = proto.ROXcomposerMessage()
        for p in self.pipeline:
            s = pmsg.pipeline.services.add()
            s.id = p.encodeId()
            for para in p.parameters:
                param = s.parameters.add()
                param.serviceParams = para

        pmsg.id = self.id
        pmsg.created = self.created
        pmsg.payload.body = self.payload
        binmsg = pmsg.SerializeToString()
        return binmsg

    @staticmethod
    def deserialize_from_protobuf(binmsg):
        msg = Message()
        pmsg = proto.ROXcomposerMessage()
        pmsg.ParseFromString(binmsg)
        msg.set_payload(pmsg.payload.body)
        msg.id = pmsg.id
        msg.created = pmsg.created
        for s in pmsg.pipeline.services:
            ip, port = Service.decodeId(s.id)
            msg.add_service(Service(ip, port, [x.serviceParams for x in s.parameters]))

        return msg

    def serialize_to_json(self):
        msg = {
            'id': self.id,
            'created': self.created,
            'pipeline': [x for x in map(lambda s: {'id': s.encodeId(), 'parameters': s.parameters}, self.pipeline)],
            'payload': self.payload
        }

        return json.dumps(msg).encode()

    @staticmethod
    def deserialize_from_json(jsonstring):
        msg = Message()
        d = json.loads(jsonstring)
        msg.set_payload(d['payload'])
        msg.id = d['id']
        for s in d['pipeline']:
            ip, port = Service.decodeId(s['id'])
            msg.add_service(Service(ip, port, s['parameters']))

        return msg

    def serialize(self):
        return frame_message(self.serialize_to_protobuf())

    @staticmethod
    def deserialize(msg):
        return Message.deserialize_from_protobuf(unframe_message(msg))
