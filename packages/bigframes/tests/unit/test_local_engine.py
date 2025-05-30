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

import pandas as pd
import pandas.testing
import pyarrow as pa
import pytest

import bigframes
import bigframes.pandas as bpd

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="2.0.0")


# All tests in this file require polars to be installed to pass.
@pytest.fixture(scope="module")
def polars_session():
    from bigframes.testing import polars_session

    return polars_session.TestSession()


@pytest.fixture(scope="module")
def small_inline_frame() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "int1": pd.Series([1, 2, 3], dtype="Int64"),
            "int2": pd.Series([-10, 20, 30], dtype="Int64"),
            "bools": pd.Series([True, None, False], dtype="boolean"),
            "strings": pd.Series(["b", "aa", "ccc"], dtype="string[pyarrow]"),
            "intLists": pd.Series(
                [[1, 2, 3], [4, 5, 6, 7], []],
                dtype=pd.ArrowDtype(pa.list_(pa.int64())),
            ),
        },
    )
    df.index = df.index.astype("Int64")
    return df


def test_polars_local_engine_add(
    small_inline_frame: pd.DataFrame, polars_session: bigframes.Session
):
    pd_df = small_inline_frame
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = (bf_df["int1"] + bf_df["int2"]).to_pandas()
    pd_result = pd_df.int1 + pd_df.int2
    pandas.testing.assert_series_equal(bf_result, pd_result)


def test_polars_local_engine_order_by(small_inline_frame: pd.DataFrame, polars_session):
    pd_df = small_inline_frame
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.sort_values("strings").to_pandas()
    pd_result = pd_df.sort_values("strings")
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_polars_local_engine_filter(small_inline_frame: pd.DataFrame, polars_session):
    pd_df = small_inline_frame
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.filter(bf_df["int2"] >= 1).to_pandas()
    pd_result = pd_df.filter(pd_df["int2"] >= 1)  # type: ignore
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_polars_local_engine_series_rename_with_mapping(polars_session):
    pd_series = pd.Series(
        ["a", "b", "c"], index=[1, 2, 3], dtype="string[pyarrow]", name="test_name"
    )
    bf_series = bpd.Series(pd_series, session=polars_session)

    bf_result = bf_series.rename({1: 100, 2: 200, 3: 300}).to_pandas()
    pd_result = pd_series.rename({1: 100, 2: 200, 3: 300})
    # pd default index is int64, bf is Int64
    pandas.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_polars_local_engine_series_rename_with_mapping_inplace(polars_session):
    pd_series = pd.Series(
        ["a", "b", "c"], index=[1, 2, 3], dtype="string[pyarrow]", name="test_name"
    )
    bf_series = bpd.Series(pd_series, session=polars_session)

    pd_series.rename({1: 100, 2: 200, 3: 300}, inplace=True)
    assert bf_series.rename({1: 100, 2: 200, 3: 300}, inplace=True) is None

    bf_result = bf_series.to_pandas()
    pd_result = pd_series
    # pd default index is int64, bf is Int64
    pandas.testing.assert_series_equal(bf_result, pd_result, check_index_type=False)


def test_polars_local_engine_reset_index(
    small_inline_frame: pd.DataFrame, polars_session
):
    pd_df = small_inline_frame
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.reset_index().to_pandas()
    pd_result = pd_df.reset_index()
    # pd default index is int64, bf is Int64
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_index_type=False)


def test_polars_local_engine_join_binop(polars_session):
    pd_df_1 = pd.DataFrame({"colA": [1, None, 3], "colB": [3, 1, 2]}, index=[1, 2, 3])
    pd_df_2 = pd.DataFrame(
        {"colA": [100, 200, 300], "colB": [30, 10, 40]}, index=[2, 1, 4]
    )
    bf_df_1 = bpd.DataFrame(pd_df_1, session=polars_session)
    bf_df_2 = bpd.DataFrame(pd_df_2, session=polars_session)

    bf_result = (bf_df_1 + bf_df_2).to_pandas()
    pd_result = pd_df_1 + pd_df_2
    # Sort since different join ordering
    pandas.testing.assert_frame_equal(
        bf_result.sort_index(),
        pd_result.sort_index(),
        check_dtype=False,
        check_index_type=False,
    )


@pytest.mark.parametrize(
    "join_type",
    ["inner", "left", "right", "outer"],
)
def test_polars_local_engine_joins(join_type, polars_session):
    pd_df_1 = pd.DataFrame(
        {"colA": [1, None, 3], "colB": [3, 1, 2]}, index=[1, 2, 3], dtype="Int64"
    )
    pd_df_2 = pd.DataFrame(
        {"colC": [100, 200, 300], "colD": [30, 10, 40]}, index=[2, 1, 4], dtype="Int64"
    )
    bf_df_1 = bpd.DataFrame(pd_df_1, session=polars_session)
    bf_df_2 = bpd.DataFrame(pd_df_2, session=polars_session)

    bf_result = bf_df_1.join(bf_df_2, how=join_type).to_pandas()
    pd_result = pd_df_1.join(pd_df_2, how=join_type)
    # Sort by index because ordering logic isn't same as pandas
    pandas.testing.assert_frame_equal(
        bf_result.sort_index(), pd_result.sort_index(), check_index_type=False
    )


def test_polars_local_engine_agg(polars_session):
    pd_df = pd.DataFrame(
        {"colA": [True, False, True, False, True], "colB": [1, 2, 3, 4, 5]}
    )
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.agg(["sum", "count"]).to_pandas()
    pd_result = pd_df.agg(["sum", "count"])
    # local engine appears to produce uint32
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False, check_index_type=False)  # type: ignore


def test_polars_local_engine_groupby_sum(polars_session):
    pd_df = pd.DataFrame(
        {"colA": [True, False, True, False, True], "colB": [1, 2, 3, 4, 5]}
    )
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.groupby("colA").sum().to_pandas()
    pd_result = pd_df.groupby("colA").sum()
    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


def test_polars_local_engine_cumsum(small_inline_frame, polars_session):
    pd_df = small_inline_frame[["int1", "int2"]]
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.cumsum().to_pandas()
    pd_result = pd_df.cumsum()
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_polars_local_engine_explode(small_inline_frame, polars_session):
    pd_df = small_inline_frame
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.explode(["intLists"]).to_pandas()
    pd_result = pd_df.explode(["intLists"])
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("start", "stop", "step"),
    [
        (1, None, None),
        (None, 4, None),
        (None, None, 2),
        (None, 50_000_000_000, 1),
        (5, 4, None),
        (3, None, 2),
        (1, 7, 2),
        (1, 7, 50_000_000_000),
        (-1, -7, -2),
        (None, -7, -2),
        (-1, None, -2),
        (-7, -1, 2),
        (-7, -1, None),
        (-7, 7, None),
        (7, -7, -2),
    ],
)
def test_polars_local_engine_slice(
    small_inline_frame, polars_session, start, stop, step
):
    pd_df = small_inline_frame
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    bf_result = bf_df.iloc[start:stop:step].to_pandas()
    pd_result = pd_df.iloc[start:stop:step]
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)
