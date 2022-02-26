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

from google.cloud.speech_v1.types import resource
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.speech.v1",
    manifest={
        "RecognizeRequest",
        "LongRunningRecognizeRequest",
        "TranscriptOutputConfig",
        "StreamingRecognizeRequest",
        "StreamingRecognitionConfig",
        "RecognitionConfig",
        "SpeakerDiarizationConfig",
        "RecognitionMetadata",
        "SpeechContext",
        "RecognitionAudio",
        "RecognizeResponse",
        "LongRunningRecognizeResponse",
        "LongRunningRecognizeMetadata",
        "StreamingRecognizeResponse",
        "StreamingRecognitionResult",
        "SpeechRecognitionResult",
        "SpeechRecognitionAlternative",
        "WordInfo",
    },
)


class RecognizeRequest(proto.Message):
    r"""The top-level message sent by the client for the ``Recognize``
    method.

    Attributes:
        config (google.cloud.speech_v1.types.RecognitionConfig):
            Required. Provides information to the
            recognizer that specifies how to process the
            request.
        audio (google.cloud.speech_v1.types.RecognitionAudio):
            Required. The audio data to be recognized.
    """

    config = proto.Field(proto.MESSAGE, number=1, message="RecognitionConfig",)
    audio = proto.Field(proto.MESSAGE, number=2, message="RecognitionAudio",)


class LongRunningRecognizeRequest(proto.Message):
    r"""The top-level message sent by the client for the
    ``LongRunningRecognize`` method.

    Attributes:
        config (google.cloud.speech_v1.types.RecognitionConfig):
            Required. Provides information to the
            recognizer that specifies how to process the
            request.
        audio (google.cloud.speech_v1.types.RecognitionAudio):
            Required. The audio data to be recognized.
        output_config (google.cloud.speech_v1.types.TranscriptOutputConfig):
            Optional. Specifies an optional destination
            for the recognition results.
    """

    config = proto.Field(proto.MESSAGE, number=1, message="RecognitionConfig",)
    audio = proto.Field(proto.MESSAGE, number=2, message="RecognitionAudio",)
    output_config = proto.Field(
        proto.MESSAGE, number=4, message="TranscriptOutputConfig",
    )


class TranscriptOutputConfig(proto.Message):
    r"""Specifies an optional destination for the recognition
    results.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        gcs_uri (str):
            Specifies a Cloud Storage URI for the recognition results.
            Must be specified in the format:
            ``gs://bucket_name/object_name``, and the bucket must
            already exist.

            This field is a member of `oneof`_ ``output_type``.
    """

    gcs_uri = proto.Field(proto.STRING, number=1, oneof="output_type",)


class StreamingRecognizeRequest(proto.Message):
    r"""The top-level message sent by the client for the
    ``StreamingRecognize`` method. Multiple
    ``StreamingRecognizeRequest`` messages are sent. The first message
    must contain a ``streaming_config`` message and must not contain
    ``audio_content``. All subsequent messages must contain
    ``audio_content`` and must not contain a ``streaming_config``
    message.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        streaming_config (google.cloud.speech_v1.types.StreamingRecognitionConfig):
            Provides information to the recognizer that specifies how to
            process the request. The first ``StreamingRecognizeRequest``
            message must contain a ``streaming_config`` message.

            This field is a member of `oneof`_ ``streaming_request``.
        audio_content (bytes):
            The audio data to be recognized. Sequential chunks of audio
            data are sent in sequential ``StreamingRecognizeRequest``
            messages. The first ``StreamingRecognizeRequest`` message
            must not contain ``audio_content`` data and all subsequent
            ``StreamingRecognizeRequest`` messages must contain
            ``audio_content`` data. The audio bytes must be encoded as
            specified in ``RecognitionConfig``. Note: as with all bytes
            fields, proto buffers use a pure binary representation (not
            base64). See `content
            limits <https://cloud.google.com/speech-to-text/quotas#content>`__.

            This field is a member of `oneof`_ ``streaming_request``.
    """

    streaming_config = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="streaming_request",
        message="StreamingRecognitionConfig",
    )
    audio_content = proto.Field(proto.BYTES, number=2, oneof="streaming_request",)


