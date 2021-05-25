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

from google.cloud.dialogflow_v2beta1.types import agent
from google.cloud.dialogflow_v2beta1.types import audio_config as gcd_audio_config
from google.cloud.dialogflow_v2beta1.types import context
from google.cloud.dialogflow_v2beta1.types import intent as gcd_intent
from google.cloud.dialogflow_v2beta1.types import session_entity_type
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import struct_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "DetectIntentRequest",
        "DetectIntentResponse",
        "QueryParameters",
        "QueryInput",
        "QueryResult",
        "KnowledgeAnswers",
        "StreamingDetectIntentRequest",
        "StreamingDetectIntentResponse",
        "StreamingRecognitionResult",
        "TextInput",
        "EventInput",
        "SentimentAnalysisRequestConfig",
        "SentimentAnalysisResult",
        "Sentiment",
    },
)


class DetectIntentRequest(proto.Message):
    r"""The request to detect user's intent.
    Attributes:
        session (str):
            Required. The name of the session this query is sent to.
            Supported formats:

            -  \`projects//agent/sessions/,
            -  ``projects/<Project ID>/locations/<Location ID>/agent/sessions/<Session ID>``,
            -  ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,
            -  ``projects/<Project ID>/locations/<Location ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,

            If ``Location ID`` is not specified we assume default 'us'
            location. If ``Environment ID`` is not specified, we assume
            default 'draft' environment (``Environment ID`` might be
            referred to as environment name at some places). If
            ``User ID`` is not specified, we are using "-". It's up to
            the API caller to choose an appropriate ``Session ID`` and
            ``User Id``. They can be a random number or some type of
            user and session identifiers (preferably hashed). The length
            of the ``Session ID`` and ``User ID`` must not exceed 36
            characters. For more information, see the `API interactions
            guide <https://cloud.google.com/dialogflow/docs/api-overview>`__.

            Note: Always use agent versions for production traffic. See
            `Versions and
            environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.
        query_params (google.cloud.dialogflow_v2beta1.types.QueryParameters):
            The parameters of this query.
        query_input (google.cloud.dialogflow_v2beta1.types.QueryInput):
            Required. The input specification. It can be
            set to:
            1.  an audio config
                which instructs the speech recognizer how to
            process the speech audio,
            2.  a conversational query in the form of text,
            or
            3.  an event that specifies which intent to
            trigger.
        output_audio_config (google.cloud.dialogflow_v2beta1.types.OutputAudioConfig):
            Instructs the speech synthesizer how to
            generate the output audio. If this field is not
            set and agent-level speech synthesizer is not
            configured, no output audio is generated.
        output_audio_config_mask (google.protobuf.field_mask_pb2.FieldMask):
            Mask for
            [output_audio_config][google.cloud.dialogflow.v2beta1.DetectIntentRequest.output_audio_config]
            indicating which settings in this request-level config
            should override speech synthesizer settings defined at
            agent-level.

            If unspecified or empty,
            [output_audio_config][google.cloud.dialogflow.v2beta1.DetectIntentRequest.output_audio_config]
            replaces the agent-level config in its entirety.
        input_audio (bytes):
            The natural language speech audio to be processed. This
            field should be populated iff ``query_input`` is set to an
            input audio config. A single request can contain up to 1
            minute of speech audio data.
    """

    session = proto.Field(proto.STRING, number=1,)
    query_params = proto.Field(proto.MESSAGE, number=2, message="QueryParameters",)
    query_input = proto.Field(proto.MESSAGE, number=3, message="QueryInput",)
    output_audio_config = proto.Field(
        proto.MESSAGE, number=4, message=gcd_audio_config.OutputAudioConfig,
    )
    output_audio_config_mask = proto.Field(
        proto.MESSAGE, number=7, message=field_mask_pb2.FieldMask,
    )
    input_audio = proto.Field(proto.BYTES, number=5,)


