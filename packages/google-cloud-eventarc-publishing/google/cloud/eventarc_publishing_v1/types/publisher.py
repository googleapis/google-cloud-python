# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import any_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.eventarc.publishing.v1",
    manifest={
        "PublishChannelConnectionEventsRequest",
        "PublishChannelConnectionEventsResponse",
        "PublishEventsRequest",
        "PublishEventsResponse",
    },
)


class PublishChannelConnectionEventsRequest(proto.Message):
    r"""The request message for the PublishChannelConnectionEvents
    method.

    Attributes:
        channel_connection (str):
            The channel_connection that the events are published from.
            For example:
            ``projects/{partner_project_id}/locations/{location}/channelConnections/{channel_connection_id}``.
        events (MutableSequence[google.protobuf.any_pb2.Any]):
            The CloudEvents v1.0 events to publish. No other types are
            allowed. If this field is set, then the ``text_events``
            fields must not be set.
        text_events (MutableSequence[str]):
            The text representation of events to publish. CloudEvent
            v1.0 in JSON format is the only allowed type. Refer to
            https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md
            for specification. If this field is set, then the ``events``
            fields must not be set.
    """

    channel_connection: str = proto.Field(
        proto.STRING,
        number=1,
    )
    events: MutableSequence[any_pb2.Any] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=any_pb2.Any,
    )
    text_events: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class PublishChannelConnectionEventsResponse(proto.Message):
    r"""The response message for the PublishChannelConnectionEvents
    method.

    """


class PublishEventsRequest(proto.Message):
    r"""The request message for the PublishEvents method.

    Attributes:
        channel (str):
            The full name of the channel to publish to. For example:
            ``projects/{project}/locations/{location}/channels/{channel-id}``.
        events (MutableSequence[google.protobuf.any_pb2.Any]):
            The CloudEvents v1.0 events to publish. No other types are
            allowed. If this field is set, then the ``text_events``
            fields must not be set.
        text_events (MutableSequence[str]):
            The text representation of events to publish. CloudEvent
            v1.0 in JSON format is the only allowed type. Refer to
            https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md
            for specification. If this field is set, then the ``events``
            fields must not be set.
    """

    channel: str = proto.Field(
        proto.STRING,
        number=1,
    )
    events: MutableSequence[any_pb2.Any] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=any_pb2.Any,
    )
    text_events: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class PublishEventsResponse(proto.Message):
    r"""The response message for the PublishEvents method."""


__all__ = tuple(sorted(__protobuf__.manifest))
