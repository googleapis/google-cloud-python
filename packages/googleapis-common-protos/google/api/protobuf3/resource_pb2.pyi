from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
RESOURCE_DEFINITION_FIELD_NUMBER: ClassVar[int]
RESOURCE_FIELD_NUMBER: ClassVar[int]
RESOURCE_REFERENCE_FIELD_NUMBER: ClassVar[int]
resource: _descriptor.FieldDescriptor
resource_definition: _descriptor.FieldDescriptor
resource_reference: _descriptor.FieldDescriptor

class ResourceDescriptor(_message.Message):
    __slots__ = ["history", "name_field", "pattern", "plural", "singular", "style", "type"]
    class History(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Style(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DECLARATIVE_FRIENDLY: ResourceDescriptor.Style
    FUTURE_MULTI_PATTERN: ResourceDescriptor.History
    HISTORY_FIELD_NUMBER: ClassVar[int]
    HISTORY_UNSPECIFIED: ResourceDescriptor.History
    NAME_FIELD_FIELD_NUMBER: ClassVar[int]
    ORIGINALLY_SINGLE_PATTERN: ResourceDescriptor.History
    PATTERN_FIELD_NUMBER: ClassVar[int]
    PLURAL_FIELD_NUMBER: ClassVar[int]
    SINGULAR_FIELD_NUMBER: ClassVar[int]
    STYLE_FIELD_NUMBER: ClassVar[int]
    STYLE_UNSPECIFIED: ResourceDescriptor.Style
    TYPE_FIELD_NUMBER: ClassVar[int]
    history: ResourceDescriptor.History
    name_field: str
    pattern: _containers.RepeatedScalarFieldContainer[str]
    plural: str
    singular: str
    style: _containers.RepeatedScalarFieldContainer[ResourceDescriptor.Style]
    type: str
    def __init__(self, type: Optional[str] = ..., pattern: Optional[Iterable[str]] = ..., name_field: Optional[str] = ..., history: Optional[Union[ResourceDescriptor.History, str]] = ..., plural: Optional[str] = ..., singular: Optional[str] = ..., style: Optional[Iterable[Union[ResourceDescriptor.Style, str]]] = ...) -> None: ...

class ResourceReference(_message.Message):
    __slots__ = ["child_type", "type"]
    CHILD_TYPE_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    child_type: str
    type: str
    def __init__(self, type: Optional[str] = ..., child_type: Optional[str] = ...) -> None: ...