class DetectIntentResponse(proto.Message):
    r"""The message returned from the DetectIntent method.
    Attributes:
        response_id (str):
            The unique identifier of the response. It can
            be used to locate a response in the training
            example set or for reporting issues.
        query_result (google.cloud.dialogflow_v2beta1.types.QueryResult):
            The selected results of the conversational query or event
            processing. See ``alternative_query_results`` for additional
            potential results.
        alternative_query_results (Sequence[google.cloud.dialogflow_v2beta1.types.QueryResult]):
            If Knowledge Connectors are enabled, there could be more
            than one result returned for a given query or event, and
            this field will contain all results except for the top one,
            which is captured in query_result. The alternative results
            are ordered by decreasing
            ``QueryResult.intent_detection_confidence``. If Knowledge
            Connectors are disabled, this field will be empty until
            multiple responses for regular intents are supported, at
            which point those additional results will be surfaced here.
        webhook_status (google.rpc.status_pb2.Status):
            Specifies the status of the webhook request.
        output_audio (bytes):
            The audio data bytes encoded as specified in the request.
            Note: The output audio is generated based on the values of
            default platform text responses found in the
            ``query_result.fulfillment_messages`` field. If multiple
            default text responses exist, they will be concatenated when
            generating audio. If no default platform text responses
            exist, the generated audio content will be empty.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        output_audio_config (google.cloud.dialogflow_v2beta1.types.OutputAudioConfig):
            The config used by the speech synthesizer to
            generate the output audio.
    """

    response_id = proto.Field(proto.STRING, number=1,)
    query_result = proto.Field(proto.MESSAGE, number=2, message="QueryResult",)
    alternative_query_results = proto.RepeatedField(
        proto.MESSAGE, number=5, message="QueryResult",
    )
    webhook_status = proto.Field(proto.MESSAGE, number=3, message=status_pb2.Status,)
    output_audio = proto.Field(proto.BYTES, number=4,)
    output_audio_config = proto.Field(
        proto.MESSAGE, number=6, message=gcd_audio_config.OutputAudioConfig,
    )


class QueryParameters(proto.Message):
    r"""Represents the parameters of the conversational query.
    Attributes:
        time_zone (str):
            The time zone of this conversational query from the `time
            zone database <https://www.iana.org/time-zones>`__, e.g.,
            America/New_York, Europe/Paris. If not provided, the time
            zone specified in agent settings is used.
        geo_location (google.type.latlng_pb2.LatLng):
            The geo location of this conversational
            query.
        contexts (Sequence[google.cloud.dialogflow_v2beta1.types.Context]):
            The collection of contexts to be activated
            before this query is executed.
        reset_contexts (bool):
            Specifies whether to delete all contexts in
            the current session before the new ones are
            activated.
        session_entity_types (Sequence[google.cloud.dialogflow_v2beta1.types.SessionEntityType]):
            Additional session entity types to replace or
            extend developer entity types with. The entity
            synonyms apply to all languages and persist for
            the session of this query.
        payload (google.protobuf.struct_pb2.Struct):
            This field can be used to pass custom data to your webhook.
            Arbitrary JSON objects are supported. If supplied, the value
            is used to populate the
            ``WebhookRequest.original_detect_intent_request.payload``
            field sent to your webhook.
        knowledge_base_names (Sequence[str]):
            KnowledgeBases to get alternative results from. If not set,
            the KnowledgeBases enabled in the agent (through UI) will be
            used. Format:
            ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>``.
        sentiment_analysis_request_config (google.cloud.dialogflow_v2beta1.types.SentimentAnalysisRequestConfig):
            Configures the type of sentiment analysis to
            perform. If not provided, sentiment analysis is
            not performed. Note: Sentiment Analysis is only
            currently available for Essentials Edition
            agents.
        sub_agents (Sequence[google.cloud.dialogflow_v2beta1.types.SubAgent]):
            For mega agent query, directly specify which
            sub agents to query. If any specified sub agent
            is not linked to the mega agent, an error will
            be returned. If empty, Dialogflow will decide
            which sub agents to query. If specified for a
            non-mega-agent query, will be silently ignored.
        webhook_headers (Sequence[google.cloud.dialogflow_v2beta1.types.QueryParameters.WebhookHeadersEntry]):
            This field can be used to pass HTTP headers
            for a webhook call. These headers will be sent
            to webhook along with the headers that have been
            configured through Dialogflow web console. The
            headers defined within this field will overwrite
            the headers configured through Dialogflow
            console if there is a conflict. Header names are
            case-insensitive. Google's specified headers are
            not allowed. Including: "Host", "Content-
            Length", "Connection", "From", "User-Agent",
            "Accept-Encoding", "If-Modified-Since", "If-
            None-Match", "X-Forwarded-For", etc.
    """

    time_zone = proto.Field(proto.STRING, number=1,)
    geo_location = proto.Field(proto.MESSAGE, number=2, message=latlng_pb2.LatLng,)
    contexts = proto.RepeatedField(proto.MESSAGE, number=3, message=context.Context,)
    reset_contexts = proto.Field(proto.BOOL, number=4,)
    session_entity_types = proto.RepeatedField(
        proto.MESSAGE, number=5, message=session_entity_type.SessionEntityType,
    )
    payload = proto.Field(proto.MESSAGE, number=6, message=struct_pb2.Struct,)
    knowledge_base_names = proto.RepeatedField(proto.STRING, number=12,)
    sentiment_analysis_request_config = proto.Field(
        proto.MESSAGE, number=10, message="SentimentAnalysisRequestConfig",
    )
    sub_agents = proto.RepeatedField(proto.MESSAGE, number=13, message=agent.SubAgent,)
    webhook_headers = proto.MapField(proto.STRING, proto.STRING, number=14,)


