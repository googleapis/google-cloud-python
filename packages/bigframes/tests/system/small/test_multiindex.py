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

import numpy as np
import pandas
import pytest

import bigframes.pandas as bpd
from bigframes.testing.utils import assert_pandas_df_equal

# Sample MultiIndex for testing DataFrames where() method.
_MULTI_INDEX = pandas.MultiIndex.from_tuples(
    [
        (0, "a"),
        (1, "b"),
        (2, "c"),
        (0, "d"),
        (1, "e"),
        (2, "f"),
        (0, "g"),
        (1, "h"),
        (2, "i"),
    ],
    names=["A", "B"],
)


def test_multi_index_from_arrays():
    bf_idx = bpd.MultiIndex.from_arrays(
        [
            pandas.Index([4, 99], dtype=pandas.Int64Dtype()),
            pandas.Index(
                [" Hello, World!", "_some_new_string"],
                dtype=pandas.StringDtype(storage="pyarrow"),
            ),
        ],
        names=[" 1index 1", "_1index 2"],
    )
    pd_idx = pandas.MultiIndex.from_arrays(
        [
            pandas.Index([4, 99], dtype=pandas.Int64Dtype()),
            pandas.Index(
                [" Hello, World!", "_some_new_string"],
                dtype=pandas.StringDtype(storage="pyarrow"),
            ),
        ],
        names=[" 1index 1", "_1index 2"],
    )
    assert bf_idx.names == pd_idx.names
    pandas.testing.assert_index_equal(bf_idx.to_pandas(), pd_idx)


def test_read_pandas_multi_index_axes():
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    index = pandas.MultiIndex.from_arrays(
        [
            pandas.Index([4, 99], dtype=pandas.Int64Dtype()),
            pandas.Index(
                [" Hello, World!", "_some_new_string"],
                dtype=pandas.StringDtype(storage="pyarrow"),
            ),
        ],
        names=[" 1index 1", "_1index 2"],
    )
    columns = pandas.MultiIndex.from_arrays(
        [
            pandas.Index([6, 87], dtype=pandas.Int64Dtype()),
            pandas.Index(
                [" Bonjour le monde!", "_une_chaîne_de_caractères"],
                dtype=pandas.StringDtype(storage="pyarrow"),
            ),
        ],
        names=[" 1columns 1", "_1new_index 2"],
    )
    pandas_df = pandas.DataFrame(
        [[1, 2], [3, 4]], index=index, columns=columns, dtype=pandas.Int64Dtype()
    )
    bf_df = bpd.DataFrame(pandas_df)
    bf_df_computed = bf_df.to_pandas()

    pandas.testing.assert_frame_equal(bf_df_computed, pandas_df)


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


