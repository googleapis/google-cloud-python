from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

ALERT: LogSeverity
CRITICAL: LogSeverity
DEBUG: LogSeverity
DEFAULT: LogSeverity
DESCRIPTOR: _descriptor.FileDescriptor
EMERGENCY: LogSeverity
ERROR: LogSeverity
INFO: LogSeverity
NOTICE: LogSeverity
WARNING: LogSeverity

class LogSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
