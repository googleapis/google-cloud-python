from google.api import label_pb2 as _label_pb2
from google.api import launch_stage_pb2 as _launch_stage_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoredResource(_message.Message):
    __slots__ = ["labels", "type"]
    class LabelsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    LABELS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.ScalarMap[str, str]
    type: str
    def __init__(self, type: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MonitoredResourceDescriptor(_message.Message):
    __slots__ = ["description", "display_name", "labels", "launch_stage", "name", "type"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_STAGE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    description: str
    display_name: str
    labels: _containers.RepeatedCompositeFieldContainer[_label_pb2.LabelDescriptor]
    launch_stage: _launch_stage_pb2.LaunchStage
    name: str
    type: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., labels: _Optional[_Iterable[_Union[_label_pb2.LabelDescriptor, _Mapping]]] = ..., launch_stage: _Optional[_Union[_launch_stage_pb2.LaunchStage, str]] = ...) -> None: ...

class MonitoredResourceMetadata(_message.Message):
    __slots__ = ["system_labels", "user_labels"]
    class UserLabelsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SYSTEM_LABELS_FIELD_NUMBER: _ClassVar[int]
    USER_LABELS_FIELD_NUMBER: _ClassVar[int]
    system_labels: _struct_pb2.Struct
    user_labels: _containers.ScalarMap[str, str]
    def __init__(self, system_labels: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., user_labels: _Optional[_Mapping[str, str]] = ...) -> None: ...
