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
from tests.system.utils import assert_pandas_df_equal


# Row Multi-index tests
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


def test_series_multi_index_idxmin(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index(["bool_col", "int64_too"])[
        "float64_col"
    ].idxmin()
    pd_result = scalars_pandas_df_index.set_index(["bool_col", "int64_too"])[
        "float64_col"
    ].idxmin()

    assert bf_result == pd_result


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
def test_df_multi_index_droplevel(scalars_df_index, scalars_pandas_df_index, level):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame.droplevel(level).to_pandas()
    pd_result = pd_frame.droplevel(level)

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
def test_series_multi_index_droplevel(scalars_df_index, scalars_pandas_df_index, level):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame["string_col"].droplevel(level).to_pandas()
    pd_result = pd_frame["string_col"].droplevel(level)

    pandas.testing.assert_series_equal(bf_result, pd_result)


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
def test_df_multi_index_reorder_levels(
    scalars_df_index, scalars_pandas_df_index, order
):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame.reorder_levels(order).to_pandas()
    pd_result = pd_frame.reorder_levels(order)

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
def test_series_multi_index_reorder_levels(
    scalars_df_index, scalars_pandas_df_index, order
):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame["string_col"].reorder_levels(order).to_pandas()
    pd_result = pd_frame["string_col"].reorder_levels(order)

    pandas.testing.assert_series_equal(bf_result, pd_result)


def test_df_multi_index_swaplevel(scalars_df_index, scalars_pandas_df_index):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame.swaplevel().to_pandas()
    pd_result = pd_frame.swaplevel()

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_series_multi_index_swaplevel(scalars_df_index, scalars_pandas_df_index):
    bf_frame = scalars_df_index.set_index(["int64_too", "bool_col", "int64_col"])
    pd_frame = scalars_pandas_df_index.set_index(["int64_too", "bool_col", "int64_col"])

    bf_result = bf_frame["string_col"].swaplevel(0, 2).to_pandas()
    pd_result = pd_frame["string_col"].swaplevel(0, 2)

    pandas.testing.assert_series_equal(bf_result, pd_result)


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
    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


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
    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


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


def test_multi_index_df_reindex(scalars_df_index, scalars_pandas_df_index):
    new_index = pandas.MultiIndex.from_tuples(
        [(4, "Hello, World!"), (99, "some_new_string")],
        names=["new_index1", "new_index2"],
    )
    bf_result = (
        scalars_df_index.set_index(["rowindex_2", "string_col"])
        .reindex(index=new_index)
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(["rowindex_2", "string_col"]).reindex(
        index=new_index
    )
    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


# Column Multi-index tests


def test_column_multi_index_getitem(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "string_col", "bool_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], columns))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_a = bf_df["a"].to_pandas()
    pd_a = pd_df["a"]
    pandas.testing.assert_frame_equal(bf_a, pd_a)

    bf_b = bf_df["b"].to_pandas()
    pd_b = pd_df["b"]
    pandas.testing.assert_frame_equal(bf_b, pd_b)

    bf_fullkey = bf_df[("a", "int64_too")].to_pandas()
    pd_fullkey = pd_df[("a", "int64_too")]
    pandas.testing.assert_series_equal(bf_fullkey, pd_fullkey)


def test_column_multi_index_concat(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "string_col", "bool_col", "int64_col"]
    multi_columns1 = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "a", "b"], [1, 1, 2, 2])
    )
    multi_columns2 = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "a", "c"], [3, 1, 2, 1])
    )

    bf_df1 = scalars_df_index[columns].copy()
    bf_df1.columns = multi_columns1
    bf_df2 = scalars_df_index[columns].copy()
    bf_df2.columns = multi_columns2

    pd_df1 = scalars_pandas_df_index[columns].copy()
    pd_df1.columns = multi_columns1
    pd_df2 = scalars_pandas_df_index[columns].copy()
    pd_df2.columns = multi_columns2

    bf_result = bpd.concat([bf_df1, bf_df2, bf_df1]).to_pandas()
    pd_result = pandas.concat([pd_df1, pd_df2, pd_df1])

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_column_multi_index_drop(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "string_col", "bool_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], columns))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_a = bf_df.drop(("a", "int64_too"), axis=1).to_pandas()
    pd_a = pd_df.drop(("a", "int64_too"), axis=1)
    pandas.testing.assert_frame_equal(bf_a, pd_a)


@pytest.mark.parametrize(
    ("key",),
    [
        ("a",),
        ("b",),
        ("c",),
    ],
)
def test_column_multi_index_assign(scalars_df_index, scalars_pandas_df_index, key):
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], columns))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    kwargs = {key: 42}
    bf_result = bf_df.assign(**kwargs).to_pandas()
    pd_result = pd_df.assign(**kwargs)

    # Pandas assign results in non-nullable dtype
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


