from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Logging(_message.Message):
    __slots__ = ("producer_destinations", "consumer_destinations")
    class LoggingDestination(_message.Message):
        __slots__ = ("monitored_resource", "logs")
        MONITORED_RESOURCE_FIELD_NUMBER: _ClassVar[int]
        LOGS_FIELD_NUMBER: _ClassVar[int]
        monitored_resource: str
        logs: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, monitored_resource: _Optional[str] = ..., logs: _Optional[_Iterable[str]] = ...) -> None: ...
    PRODUCER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    producer_destinations: _containers.RepeatedCompositeFieldContainer[Logging.LoggingDestination]
    consumer_destinations: _containers.RepeatedCompositeFieldContainer[Logging.LoggingDestination]
    def __init__(self, producer_destinations: _Optional[_Iterable[_Union[Logging.LoggingDestination, _Mapping]]] = ..., consumer_destinations: _Optional[_Iterable[_Union[Logging.LoggingDestination, _Mapping]]] = ...) -> None: ...
