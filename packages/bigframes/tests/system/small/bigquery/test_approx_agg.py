# Copyright 2024 Google LLC
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

import pytest

import bigframes.bigquery as bbq
import bigframes.pandas as bpd


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param(
            [1, 2, 3, 3, 2], [{"value": 3, "count": 2}, {"value": 2, "count": 2}]
        ),
        pytest.param(
            ["apple", "apple", "pear", "pear", "pear", "banana"],
            [{"value": "pear", "count": 3}, {"value": "apple", "count": 2}],
        ),
        pytest.param(
            [True, False, True, False, True],
            [{"value": True, "count": 3}, {"value": False, "count": 2}],
        ),
        pytest.param(
            [],
            [],
        ),
        pytest.param(
            [[1, 2], [1], [1, 2]],
            [],
            marks=pytest.mark.xfail(raises=TypeError),
        ),
    ],
    ids=["int64", "string", "bool", "null", "array"],
)
def test_approx_top_count_w_dtypes(data, expected):
    s = bpd.Series(data)
    result = bbq.approx_top_count(s, number=2)
    assert result == expected


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        pytest.param(
            0,
            [],
            marks=pytest.mark.xfail(raises=ValueError),
        ),
        pytest.param(1, [{"value": 3, "count": 2}]),
        pytest.param(
            4,
            [
                {"value": 3, "count": 2},
                {"value": 2, "count": 2},
                {"value": 1, "count": 1},
            ],
        ),
    ],
    ids=["zero", "one", "full"],
)
def test_approx_top_count_w_numbers(number, expected):
    s = bpd.Series([1, 2, 3, 3, 2])
    result = bbq.approx_top_count(s, number=number)
    assert result == expected