def test_column_multi_index_rename(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.rename(columns={"b": "c"}).to_pandas()
    pd_result = pd_df.rename(columns={"b": "c"})

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_column_multi_index_reset_index(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.reset_index().to_pandas()
    pd_result = pd_df.reset_index()

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pandas.Int64Dtype())
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_column_multi_index_binary_op(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = (bf_df[("a", "a")] + 3).to_pandas()
    pd_result = pd_df[("a", "a")] + 3

    pandas.testing.assert_series_equal(bf_result, pd_result)


def test_column_multi_index_agg(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.agg(["sum", "mean"]).to_pandas()
    pd_result = pd_df.agg(["sum", "mean"])

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_index_type=False)


def test_column_multi_index_prefix_suffix(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.add_prefix("prefixed_").add_suffix("_suffixed").to_pandas()
    pd_result = pd_df.add_prefix("prefixed_").add_suffix("_suffixed")

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_column_multi_index_cumsum(scalars_df_index, scalars_pandas_df_index):
    if pandas.__version__.startswith("1."):
        pytest.skip("pandas 1.x. does not handle nullable ints properly in cumsum")
    columns = ["int64_too", "int64_col", "float64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.cumsum().to_pandas()
    pd_result = pd_df.cumsum()

    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("level",),
    [(["l3", "l1"],), ([-2, -1],), (["l3"],), ("l2",), (-3,)],
)
def test_column_multi_index_stack(level):
    if pandas.__version__.startswith("1.") or pandas.__version__.startswith("2.0"):
        pytest.skip("pandas <2.1 uses different stack implementation")

    level1 = pandas.Index(["b", "a", "b"])
    level2 = pandas.Index(["a", "b", "b"])
    level3 = pandas.Index(["b", "b", "a"])

    multi_columns = pandas.MultiIndex.from_arrays(
        [level1, level2, level3], names=["l1", "l2", "l3"]
    )
    pd_df = pandas.DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        index=[5, 2, None],
        columns=multi_columns,
        dtype="Int64",
    )
    bf_df = bpd.DataFrame(pd_df)

    bf_result = bf_df.stack(level=level).to_pandas()
    # BigFrames emulates future_stack impl
    pd_result = pd_df.stack(level=level, future_stack=True)

    # Pandas produces NaN, where bq dataframes produces pd.NA
    # Column ordering seems to depend on pandas version
    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


def test_column_multi_index_melt():
    if pandas.__version__.startswith("1.") or pandas.__version__.startswith("2.0"):
        pytest.skip("pandas <2.1 uses different stack implementation")

    level1 = pandas.Index(["b", "a", "b"])
    level2 = pandas.Index(["a", "b", "b"])
    level3 = pandas.Index(["b", "b", "a"])

    multi_columns = pandas.MultiIndex.from_arrays(
        [level1, level2, level3], names=["l1", "l2", "l3"]
    )
    pd_df = pandas.DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        index=[5, 2, None],
        columns=multi_columns,
        dtype="Int64",
    )
    bf_df = bpd.DataFrame(pd_df)

    bf_result = bf_df.melt().to_pandas()
    pd_result = pd_df.melt()

    # BigFrames uses different string and int types, but values are identical
    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_index_type=False, check_dtype=False
    )


