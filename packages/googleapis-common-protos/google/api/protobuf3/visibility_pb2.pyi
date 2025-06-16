from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

API_VISIBILITY_FIELD_NUMBER: ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
ENUM_VISIBILITY_FIELD_NUMBER: ClassVar[int]
FIELD_VISIBILITY_FIELD_NUMBER: ClassVar[int]
MESSAGE_VISIBILITY_FIELD_NUMBER: ClassVar[int]
METHOD_VISIBILITY_FIELD_NUMBER: ClassVar[int]
VALUE_VISIBILITY_FIELD_NUMBER: ClassVar[int]
api_visibility: _descriptor.FieldDescriptor
enum_visibility: _descriptor.FieldDescriptor
field_visibility: _descriptor.FieldDescriptor
message_visibility: _descriptor.FieldDescriptor
method_visibility: _descriptor.FieldDescriptor
value_visibility: _descriptor.FieldDescriptor

class Visibility(_message.Message):
    __slots__ = ["rules"]
    RULES_FIELD_NUMBER: ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[VisibilityRule]
    def __init__(self, rules: Optional[Iterable[Union[VisibilityRule, Mapping]]] = ...) -> None: ...

class VisibilityRule(_message.Message):
    __slots__ = ["restriction", "selector"]
    RESTRICTION_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    restriction: str
    selector: str
    def __init__(self, selector: Optional[str] = ..., restriction: Optional[str] = ...) -> None: ...
