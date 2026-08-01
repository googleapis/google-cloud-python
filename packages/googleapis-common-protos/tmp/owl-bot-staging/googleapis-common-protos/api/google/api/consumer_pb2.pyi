from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectProperties(_message.Message):
    __slots__ = ["properties"]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    properties: _containers.RepeatedCompositeFieldContainer[Property]
    def __init__(self, properties: _Optional[_Iterable[_Union[Property, _Mapping]]] = ...) -> None: ...

class Property(_message.Message):
    __slots__ = ["description", "name", "type"]
    class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOOL: Property.PropertyType
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DOUBLE: Property.PropertyType
    INT64: Property.PropertyType
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRING: Property.PropertyType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNSPECIFIED: Property.PropertyType
    description: str
    name: str
    type: Property.PropertyType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[Property.PropertyType, str]] = ..., description: _Optional[str] = ...) -> None: ...