def test_column_multi_index_unstack(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "rowindex_2"]
    level1 = pandas.Index(["b", "a", "b"], dtype="string[pyarrow]")
    # Need resulting column to be pyarrow string rather than object dtype
    level2 = pandas.Index(["a", "b", "b"], dtype="string[pyarrow]")
    multi_columns = pandas.MultiIndex.from_arrays([level1, level2])
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.unstack().to_pandas()
    # Shifting sort behavior in stack
    pd_result = pd_df.unstack()

    # Pandas produces NaN, where bq dataframes produces pd.NA
    # Column ordering seems to depend on pandas version
    pandas.testing.assert_series_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.skip(reason="Pandas fails in newer versions.")
def test_column_multi_index_w_na_stack(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "rowindex_2"]
    level1 = pandas.Index(["b", pandas.NA, pandas.NA])
    # Need resulting column to be pyarrow string rather than object dtype
    level2 = pandas.Index([pandas.NA, "b", "b"], dtype="string[pyarrow]")
    multi_columns = pandas.MultiIndex.from_arrays([level1, level2])
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.stack().to_pandas()
    pd_result = pd_df.stack()

    # Pandas produces NaN, where bq dataframes produces pd.NA
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("index_names",),
    [
        (["rowindex_2", "int64_too"],),
        (["int64_too", "rowindex_2"],),
    ],
)
def test_is_monotonic_increasing(
    scalars_df_index, scalars_pandas_df_index, index_names
):
    bf_result = scalars_df_index.set_index(index_names).index
    pd_result = scalars_pandas_df_index.set_index(index_names).index

    assert bf_result.is_monotonic_increasing == pd_result.is_monotonic_increasing


@pytest.mark.parametrize(
    ("indexes",),
    [
        ({"A": [1, 2, 3], "B": [1, 2, 3], "C": [1, 2, 3]},),
        ({"A": [1, 2, 3], "B": [1, 2, 3], "C": [1, None, 3]},),
        ({"A": [1, 2, 2], "B": [1, 2, 1], "C": [1, 2, 3]},),
        ({"A": [1, 2, 2], "B": [1, 2, 3], "C": [1, 2, 1]},),
        ({"A": [1, 2, 1], "B": [1, 2, 3], "C": [1, 2, 1]},),
        ({"A": [3, 2, 1], "B": [3, 2, 1], "C": [2, 2, 1]},),
    ],
)
def test_is_monotonic_increasing_extra(indexes):
    bf_result = bpd.DataFrame(indexes)
    bf_result = bf_result.set_index(["A", "B", "C"])
    pd_result = pandas.DataFrame(indexes)
    pd_result = pd_result.set_index(["A", "B", "C"])

    assert (
        bf_result.index.is_monotonic_increasing
        == pd_result.index.is_monotonic_increasing
    )


@pytest.mark.parametrize(
    ("indexes",),
    [
        ({"A": [3, 2, 1], "B": [3, 2, 1], "C": [3, 2, 1]},),
        ({"A": [3, 2, 1], "B": [3, 2, 1], "C": [3, None, 1]},),
        ({"A": [2, 2, 1], "B": [1, 2, 1], "C": [3, 2, 1]},),
        ({"A": [2, 2, 1], "B": [3, 2, 1], "C": [1, 2, 1]},),
        ({"A": [1, 2, 1], "B": [3, 2, 1], "C": [1, 2, 1]},),
    ],
)
def test_is_monotonic_decreasing_extra(indexes):
    bf_result = bpd.DataFrame(indexes)
    bf_result = bf_result.set_index(["A", "B", "C"])
    pd_result = pandas.DataFrame(indexes)
    pd_result = pd_result.set_index(["A", "B", "C"])

    assert (
        bf_result.index.is_monotonic_decreasing
        == pd_result.index.is_monotonic_decreasing
    )


