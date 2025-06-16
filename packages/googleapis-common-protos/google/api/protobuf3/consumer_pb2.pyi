from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectProperties(_message.Message):
    __slots__ = ["properties"]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    properties: _containers.RepeatedCompositeFieldContainer[Property]
    def __init__(self, properties: Optional[Iterable[Union[Property, Mapping]]] = ...) -> None: ...

class Property(_message.Message):
    __slots__ = ["description", "name", "type"]
    class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOOL: Property.PropertyType
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    DOUBLE: Property.PropertyType
    INT64: Property.PropertyType
    NAME_FIELD_NUMBER: ClassVar[int]
    STRING: Property.PropertyType
    TYPE_FIELD_NUMBER: ClassVar[int]
    UNSPECIFIED: Property.PropertyType
    description: str
    name: str
    type: Property.PropertyType
    def __init__(self, name: Optional[str] = ..., type: Optional[Union[Property.PropertyType, str]] = ..., description: Optional[str] = ...) -> None: ...