class QueryInput(proto.Message):
    r"""Represents the query input. It can contain either:
    1.  An audio config which
        instructs the speech recognizer how to process the speech
    audio.
    2.  A conversational query in the form of text.

    3.  An event that specifies which intent to trigger.

    Attributes:
        audio_config (google.cloud.dialogflow_v2beta1.types.InputAudioConfig):
            Instructs the speech recognizer how to
            process the speech audio.
        text (google.cloud.dialogflow_v2beta1.types.TextInput):
            The natural language text to be processed.
        event (google.cloud.dialogflow_v2beta1.types.EventInput):
            The event to be processed.
        dtmf (google.cloud.dialogflow_v2beta1.types.TelephonyDtmfEvents):
            The DTMF digits used to invoke intent and
            fill in parameter value.
    """

    audio_config = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="input",
        message=gcd_audio_config.InputAudioConfig,
    )
    text = proto.Field(proto.MESSAGE, number=2, oneof="input", message="TextInput",)
    event = proto.Field(proto.MESSAGE, number=3, oneof="input", message="EventInput",)
    dtmf = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="input",
        message=gcd_audio_config.TelephonyDtmfEvents,
    )


class QueryResult(proto.Message):
    r"""Represents the result of conversational query or event
    processing.

    Attributes:
        query_text (str):
            The original conversational query text:

            -  If natural language text was provided as input,
               ``query_text`` contains a copy of the input.
            -  If natural language speech audio was provided as input,
               ``query_text`` contains the speech recognition result. If
               speech recognizer produced multiple alternatives, a
               particular one is picked.
            -  If automatic spell correction is enabled, ``query_text``
               will contain the corrected user input.
        language_code (str):
            The language that was triggered during intent detection. See
            `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes.
        speech_recognition_confidence (float):
            The Speech recognition confidence between 0.0
            and 1.0. A higher number indicates an estimated
            greater likelihood that the recognized words are
            correct. The default of 0.0 is a sentinel value
            indicating that confidence was not set.

            This field is not guaranteed to be accurate or
            set. In particular this field isn't set for
            StreamingDetectIntent since the streaming
            endpoint has separate confidence estimates per
            portion of the audio in
            StreamingRecognitionResult.
        action (str):
            The action name from the matched intent.
        parameters (google.protobuf.struct_pb2.Struct):
            The collection of extracted parameters.
            Depending on your protocol or client library
            language, this is a map, associative array,
            symbol table, dictionary, or JSON object
            composed of a collection of (MapKey, MapValue)
            pairs:
            -   MapKey type: string
            -   MapKey value: parameter name
            -   MapValue type:
                -   If parameter's entity type is a
            composite entity: map     -   Else: depending on
            parameter value type, could be one of string,
            number, boolean, null, list or map
            -   MapValue value:
                -   If parameter's entity type is a
            composite entity:         map from composite
            entity property names to property values     -
            Else: parameter value
        all_required_params_present (bool):
            This field is set to:

            -  ``false`` if the matched intent has required parameters
               and not all of the required parameter values have been
               collected.
            -  ``true`` if all required parameter values have been
               collected, or if the matched intent doesn't contain any
               required parameters.
        cancels_slot_filling (bool):
            Indicates whether the conversational query
            triggers a cancellation for slot filling.
        fulfillment_text (str):
            The text to be pronounced to the user or shown on the
            screen. Note: This is a legacy field,
            ``fulfillment_messages`` should be preferred.
        fulfillment_messages (Sequence[google.cloud.dialogflow_v2beta1.types.Intent.Message]):
            The collection of rich messages to present to
            the user.
        webhook_source (str):
            If the query was fulfilled by a webhook call, this field is
            set to the value of the ``source`` field returned in the
            webhook response.
        webhook_payload (google.protobuf.struct_pb2.Struct):
            If the query was fulfilled by a webhook call, this field is
            set to the value of the ``payload`` field returned in the
            webhook response.
        output_contexts (Sequence[google.cloud.dialogflow_v2beta1.types.Context]):
            The collection of output contexts. If applicable,
            ``output_contexts.parameters`` contains entries with name
            ``<parameter name>.original`` containing the original
            parameter values before the query.
        intent (google.cloud.dialogflow_v2beta1.types.Intent):
            The intent that matched the conversational query. Some, not
            all fields are filled in this message, including but not
            limited to: ``name``, ``display_name``, ``end_interaction``
            and ``is_fallback``.
        intent_detection_confidence (float):
            The intent detection confidence. Values range from 0.0
            (completely uncertain) to 1.0 (completely certain). This
            value is for informational purpose only and is only used to
            help match the best intent within the classification
            threshold. This value may change for the same end-user
            expression at any time due to a model retraining or change
            in implementation. If there are
            ``multiple knowledge_answers`` messages, this value is set
            to the greatest ``knowledgeAnswers.match_confidence`` value
            in the list.
        diagnostic_info (google.protobuf.struct_pb2.Struct):
            Free-form diagnostic information for the
            associated detect intent request. The fields of
            this data can change without notice, so you
            should not write code that depends on its
            structure.
            The data may contain:

            - webhook call latency
            - webhook errors
        sentiment_analysis_result (google.cloud.dialogflow_v2beta1.types.SentimentAnalysisResult):
            The sentiment analysis result, which depends on the
            ``sentiment_analysis_request_config`` specified in the
            request.
        knowledge_answers (google.cloud.dialogflow_v2beta1.types.KnowledgeAnswers):
            The result from Knowledge Connector (if any), ordered by
            decreasing ``KnowledgeAnswers.match_confidence``.
    """

    query_text = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=15,)
    speech_recognition_confidence = proto.Field(proto.FLOAT, number=2,)
    action = proto.Field(proto.STRING, number=3,)
    parameters = proto.Field(proto.MESSAGE, number=4, message=struct_pb2.Struct,)
    all_required_params_present = proto.Field(proto.BOOL, number=5,)
    cancels_slot_filling = proto.Field(proto.BOOL, number=21,)
    fulfillment_text = proto.Field(proto.STRING, number=6,)
    fulfillment_messages = proto.RepeatedField(
        proto.MESSAGE, number=7, message=gcd_intent.Intent.Message,
    )
    webhook_source = proto.Field(proto.STRING, number=8,)
    webhook_payload = proto.Field(proto.MESSAGE, number=9, message=struct_pb2.Struct,)
    output_contexts = proto.RepeatedField(
        proto.MESSAGE, number=10, message=context.Context,
    )
    intent = proto.Field(proto.MESSAGE, number=11, message=gcd_intent.Intent,)
    intent_detection_confidence = proto.Field(proto.FLOAT, number=12,)
    diagnostic_info = proto.Field(proto.MESSAGE, number=14, message=struct_pb2.Struct,)
    sentiment_analysis_result = proto.Field(
        proto.MESSAGE, number=17, message="SentimentAnalysisResult",
    )
    knowledge_answers = proto.Field(
        proto.MESSAGE, number=18, message="KnowledgeAnswers",
    )


class KnowledgeAnswers(proto.Message):
    r"""Represents the result of querying a Knowledge base.
    Attributes:
        answers (Sequence[google.cloud.dialogflow_v2beta1.types.KnowledgeAnswers.Answer]):
            A list of answers from Knowledge Connector.
    """

    class Answer(proto.Message):
        r"""An answer from Knowledge Connector.
        Attributes:
            source (str):
                Indicates which Knowledge Document this answer was extracted
                from. Format:
                ``projects/<Project ID>/knowledgeBases/<Knowledge Base ID>/documents/<Document ID>``.
            faq_question (str):
                The corresponding FAQ question if the answer
                was extracted from a FAQ Document, empty
                otherwise.
            answer (str):
                The piece of text from the ``source`` knowledge base
                document that answers this conversational query.
            match_confidence_level (google.cloud.dialogflow_v2beta1.types.KnowledgeAnswers.Answer.MatchConfidenceLevel):
                The system's confidence level that this knowledge answer is
                a good match for this conversational query. NOTE: The
                confidence level for a given ``<query, answer>`` pair may
                change without notice, as it depends on models that are
                constantly being improved. However, it will change less
                frequently than the confidence score below, and should be
                preferred for referencing the quality of an answer.
            match_confidence (float):
                The system's confidence score that this Knowledge answer is
                a good match for this conversational query. The range is
                from 0.0 (completely uncertain) to 1.0 (completely certain).
                Note: The confidence score is likely to vary somewhat
                (possibly even for identical requests), as the underlying
                model is under constant improvement. It may be deprecated in
                the future. We recommend using ``match_confidence_level``
                which should be generally more stable.
        """

        class MatchConfidenceLevel(proto.Enum):
            r"""Represents the system's confidence that this knowledge answer
            is a good match for this conversational query.
            """
            MATCH_CONFIDENCE_LEVEL_UNSPECIFIED = 0
            LOW = 1
            MEDIUM = 2
            HIGH = 3

        source = proto.Field(proto.STRING, number=1,)
        faq_question = proto.Field(proto.STRING, number=2,)
        answer = proto.Field(proto.STRING, number=3,)
        match_confidence_level = proto.Field(
            proto.ENUM, number=4, enum="KnowledgeAnswers.Answer.MatchConfidenceLevel",
        )
        match_confidence = proto.Field(proto.FLOAT, number=5,)

    answers = proto.RepeatedField(proto.MESSAGE, number=1, message=Answer,)


