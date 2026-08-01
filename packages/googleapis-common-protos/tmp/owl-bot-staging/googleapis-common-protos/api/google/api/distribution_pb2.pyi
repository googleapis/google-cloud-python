from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Distribution(_message.Message):
    __slots__ = ["bucket_counts", "bucket_options", "count", "exemplars", "mean", "range", "sum_of_squared_deviation"]
    class BucketOptions(_message.Message):
        __slots__ = ["explicit_buckets", "exponential_buckets", "linear_buckets"]
        class Explicit(_message.Message):
            __slots__ = ["bounds"]
            BOUNDS_FIELD_NUMBER: _ClassVar[int]
            bounds: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, bounds: _Optional[_Iterable[float]] = ...) -> None: ...
        class Exponential(_message.Message):
            __slots__ = ["growth_factor", "num_finite_buckets", "scale"]
            GROWTH_FACTOR_FIELD_NUMBER: _ClassVar[int]
            NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
            SCALE_FIELD_NUMBER: _ClassVar[int]
            growth_factor: float
            num_finite_buckets: int
            scale: float
            def __init__(self, num_finite_buckets: _Optional[int] = ..., growth_factor: _Optional[float] = ..., scale: _Optional[float] = ...) -> None: ...
        class Linear(_message.Message):
            __slots__ = ["num_finite_buckets", "offset", "width"]
            NUM_FINITE_BUCKETS_FIELD_NUMBER: _ClassVar[int]
            OFFSET_FIELD_NUMBER: _ClassVar[int]
            WIDTH_FIELD_NUMBER: _ClassVar[int]
            num_finite_buckets: int
            offset: float
            width: float
            def __init__(self, num_finite_buckets: _Optional[int] = ..., width: _Optional[float] = ..., offset: _Optional[float] = ...) -> None: ...
        EXPLICIT_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        EXPONENTIAL_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        LINEAR_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        explicit_buckets: Distribution.BucketOptions.Explicit
        exponential_buckets: Distribution.BucketOptions.Exponential
        linear_buckets: Distribution.BucketOptions.Linear
        def __init__(self, linear_buckets: _Optional[_Union[Distribution.BucketOptions.Linear, _Mapping]] = ..., exponential_buckets: _Optional[_Union[Distribution.BucketOptions.Exponential, _Mapping]] = ..., explicit_buckets: _Optional[_Union[Distribution.BucketOptions.Explicit, _Mapping]] = ...) -> None: ...
    class Exemplar(_message.Message):
        __slots__ = ["attachments", "timestamp", "value"]
        ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        attachments: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
        timestamp: _timestamp_pb2.Timestamp
        value: float
        def __init__(self, value: _Optional[float] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., attachments: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]] = ...) -> None: ...
    class Range(_message.Message):
        __slots__ = ["max", "min"]
        MAX_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        max: float
        min: float
        def __init__(self, min: _Optional[float] = ..., max: _Optional[float] = ...) -> None: ...
    BUCKET_COUNTS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    EXEMPLARS_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    SUM_OF_SQUARED_DEVIATION_FIELD_NUMBER: _ClassVar[int]
    bucket_counts: _containers.RepeatedScalarFieldContainer[int]
    bucket_options: Distribution.BucketOptions
    count: int
    exemplars: _containers.RepeatedCompositeFieldContainer[Distribution.Exemplar]
    mean: float
    range: Distribution.Range
    sum_of_squared_deviation: float
    def __init__(self, count: _Optional[int] = ..., mean: _Optional[float] = ..., sum_of_squared_deviation: _Optional[float] = ..., range: _Optional[_Union[Distribution.Range, _Mapping]] = ..., bucket_options: _Optional[_Union[Distribution.BucketOptions, _Mapping]] = ..., bucket_counts: _Optional[_Iterable[int]] = ..., exemplars: _Optional[_Iterable[_Union[Distribution.Exemplar, _Mapping]]] = ...) -> None: ...
