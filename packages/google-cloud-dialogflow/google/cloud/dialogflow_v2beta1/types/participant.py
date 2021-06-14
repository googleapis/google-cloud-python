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

from google.cloud.dialogflow_v2beta1.types import audio_config
from google.cloud.dialogflow_v2beta1.types import session
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "Participant",
        "Message",
        "CreateParticipantRequest",
        "GetParticipantRequest",
        "ListParticipantsRequest",
        "ListParticipantsResponse",
        "UpdateParticipantRequest",
        "OutputAudio",
        "AutomatedAgentReply",
        "SuggestionFeature",
        "AnalyzeContentRequest",
        "DtmfParameters",
        "AnalyzeContentResponse",
        "AnnotatedMessagePart",
        "MessageAnnotation",
        "ArticleAnswer",
        "FaqAnswer",
        "SmartReplyAnswer",
        "SuggestionResult",
        "SuggestArticlesRequest",
        "SuggestArticlesResponse",
        "SuggestFaqAnswersRequest",
        "SuggestFaqAnswersResponse",
        "SuggestSmartRepliesRequest",
        "SuggestSmartRepliesResponse",
        "Suggestion",
        "ListSuggestionsRequest",
        "ListSuggestionsResponse",
        "CompileSuggestionRequest",
        "CompileSuggestionResponse",
        "ResponseMessage",
    },
)


class Participant(proto.Message):
    r"""Represents a conversation participant (human agent, virtual
    agent, end-user).

    Attributes:
        name (str):
            Optional. The unique identifier of this participant. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        role (google.cloud.dialogflow_v2beta1.types.Participant.Role):
            Immutable. The role this participant plays in
            the conversation. This field must be set during
            participant creation and is then immutable.
        obfuscated_external_user_id (str):
            Optional. Obfuscated user id that should be associated with
            the created participant.

            You can specify a user id as follows:

            1. If you set this field in
               [CreateParticipantRequest][google.cloud.dialogflow.v2beta1.CreateParticipantRequest.participant]
               or
               [UpdateParticipantRequest][google.cloud.dialogflow.v2beta1.UpdateParticipantRequest.participant],
               Dialogflow adds the obfuscated user id with the
               participant.

            2. If you set this field in
               [AnalyzeContent][google.cloud.dialogflow.v2beta1.AnalyzeContentRequest.obfuscated_external_user_id]
               or
               [StreamingAnalyzeContent][google.cloud.dialogflow.v2beta1.StreamingAnalyzeContentRequest.obfuscated_external_user_id],
               Dialogflow will update
               [Participant.obfuscated_external_user_id][google.cloud.dialogflow.v2beta1.Participant.obfuscated_external_user_id].

            Dialogflow uses this user id for following purposes:

            1) Billing and measurement. If user with the same
               obfuscated_external_user_id is created in a later
               conversation, dialogflow will know it's the same user. 2)
               Agent assist suggestion personalization. For example,
               Dialogflow can use it to provide personalized smart reply
               suggestions for this user.

            Note:

            -  Please never pass raw user ids to Dialogflow. Always
               obfuscate your user id first.
            -  Dialogflow only accepts a UTF-8 encoded string, e.g., a
               hex digest of a hash function like SHA-512.
            -  The length of the user id must be <= 256 characters.
    """

    class Role(proto.Enum):
        r"""Enumeration of the roles a participant can play in a
        conversation.
        """
        ROLE_UNSPECIFIED = 0
        HUMAN_AGENT = 1
        AUTOMATED_AGENT = 2
        END_USER = 3

    name = proto.Field(proto.STRING, number=1,)
    role = proto.Field(proto.ENUM, number=2, enum=Role,)
    obfuscated_external_user_id = proto.Field(proto.STRING, number=7,)


