from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SourceInfo(_message.Message):
    __slots__ = ("source_files",)
    SOURCE_FILES_FIELD_NUMBER: _ClassVar[int]
    source_files: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    def __init__(self, source_files: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...
