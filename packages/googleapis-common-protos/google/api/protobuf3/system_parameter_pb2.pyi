from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class SystemParameter(_message.Message):
    __slots__ = ["http_header", "name", "url_query_parameter"]
    HTTP_HEADER_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    URL_QUERY_PARAMETER_FIELD_NUMBER: ClassVar[int]
    http_header: str
    name: str
    url_query_parameter: str
    def __init__(self, name: Optional[str] = ..., http_header: Optional[str] = ..., url_query_parameter: Optional[str] = ...) -> None: ...

class SystemParameterRule(_message.Message):
    __slots__ = ["parameters", "selector"]
    PARAMETERS_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[SystemParameter]
    selector: str
    def __init__(self, selector: Optional[str] = ..., parameters: Optional[Iterable[Union[SystemParameter, Mapping]]] = ...) -> None: ...

class SystemParameters(_message.Message):
    __slots__ = ["rules"]
    RULES_FIELD_NUMBER: ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[SystemParameterRule]
    def __init__(self, rules: Optional[Iterable[Union[SystemParameterRule, Mapping]]] = ...) -> None: ...
