# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.dialogflow_v2.types import participant
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2", manifest={"ConversationEvent",},
)


class ConversationEvent(proto.Message):
    r"""Represents a notification sent to Pub/Sub subscribers for
    conversation lifecycle events.

    Attributes:
        conversation (str):
            The unique identifier of the conversation this notification
            refers to. Format:
            ``projects/<Project ID>/conversations/<Conversation ID>``.
        type_ (google.cloud.dialogflow_v2.types.ConversationEvent.Type):
            The type of the event that this notification
            refers to.
        error_status (google.rpc.status_pb2.Status):
            More detailed information about an error. Only set for type
            UNRECOVERABLE_ERROR_IN_PHONE_CALL.
        new_message_payload (google.cloud.dialogflow_v2.types.Message):
            Payload of NEW_MESSAGE event.
    """

    class Type(proto.Enum):
        r"""Enumeration of the types of events available."""
        TYPE_UNSPECIFIED = 0
        CONVERSATION_STARTED = 1
        CONVERSATION_FINISHED = 2
        HUMAN_INTERVENTION_NEEDED = 3
        NEW_MESSAGE = 5
        UNRECOVERABLE_ERROR = 4

    conversation = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.ENUM, number=2, enum=Type,)
    error_status = proto.Field(proto.MESSAGE, number=3, message=status_pb2.Status,)
    new_message_payload = proto.Field(
        proto.MESSAGE, number=4, oneof="payload", message=participant.Message,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