@pytest.mark.parametrize(
    ("key"),
    [
        (2),
        ([2, 0]),
        ([(2, "capitalize, This "), (-2345, "Hello, World!")]),
    ],
)
def test_multi_index_loc_multi_row(scalars_df_index, scalars_pandas_df_index, key):
    bf_result = (
        scalars_df_index.set_index(["int64_too", "string_col"]).loc[key].to_pandas()
    )
    pd_result = scalars_pandas_df_index.set_index(["int64_too", "string_col"]).loc[key]

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_multi_index_loc_single_row(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.set_index(["int64_too", "string_col"]).loc[
        (2, "capitalize, This ")
    ]
    pd_result = scalars_pandas_df_index.set_index(["int64_too", "string_col"]).loc[
        (2, "capitalize, This ")
    ]

    pandas.testing.assert_series_equal(bf_result, pd_result)


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
        ((0, True), None),
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
    index_cols = ["int64_too", "bool_col"]
    bf_result = (
        scalars_df_index.set_index(index_cols)
        .groupby(level=level, as_index=as_index)
        .mean(numeric_only=True)
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.set_index(index_cols)
        .groupby(level=level, as_index=as_index)
        .mean(numeric_only=True)
    )
    # For as_index=False, pandas will drop index levels used as groupings
    # In the future, it will include this in the result, bigframes already does this behavior
    if not as_index:
        for col in index_cols:
            if col in bf_result.columns:
                bf_result = bf_result.drop(col, axis=1)

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
    # Drop "numeric_col" as pandas doesn't support numerics for grouped window function
    bf_result = (
        scalars_df_index.drop("numeric_col", axis=1)
        .set_index(["int64_too", "bool_col"])
        .groupby(level=level, as_index=as_index, dropna=False)
        .cumsum(numeric_only=True)
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.drop("numeric_col", axis=1)
        .set_index(["int64_too", "bool_col"])
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


def test_multi_index_dataframe_where_series_cond_none_other(
    scalars_df_index, scalars_pandas_df_index
):
    columns = ["int64_col", "float64_col"]

    # Create multi-index dataframe.
    dataframe_bf = bpd.DataFrame(
        scalars_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_df_index[columns].columns,
    )
    dataframe_pd = pandas.DataFrame(
        scalars_pandas_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_pandas_df_index[columns].columns,
    )
    dataframe_bf.columns.name = "test_name"
    dataframe_pd.columns.name = "test_name"

    # When condition is series and other is None.
    series_cond_bf = dataframe_bf["int64_col"] > 0
    series_cond_pd = dataframe_pd["int64_col"] > 0

    bf_result = dataframe_bf.where(series_cond_bf).to_pandas()
    pd_result = dataframe_pd.where(series_cond_pd)
    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
        check_dtype=False,
    )
    # Assert the index is still MultiIndex after the operation.
    assert isinstance(bf_result.index, pandas.MultiIndex), "Expected a MultiIndex"
    assert isinstance(pd_result.index, pandas.MultiIndex), "Expected a MultiIndex"


def test_multi_index_dataframe_where_series_cond_dataframe_other(
    scalars_df_index, scalars_pandas_df_index
):
    columns = ["int64_col", "int64_too"]

    # Create multi-index dataframe.
    dataframe_bf = bpd.DataFrame(
        scalars_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_df_index[columns].columns,
    )
    dataframe_pd = pandas.DataFrame(
        scalars_pandas_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_pandas_df_index[columns].columns,
    )

    # When condition is series and other is dataframe.
    series_cond_bf = dataframe_bf["int64_col"] > 1000.0
    series_cond_pd = dataframe_pd["int64_col"] > 1000.0
    dataframe_other_bf = dataframe_bf * 100.0
    dataframe_other_pd = dataframe_pd * 100.0

    bf_result = dataframe_bf.where(series_cond_bf, dataframe_other_bf).to_pandas()
    pd_result = dataframe_pd.where(series_cond_pd, dataframe_other_pd)
    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
        check_dtype=False,
    )


def test_multi_index_dataframe_where_dataframe_cond_constant_other(
    scalars_df_index, scalars_pandas_df_index
):
    columns = ["int64_col", "float64_col"]

    # Create multi-index dataframe.
    dataframe_bf = bpd.DataFrame(
        scalars_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_df_index[columns].columns,
    )
    dataframe_pd = pandas.DataFrame(
        scalars_pandas_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_pandas_df_index[columns].columns,
    )

    # When condition is dataframe and other is a constant.
    dataframe_cond_bf = dataframe_bf > 0
    dataframe_cond_pd = dataframe_pd > 0
    other = 0

    bf_result = dataframe_bf.where(dataframe_cond_bf, other).to_pandas()
    pd_result = dataframe_pd.where(dataframe_cond_pd, other)
    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
        check_dtype=False,
    )


def test_multi_index_dataframe_where_dataframe_cond_dataframe_other(
    scalars_df_index, scalars_pandas_df_index
):
    columns = ["int64_col", "int64_too", "float64_col"]

    # Create multi-index dataframe.
    dataframe_bf = bpd.DataFrame(
        scalars_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_df_index[columns].columns,
    )
    dataframe_pd = pandas.DataFrame(
        scalars_pandas_df_index[columns].values,
        index=_MULTI_INDEX,
        columns=scalars_pandas_df_index[columns].columns,
    )

    # When condition is dataframe and other is dataframe.
    dataframe_cond_bf = dataframe_bf < 1000.0
    dataframe_cond_pd = dataframe_pd < 1000.0
    dataframe_other_bf = dataframe_bf * -1.0
    dataframe_other_pd = dataframe_pd * -1.0

    bf_result = dataframe_bf.where(dataframe_cond_bf, dataframe_other_bf).to_pandas()
    pd_result = dataframe_pd.where(dataframe_cond_pd, dataframe_other_pd)
    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
        check_dtype=False,
    )


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


