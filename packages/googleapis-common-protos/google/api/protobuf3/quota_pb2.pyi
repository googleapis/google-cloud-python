from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricRule(_message.Message):
    __slots__ = ["metric_costs", "selector"]
    class MetricCostsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: int
        def __init__(self, key: Optional[str] = ..., value: Optional[int] = ...) -> None: ...
    METRIC_COSTS_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    metric_costs: _containers.ScalarMap[str, int]
    selector: str
    def __init__(self, selector: Optional[str] = ..., metric_costs: Optional[Mapping[str, int]] = ...) -> None: ...

class Quota(_message.Message):
    __slots__ = ["limits", "metric_rules"]
    LIMITS_FIELD_NUMBER: ClassVar[int]
    METRIC_RULES_FIELD_NUMBER: ClassVar[int]
    limits: _containers.RepeatedCompositeFieldContainer[QuotaLimit]
    metric_rules: _containers.RepeatedCompositeFieldContainer[MetricRule]
    def __init__(self, limits: Optional[Iterable[Union[QuotaLimit, Mapping]]] = ..., metric_rules: Optional[Iterable[Union[MetricRule, Mapping]]] = ...) -> None: ...

class QuotaLimit(_message.Message):
    __slots__ = ["default_limit", "description", "display_name", "duration", "free_tier", "max_limit", "metric", "name", "unit", "values"]
    class ValuesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: int
        def __init__(self, key: Optional[str] = ..., value: Optional[int] = ...) -> None: ...
    DEFAULT_LIMIT_FIELD_NUMBER: ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: ClassVar[int]
    DURATION_FIELD_NUMBER: ClassVar[int]
    FREE_TIER_FIELD_NUMBER: ClassVar[int]
    MAX_LIMIT_FIELD_NUMBER: ClassVar[int]
    METRIC_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    UNIT_FIELD_NUMBER: ClassVar[int]
    VALUES_FIELD_NUMBER: ClassVar[int]
    default_limit: int
    description: str
    display_name: str
    duration: str
    free_tier: int
    max_limit: int
    metric: str
    name: str
    unit: str
    values: _containers.ScalarMap[str, int]
    def __init__(self, name: Optional[str] = ..., description: Optional[str] = ..., default_limit: Optional[int] = ..., max_limit: Optional[int] = ..., free_tier: Optional[int] = ..., duration: Optional[str] = ..., metric: Optional[str] = ..., unit: Optional[str] = ..., values: Optional[Mapping[str, int]] = ..., display_name: Optional[str] = ...) -> None: ...
