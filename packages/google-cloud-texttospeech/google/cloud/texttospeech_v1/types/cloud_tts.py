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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.texttospeech.v1",
    manifest={
        "SsmlVoiceGender",
        "AudioEncoding",
        "ListVoicesRequest",
        "ListVoicesResponse",
        "Voice",
        "AdvancedVoiceOptions",
        "SynthesizeSpeechRequest",
        "CustomPronunciationParams",
        "CustomPronunciations",
        "SynthesisInput",
        "VoiceSelectionParams",
        "AudioConfig",
        "CustomVoiceParams",
        "SynthesizeSpeechResponse",
        "StreamingSynthesizeConfig",
        "StreamingSynthesisInput",
        "StreamingSynthesizeRequest",
        "StreamingSynthesizeResponse",
    },
)


class SsmlVoiceGender(proto.Enum):
    r"""Gender of the voice as described in `SSML voice
    element <https://www.w3.org/TR/speech-synthesis11/#edef_voice>`__.

    Values:
        SSML_VOICE_GENDER_UNSPECIFIED (0):
            An unspecified gender.
            In VoiceSelectionParams, this means that the
            client doesn't care which gender the selected
            voice will have. In the Voice field of
            ListVoicesResponse, this may mean that the voice
            doesn't fit any of the other categories in this
            enum, or that the gender of the voice isn't
            known.
        MALE (1):
            A male voice.
        FEMALE (2):
            A female voice.
        NEUTRAL (3):
            A gender-neutral voice. This voice is not yet
            supported.
    """
    SSML_VOICE_GENDER_UNSPECIFIED = 0
    MALE = 1
    FEMALE = 2
    NEUTRAL = 3


class AudioEncoding(proto.Enum):
    r"""Configuration to set up audio encoder. The encoding
    determines the output audio format that we'd like.

    Values:
        AUDIO_ENCODING_UNSPECIFIED (0):
            Not specified. Will return result
            [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
        LINEAR16 (1):
            Uncompressed 16-bit signed little-endian
            samples (Linear PCM). Audio content returned as
            LINEAR16 also contains a WAV header.
        MP3 (2):
            MP3 audio at 32kbps.
        OGG_OPUS (3):
            Opus encoded audio wrapped in an ogg
            container. The result will be a file which can
            be played natively on Android, and in browsers
            (at least Chrome and Firefox). The quality of
            the encoding is considerably higher than MP3
            while using approximately the same bitrate.
        MULAW (5):
            8-bit samples that compand 14-bit audio
            samples using G.711 PCMU/mu-law. Audio content
            returned as MULAW also contains a WAV header.
        ALAW (6):
            8-bit samples that compand 14-bit audio
            samples using G.711 PCMU/A-law. Audio content
            returned as ALAW also contains a WAV header.
    """
    AUDIO_ENCODING_UNSPECIFIED = 0
    LINEAR16 = 1
    MP3 = 2
    OGG_OPUS = 3
    MULAW = 5
    ALAW = 6


class ListVoicesRequest(proto.Message):
    r"""The top-level message sent by the client for the ``ListVoices``
    method.

    Attributes:
        language_code (str):
            Optional. Recommended.
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tag. If not specified, the API will return all
            supported voices. If specified, the ListVoices call will
            only return voices that can be used to synthesize this
            language_code. For example, if you specify ``"en-NZ"``, all
            ``"en-NZ"`` voices will be returned. If you specify
            ``"no"``, both ``"no-\*"`` (Norwegian) and ``"nb-\*"``
            (Norwegian Bokmal) voices will be returned.
    """

    language_code: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListVoicesResponse(proto.Message):
    r"""The message returned to the client by the ``ListVoices`` method.

    Attributes:
        voices (MutableSequence[google.cloud.texttospeech_v1.types.Voice]):
            The list of voices.
    """

    voices: MutableSequence["Voice"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Voice",
    )


class Voice(proto.Message):
    r"""Description of a voice supported by the TTS service.

    Attributes:
        language_codes (MutableSequence[str]):
            The languages that this voice supports, expressed as
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tags (e.g. "en-US", "es-419", "cmn-tw").
        name (str):
            The name of this voice.  Each distinct voice
            has a unique name.
        ssml_gender (google.cloud.texttospeech_v1.types.SsmlVoiceGender):
            The gender of this voice.
        natural_sample_rate_hertz (int):
            The natural sample rate (in hertz) for this
            voice.
    """

    language_codes: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    ssml_gender: "SsmlVoiceGender" = proto.Field(
        proto.ENUM,
        number=3,
        enum="SsmlVoiceGender",
    )
    natural_sample_rate_hertz: int = proto.Field(
        proto.INT32,
        number=4,
    )


