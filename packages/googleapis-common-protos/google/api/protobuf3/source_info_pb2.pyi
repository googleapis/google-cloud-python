from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class SourceInfo(_message.Message):
    __slots__ = ["source_files"]
    SOURCE_FILES_FIELD_NUMBER: ClassVar[int]
    source_files: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, source_files: Optional[Iterable[Union[_any_pb2.Any, Mapping]]] = ...) -> None: ...
