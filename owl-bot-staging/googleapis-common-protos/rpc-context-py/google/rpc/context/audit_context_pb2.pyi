from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditContext(_message.Message):
    __slots__ = ("audit_log", "scrubbed_request", "scrubbed_response", "scrubbed_response_item_count", "target_resource")
    AUDIT_LOG_FIELD_NUMBER: _ClassVar[int]
    SCRUBBED_REQUEST_FIELD_NUMBER: _ClassVar[int]
    SCRUBBED_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SCRUBBED_RESPONSE_ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    TARGET_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    audit_log: bytes
    scrubbed_request: _struct_pb2.Struct
    scrubbed_response: _struct_pb2.Struct
    scrubbed_response_item_count: int
    target_resource: str
    def __init__(self, audit_log: _Optional[bytes] = ..., scrubbed_request: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., scrubbed_response: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., scrubbed_response_item_count: _Optional[int] = ..., target_resource: _Optional[str] = ...) -> None: ...
