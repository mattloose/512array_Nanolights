# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow/rpc/log.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from minLights.rpc import rpc_options_pb2 as minknow_dot_rpc_dot_rpc__options__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='minknow/rpc/log.proto',
  package='ont.rpc.log',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x15minknow/rpc/log.proto\x12\x0bont.rpc.log\x1a\x1dminknow/rpc/rpc_options.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"6\n\x16GetUserMessagesRequest\x12\x1c\n\x14include_old_messages\x18\x01 \x01(\x08\"\xf9\x01\n\x0bUserMessage\x12(\n\x04time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x08severity\x18\x02 \x01(\x0e\x32\x15.ont.rpc.log.Severity\x12\x12\n\nidentifier\x18\x03 \x01(\t\x12\x14\n\x0cuser_message\x18\x04 \x01(\t\x12;\n\nextra_data\x18\x05 \x03(\x0b\x32\'.ont.rpc.log.UserMessage.ExtraDataEntry\x1a\x30\n\x0e\x45xtraDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"c\n\x16SendUserMessageRequest\x12-\n\x08severity\x18\x02 \x01(\x0e\x32\x15.ont.rpc.log.SeverityB\x04\x88\xb5\x18\x01\x12\x1a\n\x0cuser_message\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\"\x19\n\x17SendUserMessageResponse\"*\n\x0fSendPingRequest\x12\x17\n\tping_data\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\"\x12\n\x10SendPingResponse*{\n\x08Severity\x12\x1a\n\x16MESSAGE_SEVERITY_TRACE\x10\x00\x12\x19\n\x15MESSAGE_SEVERITY_INFO\x10\x01\x12\x1c\n\x18MESSAGE_SEVERITY_WARNING\x10\x02\x12\x1a\n\x16MESSAGE_SEVERITY_ERROR\x10\x03\x32\x92\x02\n\nLogService\x12V\n\x11get_user_messages\x12#.ont.rpc.log.GetUserMessagesRequest\x1a\x18.ont.rpc.log.UserMessage\"\x00\x30\x01\x12`\n\x11send_user_message\x12#.ont.rpc.log.SendUserMessageRequest\x1a$.ont.rpc.log.SendUserMessageResponse\"\x00\x12J\n\tsend_ping\x12\x1c.ont.rpc.log.SendPingRequest\x1a\x1d.ont.rpc.log.SendPingResponse\"\x00\x62\x06proto3')
  ,
  dependencies=[minknow_dot_rpc_dot_rpc__options__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])

_SEVERITY = _descriptor.EnumDescriptor(
  name='Severity',
  full_name='ont.rpc.log.Severity',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SEVERITY_TRACE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SEVERITY_INFO', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SEVERITY_WARNING', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MESSAGE_SEVERITY_ERROR', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=602,
  serialized_end=725,
)
_sym_db.RegisterEnumDescriptor(_SEVERITY)

Severity = enum_type_wrapper.EnumTypeWrapper(_SEVERITY)
MESSAGE_SEVERITY_TRACE = 0
MESSAGE_SEVERITY_INFO = 1
MESSAGE_SEVERITY_WARNING = 2
MESSAGE_SEVERITY_ERROR = 3



_GETUSERMESSAGESREQUEST = _descriptor.Descriptor(
  name='GetUserMessagesRequest',
  full_name='ont.rpc.log.GetUserMessagesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='include_old_messages', full_name='ont.rpc.log.GetUserMessagesRequest.include_old_messages', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=156,
)


_USERMESSAGE_EXTRADATAENTRY = _descriptor.Descriptor(
  name='ExtraDataEntry',
  full_name='ont.rpc.log.UserMessage.ExtraDataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ont.rpc.log.UserMessage.ExtraDataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ont.rpc.log.UserMessage.ExtraDataEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=360,
  serialized_end=408,
)

_USERMESSAGE = _descriptor.Descriptor(
  name='UserMessage',
  full_name='ont.rpc.log.UserMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='ont.rpc.log.UserMessage.time', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='ont.rpc.log.UserMessage.severity', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='identifier', full_name='ont.rpc.log.UserMessage.identifier', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_message', full_name='ont.rpc.log.UserMessage.user_message', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extra_data', full_name='ont.rpc.log.UserMessage.extra_data', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_USERMESSAGE_EXTRADATAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=408,
)


_SENDUSERMESSAGEREQUEST = _descriptor.Descriptor(
  name='SendUserMessageRequest',
  full_name='ont.rpc.log.SendUserMessageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='severity', full_name='ont.rpc.log.SendUserMessageRequest.severity', index=0,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_message', full_name='ont.rpc.log.SendUserMessageRequest.user_message', index=1,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=410,
  serialized_end=509,
)


_SENDUSERMESSAGERESPONSE = _descriptor.Descriptor(
  name='SendUserMessageResponse',
  full_name='ont.rpc.log.SendUserMessageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=511,
  serialized_end=536,
)


_SENDPINGREQUEST = _descriptor.Descriptor(
  name='SendPingRequest',
  full_name='ont.rpc.log.SendPingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ping_data', full_name='ont.rpc.log.SendPingRequest.ping_data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=538,
  serialized_end=580,
)


_SENDPINGRESPONSE = _descriptor.Descriptor(
  name='SendPingResponse',
  full_name='ont.rpc.log.SendPingResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=582,
  serialized_end=600,
)

_USERMESSAGE_EXTRADATAENTRY.containing_type = _USERMESSAGE
_USERMESSAGE.fields_by_name['time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USERMESSAGE.fields_by_name['severity'].enum_type = _SEVERITY
_USERMESSAGE.fields_by_name['extra_data'].message_type = _USERMESSAGE_EXTRADATAENTRY
_SENDUSERMESSAGEREQUEST.fields_by_name['severity'].enum_type = _SEVERITY
DESCRIPTOR.message_types_by_name['GetUserMessagesRequest'] = _GETUSERMESSAGESREQUEST
DESCRIPTOR.message_types_by_name['UserMessage'] = _USERMESSAGE
DESCRIPTOR.message_types_by_name['SendUserMessageRequest'] = _SENDUSERMESSAGEREQUEST
DESCRIPTOR.message_types_by_name['SendUserMessageResponse'] = _SENDUSERMESSAGERESPONSE
DESCRIPTOR.message_types_by_name['SendPingRequest'] = _SENDPINGREQUEST
DESCRIPTOR.message_types_by_name['SendPingResponse'] = _SENDPINGRESPONSE
DESCRIPTOR.enum_types_by_name['Severity'] = _SEVERITY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetUserMessagesRequest = _reflection.GeneratedProtocolMessageType('GetUserMessagesRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETUSERMESSAGESREQUEST,
  __module__ = 'minLights.rpc.log_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.log.GetUserMessagesRequest)
  ))
_sym_db.RegisterMessage(GetUserMessagesRequest)

UserMessage = _reflection.GeneratedProtocolMessageType('UserMessage', (_message.Message,), dict(

  ExtraDataEntry = _reflection.GeneratedProtocolMessageType('ExtraDataEntry', (_message.Message,), dict(
    DESCRIPTOR = _USERMESSAGE_EXTRADATAENTRY,
    __module__ = 'minLights.rpc.log_pb2'
    # @@protoc_insertion_point(class_scope:ont.rpc.log.UserMessage.ExtraDataEntry)
    ))
  ,
  DESCRIPTOR = _USERMESSAGE,
  __module__ = 'minLights.rpc.log_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.log.UserMessage)
  ))
_sym_db.RegisterMessage(UserMessage)
_sym_db.RegisterMessage(UserMessage.ExtraDataEntry)

SendUserMessageRequest = _reflection.GeneratedProtocolMessageType('SendUserMessageRequest', (_message.Message,), dict(
  DESCRIPTOR = _SENDUSERMESSAGEREQUEST,
  __module__ = 'minLights.rpc.log_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.log.SendUserMessageRequest)
  ))
_sym_db.RegisterMessage(SendUserMessageRequest)

SendUserMessageResponse = _reflection.GeneratedProtocolMessageType('SendUserMessageResponse', (_message.Message,), dict(
  DESCRIPTOR = _SENDUSERMESSAGERESPONSE,
  __module__ = 'minLights.rpc.log_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.log.SendUserMessageResponse)
  ))
_sym_db.RegisterMessage(SendUserMessageResponse)

SendPingRequest = _reflection.GeneratedProtocolMessageType('SendPingRequest', (_message.Message,), dict(
  DESCRIPTOR = _SENDPINGREQUEST,
  __module__ = 'minLights.rpc.log_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.log.SendPingRequest)
  ))
_sym_db.RegisterMessage(SendPingRequest)

SendPingResponse = _reflection.GeneratedProtocolMessageType('SendPingResponse', (_message.Message,), dict(
  DESCRIPTOR = _SENDPINGRESPONSE,
  __module__ = 'minLights.rpc.log_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.log.SendPingResponse)
  ))
_sym_db.RegisterMessage(SendPingResponse)


_USERMESSAGE_EXTRADATAENTRY._options = None
_SENDUSERMESSAGEREQUEST.fields_by_name['severity']._options = None
_SENDUSERMESSAGEREQUEST.fields_by_name['user_message']._options = None
_SENDPINGREQUEST.fields_by_name['ping_data']._options = None

_LOGSERVICE = _descriptor.ServiceDescriptor(
  name='LogService',
  full_name='ont.rpc.log.LogService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=728,
  serialized_end=1002,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_user_messages',
    full_name='ont.rpc.log.LogService.get_user_messages',
    index=0,
    containing_service=None,
    input_type=_GETUSERMESSAGESREQUEST,
    output_type=_USERMESSAGE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='send_user_message',
    full_name='ont.rpc.log.LogService.send_user_message',
    index=1,
    containing_service=None,
    input_type=_SENDUSERMESSAGEREQUEST,
    output_type=_SENDUSERMESSAGERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='send_ping',
    full_name='ont.rpc.log.LogService.send_ping',
    index=2,
    containing_service=None,
    input_type=_SENDPINGREQUEST,
    output_type=_SENDPINGRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_LOGSERVICE)

DESCRIPTOR.services_by_name['LogService'] = _LOGSERVICE

# @@protoc_insertion_point(module_scope)