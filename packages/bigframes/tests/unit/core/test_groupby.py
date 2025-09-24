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

import pandas as pd
import pandas.testing
import pytest

import bigframes.core.utils as utils
import bigframes.pandas as bpd

pytest.importorskip("polars")
pytest.importorskip("pandas", minversion="2.0.0")


def test_groupby_df_iter_by_key_singular(polars_session):
    pd_df = pd.DataFrame({"colA": ["a", "a", "b", "c", "c"], "colB": [1, 2, 3, 4, 5]})
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    for bf_group, pd_group in zip(bf_df.groupby("colA"), pd_df.groupby("colA")):  # type: ignore
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_df_iter_by_key_list(polars_session):
    pd_df = pd.DataFrame({"colA": ["a", "a", "b", "c", "c"], "colB": [1, 2, 3, 4, 5]})
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    for bf_group, pd_group in zip(bf_df.groupby(["colA"]), pd_df.groupby(["colA"])):  # type: ignore
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_df_iter_by_key_list_multiple(polars_session):
    pd_df = pd.DataFrame(
        {
            "colA": ["a", "a", "b", "c", "c"],
            "colB": [1, 2, 3, 4, 5],
            "colC": [True, False, True, False, True],
        }
    )
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    for bf_group, pd_group in zip(  # type: ignore
        bf_df.groupby(["colA", "colB"]), pd_df.groupby(["colA", "colB"])
    ):
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_df_iter_by_level_singular(polars_session):
    pd_df = pd.DataFrame(
        {"colA": ["a", "a", "b", "c", "c"], "colB": [1, 2, 3, 4, 5]}
    ).set_index("colA")
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    for bf_group, pd_group in zip(bf_df.groupby(level=0), pd_df.groupby(level=0)):  # type: ignore
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_df_iter_by_level_list_one_item(polars_session):
    pd_df = pd.DataFrame(
        {"colA": ["a", "a", "b", "c", "c"], "colB": [1, 2, 3, 4, 5]}
    ).set_index("colA")
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    for bf_group, pd_group in zip(bf_df.groupby(level=[0]), pd_df.groupby(level=[0])):  # type: ignore
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group

        # In pandas 2.x, we get a warning from pandas: "Creating a Groupby
        # object with a length-1 list-like level parameter will yield indexes
        # as tuples in a future version. To keep indexes as scalars, create
        # Groupby objects with a scalar level parameter instead.
        if utils.is_list_like(pd_key):
            assert bf_key == tuple(pd_key)
        else:
            assert bf_key == (pd_key,)
        pandas.testing.assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_df_iter_by_level_list_multiple(polars_session):
    pd_df = pd.DataFrame(
        {
            "colA": ["a", "a", "b", "c", "c"],
            "colB": [1, 2, 3, 4, 5],
            "colC": [True, False, True, False, True],
        }
    ).set_index(["colA", "colB"])
    bf_df = bpd.DataFrame(pd_df, session=polars_session)

    for bf_group, pd_group in zip(  # type: ignore
        bf_df.groupby(level=[0, 1]), pd_df.groupby(level=[0, 1])
    ):
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_frame_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_series_iter_by_level_singular(polars_session):
    series_index = ["a", "a", "b"]
    pd_series = pd.Series([1, 2, 3], index=series_index)
    bf_series = bpd.Series(pd_series, session=polars_session)
    bf_series.name = pd_series.name

    for bf_group, pd_group in zip(  # type: ignore
        bf_series.groupby(level=0), pd_series.groupby(level=0)
    ):
        bf_key, bf_group_series = bf_group
        bf_result = bf_group_series.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_series_iter_by_level_list_one_item(polars_session):
    series_index = ["a", "a", "b"]
    pd_series = pd.Series([1, 2, 3], index=series_index)
    bf_series = bpd.Series(pd_series, session=polars_session)
    bf_series.name = pd_series.name

    for bf_group, pd_group in zip(  # type: ignore
        bf_series.groupby(level=[0]), pd_series.groupby(level=[0])
    ):
        bf_key, bf_group_series = bf_group
        bf_result = bf_group_series.to_pandas()
        pd_key, pd_result = pd_group

        # In pandas 2.x, we get a warning from pandas: "Creating a Groupby
        # object with a length-1 list-like level parameter will yield indexes
        # as tuples in a future version. To keep indexes as scalars, create
        # Groupby objects with a scalar level parameter instead.
        if utils.is_list_like(pd_key):
            assert bf_key == tuple(pd_key)
        else:
            assert bf_key == (pd_key,)
        pandas.testing.assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_series_iter_by_level_list_multiple(polars_session):
    pd_df = pd.DataFrame(
        {
            "colA": ["a", "a", "b", "c", "c"],
            "colB": [1, 2, 3, 4, 5],
            "colC": [True, False, True, False, True],
        }
    ).set_index(["colA", "colB"])
    pd_series = pd_df["colC"]
    bf_df = bpd.DataFrame(pd_df, session=polars_session)
    bf_series = bf_df["colC"]

    for bf_group, pd_group in zip(  # type: ignore
        bf_series.groupby(level=[0, 1]), pd_series.groupby(level=[0, 1])
    ):
        bf_key, bf_group_df = bf_group
        bf_result = bf_group_df.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_series_iter_by_series(polars_session):
    pd_groups = pd.Series(["a", "a", "b"])
    bf_groups = bpd.Series(pd_groups, session=polars_session)
    pd_series = pd.Series([1, 2, 3])
    bf_series = bpd.Series(pd_series, session=polars_session)
    bf_series.name = pd_series.name

    for bf_group, pd_group in zip(  # type: ignore
        bf_series.groupby(bf_groups), pd_series.groupby(pd_groups)
    ):
        bf_key, bf_group_series = bf_group
        bf_result = bf_group_series.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_series_iter_by_series_list_one_item(polars_session):
    pd_groups = pd.Series(["a", "a", "b"])
    bf_groups = bpd.Series(pd_groups, session=polars_session)
    pd_series = pd.Series([1, 2, 3])
    bf_series = bpd.Series(pd_series, session=polars_session)
    bf_series.name = pd_series.name

    for bf_group, pd_group in zip(  # type: ignore
        bf_series.groupby([bf_groups]), pd_series.groupby([pd_groups])
    ):
        bf_key, bf_group_series = bf_group
        bf_result = bf_group_series.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )


def test_groupby_series_iter_by_series_list_multiple(polars_session):
    pd_group_a = pd.Series(["a", "a", "b", "c", "c"])
    bf_group_a = bpd.Series(pd_group_a, session=polars_session)
    pd_group_b = pd.Series([0, 0, 0, 1, 1])
    bf_group_b = bpd.Series(pd_group_b, session=polars_session)
    pd_series = pd.Series([1, 2, 3, 4, 5])
    bf_series = bpd.Series(pd_series, session=polars_session)
    bf_series.name = pd_series.name

    for bf_group, pd_group in zip(  # type: ignore
        bf_series.groupby([bf_group_a, bf_group_b]),
        pd_series.groupby([pd_group_a, pd_group_b]),
    ):
        bf_key, bf_group_series = bf_group
        bf_result = bf_group_series.to_pandas()
        pd_key, pd_result = pd_group
        assert bf_key == pd_key
        pandas.testing.assert_series_equal(
            bf_result, pd_result, check_dtype=False, check_index_type=False
        )
