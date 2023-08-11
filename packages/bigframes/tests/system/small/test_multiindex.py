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

import pandas
import pytest

import bigframes.pandas as bpd
from tests.system.utils import assert_pandas_df_equal_ignore_ordering


def test_set_multi_index(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index(["bool_col", "int64_too"]).to_pandas()
    pd_result = scalars_pandas_df_index.set_index(["bool_col", "int64_too"])

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_reset_multi_index(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index.set_index(["bool_col", "int64_too"]).reset_index().to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(
        ["bool_col", "int64_too"]
    ).reset_index()

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pandas.Int64Dtype())

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_binop_series_series_matching_multi_indices(
    scalars_df_index, scalars_pandas_df_index
):
    bf_left = scalars_df_index.set_index(["bool_col", "string_col"])
    bf_right = scalars_df_index.set_index(["bool_col", "string_col"])
    pd_left = scalars_pandas_df_index.set_index(["bool_col", "string_col"])
    pd_right = scalars_pandas_df_index.set_index(["bool_col", "string_col"])

    bf_result = bf_left["int64_col"] + bf_right["int64_too"]
    pd_result = pd_left["int64_col"] + pd_right["int64_too"]

    pandas.testing.assert_series_equal(
        bf_result.sort_index().to_pandas(), pd_result.sort_index()
    )


def test_binop_df_series_matching_multi_indices(
    scalars_df_index, scalars_pandas_df_index
):
    bf_left = scalars_df_index.set_index(["bool_col", "string_col"])
    bf_right = scalars_df_index.set_index(["bool_col", "string_col"])
    pd_left = scalars_pandas_df_index.set_index(["bool_col", "string_col"])
    pd_right = scalars_pandas_df_index.set_index(["bool_col", "string_col"])

    bf_result = bf_left[["int64_col", "int64_too"]].add(bf_right["int64_too"], axis=0)
    pd_result = pd_left[["int64_col", "int64_too"]].add(pd_right["int64_too"], axis=0)

    pandas.testing.assert_frame_equal(
        bf_result.sort_index().to_pandas(), pd_result.sort_index()
    )


def test_binop_multi_index_mono_index(scalars_df_index, scalars_pandas_df_index):
    bf_left = scalars_df_index.set_index(["bool_col", "rowindex_2"])
    bf_right = scalars_df_index.set_index("rowindex_2")
    pd_left = scalars_pandas_df_index.set_index(["bool_col", "rowindex_2"])
    pd_right = scalars_pandas_df_index.set_index("rowindex_2")

    bf_result = bf_left["int64_col"] + bf_right["int64_too"]
    pd_result = pd_left["int64_col"] + pd_right["int64_too"]

    pandas.testing.assert_series_equal(bf_result.to_pandas(), pd_result)


def test_binop_overlapping_multi_indices(scalars_df_index, scalars_pandas_df_index):
    bf_left = scalars_df_index.set_index(["bool_col", "int64_too"])
    bf_right = scalars_df_index.set_index(["bool_col", "int64_col"])
    pd_left = scalars_pandas_df_index.set_index(["bool_col", "int64_too"])
    pd_right = scalars_pandas_df_index.set_index(["bool_col", "int64_col"])

    bf_result = bf_left["int64_col"] + bf_right["int64_too"]
    pd_result = pd_left["int64_col"] + pd_right["int64_too"]

    pandas.testing.assert_series_equal(
        bf_result.sort_index().to_pandas(), pd_result.sort_index()
    )


def test_concat_compatible_multi_indices(scalars_df_index, scalars_pandas_df_index):
    if pandas.__version__.startswith("1."):
        pytest.skip("Labels not preserved in pandas 1.x.")
    bf_left = scalars_df_index.set_index(["bool_col", "int64_col"])
    bf_right = scalars_df_index.set_index(["bool_col", "int64_too"])
    pd_left = scalars_pandas_df_index.set_index(["bool_col", "int64_col"])
    pd_right = scalars_pandas_df_index.set_index(["bool_col", "int64_too"])

    bf_result = bpd.concat([bf_left, bf_right])
    pd_result = pandas.concat([pd_left, pd_right])

    pandas.testing.assert_frame_equal(bf_result.to_pandas(), pd_result)


def test_concat_multi_indices_ignore_index(scalars_df_index, scalars_pandas_df_index):
    bf_left = scalars_df_index.set_index(["bool_col", "int64_too"])
    bf_right = scalars_df_index.set_index(["bool_col", "int64_col"])
    pd_left = scalars_pandas_df_index.set_index(["bool_col", "int64_too"])
    pd_right = scalars_pandas_df_index.set_index(["bool_col", "int64_col"])

    bf_result = bpd.concat([bf_left, bf_right], ignore_index=True)
    pd_result = pandas.concat([pd_left, pd_right], ignore_index=True)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pandas.Int64Dtype())

    pandas.testing.assert_frame_equal(bf_result.to_pandas(), pd_result)


