from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TimeOfDay(_message.Message):
    __slots__ = ("hours", "minutes", "seconds", "nanos")
    HOURS_FIELD_NUMBER: _ClassVar[int]
    MINUTES_FIELD_NUMBER: _ClassVar[int]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    hours: int
    minutes: int
    seconds: int
    nanos: int
    def __init__(self, hours: _Optional[int] = ..., minutes: _Optional[int] = ..., seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
