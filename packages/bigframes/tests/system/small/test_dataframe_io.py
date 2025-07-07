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
import numpy
import numpy.testing
import pandas as pd
import pandas.testing
import pyarrow as pa
import pytest

import bigframes.dtypes as dtypes
from bigframes.testing import utils

try:
    import pandas_gbq  # type: ignore
except ImportError:  # pragma: NO COVER
    # TODO(b/332758806): Run system tests without "extras"
    pandas_gbq = None

import typing

from google.cloud import bigquery

import bigframes
import bigframes.dataframe
import bigframes.enums
import bigframes.features
import bigframes.pandas as bpd


def test_sql_executes(scalars_df_default_index, bigquery_client):
    """Test that DataFrame.sql returns executable SQL.

    DF.sql is used in public documentation such as
    https://cloud.google.com/blog/products/data-analytics/using-bigquery-dataframes-with-carto-geospatial-tools
    as a way to pass a DataFrame on to carto without executing the SQL
    immediately.

    Make sure that this SQL can be run outside of BigQuery DataFrames (assuming
    similar credentials / access to the referenced tables).
    """
    # Do some operations to make for more complex SQL.
    df = (
        scalars_df_default_index.drop(columns=["geography_col", "duration_col"])
        .groupby("string_col")
        .max()
    )
    df.index.name = None  # Don't include unnamed indexes.
    query = df.sql

    bf_result = df.to_pandas().sort_values("rowindex").reset_index(drop=True)
    bq_result = (
        bigquery_client.query_and_wait(query)
        .to_dataframe()
        .sort_values("rowindex")
        .reset_index(drop=True)
    )
    pandas.testing.assert_frame_equal(bf_result, bq_result, check_dtype=False)


def test_sql_executes_and_includes_named_index(
    scalars_df_default_index, bigquery_client
):
    """Test that DataFrame.sql returns executable SQL.

    DF.sql is used in public documentation such as
    https://cloud.google.com/blog/products/data-analytics/using-bigquery-dataframes-with-carto-geospatial-tools
    as a way to pass a DataFrame on to carto without executing the SQL
    immediately.

    Make sure that this SQL can be run outside of BigQuery DataFrames (assuming
    similar credentials / access to the referenced tables).
    """
    # Do some operations to make for more complex SQL.
    df = (
        scalars_df_default_index.drop(columns=["geography_col", "duration_col"])
        .groupby("string_col")
        .max()
    )
    query = df.sql

    bf_result = df.to_pandas().sort_values("rowindex")
    bq_result = (
        bigquery_client.query_and_wait(query)
        .to_dataframe()
        .set_index("string_col")
        .sort_values("rowindex")
    )
    pandas.testing.assert_frame_equal(
        bf_result, bq_result, check_dtype=False, check_index_type=False
    )


def test_sql_executes_and_includes_named_multiindex(
    scalars_df_default_index, bigquery_client
):
    """Test that DataFrame.sql returns executable SQL.

    DF.sql is used in public documentation such as
    https://cloud.google.com/blog/products/data-analytics/using-bigquery-dataframes-with-carto-geospatial-tools
    as a way to pass a DataFrame on to carto without executing the SQL
    immediately.

    Make sure that this SQL can be run outside of BigQuery DataFrames (assuming
    similar credentials / access to the referenced tables).
    """
    # Do some operations to make for more complex SQL.
    df = (
        scalars_df_default_index.drop(columns=["geography_col", "duration_col"])
        .groupby(["string_col", "bool_col"])
        .max()
    )
    query = df.sql

    bf_result = df.to_pandas().sort_values("rowindex")
    bq_result = (
        bigquery_client.query_and_wait(query)
        .to_dataframe()
        .set_index(["string_col", "bool_col"])
        .sort_values("rowindex")
    )
    pandas.testing.assert_frame_equal(
        bf_result, bq_result, check_dtype=False, check_index_type=False
    )


