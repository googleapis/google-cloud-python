from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Context(_message.Message):
    __slots__ = ("rules",)
    RULES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[ContextRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[ContextRule, _Mapping]]] = ...) -> None: ...

class ContextRule(_message.Message):
    __slots__ = ("selector", "requested", "provided", "allowed_request_extensions", "allowed_response_extensions")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_FIELD_NUMBER: _ClassVar[int]
    PROVIDED_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_REQUEST_EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_RESPONSE_EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    selector: str
    requested: _containers.RepeatedScalarFieldContainer[str]
    provided: _containers.RepeatedScalarFieldContainer[str]
    allowed_request_extensions: _containers.RepeatedScalarFieldContainer[str]
    allowed_response_extensions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, selector: _Optional[str] = ..., requested: _Optional[_Iterable[str]] = ..., provided: _Optional[_Iterable[str]] = ..., allowed_request_extensions: _Optional[_Iterable[str]] = ..., allowed_response_extensions: _Optional[_Iterable[str]] = ...) -> None: ...
