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

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service_com.proto',
  package='service_communication',
  syntax='proto3',
  serialized_pb=_b('\n\x11service_com.proto\x12\x15service_communication\"\x95\x01\n\x12ROXcomposerMessage\x12\x31\n\x08pipeline\x18\x01 \x01(\x0b\x32\x1f.service_communication.Pipeline\x12/\n\x07payload\x18\x02 \x01(\x0b\x32\x1e.service_communication.Payload\x12\n\n\x02id\x18\x03 \x01(\t\x12\x0f\n\x07\x63reated\x18\x04 \x01(\x03\"<\n\x08Pipeline\x12\x30\n\x08services\x18\x05 \x03(\x0b\x32\x1e.service_communication.Service\"K\n\x07Service\x12\n\n\x02id\x18\x06 \x01(\t\x12\x34\n\nparameters\x18\x07 \x03(\x0b\x32 .service_communication.Parameter\"\"\n\tParameter\x12\x15\n\rserviceParams\x18\x08 \x01(\t\"\x17\n\x07Payload\x12\x0c\n\x04\x62ody\x18\t \x01(\tb\x06proto3')
)




_ROXCOMPOSERMESSAGE = _descriptor.Descriptor(
  name='ROXcomposerMessage',
  full_name='service_communication.ROXcomposerMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pipeline', full_name='service_communication.ROXcomposerMessage.pipeline', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payload', full_name='service_communication.ROXcomposerMessage.payload', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='service_communication.ROXcomposerMessage.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created', full_name='service_communication.ROXcomposerMessage.created', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=194,
)


_PIPELINE = _descriptor.Descriptor(
  name='Pipeline',
  full_name='service_communication.Pipeline',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='services', full_name='service_communication.Pipeline.services', index=0,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=196,
  serialized_end=256,
)


_SERVICE = _descriptor.Descriptor(
  name='Service',
  full_name='service_communication.Service',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='service_communication.Service.id', index=0,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='service_communication.Service.parameters', index=1,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=258,
  serialized_end=333,
)


_PARAMETER = _descriptor.Descriptor(
  name='Parameter',
  full_name='service_communication.Parameter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='serviceParams', full_name='service_communication.Parameter.serviceParams', index=0,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=335,
  serialized_end=369,
)


_PAYLOAD = _descriptor.Descriptor(
  name='Payload',
  full_name='service_communication.Payload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='body', full_name='service_communication.Payload.body', index=0,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=371,
  serialized_end=394,
)

_ROXCOMPOSERMESSAGE.fields_by_name['pipeline'].message_type = _PIPELINE
_ROXCOMPOSERMESSAGE.fields_by_name['payload'].message_type = _PAYLOAD
_PIPELINE.fields_by_name['services'].message_type = _SERVICE
_SERVICE.fields_by_name['parameters'].message_type = _PARAMETER
DESCRIPTOR.message_types_by_name['ROXcomposerMessage'] = _ROXCOMPOSERMESSAGE
DESCRIPTOR.message_types_by_name['Pipeline'] = _PIPELINE
DESCRIPTOR.message_types_by_name['Service'] = _SERVICE
DESCRIPTOR.message_types_by_name['Parameter'] = _PARAMETER
DESCRIPTOR.message_types_by_name['Payload'] = _PAYLOAD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ROXcomposerMessage = _reflection.GeneratedProtocolMessageType('ROXcomposerMessage', (_message.Message,), dict(
  DESCRIPTOR = _ROXCOMPOSERMESSAGE,
  __module__ = 'service_com_pb2'
  # @@protoc_insertion_point(class_scope:service_communication.ROXcomposerMessage)
  ))
_sym_db.RegisterMessage(ROXcomposerMessage)

Pipeline = _reflection.GeneratedProtocolMessageType('Pipeline', (_message.Message,), dict(
  DESCRIPTOR = _PIPELINE,
  __module__ = 'service_com_pb2'
  # @@protoc_insertion_point(class_scope:service_communication.Pipeline)
  ))
_sym_db.RegisterMessage(Pipeline)

Service = _reflection.GeneratedProtocolMessageType('Service', (_message.Message,), dict(
  DESCRIPTOR = _SERVICE,
  __module__ = 'service_com_pb2'
  # @@protoc_insertion_point(class_scope:service_communication.Service)
  ))
_sym_db.RegisterMessage(Service)

Parameter = _reflection.GeneratedProtocolMessageType('Parameter', (_message.Message,), dict(
  DESCRIPTOR = _PARAMETER,
  __module__ = 'service_com_pb2'
  # @@protoc_insertion_point(class_scope:service_communication.Parameter)
  ))
_sym_db.RegisterMessage(Parameter)

Payload = _reflection.GeneratedProtocolMessageType('Payload', (_message.Message,), dict(
  DESCRIPTOR = _PAYLOAD,
  __module__ = 'service_com_pb2'
  # @@protoc_insertion_point(class_scope:service_communication.Payload)
  ))
_sym_db.RegisterMessage(Payload)


# @@protoc_insertion_point(module_scope)
