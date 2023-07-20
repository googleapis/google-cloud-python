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
    bf_result_computed = bf_result.compute()
    # Pandas std function produces float64, not matching Float64 from bigframes
    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)


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
    bf_result_computed = bf_result.compute()

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
    bf_result = bf_series.compute()

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
    ],
    ids=[
        "cumsum",
        "cummax",
        "cummin",
        "cumprod",
    ],
)
def test_dataframe_groupby_analytic(
    scalars_df_index, scalars_pandas_df_index, operator
):
    col_names = ["float64_col", "int64_col", "bool_col", "string_col"]
    bf_result = operator(scalars_df_index[col_names].groupby("string_col"))
    pd_result = operator(scalars_pandas_df_index[col_names].groupby("string_col"))
    bf_result_computed = bf_result.compute()

    pd.testing.assert_frame_equal(pd_result, bf_result_computed, check_dtype=False)
