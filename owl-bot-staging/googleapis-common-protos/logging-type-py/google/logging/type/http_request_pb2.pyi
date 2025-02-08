from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HttpRequest(_message.Message):
    __slots__ = ("request_method", "request_url", "request_size", "status", "response_size", "user_agent", "remote_ip", "server_ip", "referer", "latency", "cache_lookup", "cache_hit", "cache_validated_with_origin_server", "cache_fill_bytes", "protocol")
    REQUEST_METHOD_FIELD_NUMBER: _ClassVar[int]
    REQUEST_URL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_SIZE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    REMOTE_IP_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_FIELD_NUMBER: _ClassVar[int]
    REFERER_FIELD_NUMBER: _ClassVar[int]
    LATENCY_FIELD_NUMBER: _ClassVar[int]
    CACHE_LOOKUP_FIELD_NUMBER: _ClassVar[int]
    CACHE_HIT_FIELD_NUMBER: _ClassVar[int]
    CACHE_VALIDATED_WITH_ORIGIN_SERVER_FIELD_NUMBER: _ClassVar[int]
    CACHE_FILL_BYTES_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    request_method: str
    request_url: str
    request_size: int
    status: int
    response_size: int
    user_agent: str
    remote_ip: str
    server_ip: str
    referer: str
    latency: _duration_pb2.Duration
    cache_lookup: bool
    cache_hit: bool
    cache_validated_with_origin_server: bool
    cache_fill_bytes: int
    protocol: str
    def __init__(self, request_method: _Optional[str] = ..., request_url: _Optional[str] = ..., request_size: _Optional[int] = ..., status: _Optional[int] = ..., response_size: _Optional[int] = ..., user_agent: _Optional[str] = ..., remote_ip: _Optional[str] = ..., server_ip: _Optional[str] = ..., referer: _Optional[str] = ..., latency: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., cache_lookup: bool = ..., cache_hit: bool = ..., cache_validated_with_origin_server: bool = ..., cache_fill_bytes: _Optional[int] = ..., protocol: _Optional[str] = ...) -> None: ...
