from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PhoneNumber(_message.Message):
    __slots__ = ["e164_number", "extension", "short_code"]
    class ShortCode(_message.Message):
        __slots__ = ["number", "region_code"]
        NUMBER_FIELD_NUMBER: _ClassVar[int]
        REGION_CODE_FIELD_NUMBER: _ClassVar[int]
        number: str
        region_code: str
        def __init__(self, region_code: _Optional[str] = ..., number: _Optional[str] = ...) -> None: ...
    E164_NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    SHORT_CODE_FIELD_NUMBER: _ClassVar[int]
    e164_number: str
    extension: str
    short_code: PhoneNumber.ShortCode
    def __init__(self, e164_number: _Optional[str] = ..., short_code: _Optional[_Union[PhoneNumber.ShortCode, _Mapping]] = ..., extension: _Optional[str] = ...) -> None: ...
