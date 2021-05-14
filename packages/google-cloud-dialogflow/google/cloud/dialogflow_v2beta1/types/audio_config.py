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

from google.protobuf import duration_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.dialogflow.v2beta1",
    manifest={
        "AudioEncoding",
        "SpeechModelVariant",
        "SsmlVoiceGender",
        "OutputAudioEncoding",
        "TelephonyDtmf",
        "SpeechContext",
        "SpeechWordInfo",
        "InputAudioConfig",
        "VoiceSelectionParams",
        "SynthesizeSpeechConfig",
        "OutputAudioConfig",
        "TelephonyDtmfEvents",
        "SpeechToTextConfig",
    },
)


class AudioEncoding(proto.Enum):
    r"""Audio encoding of the audio content sent in the conversational query
    request. Refer to the `Cloud Speech API
    documentation <https://cloud.google.com/speech-to-text/docs/basics>`__
    for more details.
    """
    AUDIO_ENCODING_UNSPECIFIED = 0
    AUDIO_ENCODING_LINEAR_16 = 1
    AUDIO_ENCODING_FLAC = 2
    AUDIO_ENCODING_MULAW = 3
    AUDIO_ENCODING_AMR = 4
    AUDIO_ENCODING_AMR_WB = 5
    AUDIO_ENCODING_OGG_OPUS = 6
    AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE = 7


class SpeechModelVariant(proto.Enum):
    r"""Variant of the specified [Speech
    model][google.cloud.dialogflow.v2beta1.InputAudioConfig.model] to
    use.

    See the `Cloud Speech
    documentation <https://cloud.google.com/speech-to-text/docs/enhanced-models>`__
    for which models have different variants. For example, the
    "phone_call" model has both a standard and an enhanced variant. When
    you use an enhanced model, you will generally receive higher quality
    results than for a standard model.
    """
    SPEECH_MODEL_VARIANT_UNSPECIFIED = 0
    USE_BEST_AVAILABLE = 1
    USE_STANDARD = 2
    USE_ENHANCED = 3


class SsmlVoiceGender(proto.Enum):
    r"""Gender of the voice as described in `SSML voice
    element <https://www.w3.org/TR/speech-synthesis11/#edef_voice>`__.
    """
    SSML_VOICE_GENDER_UNSPECIFIED = 0
    SSML_VOICE_GENDER_MALE = 1
    SSML_VOICE_GENDER_FEMALE = 2
    SSML_VOICE_GENDER_NEUTRAL = 3


class OutputAudioEncoding(proto.Enum):
    r"""Audio encoding of the output audio format in Text-To-Speech."""
    OUTPUT_AUDIO_ENCODING_UNSPECIFIED = 0
    OUTPUT_AUDIO_ENCODING_LINEAR_16 = 1
    OUTPUT_AUDIO_ENCODING_MP3 = 2
    OUTPUT_AUDIO_ENCODING_MP3_64_KBPS = 4
    OUTPUT_AUDIO_ENCODING_OGG_OPUS = 3
    OUTPUT_AUDIO_ENCODING_MULAW = 5


class TelephonyDtmf(proto.Enum):
    r"""`DTMF <https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling>`__
    digit in Telephony Gateway.
    """
    TELEPHONY_DTMF_UNSPECIFIED = 0
    DTMF_ONE = 1
    DTMF_TWO = 2
    DTMF_THREE = 3
    DTMF_FOUR = 4
    DTMF_FIVE = 5
    DTMF_SIX = 6
    DTMF_SEVEN = 7
    DTMF_EIGHT = 8
    DTMF_NINE = 9
    DTMF_ZERO = 10
    DTMF_A = 11
    DTMF_B = 12
    DTMF_C = 13
    DTMF_D = 14
    DTMF_STAR = 15
    DTMF_POUND = 16


