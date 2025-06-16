# -*- coding: utf-8 -*-
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
#
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.geminidataanalytics.v1alpha",
    manifest={
        "Conversation",
        "CreateConversationRequest",
        "GetConversationRequest",
        "ListConversationsRequest",
        "ListConversationsResponse",
    },
)


class Conversation(proto.Message):
    r"""Message for a conversation.

    Attributes:
        name (str):
            Optional. Identifier. The unique resource
            name of a conversation. It's not expected to be
            set when creating a conversation.
        agents (MutableSequence[str]):
            Required. Agent(s) in the conversation.
            Currently, only one agent is supported. This
            field is repeated to allow for future support of
            multiple agents in a conversation. Format:
            projects/{project}/locations/{location}/dataAgents/{agent}
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Creation timestamp.
        last_used_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of the last used
            conversation.
        labels (MutableMapping[str, str]):
            Optional. Open-ended and user-defined labels
            that can be set by the client to tag a
            conversation (e.g. to filter conversations for
            specific surfaces/products).
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    agents: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    last_used_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    labels: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=9,
    )


class CreateConversationRequest(proto.Message):
    r"""Request for creating a conversation.

    Attributes:
        parent (str):
            Required. Parent value for
            CreateConversationRequest. Format:
            projects/{project}/locations/{location}
        conversation_id (str):
            Optional. The conversation id of the
            conversation to create.
        conversation (google.cloud.geminidataanalytics_v1alpha.types.Conversation):
            Required. The conversation to create.
        request_id (str):
            Optional. An optional request ID to identify
            requests. Specify a unique request ID so that if
            you must retry your request, the server will
            know to ignore the request if it has already
            been completed. The server will guarantee that
            for at least 60 minutes since the first request.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversation_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    conversation: "Conversation" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Conversation",
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


class GetConversationRequest(proto.Message):
    r"""Request for getting a conversation based on parent and
    conversation id.

    Attributes:
        name (str):
            Required. Name of the resource.
            Format:

            projects/{project}/locations/{location}/conversations/{conversation}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListConversationsRequest(proto.Message):
    r"""Request for listing conversations based on parent.

    Attributes:
        parent (str):
            Required. Parent value for
            ListConversationsRequest. Format:
            projects/{project}/locations/{location}
        page_size (int):
            Optional. Requested page size. Server may
            return fewer items than requested. The max page
            size is 100. All larger page sizes will be
            coerced to 100. If unspecified, server will pick
            50 as an approperiate default.
        page_token (str):
            Optional. A token identifying a page of
            results the server should return.
        filter (str):
            Optional. Returned conversations will match criteria
            specified within the filter. ListConversations allows
            filtering by:

            -  agent_id
            -  labels
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )


class ListConversationsResponse(proto.Message):
    r"""Message for response to listing conversations.

    Attributes:
        conversations (MutableSequence[google.cloud.geminidataanalytics_v1alpha.types.Conversation]):
            The list of conversations.
        next_page_token (str):
            A token identifying a page of results the
            server should return.
    """

    @property
    def raw_page(self):
        return self

    conversations: MutableSequence["Conversation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Conversation",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
