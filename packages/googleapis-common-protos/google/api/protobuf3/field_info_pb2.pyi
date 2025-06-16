from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
FIELD_INFO_FIELD_NUMBER: ClassVar[int]
field_info: _descriptor.FieldDescriptor

class FieldInfo(_message.Message):
    __slots__ = ["format", "referenced_types"]
    class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FORMAT_FIELD_NUMBER: ClassVar[int]
    FORMAT_UNSPECIFIED: FieldInfo.Format
    IPV4: FieldInfo.Format
    IPV4_OR_IPV6: FieldInfo.Format
    IPV6: FieldInfo.Format
    REFERENCED_TYPES_FIELD_NUMBER: ClassVar[int]
    UUID4: FieldInfo.Format
    format: FieldInfo.Format
    referenced_types: _containers.RepeatedCompositeFieldContainer[TypeReference]
    def __init__(self, format: Optional[Union[FieldInfo.Format, str]] = ..., referenced_types: Optional[Iterable[Union[TypeReference, Mapping]]] = ...) -> None: ...

class TypeReference(_message.Message):
    __slots__ = ["type_name"]
    TYPE_NAME_FIELD_NUMBER: ClassVar[int]
    type_name: str
    def __init__(self, type_name: Optional[str] = ...) -> None: ...
