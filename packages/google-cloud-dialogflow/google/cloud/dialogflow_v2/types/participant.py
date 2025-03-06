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

from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
import proto  # type: ignore

from google.cloud.dialogflow_v2.types import audio_config as gcd_audio_config
from google.cloud.dialogflow_v2.types import generator, session

__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2",
    manifest={
        "Participant",
        "Message",
        "CreateParticipantRequest",
        "GetParticipantRequest",
        "ListParticipantsRequest",
        "ListParticipantsResponse",
        "UpdateParticipantRequest",
        "AnalyzeContentRequest",
        "DtmfParameters",
        "AnalyzeContentResponse",
        "StreamingAnalyzeContentRequest",
        "StreamingAnalyzeContentResponse",
        "SuggestArticlesRequest",
        "SuggestArticlesResponse",
        "SuggestFaqAnswersRequest",
        "SuggestFaqAnswersResponse",
        "GenerateSuggestionsResponse",
        "SuggestSmartRepliesRequest",
        "SuggestSmartRepliesResponse",
        "AudioInput",
        "OutputAudio",
        "AutomatedAgentReply",
        "ArticleAnswer",
        "FaqAnswer",
        "SmartReplyAnswer",
        "IntentSuggestion",
        "DialogflowAssistAnswer",
        "SuggestionResult",
        "InputTextConfig",
        "AnnotatedMessagePart",
        "MessageAnnotation",
        "SuggestionInput",
        "AssistQueryParameters",
        "SuggestKnowledgeAssistRequest",
        "SuggestKnowledgeAssistResponse",
        "KnowledgeAssistAnswer",
    },
)


class Participant(proto.Message):
    r"""Represents a conversation participant (human agent, virtual
    agent, end-user).

    Attributes:
        name (str):
            Optional. The unique identifier of this participant. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        role (google.cloud.dialogflow_v2.types.Participant.Role):
            Immutable. The role this participant plays in
            the conversation. This field must be set during
            participant creation and is then immutable.
        sip_recording_media_label (str):
            Optional. Label applied to streams
            representing this participant in SIPREC XML
            metadata and SDP. This is used to assign
            transcriptions from that media stream to this
            participant. This field can be updated.
        obfuscated_external_user_id (str):
            Optional. Obfuscated user id that should be associated with
            the created participant.

            You can specify a user id as follows:

            1. If you set this field in
               [CreateParticipantRequest][google.cloud.dialogflow.v2.CreateParticipantRequest.participant]
               or
               [UpdateParticipantRequest][google.cloud.dialogflow.v2.UpdateParticipantRequest.participant],
               Dialogflow adds the obfuscated user id with the
               participant.

            2. If you set this field in
               [AnalyzeContent][google.cloud.dialogflow.v2.AnalyzeContentRequest.participant]
               or
               [StreamingAnalyzeContent][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.participant],
               Dialogflow will update
               [Participant.obfuscated_external_user_id][google.cloud.dialogflow.v2.Participant.obfuscated_external_user_id].

            Dialogflow returns an error if you try to add a user id for
            a
            non-[END_USER][google.cloud.dialogflow.v2.Participant.Role.END_USER]
            participant.

            Dialogflow uses this user id for billing and measurement
            purposes. For example, Dialogflow determines whether a user
            in one conversation returned in a later conversation.

            Note:

            -  Please never pass raw user ids to Dialogflow. Always
               obfuscate your user id first.
            -  Dialogflow only accepts a UTF-8 encoded string, e.g., a
               hex digest of a hash function like SHA-512.
            -  The length of the user id must be <= 256 characters.
        documents_metadata_filters (MutableMapping[str, str]):
            Optional. Key-value filters on the metadata of documents
            returned by article suggestion. If specified, article
            suggestion only returns suggested documents that match all
            filters in their
            [Document.metadata][google.cloud.dialogflow.v2.Document.metadata].
            Multiple values for a metadata key should be concatenated by
            comma. For example, filters to match all documents that have
            'US' or 'CA' in their market metadata values and 'agent' in
            their user metadata values will be

            ::

               documents_metadata_filters {
                 key: "market"
                 value: "US,CA"
               }
               documents_metadata_filters {
                 key: "user"
                 value: "agent"
               }
    """

    class Role(proto.Enum):
        r"""Enumeration of the roles a participant can play in a
        conversation.

        Values:
            ROLE_UNSPECIFIED (0):
                Participant role not set.
            HUMAN_AGENT (1):
                Participant is a human agent.
            AUTOMATED_AGENT (2):
                Participant is an automated agent, such as a
                Dialogflow agent.
            END_USER (3):
                Participant is an end user that has called or
                chatted with Dialogflow services.
        """
        ROLE_UNSPECIFIED = 0
        HUMAN_AGENT = 1
        AUTOMATED_AGENT = 2
        END_USER = 3

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    role: Role = proto.Field(
        proto.ENUM,
        number=2,
        enum=Role,
    )
    sip_recording_media_label: str = proto.Field(
        proto.STRING,
        number=6,
    )
    obfuscated_external_user_id: str = proto.Field(
        proto.STRING,
        number=7,
    )
    documents_metadata_filters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=8,
    )


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
        participant_role (google.cloud.dialogflow_v2.types.Participant.Role):
            Output only. The role of the participant.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the message was
            created in Contact Center AI.
        send_time (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The time when the message was sent.
            For voice messages, this is the time when an
            utterance started.
        message_annotation (google.cloud.dialogflow_v2.types.MessageAnnotation):
            Output only. The annotation for the message.
        sentiment_analysis (google.cloud.dialogflow_v2.types.SentimentAnalysisResult):
            Output only. The sentiment analysis result
            for the message.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    content: str = proto.Field(
        proto.STRING,
        number=2,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    participant: str = proto.Field(
        proto.STRING,
        number=4,
    )
    participant_role: "Participant.Role" = proto.Field(
        proto.ENUM,
        number=5,
        enum="Participant.Role",
    )
    create_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=6,
        message=timestamp_pb2.Timestamp,
    )
    send_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    message_annotation: "MessageAnnotation" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="MessageAnnotation",
    )
    sentiment_analysis: session.SentimentAnalysisResult = proto.Field(
        proto.MESSAGE,
        number=8,
        message=session.SentimentAnalysisResult,
    )


