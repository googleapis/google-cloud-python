from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Billing(_message.Message):
    __slots__ = ("consumer_destinations",)
    class BillingDestination(_message.Message):
        __slots__ = ("monitored_resource", "metrics")
        MONITORED_RESOURCE_FIELD_NUMBER: _ClassVar[int]
        METRICS_FIELD_NUMBER: _ClassVar[int]
        monitored_resource: str
        metrics: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, monitored_resource: _Optional[str] = ..., metrics: _Optional[_Iterable[str]] = ...) -> None: ...
    CONSUMER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    consumer_destinations: _containers.RepeatedCompositeFieldContainer[Billing.BillingDestination]
    def __init__(self, consumer_destinations: _Optional[_Iterable[_Union[Billing.BillingDestination, _Mapping]]] = ...) -> None: ...