class StreamingRecognitionConfig(proto.Message):
    r"""Provides information to the recognizer that specifies how to
    process the request.

    Attributes:
        config (google.cloud.speech_v1.types.RecognitionConfig):
            Required. Provides information to the
            recognizer that specifies how to process the
            request.
        single_utterance (bool):
            If ``false`` or omitted, the recognizer will perform
            continuous recognition (continuing to wait for and process
            audio even if the user pauses speaking) until the client
            closes the input stream (gRPC API) or until the maximum time
            limit has been reached. May return multiple
            ``StreamingRecognitionResult``\ s with the ``is_final`` flag
            set to ``true``.

            If ``true``, the recognizer will detect a single spoken
            utterance. When it detects that the user has paused or
            stopped speaking, it will return an
            ``END_OF_SINGLE_UTTERANCE`` event and cease recognition. It
            will return no more than one ``StreamingRecognitionResult``
            with the ``is_final`` flag set to ``true``.

            The ``single_utterance`` field can only be used with
            specified models, otherwise an error is thrown. The
            ``model`` field in [``RecognitionConfig``][] must be set to:

            -  ``command_and_search``
            -  ``phone_call`` AND additional field
               ``useEnhanced``\ =\ ``true``
            -  The ``model`` field is left undefined. In this case the
               API auto-selects a model based on any other parameters
               that you set in ``RecognitionConfig``.
        interim_results (bool):
            If ``true``, interim results (tentative hypotheses) may be
            returned as they become available (these interim results are
            indicated with the ``is_final=false`` flag). If ``false`` or
            omitted, only ``is_final=true`` result(s) are returned.
    """

    config = proto.Field(proto.MESSAGE, number=1, message="RecognitionConfig",)
    single_utterance = proto.Field(proto.BOOL, number=2,)
    interim_results = proto.Field(proto.BOOL, number=3,)