class CreateParticipantRequest(proto.Message):
    r"""The request message for
    [Participants.CreateParticipant][google.cloud.dialogflow.v2.Participants.CreateParticipant].

    Attributes:
        parent (str):
            Required. Resource identifier of the conversation adding the
            participant. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>``.
        participant (google.cloud.dialogflow_v2.types.Participant):
            Required. The participant to create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    participant: "Participant" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="Participant",
    )


class GetParticipantRequest(proto.Message):
    r"""The request message for
    [Participants.GetParticipant][google.cloud.dialogflow.v2.Participants.GetParticipant].

    Attributes:
        name (str):
            Required. The name of the participant. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListParticipantsRequest(proto.Message):
    r"""The request message for
    [Participants.ListParticipants][google.cloud.dialogflow.v2.Participants.ListParticipants].

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


class ListParticipantsResponse(proto.Message):
    r"""The response message for
    [Participants.ListParticipants][google.cloud.dialogflow.v2.Participants.ListParticipants].

    Attributes:
        participants (MutableSequence[google.cloud.dialogflow_v2.types.Participant]):
            The list of participants. There is a maximum number of items
            returned based on the page_size field in the request.
        next_page_token (str):
            Token to retrieve the next page of results or
            empty if there are no more results in the list.
    """

    @property
    def raw_page(self):
        return self

    participants: MutableSequence["Participant"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Participant",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdateParticipantRequest(proto.Message):
    r"""The request message for
    [Participants.UpdateParticipant][google.cloud.dialogflow.v2.Participants.UpdateParticipant].

    Attributes:
        participant (google.cloud.dialogflow_v2.types.Participant):
            Required. The participant to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. The mask to specify which fields to
            update.
    """

    participant: "Participant" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="Participant",
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class AnalyzeContentRequest(proto.Message):
    r"""The request message for
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        participant (str):
            Required. The name of the participant this text comes from.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        text_input (google.cloud.dialogflow_v2.types.TextInput):
            The natural language text to be processed.

            This field is a member of `oneof`_ ``input``.
        audio_input (google.cloud.dialogflow_v2.types.AudioInput):
            The natural language speech audio to be
            processed.

            This field is a member of `oneof`_ ``input``.
        event_input (google.cloud.dialogflow_v2.types.EventInput):
            An input event to send to Dialogflow.

            This field is a member of `oneof`_ ``input``.
        suggestion_input (google.cloud.dialogflow_v2.types.SuggestionInput):
            An input representing the selection of a
            suggestion.

            This field is a member of `oneof`_ ``input``.
        reply_audio_config (google.cloud.dialogflow_v2.types.OutputAudioConfig):
            Speech synthesis configuration.
            The speech synthesis settings for a virtual
            agent that may be configured for the associated
            conversation profile are not used when calling
            AnalyzeContent. If this configuration is not
            supplied, speech synthesis is disabled.
        query_params (google.cloud.dialogflow_v2.types.QueryParameters):
            Parameters for a Dialogflow virtual-agent
            query.
        assist_query_params (google.cloud.dialogflow_v2.types.AssistQueryParameters):
            Parameters for a human assist query.
        cx_parameters (google.protobuf.struct_pb2.Struct):
            Additional parameters to be put into
            Dialogflow CX session parameters. To remove a
            parameter from the session, clients should
            explicitly set the parameter value to null.

            Note: this field should only be used if you are
            connecting to a Dialogflow CX agent.
        request_id (str):
            A unique identifier for this request. Restricted to 36 ASCII
            characters. A random UUID is recommended. This request is
            only idempotent if a ``request_id`` is provided.
    """

    participant: str = proto.Field(
        proto.STRING,
        number=1,
    )
    text_input: session.TextInput = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="input",
        message=session.TextInput,
    )
    audio_input: "AudioInput" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="input",
        message="AudioInput",
    )
    event_input: session.EventInput = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="input",
        message=session.EventInput,
    )
    suggestion_input: "SuggestionInput" = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="input",
        message="SuggestionInput",
    )
    reply_audio_config: gcd_audio_config.OutputAudioConfig = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gcd_audio_config.OutputAudioConfig,
    )
    query_params: session.QueryParameters = proto.Field(
        proto.MESSAGE,
        number=9,
        message=session.QueryParameters,
    )
    assist_query_params: "AssistQueryParameters" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="AssistQueryParameters",
    )
    cx_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=18,
        message=struct_pb2.Struct,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=11,
    )


class DtmfParameters(proto.Message):
    r"""The message in the response that indicates the parameters of
    DTMF.

    Attributes:
        accepts_dtmf_input (bool):
            Indicates whether DTMF input can be handled
            in the next request.
    """

    accepts_dtmf_input: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


class AnalyzeContentResponse(proto.Message):
    r"""The response message for
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent].

    Attributes:
        reply_text (str):
            The output text content.
            This field is set if the automated agent
            responded with text to show to the user.
        reply_audio (google.cloud.dialogflow_v2.types.OutputAudio):
            The audio data bytes encoded as specified in the request.
            This field is set if:

            -  ``reply_audio_config`` was specified in the request, or
            -  The automated agent responded with audio to play to the
               user. In such case, ``reply_audio.config`` contains
               settings used to synthesize the speech.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        automated_agent_reply (google.cloud.dialogflow_v2.types.AutomatedAgentReply):
            Only set if a Dialogflow automated agent has responded. Note
            that in [AutomatedAgentReply.DetectIntentResponse][],
            [Sessions.DetectIntentResponse.output_audio][] and
            [Sessions.DetectIntentResponse.output_audio_config][] are
            always empty, use
            [reply_audio][google.cloud.dialogflow.v2.AnalyzeContentResponse.reply_audio]
            instead.
        message (google.cloud.dialogflow_v2.types.Message):
            Message analyzed by CCAI.
        human_agent_suggestion_results (MutableSequence[google.cloud.dialogflow_v2.types.SuggestionResult]):
            The suggestions for most recent human agent. The order is
            the same as
            [HumanAgentAssistantConfig.SuggestionConfig.feature_configs][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.SuggestionConfig.feature_configs]
            of
            [HumanAgentAssistantConfig.human_agent_suggestion_config][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.human_agent_suggestion_config].

            Note that any failure of Agent Assist features will not lead
            to the overall failure of an AnalyzeContent API call.
            Instead, the features will fail silently with the error
            field set in the corresponding SuggestionResult.
        end_user_suggestion_results (MutableSequence[google.cloud.dialogflow_v2.types.SuggestionResult]):
            The suggestions for end user. The order is the same as
            [HumanAgentAssistantConfig.SuggestionConfig.feature_configs][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.SuggestionConfig.feature_configs]
            of
            [HumanAgentAssistantConfig.end_user_suggestion_config][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.end_user_suggestion_config].

            Same as human_agent_suggestion_results, any failure of Agent
            Assist features will not lead to the overall failure of an
            AnalyzeContent API call. Instead, the features will fail
            silently with the error field set in the corresponding
            SuggestionResult.
        dtmf_parameters (google.cloud.dialogflow_v2.types.DtmfParameters):
            Indicates the parameters of DTMF.
    """

    reply_text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    reply_audio: "OutputAudio" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="OutputAudio",
    )
    automated_agent_reply: "AutomatedAgentReply" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AutomatedAgentReply",
    )
    message: "Message" = proto.Field(
        proto.MESSAGE,
        number=5,
        message="Message",
    )
    human_agent_suggestion_results: MutableSequence[
        "SuggestionResult"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="SuggestionResult",
    )
    end_user_suggestion_results: MutableSequence[
        "SuggestionResult"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="SuggestionResult",
    )
    dtmf_parameters: "DtmfParameters" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="DtmfParameters",
    )


class StreamingAnalyzeContentRequest(proto.Message):
    r"""The top-level message sent by the client to the
    [Participants.StreamingAnalyzeContent][google.cloud.dialogflow.v2.Participants.StreamingAnalyzeContent]
    method.

    Multiple request messages should be sent in order:

    1. The first message must contain
       [participant][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.participant],
       [config][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.config]
       and optionally
       [query_params][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.query_params].
       If you want to receive an audio response, it should also contain
       [reply_audio_config][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.reply_audio_config].
       The message must not contain
       [input][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.input].

    2. If
       [config][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.config]
       in the first message was set to
       [audio_config][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.audio_config],
       all subsequent messages must contain
       [input_audio][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.input_audio]
       to continue with Speech recognition. However, note that:

       -  Dialogflow will bill you for the audio so far.
       -  Dialogflow discards all Speech recognition results in favor of
          the text input.

    3. If
       [StreamingAnalyzeContentRequest.config][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.config]
       in the first message was set to
       [StreamingAnalyzeContentRequest.text_config][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.text_config],
       then the second message must contain only
       [input_text][google.cloud.dialogflow.v2.StreamingAnalyzeContentRequest.input_text].
       Moreover, you must not send more than two messages.

    After you sent all input, you must half-close or abort the request
    stream.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        participant (str):
            Required. The name of the participant this text comes from.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        audio_config (google.cloud.dialogflow_v2.types.InputAudioConfig):
            Instructs the speech recognizer how to
            process the speech audio.

            This field is a member of `oneof`_ ``config``.
        text_config (google.cloud.dialogflow_v2.types.InputTextConfig):
            The natural language text to be processed.

            This field is a member of `oneof`_ ``config``.
        reply_audio_config (google.cloud.dialogflow_v2.types.OutputAudioConfig):
            Speech synthesis configuration.
            The speech synthesis settings for a virtual
            agent that may be configured for the associated
            conversation profile are not used when calling
            StreamingAnalyzeContent. If this configuration
            is not supplied, speech synthesis is disabled.
        input_audio (bytes):
            The input audio content to be recognized. Must be sent if
            ``audio_config`` is set in the first message. The complete
            audio over all streaming messages must not exceed 1 minute.

            This field is a member of `oneof`_ ``input``.
        input_text (str):
            The UTF-8 encoded natural language text to be processed.
            Must be sent if ``text_config`` is set in the first message.
            Text length must not exceed 256 bytes for virtual agent
            interactions. The ``input_text`` field can be only sent
            once, and would cancel the speech recognition if any
            ongoing.

            This field is a member of `oneof`_ ``input``.
        input_dtmf (google.cloud.dialogflow_v2.types.TelephonyDtmfEvents):
            The DTMF digits used to invoke intent and
            fill in parameter value.
            This input is ignored if the previous response
            indicated that DTMF input is not accepted.

            This field is a member of `oneof`_ ``input``.
        query_params (google.cloud.dialogflow_v2.types.QueryParameters):
            Parameters for a Dialogflow virtual-agent
            query.
        assist_query_params (google.cloud.dialogflow_v2.types.AssistQueryParameters):
            Parameters for a human assist query.
        cx_parameters (google.protobuf.struct_pb2.Struct):
            Additional parameters to be put into
            Dialogflow CX session parameters. To remove a
            parameter from the session, clients should
            explicitly set the parameter value to null.

            Note: this field should only be used if you are
            connecting to a Dialogflow CX agent.
        enable_extended_streaming (bool):
            Optional. Enable full bidirectional streaming. You can keep
            streaming the audio until timeout, and there's no need to
            half close the stream to get the response.

            Restrictions:

            -  Timeout: 3 mins.
            -  Audio Encoding: only supports
               [AudioEncoding.AUDIO_ENCODING_LINEAR_16][google.cloud.dialogflow.v2.AudioEncoding.AUDIO_ENCODING_LINEAR_16]
               and
               [AudioEncoding.AUDIO_ENCODING_MULAW][google.cloud.dialogflow.v2.AudioEncoding.AUDIO_ENCODING_MULAW]
            -  Lifecycle: conversation should be in ``Assist Stage``, go
               to
               [Conversations.CreateConversation][google.cloud.dialogflow.v2.Conversations.CreateConversation]
               for more information.

            InvalidArgument Error will be returned if the one of
            restriction checks failed.

            You can find more details in
            https://cloud.google.com/agent-assist/docs/extended-streaming
        enable_partial_automated_agent_reply (bool):
            Optional. Enable partial responses from Dialogflow CX agent.
            If this flag is not enabled, response stream still contains
            only one final response even if some ``Fulfillment``\ s in
            Dialogflow CX agent have been configured to return partial
            responses.
        enable_debugging_info (bool):
            If true, ``StreamingAnalyzeContentResponse.debugging_info``
            will get populated.
    """

    participant: str = proto.Field(
        proto.STRING,
        number=1,
    )
    audio_config: gcd_audio_config.InputAudioConfig = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="config",
        message=gcd_audio_config.InputAudioConfig,
    )
    text_config: "InputTextConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="config",
        message="InputTextConfig",
    )
    reply_audio_config: gcd_audio_config.OutputAudioConfig = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gcd_audio_config.OutputAudioConfig,
    )
    input_audio: bytes = proto.Field(
        proto.BYTES,
        number=5,
        oneof="input",
    )
    input_text: str = proto.Field(
        proto.STRING,
        number=6,
        oneof="input",
    )
    input_dtmf: gcd_audio_config.TelephonyDtmfEvents = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="input",
        message=gcd_audio_config.TelephonyDtmfEvents,
    )
    query_params: session.QueryParameters = proto.Field(
        proto.MESSAGE,
        number=7,
        message=session.QueryParameters,
    )
    assist_query_params: "AssistQueryParameters" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="AssistQueryParameters",
    )
    cx_parameters: struct_pb2.Struct = proto.Field(
        proto.MESSAGE,
        number=13,
        message=struct_pb2.Struct,
    )
    enable_extended_streaming: bool = proto.Field(
        proto.BOOL,
        number=11,
    )
    enable_partial_automated_agent_reply: bool = proto.Field(
        proto.BOOL,
        number=12,
    )
    enable_debugging_info: bool = proto.Field(
        proto.BOOL,
        number=19,
    )


class StreamingAnalyzeContentResponse(proto.Message):
    r"""The top-level message returned from the ``StreamingAnalyzeContent``
    method.

    Multiple response messages can be returned in order:

    1. If the input was set to streaming audio, the first one or more
       messages contain ``recognition_result``. Each
       ``recognition_result`` represents a more complete transcript of
       what the user said. The last ``recognition_result`` has
       ``is_final`` set to ``true``.

    2. In virtual agent stage: if
       ``enable_partial_automated_agent_reply`` is true, the following N
       (currently 1 <= N <= 4) messages contain
       ``automated_agent_reply`` and optionally ``reply_audio`` returned
       by the virtual agent. The first (N-1)
       ``automated_agent_reply``\ s will have
       ``automated_agent_reply_type`` set to ``PARTIAL``. The last
       ``automated_agent_reply`` has ``automated_agent_reply_type`` set
       to ``FINAL``. If ``enable_partial_automated_agent_reply`` is not
       enabled, response stream only contains the final reply.

       In human assist stage: the following N (N >= 1) messages contain
       ``human_agent_suggestion_results``,
       ``end_user_suggestion_results`` or ``message``.

    Attributes:
        recognition_result (google.cloud.dialogflow_v2.types.StreamingRecognitionResult):
            The result of speech recognition.
        reply_text (str):
            The output text content.
            This field is set if an automated agent
            responded with a text for the user.
        reply_audio (google.cloud.dialogflow_v2.types.OutputAudio):
            The audio data bytes encoded as specified in the request.
            This field is set if:

            -  The ``reply_audio_config`` field is specified in the
               request.
            -  The automated agent, which this output comes from,
               responded with audio. In such case, the
               ``reply_audio.config`` field contains settings used to
               synthesize the speech.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        automated_agent_reply (google.cloud.dialogflow_v2.types.AutomatedAgentReply):
            Note that in [AutomatedAgentReply.DetectIntentResponse][],
            [Sessions.DetectIntentResponse.output_audio][] and
            [Sessions.DetectIntentResponse.output_audio_config][] are
            always empty, use
            [reply_audio][google.cloud.dialogflow.v2.StreamingAnalyzeContentResponse.reply_audio]
            instead.
        message (google.cloud.dialogflow_v2.types.Message):
            Message analyzed by CCAI.
        human_agent_suggestion_results (MutableSequence[google.cloud.dialogflow_v2.types.SuggestionResult]):
            The suggestions for most recent human agent. The order is
            the same as
            [HumanAgentAssistantConfig.SuggestionConfig.feature_configs][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.SuggestionConfig.feature_configs]
            of
            [HumanAgentAssistantConfig.human_agent_suggestion_config][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.human_agent_suggestion_config].
        end_user_suggestion_results (MutableSequence[google.cloud.dialogflow_v2.types.SuggestionResult]):
            The suggestions for end user. The order is the same as
            [HumanAgentAssistantConfig.SuggestionConfig.feature_configs][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.SuggestionConfig.feature_configs]
            of
            [HumanAgentAssistantConfig.end_user_suggestion_config][google.cloud.dialogflow.v2.HumanAgentAssistantConfig.end_user_suggestion_config].
        dtmf_parameters (google.cloud.dialogflow_v2.types.DtmfParameters):
            Indicates the parameters of DTMF.
        debugging_info (google.cloud.dialogflow_v2.types.CloudConversationDebuggingInfo):
            Debugging info that would get populated when
            ``StreamingAnalyzeContentRequest.enable_debugging_info`` is
            set to true.
        speech_model (str):
            The name of the actual Cloud speech model
            used for speech recognition.
    """

    recognition_result: session.StreamingRecognitionResult = proto.Field(
        proto.MESSAGE,
        number=1,
        message=session.StreamingRecognitionResult,
    )
    reply_text: str = proto.Field(
        proto.STRING,
        number=2,
    )
    reply_audio: "OutputAudio" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="OutputAudio",
    )
    automated_agent_reply: "AutomatedAgentReply" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AutomatedAgentReply",
    )
    message: "Message" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="Message",
    )
    human_agent_suggestion_results: MutableSequence[
        "SuggestionResult"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="SuggestionResult",
    )
    end_user_suggestion_results: MutableSequence[
        "SuggestionResult"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="SuggestionResult",
    )
    dtmf_parameters: "DtmfParameters" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="DtmfParameters",
    )
    debugging_info: session.CloudConversationDebuggingInfo = proto.Field(
        proto.MESSAGE,
        number=11,
        message=session.CloudConversationDebuggingInfo,
    )
    speech_model: str = proto.Field(
        proto.STRING,
        number=13,
    )


class SuggestArticlesRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestArticles][google.cloud.dialogflow.v2.Participants.SuggestArticles].

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
            [latest_message][google.cloud.dialogflow.v2.SuggestArticlesRequest.latest_message]
            to use as context when compiling the suggestion. By default
            20 and at most 50.
        assist_query_params (google.cloud.dialogflow_v2.types.AssistQueryParameters):
            Parameters for a human assist query.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    assist_query_params: "AssistQueryParameters" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AssistQueryParameters",
    )


class SuggestArticlesResponse(proto.Message):
    r"""The response message for
    [Participants.SuggestArticles][google.cloud.dialogflow.v2.Participants.SuggestArticles].

    Attributes:
        article_answers (MutableSequence[google.cloud.dialogflow_v2.types.ArticleAnswer]):
            Articles ordered by score in descending
            order.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2.SuggestArticlesResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestArticlesRequest.context_size][google.cloud.dialogflow.v2.SuggestArticlesRequest.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    article_answers: MutableSequence["ArticleAnswer"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ArticleAnswer",
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class SuggestFaqAnswersRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2.Participants.SuggestFaqAnswers].

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
        assist_query_params (google.cloud.dialogflow_v2.types.AssistQueryParameters):
            Parameters for a human assist query.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    assist_query_params: "AssistQueryParameters" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="AssistQueryParameters",
    )


