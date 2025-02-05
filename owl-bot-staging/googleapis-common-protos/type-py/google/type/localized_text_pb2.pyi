from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LocalizedText(_message.Message):
    __slots__ = ("text", "language_code")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_CODE_FIELD_NUMBER: _ClassVar[int]
    text: str
    language_code: str
    def __init__(self, text: _Optional[str] = ..., language_code: _Optional[str] = ...) -> None: ...