class RecognitionConfig(proto.Message):
    r"""Provides information to the recognizer that specifies how to
    process the request.

    Attributes:
        encoding (google.cloud.speech_v1.types.RecognitionConfig.AudioEncoding):
            Encoding of audio data sent in all ``RecognitionAudio``
            messages. This field is optional for ``FLAC`` and ``WAV``
            audio files and required for all other audio formats. For
            details, see
            [AudioEncoding][google.cloud.speech.v1.RecognitionConfig.AudioEncoding].
        sample_rate_hertz (int):
            Sample rate in Hertz of the audio data sent in all
            ``RecognitionAudio`` messages. Valid values are: 8000-48000.
            16000 is optimal. For best results, set the sampling rate of
            the audio source to 16000 Hz. If that's not possible, use
            the native sample rate of the audio source (instead of
            re-sampling). This field is optional for FLAC and WAV audio
            files, but is required for all other audio formats. For
            details, see
            [AudioEncoding][google.cloud.speech.v1.RecognitionConfig.AudioEncoding].
        audio_channel_count (int):
            The number of channels in the input audio data. ONLY set
            this for MULTI-CHANNEL recognition. Valid values for
            LINEAR16 and FLAC are ``1``-``8``. Valid values for OGG_OPUS
            are '1'-'254'. Valid value for MULAW, AMR, AMR_WB and
            SPEEX_WITH_HEADER_BYTE is only ``1``. If ``0`` or omitted,
            defaults to one channel (mono). Note: We only recognize the
            first channel by default. To perform independent recognition
            on each channel set
            ``enable_separate_recognition_per_channel`` to 'true'.
        enable_separate_recognition_per_channel (bool):
            This needs to be set to ``true`` explicitly and
            ``audio_channel_count`` > 1 to get each channel recognized
            separately. The recognition result will contain a
            ``channel_tag`` field to state which channel that result
            belongs to. If this is not true, we will only recognize the
            first channel. The request is billed cumulatively for all
            channels recognized: ``audio_channel_count`` multiplied by
            the length of the audio.
        language_code (str):
            Required. The language of the supplied audio as a
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tag. Example: "en-US". See `Language
            Support <https://cloud.google.com/speech-to-text/docs/languages>`__
            for a list of the currently supported language codes.
        alternative_language_codes (Sequence[str]):
            A list of up to 3 additional
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tags, listing possible alternative languages of the
            supplied audio. See `Language
            Support <https://cloud.google.com/speech-to-text/docs/languages>`__
            for a list of the currently supported language codes. If
            alternative languages are listed, recognition result will
            contain recognition in the most likely language detected
            including the main language_code. The recognition result
            will include the language tag of the language detected in
            the audio. Note: This feature is only supported for Voice
            Command and Voice Search use cases and performance may vary
            for other use cases (e.g., phone call transcription).
        max_alternatives (int):
            Maximum number of recognition hypotheses to be returned.
            Specifically, the maximum number of
            ``SpeechRecognitionAlternative`` messages within each
            ``SpeechRecognitionResult``. The server may return fewer
            than ``max_alternatives``. Valid values are ``0``-``30``. A
            value of ``0`` or ``1`` will return a maximum of one. If
            omitted, will return a maximum of one.
        profanity_filter (bool):
            If set to ``true``, the server will attempt to filter out
            profanities, replacing all but the initial character in each
            filtered word with asterisks, e.g. "f***". If set to
            ``false`` or omitted, profanities won't be filtered out.
        adaptation (google.cloud.speech_v1.types.SpeechAdaptation):
            Speech adaptation configuration improves the accuracy of
            speech recognition. For more information, see the `speech
            adaptation <https://cloud.google.com/speech-to-text/docs/adaptation>`__
            documentation. When speech adaptation is set it supersedes
            the ``speech_contexts`` field.
        speech_contexts (Sequence[google.cloud.speech_v1.types.SpeechContext]):
            Array of
            [SpeechContext][google.cloud.speech.v1.SpeechContext]. A
            means to provide context to assist the speech recognition.
            For more information, see `speech
            adaptation <https://cloud.google.com/speech-to-text/docs/adaptation>`__.
        enable_word_time_offsets (bool):
            If ``true``, the top result includes a list of words and the
            start and end time offsets (timestamps) for those words. If
            ``false``, no word-level time offset information is
            returned. The default is ``false``.
        enable_word_confidence (bool):
            If ``true``, the top result includes a list of words and the
            confidence for those words. If ``false``, no word-level
            confidence information is returned. The default is
            ``false``.
        enable_automatic_punctuation (bool):
            If 'true', adds punctuation to recognition
            result hypotheses. This feature is only
            available in select languages. Setting this for
            requests in other languages has no effect at
            all. The default 'false' value does not add
            punctuation to result hypotheses.
        enable_spoken_punctuation (google.protobuf.wrappers_pb2.BoolValue):
            The spoken punctuation behavior for the call If not set,
            uses default behavior based on model of choice e.g.
            command_and_search will enable spoken punctuation by default
            If 'true', replaces spoken punctuation with the
            corresponding symbols in the request. For example, "how are
            you question mark" becomes "how are you?". See
            https://cloud.google.com/speech-to-text/docs/spoken-punctuation
            for support. If 'false', spoken punctuation is not replaced.
        enable_spoken_emojis (google.protobuf.wrappers_pb2.BoolValue):
            The spoken emoji behavior for the call
            If not set, uses default behavior based on model
            of choice If 'true', adds spoken emoji
            formatting for the request. This will replace
            spoken emojis with the corresponding Unicode
            symbols in the final transcript. If 'false',
            spoken emojis are not replaced.
        diarization_config (google.cloud.speech_v1.types.SpeakerDiarizationConfig):
            Config to enable speaker diarization and set
            additional parameters to make diarization better
            suited for your application. Note: When this is
            enabled, we send all the words from the
            beginning of the audio for the top alternative
            in every consecutive STREAMING responses. This
            is done in order to improve our speaker tags as
            our models learn to identify the speakers in the
            conversation over time. For non-streaming
            requests, the diarization results will be
            provided only in the top alternative of the
            FINAL SpeechRecognitionResult.
        metadata (google.cloud.speech_v1.types.RecognitionMetadata):
            Metadata regarding this request.
        model (str):
            Which model to select for the given request. Select the
            model best suited to your domain to get best results. If a
            model is not explicitly specified, then we auto-select a
            model based on the parameters in the RecognitionConfig.

            .. raw:: html

                <table>
                  <tr>
                    <td><b>Model</b></td>
                    <td><b>Description</b></td>
                  </tr>
                  <tr>
                    <td><code>command_and_search</code></td>
                    <td>Best for short queries such as voice commands or voice search.</td>
                  </tr>
                  <tr>
                    <td><code>phone_call</code></td>
                    <td>Best for audio that originated from a phone call (typically
                    recorded at an 8khz sampling rate).</td>
                  </tr>
                  <tr>
                    <td><code>video</code></td>
                    <td>Best for audio that originated from video or includes multiple
                        speakers. Ideally the audio is recorded at a 16khz or greater
                        sampling rate. This is a premium model that costs more than the
                        standard rate.</td>
                  </tr>
                  <tr>
                    <td><code>default</code></td>
                    <td>Best for audio that is not one of the specific audio models.
                        For example, long-form audio. Ideally the audio is high-fidelity,
                        recorded at a 16khz or greater sampling rate.</td>
                  </tr>
                </table>
        use_enhanced (bool):
            Set to true to use an enhanced model for speech recognition.
            If ``use_enhanced`` is set to true and the ``model`` field
            is not set, then an appropriate enhanced model is chosen if
            an enhanced model exists for the audio.

            If ``use_enhanced`` is true and an enhanced version of the
            specified model does not exist, then the speech is
            recognized using the standard version of the specified
            model.
    """

    class AudioEncoding(proto.Enum):
        r"""The encoding of the audio data sent in the request.

        All encodings support only 1 channel (mono) audio, unless the
        ``audio_channel_count`` and
        ``enable_separate_recognition_per_channel`` fields are set.

        For best results, the audio source should be captured and
        transmitted using a lossless encoding (``FLAC`` or ``LINEAR16``).
        The accuracy of the speech recognition can be reduced if lossy
        codecs are used to capture or transmit audio, particularly if
        background noise is present. Lossy codecs include ``MULAW``,
        ``AMR``, ``AMR_WB``, ``OGG_OPUS``, ``SPEEX_WITH_HEADER_BYTE``,
        ``MP3``, and ``WEBM_OPUS``.

        The ``FLAC`` and ``WAV`` audio file formats include a header that
        describes the included audio content. You can request recognition
        for ``WAV`` files that contain either ``LINEAR16`` or ``MULAW``
        encoded audio. If you send ``FLAC`` or ``WAV`` audio file format in
        your request, you do not need to specify an ``AudioEncoding``; the
        audio encoding format is determined from the file header. If you
        specify an ``AudioEncoding`` when you send send ``FLAC`` or ``WAV``
        audio, the encoding configuration must match the encoding described
        in the audio header; otherwise the request returns an
        [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT]
        error code.
        """
        ENCODING_UNSPECIFIED = 0
        LINEAR16 = 1
        FLAC = 2
        MULAW = 3
        AMR = 4
        AMR_WB = 5
        OGG_OPUS = 6
        SPEEX_WITH_HEADER_BYTE = 7
        WEBM_OPUS = 9

    encoding = proto.Field(proto.ENUM, number=1, enum=AudioEncoding,)
    sample_rate_hertz = proto.Field(proto.INT32, number=2,)
    audio_channel_count = proto.Field(proto.INT32, number=7,)
    enable_separate_recognition_per_channel = proto.Field(proto.BOOL, number=12,)
    language_code = proto.Field(proto.STRING, number=3,)
    alternative_language_codes = proto.RepeatedField(proto.STRING, number=18,)
    max_alternatives = proto.Field(proto.INT32, number=4,)
    profanity_filter = proto.Field(proto.BOOL, number=5,)
    adaptation = proto.Field(
        proto.MESSAGE, number=20, message=resource.SpeechAdaptation,
    )
    speech_contexts = proto.RepeatedField(
        proto.MESSAGE, number=6, message="SpeechContext",
    )
    enable_word_time_offsets = proto.Field(proto.BOOL, number=8,)
    enable_word_confidence = proto.Field(proto.BOOL, number=15,)
    enable_automatic_punctuation = proto.Field(proto.BOOL, number=11,)
    enable_spoken_punctuation = proto.Field(
        proto.MESSAGE, number=22, message=wrappers_pb2.BoolValue,
    )
    enable_spoken_emojis = proto.Field(
        proto.MESSAGE, number=23, message=wrappers_pb2.BoolValue,
    )
    diarization_config = proto.Field(
        proto.MESSAGE, number=19, message="SpeakerDiarizationConfig",
    )
    metadata = proto.Field(proto.MESSAGE, number=9, message="RecognitionMetadata",)
    model = proto.Field(proto.STRING, number=13,)
    use_enhanced = proto.Field(proto.BOOL, number=14,)


