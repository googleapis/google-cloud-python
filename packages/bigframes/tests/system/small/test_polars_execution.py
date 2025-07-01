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
import pytest

import bigframes
from bigframes.testing.utils import assert_pandas_df_equal

polars = pytest.importorskip("polars", reason="polars is required for this test")


@pytest.fixture(scope="module")
def session_w_polars():
    context = bigframes.BigQueryOptions(location="US", enable_polars_execution=True)
    session = bigframes.Session(context=context)
    yield session
    session.close()  # close generated session at cleanup time


def test_polar_execution_sorted(session_w_polars, scalars_pandas_df_index):
    execution_count_before = session_w_polars._metrics.execution_count
    bf_df = session_w_polars.read_pandas(scalars_pandas_df_index)

    pd_result = scalars_pandas_df_index.sort_index(ascending=False)[
        ["int64_too", "bool_col"]
    ]
    bf_result = bf_df.sort_index(ascending=False)[["int64_too", "bool_col"]].to_pandas()

    assert session_w_polars._metrics.execution_count == execution_count_before
    assert_pandas_df_equal(bf_result, pd_result)


def test_polar_execution_sorted_filtered(session_w_polars, scalars_pandas_df_index):
    execution_count_before = session_w_polars._metrics.execution_count
    bf_df = session_w_polars.read_pandas(scalars_pandas_df_index)

    pd_result = scalars_pandas_df_index.sort_index(ascending=False).dropna(
        subset=["int64_col", "string_col"]
    )
    bf_result = (
        bf_df.sort_index(ascending=False)
        .dropna(subset=["int64_col", "string_col"])
        .to_pandas()
    )

    assert session_w_polars._metrics.execution_count == execution_count_before
    assert_pandas_df_equal(bf_result, pd_result)


def test_polar_execution_unsupported_sql_fallback(
    session_w_polars, scalars_pandas_df_index
):
    execution_count_before = session_w_polars._metrics.execution_count
    bf_df = session_w_polars.read_pandas(scalars_pandas_df_index)

    pd_df = scalars_pandas_df_index.copy()
    pd_df["str_len_col"] = pd_df.string_col.str.len()
    pd_result = pd_df

    bf_df["str_len_col"] = bf_df.string_col.str.len()
    bf_result = bf_df.to_pandas()

    # str len not supported by polar engine yet, so falls back to bq execution
    assert session_w_polars._metrics.execution_count == (execution_count_before + 1)
    assert_pandas_df_equal(bf_result, pd_result)
