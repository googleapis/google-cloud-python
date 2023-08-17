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

from typing import Tuple

import google.api_core.exceptions
import pandas as pd
import pytest

from tests.system.utils import (
    assert_pandas_df_equal_ignore_ordering,
    convert_pandas_dtypes,
)

try:
    import pandas_gbq  # type: ignore
except ImportError:
    pandas_gbq = None

import typing

import bigframes
import bigframes.dataframe


def test_to_pandas_w_correct_dtypes(scalars_df_default_index):
    """Verify to_pandas() APIs returns the expected dtypes."""
    actual = scalars_df_default_index.to_pandas().dtypes
    expected = scalars_df_default_index.dtypes

    pd.testing.assert_series_equal(actual, expected)


def test_to_pandas_array_struct_correct_result(session):
    """In future, we should support arrays and structs with arrow types.
    For now we fall back to the current connector behavior of converting
    to Python objects"""
    df = session.read_gbq(
        """SELECT
        [1, 3, 2] AS array_column,
        STRUCT(
            "a" AS string_field,
            1.2 AS float_field) AS struct_column"""
    )

    result = df.to_pandas()
    expected = pd.DataFrame(
        {
            "array_column": [[1, 3, 2]],
            "struct_column": [{"string_field": "a", "float_field": 1.2}],
        }
    )
    expected.index = expected.index.astype("Int64")
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
def test_to_csv_index(
    scalars_dfs: Tuple[bigframes.dataframe.DataFrame, pd.DataFrame],
    gcs_folder: str,
    index: bool,
):
    if pd.__version__.startswith("1."):
        pytest.skip("date_format parameter not supported in pandas 1.x.")
    """Test the `to_csv` API with the `index` parameter."""
    scalars_df, scalars_pandas_df = scalars_dfs
    index_col = None
    if scalars_df.index.name is not None:
        path = gcs_folder + f"test_index_df_to_csv_index_{index}*.csv"
        if index:
            index_col = typing.cast(str, scalars_df.index.name)
    else:
        path = gcs_folder + f"test_default_index_df_to_csv_index_{index}*.csv"

    # TODO(swast): Support "date_format" parameter and make sure our
    # DATETIME/TIMESTAMP column export is the same format as pandas by default.
    scalars_df.to_csv(path, index=index)

    # Pandas dataframes dtypes from read_csv are not fully compatible with
    # BigQuery-backed dataframes, so manually convert the dtypes specifically
    # here.
    dtype = scalars_df.reset_index().dtypes.to_dict()
    dtype.pop("geography_col")
    dtype.pop("rowindex")
    gcs_df = pd.read_csv(
        path,
        dtype=dtype,
        date_format={"timestamp_col": "YYYY-MM-DD HH:MM:SS Z"},
        index_col=index_col,
    )
    convert_pandas_dtypes(gcs_df, bytes_col=True)
    gcs_df.index.name = scalars_df.index.name

    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_pandas_df.index = scalars_pandas_df.index.astype("int64")

    # Ordering should be maintained for tables smaller than 1 GB.
    pd.testing.assert_frame_equal(gcs_df, scalars_pandas_df)


