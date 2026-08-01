from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Logging(_message.Message):
    __slots__ = ["consumer_destinations", "producer_destinations"]
    class LoggingDestination(_message.Message):
        __slots__ = ["logs", "monitored_resource"]
        LOGS_FIELD_NUMBER: _ClassVar[int]
        MONITORED_RESOURCE_FIELD_NUMBER: _ClassVar[int]
        logs: _containers.RepeatedScalarFieldContainer[str]
        monitored_resource: str
        def __init__(self, monitored_resource: _Optional[str] = ..., logs: _Optional[_Iterable[str]] = ...) -> None: ...
    CONSUMER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    consumer_destinations: _containers.RepeatedCompositeFieldContainer[Logging.LoggingDestination]
    producer_destinations: _containers.RepeatedCompositeFieldContainer[Logging.LoggingDestination]
    def __init__(self, producer_destinations: _Optional[_Iterable[_Union[Logging.LoggingDestination, _Mapping]]] = ..., consumer_destinations: _Optional[_Iterable[_Union[Logging.LoggingDestination, _Mapping]]] = ...) -> None: ...
