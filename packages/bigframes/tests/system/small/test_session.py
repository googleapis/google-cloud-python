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
import random
import tempfile
import textwrap
import time
import typing
from typing import List

import google.cloud.bigquery as bigquery
import numpy as np
import pandas as pd
import pytest

import bigframes
import bigframes.core.indexes.index
import bigframes.dataframe
import bigframes.dtypes
import bigframes.ml.linear_model

FIRST_FILE = "000000000000"


def test_read_gbq_tokyo(
    session_tokyo: bigframes.Session,
    scalars_table_tokyo: str,
    scalars_pandas_df_index: pd.DataFrame,
    tokyo_location: str,
):
    df = session_tokyo.read_gbq(scalars_table_tokyo, index_col=["rowindex"])
    result = df.sort_index().to_pandas()
    expected = scalars_pandas_df_index

    _, query_job = df._block.expr.start_query()
    assert query_job.location == tokyo_location

    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    ("query_or_table", "col_order"),
    [
        pytest.param(
            "{scalars_table_id}", ["bool_col", "int64_col"], id="two_cols_in_table"
        ),
        pytest.param(
            """SELECT
                t.int64_col + 1 as my_ints,
                t.float64_col * 2 AS my_floats,
                CONCAT(t.string_col, "_2") AS my_strings,
                t.int64_col > 0 AS my_bools,
            FROM `{scalars_table_id}` AS t
            """,
            ["my_strings"],
            id="one_cols_in_query",
        ),
        pytest.param(
            "{scalars_table_id}",
            ["unknown"],
            marks=pytest.mark.xfail(
                raises=ValueError,
                reason="Column `unknown` not found in this table.",
            ),
            id="unknown_col",
        ),
    ],
)
def test_read_gbq_w_col_order(
    session: bigframes.Session,
    scalars_table_id: str,
    query_or_table: str,
    col_order: List[str],
):
    df = session.read_gbq(
        query_or_table.format(scalars_table_id=scalars_table_id), col_order=col_order
    )
    assert df.columns.tolist() == col_order


@pytest.mark.parametrize(
    ("query_or_table", "index_col"),
    [
        pytest.param(
            "{scalars_table_id}",
            ["bool_col", "int64_col"],
            id="unique_multiindex_table",
        ),
        pytest.param(
            """SELECT
                t.float64_col * 2 AS my_floats,
                CONCAT(t.string_col, "_2") AS my_strings,
                t.int64_col > 0 AS my_bools,
            FROM `{scalars_table_id}` AS t
            """,
            ["my_strings"],
            id="string_index",
        ),
        pytest.param(
            "SELECT GENERATE_UUID() AS uuid, 0 AS my_value FROM UNNEST(GENERATE_ARRAY(1, 20))",
            ["uuid"],
            id="unique_uuid_index_query",
        ),
        pytest.param(
            """
            SELECT my_index, my_value
            FROM UNNEST(
                [
                    STRUCT<my_index INT64, my_value INT64>(0, 12),
                    STRUCT<my_index INT64, my_value INT64>(1, 12),
                    STRUCT<my_index INT64, my_value INT64>(2, 24)
                ]
            )
            -- Can't normally cluster tables with ORDER BY clause.
            ORDER BY my_index DESC
            """,
            ["my_index"],
            id="unique_index_query_has_order_by",
        ),
        pytest.param(
            """
            WITH my_table AS (
                SELECT *
                FROM UNNEST(
                    [
                        STRUCT<my_index INT64, my_value INT64>(0, 12),
                        STRUCT<my_index INT64, my_value INT64>(1, 12),
                        STRUCT<my_index INT64, my_value INT64>(2, 24)
                    ]
                )
            )
            SELECT my_index, my_value FROM my_table
            """,
            ["my_index"],
            id="unique_index_query_with_named_table_expression",
        ),
        pytest.param(
            """
            CREATE TEMP TABLE test_read_gbq_w_index_col_unique_index_query_with_script
            AS SELECT * FROM UNNEST(
                [
                    STRUCT<my_index INT64, my_value INT64>(0, 12),
                    STRUCT<my_index INT64, my_value INT64>(1, 12),
                    STRUCT<my_index INT64, my_value INT64>(2, 24)
                ]
            );
            SELECT my_index, my_value FROM test_read_gbq_w_index_col_unique_index_query_with_script
            """,
            ["my_index"],
            id="unique_index_query_with_script",
        ),
        pytest.param(
            "{scalars_table_id}",
            ["bool_col"],
            id="non_unique_index",
        ),
        pytest.param(
            "{scalars_table_id}",
            ["float64_col"],
            id="non_unique_float_index",
        ),
        pytest.param(
            "{scalars_table_id}",
            [
                "timestamp_col",
                "float64_col",
                "datetime_col",
                "int64_too",
            ],
            id="multi_part_index_direct",
        ),
        pytest.param(
            "SELECT * FROM {scalars_table_id}",
            [
                "timestamp_col",
                "float64_col",
                "string_col",
                "bool_col",
                "int64_col",
                "int64_too",
            ],
            id="multi_part_index_w_query",
        ),
    ],
)
def test_read_gbq_w_index_col(
    session: bigframes.Session,
    scalars_table_id: str,
    query_or_table: str,
    index_col: List[str],
):
    df = session.read_gbq(
        query_or_table.format(scalars_table_id=scalars_table_id),
        index_col=index_col,
    )
    assert list(df.index.names) == index_col

    # Verify that we get the expected number of results.
    bf_shape = df.shape
    result = df.to_pandas()
    assert bf_shape == result.shape