class AdvancedVoiceOptions(proto.Message):
    r"""Used for advanced voice options.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        low_latency_journey_synthesis (bool):
            Only for Journey voices. If false, the
            synthesis will be context aware and have higher
            latency.

            This field is a member of `oneof`_ ``_low_latency_journey_synthesis``.
    """

    low_latency_journey_synthesis: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )


class SynthesizeSpeechRequest(proto.Message):
    r"""The top-level message sent by the client for the
    ``SynthesizeSpeech`` method.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        input (google.cloud.texttospeech_v1.types.SynthesisInput):
            Required. The Synthesizer requires either
            plain text or SSML as input.
        voice (google.cloud.texttospeech_v1.types.VoiceSelectionParams):
            Required. The desired voice of the
            synthesized audio.
        audio_config (google.cloud.texttospeech_v1.types.AudioConfig):
            Required. The configuration of the
            synthesized audio.
        advanced_voice_options (google.cloud.texttospeech_v1.types.AdvancedVoiceOptions):
            Advanced voice options.

            This field is a member of `oneof`_ ``_advanced_voice_options``.
    """

    input: "SynthesisInput" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="SynthesisInput",
    )
    voice: "VoiceSelectionParams" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="VoiceSelectionParams",
    )
    audio_config: "AudioConfig" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AudioConfig",
    )
    advanced_voice_options: "AdvancedVoiceOptions" = proto.Field(
        proto.MESSAGE,
        number=8,
        optional=True,
        message="AdvancedVoiceOptions",
    )


class CustomPronunciationParams(proto.Message):
    r"""Pronunciation customization for a phrase.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        phrase (str):
            The phrase to which the customization will be
            applied. The phrase can be multiple words (in
            the case of proper nouns etc), but should not
            span to a whole sentence.

            This field is a member of `oneof`_ ``_phrase``.
        phonetic_encoding (google.cloud.texttospeech_v1.types.CustomPronunciationParams.PhoneticEncoding):
            The phonetic encoding of the phrase.

            This field is a member of `oneof`_ ``_phonetic_encoding``.
        pronunciation (str):
            The pronunciation of the phrase. This must be
            in the phonetic encoding specified above.

            This field is a member of `oneof`_ ``_pronunciation``.
    """

    class PhoneticEncoding(proto.Enum):
        r"""The phonetic encoding of the phrase.

        Values:
            PHONETIC_ENCODING_UNSPECIFIED (0):
                Not specified.
            PHONETIC_ENCODING_IPA (1):
                IPA. (e.g. apple -> ˈæpəl )
                https://en.wikipedia.org/wiki/International_Phonetic_Alphabet
            PHONETIC_ENCODING_X_SAMPA (2):
                X-SAMPA (e.g. apple -> "{p@l" )
                https://en.wikipedia.org/wiki/X-SAMPA
        """
        PHONETIC_ENCODING_UNSPECIFIED = 0
        PHONETIC_ENCODING_IPA = 1
        PHONETIC_ENCODING_X_SAMPA = 2

    phrase: str = proto.Field(
        proto.STRING,
        number=1,
        optional=True,
    )
    phonetic_encoding: PhoneticEncoding = proto.Field(
        proto.ENUM,
        number=2,
        optional=True,
        enum=PhoneticEncoding,
    )
    pronunciation: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )


class CustomPronunciations(proto.Message):
    r"""A collection of pronunciation customizations.

    Attributes:
        pronunciations (MutableSequence[google.cloud.texttospeech_v1.types.CustomPronunciationParams]):
            The pronunciation customizations to be
            applied.
    """

    pronunciations: MutableSequence["CustomPronunciationParams"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CustomPronunciationParams",
    )


class SynthesisInput(proto.Message):
    r"""Contains text input to be synthesized. Either ``text`` or ``ssml``
    must be supplied. Supplying both or neither returns
    [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
    The input size is limited to 5000 bytes.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            The raw text to be synthesized.

            This field is a member of `oneof`_ ``input_source``.
        ssml (str):
            The SSML document to be synthesized. The SSML document must
            be valid and well-formed. Otherwise the RPC will fail and
            return
            [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
            For more information, see
            `SSML <https://cloud.google.com/text-to-speech/docs/ssml>`__.

            This field is a member of `oneof`_ ``input_source``.
        custom_pronunciations (google.cloud.texttospeech_v1.types.CustomPronunciations):
            Optional. The pronunciation customizations to
            be applied to the input. If this is set, the
            input will be synthesized using the given
            pronunciation customizations.

            The initial support will be for EFIGS (English,
            French, Italian, German, Spanish) languages, as
            provided in VoiceSelectionParams. Journey and
            Instant Clone voices are not supported yet.

            In order to customize the pronunciation of a
            phrase, there must be an exact match of the
            phrase in the input types. If using SSML, the
            phrase must not be inside a phoneme tag
            (entirely or partially).
    """

    text: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="input_source",
    )
    ssml: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="input_source",
    )
    custom_pronunciations: "CustomPronunciations" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="CustomPronunciations",
    )


