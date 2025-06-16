from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Usage(_message.Message):
    __slots__ = ["producer_notification_channel", "requirements", "rules"]
    PRODUCER_NOTIFICATION_CHANNEL_FIELD_NUMBER: ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: ClassVar[int]
    RULES_FIELD_NUMBER: ClassVar[int]
    producer_notification_channel: str
    requirements: _containers.RepeatedScalarFieldContainer[str]
    rules: _containers.RepeatedCompositeFieldContainer[UsageRule]
    def __init__(self, requirements: Optional[Iterable[str]] = ..., rules: Optional[Iterable[Union[UsageRule, Mapping]]] = ..., producer_notification_channel: Optional[str] = ...) -> None: ...

class UsageRule(_message.Message):
    __slots__ = ["allow_unregistered_calls", "selector", "skip_service_control"]
    ALLOW_UNREGISTERED_CALLS_FIELD_NUMBER: ClassVar[int]
    SELECTOR_FIELD_NUMBER: ClassVar[int]
    SKIP_SERVICE_CONTROL_FIELD_NUMBER: ClassVar[int]
    allow_unregistered_calls: bool
    selector: str
    skip_service_control: bool
    def __init__(self, selector: Optional[str] = ..., allow_unregistered_calls: bool = ..., skip_service_control: bool = ...) -> None: ...
