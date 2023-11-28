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

import io
import operator
import tempfile
import typing
from typing import Tuple

import geopandas as gpd  # type: ignore
import numpy as np
import pandas as pd
import pandas.testing
import pyarrow as pa  # type: ignore
import pytest

import bigframes
import bigframes._config.display_options as display_options
import bigframes.dataframe as dataframe
import bigframes.series as series
from tests.system.utils import assert_pandas_df_equal, assert_series_equal


def test_df_construct_copy(scalars_dfs):
    columns = ["int64_col", "string_col", "float64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = dataframe.DataFrame(scalars_df, columns=columns).to_pandas()
    pd_result = pd.DataFrame(scalars_pandas_df, columns=columns)
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_construct_pandas(scalars_dfs):
    columns = ["int64_too", "int64_col", "float64_col", "bool_col", "string_col"]
    _, scalars_pandas_df = scalars_dfs
    bf_result = dataframe.DataFrame(scalars_pandas_df, columns=columns).to_pandas()
    pd_result = pd.DataFrame(scalars_pandas_df, columns=columns)
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_construct_pandas_set_dtype(scalars_dfs):
    columns = [
        "int64_too",
        "int64_col",
        "float64_col",
        "bool_col",
    ]
    _, scalars_pandas_df = scalars_dfs
    bf_result = dataframe.DataFrame(
        scalars_pandas_df, columns=columns, dtype="Float64"
    ).to_pandas()
    pd_result = pd.DataFrame(scalars_pandas_df, columns=columns, dtype="Float64")
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_construct_from_series(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = dataframe.DataFrame(
        {"a": scalars_df["int64_col"], "b": scalars_df["string_col"]},
        dtype="string[pyarrow]",
    ).to_pandas()
    pd_result = pd.DataFrame(
        {"a": scalars_pandas_df["int64_col"], "b": scalars_pandas_df["string_col"]},
        dtype="string[pyarrow]",
    )
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_construct_from_dict():
    input_dict = {
        "Animal": ["Falcon", "Falcon", "Parrot", "Parrot"],
        # With a space in column name. We use standardized SQL schema ids to solve the problem that BQ schema doesn't support column names with spaces. b/296751058
        "Max Speed": [380.0, 370.0, 24.0, 26.0],
    }
    bf_result = dataframe.DataFrame(input_dict).to_pandas()
    pd_result = pd.DataFrame(input_dict)

    pandas.testing.assert_frame_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


def test_get_column(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    series = scalars_df[col_name]
    bf_result = series.to_pandas()
    pd_result = scalars_pandas_df[col_name]
    assert_series_equal(bf_result, pd_result)


def test_get_column_nonstring(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    series = scalars_df.rename(columns={"int64_col": 123.1})[123.1]
    bf_result = series.to_pandas()
    pd_result = scalars_pandas_df.rename(columns={"int64_col": 123.1})[123.1]
    assert_series_equal(bf_result, pd_result)


def test_hasattr(scalars_dfs):
    scalars_df, _ = scalars_dfs
    assert hasattr(scalars_df, "int64_col")
    assert hasattr(scalars_df, "head")
    assert not hasattr(scalars_df, "not_exist")


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_head_with_custom_column_labels(
    scalars_df_index, scalars_pandas_df_index, ordered
):
    rename_mapping = {
        "int64_col": "Integer Column",
        "string_col": "言語列",
    }
    bf_df = scalars_df_index.rename(columns=rename_mapping).head(3)
    bf_result = bf_df.to_pandas(ordered=ordered)
    pd_result = scalars_pandas_df_index.rename(columns=rename_mapping).head(3)
    assert_pandas_df_equal(bf_result, pd_result, ignore_order=not ordered)


def test_tail_with_custom_column_labels(scalars_df_index, scalars_pandas_df_index):
    rename_mapping = {
        "int64_col": "Integer Column",
        "string_col": "言語列",
    }
    bf_df = scalars_df_index.rename(columns=rename_mapping).tail(3)
    bf_result = bf_df.to_pandas()
    pd_result = scalars_pandas_df_index.rename(columns=rename_mapping).tail(3)
    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        ("all",),
    ],
)
def test_df_nlargest(scalars_df_index, scalars_pandas_df_index, keep):
    bf_result = scalars_df_index.nlargest(
        3, ["bool_col", "int64_too"], keep=keep
    ).to_pandas()
    pd_result = scalars_pandas_df_index.nlargest(
        3, ["bool_col", "int64_too"], keep=keep
    )

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        ("all",),
    ],
)
def test_df_nsmallest(scalars_df_index, scalars_pandas_df_index, keep):
    bf_result = scalars_df_index.nsmallest(6, ["bool_col"], keep=keep).to_pandas()
    pd_result = scalars_pandas_df_index.nsmallest(6, ["bool_col"], keep=keep)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_get_column_by_attr(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    series = scalars_df.int64_col
    bf_result = series.to_pandas()
    pd_result = scalars_pandas_df.int64_col
    assert_series_equal(bf_result, pd_result)


def test_get_columns(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_names = ["bool_col", "float64_col", "int64_col"]
    df_subset = scalars_df.get(col_names)
    df_pandas = df_subset.to_pandas()
    pd.testing.assert_index_equal(
        df_pandas.columns, scalars_pandas_df[col_names].columns
    )


def test_get_columns_default(scalars_dfs):
    scalars_df, _ = scalars_dfs
    col_names = ["not", "column", "names"]
    result = scalars_df.get(col_names, "default_val")
    assert result == "default_val"


def test_drop_column(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name = "int64_col"
    df_pandas = scalars_df.drop(columns=col_name).to_pandas()
    pd.testing.assert_index_equal(
        df_pandas.columns, scalars_pandas_df.drop(columns=col_name).columns
    )


def test_drop_columns(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_names = ["int64_col", "geography_col", "time_col"]
    df_pandas = scalars_df.drop(columns=col_names).to_pandas()
    pd.testing.assert_index_equal(
        df_pandas.columns, scalars_pandas_df.drop(columns=col_names).columns
    )


def test_drop_labels_axis_1(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    labels = ["int64_col", "geography_col", "time_col"]

    pd_result = scalars_pandas_df.drop(labels=labels, axis=1)
    bf_result = scalars_df.drop(labels=labels, axis=1).to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_with_custom_column_labels(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    rename_mapping = {
        "int64_col": "Integer Column",
        "string_col": "言語列",
    }
    dropped_columns = [
        "言語列",
        "timestamp_col",
    ]
    bf_df = scalars_df.rename(columns=rename_mapping).drop(columns=dropped_columns)
    bf_result = bf_df.to_pandas()
    pd_result = scalars_pandas_df.rename(columns=rename_mapping).drop(
        columns=dropped_columns
    )
    assert_pandas_df_equal(bf_result, pd_result)


def test_df_memory_usage(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = scalars_pandas_df.memory_usage()
    bf_result = scalars_df.memory_usage()

    pd.testing.assert_series_equal(pd_result, bf_result, rtol=1.5)


def test_df_info(scalars_dfs):
    expected = (
        "<class 'bigframes.dataframe.DataFrame'>\n"
        "Index: 9 entries, 0 to 8\n"
        "Data columns (total 13 columns):\n"
        "  #  Column         Non-Null Count    Dtype\n"
        "---  -------------  ----------------  ------------------------------\n"
        "  0  bool_col       8 non-null        boolean\n"
        "  1  bytes_col      6 non-null        object\n"
        "  2  date_col       7 non-null        date32[day][pyarrow]\n"
        "  3  datetime_col   6 non-null        timestamp[us][pyarrow]\n"
        "  4  geography_col  4 non-null        geometry\n"
        "  5  int64_col      8 non-null        Int64\n"
        "  6  int64_too      9 non-null        Int64\n"
        "  7  numeric_col    6 non-null        object\n"
        "  8  float64_col    7 non-null        Float64\n"
        "  9  rowindex_2     9 non-null        Int64\n"
        " 10  string_col     8 non-null        string\n"
        " 11  time_col       6 non-null        time64[us][pyarrow]\n"
        " 12  timestamp_col  6 non-null        timestamp[us, tz=UTC][pyarrow]\n"
        "dtypes: Float64(1), Int64(3), boolean(1), date32[day][pyarrow](1), geometry(1), object(2), string(1), time64[us][pyarrow](1), timestamp[us, tz=UTC][pyarrow](1), timestamp[us][pyarrow](1)\n"
        "memory usage: 945 bytes\n"
    )

    scalars_df, _ = scalars_dfs
    bf_result = io.StringIO()

    scalars_df.info(buf=bf_result)

    assert expected == bf_result.getvalue()


def test_drop_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = scalars_pandas_df.drop(index=[4, 1, 2])
    bf_result = scalars_df.drop(index=[4, 1, 2]).to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_pandas_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    drop_index = scalars_pandas_df.iloc[[4, 1, 2]].index

    pd_result = scalars_pandas_df.drop(index=drop_index)
    bf_result = scalars_df.drop(index=drop_index).to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_bigframes_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    drop_index = scalars_df.loc[[4, 1, 2]].index
    drop_pandas_index = scalars_pandas_df.loc[[4, 1, 2]].index

    pd_result = scalars_pandas_df.drop(index=drop_pandas_index)
    bf_result = scalars_df.drop(index=drop_index).to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_bigframes_index_with_na(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.copy()
    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_df = scalars_df.set_index("bytes_col")
    scalars_pandas_df = scalars_pandas_df.set_index("bytes_col")
    drop_index = scalars_df.iloc[[3, 5]].index
    drop_pandas_index = scalars_pandas_df.iloc[[3, 5]].index

    pd_result = scalars_pandas_df.drop(index=drop_pandas_index)  # drop_pandas_index)
    bf_result = scalars_df.drop(index=drop_index).to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_bigframes_multiindex(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.copy()
    scalars_pandas_df = scalars_pandas_df.copy()
    sub_df = scalars_df.iloc[[4, 1, 2]]
    sub_pandas_df = scalars_pandas_df.iloc[[4, 1, 2]]
    sub_df = sub_df.set_index(["bytes_col", "numeric_col"])
    sub_pandas_df = sub_pandas_df.set_index(["bytes_col", "numeric_col"])
    drop_index = sub_df.index
    drop_pandas_index = sub_pandas_df.index

    scalars_df = scalars_df.set_index(["bytes_col", "numeric_col"])
    scalars_pandas_df = scalars_pandas_df.set_index(["bytes_col", "numeric_col"])
    bf_result = scalars_df.drop(index=drop_index).to_pandas()
    pd_result = scalars_pandas_df.drop(index=drop_pandas_index)

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_labels_axis_0(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = scalars_pandas_df.drop(labels=[4, 1, 2], axis=0)
    bf_result = scalars_df.drop(labels=[4, 1, 2], axis=0).to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_drop_index_and_columns(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    pd_result = scalars_pandas_df.drop(index=[4, 1, 2], columns="int64_col")
    bf_result = scalars_df.drop(index=[4, 1, 2], columns="int64_col").to_pandas()

    pd.testing.assert_frame_equal(pd_result, bf_result)


def test_rename(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name_dict = {"bool_col": 1.2345}
    df_pandas = scalars_df.rename(columns=col_name_dict).to_pandas()
    pd.testing.assert_index_equal(
        df_pandas.columns, scalars_pandas_df.rename(columns=col_name_dict).columns
    )


def test_repr_w_all_rows(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    # Remove columns with flaky formatting, like NUMERIC columns (which use the
    # object dtype). Also makes a copy so that mutating the index name doesn't
    # break other tests.
    scalars_df = scalars_df.drop(columns=["numeric_col"])
    scalars_pandas_df = scalars_pandas_df.drop(columns=["numeric_col"])

    if scalars_pandas_df.index.name is None:
        # Note: Not quite the same as no index / default index, but hopefully
        # simulates it well enough while being consistent enough for string
        # comparison to work.
        scalars_df = scalars_df.set_index("rowindex", drop=False).sort_index()
        scalars_df.index.name = None

    # When there are 10 or fewer rows, the outputs should be identical.
    actual = repr(scalars_df.head(10))

    with display_options.pandas_repr(bigframes.options.display):
        expected = repr(scalars_pandas_df.head(10))

    assert actual == expected


def test_repr_html_w_all_rows(scalars_dfs):
    scalars_df, _ = scalars_dfs
    # get a pandas df of the expected format
    df, _ = scalars_df._block.to_pandas()
    pandas_df = df.set_axis(scalars_df._block.column_labels, axis=1)
    pandas_df.index.name = scalars_df.index.name

    # When there are 10 or fewer rows, the outputs should be identical except for the extra note.
    actual = scalars_df.head(10)._repr_html_()
    with display_options.pandas_repr(bigframes.options.display):
        pandas_repr = pandas_df.head(10)._repr_html_()

    expected = (
        pandas_repr
        + f"[{len(pandas_df.index)} rows x {len(pandas_df.columns)} columns in total]"
    )
    assert actual == expected


def test_df_column_name_with_space(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name_dict = {"bool_col": "bool  col"}
    df_pandas = scalars_df.rename(columns=col_name_dict).to_pandas()
    pd.testing.assert_index_equal(
        df_pandas.columns, scalars_pandas_df.rename(columns=col_name_dict).columns
    )


def test_df_column_name_duplicate(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name_dict = {"int64_too": "int64_col"}
    df_pandas = scalars_df.rename(columns=col_name_dict).to_pandas()
    pd.testing.assert_index_equal(
        df_pandas.columns, scalars_pandas_df.rename(columns=col_name_dict).columns
    )


def test_get_df_column_name_duplicate(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name_dict = {"int64_too": "int64_col"}

    bf_result = scalars_df.rename(columns=col_name_dict)["int64_col"].to_pandas()
    pd_result = scalars_pandas_df.rename(columns=col_name_dict)["int64_col"]
    pd.testing.assert_index_equal(bf_result.columns, pd_result.columns)


def test_filter_df(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_bool_series = scalars_df["bool_col"]
    bf_result = scalars_df[bf_bool_series].to_pandas()

    pd_bool_series = scalars_pandas_df["bool_col"]
    pd_result = scalars_pandas_df[pd_bool_series]

    assert_pandas_df_equal(bf_result, pd_result)


def test_assign_new_column(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    kwargs = {"new_col": 2}
    df = scalars_df.assign(**kwargs)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**kwargs)

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")

    assert_pandas_df_equal(bf_result, pd_result)


def test_assign_new_column_w_loc(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df.loc[:, "new_col"] = 2
    pd_df.loc[:, "new_col"] = 2
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_new_column_w_setitem(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df["new_col"] = 2
    pd_df["new_col"] = 2
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_new_column_w_setitem_dataframe(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df["int64_col"] = bf_df["int64_too"].to_frame()
    pd_df["int64_col"] = pd_df["int64_too"].to_frame()

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_df["int64_col"] = pd_df["int64_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df)


def test_assign_new_column_w_setitem_dataframe_error(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()

    with pytest.raises(ValueError):
        bf_df["impossible_col"] = bf_df[["int64_too", "string_col"]]
    with pytest.raises(ValueError):
        pd_df["impossible_col"] = pd_df[["int64_too", "string_col"]]


def test_assign_new_column_w_setitem_list(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df["new_col"] = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    pd_df["new_col"] = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_new_column_w_setitem_list_repeated(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df["new_col"] = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    pd_df["new_col"] = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    bf_df["new_col_2"] = [1, 3, 2, 5, 4, 7, 6, 9, 8]
    pd_df["new_col_2"] = [1, 3, 2, 5, 4, 7, 6, 9, 8]
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")
    pd_result["new_col_2"] = pd_result["new_col_2"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_new_column_w_setitem_list_custom_index(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()

    # set the custom index
    pd_df = pd_df.set_index(["string_col", "int64_col"])
    bf_df = bf_df.set_index(["string_col", "int64_col"])

    bf_df["new_col"] = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    pd_df["new_col"] = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_new_column_w_setitem_list_error(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()

    with pytest.raises(ValueError):
        pd_df["new_col"] = [1, 2, 3]  # should be len 9, is 3
    with pytest.raises(ValueError):
        bf_df["new_col"] = [1, 2, 3]


def test_assign_existing_column(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    kwargs = {"int64_col": 2}
    df = scalars_df.assign(**kwargs)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**kwargs)

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["int64_col"] = pd_result["int64_col"].astype("Int64")

    assert_pandas_df_equal(bf_result, pd_result)


def test_assign_listlike_to_empty_df(session):
    empty_df = dataframe.DataFrame(session=session)
    empty_pandas_df = pd.DataFrame()

    bf_result = empty_df.assign(new_col=[1, 2, 3])
    pd_result = empty_pandas_df.assign(new_col=[1, 2, 3])

    pd_result["new_col"] = pd_result["new_col"].astype("Int64")
    pd_result.index = pd_result.index.astype("Int64")
    assert_pandas_df_equal(bf_result.to_pandas(), pd_result)


def test_assign_to_empty_df_multiindex_error(session):
    empty_df = dataframe.DataFrame(session=session)
    empty_pandas_df = pd.DataFrame()
    empty_df["empty_col_1"] = []
    empty_df["empty_col_2"] = []
    empty_pandas_df["empty_col_1"] = []
    empty_pandas_df["empty_col_2"] = []
    empty_df = empty_df.set_index(["empty_col_1", "empty_col_2"])
    empty_pandas_df = empty_pandas_df.set_index(["empty_col_1", "empty_col_2"])

    with pytest.raises(ValueError):
        empty_df.assign(new_col=[1, 2, 3, 4, 5, 6, 7, 8, 9])
    with pytest.raises(ValueError):
        empty_pandas_df.assign(new_col=[1, 2, 3, 4, 5, 6, 7, 8, 9])


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_assign_series(scalars_dfs, ordered):
    scalars_df, scalars_pandas_df = scalars_dfs
    column_name = "int64_col"
    df = scalars_df.assign(new_col=scalars_df[column_name])
    bf_result = df.to_pandas(ordered=ordered)
    pd_result = scalars_pandas_df.assign(new_col=scalars_pandas_df[column_name])

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=not ordered)


def test_assign_series_overwrite(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    column_name = "int64_col"
    df = scalars_df.assign(**{column_name: scalars_df[column_name] + 3})
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(
        **{column_name: scalars_pandas_df[column_name] + 3}
    )

    assert_pandas_df_equal(bf_result, pd_result)


def test_assign_sequential(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    kwargs = {"int64_col": 2, "new_col": 3, "new_col2": 4}
    df = scalars_df.assign(**kwargs)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**kwargs)

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["int64_col"] = pd_result["int64_col"].astype("Int64")
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")
    pd_result["new_col2"] = pd_result["new_col2"].astype("Int64")

    assert_pandas_df_equal(bf_result, pd_result)


# Require an index so that the self-join is consistent each time.
def test_assign_same_table_different_index_performs_self_join(
    scalars_df_index, scalars_pandas_df_index
):
    column_name = "int64_col"
    bf_df = scalars_df_index.assign(
        alternative_index=scalars_df_index["rowindex_2"] + 2
    )
    pd_df = scalars_pandas_df_index.assign(
        alternative_index=scalars_pandas_df_index["rowindex_2"] + 2
    )
    bf_df_2 = bf_df.set_index("alternative_index")
    pd_df_2 = pd_df.set_index("alternative_index")
    bf_result = bf_df.assign(new_col=bf_df_2[column_name] * 10).to_pandas()
    pd_result = pd_df.assign(new_col=pd_df_2[column_name] * 10)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


# Different table expression must have Index
def test_assign_different_df(
    scalars_df_index, scalars_df_2_index, scalars_pandas_df_index
):
    column_name = "int64_col"
    df = scalars_df_index.assign(new_col=scalars_df_2_index[column_name])
    bf_result = df.to_pandas()
    # Doesn't matter to pandas if it comes from the same DF or a different DF.
    pd_result = scalars_pandas_df_index.assign(
        new_col=scalars_pandas_df_index[column_name]
    )

    assert_pandas_df_equal(bf_result, pd_result)


def test_assign_different_df_w_loc(
    scalars_df_index, scalars_df_2_index, scalars_pandas_df_index
):
    bf_df = scalars_df_index.copy()
    bf_df2 = scalars_df_2_index.copy()
    pd_df = scalars_pandas_df_index.copy()
    assert "int64_col" in bf_df.columns
    assert "int64_col" in pd_df.columns
    bf_df.loc[:, "int64_col"] = bf_df2.loc[:, "int64_col"] + 1
    pd_df.loc[:, "int64_col"] = pd_df.loc[:, "int64_col"] + 1
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["int64_col"] = pd_result["int64_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_different_df_w_setitem(
    scalars_df_index, scalars_df_2_index, scalars_pandas_df_index
):
    bf_df = scalars_df_index.copy()
    bf_df2 = scalars_df_2_index.copy()
    pd_df = scalars_pandas_df_index.copy()
    assert "int64_col" in bf_df.columns
    assert "int64_col" in pd_df.columns
    bf_df["int64_col"] = bf_df2["int64_col"] + 1
    pd_df["int64_col"] = pd_df["int64_col"] + 1
    bf_result = bf_df.to_pandas()
    pd_result = pd_df

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["int64_col"] = pd_result["int64_col"].astype("Int64")

    pd.testing.assert_frame_equal(bf_result, pd_result)


def test_assign_callable_lambda(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    kwargs = {"new_col": lambda x: x["int64_col"] + x["int64_too"]}
    df = scalars_df.assign(**kwargs)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.assign(**kwargs)

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result["new_col"] = pd_result["new_col"].astype("Int64")

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("axis", "how", "ignore_index"),
    [
        (0, "any", False),
        (0, "any", True),
        (1, "any", False),
        (1, "all", False),
    ],
)
def test_df_dropna(scalars_dfs, axis, how, ignore_index):
    if pd.__version__.startswith("1."):
        pytest.skip("ignore_index parameter not supported in pandas 1.x.")
    scalars_df, scalars_pandas_df = scalars_dfs
    df = scalars_df.dropna(axis=axis, how=how, ignore_index=ignore_index)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.dropna(axis=axis, how=how, ignore_index=ignore_index)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_interpolate(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    columns = ["int64_col", "int64_too", "float64_col"]
    bf_result = scalars_df[columns].interpolate().to_pandas()
    # Pandas can only interpolate on "float64" columns
    # https://github.com/pandas-dev/pandas/issues/40252
    pd_result = scalars_pandas_df[columns].astype("float64").interpolate()

    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
        check_dtype=False,
    )


def test_df_fillna(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    df = scalars_df[["int64_col", "float64_col"]].fillna(3)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df[["int64_col", "float64_col"]].fillna(3)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_ffill(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[["int64_col", "float64_col"]].ffill(limit=1).to_pandas()
    pd_result = scalars_pandas_df[["int64_col", "float64_col"]].ffill(limit=1)

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_bfill(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[["int64_col", "float64_col"]].bfill().to_pandas()
    pd_result = scalars_pandas_df[["int64_col", "float64_col"]].bfill()

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_apply_series_series_callable(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]

    def foo(series, arg1, arg2, *, kwarg1=0, kwarg2=0):
        return series**2 + (arg1 * arg2 % 4) + (kwarg1 * kwarg2 % 7)

    bf_result = (
        scalars_df_index[columns]
        .apply(foo, args=(33, 61), kwarg1=52, kwarg2=21)
        .to_pandas()
    )

    pd_result = scalars_pandas_df_index[columns].apply(
        foo, args=(33, 61), kwarg1=52, kwarg2=21
    )

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_apply_series_listlike_callable(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]
    bf_result = (
        scalars_df_index[columns].apply(lambda x: [len(x), x.min(), 24]).to_pandas()
    )

    pd_result = scalars_pandas_df_index[columns].apply(lambda x: [len(x), x.min(), 24])

    # Convert default pandas dtypes `int64` to match BigQuery DataFrames dtypes.
    pd_result.index = pd_result.index.astype("Int64")
    pd_result = pd_result.astype("Int64")
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_apply_series_scalar_callable(
    scalars_df_index,
    scalars_pandas_df_index,
):
    columns = ["int64_too", "int64_col"]
    bf_result = scalars_df_index[columns].apply(lambda x: x.sum())

    pd_result = scalars_pandas_df_index[columns].apply(lambda x: x.sum())

    pandas.testing.assert_series_equal(bf_result, pd_result)


def test_df_keys(
    scalars_df_index,
    scalars_pandas_df_index,
):
    pandas.testing.assert_index_equal(
        scalars_df_index.keys(), scalars_pandas_df_index.keys()
    )


def test_df_iter(
    scalars_df_index,
    scalars_pandas_df_index,
):
    for bf_i, df_i in zip(scalars_df_index, scalars_pandas_df_index):
        assert bf_i == df_i


def test_iterrows(
    scalars_df_index,
    scalars_pandas_df_index,
):
    for (bf_index, bf_series), (pd_index, pd_series) in zip(
        scalars_df_index.iterrows(), scalars_pandas_df_index.iterrows()
    ):
        assert bf_index == pd_index
        pandas.testing.assert_series_equal(bf_series, pd_series)


@pytest.mark.parametrize(
    (
        "index",
        "name",
    ),
    [
        (
            True,
            "my_df",
        ),
        (False, None),
    ],
)
def test_itertuples(scalars_df_index, index, name):
    # Numeric has slightly different representation as a result of conversions.
    bf_tuples = scalars_df_index.itertuples(index, name)
    pd_tuples = scalars_df_index.to_pandas().itertuples(index, name)
    for bf_tuple, pd_tuple in zip(bf_tuples, pd_tuples):
        assert bf_tuple == pd_tuple


def test_df_isin_list(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    values = ["Hello, World!", 55555, 2.51, pd.NA, True]
    bf_result = (
        scalars_df[["int64_col", "float64_col", "string_col", "bool_col"]]
        .isin(values)
        .to_pandas()
    )
    pd_result = scalars_pandas_df[
        ["int64_col", "float64_col", "string_col", "bool_col"]
    ].isin(values)

    pandas.testing.assert_frame_equal(bf_result, pd_result.astype("boolean"))


def test_df_isin_dict(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    values = {
        "string_col": ["Hello, World!", 55555, 2.51, pd.NA, True],
        "int64_col": [5555, 2.51],
        "bool_col": [pd.NA],
    }
    bf_result = (
        scalars_df[["int64_col", "float64_col", "string_col", "bool_col"]]
        .isin(values)
        .to_pandas()
    )
    pd_result = scalars_pandas_df[
        ["int64_col", "float64_col", "string_col", "bool_col"]
    ].isin(values)

    pandas.testing.assert_frame_equal(bf_result, pd_result.astype("boolean"))


def test_df_cross_merge(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_columns = ["int64_col", "float64_col", "rowindex_2"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    # Offset the rows somewhat so that outer join can have an effect.
    right = scalars_df[right_columns].assign(rowindex_2=scalars_df["rowindex_2"] + 2)

    bf_result = left.merge(right, "cross").to_pandas()

    pd_result = scalars_pandas_df[left_columns].merge(
        scalars_pandas_df[right_columns].assign(
            rowindex_2=scalars_pandas_df["rowindex_2"] + 2
        ),
        "cross",
    )
    pd.testing.assert_frame_equal(bf_result, pd_result, check_index_type=False)


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_df_merge(scalars_dfs, merge_how):
    scalars_df, scalars_pandas_df = scalars_dfs
    on = "rowindex_2"
    left_columns = ["int64_col", "float64_col", "rowindex_2"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    # Offset the rows somewhat so that outer join can have an effect.
    right = scalars_df[right_columns].assign(rowindex_2=scalars_df["rowindex_2"] + 2)

    df = left.merge(right, merge_how, on, sort=True)
    bf_result = df.to_pandas()

    pd_result = scalars_pandas_df[left_columns].merge(
        scalars_pandas_df[right_columns].assign(
            rowindex_2=scalars_pandas_df["rowindex_2"] + 2
        ),
        merge_how,
        on,
        sort=True,
    )

    assert_pandas_df_equal(
        bf_result, pd_result, ignore_order=True, check_index_type=False
    )


@pytest.mark.parametrize(
    ("left_on", "right_on"),
    [
        (["int64_col", "rowindex_2"], ["int64_col", "rowindex_2"]),
        (["rowindex_2", "int64_col"], ["int64_col", "rowindex_2"]),
        (["rowindex_2", "float64_col"], ["int64_col", "rowindex_2"]),
    ],
)
def test_df_merge_multi_key(scalars_dfs, left_on, right_on):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_columns = ["int64_col", "float64_col", "rowindex_2"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    # Offset the rows somewhat so that outer join can have an effect.
    right = scalars_df[right_columns].assign(rowindex_2=scalars_df["rowindex_2"] + 2)

    df = left.merge(right, "outer", left_on=left_on, right_on=right_on, sort=True)
    bf_result = df.to_pandas()

    pd_result = scalars_pandas_df[left_columns].merge(
        scalars_pandas_df[right_columns].assign(
            rowindex_2=scalars_pandas_df["rowindex_2"] + 2
        ),
        "outer",
        left_on=left_on,
        right_on=right_on,
        sort=True,
    )

    assert_pandas_df_equal(
        bf_result, pd_result, ignore_order=True, check_index_type=False
    )


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_merge_custom_col_name(scalars_dfs, merge_how):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_columns = ["int64_col", "float64_col"]
    right_columns = ["int64_col", "bool_col", "string_col"]
    on = "int64_col"
    rename_columns = {"float64_col": "f64_col"}

    left = scalars_df[left_columns]
    left = left.rename(columns=rename_columns)
    right = scalars_df[right_columns]
    df = left.merge(right, merge_how, on, sort=True)
    bf_result = df.to_pandas()

    pandas_left_df = scalars_pandas_df[left_columns]
    pandas_left_df = pandas_left_df.rename(columns=rename_columns)
    pandas_right_df = scalars_pandas_df[right_columns]
    pd_result = pandas_left_df.merge(pandas_right_df, merge_how, on, sort=True)

    assert_pandas_df_equal(
        bf_result, pd_result, ignore_order=True, check_index_type=False
    )


@pytest.mark.parametrize(
    ("merge_how",),
    [
        ("inner",),
        ("outer",),
        ("left",),
        ("right",),
    ],
)
def test_merge_left_on_right_on(scalars_dfs, merge_how):
    scalars_df, scalars_pandas_df = scalars_dfs
    left_columns = ["int64_col", "float64_col", "int64_too"]
    right_columns = ["int64_col", "bool_col", "string_col", "rowindex_2"]

    left = scalars_df[left_columns]
    right = scalars_df[right_columns]

    df = left.merge(
        right, merge_how, left_on="int64_too", right_on="rowindex_2", sort=True
    )
    bf_result = df.to_pandas()

    pd_result = scalars_pandas_df[left_columns].merge(
        scalars_pandas_df[right_columns],
        merge_how,
        left_on="int64_too",
        right_on="rowindex_2",
        sort=True,
    )

    assert_pandas_df_equal(
        bf_result, pd_result, ignore_order=True, check_index_type=False
    )


def test_get_dtypes(scalars_df_default_index):
    dtypes = scalars_df_default_index.dtypes
    pd.testing.assert_series_equal(
        dtypes,
        pd.Series(
            {
                "bool_col": pd.BooleanDtype(),
                "bytes_col": np.dtype("O"),
                "date_col": pd.ArrowDtype(pa.date32()),
                "datetime_col": pd.ArrowDtype(pa.timestamp("us")),
                "geography_col": gpd.array.GeometryDtype(),
                "int64_col": pd.Int64Dtype(),
                "int64_too": pd.Int64Dtype(),
                "numeric_col": np.dtype("O"),
                "float64_col": pd.Float64Dtype(),
                "rowindex": pd.Int64Dtype(),
                "rowindex_2": pd.Int64Dtype(),
                "string_col": pd.StringDtype(storage="pyarrow"),
                "time_col": pd.ArrowDtype(pa.time64("us")),
                "timestamp_col": pd.ArrowDtype(pa.timestamp("us", tz="UTC")),
            }
        ),
    )


def test_get_dtypes_array_struct(session):
    """We may upgrade struct and array to proper arrow dtype support in future. For now,
    we return python objects"""
    df = session.read_gbq(
        """SELECT
        [1, 3, 2] AS array_column,
        STRUCT(
            "a" AS string_field,
            1.2 AS float_field) AS struct_column"""
    )

    dtypes = df.dtypes
    pd.testing.assert_series_equal(
        dtypes,
        pd.Series(
            {
                "array_column": np.dtype("O"),
                "struct_column": pd.ArrowDtype(
                    pa.struct(
                        [
                            ("string_field", pa.string()),
                            ("float_field", pa.float64()),
                        ]
                    )
                ),
            }
        ),
    )


def test_shape(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df.shape
    pd_result = scalars_pandas_df.shape

    assert bf_result == pd_result


def test_len(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = len(scalars_df)
    pd_result = len(scalars_pandas_df)

    assert bf_result == pd_result


def test_size(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df.size
    pd_result = scalars_pandas_df.size

    assert bf_result == pd_result


def test_ndim(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df.ndim
    pd_result = scalars_pandas_df.ndim

    assert bf_result == pd_result


def test_empty_false(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df.empty
    pd_result = scalars_pandas_df.empty

    assert bf_result == pd_result


def test_empty_true_column_filter(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df[[]].empty
    pd_result = scalars_pandas_df[[]].empty

    assert bf_result == pd_result


def test_empty_true_row_filter(scalars_dfs: Tuple[dataframe.DataFrame, pd.DataFrame]):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_bool: series.Series = typing.cast(series.Series, scalars_df["bool_col"])
    pd_bool: pd.Series = scalars_pandas_df["bool_col"]
    bf_false = bf_bool.notna() & (bf_bool != bf_bool)
    pd_false = pd_bool.notna() & (pd_bool != pd_bool)

    bf_result = scalars_df[bf_false].empty
    pd_result = scalars_pandas_df[pd_false].empty

    assert pd_result
    assert bf_result == pd_result


def test_empty_true_memtable(session: bigframes.Session):
    bf_df = dataframe.DataFrame(session=session)
    pd_df = pd.DataFrame()

    bf_result = bf_df.empty
    pd_result = pd_df.empty

    assert pd_result
    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("drop",),
    ((True,), (False,)),
)
def test_reset_index(scalars_df_index, scalars_pandas_df_index, drop):
    df = scalars_df_index.reset_index(drop=drop)
    assert df.index.name is None

    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df_index.reset_index(drop=drop)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    # reset_index should maintain the original ordering.
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_reset_index_then_filter(
    scalars_df_index,
    scalars_pandas_df_index,
):
    bf_filter = scalars_df_index["bool_col"].fillna(True)
    bf_df = scalars_df_index.reset_index()[bf_filter]
    bf_result = bf_df.to_pandas()
    pd_filter = scalars_pandas_df_index["bool_col"].fillna(True)
    pd_result = scalars_pandas_df_index.reset_index()[pd_filter]

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    # reset_index should maintain the original ordering and index keys
    # post-filter will have gaps.
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_reset_index_with_unnamed_index(
    scalars_df_index,
    scalars_pandas_df_index,
):
    scalars_df_index = scalars_df_index.copy()
    scalars_pandas_df_index = scalars_pandas_df_index.copy()

    scalars_df_index.index.name = None
    scalars_pandas_df_index.index.name = None
    df = scalars_df_index.reset_index(drop=False)
    assert df.index.name is None

    # reset_index(drop=False) creates a new column "index".
    assert df.columns[0] == "index"

    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df_index.reset_index(drop=False)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    # reset_index should maintain the original ordering.
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_reset_index_with_unnamed_multiindex(
    scalars_df_index,
    scalars_pandas_df_index,
):
    bf_df = dataframe.DataFrame(
        ([1, 2, 3], [2, 5, 7]),
        index=pd.MultiIndex.from_tuples([("a", "aa"), ("a", "aa")]),
    )
    pd_df = pd.DataFrame(
        ([1, 2, 3], [2, 5, 7]),
        index=pd.MultiIndex.from_tuples([("a", "aa"), ("a", "aa")]),
    )

    bf_df = bf_df.reset_index()
    pd_df = pd_df.reset_index()

    assert pd_df.columns[0] == "level_0"
    assert bf_df.columns[0] == "level_0"
    assert pd_df.columns[1] == "level_1"
    assert bf_df.columns[1] == "level_1"


def test_reset_index_with_unnamed_index_and_index_column(
    scalars_df_index,
    scalars_pandas_df_index,
):
    scalars_df_index = scalars_df_index.copy()
    scalars_pandas_df_index = scalars_pandas_df_index.copy()

    scalars_df_index.index.name = None
    scalars_pandas_df_index.index.name = None
    df = scalars_df_index.assign(index=scalars_df_index["int64_col"]).reset_index(
        drop=False
    )
    assert df.index.name is None

    # reset_index(drop=False) creates a new column "level_0" if the "index" column already exists.
    assert df.columns[0] == "level_0"

    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df_index.assign(
        index=scalars_pandas_df_index["int64_col"]
    ).reset_index(drop=False)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    # reset_index should maintain the original ordering.
    pandas.testing.assert_frame_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("drop",),
    (
        (True,),
        (False,),
    ),
)
@pytest.mark.parametrize(
    ("append",),
    (
        (True,),
        (False,),
    ),
)
@pytest.mark.parametrize(
    ("index_column",),
    (("int64_too",), ("string_col",), ("timestamp_col",)),
)
def test_set_index(scalars_dfs, index_column, drop, append):
    scalars_df, scalars_pandas_df = scalars_dfs
    df = scalars_df.set_index(index_column, append=append, drop=drop)
    bf_result = df.to_pandas()
    pd_result = scalars_pandas_df.set_index(index_column, append=append, drop=drop)

    # Sort to disambiguate when there are duplicate index labels.
    # Note: Doesn't use assert_pandas_df_equal_ignore_ordering because we get
    # "ValueError: 'timestamp_col' is both an index level and a column label,
    # which is ambiguous" when trying to sort by a column with the same name as
    # the index.
    bf_result = bf_result.sort_values("rowindex_2")
    pd_result = pd_result.sort_values("rowindex_2")

    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_set_index_key_error(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    with pytest.raises(KeyError):
        scalars_pandas_df.set_index(["not_a_col"])
    with pytest.raises(KeyError):
        scalars_df.set_index(["not_a_col"])


@pytest.mark.parametrize(
    ("ascending",),
    ((True,), (False,)),
)
@pytest.mark.parametrize(
    ("na_position",),
    (("first",), ("last",)),
)
def test_sort_index(scalars_dfs, ascending, na_position):
    index_column = "int64_col"
    scalars_df, scalars_pandas_df = scalars_dfs
    df = scalars_df.set_index(index_column)
    bf_result = df.sort_index(ascending=ascending, na_position=na_position).to_pandas()
    pd_result = scalars_pandas_df.set_index(index_column).sort_index(
        ascending=ascending, na_position=na_position
    )
    pandas.testing.assert_frame_equal(bf_result, pd_result)


def test_df_abs(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    columns = ["int64_col", "int64_too", "float64_col"]

    bf_result = scalars_df[columns].abs().to_pandas()
    pd_result = scalars_pandas_df[columns].abs()

    assert_pandas_df_equal(bf_result, pd_result)


def test_df_isnull(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    columns = ["int64_col", "int64_too", "string_col", "bool_col"]
    bf_result = scalars_df[columns].isnull().to_pandas()
    pd_result = scalars_pandas_df[columns].isnull()

    # One of dtype mismatches to be documented. Here, the `bf_result.dtype` is
    # `BooleanDtype` but the `pd_result.dtype` is `bool`.
    pd_result["int64_col"] = pd_result["int64_col"].astype(pd.BooleanDtype())
    pd_result["int64_too"] = pd_result["int64_too"].astype(pd.BooleanDtype())
    pd_result["string_col"] = pd_result["string_col"].astype(pd.BooleanDtype())
    pd_result["bool_col"] = pd_result["bool_col"].astype(pd.BooleanDtype())

    assert_pandas_df_equal(bf_result, pd_result)


def test_df_notnull(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs

    columns = ["int64_col", "int64_too", "string_col", "bool_col"]
    bf_result = scalars_df[columns].notnull().to_pandas()
    pd_result = scalars_pandas_df[columns].notnull()

    # One of dtype mismatches to be documented. Here, the `bf_result.dtype` is
    # `BooleanDtype` but the `pd_result.dtype` is `bool`.
    pd_result["int64_col"] = pd_result["int64_col"].astype(pd.BooleanDtype())
    pd_result["int64_too"] = pd_result["int64_too"].astype(pd.BooleanDtype())
    pd_result["string_col"] = pd_result["string_col"].astype(pd.BooleanDtype())
    pd_result["bool_col"] = pd_result["bool_col"].astype(pd.BooleanDtype())

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("left_labels", "right_labels", "overwrite", "fill_value"),
    [
        (["a", "b", "c"], ["c", "a", "b"], True, None),
        (["a", "b", "c"], ["c", "a", "b"], False, None),
        (["a", "b", "c"], ["a", "b", "c"], False, 2),
    ],
    ids=[
        "one_one_match_overwrite",
        "one_one_match_no_overwrite",
        "exact_match",
    ],
)
def test_combine(
    scalars_df_index,
    scalars_df_2_index,
    scalars_pandas_df_index,
    left_labels,
    right_labels,
    overwrite,
    fill_value,
):
    if pd.__version__.startswith("1."):
        pytest.skip("pd.NA vs NaN not handled well in pandas 1.x.")
    columns = ["int64_too", "int64_col", "float64_col"]

    bf_df_a = scalars_df_index[columns]
    bf_df_a.columns = left_labels
    bf_df_b = scalars_df_2_index[columns]
    bf_df_b.columns = right_labels
    bf_result = bf_df_a.combine(
        bf_df_b,
        lambda x, y: x**2 + 2 * x * y + y**2,
        overwrite=overwrite,
        fill_value=fill_value,
    ).to_pandas()

    pd_df_a = scalars_pandas_df_index[columns]
    pd_df_a.columns = left_labels
    pd_df_b = scalars_pandas_df_index[columns]
    pd_df_b.columns = right_labels
    pd_result = pd_df_a.combine(
        pd_df_b,
        lambda x, y: x**2 + 2 * x * y + y**2,
        overwrite=overwrite,
        fill_value=fill_value,
    )

    # Some dtype inconsistency for all-NULL columns
    pd.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("overwrite", "filter_func"),
    [
        (True, None),
        (False, None),
        (True, lambda x: x.isna() | (x % 2 == 0)),
    ],
    ids=[
        "default",
        "overwritefalse",
        "customfilter",
    ],
)
def test_df_update(overwrite, filter_func):
    if pd.__version__.startswith("1."):
        pytest.skip("dtype handled differently in pandas 1.x.")
    index1 = pandas.Index([1, 2, 3, 4], dtype="Int64")
    index2 = pandas.Index([1, 2, 4, 5], dtype="Int64")
    pd_df1 = pandas.DataFrame(
        {"a": [1, None, 3, 4], "b": [5, 6, None, 8]}, dtype="Int64", index=index1
    )
    pd_df2 = pandas.DataFrame(
        {"a": [None, 20, 30, 40], "c": [90, None, 110, 120]},
        dtype="Int64",
        index=index2,
    )

    bf_df1 = dataframe.DataFrame(pd_df1)
    bf_df2 = dataframe.DataFrame(pd_df2)

    bf_df1.update(bf_df2, overwrite=overwrite, filter_func=filter_func)
    pd_df1.update(pd_df2, overwrite=overwrite, filter_func=filter_func)

    pd.testing.assert_frame_equal(bf_df1.to_pandas(), pd_df1)


def test_df_idxmin():
    pd_df = pd.DataFrame(
        {"a": [1, 2, 3], "b": [7, None, 3], "c": [4, 4, 4]}, index=["x", "y", "z"]
    )
    bf_df = dataframe.DataFrame(pd_df)

    bf_result = bf_df.idxmin().to_pandas()
    pd_result = pd_df.idxmin()

    pd.testing.assert_series_equal(
        bf_result, pd_result, check_index_type=False, check_dtype=False
    )


def test_df_idxmax():
    pd_df = pd.DataFrame(
        {"a": [1, 2, 3], "b": [7, None, 3], "c": [4, 4, 4]}, index=["x", "y", "z"]
    )
    bf_df = dataframe.DataFrame(pd_df)

    bf_result = bf_df.idxmax().to_pandas()
    pd_result = pd_df.idxmax()

    pd.testing.assert_series_equal(
        bf_result, pd_result, check_index_type=False, check_dtype=False
    )


@pytest.mark.parametrize(
    ("join", "axis"),
    [
        ("outer", None),
        ("outer", 0),
        ("outer", 1),
        ("left", 0),
        ("right", 1),
        ("inner", None),
        ("inner", 1),
    ],
)
def test_df_align(join, axis):
    index1 = pandas.Index([1, 2, 3, 4], dtype="Int64")
    index2 = pandas.Index([1, 2, 4, 5], dtype="Int64")
    pd_df1 = pandas.DataFrame(
        {"a": [1, None, 3, 4], "b": [5, 6, None, 8]}, dtype="Int64", index=index1
    )
    pd_df2 = pandas.DataFrame(
        {"a": [None, 20, 30, 40], "c": [90, None, 110, 120]},
        dtype="Int64",
        index=index2,
    )

    bf_df1 = dataframe.DataFrame(pd_df1)
    bf_df2 = dataframe.DataFrame(pd_df2)

    bf_result1, bf_result2 = bf_df1.align(bf_df2, join=join, axis=axis)
    pd_result1, pd_result2 = pd_df1.align(pd_df2, join=join, axis=axis)

    # Don't check dtype as pandas does unnecessary float conversion
    pd.testing.assert_frame_equal(bf_result1.to_pandas(), pd_result1, check_dtype=False)
    pd.testing.assert_frame_equal(bf_result2.to_pandas(), pd_result2, check_dtype=False)


def test_combine_first(
    scalars_df_index,
    scalars_df_2_index,
    scalars_pandas_df_index,
):
    if pd.__version__.startswith("1."):
        pytest.skip("pd.NA vs NaN not handled well in pandas 1.x.")
    columns = ["int64_too", "int64_col", "float64_col"]

    bf_df_a = scalars_df_index[columns].iloc[0:6]
    bf_df_a.columns = ["a", "b", "c"]
    bf_df_b = scalars_df_2_index[columns].iloc[2:8]
    bf_df_b.columns = ["b", "a", "d"]
    bf_result = bf_df_a.combine_first(bf_df_b).to_pandas()

    pd_df_a = scalars_pandas_df_index[columns].iloc[0:6]
    pd_df_a.columns = ["a", "b", "c"]
    pd_df_b = scalars_pandas_df_index[columns].iloc[2:8]
    pd_df_b.columns = ["b", "a", "d"]
    pd_result = pd_df_a.combine_first(pd_df_b)

    # Some dtype inconsistency for all-NULL columns
    pd.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("op"),
    [
        operator.add,
        operator.sub,
        operator.mul,
        operator.truediv,
        operator.floordiv,
        operator.eq,
        operator.ne,
        operator.gt,
        operator.ge,
        operator.lt,
        operator.le,
    ],
    ids=[
        "add",
        "subtract",
        "multiply",
        "true_divide",
        "floor_divide",
        "eq",
        "ne",
        "gt",
        "ge",
        "lt",
        "le",
    ],
)
# TODO(garrettwu): deal with NA values
@pytest.mark.parametrize(("other_scalar"), [1, 2.5, 0, 0.0])
@pytest.mark.parametrize(("reverse_operands"), [True, False])
def test_scalar_binop(scalars_dfs, op, other_scalar, reverse_operands):
    scalars_df, scalars_pandas_df = scalars_dfs
    columns = ["int64_col", "float64_col"]

    maybe_reversed_op = (lambda x, y: op(y, x)) if reverse_operands else op

    bf_result = maybe_reversed_op(scalars_df[columns], other_scalar).to_pandas()
    pd_result = maybe_reversed_op(scalars_pandas_df[columns], other_scalar)

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.parametrize(("other_scalar"), [1, -2])
def test_mod(scalars_dfs, other_scalar):
    # Zero case excluded as pandas produces 0 result for Int64 inputs rather than NA/NaN.
    # This is likely a pandas bug as mod 0 is undefined in other dtypes, and most programming languages.
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (scalars_df[["int64_col", "int64_too"]] % other_scalar).to_pandas()
    pd_result = scalars_pandas_df[["int64_col", "int64_too"]] % other_scalar

    assert_pandas_df_equal(bf_result, pd_result)


def test_scalar_binop_str_exception(scalars_dfs):
    scalars_df, _ = scalars_dfs
    columns = ["string_col"]
    with pytest.raises(TypeError):
        (scalars_df[columns] + 1).to_pandas()


@pytest.mark.parametrize(
    ("op"),
    [
        (lambda x, y: x.add(y, axis="index")),
        (lambda x, y: x.radd(y, axis="index")),
        (lambda x, y: x.sub(y, axis="index")),
        (lambda x, y: x.rsub(y, axis="index")),
        (lambda x, y: x.mul(y, axis="index")),
        (lambda x, y: x.rmul(y, axis="index")),
        (lambda x, y: x.truediv(y, axis="index")),
        (lambda x, y: x.rtruediv(y, axis="index")),
        (lambda x, y: x.floordiv(y, axis="index")),
        (lambda x, y: x.floordiv(y, axis="index")),
        (lambda x, y: x.gt(y, axis="index")),
        (lambda x, y: x.ge(y, axis="index")),
        (lambda x, y: x.lt(y, axis="index")),
        (lambda x, y: x.le(y, axis="index")),
    ],
    ids=[
        "add",
        "radd",
        "sub",
        "rsub",
        "mul",
        "rmul",
        "truediv",
        "rtruediv",
        "floordiv",
        "rfloordiv",
        "gt",
        "ge",
        "lt",
        "le",
    ],
)
def test_series_binop_axis_index(
    scalars_dfs,
    op,
):
    scalars_df, scalars_pandas_df = scalars_dfs
    df_columns = ["int64_col", "float64_col"]
    series_column = "int64_too"

    bf_result = op(scalars_df[df_columns], scalars_df[series_column]).to_pandas()
    pd_result = op(scalars_pandas_df[df_columns], scalars_pandas_df[series_column])

    assert_pandas_df_equal(bf_result, pd_result)


@pytest.mark.parametrize(
    ("left_labels", "right_labels"),
    [
        (["a", "a", "b"], ["c", "c", "d"]),
        (["a", "b", "c"], ["c", "a", "b"]),
        (["a", "c", "c"], ["c", "a", "c"]),
        (["a", "b", "c"], ["a", "b", "c"]),
    ],
    ids=[
        "no_overlap",
        "one_one_match",
        "multi_match",
        "exact_match",
    ],
)
def test_binop_df_df_binary_op(
    scalars_df_index,
    scalars_df_2_index,
    scalars_pandas_df_index,
    left_labels,
    right_labels,
):
    if pd.__version__.startswith("1."):
        pytest.skip("pd.NA vs NaN not handled well in pandas 1.x.")
    columns = ["int64_too", "int64_col", "float64_col"]

    bf_df_a = scalars_df_index[columns]
    bf_df_a.columns = left_labels
    bf_df_b = scalars_df_2_index[columns]
    bf_df_b.columns = right_labels
    bf_result = (bf_df_a - bf_df_b).to_pandas()

    pd_df_a = scalars_pandas_df_index[columns]
    pd_df_a.columns = left_labels
    pd_df_b = scalars_pandas_df_index[columns]
    pd_df_b.columns = right_labels
    pd_result = pd_df_a - pd_df_b

    # Some dtype inconsistency for all-NULL columns
    pd.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


# Differnt table will only work for explicit index, since default index orders are arbitrary.
@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_series_binop_add_different_table(
    scalars_df_index, scalars_pandas_df_index, scalars_df_2_index, ordered
):
    df_columns = ["int64_col", "float64_col"]
    series_column = "int64_too"

    bf_result = (
        scalars_df_index[df_columns]
        .add(scalars_df_2_index[series_column], axis="index")
        .to_pandas(ordered=ordered)
    )
    pd_result = scalars_pandas_df_index[df_columns].add(
        scalars_pandas_df_index[series_column], axis="index"
    )

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=not ordered)


# TODO(garrettwu): Test series binop with different index

all_joins = pytest.mark.parametrize(
    ("how",),
    (("outer",), ("left",), ("right",), ("inner",), ("cross",)),
)


@all_joins
def test_join_same_table(scalars_dfs, how):
    bf_df, pd_df = scalars_dfs

    bf_df_a = bf_df.set_index("int64_too")[["string_col", "int64_col"]]
    bf_df_b = bf_df.set_index("int64_too")[["float64_col"]]
    bf_result = bf_df_a.join(bf_df_b, how=how).to_pandas()
    pd_df_a = pd_df.set_index("int64_too")[["string_col", "int64_col"]]
    pd_df_b = pd_df.set_index("int64_too")[["float64_col"]]
    pd_result = pd_df_a.join(pd_df_b, how=how)
    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


@all_joins
def test_join_different_table(
    scalars_df_index, scalars_df_2_index, scalars_pandas_df_index, how
):
    bf_df_a = scalars_df_index[["string_col", "int64_col"]]
    bf_df_b = scalars_df_2_index.dropna()[["float64_col"]]
    bf_result = bf_df_a.join(bf_df_b, how=how).to_pandas()
    pd_df_a = scalars_pandas_df_index[["string_col", "int64_col"]]
    pd_df_b = scalars_pandas_df_index.dropna()[["float64_col"]]
    pd_result = pd_df_a.join(pd_df_b, how=how)
    assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


def test_join_duplicate_columns_raises_not_implemented(scalars_dfs):
    scalars_df, _ = scalars_dfs
    df_a = scalars_df[["string_col", "float64_col"]]
    df_b = scalars_df[["float64_col"]]
    with pytest.raises(NotImplementedError):
        df_a.join(df_b, how="outer").to_pandas()


@all_joins
def test_join_param_on(scalars_dfs, how):
    bf_df, pd_df = scalars_dfs

    bf_df_a = bf_df[["string_col", "int64_col", "rowindex_2"]]
    bf_df_a = bf_df_a.assign(rowindex_2=bf_df_a["rowindex_2"] + 2)
    bf_df_b = bf_df[["float64_col"]]

    if how == "cross":
        with pytest.raises(ValueError):
            bf_df_a.join(bf_df_b, on="rowindex_2", how=how)
    else:
        bf_result = bf_df_a.join(bf_df_b, on="rowindex_2", how=how).to_pandas()

        pd_df_a = pd_df[["string_col", "int64_col", "rowindex_2"]]
        pd_df_a = pd_df_a.assign(rowindex_2=pd_df_a["rowindex_2"] + 2)
        pd_df_b = pd_df[["float64_col"]]
        pd_result = pd_df_a.join(pd_df_b, on="rowindex_2", how=how)
        assert_pandas_df_equal(bf_result, pd_result, ignore_order=True)


@pytest.mark.parametrize(
    ("by", "ascending", "na_position"),
    [
        ("int64_col", True, "first"),
        (["bool_col", "int64_col"], True, "last"),
        ("int64_col", False, "first"),
        (["bool_col", "int64_col"], [False, True], "last"),
        (["bool_col", "int64_col"], [True, False], "first"),
    ],
)
def test_dataframe_sort_values(
    scalars_df_index, scalars_pandas_df_index, by, ascending, na_position
):
    # Test needs values to be unique
    bf_result = scalars_df_index.sort_values(
        by, ascending=ascending, na_position=na_position
    ).to_pandas()
    pd_result = scalars_pandas_df_index.sort_values(
        by, ascending=ascending, na_position=na_position
    )

    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_dataframe_sort_values_stable(scalars_df_index, scalars_pandas_df_index):
    bf_result = (
        scalars_df_index.sort_values("int64_col", kind="stable")
        .sort_values("bool_col", kind="stable")
        .to_pandas()
    )
    pd_result = scalars_pandas_df_index.sort_values(
        "int64_col", kind="stable"
    ).sort_values("bool_col", kind="stable")

    pandas.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    ("operator", "columns"),
    [
        pytest.param(lambda x: x.cumsum(), ["float64_col", "int64_too"]),
        pytest.param(lambda x: x.cumprod(), ["float64_col", "int64_too"]),
        pytest.param(
            lambda x: x.cumprod(),
            ["string_col"],
            marks=pytest.mark.xfail(
                raises=ValueError,
            ),
        ),
    ],
    ids=[
        "cumsum",
        "cumprod",
        "non-numeric",
    ],
)
def test_dataframe_numeric_analytic_op(
    scalars_df_index, scalars_pandas_df_index, operator, columns
):
    # TODO: Add nullable ints (pandas 1.x has poor behavior on these)
    bf_series = operator(scalars_df_index[columns])
    pd_series = operator(scalars_pandas_df_index[columns])
    bf_result = bf_series.to_pandas()
    pd.testing.assert_frame_equal(pd_series, bf_result, check_dtype=False)


@pytest.mark.parametrize(
    ("operator"),
    [
        (lambda x: x.cummin()),
        (lambda x: x.cummax()),
        (lambda x: x.shift(2)),
        (lambda x: x.shift(-2)),
    ],
    ids=[
        "cummin",
        "cummax",
        "shiftpostive",
        "shiftnegative",
    ],
)
def test_dataframe_general_analytic_op(
    scalars_df_index, scalars_pandas_df_index, operator
):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col"]
    bf_series = operator(scalars_df_index[col_names])
    pd_series = operator(scalars_pandas_df_index[col_names])
    bf_result = bf_series.to_pandas()
    pd.testing.assert_frame_equal(
        pd_series,
        bf_result,
    )


@pytest.mark.parametrize(
    ("periods",),
    [
        (1,),
        (2,),
        (-1,),
    ],
)
def test_dataframe_diff(scalars_df_index, scalars_pandas_df_index, periods):
    col_names = ["int64_too", "float64_col", "int64_col"]
    bf_result = scalars_df_index[col_names].diff(periods=periods).to_pandas()
    pd_result = scalars_pandas_df_index[col_names].diff(periods=periods)
    pd.testing.assert_frame_equal(
        pd_result,
        bf_result,
    )


@pytest.mark.parametrize(
    ("periods",),
    [
        (1,),
        (2,),
        (-1,),
    ],
)
def test_dataframe_pct_change(scalars_df_index, scalars_pandas_df_index, periods):
    col_names = ["int64_too", "float64_col", "int64_col"]
    bf_result = scalars_df_index[col_names].pct_change(periods=periods).to_pandas()
    pd_result = scalars_pandas_df_index[col_names].pct_change(periods=periods)
    pd.testing.assert_frame_equal(
        pd_result,
        bf_result,
    )


def test_dataframe_agg_single_string(scalars_dfs):
    numeric_cols = ["int64_col", "int64_too", "float64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[numeric_cols].agg("sum").to_pandas()
    pd_result = scalars_pandas_df[numeric_cols].agg("sum")

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")
    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


def test_dataframe_agg_multi_string(scalars_dfs):
    numeric_cols = ["int64_col", "int64_too", "float64_col"]
    aggregations = [
        "sum",
        "mean",
        "median",
        "std",
        "var",
        "min",
        "max",
        "nunique",
        "count",
    ]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[numeric_cols].agg(aggregations).to_pandas()
    pd_result = scalars_pandas_df[numeric_cols].agg(aggregations)

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    # Drop median, as it's an approximation.
    bf_median = bf_result.loc["median", :]
    bf_result = bf_result.drop(labels=["median"])
    pd_result = pd_result.drop(labels=["median"])

    pd.testing.assert_frame_equal(pd_result, bf_result, check_index_type=False)

    # Double-check that median is at least plausible.
    assert (
        (bf_result.loc["min", :] <= bf_median) & (bf_median <= bf_result.loc["max", :])
    ).all()


def test_df_describe(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    # pyarrows time columns fail in pandas
    unsupported_columns = ["datetime_col", "timestamp_col", "time_col", "date_col"]
    bf_result = scalars_df.describe().to_pandas()

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

    pd.testing.assert_frame_equal(pd_result, bf_result, check_index_type=False)

    # Double-check that quantiles are at least plausible.
    assert (
        (bf_min <= bf_p25)
        & (bf_p25 <= bf_p50)
        & (bf_p50 <= bf_p50)
        & (bf_p75 <= bf_max)
    ).all()


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_df_stack(scalars_dfs, ordered):
    if pandas.__version__.startswith("1.") or pandas.__version__.startswith("2.0"):
        pytest.skip("pandas <2.1 uses different stack implementation")
    scalars_df, scalars_pandas_df = scalars_dfs
    # To match bigquery dataframes
    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_pandas_df.columns = scalars_pandas_df.columns.astype("string[pyarrow]")
    # Can only stack identically-typed columns
    columns = ["int64_col", "int64_too", "rowindex_2"]

    bf_result = scalars_df[columns].stack().to_pandas(ordered=ordered)
    pd_result = scalars_pandas_df[columns].stack(future_stack=True)

    # Pandas produces NaN, where bq dataframes produces pd.NA
    assert_series_equal(
        bf_result, pd_result, check_dtype=False, ignore_order=not ordered
    )


def test_df_melt_default(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    # To match bigquery dataframes
    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_pandas_df.columns = scalars_pandas_df.columns.astype("string[pyarrow]")
    # Can only stack identically-typed columns
    columns = ["int64_col", "int64_too", "rowindex_2"]

    bf_result = scalars_df[columns].melt().to_pandas()
    pd_result = scalars_pandas_df[columns].melt()

    # Pandas produces int64 index, Bigframes produces Int64 (nullable)
    pd.testing.assert_frame_equal(
        bf_result, pd_result, check_index_type=False, check_dtype=False
    )


def test_df_melt_parameterized(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    # To match bigquery dataframes
    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_pandas_df.columns = scalars_pandas_df.columns.astype("string[pyarrow]")
    # Can only stack identically-typed columns

    bf_result = scalars_df.melt(
        var_name="alice",
        value_name="bob",
        id_vars=["string_col"],
        value_vars=["int64_col", "int64_too"],
    ).to_pandas()
    pd_result = scalars_pandas_df.melt(
        var_name="alice",
        value_name="bob",
        id_vars=["string_col"],
        value_vars=["int64_col", "int64_too"],
    )

    # Pandas produces int64 index, Bigframes produces Int64 (nullable)
    pd.testing.assert_frame_equal(
        bf_result, pd_result, check_index_type=False, check_dtype=False
    )


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_df_unstack(scalars_dfs, ordered):
    scalars_df, scalars_pandas_df = scalars_dfs
    # To match bigquery dataframes
    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_pandas_df.columns = scalars_pandas_df.columns.astype("string[pyarrow]")
    # Can only stack identically-typed columns
    columns = [
        "rowindex_2",
        "int64_col",
        "int64_too",
    ]

    # unstack on mono-index produces series
    bf_result = scalars_df[columns].unstack().to_pandas(ordered=ordered)
    pd_result = scalars_pandas_df[columns].unstack()

    # Pandas produces NaN, where bq dataframes produces pd.NA
    assert_series_equal(
        bf_result, pd_result, check_dtype=False, ignore_order=not ordered
    )


@pytest.mark.parametrize(
    ("values", "index", "columns"),
    [
        ("int64_col", "int64_too", ["string_col"]),
        (["int64_col"], "int64_too", ["string_col"]),
        (["int64_col", "float64_col"], "int64_too", ["string_col"]),
    ],
)
def test_df_pivot(scalars_dfs, values, index, columns):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = scalars_df.pivot(
        values=values, index=index, columns=columns
    ).to_pandas()
    pd_result = scalars_pandas_df.pivot(values=values, index=index, columns=columns)

    # Pandas produces NaN, where bq dataframes produces pd.NA
    pd.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


@pytest.mark.parametrize(
    ("values", "index", "columns"),
    [
        (["goals", "assists"], ["team_name", "season"], ["position"]),
        (["goals", "assists"], ["season"], ["team_name", "position"]),
    ],
)
def test_df_pivot_hockey(hockey_df, hockey_pandas_df, values, index, columns):
    bf_result = (
        hockey_df.reset_index()
        .pivot(values=values, index=index, columns=columns)
        .to_pandas()
    )
    pd_result = hockey_pandas_df.reset_index().pivot(
        values=values, index=index, columns=columns
    )

    # Pandas produces NaN, where bq dataframes produces pd.NA
    pd.testing.assert_frame_equal(bf_result, pd_result, check_dtype=False)


def test_ipython_key_completions_with_drop(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_names = "string_col"
    bf_dataframe = scalars_df.drop(columns=col_names)
    pd_dataframe = scalars_pandas_df.drop(columns=col_names)
    expected = pd_dataframe.columns.tolist()

    results = bf_dataframe._ipython_key_completions_()

    assert col_names not in results
    assert results == expected
    # _ipython_key_completions_ is called with square brackets
    # so only column names are relevant with tab completion
    assert "to_gbq" not in results
    assert "merge" not in results
    assert "drop" not in results


def test_ipython_key_completions_with_rename(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name_dict = {"string_col": "a_renamed_column"}
    bf_dataframe = scalars_df.rename(columns=col_name_dict)
    pd_dataframe = scalars_pandas_df.rename(columns=col_name_dict)
    expected = pd_dataframe.columns.tolist()

    results = bf_dataframe._ipython_key_completions_()

    assert "string_col" not in results
    assert "a_renamed_column" in results
    assert results == expected
    # _ipython_key_completions_ is called with square brackets
    # so only column names are relevant with tab completion
    assert "to_gbq" not in results
    assert "merge" not in results
    assert "drop" not in results


def test__dir__with_drop(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_names = "string_col"
    bf_dataframe = scalars_df.drop(columns=col_names)
    pd_dataframe = scalars_pandas_df.drop(columns=col_names)
    expected = pd_dataframe.columns.tolist()

    results = dir(bf_dataframe)

    assert col_names not in results
    assert frozenset(expected) <= frozenset(results)
    # __dir__ is called with a '.' and displays all methods, columns names, etc.
    assert "to_gbq" in results
    assert "merge" in results
    assert "drop" in results


def test__dir__with_rename(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    col_name_dict = {"string_col": "a_renamed_column"}
    bf_dataframe = scalars_df.rename(columns=col_name_dict)
    pd_dataframe = scalars_pandas_df.rename(columns=col_name_dict)
    expected = pd_dataframe.columns.tolist()

    results = dir(bf_dataframe)

    assert "string_col" not in results
    assert "a_renamed_column" in results
    assert frozenset(expected) <= frozenset(results)
    # __dir__ is called with a '.' and displays all methods, columns names, etc.
    assert "to_gbq" in results
    assert "merge" in results
    assert "drop" in results


@pytest.mark.parametrize(
    ("start", "stop", "step"),
    [
        (0, 0, None),
        (None, None, None),
        (1, None, None),
        (None, 4, None),
        (None, None, 2),
        (None, 50000000000, 1),
        (5, 4, None),
        (3, None, 2),
        (1, 7, 2),
        (1, 7, 50000000000),
    ],
)
def test_iloc_slice(scalars_df_index, scalars_pandas_df_index, start, stop, step):
    bf_result = scalars_df_index.iloc[start:stop:step].to_pandas()
    pd_result = scalars_pandas_df_index.iloc[start:stop:step]
    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_iloc_slice_zero_step(scalars_df_index):
    with pytest.raises(ValueError):
        scalars_df_index.iloc[0:0:0]


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_iloc_slice_nested(scalars_df_index, scalars_pandas_df_index, ordered):
    bf_result = scalars_df_index.iloc[1:].iloc[1:].to_pandas(ordered=ordered)
    pd_result = scalars_pandas_df_index.iloc[1:].iloc[1:]

    assert_pandas_df_equal(bf_result, pd_result, ignore_order=not ordered)


@pytest.mark.parametrize(
    "index",
    [0, 5, -2, (2,)],
)
def test_iloc_single_integer(scalars_df_index, scalars_pandas_df_index, index):
    bf_result = scalars_df_index.iloc[index]
    pd_result = scalars_pandas_df_index.iloc[index]

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


@pytest.mark.parametrize(
    "index",
    [(2, 5), (5, 0), (0, 0)],
)
def test_iloc_tuple(scalars_df_index, scalars_pandas_df_index, index):
    bf_result = scalars_df_index.iloc[index]
    pd_result = scalars_pandas_df_index.iloc[index]

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("index", "error"),
    [
        ((1, 1, 1), pd.errors.IndexingError),
        (("asd", "asd", "asd"), pd.errors.IndexingError),
        (("asd"), TypeError),
    ],
)
def test_iloc_tuple_errors(scalars_df_index, scalars_pandas_df_index, index, error):
    with pytest.raises(error):
        scalars_df_index.iloc[index]
    with pytest.raises(error):
        scalars_pandas_df_index.iloc[index]


@pytest.mark.parametrize(
    "index",
    [(2, 5), (5, 0), (0, 0)],
)
def test_iat(scalars_df_index, scalars_pandas_df_index, index):
    bf_result = scalars_df_index.iat[index]
    pd_result = scalars_pandas_df_index.iat[index]

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("index", "error"),
    [
        (0, TypeError),
        ("asd", ValueError),
        ((1, 2, 3), TypeError),
        (("asd", "asd"), ValueError),
    ],
)
def test_iat_errors(scalars_df_index, scalars_pandas_df_index, index, error):
    with pytest.raises(error):
        scalars_pandas_df_index.iat[index]
    with pytest.raises(error):
        scalars_df_index.iat[index]


def test_iloc_single_integer_out_of_bound_error(
    scalars_df_index, scalars_pandas_df_index
):
    with pytest.raises(IndexError, match="single positional indexer is out-of-bounds"):
        scalars_df_index.iloc[99]


def test_loc_bool_series(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.loc[scalars_df_index.bool_col].to_pandas()
    pd_result = scalars_pandas_df_index.loc[scalars_pandas_df_index.bool_col]

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_loc_select_column(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.loc[:, "int64_col"].to_pandas()
    pd_result = scalars_pandas_df_index.loc[:, "int64_col"]
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_loc_single_index_with_duplicate(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("string_col", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index(
        "string_col", drop=False
    )
    index = "Hello, World!"
    bf_result = scalars_df_index.loc[index]
    pd_result = scalars_pandas_df_index.loc[index]
    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_single_index_no_duplicate(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("int64_too", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("int64_too", drop=False)
    index = -2345
    bf_result = scalars_df_index.loc[index]
    pd_result = scalars_pandas_df_index.loc[index]
    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_at_with_duplicate(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("string_col", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index(
        "string_col", drop=False
    )
    index = "Hello, World!"
    bf_result = scalars_df_index.at[index, "int64_too"]
    pd_result = scalars_pandas_df_index.at[index, "int64_too"]
    pd.testing.assert_series_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_at_no_duplicate(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.set_index("int64_too", drop=False)
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("int64_too", drop=False)
    index = -2345
    bf_result = scalars_df_index.at[index, "string_col"]
    pd_result = scalars_pandas_df_index.at[index, "string_col"]
    assert bf_result == pd_result


def test_loc_setitem_bool_series_scalar_new_col(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df.loc[bf_df["int64_too"] == 0, "new_col"] = 99
    pd_df.loc[pd_df["int64_too"] == 0, "new_col"] = 99

    # pandas type difference
    pd_df["new_col"] = pd_df["new_col"].astype("Float64")

    pd.testing.assert_frame_equal(
        bf_df.to_pandas(),
        pd_df,
    )


def test_loc_setitem_bool_series_scalar_existing_col(scalars_dfs):
    if pd.__version__.startswith("1."):
        pytest.skip("this loc overload not supported in pandas 1.x.")

    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()
    bf_df.loc[bf_df["int64_too"] == 1, "string_col"] = "hello"
    pd_df.loc[pd_df["int64_too"] == 1, "string_col"] = "hello"

    pd.testing.assert_frame_equal(
        bf_df.to_pandas(),
        pd_df,
    )


def test_loc_setitem_bool_series_scalar_type_error(scalars_dfs):
    if pd.__version__.startswith("1."):
        pytest.skip("this loc overload not supported in pandas 1.x.")

    scalars_df, scalars_pandas_df = scalars_dfs
    bf_df = scalars_df.copy()
    pd_df = scalars_pandas_df.copy()

    with pytest.raises(TypeError):
        bf_df.loc[bf_df["int64_too"] == 1, "string_col"] = 99
    with pytest.raises(TypeError):
        pd_df.loc[pd_df["int64_too"] == 1, "string_col"] = 99


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
@pytest.mark.parametrize(
    ("op"),
    [
        (lambda x: x.sum(numeric_only=True)),
        (lambda x: x.mean(numeric_only=True)),
        (lambda x: x.min(numeric_only=True)),
        (lambda x: x.max(numeric_only=True)),
        (lambda x: x.std(numeric_only=True)),
        (lambda x: x.var(numeric_only=True)),
        (lambda x: x.count(numeric_only=False)),
        (lambda x: x.nunique()),
    ],
    ids=["sum", "mean", "min", "max", "std", "var", "count", "nunique"],
)
def test_dataframe_aggregates(scalars_df_index, scalars_pandas_df_index, op, ordered):
    col_names = ["int64_too", "float64_col", "string_col", "int64_col", "bool_col"]
    bf_series = op(scalars_df_index[col_names])
    pd_series = op(scalars_pandas_df_index[col_names])
    bf_result = bf_series.to_pandas(ordered=ordered)

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_series = pd_series.astype("Float64")
    # Pandas has object index type
    assert_series_equal(
        pd_series, bf_result, check_index_type=False, ignore_order=not ordered
    )


@pytest.mark.parametrize(
    ("op"),
    [
        (lambda x: x.sum(axis=1, numeric_only=True)),
        (lambda x: x.mean(axis=1, numeric_only=True)),
        (lambda x: x.min(axis=1, numeric_only=True)),
        (lambda x: x.max(axis=1, numeric_only=True)),
        (lambda x: x.std(axis=1, numeric_only=True)),
        (lambda x: x.var(axis=1, numeric_only=True)),
    ],
    ids=["sum", "mean", "min", "max", "std", "var"],
)
def test_dataframe_aggregates_axis_1(scalars_df_index, scalars_pandas_df_index, op):
    col_names = ["int64_too", "int64_col", "float64_col", "bool_col", "string_col"]
    bf_result = op(scalars_df_index[col_names]).to_pandas()
    pd_result = op(scalars_pandas_df_index[col_names])

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")
    # Pandas has object index type
    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


def test_dataframe_aggregates_median(scalars_df_index, scalars_pandas_df_index):
    col_names = ["int64_too", "float64_col", "int64_col", "bool_col"]
    bf_result = scalars_df_index[col_names].median(numeric_only=True).to_pandas()
    pd_result = scalars_pandas_df_index[col_names].agg(["min", "max"])

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    # Median is an approximation, but double-check that median is plausible.
    for col in col_names:
        assert (pd_result.loc["min", col] <= bf_result[col]) and (
            bf_result[col] <= pd_result.loc["max", col]
        )


@pytest.mark.parametrize(
    ("op"),
    [
        (lambda x: x.all(bool_only=True)),
        (lambda x: x.any(bool_only=True)),
        (lambda x: x.all(axis=1, bool_only=True)),
        (lambda x: x.any(axis=1, bool_only=True)),
    ],
    ids=["all_axis0", "any_axis0", "all_axis1", "any_axis1"],
)
def test_dataframe_bool_aggregates(scalars_df_index, scalars_pandas_df_index, op):
    # Pandas will drop nullable 'boolean' dtype so we convert first to bool, then cast back later
    scalars_df_index = scalars_df_index.assign(
        bool_col=scalars_df_index.bool_col.fillna(False)
    )
    scalars_pandas_df_index = scalars_pandas_df_index.assign(
        bool_col=scalars_pandas_df_index.bool_col.fillna(False).astype("bool")
    )
    bf_series = op(scalars_df_index)
    pd_series = op(scalars_pandas_df_index).astype("boolean")
    bf_result = bf_series.to_pandas()

    # Pandas has object index type
    pd.testing.assert_series_equal(pd_series, bf_result, check_index_type=False)


def test_dataframe_prod(scalars_df_index, scalars_pandas_df_index):
    col_names = ["int64_too", "float64_col"]
    bf_series = scalars_df_index[col_names].prod()
    pd_series = scalars_pandas_df_index[col_names].prod()
    bf_result = bf_series.to_pandas()

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_series = pd_series.astype("Float64")
    # Pandas has object index type
    pd.testing.assert_series_equal(pd_series, bf_result, check_index_type=False)


def test_df_skew_too_few_values(scalars_dfs):
    columns = ["float64_col", "int64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[columns].head(2).skew().to_pandas()
    pd_result = scalars_pandas_df[columns].head(2).skew()

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


@pytest.mark.parametrize(
    ("ordered"),
    [
        (True),
        (False),
    ],
)
def test_df_skew(scalars_dfs, ordered):
    columns = ["float64_col", "int64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[columns].skew().to_pandas(ordered=ordered)
    pd_result = scalars_pandas_df[columns].skew()

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    assert_series_equal(
        pd_result, bf_result, check_index_type=False, ignore_order=not ordered
    )


def test_df_kurt_too_few_values(scalars_dfs):
    columns = ["float64_col", "int64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[columns].head(2).kurt().to_pandas()
    pd_result = scalars_pandas_df[columns].head(2).kurt()

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


def test_df_kurt(scalars_dfs):
    columns = ["float64_col", "int64_col"]
    scalars_df, scalars_pandas_df = scalars_dfs
    bf_result = scalars_df[columns].kurt().to_pandas()
    pd_result = scalars_pandas_df[columns].kurt()

    # Pandas may produce narrower numeric types, but bigframes always produces Float64
    pd_result = pd_result.astype("Float64")

    pd.testing.assert_series_equal(pd_result, bf_result, check_index_type=False)


@pytest.mark.parametrize(
    ("frac", "n", "random_state"),
    [
        (None, 4, None),
        (0.5, None, None),
        (None, 4, 10),
        (0.5, None, 10),
        (None, None, None),
    ],
    ids=[
        "n_wo_random_state",
        "frac_wo_random_state",
        "n_w_random_state",
        "frac_w_random_state",
        "n_default",
    ],
)
def test_sample(scalars_dfs, frac, n, random_state):
    scalars_df, _ = scalars_dfs
    df = scalars_df.sample(frac=frac, n=n, random_state=random_state)
    bf_result = df.to_pandas()

    n = 1 if n is None else n
    expected_sample_size = round(frac * scalars_df.shape[0]) if frac is not None else n
    assert bf_result.shape[0] == expected_sample_size
    assert bf_result.shape[1] == scalars_df.shape[1]


def test_sample_determinism(penguins_df_default_index):
    df = penguins_df_default_index.sample(n=100, random_state=12345).head(15)
    bf_result = df.to_pandas()
    bf_result2 = df.to_pandas()

    pandas.testing.assert_frame_equal(bf_result, bf_result2)


def test_sample_raises_value_error(scalars_dfs):
    scalars_df, _ = scalars_dfs
    with pytest.raises(
        ValueError, match="Only one of 'n' or 'frac' parameter can be specified."
    ):
        scalars_df.sample(frac=0.5, n=4)


@pytest.mark.parametrize(
    ("axis",),
    [
        (None,),
        (0,),
        (1,),
    ],
)
def test_df_add_prefix(scalars_df_index, scalars_pandas_df_index, axis):
    if pd.__version__.startswith("1."):
        pytest.skip("add_prefix axis parameter not supported in pandas 1.x.")
    bf_result = scalars_df_index.add_prefix("prefix_", axis).to_pandas()

    pd_result = scalars_pandas_df_index.add_prefix("prefix_", axis)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
    )


@pytest.mark.parametrize(
    ("axis",),
    [
        (0,),
        (1,),
    ],
)
def test_df_add_suffix(scalars_df_index, scalars_pandas_df_index, axis):
    if pd.__version__.startswith("1."):
        pytest.skip("add_prefix axis parameter not supported in pandas 1.x.")
    bf_result = scalars_df_index.add_suffix("_suffix", axis).to_pandas()

    pd_result = scalars_pandas_df_index.add_suffix("_suffix", axis)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
        check_index_type=False,
    )


def test_df_columns_filter_items(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("2.0") or pd.__version__.startswith("1."):
        pytest.skip("pandas filter items behavior different pre-2.1")
    bf_result = scalars_df_index.filter(items=["string_col", "int64_col"]).to_pandas()

    pd_result = scalars_pandas_df_index.filter(items=["string_col", "int64_col"])
    # Ignore column ordering as pandas order differently depending on version
    pd.testing.assert_frame_equal(
        bf_result.sort_index(axis=1),
        pd_result.sort_index(axis=1),
    )


def test_df_columns_filter_like(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.filter(like="64_col").to_pandas()

    pd_result = scalars_pandas_df_index.filter(like="64_col")

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_columns_filter_regex(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.filter(regex="^[^_]+$").to_pandas()

    pd_result = scalars_pandas_df_index.filter(regex="^[^_]+$")

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_rows_filter_items(scalars_df_index, scalars_pandas_df_index):
    if pd.__version__.startswith("2.0") or pd.__version__.startswith("1."):
        pytest.skip("pandas filter items behavior different pre-2.1")
    bf_result = scalars_df_index.filter(items=[5, 1, 3], axis=0).to_pandas()

    pd_result = scalars_pandas_df_index.filter(items=[5, 1, 3], axis=0)

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    # Ignore ordering as pandas order differently depending on version
    assert_pandas_df_equal(
        bf_result,
        pd_result,
        ignore_order=True,
        check_names=False,
    )


def test_df_rows_filter_like(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.copy().set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.copy().set_index("string_col")

    bf_result = scalars_df_index.filter(like="ello", axis=0).to_pandas()

    pd_result = scalars_pandas_df_index.filter(like="ello", axis=0)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_rows_filter_regex(scalars_df_index, scalars_pandas_df_index):
    scalars_df_index = scalars_df_index.copy().set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.copy().set_index("string_col")

    bf_result = scalars_df_index.filter(regex="^[GH].*", axis=0).to_pandas()

    pd_result = scalars_pandas_df_index.filter(regex="^[GH].*", axis=0)

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_reindex_rows_list(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.reindex(index=[5, 1, 3, 99, 1]).to_pandas()

    pd_result = scalars_pandas_df_index.reindex(index=[5, 1, 3, 99, 1])

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_reindex_rows_index(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.reindex(
        index=pd.Index([5, 1, 3, 99, 1], name="newname")
    ).to_pandas()

    pd_result = scalars_pandas_df_index.reindex(
        index=pd.Index([5, 1, 3, 99, 1], name="newname")
    )

    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_reindex_nonunique(scalars_df_index):
    with pytest.raises(ValueError):
        # int64_too is non-unique
        scalars_df_index.set_index("int64_too").reindex(
            index=[5, 1, 3, 99, 1], validate=True
        )


def test_df_reindex_columns(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.reindex(
        columns=["not_a_col", "int64_col", "int64_too"]
    ).to_pandas()

    pd_result = scalars_pandas_df_index.reindex(
        columns=["not_a_col", "int64_col", "int64_too"]
    )

    # Pandas uses float64 as default for newly created empty column, bf uses Float64
    pd_result.not_a_col = pd_result.not_a_col.astype(pandas.Float64Dtype())
    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_equals_identical(scalars_df_index, scalars_pandas_df_index):
    unsupported = [
        "geography_col",
    ]
    scalars_df_index = scalars_df_index.drop(columns=unsupported)
    scalars_pandas_df_index = scalars_pandas_df_index.drop(columns=unsupported)

    bf_result = scalars_df_index.equals(scalars_df_index)
    pd_result = scalars_pandas_df_index.equals(scalars_pandas_df_index)

    assert pd_result == bf_result


def test_df_equals_series(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index[["int64_col"]].equals(scalars_df_index["int64_col"])
    pd_result = scalars_pandas_df_index[["int64_col"]].equals(
        scalars_pandas_df_index["int64_col"]
    )

    assert pd_result == bf_result


def test_df_equals_different_dtype(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_col", "int64_too"]
    scalars_df_index = scalars_df_index[columns]
    scalars_pandas_df_index = scalars_pandas_df_index[columns]

    bf_modified = scalars_df_index.copy()
    bf_modified = bf_modified.astype("Float64")

    pd_modified = scalars_pandas_df_index.copy()
    pd_modified = pd_modified.astype("Float64")

    bf_result = scalars_df_index.equals(bf_modified)
    pd_result = scalars_pandas_df_index.equals(pd_modified)

    assert pd_result == bf_result


def test_df_equals_different_values(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_col", "int64_too"]
    scalars_df_index = scalars_df_index[columns]
    scalars_pandas_df_index = scalars_pandas_df_index[columns]

    bf_modified = scalars_df_index.copy()
    bf_modified["int64_col"] = bf_modified.int64_col + 1

    pd_modified = scalars_pandas_df_index.copy()
    pd_modified["int64_col"] = pd_modified.int64_col + 1

    bf_result = scalars_df_index.equals(bf_modified)
    pd_result = scalars_pandas_df_index.equals(pd_modified)

    assert pd_result == bf_result


def test_df_equals_extra_column(scalars_df_index, scalars_pandas_df_index):
    columns = ["int64_col", "int64_too"]
    more_columns = ["int64_col", "int64_too", "float64_col"]

    bf_result = scalars_df_index[columns].equals(scalars_df_index[more_columns])
    pd_result = scalars_pandas_df_index[columns].equals(
        scalars_pandas_df_index[more_columns]
    )

    assert pd_result == bf_result


def test_df_reindex_like(scalars_df_index, scalars_pandas_df_index):
    reindex_target_bf = scalars_df_index.reindex(
        columns=["not_a_col", "int64_col", "int64_too"], index=[5, 1, 3, 99, 1]
    )
    bf_result = scalars_df_index.reindex_like(reindex_target_bf).to_pandas()

    reindex_target_pd = scalars_pandas_df_index.reindex(
        columns=["not_a_col", "int64_col", "int64_too"], index=[5, 1, 3, 99, 1]
    )
    pd_result = scalars_pandas_df_index.reindex_like(reindex_target_pd)

    # Pandas uses float64 as default for newly created empty column, bf uses Float64
    # Pandas uses int64 instead of Int64 (nullable) dtype.
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())
    # Pandas uses float64 as default for newly created empty column, bf uses Float64
    pd_result.not_a_col = pd_result.not_a_col.astype(pandas.Float64Dtype())
    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_values(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.values

    pd_result = scalars_pandas_df_index.values
    # Numpy isn't equipped to compare non-numeric objects, so convert back to dataframe
    pd.testing.assert_frame_equal(
        pd.DataFrame(bf_result), pd.DataFrame(pd_result), check_dtype=False
    )


def test_df_to_numpy(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.to_numpy()

    pd_result = scalars_pandas_df_index.to_numpy()
    # Numpy isn't equipped to compare non-numeric objects, so convert back to dataframe
    pd.testing.assert_frame_equal(
        pd.DataFrame(bf_result), pd.DataFrame(pd_result), check_dtype=False
    )


def test_df___array__(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.__array__()

    pd_result = scalars_pandas_df_index.__array__()
    # Numpy isn't equipped to compare non-numeric objects, so convert back to dataframe
    pd.testing.assert_frame_equal(
        pd.DataFrame(bf_result), pd.DataFrame(pd_result), check_dtype=False
    )


def test_getattr_attribute_error_when_pandas_has(scalars_df_index):
    # asof is implemented in pandas but not in bigframes
    with pytest.raises(AttributeError):
        scalars_df_index.asof()


def test_getattr_attribute_error(scalars_df_index):
    with pytest.raises(AttributeError):
        scalars_df_index.not_a_method()


def test_loc_list_string_index(scalars_df_index, scalars_pandas_df_index):
    index_list = scalars_pandas_df_index.string_col.iloc[[0, 1, 1, 5]].values

    scalars_df_index = scalars_df_index.set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("string_col")

    bf_result = scalars_df_index.loc[index_list].to_pandas()
    pd_result = scalars_pandas_df_index.loc[index_list]

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_loc_list_integer_index(scalars_df_index, scalars_pandas_df_index):
    index_list = [3, 2, 1, 3, 2, 1]

    bf_result = scalars_df_index.loc[index_list]
    pd_result = scalars_pandas_df_index.loc[index_list]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_list_multiindex(scalars_df_index, scalars_pandas_df_index):
    scalars_df_multiindex = scalars_df_index.set_index(["string_col", "int64_col"])
    scalars_pandas_df_multiindex = scalars_pandas_df_index.set_index(
        ["string_col", "int64_col"]
    )
    index_list = [("Hello, World!", -234892), ("Hello, World!", 123456789)]

    bf_result = scalars_df_multiindex.loc[index_list]
    pd_result = scalars_pandas_df_multiindex.loc[index_list]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_iloc_list(scalars_df_index, scalars_pandas_df_index):
    index_list = [0, 0, 0, 5, 4, 7]

    bf_result = scalars_df_index.iloc[index_list]
    pd_result = scalars_pandas_df_index.iloc[index_list]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_iloc_list_multiindex(scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_df = scalars_df.copy()
    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_df = scalars_df.set_index(["bytes_col", "numeric_col"])
    scalars_pandas_df = scalars_pandas_df.set_index(["bytes_col", "numeric_col"])

    index_list = [0, 0, 0, 5, 4, 7]

    bf_result = scalars_df.iloc[index_list]
    pd_result = scalars_pandas_df.iloc[index_list]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_iloc_empty_list(scalars_df_index, scalars_pandas_df_index):
    index_list = []

    bf_result = scalars_df_index.iloc[index_list]
    pd_result = scalars_pandas_df_index.iloc[index_list]

    bf_result = bf_result.to_pandas()
    assert bf_result.shape == pd_result.shape  # types are known to be different


def test_rename_axis(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.rename_axis("newindexname")
    pd_result = scalars_pandas_df_index.rename_axis("newindexname")

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_rename_axis_nonstring(scalars_df_index, scalars_pandas_df_index):
    bf_result = scalars_df_index.rename_axis((4,))
    pd_result = scalars_pandas_df_index.rename_axis((4,))

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_series_string_index(scalars_df_index, scalars_pandas_df_index):
    pd_string_series = scalars_pandas_df_index.string_col.iloc[[0, 5, 1, 1, 5]]
    bf_string_series = scalars_df_index.string_col.iloc[[0, 5, 1, 1, 5]]

    scalars_df_index = scalars_df_index.set_index("string_col")
    scalars_pandas_df_index = scalars_pandas_df_index.set_index("string_col")

    bf_result = scalars_df_index.loc[bf_string_series]
    pd_result = scalars_pandas_df_index.loc[pd_string_series]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_series_multiindex(scalars_df_index, scalars_pandas_df_index):
    pd_string_series = scalars_pandas_df_index.string_col.iloc[[0, 5, 1, 1, 5]]
    bf_string_series = scalars_df_index.string_col.iloc[[0, 5, 1, 1, 5]]

    scalars_df_multiindex = scalars_df_index.set_index(["string_col", "int64_col"])
    scalars_pandas_df_multiindex = scalars_pandas_df_index.set_index(
        ["string_col", "int64_col"]
    )

    bf_result = scalars_df_multiindex.loc[bf_string_series]
    pd_result = scalars_pandas_df_multiindex.loc[pd_string_series]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_index_integer_index(scalars_df_index, scalars_pandas_df_index):
    pd_index = scalars_pandas_df_index.iloc[[0, 5, 1, 1, 5]].index
    bf_index = scalars_df_index.iloc[[0, 5, 1, 1, 5]].index

    bf_result = scalars_df_index.loc[bf_index]
    pd_result = scalars_pandas_df_index.loc[pd_index]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


def test_loc_bf_index_integer_index_renamed_col(
    scalars_df_index, scalars_pandas_df_index
):
    scalars_df_index = scalars_df_index.rename(columns={"int64_col": "rename"})
    scalars_pandas_df_index = scalars_pandas_df_index.rename(
        columns={"int64_col": "rename"}
    )

    pd_index = scalars_pandas_df_index.iloc[[0, 5, 1, 1, 5]].index
    bf_index = scalars_df_index.iloc[[0, 5, 1, 1, 5]].index

    bf_result = scalars_df_index.loc[bf_index]
    pd_result = scalars_pandas_df_index.loc[pd_index]

    pd.testing.assert_frame_equal(
        bf_result.to_pandas(),
        pd_result,
    )


@pytest.mark.parametrize(
    ("subset"),
    [
        None,
        "bool_col",
        ["bool_col", "int64_too"],
    ],
)
@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        (False,),
    ],
)
def test_df_drop_duplicates(scalars_df_index, scalars_pandas_df_index, keep, subset):
    columns = ["bool_col", "int64_too", "int64_col"]
    bf_series = scalars_df_index[columns].drop_duplicates(subset, keep=keep).to_pandas()
    pd_series = scalars_pandas_df_index[columns].drop_duplicates(subset, keep=keep)
    pd.testing.assert_frame_equal(
        pd_series,
        bf_series,
    )


@pytest.mark.parametrize(
    ("subset"),
    [
        None,
        ["bool_col"],
    ],
)
@pytest.mark.parametrize(
    ("keep",),
    [
        ("first",),
        ("last",),
        (False,),
    ],
)
def test_df_duplicated(scalars_df_index, scalars_pandas_df_index, keep, subset):
    columns = ["bool_col", "int64_too", "int64_col"]
    bf_series = scalars_df_index[columns].duplicated(subset, keep=keep).to_pandas()
    pd_series = scalars_pandas_df_index[columns].duplicated(subset, keep=keep)
    pd.testing.assert_series_equal(pd_series, bf_series, check_dtype=False)


def test_df_to_dict(scalars_df_index, scalars_pandas_df_index):
    unsupported = ["numeric_col"]  # formatted differently
    bf_result = scalars_df_index.drop(columns=unsupported).to_dict()
    pd_result = scalars_pandas_df_index.drop(columns=unsupported).to_dict()

    assert bf_result == pd_result


def test_df_to_excel(scalars_df_index, scalars_pandas_df_index):
    unsupported = ["timestamp_col"]
    with tempfile.TemporaryFile() as bf_result_file, tempfile.TemporaryFile() as pd_result_file:
        scalars_df_index.drop(columns=unsupported).to_excel(bf_result_file)
        scalars_pandas_df_index.drop(columns=unsupported).to_excel(pd_result_file)
        bf_result = bf_result_file.read()
        pd_result = bf_result_file.read()

    assert bf_result == pd_result


def test_df_to_latex(scalars_df_index, scalars_pandas_df_index):
    unsupported = ["numeric_col"]  # formatted differently
    bf_result = scalars_df_index.drop(columns=unsupported).to_latex()
    pd_result = scalars_pandas_df_index.drop(columns=unsupported).to_latex()

    assert bf_result == pd_result


def test_df_to_records(scalars_df_index, scalars_pandas_df_index):
    unsupported = ["numeric_col"]
    bf_result = scalars_df_index.drop(columns=unsupported).to_records()
    pd_result = scalars_pandas_df_index.drop(columns=unsupported).to_records()

    for bfi, pdi in zip(bf_result, pd_result):
        for bfj, pdj in zip(bfi, pdi):
            assert pd.isna(bfj) and pd.isna(pdj) or bfj == pdj


def test_df_to_string(scalars_df_index, scalars_pandas_df_index):
    unsupported = ["numeric_col"]  # formatted differently

    bf_result = scalars_df_index.drop(columns=unsupported).to_string()
    pd_result = scalars_pandas_df_index.drop(columns=unsupported).to_string()

    assert bf_result == pd_result


def test_df_to_markdown(scalars_df_index, scalars_pandas_df_index):
    # Nulls have bug from tabulate https://github.com/astanin/python-tabulate/issues/231
    bf_result = scalars_df_index.dropna().to_markdown()
    pd_result = scalars_pandas_df_index.dropna().to_markdown()

    assert bf_result == pd_result


def test_df_to_pickle(scalars_df_index, scalars_pandas_df_index):
    with tempfile.TemporaryFile() as bf_result_file, tempfile.TemporaryFile() as pd_result_file:
        scalars_df_index.to_pickle(bf_result_file)
        scalars_pandas_df_index.to_pickle(pd_result_file)
        bf_result = bf_result_file.read()
        pd_result = bf_result_file.read()

    assert bf_result == pd_result


def test_df_to_orc(scalars_df_index, scalars_pandas_df_index):
    unsupported = [
        "numeric_col",
        "bytes_col",
        "date_col",
        "datetime_col",
        "time_col",
        "timestamp_col",
        "geography_col",
    ]

    bf_result_file = tempfile.TemporaryFile()
    pd_result_file = tempfile.TemporaryFile()
    scalars_df_index.drop(columns=unsupported).to_orc(bf_result_file)
    scalars_pandas_df_index.drop(columns=unsupported).reset_index().to_orc(
        pd_result_file
    )
    bf_result = bf_result_file.read()
    pd_result = bf_result_file.read()

    assert bf_result == pd_result


@pytest.mark.parametrize(
    ("subset", "normalize", "ascending", "dropna"),
    [
        (None, False, False, False),
        (None, True, True, True),
        ("bool_col", True, False, True),
    ],
)
def test_df_value_counts(scalars_dfs, subset, normalize, ascending, dropna):
    scalars_df, scalars_pandas_df = scalars_dfs

    bf_result = (
        scalars_df[["string_col", "bool_col"]]
        .value_counts(subset, normalize=normalize, ascending=ascending, dropna=dropna)
        .to_pandas()
    )
    pd_result = scalars_pandas_df[["string_col", "bool_col"]].value_counts(
        subset, normalize=normalize, ascending=ascending, dropna=dropna
    )

    # Older pandas version may not have these values, bigframes tries to emulate 2.0+
    pd_result.name = "count"
    pd_result.index.names = bf_result.index.names

    pd.testing.assert_series_equal(
        bf_result, pd_result, check_dtype=False, check_index_type=False
    )


@pytest.mark.parametrize(
    ("na_option", "method", "ascending", "numeric_only"),
    [
        ("keep", "average", True, True),
        ("top", "min", False, False),
        ("bottom", "max", False, False),
        ("top", "first", False, False),
        ("bottom", "dense", False, False),
    ],
)
@pytest.mark.skipif(
    True, reason="Blocked by possible pandas rank() regression (b/283278923)"
)
def test_df_rank_with_nulls(
    scalars_df_index,
    scalars_pandas_df_index,
    na_option,
    method,
    ascending,
    numeric_only,
):
    unsupported_columns = ["geography_col"]
    bf_result = (
        scalars_df_index.drop(columns=unsupported_columns)
        .rank(
            na_option=na_option,
            method=method,
            ascending=ascending,
            numeric_only=numeric_only,
        )
        .to_pandas()
    )
    pd_result = (
        scalars_pandas_df_index.drop(columns=unsupported_columns)
        .rank(
            na_option=na_option,
            method=method,
            ascending=ascending,
            numeric_only=numeric_only,
        )
        .astype(pd.Float64Dtype())
    )

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_bool_interpretation_error(scalars_df_index):
    with pytest.raises(ValueError):
        True if scalars_df_index else False


def test_query_job_setters(scalars_df_default_index: dataframe.DataFrame):
    job_ids = set()
    repr(scalars_df_default_index)
    assert scalars_df_default_index.query_job is not None
    job_ids.add(scalars_df_default_index.query_job.job_id)
    scalars_df_default_index.to_pandas()
    job_ids.add(scalars_df_default_index.query_job.job_id)

    assert len(job_ids) == 2


def test_df_cached(scalars_df_index):
    df = scalars_df_index.set_index(["int64_too", "int64_col"]).sort_values(
        "string_col"
    )
    df = df[df["rowindex_2"] % 2 == 0]

    df_cached_copy = df._cached()
    pandas.testing.assert_frame_equal(df.to_pandas(), df_cached_copy.to_pandas())


def test_df_dot_inline(session):
    df1 = pd.DataFrame([[1, 2, 3], [2, 5, 7]])
    df2 = pd.DataFrame([[2, 4, 8], [1, 5, 10], [3, 6, 9]])

    bf1 = session.read_pandas(df1)
    bf2 = session.read_pandas(df2)
    bf_result = bf1.dot(bf2).to_pandas()
    pd_result = df1.dot(df2)

    # Patch pandas dtypes for testing parity
    # Pandas uses int64 instead of Int64 (nullable) dtype.
    for name in pd_result.columns:
        pd_result[name] = pd_result[name].astype(pd.Int64Dtype())
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_dot(
    matrix_2by3_df, matrix_2by3_pandas_df, matrix_3by4_df, matrix_3by4_pandas_df
):
    bf_result = matrix_2by3_df.dot(matrix_3by4_df).to_pandas()
    pd_result = matrix_2by3_pandas_df.dot(matrix_3by4_pandas_df)

    # Patch pandas dtypes for testing parity
    # Pandas result is object instead of Int64 (nullable) dtype.
    for name in pd_result.columns:
        pd_result[name] = pd_result[name].astype(pd.Int64Dtype())

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_dot_operator(
    matrix_2by3_df, matrix_2by3_pandas_df, matrix_3by4_df, matrix_3by4_pandas_df
):
    bf_result = (matrix_2by3_df @ matrix_3by4_df).to_pandas()
    pd_result = matrix_2by3_pandas_df @ matrix_3by4_pandas_df

    # Patch pandas dtypes for testing parity
    # Pandas result is object instead of Int64 (nullable) dtype.
    for name in pd_result.columns:
        pd_result[name] = pd_result[name].astype(pd.Int64Dtype())

    pd.testing.assert_frame_equal(
        bf_result,
        pd_result,
    )


def test_df_dot_series_inline():
    left = [[1, 2, 3], [2, 5, 7]]
    right = [2, 1, 3]

    bf1 = dataframe.DataFrame(left)
    bf2 = series.Series(right)
    bf_result = bf1.dot(bf2).to_pandas()

    df1 = pd.DataFrame(left)
    df2 = pd.Series(right)
    pd_result = df1.dot(df2)

    # Patch pandas dtypes for testing parity
    # Pandas result is int64 instead of Int64 (nullable) dtype.
    pd_result = pd_result.astype(pd.Int64Dtype())
    pd_result.index = pd_result.index.astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_df_dot_series(
    matrix_2by3_df, matrix_2by3_pandas_df, matrix_3by4_df, matrix_3by4_pandas_df
):
    bf_result = matrix_2by3_df.dot(matrix_3by4_df["x"]).to_pandas()
    pd_result = matrix_2by3_pandas_df.dot(matrix_3by4_pandas_df["x"])

    # Patch pandas dtypes for testing parity
    # Pandas result is object instead of Int64 (nullable) dtype.
    pd_result = pd_result.astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_df_dot_operator_series(
    matrix_2by3_df, matrix_2by3_pandas_df, matrix_3by4_df, matrix_3by4_pandas_df
):
    bf_result = (matrix_2by3_df @ matrix_3by4_df["x"]).to_pandas()
    pd_result = matrix_2by3_pandas_df @ matrix_3by4_pandas_df["x"]

    # Patch pandas dtypes for testing parity
    # Pandas result is object instead of Int64 (nullable) dtype.
    pd_result = pd_result.astype(pd.Int64Dtype())

    pd.testing.assert_series_equal(
        bf_result,
        pd_result,
    )


def test_to_pandas_downsampling_option_override(session):
    df = session.read_gbq("bigframes-dev.bigframes_tests_sys.batting")
    download_size = 1

    df = df.to_pandas(max_download_size=download_size, sampling_method="head")

    total_memory_bytes = df.memory_usage(deep=True).sum()
    total_memory_mb = total_memory_bytes / (1024 * 1024)
    assert total_memory_mb == pytest.approx(download_size, rel=0.3)
