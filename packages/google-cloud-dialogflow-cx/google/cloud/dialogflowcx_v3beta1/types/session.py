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


from google.cloud.dialogflowcx_v3beta1.types import audio_config
from google.cloud.dialogflowcx_v3beta1.types import intent as gcdc_intent
from google.cloud.dialogflowcx_v3beta1.types import page
from google.cloud.dialogflowcx_v3beta1.types import response_message
from google.cloud.dialogflowcx_v3beta1.types import session_entity_type
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import struct_pb2 as struct  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore
from google.type import latlng_pb2 as latlng  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.cx.v3beta1",
    manifest={
        "DetectIntentRequest",
        "DetectIntentResponse",
        "StreamingDetectIntentRequest",
        "StreamingDetectIntentResponse",
        "StreamingRecognitionResult",
        "QueryParameters",
        "QueryInput",
        "QueryResult",
        "TextInput",
        "IntentInput",
        "AudioInput",
        "Match",
        "MatchIntentRequest",
        "MatchIntentResponse",
        "FulfillIntentRequest",
        "FulfillIntentResponse",
    },
)


class DetectIntentRequest(proto.Message):
    r"""The request to detect user's intent.

    Attributes:
        session (str):
            Required. The name of the session this query is sent to.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
            or
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
            If ``Environment ID`` is not specified, we assume default
            'draft' environment. It's up to the API caller to choose an
            appropriate ``Session ID``. It can be a random number or
            some type of session identifiers (preferably hashed). The
            length of the ``Session ID`` must not exceed 36 characters.
        query_params (~.gcdc_session.QueryParameters):
            The parameters of this query.
        query_input (~.gcdc_session.QueryInput):
            Required. The input specification.
        output_audio_config (~.audio_config.OutputAudioConfig):
            Instructs the speech synthesizer how to
            generate the output audio.
    """

    session = proto.Field(proto.STRING, number=1)

    query_params = proto.Field(proto.MESSAGE, number=2, message="QueryParameters",)

    query_input = proto.Field(proto.MESSAGE, number=3, message="QueryInput",)

    output_audio_config = proto.Field(
        proto.MESSAGE, number=4, message=audio_config.OutputAudioConfig,
    )


class DetectIntentResponse(proto.Message):
    r"""The message returned from the DetectIntent method.

    Attributes:
        response_id (str):
            Output only. The unique identifier of the
            response. It can be used to locate a response in
            the training example set or for reporting
            issues.
        query_result (~.gcdc_session.QueryResult):
            The result of the conversational query.
        output_audio (bytes):
            The audio data bytes encoded as specified in the request.
            Note: The output audio is generated based on the values of
            default platform text responses found in the
            [``query_result.response_messages``][google.cloud.dialogflow.cx.v3beta1.QueryResult.response_messages]
            field. If multiple default text responses exist, they will
            be concatenated when generating audio. If no default
            platform text responses exist, the generated audio content
            will be empty.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        output_audio_config (~.audio_config.OutputAudioConfig):
            The config used by the speech synthesizer to
            generate the output audio.
    """

    response_id = proto.Field(proto.STRING, number=1)

    query_result = proto.Field(proto.MESSAGE, number=2, message="QueryResult",)

    output_audio = proto.Field(proto.BYTES, number=4)

    output_audio_config = proto.Field(
        proto.MESSAGE, number=5, message=audio_config.OutputAudioConfig,
    )


