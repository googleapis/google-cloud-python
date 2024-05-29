# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.discoveryengine.v1beta",
    manifest={
        "Session",
        "Query",
    },
)


class Session(proto.Message):
    r"""External session proto definition.

    Attributes:
        name (str):
            Immutable. Fully qualified name
            ``projects/{project}/locations/global/collections/{collection}/engines/{engine}/sessions/*``
        state (google.cloud.discoveryengine_v1beta.types.Session.State):
            The state of the session.
        user_pseudo_id (str):
            A unique identifier for tracking users.
        turns (MutableSequence[google.cloud.discoveryengine_v1beta.types.Session.Turn]):
            Turns.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the session started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the session finished.
    """

    class State(proto.Enum):
        r"""Enumeration of the state of the session.

        Values:
            STATE_UNSPECIFIED (0):
                State is unspecified.
            IN_PROGRESS (1):
                The session is currently open.
        """
        STATE_UNSPECIFIED = 0
        IN_PROGRESS = 1

    class Turn(proto.Message):
        r"""Represents a turn, including a query from the user and a
        answer from service.

        Attributes:
            query (google.cloud.discoveryengine_v1beta.types.Query):
                The user query.
            answer (str):
                The resource name of the answer to the user
                query.
                Only set if the answer generation (/answer API
                call) happened in this turn.
        """

        query: "Query" = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Query",
        )
        answer: str = proto.Field(
            proto.STRING,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=2,
        enum=State,
    )
    user_pseudo_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    turns: MutableSequence[Turn] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=Turn,
    )
    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=5,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )


class Query(proto.Message):
    r"""Defines a user inputed query.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            Plain text.

            This field is a member of `oneof`_ ``content``.
        query_id (str):
            Unique Id for the query.
    """

    text: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="content",
    )
    query_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
