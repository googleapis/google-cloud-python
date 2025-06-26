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

import datetime as dt
import json
import math
import re
import tempfile

import db_dtypes  # type: ignore
import geopandas as gpd  # type: ignore
import google.api_core.exceptions
import numpy
from packaging.version import Version
import pandas as pd
import pyarrow as pa  # type: ignore
import pytest
import shapely.geometry  # type: ignore

import bigframes.dtypes as dtypes
import bigframes.features
import bigframes.pandas
import bigframes.series as series
from bigframes.testing.utils import (
    assert_pandas_df_equal,
    assert_series_equal,
    get_first_file_from_wildcard,
)


def test_series_construct_copy(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = series.Series(
        scalars_df["int64_col"], name="test_series", dtype="Float64"
    ).to_pandas()
    pd_result = pd.Series(
        scalars_pandas_df["int64_col"], name="test_series", dtype="Float64"
    )
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_nullable_ints():
    bf_result = series.Series(
        [1, 3, bigframes.pandas.NA], index=[0, 4, bigframes.pandas.NA]
    ).to_pandas()

    # TODO(b/340885567): fix type error
    expected_index = pd.Index(  # type: ignore
        [0, 4, None],
        dtype=pd.Int64Dtype(),
    )
    expected = pd.Series([1, 3, pd.NA], dtype=pd.Int64Dtype(), index=expected_index)

    pd.testing.assert_series_equal(bf_result, expected)


def test_series_construct_timestamps():
    datetimes = [
        dt.datetime(2020, 1, 20, 20, 20, 20, 20),
        dt.datetime(2019, 1, 20, 20, 20, 20, 20),
        None,
    ]
    bf_result = series.Series(datetimes).to_pandas()
    pd_result = pd.Series(datetimes, dtype=pd.ArrowDtype(pa.timestamp("us")))

    pd.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_series_construct_copy_with_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = series.Series(
        scalars_df["int64_col"],
        name="test_series",
        dtype="Float64",
        index=scalars_df["int64_too"],
    ).to_pandas()
    pd_result = pd.Series(
        scalars_pandas_df["int64_col"],
        name="test_series",
        dtype="Float64",
        index=scalars_pandas_df["int64_too"],
    )
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_copy_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = series.Series(
        scalars_df.index,
        name="test_series",
        dtype="Float64",
        index=scalars_df["int64_too"],
    ).to_pandas()
    pd_result = pd.Series(
        scalars_pandas_df.index,
        name="test_series",
        dtype="Float64",
        index=scalars_pandas_df["int64_too"],
    )
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_pandas(scalars_dfs):
    _, scalars_pandas_df = scalars_dfs
    bf_result = series.Series(
        scalars_pandas_df["int64_col"], name="test_series", dtype="Float64"
    )
    pd_result = pd.Series(
        scalars_pandas_df["int64_col"], name="test_series", dtype="Float64"
    )
    assert bf_result.shape == pd_result.shape
    pd.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


def test_series_construct_from_list():
    bf_result = series.Series([1, 1, 2, 3, 5, 8, 13], dtype="Int64").to_pandas()
    pd_result = pd.Series([1, 1, 2, 3, 5, 8, 13], dtype="Int64")

    # BigQuery DataFrame default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_reindex():
    bf_result = series.Series(
        series.Series({1: 10, 2: 30, 3: 30}), index=[3, 2], dtype="Int64"
    ).to_pandas()
    pd_result = pd.Series(pd.Series({1: 10, 2: 30, 3: 30}), index=[3, 2], dtype="Int64")

    # BigQuery DataFrame default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_from_list_w_index():
    bf_result = series.Series(
        [1, 1, 2, 3, 5, 8, 13], index=[10, 20, 30, 40, 50, 60, 70], dtype="Int64"
    ).to_pandas()
    pd_result = pd.Series(
        [1, 1, 2, 3, 5, 8, 13], index=[10, 20, 30, 40, 50, 60, 70], dtype="Int64"
    )

    # BigQuery DataFrame default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_empty(session: bigframes.Session):
    bf_series: series.Series = series.Series(session=session)
    pd_series: pd.Series = pd.Series()

    bf_result = bf_series.empty
    pd_result = pd_series.empty

    assert pd_result
    assert bf_result == pd_result


def test_series_construct_scalar_no_index():
    bf_result = series.Series("hello world", dtype="string[pyarrow]").to_pandas()
    pd_result = pd.Series("hello world", dtype="string[pyarrow]")

    # BigQuery DataFrame default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_scalar_w_index():
    bf_result = series.Series(
        "hello world", dtype="string[pyarrow]", index=[0, 2, 1]
    ).to_pandas()
    pd_result = pd.Series("hello world", dtype="string[pyarrow]", index=[0, 2, 1])

    # BigQuery DataFrame default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_nan():
    bf_result = series.Series(numpy.nan).to_pandas()
    pd_result = pd.Series(numpy.nan)

    pd_result.index = pd_result.index.astype("Int64")
    pd_result = pd_result.astype("Float64")

    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_scalar_w_bf_index():
    bf_result = series.Series(
        "hello", index=bigframes.pandas.Index([1, 2, 3])
    ).to_pandas()
    pd_result = pd.Series("hello", index=pd.Index([1, 2, 3], dtype="Int64"))

    pd_result = pd_result.astype("string[pyarrow]")

    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_construct_from_list_escaped_strings():
    """Check that special characters are supported."""
    strings = [
        "string\nwith\nnewline",
        "string\twith\ttabs",
        "string\\with\\backslashes",
    ]
    bf_result = series.Series(strings, name="test_series", dtype="string[pyarrow]")
    pd_result = pd.Series(strings, name="test_series", dtype="string[pyarrow]")

    # BigQuery DataFrame default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


def test_series_construct_geodata():
    pd_series = pd.Series(
        [
            shapely.geometry.Point(1, 1),
            shapely.geometry.Point(2, 2),
            shapely.geometry.Point(3, 3),
        ],
        dtype=gpd.array.GeometryDtype(),
    )

    series = bigframes.pandas.Series(pd_series)

    pd.testing.assert_series_equal(
        pd_series, series.to_pandas(), check_index_type=False
    )


@pytest.mark.parametrize(
    ("dtype"),
    [
        pytest.param(pd.Int64Dtype(), id="int"),
        pytest.param(pd.Float64Dtype(), id="float"),
        pytest.param(pd.StringDtype(storage="pyarrow"), id="string"),
    ],
)
def test_series_construct_w_dtype(dtype):
    data = [1, 2, 3]
    expected = pd.Series(data, dtype=dtype)
    expected.index = expected.index.astype("Int64")
    series = bigframes.pandas.Series(data, dtype=dtype)
    pd.testing.assert_series_equal(series.to_pandas(), expected)


def test_series_construct_w_dtype_for_struct():
    # The data shows the struct fields are disordered and correctly handled during
    # construction.
    data = [
        {"a": 1, "c": "pandas", "b": dt.datetime(2020, 1, 20, 20, 20, 20, 20)},
        {"a": 2, "c": "pandas", "b": dt.datetime(2019, 1, 20, 20, 20, 20, 20)},
        {"a": 1, "c": "numpy", "b": None},
    ]
    dtype = pd.ArrowDtype(
        pa.struct([("a", pa.int64()), ("c", pa.string()), ("b", pa.timestamp("us"))])
    )
    series = bigframes.pandas.Series(data, dtype=dtype)
    expected = pd.Series(data, dtype=dtype)
    expected.index = expected.index.astype("Int64")
    pd.testing.assert_series_equal(series.to_pandas(), expected)


def test_series_construct_w_dtype_for_array_string():
    data = [["1", "2", "3"], [], ["4", "5"]]
    dtype = pd.ArrowDtype(pa.list_(pa.string()))
    series = bigframes.pandas.Series(data, dtype=dtype)
    expected = pd.Series(data, dtype=dtype)
    expected.index = expected.index.astype("Int64")

    # Skip dtype check due to internal issue b/321013333. This issue causes array types
    # to be converted to the `object` dtype when calling `to_pandas()`, resulting in
    # a mismatch with the expected Pandas type.
    if bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable:
        check_dtype = True
    else:
        check_dtype = False

    pd.testing.assert_series_equal(
        series.to_pandas(), expected, check_dtype=check_dtype
    )


def test_series_construct_w_dtype_for_array_struct():
    data = [[{"a": 1, "c": "aa"}, {"a": 2, "c": "bb"}], [], [{"a": 3, "c": "cc"}]]
    dtype = pd.ArrowDtype(pa.list_(pa.struct([("a", pa.int64()), ("c", pa.string())])))
    series = bigframes.pandas.Series(data, dtype=dtype)
    expected = pd.Series(data, dtype=dtype)
    expected.index = expected.index.astype("Int64")

    # Skip dtype check due to internal issue b/321013333. This issue causes array types
    # to be converted to the `object` dtype when calling `to_pandas()`, resulting in
    # a mismatch with the expected Pandas type.
    if bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable:
        check_dtype = True
    else:
        check_dtype = False

    pd.testing.assert_series_equal(
        series.to_pandas(), expected, check_dtype=check_dtype
    )


def test_series_construct_local_unordered_has_sequential_index(unordered_session):
    series = bigframes.pandas.Series(
        ["Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat"], session=unordered_session
    )
    expected: pd.Index = pd.Index([0, 1, 2, 3, 4, 5, 6], dtype=pd.Int64Dtype())
    pd.testing.assert_index_equal(series.index.to_pandas(), expected)


def test_series_construct_w_dtype_for_json():
    data = [
        "1",
        '"str"',
        "false",
        '["a", {"b": 1}, null]',
        None,
        '{"a": {"b": [1, 2, 3], "c": true}}',
    ]
    s = bigframes.pandas.Series(data, dtype=dtypes.JSON_DTYPE)

    assert s[0] == "1"
    assert s[1] == '"str"'
    assert s[2] == "false"
    assert s[3] == '["a",{"b":1},null]'
    assert pd.isna(s[4])
    assert s[5] == '{"a":{"b":[1,2,3],"c":true}}'


def test_series_keys(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_col"].keys().to_pandas()
    pd_result = scalars_pandas_df["int64_col"].keys()
    pd.testing.assert_index_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ["data", "index"],
    [
        (["a", "b", "c"], None),
        ([1, 2, 3], ["a", "b", "c"]),
        ([1, 2, None], ["a", "b", "c"]),
        ([1, 2, 3], [pd.NA, "b", "c"]),
        ([numpy.nan, 2, 3], ["a", "b", "c"]),
    ],
)
def test_series_items(data, index):
    bf_series = series.Series(data, index=index)
    pd_series = pd.Series(data, index=index)

    for (bf_index, bf_value), (pd_index, pd_value) in zip(
        bf_series.items(), pd_series.items()
    ):
        # TODO(jialuo): Remove the if conditions after b/373699458 is addressed.
        if not pd.isna(bf_index) or not pd.isna(pd_index):
            assert bf_index == pd_index
        if not pd.isna(bf_value) or not pd.isna(pd_value):
            assert bf_value == pd_value


@pytest.mark.parametrize(
    ["col_name", "expected_dtype"],
    [
        ("bool_col", pd.BooleanDtype()),
        # TODO(swast): Use a more efficient type.
        ("bytes_col", pd.ArrowDtype(pa.binary())),
        ("date_col", pd.ArrowDtype(pa.date32())),
        ("datetime_col", pd.ArrowDtype(pa.timestamp("us"))),
        ("float64_col", pd.Float64Dtype()),
        ("geography_col", gpd.array.GeometryDtype()),
        ("int64_col", pd.Int64Dtype()),
        # TODO(swast): Use a more efficient type.
        ("numeric_col", pd.ArrowDtype(pa.decimal128(38, 9))),
        ("int64_too", pd.Int64Dtype()),
        ("string_col", pd.StringDtype(storage="pyarrow")),
        ("time_col", pd.ArrowDtype(pa.time64("us"))),
        ("timestamp_col", pd.ArrowDtype(pa.timestamp("us", tz="UTC"))),
    ],
)
def test_get_column(scalars_dfs, col_name, expected_dtype):
    scalars_df, scalars_pandas_df = scalars_dfs
    series = scalars_df[col_name]
    series_pandas = series.to_pandas()
    assert series_pandas.dtype == expected_dtype
    assert series_pandas.shape[0] == scalars_pandas_df.shape[0]


def test_get_column_w_json(json_df, json_pandas_df):
    series = json_df["json_col"]
    series_pandas = series.to_pandas()
    assert series.dtype == pd.ArrowDtype(db_dtypes.JSONArrowType())
    assert series_pandas.shape[0] == json_pandas_df.shape[0]


def test_series_get_column_default(scalars_dfs):
    scalars_df, _ = scalars_dfs
    result = scalars_df.get(123123123123123, "default_val")
    assert result == "default_val"


def test_series_equals_identical(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.int64_col.equals(scalars_df_index.int64_col)
    pd_result = scalars_pandas_df_index.int64_col.equals(
        scalars_pandas_df_index.int64_col
    )

    assert pd_result == bf_result


def test_series_equals_df(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].equals(scalars_df_index[["int64_col"]])
    pd_result = scalars_pandas_df_index["int64_col"].equals(
        scalars_pandas_df_index[["int64_col"]]
    )

    assert pd_result == bf_result


def test_series_equals_different_dtype(scalars_df_index, scalars_pandas_df_index):
    bf_series = scalars_df_index["int64_col"]
    pd_series = scalars_pandas_df_index["int64_col"]

    bf_result = bf_series.equals(bf_series.astype("Float64"))
    pd_result = pd_series.equals(pd_series.astype("Float64"))

    assert pd_result == bf_result


def test_series_equals_different_values(scalars_df_index, scalars_pandas_df_index):
    bf_series = scalars_df_index["int64_col"]
    pd_series = scalars_pandas_df_index["int64_col"]

    bf_result = bf_series.equals(bf_series + 1)
    pd_result = pd_series.equals(pd_series + 1)

    assert pd_result == bf_result


def test_series_get_with_default_index(scalars_dfs):
    col_name = "float64_col"
    key = 2
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].get(key)
    pd_result = scalars_pandas_df[col_name].get(key)
    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("index_col", "key"),
    (
        ("int64_too", 2),
        ("string_col", "Hello, World!"),
        ("int64_too", slice(2, 6)),
    ),
)
def test_series___getitem__(scalars_dfs, index_col, key):
    col_name = "float64_col"
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.set_index(index_col, drop=False)
    scalars_pandas_df = scalars_pandas_df.set_index(index_col, drop=False)
    bf_result = scalars_df[col_name][key]
    pd_result = scalars_pandas_df[col_name][key]
    pd.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


@pytest.mark.parametrize(
    ("key",),
    (
        (-2,),
        (-1,),
        (0,),
        (1,),
    ),
)
def test_series___getitem___with_int_key(scalars_dfs, key):
    col_name = "int64_too"
    index_col = "string_col"
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.set_index(index_col, drop=False)
    scalars_pandas_df = scalars_pandas_df.set_index(index_col, drop=False)
    bf_result = scalars_df[col_name][key]
    pd_result = scalars_pandas_df[col_name][key]
    assert bf_result == pd_result


def test_series___getitem___with_default_index(scalars_dfs):
    col_name = "float64_col"
    key = 2
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name][key]
    pd_result = scalars_pandas_df[col_name][key]
    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("index_col", "key", "value"),
    (
        ("int64_too", 2, "new_string_value"),
        ("string_col", "Hello, World!", "updated_value"),
        ("int64_too", 0, None),
    ),
)
def test_series___setitem__(scalars_dfs, index_col, key, value):
    col_name = "string_col"
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.set_index(index_col, drop=False)
    scalars_pandas_df = scalars_pandas_df.set_index(index_col, drop=False)

    bf_series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name].copy()

    bf_series[key] = value
    pd_series[key] = value

    pd.testing.assert_series_equal(bf_series.to_pandas(), pd_series)


