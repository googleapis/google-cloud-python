from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetPolicyOptions(_message.Message):
    __slots__ = ("requested_policy_version",)
    REQUESTED_POLICY_VERSION_FIELD_NUMBER: _ClassVar[int]
    requested_policy_version: int
    def __init__(self, requested_policy_version: _Optional[int] = ...) -> None: ...
