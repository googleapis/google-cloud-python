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

from google.cloud.dialogflow_v2beta1.types import participant

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "Conversation",
        "ConversationPhoneNumber",
        "CreateConversationRequest",
        "ListConversationsRequest",
        "ListConversationsResponse",
        "GetConversationRequest",
        "CompleteConversationRequest",
        "CreateMessageRequest",
        "BatchCreateMessagesRequest",
        "BatchCreateMessagesResponse",
        "ListMessagesRequest",
        "ListMessagesResponse",
        "SuggestConversationSummaryRequest",
        "SuggestConversationSummaryResponse",
    },
)


class Conversation(proto.Message):
    r"""Represents a conversation.
    A conversation is an interaction between an agent, including
    live agents and Dialogflow agents, and a support customer.
    Conversations can include phone calls and text-based chat
    sessions.

    Attributes:
        name (str):
            Output only. The unique identifier of this conversation.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        lifecycle_state (google.cloud.dialogflow_v2beta1.types.Conversation.LifecycleState):
            Output only. The current state of the
            Conversation.
        conversation_profile (str):
            Required. The Conversation Profile to be used to configure
            this Conversation. This field cannot be updated. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversationProfiles/<Conversation Profile ID>``.
        phone_number (google.cloud.dialogflow_v2beta1.types.ConversationPhoneNumber):
            Output only. Required if the conversation is
            to be connected over telephony.
        conversation_stage (google.cloud.dialogflow_v2beta1.types.Conversation.ConversationStage):
            The stage of a conversation. It indicates whether the
            virtual agent or a human agent is handling the conversation.

            If the conversation is created with the conversation profile
            that has Dialogflow config set, defaults to
            [ConversationStage.VIRTUAL_AGENT_STAGE][google.cloud.dialogflow.v2beta1.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE];
            Otherwise, defaults to
            [ConversationStage.HUMAN_ASSIST_STAGE][google.cloud.dialogflow.v2beta1.Conversation.ConversationStage.HUMAN_ASSIST_STAGE].

            If the conversation is created with the conversation profile
            that has Dialogflow config set but explicitly sets
            conversation_stage to
            [ConversationStage.HUMAN_ASSIST_STAGE][google.cloud.dialogflow.v2beta1.Conversation.ConversationStage.HUMAN_ASSIST_STAGE],
            it skips
            [ConversationStage.VIRTUAL_AGENT_STAGE][google.cloud.dialogflow.v2beta1.Conversation.ConversationStage.VIRTUAL_AGENT_STAGE]
            stage and directly goes to
            [ConversationStage.HUMAN_ASSIST_STAGE][google.cloud.dialogflow.v2beta1.Conversation.ConversationStage.HUMAN_ASSIST_STAGE].
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the conversation was
            started.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the conversation was
            finished.
    """

    class LifecycleState(proto.Enum):
        r"""Enumeration of the completion status of the conversation."""
        LIFECYCLE_STATE_UNSPECIFIED = 0
        IN_PROGRESS = 1
        COMPLETED = 2

    class ConversationStage(proto.Enum):
        r"""Enumeration of the different conversation stages a
        conversation can be in. Reference:
        https://cloud.google.com/dialogflow/priv/docs/contact-center/basics#stages
        """
        CONVERSATION_STAGE_UNSPECIFIED = 0
        VIRTUAL_AGENT_STAGE = 1
        HUMAN_ASSIST_STAGE = 2

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    lifecycle_state: LifecycleState = proto.Field(
        proto.ENUM,
        number=2,
        enum=LifecycleState,
    )
    conversation_profile: str = proto.Field(
        proto.STRING,
        number=3,
    )
    phone_number: "ConversationPhoneNumber" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="ConversationPhoneNumber",
    )
    conversation_stage: ConversationStage = proto.Field(
        proto.ENUM,
        number=7,
        enum=ConversationStage,
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


class ConversationPhoneNumber(proto.Message):
    r"""Represents a phone number for telephony integration. It
    allows for connecting a particular conversation over telephony.

    Attributes:
        phone_number (str):
            Output only. The phone number to connect to
            this conversation.
    """

    phone_number: str = proto.Field(
        proto.STRING,
        number=3,
    )


class CreateConversationRequest(proto.Message):
    r"""The request message for
    [Conversations.CreateConversation][google.cloud.dialogflow.v2beta1.Conversations.CreateConversation].

    Attributes:
        parent (str):
            Required. Resource identifier of the project creating the
            conversation. Format:
            ``projects/<Project ID>/locations/<Location ID>``.
        conversation (google.cloud.dialogflow_v2beta1.types.Conversation):
            Required. The conversation to create.
        conversation_id (str):
            Optional. Identifier of the conversation. Generally it's
            auto generated by Google. Only set it if you cannot wait for
            the response to return a auto-generated one to you.

            The conversation ID must be compliant with the regression
            fomula "[a-zA-Z][a-zA-Z0-9_-]*" with the characters length
            in range of [3,64]. If the field is provided, the caller is
            resposible for

            1. the uniqueness of the ID, otherwise the request will be
               rejected.
            2. the consistency for whether to use custom ID or not under
               a project to better ensure uniqueness.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    conversation: "Conversation" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Conversation",
    )
    conversation_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListConversationsRequest(proto.Message):
    r"""The request message for
    [Conversations.ListConversations][google.cloud.dialogflow.v2beta1.Conversations.ListConversations].

    Attributes:
        parent (str):
            Required. The project from which to list all conversation.
            Format: ``projects/<Project ID>/locations/<Location ID>``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
        filter (str):
            A filter expression that filters conversations listed in the
            response. In general, the expression must specify the field
            name, a comparison operator, and the value to use for
            filtering:

            .. raw:: html

                <ul>
                  <li>The value must be a string, a number, or a boolean.</li>
                  <li>The comparison operator must be either `=`,`!=`, `>`, or `<`.</li>
                  <li>To filter on multiple expressions, separate the
                      expressions with `AND` or `OR` (omitting both implies `AND`).</li>
                  <li>For clarity, expressions can be enclosed in parentheses.</li>
                </ul>
                Only `lifecycle_state` can be filtered on in this way. For example,
                the following expression only returns `COMPLETED` conversations:

            ``lifecycle_state = "COMPLETED"``

            For more information about filtering, see `API
            Filtering <https://aip.dev/160>`__.
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
    r"""The response message for
    [Conversations.ListConversations][google.cloud.dialogflow.v2beta1.Conversations.ListConversations].

    Attributes:
        conversations (MutableSequence[google.cloud.dialogflow_v2beta1.types.Conversation]):
            The list of conversations. There will be a maximum number of
            items returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
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


class GetConversationRequest(proto.Message):
    r"""The request message for
    [Conversations.GetConversation][google.cloud.dialogflow.v2beta1.Conversations.GetConversation].

    Attributes:
        name (str):
            Required. The name of the conversation. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CompleteConversationRequest(proto.Message):
    r"""The request message for
    [Conversations.CompleteConversation][google.cloud.dialogflow.v2beta1.Conversations.CompleteConversation].

    Attributes:
        name (str):
            Required. Resource identifier of the conversation to close.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class CreateMessageRequest(proto.Message):
    r"""The request message to create one Message. Currently it is
    only used in BatchCreateMessagesRequest.

    Attributes:
        parent (str):
            Required. Resource identifier of the conversation to create
            message. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        message (google.cloud.dialogflow_v2beta1.types.Message):
            Required. The message to create.
            [Message.participant][google.cloud.dialogflow.v2beta1.Message.participant]
            is required.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    message: participant.Message = proto.Field(
        proto.MESSAGE,
        number=2,
        message=participant.Message,
    )


class BatchCreateMessagesRequest(proto.Message):
    r"""The request message for
    [Conversations.BatchCreateMessagesRequest][].

    Attributes:
        parent (str):
            Required. Resource identifier of the conversation to create
            message. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        requests (MutableSequence[google.cloud.dialogflow_v2beta1.types.CreateMessageRequest]):
            Required. A maximum of 1000 Messages can be created in a
            batch. [CreateMessageRequest.message.send_time][] is
            required. All created messages will have identical
            [Message.create_time][google.cloud.dialogflow.v2beta1.Message.create_time].
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    requests: MutableSequence["CreateMessageRequest"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="CreateMessageRequest",
    )


class BatchCreateMessagesResponse(proto.Message):
    r"""The request message for
    [Conversations.BatchCreateMessagesResponse][].

    Attributes:
        messages (MutableSequence[google.cloud.dialogflow_v2beta1.types.Message]):
            Messages created.
    """

    messages: MutableSequence[participant.Message] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=participant.Message,
    )


class ListMessagesRequest(proto.Message):
    r"""The request message for
    [Conversations.ListMessages][google.cloud.dialogflow.v2beta1.Conversations.ListMessages].

    Attributes:
        parent (str):
            Required. The name of the conversation to list messages for.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``
        filter (str):
            Optional. Filter on message fields. Currently predicates on
            ``create_time`` and ``create_time_epoch_microseconds`` are
            supported. ``create_time`` only support milliseconds
            accuracy. E.g.,
            ``create_time_epoch_microseconds > 1551790877964485`` or
            ``create_time > "2017-01-15T01:30:15.01Z"``.

            For more information about filtering, see `API
            Filtering <https://aip.dev/160>`__.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListMessagesResponse(proto.Message):
    r"""The response message for
    [Conversations.ListMessages][google.cloud.dialogflow.v2beta1.Conversations.ListMessages].

    Attributes:
        messages (MutableSequence[google.cloud.dialogflow_v2beta1.types.Message]):
            Required. The list of messages. There will be a maximum
            number of items returned based on the page_size field in the
            request. ``messages`` is sorted by ``create_time`` in
            descending order.
        next_page_token (str):
            Optional. Token to retrieve the next page of
            results, or empty if there are no more results
            in the list.
    """

    @property
    def raw_page(self):
        return self

    messages: MutableSequence[participant.Message] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=participant.Message,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SuggestConversationSummaryRequest(proto.Message):
    r"""The request message for
    [Conversations.SuggestConversationSummary][google.cloud.dialogflow.v2beta1.Conversations.SuggestConversationSummary].

    Attributes:
        conversation (str):
            Required. The conversation to fetch suggestion for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        latest_message (str):
            The name of the latest conversation message used as context
            for compiling suggestion. If empty, the latest message of
            the conversation will be used.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Max number of messages prior to and including
            [latest_message] to use as context when compiling the
            suggestion. By default 500 and at most 1000.
    """

    conversation: str = proto.Field(
        proto.STRING,
        number=1,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=3,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=4,
    )


class SuggestConversationSummaryResponse(proto.Message):
    r"""The response message for
    [Conversations.SuggestConversationSummary][google.cloud.dialogflow.v2beta1.Conversations.SuggestConversationSummary].

    Attributes:
        summary (google.cloud.dialogflow_v2beta1.types.SuggestConversationSummaryResponse.Summary):
            Generated summary.
        latest_message (str):
            The name of the latest conversation message used as context
            for compiling suggestion.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [last_conversation_message][] used to compile the
            suggestion. It may be smaller than the
            [SuggestSummaryRequest.context_size][] field in the request
            if there weren't that many messages in the conversation.
    """

    class Summary(proto.Message):
        r"""Generated summary for a conversation.

        Attributes:
            text (str):
                The summary content that is concatenated into
                one string.
            text_sections (MutableMapping[str, str]):
                The summary content that is divided into
                sections. The key is the section's name and the
                value is the section's content. There is no
                specific format for the key or value.
            answer_record (str):
                The name of the answer record. Format:
                "projects/<Project ID>/answerRecords/<Answer
                Record ID>".
        """

        text: str = proto.Field(
            proto.STRING,
            number=1,
        )
        text_sections: MutableMapping[str, str] = proto.MapField(
            proto.STRING,
            proto.STRING,
            number=4,
        )
        answer_record: str = proto.Field(
            proto.STRING,
            number=3,
        )

    summary: Summary = proto.Field(
        proto.MESSAGE,
        number=1,
        message=Summary,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