class StreamingDetectIntentRequest(proto.Message):
    r"""The top-level message sent by the client to the
    [Sessions.StreamingDetectIntent][google.cloud.dialogflow.v2beta1.Sessions.StreamingDetectIntent]
    method.

    Multiple request messages should be sent in order:

    1. The first message must contain
       [session][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.session],
       [query_input][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.query_input]
       plus optionally
       [query_params][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.query_params].
       If the client wants to receive an audio response, it should also
       contain
       [output_audio_config][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.output_audio_config].
       The message must not contain
       [input_audio][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.input_audio].

    2. If
       [query_input][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.query_input]
       was set to
       [query_input.audio_config][google.cloud.dialogflow.v2beta1.InputAudioConfig],
       all subsequent messages must contain
       [input_audio][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.input_audio]
       to continue with Speech recognition. If you decide to rather
       detect an intent from text input after you already started Speech
       recognition, please send a message with
       [query_input.text][google.cloud.dialogflow.v2beta1.QueryInput.text].

       However, note that:

       -  Dialogflow will bill you for the audio duration so far.
       -  Dialogflow discards all Speech recognition results in favor of
          the input text.
       -  Dialogflow will use the language code from the first message.

    After you sent all input, you must half-close or abort the request
    stream.

    Attributes:
        session (str):
            Required. The name of the session the query is sent to.
            Supported formats:

            -  \`projects//agent/sessions/,
            -  ``projects/<Project ID>/locations/<Location ID>/agent/sessions/<Session ID>``,
            -  ``projects/<Project ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,
            -  ``projects/<Project ID>/locations/<Location ID>/agent/environments/<Environment ID>/users/<User ID>/sessions/<Session ID>``,

            If ``Location ID`` is not specified we assume default 'us'
            location. If ``Environment ID`` is not specified, we assume
            default 'draft' environment. If ``User ID`` is not
            specified, we are using "-". It's up to the API caller to
            choose an appropriate ``Session ID`` and ``User Id``. They
            can be a random number or some type of user and session
            identifiers (preferably hashed). The length of the
            ``Session ID`` and ``User ID`` must not exceed 36
            characters.

            For more information, see the `API interactions
            guide <https://cloud.google.com/dialogflow/docs/api-overview>`__.

            Note: Always use agent versions for production traffic. See
            `Versions and
            environments <https://cloud.google.com/dialogflow/es/docs/agents-versions>`__.
        query_params (google.cloud.dialogflow_v2beta1.types.QueryParameters):
            The parameters of this query.
        query_input (google.cloud.dialogflow_v2beta1.types.QueryInput):
            Required. The input specification. It can be
            set to:
            1.  an audio config which instructs the speech
            recognizer how to process     the speech audio,

            2.  a conversational query in the form of text,
            or
            3.  an event that specifies which intent to
            trigger.
        single_utterance (bool):
            DEPRECATED. Please use
            [InputAudioConfig.single_utterance][google.cloud.dialogflow.v2beta1.InputAudioConfig.single_utterance]
            instead. If ``false`` (default), recognition does not cease
            until the client closes the stream. If ``true``, the
            recognizer will detect a single spoken utterance in input
            audio. Recognition ceases when it detects the audio's voice
            has stopped or paused. In this case, once a detected intent
            is received, the client should close the stream and start a
            new request with a new stream as needed. This setting is
            ignored when ``query_input`` is a piece of text or an event.
        output_audio_config (google.cloud.dialogflow_v2beta1.types.OutputAudioConfig):
            Instructs the speech synthesizer how to
            generate the output audio. If this field is not
            set and agent-level speech synthesizer is not
            configured, no output audio is generated.
        output_audio_config_mask (google.protobuf.field_mask_pb2.FieldMask):
            Mask for
            [output_audio_config][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.output_audio_config]
            indicating which settings in this request-level config
            should override speech synthesizer settings defined at
            agent-level.

            If unspecified or empty,
            [output_audio_config][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.output_audio_config]
            replaces the agent-level config in its entirety.
        input_audio (bytes):
            The input audio content to be recognized. Must be sent if
            ``query_input`` was set to a streaming input audio config.
            The complete audio over all streaming messages must not
            exceed 1 minute.
    """

    session = proto.Field(proto.STRING, number=1,)
    query_params = proto.Field(proto.MESSAGE, number=2, message="QueryParameters",)
    query_input = proto.Field(proto.MESSAGE, number=3, message="QueryInput",)
    single_utterance = proto.Field(proto.BOOL, number=4,)
    output_audio_config = proto.Field(
        proto.MESSAGE, number=5, message=gcd_audio_config.OutputAudioConfig,
    )
    output_audio_config_mask = proto.Field(
        proto.MESSAGE, number=7, message=field_mask_pb2.FieldMask,
    )
    input_audio = proto.Field(proto.BYTES, number=6,)


class StreamingDetectIntentResponse(proto.Message):
    r"""The top-level message returned from the ``StreamingDetectIntent``
    method.

    Multiple response messages can be returned in order:

    1. If the input was set to streaming audio, the first one or more
       messages contain ``recognition_result``. Each
       ``recognition_result`` represents a more complete transcript of
       what the user said. The last ``recognition_result`` has
       ``is_final`` set to ``true``.

    2. The next message contains ``response_id``, ``query_result``,
       ``alternative_query_results`` and optionally ``webhook_status``
       if a WebHook was called.

    3. If ``output_audio_config`` was specified in the request or
       agent-level speech synthesizer is configured, all subsequent
       messages contain ``output_audio`` and ``output_audio_config``.

    Attributes:
        response_id (str):
            The unique identifier of the response. It can
            be used to locate a response in the training
            example set or for reporting issues.
        recognition_result (google.cloud.dialogflow_v2beta1.types.StreamingRecognitionResult):
            The result of speech recognition.
        query_result (google.cloud.dialogflow_v2beta1.types.QueryResult):
            The selected results of the conversational query or event
            processing. See ``alternative_query_results`` for additional
            potential results.
        alternative_query_results (Sequence[google.cloud.dialogflow_v2beta1.types.QueryResult]):
            If Knowledge Connectors are enabled, there could be more
            than one result returned for a given query or event, and
            this field will contain all results except for the top one,
            which is captured in query_result. The alternative results
            are ordered by decreasing
            ``QueryResult.intent_detection_confidence``. If Knowledge
            Connectors are disabled, this field will be empty until
            multiple responses for regular intents are supported, at
            which point those additional results will be surfaced here.
        webhook_status (google.rpc.status_pb2.Status):
            Specifies the status of the webhook request.
        output_audio (bytes):
            The audio data bytes encoded as specified in the request.
            Note: The output audio is generated based on the values of
            default platform text responses found in the
            ``query_result.fulfillment_messages`` field. If multiple
            default text responses exist, they will be concatenated when
            generating audio. If no default platform text responses
            exist, the generated audio content will be empty.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        output_audio_config (google.cloud.dialogflow_v2beta1.types.OutputAudioConfig):
            The config used by the speech synthesizer to
            generate the output audio.
    """

    response_id = proto.Field(proto.STRING, number=1,)
    recognition_result = proto.Field(
        proto.MESSAGE, number=2, message="StreamingRecognitionResult",
    )
    query_result = proto.Field(proto.MESSAGE, number=3, message="QueryResult",)
    alternative_query_results = proto.RepeatedField(
        proto.MESSAGE, number=7, message="QueryResult",
    )
    webhook_status = proto.Field(proto.MESSAGE, number=4, message=status_pb2.Status,)
    output_audio = proto.Field(proto.BYTES, number=5,)
    output_audio_config = proto.Field(
        proto.MESSAGE, number=6, message=gcd_audio_config.OutputAudioConfig,
    )


