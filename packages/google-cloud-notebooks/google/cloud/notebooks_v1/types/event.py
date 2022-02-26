# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
#
import proto  # type: ignore

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(package="google.cloud.notebooks.v1", manifest={"Event",},)


class Event(proto.Message):
    r"""The definition of an Event for a managed / semi-managed
    notebook instance.

    Attributes:
        report_time (google.protobuf.timestamp_pb2.Timestamp):
            Event report time.
        type_ (google.cloud.notebooks_v1.types.Event.EventType):
            Event type.
    """

    class EventType(proto.Enum):
        r"""The definition of the even types."""
        EVENT_TYPE_UNSPECIFIED = 0
        IDLE = 1

    report_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    type_ = proto.Field(proto.ENUM, number=2, enum=EventType,)


__all__ = tuple(sorted(__protobuf__.manifest))
