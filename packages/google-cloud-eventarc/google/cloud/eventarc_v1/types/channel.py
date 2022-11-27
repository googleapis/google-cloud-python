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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.eventarc.v1",
    manifest={
        "Channel",
    },
)


class Channel(proto.Message):
    r"""A representation of the Channel resource.
    A Channel is a resource on which event providers publish their
    events. The published events are delivered through the transport
    associated with the channel. Note that a channel is associated
    with exactly one event provider.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Required. The resource name of the channel. Must be unique
            within the location on the project and must be in
            ``projects/{project}/locations/{location}/channels/{channel_id}``
            format.
        uid (str):
            Output only. Server assigned unique
            identifier for the channel. The value is a UUID4
            string and guaranteed to remain unchanged until
            the resource is deleted.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The creation time.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The last-modified time.
        provider (str):
            The name of the event provider (e.g. Eventarc SaaS partner)
            associated with the channel. This provider will be granted
            permissions to publish events to the channel. Format:
            ``projects/{project}/locations/{location}/providers/{provider_id}``.
        pubsub_topic (str):
            Output only. The name of the Pub/Sub topic created and
            managed by Eventarc system as a transport for the event
            delivery. Format: ``projects/{project}/topics/{topic_id}``.

            This field is a member of `oneof`_ ``transport``.
        state (google.cloud.eventarc_v1.types.Channel.State):
            Output only. The state of a Channel.
        activation_token (str):
            Output only. The activation token for the
            channel. The token must be used by the provider
            to register the channel for publishing.
        crypto_key_name (str):
            Optional. Resource name of a KMS crypto key (managed by the
            user) used to encrypt/decrypt their event data.

            It must match the pattern
            ``projects/*/locations/*/keyRings/*/cryptoKeys/*``.
    """

    class State(proto.Enum):
        r"""State lists all the possible states of a Channel"""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        ACTIVE = 2
        INACTIVE = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    provider: str = proto.Field(
        proto.STRING,
        number=7,
    )
    pubsub_topic: str = proto.Field(
        proto.STRING,
        number=8,
        oneof="transport",
    )
    state: State = proto.Field(
        proto.ENUM,
        number=9,
        enum=State,
    )
    activation_token: str = proto.Field(
        proto.STRING,
        number=10,
    )
    crypto_key_name: str = proto.Field(
        proto.STRING,
        number=11,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
