# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"");
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

from unittest import mock

import pytest

import bigframes.bigquery
import bigframes.core.sql.table
import bigframes.session


@pytest.fixture
def mock_session():
    return mock.create_autospec(spec=bigframes.session.Session)


def test_create_external_table_ddl():
    sql = bigframes.core.sql.table.create_external_table_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "CREATE EXTERNAL TABLE my-project.my_dataset.my_table (col1 INT64, col2 STRING) OPTIONS (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_create_external_table_ddl_replace():
    sql = bigframes.core.sql.table.create_external_table_ddl(
        "my-project.my_dataset.my_table",
        replace=True,
        columns={"col1": "INT64", "col2": "STRING"},
        options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "CREATE OR REPLACE EXTERNAL TABLE my-project.my_dataset.my_table (col1 INT64, col2 STRING) OPTIONS (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_create_external_table_ddl_if_not_exists():
    sql = bigframes.core.sql.table.create_external_table_ddl(
        "my-project.my_dataset.my_table",
        if_not_exists=True,
        columns={"col1": "INT64", "col2": "STRING"},
        options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "CREATE EXTERNAL TABLE IF NOT EXISTS my-project.my_dataset.my_table (col1 INT64, col2 STRING) OPTIONS (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_create_external_table_ddl_partition_columns():
    sql = bigframes.core.sql.table.create_external_table_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        partition_columns={"part1": "DATE", "part2": "STRING"},
        options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "CREATE EXTERNAL TABLE my-project.my_dataset.my_table (col1 INT64, col2 STRING) WITH PARTITION COLUMNS (part1 DATE, part2 STRING) OPTIONS (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


def test_create_external_table_ddl_connection():
    sql = bigframes.core.sql.table.create_external_table_ddl(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        connection_name="my-connection",
        options={"format": "CSV", "uris": ["gs://bucket/path*"]},
    )
    expected = "CREATE EXTERNAL TABLE my-project.my_dataset.my_table (col1 INT64, col2 STRING) WITH CONNECTION `my-connection` OPTIONS (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert sql == expected


@mock.patch("bigframes.bigquery._operations.table._get_table_metadata")
def test_create_external_table(get_table_metadata_mock, mock_session):
    bigframes.bigquery.create_external_table(
        "my-project.my_dataset.my_table",
        columns={"col1": "INT64", "col2": "STRING"},
        options={"format": "CSV", "uris": ["gs://bucket/path*"]},
        session=mock_session,
    )
    mock_session.read_gbq_query.assert_called_once()
    generated_sql = mock_session.read_gbq_query.call_args[0][0]
    expected = "CREATE EXTERNAL TABLE my-project.my_dataset.my_table (col1 INT64, col2 STRING) OPTIONS (format = 'CSV', uris = ['gs://bucket/path*'])"
    assert generated_sql == expected
    get_table_metadata_mock.assert_called_once()
