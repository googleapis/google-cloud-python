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
import json
import random
import re
import tempfile
import textwrap
import time
import typing
from typing import List, Optional, Sequence
import warnings

import bigframes_vendored.pandas.io.gbq as vendored_pandas_gbq
import db_dtypes  # type:ignore
import google
import google.cloud.bigquery as bigquery
import numpy as np
import pandas as pd
import pandas.arrays as arrays
import pyarrow as pa
import pytest

import bigframes
import bigframes.dataframe
import bigframes.dtypes
import bigframes.ml.linear_model
from bigframes.testing import utils

all_write_engines = pytest.mark.parametrize(
    "write_engine",
    [
        "default",
        "bigquery_inline",
        "bigquery_load",
        "bigquery_streaming",
        "bigquery_write",
    ],
)


@pytest.fixture(scope="module")
def df_and_local_csv(scalars_df_index):
    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # datetime, numeric and geometry types, so they're skipped here.
    drop_columns = [
        "bytes_col",
        "datetime_col",
        "numeric_col",
        "geography_col",
        "duration_col",
    ]
    scalars_df_index = scalars_df_index.drop(columns=drop_columns)

    with tempfile.TemporaryDirectory() as dir:
        # Prepares local CSV file for reading
        path = dir + "/test_read_csv_w_local_csv.csv"
        scalars_df_index.to_csv(path, index=True)
        yield scalars_df_index, path


@pytest.fixture(scope="module")
def df_and_gcs_csv(scalars_df_index, gcs_folder):
    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # datetime, numeric and geometry types, so they're skipped here.
    drop_columns = [
        "bytes_col",
        "datetime_col",
        "numeric_col",
        "geography_col",
        "duration_col",
    ]
    scalars_df_index = scalars_df_index.drop(columns=drop_columns)

    path = gcs_folder + "test_read_csv_w_gcs_csv*.csv"
    read_path = utils.get_first_file_from_wildcard(path)
    scalars_df_index.to_csv(path, index=True)
    return scalars_df_index, read_path


@pytest.fixture(scope="module")
def df_and_gcs_csv_for_two_columns(scalars_df_index, gcs_folder):
    # Some tests require only two columns to be present in the CSV file.
    selected_cols = ["bool_col", "int64_col"]
    scalars_df_index = scalars_df_index[selected_cols]

    path = gcs_folder + "df_and_gcs_csv_for_two_columns*.csv"
    read_path = utils.get_first_file_from_wildcard(path)
    scalars_df_index.to_csv(path, index=True)
    return scalars_df_index, read_path


def test_read_gbq_tokyo(
    session_tokyo: bigframes.Session,
    scalars_table_tokyo: str,
    scalars_pandas_df_index: pd.DataFrame,
    tokyo_location: str,
):
    df = session_tokyo.read_gbq(scalars_table_tokyo, index_col=["rowindex"])
    df.sort_index(inplace=True)
    expected = scalars_pandas_df_index

    # use_explicit_destination=True, otherwise might use path with no query_job
    exec_result = session_tokyo._executor.execute(
        df._block.expr, use_explicit_destination=True
    )
    assert exec_result.query_job is not None
    assert exec_result.query_job.location == tokyo_location

    assert len(expected) == exec_result.total_rows


@pytest.mark.parametrize(
    ("query_or_table", "columns"),
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
    ],
)
def test_read_gbq_w_columns(
    session: bigframes.Session,
    scalars_table_id: str,
    query_or_table: str,
    columns: List[str],
):
    df = session.read_gbq(
        query_or_table.format(scalars_table_id=scalars_table_id), columns=columns
    )
    assert df.columns.tolist() == columns


def test_read_gbq_w_unknown_column(
    session: bigframes.Session,
    scalars_table_id: str,
):
    with pytest.raises(
        ValueError,
        match=re.escape("Column 'int63_col' is not found. Did you mean 'int64_col'?"),
    ):
        session.read_gbq(
            scalars_table_id,
            columns=["string_col", "int63_col", "bool_col"],
        )