def test_column_multi_index_droplevel(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "string_col", "bool_col"]
    multi_columns = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "a"], ["c", "d", "e"], ["f", "g", "f"])
    )
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.droplevel(1, axis=1).to_pandas()
    pd_result = pd_df.droplevel(1, axis=1)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_column_multi_index_reindex(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "rowindex_2"]
    multi_columns = pandas.MultiIndex.from_tuples(zip(["a", "b", "a"], ["a", "b", "b"]))
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    new_index = pandas.MultiIndex.from_tuples(
        [("z", "a"), ("a", "a")], names=["newname1", "newname2"]
    )

    bf_result = bf_df.reindex(columns=new_index).to_pandas()

    pd_result = pd_df.reindex(columns=new_index)

    # Pandas uses float64 as default for newly created empty column, bf uses Float64
    pd_result[("z", "a")] = pd_result[("z", "a")].astype(pandas.Float64Dtype())

    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_column_multi_index_reorder_levels(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "string_col", "bool_col"]
    multi_columns = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "a"], ["c", "d", "e"], ["f", "g", "f"])
    )
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.reorder_levels([-2, -1, 0], axis=1).to_pandas()
    pd_result = pd_df.reorder_levels([-2, -1, 0], axis=1)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("level",),
    [(["position", "team_name"],), ([-2, -1],), (["position"],), ("season",), (-3,)],
)
def test_df_multi_index_unstack(hockey_df, hockey_pandas_df, level):
    bf_result = (
        hockey_df.set_index(["team_name", "position"], append=True)
        .unstack(level=level)
        .to_pandas()
    )
    pd_result = hockey_pandas_df.set_index(
        ["team_name", "position"], append=True
    ).unstack(level=level)

    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("level",),
    [(["position", "team_name"],), ([-2, -1],), (["position"],), ("season",), (-3,)],
)
def test_series_multi_index_unstack(hockey_df, hockey_pandas_df, level):
    bf_result = (
        hockey_df.set_index(["team_name", "position"], append=True)["number"]
        .unstack(level=level)
        .to_pandas()
    )
    pd_result = hockey_pandas_df.set_index(["team_name", "position"], append=True)[
        "number"
    ].unstack(level=level)

    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


def test_column_multi_index_swaplevel(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "string_col", "bool_col"]
    multi_columns = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "a"], ["c", "d", "e"], ["f", "g", "f"])
    )
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf_df.swaplevel(-3, -1, axis=1).to_pandas()
    pd_result = pd_df.swaplevel(-3, -1, axis=1)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_multi_index_dot_not_supported():
    left_matrix = [[1, 2, 3], [2, 5, 7]]
    right_matrix = [[2, 4, 8], [1, 5, 10], [3, 6, 9]]

    # Left multi-index
    left_index = pandas.MultiIndex.from_tuples([("a", "aa"), ("a", "ab")])
    bf1 = bpd.DataFrame(left_matrix, index=left_index)
    bf2 = bpd.DataFrame(right_matrix)
    with pytest.raises(NotImplementedError, match="Multi-index input is not supported"):
        bf1.dot(bf2)

    with pytest.raises(NotImplementedError, match="Multi-index input is not supported"):
        bf1 @ bf2

    # right multi-index
    right_index = pandas.MultiIndex.from_tuples([("a", "aa"), ("a", "ab"), ("b", "bb")])
    bf1 = bpd.DataFrame(left_matrix)
    bf2 = bpd.DataFrame(right_matrix, index=right_index)
    with pytest.raises(NotImplementedError, match="Multi-index input is not supported"):
        bf1.dot(bf2)

    with pytest.raises(NotImplementedError, match="Multi-index input is not supported"):
        bf1 @ bf2


def test_column_multi_index_dot_not_supported():
    left_matrix = [[1, 2, 3], [2, 5, 7]]
    right_matrix = [[2, 4, 8], [1, 5, 10], [3, 6, 9]]

    multi_level_columns = pandas.MultiIndex.from_arrays(
        [["col0", "col0", "col1"], ["col00", "col01", "col11"]]
    )

    # Left multi-columns
    bf1 = bpd.DataFrame(left_matrix, columns=multi_level_columns)
    bf2 = bpd.DataFrame(right_matrix)
    with pytest.raises(
        NotImplementedError, match="Multi-level column input is not supported"
    ):
        bf1.dot(bf2)

    with pytest.raises(
        NotImplementedError, match="Multi-level column input is not supported"
    ):
        bf1 @ bf2

    # right multi-columns
    bf1 = bpd.DataFrame(left_matrix)
    bf2 = bpd.DataFrame(right_matrix, columns=multi_level_columns)
    with pytest.raises(
        NotImplementedError, match="Multi-level column input is not supported"
    ):
        bf1.dot(bf2)

    with pytest.raises(
        NotImplementedError, match="Multi-level column input is not supported"
    ):
        bf1 @ bf2