@pytest.mark.parametrize(
    ("key", "value"),
    (
        (0, 999),
        (1, 888),
        (0, None),
        (-2345, 777),
    ),
)
def test_series___setitem___with_int_key_numeric(scalars_dfs, key, value):
    col_name = "int64_col"
    index_col = "int64_too"
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.set_index(index_col, drop=False)
    scalars_pandas_df = scalars_pandas_df.set_index(index_col, drop=False)

    bf_series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name].copy()

    bf_series[key] = value
    pd_series[key] = value

    pd.testing.assert_series_equal(bf_series.to_pandas(), pd_series)


def test_series___setitem___with_default_index(scalars_dfs):
    col_name = "float64_col"
    key = 2
    value = 123.456
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name].copy()

    bf_series[key] = value
    pd_series[key] = value

    assert bf_series.to_pandas().iloc[key] == pd_series.iloc[key]


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_too",),
    ),
)
def test_abs(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].abs().to_pandas()
    pd_result = scalars_pandas_df[col_name].abs()

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_too",),
    ),
)
def test_series_pos(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (+scalars_df[col_name]).to_pandas()
    pd_result = +scalars_pandas_df[col_name]

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_too",),
    ),
)
def test_series_neg(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (-scalars_df[col_name]).to_pandas()
    pd_result = -scalars_pandas_df[col_name]

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("bool_col",),
        ("int64_col",),
    ),
)
def test_series_invert(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (~scalars_df[col_name]).to_pandas()
    pd_result = ~scalars_pandas_df[col_name]

    assert_series_equal(pd_result, bf_result)


def test_fillna(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name].fillna("Missing").to_pandas()
    pd_result = scalars_pandas_df[col_name].fillna("Missing")
    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_series_replace_scalar_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = (
        scalars_df[col_name].replace("Hello, World!", "Howdy, Planet!").to_pandas()
    )
    pd_result = scalars_pandas_df[col_name].replace("Hello, World!", "Howdy, Planet!")

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


def test_series_replace_regex_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = (
        scalars_df[col_name].replace("^H.l", "Howdy, Planet!", regex=True).to_pandas()
    )
    pd_result = scalars_pandas_df[col_name].replace(
        "^H.l", "Howdy, Planet!", regex=True
    )

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


def test_series_replace_list_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = (
        scalars_df[col_name]
        .replace(["Hello, World!", "T"], "Howdy, Planet!")
        .to_pandas()
    )
    pd_result = scalars_pandas_df[col_name].replace(
        ["Hello, World!", "T"], "Howdy, Planet!"
    )

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


def test_series_replace_nans_with_pd_na(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name].replace({pd.NA: "UNKNOWN"}).to_pandas()
    pd_result = scalars_pandas_df[col_name].replace({pd.NA: "UNKNOWN"})

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("replacement_dict",),
    (
        ({"Hello, World!": "Howdy, Planet!", "T": "R"},),
        ({},),
    ),
    ids=[
        "non-empty",
        "empty",
    ],
)
def test_series_replace_dict(scalars_dfs, replacement_dict):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name].replace(replacement_dict).to_pandas()
    pd_result = scalars_pandas_df[col_name].replace(replacement_dict)

    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("method",),
    (
        ("linear",),
        ("values",),
        ("slinear",),
        ("nearest",),
        ("zero",),
        ("pad",),
    ),
)
def test_series_interpolate(method):
    pytest.importorskip("scipy")

    values = [None, 1, 2, None, None, 16, None]
    index = [-3.2, 11.4, 3.56, 4, 4.32, 5.55, 76.8]
    pd_series = pd.Series(values, index)
    bf_series = series.Series(pd_series)

    # Pandas can only interpolate on "float64" columns
    # https://github.com/pandas-dev/pandas/issues/40252
    pd_result = pd_series.astype("float64").interpolate(method=method)
    bf_result = bf_series.interpolate(method=method).to_pandas()

    # pd uses non-null types, while bf uses nullable types
    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize(
    ("ignore_index",),
    (
        (True,),
        (False,),
    ),
)
def test_series_dropna(scalars_dfs, ignore_index):
    if pd.__version__.startswith("1."):
        pytest.skip("ignore_index parameter not supported in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name].dropna(ignore_index=ignore_index).to_pandas()
    pd_result = scalars_pandas_df[col_name].dropna(ignore_index=ignore_index)
    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


@pytest.mark.parametrize(
    ("agg",),
    (
        ("sum",),
        ("size",),
    ),
)
def test_series_agg_single_string(scalars_dfs, agg):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_col"].agg(agg)
    pd_result = scalars_pandas_df["int64_col"].agg(agg)
    assert math.isclose(pd_result, bf_result)


def test_series_agg_multi_string(scalars_dfs):
    aggregations = [
        "sum",
        "mean",
        "std",
        "var",
        "min",
        "max",
        "nunique",
        "count",
        "size",
    ]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_col"].agg(aggregations).to_pandas()
    pd_result = scalars_pandas_df["int64_col"].agg(aggregations)

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("string_col",),
        ("int64_col",),
    ),
)
def test_max(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].max()
    pd_result = scalars_pandas_df[col_name].max()
    assert pd_result == bf_result


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("string_col",),
        ("int64_col",),
    ),
)
def test_min(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].min()
    pd_result = scalars_pandas_df[col_name].min()
    assert pd_result == bf_result


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_col",),
    ),
)
def test_std(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].std()
    pd_result = scalars_pandas_df[col_name].std()
    assert math.isclose(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_col",),
    ),
)
def test_kurt(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].kurt()
    pd_result = scalars_pandas_df[col_name].kurt()
    assert math.isclose(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_col",),
    ),
)
def test_skew(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].skew()
    pd_result = scalars_pandas_df[col_name].skew()
    assert math.isclose(pd_result, bf_result)


def test_skew_undefined(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_col"].iloc[:2].skew()
    pd_result = scalars_pandas_df["int64_col"].iloc[:2].skew()
    # both should be pd.NA
    assert pd_result is bf_result


def test_kurt_undefined(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_col"].iloc[:3].kurt()
    pd_result = scalars_pandas_df["int64_col"].iloc[:3].kurt()
    # both should be pd.NA
    assert pd_result is bf_result


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("float64_col",),
        ("int64_col",),
    ),
)
def test_var(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].var()
    pd_result = scalars_pandas_df[col_name].var()
    assert math.isclose(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("bool_col",),
        ("int64_col",),
    ),
)
def test_mode_stat(scalars_df_index, scalars_pandas_df_index, col_name):
    bf_result = scalars_df_index[col_name].mode().to_pandas()
    pd_result = scalars_pandas_df_index[col_name].mode()

    ## Mode implicitly resets index, and bigframes default indices use nullable Int64
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x, y: x + y),
        (lambda x, y: x - y),
        (lambda x, y: x * y),
        (lambda x, y: x / y),
        (lambda x, y: x // y),
        (lambda x, y: x < y),
        (lambda x, y: x > y),
        (lambda x, y: x <= y),
        (lambda x, y: x >= y),
    ],
    ids=[
        "add",
        "subtract",
        "multiply",
        "divide",
        "floordivide",
        "less_than",
        "greater_than",
        "less_than_equal",
        "greater_than_equal",
    ],
)
@pytest.mark.parametrize(("other_scalar"), [-1, 0, 14, pd.NA])
@pytest.mark.parametrize(("reverse_operands"), [True, False])
def test_series_int_int_operators_scalar(
    scalars_dfs, operator, other_scalar, reverse_operands
):
    scalars_df, scalars_pandas_df = scalars_dfs

    maybe_reversed_op = (lambda x, y: operator(y, x)) if reverse_operands else operator

    bf_result = maybe_reversed_op(scalars_df["int64_col"], other_scalar).to_pandas()
    pd_result = maybe_reversed_op(scalars_pandas_df["int64_col"], other_scalar)

    assert_series_equal(pd_result, bf_result)


def test_series_pow_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (scalars_df["int64_col"] ** 2).to_pandas()
    pd_result = scalars_pandas_df["int64_col"] ** 2

    assert_series_equal(pd_result, bf_result)


def test_series_pow_scalar_reverse(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (0.8 ** scalars_df["int64_col"]).to_pandas()
    pd_result = 0.8 ** scalars_pandas_df["int64_col"]

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x, y: x & y),
        (lambda x, y: x | y),
        (lambda x, y: x ^ y),
    ],
    ids=[
        "and",
        "or",
        "xor",
    ],
)
@pytest.mark.parametrize(("other_scalar"), [True, False, pd.NA])
@pytest.mark.parametrize(("reverse_operands"), [True, False])
def test_series_bool_bool_operators_scalar(
    scalars_dfs, operator, other_scalar, reverse_operands
):
    scalars_df, scalars_pandas_df = scalars_dfs

    maybe_reversed_op = (lambda x, y: operator(y, x)) if reverse_operands else operator

    bf_result = maybe_reversed_op(scalars_df["bool_col"], other_scalar).to_pandas()
    pd_result = maybe_reversed_op(scalars_pandas_df["bool_col"], other_scalar)

    assert_series_equal(pd_result.astype(pd.BooleanDtype()), bf_result)


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x, y: x + y),
        (lambda x, y: x - y),
        (lambda x, y: x * y),
        (lambda x, y: x / y),
        (lambda x, y: x < y),
        (lambda x, y: x > y),
        (lambda x, y: x <= y),
        (lambda x, y: x >= y),
        (lambda x, y: x % y),
        (lambda x, y: x // y),
        (lambda x, y: x & y),
        (lambda x, y: x | y),
        (lambda x, y: x ^ y),
    ],
    ids=[
        "add",
        "subtract",
        "multiply",
        "divide",
        "less_than",
        "greater_than",
        "less_than_equal",
        "greater_than_equal",
        "modulo",
        "floordivide",
        "bitwise_and",
        "bitwise_or",
        "bitwise_xor",
    ],
)
def test_series_int_int_operators_series(scalars_dfs, operator):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = operator(scalars_df["int64_col"], scalars_df["int64_too"]).to_pandas()
    pd_result = operator(scalars_pandas_df["int64_col"], scalars_pandas_df["int64_too"])
    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_x",),
    [
        ("int64_col",),
        ("int64_too",),
        ("float64_col",),
    ],
)
@pytest.mark.parametrize(
    ("col_y",),
    [
        ("int64_col",),
        ("int64_too",),
        ("float64_col",),
    ],
)
@pytest.mark.parametrize(
    ("method",),
    [
        ("mod",),
        ("rmod",),
    ],
)
def test_mods(scalars_dfs, col_x, col_y, method):
    scalars_df, scalars_pandas_df = scalars_dfs
    x_bf = scalars_df[col_x]
    y_bf = scalars_df[col_y]
    bf_series = getattr(x_bf, method)(y_bf)
    # BigQuery's mod functions return [BIG]NUMERIC values unless both arguments are integers.
    # https://cloud.google.com/bigquery/docs/reference/standard-sql/mathematical_functions#mod
    if x_bf.dtype == pd.Int64Dtype() and y_bf.dtype == pd.Int64Dtype():
        bf_result = bf_series.to_pandas()
    else:
        bf_result = bf_series.astype("Float64").to_pandas()
    pd_result = getattr(scalars_pandas_df[col_x], method)(scalars_pandas_df[col_y])
    pd.testing.assert_series_equal(pd_result, bf_result)


