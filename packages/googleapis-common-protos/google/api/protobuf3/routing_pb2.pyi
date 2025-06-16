from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
ROUTING_FIELD_NUMBER: ClassVar[int]
routing: _descriptor.FieldDescriptor

class RoutingParameter(_message.Message):
    __slots__ = ["field", "path_template"]
    FIELD_FIELD_NUMBER: ClassVar[int]
    PATH_TEMPLATE_FIELD_NUMBER: ClassVar[int]
    field: str
    path_template: str
    def __init__(self, field: Optional[str] = ..., path_template: Optional[str] = ...) -> None: ...

class RoutingRule(_message.Message):
    __slots__ = ["routing_parameters"]
    ROUTING_PARAMETERS_FIELD_NUMBER: ClassVar[int]
    routing_parameters: _containers.RepeatedCompositeFieldContainer[RoutingParameter]
    def __init__(self, routing_parameters: Optional[Iterable[Union[RoutingParameter, Mapping]]] = ...) -> None: ...
