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

import db_dtypes  # type: ignore
import pyarrow as pa  # type: ignore
import pytest
import shapely.geometry  # type: ignore

import bigframes.dtypes


@pytest.mark.parametrize(
    ["python_type", "expected_dtype"],
    [
        (bool, bigframes.dtypes.BOOL_DTYPE),
        (int, bigframes.dtypes.INT_DTYPE),
        (str, bigframes.dtypes.STRING_DTYPE),
        (shapely.geometry.Point, bigframes.dtypes.GEO_DTYPE),
        (shapely.geometry.Polygon, bigframes.dtypes.GEO_DTYPE),
        (shapely.geometry.base.BaseGeometry, bigframes.dtypes.GEO_DTYPE),
    ],
)
def test_bigframes_type_supports_python_types(python_type, expected_dtype):
    got_dtype = bigframes.dtypes.bigframes_type(python_type)
    assert got_dtype == expected_dtype


@pytest.mark.parametrize(
    ["scalar", "expected_dtype"],
    [
        (pa.scalar(1_000_000_000, type=pa.int64()), bigframes.dtypes.INT_DTYPE),
        (pa.scalar(True, type=pa.bool_()), bigframes.dtypes.BOOL_DTYPE),
        (pa.scalar("hello", type=pa.string()), bigframes.dtypes.STRING_DTYPE),
        # Support NULL scalars.
        (pa.scalar(None, type=pa.int64()), bigframes.dtypes.INT_DTYPE),
        (pa.scalar(None, type=pa.bool_()), bigframes.dtypes.BOOL_DTYPE),
        (pa.scalar(None, type=pa.string()), bigframes.dtypes.STRING_DTYPE),
    ],
)
def test_infer_literal_type_arrow_scalar(scalar, expected_dtype):
    assert bigframes.dtypes.infer_literal_type(scalar) == expected_dtype


@pytest.mark.parametrize(
    ["type_", "expected"],
    [
        (pa.int64(), False),
        (db_dtypes.JSONArrowType(), True),
        (pa.struct([("int", pa.int64()), ("str", pa.string())]), False),
        (pa.struct([("int", pa.int64()), ("json", db_dtypes.JSONArrowType())]), True),
        (pa.list_(pa.int64()), False),
        (pa.list_(db_dtypes.JSONArrowType()), True),
        (
            pa.list_(
                pa.struct([("int", pa.int64()), ("json", db_dtypes.JSONArrowType())])
            ),
            True,
        ),
    ],
)
def test_contains_db_dtypes_json_arrow_type(type_, expected):
    assert bigframes.dtypes.contains_db_dtypes_json_arrow_type(type_) == expected
