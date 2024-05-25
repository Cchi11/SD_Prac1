from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddClientRequest(_message.Message):
    __slots__ = ("client_name", "client_address_and_port")
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ADDRESS_AND_PORT_FIELD_NUMBER: _ClassVar[int]
    client_name: str
    client_address_and_port: str
    def __init__(self, client_name: _Optional[str] = ..., client_address_and_port: _Optional[str] = ...) -> None: ...

class ClientNameRequest(_message.Message):
    __slots__ = ("client_name",)
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    client_name: str
    def __init__(self, client_name: _Optional[str] = ...) -> None: ...

class ClientInfo(_message.Message):
    __slots__ = ("client_name", "client_address_and_port")
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ADDRESS_AND_PORT_FIELD_NUMBER: _ClassVar[int]
    client_name: str
    client_address_and_port: str
    def __init__(self, client_name: _Optional[str] = ..., client_address_and_port: _Optional[str] = ...) -> None: ...

class InfoFromNameServer(_message.Message):
    __slots__ = ("accepted",)
    ACCEPTED_FIELD_NUMBER: _ClassVar[int]
    accepted: int
    def __init__(self, accepted: _Optional[int] = ...) -> None: ...

class ErrorInfo(_message.Message):
    __slots__ = ("error_message",)
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_message: int
    def __init__(self, error_message: _Optional[int] = ...) -> None: ...

class GetClientInfoResponse(_message.Message):
    __slots__ = ("connectionInfo", "errorInfo")
    CONNECTIONINFO_FIELD_NUMBER: _ClassVar[int]
    ERRORINFO_FIELD_NUMBER: _ClassVar[int]
    connectionInfo: ClientInfo
    errorInfo: ErrorInfo
    def __init__(self, connectionInfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., errorInfo: _Optional[_Union[ErrorInfo, _Mapping]] = ...) -> None: ...
