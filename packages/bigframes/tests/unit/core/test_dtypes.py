# Copyright 2023 Google LLC
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

import bigframes_vendored.ibis.backends.bigquery.datatypes as ibis_bq_types
import bigframes_vendored.ibis.expr.datatypes as ibis_dtypes
import bigframes_vendored.ibis.expr.types as ibis_types
import geopandas as gpd  # type: ignore
import numpy as np
import pandas as pd
import pyarrow as pa  # type: ignore
import pytest
import shapely.geometry  # type: ignore

import bigframes.core.compile.ibis_types
import bigframes.dtypes


@pytest.mark.parametrize(
    ["ibis_dtype", "bigframes_dtype"],
    [
        # TODO(bmil): Add ARRAY, INTERVAL, STRUCT to cover all the standard
        # BigQuery data types as they appear in Ibis:
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types
        pytest.param(
            ibis_dtypes.Decimal(precision=76, scale=38, nullable=True),
            pd.ArrowDtype(pa.decimal256(76, 38)),
            id="bignumeric",
        ),
        pytest.param(ibis_dtypes.boolean, pd.BooleanDtype(), id="bool"),
        pytest.param(ibis_dtypes.binary, pd.ArrowDtype(pa.binary()), id="bytes"),
        pytest.param(ibis_dtypes.date, pd.ArrowDtype(pa.date32()), id="date"),
        pytest.param(
            ibis_dtypes.Timestamp(), pd.ArrowDtype(pa.timestamp("us")), id="datetime"
        ),
        pytest.param(ibis_dtypes.float64, pd.Float64Dtype(), id="float"),
        pytest.param(
            ibis_dtypes.GeoSpatial(geotype="geography", srid=4326, nullable=True),
            gpd.array.GeometryDtype(),
            id="geography",
        ),
        pytest.param(ibis_dtypes.int8, pd.Int64Dtype(), id="int8-as-int64"),
        pytest.param(ibis_dtypes.int64, pd.Int64Dtype(), id="int64"),
        # TODO(tswast): custom dtype (or at least string dtype) for JSON objects
        pytest.param(
            ibis_dtypes.Decimal(precision=38, scale=9, nullable=True),
            pd.ArrowDtype(pa.decimal128(38, 9)),
            id="numeric",
        ),
        pytest.param(
            ibis_dtypes.string, pd.StringDtype(storage="pyarrow"), id="string"
        ),
        pytest.param(ibis_dtypes.time, pd.ArrowDtype(pa.time64("us")), id="time"),
        pytest.param(
            ibis_dtypes.Timestamp(timezone="UTC"),
            pd.ArrowDtype(pa.timestamp("us", tz="UTC")),  # type: ignore
            id="timestamp",
        ),
    ],
)
def test_ibis_dtype_converts(ibis_dtype, bigframes_dtype):
    """Test all the Ibis data types needed to read BigQuery tables"""
    result = bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(ibis_dtype)
    assert result == bigframes_dtype


def test_ibis_timestamp_pst_raises_unexpected_datatype():
    """BigQuery timestamp only supports UTC time"""
    with pytest.raises(ValueError, match="'PST'"):
        bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(
            ibis_dtypes.Timestamp(timezone="PST")
        )


def test_ibis_float32_raises_unexpected_datatype():
    """Other Ibis types not read from BigQuery are not expected"""
    with pytest.raises(ValueError, match="Unexpected Ibis data type"):
        bigframes.core.compile.ibis_types.ibis_dtype_to_bigframes_dtype(
            ibis_dtypes.float32
        )


IBIS_ARROW_DTYPES = (
    (ibis_dtypes.boolean, pa.bool_()),
    (ibis_dtypes.date, pa.date32()),
    (ibis_dtypes.Timestamp(), pa.timestamp("us")),
    (ibis_dtypes.float64, pa.float64()),
    (
        ibis_dtypes.Timestamp(timezone="UTC"),
        pa.timestamp("us", tz="UTC"),
    ),
    (
        ibis_dtypes.Struct.from_tuples(
            [
                ("name", ibis_dtypes.string()),
                ("version", ibis_dtypes.int64()),
            ]
        ),
        pa.struct(
            [
                ("name", pa.string()),
                ("version", pa.int64()),
            ]
        ),
    ),
    (
        ibis_dtypes.Struct.from_tuples(
            [
                (
                    "nested",
                    ibis_dtypes.Struct.from_tuples(
                        [
                            ("field", ibis_dtypes.string()),
                        ]
                    ),
                ),
            ]
        ),
        pa.struct(
            [
                (
                    "nested",
                    pa.struct(
                        [
                            ("field", pa.string()),
                        ]
                    ),
                ),
            ]
        ),
    ),
)


