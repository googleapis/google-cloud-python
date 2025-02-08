from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.api import client_pb2 as _client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListLocationsRequest(_message.Message):
    __slots__ = ("name", "filter", "page_size", "page_token")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    name: str
    filter: str
    page_size: int
    page_token: str
    def __init__(self, name: _Optional[str] = ..., filter: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListLocationsResponse(_message.Message):
    __slots__ = ("locations", "next_page_token")
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    locations: _containers.RepeatedCompositeFieldContainer[Location]
    next_page_token: str
    def __init__(self, locations: _Optional[_Iterable[_Union[Location, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetLocationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ("name", "location_id", "display_name", "labels", "metadata")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    location_id: str
    display_name: str
    labels: _containers.ScalarMap[str, str]
    metadata: _any_pb2.Any
    def __init__(self, name: _Optional[str] = ..., location_id: _Optional[str] = ..., display_name: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., metadata: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
