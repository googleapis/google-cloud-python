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

import pandas as pd
import pandas.testing
import pyarrow
import pytest

import bigframes.dtypes
import bigframes.functions.function_template as bff_template

HELLO_WORLD_BASE64_BYTES = b"SGVsbG8sIFdvcmxkIQ=="
HELLO_WORLD_BASE64_STR = "SGVsbG8sIFdvcmxkIQ=="


@pytest.mark.parametrize(
    ["type_", "json_value", "expected"],
    (
        pytest.param(
            # Type names should match those in BigQueryType.from_ibis in
            # third_party/bigframes_vendored/ibis/backends/bigquery/datatypes.py
            "BOOLEAN",
            True,
            True,
        ),
        pytest.param(
            "BYTES",
            HELLO_WORLD_BASE64_STR,
            b"Hello, World!",
        ),
        pytest.param(
            "FLOAT64",
            1.25,
            1.25,
        ),
        pytest.param(
            "INT64",
            123,
            123,
        ),
        pytest.param(
            "STRING",
            "Hello, World!",
            "Hello, World!",
        ),
    ),
)
def test_convert_from_bq_json(type_, json_value, expected):
    got = bff_template.convert_from_bq_json(type_, json_value)
    assert got == expected


@pytest.mark.parametrize(
    "type_",
    [
        # Type names should match those in BigQueryType.from_ibis in
        # third_party/bigframes_vendored/ibis/backends/bigquery/datatypes.py
        "BOOLEAN",
        "BYTES",
        "FLOAT64",
        "INT64",
        "STRING",
    ],
)
def test_convert_from_bq_json_none(type_):
    got = bff_template.convert_from_bq_json(type_, None)
    assert got is None


@pytest.mark.parametrize(
    ["type_", "value", "expected"],
    (
        pytest.param(
            # Type names should match those in BigQueryType.from_ibis in
            # third_party/bigframes_vendored/ibis/backends/bigquery/datatypes.py
            "BOOLEAN",
            True,
            True,
        ),
        pytest.param(
            "BYTES",
            b"Hello, World!",
            HELLO_WORLD_BASE64_STR,
        ),
        pytest.param(
            "FLOAT64",
            1.25,
            1.25,
        ),
        pytest.param(
            "INT64",
            123,
            123,
        ),
        pytest.param(
            "STRING",
            "Hello, World!",
            "Hello, World!",
        ),
    ),
)
def test_convert_to_bq_json(type_, value, expected):
    got = bff_template.convert_to_bq_json(type_, value)
    assert got == expected


@pytest.mark.parametrize(
    "type_",
    [
        # Type names should match those in BigQueryType.from_ibis in
        # third_party/bigframes_vendored/ibis/backends/bigquery/datatypes.py
        "BOOLEAN",
        "BYTES",
        "FLOAT64",
        "INT64",
        "STRING",
    ],
)
def test_convert_to_bq_json_none(type_):
    got = bff_template.convert_to_bq_json(type_, None)
    assert got is None


@pytest.mark.parametrize(
    ["row_json", "expected"],
    (
        pytest.param(
            json.dumps(
                {
                    "names": ["'my-index'", "'col1'", "'col2'", "'col3'"],
                    "types": ["string", "Int64", "Int64", "Int64"],
                    "values": ["my-index-value", "1", None, "-1"],
                    "indexlength": 1,
                    "dtype": "Int64",
                }
            ),
            pd.Series(
                [1, pd.NA, -1],
                dtype="Int64",
                index=["col1", "col2", "col3"],
                name="my-index-value",
            ),
            id="int64-string-index",
        ),
        pytest.param(
            json.dumps(
                {
                    "names": ["'col1'", "'col2'", "'col3'"],
                    "types": ["binary[pyarrow]", "binary[pyarrow]", "binary[pyarrow]"],
                    "values": [HELLO_WORLD_BASE64_STR, "dGVzdDI=", "dGVzdDM="],
                    "indexlength": 0,
                    "dtype": "binary[pyarrow]",
                }
            ),
            pd.Series(
                [b"Hello, World!", b"test2", b"test3"],
                dtype=pd.ArrowDtype(pyarrow.binary()),
                index=["col1", "col2", "col3"],
                name=(),
            ),
            id="binary-no-index",
        ),
    ),
)
def test_get_pd_series(row_json, expected):
    got = bff_template.get_pd_series(row_json)
    pandas.testing.assert_series_equal(got, expected)


def test_get_pd_series_converter_dtypes():
    """Ensures the string format of the dtype doesn't change from that expected by get_pd_series."""

    # Keep in sync with value_converters in get_pd_series.
    # NOTE: Any change here is a red flag that there has been a breaking change
    # that will affect deployed axis=1 remote functions.
    assert str(bigframes.dtypes.BOOL_DTYPE) == "boolean"
    assert str(bigframes.dtypes.BYTES_DTYPE) == "binary[pyarrow]"
    assert str(bigframes.dtypes.FLOAT_DTYPE) == "Float64"
    assert str(bigframes.dtypes.INT_DTYPE) == "Int64"
    assert str(bigframes.dtypes.STRING_DTYPE) == "string"
