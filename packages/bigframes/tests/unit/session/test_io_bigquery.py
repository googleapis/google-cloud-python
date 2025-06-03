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

import datetime
import re
from typing import Iterable, Optional
from unittest import mock

import google.cloud.bigquery as bigquery
import pytest

import bigframes
from bigframes.core import log_adapter
import bigframes.pandas as bpd
import bigframes.session._io.bigquery as io_bq
from bigframes.testing import mocks


@pytest.fixture(scope="function")
def mock_bq_client():
    mock_client = mock.create_autospec(bigquery.Client)
    mock_query_job = mock.create_autospec(bigquery.QueryJob)
    mock_row_iterator = mock.create_autospec(bigquery.table.RowIterator)

    mock_query_job.result.return_value = mock_row_iterator

    mock_destination = bigquery.DatasetReference(
        project="mock_project", dataset_id="mock_dataset"
    )
    mock_query_job.destination = mock_destination

    mock_client.query.return_value = mock_query_job

    return mock_client


def test_create_job_configs_labels_is_none():
    api_methods = ["agg", "series-mode"]
    labels = io_bq.create_job_configs_labels(
        job_configs_labels=None, api_methods=api_methods
    )
    expected_dict = {"bigframes-api": "agg", "recent-bigframes-api-0": "series-mode"}
    assert labels is not None
    assert labels == expected_dict


def test_create_job_configs_labels_always_includes_bigframes_api():
    labels = io_bq.create_job_configs_labels(None, [])
    assert labels == {
        "bigframes-api": "unknown",
    }


def test_create_job_configs_labels_includes_extra_query_labels():
    user_labels = {"my-label-1": "my-value-1", "my-label-2": "my-value-2"}

    with bigframes.option_context("compute.extra_query_labels", user_labels):
        labels = io_bq.create_job_configs_labels(None, [])
        assert labels == {
            "my-label-1": "my-value-1",
            "my-label-2": "my-value-2",
            "bigframes-api": "unknown",
        }


def test_create_job_configs_labels_length_limit_not_met():
    cur_labels = {
        "source": "bigquery-dataframes-temp",
    }
    api_methods = ["agg", "series-mode"]
    labels = io_bq.create_job_configs_labels(
        job_configs_labels=cur_labels, api_methods=api_methods
    )
    expected_dict = {
        "source": "bigquery-dataframes-temp",
        "bigframes-api": "agg",
        "recent-bigframes-api-0": "series-mode",
    }
    assert labels is not None
    assert len(labels) == 3
    assert labels == expected_dict


def test_create_job_configs_labels_log_adaptor_call_method_under_length_limit():
    log_adapter.get_and_reset_api_methods()
    cur_labels = {
        "source": "bigquery-dataframes-temp",
    }
    df = bpd.DataFrame(
        {"col1": [1, 2], "col2": [3, 4]}, session=mocks.create_bigquery_session()
    )
    # Test running two methods
    df.head()
    df.max()
    df.columns
    api_methods = log_adapter._api_methods

    labels = io_bq.create_job_configs_labels(
        job_configs_labels=cur_labels, api_methods=api_methods
    )
    expected_dict = {
        "source": "bigquery-dataframes-temp",
        "bigframes-api": "dataframe-columns",
        "recent-bigframes-api-0": "dataframe-max",
        "recent-bigframes-api-1": "dataframe-head",
        "recent-bigframes-api-2": "dataframe-__init__",
    }
    assert labels == expected_dict


def test_create_job_configs_labels_length_limit_met_and_labels_is_none():
    log_adapter.get_and_reset_api_methods()
    df = bpd.DataFrame(
        {"col1": [1, 2], "col2": [3, 4]}, session=mocks.create_bigquery_session()
    )
    # Test running methods more than the labels' length limit
    for i in range(100):
        df.head()
    api_methods = log_adapter._api_methods

    labels = io_bq.create_job_configs_labels(
        job_configs_labels=None, api_methods=api_methods
    )
    assert labels is not None
    assert len(labels) == log_adapter.MAX_LABELS_COUNT
    assert "dataframe-head" in labels.values()


def test_create_job_configs_labels_length_limit_met():
    log_adapter.get_and_reset_api_methods()
    cur_labels = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
    }
    for i in range(53):
        key = f"bigframes-api-test-{i}"
        value = f"test{i}"
        cur_labels[key] = value
    # If cur_labels length is 62, we can only add one label from api_methods
    df = bpd.DataFrame(
        {"col1": [1, 2], "col2": [3, 4]}, session=mocks.create_bigquery_session()
    )
    # Test running two methods
    df.head()
    df.max()
    api_methods = log_adapter._api_methods

    labels = io_bq.create_job_configs_labels(
        job_configs_labels=cur_labels, api_methods=api_methods
    )
    assert labels is not None
    assert len(labels) == 56
    assert "dataframe-max" in labels.values()
    assert "dataframe-head" not in labels.values()
    assert "bigframes-api" in labels.keys()
    assert "source" in labels.keys()


