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

import math
import re
import tempfile

import geopandas as gpd  # type: ignore
import numpy
import pandas as pd
import pyarrow as pa  # type: ignore
import pytest

import bigframes.pandas
import bigframes.series as series
from tests.system.utils import assert_pandas_df_equal, assert_series_equal


def test_series_construct_copy(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = series.Series(
        scalars_df["int64_col"], name="test_series", dtype="Float64"
    ).to_pandas()
    pd_result = pd.Series(
        scalars_pandas_df["int64_col"], name="test_series", dtype="Float64"
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


@pytest.mark.parametrize(
    ["col_name", "expected_dtype"],
    [
        ("bool_col", pd.BooleanDtype()),
        # TODO(swast): Use a more efficient type.
        ("bytes_col", numpy.dtype("object")),
        ("date_col", pd.ArrowDtype(pa.date32())),
        ("datetime_col", pd.ArrowDtype(pa.timestamp("us"))),
        ("float64_col", pd.Float64Dtype()),
        ("geography_col", gpd.array.GeometryDtype()),
        ("int64_col", pd.Int64Dtype()),
        # TODO(swast): Use a more efficient type.
        ("numeric_col", numpy.dtype("object")),
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


def test_series___getitem___with_int_key(scalars_dfs):
    col_name = "int64_too"
    index_col = "string_col"
    key = 2
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


def test_series_agg_single_string(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_col"].agg("sum")
    pd_result = scalars_pandas_df["int64_col"].agg("sum")
    assert math.isclose(pd_result, bf_result)


def test_series_agg_multi_string(scalars_dfs):
    aggregations = ["sum", "mean", "std", "var", "min", "max", "nunique", "count"]
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
    ],
    ids=[
        "and",
        "or",
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
def test_corr(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df["int64_too"].corr(scalars_df["int64_too"])
    pd_result = (
        scalars_pandas_df["int64_too"]
        .astype("int64")
        .corr(scalars_pandas_df["int64_too"].astype("int64"))
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


def test_series_add_pandas_series_not_implemented(scalars_dfs):
    scalars_df, _ = scalars_dfs
    with pytest.raises(NotImplementedError):
        (
            scalars_df["float64_col"]
            + pd.Series(
                [1, 1, 1, 1],
            )
        ).to_pandas()


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


def test_repr(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    if scalars_pandas_df.index.name != "rowindex":
        pytest.skip("Require index & ordering for consistent repr.")

    col_name = "int64_col"
    bf_series = scalars_df[col_name]
    pd_series = scalars_pandas_df[col_name]
    assert repr(bf_series) == repr(pd_series)


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
    bf_series = scalars_df[col_name].groupby(scalars_df["string_col"]).sum()
    pd_series = (
        scalars_pandas_df[col_name].groupby(scalars_pandas_df["string_col"]).sum()
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
    if scalars_pandas_df.index.name != "rowindex":
        pytest.skip("Require index for groupby level.")

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
    if scalars_pandas_df.index.name != "rowindex":
        pytest.skip("Require index for groupby level.")

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


def test_groupby_median(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"
    bf_series = (
        scalars_df[col_name].groupby(scalars_df["string_col"], dropna=False).median()
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
    )
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
        (lambda x: x.cumprod()),
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
    ).astype(pd.Int64Dtype())
    pd.testing.assert_series_equal(
        pd_series,
        bf_series,
    )


def test_drop_label(scalars_df_index, scalars_pandas_df_index):
    col_name = "int64_col"
    bf_series = scalars_df_index[col_name].drop(1).to_pandas()
    pd_series = scalars_pandas_df_index[col_name].drop(1)
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
    bf_uniq = scalars_df_index[col_name].unique().to_numpy()
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


def test_empty_true_memtable(session: bigframes.Session):
    bf_series: series.Series = series.Series(session=session)
    pd_series: pd.Series = pd.Series()

    bf_result = bf_series.empty
    pd_result = pd_series.empty

    assert pd_result
    assert bf_result == pd_result


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

    if scalars_df.index.name is None:
        pytest.skip("Require explicit index for offset ops.")

    bf_result = scalars_df["string_col"].head(2).to_pandas()
    pd_result = scalars_pandas_df["string_col"].head(2)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_tail(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    if scalars_df.index.name is None:
        pytest.skip("Require explicit index for offset ops.")

    bf_result = scalars_df["string_col"].tail(2).to_pandas()
    pd_result = scalars_pandas_df["string_col"].tail(2)

    assert_series_equal(
        pd_result,
        bf_result,
    )


def test_head_then_scalar_operation(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    if scalars_df.index.name is None:
        pytest.skip("Require explicit index for offset ops.")

    bf_result = (scalars_df["float64_col"].head(1) + 4).to_pandas()
    pd_result = scalars_pandas_df["float64_col"].head(1) + 4

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_head_then_series_operation(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    if scalars_df.index.name is None:
        pytest.skip("Require explicit index for offset ops.")

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
    ("na_option",),
    [
        ("keep",),
        ("top",),
        ("bottom",),
    ],
)
@pytest.mark.parametrize(
    ("method",),
    [
        ("average",),
        ("min",),
        ("max",),
        ("first",),
        ("dense",),
    ],
)
@pytest.mark.skipif(
    True, reason="Blocked by possible pandas rank() regression (b/283278923)"
)
def test_rank_with_nulls(scalars_df_index, scalars_pandas_df_index, na_option, method):
    col_name = "bool_col"
    bf_result = (
        scalars_df_index[col_name].rank(na_option=na_option, method=method).to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index[col_name]
        .rank(na_option=na_option, method=method)
        .astype(pd.Float64Dtype())
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


def test_value_counts(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_too"

    bf_result = scalars_df[col_name].value_counts().to_pandas()
    pd_result = scalars_pandas_df[col_name].value_counts()

    # Older pandas version may not have these values, bigframes tries to emulate 2.0+
    pd_result.name = "count"
    pd_result.index.name = col_name

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_value_counts_w_cut(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"

    bf_cut = bigframes.pandas.cut(scalars_df[col_name], 3, labels=False)
    pd_cut = pd.cut(scalars_pandas_df[col_name], 3, labels=False)

    bf_result = bf_cut.value_counts().to_pandas()
    pd_result = pd_cut.value_counts()
    # Older pandas version may not have these values, bigframes tries to emulate 2.0+
    pd_result.name = "count"
    pd_result.index.name = col_name
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


def test_to_frame(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df["int64_col"].to_frame().to_pandas()
    pd_result = scalars_pandas_df["int64_col"].to_frame()

    assert_pandas_df_equal(bf_result, pd_result)


def test_to_json(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].to_json()
    pd_result = scalars_pandas_df_index["int64_col"].to_json()

    assert bf_result == pd_result


def test_to_csv(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].to_csv()
    pd_result = scalars_pandas_df_index["int64_col"].to_csv()

    assert bf_result == pd_result


def test_to_latex(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index["int64_col"].to_latex()
    pd_result = scalars_pandas_df_index["int64_col"].to_latex()

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
    ("column", "to_type"),
    [
        ("int64_col", "Float64"),
        ("int64_col", "Int64"),  # No-op
        ("int64_col", pd.Float64Dtype()),
        ("int64_col", "string[pyarrow]"),
        ("int64_col", "boolean"),
        ("bool_col", "Int64"),
        ("bool_col", "string[pyarrow]"),
        # pandas actually doesn't let folks convert to/from naive timestamp and
        # raises a deprecation warning to use tz_localize/tz_convert instead,
        # but BigQuery always stores values as UTC and doesn't have to deal
        # with timezone conversions, so we'll allow it.
        ("timestamp_col", pd.ArrowDtype(pa.timestamp("us"))),
        ("datetime_col", pd.ArrowDtype(pa.timestamp("us", tz="UTC"))),
        ("date_col", "string[pyarrow]"),
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
def test_astype(scalars_df_index, scalars_pandas_df_index, column, to_type):
    bf_result = scalars_df_index[column].astype(to_type).to_pandas()
    pd_result = scalars_pandas_df_index[column].astype(to_type)
    pd.testing.assert_series_equal(bf_result, pd_result)


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


@pytest.mark.parametrize(
    "index",
    [0, 5, -2],
)
def test_iloc_single_integer(scalars_df_index, scalars_pandas_df_index, index):
    bf_result = scalars_df_index.string_col.iloc[index]
    pd_result = scalars_pandas_df_index.string_col.iloc[index]

    assert bf_result == pd_result


def test_iloc_single_integer_out_of_bound_error(
    scalars_df_index, scalars_pandas_df_index
):
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
    scalars_df = series.Series(series_input)
    scalars_pandas_df = pd.Series(series_input)
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
