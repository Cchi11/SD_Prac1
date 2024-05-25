from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class clientMessage(_message.Message):
    __slots__ = ("clientName", "clientMessage")
    CLIENTNAME_FIELD_NUMBER: _ClassVar[int]
    CLIENTMESSAGE_FIELD_NUMBER: _ClassVar[int]
    clientName: str
    clientMessage: str
    def __init__(self, clientName: _Optional[str] = ..., clientMessage: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
