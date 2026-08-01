from google.api import label_pb2 as _label_pb2
from google.api import launch_stage_pb2 as _launch_stage_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Metric(_message.Message):
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

class MetricDescriptor(_message.Message):
    __slots__ = ["description", "display_name", "labels", "launch_stage", "metadata", "metric_kind", "monitored_resource_types", "name", "type", "unit", "value_type"]
    class MetricKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class MetricDescriptorMetadata(_message.Message):
        __slots__ = ["ingest_delay", "launch_stage", "sample_period", "time_series_resource_hierarchy_level"]
        class TimeSeriesResourceHierarchyLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        FOLDER: MetricDescriptor.MetricDescriptorMetadata.TimeSeriesResourceHierarchyLevel
        INGEST_DELAY_FIELD_NUMBER: _ClassVar[int]
        LAUNCH_STAGE_FIELD_NUMBER: _ClassVar[int]
        ORGANIZATION: MetricDescriptor.MetricDescriptorMetadata.TimeSeriesResourceHierarchyLevel
        PROJECT: MetricDescriptor.MetricDescriptorMetadata.TimeSeriesResourceHierarchyLevel
        SAMPLE_PERIOD_FIELD_NUMBER: _ClassVar[int]
        TIME_SERIES_RESOURCE_HIERARCHY_LEVEL_FIELD_NUMBER: _ClassVar[int]
        TIME_SERIES_RESOURCE_HIERARCHY_LEVEL_UNSPECIFIED: MetricDescriptor.MetricDescriptorMetadata.TimeSeriesResourceHierarchyLevel
        ingest_delay: _duration_pb2.Duration
        launch_stage: _launch_stage_pb2.LaunchStage
        sample_period: _duration_pb2.Duration
        time_series_resource_hierarchy_level: _containers.RepeatedScalarFieldContainer[MetricDescriptor.MetricDescriptorMetadata.TimeSeriesResourceHierarchyLevel]
        def __init__(self, launch_stage: _Optional[_Union[_launch_stage_pb2.LaunchStage, str]] = ..., sample_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., ingest_delay: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., time_series_resource_hierarchy_level: _Optional[_Iterable[_Union[MetricDescriptor.MetricDescriptorMetadata.TimeSeriesResourceHierarchyLevel, str]]] = ...) -> None: ...
    BOOL: MetricDescriptor.ValueType
    CUMULATIVE: MetricDescriptor.MetricKind
    DELTA: MetricDescriptor.MetricKind
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION: MetricDescriptor.ValueType
    DOUBLE: MetricDescriptor.ValueType
    GAUGE: MetricDescriptor.MetricKind
    INT64: MetricDescriptor.ValueType
    LABELS_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_STAGE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    METRIC_KIND_FIELD_NUMBER: _ClassVar[int]
    METRIC_KIND_UNSPECIFIED: MetricDescriptor.MetricKind
    MONEY: MetricDescriptor.ValueType
    MONITORED_RESOURCE_TYPES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STRING: MetricDescriptor.ValueType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_UNSPECIFIED: MetricDescriptor.ValueType
    description: str
    display_name: str
    labels: _containers.RepeatedCompositeFieldContainer[_label_pb2.LabelDescriptor]
    launch_stage: _launch_stage_pb2.LaunchStage
    metadata: MetricDescriptor.MetricDescriptorMetadata
    metric_kind: MetricDescriptor.MetricKind
    monitored_resource_types: _containers.RepeatedScalarFieldContainer[str]
    name: str
    type: str
    unit: str
    value_type: MetricDescriptor.ValueType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., labels: _Optional[_Iterable[_Union[_label_pb2.LabelDescriptor, _Mapping]]] = ..., metric_kind: _Optional[_Union[MetricDescriptor.MetricKind, str]] = ..., value_type: _Optional[_Union[MetricDescriptor.ValueType, str]] = ..., unit: _Optional[str] = ..., description: _Optional[str] = ..., display_name: _Optional[str] = ..., metadata: _Optional[_Union[MetricDescriptor.MetricDescriptorMetadata, _Mapping]] = ..., launch_stage: _Optional[_Union[_launch_stage_pb2.LaunchStage, str]] = ..., monitored_resource_types: _Optional[_Iterable[str]] = ...) -> None: ...
