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

from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

import bigframes
import bigframes.pandas as bpd

CURRENT_DIR = Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"


@pytest.fixture(scope="module")
def scalars_pandas_df_index():
    df = pd.read_json(
        DATA_DIR / "scalars.jsonl",
        lines=True,
    )
    from bigframes.testing.utils import convert_pandas_dtypes

    convert_pandas_dtypes(df, bytes_col=True)

    df = df.set_index("rowindex", drop=False)
    df.index.name = None
    return df.set_index("rowindex").sort_index()


@pytest.fixture(scope="module", autouse=True)
def session():
    import bigframes.core.global_session
    from bigframes.testing import polars_session

    with bpd.option_context("experiments.enable_python_transpiler", True):
        session = polars_session.TestSession()
        with bigframes.core.global_session._GlobalSessionContext(session):
            yield session


@pytest.fixture(scope="module")
def scalars_df_index(
    session: bigframes.Session, scalars_pandas_df_index
) -> bpd.DataFrame:
    return session.read_pandas(scalars_pandas_df_index)


# Tests for groupby.agg custom lambdas


def test_series_groupby_agg_transpile(scalars_df_index, scalars_pandas_df_index):
    def custom_agg(s):
        return s.sum() - s.mean()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(subset=["int64_col", "bool_col"])

    bf_result = bf_df.groupby("bool_col")["int64_col"].agg(custom_agg).to_pandas()
    pd_result = pd_df.groupby("bool_col")["int64_col"].agg(custom_agg)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_dataframe_groupby_agg_func_transpile(
    scalars_df_index, scalars_pandas_df_index
):
    def custom_agg(s):
        return (s.max() - s.min()) / s.count()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "int64_too", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "bool_col"]
    )

    bf_result = (
        bf_df[["int64_col", "int64_too", "bool_col"]]
        .groupby("bool_col")
        .agg(custom_agg)
        .to_pandas()
    )
    pd_result = (
        pd_df[["int64_col", "int64_too", "bool_col"]]
        .groupby("bool_col")
        .agg(custom_agg)
    )

    assert_frame_equal(bf_result, pd_result, check_dtype=False)


def test_dataframe_groupby_agg_dict_transpile(
    scalars_df_index, scalars_pandas_df_index
):
    def custom_agg1(s):
        return s.sum() - s.mean()

    def custom_agg2(s):
        return s.max() - s.min()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "int64_too", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "bool_col"]
    )

    bf_result = (
        bf_df.groupby("bool_col")
        .agg({"int64_col": custom_agg1, "int64_too": custom_agg2})
        .to_pandas()
    )
    pd_result = pd_df.groupby("bool_col").agg(
        {"int64_col": custom_agg1, "int64_too": custom_agg2}
    )

    assert_frame_equal(bf_result, pd_result, check_dtype=False)


def test_dataframe_groupby_agg_list_transpile(
    scalars_df_index, scalars_pandas_df_index
):
    def custom_agg1(s):
        return s.sum() - s.mean()

    def custom_agg2(s):
        return s.max() - s.min()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(subset=["int64_col", "bool_col"])

    bf_result = (
        bf_df[["int64_col", "bool_col"]]
        .groupby("bool_col")
        .agg([custom_agg1, custom_agg2])
        .to_pandas()
    )
    pd_result = (
        pd_df[["int64_col", "bool_col"]]
        .groupby("bool_col")
        .agg([custom_agg1, custom_agg2])
    )

    assert_frame_equal(bf_result, pd_result, check_dtype=False)


# Tests for groupby.transform broadcasting lambdas


def test_series_groupby_transform_transpile(scalars_df_index, scalars_pandas_df_index):
    def custom_transform(s):
        return s - s.mean()

    bf_df = scalars_df_index.dropna(subset=["int64_col", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(subset=["int64_col", "bool_col"])

    bf_result = (
        bf_df.groupby("bool_col")["int64_col"].transform(custom_transform).to_pandas()
    )
    pd_result = pd_df.groupby("bool_col")["int64_col"].transform(custom_transform)

    assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_dataframe_groupby_transform_transpile(
    scalars_df_index, scalars_pandas_df_index
):
    def custom_transform(s):
        return (s - s.min()) / (s.max() - s.min())

    bf_df = scalars_df_index.dropna(subset=["int64_col", "int64_too", "bool_col"])
    pd_df = scalars_pandas_df_index.dropna(
        subset=["int64_col", "int64_too", "bool_col"]
    )

    bf_result = (
        bf_df[["int64_col", "int64_too", "bool_col"]]
        .groupby("bool_col")
        .transform(custom_transform)
        .to_pandas()
    )
    pd_result = (
        pd_df[["int64_col", "int64_too", "bool_col"]]
        .groupby("bool_col")
        .transform(custom_transform)
    )

    assert_frame_equal(bf_result, pd_result, check_dtype=False)


# Rejection / unsupported apply test


def test_groupby_apply_raises(scalars_df_index):
    with pytest.raises(
        NotImplementedError,
        match="SeriesGroupBy.apply is not implemented",
    ):
        scalars_df_index.groupby("bool_col")["int64_col"].apply(lambda s: s.sum())

    with pytest.raises(
        NotImplementedError,
        match="DataFrameGroupBy.apply is not implemented",
    ):
        scalars_df_index.groupby("bool_col").apply(lambda df: df.int64_col.sum())
