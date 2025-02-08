from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OK: _ClassVar[Code]
    CANCELLED: _ClassVar[Code]
    UNKNOWN: _ClassVar[Code]
    INVALID_ARGUMENT: _ClassVar[Code]
    DEADLINE_EXCEEDED: _ClassVar[Code]
    NOT_FOUND: _ClassVar[Code]
    ALREADY_EXISTS: _ClassVar[Code]
    PERMISSION_DENIED: _ClassVar[Code]
    UNAUTHENTICATED: _ClassVar[Code]
    RESOURCE_EXHAUSTED: _ClassVar[Code]
    FAILED_PRECONDITION: _ClassVar[Code]
    ABORTED: _ClassVar[Code]
    OUT_OF_RANGE: _ClassVar[Code]
    UNIMPLEMENTED: _ClassVar[Code]
    INTERNAL: _ClassVar[Code]
    UNAVAILABLE: _ClassVar[Code]
    DATA_LOSS: _ClassVar[Code]
OK: Code
CANCELLED: Code
UNKNOWN: Code
INVALID_ARGUMENT: Code
DEADLINE_EXCEEDED: Code
NOT_FOUND: Code
ALREADY_EXISTS: Code
PERMISSION_DENIED: Code
UNAUTHENTICATED: Code
RESOURCE_EXHAUSTED: Code
FAILED_PRECONDITION: Code
ABORTED: Code
OUT_OF_RANGE: Code
UNIMPLEMENTED: Code
INTERNAL: Code
UNAVAILABLE: Code
DATA_LOSS: Code