class Message(proto.Message):
    r"""Represents a message posted into a conversation.
    Attributes:
        name (str):
            Optional. The unique identifier of the message. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        content (str):
            Required. The message content.
        language_code (str):
            Optional. The message language. This should be a
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tag. Example: "en-US".
        participant (str):
            Output only. The participant that sends this
            message.
        participant_role (google.cloud.dialogflow_v2beta1.types.Participant.Role):
            Output only. The role of the participant.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the message was
            created in Contact Center AI.
        send_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The time when the message was sent.
        message_annotation (google.cloud.dialogflow_v2beta1.types.MessageAnnotation):
            Output only. The annotation for the message.
        sentiment_analysis (google.cloud.dialogflow_v2beta1.types.SentimentAnalysisResult):
            Output only. The sentiment analysis result
            for the message.
    """

    name = proto.Field(proto.STRING, number=1,)
    content = proto.Field(proto.STRING, number=2,)
    language_code = proto.Field(proto.STRING, number=3,)
    participant = proto.Field(proto.STRING, number=4,)
    participant_role = proto.Field(proto.ENUM, number=5, enum="Participant.Role",)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    send_time = proto.Field(proto.MESSAGE, number=9, message=timestamp_pb2.Timestamp,)
    message_annotation = proto.Field(
        proto.MESSAGE, number=7, message="MessageAnnotation",
    )
    sentiment_analysis = proto.Field(
        proto.MESSAGE, number=8, message=session.SentimentAnalysisResult,
    )


class CreateParticipantRequest(proto.Message):
    r"""The request message for
    [Participants.CreateParticipant][google.cloud.dialogflow.v2beta1.Participants.CreateParticipant].

    Attributes:
        parent (str):
            Required. Resource identifier of the conversation adding the
            participant. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        participant (google.cloud.dialogflow_v2beta1.types.Participant):
            Required. The participant to create.
    """

    parent = proto.Field(proto.STRING, number=1,)
    participant = proto.Field(proto.MESSAGE, number=2, message="Participant",)


class GetParticipantRequest(proto.Message):
    r"""The request message for
    [Participants.GetParticipant][google.cloud.dialogflow.v2beta1.Participants.GetParticipant].

    Attributes:
        name (str):
            Required. The name of the participant. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListParticipantsRequest(proto.Message):
    r"""The request message for
    [Participants.ListParticipants][google.cloud.dialogflow.v2beta1.Participants.ListParticipants].

    Attributes:
        parent (str):
            Required. The conversation to list all participants from.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. By default 100 and at
            most 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)


