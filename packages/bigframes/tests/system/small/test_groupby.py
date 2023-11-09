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

import pandas as pd
import pytest

import bigframes.pandas as bpd
from tests.system.utils import assert_pandas_df_equal


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x: x.sum(numeric_only=True)),
        (lambda x: x.mean(numeric_only=True)),
        (lambda x: x.min(numeric_only=True)),
        (lambda x: x.max(numeric_only=True)),
        (lambda x: x.std(numeric_only=True)),
        (lambda x: x.var(numeric_only=True)),
    ],
    ids=[
        "sum",
        "mean",
        "min",
        "max",
        "std",
        "var",
    ],
)
def test_dataframe_groupby_numeric_aggregate(
    scalars_df_index, scalars_pandas_df_index, operator
):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = operator(scalars_df_index[col_names].groupby("string_col"))
    pd_result = operator(scalars_pandas_df_index[col_names].groupby("string_col"))
    bf_result_computed = bf_result.to_pandas()
    # Pandas std function produces float64, not matching Float64 from bigframes
    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


def test_dataframe_groupby_median(scalars_df_index, scalars_pandas_df_index):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = (
        scalars_df_index[col_names].groupby("string_col").median(numeric_only=True)
    )
    pd_min = (
        scalars_pandas_df_index[col_names].groupby("string_col").min(numeric_only=True)
    )
    pd_max = (
        scalars_pandas_df_index[col_names].groupby("string_col").max(numeric_only=True)
    )
    bf_result_computed = bf_result.to_pandas()
    # Median is approximate. Just check for plausibility.
    assert ((pd_min <= bf_result_computed) & (bf_result_computed <= pd_max)).all().all()


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x: x.count()),
        (lambda x: x.any()),
        (lambda x: x.all()),
    ],
    ids=[
        "count",
        "any",
        "all",
    ],
)
def test_dataframe_groupby_aggregate(
    scalars_df_index, scalars_pandas_df_index, operator
):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = operator(scalars_df_index[col_names].groupby("string_col"))
    pd_result = operator(scalars_pandas_df_index[col_names].groupby("string_col"))
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_dataframe_groupby_agg_string(
    scalars_df_index, scalars_pandas_df_index, ordered
):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = scalars_df_index[col_names].groupby("string_col").agg("count")
    pd_result = scalars_pandas_df_index[col_names].groupby("string_col").agg("count")
    bf_result_computed = bf_result.to_pandas(ordered=ordered)

    assert_pandas_df_equal(
        pd_result, bf_result_computed, check_dtype=False, ignore_order=not ordered
    )


def test_dataframe_groupby_agg_list(scalars_df_index, scalars_pandas_df_index):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = scalars_df_index[col_names].groupby("string_col").agg(["count", "min"])
    pd_result = (
        scalars_pandas_df_index[col_names].groupby("string_col").agg(["count", "min"])
    )
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


def test_dataframe_groupby_agg_dict_with_list(
    scalars_df_index, scalars_pandas_df_index
):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = (
        scalars_df_index[col_names]
        .groupby("string_col")
        .agg({"int64_too": ["mean", "max"], "string_col": "count"})
    )
    pd_result = (
        scalars_pandas_df_index[col_names]
        .groupby("string_col")
        .agg({"int64_too": ["mean", "max"], "string_col": "count"})
    )
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


def test_dataframe_groupby_agg_dict_no_lists(scalars_df_index, scalars_pandas_df_index):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = (
        scalars_df_index[col_names]
        .groupby("string_col")
        .agg({"int64_too": "mean", "string_col": "count"})
    )
    pd_result = (
        scalars_pandas_df_index[col_names]
        .groupby("string_col")
        .agg({"int64_too": "mean", "string_col": "count"})
    )
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


def test_dataframe_groupby_agg_named(scalars_df_index, scalars_pandas_df_index):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = (
        scalars_df_index[col_names]
        .groupby("string_col")
        .agg(
            agg1=bpd.NamedAgg("int64_too", "sum"),
            agg2=bpd.NamedAgg("float64_col", "max"),
        )
    )
    pd_result = (
        scalars_pandas_df_index[col_names]
        .groupby("string_col")
        .agg(
            agg1=pd.NamedAgg("int64_too", "sum"), agg2=pd.NamedAgg("float64_col", "max")
        )
    )
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