class VoiceSelectionParams(proto.Message):
    r"""Description of which voice to use for a synthesis request.

    Attributes:
        language_code (str):
            Required. The language (and potentially also the region) of
            the voice expressed as a
            `BCP-47 <https://www.rfc-editor.org/rfc/bcp/bcp47.txt>`__
            language tag, e.g. "en-US". This should not include a script
            tag (e.g. use "cmn-cn" rather than "cmn-Hant-cn"), because
            the script will be inferred from the input provided in the
            SynthesisInput. The TTS service will use this parameter to
            help choose an appropriate voice. Note that the TTS service
            may choose a voice with a slightly different language code
            than the one selected; it may substitute a different region
            (e.g. using en-US rather than en-CA if there isn't a
            Canadian voice available), or even a different language,
            e.g. using "nb" (Norwegian Bokmal) instead of "no"
            (Norwegian)".
        name (str):
            The name of the voice. If both the name and the gender are
            not set, the service will choose a voice based on the other
            parameters such as language_code.
        ssml_gender (google.cloud.texttospeech_v1.types.SsmlVoiceGender):
            The preferred gender of the voice. If not set, the service
            will choose a voice based on the other parameters such as
            language_code and name. Note that this is only a preference,
            not requirement; if a voice of the appropriate gender is not
            available, the synthesizer should substitute a voice with a
            different gender rather than failing the request.
        custom_voice (google.cloud.texttospeech_v1.types.CustomVoiceParams):
            The configuration for a custom voice. If
            [CustomVoiceParams.model] is set, the service will choose
            the custom voice matching the specified configuration.
    """

    language_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    name: str = proto.Field(
        proto.STRING,
        number=2,
    )
    ssml_gender: "SsmlVoiceGender" = proto.Field(
        proto.ENUM,
        number=3,
        enum="SsmlVoiceGender",
    )
    custom_voice: "CustomVoiceParams" = proto.Field(
        proto.MESSAGE,
        number=4,
        message="CustomVoiceParams",
    )


class AudioConfig(proto.Message):
    r"""Description of audio data to be synthesized.

    Attributes:
        audio_encoding (google.cloud.texttospeech_v1.types.AudioEncoding):
            Required. The format of the audio byte
            stream.
        speaking_rate (float):
            Optional. Input only. Speaking rate/speed, in the range
            [0.25, 4.0]. 1.0 is the normal native speed supported by the
            specific voice. 2.0 is twice as fast, and 0.5 is half as
            fast. If unset(0.0), defaults to the native 1.0 speed. Any
            other values < 0.25 or > 4.0 will return an error.
        pitch (float):
            Optional. Input only. Speaking pitch, in the range [-20.0,
            20.0]. 20 means increase 20 semitones from the original
            pitch. -20 means decrease 20 semitones from the original
            pitch.
        volume_gain_db (float):
            Optional. Input only. Volume gain (in dB) of the normal
            native volume supported by the specific voice, in the range
            [-96.0, 16.0]. If unset, or set to a value of 0.0 (dB), will
            play at normal native signal amplitude. A value of -6.0 (dB)
            will play at approximately half the amplitude of the normal
            native signal amplitude. A value of +6.0 (dB) will play at
            approximately twice the amplitude of the normal native
            signal amplitude. Strongly recommend not to exceed +10 (dB)
            as there's usually no effective increase in loudness for any
            value greater than that.
        sample_rate_hertz (int):
            Optional. The synthesis sample rate (in hertz) for this
            audio. When this is specified in SynthesizeSpeechRequest, if
            this is different from the voice's natural sample rate, then
            the synthesizer will honor this request by converting to the
            desired sample rate (which might result in worse audio
            quality), unless the specified sample rate is not supported
            for the encoding chosen, in which case it will fail the
            request and return
            [google.rpc.Code.INVALID_ARGUMENT][google.rpc.Code.INVALID_ARGUMENT].
        effects_profile_id (MutableSequence[str]):
            Optional. Input only. An identifier which selects 'audio
            effects' profiles that are applied on (post synthesized)
            text to speech. Effects are applied on top of each other in
            the order they are given. See `audio
            profiles <https://cloud.google.com/text-to-speech/docs/audio-profiles>`__
            for current supported profile ids.
    """

    audio_encoding: "AudioEncoding" = proto.Field(
        proto.ENUM,
        number=1,
        enum="AudioEncoding",
    )
    speaking_rate: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )
    pitch: float = proto.Field(
        proto.DOUBLE,
        number=3,
    )
    volume_gain_db: float = proto.Field(
        proto.DOUBLE,
        number=4,
    )
    sample_rate_hertz: int = proto.Field(
        proto.INT32,
        number=5,
    )
    effects_profile_id: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )


class CustomVoiceParams(proto.Message):
    r"""Description of the custom voice to be synthesized.

    Attributes:
        model (str):
            Required. The name of the AutoML model that
            synthesizes the custom voice.
        reported_usage (google.cloud.texttospeech_v1.types.CustomVoiceParams.ReportedUsage):
            Optional. Deprecated. The usage of the
            synthesized audio to be reported.
    """

    class ReportedUsage(proto.Enum):
        r"""Deprecated. The usage of the synthesized audio. Usage does
        not affect billing.

        Values:
            REPORTED_USAGE_UNSPECIFIED (0):
                Request with reported usage unspecified will
                be rejected.
            REALTIME (1):
                For scenarios where the synthesized audio is
                not downloadable and can only be used once. For
                example, real-time request in IVR system.
            OFFLINE (2):
                For scenarios where the synthesized audio is
                downloadable and can be reused. For example, the
                synthesized audio is downloaded, stored in
                customer service system and played repeatedly.
        """
        REPORTED_USAGE_UNSPECIFIED = 0
        REALTIME = 1
        OFFLINE = 2

    model: str = proto.Field(
        proto.STRING,
        number=1,
    )
    reported_usage: ReportedUsage = proto.Field(
        proto.ENUM,
        number=3,
        enum=ReportedUsage,
    )


class SynthesizeSpeechResponse(proto.Message):
    r"""The message returned to the client by the ``SynthesizeSpeech``
    method.

    Attributes:
        audio_content (bytes):
            The audio data bytes encoded as specified in the request,
            including the header for encodings that are wrapped in
            containers (e.g. MP3, OGG_OPUS). For LINEAR16 audio, we
            include the WAV header. Note: as with all bytes fields,
            protobuffers use a pure binary representation, whereas JSON
            representations use base64.
    """

    audio_content: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )


class StreamingSynthesizeConfig(proto.Message):
    r"""Provides configuration information for the
    StreamingSynthesize request.

    Attributes:
        voice (google.cloud.texttospeech_v1.types.VoiceSelectionParams):
            Required. The desired voice of the
            synthesized audio.
    """

    voice: "VoiceSelectionParams" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="VoiceSelectionParams",
    )


class StreamingSynthesisInput(proto.Message):
    r"""Input to be synthesized.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        text (str):
            The raw text to be synthesized. It is
            recommended that each input contains complete,
            terminating sentences, as this will likely
            result in better prosody in the output audio.
            That being said, users are free to input text
            however they please.

            This field is a member of `oneof`_ ``input_source``.
    """

    text: str = proto.Field(
        proto.STRING,
        number=1,
        oneof="input_source",
    )


class StreamingSynthesizeRequest(proto.Message):
    r"""Request message for the ``StreamingSynthesize`` method. Multiple
    ``StreamingSynthesizeRequest`` messages are sent in one call. The
    first message must contain a ``streaming_config`` that fully
    specifies the request configuration and must not contain ``input``.
    All subsequent messages must only have ``input`` set.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        streaming_config (google.cloud.texttospeech_v1.types.StreamingSynthesizeConfig):
            StreamingSynthesizeConfig to be used in this streaming
            attempt. Only specified in the first message sent in a
            ``StreamingSynthesize`` call.

            This field is a member of `oneof`_ ``streaming_request``.
        input (google.cloud.texttospeech_v1.types.StreamingSynthesisInput):
            Input to synthesize. Specified in all messages but the first
            in a ``StreamingSynthesize`` call.

            This field is a member of `oneof`_ ``streaming_request``.
    """

    streaming_config: "StreamingSynthesizeConfig" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="streaming_request",
        message="StreamingSynthesizeConfig",
    )
    input: "StreamingSynthesisInput" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="streaming_request",
        message="StreamingSynthesisInput",
    )


class StreamingSynthesizeResponse(proto.Message):
    r"""``StreamingSynthesizeResponse`` is the only message returned to the
    client by ``StreamingSynthesize`` method. A series of zero or more
    ``StreamingSynthesizeResponse`` messages are streamed back to the
    client.

    Attributes:
        audio_content (bytes):
            The audio data bytes encoded as specified in
            the request. This is headerless LINEAR16 audio
            with a sample rate of 24000.
    """

    audio_content: bytes = proto.Field(
        proto.BYTES,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