def test_read_gbq_w_anonymous_query_results_table(session: bigframes.Session):
    """Ensure BigQuery DataFrames can be used to inspect the results of a query job."""
    query = textwrap.dedent(
        """
        SELECT SUM(`number`) AS total_people, name
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        GROUP BY name
        HAVING name < "B"
        """
    )
    job = session.bqclient.query(query)
    expected = job.to_dataframe().set_index("name").sort_index()
    destination = f"{job.destination.project}.{job.destination.dataset_id}.{job.destination.table_id}"
    df = session.read_gbq(destination, index_col="name")
    result = df.to_pandas()
    expected.index = expected.index.astype(result.index.dtype)
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_read_gbq_w_primary_keys_table(
    session: bigframes.Session, usa_names_grouped_table: bigquery.Table
):
    table = usa_names_grouped_table
    # TODO(b/305264153): Use public properties to fetch primary keys once
    # added to google-cloud-bigquery.
    primary_keys = (
        table._properties.get("tableConstraints", {})
        .get("primaryKey", {})
        .get("columns")
    )
    assert len(primary_keys) != 0

    df = session.read_gbq(f"{table.project}.{table.dataset_id}.{table.table_id}")
    result = df.head(100).to_pandas()

    # Verify that the DataFrame is already sorted by primary keys.
    sorted_result = result.sort_values(primary_keys)
    pd.testing.assert_frame_equal(result, sorted_result)

    # Verify that we're working from a snapshot rather than a copy of the table.
    assert "FOR SYSTEM_TIME AS OF TIMESTAMP" in df.sql


@pytest.mark.parametrize(
    ("query_or_table", "max_results"),
    [
        pytest.param("{scalars_table_id}", 2, id="two_rows_in_table"),
        pytest.param(
            """SELECT
                t.float64_col * 2 AS my_floats,
                CONCAT(t.string_col, "_2") AS my_strings,
                t.int64_col > 0 AS my_bools,
            FROM `{scalars_table_id}` AS t
            """,
            2,
            id="three_rows_in_query",
        ),
        pytest.param(
            "{scalars_table_id}",
            -1,
            marks=pytest.mark.xfail(
                raises=ValueError,
                reason="`max_results` should be a positive number.",
            ),
            id="neg_rows",
        ),
    ],
)
def test_read_gbq_w_max_results(
    session: bigframes.Session,
    scalars_table_id: str,
    query_or_table: str,
    max_results: int,
):
    df = session.read_gbq(
        query_or_table.format(scalars_table_id=scalars_table_id),
        max_results=max_results,
    )
    bf_result = df.to_pandas()
    assert bf_result.shape[0] == max_results


