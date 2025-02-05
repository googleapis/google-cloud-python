from google.api import policy_pb2 as _policy_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Control(_message.Message):
    __slots__ = ("environment", "method_policies")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    METHOD_POLICIES_FIELD_NUMBER: _ClassVar[int]
    environment: str
    method_policies: _containers.RepeatedCompositeFieldContainer[_policy_pb2.MethodPolicy]
    def __init__(self, environment: _Optional[str] = ..., method_policies: _Optional[_Iterable[_Union[_policy_pb2.MethodPolicy, _Mapping]]] = ...) -> None: ...