class SpeakerDiarizationConfig(proto.Message):
    r"""Config to enable speaker diarization.

    Attributes:
        enable_speaker_diarization (bool):
            If 'true', enables speaker detection for each recognized
            word in the top alternative of the recognition result using
            a speaker_tag provided in the WordInfo.
        min_speaker_count (int):
            Minimum number of speakers in the
            conversation. This range gives you more
            flexibility by allowing the system to
            automatically determine the correct number of
            speakers. If not set, the default value is 2.
        max_speaker_count (int):
            Maximum number of speakers in the
            conversation. This range gives you more
            flexibility by allowing the system to
            automatically determine the correct number of
            speakers. If not set, the default value is 6.
        speaker_tag (int):
            Output only. Unused.
    """

    enable_speaker_diarization = proto.Field(proto.BOOL, number=1,)
    min_speaker_count = proto.Field(proto.INT32, number=2,)
    max_speaker_count = proto.Field(proto.INT32, number=3,)
    speaker_tag = proto.Field(proto.INT32, number=5,)


class RecognitionMetadata(proto.Message):
    r"""Description of audio data to be recognized.

    Attributes:
        interaction_type (google.cloud.speech_v1.types.RecognitionMetadata.InteractionType):
            The use case most closely describing the
            audio content to be recognized.
        industry_naics_code_of_audio (int):
            The industry vertical to which this speech
            recognition request most closely applies. This
            is most indicative of the topics contained in
            the audio.  Use the 6-digit NAICS code to
            identify the industry vertical - see
            https://www.naics.com/search/.
        microphone_distance (google.cloud.speech_v1.types.RecognitionMetadata.MicrophoneDistance):
            The audio type that most closely describes
            the audio being recognized.
        original_media_type (google.cloud.speech_v1.types.RecognitionMetadata.OriginalMediaType):
            The original media the speech was recorded
            on.
        recording_device_type (google.cloud.speech_v1.types.RecognitionMetadata.RecordingDeviceType):
            The type of device the speech was recorded
            with.
        recording_device_name (str):
            The device used to make the recording.
            Examples 'Nexus 5X' or 'Polycom SoundStation IP
            6000' or 'POTS' or 'VoIP' or 'Cardioid
            Microphone'.
        original_mime_type (str):
            Mime type of the original audio file. For example
            ``audio/m4a``, ``audio/x-alaw-basic``, ``audio/mp3``,
            ``audio/3gpp``. A list of possible audio mime types is
            maintained at
            http://www.iana.org/assignments/media-types/media-types.xhtml#audio
        audio_topic (str):
            Description of the content. Eg. "Recordings
            of federal supreme court hearings from 2012".
    """

    class InteractionType(proto.Enum):
        r"""Use case categories that the audio recognition request can be
        described by.
        """
        INTERACTION_TYPE_UNSPECIFIED = 0
        DISCUSSION = 1
        PRESENTATION = 2
        PHONE_CALL = 3
        VOICEMAIL = 4
        PROFESSIONALLY_PRODUCED = 5
        VOICE_SEARCH = 6
        VOICE_COMMAND = 7
        DICTATION = 8

    class MicrophoneDistance(proto.Enum):
        r"""Enumerates the types of capture settings describing an audio
        file.
        """
        MICROPHONE_DISTANCE_UNSPECIFIED = 0
        NEARFIELD = 1
        MIDFIELD = 2
        FARFIELD = 3

    class OriginalMediaType(proto.Enum):
        r"""The original media the speech was recorded on."""
        ORIGINAL_MEDIA_TYPE_UNSPECIFIED = 0
        AUDIO = 1
        VIDEO = 2

    class RecordingDeviceType(proto.Enum):
        r"""The type of device the speech was recorded with."""
        RECORDING_DEVICE_TYPE_UNSPECIFIED = 0
        SMARTPHONE = 1
        PC = 2
        PHONE_LINE = 3
        VEHICLE = 4
        OTHER_OUTDOOR_DEVICE = 5
        OTHER_INDOOR_DEVICE = 6

    interaction_type = proto.Field(proto.ENUM, number=1, enum=InteractionType,)
    industry_naics_code_of_audio = proto.Field(proto.UINT32, number=3,)
    microphone_distance = proto.Field(proto.ENUM, number=4, enum=MicrophoneDistance,)
    original_media_type = proto.Field(proto.ENUM, number=5, enum=OriginalMediaType,)
    recording_device_type = proto.Field(proto.ENUM, number=6, enum=RecordingDeviceType,)
    recording_device_name = proto.Field(proto.STRING, number=7,)
    original_mime_type = proto.Field(proto.STRING, number=8,)
    audio_topic = proto.Field(proto.STRING, number=10,)


