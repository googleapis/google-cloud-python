from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

ABORTED: Code
ALREADY_EXISTS: Code
CANCELLED: Code
DATA_LOSS: Code
DEADLINE_EXCEEDED: Code
DESCRIPTOR: _descriptor.FileDescriptor
FAILED_PRECONDITION: Code
INTERNAL: Code
INVALID_ARGUMENT: Code
NOT_FOUND: Code
OK: Code
OUT_OF_RANGE: Code
PERMISSION_DENIED: Code
RESOURCE_EXHAUSTED: Code
UNAUTHENTICATED: Code
UNAVAILABLE: Code
UNIMPLEMENTED: Code
UNKNOWN: Code

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
