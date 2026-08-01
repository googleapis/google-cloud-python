from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Documentation(_message.Message):
    __slots__ = ["documentation_root_url", "overview", "pages", "rules", "service_root_url", "summary"]
    DOCUMENTATION_ROOT_URL_FIELD_NUMBER: _ClassVar[int]
    OVERVIEW_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ROOT_URL_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    documentation_root_url: str
    overview: str
    pages: _containers.RepeatedCompositeFieldContainer[Page]
    rules: _containers.RepeatedCompositeFieldContainer[DocumentationRule]
    service_root_url: str
    summary: str
    def __init__(self, summary: _Optional[str] = ..., pages: _Optional[_Iterable[_Union[Page, _Mapping]]] = ..., rules: _Optional[_Iterable[_Union[DocumentationRule, _Mapping]]] = ..., documentation_root_url: _Optional[str] = ..., service_root_url: _Optional[str] = ..., overview: _Optional[str] = ...) -> None: ...

class DocumentationRule(_message.Message):
    __slots__ = ["deprecation_description", "description", "selector"]
    DEPRECATION_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    deprecation_description: str
    description: str
    selector: str
    def __init__(self, selector: _Optional[str] = ..., description: _Optional[str] = ..., deprecation_description: _Optional[str] = ...) -> None: ...

class Page(_message.Message):
    __slots__ = ["content", "name", "subpages"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUBPAGES_FIELD_NUMBER: _ClassVar[int]
    content: str
    name: str
    subpages: _containers.RepeatedCompositeFieldContainer[Page]
    def __init__(self, name: _Optional[str] = ..., content: _Optional[str] = ..., subpages: _Optional[_Iterable[_Union[Page, _Mapping]]] = ...) -> None: ...