def test_read_gbq_w_script_no_select(session, dataset_id: str):
    ddl = f"""
    CREATE TABLE `{dataset_id}.test_read_gbq_w_ddl` (
        `col_a` INT64,
        `col_b` STRING
    );

    INSERT INTO `{dataset_id}.test_read_gbq_w_ddl`
    VALUES (123, 'hello world');
    """
    df = session.read_gbq(ddl).to_pandas()
    assert df["statement_type"][0] == "SCRIPT"


def test_read_gbq_twice_with_same_timestamp(session, penguins_table_id):
    df1 = session.read_gbq(penguins_table_id)
    time.sleep(1)
    df2 = session.read_gbq(penguins_table_id)
    df1.columns = [
        "species1",
        "island1",
        "culmen_length_mm1",
        "culmen_depth_mm1",
        "flipper_length_mm1",
        "body_mass_g1",
        "sex1",
    ]
    df3 = df1.join(df2)
    assert df3 is not None


def test_read_gbq_model(session, penguins_linear_model_name):
    model = session.read_gbq_model(penguins_linear_model_name)
    assert isinstance(model, bigframes.ml.linear_model.LinearRegression)


def test_read_pandas(session, scalars_dfs):
    _, scalars_pandas_df = scalars_dfs

    df = session.read_pandas(scalars_pandas_df)

    result = df.to_pandas()
    expected = scalars_pandas_df

    pd.testing.assert_frame_equal(result, expected)


def test_read_pandas_col_label_w_space(session: bigframes.Session):
    expected = pd.DataFrame(
        {
            "Animal": ["Falcon", "Falcon", "Parrot", "Parrot"],
            "Max Speed": [380.0, 370.0, 24.0, 26.0],
        }
    )
    result = session.read_pandas(expected).to_pandas()

    pd.testing.assert_frame_equal(
        result, expected, check_index_type=False, check_dtype=False
    )


def test_read_pandas_multi_index(session, scalars_pandas_df_multi_index):
    df = session.read_pandas(scalars_pandas_df_multi_index)
    result = df.to_pandas()
    pd.testing.assert_frame_equal(result, scalars_pandas_df_multi_index)


def test_read_pandas_rowid_exists_adds_suffix(session, scalars_pandas_df_default_index):
    pandas_df = scalars_pandas_df_default_index.copy()
    pandas_df["rowid"] = np.arange(pandas_df.shape[0])

    df_roundtrip = session.read_pandas(pandas_df).to_pandas()
    pd.testing.assert_frame_equal(df_roundtrip, pandas_df, check_dtype=False)


def test_read_pandas_tokyo(
    session_tokyo: bigframes.Session,
    scalars_pandas_df_index: pd.DataFrame,
    tokyo_location: str,
):
    df = session_tokyo.read_pandas(scalars_pandas_df_index)
    result = df.to_pandas()
    expected = scalars_pandas_df_index

    _, query_job = df._block.expr.start_query()
    assert query_job.location == tokyo_location

    pd.testing.assert_frame_equal(result, expected)


def test_read_csv_gcs_default_engine(session, scalars_dfs, gcs_folder):
    scalars_df, _ = scalars_dfs
    if scalars_df.index.name is not None:
        path = gcs_folder + "test_read_csv_gcs_default_engine_w_index*.csv"
    else:
        path = gcs_folder + "test_read_csv_gcs_default_engine_wo_index*.csv"
    read_path = path.replace("*", FIRST_FILE)
    scalars_df.to_csv(path, index=False)
    dtype = scalars_df.dtypes.to_dict()
    dtype.pop("geography_col")
    df = session.read_csv(
        read_path,
        # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
        dtype=dtype,
    )

    # TODO(chelsealin): If we serialize the index, can more easily compare values.
    pd.testing.assert_index_equal(df.columns, scalars_df.columns)

    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # numeric and geometry types, so they're skipped here.
    df = df.drop(columns=["bytes_col", "numeric_col", "geography_col"])
    scalars_df = scalars_df.drop(columns=["bytes_col", "numeric_col", "geography_col"])
    assert df.shape[0] == scalars_df.shape[0]
    pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)


