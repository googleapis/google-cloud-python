from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Backend(_message.Message):
    __slots__ = ["rules"]
    RULES_FIELD_NUMBER: ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[BackendRule]
    def __init__(self, rules: Optional[Iterable[Union[BackendRule, Mapping]]] = ...) -> None: ...

class BackendRule(_message.Message):
    __slots__ = ["address", "deadline", "disable_auth", "jwt_audience", "min_deadline", "operation_deadline", "overrides_by_request_protocol", "path_translation", "protocol", "selector"]
    class PathTranslation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class OverridesByRequestProtocolEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: BackendRule
        def __init__(self, key: Optional[str] = ..., value: Optional[Union[BackendRule, Mapping]] = ...) -> None: ...
    ADDRESS_FIELD_NUMBER: ClassVar[int]
    APPEND_PATH_TO_ADDRESS: BackendRule.PathTranslation
    CONSTANT_ADDRESS: BackendRule.PathTranslation
    DEADLINE_FIELD_NUMBER: ClassVar[int]
    DISABLE_AUTH_FIELD_NUMBER: ClassVar[int]
    JWT_AUDIENCE_FIELD_NUMBER: ClassVar[int]
    MIN_DEADLINE_FIELD_NUMBER: ClassVar[int]
    OPERATION_DEADLINE_FIELD_NUMBER: ClassVar[int]
    OVERRIDES_BY_REQUEST_PROTOCOL_FIELD_NUMBER: ClassVar[int]
    PATH_TRANSLATION_FIELD_NUMBER: ClassVar[int]
    PATH_TRANSLATION_UNSPECIFIED: BackendRule.PathTranslation
    PROTOCOL_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    address: str
    deadline: float
    disable_auth: bool
    jwt_audience: str
    min_deadline: float
    operation_deadline: float
    overrides_by_request_protocol: _containers.MessageMap[str, BackendRule]
    path_translation: BackendRule.PathTranslation
    protocol: str
    selector: str
    def __init__(self, selector: Optional[str] = ..., address: Optional[str] = ..., deadline: Optional[float] = ..., min_deadline: Optional[float] = ..., operation_deadline: Optional[float] = ..., path_translation: Optional[Union[BackendRule.PathTranslation, str]] = ..., jwt_audience: Optional[str] = ..., disable_auth: bool = ..., protocol: Optional[str] = ..., overrides_by_request_protocol: Optional[Mapping[str, BackendRule]] = ...) -> None: ...