class SuggestFaqAnswersResponse(proto.Message):
    r"""The request message for
    [Participants.SuggestFaqAnswers][google.cloud.dialogflow.v2.Participants.SuggestFaqAnswers].

    Attributes:
        faq_answers (MutableSequence[google.cloud.dialogflow_v2.types.FaqAnswer]):
            Answers extracted from FAQ documents.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2.SuggestFaqAnswersResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestFaqAnswersRequest.context_size][google.cloud.dialogflow.v2.SuggestFaqAnswersRequest.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    faq_answers: MutableSequence["FaqAnswer"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="FaqAnswer",
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class GenerateSuggestionsResponse(proto.Message):
    r"""The response message for
    [Conversations.GenerateSuggestions][google.cloud.dialogflow.v2.Conversations.GenerateSuggestions].

    Attributes:
        generator_suggestion_answers (MutableSequence[google.cloud.dialogflow_v2.types.GenerateSuggestionsResponse.GeneratorSuggestionAnswer]):
            The answers generated for the conversation
            based on context.
        latest_message (str):
            The name of the latest conversation message used as context
            for compiling suggestion.

            Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
    """

    class GeneratorSuggestionAnswer(proto.Message):
        r"""A GeneratorSuggestion answer.

        Attributes:
            generator_suggestion (google.cloud.dialogflow_v2.types.GeneratorSuggestion):
                Suggestion details.
            source_generator (str):
                The name of the generator used to generate this suggestion.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/generators/<Generator ID>``.
            answer_record (str):
                Answer record that uniquely identifies the
                suggestion. This can be used to provide
                suggestion feedback.
        """

        generator_suggestion: generator.GeneratorSuggestion = proto.Field(
            proto.MESSAGE,
            number=1,
            message=generator.GeneratorSuggestion,
        )
        source_generator: str = proto.Field(
            proto.STRING,
            number=2,
        )
        answer_record: str = proto.Field(
            proto.STRING,
            number=3,
        )

    generator_suggestion_answers: MutableSequence[
        GeneratorSuggestionAnswer
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=GeneratorSuggestionAnswer,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SuggestSmartRepliesRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestSmartReplies][google.cloud.dialogflow.v2.Participants.SuggestSmartReplies].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestion
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        current_text_input (google.cloud.dialogflow_v2.types.TextInput):
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
            Max number of messages prior to and including
            [latest_message] to use as context when compiling the
            suggestion. By default 20 and at most 50.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    current_text_input: session.TextInput = proto.Field(
        proto.MESSAGE,
        number=4,
        message=session.TextInput,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class SuggestSmartRepliesResponse(proto.Message):
    r"""The response message for
    [Participants.SuggestSmartReplies][google.cloud.dialogflow.v2.Participants.SuggestSmartReplies].

    Attributes:
        smart_reply_answers (MutableSequence[google.cloud.dialogflow_v2.types.SmartReplyAnswer]):
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
            [latest_message][google.cloud.dialogflow.v2.SuggestSmartRepliesResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestSmartRepliesRequest.context_size][google.cloud.dialogflow.v2.SuggestSmartRepliesRequest.context_size]
            field in the request if there aren't that many messages in
            the conversation.
    """

    smart_reply_answers: MutableSequence["SmartReplyAnswer"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="SmartReplyAnswer",
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class AudioInput(proto.Message):
    r"""Represents the natural language speech audio to be processed.

    Attributes:
        config (google.cloud.dialogflow_v2.types.InputAudioConfig):
            Required. Instructs the speech recognizer how
            to process the speech audio.
        audio (bytes):
            Required. The natural language speech audio
            to be processed. A single request can contain up
            to 2 minutes of speech audio data. The
            transcribed text cannot contain more than 256
            bytes for virtual agent interactions.
    """

    config: gcd_audio_config.InputAudioConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_audio_config.InputAudioConfig,
    )
    audio: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class OutputAudio(proto.Message):
    r"""Represents the natural language speech audio to be played to
    the end user.

    Attributes:
        config (google.cloud.dialogflow_v2.types.OutputAudioConfig):
            Instructs the speech synthesizer how to
            generate the speech audio.
        audio (bytes):
            The natural language speech audio.
    """

    config: gcd_audio_config.OutputAudioConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcd_audio_config.OutputAudioConfig,
    )
    audio: bytes = proto.Field(
        proto.BYTES,
        number=2,
    )


class AutomatedAgentReply(proto.Message):
    r"""Represents a response from an automated agent.

    Attributes:
        detect_intent_response (google.cloud.dialogflow_v2.types.DetectIntentResponse):
            Response of the Dialogflow
            [Sessions.DetectIntent][google.cloud.dialogflow.v2.Sessions.DetectIntent]
            call.
        automated_agent_reply_type (google.cloud.dialogflow_v2.types.AutomatedAgentReply.AutomatedAgentReplyType):
            AutomatedAgentReply type.
        allow_cancellation (bool):
            Indicates whether the partial automated agent
            reply is interruptible when a later reply
            message arrives. e.g. if the agent specified
            some music as partial response, it can be
            cancelled.
        cx_current_page (str):
            The unique identifier of the current Dialogflow CX
            conversation page. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
    """

    class AutomatedAgentReplyType(proto.Enum):
        r"""Represents different automated agent reply types.

        Values:
            AUTOMATED_AGENT_REPLY_TYPE_UNSPECIFIED (0):
                Not specified. This should never happen.
            PARTIAL (1):
                Partial reply. e.g. Aggregated responses in a
                ``Fulfillment`` that enables ``return_partial_response`` can
                be returned as partial reply. WARNING: partial reply is not
                eligible for barge-in.
            FINAL (2):
                Final reply.
        """
        AUTOMATED_AGENT_REPLY_TYPE_UNSPECIFIED = 0
        PARTIAL = 1
        FINAL = 2

    detect_intent_response: session.DetectIntentResponse = proto.Field(
        proto.MESSAGE,
        number=1,
        message=session.DetectIntentResponse,
    )
    automated_agent_reply_type: AutomatedAgentReplyType = proto.Field(
        proto.ENUM,
        number=7,
        enum=AutomatedAgentReplyType,
    )
    allow_cancellation: bool = proto.Field(
        proto.BOOL,
        number=8,
    )
    cx_current_page: str = proto.Field(
        proto.STRING,
        number=11,
    )


class ArticleAnswer(proto.Message):
    r"""Represents article answer.

    Attributes:
        title (str):
            The article title.
        uri (str):
            The article URI.
        snippets (MutableSequence[str]):
            Article snippets.
        confidence (float):
            Article match confidence.
            The system's confidence score that this article
            is a good match for this conversation, as a
            value from 0.0 (completely uncertain) to 1.0
            (completely certain).
        metadata (MutableMapping[str, str]):
            A map that contains metadata about the answer
            and the document from which it originates.
        answer_record (str):
            The name of answer record, in the format of
            "projects/<Project ID>/locations/<Location
            ID>/answerRecords/<Answer Record ID>".
    """

    title: str = proto.Field(
        proto.STRING,
        number=1,
    )
    uri: str = proto.Field(
        proto.STRING,
        number=2,
    )
    snippets: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    confidence: float = proto.Field(
        proto.FLOAT,
        number=4,
    )
    metadata: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    answer_record: str = proto.Field(
        proto.STRING,
        number=6,
    )


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
        metadata (MutableMapping[str, str]):
            A map that contains metadata about the answer
            and the document from which it originates.
        answer_record (str):
            The name of answer record, in the format of
            "projects/<Project ID>/locations/<Location
            ID>/answerRecords/<Answer Record ID>".
    """

    answer: str = proto.Field(
        proto.STRING,
        number=1,
    )
    confidence: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    question: str = proto.Field(
        proto.STRING,
        number=3,
    )
    source: str = proto.Field(
        proto.STRING,
        number=4,
    )
    metadata: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    answer_record: str = proto.Field(
        proto.STRING,
        number=6,
    )


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

    reply: str = proto.Field(
        proto.STRING,
        number=1,
    )
    confidence: float = proto.Field(
        proto.FLOAT,
        number=2,
    )
    answer_record: str = proto.Field(
        proto.STRING,
        number=3,
    )