# We work around a pandas bug that doesn't handle correlating nullable dtypes by doing this
# manually with dumb self-correlation instead of parameterized as test_mods is above.
def test_series_corr(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_too"].corr(scalars_df["int64_too"])
    pd_result = (
        scalars_pandas_df["int64_too"]
        .astype("int64")
        .corr(scalars_pandas_df["int64_too"].astype("int64"))
    )
    assert math.isclose(pd_result, bf_result)


def test_series_autocorr(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["float64_col"].autocorr(2)
    pd_result = scalars_pandas_df["float64_col"].autocorr(2)
    assert math.isclose(pd_result, bf_result)


def test_series_cov(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_too"].cov(scalars_df["int64_too"])
    pd_result = (
        scalars_pandas_df["int64_too"]
        .astype("int64")
        .cov(scalars_pandas_df["int64_too"].astype("int64"))
    )
    assert math.isclose(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_x",),
    [
        ("int64_col",),
        ("float64_col",),
    ],
)
@pytest.mark.parametrize(
    ("col_y",),
    [
        ("int64_col",),
        ("float64_col",),
    ],
)
@pytest.mark.parametrize(
    ("method",),
    [
        ("divmod",),
        ("rdivmod",),
    ],
)
def test_divmods_series(scalars_dfs, col_x, col_y, method):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_div_result, bf_mod_result = getattr(scalars_df[col_x], method)(scalars_df[col_y])
    pd_div_result, pd_mod_result = getattr(scalars_pandas_df[col_x], method)(
        scalars_pandas_df[col_y]
    )
    # BigQuery's mod functions return NUMERIC values for non-INT64 inputs.
    if bf_div_result.dtype == pd.Int64Dtype():
        pd.testing.assert_series_equal(pd_div_result, bf_div_result.to_pandas())
    else:
        pd.testing.assert_series_equal(
            pd_div_result, bf_div_result.astype("Float64").to_pandas()
        )

    if bf_mod_result.dtype == pd.Int64Dtype():
        pd.testing.assert_series_equal(pd_mod_result, bf_mod_result.to_pandas())
    else:
        pd.testing.assert_series_equal(
            pd_mod_result, bf_mod_result.astype("Float64").to_pandas()
        )


@pytest.mark.parametrize(
    ("col_x",),
    [
        ("int64_col",),
        ("float64_col",),
    ],
)
@pytest.mark.parametrize(
    ("other",),
    [
        (-1000,),
        (678,),
    ],
)
@pytest.mark.parametrize(
    ("method",),
    [
        ("divmod",),
        ("rdivmod",),
    ],
)
def test_divmods_scalars(scalars_dfs, col_x, other, method):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_div_result, bf_mod_result = getattr(scalars_df[col_x], method)(other)
    pd_div_result, pd_mod_result = getattr(scalars_pandas_df[col_x], method)(other)
    # BigQuery's mod functions return NUMERIC values for non-INT64 inputs.
    if bf_div_result.dtype == pd.Int64Dtype():
        pd.testing.assert_series_equal(pd_div_result, bf_div_result.to_pandas())
    else:
        pd.testing.assert_series_equal(
            pd_div_result, bf_div_result.astype("Float64").to_pandas()
        )

    if bf_mod_result.dtype == pd.Int64Dtype():
        pd.testing.assert_series_equal(pd_mod_result, bf_mod_result.to_pandas())
    else:
        pd.testing.assert_series_equal(
            pd_mod_result, bf_mod_result.astype("Float64").to_pandas()
        )


@pytest.mark.parametrize(
    ("other",),
    [
        (3,),
        (-6.2,),
    ],
)
def test_series_add_scalar(scalars_dfs, other):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (scalars_df["float64_col"] + other).to_pandas()
    pd_result = scalars_pandas_df["float64_col"] + other

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("left_col", "right_col"),
    [
        ("float64_col", "float64_col"),
        ("int64_col", "float64_col"),
        ("int64_col", "int64_too"),
    ],
)
def test_series_add_bigframes_series(scalars_dfs, left_col, right_col):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (scalars_df[left_col] + scalars_df[right_col]).to_pandas()
    pd_result = scalars_pandas_df[left_col] + scalars_pandas_df[right_col]

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("left_col", "right_col", "righter_col"),
    [
        ("float64_col", "float64_col", "float64_col"),
        ("int64_col", "int64_col", "int64_col"),
    ],
)
def test_series_add_bigframes_series_nested(
    scalars_dfs, left_col, right_col, righter_col
):
    """Test that we can correctly add multiple times."""
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (
        (scalars_df[left_col] + scalars_df[right_col]) + scalars_df[righter_col]
    ).to_pandas()
    pd_result = (
        scalars_pandas_df[left_col] + scalars_pandas_df[right_col]
    ) + scalars_pandas_df[righter_col]

    assert_series_equal(pd_result, bf_result)


def test_series_add_different_table_default_index(
    scalars_df_default_index,
    scalars_df_2_default_index,
):
    bf_result = (
        scalars_df_default_index["float64_col"]
        + scalars_df_2_default_index["float64_col"]
    ).to_pandas()
    pd_result = (
        # Default index may not have a well defined order, but it should at
        # least be consistent across to_pandas() calls.
        scalars_df_default_index["float64_col"].to_pandas()
        + scalars_df_2_default_index["float64_col"].to_pandas()
    )
    # TODO(swast): Can remove sort_index() when there's default ordering.
    pd.testing.assert_series_equal(bf_result.sort_index(), pd_result.sort_index())


def test_series_add_different_table_with_index(
    scalars_df_index, scalars_df_2_index, scalars_pandas_df_index
):
    scalars_pandas_df = scalars_pandas_df_index
    bf_result = scalars_df_index["float64_col"] + scalars_df_2_index["int64_col"]
    # When index values are unique, we can emulate with values from the same
    # DataFrame.
    pd_result = scalars_pandas_df["float64_col"] + scalars_pandas_df["int64_col"]
    pd.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


def test_reset_index_drop(scalars_df_index, scalars_pandas_df_index):
    scalars_pandas_df = scalars_pandas_df_index
    bf_result = (
        scalars_df_index["float64_col"]
        .sort_index(ascending=False)
        .reset_index(drop=True)
    ).iloc[::2]
    pd_result = (
        scalars_pandas_df["float64_col"]
        .sort_index(ascending=False)
        .reset_index(drop=True)
    ).iloc[::2]

    # BigQuery DataFrames default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


@pytest.mark.parametrize(
    ("name",),
    [
        ("some_name",),
        (None,),
    ],
)
def test_reset_index_no_drop(scalars_df_index, scalars_pandas_df_index, name):
    scalars_pandas_df = scalars_pandas_df_index
    kw_args = {"name": name} if name else {}
    bf_result = (
        scalars_df_index["float64_col"]
        .sort_index(ascending=False)
        .reset_index(drop=False, **kw_args)
    )
    pd_result = (
        scalars_pandas_df["float64_col"]
        .sort_index(ascending=False)
        .reset_index(drop=False, **kw_args)
    )

    # BigQuery DataFrames default indices use nullable Int64 always
    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_frame_equal(bf_result.to_pandas(), pd_result)


def test_copy(scalars_df_index, scalars_pandas_df_index):
    col_name = "float64_col"
    # Expect mutation on original not to effect_copy
    bf_series = scalars_df_index[col_name].copy()
    bf_copy = bf_series.copy()
    bf_copy.loc[0] = 5.6
    bf_series.loc[0] = 3.4

    pd_series = scalars_pandas_df_index[col_name].copy()
    pd_copy = pd_series.copy()
    pd_copy.loc[0] = 5.6
    pd_series.loc[0] = 3.4

    assert bf_copy.to_pandas().loc[0] != bf_series.to_pandas().loc[0]
    pd.testing.assert_series_equal(bf_copy.to_pandas(), pd_copy)


def test_isin_raise_error(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_too"
    with pytest.raises(TypeError):
        scalars_df_index[col_name].isin("whatever").to_pandas()


@pytest.mark.parametrize(
    (
        "col_name",
        "test_set",
    ),
    [
        (
            "int64_col",
            [314159, 2.0, 3, pd.NA],
        ),
        (
            "int64_col",
            [2, 55555, 4],
        ),
        (
            "float64_col",
            [-123.456, 1.25, pd.NA],
        ),
        (
            "int64_too",
            [1, 2, pd.NA],
        ),
        (
            "string_col",
            ["Hello, World!", "Hi", "こんにちは"],
        ),
    ],
)
def test_isin(scalars_dfs, col_name, test_set):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[col_name].isin(test_set).to_pandas()
    pd_result = scalars_pandas_df[col_name].isin(test_set).astype("boolean")
    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    (
        "col_name",
        "test_set",
    ),
    [
        (
            "int64_col",
            [314159, 2.0, 3, pd.NA],
        ),
        (
            "int64_col",
            [2, 55555, 4],
        ),
        (
            "float64_col",
            [-123.456, 1.25, pd.NA],
        ),
        (
            "int64_too",
            [1, 2, pd.NA],
        ),
        (
            "string_col",
            ["Hello, World!", "Hi", "こんにちは"],
        ),
    ],
)
def test_isin_bigframes_values(scalars_dfs, col_name, test_set, session):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (
        scalars_df[col_name].isin(series.Series(test_set, session=session)).to_pandas()
    )
    pd_result = scalars_pandas_df[col_name].isin(test_set).astype("boolean")
    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


def test_isin_bigframes_index(scalars_dfs, session):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = (
        scalars_df["string_col"]
        .isin(bigframes.pandas.Index(["Hello, World!", "Hi", "こんにちは"], session=session))
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df["string_col"]
        .isin(pd.Index(["Hello, World!", "Hi", "こんにちは"]))
        .astype("boolean")
    )
    pd.testing.assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    (
        "col_name",
        "test_set",
    ),
    [
        (
            "int64_col",
            [314159, 2.0, 3, pd.NA],
        ),
        (
            "int64_col",
            [2, 55555, 4],
        ),
        (
            "float64_col",
            [-123.456, 1.25, pd.NA],
        ),
        (
            "int64_too",
            [1, 2, pd.NA],
        ),
        (
            "string_col",
            ["Hello, World!", "Hi", "こんにちは"],
        ),
    ],
)
def test_isin_bigframes_values_as_predicate(
    scalars_dfs_maybe_ordered, col_name, test_set
):
    scalars_df, scalars_pandas_df = scalars_dfs_maybe_ordered
    bf_predicate = scalars_df[col_name].isin(
        series.Series(test_set, session=scalars_df._session)
    )
    bf_result = scalars_df[bf_predicate].to_pandas()
    pd_predicate = scalars_pandas_df[col_name].isin(test_set)
    pd_result = scalars_pandas_df[pd_predicate]

    pd.testing.assert_frame_equal(
        pd_result.reset_index(),
        bf_result.reset_index(),
    )