class SpeechContext(proto.Message):
    r"""Hints for the speech recognizer to help with recognition in a
    specific conversation state.

    Attributes:
        phrases (Sequence[str]):
            Optional. A list of strings containing words and phrases
            that the speech recognizer should recognize with higher
            likelihood.

            This list can be used to:

            -  improve accuracy for words and phrases you expect the
               user to say, e.g. typical commands for your Dialogflow
               agent
            -  add additional words to the speech recognizer vocabulary
            -  ...

            See the `Cloud Speech
            documentation <https://cloud.google.com/speech-to-text/quotas>`__
            for usage limits.
        boost (float):
            Optional. Boost for this context compared to other contexts:

            -  If the boost is positive, Dialogflow will increase the
               probability that the phrases in this context are
               recognized over similar sounding phrases.
            -  If the boost is unspecified or non-positive, Dialogflow
               will not apply any boost.

            Dialogflow recommends that you use boosts in the range (0,
            20] and that you find a value that fits your use case with
            binary search.
    """

    phrases = proto.RepeatedField(proto.STRING, number=1,)
    boost = proto.Field(proto.FLOAT, number=2,)


class SpeechWordInfo(proto.Message):
    r"""Information for a word recognized by the speech recognizer.
    Attributes:
        word (str):
            The word this info is for.
        start_offset (google.protobuf.duration_pb2.Duration):
            Time offset relative to the beginning of the
            audio that corresponds to the start of the
            spoken word. This is an experimental feature and
            the accuracy of the time offset can vary.
        end_offset (google.protobuf.duration_pb2.Duration):
            Time offset relative to the beginning of the
            audio that corresponds to the end of the spoken
            word. This is an experimental feature and the
            accuracy of the time offset can vary.
        confidence (float):
            The Speech confidence between 0.0 and 1.0 for
            this word. A higher number indicates an
            estimated greater likelihood that the recognized
            word is correct. The default of 0.0 is a
            sentinel value indicating that confidence was
            not set.

            This field is not guaranteed to be fully stable
            over time for the same audio input. Users should
            also not rely on it to always be provided.
    """

    word = proto.Field(proto.STRING, number=3,)
    start_offset = proto.Field(proto.MESSAGE, number=1, message=duration_pb2.Duration,)
    end_offset = proto.Field(proto.MESSAGE, number=2, message=duration_pb2.Duration,)
    confidence = proto.Field(proto.FLOAT, number=4,)


