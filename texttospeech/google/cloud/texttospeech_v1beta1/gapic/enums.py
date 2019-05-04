# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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


class AudioEncoding(enum.IntEnum):
    """
    Configuration to set up audio encoder. The encoding determines the output
    audio format that we'd like.

    Attributes:
      AUDIO_ENCODING_UNSPECIFIED (int): Not specified. Will return result ``google.rpc.Code.INVALID_ARGUMENT``.
      LINEAR16 (int): Uncompressed 16-bit signed little-endian samples (Linear PCM).
      Audio content returned as LINEAR16 also contains a WAV header.
      MP3 (int): MP3 audio.
      OGG_OPUS (int): Opus encoded audio wrapped in an ogg container. The result will be a
      file which can be played natively on Android, and in browsers (at least
      Chrome and Firefox). The quality of the encoding is considerably higher
      than MP3 while using approximately the same bitrate.
    """

    AUDIO_ENCODING_UNSPECIFIED = 0
    LINEAR16 = 1
    MP3 = 2
    OGG_OPUS = 3


class SsmlVoiceGender(enum.IntEnum):
    """
    Gender of the voice as described in `SSML voice
    element <https://www.w3.org/TR/speech-synthesis11/#edef_voice>`__.

    Attributes:
      SSML_VOICE_GENDER_UNSPECIFIED (int): An unspecified gender.
      In VoiceSelectionParams, this means that the client doesn't care which
      gender the selected voice will have. In the Voice field of
      ListVoicesResponse, this may mean that the voice doesn't fit any of the
      other categories in this enum, or that the gender of the voice isn't known.
      MALE (int): A male voice.
      FEMALE (int): A female voice.
      NEUTRAL (int): A gender-neutral voice.
    """

    SSML_VOICE_GENDER_UNSPECIFIED = 0
    MALE = 1
    FEMALE = 2
    NEUTRAL = 3