def test_read_gbq_w_unknown_index_col(
    session: bigframes.Session,
    scalars_table_id: str,
):
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Column 'int64_two' of `index_col` not found in this table. Did you mean 'int64_too'?"
        ),
    ):
        session.read_gbq(
            scalars_table_id,
            index_col=["int64_col", "int64_two"],
        )


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
            ORDER BY my_strings
            """,
            ["my_strings"],
            id="string_index_w_order_by",
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
    # Validate that the table we're querying has a primary key.
    table = usa_names_grouped_table
    table_constraints = table.table_constraints
    assert table_constraints is not None
    primary_key = table_constraints.primary_key
    assert primary_key is not None
    primary_keys = primary_key.columns
    assert len(primary_keys) != 0

    df = session.read_gbq(f"{table.project}.{table.dataset_id}.{table.table_id}")
    result = df.head(100).to_pandas()

    # Verify that primary keys are used as the index.
    assert list(result.index.names) == list(primary_keys)

    # Verify that the DataFrame is already sorted by primary keys.
    sorted_result = result.sort_values(primary_keys)
    pd.testing.assert_frame_equal(result, sorted_result)

    # Verify that we're working from a snapshot rather than a copy of the table.
    assert "FOR SYSTEM_TIME AS OF TIMESTAMP" in df.sql


def test_read_gbq_w_primary_keys_table_and_filters(
    session: bigframes.Session, usa_names_grouped_table: bigquery.Table
):
    """
    Verify fix for internal issue 338039517, where using filters didn't use the
    primary keys for indexing / ordering.
    """
    # Validate that the table we're querying has a primary key.
    table = usa_names_grouped_table
    table_constraints = table.table_constraints
    assert table_constraints is not None
    primary_key = table_constraints.primary_key
    assert primary_key is not None
    primary_keys = primary_key.columns
    assert len(primary_keys) != 0

    df = session.read_gbq(
        f"{table.project}.{table.dataset_id}.{table.table_id}",
        filters=typing.cast(
            vendored_pandas_gbq.FiltersType,
            [
                ("name", "LIKE", "W%"),
                ("total_people", ">", 100),
            ],
        ),
    )
    result = df.to_pandas()

    # Verify that primary keys are used as the index.
    assert list(result.index.names) == list(primary_keys)

    # Verify that the DataFrame is already sorted by primary keys.
    sorted_result = result.sort_values(primary_keys)
    pd.testing.assert_frame_equal(result, sorted_result)


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


@pytest.mark.parametrize(
    "source_table",
    [
        # Wildcard tables
        "bigquery-public-data.noaa_gsod.gsod194*",
        # Linked datasets
        "bigframes-dev.thelook_ecommerce.orders",
        # Materialized views
        "bigframes-dev.bigframes_tests_sys.base_table_mat_view",
    ],
)
def test_read_gbq_warns_time_travel_disabled(session, source_table):
    with warnings.catch_warnings(record=True) as warned:
        session.read_gbq(source_table, use_cache=False)
        assert len(warned) == 1
        assert warned[0].category == bigframes.exceptions.TimeTravelDisabledWarning


def test_read_gbq_w_ambigous_name(
    session: bigframes.Session,
):
    # Ensure read_gbq works when table and column share a name
    df = (
        session.read_gbq("bigframes-dev.bigframes_tests_sys.ambiguous_name")
        .sort_values("x", ascending=False)
        .reset_index(drop=True)
        .to_pandas()
    )
    pd_df = pd.DataFrame({"x": [2, 1], "ambiguous_name": [20, 10]})
    pd.testing.assert_frame_equal(df, pd_df, check_dtype=False, check_index_type=False)


def test_read_gbq_table_clustered_with_filter(session: bigframes.Session):
    df = session.read_gbq_table(
        "bigquery-public-data.cloud_storage_geo_index.landsat_index",
        filters=typing.cast(
            vendored_pandas_gbq.FiltersType,
            [[("sensor_id", "LIKE", "OLI%")], [("sensor_id", "LIKE", "%TIRS")]],
        ),
        columns=["sensor_id"],
    )
    sensors = df.groupby(["sensor_id"]).agg("count").to_pandas(ordered=False)
    assert "OLI" in sensors.index
    assert "TIRS" in sensors.index
    assert "OLI_TIRS" in sensors.index


_GSOD_ALL_TABLES = "bigquery-public-data.noaa_gsod.gsod*"
_GSOD_1930S = "bigquery-public-data.noaa_gsod.gsod193*"


@pytest.mark.parametrize(
    "api_method",
    # Test that both methods work as there's a risk that read_gbq /
    # read_gbq_table makes for an infinite loop. Table reads can convert to
    # queries and read_gbq reads from tables.
    ["read_gbq", "read_gbq_table"],
)
@pytest.mark.parametrize(
    ("filters", "table_id", "index_col", "columns", "max_results"),
    [
        pytest.param(
            [("_table_suffix", ">=", "1930"), ("_table_suffix", "<=", "1939")],
            _GSOD_ALL_TABLES,
            ["stn", "wban", "year", "mo", "da"],
            ["temp", "max", "min"],
            100,
            id="all",
        ),
        pytest.param(
            (),  # filters
            _GSOD_1930S,
            (),  # index_col
            ["temp", "max", "min"],
            None,  # max_results
            id="columns",
        ),
        pytest.param(
            [("_table_suffix", ">=", "1930"), ("_table_suffix", "<=", "1939")],
            _GSOD_ALL_TABLES,
            (),  # index_col,
            (),  # columns
            None,  # max_results
            id="filters",
        ),
        pytest.param(
            (),  # filters
            _GSOD_1930S,
            ["stn", "wban", "year", "mo", "da"],
            (),  # columns
            None,  # max_results
            id="index_col",
        ),
        pytest.param(
            (),  # filters
            _GSOD_1930S,
            (),  # index_col
            (),  # columns
            100,  # max_results
            id="max_results",
        ),
    ],
)
def test_read_gbq_wildcard(
    session: bigframes.Session,
    api_method: str,
    filters,
    table_id: str,
    index_col: Sequence[str],
    columns: Sequence[str],
    max_results: Optional[int],
):
    table_metadata = session.bqclient.get_table(table_id)
    method = getattr(session, api_method)
    df = method(
        table_id,
        filters=filters,
        index_col=index_col,
        columns=columns,
        max_results=max_results,
    )
    num_rows, num_columns = df.shape

    if index_col:
        assert list(df.index.names) == list(index_col)
    else:
        assert df.index.name is None

    expected_columns = (
        columns
        if columns
        else [
            field.name
            for field in table_metadata.schema
            if field.name not in index_col and field.name not in columns
        ]
    )
    assert list(df.columns) == expected_columns
    assert num_rows > 0
    assert num_columns == len(expected_columns)


@pytest.mark.parametrize(
    ("config"),
    [
        {
            "query": {
                "useQueryCache": True,
                "maximumBytesBilled": "1000000000",
                "timeoutMs": 10000,
            }
        },
        pytest.param(
            {"query": {"useQueryCache": True, "timeoutMs": 50}},
            marks=pytest.mark.xfail(
                raises=google.api_core.exceptions.BadRequest,
                reason="Expected failure due to timeout being set too short.",
            ),
        ),
        pytest.param(
            {"query": {"useQueryCache": False, "maximumBytesBilled": "100"}},
            marks=pytest.mark.xfail(
                raises=google.api_core.exceptions.InternalServerError,
                reason="Expected failure when the query exceeds the maximum bytes billed limit.",
            ),
        ),
    ],
)
def test_read_gbq_with_configuration(
    session: bigframes.Session, scalars_table_id: str, config: dict
):
    query = f"""SELECT
                t.float64_col * 2 AS my_floats,
                CONCAT(t.string_col, "_2") AS my_strings,
                t.int64_col > 0 AS my_bools,
            FROM `{scalars_table_id}` AS t
            """

    df = session.read_gbq(query, configuration=config)

    assert df.shape == (9, 3)


def test_read_gbq_with_custom_global_labels(
    session: bigframes.Session, scalars_table_id: str
):
    # Ensure we use thread-local variables to avoid conflicts with parallel tests.
    with bigframes.option_context("compute.extra_query_labels", {}):
        bigframes.options.compute.assign_extra_query_labels(test1=1, test2="abc")
        bigframes.options.compute.extra_query_labels["test3"] = False

        query_job = session.read_gbq(scalars_table_id).query_job

        # No real job created from read_gbq, so we should expect 0 labels
        assert query_job is not None
        assert query_job.labels == {}
    # No labels outside of the option_context.
    assert len(bigframes.options.compute.extra_query_labels) == 0


def test_read_gbq_external_table(session: bigframes.Session):
    # Verify the table is external to ensure it hasn't been altered
    external_table_id = "bigframes-dev.bigframes_tests_sys.parquet_external_table"
    external_table = session.bqclient.get_table(external_table_id)
    assert external_table.table_type == "EXTERNAL"

    df = session.read_gbq(external_table_id)

    assert list(df.columns) == ["idx", "s1", "s2", "s3", "s4", "i1", "f1", "i2", "f2"]
    assert df["i1"].max() == 99


def test_read_gbq_w_json(session):
    sql = """
        SELECT 0 AS id, JSON_OBJECT('boolean', True) AS json_col,
        UNION ALL
        SELECT 1, JSON_OBJECT('int', 100),
        UNION ALL
        SELECT 2, JSON_OBJECT('float', 0.98),
        UNION ALL
        SELECT 3, JSON_OBJECT('string', 'hello world'),
        UNION ALL
        SELECT 4, JSON_OBJECT('array', [8, 9, 10]),
        UNION ALL
        SELECT 5, JSON_OBJECT('null', null),
        UNION ALL
        SELECT 6, JSON_OBJECT('b', 2, 'a', 1),
        UNION ALL
        SELECT
            7,
            JSON_OBJECT(
                'dict',
                JSON_OBJECT(
                    'int', 1,
                    'array', [JSON_OBJECT('foo', 1), JSON_OBJECT('bar', 'hello')]
                )
            ),
    """
    df = session.read_gbq(sql, index_col="id")

    assert df.dtypes["json_col"] == pd.ArrowDtype(db_dtypes.JSONArrowType())

    assert df["json_col"][0] == '{"boolean":true}'
    assert df["json_col"][1] == '{"int":100}'
    assert df["json_col"][2] == '{"float":0.98}'
    assert df["json_col"][3] == '{"string":"hello world"}'
    assert df["json_col"][4] == '{"array":[8,9,10]}'
    assert df["json_col"][5] == '{"null":null}'

    # Verifies JSON strings preserve array order, regardless of dictionary key order.
    assert df["json_col"][6] == '{"a":1,"b":2}'
    assert df["json_col"][7] == '{"dict":{"array":[{"foo":1},{"bar":"hello"}],"int":1}}'


def test_read_gbq_w_json_and_compare_w_pandas_json(session):
    df = session.read_gbq("SELECT JSON_OBJECT('foo', 10, 'bar', TRUE) AS json_col")
    assert df.dtypes["json_col"] == pd.ArrowDtype(db_dtypes.JSONArrowType())

    # These JSON strings are compatible with BigQuery's JSON storage,
    pd_df = pd.DataFrame(
        {"json_col": ['{"bar":true,"foo":10}']},
        dtype=pd.ArrowDtype(db_dtypes.JSONArrowType()),
    )
    pd_df.index = pd_df.index.astype("Int64")
    pd.testing.assert_series_equal(df.dtypes, pd_df.dtypes)
    pd.testing.assert_series_equal(df["json_col"].to_pandas(), pd_df["json_col"])


def test_read_gbq_w_json_in_struct(session):
    """Avoid regressions for internal issue 381148539."""
    sql = """
        SELECT 0 AS id, STRUCT(JSON_OBJECT('boolean', True) AS data, 1 AS number) AS struct_col
        UNION ALL
        SELECT 1, STRUCT(JSON_OBJECT('int', 100), 2),
        UNION ALL
        SELECT 2, STRUCT(JSON_OBJECT('float', 0.98), 3),
        UNION ALL
        SELECT 3, STRUCT(JSON_OBJECT('string', 'hello world'), 4),
        UNION ALL
        SELECT 4, STRUCT(JSON_OBJECT('array', [8, 9, 10]), 5),
        UNION ALL
        SELECT 5, STRUCT(JSON_OBJECT('null', null), 6),
        UNION ALL
        SELECT
            6,
            STRUCT(JSON_OBJECT(
                'dict',
                JSON_OBJECT(
                    'int', 1,
                    'array', [JSON_OBJECT('foo', 1), JSON_OBJECT('bar', 'hello')]
                )
            ), 7),
    """
    df = session.read_gbq(sql, index_col="id")

    assert isinstance(df.dtypes["struct_col"], pd.ArrowDtype)
    assert isinstance(df.dtypes["struct_col"].pyarrow_dtype, pa.StructType)

    data = df["struct_col"].struct.field("data")
    assert data.dtype == pd.ArrowDtype(db_dtypes.JSONArrowType())

    assert data[0] == '{"boolean":true}'
    assert data[1] == '{"int":100}'
    assert data[2] == '{"float":0.98}'
    assert data[3] == '{"string":"hello world"}'
    assert data[4] == '{"array":[8,9,10]}'
    assert data[5] == '{"null":null}'
    assert data[6] == '{"dict":{"array":[{"foo":1},{"bar":"hello"}],"int":1}}'


def test_read_gbq_w_json_in_array(session):
    sql = """
        SELECT
            0 AS id,
            [
                JSON_OBJECT('boolean', True),
                JSON_OBJECT('int', 100),
                JSON_OBJECT('float', 0.98),
                JSON_OBJECT('string', 'hello world'),
                JSON_OBJECT('array', [8, 9, 10]),
                JSON_OBJECT('null', null),
                JSON_OBJECT(
                    'dict',
                    JSON_OBJECT(
                        'int', 1,
                        'array', [JSON_OBJECT('bar', 'hello'), JSON_OBJECT('foo', 1)]
                    )
                )
            ] AS array_col,
    """
    df = session.read_gbq(sql, index_col="id")

    assert isinstance(df.dtypes["array_col"], pd.ArrowDtype)
    assert isinstance(df.dtypes["array_col"].pyarrow_dtype, pa.ListType)

    data = df["array_col"]
    assert data.list.len()[0] == 7
    assert data.list[0].dtype == pd.ArrowDtype(db_dtypes.JSONArrowType())

    assert data[0] == [
        '{"boolean":true}',
        '{"int":100}',
        '{"float":0.98}',
        '{"string":"hello world"}',
        '{"array":[8,9,10]}',
        '{"null":null}',
        '{"dict":{"array":[{"bar":"hello"},{"foo":1}],"int":1}}',
    ]


def test_read_gbq_model(session, penguins_linear_model_name):
    model = session.read_gbq_model(penguins_linear_model_name)
    assert isinstance(model, bigframes.ml.linear_model.LinearRegression)


def test_read_pandas(session, scalars_dfs):
    _, scalars_pandas_df = scalars_dfs

    df = session.read_pandas(scalars_pandas_df)

    result = df.to_pandas()
    expected = scalars_pandas_df

    pd.testing.assert_frame_equal(result, expected)


def test_read_pandas_series(session):

    idx: pd.Index = pd.Index([2, 7, 1, 2, 8], dtype=pd.Int64Dtype())
    pd_series = pd.Series([3, 1, 4, 1, 5], dtype=pd.Int64Dtype(), index=idx)
    bf_series = session.read_pandas(pd_series)

    pd.testing.assert_series_equal(bf_series.to_pandas(), pd_series)


def test_read_pandas_index(session):

    pd_idx: pd.Index = pd.Index([2, 7, 1, 2, 8], dtype=pd.Int64Dtype())
    bf_idx = session.read_pandas(pd_idx)

    pd.testing.assert_index_equal(bf_idx.to_pandas(), pd_idx)


def test_read_pandas_w_unsupported_mixed_dtype(session):
    with pytest.raises(ValueError, match="Could not convert"):
        session.read_pandas(pd.DataFrame({"a": [1, "hello"]}))


def test_read_pandas_inline_respects_location():
    options = bigframes.BigQueryOptions(location="europe-west1")
    session = bigframes.Session(options)

    df = session.read_pandas(pd.DataFrame([[1, 2, 3], [4, 5, 6]]))
    df.to_gbq()

    assert df.query_job is not None

    table = session.bqclient.get_table(df.query_job.destination)
    assert table.location == "europe-west1"


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
    df.to_gbq()
    expected = scalars_pandas_df_index

    result = session_tokyo._executor.execute(
        df._block.expr, use_explicit_destination=True
    )
    assert result.query_job is not None
    assert result.query_job.location == tokyo_location

    assert len(expected) == result.total_rows


@all_write_engines
def test_read_pandas_timedelta_dataframes(session, write_engine):
    pytest.importorskip(
        "pandas",
        minversion="2.0.0",
        reason="old versions don't support local casting to arrow duration",
    )
    pandas_df = pd.DataFrame({"my_col": pd.to_timedelta([1, 2, 3], unit="d")})

    actual_result = session.read_pandas(
        pandas_df, write_engine=write_engine
    ).to_pandas()
    expected_result = pandas_df.astype(bigframes.dtypes.TIMEDELTA_DTYPE)
    expected_result.index = expected_result.index.astype(bigframes.dtypes.INT_DTYPE)

    pd.testing.assert_frame_equal(actual_result, expected_result)


@all_write_engines
def test_read_pandas_timedelta_series(session, write_engine):
    expected_series = pd.Series(pd.to_timedelta([1, 2, 3], unit="d"))

    actual_result = (
        session.read_pandas(expected_series, write_engine=write_engine)
        .to_pandas()
        .astype("timedelta64[ns]")
    )

    pd.testing.assert_series_equal(
        actual_result, expected_series, check_index_type=False
    )


@all_write_engines
def test_read_pandas_timedelta_index(session, write_engine):
    expected_index = pd.to_timedelta(
        [1, 2, 3], unit="d"
    )  # to_timedelta returns an index

    actual_result = (
        session.read_pandas(expected_index, write_engine=write_engine)
        .to_pandas()
        .astype("timedelta64[ns]")
    )

    pd.testing.assert_index_equal(actual_result, expected_index)


@all_write_engines
def test_read_pandas_json_dataframes(session, write_engine):
    json_data = [
        "1",
        None,
        '["1","3","5"]',
        '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}',
    ]
    expected_df = pd.DataFrame(
        {"my_col": pd.Series(json_data, dtype=bigframes.dtypes.JSON_DTYPE)}
    )

    actual_result = session.read_pandas(
        expected_df, write_engine=write_engine
    ).to_pandas()

    pd.testing.assert_frame_equal(actual_result, expected_df, check_index_type=False)


@all_write_engines
def test_read_pandas_json_series(session, write_engine):
    json_data = [
        "1",
        None,
        '[1,"3",null,{"a":null}]',
        '{"a":1,"b":["x","y"],"c":{"x":[],"y":null,"z":false}}',
    ]
    expected_series = pd.Series(json_data, dtype=bigframes.dtypes.JSON_DTYPE)

    actual_result = session.read_pandas(
        expected_series, write_engine=write_engine
    ).to_pandas()
    pd.testing.assert_series_equal(
        actual_result, expected_series, check_index_type=False
    )


@all_write_engines
def test_read_pandas_json_series_w_invalid_json(session, write_engine):
    json_data = [
        "False",  # Should be "false"
    ]
    pd_s = pd.Series(json_data, dtype=bigframes.dtypes.JSON_DTYPE)

    with pytest.raises(json.JSONDecodeError):
        session.read_pandas(pd_s, write_engine=write_engine)


@all_write_engines
def test_read_pandas_json_index(session, write_engine):
    json_data = [
        "1",
        None,
        '["1","3","5"]',
        '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}',
    ]
    expected_index: pd.Index = pd.Index(json_data, dtype=bigframes.dtypes.JSON_DTYPE)
    actual_result = session.read_pandas(
        expected_index, write_engine=write_engine
    ).to_pandas()
    pd.testing.assert_index_equal(actual_result, expected_index)


@pytest.mark.parametrize(
    ("write_engine"),
    [
        pytest.param("bigquery_load"),
    ],
)
def test_read_pandas_w_nested_json_fails(session, write_engine):
    data = [
        [{"json_field": "1"}],
        [{"json_field": None}],
        [{"json_field": '["1","3","5"]'}],
        [{"json_field": '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}'}],
    ]
    # PyArrow currently lacks support for creating structs or lists containing extension types.
    # See issue: https://github.com/apache/arrow/issues/45262
    pa_array = pa.array(data, type=pa.list_(pa.struct([("json_field", pa.string())])))
    pd_s = pd.Series(
        arrays.ArrowExtensionArray(pa_array),  # type: ignore
        dtype=pd.ArrowDtype(
            pa.list_(pa.struct([("json_field", bigframes.dtypes.JSON_ARROW_TYPE)]))
        ),
    )
    with pytest.raises(NotImplementedError, match="Nested JSON types, found in column"):
        session.read_pandas(pd_s, write_engine=write_engine)


@pytest.mark.parametrize(
    ("write_engine"),
    [
        pytest.param("default"),
        pytest.param("bigquery_inline"),
        pytest.param("bigquery_streaming"),
        pytest.param("bigquery_write"),
    ],
)
def test_read_pandas_w_nested_json(session, write_engine):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    data = [
        [{"json_field": "1"}],
        [{"json_field": None}],
        [{"json_field": '["1","3","5"]'}],
        [{"json_field": '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}'}],
    ]
    pa_array = pa.array(data, type=pa.list_(pa.struct([("json_field", pa.string())])))
    pd_s = pd.Series(
        arrays.ArrowExtensionArray(pa_array),  # type: ignore
        dtype=pd.ArrowDtype(
            pa.list_(pa.struct([("json_field", bigframes.dtypes.JSON_ARROW_TYPE)]))
        ),
    )
    bq_s = (
        session.read_pandas(pd_s, write_engine=write_engine)
        .to_pandas()
        .reset_index(drop=True)
    )
    pd.testing.assert_series_equal(bq_s, pd_s)


@pytest.mark.parametrize(
    ("write_engine"),
    [
        pytest.param("default"),
        pytest.param("bigquery_inline"),
        pytest.param("bigquery_load"),
        pytest.param("bigquery_streaming"),
    ],
)
def test_read_pandas_w_nested_invalid_json(session, write_engine):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    data = [
        [{"json_field": "NULL"}],  # Should be "null"
    ]
    pa_array = pa.array(data, type=pa.list_(pa.struct([("json_field", pa.string())])))
    pd_s = pd.Series(
        arrays.ArrowExtensionArray(pa_array),  # type: ignore
        dtype=pd.ArrowDtype(
            pa.list_(pa.struct([("json_field", bigframes.dtypes.JSON_ARROW_TYPE)]))
        ),
    )

    with pytest.raises(json.JSONDecodeError):
        session.read_pandas(pd_s, write_engine=write_engine)


@pytest.mark.parametrize(
    ("write_engine"),
    [
        pytest.param("bigquery_load"),
    ],
)
def test_read_pandas_w_nested_json_index_fails(session, write_engine):
    data = [
        [{"json_field": "1"}],
        [{"json_field": None}],
        [{"json_field": '["1","3","5"]'}],
        [{"json_field": '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}'}],
    ]
    # PyArrow currently lacks support for creating structs or lists containing extension types.
    # See issue: https://github.com/apache/arrow/issues/45262
    pa_array = pa.array(data, type=pa.list_(pa.struct([("json_field", pa.string())])))
    pd_idx: pd.Index = pd.Index(
        arrays.ArrowExtensionArray(pa_array),  # type: ignore
        dtype=pd.ArrowDtype(
            pa.list_(pa.struct([("json_field", bigframes.dtypes.JSON_ARROW_TYPE)]))
        ),
    )
    with pytest.raises(NotImplementedError, match="Nested JSON types, found in"):
        session.read_pandas(pd_idx, write_engine=write_engine)


@pytest.mark.parametrize(
    ("write_engine"),
    [
        pytest.param("default"),
        pytest.param("bigquery_inline"),
        pytest.param("bigquery_streaming"),
        pytest.param("bigquery_write"),
    ],
)
def test_read_pandas_w_nested_json_index(session, write_engine):
    # TODO: supply a reason why this isn't compatible with pandas 1.x
    pytest.importorskip("pandas", minversion="2.0.0")
    data = [
        [{"json_field": "1"}],
        [{"json_field": None}],
        [{"json_field": '["1","3","5"]'}],
        [{"json_field": '{"a":1,"b":["x","y"],"c":{"x":[],"z":false}}'}],
    ]
    pa_array = pa.array(data, type=pa.list_(pa.struct([("name", pa.string())])))
    pd_idx: pd.Index = pd.Index(
        arrays.ArrowExtensionArray(pa_array),  # type: ignore
        dtype=pd.ArrowDtype(
            pa.list_(pa.struct([("name", bigframes.dtypes.JSON_ARROW_TYPE)]))
        ),
    )
    bq_idx = session.read_pandas(pd_idx, write_engine=write_engine).to_pandas()
    pd.testing.assert_index_equal(bq_idx, pd_idx)


@all_write_engines
def test_read_csv_for_gcs_file_w_write_engine(session, df_and_gcs_csv, write_engine):
    scalars_df, path = df_and_gcs_csv

    # Compares results for pandas and bigframes engines
    pd_df = session.read_csv(
        path,
        index_col="rowindex",
        write_engine=write_engine,
        dtype=scalars_df.dtypes.to_dict(),
    )
    pd.testing.assert_frame_equal(pd_df.to_pandas(), scalars_df.to_pandas())

    if write_engine in ("default", "bigquery_load"):
        bf_df = session.read_csv(
            path, engine="bigquery", index_col="rowindex", write_engine=write_engine
        )
        pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


@pytest.mark.parametrize(
    "sep",
    [
        pytest.param(",", id="default_sep"),
        pytest.param("\t", id="custom_sep"),
    ],
)
def test_read_csv_for_local_file_w_sep(session, df_and_local_csv, sep):
    scalars_df, _ = df_and_local_csv

    with tempfile.TemporaryDirectory() as dir:
        # Prepares local CSV file for reading
        path = dir + "/test_read_csv_for_local_file_w_sep.csv"
        scalars_df.to_csv(path, index=True, sep=sep)

        # Compares results for pandas and bigframes engines
        with open(path, "rb") as buffer:
            bf_df = session.read_csv(
                buffer, engine="bigquery", index_col="rowindex", sep=sep
            )
        with open(path, "rb") as buffer:
            # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
            pd_df = session.read_csv(
                buffer, index_col="rowindex", sep=sep, dtype=scalars_df.dtypes.to_dict()
            )
        pd.testing.assert_frame_equal(bf_df.to_pandas(), scalars_df.to_pandas())
        pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


@pytest.mark.parametrize(
    "index_col",
    [
        pytest.param(None, id="none"),
        pytest.param(False, id="false"),
        pytest.param([], id="empty_list"),
    ],
)
def test_read_csv_for_index_col_w_false(session, df_and_local_csv, index_col):
    # Compares results for pandas and bigframes engines
    scalars_df, path = df_and_local_csv
    with open(path, "rb") as buffer:
        bf_df = session.read_csv(
            buffer,
            engine="bigquery",
            index_col=index_col,
        )
    with open(path, "rb") as buffer:
        # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
        pd_df = session.read_csv(
            buffer, index_col=index_col, dtype=scalars_df.dtypes.to_dict()
        )

    assert bf_df.shape == pd_df.shape

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index("rowindex").sort_index()
    pd_df = pd_df.set_index("rowindex")
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


@pytest.mark.parametrize(
    "index_col",
    [
        pytest.param("rowindex", id="single_str"),
        pytest.param(["rowindex", "bool_col"], id="multi_str"),
        pytest.param(0, id="single_int"),
        pytest.param([0, 2], id="multi_int"),
        pytest.param([0, "bool_col"], id="mix_types"),
    ],
)
def test_read_csv_for_index_col(session, df_and_gcs_csv, index_col):
    scalars_pandas_df, path = df_and_gcs_csv
    bf_df = session.read_csv(path, engine="bigquery", index_col=index_col)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(
        path, index_col=index_col, dtype=scalars_pandas_df.dtypes.to_dict()
    )

    assert bf_df.shape == pd_df.shape
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


@pytest.mark.parametrize(
    ("index_col", "error_type", "error_msg"),
    [
        pytest.param(
            True, ValueError, "The value of index_col couldn't be 'True'", id="true"
        ),
        pytest.param(100, ValueError, "out of bounds", id="single_int"),
        pytest.param([0, 200], ValueError, "out of bounds", id="multi_int"),
        pytest.param(
            [0.1], TypeError, "it must contain either strings", id="invalid_iterable"
        ),
        pytest.param(
            3.14, TypeError, "Unsupported type for index_col", id="unsupported_type"
        ),
    ],
)
def test_read_csv_raises_error_for_invalid_index_col(
    session, df_and_gcs_csv, index_col, error_type, error_msg
):
    _, path = df_and_gcs_csv
    with pytest.raises(
        error_type,
        match=error_msg,
    ):
        session.read_csv(path, engine="bigquery", index_col=index_col)


def test_read_csv_for_names(session, df_and_gcs_csv_for_two_columns):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["a", "b", "c"]
    bf_df = session.read_csv(path, engine="bigquery", names=names)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(path, names=names, dtype=bf_df.dtypes.to_dict())

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index(names[0]).sort_index()
    pd_df = pd_df.set_index(names[0])
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_for_names_more_than_columns_can_raise_error(
    session, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns
    names = ["a", "b", "c", "d"]
    with pytest.raises(
        ValueError,
        match="Too many columns specified: expected 3 and found 4",
    ):
        session.read_csv(path, engine="bigquery", names=names)


def test_read_csv_for_names_less_than_columns(session, df_and_gcs_csv_for_two_columns):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["b", "c"]
    bf_df = session.read_csv(path, engine="bigquery", names=names)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(path, names=names, dtype=bf_df.dtypes.to_dict())

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # Pandas's index name is None, while BigFrames's index name is "rowindex".
    pd_df.index.name = "rowindex"
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_for_names_less_than_columns_raise_error_when_index_col_set(
    session, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["b", "c"]
    with pytest.raises(
        KeyError,
        match="ensure the number of `names` matches the number of columns in your data.",
    ):
        session.read_csv(path, engine="bigquery", names=names, index_col="rowindex")


@pytest.mark.parametrize(
    "index_col",
    [
        pytest.param("a", id="single_str"),
        pytest.param(["a", "b"], id="multi_str"),
        pytest.param(0, id="single_int"),
    ],
)
def test_read_csv_for_names_and_index_col(
    session, df_and_gcs_csv_for_two_columns, index_col
):
    _, path = df_and_gcs_csv_for_two_columns
    names = ["a", "b", "c"]
    bf_df = session.read_csv(path, engine="bigquery", index_col=index_col, names=names)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(
        path, index_col=index_col, names=names, dtype=bf_df.dtypes.to_dict()
    )

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()
    pd.testing.assert_frame_equal(
        bf_df.to_pandas(), pd_df.to_pandas(), check_index_type=False
    )


@pytest.mark.parametrize(
    "usecols",
    [
        pytest.param(["a", "b", "c"], id="same"),
        pytest.param(["a", "c"], id="less_than_names"),
    ],
)
def test_read_csv_for_names_and_usecols(
    session, usecols, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["a", "b", "c"]
    bf_df = session.read_csv(path, engine="bigquery", names=names, usecols=usecols)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(
        path, names=names, usecols=usecols, dtype=bf_df.dtypes.to_dict()
    )

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index(names[0]).sort_index()
    pd_df = pd_df.set_index(names[0])
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_for_names_and_invalid_usecols(
    session, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["a", "b", "c"]
    usecols = ["a", "X"]
    with pytest.raises(
        ValueError,
        match=re.escape("Column 'X' is not found. "),
    ):
        session.read_csv(path, engine="bigquery", names=names, usecols=usecols)


@pytest.mark.parametrize(
    ("usecols", "index_col"),
    [
        pytest.param(["a", "b", "c"], "a", id="same"),
        pytest.param(["a", "b", "c"], ["a", "b"], id="same_two_index"),
        pytest.param(["a", "c"], 0, id="less_than_names"),
    ],
)
def test_read_csv_for_names_and_usecols_and_indexcol(
    session, usecols, index_col, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["a", "b", "c"]
    bf_df = session.read_csv(
        path, engine="bigquery", names=names, usecols=usecols, index_col=index_col
    )

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(
        path,
        names=names,
        usecols=usecols,
        index_col=index_col,
        dtype=bf_df.reset_index().dtypes.to_dict(),
    )

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_for_names_less_than_columns_and_same_usecols(
    session, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns
    names = ["a", "c"]
    usecols = ["a", "c"]
    bf_df = session.read_csv(path, engine="bigquery", names=names, usecols=usecols)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(
        path, names=names, usecols=usecols, dtype=bf_df.dtypes.to_dict()
    )

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index(names[0]).sort_index()
    pd_df = pd_df.set_index(names[0])
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_for_names_less_than_columns_and_mismatched_usecols(
    session, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns
    names = ["a", "b"]
    usecols = ["a"]
    with pytest.raises(
        ValueError,
        match=re.escape("Number of passed names did not match number"),
    ):
        session.read_csv(path, engine="bigquery", names=names, usecols=usecols)


def test_read_csv_for_names_less_than_columns_and_different_usecols(
    session, df_and_gcs_csv_for_two_columns
):
    _, path = df_and_gcs_csv_for_two_columns
    names = ["a", "b"]
    usecols = ["a", "c"]
    with pytest.raises(
        ValueError,
        match=re.escape("Usecols do not match columns"),
    ):
        session.read_csv(path, engine="bigquery", names=names, usecols=usecols)


def test_read_csv_for_dtype(session, df_and_gcs_csv_for_two_columns):
    _, path = df_and_gcs_csv_for_two_columns

    dtype = {"bool_col": pd.BooleanDtype(), "int64_col": pd.Float64Dtype()}
    bf_df = session.read_csv(path, engine="bigquery", dtype=dtype)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(path, dtype=dtype)

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index("rowindex").sort_index()
    pd_df = pd_df.set_index("rowindex")
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_for_dtype_w_names(session, df_and_gcs_csv_for_two_columns):
    _, path = df_and_gcs_csv_for_two_columns

    names = ["a", "b", "c"]
    dtype = {"b": pd.BooleanDtype(), "c": pd.Float64Dtype()}
    bf_df = session.read_csv(path, engine="bigquery", names=names, dtype=dtype)

    # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
    pd_df = session.read_csv(path, names=names, dtype=dtype)

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index("a").sort_index()
    pd_df = pd_df.set_index("a")
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


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
    read_path = utils.get_first_file_from_wildcard(path)
    scalars_df_index.to_csv(path)
    with pytest.raises(NotImplementedError, match=match):
        session.read_csv(read_path, **kwargs)


@pytest.mark.parametrize(
    "header",
    [0, 1, 5],
)
def test_read_csv_for_gcs_file_w_header(session, df_and_gcs_csv, header):
    # Compares results for pandas and bigframes engines
    scalars_df, path = df_and_gcs_csv
    bf_df = session.read_csv(path, engine="bigquery", index_col=False, header=header)
    pd_df = session.read_csv(
        path, index_col=False, header=header, dtype=scalars_df.dtypes.to_dict()
    )

    # b/408461403: workaround the issue where the slice does not work for DataFrame.
    expected_df = session.read_pandas(scalars_df.to_pandas()[header:])

    assert pd_df.shape[0] == expected_df.shape[0]
    assert bf_df.shape[0] == pd_df.shape[0]

    # We use a default index because of index_col=False, so the previous index
    # column is just loaded as a column.
    assert len(pd_df.columns) == len(expected_df.columns) + 1
    assert len(bf_df.columns) == len(pd_df.columns)

    # When `header > 0`, pandas and BigFrames may handle column naming differently.
    # Pandas uses the literal content of the specified header row for column names,
    # regardless of what it is. BigQuery, however, might generate default names based
    # on data type (e.g.,bool_field_0,string_field_1, etc.).
    if header == 0:
        # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
        # (b/280889935) or guarantee row ordering.
        bf_df = bf_df.set_index("rowindex").sort_index()
        pd_df = pd_df.set_index("rowindex")
        pd.testing.assert_frame_equal(bf_df.to_pandas(), scalars_df.to_pandas())
        pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_w_usecols(session, df_and_local_csv):
    # Compares results for pandas and bigframes engines
    scalars_df, path = df_and_local_csv
    usecols = ["rowindex", "bool_col"]
    with open(path, "rb") as buffer:
        bf_df = session.read_csv(
            buffer,
            engine="bigquery",
            usecols=usecols,
        )
    with open(path, "rb") as buffer:
        # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
        pd_df = session.read_csv(
            buffer,
            usecols=usecols,
            dtype=scalars_df[["bool_col"]].dtypes.to_dict(),
        )

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    # BigFrames requires `sort_index()` because BigQuery doesn't preserve row IDs
    # (b/280889935) or guarantee row ordering.
    bf_df = bf_df.set_index("rowindex").sort_index()
    pd_df = pd_df.set_index("rowindex")
    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_w_usecols_and_indexcol(session, df_and_local_csv):
    # Compares results for pandas and bigframes engines
    scalars_df, path = df_and_local_csv
    usecols = ["rowindex", "bool_col"]
    with open(path, "rb") as buffer:
        bf_df = session.read_csv(
            buffer,
            engine="bigquery",
            usecols=usecols,
            index_col="rowindex",
        )
    with open(path, "rb") as buffer:
        # Convert default pandas dtypes to match BigQuery DataFrames dtypes.
        pd_df = session.read_csv(
            buffer,
            usecols=usecols,
            index_col="rowindex",
            dtype=scalars_df[["bool_col"]].dtypes.to_dict(),
        )

    assert bf_df.shape == pd_df.shape
    assert bf_df.columns.tolist() == pd_df.columns.tolist()

    pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


def test_read_csv_w_indexcol_not_in_usecols(session, df_and_local_csv):
    _, path = df_and_local_csv
    with open(path, "rb") as buffer:
        with pytest.raises(
            ValueError,
            match=re.escape("The specified index column(s) were not found"),
        ):
            session.read_csv(
                buffer,
                engine="bigquery",
                usecols=["bool_col"],
                index_col="rowindex",
            )


@pytest.mark.parametrize(
    "engine",
    [
        pytest.param(
            "bigquery",
            id="bq_engine",
            marks=pytest.mark.xfail(
                raises=NotImplementedError,
            ),
        ),
        pytest.param(None, id="default_engine"),
    ],
)
def test_read_csv_for_others_files(session, engine):
    uri = "https://raw.githubusercontent.com/googleapis/python-bigquery-dataframes/main/tests/data/people.csv"
    df = session.read_csv(uri, engine=engine)
    assert len(df.columns) == 3


def test_read_csv_local_w_encoding(session, penguins_pandas_df_default_index):
    with tempfile.TemporaryDirectory() as dir:
        path = dir + "/test_read_csv_local_w_encoding.csv"
        # Using the pandas to_csv method because the BQ one does not support local write.
        penguins_pandas_df_default_index.index.name = "rowindex"
        penguins_pandas_df_default_index.to_csv(path, index=True, encoding="ISO-8859-1")

        # File can only be read using the same character encoding as when written.
        pd_df = session.read_csv(
            path,
            index_col="rowindex",
            encoding="ISO-8859-1",
            dtype=penguins_pandas_df_default_index.dtypes.to_dict(),
        )

        bf_df = session.read_csv(
            path, engine="bigquery", index_col="rowindex", encoding="ISO-8859-1"
        )
        pd.testing.assert_frame_equal(
            bf_df.to_pandas(), penguins_pandas_df_default_index
        )
        pd.testing.assert_frame_equal(bf_df.to_pandas(), pd_df.to_pandas())


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


@pytest.mark.parametrize(
    ("engine", "filename"),
    (
        pytest.param(
            "auto",
            "000000000000.parquet",
            id="auto",
        ),
        pytest.param(
            "pyarrow",
            "000000000000.parquet",
            id="pyarrow",
        ),
        pytest.param(
            "bigquery",
            "000000000000.parquet",
            id="bigquery",
        ),
        pytest.param(
            "bigquery",
            "*.parquet",
            id="bigquery_wildcard",
        ),
        pytest.param(
            "auto",
            "*.parquet",
            id="auto_wildcard",
            marks=pytest.mark.xfail(
                raises=ValueError,
            ),
        ),
    ),
)
def test_read_parquet_gcs(
    session: bigframes.Session, scalars_dfs, gcs_folder, engine, filename
):
    scalars_df, _ = scalars_dfs
    # Include wildcard so that multiple files can be written/read if > 1 GB.
    # https://cloud.google.com/bigquery/docs/exporting-data#exporting_data_into_one_or_more_files
    write_path = gcs_folder + test_read_parquet_gcs.__name__ + "*.parquet"
    read_path = gcs_folder + test_read_parquet_gcs.__name__ + filename

    df_in: bigframes.dataframe.DataFrame = scalars_df.copy()
    # GEOGRAPHY not supported in parquet export.
    df_in = df_in.drop(columns="geography_col")
    # Make sure we can also serialize the order.
    df_write = df_in.reset_index(drop=False)
    df_write.index.name = f"ordering_id_{random.randrange(1_000_000)}"
    df_write.to_parquet(write_path, index=True)

    df_out = (
        session.read_parquet(read_path, engine=engine)
        # Restore order.
        .set_index(df_write.index.name).sort_index()
        # Restore index.
        .set_index(typing.cast(str, df_in.index.name))
    )

    # DATETIME gets loaded as TIMESTAMP in parquet. See:
    # https://cloud.google.com/bigquery/docs/exporting-data#parquet_export_details
    df_out = df_out.assign(
        datetime_col=df_out["datetime_col"].astype("timestamp[us][pyarrow]"),
        timestamp_col=df_out["timestamp_col"].astype("timestamp[us, tz=UTC][pyarrow]"),
        duration_col=df_out["duration_col"].astype("duration[us][pyarrow]"),
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
        session.read_parquet(path, engine="bigquery")
        # Restore order.
        .set_index(df_write.index.name).sort_index()
        # Restore index.
        .set_index(typing.cast(str, df_in.index.name))
    )

    # DATETIME gets loaded as TIMESTAMP in parquet. See:
    # https://cloud.google.com/bigquery/docs/exporting-data#parquet_export_details
    df_out = df_out.assign(
        datetime_col=df_out["datetime_col"].astype("timestamp[us][pyarrow]"),
        duration_col=df_out["duration_col"].astype("duration[us][pyarrow]"),
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
    read_path = utils.get_first_file_from_wildcard(path)
    scalars_df.to_json(path, index=False, lines=True, orient="records")
    df = session.read_json(read_path, lines=True, orient="records", engine="bigquery")

    # The auto detects of BigQuery load job does not preserve any ordering of columns for json.
    pd.testing.assert_index_equal(
        df.columns.sort_values(), scalars_df.columns.sort_values()
    )

    # The auto detects of BigQuery load job have restrictions to detect the bytes,
    # datetime, numeric and geometry types, so they're skipped here.
    df = df.drop(
        columns=[
            "bytes_col",
            "datetime_col",
            "numeric_col",
            "geography_col",
            "duration_col",
        ]
    )
    scalars_df = scalars_df.drop(
        columns=[
            "bytes_col",
            "datetime_col",
            "numeric_col",
            "geography_col",
            "duration_col",
        ]
    )
    assert df.shape[0] == scalars_df.shape[0]
    pd.testing.assert_series_equal(
        df.dtypes.sort_index(), scalars_df.dtypes.sort_index()
    )


def test_read_json_gcs_default_engine(session, scalars_dfs, gcs_folder):
    scalars_df, _ = scalars_dfs
    path = gcs_folder + "test_read_json_gcs_default_engine_w_index*.json"
    read_path = utils.get_first_file_from_wildcard(path)
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
    df = df.drop(columns=["bytes_col", "numeric_col", "geography_col", "duration_col"])
    scalars_df = scalars_df.drop(
        columns=["bytes_col", "numeric_col", "geography_col", "duration_col"]
    )

    # pandas read_json does not respect the dtype overrides for these columns
    df = df.drop(columns=["date_col", "datetime_col", "time_col"])
    scalars_df = scalars_df.drop(columns=["date_col", "datetime_col", "time_col"])

    assert df.shape[0] == scalars_df.shape[0]
    pd.testing.assert_series_equal(df.dtypes, scalars_df.dtypes)


@pytest.mark.parametrize(
    ("query_or_table", "index_col", "columns"),
    [
        pytest.param(
            "{scalars_table_id}",
            ("int64_col", "string_col", "int64_col"),
            ("float64_col", "bool_col"),
            id="table_input_index_col_dup",
            marks=pytest.mark.xfail(
                raises=ValueError,
                reason="ValueError: Duplicate names within 'index_col'.",
                strict=True,
            ),
        ),
        pytest.param(
            """SELECT int64_col, string_col, float64_col, bool_col
               FROM `{scalars_table_id}`""",
            ("int64_col",),
            ("string_col", "float64_col", "string_col"),
            id="query_input_columns_dup",
            marks=pytest.mark.xfail(
                raises=ValueError,
                reason="ValueError: Duplicate names within 'columns'.",
                strict=True,
            ),
        ),
        pytest.param(
            "{scalars_table_id}",
            ("int64_col", "string_col"),
            ("float64_col", "string_col", "bool_col"),
            id="table_input_cross_dup",
            marks=pytest.mark.xfail(
                raises=ValueError,
                reason="ValueError: Overlap between 'index_col' and 'columns'.",
                strict=True,
            ),
        ),
    ],
)
def test_read_gbq_duplicate_columns_xfail(
    session: bigframes.Session,
    scalars_table_id: str,
    query_or_table: str,
    index_col: tuple,
    columns: tuple,
):
    session.read_gbq(
        query_or_table.format(scalars_table_id=scalars_table_id),
        index_col=index_col,
        columns=columns,
    )


def test_read_gbq_with_table_ref_dry_run(scalars_table_id, session):
    result = session.read_gbq(scalars_table_id, dry_run=True)

    assert isinstance(result, pd.Series)
    _assert_table_dry_run_stats_are_valid(result)


def test_read_gbq_with_query_dry_run(scalars_table_id, session):
    query = f"SELECT * FROM {scalars_table_id} LIMIT 10;"
    result = session.read_gbq(query, dry_run=True)

    assert isinstance(result, pd.Series)
    _assert_query_dry_run_stats_are_valid(result)


def test_read_gbq_dry_run_with_column_and_index(scalars_table_id, session):
    query = f"SELECT * FROM {scalars_table_id} LIMIT 10;"
    result = session.read_gbq(
        query, dry_run=True, columns=["int64_col", "float64_col"], index_col="int64_too"
    )

    assert isinstance(result, pd.Series)
    _assert_query_dry_run_stats_are_valid(result)
    assert result["columnCount"] == 2
    assert result["columnDtypes"] == {
        "int64_col": pd.Int64Dtype(),
        "float64_col": pd.Float64Dtype(),
    }
    assert result["indexLevel"] == 1
    assert result["indexDtypes"] == [pd.Int64Dtype()]


def test_read_gbq_table_dry_run(scalars_table_id, session):
    result = session.read_gbq_table(scalars_table_id, dry_run=True)

    assert isinstance(result, pd.Series)
    _assert_table_dry_run_stats_are_valid(result)


def test_read_gbq_table_dry_run_with_max_results(scalars_table_id, session):
    result = session.read_gbq_table(scalars_table_id, dry_run=True, max_results=100)

    assert isinstance(result, pd.Series)
    _assert_query_dry_run_stats_are_valid(result)


def test_read_gbq_query_dry_run(scalars_table_id, session):
    query = f"SELECT * FROM {scalars_table_id} LIMIT 10;"
    result = session.read_gbq_query(query, dry_run=True)

    assert isinstance(result, pd.Series)
    _assert_query_dry_run_stats_are_valid(result)


def _assert_query_dry_run_stats_are_valid(result: pd.Series):
    expected_index = pd.Index(
        [
            "columnCount",
            "columnDtypes",
            "indexLevel",
            "indexDtypes",
            "bigquerySchema",
            "projectId",
            "location",
            "jobType",
            "dispatchedSql",
            "destinationTable",
            "useLegacySql",
            "referencedTables",
            "totalBytesProcessed",
            "cacheHit",
            "statementType",
            "creationTime",
        ]
    )

    pd.testing.assert_index_equal(result.index, expected_index)
    assert result["columnCount"] + result["indexLevel"] > 0


def _assert_table_dry_run_stats_are_valid(result: pd.Series):
    expected_index = pd.Index(
        [
            "isQuery",
            "columnCount",
            "columnDtypes",
            "bigquerySchema",
            "numBytes",
            "numRows",
            "location",
            "type",
            "creationTime",
            "lastModifiedTime",
        ]
    )

    pd.testing.assert_index_equal(result.index, expected_index)
    assert result["columnCount"] == len(result["columnDtypes"])