class IntentSuggestion(proto.Message):
    r"""Represents an intent suggestion.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        display_name (str):
            The display name of the intent.
        intent_v2 (str):
            The unique identifier of this
            [intent][google.cloud.dialogflow.v2.Intent]. Format:
            ``projects/<Project ID>/locations/<Location ID>/agent/intents/<Intent ID>``.

            This field is a member of `oneof`_ ``intent``.
        description (str):
            Human readable description for better
            understanding an intent like its scope, content,
            result etc. Maximum character limit: 140
            characters.
    """

    display_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    intent_v2: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="intent",
    )
    description: str = proto.Field(
        proto.STRING,
        number=5,
    )


class DialogflowAssistAnswer(proto.Message):
    r"""Represents a Dialogflow assist answer.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        query_result (google.cloud.dialogflow_v2.types.QueryResult):
            Result from v2 agent.

            This field is a member of `oneof`_ ``result``.
        intent_suggestion (google.cloud.dialogflow_v2.types.IntentSuggestion):
            An intent suggestion generated from
            conversation.

            This field is a member of `oneof`_ ``result``.
        answer_record (str):
            The name of answer record, in the format of
            "projects/<Project ID>/locations/<Location
            ID>/answerRecords/<Answer Record ID>".
    """

    query_result: session.QueryResult = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="result",
        message=session.QueryResult,
    )
    intent_suggestion: "IntentSuggestion" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="result",
        message="IntentSuggestion",
    )
    answer_record: str = proto.Field(
        proto.STRING,
        number=2,
    )