class ListParticipantsResponse(proto.Message):
    r"""The response message for
    [Participants.ListParticipants][google.cloud.dialogflow.v2beta1.Participants.ListParticipants].

    Attributes:
        participants (Sequence[google.cloud.dialogflow_v2beta1.types.Participant]):
            The list of participants. There is a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results or
            empty if there are no more results in the list.
    """

    @property
    def raw_page(self):
        return self

    participants = proto.RepeatedField(proto.MESSAGE, number=1, message="Participant",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class UpdateParticipantRequest(proto.Message):
    r"""The request message for
    [Participants.UpdateParticipant][google.cloud.dialogflow.v2beta1.Participants.UpdateParticipant].

    Attributes:
        participant (google.cloud.dialogflow_v2beta1.types.Participant):
            Required. The participant to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The mask to specify which fields to
            update.
    """

    participant = proto.Field(proto.MESSAGE, number=1, message="Participant",)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class OutputAudio(proto.Message):
    r"""Represents the natural language speech audio to be played to
    the end user.

    Attributes:
        config (google.cloud.dialogflow_v2beta1.types.OutputAudioConfig):
            Required. Instructs the speech synthesizer
            how to generate the speech audio.
        audio (bytes):
            Required. The natural language speech audio.
    """

    config = proto.Field(
        proto.MESSAGE, number=1, message=audio_config.OutputAudioConfig,
    )
    audio = proto.Field(proto.BYTES, number=2,)


class AutomatedAgentReply(proto.Message):
    r"""Represents a response from an automated agent.
    Attributes:
        detect_intent_response (google.cloud.dialogflow_v2beta1.types.DetectIntentResponse):
            Response of the Dialogflow
            [Sessions.DetectIntent][google.cloud.dialogflow.v2beta1.Sessions.DetectIntent]
            call.
        response_messages (Sequence[google.cloud.dialogflow_v2beta1.types.ResponseMessage]):
            Response messages from the automated agent.
        intent (str):
            Name of the intent if an intent is matched for the query.
            For a V2 query, the value format is
            ``projects/<Project ID>/locations/ <Location ID>/agent/intents/<Intent ID>``.
            For a V3 query, the value format is
            ``projects/<Project ID>/locations/ <Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
        event (str):
            Event name if an event is triggered for the
            query.
        match_confidence (float):
            The confidence of the match. Values range
            from 0.0 (completely uncertain) to 1.0
            (completely certain). This value is for
            informational purpose only and is only used to
            help match the best intent within the
            classification threshold. This value may change
            for the same end-user expression at any time due
            to a model retraining or change in
            implementation.
        parameters (google.protobuf.struct_pb2.Struct):
            The collection of current parameters at the
            time of this response.
        cx_session_parameters (google.protobuf.struct_pb2.Struct):
            The collection of current Dialogflow CX agent session
            parameters at the time of this response. Deprecated: Use
            ``parameters`` instead.
        automated_agent_reply_type (google.cloud.dialogflow_v2beta1.types.AutomatedAgentReply.AutomatedAgentReplyType):
            AutomatedAgentReply type.
        allow_cancellation (bool):
            Indicates whether the partial automated agent
            reply is interruptible when a later reply
            message arrives. e.g. if the agent specified
            some music as partial response, it can be
            cancelled.
    """

    class AutomatedAgentReplyType(proto.Enum):
        r"""Represents different automated agent reply types."""
        AUTOMATED_AGENT_REPLY_TYPE_UNSPECIFIED = 0
        PARTIAL = 1
        FINAL = 2

    detect_intent_response = proto.Field(
        proto.MESSAGE, number=1, oneof="response", message=session.DetectIntentResponse,
    )
    response_messages = proto.RepeatedField(
        proto.MESSAGE, number=3, message="ResponseMessage",
    )
    intent = proto.Field(proto.STRING, number=4, oneof="match",)
    event = proto.Field(proto.STRING, number=5, oneof="match",)
    match_confidence = proto.Field(proto.FLOAT, number=9,)
    parameters = proto.Field(proto.MESSAGE, number=10, message=struct_pb2.Struct,)
    cx_session_parameters = proto.Field(
        proto.MESSAGE, number=6, message=struct_pb2.Struct,
    )
    automated_agent_reply_type = proto.Field(
        proto.ENUM, number=7, enum=AutomatedAgentReplyType,
    )
    allow_cancellation = proto.Field(proto.BOOL, number=8,)


class SuggestionFeature(proto.Message):
    r"""The type of Human Agent Assistant API suggestion to perform, and the
    maximum number of results to return for that type. Multiple
    ``Feature`` objects can be specified in the ``features`` list.

    Attributes:
        type_ (google.cloud.dialogflow_v2beta1.types.SuggestionFeature.Type):
            Type of Human Agent Assistant API feature to
            request.
    """

    class Type(proto.Enum):
        r"""Defines the type of Human Agent Assistant feature."""
        TYPE_UNSPECIFIED = 0
        ARTICLE_SUGGESTION = 1
        FAQ = 2
        SMART_REPLY = 3

    type_ = proto.Field(proto.ENUM, number=1, enum=Type,)


class AnalyzeContentRequest(proto.Message):
    r"""The request message for
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent].

    Attributes:
        participant (str):
            Required. The name of the participant this text comes from.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        text_input (google.cloud.dialogflow_v2beta1.types.TextInput):
            The natural language text to be processed.
        event_input (google.cloud.dialogflow_v2beta1.types.EventInput):
            An input event to send to Dialogflow.
        reply_audio_config (google.cloud.dialogflow_v2beta1.types.OutputAudioConfig):
            Speech synthesis configuration.
            The speech synthesis settings for a virtual
            agent that may be configured for the associated
            conversation profile are not used when calling
            AnalyzeContent. If this configuration is not
            supplied, speech synthesis is disabled.
        query_params (google.cloud.dialogflow_v2beta1.types.QueryParameters):
            Parameters for a Dialogflow virtual-agent
            query.
        message_send_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The send time of the message from
            end user or human agent's perspective. It is
            used for identifying the same message under one
            participant.

            Given two messages under the same participant:
            - If send time are different regardless of
            whether the content of the  messages are exactly
            the same, the conversation will regard them as
            two distinct messages sent by the participant.
            - If send time is the same regardless of whether
            the content of the  messages are exactly the
            same, the conversation will regard them as  same
            message, and ignore the message received later.
            If the value is not provided, a new request will
            always be regarded as a new message without any
            de-duplication.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if a ``request_id`` is provided.
    """

    participant = proto.Field(proto.STRING, number=1,)
    text_input = proto.Field(
        proto.MESSAGE, number=6, oneof="input", message=session.TextInput,
    )
    event_input = proto.Field(
        proto.MESSAGE, number=8, oneof="input", message=session.EventInput,
    )
    reply_audio_config = proto.Field(
        proto.MESSAGE, number=5, message=audio_config.OutputAudioConfig,
    )
    query_params = proto.Field(
        proto.MESSAGE, number=9, message=session.QueryParameters,
    )
    message_send_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp_pb2.Timestamp,
    )
    request_id = proto.Field(proto.STRING, number=11,)