def test_to_arrow(scalars_df_default_index, scalars_pandas_df_default_index):
    """Verify to_arrow() APIs returns the expected data."""
    expected = pa.Table.from_pandas(
        scalars_pandas_df_default_index.drop(columns=["geography_col"])
    )

    with pytest.warns(
        bigframes.exceptions.PreviewWarning,
        match="to_arrow",
    ):
        actual = scalars_df_default_index.drop(columns=["geography_col"]).to_arrow()

    # Make string_col match type. Otherwise, pa.Table.from_pandas uses
    # LargeStringArray. LargeStringArray is unnecessary because our strings are
    # less than 2 GB.
    expected = expected.set_column(
        expected.column_names.index("string_col"),
        pa.field("string_col", pa.string()),
        expected["string_col"].cast(pa.string()),
    )

    # Note: the final .equals assertion covers all these checks, but these
    # finer-grained assertions are easier to debug.
    assert actual.column_names == expected.column_names
    for column in actual.column_names:
        assert actual[column].equals(expected[column])
    assert actual.equals(expected)


def test_to_arrow_multiindex(scalars_df_index, scalars_pandas_df_index):
    scalars_df_multiindex = scalars_df_index.set_index(["string_col", "int64_col"])
    scalars_pandas_df_multiindex = scalars_pandas_df_index.set_index(
        ["string_col", "int64_col"]
    )
    expected = pa.Table.from_pandas(
        scalars_pandas_df_multiindex.drop(columns=["geography_col"])
    )

    with pytest.warns(
        bigframes.exceptions.PreviewWarning,
        match="to_arrow",
    ):
        actual = scalars_df_multiindex.drop(columns=["geography_col"]).to_arrow()

    # Make string_col match type. Otherwise, pa.Table.from_pandas uses
    # LargeStringArray. LargeStringArray is unnecessary because our strings are
    # less than 2 GB.
    expected = expected.set_column(
        expected.column_names.index("string_col"),
        pa.field("string_col", pa.string()),
        expected["string_col"].cast(pa.string()),
    )

    # Note: the final .equals assertion covers all these checks, but these
    # finer-grained assertions are easier to debug.
    assert actual.column_names == expected.column_names
    for column in actual.column_names:
        assert actual[column].equals(expected[column])
    assert actual.equals(expected)


def test_to_pandas_w_correct_dtypes(scalars_df_default_index):
    """Verify to_pandas() APIs returns the expected dtypes."""
    actual = scalars_df_default_index.to_pandas().dtypes
    expected = scalars_df_default_index.dtypes

    pd.testing.assert_series_equal(actual, expected)


