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
from typing import Iterable
import unittest.mock as mock

import google.cloud.bigquery as bigquery
import pytest

import bigframes
from bigframes.core import log_adapter
import bigframes.pandas as bpd
import bigframes.session._io.bigquery as io_bq


def test_create_job_configs_labels_is_none():
    api_methods = ["agg", "series-mode"]
    labels = io_bq.create_job_configs_labels(
        job_configs_labels=None, api_methods=api_methods
    )
    expected_dict = {
        "recent-bigframes-api-0": "agg",
        "recent-bigframes-api-1": "series-mode",
    }
    assert labels is not None
    assert labels == expected_dict


def test_create_job_configs_labels_length_limit_not_met():
    cur_labels = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
    }
    api_methods = ["agg", "series-mode"]
    labels = io_bq.create_job_configs_labels(
        job_configs_labels=cur_labels, api_methods=api_methods
    )
    expected_dict = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
        "recent-bigframes-api-0": "agg",
        "recent-bigframes-api-1": "series-mode",
    }
    assert labels is not None
    assert len(labels) == 4
    assert labels == expected_dict


def test_create_job_configs_labels_log_adaptor_call_method_under_length_limit():
    log_adapter.get_and_reset_api_methods()
    cur_labels = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
    }
    df = bpd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    # Test running two methods
    df.head()
    df.max()
    api_methods = log_adapter._api_methods

    labels = io_bq.create_job_configs_labels(
        job_configs_labels=cur_labels, api_methods=api_methods
    )
    expected_dict = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
        "recent-bigframes-api-0": "__init__",
        "recent-bigframes-api-1": "max",
        "recent-bigframes-api-2": "__init__",
        "recent-bigframes-api-3": "head",
        "recent-bigframes-api-4": "__init__",
    }
    assert labels is not None
    assert len(labels) == 7
    assert labels == expected_dict


def test_create_job_configs_labels_length_limit_met_and_labels_is_none():
    log_adapter.get_and_reset_api_methods()
    df = bpd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    # Test running methods more than the labels' length limit
    for i in range(66):
        df.head()
    api_methods = log_adapter._api_methods

    labels = io_bq.create_job_configs_labels(
        job_configs_labels=None, api_methods=api_methods
    )
    assert labels is not None
    assert len(labels) == 64
    assert "head" in labels.values()


def test_create_job_configs_labels_length_limit_met():
    log_adapter.get_and_reset_api_methods()
    cur_labels = {
        "bigframes-api": "read_pandas",
        "source": "bigquery-dataframes-temp",
    }
    for i in range(60):
        key = f"bigframes-api-test-{i}"
        value = f"test{i}"
        cur_labels[key] = value
    # If cur_labels length is 62, we can only add one label from api_methods
    df = bpd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    # Test running two methods
    df.head()
    df.max()
    api_methods = log_adapter._api_methods

    labels = io_bq.create_job_configs_labels(
        job_configs_labels=cur_labels, api_methods=api_methods
    )
    assert labels is not None
    assert len(labels) == 64
    assert "max" in labels.values()
    assert "head" not in labels.values()
    assert "bigframes-api" in labels.keys()
    assert "source" in labels.keys()


def test_create_snapshot_sql_doesnt_timetravel_anonymous_datasets():
    table_ref = bigquery.TableReference.from_string(
        "my-test-project._e8166e0cdb.anonbb92cd"
    )

    sql = bigframes.session._io.bigquery.create_snapshot_sql(
        table_ref, datetime.datetime.now(datetime.timezone.utc)
    )

    # Anonymous query results tables don't support time travel.
    assert "SYSTEM_TIME" not in sql

    # Need fully-qualified table name.
    assert "`my-test-project`.`_e8166e0cdb`.`anonbb92cd`" in sql


def test_create_temp_table_default_expiration():
    """Make sure the created table has an expiration."""
    bqclient = mock.create_autospec(bigquery.Client)
    dataset = bigquery.DatasetReference("test-project", "test_dataset")
    expiration = datetime.datetime(
        2023, 11, 2, 13, 44, 55, 678901, datetime.timezone.utc
    )

    bigframes.session._io.bigquery.create_temp_table(bqclient, dataset, expiration)

    bqclient.create_table.assert_called_once()
    call_args = bqclient.create_table.call_args
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
