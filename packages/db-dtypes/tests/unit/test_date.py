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
import operator

import pandas
import pandas.testing
import pytest

import db_dtypes
from db_dtypes import pandas_backports


def test_construct_from_string_with_nonstring():
    with pytest.raises(TypeError):
        db_dtypes.DateDtype.construct_from_string(object())


def test__cmp_method_with_scalar():
    input_array = db_dtypes.DateArray([datetime.date(1900, 1, 1)])
    got = input_array._cmp_method(datetime.date(1900, 1, 1), operator.eq)
    assert got[0]


@pytest.mark.parametrize(
    "value, expected",
    [
        # Min/Max values for pandas.Timestamp.
        ("1677-09-22", datetime.date(1677, 9, 22)),
        ("2262-04-11", datetime.date(2262, 4, 11)),
        # Typical "zero" values.
        ("1900-01-01", datetime.date(1900, 1, 1)),
        ("1970-01-01", datetime.date(1970, 1, 1)),
        # Assorted values.
        ("1993-10-31", datetime.date(1993, 10, 31)),
        ("2012-02-29", datetime.date(2012, 2, 29)),
        ("2021-12-17", datetime.date(2021, 12, 17)),
        ("2038-01-19", datetime.date(2038, 1, 19)),
    ],
)
def test_date_parsing(value, expected):
    assert pandas.Series([value], dtype="dbdate")[0] == expected


@pytest.mark.parametrize(
    "value, error",
    [
        ("thursday", "Bad date string: 'thursday'"),
        ("1-2-thursday", "Bad date string: '1-2-thursday'"),
        ("1-2-3-4", "Bad date string: '1-2-3-4'"),
        ("1-2-3.f", "Bad date string: '1-2-3.f'"),
        ("1-d-3", "Bad date string: '1-d-3'"),
        ("1-3", "Bad date string: '1-3'"),
        ("1", "Bad date string: '1'"),
        ("", "Bad date string: ''"),
        ("2021-2-99", "day is out of range for month"),
        ("2021-99-1", "month must be in 1[.][.]12"),
        ("10000-1-1", "year 10000 is out of range"),
        # Outside of min/max values pandas.Timestamp.
        ("0001-01-01", "Out of bounds"),
        ("9999-12-31", "Out of bounds"),
        ("1677-09-21", "Out of bounds"),
        ("2262-04-12", "Out of bounds"),
    ],
)
def test_date_parsing_errors(value, error):
    with pytest.raises(ValueError, match=error):
        pandas.Series([value], dtype="dbdate")


@pytest.mark.skipif(
    not hasattr(pandas_backports, "numpy_validate_median"),
    reason="median not available with this version of pandas",
)
@pytest.mark.parametrize(
    "values, expected",
    [
        (["1970-01-01", "1900-01-01", "2000-01-01"], datetime.date(1970, 1, 1)),
        (
            [
                None,
                "1900-01-01",
                pandas.NA if hasattr(pandas, "NA") else None,
                pandas.NaT,
                float("nan"),
            ],
            datetime.date(1900, 1, 1),
        ),
        (["2222-02-01", "2222-02-03"], datetime.date(2222, 2, 2)),
    ],
)
def test_date_median(values, expected):
    series = pandas.Series(values, dtype="dbdate")
    assert series.median() == expected