def test_to_pandas_array_struct_correct_result(session):
    """In future, we should support arrays with arrow types.
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
            "array_column": pd.Series(
                [[1, 3, 2]],
                dtype=(
                    pd.ArrowDtype(pa.list_(pa.int64()))
                    if bigframes.features.PANDAS_VERSIONS.is_arrow_list_dtype_usable
                    else "object"
                ),
            ),
            "struct_column": pd.Series(
                [{"string_field": "a", "float_field": 1.2}],
                dtype=pd.ArrowDtype(
                    pa.struct(
                        [
                            ("string_field", pa.string()),
                            ("float_field", pa.float64()),
                        ]
                    )
                ),
            ),
        }
    )
    expected.index = expected.index.astype("Int64")
    pd.testing.assert_series_equal(result.dtypes, expected.dtypes)
    pd.testing.assert_series_equal(result["array_column"], expected["array_column"])
    # assert_series_equal not implemented for struct columns yet. Compare
    # values as Python objects, instead.
    pd.testing.assert_series_equal(
        result["struct_column"].astype("O"), expected["struct_column"].astype("O")
    )


def test_to_pandas_override_global_option(scalars_df_index):
    # Direct call to_pandas uses global default setting (allow_large_results=True),
    # table has 'bqdf' prefix.
    with bigframes.option_context("compute.allow_large_results", True):

        scalars_df_index.to_pandas()
        table_id = scalars_df_index._query_job.destination.table_id
        assert table_id is not None

        # When allow_large_results=False, a query_job object should not be created.
        # Therefore, the table_id should remain unchanged.
        scalars_df_index.to_pandas(allow_large_results=False)
        assert scalars_df_index._query_job.destination.table_id == table_id


def test_to_pandas_downsampling_option_override(session):
    df = session.read_gbq("bigframes-dev.bigframes_tests_sys.batting")
    download_size = 1

    with pytest.warns(
        UserWarning, match="The data size .* exceeds the maximum download limit"
    ):
        # limits only apply for allow_large_result=True
        df = df.to_pandas(
            max_download_size=download_size,
            sampling_method="head",
            allow_large_results=True,
        )

    total_memory_bytes = df.memory_usage(deep=True).sum()
    total_memory_mb = total_memory_bytes / (1024 * 1024)
    assert total_memory_mb == pytest.approx(download_size, rel=0.5)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        pytest.param(
            {"sampling_method": "head"},
            r"DEPRECATED[\S\s]*sampling_method[\S\s]*DataFrame.sample",
            id="sampling_method",
        ),
        pytest.param(
            {"random_state": 10},
            r"DEPRECATED[\S\s]*random_state[\S\s]*DataFrame.sample",
            id="random_state",
        ),
        pytest.param(
            {"max_download_size": 10},
            r"DEPRECATED[\S\s]*max_download_size[\S\s]*DataFrame.to_pandas_batches",
            id="max_download_size",
        ),
    ],
)
def test_to_pandas_warns_deprecated_parameters(scalars_df_index, kwargs, message):
    with pytest.warns(FutureWarning, match=message):
        scalars_df_index.to_pandas(
            # limits only apply for allow_large_result=True
            allow_large_results=True,
            **kwargs,
        )


def test_to_pandas_dry_run(session, scalars_pandas_df_multi_index):
    bf_df = session.read_pandas(scalars_pandas_df_multi_index)

    result = bf_df.to_pandas(dry_run=True)

    assert isinstance(result, pd.Series)
    assert len(result) > 0


def test_to_arrow_override_global_option(scalars_df_index):
    # Direct call to_arrow uses global default setting (allow_large_results=True),
    with bigframes.option_context("compute.allow_large_results", True):

        scalars_df_index.to_arrow()
        table_id = scalars_df_index._query_job.destination.table_id
        assert table_id is not None

        # When allow_large_results=False, a query_job object should not be created.
        # Therefore, the table_id should remain unchanged.
        scalars_df_index.to_arrow(allow_large_results=False)
        assert scalars_df_index._query_job.destination.table_id == table_id


def test_to_pandas_batches_w_correct_dtypes(scalars_df_default_index):
    """Verify to_pandas_batches() APIs returns the expected dtypes."""
    expected = scalars_df_default_index.dtypes
    for df in scalars_df_default_index.to_pandas_batches():
        actual = df.dtypes
        pd.testing.assert_series_equal(actual, expected)


def test_to_pandas_batches_w_empty_dataframe(session):
    """Verify to_pandas_batches() APIs returns at least one DataFrame.

    See b/428918844 for additional context.
    """
    empty = bpd.DataFrame(
        {
            "idx1": [],
            "idx2": [],
            "col1": pandas.Series([], dtype="string[pyarrow]"),
            "col2": pandas.Series([], dtype="Int64"),
        },
        session=session,
    ).set_index(["idx1", "idx2"], drop=True)

    results = list(empty.to_pandas_batches())
    assert len(results) == 1
    assert list(results[0].index.names) == ["idx1", "idx2"]
    assert list(results[0].columns) == ["col1", "col2"]
    pandas.testing.assert_series_equal(results[0].dtypes, empty.dtypes)


@pytest.mark.parametrize("allow_large_results", (True, False))
def test_to_pandas_batches_w_page_size_and_max_results(session, allow_large_results):
    """Verify to_pandas_batches() APIs returns the expected page size.

    Regression test for b/407521010.
    """
    bf_df = session.read_gbq(
        "bigquery-public-data.usa_names.usa_1910_2013",
        index_col=bigframes.enums.DefaultIndexKind.NULL,
    )
    expected_column_count = len(bf_df.columns)

    batch_count = 0
    for pd_df in bf_df.to_pandas_batches(
        page_size=42, allow_large_results=allow_large_results, max_results=42 * 3
    ):
        batch_row_count, batch_column_count = pd_df.shape
        batch_count += 1
        assert batch_column_count == expected_column_count
        assert batch_row_count == 42

    assert batch_count == 3


@pytest.mark.parametrize(
    ("index",),
    [(True,), (False,)],
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
    path = gcs_folder + f"test_index_df_to_csv_index_{index}*.csv"
    if index:
        index_col = typing.cast(str, scalars_df.index.name)

    # TODO(swast): Support "date_format" parameter and make sure our
    # DATETIME/TIMESTAMP column export is the same format as pandas by default.
    scalars_df.to_csv(path, index=index)

    # Pandas dataframes dtypes from read_csv are not fully compatible with
    # BigQuery-backed dataframes, so manually convert the dtypes specifically
    # here.
    dtype = scalars_df.reset_index().dtypes.to_dict()
    dtype.pop("geography_col")
    dtype.pop("rowindex")
    # read_csv will decode into bytes inproperly, convert_pandas_dtypes will encode properly from string
    dtype.pop("bytes_col")
    gcs_df = pd.read_csv(
        utils.get_first_file_from_wildcard(path),
        dtype=dtype,
        date_format={"timestamp_col": "YYYY-MM-DD HH:MM:SS Z"},
        index_col=index_col,
    )
    utils.convert_pandas_dtypes(gcs_df, bytes_col=True)
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
    # read_csv will decode into bytes inproperly, convert_pandas_dtypes will encode properly from string
    dtype.pop("bytes_col")
    gcs_df = pd.read_csv(
        utils.get_first_file_from_wildcard(path),
        sep="\t",
        dtype=dtype,
        date_format={"timestamp_col": "YYYY-MM-DD HH:MM:SS Z"},
        index_col=index_col,
    )
    utils.convert_pandas_dtypes(gcs_df, bytes_col=True)
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
def test_to_gbq_w_index(scalars_dfs, dataset_id, index):
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

    utils.convert_pandas_dtypes(df_out, bytes_col=False)
    # pd.read_gbq interprets bytes_col as object, reconvert to pyarrow binary
    df_out["bytes_col"] = df_out["bytes_col"].astype(pd.ArrowDtype(pa.binary()))
    expected = scalars_pandas_df.copy()
    expected.index.name = index_col
    pd.testing.assert_frame_equal(df_out, expected, check_index_type=False)


def test_to_gbq_if_exists_is_fail(scalars_dfs, dataset_id):
    scalars_df, scalars_pandas_df = scalars_dfs
    destination_table = f"{dataset_id}.test_to_gbq_if_exists_is_fails"
    scalars_df.to_gbq(destination_table)

    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == len(scalars_pandas_df)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    # Test default value is "fails"
    with pytest.raises(ValueError, match="Table already exists"):
        scalars_df.to_gbq(destination_table)

    with pytest.raises(ValueError, match="Table already exists"):
        scalars_df.to_gbq(destination_table, if_exists="fail")


def test_to_gbq_if_exists_is_replace(scalars_dfs, dataset_id):
    scalars_df, scalars_pandas_df = scalars_dfs
    destination_table = f"{dataset_id}.test_to_gbq_if_exists_is_replace"
    scalars_df.to_gbq(destination_table)

    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == len(scalars_pandas_df)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    # When replacing a table with same schema
    scalars_df.to_gbq(destination_table, if_exists="replace")
    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == len(scalars_pandas_df)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    # When replacing a table with different schema
    partitial_scalars_df = scalars_df.drop(columns=["string_col"])
    partitial_scalars_df.to_gbq(destination_table, if_exists="replace")
    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == len(partitial_scalars_df)
    pd.testing.assert_index_equal(gcs_df.columns, partitial_scalars_df.columns)


def test_to_gbq_if_exists_is_append(scalars_dfs, dataset_id):
    scalars_df, scalars_pandas_df = scalars_dfs
    destination_table = f"{dataset_id}.test_to_gbq_if_exists_is_append"
    scalars_df.to_gbq(destination_table)

    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == len(scalars_pandas_df)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    # When appending to a table with same schema
    scalars_df.to_gbq(destination_table, if_exists="append")
    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == 2 * len(scalars_pandas_df)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    # When appending to a table with different schema
    partitial_scalars_df = scalars_df.drop(columns=["string_col"])
    partitial_scalars_df.to_gbq(destination_table, if_exists="append")
    gcs_df = pd.read_gbq(destination_table, index_col="rowindex")
    assert len(gcs_df) == 3 * len(partitial_scalars_df)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_df.columns)


def test_to_gbq_w_duplicate_column_names(
    scalars_df_index, scalars_pandas_df_index, dataset_id
):
    """Test the `to_gbq` API when dealing with duplicate column names."""
    destination_table = f"{dataset_id}.test_to_gbq_w_duplicate_column_names"

    # Renaming 'int64_too' to 'int64_col', which will result in 'int64_too'
    # becoming 'int64_col_1' after deduplication.
    scalars_df_index = scalars_df_index.rename(columns={"int64_too": "int64_col"})
    scalars_df_index.to_gbq(destination_table, if_exists="replace")

    bf_result = bpd.read_gbq(destination_table, index_col="rowindex").to_pandas()

    pd.testing.assert_series_equal(
        scalars_pandas_df_index["int64_col"], bf_result["int64_col"]
    )
    pd.testing.assert_series_equal(
        scalars_pandas_df_index["int64_too"],
        bf_result["int64_col_1"],
        check_names=False,
    )


def test_to_gbq_w_protected_column_names(
    scalars_df_index, scalars_pandas_df_index, dataset_id
):
    """
    Column names can't use any of the following prefixes:

    * _TABLE_
    * _FILE_
    * _PARTITION
    * _ROW_TIMESTAMP
    * __ROOT__
    * _COLIDENTIFIER

    See: https://cloud.google.com/bigquery/docs/schemas#column_names
    """
    destination_table = f"{dataset_id}.test_to_gbq_w_protected_column_names"

    scalars_df_index = scalars_df_index.rename(
        columns={
            "bool_col": "_Table_Suffix",
            "bytes_col": "_file_path",
            "date_col": "_PARTITIONDATE",
            "datetime_col": "_ROW_TIMESTAMP",
            "int64_col": "__ROOT__",
            "int64_too": "_COLIDENTIFIER",
            "numeric_col": "COLIDENTIFIER",  # Create a collision at serialization time.
        }
    )[
        [
            "_Table_Suffix",
            "_file_path",
            "_PARTITIONDATE",
            "_ROW_TIMESTAMP",
            "__ROOT__",
            "_COLIDENTIFIER",
            "COLIDENTIFIER",
        ]
    ]
    scalars_df_index.to_gbq(destination_table, if_exists="replace")

    bf_result = bpd.read_gbq(destination_table, index_col="rowindex").to_pandas()

    # Leading _ characters are removed to make these columns valid in BigQuery.
    expected = scalars_pandas_df_index.rename(
        columns={
            "bool_col": "Table_Suffix",
            "bytes_col": "file_path",
            "date_col": "PARTITIONDATE",
            "datetime_col": "ROW_TIMESTAMP",
            "int64_col": "ROOT__",
            "int64_too": "COLIDENTIFIER",
            "numeric_col": "COLIDENTIFIER_1",
        }
    )[
        [
            "Table_Suffix",
            "file_path",
            "PARTITIONDATE",
            "ROW_TIMESTAMP",
            "ROOT__",
            "COLIDENTIFIER",
            "COLIDENTIFIER_1",
        ]
    ]

    pd.testing.assert_frame_equal(bf_result, expected)


def test_to_gbq_w_flexible_column_names(
    scalars_df_index, dataset_id: str, bigquery_client
):
    """Test the `to_gbq` API when dealing with flexible column names.

    This test is for BigQuery-backed storage nodes.

    See: https://cloud.google.com/bigquery/docs/schemas#flexible-column-names
    """
    destination_table = f"{dataset_id}.test_to_gbq_w_flexible_column_names"
    renamed_columns = {
        # First column in Japanese (tests unicode).
        "bool_col": "最初のカラム",
        "bytes_col": "col with space",
        # Dots aren't allowed in BigQuery column names, so these should be translated
        "date_col": "col.with.dots",
        "datetime_col": "col-with-hyphens",
        "geography_col": "1start_with_number",
        "int64_col": "col_with_underscore",
        # Just numbers.
        "int64_too": "123",
    }
    bf_df = scalars_df_index[renamed_columns.keys()].rename(columns=renamed_columns)
    assert list(bf_df.columns) == list(renamed_columns.values())
    bf_df.to_gbq(destination_table, index=False)

    table = bigquery_client.get_table(destination_table)
    columns = [field.name for field in table.schema]
    assert columns == [
        "最初のカラム",
        "col with space",
        # Dots aren't allowed in BigQuery column names, so these should be translated
        "col_with_dots",
        "col-with-hyphens",
        "1start_with_number",
        "col_with_underscore",
        "123",
    ]


def test_to_gbq_w_flexible_column_names_local_node(
    session, dataset_id: str, bigquery_client
):
    """Test the `to_gbq` API when dealing with flexible column names.

    This test is for local nodes, e.g. read_pandas(), since those may go through
    a different code path compared to data that starts in BigQuery.

    See: https://cloud.google.com/bigquery/docs/schemas#flexible-column-names
    """
    destination_table = f"{dataset_id}.test_to_gbq_w_flexible_column_names_local_node"

    data = {
        # First column in Japanese (tests unicode).
        "最初のカラム": [1, 2, 3],
        "col with space": [4, 5, 6],
        # Dots aren't allowed in BigQuery column names, so these should be translated
        "col.with.dots": [7, 8, 9],
        "col-with-hyphens": [10, 11, 12],
        "1start_with_number": [13, 14, 15],
        "col_with_underscore": [16, 17, 18],
        "123": [19, 20, 21],
    }
    pd_df = pd.DataFrame(data)
    assert list(pd_df.columns) == list(data.keys())
    bf_df = session.read_pandas(pd_df)
    assert list(bf_df.columns) == list(data.keys())
    bf_df.to_gbq(destination_table, index=False)

    table = bigquery_client.get_table(destination_table)
    columns = [field.name for field in table.schema]
    assert columns == [
        "最初のカラム",
        "col with space",
        # Dots aren't allowed in BigQuery column names, so these should be translated
        "col_with_dots",
        "col-with-hyphens",
        "1start_with_number",
        "col_with_underscore",
        "123",
    ]


def test_to_gbq_w_None_column_names(
    scalars_df_index, scalars_pandas_df_index, dataset_id
):
    """Test the `to_gbq` API with None as a column name."""
    destination_table = f"{dataset_id}.test_to_gbq_w_none_column_names"

    scalars_df_index = scalars_df_index.rename(columns={"int64_too": None})
    scalars_df_index.to_gbq(destination_table, if_exists="replace")

    bf_result = bpd.read_gbq(destination_table, index_col="rowindex").to_pandas()

    pd.testing.assert_series_equal(
        scalars_pandas_df_index["int64_col"], bf_result["int64_col"]
    )
    pd.testing.assert_series_equal(
        scalars_pandas_df_index["int64_too"],
        bf_result["bigframes_unnamed_column"],
        check_names=False,
    )


@pytest.mark.parametrize(
    "clustering_columns",
    [
        pytest.param(["int64_col", "geography_col"]),
        pytest.param(
            ["float64_col"],
            marks=pytest.mark.xfail(raises=google.api_core.exceptions.BadRequest),
        ),
        pytest.param(
            ["int64_col", "int64_col"],
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ],
)
def test_to_gbq_w_clustering(
    scalars_df_default_index,
    dataset_id,
    bigquery_client,
    clustering_columns,
):
    """Test the `to_gbq` API for creating clustered tables."""
    destination_table = (
        f"{dataset_id}.test_to_gbq_clustering_{'_'.join(clustering_columns)}"
    )

    scalars_df_default_index.to_gbq(
        destination_table, clustering_columns=clustering_columns
    )
    table = bigquery_client.get_table(destination_table)

    assert list(table.clustering_fields) == clustering_columns
    assert table.expires is None


def test_to_gbq_w_clustering_no_destination(
    scalars_df_default_index,
    bigquery_client,
):
    """Test the `to_gbq` API for creating clustered tables without destination."""
    clustering_columns = ["int64_col", "geography_col"]
    destination_table = scalars_df_default_index.to_gbq(
        clustering_columns=clustering_columns
    )
    table = bigquery_client.get_table(destination_table)

    assert list(table.clustering_fields) == clustering_columns
    assert table.expires is not None


def test_to_gbq_w_clustering_existing_table(
    scalars_df_default_index,
    dataset_id,
    bigquery_client,
):
    destination_table = f"{dataset_id}.test_to_gbq_w_clustering_existing_table"
    scalars_df_default_index.to_gbq(destination_table)

    table = bigquery_client.get_table(destination_table)
    assert table.clustering_fields is None
    assert table.expires is None

    with pytest.raises(ValueError, match="Table clustering fields cannot be changed"):
        clustering_columns = ["int64_col"]
        scalars_df_default_index.to_gbq(
            destination_table,
            if_exists="replace",
            clustering_columns=clustering_columns,
        )


def test_to_gbq_w_invalid_destination_table(scalars_df_index):
    with pytest.raises(ValueError):
        scalars_df_index.to_gbq("table_id")


def test_to_gbq_w_json(bigquery_client):
    """Test the `to_gbq` API can get a JSON column."""
    s1 = bpd.Series([1, 2, 3, 4])
    s2 = bpd.Series(
        ['"a"', "1", "false", '["a", {"b": 1}]', '{"c": [1, 2, 3]}'],
        dtype=dtypes.JSON_DTYPE,
    )

    df = bpd.DataFrame({"id": s1, "json_col": s2})
    destination_table = df.to_gbq()
    table = bigquery_client.get_table(destination_table)

    assert table.schema[1].name == "json_col"
    assert table.schema[1].field_type == "JSON"


def test_to_gbq_with_timedelta(bigquery_client, dataset_id):
    destination_table = f"{dataset_id}.test_to_gbq_with_timedelta"
    s1 = bpd.Series([1, 2, 3, 4])
    s2 = bpd.to_timedelta(bpd.Series([1, 2, 3, 4]), unit="s")
    df = bpd.DataFrame({"id": s1, "timedelta_col": s2})

    df.to_gbq(destination_table)
    table = bigquery_client.get_table(destination_table)

    assert table.schema[1].name == "timedelta_col"
    assert table.schema[1].field_type == "INTEGER"
    assert dtypes.TIMEDELTA_DESCRIPTION_TAG in table.schema[1].description


def test_gbq_round_trip_with_timedelta(session, dataset_id):
    destination_table = f"{dataset_id}.test_gbq_roundtrip_with_timedelta"
    df = pd.DataFrame(
        {
            "col_1": [1],
            "col_2": [pd.Timedelta(1, "s")],
            "col_3": [1.1],
        }
    )
    bpd.DataFrame(df).to_gbq(destination_table)

    result = session.read_gbq(destination_table)

    assert result["col_1"].dtype == dtypes.INT_DTYPE
    assert result["col_2"].dtype == dtypes.TIMEDELTA_DTYPE
    assert result["col_3"].dtype == dtypes.FLOAT_DTYPE


def test_to_gbq_timedelta_tag_ignored_when_appending(bigquery_client, dataset_id):
    # First, create a table
    destination_table = f"{dataset_id}.test_to_gbq_timedelta_tag_ignored_when_appending"
    schema = [bigquery.SchemaField("my_col", "INTEGER")]
    bigquery_client.create_table(bigquery.Table(destination_table, schema))

    # Then, append to that table with timedelta values
    df = pd.DataFrame(
        {
            "my_col": [pd.Timedelta(1, "s")],
        }
    )
    bpd.DataFrame(df).to_gbq(destination_table, if_exists="append")

    table = bigquery_client.get_table(destination_table)
    assert table.schema[0].name == "my_col"
    assert table.schema[0].field_type == "INTEGER"
    assert table.schema[0].description is None


@pytest.mark.parametrize(
    ("index"),
    [True, False],
)
def test_to_json_index_invalid_orient(
    scalars_dfs: Tuple[bigframes.dataframe.DataFrame, pd.DataFrame],
    gcs_folder: str,
    index: bool,
):
    scalars_df, _ = scalars_dfs
    path = gcs_folder + f"test_index_df_to_json_index_{index}*.jsonl"
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
    scalars_df, _ = scalars_dfs
    path = gcs_folder + f"test_index_df_to_json_index_{index}.jsonl"
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
    """Test the `to_json` API with the `index` parameter.

    Uses the scalable options orient='records' and lines=True.
    """
    scalars_df, scalars_pandas_df = scalars_dfs
    path = gcs_folder + f"test_index_df_to_json_index_{index}*.jsonl"

    scalars_df.to_json(path, index=index, orient="records", lines=True)

    gcs_df = pd.read_json(
        utils.get_first_file_from_wildcard(path),
        lines=True,
        convert_dates=["datetime_col"],
    )
    utils.convert_pandas_dtypes(gcs_df, bytes_col=True)
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
    path = gcs_folder + f"test_index_df_to_parquet_{index}*.parquet"

    # TODO(b/268693993): Type GEOGRAPHY is not currently supported for parquet.
    scalars_df = scalars_df.drop(columns="geography_col")
    scalars_pandas_df = scalars_pandas_df.drop(columns="geography_col")

    # TODO(swast): Do a bit more processing on the input DataFrame to ensure
    # the exported results are from the generated query, not just the source
    # table.
    scalars_df.to_parquet(path, index=index)

    gcs_df = pd.read_parquet(utils.get_first_file_from_wildcard(path))
    utils.convert_pandas_dtypes(gcs_df, bytes_col=False)
    if index and scalars_df.index.name is not None:
        gcs_df = gcs_df.set_index(scalars_df.index.name)

    assert len(gcs_df.index) == len(scalars_pandas_df.index)
    pd.testing.assert_index_equal(gcs_df.columns, scalars_pandas_df.columns)

    gcs_df.index.name = scalars_df.index.name
    gcs_df.index = gcs_df.index.astype("Int64")
    scalars_pandas_df.index = scalars_pandas_df.index.astype("Int64")

    # Ordering should be maintained for tables smaller than 1 GB.
    pd.testing.assert_frame_equal(
        gcs_df.drop("bytes_col", axis=1), scalars_pandas_df.drop("bytes_col", axis=1)
    )


def test_to_sql_query_unnamed_index_included(
    session: bigframes.Session,
    scalars_df_default_index: bpd.DataFrame,
    scalars_pandas_df_default_index: pd.DataFrame,
):
    bf_df = scalars_df_default_index.reset_index(drop=True).drop(columns="duration_col")
    sql, idx_ids, idx_labels = bf_df._to_sql_query(include_index=True)
    assert len(idx_labels) == 1
    assert len(idx_ids) == 1
    assert idx_labels[0] is None
    assert idx_ids[0].startswith("bigframes")

    pd_df = scalars_pandas_df_default_index.reset_index(drop=True).drop(
        columns="duration_col"
    )
    roundtrip = session.read_gbq(sql, index_col=idx_ids)
    roundtrip.index.names = [None]
    utils.assert_pandas_df_equal(roundtrip.to_pandas(), pd_df, check_index_type=False)


def test_to_sql_query_named_index_included(
    session: bigframes.Session,
    scalars_df_default_index: bpd.DataFrame,
    scalars_pandas_df_default_index: pd.DataFrame,
):
    bf_df = scalars_df_default_index.set_index("rowindex_2", drop=True).drop(
        columns="duration_col"
    )
    sql, idx_ids, idx_labels = bf_df._to_sql_query(include_index=True)
    assert len(idx_labels) == 1
    assert len(idx_ids) == 1
    assert idx_labels[0] == "rowindex_2"
    assert idx_ids[0] == "rowindex_2"

    pd_df = scalars_pandas_df_default_index.set_index("rowindex_2", drop=True).drop(
        columns="duration_col"
    )
    roundtrip = session.read_gbq(sql, index_col=idx_ids)
    utils.assert_pandas_df_equal(roundtrip.to_pandas(), pd_df)


def test_to_sql_query_unnamed_index_excluded(
    session: bigframes.Session,
    scalars_df_default_index: bpd.DataFrame,
    scalars_pandas_df_default_index: pd.DataFrame,
):
    bf_df = scalars_df_default_index.reset_index(drop=True).drop(columns="duration_col")
    sql, idx_ids, idx_labels = bf_df._to_sql_query(include_index=False)
    assert len(idx_labels) == 0
    assert len(idx_ids) == 0

    pd_df = scalars_pandas_df_default_index.reset_index(drop=True).drop(
        columns="duration_col"
    )
    roundtrip = session.read_gbq(sql)
    utils.assert_pandas_df_equal(
        roundtrip.to_pandas(), pd_df, check_index_type=False, ignore_order=True
    )


def test_to_sql_query_named_index_excluded(
    session: bigframes.Session,
    scalars_df_default_index: bpd.DataFrame,
    scalars_pandas_df_default_index: pd.DataFrame,
):
    bf_df = scalars_df_default_index.set_index("rowindex_2", drop=True).drop(
        columns="duration_col"
    )
    sql, idx_ids, idx_labels = bf_df._to_sql_query(include_index=False)
    assert len(idx_labels) == 0
    assert len(idx_ids) == 0

    pd_df = (
        scalars_pandas_df_default_index.set_index("rowindex_2", drop=True)
        .reset_index(drop=True)
        .drop(columns="duration_col")
    )
    roundtrip = session.read_gbq(sql)
    utils.assert_pandas_df_equal(
        roundtrip.to_pandas(), pd_df, check_index_type=False, ignore_order=True
    )


def test_to_numpy(scalars_dfs):
    bf_df, pd_df = scalars_dfs

    bf_result = numpy.array(bf_df[["int64_too"]], dtype="int64")
    pd_result = numpy.array(pd_df[["int64_too"]], dtype="int64")

    numpy.testing.assert_array_equal(bf_result, pd_result)
