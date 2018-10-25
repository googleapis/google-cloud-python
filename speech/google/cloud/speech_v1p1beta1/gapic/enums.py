# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Wrappers for protocol buffer enum types."""

import enum


class RecognitionConfig(object):
    class AudioEncoding(enum.IntEnum):
        """
        The encoding of the audio data sent in the request.

        All encodings support only 1 channel (mono) audio.

        For best results, the audio source should be captured and transmitted using
        a lossless encoding (``FLAC`` or ``LINEAR16``). The accuracy of the speech
        recognition can be reduced if lossy codecs are used to capture or transmit
        audio, particularly if background noise is present. Lossy codecs include
        ``MULAW``, ``AMR``, ``AMR_WB``, ``OGG_OPUS``, and ``SPEEX_WITH_HEADER_BYTE``.

        The ``FLAC`` and ``WAV`` audio file formats include a header that describes the
        included audio content. You can request recognition for ``WAV`` files that
        contain either ``LINEAR16`` or ``MULAW`` encoded audio.
        If you send ``FLAC`` or ``WAV`` audio file format in
        your request, you do not need to specify an ``AudioEncoding``; the audio
        encoding format is determined from the file header. If you specify
        an ``AudioEncoding`` when you send  send ``FLAC`` or ``WAV`` audio, the
        encoding configuration must match the encoding described in the audio
        header; otherwise the request returns an
        ``google.rpc.Code.INVALID_ARGUMENT`` error code.

        Attributes:
          ENCODING_UNSPECIFIED (int): Not specified.
          LINEAR16 (int): Uncompressed 16-bit signed little-endian samples (Linear PCM).
          FLAC (int): ``FLAC`` (Free Lossless Audio
          Codec) is the recommended encoding because it is
          lossless--therefore recognition is not compromised--and
          requires only about half the bandwidth of ``LINEAR16``. ``FLAC`` stream
          encoding supports 16-bit and 24-bit samples, however, not all fields in
          ``STREAMINFO`` are supported.
          MULAW (int): 8-bit samples that compand 14-bit audio samples using G.711 PCMU/mu-law.
          AMR (int): Adaptive Multi-Rate Narrowband codec. ``sample_rate_hertz`` must be 8000.
          AMR_WB (int): Adaptive Multi-Rate Wideband codec. ``sample_rate_hertz`` must be 16000.
          OGG_OPUS (int): Opus encoded audio frames in Ogg container
          (`OggOpus <https://wiki.xiph.org/OggOpus>`_).
          ``sample_rate_hertz`` must be one of 8000, 12000, 16000, 24000, or 48000.
          SPEEX_WITH_HEADER_BYTE (int): Although the use of lossy encodings is not recommended, if a very low
          bitrate encoding is required, ``OGG_OPUS`` is highly preferred over
          Speex encoding. The `Speex <https://speex.org/>`_  encoding supported by
          Cloud Speech API has a header byte in each block, as in MIME type
          ``audio/x-speex-with-header-byte``.
          It is a variant of the RTP Speex encoding defined in
          `RFC 5574 <https://tools.ietf.org/html/rfc5574>`_.
          The stream is a sequence of blocks, one block per RTP packet. Each block
          starts with a byte containing the length of the block, in bytes, followed
          by one or more frames of Speex data, padded to an integral number of
          bytes (octets) as specified in RFC 5574. In other words, each RTP header
          is replaced with a single byte containing the block length. Only Speex
          wideband is supported. ``sample_rate_hertz`` must be 16000.
        """
        ENCODING_UNSPECIFIED = 0
        LINEAR16 = 1
        FLAC = 2
        MULAW = 3
        AMR = 4
        AMR_WB = 5
        OGG_OPUS = 6
        SPEEX_WITH_HEADER_BYTE = 7


