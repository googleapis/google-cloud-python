from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

API_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
DESCRIPTOR: _descriptor.FileDescriptor
ENUM_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
FIELD_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
MESSAGE_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
METHOD_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
VALUE_VISIBILITY_FIELD_NUMBER: _ClassVar[int]
api_visibility: _descriptor.FieldDescriptor
enum_visibility: _descriptor.FieldDescriptor
field_visibility: _descriptor.FieldDescriptor
message_visibility: _descriptor.FieldDescriptor
method_visibility: _descriptor.FieldDescriptor
value_visibility: _descriptor.FieldDescriptor

class Visibility(_message.Message):
    __slots__ = ["rules"]
    RULES_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[VisibilityRule]
    def __init__(self, rules: _Optional[_Iterable[_Union[VisibilityRule, _Mapping]]] = ...) -> None: ...

class VisibilityRule(_message.Message):
    __slots__ = ["restriction", "selector"]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    restriction: str
    selector: str
    def __init__(self, selector: _Optional[str] = ..., restriction: _Optional[str] = ...) -> None: ...