def test_read_csv_gcs_bq_engine(session, scalars_dfs, gcs_folder):
    scalars_df, _ = scalars_dfs
    if scalars_df.index.name is not None:
        path = gcs_folder + "test_read_csv_gcs_bq_engine_w_index*.csv"
    else:
        path = gcs_folder + "test_read_csv_gcs_bq_engine_wo_index*.csv"
    scalars_df.to_csv(path, index=False)
    df = session.read_csv(path, engine="bigquery")

    # TODO(chelsealin): If we serialize the index, can more easily compare values.
    pd.testing.assert_index_equal(df.columns, scalars_df.columns)

    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # datetime, numeric and geometry types, so they're skipped here.
    df = df.drop(columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"])
    scalars_df = scalars_df.drop(
        columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"]
    )
    assert df.shape[0] == scalars_df.shape[0]
    pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)


@pytest.mark.parametrize(
    "sep",
    [
        pytest.param(",", id="default_sep"),
        pytest.param("\t", id="custom_sep"),
    ],
)
def test_read_csv_local_default_engine(session, scalars_dfs, sep):
    scalars_df, scalars_pandas_df = scalars_dfs
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_default_engine.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df.to_csv(path, index=False, sep=sep)
        dtype = scalars_df.dtypes.to_dict()
        dtype.pop("geography_col")
        df = session.read_csv(
            path,
            sep=sep,
            # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
            dtype=dtype,
        )

        # TODO(chelsealin): If we serialize the index, can more easily compare values.
        pd.testing.assert_index_equal(df.columns, scalars_df.columns)

        # The auto detects of BigQuery load job have restrictions to detect the bytes,
        # numeric and geometry types, so they're skipped here.
        df = df.drop(columns=["bytes_col", "numeric_col", "geography_col"])
        scalars_df = scalars_df.drop(
            columns=["bytes_col", "numeric_col", "geography_col"]
        )
        assert df.shape[0] == scalars_df.shape[0]
        pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)


@pytest.mark.parametrize(
    "sep",
    [
        pytest.param(",", id="default_sep"),
        pytest.param("\t", id="custom_sep"),
    ],
)
def test_read_csv_local_bq_engine(session, scalars_dfs, sep):
    scalars_df, scalars_pandas_df = scalars_dfs
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_bq_engine.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df.to_csv(path, index=False, sep=sep)
        df = session.read_csv(path, engine="bigquery", sep=sep)

        # TODO(chelsealin): If we serialize the index, can more easily compare values.
        pd.testing.assert_index_equal(df.columns, scalars_df.columns)

        # The auto detects of BigQuery load job have restrictions to detect the bytes,
        # datetime, numeric and geometry types, so they're skipped here.
        df = df.drop(
            columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"]
        )
        scalars_df = scalars_df.drop(
            columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"]
        )
        assert df.shape[0] == scalars_df.shape[0]
        pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)


def test_read_csv_localbuffer_bq_engine(session, scalars_dfs):
    scalars_df, scalars_pandas_df = scalars_dfs
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_bq_engine.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df.to_csv(path, index=False)
        with open(path, "rb") as buffer:
            df = session.read_csv(buffer, engine="bigquery")

        # TODO(chelsealin): If we serialize the index, can more easily compare values.
        pd.testing.assert_index_equal(df.columns, scalars_df.columns)

        # The auto detects of BigQuery load job have restrictions to detect the bytes,
        # datetime, numeric and geometry types, so they're skipped here.
        df = df.drop(
            columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"]
        )
        scalars_df = scalars_df.drop(
            columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"]
        )
        assert df.shape[0] == scalars_df.shape[0]
        pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        pytest.param(
            {"engine": "bigquery", "names": []},
            "BigQuery engine does not support these arguments",
            id="with_names",
        ),
        pytest.param(
            {"engine": "bigquery", "dtype": {}},
            "BigQuery engine does not support these arguments",
            id="with_dtype",
        ),
        pytest.param(
            {"engine": "bigquery", "index_col": False},
            "BigQuery engine only supports a single column name for `index_col`.",
            id="with_index_col_false",
        ),
        pytest.param(
            {"engine": "bigquery", "index_col": 5},
            "BigQuery engine only supports a single column name for `index_col`.",
            id="with_index_col_not_str",
        ),
        pytest.param(
            {"engine": "bigquery", "usecols": [1, 2]},
            "BigQuery engine only supports an iterable of strings for `usecols`.",
            id="with_usecols_invalid",
        ),
        pytest.param(
            {"engine": "bigquery", "encoding": "ASCII"},
            "BigQuery engine only supports the following encodings",
            id="with_encoding_invalid",
        ),
    ],
)
def test_read_csv_bq_engine_throws_not_implemented_error(session, kwargs, match):
    with pytest.raises(NotImplementedError, match=match):
        session.read_csv("", **kwargs)


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        pytest.param(
            {"chunksize": 5},
            "'chunksize' and 'iterator' arguments are not supported.",
            id="with_chunksize",
        ),
        pytest.param(
            {"iterator": True},
            "'chunksize' and 'iterator' arguments are not supported.",
            id="with_iterator",
        ),
    ],
)
def test_read_csv_default_engine_throws_not_implemented_error(
    session,
    scalars_df_index,
    gcs_folder,
    kwargs,
    match,
):
    path = (
        gcs_folder
        + "test_read_csv_gcs_default_engine_throws_not_implemented_error*.csv"
    )
    read_path = path.replace("*", FIRST_FILE)
    scalars_df_index.to_csv(path)
    with pytest.raises(NotImplementedError, match=match):
        session.read_csv(read_path, **kwargs)