class SpeechContext(proto.Message):
    r"""Provides "hints" to the speech recognizer to favor specific
    words and phrases in the results.

    Attributes:
        phrases (Sequence[str]):
            A list of strings containing words and phrases "hints" so
            that the speech recognition is more likely to recognize
            them. This can be used to improve the accuracy for specific
            words and phrases, for example, if specific commands are
            typically spoken by the user. This can also be used to add
            additional words to the vocabulary of the recognizer. See
            `usage
            limits <https://cloud.google.com/speech-to-text/quotas#content>`__.

            List items can also be set to classes for groups of words
            that represent common concepts that occur in natural
            language. For example, rather than providing phrase hints
            for every month of the year, using the $MONTH class improves
            the likelihood of correctly transcribing audio that includes
            months.
        boost (float):
            Hint Boost. Positive value will increase the probability
            that a specific phrase will be recognized over other similar
            sounding phrases. The higher the boost, the higher the
            chance of false positive recognition as well. Negative boost
            values would correspond to anti-biasing. Anti-biasing is not
            enabled, so negative boost will simply be ignored. Though
            ``boost`` can accept a wide range of positive values, most
            use cases are best served with values between 0 and 20. We
            recommend using a binary search approach to finding the
            optimal value for your use case.
    """

    phrases = proto.RepeatedField(proto.STRING, number=1,)
    boost = proto.Field(proto.FLOAT, number=4,)


