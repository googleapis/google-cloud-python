# Copyright 2021 Google LLC
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

import pandas
import pytest

# To register the types.
import db_dtypes  # noqa


@pytest.mark.parametrize(
    "value, expected",
    [
        # Midnight
        ("0", datetime.time(0)),
        ("0:0", datetime.time(0)),
        ("0:0:0", datetime.time(0)),
        ("0:0:0.", datetime.time(0)),
        ("0:0:0.0", datetime.time(0)),
        ("0:0:0.000000", datetime.time(0)),
        ("00:00:00", datetime.time(0, 0, 0)),
        ("  00:00:00  ", datetime.time(0, 0, 0)),
        # Short values
        ("1", datetime.time(1)),
        ("23", datetime.time(23)),
        ("1:2", datetime.time(1, 2)),
        ("23:59", datetime.time(23, 59)),
        ("1:2:3", datetime.time(1, 2, 3)),
        ("23:59:59", datetime.time(23, 59, 59)),
        # Non-octal values.
        ("08:08:08", datetime.time(8, 8, 8)),
        ("09:09:09", datetime.time(9, 9, 9)),
        # Fractional seconds can cause rounding problems if cast to float. See:
        # https://github.com/googleapis/python-db-dtypes-pandas/issues/18
        ("0:0:59.876543", datetime.time(0, 0, 59, 876543)),
        ("01:01:01.010101", datetime.time(1, 1, 1, 10101)),
        ("09:09:09.090909", datetime.time(9, 9, 9, 90909)),
        ("11:11:11.111111", datetime.time(11, 11, 11, 111111)),
        ("19:16:23.987654", datetime.time(19, 16, 23, 987654)),
        # Microsecond precision
        ("00:00:00.000001", datetime.time(0, 0, 0, 1)),
        ("23:59:59.999999", datetime.time(23, 59, 59, 999_999)),
        # TODO: Support nanosecond precision values without truncation.
        # https://github.com/googleapis/python-db-dtypes-pandas/issues/19
        ("0:0:0.000001001", datetime.time(0, 0, 0, 1)),
        ("23:59:59.999999000", datetime.time(23, 59, 59, 999_999)),
        ("23:59:59.999999999", datetime.time(23, 59, 59, 999_999)),
    ],
)
def test_time_parsing(value, expected):
    assert pandas.Series([value], dtype="dbtime")[0] == expected


@pytest.mark.parametrize(
    "value, error",
    [
        ("thursday", "Bad time string: 'thursday'"),
        ("1:2:3thursday", "Bad time string: '1:2:3thursday'"),
        ("1:2:3:4", "Bad time string: '1:2:3:4'"),
        ("1:2:3.f", "Bad time string: '1:2:3.f'"),
        ("1:d:3", "Bad time string: '1:d:3'"),
        ("1:2.3", "Bad time string: '1:2.3'"),
        ("", "Bad time string: ''"),
        ("1:2:99", "second must be in 0[.][.]59"),
        ("1:99", "minute must be in 0[.][.]59"),
        ("99", "hour must be in 0[.][.]23"),
    ],
)
def test_time_parsing_errors(value, error):
    with pytest.raises(ValueError, match=error):
        pandas.Series([value], dtype="dbtime")