def test_read_csv_gcs_default_engine_w_header(session, scalars_df_index, gcs_folder):
    path = gcs_folder + "test_read_csv_gcs_default_engine_w_header*.csv"
    read_path = path.replace("*", FIRST_FILE)
    scalars_df_index.to_csv(path)

    # Skips header=N rows, normally considers the N+1th row as the header, but overridden by
    # passing the `names` argument. In this case, pandas will skip the N+1th row too, take
    # the column names from `names`, and begin reading data from the N+2th row.
    df = session.read_csv(
        read_path,
        header=2,
        names=scalars_df_index.columns.to_list(),
    )
    assert df.shape[0] == scalars_df_index.shape[0] - 2
    assert len(df.columns) == len(scalars_df_index.columns)


def test_read_csv_gcs_bq_engine_w_header(session, scalars_df_index, gcs_folder):
    path = gcs_folder + "test_read_csv_gcs_bq_engine_w_header*.csv"
    scalars_df_index.to_csv(path, index=False)

    # Skip the header and the first 2 data rows. Note that one line of header
    # also got added while writing the csv through `to_csv`, so we would have to
    # pass headers=3 in the `read_csv` to skip reading the header and two rows.
    # Without provided schema, the column names would be like `bool_field_0`,
    # `string_field_1` and etc.
    df = session.read_csv(path, header=3, engine="bigquery")
    assert df.shape[0] == scalars_df_index.shape[0] - 2
    assert len(df.columns) == len(scalars_df_index.columns)


def test_read_csv_local_default_engine_w_header(session, scalars_pandas_df_index):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_default_engine_w_header.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df_index.to_csv(path, index=False)

        # Skips header=N rows. Normally row N+1 would be the header now, but overridden by
        # passing the `names` argument. In this case, pandas will skip row N+1 too, infer
        # the column names from `names`, and begin reading data from row N+2.
        df = session.read_csv(
            path,
            header=2,
            names=scalars_pandas_df_index.columns.to_list(),
        )
        assert df.shape[0] == scalars_pandas_df_index.shape[0] - 2
        assert len(df.columns) == len(scalars_pandas_df_index.columns)


def test_read_csv_local_bq_engine_w_header(session, scalars_pandas_df_index):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_bq_engine_w_header.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df_index.to_csv(path, index=False)

        # Skip the header and the first 2 data rows. Note that one line of
        # header also got added while writing the csv through `to_csv`, so we
        # would have to pass headers=3 in the `read_csv` to skip reading the
        # header and two rows. Without provided schema, the column names would
        # be like `bool_field_0`, `string_field_1` and etc.
        df = session.read_csv(path, header=3, engine="bigquery")
        assert df.shape[0] == scalars_pandas_df_index.shape[0] - 2
        assert len(df.columns) == len(scalars_pandas_df_index.columns)


