from google.iam.v1 import policy_pb2 as _policy_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuditData(_message.Message):
    __slots__ = ("policy_delta",)
    POLICY_DELTA_FIELD_NUMBER: _ClassVar[int]
    policy_delta: _policy_pb2.PolicyDelta
    def __init__(self, policy_delta: _Optional[_Union[_policy_pb2.PolicyDelta, _Mapping]] = ...) -> None: ...
