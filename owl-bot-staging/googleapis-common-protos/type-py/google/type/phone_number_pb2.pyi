from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PhoneNumber(_message.Message):
    __slots__ = ("e164_number", "short_code", "extension")
    class ShortCode(_message.Message):
        __slots__ = ("region_code", "number")
        REGION_CODE_FIELD_NUMBER: _ClassVar[int]
        NUMBER_FIELD_NUMBER: _ClassVar[int]
        region_code: str
        number: str
        def __init__(self, region_code: _Optional[str] = ..., number: _Optional[str] = ...) -> None: ...
    E164_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SHORT_CODE_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    e164_number: str
    short_code: PhoneNumber.ShortCode
    extension: str
    def __init__(self, e164_number: _Optional[str] = ..., short_code: _Optional[_Union[PhoneNumber.ShortCode, _Mapping]] = ..., extension: _Optional[str] = ...) -> None: ...
