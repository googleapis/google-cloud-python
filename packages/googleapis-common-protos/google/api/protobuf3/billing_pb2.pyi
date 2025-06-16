from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Billing(_message.Message):
    __slots__ = ["consumer_destinations"]
    class BillingDestination(_message.Message):
        __slots__ = ["metrics", "monitored_resource"]
        METRICS_FIELD_NUMBER: ClassVar[int]
        MONITORED_RESOURCE_FIELD_NUMBER: ClassVar[int]
        metrics: _containers.RepeatedScalarFieldContainer[str]
        monitored_resource: str
        def __init__(self, monitored_resource: Optional[str] = ..., metrics: Optional[Iterable[str]] = ...) -> None: ...
    CONSUMER_DESTINATIONS_FIELD_NUMBER: ClassVar[int]
    consumer_destinations: _containers.RepeatedCompositeFieldContainer[Billing.BillingDestination]
    def __init__(self, consumer_destinations: Optional[Iterable[Union[Billing.BillingDestination, Mapping]]] = ...) -> None: ...
