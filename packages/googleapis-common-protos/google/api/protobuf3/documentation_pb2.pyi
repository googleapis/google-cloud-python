from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Documentation(_message.Message):
    __slots__ = ["documentation_root_url", "overview", "pages", "rules", "service_root_url", "summary"]
    DOCUMENTATION_ROOT_URL_FIELD_NUMBER: ClassVar[int]
    OVERVIEW_FIELD_NUMBER: ClassVar[int]
    PAGES_FIELD_NUMBER: ClassVar[int]
    RULES_FIELD_NUMBER: ClassVar[int]
    SERVICE_ROOT_URL_FIELD_NUMBER: ClassVar[int]
    SUMMARY_FIELD_NUMBER: ClassVar[int]
    documentation_root_url: str
    overview: str
    pages: _containers.RepeatedCompositeFieldContainer[Page]
    rules: _containers.RepeatedCompositeFieldContainer[DocumentationRule]
    service_root_url: str
    summary: str
    def __init__(self, summary: Optional[str] = ..., pages: Optional[Iterable[Union[Page, Mapping]]] = ..., rules: Optional[Iterable[Union[DocumentationRule, Mapping]]] = ..., documentation_root_url: Optional[str] = ..., service_root_url: Optional[str] = ..., overview: Optional[str] = ...) -> None: ...

class DocumentationRule(_message.Message):
    __slots__ = ["deprecation_description", "description", "selector"]
    DEPRECATION_DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    deprecation_description: str
    description: str
    selector: str
    def __init__(self, selector: Optional[str] = ..., description: Optional[str] = ..., deprecation_description: Optional[str] = ...) -> None: ...

class Page(_message.Message):
    __slots__ = ["content", "name", "subpages"]
    CONTENT_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    SUBPAGES_FIELD_NUMBER: ClassVar[int]
    content: str
    name: str
    subpages: _containers.RepeatedCompositeFieldContainer[Page]
    def __init__(self, name: Optional[str] = ..., content: Optional[str] = ..., subpages: Optional[Iterable[Union[Page, Mapping]]] = ...) -> None: ...