def test_read_csv_gcs_default_engine_w_index_col_name(
    session, scalars_df_default_index, gcs_folder
):
    path = gcs_folder + "test_read_csv_gcs_default_engine_w_index_col_name*.csv"
    read_path = path.replace("*", FIRST_FILE)
    scalars_df_default_index.to_csv(path)

    df = session.read_csv(read_path, index_col="rowindex")
    scalars_df_default_index = scalars_df_default_index.set_index(
        "rowindex"
    ).sort_index()
    pd.testing.assert_index_equal(df.columns, scalars_df_default_index.columns)
    assert df.index.name == "rowindex"


def test_read_csv_gcs_default_engine_w_index_col_index(
    session, scalars_df_default_index, gcs_folder
):
    path = gcs_folder + "test_read_csv_gcs_default_engine_w_index_col_index*.csv"
    read_path = path.replace("*", FIRST_FILE)
    scalars_df_default_index.to_csv(path)

    index_col = scalars_df_default_index.columns.to_list().index("rowindex")
    df = session.read_csv(read_path, index_col=index_col)
    scalars_df_default_index = scalars_df_default_index.set_index(
        "rowindex"
    ).sort_index()
    pd.testing.assert_index_equal(df.columns, scalars_df_default_index.columns)
    assert df.index.name == "rowindex"


def test_read_csv_local_default_engine_w_index_col_name(
    session, scalars_pandas_df_default_index
):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_default_engine_w_index_col_name"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df_default_index.to_csv(path, index=False)

        df = session.read_csv(path, index_col="rowindex")
        scalars_pandas_df_default_index = scalars_pandas_df_default_index.set_index(
            "rowindex"
        ).sort_index()
        pd.testing.assert_index_equal(
            df.columns, scalars_pandas_df_default_index.columns
        )
        assert df.index.name == "rowindex"


def test_read_csv_local_default_engine_w_index_col_index(
    session, scalars_pandas_df_default_index
):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_default_engine_w_index_col_index"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df_default_index.to_csv(path, index=False)

        index_col = scalars_pandas_df_default_index.columns.to_list().index("rowindex")
        df = session.read_csv(path, index_col=index_col)
        scalars_pandas_df_default_index = scalars_pandas_df_default_index.set_index(
            "rowindex"
        ).sort_index()
        pd.testing.assert_index_equal(
            df.columns, scalars_pandas_df_default_index.columns
        )
        assert df.index.name == "rowindex"


@pytest.mark.parametrize(
    "engine",
    [
        pytest.param("bigquery", id="bq_engine"),
        pytest.param(None, id="default_engine"),
    ],
)
def test_read_csv_gcs_w_usecols(session, scalars_df_index, gcs_folder, engine):
    path = gcs_folder + "test_read_csv_gcs_w_usecols"
    path = path + "_default_engine*.csv" if engine is None else path + "_bq_engine*.csv"
    read_path = path.replace("*", FIRST_FILE) if engine is None else path
    scalars_df_index.to_csv(path)

    # df should only have 1 column which is bool_col.
    df = session.read_csv(read_path, usecols=["bool_col"], engine=engine)
    assert len(df.columns) == 1


@pytest.mark.parametrize(
    "engine",
    [
        pytest.param("bigquery", id="bq_engine"),
        pytest.param(None, id="default_engine"),
    ],
)
def test_read_csv_local_w_usecols(session, scalars_pandas_df_index, engine):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_w_usecols.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        scalars_pandas_df_index.to_csv(path, index=False)

        # df should only have 1 column which is bool_col.
        df = session.read_csv(path, usecols=["bool_col"], engine=engine)
        assert len(df.columns) == 1


@pytest.mark.parametrize(
    "engine",
    [
        pytest.param("bigquery", id="bq_engine"),
        pytest.param(None, id="default_engine"),
    ],
)
def test_read_csv_local_w_encoding(session, penguins_pandas_df_default_index, engine):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_w_encoding.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        penguins_pandas_df_default_index.to_csv(
            path, index=False, encoding="ISO-8859-1"
        )

        # File can only be read using the same character encoding as when written.
        df = session.read_csv(path, engine=engine, encoding="ISO-8859-1")

        # TODO(chelsealin): If we serialize the index, can more easily compare values.
        pd.testing.assert_index_equal(
            df.columns, penguins_pandas_df_default_index.columns
        )

        assert df.shape[0] == penguins_pandas_df_default_index.shape[0]


