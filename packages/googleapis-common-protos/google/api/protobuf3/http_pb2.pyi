from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class CustomHttpPattern(_message.Message):
    __slots__ = ["kind", "path"]
    KIND_FIELD_NUMBER: ClassVar[int]
    PATH_FIELD_NUMBER: ClassVar[int]
    kind: str
    path: str
    def __init__(self, kind: Optional[str] = ..., path: Optional[str] = ...) -> None: ...

class Http(_message.Message):
    __slots__ = ["fully_decode_reserved_expansion", "rules"]
    FULLY_DECODE_RESERVED_EXPANSION_FIELD_NUMBER: ClassVar[int]
    RULES_FIELD_NUMBER: ClassVar[int]
    fully_decode_reserved_expansion: bool
    rules: _containers.RepeatedCompositeFieldContainer[HttpRule]
    def __init__(self, rules: Optional[Iterable[Union[HttpRule, Mapping]]] = ..., fully_decode_reserved_expansion: bool = ...) -> None: ...

class HttpRule(_message.Message):
    __slots__ = ["additional_bindings", "body", "custom", "delete", "get", "patch", "post", "put", "response_body", "selector"]
    ADDITIONAL_BINDINGS_FIELD_NUMBER: ClassVar[int]
    BODY_FIELD_NUMBER: ClassVar[int]
    CUSTOM_FIELD_NUMBER: ClassVar[int]
    DELETE_FIELD_NUMBER: ClassVar[int]
    GET_FIELD_NUMBER: ClassVar[int]
    PATCH_FIELD_NUMBER: ClassVar[int]
    POST_FIELD_NUMBER: ClassVar[int]
    PUT_FIELD_NUMBER: ClassVar[int]
    RESPONSE_BODY_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
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
    def __init__(self, selector: Optional[str] = ..., get: Optional[str] = ..., put: Optional[str] = ..., post: Optional[str] = ..., delete: Optional[str] = ..., patch: Optional[str] = ..., custom: Optional[Union[CustomHttpPattern, Mapping]] = ..., body: Optional[str] = ..., response_body: Optional[str] = ..., additional_bindings: Optional[Iterable[Union[HttpRule, Mapping]]] = ...) -> None: ...