@pytest.mark.parametrize(
    ("as_index"),
    [
        (True),
        (False),
    ],
)
def test_dataframe_groupby_multi_sum(
    scalars_df_index, scalars_pandas_df_index, as_index
):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col", "string_col"]
    bf_series = (
        scalars_df_index[col_names]
        .groupby(["bool_col", "int64_col"], as_index=as_index)
        .sum(numeric_only=True)
    )
    pd_series = (
        scalars_pandas_df_index[col_names]
        .groupby(["bool_col", "int64_col"], as_index=as_index)
        .sum(numeric_only=True)
    )
    bf_result = bf_series.to_pandas()

    if not as_index:
        # BigQuery DataFrames default indices use nullable Int64 always
        pd_series.index = pd_series.index.astype("Int64")

    pd.testing.assert_frame_equal(
        pd_series,
        bf_result,
    )


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x: x.cumsum(numeric_only=True)),
        (lambda x: x.cummax(numeric_only=True)),
        (lambda x: x.cummin(numeric_only=True)),
        (lambda x: x.cumprod()),
        (lambda x: x.shift(periods=2)),
    ],
    ids=[
        "cumsum",
        "cummax",
        "cummin",
        "cumprod",
        "shift",
    ],
)
def test_dataframe_groupby_analytic(
    scalars_df_index, scalars_pandas_df_index, operator
):
    col_names = ["float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = operator(scalars_df_index[col_names].groupby("string_col"))
    pd_result = operator(scalars_pandas_df_index[col_names].groupby("string_col"))
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


def test_series_groupby_skew(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.groupby("bool_col")["int64_too"].skew().to_pandas()
    pd_result = scalars_pandas_df_index.groupby("bool_col")["int64_too"].skew()

    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


def test_series_groupby_kurt(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.groupby("bool_col")["int64_too"].kurt().to_pandas()
    # Pandas doesn't have groupby.kurt yet: https://github.com/pandas-dev/pandas/issues/40139
    pd_result = scalars_pandas_df_index.groupby("bool_col")["int64_too"].apply(
        pd.Series.kurt
    )

    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


def test_dataframe_groupby_skew(scalars_df_index, scalars_pandas_df_index):
    col_names = ["float64_col", "int64_col", "bool_col"]
    bf_result = scalars_df_index[col_names].groupby("bool_col").skew().to_pandas()
    pd_result = scalars_pandas_df_index[col_names].groupby("bool_col").skew()

    pd.testing.assert_frame_equal(pd_result, bf_result, check_dtype=False)


def test_dataframe_groupby_kurt(scalars_df_index, scalars_pandas_df_index):
    col_names = ["float64_col", "int64_col", "bool_col"]
    bf_result = scalars_df_index[col_names].groupby("bool_col").kurt().to_pandas()
    # Pandas doesn't have groupby.kurt yet: https://github.com/pandas-dev/pandas/issues/40139
    pd_result = (
        scalars_pandas_df_index[col_names]
        .groupby("bool_col")
        .apply(pd.Series.kurt)
        .drop("bool_col", axis=1)
    )

    pd.testing.assert_frame_equal(pd_result, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_dataframe_groupby_diff(scalars_df_index, scalars_pandas_df_index, ordered):
    col_names = ["float64_col", "int64_col", "string_col"]
    bf_result = scalars_df_index[col_names].groupby("string_col").diff(-1)
    pd_result = scalars_pandas_df_index[col_names].groupby("string_col").diff(-1)
    bf_result_computed = bf_result.to_pandas(ordered=ordered)

    assert_pandas_df_equal(
        pd_result, bf_result_computed, check_dtype=False, ignore_order=not ordered
    )


def test_dataframe_groupby_getitem(
    scalars_df_index,
    scalars_pandas_df_index,
):
    col_names = ["float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = (
        scalars_df_index[col_names].groupby("string_col")["int64_col"].min().to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index[col_names].groupby("string_col")["int64_col"].min()
    )

    pd.testing.assert_series_equal(pd_result, bf_result, check_dtype=False)


def test_dataframe_groupby_getitem_list(
    scalars_df_index,
    scalars_pandas_df_index,
):
    col_names = ["float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = (
        scalars_df_index[col_names].groupby("string_col")[col_names].min().to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index[col_names].groupby("string_col")[col_names].min()
    )

    pd.testing.assert_frame_equal(pd_result, bf_result, check_dtype=False)


def test_series_groupby_agg_string(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["int64_col"]
        .groupby(scalars_df_index["string_col"])
        .agg("count")
    )
    pd_result = (
        scalars_pandas_df_index["int64_col"]
        .groupby(scalars_pandas_df_index["string_col"])
        .agg("count")
    )
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_series_equal(
        pd_result, bf_result_computed, check_dtype=False, check_names=False
    )


def test_series_groupby_agg_list(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index["int64_col"]
        .groupby(scalars_df_index["string_col"])
        .agg(["sum", "mean"])
    )
    pd_result = (
        scalars_pandas_df_index["int64_col"]
        .groupby(scalars_pandas_df_index["string_col"])
        .agg(["sum", "mean"])
    )
    bf_result_computed = bf_result.to_pandas()

    pd.testing.assert_frame_equal(
        pd_result, bf_result_computed, check_dtype=False, check_names=False
    )