@pytest.mark.parametrize(("ibis_dtype", "arrow_dtype"), IBIS_ARROW_DTYPES)
def test_arrow_dtype_to_ibis_dtype(ibis_dtype, arrow_dtype):
    result = bigframes.core.compile.ibis_types._arrow_dtype_to_ibis_dtype(arrow_dtype)
    assert result == ibis_dtype


@pytest.mark.parametrize(("ibis_dtype", "arrow_dtype"), IBIS_ARROW_DTYPES)
def test_ibis_dtype_to_arrow_dtype(ibis_dtype, arrow_dtype):
    result = bigframes.core.compile.ibis_types._ibis_dtype_to_arrow_dtype(ibis_dtype)
    assert result == arrow_dtype


@pytest.mark.parametrize(
    ("ibis_dtype", "bigquery_type"),
    [(ibis_dtypes.String(), "STRING"), (ibis_dtypes.String(nullable=False), "STRING")],
)
def test_ibis_dtype_to_bigquery_type(ibis_dtype, bigquery_type):
    result = ibis_bq_types.BigQueryType.from_ibis(ibis_dtype)
    assert result == bigquery_type


@pytest.mark.parametrize(
    ["bigframes_dtype", "ibis_dtype"],
    [
        # This test covers all dtypes that BigQuery DataFrames can exactly map to Ibis
        (pd.BooleanDtype(), ibis_dtypes.boolean),
        (pd.ArrowDtype(pa.date32()), ibis_dtypes.date),
        (pd.ArrowDtype(pa.timestamp("us")), ibis_dtypes.Timestamp()),
        (pd.Float64Dtype(), ibis_dtypes.float64),
        (pd.Int64Dtype(), ibis_dtypes.int64),
        (pd.StringDtype(storage="pyarrow"), ibis_dtypes.string),
        (pd.ArrowDtype(pa.time64("us")), ibis_dtypes.time),
        (
            pd.ArrowDtype(pa.timestamp("us", tz="UTC")),  # type: ignore
            ibis_dtypes.Timestamp(timezone="UTC"),
        ),
    ],
    ids=[
        "boolean",
        "date",
        "datetime",
        "float",
        "int",
        "string",
        "time",
        "timestamp",
    ],
)
def test_bigframes_dtype_converts(ibis_dtype, bigframes_dtype):
    """Test all the Ibis data types needed to read BigQuery tables"""
    result = bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype(
        bigframes_dtype
    )
    assert result == ibis_dtype


@pytest.mark.parametrize(
    ["bigframes_dtype_str", "ibis_dtype"],
    [
        # This test covers all dtypes that BigQuery DataFrames can exactly map to Ibis
        ("boolean", ibis_dtypes.boolean),
        ("date32[day][pyarrow]", ibis_dtypes.date),
        ("timestamp[us][pyarrow]", ibis_dtypes.Timestamp()),
        ("Float64", ibis_dtypes.float64),
        ("Int64", ibis_dtypes.int64),
        ("string[pyarrow]", ibis_dtypes.string),
        ("time64[us][pyarrow]", ibis_dtypes.time),
        (
            "timestamp[us, tz=UTC][pyarrow]",
            ibis_dtypes.Timestamp(timezone="UTC"),
        ),
        # Special case - "string" is acceptable for "string[pyarrow]"
        ("string", ibis_dtypes.string),
    ],
)
def test_bigframes_string_dtype_converts(ibis_dtype, bigframes_dtype_str):
    """Test all the Ibis data types needed to read BigQuery tables"""
    result = bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype(
        bigframes.dtypes.bigframes_type(bigframes_dtype_str)
    )
    assert result == ibis_dtype


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


def test_unsupported_dtype_raises_unexpected_datatype():
    """Incompatible dtypes should fail when passed into BigQuery DataFrames"""
    with pytest.raises(ValueError, match="Datatype has no ibis type mapping"):
        bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype(np.float32)


def test_unsupported_dtype_str_raises_unexpected_datatype():
    """Incompatible dtypes should fail when passed into BigQuery DataFrames"""
    with pytest.raises(ValueError, match="Datatype has no ibis type mapping"):
        bigframes.core.compile.ibis_types.bigframes_dtype_to_ibis_dtype("int64")


@pytest.mark.parametrize(
    ["literal", "ibis_scalar"],
    [
        (True, ibis_types.literal(True, ibis_dtypes.boolean)),
        (5, ibis_types.literal(5, ibis_dtypes.int64)),
        (-33.2, ibis_types.literal(-33.2, ibis_dtypes.float64)),
    ],
)
def test_literal_to_ibis_scalar_converts(literal, ibis_scalar):
    assert bigframes.core.compile.ibis_types.literal_to_ibis_scalar(literal).equals(
        ibis_scalar
    )


def test_literal_to_ibis_scalar_throws_on_incompatible_literal():
    with pytest.raises(
        ValueError,
    ):
        bigframes.core.compile.ibis_types.literal_to_ibis_scalar({"mykey": "myval"})