class DtmfParameters(proto.Message):
    r"""The message in the response that indicates the parameters of
    DTMF.

    Attributes:
        accepts_dtmf_input (bool):
            Indicates whether DTMF input can be handled
            in the next request.
    """

    accepts_dtmf_input = proto.Field(proto.BOOL, number=1,)


class AnalyzeContentResponse(proto.Message):
    r"""The response message for
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent].

    Attributes:
        reply_text (str):
            Output only. The output text content.
            This field is set if the automated agent
            responded with text to show to the user.
        reply_audio (google.cloud.dialogflow_v2beta1.types.OutputAudio):
            Optional. The audio data bytes encoded as specified in the
            request. This field is set if:

            -  ``reply_audio_config`` was specified in the request, or
            -  The automated agent responded with audio to play to the
               user. In such case, ``reply_audio.config`` contains
               settings used to synthesize the speech.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        automated_agent_reply (google.cloud.dialogflow_v2beta1.types.AutomatedAgentReply):
            Optional. Only set if a Dialogflow automated agent has
            responded. Note that:
            [AutomatedAgentReply.detect_intent_response.output_audio][]
            and
            [AutomatedAgentReply.detect_intent_response.output_audio_config][]
            are always empty, use
            [reply_audio][google.cloud.dialogflow.v2beta1.AnalyzeContentResponse.reply_audio]
            instead.
        message (google.cloud.dialogflow_v2beta1.types.Message):
            Output only. Message analyzed by CCAI.
        human_agent_suggestion_results (Sequence[google.cloud.dialogflow_v2beta1.types.SuggestionResult]):
            The suggestions for most recent human agent. The order is
            the same as
            [HumanAgentAssistantConfig.SuggestionConfig.feature_configs][google.cloud.dialogflow.v2beta1.HumanAgentAssistantConfig.SuggestionConfig.feature_configs]
            of
            [HumanAgentAssistantConfig.human_agent_suggestion_config][google.cloud.dialogflow.v2beta1.HumanAgentAssistantConfig.human_agent_suggestion_config].
        end_user_suggestion_results (Sequence[google.cloud.dialogflow_v2beta1.types.SuggestionResult]):
            The suggestions for end user. The order is the same as
            [HumanAgentAssistantConfig.SuggestionConfig.feature_configs][google.cloud.dialogflow.v2beta1.HumanAgentAssistantConfig.SuggestionConfig.feature_configs]
            of
            [HumanAgentAssistantConfig.end_user_suggestion_config][google.cloud.dialogflow.v2beta1.HumanAgentAssistantConfig.end_user_suggestion_config].
        dtmf_parameters (google.cloud.dialogflow_v2beta1.types.DtmfParameters):
            Indicates the parameters of DTMF.
    """

    reply_text = proto.Field(proto.STRING, number=1,)
    reply_audio = proto.Field(proto.MESSAGE, number=2, message="OutputAudio",)
    automated_agent_reply = proto.Field(
        proto.MESSAGE, number=3, message="AutomatedAgentReply",
    )
    message = proto.Field(proto.MESSAGE, number=5, message="Message",)
    human_agent_suggestion_results = proto.RepeatedField(
        proto.MESSAGE, number=6, message="SuggestionResult",
    )
    end_user_suggestion_results = proto.RepeatedField(
        proto.MESSAGE, number=7, message="SuggestionResult",
    )
    dtmf_parameters = proto.Field(proto.MESSAGE, number=9, message="DtmfParameters",)