def test_isnull(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "float64_col"
    bf_series = scalars_df[col_name].isnull().to_pandas()
    pd_series = scalars_pandas_df[col_name].isnull()

    # One of dtype mismatches to be documented. Here, the `bf_series.dtype` is `BooleanDtype` but
    # the `pd_series.dtype` is `bool`.
    assert_series_equal(pd_series.astype(pd.BooleanDtype()), bf_series)


def test_notnull(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_series = scalars_df[col_name].notnull().to_pandas()
    pd_series = scalars_pandas_df[col_name].notnull()

    # One of dtype mismatches to be documented. Here, the `bf_series.dtype` is `BooleanDtype` but
    # the `pd_series.dtype` is `bool`.
    assert_series_equal(pd_series.astype(pd.BooleanDtype()), bf_series)


def test_round(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "float64_col"
    bf_result = scalars_df[col_name].round().to_pandas()
    pd_result = scalars_pandas_df[col_name].round()

    assert_series_equal(pd_result, bf_result)


def test_eq_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_result = scalars_df[col_name].eq(0).to_pandas()
    pd_result = scalars_pandas_df[col_name].eq(0)

    assert_series_equal(pd_result, bf_result)


def test_eq_wider_type_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_result = scalars_df[col_name].eq(1.0).to_pandas()
    pd_result = scalars_pandas_df[col_name].eq(1.0)

    assert_series_equal(pd_result, bf_result)


def test_ne_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_result = (scalars_df[col_name] != 0).to_pandas()
    pd_result = scalars_pandas_df[col_name] != 0

    assert_series_equal(pd_result, bf_result)


def test_eq_int_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_result = (scalars_df[col_name] == 0).to_pandas()
    pd_result = scalars_pandas_df[col_name] == 0

    assert_series_equal(pd_result, bf_result)


@pytest.mark.parametrize(
    ("col_name",),
    (
        ("string_col",),
        ("float64_col",),
        ("int64_too",),
    ),
)
def test_eq_same_type_series(scalars_dfs, col_name):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = (scalars_df[col_name] == scalars_df[col_name]).to_pandas()
    pd_result = scalars_pandas_df[col_name] == scalars_pandas_df[col_name]

    # One of dtype mismatches to be documented. Here, the `bf_series.dtype` is `BooleanDtype` but
    # the `pd_series.dtype` is `bool`.
    assert_series_equal(pd_result.astype(pd.BooleanDtype()), bf_result)


def test_loc_setitem_cell(scalars_df_index, scalars_pandas_df_index):
    bf_original = scalars_df_index["string_col"]
    bf_series = scalars_df_index["string_col"]
    pd_original = scalars_pandas_df_index["string_col"]
    pd_series = scalars_pandas_df_index["string_col"].copy()
    bf_series.loc[2] = "This value isn't in the test data."
    pd_series.loc[2] = "This value isn't in the test data."
    bf_result = bf_series.to_pandas()
    pd_result = pd_series
    pd.testing.assert_series_equal(bf_result, pd_result)
    # Per Copy-on-Write semantics, other references to the original DataFrame
    # should remain unchanged.
    pd.testing.assert_series_equal(bf_original.to_pandas(), pd_original)


def test_at_setitem_row_label_scalar(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series = scalars_df["int64_col"]
    pd_series = scalars_pandas_df["int64_col"].copy()
    bf_series.at[1] = 1000
    pd_series.at[1] = 1000
    bf_result = bf_series.to_pandas()
    pd_result = pd_series.astype("Int64")
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_ne_obj_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = (scalars_df[col_name] != scalars_df[col_name]).to_pandas()
    pd_result = scalars_pandas_df[col_name] != scalars_pandas_df[col_name]

    # One of dtype mismatches to be documented. Here, the `bf_series.dtype` is `BooleanDtype` but
    # the `pd_series.dtype` is `bool`.
    assert_series_equal(pd_result.astype(pd.BooleanDtype()), bf_result)


def test_indexing_using_unselected_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name][scalars_df["int64_too"].eq(0)].to_pandas()
    pd_result = scalars_pandas_df[col_name][scalars_pandas_df["int64_too"].eq(0)]

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_indexing_using_selected_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "string_col"
    bf_result = scalars_df[col_name][
        scalars_df["string_col"].eq("Hello, World!")
    ].to_pandas()
    pd_result = scalars_pandas_df[col_name][
        scalars_pandas_df["string_col"].eq("Hello, World!")
    ]

    assert_series_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("indices"),
    [
        ([1, 3, 5]),
        ([5, -3, -5, -6]),
        ([-2, -4, -6]),
    ],
)
def test_take(scalars_dfs, indices):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df.take(indices).to_pandas()
    pd_result = scalars_pandas_df.take(indices)

    assert_pandas_df_equal(bf_result, pd_result)


def test_nested_filter(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    string_col = scalars_df["string_col"]
    int64_too = scalars_df["int64_too"]
    bool_col = scalars_df["bool_col"] == bool(
        True
    )  # Convert from nullable bool to nonnullable bool usable as indexer
    bf_result = string_col[int64_too == 0][~bool_col].to_pandas()

    pd_string_col = scalars_pandas_df["string_col"]
    pd_int64_too = scalars_pandas_df["int64_too"]
    pd_bool_col = scalars_pandas_df["bool_col"] == bool(
        True
    )  # Convert from nullable bool to nonnullable bool usable as indexer
    pd_result = pd_string_col[pd_int64_too == 0][~pd_bool_col]

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_binop_repeated_application_does_row_identity_joins(scalars_dfs):
    """Make sure row identity joins kick in so that we don't do way more joins than expected."""
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series = scalars_df["int64_col"]
    pd_series = scalars_pandas_df["int64_col"]

    num_joins = 10
    for _ in range(num_joins):
        bf_series = bf_series + bf_series
        pd_series = pd_series + pd_series

    bf_result = bf_series.to_pandas()
    pd_result = pd_series
    assert_series_equal(
        bf_result,
        pd_result,
    )

    bf_sql, _, _ = bf_series.to_frame()._to_sql_query(include_index=True)
    selects = re.findall("SELECT", bf_sql.upper())
    assert 0 < len(selects) < (num_joins // 2)


def test_binop_opposite_filters(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    int64_col1 = scalars_df["int64_col"]
    int64_col2 = scalars_df["int64_col"]
    bool_col = scalars_df["bool_col"]
    bf_result = (int64_col1[bool_col] + int64_col2[bool_col.__invert__()]).to_pandas()

    pd_int64_col1 = scalars_pandas_df["int64_col"]
    pd_int64_col2 = scalars_pandas_df["int64_col"]
    pd_bool_col = scalars_pandas_df["bool_col"]
    pd_result = pd_int64_col1[pd_bool_col] + pd_int64_col2[pd_bool_col.__invert__()]

    # Passes with ignore_order=False only with some dependency sets
    # TODO: Determine desired behavior and make test more strict
    assert_series_equal(bf_result, pd_result, ignore_order=True)


def test_binop_left_filtered(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    int64_col = scalars_df["int64_col"]
    float64_col = scalars_df["float64_col"]
    bool_col = scalars_df["bool_col"]
    bf_result = (int64_col[bool_col] + float64_col).to_pandas()

    pd_int64_col = scalars_pandas_df["int64_col"]
    pd_float64_col = scalars_pandas_df["float64_col"]
    pd_bool_col = scalars_pandas_df["bool_col"]
    pd_result = pd_int64_col[pd_bool_col] + pd_float64_col

    # Passes with ignore_order=False only with some dependency sets
    # TODO: Determine desired behavior and make test more strict
    assert_series_equal(bf_result, pd_result, ignore_order=True)


def test_binop_right_filtered(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    int64_col = scalars_df["int64_col"]
    float64_col = scalars_df["float64_col"]
    bool_col = scalars_df["bool_col"]
    bf_result = (float64_col + int64_col[bool_col]).to_pandas()

    pd_int64_col = scalars_pandas_df["int64_col"]
    pd_float64_col = scalars_pandas_df["float64_col"]
    pd_bool_col = scalars_pandas_df["bool_col"]
    pd_result = pd_float64_col + pd_int64_col[pd_bool_col]

    assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("other",),
    [
        ([-1.4, 2.3, None],),
        (pd.Index([-1.4, 2.3, None]),),
        (pd.Series([-1.4, 2.3, None], index=[44, 2, 1]),),
    ],
)
def test_series_binop_w_other_types(scalars_dfs, other):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (scalars_df["int64_col"].head(3) + other).to_pandas()
    pd_result = scalars_pandas_df["int64_col"].head(3) + other

    assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("other",),
    [
        ([-1.4, 2.3, None],),
        (pd.Index([-1.4, 2.3, None]),),
        (pd.Series([-1.4, 2.3, None], index=[44, 2, 1]),),
    ],
)
def test_series_reverse_binop_w_other_types(scalars_dfs, other):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (other + scalars_df["int64_col"].head(3)).to_pandas()
    pd_result = other + scalars_pandas_df["int64_col"].head(3)

    assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_combine_first(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    int64_col = scalars_df["int64_col"].head(7)
    float64_col = scalars_df["float64_col"].tail(7)
    bf_result = int64_col.combine_first(float64_col).to_pandas()

    pd_int64_col = scalars_pandas_df["int64_col"].head(7)
    pd_float64_col = scalars_pandas_df["float64_col"].tail(7)
    pd_result = pd_int64_col.combine_first(pd_float64_col)

    assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_update(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    int64_col = scalars_df["int64_col"].head(7)
    float64_col = scalars_df["float64_col"].tail(7).copy()
    float64_col.update(int64_col)

    pd_int64_col = scalars_pandas_df["int64_col"].head(7)
    pd_float64_col = scalars_pandas_df["float64_col"].tail(7).copy()
    pd_float64_col.update(pd_int64_col)

    assert_series_equal(
        float64_col.to_pandas(),
        pd_float64_col,
    )


def test_mean(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].mean()
    pd_result = scalars_pandas_df[col_name].mean()
    assert math.isclose(pd_result, bf_result)


def test_median(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].median()
    pd_max = scalars_pandas_df[col_name].max()
    pd_min = scalars_pandas_df[col_name].min()
    # Median is approximate, so just check for plausibility.
    assert pd_min < bf_result < pd_max


def test_median_exact(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].median(exact=True)
    pd_result = scalars_pandas_df[col_name].median()
    assert math.isclose(pd_result, bf_result)


def test_series_quantile(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name]

    pd_result = pd_series.quantile([0.0, 0.4, 0.6, 1.0])
    bf_result = bf_series.quantile([0.0, 0.4, 0.6, 1.0])
    pd.testing.assert_series_equal(
        pd_result, bf_result.to_pandas(), check_dtype=False, check_index_type=False
    )


def test_numeric_literal(scalars_dfs):
    scalars_df, _ = scalars_dfs
    col_name = "numeric_col"
    assert scalars_df[col_name].dtype == pd.ArrowDtype(pa.decimal128(38, 9))
    bf_result = scalars_df[col_name] + 42
    assert bf_result.size == scalars_df[col_name].size
    assert bf_result.dtype == pd.ArrowDtype(pa.decimal128(38, 9))


def test_series_small_repr(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    col_name = "int64_col"
    bf_series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name]
    assert repr(bf_series) == pd_series.to_string(length=False, dtype=True, name=True)


def test_sum(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].sum()
    pd_result = scalars_pandas_df[col_name].sum()
    assert pd_result == bf_result


def test_product(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "float64_col"
    bf_result = scalars_df[col_name].product()
    pd_result = scalars_pandas_df[col_name].product()
    assert math.isclose(pd_result, bf_result)


def test_cumprod(scalars_dfs):
    if pd.__version__.startswith("1."):
        pytest.skip("Series.cumprod NA mask are different in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "float64_col"
    bf_result = scalars_df[col_name].cumprod()
    pd_result = scalars_pandas_df[col_name].cumprod()
    pd.testing.assert_series_equal(
        pd_result,
        bf_result.to_pandas(),
    )


def test_count(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].count()
    pd_result = scalars_pandas_df[col_name].count()
    assert pd_result == bf_result


def test_nunique(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = (scalars_df[col_name] % 3).nunique()
    pd_result = (scalars_pandas_df[col_name] % 3).nunique()
    assert pd_result == bf_result


def test_all(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].all()
    pd_result = scalars_pandas_df[col_name].all()
    assert pd_result == bf_result


def test_any(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    bf_result = scalars_df[col_name].any()
    pd_result = scalars_pandas_df[col_name].any()
    assert pd_result == bf_result


def test_groupby_sum(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = (
        scalars_df[col_name]
        .groupby([scalars_df["bool_col"], ~scalars_df["bool_col"]])
        .sum()
    )
    pd_series = (
        scalars_pandas_df[col_name]
        .groupby([scalars_pandas_df["bool_col"], ~scalars_pandas_df["bool_col"]])
        .sum()
    )
    # TODO(swast): Update groupby to use index based on group by key(s).
    bf_result = bf_series.to_pandas()
    assert_series_equal(
        pd_series,
        bf_result,
        check_exact=False,
    )


def test_groupby_std(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = scalars_df[col_name].groupby(scalars_df["string_col"]).std()
    pd_series = (
        scalars_pandas_df[col_name]
        .groupby(scalars_pandas_df["string_col"])
        .std()
        .astype(pd.Float64Dtype())
    )
    bf_result = bf_series.to_pandas()
    assert_series_equal(
        pd_series,
        bf_result,
        check_exact=False,
    )


def test_groupby_var(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = scalars_df[col_name].groupby(scalars_df["string_col"]).var()
    pd_series = (
        scalars_pandas_df[col_name].groupby(scalars_pandas_df["string_col"]).var()
    )
    bf_result = bf_series.to_pandas()
    assert_series_equal(
        pd_series,
        bf_result,
        check_exact=False,
    )


def test_groupby_level_sum(scalars_dfs):
    # TODO(tbergeron): Use a non-unique index once that becomes possible in tests
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"

    bf_series = scalars_df[col_name].groupby(level=0).sum()
    pd_series = scalars_pandas_df[col_name].groupby(level=0).sum()
    # TODO(swast): Update groupby to use index based on group by key(s).
    pd.testing.assert_series_equal(
        pd_series.sort_index(),
        bf_series.to_pandas().sort_index(),
    )


def test_groupby_level_list_sum(scalars_dfs):
    # TODO(tbergeron): Use a non-unique index once that becomes possible in tests
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"

    bf_series = scalars_df[col_name].groupby(level=["rowindex"]).sum()
    pd_series = scalars_pandas_df[col_name].groupby(level=["rowindex"]).sum()
    # TODO(swast): Update groupby to use index based on group by key(s).
    pd.testing.assert_series_equal(
        pd_series.sort_index(),
        bf_series.to_pandas().sort_index(),
    )


def test_groupby_mean(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = (
        scalars_df[col_name].groupby(scalars_df["string_col"], dropna=False).mean()
    )
    pd_series = (
        scalars_pandas_df[col_name]
        .groupby(scalars_pandas_df["string_col"], dropna=False)
        .mean()
    )
    # TODO(swast): Update groupby to use index based on group by key(s).
    bf_result = bf_series.to_pandas()
    assert_series_equal(
        pd_series,
        bf_result,
    )


def test_groupby_median_exact(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_result = (
        scalars_df[col_name].groupby(scalars_df["string_col"], dropna=False).median()
    )
    pd_result = (
        scalars_pandas_df[col_name]
        .groupby(scalars_pandas_df["string_col"], dropna=False)
        .median()
    )

    assert_series_equal(
        pd_result,
        bf_result.to_pandas(),
    )


def test_groupby_median_inexact(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = (
        scalars_df[col_name]
        .groupby(scalars_df["string_col"], dropna=False)
        .median(exact=False)
    )
    pd_max = (
        scalars_pandas_df[col_name]
        .groupby(scalars_pandas_df["string_col"], dropna=False)
        .max()
    )
    pd_min = (
        scalars_pandas_df[col_name]
        .groupby(scalars_pandas_df["string_col"], dropna=False)
        .min()
    )
    # TODO(swast): Update groupby to use index based on group by key(s).
    bf_result = bf_series.to_pandas()

    # Median is approximate, so just check that it's plausible.
    assert ((pd_min <= bf_result) & (bf_result <= pd_max)).all()


def test_groupby_prod(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = scalars_df[col_name].groupby(scalars_df["int64_col"]).prod()
    pd_series = (
        scalars_pandas_df[col_name].groupby(scalars_pandas_df["int64_col"]).prod()
    ).astype(pd.Float64Dtype())
    # TODO(swast): Update groupby to use index based on group by key(s).
    bf_result = bf_series.to_pandas()
    assert_series_equal(
        pd_series,
        bf_result,
    )


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x: x.cumsum()),
        (lambda x: x.cumcount()),
        (lambda x: x.cummin()),
        (lambda x: x.cummax()),
        # Pandas 2.2 casts to cumprod to float.
        (lambda x: x.cumprod().astype("Float64")),
        (lambda x: x.diff()),
        (lambda x: x.shift(2)),
        (lambda x: x.shift(-2)),
    ],
    ids=[
        "cumsum",
        "cumcount",
        "cummin",
        "cummax",
        "cumprod",
        "diff",
        "shiftpostive",
        "shiftnegative",
    ],
)
def test_groupby_window_ops(scalars_df_index, scalars_pandas_df_index, operator):
    col_name = "int64_col"
    group_key = "int64_too"  # has some duplicates values, good for grouping
    bf_series = (
        operator(scalars_df_index[col_name].groupby(scalars_df_index[group_key]))
    ).to_pandas()
    pd_series = operator(
        scalars_pandas_df_index[col_name].groupby(scalars_pandas_df_index[group_key])
    ).astype(bf_series.dtype)

    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )


@pytest.mark.parametrize(
    ("label", "col_name"),
    [
        (0, "bool_col"),
        (1, "int64_col"),
    ],
)
def test_drop_label(scalars_df_index, scalars_pandas_df_index, label, col_name):
    bf_series = scalars_df_index[col_name].drop(label).to_pandas()
    pd_series = scalars_pandas_df_index[col_name].drop(label)
    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )


def test_drop_label_list(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"
    bf_series = scalars_df_index[col_name].drop([1, 3]).to_pandas()
    pd_series = scalars_pandas_df_index[col_name].drop([1, 3])
    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )


@pytest.mark.parametrize(
    ("col_name",),
    [
        ("bool_col",),
        ("int64_too",),
    ],
)
@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        (False,),
    ],
)
def test_drop_duplicates(scalars_df_index, scalars_pandas_df_index, keep, col_name):
    bf_series = scalars_df_index[col_name].drop_duplicates(keep=keep).to_pandas()
    pd_series = scalars_pandas_df_index[col_name].drop_duplicates(keep=keep)
    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )


@pytest.mark.parametrize(
    ("col_name",),
    [
        ("bool_col",),
        ("int64_too",),
    ],
)
def test_unique(scalars_df_index, scalars_pandas_df_index, col_name):
    bf_uniq = scalars_df_index[col_name].unique().to_numpy(na_value=None)
    pd_uniq = scalars_pandas_df_index[col_name].unique()
    numpy.array_equal(pd_uniq, bf_uniq)


@pytest.mark.parametrize(
    ("col_name",),
    [
        ("bool_col",),
        ("int64_too",),
    ],
)
@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        (False,),
    ],
)
def test_duplicated(scalars_df_index, scalars_pandas_df_index, keep, col_name):
    bf_series = scalars_df_index[col_name].duplicated(keep=keep).to_pandas()
    pd_series = scalars_pandas_df_index[col_name].duplicated(keep=keep)
    pd.testing.assert_series_equal(pd_series, bf_series, check_dtype=False)


def test_shape(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].shape
    pd_result = scalars_pandas_df["string_col"].shape

    assert pd_result == bf_result


def test_len(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = len(scalars_df["string_col"])
    pd_result = len(scalars_pandas_df["string_col"])

    assert pd_result == bf_result


def test_size(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].size
    pd_result = scalars_pandas_df["string_col"].size

    assert pd_result == bf_result


def test_series_hasnans_true(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].hasnans
    pd_result = scalars_pandas_df["string_col"].hasnans

    assert pd_result == bf_result


def test_series_hasnans_false(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].dropna().hasnans
    pd_result = scalars_pandas_df["string_col"].dropna().hasnans

    assert pd_result == bf_result


def test_empty_false(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].empty
    pd_result = scalars_pandas_df["string_col"].empty

    assert pd_result == bf_result


def test_empty_true_row_filter(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"][
        scalars_df["string_col"] == "won't find this"
    ].empty
    pd_result = scalars_pandas_df["string_col"][
        scalars_pandas_df["string_col"] == "won't find this"
    ].empty

    assert pd_result
    assert pd_result == bf_result


def test_series_names(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].copy()
    bf_result.index.name = "new index name"
    bf_result.name = "new series name"

    pd_result = scalars_pandas_df["string_col"].copy()
    pd_result.index.name = "new index name"
    pd_result.name = "new series name"

    assert pd_result.name == bf_result.name
    assert pd_result.index.name == bf_result.index.name


def test_dtype(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].dtype
    pd_result = scalars_pandas_df["string_col"].dtype

    assert pd_result == bf_result


def test_dtypes(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["int64_col"].dtypes
    pd_result = scalars_pandas_df["int64_col"].dtypes

    assert pd_result == bf_result


def test_head(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].head(2).to_pandas()
    pd_result = scalars_pandas_df["string_col"].head(2)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_tail(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["string_col"].tail(2).to_pandas()
    pd_result = scalars_pandas_df["string_col"].tail(2)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_head_then_scalar_operation(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (scalars_df["float64_col"].head(1) + 4).to_pandas()
    pd_result = scalars_pandas_df["float64_col"].head(1) + 4

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_head_then_series_operation(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (
        scalars_df["float64_col"].head(4) + scalars_df["float64_col"].head(2)
    ).to_pandas()
    pd_result = scalars_pandas_df["float64_col"].head(4) + scalars_pandas_df[
        "float64_col"
    ].head(2)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_peek(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    peek_result = scalars_df["float64_col"].peek(n=3, force=False)

    pd.testing.assert_series_equal(
        peek_result,
        scalars_pandas_df["float64_col"].reindex_like(peek_result),
    )
    assert len(peek_result) == 3


def test_series_peek_with_large_results_not_allowed(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    session = scalars_df._block.session
    slot_millis_sum = session.slot_millis_sum
    peek_result = scalars_df["float64_col"].peek(
        n=3, force=False, allow_large_results=False
    )

    # The metrics won't be fully updated when we call query_and_wait.
    print(session.slot_millis_sum - slot_millis_sum)
    assert session.slot_millis_sum - slot_millis_sum < 500
    pd.testing.assert_series_equal(
        peek_result,
        scalars_pandas_df["float64_col"].reindex_like(peek_result),
    )
    assert len(peek_result) == 3


def test_series_peek_multi_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_series = scalars_df.set_index(["string_col", "bool_col"])["float64_col"]
    bf_series.name = ("2-part", "name")
    pd_series = scalars_pandas_df.set_index(["string_col", "bool_col"])["float64_col"]
    pd_series.name = ("2-part", "name")
    peek_result = bf_series.peek(n=3, force=False)
    pd.testing.assert_series_equal(
        peek_result,
        pd_series.reindex_like(peek_result),
    )


def test_series_peek_filtered(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    peek_result = scalars_df[scalars_df.int64_col > 0]["float64_col"].peek(
        n=3, force=False
    )
    pd_result = scalars_pandas_df[scalars_pandas_df.int64_col > 0]["float64_col"]
    pd.testing.assert_series_equal(
        peek_result,
        pd_result.reindex_like(peek_result),
    )


def test_series_peek_force(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    cumsum_df = scalars_df[["int64_col", "int64_too"]].cumsum()
    df_filtered = cumsum_df[cumsum_df.int64_col > 0]["int64_too"]
    peek_result = df_filtered.peek(n=3, force=True)
    pd_cumsum_df = scalars_pandas_df[["int64_col", "int64_too"]].cumsum()
    pd_result = pd_cumsum_df[pd_cumsum_df.int64_col > 0]["int64_too"]
    pd.testing.assert_series_equal(
        peek_result,
        pd_result.reindex_like(peek_result),
    )


def test_series_peek_force_float(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    cumsum_df = scalars_df[["int64_col", "float64_col"]].cumsum()
    df_filtered = cumsum_df[cumsum_df.float64_col > 0]["float64_col"]
    peek_result = df_filtered.peek(n=3, force=True)
    pd_cumsum_df = scalars_pandas_df[["int64_col", "float64_col"]].cumsum()
    pd_result = pd_cumsum_df[pd_cumsum_df.float64_col > 0]["float64_col"]
    pd.testing.assert_series_equal(
        peek_result,
        pd_result.reindex_like(peek_result),
    )


def test_shift(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"
    bf_result = scalars_df_index[col_name].shift().to_pandas()
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = scalars_pandas_df_index[col_name].shift().astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_ffill(scalars_df_index, scalars_pandas_df_index):
    col_name = "numeric_col"
    bf_result = scalars_df_index[col_name].ffill(limit=1).to_pandas()
    pd_result = scalars_pandas_df_index[col_name].ffill(limit=1)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_bfill(scalars_df_index, scalars_pandas_df_index):
    col_name = "numeric_col"
    bf_result = scalars_df_index[col_name].bfill(limit=2).to_pandas()
    pd_result = scalars_pandas_df_index[col_name].bfill(limit=2)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cumsum_int(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("1."):
        pytest.skip("Series.cumsum NA mask are different in pandas 1.x.")

    col_name = "int64_col"
    bf_result = scalars_df_index[col_name].cumsum().to_pandas()
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = scalars_pandas_df_index[col_name].cumsum().astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cumsum_int_ordered(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("1."):
        pytest.skip("Series.cumsum NA mask are different in pandas 1.x.")

    col_name = "int64_col"
    bf_result = (
        scalars_df_index.sort_values(by="rowindex_2")[col_name].cumsum().to_pandas()
    )
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = (
        scalars_pandas_df_index.sort_values(by="rowindex_2")[col_name]
        .cumsum()
        .astype(pd.Int64Dtype())
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        ("all",),
    ],
)
def test_series_nlargest(scalars_df_index, scalars_pandas_df_index, keep):
    col_name = "bool_col"
    bf_result = scalars_df_index[col_name].nlargest(4, keep=keep).to_pandas()
    pd_result = scalars_pandas_df_index[col_name].nlargest(4, keep=keep)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("periods",),
    [
        (1,),
        (2,),
        (-1,),
    ],
)
def test_diff(scalars_df_index, scalars_pandas_df_index, periods):
    bf_result = scalars_df_index["int64_col"].diff(periods=periods).to_pandas()
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = (
        scalars_pandas_df_index["int64_col"]
        .diff(periods=periods)
        .astype(pd.Int64Dtype())
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("periods",),
    [
        (1,),
        (2,),
        (-1,),
    ],
)
def test_series_pct_change(scalars_df_index, scalars_pandas_df_index, periods):
    bf_result = scalars_df_index["int64_col"].pct_change(periods=periods).to_pandas()
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = scalars_pandas_df_index["int64_col"].pct_change(periods=periods)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        ("all",),
    ],
)
def test_series_nsmallest(scalars_df_index, scalars_pandas_df_index, keep):
    col_name = "bool_col"
    bf_result = scalars_df_index[col_name].nsmallest(2, keep=keep).to_pandas()
    pd_result = scalars_pandas_df_index[col_name].nsmallest(2, keep=keep)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_rank_ints(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_too"
    bf_result = scalars_df_index[col_name].rank().to_pandas()
    pd_result = scalars_pandas_df_index[col_name].rank().astype(pd.Float64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cast_float_to_int(scalars_df_index, scalars_pandas_df_index):
    col_name = "float64_col"
    bf_result = scalars_df_index[col_name].astype(pd.Int64Dtype()).to_pandas()
    # cumsum does not behave well on nullable floats in pandas, produces object type and never ignores NA
    pd_result = scalars_pandas_df_index[col_name].astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cast_float_to_bool(scalars_df_index, scalars_pandas_df_index):
    col_name = "float64_col"
    bf_result = scalars_df_index[col_name].astype(pd.BooleanDtype()).to_pandas()
    # cumsum does not behave well on nullable floats in pandas, produces object type and never ignores NA
    pd_result = scalars_pandas_df_index[col_name].astype(pd.BooleanDtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cumsum_nested(scalars_df_index, scalars_pandas_df_index):
    col_name = "float64_col"
    bf_result = scalars_df_index[col_name].cumsum().cumsum().cumsum().to_pandas()
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = (
        scalars_pandas_df_index[col_name]
        .cumsum()
        .cumsum()
        .cumsum()
        .astype(pd.Float64Dtype())
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_nested_analytic_ops_align(scalars_df_index, scalars_pandas_df_index):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    col_name = "float64_col"
    # set non-unique index to check implicit alignment
    bf_series = scalars_df_index.set_index("bool_col")[col_name].fillna(0.0)
    pd_series = scalars_pandas_df_index.set_index("bool_col")[col_name].fillna(0.0)

    bf_result = (
        (bf_series + 5)
        + (bf_series.cumsum().cumsum().cumsum() + bf_series.rolling(window=3).mean())
        + bf_series.expanding().max()
    ).to_pandas()
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = (
        (pd_series + 5)
        + (
            pd_series.cumsum().cumsum().cumsum().astype(pd.Float64Dtype())
            + pd_series.rolling(window=3).mean()
        )
        + pd_series.expanding().max()
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cumsum_int_filtered(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"

    bf_col = scalars_df_index[col_name]
    bf_result = bf_col[bf_col > -2].cumsum().to_pandas()

    pd_col = scalars_pandas_df_index[col_name]
    # cumsum does not behave well on nullable ints in pandas, produces object type and never ignores NA
    pd_result = pd_col[pd_col > -2].cumsum().astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cumsum_float(scalars_df_index, scalars_pandas_df_index):
    col_name = "float64_col"
    bf_result = scalars_df_index[col_name].cumsum().to_pandas()
    # cumsum does not behave well on nullable floats in pandas, produces object type and never ignores NA
    pd_result = scalars_pandas_df_index[col_name].cumsum().astype(pd.Float64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cummin_int(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"
    bf_result = scalars_df_index[col_name].cummin().to_pandas()
    pd_result = scalars_pandas_df_index[col_name].cummin()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_cummax_int(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"
    bf_result = scalars_df_index[col_name].cummax().to_pandas()
    pd_result = scalars_pandas_df_index[col_name].cummax()

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("kwargs"),
    [
        {},
        {"normalize": True},
        {"ascending": True},
    ],
    ids=[
        "default",
        "normalize",
        "ascending",
    ],
)
def test_value_counts(scalars_dfs, kwargs):
    if pd.__version__.startswith("1."):
        pytest.skip("pandas 1.x produces different column labels.")
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"

    # Pandas `value_counts` can produce non-deterministic results with tied counts.
    # Remove duplicates to enforce a consistent output.
    s = scalars_df[col_name].drop(0)
    pd_s = scalars_pandas_df[col_name].drop(0)

    bf_result = s.value_counts(**kwargs).to_pandas()
    pd_result = pd_s.value_counts(**kwargs)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_value_counts_with_na(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"

    bf_result = scalars_df[col_name].value_counts(dropna=False).to_pandas()
    pd_result = scalars_pandas_df[col_name].value_counts(dropna=False)

    # Older pandas version may not have these values, bigframes tries to emulate 2.0+
    pd_result.name = "count"
    pd_result.index.name = col_name

    assert_series_equal(
        bf_result,
        pd_result,
        # bigframes values_counts does not honor ordering in the original data
        ignore_order=True,
    )


def test_value_counts_w_cut(scalars_dfs):
    if pd.__version__.startswith("1."):
        pytest.skip("value_counts results different in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"

    bf_cut = bigframes.pandas.cut(scalars_df[col_name], 3, labels=False)
    pd_cut = pd.cut(scalars_pandas_df[col_name], 3, labels=False)

    bf_result = bf_cut.value_counts().to_pandas()
    pd_result = pd_cut.value_counts()
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.Int64Dtype()),
    )


def test_iloc_nested(scalars_df_index, scalars_pandas_df_index):

    bf_result = scalars_df_index["string_col"].iloc[1:].iloc[1:].to_pandas()
    pd_result = scalars_pandas_df_index["string_col"].iloc[1:].iloc[1:]

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("start", "stop", "step"),
    [
        (1, None, None),
        (None, 4, None),
        (None, None, 2),
        (None, 50000000000, 1),
        (5, 4, None),
        (3, None, 2),
        (1, 7, 2),
        (1, 7, 50000000000),
        (-1, -7, -2),
        (None, -7, -2),
        (-1, None, -2),
        (-7, -1, 2),
        (-7, -1, None),
        (-7, 7, None),
        (7, -7, -2),
    ],
)
def test_series_iloc(scalars_df_index, scalars_pandas_df_index, start, stop, step):
    bf_result = scalars_df_index["string_col"].iloc[start:stop:step].to_pandas()
    pd_result = scalars_pandas_df_index["string_col"].iloc[start:stop:step]
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_at(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("int64_too", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("int64_too", drop=False)
    index = -2345
    bf_result = scalars_df_index["string_col"].at[index]
    pd_result = scalars_pandas_df_index["string_col"].at[index]

    assert bf_result == pd_result


def test_iat(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].iat[3]
    pd_result = scalars_pandas_df_index["int64_too"].iat[3]

    assert bf_result == pd_result


def test_iat_error(scalars_df_index, scalars_pandas_df_index):
    with pytest.raises(ValueError):
        scalars_pandas_df_index["int64_too"].iat["asd"]
    with pytest.raises(ValueError):
        scalars_df_index["int64_too"].iat["asd"]


def test_series_add_prefix(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].add_prefix("prefix_").to_pandas()

    pd_result = scalars_pandas_df_index["int64_too"].add_prefix("prefix_")

    # Index will be object type in pandas, string type in bigframes, but same values
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_index_type=False,
    )


def test_series_add_suffix(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].add_suffix("_suffix").to_pandas()

    pd_result = scalars_pandas_df_index["int64_too"].add_suffix("_suffix")

    # Index will be object type in pandas, string type in bigframes, but same values
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_index_type=False,
    )


def test_series_filter_items(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("2.0") or pd.__version__.startswith("1."):
        pytest.skip("pandas filter items behavior different pre-2.1")
    bf_result = scalars_df_index["float64_col"].filter(items=[5, 1, 3]).to_pandas()

    pd_result = scalars_pandas_df_index["float64_col"].filter(items=[5, 1, 3])

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    # Ignore ordering as pandas order differently depending on version
    assert_series_equal(bf_result, pd_result, check_names=False, ignore_order=True)


def test_series_filter_like(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.copy().set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.copy().set_index("string_col")

    bf_result = scalars_df_index["float64_col"].filter(like="ello").to_pandas()

    pd_result = scalars_pandas_df_index["float64_col"].filter(like="ello")

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_filter_regex(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.copy().set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.copy().set_index("string_col")

    bf_result = scalars_df_index["float64_col"].filter(regex="^[GH].*").to_pandas()

    pd_result = scalars_pandas_df_index["float64_col"].filter(regex="^[GH].*")

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_reindex(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["float64_col"].reindex(index=[5, 1, 3, 99, 1]).to_pandas()
    )

    pd_result = scalars_pandas_df_index["float64_col"].reindex(index=[5, 1, 3, 99, 1])

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_reindex_nonunique(scalars_df_index):
    with pytest.raises(ValueError):
        # int64_too is non-unique
        scalars_df_index.set_index("int64_too")["float64_col"].reindex(
            index=[5, 1, 3, 99, 1], validate=True
        )


def test_series_reindex_like(scalars_df_index, scalars_pandas_df_index):
    bf_reindex_target = scalars_df_index["float64_col"].reindex(index=[5, 1, 3, 99, 1])
    bf_result = (
        scalars_df_index["int64_too"].reindex_like(bf_reindex_target).to_pandas()
    )

    pd_reindex_target = scalars_pandas_df_index["float64_col"].reindex(
        index=[5, 1, 3, 99, 1]
    )
    pd_result = scalars_pandas_df_index["int64_too"].reindex_like(pd_reindex_target)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_where_with_series(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["int64_col"]
        .where(scalars_df_index["bool_col"], scalars_df_index["int64_too"])
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_col"].where(
        scalars_pandas_df_index["bool_col"], scalars_pandas_df_index["int64_too"]
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_where_with_different_indices(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["int64_col"]
        .iloc[::2]
        .where(
            scalars_df_index["bool_col"].iloc[2:],
            scalars_df_index["int64_too"].iloc[:5],
        )
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index["int64_col"]
        .iloc[::2]
        .where(
            scalars_pandas_df_index["bool_col"].iloc[2:],
            scalars_pandas_df_index["int64_too"].iloc[:5],
        )
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_where_with_default(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["int64_col"].where(scalars_df_index["bool_col"]).to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_col"].where(
        scalars_pandas_df_index["bool_col"]
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_clip(scalars_df_index, scalars_pandas_df_index, ordered):
    col_bf = scalars_df_index["int64_col"]
    lower_bf = scalars_df_index["int64_too"] - 1
    upper_bf = scalars_df_index["int64_too"] + 1
    bf_result = col_bf.clip(lower_bf, upper_bf).to_pandas(ordered=ordered)

    col_pd = scalars_pandas_df_index["int64_col"]
    lower_pd = scalars_pandas_df_index["int64_too"] - 1
    upper_pd = scalars_pandas_df_index["int64_too"] + 1
    pd_result = col_pd.clip(lower_pd, upper_pd)

    assert_series_equal(bf_result, pd_result, ignore_order=not ordered)


def test_clip_int_with_float_bounds(scalars_df_index, scalars_pandas_df_index):
    col_bf = scalars_df_index["int64_too"]
    bf_result = col_bf.clip(-100, 3.14151593).to_pandas()

    col_pd = scalars_pandas_df_index["int64_too"]
    # pandas doesn't work with Int64 and clip with floats
    pd_result = col_pd.astype("int64").clip(-100, 3.14151593).astype("Float64")

    assert_series_equal(bf_result, pd_result)


def test_clip_filtered_two_sided(scalars_df_index, scalars_pandas_df_index):
    col_bf = scalars_df_index["int64_col"].iloc[::2]
    lower_bf = scalars_df_index["int64_too"].iloc[2:] - 1
    upper_bf = scalars_df_index["int64_too"].iloc[:5] + 1
    bf_result = col_bf.clip(lower_bf, upper_bf).to_pandas()

    col_pd = scalars_pandas_df_index["int64_col"].iloc[::2]
    lower_pd = scalars_pandas_df_index["int64_too"].iloc[2:] - 1
    upper_pd = scalars_pandas_df_index["int64_too"].iloc[:5] + 1
    pd_result = col_pd.clip(lower_pd, upper_pd)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_clip_filtered_one_sided(scalars_df_index, scalars_pandas_df_index):
    col_bf = scalars_df_index["int64_col"].iloc[::2]
    lower_bf = scalars_df_index["int64_too"].iloc[2:] - 1
    bf_result = col_bf.clip(lower_bf, None).to_pandas()

    col_pd = scalars_pandas_df_index["int64_col"].iloc[::2]
    lower_pd = scalars_pandas_df_index["int64_too"].iloc[2:] - 1
    pd_result = col_pd.clip(lower_pd, None)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_dot(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_too"] @ scalars_df["int64_too"]

    pd_result = scalars_pandas_df["int64_too"] @ scalars_pandas_df["int64_too"]

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("left", "right", "inclusive"),
    [
        (-234892, 55555, "left"),
        (-234892, 55555, "both"),
        (-234892, 55555, "neither"),
        (-234892, 55555, "right"),
    ],
)
def test_between(scalars_df_index, scalars_pandas_df_index, left, right, inclusive):
    bf_result = (
        scalars_df_index["int64_col"].between(left, right, inclusive).to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_col"].between(left, right, inclusive)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.BooleanDtype()),
    )


def test_series_case_when(scalars_dfs_maybe_ordered):
    pytest.importorskip(
        "pandas",
        minversion="2.2.0",
        reason="case_when added in pandas 2.2.0",
    )
    scalars_df, scalars_pandas_df = scalars_dfs_maybe_ordered

    bf_series = scalars_df["int64_col"]
    pd_series = scalars_pandas_df["int64_col"]

    # TODO(tswast): pandas case_when appears to assume True when a value is
    # null. I suspect this should be considered a bug in pandas.

    # Generate 150 conditions to test case_when with a large number of conditions
    bf_conditions = (
        [((bf_series > 645).fillna(True), bf_series - 1)]
        + [((bf_series > (-100 + i * 5)).fillna(True), i) for i in range(148, 0, -1)]
        + [((bf_series <= -100).fillna(True), pd.NA)]
    )

    pd_conditions = (
        [((pd_series > 645), pd_series - 1)]
        + [((pd_series > (-100 + i * 5)), i) for i in range(148, 0, -1)]
        + [(pd_series <= -100, pd.NA)]
    )

    assert len(bf_conditions) == 150

    bf_result = bf_series.case_when(bf_conditions).to_pandas()
    pd_result = pd_series.case_when(pd_conditions)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype(pd.Int64Dtype()),
    )


def test_series_case_when_change_type(scalars_dfs_maybe_ordered):
    pytest.importorskip(
        "pandas",
        minversion="2.2.0",
        reason="case_when added in pandas 2.2.0",
    )
    scalars_df, scalars_pandas_df = scalars_dfs_maybe_ordered

    bf_series = scalars_df["int64_col"]
    pd_series = scalars_pandas_df["int64_col"]

    # TODO(tswast): pandas case_when appears to assume True when a value is
    # null. I suspect this should be considered a bug in pandas.

    bf_conditions = [
        ((bf_series > 645).fillna(True), scalars_df["string_col"]),
        ((bf_series <= -100).fillna(True), pd.NA),
        (True, "not_found"),
    ]

    pd_conditions = [
        ((pd_series > 645).fillna(True), scalars_pandas_df["string_col"]),
        ((pd_series <= -100).fillna(True), pd.NA),
        # pandas currently fails if both the condition and the value are literals.
        ([True] * len(pd_series), ["not_found"] * len(pd_series)),
    ]

    bf_result = bf_series.case_when(bf_conditions).to_pandas()
    pd_result = pd_series.case_when(pd_conditions)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result.astype("string[pyarrow]"),
    )


def test_to_frame(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["int64_col"].to_frame().to_pandas()
    pd_result = scalars_pandas_df["int64_col"].to_frame()

    assert_pandas_df_equal(bf_result, pd_result)


def test_to_frame_no_name(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["int64_col"].rename(None).to_frame().to_pandas()
    pd_result = scalars_pandas_df["int64_col"].rename(None).to_frame()

    assert_pandas_df_equal(bf_result, pd_result)


def test_to_json(gcs_folder, scalars_df_index, scalars_pandas_df_index):
    path = gcs_folder + "test_series_to_json*.jsonl"
    scalars_df_index["int64_col"].to_json(path, lines=True, orient="records")
    gcs_df = pd.read_json(get_first_file_from_wildcard(path), lines=True)

    pd.testing.assert_series_equal(
        gcs_df["int64_col"].astype(pd.Int64Dtype()),
        scalars_pandas_df_index["int64_col"],
        check_dtype=False,
        check_index=False,
    )


def test_to_csv(gcs_folder, scalars_df_index, scalars_pandas_df_index):
    path = gcs_folder + "test_series_to_csv*.csv"
    scalars_df_index["int64_col"].to_csv(path)
    gcs_df = pd.read_csv(get_first_file_from_wildcard(path))

    pd.testing.assert_series_equal(
        gcs_df["int64_col"].astype(pd.Int64Dtype()),
        scalars_pandas_df_index["int64_col"],
        check_dtype=False,
        check_index=False,
    )


def test_to_latex(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].to_latex()
    pd_result = scalars_pandas_df_index["int64_col"].to_latex()

    assert bf_result == pd_result


def test_series_to_json_local_str(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.int64_col.to_json()
    pd_result = scalars_pandas_df_index.int64_col.to_json()

    assert bf_result == pd_result


def test_series_to_json_local_file(scalars_df_index, scalars_pandas_df_index):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    with tempfile.TemporaryFile() as bf_result_file, tempfile.TemporaryFile() as pd_result_file:
        scalars_df_index.int64_col.to_json(bf_result_file)
        scalars_pandas_df_index.int64_col.to_json(pd_result_file)

        bf_result = bf_result_file.read()
        pd_result = pd_result_file.read()

    assert bf_result == pd_result


def test_series_to_csv_local_str(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.int64_col.to_csv()
    # default_handler for arrow types that have no default conversion
    pd_result = scalars_pandas_df_index.int64_col.to_csv()

    assert bf_result == pd_result


def test_series_to_csv_local_file(scalars_df_index, scalars_pandas_df_index):
    with tempfile.TemporaryFile() as bf_result_file, tempfile.TemporaryFile() as pd_result_file:
        scalars_df_index.int64_col.to_csv(bf_result_file)
        scalars_pandas_df_index.int64_col.to_csv(pd_result_file)

        bf_result = bf_result_file.read()
        pd_result = pd_result_file.read()

    assert bf_result == pd_result


def test_to_dict(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].to_dict()

    pd_result = scalars_pandas_df_index["int64_too"].to_dict()

    assert bf_result == pd_result


def test_to_excel(scalars_df_index, scalars_pandas_df_index):
    bf_result_file = tempfile.TemporaryFile()
    pd_result_file = tempfile.TemporaryFile()
    scalars_df_index["int64_too"].to_excel(bf_result_file)
    scalars_pandas_df_index["int64_too"].to_excel(pd_result_file)
    bf_result = bf_result_file.read()
    pd_result = bf_result_file.read()

    assert bf_result == pd_result


def test_to_pickle(scalars_df_index, scalars_pandas_df_index):
    bf_result_file = tempfile.TemporaryFile()
    pd_result_file = tempfile.TemporaryFile()
    scalars_df_index["int64_too"].to_pickle(bf_result_file)
    scalars_pandas_df_index["int64_too"].to_pickle(pd_result_file)
    bf_result = bf_result_file.read()
    pd_result = bf_result_file.read()

    assert bf_result == pd_result


def test_to_string(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].to_string()

    pd_result = scalars_pandas_df_index["int64_too"].to_string()

    assert bf_result == pd_result


def test_to_list(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].to_list()

    pd_result = scalars_pandas_df_index["int64_too"].to_list()

    assert bf_result == pd_result


def test_to_numpy(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].to_numpy()

    pd_result = scalars_pandas_df_index["int64_too"].to_numpy()

    assert (bf_result == pd_result).all()


def test_to_xarray(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].to_xarray()

    pd_result = scalars_pandas_df_index["int64_too"].to_xarray()

    assert bf_result.equals(pd_result)


def test_to_markdown(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].to_markdown()

    pd_result = scalars_pandas_df_index["int64_too"].to_markdown()

    assert bf_result == pd_result


def test_series_values(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_too"].values

    pd_result = scalars_pandas_df_index["int64_too"].values
    # Numpy isn't equipped to compare non-numeric objects, so convert back to dataframe
    pd.testing.assert_series_equal(
        pd.Series(bf_result), pd.Series(pd_result), check_dtype=False
    )


def test_series___array__(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["float64_col"].__array__()

    pd_result = scalars_pandas_df_index["float64_col"].__array__()
    # Numpy isn't equipped to compare non-numeric objects, so convert back to dataframe
    numpy.array_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("ascending", "na_position"),
    [
        (True, "first"),
        (True, "last"),
        (False, "first"),
        (False, "last"),
    ],
)
def test_sort_values(scalars_df_index, scalars_pandas_df_index, ascending, na_position):
    # Test needs values to be unique
    bf_result = (
        scalars_df_index["int64_col"]
        .sort_values(ascending=ascending, na_position=na_position)
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_col"].sort_values(
        ascending=ascending, na_position=na_position
    )

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_sort_values_inplace(scalars_df_index, scalars_pandas_df_index):
    # Test needs values to be unique
    bf_series = scalars_df_index["int64_col"].copy()
    bf_series.sort_values(ascending=False, inplace=True)
    bf_result = bf_series.to_pandas()
    pd_result = scalars_pandas_df_index["int64_col"].sort_values(ascending=False)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("ascending"),
    [
        (True,),
        (False,),
    ],
)
def test_sort_index(scalars_df_index, scalars_pandas_df_index, ascending):
    bf_result = (
        scalars_df_index["int64_too"].sort_index(ascending=ascending).to_pandas()
    )
    pd_result = scalars_pandas_df_index["int64_too"].sort_index(ascending=ascending)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_series_sort_index_inplace(scalars_df_index, scalars_pandas_df_index):
    bf_series = scalars_df_index["int64_too"].copy()
    bf_series.sort_index(ascending=False, inplace=True)
    bf_result = bf_series.to_pandas()
    pd_result = scalars_pandas_df_index["int64_too"].sort_index(ascending=False)

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_mask_default_value(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df["int64_col"]
    bf_col_masked = bf_col.mask(bf_col % 2 == 1)
    bf_result = bf_col.to_frame().assign(int64_col_masked=bf_col_masked).to_pandas()

    pd_col = scalars_pandas_df["int64_col"]
    pd_col_masked = pd_col.mask(pd_col % 2 == 1)
    pd_result = pd_col.to_frame().assign(int64_col_masked=pd_col_masked)

    assert_pandas_df_equal(bf_result, pd_result)


def test_mask_custom_value(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df["int64_col"]
    bf_col_masked = bf_col.mask(bf_col % 2 == 1, -1)
    bf_result = bf_col.to_frame().assign(int64_col_masked=bf_col_masked).to_pandas()

    pd_col = scalars_pandas_df["int64_col"]
    pd_col_masked = pd_col.mask(pd_col % 2 == 1, -1)
    pd_result = pd_col.to_frame().assign(int64_col_masked=pd_col_masked)

    # TODO(shobs): There is a pd.NA value in the original series, which is not
    # odd so should be left as is, but it is being masked in pandas.
    # Accidentally the bigframes bahavior matches, but it should be updated
    # after the resolution of https://github.com/pandas-dev/pandas/issues/52955
    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("lambda_",),
    [
        pytest.param(lambda x: x > 0),
        pytest.param(
            lambda x: True if x > 0 else False,
            marks=pytest.mark.xfail(
                raises=ValueError,
            ),
        ),
    ],
    ids=[
        "lambda_arithmatic",
        "lambda_arbitrary",
    ],
)
def test_mask_lambda(scalars_dfs, lambda_):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df["int64_col"]
    bf_result = bf_col.mask(lambda_).to_pandas()

    pd_col = scalars_pandas_df["int64_col"]
    pd_result = pd_col.mask(lambda_)

    # ignore dtype check, which are Int64 and object respectively
    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_mask_simple_udf(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    def foo(x):
        return x < 1000000

    bf_col = scalars_df["int64_col"]
    bf_result = bf_col.mask(foo).to_pandas()

    pd_col = scalars_pandas_df["int64_col"]
    pd_result = pd_col.mask(foo)

    # ignore dtype check, which are Int64 and object respectively
    assert_series_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize("errors", ["raise", "null"])
@pytest.mark.parametrize(
    ("column", "to_type"),
    [
        ("int64_col", "Float64"),
        ("int64_col", "Int64"),  # No-op
        ("int64_col", pd.Float64Dtype()),
        ("int64_col", "string[pyarrow]"),
        ("int64_col", "boolean"),
        ("int64_col", pd.ArrowDtype(pa.decimal128(38, 9))),
        ("int64_col", pd.ArrowDtype(pa.decimal256(76, 38))),
        ("int64_col", pd.ArrowDtype(pa.timestamp("us"))),
        ("int64_col", pd.ArrowDtype(pa.timestamp("us", tz="UTC"))),
        ("int64_col", "time64[us][pyarrow]"),
        ("int64_col", pd.ArrowDtype(db_dtypes.JSONArrowType())),
        ("bool_col", "Int64"),
        ("bool_col", "string[pyarrow]"),
        ("bool_col", "Float64"),
        ("bool_col", pd.ArrowDtype(db_dtypes.JSONArrowType())),
        ("string_col", "binary[pyarrow]"),
        ("bytes_col", "string[pyarrow]"),
        # pandas actually doesn't let folks convert to/from naive timestamp and
        # raises a deprecation warning to use tz_localize/tz_convert instead,
        # but BigQuery always stores values as UTC and doesn't have to deal
        # with timezone conversions, so we'll allow it.
        ("timestamp_col", "date32[day][pyarrow]"),
        ("timestamp_col", "time64[us][pyarrow]"),
        ("timestamp_col", pd.ArrowDtype(pa.timestamp("us"))),
        ("datetime_col", "date32[day][pyarrow]"),
        pytest.param(
            "datetime_col",
            "string[pyarrow]",
            marks=pytest.mark.skipif(
                pd.__version__.startswith("2.2"),
                reason="pandas 2.2 uses T as date/time separator whereas earlier versions use space",
            ),
        ),
        ("datetime_col", "time64[us][pyarrow]"),
        ("datetime_col", pd.ArrowDtype(pa.timestamp("us", tz="UTC"))),
        ("date_col", "string[pyarrow]"),
        ("date_col", pd.ArrowDtype(pa.timestamp("us"))),
        ("date_col", pd.ArrowDtype(pa.timestamp("us", tz="UTC"))),
        ("time_col", "string[pyarrow]"),
        # TODO(bmil): fix Ibis bug: BigQuery backend rounds to nearest int
        # ("float64_col", "Int64"),
        # TODO(bmil): decide whether to fix Ibis bug: BigQuery backend
        # formats floats with no decimal places if they have no fractional
        # part, and does not switch to scientific notation for > 10^15
        # ("float64_col", "string[pyarrow]")
        # TODO(bmil): add any other compatible conversions per
        # https://cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions
    ],
)
def test_astype(scalars_df_index, scalars_pandas_df_index, column, to_type, errors):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    bf_result = scalars_df_index[column].astype(to_type, errors=errors).to_pandas()
    pd_result = scalars_pandas_df_index[column].astype(to_type)
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_astype_python(session):
    input = pd.Series(["hello", "world", "3.11", "4000"])
    exepcted = pd.Series(
        [None, None, 3.11, 4000],
        dtype="Float64",
        index=pd.Index([0, 1, 2, 3], dtype="Int64"),
    )
    result = session.read_pandas(input).astype(float, errors="null").to_pandas()
    pd.testing.assert_series_equal(result, exepcted)


def test_astype_safe(session):
    input = pd.Series(["hello", "world", "3.11", "4000"])
    exepcted = pd.Series(
        [None, None, 3.11, 4000],
        dtype="Float64",
        index=pd.Index([0, 1, 2, 3], dtype="Int64"),
    )
    result = session.read_pandas(input).astype("Float64", errors="null").to_pandas()
    pd.testing.assert_series_equal(result, exepcted)


def test_series_astype_w_invalid_error(session):
    input = pd.Series(["hello", "world", "3.11", "4000"])
    with pytest.raises(ValueError):
        session.read_pandas(input).astype("Float64", errors="bad_value")


def test_astype_numeric_to_int(scalars_df_index, scalars_pandas_df_index):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    column = "numeric_col"
    to_type = "Int64"
    bf_result = scalars_df_index[column].astype(to_type).to_pandas()
    # Round to the nearest whole number to avoid TypeError
    pd_result = scalars_pandas_df_index[column].round(0).astype(to_type)
    pd.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("column", "to_type"),
    [
        ("timestamp_col", "int64[pyarrow]"),
        ("datetime_col", "int64[pyarrow]"),
        ("time_col", "int64[pyarrow]"),
    ],
)
def test_date_time_astype_int(
    scalars_df_index, scalars_pandas_df_index, column, to_type
):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    bf_result = scalars_df_index[column].astype(to_type).to_pandas()
    pd_result = scalars_pandas_df_index[column].astype(to_type)
    pd.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)
    assert bf_result.dtype == "Int64"


def test_string_astype_int():
    pd_series = pd.Series(["4", "-7", "0", "    -03"])
    bf_series = series.Series(pd_series)

    pd_result = pd_series.astype("Int64")
    bf_result = bf_series.astype("Int64").to_pandas()

    pd.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_string_astype_float():
    pd_series = pd.Series(
        ["1", "-1", "-0", "000", "    -03.235", "naN", "-inf", "INf", ".33", "7.235e-8"]
    )

    bf_series = series.Series(pd_series)

    pd_result = pd_series.astype("Float64")
    bf_result = bf_series.astype("Float64").to_pandas()

    pd.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_string_astype_date():
    if int(pa.__version__.split(".")[0]) < 15:
        pytest.skip(
            "Avoid pyarrow.lib.ArrowNotImplementedError: "
            "Unsupported cast from string to date32 using function cast_date32."
        )

    pd_series = pd.Series(["2014-08-15", "2215-08-15", "2016-02-29"]).astype(
        pd.ArrowDtype(pa.string())
    )

    bf_series = series.Series(pd_series)

    # TODO(b/340885567): fix type error
    pd_result = pd_series.astype("date32[day][pyarrow]")  # type: ignore
    bf_result = bf_series.astype("date32[day][pyarrow]").to_pandas()

    pd.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_string_astype_datetime():
    pd_series = pd.Series(
        ["2014-08-15 08:15:12", "2015-08-15 08:15:12.654754", "2016-02-29 00:00:00"]
    ).astype(pd.ArrowDtype(pa.string()))

    bf_series = series.Series(pd_series)

    pd_result = pd_series.astype(pd.ArrowDtype(pa.timestamp("us")))
    bf_result = bf_series.astype(pd.ArrowDtype(pa.timestamp("us"))).to_pandas()

    pd.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_string_astype_timestamp():
    pd_series = pd.Series(
        [
            "2014-08-15 08:15:12+00:00",
            "2015-08-15 08:15:12.654754+05:00",
            "2016-02-29 00:00:00+08:00",
        ]
    ).astype(pd.ArrowDtype(pa.string()))

    bf_series = series.Series(pd_series)

    pd_result = pd_series.astype(pd.ArrowDtype(pa.timestamp("us", tz="UTC")))
    bf_result = bf_series.astype(
        pd.ArrowDtype(pa.timestamp("us", tz="UTC"))
    ).to_pandas()

    pd.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_timestamp_astype_string():
    bf_series = series.Series(
        [
            "2014-08-15 08:15:12+00:00",
            "2015-08-15 08:15:12.654754+05:00",
            "2016-02-29 00:00:00+08:00",
        ]
    ).astype(pd.ArrowDtype(pa.timestamp("us", tz="UTC")))

    expected_result = pd.Series(
        [
            "2014-08-15 08:15:12+00",
            "2015-08-15 03:15:12.654754+00",
            "2016-02-28 16:00:00+00",
        ]
    )
    bf_result = bf_series.astype(pa.string()).to_pandas()

    pd.testing.assert_series_equal(
        bf_result, expected_result, check_index_type=False, check_dtype=False
    )
    assert bf_result.dtype == "string[pyarrow]"


@pytest.mark.parametrize("errors", ["raise", "null"])
def test_float_astype_json(errors):
    data = ["1.25", "2500000000", None, "-12323.24"]
    bf_series = series.Series(data, dtype=dtypes.FLOAT_DTYPE)

    bf_result = bf_series.astype(dtypes.JSON_DTYPE, errors=errors)
    assert bf_result.dtype == dtypes.JSON_DTYPE

    expected_result = pd.Series(data, dtype=dtypes.JSON_DTYPE)
    expected_result.index = expected_result.index.astype("Int64")
    pd.testing.assert_series_equal(bf_result.to_pandas(), expected_result)


@pytest.mark.parametrize("errors", ["raise", "null"])
def test_string_astype_json(errors):
    data = [
        "1",
        None,
        '["1","3","5"]',
        '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}',
    ]
    bf_series = series.Series(data, dtype=dtypes.STRING_DTYPE)

    bf_result = bf_series.astype(dtypes.JSON_DTYPE, errors=errors)
    assert bf_result.dtype == dtypes.JSON_DTYPE

    pd_result = bf_series.to_pandas().astype(dtypes.JSON_DTYPE)
    pd.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


def test_string_astype_json_in_safe_mode():
    data = ["this is not a valid json string"]
    bf_series = series.Series(data, dtype=dtypes.STRING_DTYPE)
    bf_result = bf_series.astype(dtypes.JSON_DTYPE, errors="null")
    assert bf_result.dtype == dtypes.JSON_DTYPE

    expected = pd.Series([None], dtype=dtypes.JSON_DTYPE)
    expected.index = expected.index.astype("Int64")
    pd.testing.assert_series_equal(bf_result.to_pandas(), expected)


def test_string_astype_json_raise_error():
    data = ["this is not a valid json string"]
    bf_series = series.Series(data, dtype=dtypes.STRING_DTYPE)
    with pytest.raises(
        google.api_core.exceptions.BadRequest,
        match="syntax error while parsing value",
    ):
        bf_series.astype(dtypes.JSON_DTYPE, errors="raise").to_pandas()


@pytest.mark.parametrize("errors", ["raise", "null"])
@pytest.mark.parametrize(
    ("data", "to_type"),
    [
        pytest.param(["1", "10.0", None], dtypes.INT_DTYPE, id="to_int"),
        pytest.param(["0.0001", "2500000000", None], dtypes.FLOAT_DTYPE, id="to_float"),
        pytest.param(["true", "false", None], dtypes.BOOL_DTYPE, id="to_bool"),
        pytest.param(['"str"', None], dtypes.STRING_DTYPE, id="to_string"),
        pytest.param(
            ['"str"', None],
            dtypes.TIME_DTYPE,
            id="invalid",
            marks=pytest.mark.xfail(raises=TypeError),
        ),
    ],
)
def test_json_astype_others(data, to_type, errors):
    bf_series = series.Series(data, dtype=dtypes.JSON_DTYPE)

    bf_result = bf_series.astype(to_type, errors=errors)
    assert bf_result.dtype == to_type

    load_data = [json.loads(item) if item is not None else None for item in data]
    expected = pd.Series(load_data, dtype=to_type)
    expected.index = expected.index.astype("Int64")
    pd.testing.assert_series_equal(bf_result.to_pandas(), expected)


@pytest.mark.parametrize(
    ("data", "to_type"),
    [
        pytest.param(["10.2", None], dtypes.INT_DTYPE, id="to_int"),
        pytest.param(["false", None], dtypes.FLOAT_DTYPE, id="to_float"),
        pytest.param(["10.2", None], dtypes.BOOL_DTYPE, id="to_bool"),
        pytest.param(["true", None], dtypes.STRING_DTYPE, id="to_string"),
    ],
)
def test_json_astype_others_raise_error(data, to_type):
    bf_series = series.Series(data, dtype=dtypes.JSON_DTYPE)
    with pytest.raises(google.api_core.exceptions.BadRequest):
        bf_series.astype(to_type, errors="raise").to_pandas()


@pytest.mark.parametrize(
    ("data", "to_type"),
    [
        pytest.param(["10.2", None], dtypes.INT_DTYPE, id="to_int"),
        pytest.param(["false", None], dtypes.FLOAT_DTYPE, id="to_float"),
        pytest.param(["10.2", None], dtypes.BOOL_DTYPE, id="to_bool"),
        pytest.param(["true", None], dtypes.STRING_DTYPE, id="to_string"),
    ],
)
def test_json_astype_others_in_safe_mode(data, to_type):
    bf_series = series.Series(data, dtype=dtypes.JSON_DTYPE)
    bf_result = bf_series.astype(to_type, errors="null")
    assert bf_result.dtype == to_type

    expected = pd.Series([None, None], dtype=to_type)
    expected.index = expected.index.astype("Int64")
    pd.testing.assert_series_equal(bf_result.to_pandas(), expected)


@pytest.mark.parametrize(
    "index",
    [0, 5, -2],
)
def test_iloc_single_integer(scalars_df_index, scalars_pandas_df_index, index):
    bf_result = scalars_df_index.string_col.iloc[index]
    pd_result = scalars_pandas_df_index.string_col.iloc[index]

    assert bf_result == pd_result


def test_iloc_single_integer_out_of_bound_error(scalars_df_index):
    with pytest.raises(IndexError, match="single positional indexer is out-of-bounds"):
        scalars_df_index.string_col.iloc[99]


def test_loc_bool_series_explicit_index(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.loc[scalars_df_index.bool_col].to_pandas()
    pd_result = scalars_pandas_df_index.string_col.loc[scalars_pandas_df_index.bool_col]

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_loc_bool_series_default_index(
    scalars_df_default_index, scalars_pandas_df_default_index
):
    bf_result = scalars_df_default_index.string_col.loc[
        scalars_df_default_index.bool_col
    ].to_pandas()
    pd_result = scalars_pandas_df_default_index.string_col.loc[
        scalars_pandas_df_default_index.bool_col
    ]

    assert_pandas_df_equal(
        bf_result.to_frame(),
        pd_result.to_frame(),
    )


def test_argmin(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.argmin()
    pd_result = scalars_pandas_df_index.string_col.argmin()
    assert bf_result == pd_result


def test_argmax(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.int64_too.argmax()
    pd_result = scalars_pandas_df_index.int64_too.argmax()
    assert bf_result == pd_result


def test_series_idxmin(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.idxmin()
    pd_result = scalars_pandas_df_index.string_col.idxmin()
    assert bf_result == pd_result


def test_series_idxmax(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.int64_too.idxmax()
    pd_result = scalars_pandas_df_index.int64_too.idxmax()
    assert bf_result == pd_result


def test_getattr_attribute_error_when_pandas_has(scalars_df_index):
    # asof is implemented in pandas but not in bigframes
    with pytest.raises(AttributeError):
        scalars_df_index.string_col.asof()


def test_getattr_attribute_error(scalars_df_index):
    with pytest.raises(AttributeError):
        scalars_df_index.string_col.not_a_method()


def test_rename(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.rename("newname")
    pd_result = scalars_pandas_df_index.string_col.rename("newname")

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_rename_nonstring(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.rename((4, 2))
    pd_result = scalars_pandas_df_index.string_col.rename((4, 2))

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_rename_dict_same_type(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.rename({1: 100, 2: 200})
    pd_result = scalars_pandas_df_index.string_col.rename({1: 100, 2: 200})

    pd_result.index = pd_result.index.astype("Int64")

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_rename_axis(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.string_col.rename_axis("newindexname")
    pd_result = scalars_pandas_df_index.string_col.rename_axis("newindexname")

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_list_string_index(scalars_df_index, scalars_pandas_df_index):
    index_list = scalars_pandas_df_index.string_col.iloc[[0, 1, 1, 5]].values

    scalars_df_index = scalars_df_index.set_index("string_col", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index(
        "string_col", drop=False
    )

    bf_result = scalars_df_index.string_col.loc[index_list]
    pd_result = scalars_pandas_df_index.string_col.loc[index_list]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_list_integer_index(scalars_df_index, scalars_pandas_df_index):
    index_list = [3, 2, 1, 3, 2, 1]

    bf_result = scalars_df_index.bool_col.loc[index_list]
    pd_result = scalars_pandas_df_index.bool_col.loc[index_list]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_list_multiindex(scalars_df_index, scalars_pandas_df_index):
    scalars_df_multiindex = scalars_df_index.set_index(["string_col", "int64_col"])
    scalars_pandas_df_multiindex = scalars_pandas_df_index.set_index(
        ["string_col", "int64_col"]
    )
    index_list = [("Hello, World!", -234892), ("Hello, World!", 123456789)]

    bf_result = scalars_df_multiindex.int64_too.loc[index_list]
    pd_result = scalars_pandas_df_multiindex.int64_too.loc[index_list]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_iloc_list(scalars_df_index, scalars_pandas_df_index):
    index_list = [0, 0, 0, 5, 4, 7]

    bf_result = scalars_df_index.string_col.iloc[index_list]
    pd_result = scalars_pandas_df_index.string_col.iloc[index_list]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_iloc_list_nameless(scalars_df_index, scalars_pandas_df_index):
    index_list = [0, 0, 0, 5, 4, 7]

    bf_series = scalars_df_index.string_col.rename(None)
    bf_result = bf_series.iloc[index_list]
    pd_series = scalars_pandas_df_index.string_col.rename(None)
    pd_result = pd_series.iloc[index_list]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_list_nameless(scalars_df_index, scalars_pandas_df_index):
    index_list = [0, 0, 0, 5, 4, 7]

    bf_series = scalars_df_index.string_col.rename(None)
    bf_result = bf_series.loc[index_list]

    pd_series = scalars_pandas_df_index.string_col.rename(None)
    pd_result = pd_series.loc[index_list]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_series_string_index(scalars_df_index, scalars_pandas_df_index):
    pd_string_series = scalars_pandas_df_index.string_col.iloc[[0, 5, 1, 1, 5]]
    bf_string_series = scalars_df_index.string_col.iloc[[0, 5, 1, 1, 5]]

    scalars_df_index = scalars_df_index.set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("string_col")

    bf_result = scalars_df_index.date_col.loc[bf_string_series]
    pd_result = scalars_pandas_df_index.date_col.loc[pd_string_series]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_series_multiindex(scalars_df_index, scalars_pandas_df_index):
    pd_string_series = scalars_pandas_df_index.string_col.iloc[[0, 5, 1, 1, 5]]
    bf_string_series = scalars_df_index.string_col.iloc[[0, 5, 1, 1, 5]]

    scalars_df_multiindex = scalars_df_index.set_index(["string_col", "int64_col"])
    scalars_pandas_df_multiindex = scalars_pandas_df_index.set_index(
        ["string_col", "int64_col"]
    )

    bf_result = scalars_df_multiindex.int64_too.loc[bf_string_series]
    pd_result = scalars_pandas_df_multiindex.int64_too.loc[pd_string_series]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_index_integer_index(scalars_df_index, scalars_pandas_df_index):
    pd_index = scalars_pandas_df_index.iloc[[0, 5, 1, 1, 5]].index
    bf_index = scalars_df_index.iloc[[0, 5, 1, 1, 5]].index

    bf_result = scalars_df_index.date_col.loc[bf_index]
    pd_result = scalars_pandas_df_index.date_col.loc[pd_index]

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_single_index_with_duplicate(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("string_col", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index(
        "string_col", drop=False
    )
    index = "Hello, World!"
    bf_result = scalars_df_index.date_col.loc[index]
    pd_result = scalars_pandas_df_index.date_col.loc[index]
    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_single_index_no_duplicate(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("int64_too", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("int64_too", drop=False)
    index = -2345
    bf_result = scalars_df_index.date_col.loc[index]
    pd_result = scalars_pandas_df_index.date_col.loc[index]
    assert bf_result == pd_result


def test_series_bool_interpretation_error(scalars_df_index):
    with pytest.raises(ValueError):
        True if scalars_df_index["string_col"] else False


def test_query_job_setters(scalars_dfs):
    # if allow_large_results=False, might not create query job
    with bigframes.option_context("compute.allow_large_results", True):
        job_ids = set()
        df, _ = scalars_dfs
        series = df["int64_col"]
        assert series.query_job is not None
        repr(series)
        job_ids.add(series.query_job.job_id)
        series.to_pandas()
        job_ids.add(series.query_job.job_id)
        assert len(job_ids) == 2


@pytest.mark.parametrize(
    ("series_input",),
    [
        ([1, 2, 3, 4, 5],),
        ([1, 1, 3, 5, 5],),
        ([1, pd.NA, 4, 5, 5],),
        ([1, 3, 2, 5, 4],),
        ([pd.NA, pd.NA],),
        ([1, 1, 1, 1, 1],),
    ],
)
def test_is_monotonic_increasing(series_input):
    scalars_df = series.Series(series_input, dtype=pd.Int64Dtype())
    scalars_pandas_df = pd.Series(series_input, dtype=pd.Int64Dtype())
    assert (
        scalars_df.is_monotonic_increasing == scalars_pandas_df.is_monotonic_increasing
    )


@pytest.mark.parametrize(
    ("series_input",),
    [
        ([1],),
        ([5, 4, 3, 2, 1],),
        ([5, 5, 3, 1, 1],),
        ([1, pd.NA, 4, 5, 5],),
        ([5, pd.NA, 4, 2, 1],),
        ([1, 1, 1, 1, 1],),
    ],
)
def test_is_monotonic_decreasing(series_input):
    scalars_df = series.Series(series_input)
    scalars_pandas_df = pd.Series(series_input)
    assert (
        scalars_df.is_monotonic_decreasing == scalars_pandas_df.is_monotonic_decreasing
    )


def test_map_dict_input(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    local_map = dict()
    # construct a local map, incomplete to cover <NA> behavior
    for s in scalars_pandas_df.string_col[:-3]:
        if isinstance(s, str):
            local_map[s] = ord(s[0])

    pd_result = scalars_pandas_df.string_col.map(local_map)
    pd_result = pd_result.astype("Int64")  # pandas type differences
    bf_result = scalars_df.string_col.map(local_map)

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_map_series_input(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    new_index = scalars_pandas_df.int64_too.drop_duplicates()
    pd_map_series = scalars_pandas_df.string_col.iloc[0 : len(new_index)]
    pd_map_series.index = new_index
    bf_map_series = series.Series(
        pd_map_series, session=scalars_df._get_block().expr.session
    )

    pd_result = scalars_pandas_df.int64_too.map(pd_map_series)
    bf_result = scalars_df.int64_too.map(bf_map_series)

    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_map_series_input_duplicates_error(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    new_index = scalars_pandas_df.int64_too
    pd_map_series = scalars_pandas_df.string_col.iloc[0 : len(new_index)]
    pd_map_series.index = new_index
    bf_map_series = series.Series(
        pd_map_series, session=scalars_df._get_block().expr.session
    )

    with pytest.raises(pd.errors.InvalidIndexError):
        scalars_pandas_df.int64_too.map(pd_map_series)
    with pytest.raises(pd.errors.InvalidIndexError):
        scalars_df.int64_too.map(bf_map_series, verify_integrity=True)


@pytest.mark.parametrize(
    ("frac", "n", "random_state"),
    [
        (None, 4, None),
        (0.5, None, None),
        (None, 4, 10),
        (0.5, None, 10),
        (None, None, None),
    ],
    ids=[
        "n_wo_random_state",
        "frac_wo_random_state",
        "n_w_random_state",
        "frac_w_random_state",
        "n_default",
    ],
)
def test_sample(scalars_dfs, frac, n, random_state):
    scalars_df, _ = scalars_dfs
    df = scalars_df.int64_col.sample(frac=frac, n=n, random_state=random_state)
    bf_result = df.to_pandas()

    n = 1 if n is None else n
    expected_sample_size = round(frac * scalars_df.shape[0]) if frac is not None else n
    assert bf_result.shape[0] == expected_sample_size


def test_series_iter(
    scalars_df_index,
    scalars_pandas_df_index,
):
    for bf_i, pd_i in zip(
        scalars_df_index["int64_too"], scalars_pandas_df_index["int64_too"]
    ):
        assert bf_i == pd_i


@pytest.mark.parametrize(
    (
        "col",
        "lambda_",
    ),
    [
        pytest.param("int64_col", lambda x: x * x + x + 1),
        pytest.param("int64_col", lambda x: x % 2 == 1),
        pytest.param("string_col", lambda x: x + "_suffix"),
    ],
    ids=[
        "lambda_int_int",
        "lambda_int_bool",
        "lambda_str_str",
    ],
)
def test_apply_lambda(scalars_dfs, col, lambda_):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df[col]

    # Can't be applied to BigFrames Series without by_row=False
    with pytest.raises(ValueError, match="by_row=False"):
        bf_col.apply(lambda_)

    bf_result = bf_col.apply(lambda_, by_row=False).to_pandas()

    pd_col = scalars_pandas_df[col]
    if pd.__version__[:3] in ("2.2", "2.3"):
        pd_result = pd_col.apply(lambda_, by_row=False)
    else:
        pd_result = pd_col.apply(lambda_)

    # ignore dtype check, which are Int64 and object respectively
    # Some columns implicitly convert to floating point. Use check_exact=False to ensure we're "close enough"
    assert_series_equal(
        bf_result, pd_result, check_dtype=False, check_exact=False, rtol=0.001
    )


@pytest.mark.parametrize(
    ("ufunc",),
    [
        pytest.param(numpy.log),
        pytest.param(numpy.sqrt),
        pytest.param(numpy.sin),
    ],
    ids=[
        "log",
        "sqrt",
        "sin",
    ],
)
def test_apply_numpy_ufunc(scalars_dfs, ufunc):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df["int64_col"]

    # Can't be applied to BigFrames Series without by_row=False
    with pytest.raises(ValueError, match="by_row=False"):
        bf_col.apply(ufunc)

    bf_result = bf_col.apply(ufunc, by_row=False).to_pandas()

    pd_col = scalars_pandas_df["int64_col"]
    pd_result = pd_col.apply(ufunc)

    assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("ufunc",),
    [
        pytest.param(numpy.add),
        pytest.param(numpy.divide),
    ],
    ids=[
        "add",
        "divide",
    ],
)
def test_combine_series_ufunc(scalars_dfs, ufunc):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df["int64_col"].dropna()
    bf_result = bf_col.combine(bf_col, ufunc).to_pandas()

    pd_col = scalars_pandas_df["int64_col"].dropna()
    pd_result = pd_col.combine(pd_col, ufunc)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_combine_scalar_ufunc(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_col = scalars_df["int64_col"].dropna()
    bf_result = bf_col.combine(2.5, numpy.add).to_pandas()

    pd_col = scalars_pandas_df["int64_col"].dropna()
    pd_result = pd_col.combine(2.5, numpy.add)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_apply_simple_udf(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    def foo(x):
        return x * x + 2 * x + 3

    bf_col = scalars_df["int64_col"]

    # Can't be applied to BigFrames Series without by_row=False
    with pytest.raises(ValueError, match="by_row=False"):
        bf_col.apply(foo)

    bf_result = bf_col.apply(foo, by_row=False).to_pandas()

    pd_col = scalars_pandas_df["int64_col"]

    if pd.__version__[:3] in ("2.2", "2.3"):
        pd_result = pd_col.apply(foo, by_row=False)
    else:
        pd_result = pd_col.apply(foo)

    # ignore dtype check, which are Int64 and object respectively
    # Some columns implicitly convert to floating point. Use check_exact=False to ensure we're "close enough"
    assert_series_equal(
        bf_result, pd_result, check_dtype=False, check_exact=False, rtol=0.001
    )


@pytest.mark.parametrize(
    ("col", "lambda_", "exception"),
    [
        pytest.param("int64_col", {1: 2, 3: 4}, ValueError),
        pytest.param("int64_col", numpy.square, TypeError),
        pytest.param("string_col", lambda x: x.capitalize(), AttributeError),
    ],
    ids=[
        "not_callable",
        "numpy_ufunc",
        "custom_lambda",
    ],
)
def test_apply_not_supported(scalars_dfs, col, lambda_, exception):
    scalars_df, _ = scalars_dfs

    bf_col = scalars_df[col]
    with pytest.raises(exception):
        bf_col.apply(lambda_, by_row=False)


def test_series_pipe(
    scalars_df_index,
    scalars_pandas_df_index,
):
    column = "int64_too"

    def foo(x: int, y: int, df):
        return (df + x) % y

    bf_result = (
        scalars_df_index[column]
        .pipe((foo, "df"), x=7, y=9)
        .pipe(lambda x: x**2)
        .to_pandas()
    )

    pd_result = (
        scalars_pandas_df_index[column]
        .pipe((foo, "df"), x=7, y=9)
        .pipe(lambda x: x**2)
    )

    assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("data"),
    [
        pytest.param([1, 2, 3], id="int"),
        pytest.param([[1, 2, 3], [], numpy.nan, [3, 4]], id="int_array"),
        pytest.param(
            [["A", "AA", "AAA"], ["BB", "B"], numpy.nan, [], ["C"]], id="string_array"
        ),
        pytest.param(
            [
                {"A": {"x": 1.0}, "B": "b"},
                {"A": {"y": 2.0}, "B": "bb"},
                {"A": {"z": 4.0}},
                {},
                numpy.nan,
            ],
            id="struct_array",
        ),
    ],
)
def test_series_explode(data):
    s = bigframes.pandas.Series(data)
    pd_s = s.to_pandas()
    pd.testing.assert_series_equal(
        s.explode().to_pandas(),
        pd_s.explode(),
        check_index_type=False,
        check_dtype=False,
    )


@pytest.mark.parametrize(
    ("index", "ignore_index"),
    [
        pytest.param(None, True, id="default_index"),
        pytest.param(None, False, id="ignore_default_index"),
        pytest.param([5, 1, 3, 2], True, id="unordered_index"),
        pytest.param([5, 1, 3, 2], False, id="ignore_unordered_index"),
        pytest.param(["z", "x", "a", "b"], True, id="str_index"),
        pytest.param(["z", "x", "a", "b"], False, id="ignore_str_index"),
        pytest.param(
            pd.Index(["z", "x", "a", "b"], name="idx"), True, id="str_named_index"
        ),
        pytest.param(
            pd.Index(["z", "x", "a", "b"], name="idx"),
            False,
            id="ignore_str_named_index",
        ),
        pytest.param(
            pd.MultiIndex.from_frame(
                pd.DataFrame({"idx0": [5, 1, 3, 2], "idx1": ["z", "x", "a", "b"]})
            ),
            True,
            id="multi_index",
        ),
        pytest.param(
            pd.MultiIndex.from_frame(
                pd.DataFrame({"idx0": [5, 1, 3, 2], "idx1": ["z", "x", "a", "b"]})
            ),
            False,
            id="ignore_multi_index",
        ),
    ],
)
def test_series_explode_w_index(index, ignore_index):
    data = [[], [200.0, 23.12], [4.5, -9.0], [1.0]]
    s = bigframes.pandas.Series(data, index=index)
    pd_s = pd.Series(data, index=index)
    # TODO(b/340885567): fix type error
    pd.testing.assert_series_equal(
        s.explode(ignore_index=ignore_index).to_pandas(),  # type: ignore
        pd_s.explode(ignore_index=ignore_index).astype(pd.Float64Dtype()),  # type: ignore
        check_index_type=False,
    )


@pytest.mark.parametrize(
    ("ignore_index", "ordered"),
    [
        pytest.param(True, True, id="include_index_ordered"),
        pytest.param(True, False, id="include_index_unordered"),
        pytest.param(False, True, id="ignore_index_ordered"),
    ],
)
def test_series_explode_reserve_order(ignore_index, ordered):
    data = [numpy.random.randint(0, 10, 10) for _ in range(10)]
    s = bigframes.pandas.Series(data)
    pd_s = pd.Series(data)

    # TODO(b/340885567): fix type error
    res = s.explode(ignore_index=ignore_index).to_pandas(ordered=ordered)  # type: ignore
    # TODO(b/340885567): fix type error
    pd_res = pd_s.explode(ignore_index=ignore_index).astype(pd.Int64Dtype())  # type: ignore
    pd_res.index = pd_res.index.astype(pd.Int64Dtype())
    pd.testing.assert_series_equal(
        res if ordered else res.sort_index(),
        pd_res,
    )


def test_series_explode_w_aggregate():
    data = [[1, 2, 3], [], numpy.nan, [3, 4]]
    s = bigframes.pandas.Series(data)
    pd_s = pd.Series(data)
    assert s.explode().sum() == pd_s.explode().sum()


def test_series_construct_empty_array():
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    s = bigframes.pandas.Series([[]])
    expected = pd.Series(
        [[]],
        dtype=pd.ArrowDtype(pa.list_(pa.float64())),
        index=pd.Index([0], dtype=pd.Int64Dtype()),
    )
    pd.testing.assert_series_equal(
        expected,
        s.to_pandas(),
    )


@pytest.mark.parametrize(
    ("data"),
    [
        pytest.param(numpy.nan, id="null"),
        pytest.param([numpy.nan], id="null_array"),
        pytest.param([[]], id="empty_array"),
        pytest.param([numpy.nan, []], id="null_and_empty_array"),
    ],
)
def test_series_explode_null(data):
    s = bigframes.pandas.Series(data)
    pd.testing.assert_series_equal(
        s.explode().to_pandas(),
        s.to_pandas().explode(),
        check_dtype=False,
    )


@pytest.mark.parametrize(
    ("append", "level", "col", "rule"),
    [
        pytest.param(False, None, "timestamp_col", "75D"),
        pytest.param(True, 1, "timestamp_col", "25W"),
        pytest.param(False, None, "datetime_col", "3ME"),
        pytest.param(True, "timestamp_col", "timestamp_col", "1YE"),
    ],
)
def test__resample(scalars_df_index, scalars_pandas_df_index, append, level, col, rule):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df_index = scalars_df_index.set_index(col, append=append)["int64_col"]
    scalars_pandas_df_index = scalars_pandas_df_index.set_index(col, append=append)[
        "int64_col"
    ]
    bf_result = scalars_df_index._resample(rule=rule, level=level).min().to_pandas()
    pd_result = scalars_pandas_df_index.resample(rule=rule, level=level).min()
    pd.testing.assert_series_equal(bf_result, pd_result)


def test_series_struct_get_field_by_attribute(
    nested_structs_df, nested_structs_pandas_df
):
    if Version(pd.__version__) < Version("2.2.0"):
        pytest.skip("struct accessor is not supported before pandas 2.2")

    bf_series = nested_structs_df["person"]
    df_series = nested_structs_pandas_df["person"]

    pd.testing.assert_series_equal(
        bf_series.address.city.to_pandas(),
        df_series.struct.field("address").struct.field("city"),
        check_dtype=False,
        check_index=False,
    )
    pd.testing.assert_series_equal(
        bf_series.address.country.to_pandas(),
        df_series.struct.field("address").struct.field("country"),
        check_dtype=False,
        check_index=False,
    )


def test_series_struct_fields_in_dir(nested_structs_df):
    series = nested_structs_df["person"]

    assert "age" in dir(series)
    assert "address" in dir(series)
    assert "city" in dir(series.address)
    assert "country" in dir(series.address)


def test_series_struct_class_attributes_shadow_struct_fields(nested_structs_df):
    series = nested_structs_df["person"]

    assert series.name == "person"


def test_series_to_pandas_dry_run(scalars_df_index):
    bf_series = scalars_df_index["int64_col"]

    result = bf_series.to_pandas(dry_run=True)

    assert isinstance(result, pd.Series)
    assert len(result) > 0


def test_series_item(session):
    # Test with a single item
    bf_s_single = bigframes.pandas.Series([42], session=session)
    pd_s_single = pd.Series([42])
    assert bf_s_single.item() == pd_s_single.item()


def test_series_item_with_multiple(session):
    # Test with multiple items
    bf_s_multiple = bigframes.pandas.Series([1, 2, 3], session=session)
    pd_s_multiple = pd.Series([1, 2, 3])

    try:
        pd_s_multiple.item()
    except ValueError as e:
        expected_message = str(e)
    else:
        raise AssertionError("Expected ValueError from pandas, but didn't get one")

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        bf_s_multiple.item()


def test_series_item_with_empty(session):
    # Test with an empty Series
    bf_s_empty = bigframes.pandas.Series([], dtype="Int64", session=session)
    pd_s_empty = pd.Series([], dtype="Int64")

    try:
        pd_s_empty.item()
    except ValueError as e:
        expected_message = str(e)
    else:
        raise AssertionError("Expected ValueError from pandas, but didn't get one")

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        bf_s_empty.item()
