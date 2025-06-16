from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
FIELD_INFO_FIELD_NUMBER: _ClassVar[int]
field_info: _descriptor.FieldDescriptor

class FieldInfo(_message.Message):
    __slots__ = ("format", "referenced_types")
    class Format(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FORMAT_UNSPECIFIED: _ClassVar[FieldInfo.Format]
        UUID4: _ClassVar[FieldInfo.Format]
        IPV4: _ClassVar[FieldInfo.Format]
        IPV6: _ClassVar[FieldInfo.Format]
        IPV4_OR_IPV6: _ClassVar[FieldInfo.Format]
    FORMAT_UNSPECIFIED: FieldInfo.Format
    UUID4: FieldInfo.Format
    IPV4: FieldInfo.Format
    IPV6: FieldInfo.Format
    IPV4_OR_IPV6: FieldInfo.Format
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    REFERENCED_TYPES_FIELD_NUMBER: _ClassVar[int]
    format: FieldInfo.Format
    referenced_types: _containers.RepeatedCompositeFieldContainer[TypeReference]
    def __init__(self, format: _Optional[_Union[FieldInfo.Format, str]] = ..., referenced_types: _Optional[_Iterable[_Union[TypeReference, _Mapping]]] = ...) -> None: ...

class TypeReference(_message.Message):
    __slots__ = ("type_name",)
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_name: str
    def __init__(self, type_name: _Optional[str] = ...) -> None: ...