class SuggestionResult(proto.Message):
    r"""One response of different type of suggestion response which is used
    in the response of
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent]
    and
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2.Participants.AnalyzeContent],
    as well as
    [HumanAgentAssistantEvent][google.cloud.dialogflow.v2.HumanAgentAssistantEvent].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        error (google.rpc.status_pb2.Status):
            Error status if the request failed.

            This field is a member of `oneof`_ ``suggestion_response``.
        suggest_articles_response (google.cloud.dialogflow_v2.types.SuggestArticlesResponse):
            SuggestArticlesResponse if request is for
            ARTICLE_SUGGESTION.

            This field is a member of `oneof`_ ``suggestion_response``.
        suggest_knowledge_assist_response (google.cloud.dialogflow_v2.types.SuggestKnowledgeAssistResponse):
            SuggestKnowledgeAssistResponse if request is for
            KNOWLEDGE_ASSIST.

            This field is a member of `oneof`_ ``suggestion_response``.
        suggest_faq_answers_response (google.cloud.dialogflow_v2.types.SuggestFaqAnswersResponse):
            SuggestFaqAnswersResponse if request is for FAQ_ANSWER.

            This field is a member of `oneof`_ ``suggestion_response``.
        suggest_smart_replies_response (google.cloud.dialogflow_v2.types.SuggestSmartRepliesResponse):
            SuggestSmartRepliesResponse if request is for SMART_REPLY.

            This field is a member of `oneof`_ ``suggestion_response``.
        generate_suggestions_response (google.cloud.dialogflow_v2.types.GenerateSuggestionsResponse):
            Suggestions generated using generators
            triggered by customer or agent messages.

            This field is a member of `oneof`_ ``suggestion_response``.
    """

    error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="suggestion_response",
        message=status_pb2.Status,
    )
    suggest_articles_response: "SuggestArticlesResponse" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="suggestion_response",
        message="SuggestArticlesResponse",
    )
    suggest_knowledge_assist_response: "SuggestKnowledgeAssistResponse" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="suggestion_response",
        message="SuggestKnowledgeAssistResponse",
    )
    suggest_faq_answers_response: "SuggestFaqAnswersResponse" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="suggestion_response",
        message="SuggestFaqAnswersResponse",
    )
    suggest_smart_replies_response: "SuggestSmartRepliesResponse" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="suggestion_response",
        message="SuggestSmartRepliesResponse",
    )
    generate_suggestions_response: "GenerateSuggestionsResponse" = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="suggestion_response",
        message="GenerateSuggestionsResponse",
    )


