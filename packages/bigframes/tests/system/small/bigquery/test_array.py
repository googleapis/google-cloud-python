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

import numpy as np
import pandas as pd
import pytest

import bigframes.bigquery as bbq
import bigframes.dtypes
import bigframes.pandas as bpd


@pytest.mark.parametrize(
    ["input_data", "expected"],
    [
        pytest.param(
            [["A", "AA", "AAA"], ["BB", "B"], np.nan, [], ["C"]],
            [
                3,
                2,
                # TODO(b/336880368): Allow for NULL values to be input for ARRAY
                # columns.  Once we actually store NULL values, this will be
                # NULL where the input is NULL.
                0,
                0,
                1,
            ],
            id="small-string",
        ),
        pytest.param(
            [[1, 2, 3], [4, 5], [], [], [6]], [3, 2, 0, 0, 1], id="small-int64"
        ),
        pytest.param(
            [
                # Regression test for b/414374215 where the Series constructor
                # returns empty lists when the lists are too big to embed in
                # SQL.
                list(np.random.randint(-1_000_000, 1_000_000, size=1000)),
                list(np.random.randint(-1_000_000, 1_000_000, size=967)),
                list(np.random.randint(-1_000_000, 1_000_000, size=423)),
                list(np.random.randint(-1_000_000, 1_000_000, size=5000)),
                list(np.random.randint(-1_000_000, 1_000_000, size=1003)),
                list(np.random.randint(-1_000_000, 1_000_000, size=9999)),
            ],
            [
                1000,
                967,
                423,
                5000,
                1003,
                9999,
            ],
            id="larger-int64",
        ),
    ],
)
def test_array_length(input_data, expected):
    series = bpd.Series(input_data)
    expected = pd.Series(expected, dtype=bigframes.dtypes.INT_DTYPE)
    pd.testing.assert_series_equal(
        bbq.array_length(series).to_pandas(),
        expected,
        check_index_type=False,
    )


@pytest.mark.parametrize(
    ("input_data", "output_data"),
    [
        pytest.param([1, 2, 3, 4, 5], [[1, 2], [3, 4], [5]], id="ints"),
        pytest.param(
            ["e", "d", "c", "b", "a"],
            [["e", "d"], ["c", "b"], ["a"]],
            id="reverse_strings",
        ),
        pytest.param(
            [1.0, 2.0, np.nan, np.nan, np.nan], [[1.0, 2.0], [], []], id="nans"
        ),
        pytest.param(
            [{"A": {"x": 1.0}}, {"A": {"z": 4.0}}, {}, {"B": "b"}, np.nan],
            [[{"A": {"x": 1.0}}, {"A": {"z": 4.0}}], [{}, {"B": "b"}], []],
            id="structs",
        ),
    ],
)
def test_array_agg_w_series_groupby(input_data, output_data):
    input_index = ["a", "a", "b", "b", "c"]
    series = bpd.Series(input_data, index=input_index)
    result = bbq.array_agg(series.groupby(level=0))

    expected = bpd.Series(output_data, index=["a", "b", "c"])
    pd.testing.assert_series_equal(
        result.to_pandas(),  # type: ignore
        expected.to_pandas(),
    )


def test_array_agg_w_dataframe_groupby():
    data = {
        "a": [1, 1, 2, 1],
        "b": [2, None, 1, 2],
        "c": [3, 4, 3, 2],
    }
    df = bpd.DataFrame(data)
    result = bbq.array_agg(df.groupby(by=["b"]))

    expected_data = {
        "b": [1.0, 2.0],
        "a": [[2], [1, 1]],
        "c": [[3], [3, 2]],
    }
    expected = bpd.DataFrame(expected_data).set_index("b")

    pd.testing.assert_frame_equal(
        result.to_pandas(),  # type: ignore
        expected.to_pandas(),
    )


def test_array_agg_w_series():
    series = bpd.Series([1, 2, 3, 4, 5], index=["a", "a", "b", "b", "c"])
    # Mypy error expected: array_agg currently incompatible with Series.
    # Test for coverage.
    with pytest.raises(ValueError):
        bbq.array_agg(series)  # type: ignore


@pytest.mark.parametrize(
    ("ascending", "expected_b", "expected_c"),
    [
        pytest.param(
            True, [["a", "b"], ["e", "d", "c"]], [[4, 5], [1, 2, 3]], id="asc"
        ),
        pytest.param(
            False, [["b", "a"], ["c", "d", "e"]], [[5, 4], [3, 2, 1]], id="des"
        ),
    ],
)
def test_array_agg_reserve_order(ascending, expected_b, expected_c):
    data = {
        "a": [1, 1, 2, 2, 2],
        "b": ["a", "b", "c", "d", "e"],
        "c": [4, 5, 3, 2, 1],
    }
    df = bpd.DataFrame(data)

    result = bbq.array_agg(df.sort_values("c", ascending=ascending).groupby(by=["a"]))
    expected_data = {
        "a": [1, 2],
        "b": expected_b,
        "c": expected_c,
    }
    expected = bpd.DataFrame(expected_data).set_index("a")

    pd.testing.assert_frame_equal(
        result.to_pandas(),  # type: ignore
        expected.to_pandas(),
    )


def test_array_agg_matches_after_explode():
    data = {
        "index": np.arange(10),
        "a": [np.random.randint(0, 10, 10) for _ in range(10)],
        "b": [np.random.randint(0, 10, 10) for _ in range(10)],
    }
    df = bpd.DataFrame(data).set_index("index")
    result = bbq.array_agg(df.explode(["a", "b"]).groupby(level=0))
    result.index.name = "index"

    pd.testing.assert_frame_equal(
        result.to_pandas(),  # type: ignore
        df.to_pandas(),
    )


@pytest.mark.parametrize(
    ("data"),
    [
        pytest.param([[1, 2], [3, 4], [5]], id="int_array"),
        pytest.param(["hello", "world"], id="string"),
    ],
)
def test_array_to_string_w_type_checks(data):
    series = bpd.Series(data)
    with pytest.raises(TypeError):
        bbq.array_to_string(series, delimiter=", ")
