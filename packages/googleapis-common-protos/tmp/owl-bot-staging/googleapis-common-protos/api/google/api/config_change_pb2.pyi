from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ADDED: ChangeType
CHANGE_TYPE_UNSPECIFIED: ChangeType
DESCRIPTOR: _descriptor.FileDescriptor
MODIFIED: ChangeType
REMOVED: ChangeType

class Advice(_message.Message):
    __slots__ = ["description"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: str
    def __init__(self, description: _Optional[str] = ...) -> None: ...

class ConfigChange(_message.Message):
    __slots__ = ["advices", "change_type", "element", "new_value", "old_value"]
    ADVICES_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_FIELD_NUMBER: _ClassVar[int]
    NEW_VALUE_FIELD_NUMBER: _ClassVar[int]
    OLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    advices: _containers.RepeatedCompositeFieldContainer[Advice]
    change_type: ChangeType
    element: str
    new_value: str
    old_value: str
    def __init__(self, element: _Optional[str] = ..., old_value: _Optional[str] = ..., new_value: _Optional[str] = ..., change_type: _Optional[_Union[ChangeType, str]] = ..., advices: _Optional[_Iterable[_Union[Advice, _Mapping]]] = ...) -> None: ...

class ChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
