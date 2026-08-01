from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HttpRequest(_message.Message):
    __slots__ = ["cache_fill_bytes", "cache_hit", "cache_lookup", "cache_validated_with_origin_server", "latency", "protocol", "referer", "remote_ip", "request_method", "request_size", "request_url", "response_size", "server_ip", "status", "user_agent"]
    CACHE_FILL_BYTES_FIELD_NUMBER: _ClassVar[int]
    CACHE_HIT_FIELD_NUMBER: _ClassVar[int]
    CACHE_LOOKUP_FIELD_NUMBER: _ClassVar[int]
    CACHE_VALIDATED_WITH_ORIGIN_SERVER_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    REFERER_FIELD_NUMBER: _ClassVar[int]
    REMOTE_IP_FIELD_NUMBER: _ClassVar[int]
    REQUEST_METHOD_FIELD_NUMBER: _ClassVar[int]
    REQUEST_SIZE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_URL_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    cache_fill_bytes: int
    cache_hit: bool
    cache_lookup: bool
    cache_validated_with_origin_server: bool
    latency: _duration_pb2.Duration
    protocol: str
    referer: str
    remote_ip: str
    request_method: str
    request_size: int
    request_url: str
    response_size: int
    server_ip: str
    status: int
    user_agent: str
    def __init__(self, request_method: _Optional[str] = ..., request_url: _Optional[str] = ..., request_size: _Optional[int] = ..., status: _Optional[int] = ..., response_size: _Optional[int] = ..., user_agent: _Optional[str] = ..., remote_ip: _Optional[str] = ..., server_ip: _Optional[str] = ..., referer: _Optional[str] = ..., latency: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., cache_lookup: bool = ..., cache_hit: bool = ..., cache_validated_with_origin_server: bool = ..., cache_fill_bytes: _Optional[int] = ..., protocol: _Optional[str] = ...) -> None: ...
