from google.api import label_pb2 as _label_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogDescriptor(_message.Message):
    __slots__ = ["description", "display_name", "labels", "name"]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: ClassVar[int]
    LABELS_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    description: str
    display_name: str
    labels: _containers.RepeatedCompositeFieldContainer[_label_pb2.LabelDescriptor]
    name: str
    def __init__(self, name: Optional[str] = ..., labels: Optional[Iterable[Union[_label_pb2.LabelDescriptor, Mapping]]] = ..., description: Optional[str] = ..., display_name: Optional[str] = ...) -> None: ...
