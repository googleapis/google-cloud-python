# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Monitoring(_message.Message):
    __slots__ = ["consumer_destinations", "producer_destinations"]
    class MonitoringDestination(_message.Message):
        __slots__ = ["metrics", "monitored_resource"]
        METRICS_FIELD_NUMBER: _ClassVar[int]
        MONITORED_RESOURCE_FIELD_NUMBER: _ClassVar[int]
        metrics: _containers.RepeatedScalarFieldContainer[str]
        monitored_resource: str
        def __init__(
            self,
            monitored_resource: _Optional[str] = ...,
            metrics: _Optional[_Iterable[str]] = ...,
        ) -> None: ...

    CONSUMER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    PRODUCER_DESTINATIONS_FIELD_NUMBER: _ClassVar[int]
    consumer_destinations: _containers.RepeatedCompositeFieldContainer[
        Monitoring.MonitoringDestination
    ]
    producer_destinations: _containers.RepeatedCompositeFieldContainer[
        Monitoring.MonitoringDestination
    ]
    def __init__(
        self,
        producer_destinations: _Optional[
            _Iterable[_Union[Monitoring.MonitoringDestination, _Mapping]]
        ] = ...,
        consumer_destinations: _Optional[
            _Iterable[_Union[Monitoring.MonitoringDestination, _Mapping]]
        ] = ...,
    ) -> None: ...