class RecognitionAudio(proto.Message):
    r"""Contains audio data in the encoding specified in the
    ``RecognitionConfig``. Either ``content`` or ``uri`` must be
    supplied. Supplying both or neither returns
    [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
    See `content
    limits <https://cloud.google.com/speech-to-text/quotas#content>`__.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        content (bytes):
            The audio data bytes encoded as specified in
            ``RecognitionConfig``. Note: as with all bytes fields, proto
            buffers use a pure binary representation, whereas JSON
            representations use base64.

            This field is a member of `oneof`_ ``audio_source``.
        uri (str):
            URI that points to a file that contains audio data bytes as
            specified in ``RecognitionConfig``. The file must not be
            compressed (for example, gzip). Currently, only Google Cloud
            Storage URIs are supported, which must be specified in the
            following format: ``gs://bucket_name/object_name`` (other
            URI formats return
            [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT]).
            For more information, see `Request
            URIs <https://cloud.google.com/storage/docs/reference-uris>`__.

            This field is a member of `oneof`_ ``audio_source``.
    """

    content = proto.Field(proto.BYTES, number=1, oneof="audio_source",)
    uri = proto.Field(proto.STRING, number=2, oneof="audio_source",)


class RecognizeResponse(proto.Message):
    r"""The only message returned to the client by the ``Recognize`` method.
    It contains the result as zero or more sequential
    ``SpeechRecognitionResult`` messages.

    Attributes:
        results (Sequence[google.cloud.speech_v1.types.SpeechRecognitionResult]):
            Sequential list of transcription results
            corresponding to sequential portions of audio.
        total_billed_time (google.protobuf.duration_pb2.Duration):
            When available, billed audio seconds for the
            corresponding request.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="SpeechRecognitionResult",
    )
    total_billed_time = proto.Field(
        proto.MESSAGE, number=3, message=duration_pb2.Duration,
    )


class LongRunningRecognizeResponse(proto.Message):
    r"""The only message returned to the client by the
    ``LongRunningRecognize`` method. It contains the result as zero or
    more sequential ``SpeechRecognitionResult`` messages. It is included
    in the ``result.response`` field of the ``Operation`` returned by
    the ``GetOperation`` call of the ``google::longrunning::Operations``
    service.

    Attributes:
        results (Sequence[google.cloud.speech_v1.types.SpeechRecognitionResult]):
            Sequential list of transcription results
            corresponding to sequential portions of audio.
        total_billed_time (google.protobuf.duration_pb2.Duration):
            When available, billed audio seconds for the
            corresponding request.
        output_config (google.cloud.speech_v1.types.TranscriptOutputConfig):
            Original output config if present in the
            request.
        output_error (google.rpc.status_pb2.Status):
            If the transcript output fails this field
            contains the relevant error.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="SpeechRecognitionResult",
    )
    total_billed_time = proto.Field(
        proto.MESSAGE, number=3, message=duration_pb2.Duration,
    )
    output_config = proto.Field(
        proto.MESSAGE, number=6, message="TranscriptOutputConfig",
    )
    output_error = proto.Field(proto.MESSAGE, number=7, message=status_pb2.Status,)


class LongRunningRecognizeMetadata(proto.Message):
    r"""Describes the progress of a long-running ``LongRunningRecognize``
    call. It is included in the ``metadata`` field of the ``Operation``
    returned by the ``GetOperation`` call of the
    ``google::longrunning::Operations`` service.

    Attributes:
        progress_percent (int):
            Approximate percentage of audio processed
            thus far. Guaranteed to be 100 when the audio is
            fully processed and the results are available.
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Time when the request was received.
        last_update_time (google.protobuf.timestamp_pb2.Timestamp):
            Time of the most recent processing update.
        uri (str):
            Output only. The URI of the audio file being
            transcribed. Empty if the audio was sent as byte
            content.
    """

    progress_percent = proto.Field(proto.INT32, number=1,)
    start_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    last_update_time = proto.Field(
        proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,
    )
    uri = proto.Field(proto.STRING, number=4,)


