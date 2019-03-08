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


class ErrorGroupOrder(enum.IntEnum):
    """
    A sorting order of error groups.

    Attributes:
      GROUP_ORDER_UNSPECIFIED (int): No group order specified.
      COUNT_DESC (int): Total count of errors in the given time window in descending order.
      LAST_SEEN_DESC (int): Timestamp when the group was last seen in the given time window
      in descending order.
      CREATED_DESC (int): Timestamp when the group was created in descending order.
      AFFECTED_USERS_DESC (int): Number of affected users in the given time window in descending order.
    """

    GROUP_ORDER_UNSPECIFIED = 0
    COUNT_DESC = 1
    LAST_SEEN_DESC = 2
    CREATED_DESC = 3
    AFFECTED_USERS_DESC = 4


class TimedCountAlignment(enum.IntEnum):
    """
    Specifies how the time periods of error group counts are aligned.

    Attributes:
      ERROR_COUNT_ALIGNMENT_UNSPECIFIED (int): No alignment specified.
      ALIGNMENT_EQUAL_ROUNDED (int): The time periods shall be consecutive, have width equal to the requested
      duration, and be aligned at the ``alignment_time`` provided in the
      request. The ``alignment_time`` does not have to be inside the query
      period but even if it is outside, only time periods are returned which
      overlap with the query period. A rounded alignment will typically result
      in a different size of the first or the last time period.
      ALIGNMENT_EQUAL_AT_END (int): The time periods shall be consecutive, have width equal to the
      requested duration, and be aligned at the end of the requested time
      period. This can result in a different size of the
      first time period.
    """

    ERROR_COUNT_ALIGNMENT_UNSPECIFIED = 0
    ALIGNMENT_EQUAL_ROUNDED = 1
    ALIGNMENT_EQUAL_AT_END = 2


class QueryTimeRange(object):
    class Period(enum.IntEnum):
        """
        The supported time ranges.

        Attributes:
          PERIOD_UNSPECIFIED (int): Do not use.
          PERIOD_1_HOUR (int): Retrieve data for the last hour.
          Recommended minimum timed count duration: 1 min.
          PERIOD_6_HOURS (int): Retrieve data for the last 6 hours.
          Recommended minimum timed count duration: 10 min.
          PERIOD_1_DAY (int): Retrieve data for the last day.
          Recommended minimum timed count duration: 1 hour.
          PERIOD_1_WEEK (int): Retrieve data for the last week.
          Recommended minimum timed count duration: 6 hours.
          PERIOD_30_DAYS (int): Retrieve data for the last 30 days.
          Recommended minimum timed count duration: 1 day.
        """

        PERIOD_UNSPECIFIED = 0
        PERIOD_1_HOUR = 1
        PERIOD_6_HOURS = 2
        PERIOD_1_DAY = 3
        PERIOD_1_WEEK = 4
        PERIOD_30_DAYS = 5
