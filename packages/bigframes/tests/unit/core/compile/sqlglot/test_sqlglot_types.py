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

import pandas as pd
import pyarrow as pa

import bigframes.core.compile.sqlglot.sqlglot_types as sgt
import bigframes.dtypes as dtypes


def test_from_bigframes_simple_dtypes():
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.INT_DTYPE) == "INT64"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.FLOAT_DTYPE) == "FLOAT64"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.STRING_DTYPE) == "STRING"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.BOOL_DTYPE) == "BOOLEAN"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.DATE_DTYPE) == "DATE"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.TIME_DTYPE) == "TIME"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.DATETIME_DTYPE) == "DATETIME"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.TIMESTAMP_DTYPE) == "TIMESTAMP"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.BYTES_DTYPE) == "BYTES"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.NUMERIC_DTYPE) == "NUMERIC"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.BIGNUMERIC_DTYPE) == "BIGNUMERIC"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.JSON_DTYPE) == "JSON"
    assert sgt.SQLGlotType.from_bigframes_dtype(dtypes.GEO_DTYPE) == "GEOGRAPHY"


def test_from_bigframes_struct_dtypes():
    fields = [pa.field("int_col", pa.int64()), pa.field("bool_col", pa.bool_())]
    struct_type = pd.ArrowDtype(pa.struct(fields))
    expected = "STRUCT<int_col INT64, bool_col BOOLEAN>"
    assert sgt.SQLGlotType.from_bigframes_dtype(struct_type) == expected


def test_from_bigframes_array_dtypes():
    int_array_type = pd.ArrowDtype(pa.list_(pa.int64()))
    assert sgt.SQLGlotType.from_bigframes_dtype(int_array_type) == "ARRAY<INT64>"

    string_array_type = pd.ArrowDtype(pa.list_(pa.string()))
    assert sgt.SQLGlotType.from_bigframes_dtype(string_array_type) == "ARRAY<STRING>"


def test_from_bigframes_multi_nested_dtypes():
    fields = [
        pa.field("string_col", pa.string()),
        pa.field("date_col", pa.date32()),
        pa.field("array_col", pa.list_(pa.timestamp("us"))),
    ]
    array_type = pd.ArrowDtype(pa.list_(pa.struct(fields)))

    expected = (
        "ARRAY<STRUCT<string_col STRING, date_col DATE, array_col ARRAY<DATETIME>>>"
    )
    assert sgt.SQLGlotType.from_bigframes_dtype(array_type) == expected