def test_read_pickle_local(session, penguins_pandas_df_default_index, tmp_path):
    path = tmp_path / "test_read_csv_local_w_encoding.pkl"

    penguins_pandas_df_default_index.to_pickle(path)
    df = session.read_pickle(path)

    pd.testing.assert_frame_equal(penguins_pandas_df_default_index, df.to_pandas())


def test_read_pickle_buffer(session, penguins_pandas_df_default_index):
    buffer = io.BytesIO()
    penguins_pandas_df_default_index.to_pickle(buffer)
    buffer.seek(0)
    df = session.read_pickle(buffer)

    pd.testing.assert_frame_equal(penguins_pandas_df_default_index, df.to_pandas())


def test_read_pickle_series_buffer(session):
    pd_series = pd.Series([1, 2, 3, 4, 5], dtype="Int64")
    buffer = io.BytesIO()
    pd_series.to_pickle(buffer)
    buffer.seek(0)
    bf_series = session.read_pickle(buffer).to_pandas()
    pd_series.index = pd_series.index.astype("Int64")

    assert (pd_series == bf_series).all()


def test_read_pickle_gcs(session, penguins_pandas_df_default_index, gcs_folder):
    path = gcs_folder + "test_read_pickle_gcs.pkl"
    penguins_pandas_df_default_index.to_pickle(path)
    df = session.read_pickle(path)

    pd.testing.assert_frame_equal(penguins_pandas_df_default_index, df.to_pandas())


def test_read_parquet_gcs(session: bigframes.Session, scalars_dfs, gcs_folder):
    scalars_df, _ = scalars_dfs
    # Include wildcard so that multiple files can be written/read if > 1 GB.
    # https://cloud.google.com/bigquery/docs/exporting-data#exporting_data_into_one_or_more_files
    path = gcs_folder + test_read_parquet_gcs.__name__ + "*.parquet"
    df_in: bigframes.dataframe.DataFrame = scalars_df.copy()
    # GEOGRAPHY not supported in parquet export.
    df_in = df_in.drop(columns="geography_col")
    # Make sure we can also serialize the order.
    df_write = df_in.reset_index(drop=False)
    df_write.index.name = f"ordering_id_{random.randrange(1_000_000)}"
    df_write.to_parquet(path, index=True)

    df_out = (
        session.read_parquet(path)
        # Restore order.
        .set_index(df_write.index.name).sort_index()
        # Restore index.
        .set_index(typing.cast(str, df_in.index.name))
    )

    # DATETIME gets loaded as TIMESTAMP in parquet. See:
    # https://cloud.google.com/bigquery/docs/exporting-data#parquet_export_details
    df_out = df_out.assign(
        datetime_col=df_out["datetime_col"].astype("timestamp[us][pyarrow]")
    )

    # Make sure we actually have at least some values before comparing.
    assert df_out.size != 0
    pd_df_in = df_in.to_pandas()
    pd_df_out = df_out.to_pandas()
    pd.testing.assert_frame_equal(pd_df_in, pd_df_out)


@pytest.mark.parametrize(
    "compression",
    [
        None,
        "gzip",
        "snappy",
    ],
)
def test_read_parquet_gcs_compressed(
    session: bigframes.Session, scalars_dfs, gcs_folder, compression
):
    scalars_df, _ = scalars_dfs
    # Include wildcard so that multiple files can be written/read if > 1 GB.
    # https://cloud.google.com/bigquery/docs/exporting-data#exporting_data_into_one_or_more_files
    path = (
        gcs_folder
        + test_read_parquet_gcs_compressed.__name__
        + (f"_{compression}" if compression else "")
        + "*.parquet"
    )
    df_in: bigframes.dataframe.DataFrame = scalars_df.copy()
    # GEOGRAPHY not supported in parquet export.
    df_in = df_in.drop(columns="geography_col")
    # Make sure we can also serialize the order.
    df_write = df_in.reset_index(drop=False)
    df_write.index.name = f"ordering_id_{random.randrange(1_000_000)}"
    df_write.to_parquet(path, compression=compression, index=True)

    df_out = (
        session.read_parquet(path)
        # Restore order.
        .set_index(df_write.index.name).sort_index()
        # Restore index.
        .set_index(typing.cast(str, df_in.index.name))
    )

    # DATETIME gets loaded as TIMESTAMP in parquet. See:
    # https://cloud.google.com/bigquery/docs/exporting-data#parquet_export_details
    df_out = df_out.assign(
        datetime_col=df_out["datetime_col"].astype("timestamp[us][pyarrow]")
    )

    # Make sure we actually have at least some values before comparing.
    assert df_out.size != 0
    pd_df_in = df_in.to_pandas()
    pd_df_out = df_out.to_pandas()
    pd.testing.assert_frame_equal(pd_df_in, pd_df_out)


