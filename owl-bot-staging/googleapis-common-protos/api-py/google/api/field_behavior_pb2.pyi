from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class FieldBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FIELD_BEHAVIOR_UNSPECIFIED: _ClassVar[FieldBehavior]
    OPTIONAL: _ClassVar[FieldBehavior]
    REQUIRED: _ClassVar[FieldBehavior]
    OUTPUT_ONLY: _ClassVar[FieldBehavior]
    INPUT_ONLY: _ClassVar[FieldBehavior]
    IMMUTABLE: _ClassVar[FieldBehavior]
    UNORDERED_LIST: _ClassVar[FieldBehavior]
    NON_EMPTY_DEFAULT: _ClassVar[FieldBehavior]
    IDENTIFIER: _ClassVar[FieldBehavior]
FIELD_BEHAVIOR_UNSPECIFIED: FieldBehavior
OPTIONAL: FieldBehavior
REQUIRED: FieldBehavior
OUTPUT_ONLY: FieldBehavior
INPUT_ONLY: FieldBehavior
IMMUTABLE: FieldBehavior
UNORDERED_LIST: FieldBehavior
NON_EMPTY_DEFAULT: FieldBehavior
IDENTIFIER: FieldBehavior
FIELD_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
field_behavior: _descriptor.FieldDescriptor
