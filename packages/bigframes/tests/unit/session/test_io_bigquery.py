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

import bigframes.session._io.bigquery


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


def test_create_snapshot_sql_doesnt_timetravel_session_tables():
    table_ref = bigquery.TableReference.from_string("my-test-project._session.abcdefg")

    sql = bigframes.session._io.bigquery.create_snapshot_sql(
        table_ref, datetime.datetime.now(datetime.timezone.utc)
    )

    # We aren't modifying _SESSION tables, so don't use time travel.
    assert "SYSTEM_TIME" not in sql

    # Don't need the project ID for _SESSION tables.
    assert "my-test-project" not in sql


def test_create_temp_table_default_expiration():
    """Make sure the created table has an expiration."""
    bqclient = mock.create_autospec(bigquery.Client)
    dataset = bigquery.DatasetReference("test-project", "test_dataset")
    now = datetime.datetime.now(datetime.timezone.utc)
    expiration = datetime.timedelta(days=3)
    expected_expires = now + expiration

    bigframes.session._io.bigquery.create_temp_table(bqclient, dataset, expiration)

    bqclient.create_table.assert_called_once()
    call_args = bqclient.create_table.call_args
    table = call_args.args[0]
    assert table.project == "test-project"
    assert table.dataset_id == "test_dataset"
    assert table.table_id.startswith("bqdf")
    assert (
        (expected_expires - datetime.timedelta(minutes=1))
        < table.expires
        < (expected_expires + datetime.timedelta(minutes=1))
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
    sql = bigframes.session._io.bigquery.bq_schema_to_sql(schema)
    assert sql == expected