def test_to_csv_tabs(
    scalars_dfs: Tuple[bigframes.dataframe.DataFrame, pd.DataFrame],
    gcs_folder: str,
):
    if pd.__version__.startswith("1."):
        pytest.skip("date_format parameter not supported in pandas 1.x.")
    """Test the `to_csv` API with the `sep` parameter."""
    scalars_df, scalars_pandas_df = scalars_dfs
    index_col = typing.cast(str, scalars_df.index.name)
    path = gcs_folder + "test_to_csv_tabs*.csv"

    # TODO(swast): Support "date_format" parameter and make sure our
    # DATETIME/TIMESTAMP column export is the same format as pandas by default.
    scalars_df.to_csv(path, sep="\t", index=True)

    # Pandas dataframes dtypes from read_csv are not fully compatible with
    # BigQuery-backed dataframes, so manually convert the dtypes specifically
    # here.
    dtype = scalars_df.reset_index().dtypes.to_dict()
    dtype.pop("geography_col")
    dtype.pop("rowindex")
    gcs_df = pd.read_csv(
        path,
        sep="\t",
        dtype=dtype,
        date_format={"timestamp_col": "YYYY-MM-DD HH:MM:SS Z"},
        index_col=index_col,
    )
    convert_pandas_dtypes(gcs_df, bytes_col=True)
    gcs_df.index.name = scalars_df.index.name

    scalars_pandas_df = scalars_pandas_df.copy()
    scalars_pandas_df.index = scalars_pandas_df.index.astype("int64")

    # Ordering should be maintained for tables smaller than 1 GB.
    pd.testing.assert_frame_equal(gcs_df, scalars_pandas_df)


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
@pytest.mark.skipif(pandas_gbq is None, reason="required by pd.read_gbq")
def test_to_gbq_index(scalars_dfs, dataset_id, index):
    """Test the `to_gbq` API with the `index` parameter."""
    scalars_df, scalars_pandas_df = scalars_dfs
    destination_table = f"{dataset_id}.test_index_df_to_gbq_{index}"
    df_in = scalars_df.copy()
    if index:
        index_col = "index"
        df_in.index.name = index_col
    else:
        index_col = None

    df_in.to_gbq(destination_table, if_exists="replace", index=index)
    df_out = pd.read_gbq(destination_table, index_col=index_col)

    if index:
        df_out = df_out.sort_index()
    else:
        df_out = df_out.sort_values("rowindex_2").reset_index(drop=True)

    convert_pandas_dtypes(df_out, bytes_col=False)
    expected = scalars_pandas_df.copy()
    expected.index.name = index_col
    pd.testing.assert_frame_equal(df_out, expected, check_index_type=False)


@pytest.mark.parametrize(
    ("if_exists", "expected_index"),
    [
        pytest.param("replace", 1),
        pytest.param("append", 2),
        pytest.param(
            "fail",
            0,
            marks=pytest.mark.xfail(
                raises=google.api_core.exceptions.Conflict,
            ),
        ),
        pytest.param(
            "unknown",
            0,
            marks=pytest.mark.xfail(
                raises=ValueError,
            ),
        ),
    ],
)
@pytest.mark.skipif(pandas_gbq is None, reason="required by pd.read_gbq")
def test_to_gbq_if_exists(
    scalars_df_default_index,
    scalars_pandas_df_default_index,
    dataset_id,
    if_exists,
    expected_index,
):
    """Test the `to_gbq` API with the `if_exists` parameter."""
    destination_table = f"{dataset_id}.test_to_gbq_if_exists_{if_exists}"

    scalars_df_default_index.to_gbq(destination_table)
    scalars_df_default_index.to_gbq(destination_table, if_exists=if_exists)

    gcs_df = pd.read_gbq(destination_table)
    assert len(gcs_df.index) == expected_index * len(
        scalars_pandas_df_default_index.index
    )
    pd.testing.assert_index_equal(
        gcs_df.columns, scalars_pandas_df_default_index.columns
    )