def test_add_and_trim_labels_length_limit_met():
    log_adapter.get_and_reset_api_methods()
    cur_labels = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
    }
    for i in range(10):
        key = f"bigframes-api-test-{i}"
        value = f"test{i}"
        cur_labels[key] = value

    df = bpd.DataFrame(
        {"col1": [1, 2], "col2": [3, 4]}, session=mocks.create_bigquery_session()
    )

    job_config = bigquery.job.QueryJobConfig()
    job_config.labels = cur_labels

    df.max()
    for _ in range(52):
        df.head()

    io_bq.add_and_trim_labels(job_config=job_config)
    assert job_config.labels is not None
    assert len(job_config.labels) == 56
    assert "dataframe-max" not in job_config.labels.values()
    assert "dataframe-head" in job_config.labels.values()
    assert "bigframes-api" in job_config.labels.keys()
    assert "source" in job_config.labels.keys()


@pytest.mark.parametrize(
    ("timeout", "api_name"),
    [(None, None), (30.0, "test_api")],
)
def test_start_query_with_client_labels_length_limit_met(
    mock_bq_client: bigquery.Client, timeout: Optional[float], api_name
):
    sql = "select * from abc"
    cur_labels = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
    }
    for i in range(10):
        key = f"bigframes-api-test-{i}"
        value = f"test{i}"
        cur_labels[key] = value

    df = bpd.DataFrame(
        {"col1": [1, 2], "col2": [3, 4]}, session=mocks.create_bigquery_session()
    )

    job_config = bigquery.job.QueryJobConfig()
    job_config.labels = cur_labels

    df.max()
    for _ in range(52):
        df.head()

    io_bq.start_query_with_client(
        mock_bq_client,
        sql,
        job_config=job_config,
        location=None,
        project=None,
        timeout=timeout,
        metrics=None,
        query_with_job=True,
    )

    assert job_config.labels is not None
    assert len(job_config.labels) == 56
    assert "dataframe-max" not in job_config.labels.values()
    assert "dataframe-head" in job_config.labels.values()
    assert "bigframes-api" in job_config.labels.keys()
    assert "source" in job_config.labels.keys()


def test_create_temp_table_default_expiration():
    """Make sure the created table has an expiration."""
    expiration = datetime.datetime(
        2023, 11, 2, 13, 44, 55, 678901, datetime.timezone.utc
    )

    session = mocks.create_bigquery_session()
    table_ref = bigquery.TableReference.from_string(
        "test-project.test_dataset.bqdf_new_random_table"
    )
    bigframes.session._io.bigquery.create_temp_table(
        session.bqclient, table_ref, expiration
    )

    session.bqclient.create_table.assert_called_once()
    call_args = session.bqclient.create_table.call_args
    table = call_args.args[0]
    assert table.project == "test-project"
    assert table.dataset_id == "test_dataset"
    assert table.table_id.startswith("bqdf")
    assert (
        (expiration - datetime.timedelta(minutes=1))
        < table.expires
        < (expiration + datetime.timedelta(minutes=1))
    )


@pytest.mark.parametrize(
    ("schema", "expected"),
    (
        (
            [bigquery.SchemaField("My Column", "INTEGER")],
            "`My Column` INT64",
        ),
        (
            [
                bigquery.SchemaField("My Column", "INTEGER"),
                bigquery.SchemaField("Float Column", "FLOAT"),
                bigquery.SchemaField("Bool Column", "BOOLEAN"),
            ],
            "`My Column` INT64, `Float Column` FLOAT64, `Bool Column` BOOL",
        ),
        (
            [
                bigquery.SchemaField("My Column", "INTEGER", mode="REPEATED"),
                bigquery.SchemaField("Float Column", "FLOAT", mode="REPEATED"),
                bigquery.SchemaField("Bool Column", "BOOLEAN", mode="REPEATED"),
            ],
            "`My Column` ARRAY<INT64>, `Float Column` ARRAY<FLOAT64>, `Bool Column` ARRAY<BOOL>",
        ),
        (
            [
                bigquery.SchemaField(
                    "My Column",
                    "RECORD",
                    mode="REPEATED",
                    fields=(
                        bigquery.SchemaField("Float Column", "FLOAT", mode="REPEATED"),
                        bigquery.SchemaField("Bool Column", "BOOLEAN", mode="REPEATED"),
                        bigquery.SchemaField(
                            "Nested Column",
                            "RECORD",
                            fields=(bigquery.SchemaField("Int Column", "INTEGER"),),
                        ),
                    ),
                ),
            ],
            (
                "`My Column` ARRAY<STRUCT<"
                + "`Float Column` ARRAY<FLOAT64>,"
                + " `Bool Column` ARRAY<BOOL>,"
                + " `Nested Column` STRUCT<`Int Column` INT64>>>"
            ),
        ),
    ),
)
def test_bq_schema_to_sql(schema: Iterable[bigquery.SchemaField], expected: str):
    sql = io_bq.bq_schema_to_sql(schema)
    assert sql == expected