class InputAudioConfig(proto.Message):
    r"""Instructs the speech recognizer on how to process the audio
    content.

    Attributes:
        audio_encoding (google.cloud.dialogflow_v2beta1.types.AudioEncoding):
            Required. Audio encoding of the audio content
            to process.
        sample_rate_hertz (int):
            Required. Sample rate (in Hertz) of the audio content sent
            in the query. Refer to `Cloud Speech API
            documentation <https://cloud.google.com/speech-to-text/docs/basics>`__
            for more details.
        language_code (str):
            Required. The language of the supplied audio. Dialogflow
            does not do translations. See `Language
            Support <https://cloud.google.com/dialogflow/docs/reference/language>`__
            for a list of the currently supported language codes. Note
            that queries in the same session do not necessarily need to
            specify the same language.
        enable_word_info (bool):
            If ``true``, Dialogflow returns
            [SpeechWordInfo][google.cloud.dialogflow.v2beta1.SpeechWordInfo]
            in
            [StreamingRecognitionResult][google.cloud.dialogflow.v2beta1.StreamingRecognitionResult]
            with information about the recognized speech words, e.g.
            start and end time offsets. If false or unspecified, Speech
            doesn't return any word-level information.
        phrase_hints (Sequence[str]):
            A list of strings containing words and phrases that the
            speech recognizer should recognize with higher likelihood.

            See `the Cloud Speech
            documentation <https://cloud.google.com/speech-to-text/docs/basics#phrase-hints>`__
            for more details.

            This field is deprecated. Please use `speech_contexts <>`__
            instead. If you specify both `phrase_hints <>`__ and
            `speech_contexts <>`__, Dialogflow will treat the
            `phrase_hints <>`__ as a single additional
            `SpeechContext <>`__.
        speech_contexts (Sequence[google.cloud.dialogflow_v2beta1.types.SpeechContext]):
            Context information to assist speech recognition.

            See `the Cloud Speech
            documentation <https://cloud.google.com/speech-to-text/docs/basics#phrase-hints>`__
            for more details.
        model (str):
            Which Speech model to select for the given request. Select
            the model best suited to your domain to get best results. If
            a model is not explicitly specified, then we auto-select a
            model based on the parameters in the InputAudioConfig. If
            enhanced speech model is enabled for the agent and an
            enhanced version of the specified model for the language
            does not exist, then the speech is recognized using the
            standard version of the specified model. Refer to `Cloud
            Speech API
            documentation <https://cloud.google.com/speech-to-text/docs/basics#select-model>`__
            for more details.
        model_variant (google.cloud.dialogflow_v2beta1.types.SpeechModelVariant):
            Which variant of the [Speech
            model][google.cloud.dialogflow.v2beta1.InputAudioConfig.model]
            to use.
        single_utterance (bool):
            If ``false`` (default), recognition does not cease until the
            client closes the stream. If ``true``, the recognizer will
            detect a single spoken utterance in input audio. Recognition
            ceases when it detects the audio's voice has stopped or
            paused. In this case, once a detected intent is received,
            the client should close the stream and start a new request
            with a new stream as needed. Note: This setting is relevant
            only for streaming methods. Note: When specified,
            InputAudioConfig.single_utterance takes precedence over
            StreamingDetectIntentRequest.single_utterance.
        disable_no_speech_recognized_event (bool):
            Only used in
            [Participants.AnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.AnalyzeContent]
            and
            [Participants.StreamingAnalyzeContent][google.cloud.dialogflow.v2beta1.Participants.StreamingAnalyzeContent].
            If ``false`` and recognition doesn't return any result,
            trigger ``NO_SPEECH_RECOGNIZED`` event to Dialogflow agent.
    """

    audio_encoding = proto.Field(proto.ENUM, number=1, enum="AudioEncoding",)
    sample_rate_hertz = proto.Field(proto.INT32, number=2,)
    language_code = proto.Field(proto.STRING, number=3,)
    enable_word_info = proto.Field(proto.BOOL, number=13,)
    phrase_hints = proto.RepeatedField(proto.STRING, number=4,)
    speech_contexts = proto.RepeatedField(
        proto.MESSAGE, number=11, message="SpeechContext",
    )
    model = proto.Field(proto.STRING, number=7,)
    model_variant = proto.Field(proto.ENUM, number=10, enum="SpeechModelVariant",)
    single_utterance = proto.Field(proto.BOOL, number=8,)
    disable_no_speech_recognized_event = proto.Field(proto.BOOL, number=14,)


class VoiceSelectionParams(proto.Message):
    r"""Description of which voice to use for speech synthesis.
    Attributes:
        name (str):
            Optional. The name of the voice. If not set, the service
            will choose a voice based on the other parameters such as
            language_code and
            [ssml_gender][google.cloud.dialogflow.v2beta1.VoiceSelectionParams.ssml_gender].

            For the list of available voices, please refer to `Supported
            voices and
            languages <https://cloud.google.com/text-to-speech/docs/voices>`__.
        ssml_gender (google.cloud.dialogflow_v2beta1.types.SsmlVoiceGender):
            Optional. The preferred gender of the voice. If not set, the
            service will choose a voice based on the other parameters
            such as language_code and
            [name][google.cloud.dialogflow.v2beta1.VoiceSelectionParams.name].
            Note that this is only a preference, not requirement. If a
            voice of the appropriate gender is not available, the
            synthesizer should substitute a voice with a different
            gender rather than failing the request.
    """

    name = proto.Field(proto.STRING, number=1,)
    ssml_gender = proto.Field(proto.ENUM, number=2, enum="SsmlVoiceGender",)


