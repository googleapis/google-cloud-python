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


class DataFormat(enum.IntEnum):
    """
    Data format for input or output data.

    Attributes:
      DATA_FORMAT_UNSPECIFIED (int)
      AVRO (int): Avro is a standard open source row based file format.
      See https://avro.apache.org/ for more details.
      ARROW (int): Arrow is a standard open source column-based message format.
      See https://arrow.apache.org/ for more details.
    """

    DATA_FORMAT_UNSPECIFIED = 0
    AVRO = 1
    ARROW = 2


class ArrowSerializationOptions(object):
    class Format(enum.IntEnum):
        """
        The IPC format to use when serializing Arrow streams.

        Attributes:
          FORMAT_UNSPECIFIED (int): If unspecied the IPC format as of 0.15 release will be used.
          ARROW_0_14 (int): Use the legacy IPC message format as of Apache Arrow Release 0.14.
          ARROW_0_15 (int): Use the message format as of Apache Arrow Release 0.15.
        """

        FORMAT_UNSPECIFIED = 0
        ARROW_0_14 = 1
        ARROW_0_15 = 2