class InputTextConfig(proto.Message):
    r"""Defines the language used in the input text.

    Attributes:
        language_code (str):
            Required. The language of this conversational query. See
            `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes.
    """

    language_code: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AnnotatedMessagePart(proto.Message):
    r"""Represents a part of a message possibly annotated with an
    entity. The part can be an entity or purely a part of the
    message between two entities or message start/end.

    Attributes:
        text (str):
            A part of a message possibly annotated with
            an entity.
        entity_type (str):
            The `Dialogflow system entity
            type <https://cloud.google.com/dialogflow/docs/reference/system-entities>`__
            of this message part. If this is empty, Dialogflow could not
            annotate the phrase part with a system entity.
        formatted_value (google.protobuf.struct_pb2.Value):
            The `Dialogflow system entity formatted
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

    text: str = proto.Field(
        proto.STRING,
        number=1,
    )
    entity_type: str = proto.Field(
        proto.STRING,
        number=2,
    )
    formatted_value: struct_pb2.Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=struct_pb2.Value,
    )


class MessageAnnotation(proto.Message):
    r"""Represents the result of annotation for the message.

    Attributes:
        parts (MutableSequence[google.cloud.dialogflow_v2.types.AnnotatedMessagePart]):
            The collection of annotated message parts ordered by their
            position in the message. You can recover the annotated
            message by concatenating [AnnotatedMessagePart.text].
        contain_entities (bool):
            Indicates whether the text message contains
            entities.
    """

    parts: MutableSequence["AnnotatedMessagePart"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AnnotatedMessagePart",
    )
    contain_entities: bool = proto.Field(
        proto.BOOL,
        number=2,
    )


class SuggestionInput(proto.Message):
    r"""Represents the selection of a suggestion.

    Attributes:
        answer_record (str):
            Required. The ID of a suggestion selected by the human
            agent. The suggestion(s) were generated in a previous call
            to request Dialogflow assist. The format is:
            ``projects/<Project ID>/locations/<Location ID>/answerRecords/<Answer Record ID>``
            where is an alphanumeric string.
    """

    answer_record: str = proto.Field(
        proto.STRING,
        number=1,
    )


class AssistQueryParameters(proto.Message):
    r"""Represents the parameters of human assist query.

    Attributes:
        documents_metadata_filters (MutableMapping[str, str]):
            Key-value filters on the metadata of documents returned by
            article suggestion. If specified, article suggestion only
            returns suggested documents that match all filters in their
            [Document.metadata][google.cloud.dialogflow.v2.Document.metadata].
            Multiple values for a metadata key should be concatenated by
            comma. For example, filters to match all documents that have
            'US' or 'CA' in their market metadata values and 'agent' in
            their user metadata values will be

            ::

               documents_metadata_filters {
                 key: "market"
                 value: "US,CA"
               }
               documents_metadata_filters {
                 key: "user"
                 value: "agent"
               }
    """

    documents_metadata_filters: MutableMapping[str, str] = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )


class SuggestKnowledgeAssistRequest(proto.Message):
    r"""The request message for
    [Participants.SuggestKnowledgeAssist][google.cloud.dialogflow.v2.Participants.SuggestKnowledgeAssist].

    Attributes:
        parent (str):
            Required. The name of the participant to fetch suggestions
            for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/participants/<Participant ID>``.
        latest_message (str):
            Optional. The name of the latest conversation message to
            compile suggestions for. If empty, it will be the latest
            message of the conversation. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Optional. Max number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2.SuggestKnowledgeAssistRequest.latest_message]
            to use as context when compiling the suggestion. The context
            size is by default 100 and at most 100.
        previous_suggested_query (str):
            Optional. The previously suggested query for
            the given conversation. This helps identify
            whether the next suggestion we generate is
            reasonably different from the previous one. This
            is useful to avoid similar suggestions within
            the conversation.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )
    previous_suggested_query: str = proto.Field(
        proto.STRING,
        number=4,
    )