@pytest.mark.parametrize(
    (
        "query_or_table",
        "columns",
        "filters",
        "max_results",
        "time_travel_timestamp",
        "expected_output",
    ),
    [
        pytest.param(
            "test_table",
            ["row_index", "string_col"],
            [
                (("rowindex", "not in", [0, 6]),),
                (("string_col", "in", ["Hello, World!", "こんにちは"]),),
            ],
            123,  # max_results,
            datetime.datetime(
                2024, 5, 14, 12, 42, 36, 125125, tzinfo=datetime.timezone.utc
            ),
            (
                "SELECT `row_index`, `string_col` FROM `test_table` "
                "FOR SYSTEM_TIME AS OF TIMESTAMP('2024-05-14T12:42:36.125125+00:00') "
                "WHERE `rowindex` NOT IN (0, 6) OR `string_col` IN ('Hello, World!', "
                "'こんにちは') LIMIT 123"
            ),
            id="table-all_params-filter_or_operation",
        ),
        pytest.param(
            (
                """SELECT
                    rowindex,
                    string_col,
                FROM `test_table` AS t
                """
            ),
            ["rowindex", "string_col"],
            [
                ("rowindex", "<", 4),
                ("string_col", "==", "Hello, World!"),
            ],
            123,  # max_results,
            datetime.datetime(
                2024, 5, 14, 12, 42, 36, 125125, tzinfo=datetime.timezone.utc
            ),
            (
                """SELECT `rowindex`, `string_col` FROM (SELECT
                    rowindex,
                    string_col,
                FROM `test_table` AS t
                ) """
                "FOR SYSTEM_TIME AS OF TIMESTAMP('2024-05-14T12:42:36.125125+00:00') "
                "WHERE `rowindex` < 4 AND `string_col` = 'Hello, World!' "
                "LIMIT 123"
            ),
            id="subquery-all_params-filter_and_operation",
        ),
        pytest.param(
            "test_table",
            ["col_a", "col_b"],
            [],
            None,  # max_results
            None,  # time_travel_timestampe
            "SELECT `col_a`, `col_b` FROM `test_table`",
            id="table-columns",
        ),
        pytest.param(
            "test_table",
            [],
            [("date_col", ">", "2022-10-20")],
            None,  # max_results
            None,  # time_travel_timestampe
            "SELECT * FROM `test_table` WHERE `date_col` > '2022-10-20'",
            id="table-filter",
        ),
        pytest.param(
            "test_table*",
            [],
            [],
            None,  # max_results
            None,  # time_travel_timestampe
            "SELECT * FROM `test_table*`",
            id="wildcard-no_params",
        ),
        pytest.param(
            "test_table*",
            [],
            [("_TABLE_SUFFIX", ">", "2022-10-20")],
            None,  # max_results
            None,  # time_travel_timestampe
            "SELECT * FROM `test_table*` WHERE `_TABLE_SUFFIX` > '2022-10-20'",
            id="wildcard-filter",
        ),
    ],
)
def test_to_query(
    query_or_table,
    columns,
    filters,
    max_results,
    time_travel_timestamp,
    expected_output,
):
    query = io_bq.to_query(
        query_or_table,
        columns=columns,
        sql_predicate=io_bq.compile_filters(filters),
        max_results=max_results,
        time_travel_timestamp=time_travel_timestamp,
    )
    assert query == expected_output


@pytest.mark.parametrize(
    ("filters", "expected_message"),
    (
        pytest.param(
            ["date_col", ">", "2022-10-20"],
            "Elements of filters must be tuples of length 3, but got 'd'",
        ),
    ),
)
def test_to_query_fails_with_bad_filters(filters, expected_message):
    with pytest.raises(ValueError, match=re.escape(expected_message)):
        io_bq.to_query(
            "test_table",
            columns=(),
            sql_predicate=io_bq.compile_filters(filters),
            max_results=None,
            time_travel_timestamp=None,
        )