def test_column_multi_index_any():
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    columns = pandas.MultiIndex.from_tuples(
        [("col0", "col00"), ("col0", "col00"), ("col1", "col11")]
    )
    pd_df = pandas.DataFrame(
        [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]], columns=columns
    )
    bf_df = bpd.DataFrame(pd_df)

    pd_result = pd_df.isna().any()
    bf_result = bf_df.isna().any().to_pandas()

    pandas.testing.assert_frame_equal(
        bf_result.reset_index(drop=False),
        pd_result.reset_index(drop=False),
        check_dtype=False,
    )


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
    assert isinstance(pd_result, pandas.DataFrame)
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
    level1: pandas.Index = pandas.Index(["b", "a", "b"], dtype="string[pyarrow]")
    # Need resulting column to be pyarrow string rather than object dtype
    level2: pandas.Index = pandas.Index(["a", "b", "b"], dtype="string[pyarrow]")
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


def test_corr_w_multi_index(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "float64_col", "int64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "b"], [1, 2, 2]), names=[None, "level_2"]
    )

    bf = scalars_df_index[columns].copy()
    bf.columns = multi_columns

    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf.corr(numeric_only=True).to_pandas()
    pd_result = pd_df.corr(numeric_only=True)

    # BigFrames and Pandas differ in their data type handling:
    # - Column types: BigFrames uses Float64, Pandas uses float64.
    # - Index types: BigFrames uses strign, Pandas uses object.
    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


def test_cov_w_multi_index(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "float64_col", "int64_col"]
    multi_columns = pandas.MultiIndex.from_tuples(
        zip(["a", "b", "b"], [1, 2, 2]), names=["level_1", None]
    )

    bf = scalars_df_index[columns].copy()
    bf.columns = multi_columns

    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    bf_result = bf.cov(numeric_only=True).to_pandas()
    pd_result = pd_df.cov(numeric_only=True)

    # BigFrames and Pandas differ in their data type handling:
    # - Column types: BigFrames uses Float64, Pandas uses float64.
    # - Index types: BigFrames uses string, Pandas uses object.
    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


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


def test_explode_w_column_multi_index():
    data = [[[1, 1], np.nan, [3, 3]], [[2], [5], []]]
    multi_level_columns = pandas.MultiIndex.from_arrays(
        [["col0", "col0", "col1"], ["col00", "col01", "col11"]]
    )

    df = bpd.DataFrame(data, columns=multi_level_columns)
    pd_df = df.to_pandas()

    assert isinstance(pd_df, pandas.DataFrame)
    assert isinstance(pd_df["col0"], pandas.DataFrame)
    pandas.testing.assert_frame_equal(
        df["col0"].explode("col00").to_pandas(),
        pd_df["col0"].explode("col00"),
        check_dtype=False,
        check_index_type=False,
    )


def test_explode_w_multi_index():
    data = [[[1, 1], np.nan, [3, 3]], [[2], [5], []]]
    columns = ["col00", "col01", "col11"]
    multi_index = pandas.MultiIndex.from_frame(
        pandas.DataFrame({"idx0": [5, 1], "idx1": ["z", "x"]})
    )

    df = bpd.DataFrame(data, index=multi_index, columns=columns)
    pd_df = df.to_pandas()

    pandas.testing.assert_frame_equal(
        df.explode("col00").to_pandas(),
        pd_df.explode("col00"),
        check_dtype=False,
        check_index_type=False,
    )


def test_column_multi_index_w_na_stack(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_too", "int64_col", "rowindex_2"]
    level1 = pandas.Index(["b", "c", "d"])
    # Need resulting column to be pyarrow string rather than object dtype
    level2: pandas.Index = pandas.Index([None, "b", "b"], dtype="string[pyarrow]")
    multi_columns = pandas.MultiIndex.from_arrays([level1, level2])
    bf_df = scalars_df_index[columns].copy()
    bf_df.columns = multi_columns
    pd_df = scalars_pandas_df_index[columns].copy()
    pd_df.columns = multi_columns

    pd_result = pd_df.stack()
    bf_result = bf_df.stack().to_pandas()

    # Pandas produces pd.NA, where bq dataframes produces NaN
    pd_result["c"] = pd_result["c"].replace(pandas.NA, np.nan)
    pandas.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)