class StreamingDetectIntentRequest(proto.Message):
    r"""The top-level message sent by the client to the
    [Sessions.StreamingDetectIntent][google.cloud.dialogflow.cx.v3beta1.Sessions.StreamingDetectIntent]
    method.

    Multiple request messages should be sent in order:

    1. The first message must contain
       [session][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.session],
       [query_input][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.query_input]
       plus optionally
       [query_params][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.query_params].
       If the client wants to receive an audio response, it should also
       contain
       [output_audio_config][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.output_audio_config].

    2. If
       [query_input][google.cloud.dialogflow.cx.v3beta1.StreamingDetectIntentRequest.query_input]
       was set to
       [query_input.audio.config][google.cloud.dialogflow.cx.v3beta1.AudioInput.config],
       all subsequent messages must contain
       [query_input.audio.audio][google.cloud.dialogflow.cx.v3beta1.AudioInput.audio]
       to continue with Speech recognition. If you decide to rather
       detect an intent from text input after you already started Speech
       recognition, please send a message with
       [query_input.text][google.cloud.dialogflow.cx.v3beta1.QueryInput.text].

       However, note that:

       -  Dialogflow will bill you for the audio duration so far.
       -  Dialogflow discards all Speech recognition results in favor of
          the input text.
       -  Dialogflow will use the language code from the first message.

    After you sent all input, you must half-close or abort the request
    stream.

    Attributes:
        session (str):
            The name of the session this query is sent to. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
            or
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
            If ``Environment ID`` is not specified, we assume default
            'draft' environment. It's up to the API caller to choose an
            appropriate ``Session ID``. It can be a random number or
            some type of session identifiers (preferably hashed). The
            length of the ``Session ID`` must not exceed 36 characters.
            Note: session must be set in the first request.
        query_params (~.gcdc_session.QueryParameters):
            The parameters of this query.
        query_input (~.gcdc_session.QueryInput):
            Required. The input specification.
        output_audio_config (~.audio_config.OutputAudioConfig):
            Instructs the speech synthesizer how to
            generate the output audio.
    """

    session = proto.Field(proto.STRING, number=1)

    query_params = proto.Field(proto.MESSAGE, number=2, message="QueryParameters",)

    query_input = proto.Field(proto.MESSAGE, number=3, message="QueryInput",)

    output_audio_config = proto.Field(
        proto.MESSAGE, number=4, message=audio_config.OutputAudioConfig,
    )