class AnnotatedMessagePart(proto.Message):
    r"""Represents a part of a message possibly annotated with an
    entity. The part can be an entity or purely a part of the
    message between two entities or message start/end.

    Attributes:
        text (str):
            Required. A part of a message possibly
            annotated with an entity.
        entity_type (str):
            Optional. The `Dialogflow system entity
            type <https://cloud.google.com/dialogflow/docs/reference/system-entities>`__
            of this message part. If this is empty, Dialogflow could not
            annotate the phrase part with a system entity.
        formatted_value (google.protobuf.struct_pb2.Value):
            Optional. The `Dialogflow system entity formatted
            value <https://cloud.google.com/dialogflow/docs/reference/system-entities>`__
            of this message part. For example for a system entity of
            type ``@sys.unit-currency``, this may contain:

            .. raw:: html

                <pre>
                {
                  "amount": 5,
                  "currency": "USD"
                }
                </pre>
    """

    text = proto.Field(proto.STRING, number=1,)
    entity_type = proto.Field(proto.STRING, number=2,)
    formatted_value = proto.Field(proto.MESSAGE, number=3, message=struct_pb2.Value,)


class MessageAnnotation(proto.Message):
    r"""Represents the result of annotation for the message.
    Attributes:
        parts (Sequence[google.cloud.dialogflow_v2beta1.types.AnnotatedMessagePart]):
            Optional. The collection of annotated message parts ordered
            by their position in the message. You can recover the
            annotated message by concatenating
            [AnnotatedMessagePart.text].
        contain_entities (bool):
            Required. Indicates whether the text message
            contains entities.
    """

    parts = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AnnotatedMessagePart",
    )
    contain_entities = proto.Field(proto.BOOL, number=2,)


class ArticleAnswer(proto.Message):
    r"""Represents article answer.
    Attributes:
        title (str):
            The article title.
        uri (str):
            The article URI.
        snippets (Sequence[str]):
            Output only. Article snippets.
        metadata (Sequence[google.cloud.dialogflow_v2beta1.types.ArticleAnswer.MetadataEntry]):
            A map that contains metadata about the answer
            and the document from which it originates.
        answer_record (str):
            The name of answer record, in the format of
            "projects/<Project ID>/locations/<Location
            ID>/answerRecords/<Answer Record ID>".
    """

    title = proto.Field(proto.STRING, number=1,)
    uri = proto.Field(proto.STRING, number=2,)
    snippets = proto.RepeatedField(proto.STRING, number=3,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=5,)
    answer_record = proto.Field(proto.STRING, number=6,)


class FaqAnswer(proto.Message):
    r"""Represents answer from "frequently asked questions".
    Attributes:
        answer (str):
            The piece of text from the ``source`` knowledge base
            document.
        confidence (float):
            The system's confidence score that this
            Knowledge answer is a good match for this
            conversational query, range from 0.0 (completely
            uncertain) to 1.0 (completely certain).
        question (str):
            The corresponding FAQ question.
        source (str):
            Indicates which Knowledge Document this answer was extracted
            from. Format:
            ``projects/<Project ID>/locations/<Location ID>/agent/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
        metadata (Sequence[google.cloud.dialogflow_v2beta1.types.FaqAnswer.MetadataEntry]):
            A map that contains metadata about the answer
            and the document from which it originates.
        answer_record (str):
            The name of answer record, in the format of
            "projects/<Project ID>/locations/<Location
            ID>/answerRecords/<Answer Record ID>".
    """

    answer = proto.Field(proto.STRING, number=1,)
    confidence = proto.Field(proto.FLOAT, number=2,)
    question = proto.Field(proto.STRING, number=3,)
    source = proto.Field(proto.STRING, number=4,)
    metadata = proto.MapField(proto.STRING, proto.STRING, number=5,)
    answer_record = proto.Field(proto.STRING, number=6,)


class SmartReplyAnswer(proto.Message):
    r"""Represents a smart reply answer.
    Attributes:
        reply (str):
            The content of the reply.
        confidence (float):
            Smart reply confidence.
            The system's confidence score that this reply is
            a good match for this conversation, as a value
            from 0.0 (completely uncertain) to 1.0
            (completely certain).
        answer_record (str):
            The name of answer record, in the format of
            "projects/<Project ID>/locations/<Location
            ID>/answerRecords/<Answer Record ID>".
    """

    reply = proto.Field(proto.STRING, number=1,)
    confidence = proto.Field(proto.FLOAT, number=2,)
    answer_record = proto.Field(proto.STRING, number=3,)