class SynthesizeSpeechConfig(proto.Message):
    r"""Configuration of how speech should be synthesized.
    Attributes:
        speaking_rate (float):
            Optional. Speaking rate/speed, in the range [0.25, 4.0]. 1.0
            is the normal native speed supported by the specific voice.
            2.0 is twice as fast, and 0.5 is half as fast. If
            unset(0.0), defaults to the native 1.0 speed. Any other
            values < 0.25 or > 4.0 will return an error.
        pitch (float):
            Optional. Speaking pitch, in the range [-20.0, 20.0]. 20
            means increase 20 semitones from the original pitch. -20
            means decrease 20 semitones from the original pitch.
        volume_gain_db (float):
            Optional. Volume gain (in dB) of the normal native volume
            supported by the specific voice, in the range [-96.0, 16.0].
            If unset, or set to a value of 0.0 (dB), will play at normal
            native signal amplitude. A value of -6.0 (dB) will play at
            approximately half the amplitude of the normal native signal
            amplitude. A value of +6.0 (dB) will play at approximately
            twice the amplitude of the normal native signal amplitude.
            We strongly recommend not to exceed +10 (dB) as there's
            usually no effective increase in loudness for any value
            greater than that.
        effects_profile_id (Sequence[str]):
            Optional. An identifier which selects 'audio
            effects' profiles that are applied on (post
            synthesized) text to speech. Effects are applied
            on top of each other in the order they are
            given.
        voice (google.cloud.dialogflow_v2beta1.types.VoiceSelectionParams):
            Optional. The desired voice of the
            synthesized audio.
    """

    speaking_rate = proto.Field(proto.DOUBLE, number=1,)
    pitch = proto.Field(proto.DOUBLE, number=2,)
    volume_gain_db = proto.Field(proto.DOUBLE, number=3,)
    effects_profile_id = proto.RepeatedField(proto.STRING, number=5,)
    voice = proto.Field(proto.MESSAGE, number=4, message="VoiceSelectionParams",)


class OutputAudioConfig(proto.Message):
    r"""Instructs the speech synthesizer how to generate the output
    audio content. If this audio config is supplied in a request, it
    overrides all existing text-to-speech settings applied to the
    agent.

    Attributes:
        audio_encoding (google.cloud.dialogflow_v2beta1.types.OutputAudioEncoding):
            Required. Audio encoding of the synthesized
            audio content.
        sample_rate_hertz (int):
            The synthesis sample rate (in hertz) for this
            audio. If not provided, then the synthesizer
            will use the default sample rate based on the
            audio encoding. If this is different from the
            voice's natural sample rate, then the
            synthesizer will honor this request by
            converting to the desired sample rate (which
            might result in worse audio quality).
        synthesize_speech_config (google.cloud.dialogflow_v2beta1.types.SynthesizeSpeechConfig):
            Configuration of how speech should be
            synthesized.
    """

    audio_encoding = proto.Field(proto.ENUM, number=1, enum="OutputAudioEncoding",)
    sample_rate_hertz = proto.Field(proto.INT32, number=2,)
    synthesize_speech_config = proto.Field(
        proto.MESSAGE, number=3, message="SynthesizeSpeechConfig",
    )


class TelephonyDtmfEvents(proto.Message):
    r"""A wrapper of repeated TelephonyDtmf digits.
    Attributes:
        dtmf_events (Sequence[google.cloud.dialogflow_v2beta1.types.TelephonyDtmf]):
            A sequence of TelephonyDtmf digits.
    """

    dtmf_events = proto.RepeatedField(proto.ENUM, number=1, enum="TelephonyDtmf",)


class SpeechToTextConfig(proto.Message):
    r"""Configures speech transcription for
    [ConversationProfile][google.cloud.dialogflow.v2beta1.ConversationProfile].

    Attributes:
        speech_model_variant (google.cloud.dialogflow_v2beta1.types.SpeechModelVariant):
            Optional. The speech model used in speech to text.
            ``SPEECH_MODEL_VARIANT_UNSPECIFIED``, ``USE_BEST_AVAILABLE``
            will be treated as ``USE_ENHANCED``. It can be overridden in
            [AnalyzeContentRequest][google.cloud.dialogflow.v2beta1.AnalyzeContentRequest]
            and
            [StreamingAnalyzeContentRequest][google.cloud.dialogflow.v2beta1.StreamingAnalyzeContentRequest]
            request.
    """

    speech_model_variant = proto.Field(proto.ENUM, number=1, enum="SpeechModelVariant",)


__all__ = tuple(sorted(__protobuf__.manifest))