class SuggestKnowledgeAssistResponse(proto.Message):
    r"""The response message for
    [Participants.SuggestKnowledgeAssist][google.cloud.dialogflow.v2.Participants.SuggestKnowledgeAssist].

    Attributes:
        knowledge_assist_answer (google.cloud.dialogflow_v2.types.KnowledgeAssistAnswer):
            Output only. Knowledge Assist suggestion.
        latest_message (str):
            The name of the latest conversation message used to compile
            suggestion for. Format:
            ``projects/<Project ID>/locations/<Location ID>/conversations/<Conversation ID>/messages/<Message ID>``.
        context_size (int):
            Number of messages prior to and including
            [latest_message][google.cloud.dialogflow.v2.SuggestKnowledgeAssistResponse.latest_message]
            to compile the suggestion. It may be smaller than the
            [SuggestKnowledgeAssistRequest.context_size][google.cloud.dialogflow.v2.SuggestKnowledgeAssistRequest.context_size]
            field in the request if there are fewer messages in the
            conversation.
    """

    knowledge_assist_answer: "KnowledgeAssistAnswer" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="KnowledgeAssistAnswer",
    )
    latest_message: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class KnowledgeAssistAnswer(proto.Message):
    r"""Represents a Knowledge Assist answer.

    Attributes:
        suggested_query (google.cloud.dialogflow_v2.types.KnowledgeAssistAnswer.SuggestedQuery):
            The query suggested based on the context.
            Suggestion is made only if it is different from
            the previous suggestion.
        suggested_query_answer (google.cloud.dialogflow_v2.types.KnowledgeAssistAnswer.KnowledgeAnswer):
            The answer generated for the suggested query.
            Whether or not an answer is generated depends on
            how confident we are about the generated query.
        answer_record (str):
            The name of the answer record. Format:
            ``projects/<Project ID>/locations/<location ID>/answer Records/<Answer Record ID>``.
    """

    class SuggestedQuery(proto.Message):
        r"""Represents a suggested query.

        Attributes:
            query_text (str):
                Suggested query text.
        """

        query_text: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class KnowledgeAnswer(proto.Message):
        r"""Represents an answer from Knowledge. Currently supports FAQ
        and Generative answers.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            answer_text (str):
                The piece of text from the ``source`` that answers this
                suggested query.
            faq_source (google.cloud.dialogflow_v2.types.KnowledgeAssistAnswer.KnowledgeAnswer.FaqSource):
                Populated if the prediction came from FAQ.

                This field is a member of `oneof`_ ``source``.
            generative_source (google.cloud.dialogflow_v2.types.KnowledgeAssistAnswer.KnowledgeAnswer.GenerativeSource):
                Populated if the prediction was Generative.

                This field is a member of `oneof`_ ``source``.
        """

        class FaqSource(proto.Message):
            r"""Details about source of FAQ answer.

            Attributes:
                question (str):
                    The corresponding FAQ question.
            """

            question: str = proto.Field(
                proto.STRING,
                number=2,
            )

        class GenerativeSource(proto.Message):
            r"""Details about source of Generative answer.

            Attributes:
                snippets (MutableSequence[google.cloud.dialogflow_v2.types.KnowledgeAssistAnswer.KnowledgeAnswer.GenerativeSource.Snippet]):
                    All snippets used for this Generative
                    Prediction, with their source URI and data.
            """

            class Snippet(proto.Message):
                r"""Snippet Source for a Generative Prediction.

                Attributes:
                    uri (str):
                        URI the data is sourced from.
                    text (str):
                        Text taken from that URI.
                    title (str):
                        Title of the document.
                    metadata (google.protobuf.struct_pb2.Struct):
                        Metadata of the document.
                """

                uri: str = proto.Field(
                    proto.STRING,
                    number=2,
                )
                text: str = proto.Field(
                    proto.STRING,
                    number=3,
                )
                title: str = proto.Field(
                    proto.STRING,
                    number=4,
                )
                metadata: struct_pb2.Struct = proto.Field(
                    proto.MESSAGE,
                    number=5,
                    message=struct_pb2.Struct,
                )

            snippets: MutableSequence[
                "KnowledgeAssistAnswer.KnowledgeAnswer.GenerativeSource.Snippet"
            ] = proto.RepeatedField(
                proto.MESSAGE,
                number=1,
                message="KnowledgeAssistAnswer.KnowledgeAnswer.GenerativeSource.Snippet",
            )

        answer_text: str = proto.Field(
            proto.STRING,
            number=1,
        )
        faq_source: "KnowledgeAssistAnswer.KnowledgeAnswer.FaqSource" = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="source",
            message="KnowledgeAssistAnswer.KnowledgeAnswer.FaqSource",
        )
        generative_source: "KnowledgeAssistAnswer.KnowledgeAnswer.GenerativeSource" = (
            proto.Field(
                proto.MESSAGE,
                number=4,
                oneof="source",
                message="KnowledgeAssistAnswer.KnowledgeAnswer.GenerativeSource",
            )
        )

    suggested_query: SuggestedQuery = proto.Field(
        proto.MESSAGE,
        number=1,
        message=SuggestedQuery,
    )
    suggested_query_answer: KnowledgeAnswer = proto.Field(
        proto.MESSAGE,
        number=2,
        message=KnowledgeAnswer,
    )
    answer_record: str = proto.Field(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
