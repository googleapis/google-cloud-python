from google.api import annotations_pb2 as _annotations_pb2
from google.api import client_pb2 as _client_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.rpc import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
OPERATION_INFO_FIELD_NUMBER: _ClassVar[int]
operation_info: _descriptor.FieldDescriptor

class Operation(_message.Message):
    __slots__ = ("name", "metadata", "done", "error", "response")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    name: str
    metadata: _any_pb2.Any
    done: bool
    error: _status_pb2.Status
    response: _any_pb2.Any
    def __init__(self, name: _Optional[str] = ..., metadata: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., done: bool = ..., error: _Optional[_Union[_status_pb2.Status, _Mapping]] = ..., response: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class GetOperationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListOperationsRequest(_message.Message):
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

class ListOperationsResponse(_message.Message):
    __slots__ = ("operations", "next_page_token")
    OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    operations: _containers.RepeatedCompositeFieldContainer[Operation]
    next_page_token: str
    def __init__(self, operations: _Optional[_Iterable[_Union[Operation, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class CancelOperationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteOperationRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class WaitOperationRequest(_message.Message):
    __slots__ = ("name", "timeout")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    name: str
    timeout: _duration_pb2.Duration
    def __init__(self, name: _Optional[str] = ..., timeout: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class OperationInfo(_message.Message):
    __slots__ = ("response_type", "metadata_type")
    RESPONSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    response_type: str
    metadata_type: str
    def __init__(self, response_type: _Optional[str] = ..., metadata_type: _Optional[str] = ...) -> None: ...