def test_to_gbq_w_invalid_destination_table(scalars_df_index):
    with pytest.raises(ValueError):
        scalars_df_index.to_gbq("table_id")


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
def test_to_json_index_invalid_orient(
    scalars_dfs: Tuple[bigframes.dataframe.DataFrame, pd.DataFrame],
    gcs_folder: str,
    index: bool,
):
    scalars_df, scalars_pandas_df = scalars_dfs
    if scalars_df.index.name is not None:
        path = gcs_folder + f"test_index_df_to_json_index_{index}*.jsonl"
    else:
        path = gcs_folder + f"test_default_index_df_to_json_index_{index}*.jsonl"
    with pytest.raises(ValueError):
        scalars_df.to_json(path, index=index, lines=True)


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
def test_to_json_index_invalid_lines(
    scalars_dfs: Tuple[bigframes.dataframe.DataFrame, pd.DataFrame],
    gcs_folder: str,
    index: bool,
):
    scalars_df, scalars_pandas_df = scalars_dfs
    if scalars_df.index.name is not None:
        path = gcs_folder + f"test_index_df_to_json_index_{index}.jsonl"
    else:
        path = gcs_folder + f"test_default_index_df_to_json_index_{index}.jsonl"
    with pytest.raises(NotImplementedError):
        scalars_df.to_json(path, index=index)


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
def test_to_json_index_records_orient(
    scalars_dfs: Tuple[bigframes.dataframe.DataFrame, pd.DataFrame],
    gcs_folder: str,
    index: bool,
):
    """Test the `to_json` API with the `index` parameter."""
    scalars_df, scalars_pandas_df = scalars_dfs
    if scalars_df.index.name is not None:
        path = gcs_folder + f"test_index_df_to_json_index_{index}*.jsonl"
    else:
        path = gcs_folder + f"test_default_index_df_to_json_index_{index}*.jsonl"

    """ Test the `to_json` API with `orient` is `records` and `lines` is True"""
    scalars_df.to_json(path, index=index, orient="records", lines=True)

    gcs_df = pd.read_json(path, lines=True, convert_dates=["datetime_col"])
    convert_pandas_dtypes(gcs_df, bytes_col=True)
    if index and scalars_df.index.name is not None:
        gcs_df = gcs_df.set_index(scalars_df.index.name)

    assert len(gcs_df.index) == len(scalars_pandas_df.index)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    gcs_df.index.name = scalars_df.index.name
    gcs_df.index = gcs_df.index.astype("Int64")
    scalars_pandas_df.index = scalars_pandas_df.index.astype("Int64")

    # Ordering should be maintained for tables smaller than 1 GB.
    pd.testing.assert_frame_equal(gcs_df, scalars_pandas_df)


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
def test_to_parquet_index(scalars_dfs, gcs_folder, index):
    """Test the `to_parquet` API with the `index` parameter."""
    scalars_df, scalars_pandas_df = scalars_dfs
    scalars_pandas_df = scalars_pandas_df.copy()

    if scalars_df.index.name is not None:
        path = gcs_folder + f"test_index_df_to_parquet_{index}*.parquet"
    else:
        path = gcs_folder + f"test_default_index_df_to_parquet_{index}*.parquet"

    # TODO(b/268693993): Type GEOGRAPHY is not currently supported for parquet.
    scalars_df = scalars_df.drop(columns="geography_col")
    scalars_pandas_df = scalars_pandas_df.drop(columns="geography_col")

    # TODO(swast): Do a bit more processing on the input DataFrame to ensure
    # the exported results are from the generated query, not just the source
    # table.
    scalars_df.to_parquet(path, index=index)

    gcs_df = pd.read_parquet(path.replace("*", "000000000000"))
    convert_pandas_dtypes(gcs_df, bytes_col=False)
    if index and scalars_df.index.name is not None:
        gcs_df = gcs_df.set_index(scalars_df.index.name)

    assert len(gcs_df.index) == len(scalars_pandas_df.index)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    gcs_df.index.name = scalars_df.index.name
    gcs_df.index = gcs_df.index.astype("Int64")
    scalars_pandas_df.index = scalars_pandas_df.index.astype("Int64")

    # Ordering should be maintained for tables smaller than 1 GB.
    pd.testing.assert_frame_equal(gcs_df, scalars_pandas_df)


def test_to_sql_query_named_index_included(
    session, scalars_df_index, scalars_pandas_df_index
):
    sql, index_columns = scalars_df_index._to_sql_query(always_include_index=True)
    assert len(index_columns) == 1
    index_column, is_named = index_columns[0]
    assert index_column == "rowindex"
    assert is_named

    roundtrip = session.read_gbq(sql, index_col=[index_column])
    assert_pandas_df_equal_ignore_ordering(
        roundtrip.to_pandas(), scalars_pandas_df_index
    )


def test_to_sql_query_unnamed_index_excluded(
    session, scalars_df_default_index, scalars_pandas_df_default_index
):
    # The .sql property should return SQL without the unnamed indexes
    sql, index_columns = scalars_df_default_index._to_sql_query(
        always_include_index=False
    )
    assert len(index_columns) == 0

    roundtrip = session.read_gbq(sql)
    assert_pandas_df_equal_ignore_ordering(
        roundtrip.to_pandas(), scalars_pandas_df_default_index
    )


def test_to_sql_query_unnamed_index_always_include(
    session,
    scalars_df_default_index: bigframes.dataframe.DataFrame,
    scalars_pandas_df_default_index,
):
    sql, index_columns = scalars_df_default_index._to_sql_query(
        always_include_index=True
    )
    assert len(index_columns) == 1
    index_column, is_named = index_columns[0]
    assert index_column == "bigframes_index_0"
    assert not is_named

    roundtrip = session.read_gbq(sql, index_col=[index_column])
    roundtrip.index.name = None
    assert_pandas_df_equal_ignore_ordering(
        roundtrip.to_pandas(), scalars_pandas_df_default_index
    )
