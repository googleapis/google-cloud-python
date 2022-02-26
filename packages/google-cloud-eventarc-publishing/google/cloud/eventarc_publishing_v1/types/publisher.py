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

from google.protobuf import any_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.eventarc.publishing.v1",
    manifest={
        "PublishChannelConnectionEventsRequest",
        "PublishChannelConnectionEventsResponse",
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
        events (Sequence[google.protobuf.any_pb2.Any]):
            The CloudEvents v1.0 events to publish. No
            other types are allowed.
    """

    channel_connection = proto.Field(proto.STRING, number=1,)
    events = proto.RepeatedField(proto.MESSAGE, number=2, message=any_pb2.Any,)


class PublishChannelConnectionEventsResponse(proto.Message):
    r"""The response message for the PublishChannelConnectionEvents
    method.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
