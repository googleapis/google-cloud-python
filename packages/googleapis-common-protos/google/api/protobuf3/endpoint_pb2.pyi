from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Endpoint(_message.Message):
    __slots__ = ["aliases", "allow_cors", "name", "target"]
    ALIASES_FIELD_NUMBER: ClassVar[int]
    ALLOW_CORS_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TARGET_FIELD_NUMBER: ClassVar[int]
    aliases: _containers.RepeatedScalarFieldContainer[str]
    allow_cors: bool
    name: str
    target: str
    def __init__(self, name: Optional[str] = ..., aliases: Optional[Iterable[str]] = ..., target: Optional[str] = ..., allow_cors: bool = ...) -> None: ...
