from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Distribution(_message.Message):
    __slots__ = ["bucket_counts", "bucket_options", "count", "exemplars", "mean", "range", "sum_of_squared_deviation"]
    class BucketOptions(_message.Message):
        __slots__ = ["explicit_buckets", "exponential_buckets", "linear_buckets"]
        class Explicit(_message.Message):
            __slots__ = ["bounds"]
            BOUNDS_FIELD_NUMBER: ClassVar[int]
            bounds: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, bounds: Optional[Iterable[float]] = ...) -> None: ...
        class Exponential(_message.Message):
            __slots__ = ["growth_factor", "num_finite_buckets", "scale"]
            GROWTH_FACTOR_FIELD_NUMBER: ClassVar[int]
            NUM_FINITE_BUCKETS_FIELD_NUMBER: ClassVar[int]
            SCALE_FIELD_NUMBER: ClassVar[int]
            growth_factor: float
            num_finite_buckets: int
            scale: float
            def __init__(self, num_finite_buckets: Optional[int] = ..., growth_factor: Optional[float] = ..., scale: Optional[float] = ...) -> None: ...
        class Linear(_message.Message):
            __slots__ = ["num_finite_buckets", "offset", "width"]
            NUM_FINITE_BUCKETS_FIELD_NUMBER: ClassVar[int]
            OFFSET_FIELD_NUMBER: ClassVar[int]
            WIDTH_FIELD_NUMBER: ClassVar[int]
            num_finite_buckets: int
            offset: float
            width: float
            def __init__(self, num_finite_buckets: Optional[int] = ..., width: Optional[float] = ..., offset: Optional[float] = ...) -> None: ...
        EXPLICIT_BUCKETS_FIELD_NUMBER: ClassVar[int]
        EXPONENTIAL_BUCKETS_FIELD_NUMBER: ClassVar[int]
        LINEAR_BUCKETS_FIELD_NUMBER: ClassVar[int]
        explicit_buckets: Distribution.BucketOptions.Explicit
        exponential_buckets: Distribution.BucketOptions.Exponential
        linear_buckets: Distribution.BucketOptions.Linear
        def __init__(self, linear_buckets: Optional[Union[Distribution.BucketOptions.Linear, Mapping]] = ..., exponential_buckets: Optional[Union[Distribution.BucketOptions.Exponential, Mapping]] = ..., explicit_buckets: Optional[Union[Distribution.BucketOptions.Explicit, Mapping]] = ...) -> None: ...
    class Exemplar(_message.Message):
        __slots__ = ["attachments", "timestamp", "value"]
        ATTACHMENTS_FIELD_NUMBER: ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        attachments: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
        timestamp: _timestamp_pb2.Timestamp
        value: float
        def __init__(self, value: Optional[float] = ..., timestamp: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., attachments: Optional[Iterable[Union[_any_pb2.Any, Mapping]]] = ...) -> None: ...
    class Range(_message.Message):
        __slots__ = ["max", "min"]
        MAX_FIELD_NUMBER: ClassVar[int]
        MIN_FIELD_NUMBER: ClassVar[int]
        max: float
        min: float
        def __init__(self, min: Optional[float] = ..., max: Optional[float] = ...) -> None: ...
    BUCKET_COUNTS_FIELD_NUMBER: ClassVar[int]
    BUCKET_OPTIONS_FIELD_NUMBER: ClassVar[int]
    COUNT_FIELD_NUMBER: ClassVar[int]
    EXEMPLARS_FIELD_NUMBER: ClassVar[int]
    MEAN_FIELD_NUMBER: ClassVar[int]
    RANGE_FIELD_NUMBER: ClassVar[int]
    SUM_OF_SQUARED_DEVIATION_FIELD_NUMBER: ClassVar[int]
    bucket_counts: _containers.RepeatedScalarFieldContainer[int]
    bucket_options: Distribution.BucketOptions
    count: int
    exemplars: _containers.RepeatedCompositeFieldContainer[Distribution.Exemplar]
    mean: float
    range: Distribution.Range
    sum_of_squared_deviation: float
    def __init__(self, count: Optional[int] = ..., mean: Optional[float] = ..., sum_of_squared_deviation: Optional[float] = ..., range: Optional[Union[Distribution.Range, Mapping]] = ..., bucket_options: Optional[Union[Distribution.BucketOptions, Mapping]] = ..., bucket_counts: Optional[Iterable[int]] = ..., exemplars: Optional[Iterable[Union[Distribution.Exemplar, Mapping]]] = ...) -> None: ...
