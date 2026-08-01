from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CustomHttpPattern(_message.Message):
    __slots__ = ["kind", "path"]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    kind: str
    path: str
    def __init__(self, kind: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class Http(_message.Message):
    __slots__ = ["fully_decode_reserved_expansion", "rules"]
    FULLY_DECODE_RESERVED_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    fully_decode_reserved_expansion: bool
    rules: _containers.RepeatedCompositeFieldContainer[HttpRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[HttpRule, _Mapping]]] = ..., fully_decode_reserved_expansion: bool = ...) -> None: ...

class HttpRule(_message.Message):
    __slots__ = ["additional_bindings", "body", "custom", "delete", "get", "patch", "post", "put", "response_body", "selector"]
    ADDITIONAL_BINDINGS_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    GET_FIELD_NUMBER: _ClassVar[int]
    PATCH_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    PUT_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    additional_bindings: _containers.RepeatedCompositeFieldContainer[HttpRule]
    body: str
    custom: CustomHttpPattern
    delete: str
    get: str
    patch: str
    post: str
    put: str
    response_body: str
    selector: str
    def __init__(self, selector: _Optional[str] = ..., get: _Optional[str] = ..., put: _Optional[str] = ..., post: _Optional[str] = ..., delete: _Optional[str] = ..., patch: _Optional[str] = ..., custom: _Optional[_Union[CustomHttpPattern, _Mapping]] = ..., body: _Optional[str] = ..., response_body: _Optional[str] = ..., additional_bindings: _Optional[_Iterable[_Union[HttpRule, _Mapping]]] = ...) -> None: ...
