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