class StreamingRecognizeResponse(proto.Message):
    r"""``StreamingRecognizeResponse`` is the only message returned to the
    client by ``StreamingRecognize``. A series of zero or more
    ``StreamingRecognizeResponse`` messages are streamed back to the
    client. If there is no recognizable audio, and ``single_utterance``
    is set to false, then no messages are streamed back to the client.

    Here's an example of a series of ``StreamingRecognizeResponse``\ s
    that might be returned while processing audio:

    1. results { alternatives { transcript: "tube" } stability: 0.01 }

    2. results { alternatives { transcript: "to be a" } stability: 0.01
       }

    3. results { alternatives { transcript: "to be" } stability: 0.9 }
       results { alternatives { transcript: " or not to be" } stability:
       0.01 }

    4. results { alternatives { transcript: "to be or not to be"
       confidence: 0.92 } alternatives { transcript: "to bee or not to
       bee" } is_final: true }

    5. results { alternatives { transcript: " that's" } stability: 0.01
       }

    6. results { alternatives { transcript: " that is" } stability: 0.9
       } results { alternatives { transcript: " the question" }
       stability: 0.01 }

    7. results { alternatives { transcript: " that is the question"
       confidence: 0.98 } alternatives { transcript: " that was the
       question" } is_final: true }

    Notes:

    -  Only two of the above responses #4 and #7 contain final results;
       they are indicated by ``is_final: true``. Concatenating these
       together generates the full transcript: "to be or not to be that
       is the question".

    -  The others contain interim ``results``. #3 and #6 contain two
       interim ``results``: the first portion has a high stability and
       is less likely to change; the second portion has a low stability
       and is very likely to change. A UI designer might choose to show
       only high stability ``results``.

    -  The specific ``stability`` and ``confidence`` values shown above
       are only for illustrative purposes. Actual values may vary.

    -  In each response, only one of these fields will be set:
       ``error``, ``speech_event_type``, or one or more (repeated)
       ``results``.

    Attributes:
        error (google.rpc.status_pb2.Status):
            If set, returns a [google.rpc.Status][google.rpc.Status]
            message that specifies the error for the operation.
        results (Sequence[google.cloud.speech_v1.types.StreamingRecognitionResult]):
            This repeated list contains zero or more results that
            correspond to consecutive portions of the audio currently
            being processed. It contains zero or one ``is_final=true``
            result (the newly settled portion), followed by zero or more
            ``is_final=false`` results (the interim results).
        speech_event_type (google.cloud.speech_v1.types.StreamingRecognizeResponse.SpeechEventType):
            Indicates the type of speech event.
        total_billed_time (google.protobuf.duration_pb2.Duration):
            When available, billed audio seconds for the
            stream. Set only if this is the last response in
            the stream.
    """

    class SpeechEventType(proto.Enum):
        r"""Indicates the type of speech event."""
        SPEECH_EVENT_UNSPECIFIED = 0
        END_OF_SINGLE_UTTERANCE = 1

    error = proto.Field(proto.MESSAGE, number=1, message=status_pb2.Status,)
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="StreamingRecognitionResult",
    )
    speech_event_type = proto.Field(proto.ENUM, number=4, enum=SpeechEventType,)
    total_billed_time = proto.Field(
        proto.MESSAGE, number=5, message=duration_pb2.Duration,
    )


class StreamingRecognitionResult(proto.Message):
    r"""A streaming speech recognition result corresponding to a
    portion of the audio that is currently being processed.

    Attributes:
        alternatives (Sequence[google.cloud.speech_v1.types.SpeechRecognitionAlternative]):
            May contain one or more recognition hypotheses (up to the
            maximum specified in ``max_alternatives``). These
            alternatives are ordered in terms of accuracy, with the top
            (first) alternative being the most probable, as ranked by
            the recognizer.
        is_final (bool):
            If ``false``, this ``StreamingRecognitionResult`` represents
            an interim result that may change. If ``true``, this is the
            final time the speech service will return this particular
            ``StreamingRecognitionResult``, the recognizer will not
            return any further hypotheses for this portion of the
            transcript and corresponding audio.
        stability (float):
            An estimate of the likelihood that the recognizer will not
            change its guess about this interim result. Values range
            from 0.0 (completely unstable) to 1.0 (completely stable).
            This field is only provided for interim results
            (``is_final=false``). The default of 0.0 is a sentinel value
            indicating ``stability`` was not set.
        result_end_time (google.protobuf.duration_pb2.Duration):
            Time offset of the end of this result
            relative to the beginning of the audio.
        channel_tag (int):
            For multi-channel audio, this is the channel number
            corresponding to the recognized result for the audio from
            that channel. For audio_channel_count = N, its output values
            can range from '1' to 'N'.
        language_code (str):
            Output only. The
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tag of the language in this result. This language
            code was detected to have the most likelihood of being
            spoken in the audio.
    """

    alternatives = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SpeechRecognitionAlternative",
    )
    is_final = proto.Field(proto.BOOL, number=2,)
    stability = proto.Field(proto.FLOAT, number=3,)
    result_end_time = proto.Field(
        proto.MESSAGE, number=4, message=duration_pb2.Duration,
    )
    channel_tag = proto.Field(proto.INT32, number=5,)
    language_code = proto.Field(proto.STRING, number=6,)


