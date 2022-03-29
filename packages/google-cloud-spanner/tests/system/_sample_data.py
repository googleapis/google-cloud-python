# Copyright 2021 Google LLC All rights reserved.
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

import datetime
import math

from google.api_core import datetime_helpers
from google.cloud._helpers import UTC
from google.cloud import spanner_v1


TABLE = "contacts"
COLUMNS = ("contact_id", "first_name", "last_name", "email")
ROW_DATA = (
    (1, "Phred", "Phlyntstone", "phred@example.com"),
    (2, "Bharney", "Rhubble", "bharney@example.com"),
    (3, "Wylma", "Phlyntstone", "wylma@example.com"),
)
ALL = spanner_v1.KeySet(all_=True)
SQL = "SELECT * FROM contacts ORDER BY contact_id"

COUNTERS_TABLE = "counters"
COUNTERS_COLUMNS = ("name", "value")


def _assert_timestamp(value, nano_value):
    assert isinstance(value, datetime.datetime)
    assert value.tzinfo is None
    assert nano_value.tzinfo is UTC

    assert value.year == nano_value.year
    assert value.month == nano_value.month
    assert value.day == nano_value.day
    assert value.hour == nano_value.hour
    assert value.minute == nano_value.minute
    assert value.second == nano_value.second
    assert value.microsecond == nano_value.microsecond

    if isinstance(value, datetime_helpers.DatetimeWithNanoseconds):
        assert value.nanosecond == nano_value.nanosecond
    else:
        assert value.microsecond * 1000 == nano_value.nanosecond


def _check_rows_data(rows_data, expected=ROW_DATA, recurse_into_lists=True):
    assert len(rows_data) == len(expected)

    for row, expected in zip(rows_data, expected):
        _check_row_data(row, expected, recurse_into_lists=recurse_into_lists)


def _check_row_data(row_data, expected, recurse_into_lists=True):
    assert len(row_data) == len(expected)

    for found_cell, expected_cell in zip(row_data, expected):
        _check_cell_data(
            found_cell, expected_cell, recurse_into_lists=recurse_into_lists
        )


def _check_cell_data(found_cell, expected_cell, recurse_into_lists=True):

    if isinstance(found_cell, datetime_helpers.DatetimeWithNanoseconds):
        _assert_timestamp(expected_cell, found_cell)

    elif isinstance(found_cell, float) and math.isnan(found_cell):
        assert math.isnan(expected_cell)

    elif isinstance(found_cell, list) and recurse_into_lists:
        assert len(found_cell) == len(expected_cell)

        for found_item, expected_item in zip(found_cell, expected_cell):
            _check_cell_data(found_item, expected_item)

    else:
        assert found_cell == expected_cell
