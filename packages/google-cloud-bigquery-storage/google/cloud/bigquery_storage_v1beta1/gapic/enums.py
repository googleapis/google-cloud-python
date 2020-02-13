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
      DATA_FORMAT_UNSPECIFIED (int): Data format is unspecified.
      AVRO (int): Avro is a standard open source row based file format.
      See https://avro.apache.org/ for more details.
      ARROW (int)
    """

    DATA_FORMAT_UNSPECIFIED = 0
    AVRO = 1
    ARROW = 3


class ShardingStrategy(enum.IntEnum):
    """
    Strategy for distributing data among multiple streams in a read session.

    Attributes:
      SHARDING_STRATEGY_UNSPECIFIED (int): Same as LIQUID.
      LIQUID (int): Assigns data to each stream based on the client's read rate. The faster the
      client reads from a stream, the more data is assigned to the stream. In
      this strategy, it's possible to read all data from a single stream even if
      there are other streams present.
      BALANCED (int): Assigns data to each stream such that roughly the same number of rows can
      be read from each stream. Because the server-side unit for assigning data
      is collections of rows, the API does not guarantee that each stream will
      return the same number or rows. Additionally, the limits are enforced based
      on the number of pre-filtering rows, so some filters can lead to lopsided
      assignments.
    """

    SHARDING_STRATEGY_UNSPECIFIED = 0
    LIQUID = 1
    BALANCED = 2