class StreamingDetectIntentResponse(proto.Message):
    r"""The top-level message returned from the ``StreamingDetectIntent``
    method.

    Multiple response messages can be returned in order:

    1. If the input was set to streaming audio, the first one or more
       messages contain ``recognition_result``. Each
       ``recognition_result`` represents a more complete transcript of
       what the user said. The last ``recognition_result`` has
       ``is_final`` set to ``true``.

    2. The last message contains ``detect_intent_response``.

    Attributes:
        recognition_result (~.gcdc_session.StreamingRecognitionResult):
            The result of speech recognition.
        detect_intent_response (~.gcdc_session.DetectIntentResponse):
            The response from detect intent.
    """

    recognition_result = proto.Field(
        proto.MESSAGE, number=1, oneof="response", message="StreamingRecognitionResult",
    )

    detect_intent_response = proto.Field(
        proto.MESSAGE, number=2, oneof="response", message=DetectIntentResponse,
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
        message_type (~.gcdc_session.StreamingRecognitionResult.MessageType):
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
        speech_word_info (Sequence[~.audio_config.SpeechWordInfo]):
            Word-specific information for the words recognized by Speech
            in
            [transcript][google.cloud.dialogflow.cx.v3beta1.StreamingRecognitionResult.transcript].
            Populated if and only if ``message_type`` = ``TRANSCRIPT``
            and [InputAudioConfig.enable_word_info] is set.
        speech_end_offset (~.duration.Duration):
            Time offset of the end of this Speech recognition result
            relative to the beginning of the audio. Only populated for
            ``message_type`` = ``TRANSCRIPT``.
    """

    class MessageType(proto.Enum):
        r"""Type of the response message."""
        MESSAGE_TYPE_UNSPECIFIED = 0
        TRANSCRIPT = 1
        END_OF_SINGLE_UTTERANCE = 2

    message_type = proto.Field(proto.ENUM, number=1, enum=MessageType,)

    transcript = proto.Field(proto.STRING, number=2)

    is_final = proto.Field(proto.BOOL, number=3)

    confidence = proto.Field(proto.FLOAT, number=4)

    stability = proto.Field(proto.FLOAT, number=6)

    speech_word_info = proto.RepeatedField(
        proto.MESSAGE, number=7, message=audio_config.SpeechWordInfo,
    )

    speech_end_offset = proto.Field(proto.MESSAGE, number=8, message=duration.Duration,)


class QueryParameters(proto.Message):
    r"""Represents the parameters of a conversational query.

    Attributes:
        time_zone (str):
            The time zone of this conversational query from the `time
            zone database <https://www.iana.org/time-zones>`__, e.g.,
            America/New_York, Europe/Paris. If not provided, the time
            zone specified in the agent is used.
        geo_location (~.latlng.LatLng):
            The geo location of this conversational
            query.
        session_entity_types (Sequence[~.session_entity_type.SessionEntityType]):
            Additional session entity types to replace or
            extend developer entity types with. The entity
            synonyms apply to all languages and persist for
            the session of this query.
        payload (~.struct.Struct):
            This field can be used to pass custom data
            into the webhook associated with the agent.
            Arbitrary JSON objects are supported.
        parameters (~.struct.Struct):
            Additional parameters to be put into [session
            parameters][SessionInfo.parameters]. To remove a parameter
            from the session, clients should explicitly set the
            parameter value to null.

            Depending on your protocol or client library language, this
            is a map, associative array, symbol table, dictionary, or
            JSON object composed of a collection of (MapKey, MapValue)
            pairs:

            -  MapKey type: string
            -  MapKey value: parameter name
            -  MapValue type:

               -  If parameter's entity type is a composite entity: map
               -  Else: string or number, depending on parameter value
                  type

            -  MapValue value:

               -  If parameter's entity type is a composite entity: map
                  from composite entity property names to property
                  values
               -  Else: parameter value
    """

    time_zone = proto.Field(proto.STRING, number=1)

    geo_location = proto.Field(proto.MESSAGE, number=2, message=latlng.LatLng,)

    session_entity_types = proto.RepeatedField(
        proto.MESSAGE, number=3, message=session_entity_type.SessionEntityType,
    )

    payload = proto.Field(proto.MESSAGE, number=4, message=struct.Struct,)

    parameters = proto.Field(proto.MESSAGE, number=5, message=struct.Struct,)


class QueryInput(proto.Message):
    r"""Represents the query input. It can contain either:
    1.  A conversational query in the form of text.

    2.  An intent query that specifies which intent to trigger.

    Attributes:
        text (~.gcdc_session.TextInput):
            The natural language text to be processed.
        intent (~.gcdc_session.IntentInput):
            The intent to be triggered.
        audio (~.gcdc_session.AudioInput):
            The natural language speech audio to be
            processed.
        language_code (str):
            Required. The language of the input. See `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes. Note
            that queries in the same session do not necessarily need to
            specify the same language.
    """

    text = proto.Field(proto.MESSAGE, number=2, oneof="input", message="TextInput",)

    intent = proto.Field(proto.MESSAGE, number=3, oneof="input", message="IntentInput",)

    audio = proto.Field(proto.MESSAGE, number=5, oneof="input", message="AudioInput",)

    language_code = proto.Field(proto.STRING, number=4)


class QueryResult(proto.Message):
    r"""Represents the result of a conversational query.

    Attributes:
        text (str):
            If [natural language
            text][google.cloud.dialogflow.cx.v3beta1.TextInput] was
            provided as input, this field will contain a copy of the
            text.
        trigger_intent (str):
            If an
            [intent][google.cloud.dialogflow.cx.v3beta1.IntentInput] was
            provided as input, this field will contain a copy of the
            intent identifier.
        transcript (str):
            If [natural language speech
            audio][google.cloud.dialogflow.cx.v3beta1.AudioInput] was
            provided as input, this field will contain the trascript for
            the audio.
        trigger_event (str):
            If an [event][google.cloud.dialogflow.cx.v3beta1.EventInput]
            was provided as input, this field will contain the name of
            the event.
        language_code (str):
            The language that was triggered during intent detection. See
            `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes.
        parameters (~.struct.Struct):
            The collected [session
            parameters][google.cloud.dialogflow.cx.v3beta1.SessionInfo.parameters].

            Depending on your protocol or client library language, this
            is a map, associative array, symbol table, dictionary, or
            JSON object composed of a collection of (MapKey, MapValue)
            pairs:

            -  MapKey type: string
            -  MapKey value: parameter name
            -  MapValue type:

               -  If parameter's entity type is a composite entity: map
               -  Else: string or number, depending on parameter value
                  type

            -  MapValue value:

               -  If parameter's entity type is a composite entity: map
                  from composite entity property names to property
                  values
               -  Else: parameter value
        response_messages (Sequence[~.response_message.ResponseMessage]):
            The list of rich messages returned to the
            client. Responses vary from simple text messages
            to more sophisticated, structured payloads used
            to drive complex logic.
        webhook_statuses (Sequence[~.status.Status]):
            The list of webhook call status in the order
            of call sequence.
        webhook_payloads (Sequence[~.struct.Struct]):
            The list of webhook payload in
            [WebhookResponse.payload][google.cloud.dialogflow.cx.v3beta1.WebhookResponse.payload],
            in the order of call sequence. If some webhook call fails or
            doesn't return any payload, an empty ``Struct`` would be
            used instead.
        current_page (~.page.Page):
            The current [Page][google.cloud.dialogflow.cx.v3beta1.Page].
            Some, not all fields are filled in this message, including
            but not limited to ``name`` and ``display_name``.
        intent (~.gcdc_intent.Intent):
            The [Intent][google.cloud.dialogflow.cx.v3beta1.Intent] that
            matched the conversational query. Some, not all fields are
            filled in this message, including but not limited to:
            ``name`` and ``display_name``. This field is deprecated,
            please use
            [QueryResult.match][google.cloud.dialogflow.cx.v3beta1.QueryResult.match]
            instead.
        intent_detection_confidence (float):
            The intent detection confidence. Values range from 0.0
            (completely uncertain) to 1.0 (completely certain). This
            value is for informational purpose only and is only used to
            help match the best intent within the classification
            threshold. This value may change for the same end-user
            expression at any time due to a model retraining or change
            in implementation. This field is deprecated, please use
            [QueryResult.match][google.cloud.dialogflow.cx.v3beta1.QueryResult.match]
            instead.
        match (~.gcdc_session.Match):
            Intent match result, could be an intent or an
            event.
        diagnostic_info (~.struct.Struct):
            The free-form diagnostic info. For example,
            this field could contain webhook call latency.
            The string keys of the Struct's fields map can
            change without notice.
    """

    text = proto.Field(proto.STRING, number=1, oneof="query")

    trigger_intent = proto.Field(proto.STRING, number=11, oneof="query")

    transcript = proto.Field(proto.STRING, number=12, oneof="query")

    trigger_event = proto.Field(proto.STRING, number=14, oneof="query")

    language_code = proto.Field(proto.STRING, number=2)

    parameters = proto.Field(proto.MESSAGE, number=3, message=struct.Struct,)

    response_messages = proto.RepeatedField(
        proto.MESSAGE, number=4, message=response_message.ResponseMessage,
    )

    webhook_statuses = proto.RepeatedField(
        proto.MESSAGE, number=13, message=status.Status,
    )

    webhook_payloads = proto.RepeatedField(
        proto.MESSAGE, number=6, message=struct.Struct,
    )

    current_page = proto.Field(proto.MESSAGE, number=7, message=page.Page,)

    intent = proto.Field(proto.MESSAGE, number=8, message=gcdc_intent.Intent,)

    intent_detection_confidence = proto.Field(proto.FLOAT, number=9)

    match = proto.Field(proto.MESSAGE, number=15, message="Match",)

    diagnostic_info = proto.Field(proto.MESSAGE, number=10, message=struct.Struct,)


class TextInput(proto.Message):
    r"""Represents the natural language text to be processed.

    Attributes:
        text (str):
            Required. The UTF-8 encoded natural language
            text to be processed. Text length must not
            exceed 256 characters.
    """

    text = proto.Field(proto.STRING, number=1)


class IntentInput(proto.Message):
    r"""Represents the intent to trigger programmatically rather than
    as a result of natural language processing.

    Attributes:
        intent (str):
            Required. The unique identifier of the intent. Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/intents/<Intent ID>``.
    """

    intent = proto.Field(proto.STRING, number=1)


class AudioInput(proto.Message):
    r"""Represents the natural speech audio to be processed.

    Attributes:
        config (~.audio_config.InputAudioConfig):
            Required. Instructs the speech recognizer how
            to process the speech audio.
        audio (bytes):
            The natural language speech audio to be processed. A single
            request can contain up to 1 minute of speech audio data. The
            [transcribed
            text][google.cloud.dialogflow.cx.v3beta1.QueryResult.transcript]
            cannot contain more than 256 bytes.

            For non-streaming audio detect intent, both ``config`` and
            ``audio`` must be provided. For streaming audio detect
            intent, ``config`` must be provided in the first request and
            ``audio`` must be provided in all following requests.
    """

    config = proto.Field(
        proto.MESSAGE, number=1, message=audio_config.InputAudioConfig,
    )

    audio = proto.Field(proto.BYTES, number=2)


class Match(proto.Message):
    r"""Represents one match result of [MatchIntent][].

    Attributes:
        intent (~.gcdc_intent.Intent):
            The [Intent][google.cloud.dialogflow.cx.v3beta1.Intent] that
            matched the query. Some, not all fields are filled in this
            message, including but not limited to: ``name`` and
            ``display_name``. Only filled for
            [``INTENT``][google.cloud.dialogflow.cx.v3beta1.Match.MatchType]
            match type.
        parameters (~.struct.Struct):
            The collection of parameters extracted from
            the query.
            Depending on your protocol or client library
            language, this is a map, associative array,
            symbol table, dictionary, or JSON object
            composed of a collection of (MapKey, MapValue)
            pairs:
            -   MapKey type: string
            -   MapKey value: parameter name
            -   MapValue type:
                -   If parameter's entity type is a
            composite entity: map     -   Else: string or
            number, depending on parameter value type -
            MapValue value:
                -   If parameter's entity type is a
            composite entity:         map from composite
            entity property names to property values     -
            Else: parameter value
        resolved_input (str):
            Final text input which was matched during
            MatchIntent. This value can be different from
            original input sent in request because of
            spelling correction or other processing.
        match_type (~.gcdc_session.Match.MatchType):
            Type of this
            [Match][google.cloud.dialogflow.cx.v3beta1.Match].
        confidence (float):
            The confidence of this match. Values range
            from 0.0 (completely uncertain) to 1.0
            (completely certain). This value is for
            informational purpose only and is only used to
            help match the best intent within the
            classification threshold. This value may change
            for the same end-user expression at any time due
            to a model retraining or change in
            implementation.
    """

    class MatchType(proto.Enum):
        r"""Type of a Match."""
        MATCH_TYPE_UNSPECIFIED = 0
        INTENT = 1
        DIRECT_INTENT = 2
        PARAMETER_FILLING = 3
        NO_MATCH = 4
        NO_INPUT = 5

    intent = proto.Field(proto.MESSAGE, number=1, message=gcdc_intent.Intent,)

    parameters = proto.Field(proto.MESSAGE, number=2, message=struct.Struct,)

    resolved_input = proto.Field(proto.STRING, number=3)

    match_type = proto.Field(proto.ENUM, number=4, enum=MatchType,)

    confidence = proto.Field(proto.FLOAT, number=5)


class MatchIntentRequest(proto.Message):
    r"""Request of [MatchIntent][].

    Attributes:
        session (str):
            Required. The name of the session this query is sent to.
            Format:
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/sessions/<Session ID>``
            or
            ``projects/<Project ID>/locations/<Location ID>/agents/<Agent ID>/environments/<Environment ID>/sessions/<Session ID>``.
            If ``Environment ID`` is not specified, we assume default
            'draft' environment. It's up to the API caller to choose an
            appropriate ``Session ID``. It can be a random number or
            some type of session identifiers (preferably hashed). The
            length of the ``Session ID`` must not exceed 36 characters.
        query_params (~.gcdc_session.QueryParameters):
            The parameters of this query.
        query_input (~.gcdc_session.QueryInput):
            Required. The input specification.
    """

    session = proto.Field(proto.STRING, number=1)

    query_params = proto.Field(proto.MESSAGE, number=2, message=QueryParameters,)

    query_input = proto.Field(proto.MESSAGE, number=3, message=QueryInput,)


class MatchIntentResponse(proto.Message):
    r"""Response of [MatchIntent][].

    Attributes:
        text (str):
            If [natural language
            text][google.cloud.dialogflow.cx.v3beta1.TextInput] was
            provided as input, this field will contain a copy of the
            text.
        trigger_intent (str):
            If an
            [intent][google.cloud.dialogflow.cx.v3beta1.IntentInput] was
            provided as input, this field will contain a copy of the
            intent identifier.
        transcript (str):
            If [natural language speech
            audio][google.cloud.dialogflow.cx.v3beta1.AudioInput] was
            provided as input, this field will contain the trascript for
            the audio.
        matches (Sequence[~.gcdc_session.Match]):
            Match results, if more than one, ordered
            descendingly by the confidence we have that the
            particular intent matches the query.
        current_page (~.page.Page):
            The current [Page][google.cloud.dialogflow.cx.v3beta1.Page].
            Some, not all fields are filled in this message, including
            but not limited to ``name`` and ``display_name``.
    """

    text = proto.Field(proto.STRING, number=1, oneof="query")

    trigger_intent = proto.Field(proto.STRING, number=2, oneof="query")

    transcript = proto.Field(proto.STRING, number=3, oneof="query")

    matches = proto.RepeatedField(proto.MESSAGE, number=4, message=Match,)

    current_page = proto.Field(proto.MESSAGE, number=5, message=page.Page,)


class FulfillIntentRequest(proto.Message):
    r"""Request of [FulfillIntent][]

    Attributes:
        match_intent_request (~.gcdc_session.MatchIntentRequest):
            Must be same as the corresponding MatchIntent
            request, otherwise the behavior is undefined.
        match (~.gcdc_session.Match):
            The matched intent/event to fulfill.
        output_audio_config (~.audio_config.OutputAudioConfig):
            Instructs the speech synthesizer how to
            generate output audio.
    """

    match_intent_request = proto.Field(
        proto.MESSAGE, number=1, message=MatchIntentRequest,
    )

    match = proto.Field(proto.MESSAGE, number=2, message=Match,)

    output_audio_config = proto.Field(
        proto.MESSAGE, number=3, message=audio_config.OutputAudioConfig,
    )


class FulfillIntentResponse(proto.Message):
    r"""Response of [FulfillIntent][]

    Attributes:
        response_id (str):
            Output only. The unique identifier of the
            response. It can be used to locate a response in
            the training example set or for reporting
            issues.
        query_result (~.gcdc_session.QueryResult):
            The result of the conversational query.
        output_audio (bytes):
            The audio data bytes encoded as specified in the request.
            Note: The output audio is generated based on the values of
            default platform text responses found in the
            [``query_result.response_messages``][google.cloud.dialogflow.cx.v3beta1.QueryResult.response_messages]
            field. If multiple default text responses exist, they will
            be concatenated when generating audio. If no default
            platform text responses exist, the generated audio content
            will be empty.

            In some scenarios, multiple output audio fields may be
            present in the response structure. In these cases, only the
            top-most-level audio output has content.
        output_audio_config (~.audio_config.OutputAudioConfig):
            The config used by the speech synthesizer to
            generate the output audio.
    """

    response_id = proto.Field(proto.STRING, number=1)

    query_result = proto.Field(proto.MESSAGE, number=2, message=QueryResult,)

    output_audio = proto.Field(proto.BYTES, number=3)

    output_audio_config = proto.Field(
        proto.MESSAGE, number=4, message=audio_config.OutputAudioConfig,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
