from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SystemParameters(_message.Message):
    __slots__ = ("rules",)
    RULES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[SystemParameterRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[SystemParameterRule, _Mapping]]] = ...) -> None: ...

class SystemParameterRule(_message.Message):
    __slots__ = ("selector", "parameters")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    selector: str
    parameters: _containers.RepeatedCompositeFieldContainer[SystemParameter]
    def __init__(self, selector: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[SystemParameter, _Mapping]]] = ...) -> None: ...

class SystemParameter(_message.Message):
    __slots__ = ("name", "http_header", "url_query_parameter")
    NAME_FIELD_NUMBER: _ClassVar[int]
    HTTP_HEADER_FIELD_NUMBER: _ClassVar[int]
    URL_QUERY_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    name: str
    http_header: str
    url_query_parameter: str
    def __init__(self, name: _Optional[str] = ..., http_header: _Optional[str] = ..., url_query_parameter: _Optional[str] = ...) -> None: ...
