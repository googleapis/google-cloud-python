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
from typing import MutableMapping, MutableSequence

from google.protobuf import duration_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.video.stitcher.v1",
    manifest={
        "Event",
        "ProgressEvent",
    },
)


class Event(proto.Message):
    r"""Describes an event and a trigger URI.

    Attributes:
        type_ (google.cloud.video.stitcher_v1.types.Event.EventType):
            Describes the event that occurred.
        uri (str):
            The URI to trigger for this event.
        id (str):
            The ID of the event.
        offset (google.protobuf.duration_pb2.Duration):
            The offset in seconds if the event type is ``PROGRESS``.
    """

    class EventType(proto.Enum):
        r"""Describes the event that occurred."""
        EVENT_TYPE_UNSPECIFIED = 0
        CREATIVE_VIEW = 1
        START = 2
        BREAK_START = 3
        BREAK_END = 4
        IMPRESSION = 5
        FIRST_QUARTILE = 6
        MIDPOINT = 7
        THIRD_QUARTILE = 8
        COMPLETE = 9
        PROGRESS = 10
        MUTE = 11
        UNMUTE = 12
        PAUSE = 13
        CLICK = 14
        CLICK_THROUGH = 15
        REWIND = 16
        RESUME = 17
        ERROR = 18
        EXPAND = 21
        COLLAPSE = 22
        CLOSE = 24
        CLOSE_LINEAR = 25
        SKIP = 26
        ACCEPT_INVITATION = 27

    type_: EventType = proto.Field(
        proto.ENUM,
        number=1,
        enum=EventType,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    offset: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=4,
        message=duration_pb2.Duration,
    )


class ProgressEvent(proto.Message):
    r"""Indicates a time in which a list of events should be
    triggered during media playback.

    Attributes:
        time_offset (google.protobuf.duration_pb2.Duration):
            The time when the following tracking events
            occurs. The time is in seconds relative to the
            start of the VOD asset.
        events (MutableSequence[google.cloud.video.stitcher_v1.types.Event]):
            The list of progress tracking events for the ad break. These
            can be of the following IAB types: ``BREAK_START``,
            ``BREAK_END``, ``IMPRESSION``, ``CREATIVE_VIEW``, ``START``,
            ``FIRST_QUARTILE``, ``MIDPOINT``, ``THIRD_QUARTILE``,
            ``COMPLETE``, ``PROGRESS``.
    """

    time_offset: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=1,
        message=duration_pb2.Duration,
    )
    events: MutableSequence["Event"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="Event",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
