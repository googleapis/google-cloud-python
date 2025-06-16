from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Context(_message.Message):
    __slots__ = ["rules"]
    RULES_FIELD_NUMBER: ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[ContextRule]
    def __init__(self, rules: Optional[Iterable[Union[ContextRule, Mapping]]] = ...) -> None: ...

class ContextRule(_message.Message):
    __slots__ = ["allowed_request_extensions", "allowed_response_extensions", "provided", "requested", "selector"]
    ALLOWED_REQUEST_EXTENSIONS_FIELD_NUMBER: ClassVar[int]
    ALLOWED_RESPONSE_EXTENSIONS_FIELD_NUMBER: ClassVar[int]
    PROVIDED_FIELD_NUMBER: ClassVar[int]
    REQUESTED_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    allowed_request_extensions: _containers.RepeatedScalarFieldContainer[str]
    allowed_response_extensions: _containers.RepeatedScalarFieldContainer[str]
    provided: _containers.RepeatedScalarFieldContainer[str]
    requested: _containers.RepeatedScalarFieldContainer[str]
    selector: str
    def __init__(self, selector: Optional[str] = ..., requested: Optional[Iterable[str]] = ..., provided: Optional[Iterable[str]] = ..., allowed_request_extensions: Optional[Iterable[str]] = ..., allowed_response_extensions: Optional[Iterable[str]] = ...) -> None: ...
