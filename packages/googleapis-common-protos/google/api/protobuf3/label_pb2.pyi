from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class LabelDescriptor(_message.Message):
    __slots__ = ["description", "key", "value_type"]
    class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BOOL: LabelDescriptor.ValueType
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    INT64: LabelDescriptor.ValueType
    KEY_FIELD_NUMBER: ClassVar[int]
    STRING: LabelDescriptor.ValueType
    VALUE_TYPE_FIELD_NUMBER: ClassVar[int]
    description: str
    key: str
    value_type: LabelDescriptor.ValueType
    def __init__(self, key: Optional[str] = ..., value_type: Optional[Union[LabelDescriptor.ValueType, str]] = ..., description: Optional[str] = ...) -> None: ...