def test_multi_index_loc(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "bool_col"]).loc[[2, 0]].to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(["int64_too", "bool_col"]).loc[[2, 0]]

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_multi_index_getitem_bool(scalars_df_index, scalars_pandas_df_index):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col"])

    bf_result = bf_frame[bf_frame["int64_col"] > 0].to_pandas()
    pd_result = pd_frame[pd_frame["int64_col"] > 0]

    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("level"),
    [
        (1),
        ("int64_too"),
        ([0, 2]),
        ([2, "bool_col"]),
    ],
    ids=["level_num", "level_name", "list", "mixed_list"],
)
def test_multi_index_droplevel(scalars_df_index, scalars_pandas_df_index, level):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame.droplevel(level).to_pandas()
    pd_result = pd_frame.droplevel(level)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("labels", "level"),
    [
        (1, 0),
        ([0, 1], 0),
        ([True, None], 1),
    ],
)
def test_multi_index_drop(scalars_df_index, scalars_pandas_df_index, labels, level):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame.drop(labels=labels, axis="index", level=level).to_pandas()
    pd_result = pd_frame.drop(labels=labels, axis="index", level=level)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("order"),
    [
        (1, 0, 2),
        (["int64_col", "bool_col", "int64_too"]),
        (["int64_col", "bool_col", 0]),
    ],
    ids=[
        "level_nums",
        "level_names",
        "num_names_mixed",
    ],
)
def test_multi_index_reorder_levels(scalars_df_index, scalars_pandas_df_index, order):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame.reorder_levels(order).to_pandas()
    pd_result = pd_frame.reorder_levels(order)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_multi_index_series_groupby(scalars_df_index, scalars_pandas_df_index):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col"])
    bf_result = (
        bf_frame["float64_col"]
        .groupby([bf_frame.int64_col % 2, "bool_col"])
        .mean()
        .to_pandas()
    )
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col"])
    pd_result = (
        pd_frame["float64_col"].groupby([pd_frame.int64_col % 2, "bool_col"]).mean()
    )

    pandas.testing.assert_series_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("level"),
    [
        (1),
        ([0]),
        (["bool_col"]),
        (["bool_col", "int64_too"]),
    ],
)
def test_multi_index_series_groupby_level(
    scalars_df_index, scalars_pandas_df_index, level
):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "bool_col"])["float64_col"]
        .groupby(level=level)
        .mean()
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.set_index(["int64_too", "bool_col"])["float64_col"]
        .groupby(level=level)
        .mean()
    )

    pandas.testing.assert_series_equal(bf_result, pd_result)


def test_multi_index_dataframe_groupby(scalars_df_index, scalars_pandas_df_index):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col"])
    bf_result = (
        bf_frame.groupby([bf_frame.int64_col % 2, "bool_col"])
        .mean(numeric_only=True)
        .to_pandas()
    )
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col"])
    pd_result = pd_frame.groupby([pd_frame.int64_col % 2, "bool_col"]).mean(
        numeric_only=True
    )

    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("level", "as_index"),
    [
        (1, True),
        ([0], False),
        (["bool_col"], True),
        (["bool_col", "int64_too"], False),
    ],
)
def test_multi_index_dataframe_groupby_level_aggregate(
    scalars_df_index, scalars_pandas_df_index, level, as_index
):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "bool_col"])
        .groupby(level=level, as_index=as_index)
        .mean(numeric_only=True)
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.set_index(["int64_too", "bool_col"])
        .groupby(level=level, as_index=as_index)
        .mean(numeric_only=True)
    )

    # Pandas will have int64 index, while bigquery will have Int64 when resetting
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_index_type=False)


