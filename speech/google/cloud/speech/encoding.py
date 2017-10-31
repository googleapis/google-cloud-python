# Copyright 2016 Google LLC
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

"""Encodings used by the Google Cloud Speech API."""


class Encoding(object):
    """Audio encoding types.

    See
    https://cloud.google.com/speech/reference/rest/v1/RecognitionConfig#AudioEncoding
    """

    LINEAR16 = 'LINEAR16'
    """LINEAR16 encoding type."""

    FLAC = 'FLAC'
    """FLAC encoding type."""

    MULAW = 'MULAW'
    """MULAW encoding type."""

    AMR = 'AMR'
    """AMR encoding type."""

    AMR_WB = 'AMR_WB'
    """AMR_WB encoding type."""

    OGG_OPUS = 'OGG_OPUS'
    """OGG_OPUS encoding type."""

    SPEEX_WITH_HEADER_BYTE = 'SPEEX_WITH_HEADER_BYTE'
    """SPEEX_WITH_HEADER_BYTE encoding type."""
