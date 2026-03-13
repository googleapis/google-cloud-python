# Copyright 2025 Google LLC
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

import pyarrow as pa
import pytest

from bigframes.operations import output_schemas


@pytest.mark.parametrize(
    ("sql", "expected"),
    [
        ("INT64", pa.int64()),
        (" INT64  ", pa.int64()),
        ("int64", pa.int64()),
        ("FLOAT64", pa.float64()),
        ("STRING", pa.string()),
        ("BOOL", pa.bool_()),
        ("ARRAY<INT64>", pa.list_(pa.int64())),
        (
            "STRUCT<x INT64, y FLOAT64>",
            pa.struct((pa.field("x", pa.int64()), pa.field("y", pa.float64()))),
        ),
        (
            "STRUCT< x INT64,  y  FLOAT64>",
            pa.struct((pa.field("x", pa.int64()), pa.field("y", pa.float64()))),
        ),
        (
            "STRUCT<y INT64,  x  FLOAT64>",
            pa.struct((pa.field("x", pa.float64()), pa.field("y", pa.int64()))),
        ),
        (
            "ARRAY<STRUCT<y INT64, x INT64>>",
            pa.list_(pa.struct((pa.field("x", pa.int64()), pa.field("y", pa.int64())))),
        ),
        (
            "STRUCT<y STRUCT<b STRING, a BOOL>, x ARRAY<FLOAT64>>",
            pa.struct(
                (
                    pa.field("x", pa.list_(pa.float64())),
                    pa.field(
                        "y",
                        pa.struct(
                            (pa.field("a", pa.bool_()), pa.field("b", pa.string()))
                        ),
                    ),
                )
            ),
        ),
    ],
)
def test_parse_sql_to_pyarrow_dtype(sql, expected):
    assert output_schemas.parse_sql_type(sql) == expected


@pytest.mark.parametrize(
    "sql",
    [
        "a INT64",
        "ARRAY<>",
        "ARRAY<INT64",
        "ARRAY<x INT64>" "ARRAY<int64>" "STRUCT<>",
        "DATE",
        "STRUCT<INT64, FLOAT64>",
        "ARRAY<ARRAY<>>",
    ],
)
def test_parse_sql_to_pyarrow_dtype_invalid_input_raies_error(sql):
    with pytest.raises(ValueError):
        output_schemas.parse_sql_type(sql)


@pytest.mark.parametrize(
    ("sql", "expected"),
    [
        ("x INT64", (pa.field("x", pa.int64()),)),
        (
            "x INT64, y FLOAT64",
            (pa.field("x", pa.int64()), pa.field("y", pa.float64())),
        ),
        (
            "y FLOAT64, x INT64",
            (pa.field("x", pa.int64()), pa.field("y", pa.float64())),
        ),
    ],
)
def test_parse_sql_fields(sql, expected):
    assert output_schemas.parse_sql_fields(sql) == expected