@pytest.mark.parametrize(
    ("level", "as_index"),
    [
        (1, True),
        ([0], False),
        (
            ["bool_col"],
            True,
        ),
        (["bool_col", "int64_too"], False),
    ],
)
def test_multi_index_dataframe_groupby_level_analytic(
    scalars_df_index, scalars_pandas_df_index, level, as_index
):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "bool_col"])
        .groupby(level=level, as_index=as_index, dropna=False)
        .cumsum(numeric_only=True)
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.set_index(["int64_too", "bool_col"])
        .groupby(level=level, as_index=as_index, dropna=False)
        .cumsum(numeric_only=True)
    )

    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


all_joins = pytest.mark.parametrize(
    ("how",),
    (
        ("outer",),
        ("left",),
        ("right",),
        ("inner",),
    ),
)


@all_joins
# Both DFs are multi-index
def test_multi_index_dataframe_join(scalars_dfs, how):
    bf_df, pd_df = scalars_dfs

    bf_df_a = bf_df.set_index((["bool_col", "rowindex_2"]))[["string_col", "int64_col"]]
    bf_df_b = bf_df.assign(rowindex_2=bf_df["rowindex_2"] + 2).set_index(
        (["bool_col", "rowindex_2"])
    )[["float64_col"]]
    bf_result = bf_df_a.join(bf_df_b, how=how).to_pandas()

    pd_df_a = pd_df.set_index((["bool_col", "rowindex_2"]))[["string_col", "int64_col"]]
    pd_df_b = pd_df.assign(rowindex_2=pd_df["rowindex_2"] + 2).set_index(
        (["bool_col", "rowindex_2"])
    )[["float64_col"]]
    pd_result = pd_df_a.join(pd_df_b, how=how)
    assert_pandas_df_equal_ignore_ordering(bf_result, pd_result)


@all_joins
# Only left DF is multi-index
def test_multi_index_dataframe_join_on(scalars_dfs, how):
    bf_df, pd_df = scalars_dfs

    bf_df_a = bf_df.set_index((["int64_too", "bool_col"]))[
        ["string_col", "int64_col", "rowindex_2"]
    ]
    bf_df_a = bf_df_a.assign(rowindex_2=bf_df_a["rowindex_2"] + 2)
    bf_df_b = bf_df[["float64_col"]]
    bf_result = bf_df_a.join(bf_df_b, on="rowindex_2", how=how).to_pandas()

    pd_df_a = pd_df.set_index((["int64_too", "bool_col"]))[
        ["string_col", "int64_col", "rowindex_2"]
    ]
    pd_df_a = pd_df_a.assign(rowindex_2=pd_df_a["rowindex_2"] + 2)
    pd_df_b = pd_df[["float64_col"]]
    pd_result = pd_df_a.join(pd_df_b, on="rowindex_2", how=how)
    assert_pandas_df_equal_ignore_ordering(bf_result, pd_result)


@pytest.mark.parametrize(
    ("level",),
    [
        (1,),
        ([0],),
        (["bool_col"],),
        (["bool_col", "int64_too"],),
    ],
)
def test_multi_index_series_groupby_level_aggregate(
    scalars_df_index, scalars_pandas_df_index, level
):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "bool_col"])["float64_col"]
        .groupby(level=level)
        .mean()
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.set_index(["int64_too", "bool_col"])["float64_col"]
        .groupby(level=level)
        .mean()
    )

    pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("level",),
    [
        (1,),
        ([0],),
        (["bool_col"],),
        (["bool_col", "int64_too"],),
    ],
)
def test_multi_index_series_groupby_level_analytic(
    scalars_df_index, scalars_pandas_df_index, level
):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "bool_col"])["float64_col"]
        .groupby(level=level, dropna=False)
        .cumsum()
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.set_index(["int64_too", "bool_col"])["float64_col"]
        .groupby(level=level, dropna=False)
        .cumsum()
    )

    pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)


def test_multi_index_series_rename_dict_same_type(
    scalars_df_index, scalars_pandas_df_index
):
    bf_result = (
        scalars_df_index.set_index(["rowindex_2", "int64_too"])["string_col"]
        .rename({1: 100, 2: 200})
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(["rowindex_2", "int64_too"])[
        "string_col"
    ].rename({1: 100, 2: 200})

    pandas.testing.assert_series_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )
