# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: private_chat.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12private_chat.proto\":\n\rclientMessage\x12\x12\n\nclientName\x18\x01 \x01(\t\x12\x15\n\rclientMessage\x18\x02 \x01(\t\"\x07\n\x05\x45mpty2;\n\x12PrivateChatService\x12%\n\x0bsendMessage\x12\x0e.clientMessage\x1a\x06.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'private_chat_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CLIENTMESSAGE']._serialized_start=22
  _globals['_CLIENTMESSAGE']._serialized_end=80
  _globals['_EMPTY']._serialized_start=82
  _globals['_EMPTY']._serialized_end=89
  _globals['_PRIVATECHATSERVICE']._serialized_start=91
  _globals['_PRIVATECHATSERVICE']._serialized_end=150
# @@protoc_insertion_point(module_scope)