class StreamingRecognitionResult(proto.Message):
    r"""Contains a speech recognition result corresponding to a portion of
    the audio that is currently being processed or an indication that
    this is the end of the single requested utterance.

    Example:

    1. transcript: "tube"

    2. transcript: "to be a"

    3. transcript: "to be"

    4. transcript: "to be or not to be" is_final: true

    5. transcript: " that's"

    6. transcript: " that is"

    7. message_type: ``END_OF_SINGLE_UTTERANCE``

    8. transcript: " that is the question" is_final: true

    Only two of the responses contain final results (#4 and #8 indicated
    by ``is_final: true``). Concatenating these generates the full
    transcript: "to be or not to be that is the question".

    In each response we populate:

    -  for ``TRANSCRIPT``: ``transcript`` and possibly ``is_final``.

    -  for ``END_OF_SINGLE_UTTERANCE``: only ``message_type``.

    Attributes:
        message_type (google.cloud.dialogflow_v2beta1.types.StreamingRecognitionResult.MessageType):
            Type of the result message.
        transcript (str):
            Transcript text representing the words that the user spoke.
            Populated if and only if ``message_type`` = ``TRANSCRIPT``.
        is_final (bool):
            If ``false``, the ``StreamingRecognitionResult`` represents
            an interim result that may change. If ``true``, the
            recognizer will not return any further hypotheses about this
            piece of the audio. May only be populated for
            ``message_type`` = ``TRANSCRIPT``.
        confidence (float):
            The Speech confidence between 0.0 and 1.0 for the current
            portion of audio. A higher number indicates an estimated
            greater likelihood that the recognized words are correct.
            The default of 0.0 is a sentinel value indicating that
            confidence was not set.

            This field is typically only provided if ``is_final`` is
            true and you should not rely on it being accurate or even
            set.
        stability (float):
            An estimate of the likelihood that the speech recognizer
            will not change its guess about this interim recognition
            result:

            -  If the value is unspecified or 0.0, Dialogflow didn't
               compute the stability. In particular, Dialogflow will
               only provide stability for ``TRANSCRIPT`` results with
               ``is_final = false``.
            -  Otherwise, the value is in (0.0, 1.0] where 0.0 means
               completely unstable and 1.0 means completely stable.
        speech_word_info (Sequence[google.cloud.dialogflow_v2beta1.types.SpeechWordInfo]):
            Word-specific information for the words recognized by Speech
            in
            [transcript][google.cloud.dialogflow.v2beta1.StreamingRecognitionResult.transcript].
            Populated if and only if ``message_type`` = ``TRANSCRIPT``
            and [InputAudioConfig.enable_word_info] is set.
        speech_end_offset (google.protobuf.duration_pb2.Duration):
            Time offset of the end of this Speech recognition result
            relative to the beginning of the audio. Only populated for
            ``message_type`` = ``TRANSCRIPT``.
        dtmf_digits (google.cloud.dialogflow_v2beta1.types.TelephonyDtmfEvents):
            DTMF digits. Populated if and only if ``message_type`` =
            ``DTMF_DIGITS``.
    """

    class MessageType(proto.Enum):
        r"""Type of the response message."""
        MESSAGE_TYPE_UNSPECIFIED = 0
        TRANSCRIPT = 1
        DTMF_DIGITS = 3
        END_OF_SINGLE_UTTERANCE = 2
        PARTIAL_DTMF_DIGITS = 4

    message_type = proto.Field(proto.ENUM, number=1, enum=MessageType,)
    transcript = proto.Field(proto.STRING, number=2,)
    is_final = proto.Field(proto.BOOL, number=3,)
    confidence = proto.Field(proto.FLOAT, number=4,)
    stability = proto.Field(proto.FLOAT, number=6,)
    speech_word_info = proto.RepeatedField(
        proto.MESSAGE, number=7, message=gcd_audio_config.SpeechWordInfo,
    )
    speech_end_offset = proto.Field(
        proto.MESSAGE, number=8, message=duration_pb2.Duration,
    )
    dtmf_digits = proto.Field(
        proto.MESSAGE, number=5, message=gcd_audio_config.TelephonyDtmfEvents,
    )


