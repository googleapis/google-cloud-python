from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class LogSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEFAULT: _ClassVar[LogSeverity]
    DEBUG: _ClassVar[LogSeverity]
    INFO: _ClassVar[LogSeverity]
    NOTICE: _ClassVar[LogSeverity]
    WARNING: _ClassVar[LogSeverity]
    ERROR: _ClassVar[LogSeverity]
    CRITICAL: _ClassVar[LogSeverity]
    ALERT: _ClassVar[LogSeverity]
    EMERGENCY: _ClassVar[LogSeverity]
DEFAULT: LogSeverity
DEBUG: LogSeverity
INFO: LogSeverity
NOTICE: LogSeverity
WARNING: LogSeverity
ERROR: LogSeverity
CRITICAL: LogSeverity
ALERT: LogSeverity
EMERGENCY: LogSeverity
