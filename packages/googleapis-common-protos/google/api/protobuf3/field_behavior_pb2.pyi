from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar

DESCRIPTOR: _descriptor.FileDescriptor
FIELD_BEHAVIOR_FIELD_NUMBER: ClassVar[int]
FIELD_BEHAVIOR_UNSPECIFIED: FieldBehavior
IDENTIFIER: FieldBehavior
IMMUTABLE: FieldBehavior
INPUT_ONLY: FieldBehavior
NON_EMPTY_DEFAULT: FieldBehavior
OPTIONAL: FieldBehavior
OUTPUT_ONLY: FieldBehavior
REQUIRED: FieldBehavior
UNORDERED_LIST: FieldBehavior
field_behavior: _descriptor.FieldDescriptor

class FieldBehavior(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