class TextInput(proto.Message):
    r"""Represents the natural language text to be processed.
    Attributes:
        text (str):
            Required. The UTF-8 encoded natural language
            text to be processed. Text length must not
            exceed 256 characters.
        language_code (str):
            Required. The language of this conversational query. See
            `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes. Note
            that queries in the same session do not necessarily need to
            specify the same language.
    """

    text = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)


class EventInput(proto.Message):
    r"""Events allow for matching intents by event name instead of the
    natural language input. For instance, input
    ``<event: { name: "welcome_event", parameters: { name: "Sam" } }>``
    can trigger a personalized welcome response. The parameter ``name``
    may be used by the agent in the response:
    ``"Hello #welcome_event.name! What can I do for you today?"``.

    Attributes:
        name (str):
            Required. The unique identifier of the event.
        parameters (google.protobuf.struct_pb2.Struct):
            The collection of parameters associated with
            the event.
            Depending on your protocol or client library
            language, this is a map, associative array,
            symbol table, dictionary, or JSON object
            composed of a collection of (MapKey, MapValue)
            pairs:
            -   MapKey type: string
            -   MapKey value: parameter name
            -   MapValue type:
                -   If parameter's entity type is a
            composite entity: map     -   Else: depending on
            parameter value type, could be one of string,
            number, boolean, null, list or map
            -   MapValue value:
                -   If parameter's entity type is a
            composite entity:         map from composite
            entity property names to property values     -
            Else: parameter value
        language_code (str):
            Required. The language of this query. See `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes. Note
            that queries in the same session do not necessarily need to
            specify the same language.
    """

    name = proto.Field(proto.STRING, number=1,)
    parameters = proto.Field(proto.MESSAGE, number=2, message=struct_pb2.Struct,)
    language_code = proto.Field(proto.STRING, number=3,)


class SentimentAnalysisRequestConfig(proto.Message):
    r"""Configures the types of sentiment analysis to perform.
    Attributes:
        analyze_query_text_sentiment (bool):
            Instructs the service to perform sentiment analysis on
            ``query_text``. If not provided, sentiment analysis is not
            performed on ``query_text``.
    """

    analyze_query_text_sentiment = proto.Field(proto.BOOL, number=1,)


class SentimentAnalysisResult(proto.Message):
    r"""The result of sentiment analysis. Sentiment analysis inspects user
    input and identifies the prevailing subjective opinion, especially
    to determine a user's attitude as positive, negative, or neutral.
    For [Participants.DetectIntent][], it needs to be configured in
    [DetectIntentRequest.query_params][google.cloud.dialogflow.v2beta1.DetectIntentRequest.query_params].
    For [Participants.StreamingDetectIntent][], it needs to be
    configured in
    [StreamingDetectIntentRequest.query_params][google.cloud.dialogflow.v2beta1.StreamingDetectIntentRequest.query_params].
    And for
    [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent]
    and
    [Participants.StreamingAnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.StreamingAnalyzeContent],
    it needs to be configured in
    [ConversationProfile.human_agent_assistant_config][google.cloud.dialogflow.v2beta1.ConversationProfile.human_agent_assistant_config]

    Attributes:
        query_text_sentiment (google.cloud.dialogflow_v2beta1.types.Sentiment):
            The sentiment analysis result for ``query_text``.
    """

    query_text_sentiment = proto.Field(proto.MESSAGE, number=1, message="Sentiment",)


class Sentiment(proto.Message):
    r"""The sentiment, such as positive/negative feeling or
    association, for a unit of analysis, such as the query text.

    Attributes:
        score (float):
            Sentiment score between -1.0 (negative
            sentiment) and 1.0 (positive sentiment).
        magnitude (float):
            A non-negative number in the [0, +inf) range, which
            represents the absolute magnitude of sentiment, regardless
            of score (positive or negative).
    """

    score = proto.Field(proto.FLOAT, number=1,)
    magnitude = proto.Field(proto.FLOAT, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
