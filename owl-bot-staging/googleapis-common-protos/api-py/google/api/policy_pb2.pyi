from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
FIELD_POLICY_FIELD_NUMBER: _ClassVar[int]
field_policy: _descriptor.FieldDescriptor
METHOD_POLICY_FIELD_NUMBER: _ClassVar[int]
method_policy: _descriptor.FieldDescriptor

class FieldPolicy(_message.Message):
    __slots__ = ("selector", "resource_permission", "resource_type")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    selector: str
    resource_permission: str
    resource_type: str
    def __init__(self, selector: _Optional[str] = ..., resource_permission: _Optional[str] = ..., resource_type: _Optional[str] = ...) -> None: ...

class MethodPolicy(_message.Message):
    __slots__ = ("selector", "request_policies")
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    REQUEST_POLICIES_FIELD_NUMBER: _ClassVar[int]
    selector: str
    request_policies: _containers.RepeatedCompositeFieldContainer[FieldPolicy]
    def __init__(self, selector: _Optional[str] = ..., request_policies: _Optional[_Iterable[_Union[FieldPolicy, _Mapping]]] = ...) -> None: ...