class SuggestionResult(proto.Message):
    r"""One response of different type of suggestion response which is used
    in the response of
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent]
    and
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent],
    as well as
    [HumanAgentAssistantEvent][google.cloud.dialogflow.v2beta1.HumanAgentAssistantEvent].

    Attributes:
        error (google.rpc.status_pb2.Status):
            Error status if the request failed.
        suggest_articles_response (google.cloud.dialogflow_v2beta1.types.SuggestArticlesResponse):
            SuggestArticlesResponse if request is for
            ARTICLE_SUGGESTION.
        suggest_faq_answers_response (google.cloud.dialogflow_v2beta1.types.SuggestFaqAnswersResponse):
            SuggestFaqAnswersResponse if request is for FAQ_ANSWER.
        suggest_smart_replies_response (google.cloud.dialogflow_v2beta1.types.SuggestSmartRepliesResponse):
            SuggestSmartRepliesResponse if request is for SMART_REPLY.
    """

    error = proto.Field(
        proto.MESSAGE, number=1, oneof="suggestion_response", message=status_pb2.Status,
    )
    suggest_articles_response = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="suggestion_response",
        message="SuggestArticlesResponse",
    )
    suggest_faq_answers_response = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="suggestion_response",
        message="SuggestFaqAnswersResponse",
    )
    suggest_smart_replies_response = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="suggestion_response",
        message="SuggestSmartRepliesResponse",
    )


class SuggestArticlesRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestArticles][google.cloud.dialogflow.v2beta1.Participants.SuggestArticles].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestion
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        latest_message (str):
            Optional. The name of the latest conversation message to
            compile suggestion for. If empty, it will be the latest
            message of the conversation.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Optional. Max number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2beta1.SuggestArticlesRequest.latest_message]
            to use as context when compiling the suggestion. By default
            20 and at most 50.
    """

    parent = proto.Field(proto.STRING, number=1,)
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class SuggestArticlesResponse(proto.Message):
    r"""The response message for
    [Participants.SuggestArticles][google.cloud.dialogflow.v2beta1.Participants.SuggestArticles].

    Attributes:
        article_answers (Sequence[google.cloud.dialogflow_v2beta1.types.ArticleAnswer]):
            Output only. Articles ordered by score in
            descending order.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2beta1.SuggestArticlesResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestArticlesResponse.context_size][google.cloud.dialogflow.v2beta1.SuggestArticlesResponse.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    article_answers = proto.RepeatedField(
        proto.MESSAGE, number=1, message="ArticleAnswer",
    )
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class SuggestFaqAnswersRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2beta1.Participants.SuggestFaqAnswers].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestion
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        latest_message (str):
            Optional. The name of the latest conversation message to
            compile suggestion for. If empty, it will be the latest
            message of the conversation.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Optional. Max number of messages prior to and including
            [latest_message] to use as context when compiling the
            suggestion. By default 20 and at most 50.
    """

    parent = proto.Field(proto.STRING, number=1,)
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class SuggestFaqAnswersResponse(proto.Message):
    r"""The request message for
    [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2beta1.Participants.SuggestFaqAnswers].

    Attributes:
        faq_answers (Sequence[google.cloud.dialogflow_v2beta1.types.FaqAnswer]):
            Output only. Answers extracted from FAQ
            documents.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2beta1.SuggestFaqAnswersResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestFaqAnswersRequest.context_size][google.cloud.dialogflow.v2beta1.SuggestFaqAnswersRequest.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    faq_answers = proto.RepeatedField(proto.MESSAGE, number=1, message="FaqAnswer",)
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class SuggestSmartRepliesRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestSmartReplies][google.cloud.dialogflow.v2beta1.Participants.SuggestSmartReplies].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestion
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        current_text_input (google.cloud.dialogflow_v2beta1.types.TextInput):
            The current natural language text segment to
            compile suggestion for. This provides a way for
            user to get follow up smart reply suggestion
            after a smart reply selection, without sending a
            text message.
        latest_message (str):
            The name of the latest conversation message to compile
            suggestion for. If empty, it will be the latest message of
            the conversation.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Optional. Max number of messages prior to and including
            [latest_message] to use as context when compiling the
            suggestion. By default 20 and at most 50.
    """

    parent = proto.Field(proto.STRING, number=1,)
    current_text_input = proto.Field(
        proto.MESSAGE, number=4, message=session.TextInput,
    )
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class SuggestSmartRepliesResponse(proto.Message):
    r"""The response message for
    [Participants.SuggestSmartReplies][google.cloud.dialogflow.v2beta1.Participants.SuggestSmartReplies].

    Attributes:
        smart_reply_answers (Sequence[google.cloud.dialogflow_v2beta1.types.SmartReplyAnswer]):
            Output only. Multiple reply options provided
            by smart reply service. The order is based on
            the rank of the model prediction. The maximum
            number of the returned replies is set in
            SmartReplyConfig.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2beta1.SuggestSmartRepliesResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestSmartRepliesRequest.context_size][google.cloud.dialogflow.v2beta1.SuggestSmartRepliesRequest.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    smart_reply_answers = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SmartReplyAnswer",
    )
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class Suggestion(proto.Message):
    r"""Represents a suggestion for a human agent.
    Attributes:
        name (str):
            Output only. The name of this suggestion. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/*/suggestions/<Suggestion ID>``.
        articles (Sequence[google.cloud.dialogflow_v2beta1.types.Suggestion.Article]):
            Output only. Articles ordered by score in
            descending order.
        faq_answers (Sequence[google.cloud.dialogflow_v2beta1.types.Suggestion.FaqAnswer]):
            Output only. Answers extracted from FAQ
            documents.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the suggestion was
            created.
        latest_message (str):
            Output only. Latest message used as context to compile this
            suggestion.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
    """

    class Article(proto.Message):
        r"""Represents suggested article.
        Attributes:
            title (str):
                Output only. The article title.
            uri (str):
                Output only. The article URI.
            snippets (Sequence[str]):
                Output only. Article snippets.
            metadata (Sequence[google.cloud.dialogflow_v2beta1.types.Suggestion.Article.MetadataEntry]):
                Output only. A map that contains metadata
                about the answer and the document from which it
                originates.
            answer_record (str):
                Output only. The name of answer record, in
                the format of "projects/<Project
                ID>/locations/<Location
                ID>/answerRecords/<Answer Record ID>".
        """

        title = proto.Field(proto.STRING, number=1,)
        uri = proto.Field(proto.STRING, number=2,)
        snippets = proto.RepeatedField(proto.STRING, number=3,)
        metadata = proto.MapField(proto.STRING, proto.STRING, number=5,)
        answer_record = proto.Field(proto.STRING, number=6,)

    class FaqAnswer(proto.Message):
        r"""Represents suggested answer from "frequently asked
        questions".

        Attributes:
            answer (str):
                Output only. The piece of text from the ``source`` knowledge
                base document.
            confidence (float):
                The system's confidence score that this
                Knowledge answer is a good match for this
                conversational query, range from 0.0 (completely
                uncertain) to 1.0 (completely certain).
            question (str):
                Output only. The corresponding FAQ question.
            source (str):
                Output only. Indicates which Knowledge Document this answer
                was extracted from. Format:
                ``projects/<Project ID>/locations/<Location ID>/agent/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
            metadata (Sequence[google.cloud.dialogflow_v2beta1.types.Suggestion.FaqAnswer.MetadataEntry]):
                Output only. A map that contains metadata
                about the answer and the document from which it
                originates.
            answer_record (str):
                Output only. The name of answer record, in
                the format of "projects/<Project
                ID>/locations/<Location
                ID>/answerRecords/<Answer Record ID>".
        """

        answer = proto.Field(proto.STRING, number=1,)
        confidence = proto.Field(proto.FLOAT, number=2,)
        question = proto.Field(proto.STRING, number=3,)
        source = proto.Field(proto.STRING, number=4,)
        metadata = proto.MapField(proto.STRING, proto.STRING, number=5,)
        answer_record = proto.Field(proto.STRING, number=6,)

    name = proto.Field(proto.STRING, number=1,)
    articles = proto.RepeatedField(proto.MESSAGE, number=2, message=Article,)
    faq_answers = proto.RepeatedField(proto.MESSAGE, number=4, message=FaqAnswer,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    latest_message = proto.Field(proto.STRING, number=7,)


class ListSuggestionsRequest(proto.Message):
    r"""The request message for
    [Participants.ListSuggestions][google.cloud.dialogflow.v2beta1.Participants.ListSuggestions].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestions
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        page_size (int):
            Optional. The maximum number of items to
            return in a single page. The default value is
            100; the maximum value is 1000.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            list request.
        filter (str):
            Optional. Filter on suggestions fields. Currently predicates
            on ``create_time`` and ``create_time_epoch_microseconds``
            are supported. ``create_time`` only support milliseconds
            accuracy. E.g.,
            ``create_time_epoch_microseconds > 1551790877964485`` or
            ``create_time > "2017-01-15T01:30:15.01Z"``

            For more information about filtering, see `API
            Filtering <https://aip.dev/160>`__.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)


class ListSuggestionsResponse(proto.Message):
    r"""The response message for
    [Participants.ListSuggestions][google.cloud.dialogflow.v2beta1.Participants.ListSuggestions].

    Attributes:
        suggestions (Sequence[google.cloud.dialogflow_v2beta1.types.Suggestion]):
            Required. The list of suggestions. There will be a maximum
            number of items returned based on the page_size field in the
            request. ``suggestions`` is sorted by ``create_time`` in
            descending order.
        next_page_token (str):
            Optional. Token to retrieve the next page of
            results or empty if there are no more results in
            the list.
    """

    @property
    def raw_page(self):
        return self

    suggestions = proto.RepeatedField(proto.MESSAGE, number=1, message="Suggestion",)
    next_page_token = proto.Field(proto.STRING, number=2,)


class CompileSuggestionRequest(proto.Message):
    r"""The request message for
    [Participants.CompileSuggestion][google.cloud.dialogflow.v2beta1.Participants.CompileSuggestion].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestion
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        latest_message (str):
            Optional. The name of the latest conversation message to
            compile suggestion for. If empty, it will be the latest
            message of the conversation.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Optional. Max number of messages prior to and including
            [latest_message] to use as context when compiling the
            suggestion. If zero or less than zero, 20 is used.
    """

    parent = proto.Field(proto.STRING, number=1,)
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class CompileSuggestionResponse(proto.Message):
    r"""The response message for
    [Participants.CompileSuggestion][google.cloud.dialogflow.v2beta1.Participants.CompileSuggestion].

    Attributes:
        suggestion (google.cloud.dialogflow_v2beta1.types.Suggestion):
            The compiled suggestion.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2beta1.CompileSuggestionResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [CompileSuggestionRequest.context_size][google.cloud.dialogflow.v2beta1.CompileSuggestionRequest.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    suggestion = proto.Field(proto.MESSAGE, number=1, message="Suggestion",)
    latest_message = proto.Field(proto.STRING, number=2,)
    context_size = proto.Field(proto.INT32, number=3,)


class ResponseMessage(proto.Message):
    r"""Response messages from an automated agent.
    Attributes:
        text (google.cloud.dialogflow_v2beta1.types.ResponseMessage.Text):
            Returns a text response.
        payload (google.protobuf.struct_pb2.Struct):
            Returns a response containing a custom,
            platform-specific payload.
        live_agent_handoff (google.cloud.dialogflow_v2beta1.types.ResponseMessage.LiveAgentHandoff):
            Hands off conversation to a live agent.
        end_interaction (google.cloud.dialogflow_v2beta1.types.ResponseMessage.EndInteraction):
            A signal that indicates the interaction with
            the Dialogflow agent has ended.
    """

    class Text(proto.Message):
        r"""The text response message.
        Attributes:
            text (Sequence[str]):
                A collection of text responses.
        """

        text = proto.RepeatedField(proto.STRING, number=1,)

    class LiveAgentHandoff(proto.Message):
        r"""Indicates that the conversation should be handed off to a human
        agent.

        Dialogflow only uses this to determine which conversations were
        handed off to a human agent for measurement purposes. What else to
        do with this signal is up to you and your handoff procedures.

        You may set this, for example:

        -  In the entry fulfillment of a CX Page if entering the page
           indicates something went extremely wrong in the conversation.
        -  In a webhook response when you determine that the customer issue
           can only be handled by a human.

        Attributes:
            metadata (google.protobuf.struct_pb2.Struct):
                Custom metadata for your handoff procedure.
                Dialogflow doesn't impose any structure on this.
        """

        metadata = proto.Field(proto.MESSAGE, number=1, message=struct_pb2.Struct,)

    class EndInteraction(proto.Message):
        r"""Indicates that interaction with the Dialogflow agent has
        ended.
            """

    text = proto.Field(proto.MESSAGE, number=1, oneof="message", message=Text,)
    payload = proto.Field(
        proto.MESSAGE, number=2, oneof="message", message=struct_pb2.Struct,
    )
    live_agent_handoff = proto.Field(
        proto.MESSAGE, number=3, oneof="message", message=LiveAgentHandoff,
    )
    end_interaction = proto.Field(
        proto.MESSAGE, number=4, oneof="message", message=EndInteraction,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