class RecognitionMetadata(object):
    class InteractionType(enum.IntEnum):
        """
        Use case categories that the audio recognition request can be described
        by.

        Attributes:
          INTERACTION_TYPE_UNSPECIFIED (int): Use case is either unknown or is something other than one of the other
          values below.
          DISCUSSION (int): Multiple people in a conversation or discussion. For example in a
          meeting with two or more people actively participating. Typically
          all the primary people speaking would be in the same room (if not,
          see PHONE_CALL)
          PRESENTATION (int): One or more persons lecturing or presenting to others, mostly
          uninterrupted.
          PHONE_CALL (int): A phone-call or video-conference in which two or more people, who are
          not in the same room, are actively participating.
          VOICEMAIL (int): A recorded message intended for another person to listen to.
          PROFESSIONALLY_PRODUCED (int): Professionally produced audio (eg. TV Show, Podcast).
          VOICE_SEARCH (int): Transcribe spoken questions and queries into text.
          VOICE_COMMAND (int): Transcribe voice commands, such as for controlling a device.
          DICTATION (int): Transcribe speech to text to create a written document, such as a
          text-message, email or report.
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

    class MicrophoneDistance(enum.IntEnum):
        """
        Enumerates the types of capture settings describing an audio file.

        Attributes:
          MICROPHONE_DISTANCE_UNSPECIFIED (int): Audio type is not known.
          NEARFIELD (int): The audio was captured from a closely placed microphone. Eg. phone,
          dictaphone, or handheld microphone. Generally if there speaker is within
          1 meter of the microphone.
          MIDFIELD (int): The speaker if within 3 meters of the microphone.
          FARFIELD (int): The speaker is more than 3 meters away from the microphone.
        """
        MICROPHONE_DISTANCE_UNSPECIFIED = 0
        NEARFIELD = 1
        MIDFIELD = 2
        FARFIELD = 3

    class OriginalMediaType(enum.IntEnum):
        """
        The original media the speech was recorded on.

        Attributes:
          ORIGINAL_MEDIA_TYPE_UNSPECIFIED (int): Unknown original media type.
          AUDIO (int): The speech data is an audio recording.
          VIDEO (int): The speech data originally recorded on a video.
        """
        ORIGINAL_MEDIA_TYPE_UNSPECIFIED = 0
        AUDIO = 1
        VIDEO = 2

    class RecordingDeviceType(enum.IntEnum):
        """
        The type of device the speech was recorded with.

        Attributes:
          RECORDING_DEVICE_TYPE_UNSPECIFIED (int): The recording device is unknown.
          SMARTPHONE (int): Speech was recorded on a smartphone.
          PC (int): Speech was recorded using a personal computer or tablet.
          PHONE_LINE (int): Speech was recorded over a phone line.
          VEHICLE (int): Speech was recorded in a vehicle.
          OTHER_OUTDOOR_DEVICE (int): Speech was recorded outdoors.
          OTHER_INDOOR_DEVICE (int): Speech was recorded indoors.
        """
        RECORDING_DEVICE_TYPE_UNSPECIFIED = 0
        SMARTPHONE = 1
        PC = 2
        PHONE_LINE = 3
        VEHICLE = 4
        OTHER_OUTDOOR_DEVICE = 5
        OTHER_INDOOR_DEVICE = 6


class StreamingRecognizeResponse(object):
    class SpeechEventType(enum.IntEnum):
        """
        Indicates the type of speech event.

        Attributes:
          SPEECH_EVENT_UNSPECIFIED (int): No speech event specified.
          END_OF_SINGLE_UTTERANCE (int): This event indicates that the server has detected the end of the user's
          speech utterance and expects no additional speech. Therefore, the server
          will not process additional audio (although it may subsequently return
          additional results). The client should stop sending additional audio
          data, half-close the gRPC connection, and wait for any additional results
          until the server closes the gRPC connection. This event is only sent if
          ``single_utterance`` was set to ``true``, and is not used otherwise.
        """
        SPEECH_EVENT_UNSPECIFIED = 0
        END_OF_SINGLE_UTTERANCE = 1
