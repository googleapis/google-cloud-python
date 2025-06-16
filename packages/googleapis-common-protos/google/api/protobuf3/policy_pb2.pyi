from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
FIELD_POLICY_FIELD_NUMBER: ClassVar[int]
METHOD_POLICY_FIELD_NUMBER: ClassVar[int]
field_policy: _descriptor.FieldDescriptor
method_policy: _descriptor.FieldDescriptor

class FieldPolicy(_message.Message):
    __slots__ = ["resource_permission", "resource_type", "selector"]
    RESOURCE_PERMISSION_FIELD_NUMBER: ClassVar[int]
    RESOURCE_TYPE_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    resource_permission: str
    resource_type: str
    selector: str
    def __init__(self, selector: Optional[str] = ..., resource_permission: Optional[str] = ..., resource_type: Optional[str] = ...) -> None: ...

class MethodPolicy(_message.Message):
    __slots__ = ["request_policies", "selector"]
    REQUEST_POLICIES_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    request_policies: _containers.RepeatedCompositeFieldContainer[FieldPolicy]
    selector: str
    def __init__(self, selector: Optional[str] = ..., request_policies: Optional[Iterable[Union[FieldPolicy, Mapping]]] = ...) -> None: ...
