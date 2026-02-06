# Copyright 2026 Google LLC
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

import operator
import pathlib
from typing import Generator

import pandas as pd
import pytest

import bigframes
import bigframes.pandas as bpd
from bigframes.testing.utils import assert_frame_equal, convert_pandas_dtypes

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="3.0.0")


CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"


@pytest.fixture(scope="module", autouse=True)
def session() -> Generator[bigframes.Session, None, None]:
    import bigframes.core.global_session
    from bigframes.testing import polars_session

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
def scalars_df_2_index(
    session: bigframes.Session, scalars_pandas_df_index
) -> bpd.DataFrame:
    return session.read_pandas(scalars_pandas_df_index)


@pytest.fixture(scope="module")
def scalars_dfs(
    scalars_df_index,
    scalars_pandas_df_index,
):
    return scalars_df_index, scalars_pandas_df_index


@pytest.mark.parametrize(
    ("op",),
    [
        (operator.invert,),
    ],
)
def test_pd_col_unary_operators(scalars_dfs, op):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_kwargs = {
        "result": op(bpd.col("float64_col")),
    }
    pd_kwargs = {
        "result": op(pd.col("float64_col")),  # type: ignore
    }
    df = scalars_df.assign(**bf_kwargs)

    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**pd_kwargs)

    assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("op",),
    [
        (operator.add,),
        (operator.sub,),
        (operator.mul,),
        (operator.truediv,),
        (operator.floordiv,),
        (operator.gt,),
        (operator.lt,),
        (operator.ge,),
        (operator.le,),
        (operator.eq,),
        (operator.mod,),
    ],
)
def test_pd_col_binary_operators(scalars_dfs, op):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_kwargs = {
        "result": op(bpd.col("float64_col"), 2.4),
        "reverse_result": op(2.4, bpd.col("float64_col")),
    }
    pd_kwargs = {
        "result": op(pd.col("float64_col"), 2.4),  # type: ignore
        "reverse_result": op(2.4, pd.col("float64_col")),  # type: ignore
    }
    df = scalars_df.assign(**bf_kwargs)

    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**pd_kwargs)

    assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("op",),
    [
        (operator.and_,),
        (operator.or_,),
        (operator.xor,),
    ],
)
def test_pd_col_binary_bool_operators(scalars_dfs, op):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_kwargs = {
        "result": op(bpd.col("bool_col"), True),
        "reverse_result": op(False, bpd.col("bool_col")),
    }
    pd_kwargs = {
        "result": op(pd.col("bool_col"), True),  # type: ignore
        "reverse_result": op(False, pd.col("bool_col")),  # type: ignore
    }
    df = scalars_df.assign(**bf_kwargs)

    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**pd_kwargs)

    assert_frame_equal(bf_result, pd_result)
