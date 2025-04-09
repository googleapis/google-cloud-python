from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Endpoint(_message.Message):
    __slots__ = ("name", "aliases", "target", "allow_cors")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ALLOW_CORS_FIELD_NUMBER: _ClassVar[int]
    name: str
    aliases: _containers.RepeatedScalarFieldContainer[str]
    target: str
    allow_cors: bool
    def __init__(self, name: _Optional[str] = ..., aliases: _Optional[_Iterable[str]] = ..., target: _Optional[str] = ..., allow_cors: bool = ...) -> None: ...
