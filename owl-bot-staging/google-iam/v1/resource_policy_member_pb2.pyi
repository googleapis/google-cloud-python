from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResourcePolicyMember(_message.Message):
    __slots__ = ("iam_policy_name_principal", "iam_policy_uid_principal")
    IAM_POLICY_NAME_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    IAM_POLICY_UID_PRINCIPAL_FIELD_NUMBER: _ClassVar[int]
    iam_policy_name_principal: str
    iam_policy_uid_principal: str
    def __init__(self, iam_policy_name_principal: _Optional[str] = ..., iam_policy_uid_principal: _Optional[str] = ...) -> None: ...