@pytest.mark.parametrize(
    "compression",
    [
        "brotli",
        "lz4",
        "zstd",
        "unknown",
    ],
)
def test_read_parquet_gcs_compression_not_supported(
    session: bigframes.Session, scalars_dfs, gcs_folder, compression
):
    scalars_df, _ = scalars_dfs
    # Include wildcard so that multiple files can be written/read if > 1 GB.
    # https://cloud.google.com/bigquery/docs/exporting-data#exporting_data_into_one_or_more_files
    path = (
        gcs_folder
        + test_read_parquet_gcs_compression_not_supported.__name__
        + (f"_{compression}" if compression else "")
        + "*.parquet"
    )
    df_in: bigframes.dataframe.DataFrame = scalars_df.copy()
    # GEOGRAPHY not supported in parquet export.
    df_in = df_in.drop(columns="geography_col")
    # Make sure we can also serialize the order.
    df_write = df_in.reset_index(drop=False)
    df_write.index.name = f"ordering_id_{random.randrange(1_000_000)}"

    with pytest.raises(
        ValueError, match=f"'{compression}' is not valid for compression"
    ):
        df_write.to_parquet(path, compression=compression, index=True)


def test_read_json_gcs_bq_engine(session, scalars_dfs, gcs_folder):
    scalars_df, _ = scalars_dfs
    path = gcs_folder + "test_read_json_gcs_bq_engine_w_index*.json"
    read_path = path.replace("*", FIRST_FILE)
    scalars_df.to_json(path, index=False, lines=True, orient="records")
    df = session.read_json(read_path, lines=True, orient="records", engine="bigquery")

    # The auto detects of BigQuery load job does not preserve any ordering of columns for json.
    pd.testing.assert_index_equal(
        df.columns.sort_values(), scalars_df.columns.sort_values()
    )

    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # datetime, numeric and geometry types, so they're skipped here.
    df = df.drop(columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"])
    scalars_df = scalars_df.drop(
        columns=["bytes_col", "datetime_col", "numeric_col", "geography_col"]
    )
    assert df.shape[0] == scalars_df.shape[0]
    pd.testing.assert_series_equal(
        df.dtypes.sort_index(), scalars_df.dtypes.sort_index()
    )


def test_read_json_gcs_default_engine(session, scalars_dfs, gcs_folder):
    scalars_df, _ = scalars_dfs
    path = gcs_folder + "test_read_json_gcs_default_engine_w_index*.json"
    read_path = path.replace("*", FIRST_FILE)
    scalars_df.to_json(
        path,
        index=False,
        lines=True,
        orient="records",
    )
    dtype = scalars_df.dtypes.to_dict()
    dtype.pop("geography_col")

    df = session.read_json(
        read_path,
        # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
        dtype=dtype,
        lines=True,
        orient="records",
    )

    pd.testing.assert_index_equal(df.columns, scalars_df.columns)

    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # numeric and geometry types, so they're skipped here.
    df = df.drop(columns=["bytes_col", "numeric_col", "geography_col"])
    scalars_df = scalars_df.drop(columns=["bytes_col", "numeric_col", "geography_col"])

    # pandas read_json does not respect the dtype overrides for these columns
    df = df.drop(columns=["date_col", "datetime_col", "time_col"])
    scalars_df = scalars_df.drop(columns=["date_col", "datetime_col", "time_col"])

    assert df.shape[0] == scalars_df.shape[0]
    pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)
