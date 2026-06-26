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

import pathlib
from typing import Generator

import pandas as pd
import pandas.testing
import pytest

import bigframes
import bigframes.pandas as bpd
from bigframes.testing.utils import (
    assert_frame_equal,
    assert_series_equal,
    convert_pandas_dtypes,
)

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="2.0.0")

CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"


@pytest.fixture(scope="module", autouse=True)
def session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session
    from bigframes.testing import polars_session

    with bpd.option_context("experiments.enable_python_transpiler", True):
        session = polars_session.TestSession()
        with bigframes.core.global_session._GlobalSessionContext(session):
            yield session


@pytest.fixture(scope="module")
def scalars_pandas_df_index() -> pd.DataFrame:
    """pd.DataFrame pointing at test data."""

    df = pd.read_json(
        DATA_DIR / "scalars.jsonl",
        lines=True,
    )
    convert_pandas_dtypes(df, bytes_col=True)

    df = df.set_index("rowindex", drop=False)
    df.index.name = None
    return df.set_index("rowindex").sort_index()


@pytest.fixture(scope="module")
def scalars_df_index(
    session: bigframes.Session, scalars_pandas_df_index
) -> bpd.DataFrame:
    return session.read_pandas(scalars_pandas_df_index)


@pytest.fixture(scope="module")
def scalars_dfs(
    scalars_df_index,
    scalars_pandas_df_index,
):
    return scalars_df_index, scalars_pandas_df_index


def test_dataframe_map_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input):
        return input * 3 + 12

    bf_result = scalars_df_index[columns].map(foo, na_action="ignore").to_pandas()

    pd_result = (
        scalars_pandas_df_index[columns].map(foo, na_action="ignore").astype("Int64")
    )

    assert_frame_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input):
        return input.int64_too + input.int64_col

    bf_result = scalars_df_index[columns].apply(foo, axis=1).to_pandas()

    pd_result = scalars_pandas_df_index[columns].apply(foo, axis=1).astype("Int64")

    assert_series_equal(bf_result, pd_result)


def test_series_combine_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    def which_smaller(left, right):
        return (left * right) + 3

    bf_result = (
        scalars_df_index["int64_too"]
        .combine(scalars_df_index["int64_col"], which_smaller)
        .to_pandas()
    )

    pd_result = scalars_pandas_df_index["int64_too"].combine(
        scalars_pandas_df_index["int64_col"], which_smaller
    )

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile_with_defaults(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input, x=10, y=5):
        return input.int64_too + input.int64_col + x + y

    bf_result = scalars_df_index[columns].apply(foo, axis=1).to_pandas()
    pd_result = scalars_pandas_df_index[columns].apply(foo, axis=1).astype("Int64")

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile_with_args(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input, x, y=5):
        return input.int64_too + input.int64_col + x + y

    bf_result = (
        scalars_df_index[columns].apply(foo, axis=1, args=(12,), y=20).to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index[columns]
        .apply(foo, axis=1, args=(12,), y=20)
        .astype("Int64")
    )

    assert_series_equal(bf_result, pd_result)


def test_dataframe_apply_axis_1_transpile_invalid_bindings(
    scalars_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(input, x, y=5):
        return input.int64_too + input.int64_col + x + y

    # 1. Unexpected keyword argument
    with pytest.raises(TypeError, match="unexpected keyword argument 'z'"):
        scalars_df_index[columns].apply(foo, axis=1, args=(10,), z=20)

    # 2. Multiple values for keyword argument 'x'
    with pytest.raises(TypeError, match="multiple values for argument 'x'"):
        scalars_df_index[columns].apply(foo, axis=1, args=(10,), x=20)

    # 3. Too many positional arguments
    with pytest.raises(TypeError, match="too many positional arguments"):
        scalars_df_index[columns].apply(foo, axis=1, args=(10, 20, 30))

    # 4. Missing required argument 'x'
    with pytest.raises(TypeError, match="missing a required argument: 'x'"):
        scalars_df_index[columns].apply(foo, axis=1)


def test_series_apply_transpile(
    scalars_df_index,
    scalars_pandas_df_index,
):
    def foo(x, y=10):
        return x * 2 + y

    bf_result = scalars_df_index["int64_col"].apply(foo, args=(5,)).to_pandas()
    pd_result = (
        scalars_pandas_df_index["int64_col"].apply(foo, args=(5,)).astype("Int64")
    )

    assert_series_equal(bf_result, pd_result)


def test_series_apply_transpile_invalid_bindings(
    scalars_df_index,
):
    def foo(x, y):
        return x + y

    # Too many positional args: foo takes 2 args (x, y), we pass self and 2 more args (total 3 positional)
    with pytest.raises(
        TypeError, match="too many positional arguments: expected 2, got 3"
    ):
        scalars_df_index["int64_col"].apply(foo, args=(10, 20))

    # Missing required argument: foo takes 2 args, we only pass self (so y is missing)
    with pytest.raises(TypeError, match="missing required argument: 'y'"):
        scalars_df_index["int64_col"].apply(foo)


def test_transpilation_unsupported_ops_raise(
    scalars_df_index,
):
    def foo_with_if(x):
        if x > 0:
            return x
        return -x

    with pytest.raises(ValueError):
        scalars_df_index["int64_col"].apply(foo_with_if)

    def foo_with_loop(x):
        total = 0
        for i in range(x):
            total += i
        return total

    with pytest.raises(ValueError):
        scalars_df_index["int64_col"].apply(foo_with_loop)
