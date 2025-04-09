from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LabelDescriptor(_message.Message):
    __slots__ = ("key", "value_type", "description")
    class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STRING: _ClassVar[LabelDescriptor.ValueType]
        BOOL: _ClassVar[LabelDescriptor.ValueType]
        INT64: _ClassVar[LabelDescriptor.ValueType]
    STRING: LabelDescriptor.ValueType
    BOOL: LabelDescriptor.ValueType
    INT64: LabelDescriptor.ValueType
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    key: str
    value_type: LabelDescriptor.ValueType
    description: str
    def __init__(self, key: _Optional[str] = ..., value_type: _Optional[_Union[LabelDescriptor.ValueType, str]] = ..., description: _Optional[str] = ...) -> None: ...
