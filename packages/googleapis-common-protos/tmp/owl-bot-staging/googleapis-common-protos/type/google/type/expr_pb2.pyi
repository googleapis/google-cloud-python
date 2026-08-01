from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Expr(_message.Message):
    __slots__ = ["description", "expression", "location", "title"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    description: str
    expression: str
    location: str
    title: str
    def __init__(self, expression: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...