class SpeechRecognitionResult(proto.Message):
    r"""A speech recognition result corresponding to a portion of the
    audio.

    Attributes:
        alternatives (Sequence[google.cloud.speech_v1.types.SpeechRecognitionAlternative]):
            May contain one or more recognition hypotheses (up to the
            maximum specified in ``max_alternatives``). These
            alternatives are ordered in terms of accuracy, with the top
            (first) alternative being the most probable, as ranked by
            the recognizer.
        channel_tag (int):
            For multi-channel audio, this is the channel number
            corresponding to the recognized result for the audio from
            that channel. For audio_channel_count = N, its output values
            can range from '1' to 'N'.
        result_end_time (google.protobuf.duration_pb2.Duration):
            Time offset of the end of this result
            relative to the beginning of the audio.
        language_code (str):
            Output only. The
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tag of the language in this result. This language
            code was detected to have the most likelihood of being
            spoken in the audio.
    """

    alternatives = proto.RepeatedField(
        proto.MESSAGE, number=1, message="SpeechRecognitionAlternative",
    )
    channel_tag = proto.Field(proto.INT32, number=2,)
    result_end_time = proto.Field(
        proto.MESSAGE, number=4, message=duration_pb2.Duration,
    )
    language_code = proto.Field(proto.STRING, number=5,)


class SpeechRecognitionAlternative(proto.Message):
    r"""Alternative hypotheses (a.k.a. n-best list).

    Attributes:
        transcript (str):
            Transcript text representing the words that
            the user spoke.
        confidence (float):
            The confidence estimate between 0.0 and 1.0. A higher number
            indicates an estimated greater likelihood that the
            recognized words are correct. This field is set only for the
            top alternative of a non-streaming result or, of a streaming
            result where ``is_final=true``. This field is not guaranteed
            to be accurate and users should not rely on it to be always
            provided. The default of 0.0 is a sentinel value indicating
            ``confidence`` was not set.
        words (Sequence[google.cloud.speech_v1.types.WordInfo]):
            A list of word-specific information for each recognized
            word. Note: When ``enable_speaker_diarization`` is true, you
            will see all the words from the beginning of the audio.
    """

    transcript = proto.Field(proto.STRING, number=1,)
    confidence = proto.Field(proto.FLOAT, number=2,)
    words = proto.RepeatedField(proto.MESSAGE, number=3, message="WordInfo",)


class WordInfo(proto.Message):
    r"""Word-specific information for recognized words.

    Attributes:
        start_time (google.protobuf.duration_pb2.Duration):
            Time offset relative to the beginning of the audio, and
            corresponding to the start of the spoken word. This field is
            only set if ``enable_word_time_offsets=true`` and only in
            the top hypothesis. This is an experimental feature and the
            accuracy of the time offset can vary.
        end_time (google.protobuf.duration_pb2.Duration):
            Time offset relative to the beginning of the audio, and
            corresponding to the end of the spoken word. This field is
            only set if ``enable_word_time_offsets=true`` and only in
            the top hypothesis. This is an experimental feature and the
            accuracy of the time offset can vary.
        word (str):
            The word corresponding to this set of
            information.
        confidence (float):
            The confidence estimate between 0.0 and 1.0. A higher number
            indicates an estimated greater likelihood that the
            recognized words are correct. This field is set only for the
            top alternative of a non-streaming result or, of a streaming
            result where ``is_final=true``. This field is not guaranteed
            to be accurate and users should not rely on it to be always
            provided. The default of 0.0 is a sentinel value indicating
            ``confidence`` was not set.
        speaker_tag (int):
            Output only. A distinct integer value is assigned for every
            speaker within the audio. This field specifies which one of
            those speakers was detected to have spoken this word. Value
            ranges from '1' to diarization_speaker_count. speaker_tag is
            set if enable_speaker_diarization = 'true' and only in the
            top alternative.
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=duration_pb2.Duration,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)
    word = proto.Field(proto.STRING, number=3,)
    confidence = proto.Field(proto.FLOAT, number=4,)
    speaker_tag = proto.Field(proto.INT32, number=5,)


__all__ = tuple(sorted(__protobuf__.manifest))
