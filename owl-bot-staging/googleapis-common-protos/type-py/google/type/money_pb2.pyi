from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Money(_message.Message):
    __slots__ = ("currency_code", "units", "nanos")
    CURRENCY_CODE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    currency_code: str
    units: int
    nanos: int
    def __init__(self, currency_code: _Optional[str] = ..., units: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
