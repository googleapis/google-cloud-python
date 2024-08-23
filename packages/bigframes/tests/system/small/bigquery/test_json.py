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

import json

import geopandas as gpd  # type: ignore
import pandas as pd
import pytest

import bigframes.bigquery as bbq
import bigframes.pandas as bpd


def _get_series_from_json(json_data):
    # Note: converts None to sql "null" and not to json none.
    values = [
        f"JSON '{json.dumps(data)}'" if data is not None else "NULL"
        for data in json_data
    ]
    sql = " UNION ALL ".join(
        [f"SELECT {id} AS id, {value} AS data" for id, value in enumerate(values)]
    )
    df = bpd.read_gbq(sql).set_index("id").sort_index()
    return df["data"]


@pytest.mark.parametrize(
    ("json_path", "expected_json"),
    [
        pytest.param("$.a", [{"a": 10}], id="simple"),
        pytest.param("$.a.b.c", [{"a": {"b": {"c": 10, "d": []}}}], id="nested"),
    ],
)
def test_json_set_at_json_path(json_path, expected_json):
    s = _get_series_from_json([{"a": {"b": {"c": "tester", "d": []}}}])
    actual = bbq.json_set(s, json_path_value_pairs=[(json_path, 10)])

    expected = _get_series_from_json(expected_json)
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
    )


@pytest.mark.parametrize(
    ("json_value", "expected_json"),
    [
        pytest.param(10, [{"a": {"b": 10}}, {"a": {"b": 10}}], id="int"),
        pytest.param(0.333, [{"a": {"b": 0.333}}, {"a": {"b": 0.333}}], id="float"),
        pytest.param("eng", [{"a": {"b": "eng"}}, {"a": {"b": "eng"}}], id="string"),
        pytest.param([1, 2], [{"a": {"b": 1}}, {"a": {"b": 2}}], id="series"),
    ],
)
def test_json_set_at_json_value_type(json_value, expected_json):
    s = _get_series_from_json([{"a": {"b": "dev"}}, {"a": {"b": [1, 2]}}])
    actual = bbq.json_set(s, json_path_value_pairs=[("$.a.b", json_value)])

    expected = _get_series_from_json(expected_json)
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
    )


def test_json_set_w_more_pairs():
    s = _get_series_from_json([{"a": 2}, {"b": 5}, {"c": 1}])
    actual = bbq.json_set(
        s, json_path_value_pairs=[("$.a", 1), ("$.b", 2), ("$.a", [3, 4, 5])]
    )
    expected = _get_series_from_json(
        [{"a": 3, "b": 2}, {"a": 4, "b": 2}, {"a": 5, "b": 2, "c": 1}]
    )
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
    )


def test_json_set_w_invalid_json_path_value_pairs():
    with pytest.raises(ValueError):
        bbq.json_set(
            _get_series_from_json([{"a": 10}]), json_path_value_pairs=[("$.a", 1, 100)]  # type: ignore
        )


def test_json_set_w_invalid_value_type():
    with pytest.raises(TypeError):
        bbq.json_set(
            _get_series_from_json([{"a": 10}]),
            json_path_value_pairs=[
                (
                    "$.a",
                    bpd.read_pandas(
                        gpd.GeoSeries.from_wkt(["POINT (1 2)", "POINT (2 1)"])
                    ),
                )
            ],
        )


def test_json_set_w_invalid_series_type():
    with pytest.raises(TypeError):
        bbq.json_set(bpd.Series([1, 2]), json_path_value_pairs=[("$.a", 1)])


def test_json_extract_from_json():
    s = _get_series_from_json([{"a": {"b": [1, 2]}}, {"a": {"c": 1}}, {"a": {"b": 0}}])
    actual = bbq.json_extract(s, "$.a.b").to_pandas()
    # After the introduction of the JSON type, the output should be a JSON-formatted series.
    expected = _get_series_from_json([[1, 2], None, 0]).to_pandas()
    pd.testing.assert_series_equal(
        actual,
        expected,
    )


def test_json_extract_from_string():
    s = bpd.Series(['{"a": {"b": [1, 2]}}', '{"a": {"c": 1}}', '{"a": {"b": 0}}'])
    actual = bbq.json_extract(s, "$.a.b")
    expected = _get_series_from_json([[1, 2], None, 0])
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
        check_names=False,
    )


def test_json_extract_w_invalid_series_type():
    with pytest.raises(TypeError):
        bbq.json_extract(bpd.Series([1, 2]), "$.a")


def test_json_extract_array_from_json_strings():
    s = bpd.Series(['{"a": [1, 2, 3]}', '{"a": []}', '{"a": [4,5]}'])
    actual = bbq.json_extract_array(s, "$.a")
    expected = bpd.Series([["1", "2", "3"], [], ["4", "5"]])
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
    )


def test_json_extract_array_from_array_strings():
    s = bpd.Series(["[1, 2, 3]", "[]", "[4,5]"])
    actual = bbq.json_extract_array(s)
    expected = bpd.Series([["1", "2", "3"], [], ["4", "5"]])
    pd.testing.assert_series_equal(
        actual.to_pandas(),
        expected.to_pandas(),
    )


def test_json_extract_array_w_invalid_series_type():
    with pytest.raises(TypeError):
        bbq.json_extract_array(bpd.Series([1, 2]))
