from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class HttpBody(_message.Message):
    __slots__ = ["content_type", "data", "extensions"]
    CONTENT_TYPE_FIELD_NUMBER: ClassVar[int]
    DATA_FIELD_NUMBER: ClassVar[int]
    EXTENSIONS_FIELD_NUMBER: ClassVar[int]
    content_type: str
    data: bytes
    extensions: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, content_type: Optional[str] = ..., data: Optional[bytes] = ..., extensions: Optional[Iterable[Union[_any_pb2.Any, Mapping]]] = ...) -> None: ...
