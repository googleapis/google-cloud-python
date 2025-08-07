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

import pandas.testing
import pytest


def test_df_describe_non_temporal(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs
    # excluding temporal columns here because BigFrames cannot perform percentiles operations on them
    unsupported_columns = [
        "datetime_col",
        "timestamp_col",
        "time_col",
        "date_col",
        "duration_col",
    ]
    bf_result = scalars_df.drop(columns=unsupported_columns).describe().to_pandas()

    modified_pd_df = scalars_pandas_df.drop(columns=unsupported_columns)
    pd_result = modified_pd_df.describe()

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    # Drop quartiles, as they are approximate
    bf_min = bf_result.loc["min", :]
    bf_p25 = bf_result.loc["25%", :]
    bf_p50 = bf_result.loc["50%", :]
    bf_p75 = bf_result.loc["75%", :]
    bf_max = bf_result.loc["max", :]

    bf_result = bf_result.drop(labels=["25%", "50%", "75%"])
    pd_result = pd_result.drop(labels=["25%", "50%", "75%"])

    pandas.testing.assert_frame_equal(pd_result, bf_result, check_index_type=False)

    # Double-check that quantiles are at least plausible.
    assert (
        (bf_min <= bf_p25)
        & (bf_p25 <= bf_p50)
        & (bf_p50 <= bf_p50)
        & (bf_p75 <= bf_max)
    ).all()


@pytest.mark.parametrize("include", [None, "all"])
def test_df_describe_non_numeric(scalars_dfs, include):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    # Excluding "date_col" here because in BigFrames it is used as PyArrow[date32()], which is
    # considered numerical in Pandas
    target_columns = ["string_col", "bytes_col", "bool_col", "time_col"]

    modified_bf = scalars_df[target_columns]
    bf_result = modified_bf.describe(include=include).to_pandas()

    modified_pd_df = scalars_pandas_df[target_columns]
    pd_result = modified_pd_df.describe(include=include)

    # Reindex results with the specified keys and their order, because
    # the relative order is not important.
    bf_result = bf_result.reindex(["count", "nunique"])
    pd_result = pd_result.reindex(
        ["count", "unique"]
        # BF counter part of "unique" is called "nunique"
    ).rename(index={"unique": "nunique"})

    pandas.testing.assert_frame_equal(
        pd_result.astype("Int64"),
        bf_result,
        check_index_type=False,
    )


def test_df_describe_temporal(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    temporal_columns = ["datetime_col", "timestamp_col", "time_col", "date_col"]

    modified_bf = scalars_df[temporal_columns]
    bf_result = modified_bf.describe(include="all").to_pandas()

    modified_pd_df = scalars_pandas_df[temporal_columns]
    pd_result = modified_pd_df.describe(include="all")

    # Reindex results with the specified keys and their order, because
    # the relative order is not important.
    bf_result = bf_result.reindex(["count", "nunique"])
    pd_result = pd_result.reindex(
        ["count", "unique"]
        # BF counter part of "unique" is called "nunique"
    ).rename(index={"unique": "nunique"})

    pandas.testing.assert_frame_equal(
        pd_result.astype("Float64"),
        bf_result.astype("Float64"),
        check_index_type=False,
    )


def test_df_describe_mixed_types_include_all(scalars_dfs):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    scalars_df, scalars_pandas_df = scalars_dfs

    numeric_columns = [
        "int64_col",
        "float64_col",
    ]
    non_numeric_columns = ["string_col"]
    supported_columns = numeric_columns + non_numeric_columns

    modified_bf = scalars_df[supported_columns]
    bf_result = modified_bf.describe(include="all").to_pandas()

    modified_pd_df = scalars_pandas_df[supported_columns]
    pd_result = modified_pd_df.describe(include="all")

    # Drop quartiles, as they are approximate
    bf_min = bf_result.loc["min", :]
    bf_p25 = bf_result.loc["25%", :]
    bf_p50 = bf_result.loc["50%", :]
    bf_p75 = bf_result.loc["75%", :]
    bf_max = bf_result.loc["max", :]

    # Reindex results with the specified keys and their order, because
    # the relative order is not important.
    bf_result = bf_result.reindex(["count", "nunique", "mean", "std", "min", "max"])
    pd_result = pd_result.reindex(
        ["count", "unique", "mean", "std", "min", "max"]
        # BF counter part of "unique" is called "nunique"
    ).rename(index={"unique": "nunique"})

    pandas.testing.assert_frame_equal(
        pd_result[numeric_columns].astype("Float64"),
        bf_result[numeric_columns],
        check_index_type=False,
    )

    pandas.testing.assert_frame_equal(
        pd_result[non_numeric_columns].astype("Int64"),
        bf_result[non_numeric_columns],
        check_index_type=False,
    )

    # Double-check that quantiles are at least plausible.
    assert (
        (bf_min <= bf_p25)
        & (bf_p25 <= bf_p50)
        & (bf_p50 <= bf_p50)
        & (bf_p75 <= bf_max)
    ).all()


def test_series_describe_numeric(scalars_dfs):
    target_col = "int64_col"
    bf_df, pd_df = scalars_dfs
    bf_s, pd_s = bf_df[target_col], pd_df[target_col]

    bf_result = (
        bf_s.describe()
        .to_pandas()
        .reindex(["count", "nunique", "mean", "std", "min", "max"])
    )
    pd_result = (
        pd_s.describe()
        .reindex(["count", "unique", "mean", "std", "min", "max"])
        .rename(index={"unique": "nunique"})
    )

    pandas.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_dtype=False,
        check_index_type=False,
    )


def test_series_describe_non_numeric(scalars_dfs):
    target_col = "string_col"
    bf_df, pd_df = scalars_dfs
    bf_s, pd_s = bf_df[target_col], pd_df[target_col]

    bf_result = bf_s.describe().to_pandas().reindex(["count", "nunique"])
    pd_result = (
        pd_s.describe().reindex(["count", "unique"]).rename(index={"unique": "nunique"})
    )

    pandas.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_dtype=False,
        check_index_type=False,
    )


def test_series_describe_temporal(scalars_dfs):
    # Pandas returns <NA> for unique timestamps only after 2.1.0
    pytest.importorskip("pandas", minversion="2.1.0")
    target_col = "timestamp_col"
    bf_df, pd_df = scalars_dfs
    bf_s, pd_s = bf_df[target_col], pd_df[target_col]

    bf_result = bf_s.describe().to_pandas().reindex(["count", "nunique"])
    pd_result = (
        pd_s.describe().reindex(["count", "unique"]).rename(index={"unique": "nunique"})
    )

    pandas.testing.assert_series_equal(
        bf_result,
        pd_result,
        check_dtype=False,
        check_index_type=False,
    )
