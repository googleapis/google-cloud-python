# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
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


class CompressionType(enum.IntEnum):
    """
    The ways in which threat entry sets can be compressed.

    Attributes:
      COMPRESSION_TYPE_UNSPECIFIED (int): Unknown.
      RAW (int): Raw, uncompressed data.
      RICE (int): Rice-Golomb encoded data.
    """

    COMPRESSION_TYPE_UNSPECIFIED = 0
    RAW = 1
    RICE = 2


class ThreatType(enum.IntEnum):
    """
    The type of threat. This maps dirrectly to the threat list a threat may
    belong to.

    Attributes:
      THREAT_TYPE_UNSPECIFIED (int): Unknown.
      MALWARE (int): Malware targeting any platform.
      SOCIAL_ENGINEERING (int): Social engineering targeting any platform.
      UNWANTED_SOFTWARE (int): Unwanted software targeting any platform.
    """

    THREAT_TYPE_UNSPECIFIED = 0
    MALWARE = 1
    SOCIAL_ENGINEERING = 2
    UNWANTED_SOFTWARE = 3


class ComputeThreatListDiffResponse(object):
    class ResponseType(enum.IntEnum):
        """
        The type of response sent to the client.

        Attributes:
          RESPONSE_TYPE_UNSPECIFIED (int): Unknown.
          DIFF (int): Partial updates are applied to the client's existing local database.
          RESET (int): Full updates resets the client's entire local database. This means
          that either the client had no state, was seriously out-of-date,
          or the client is believed to be corrupt.
        """

        RESPONSE_TYPE_UNSPECIFIED = 0
        DIFF = 1
        RESET = 2
