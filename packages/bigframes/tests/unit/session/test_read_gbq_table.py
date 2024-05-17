# Copyright 2024 Google LLC
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

"""Unit tests for read_gbq_table helper functions."""

import datetime
import unittest.mock as mock

import google.cloud.bigquery
import google.cloud.bigquery as bigquery
import pytest

import bigframes.session._io.bigquery.read_gbq_table as bf_read_gbq_table

from .. import resources


def test_get_ibis_time_travel_table_doesnt_timetravel_anonymous_datasets():
    bqsession = resources.create_bigquery_session()

    table_ref = bigquery.TableReference.from_string(
        "my-test-project._e8166e0cdb.anonbb92cd"
    )

    table_expression = bf_read_gbq_table.get_ibis_time_travel_table(
        bqsession.ibis_client,
        table_ref,
        index_cols=(),
        columns=(),
        filters=(),
        time_travel_timestamp=datetime.datetime.now(datetime.timezone.utc),
    )
    sql = table_expression.compile()

    # Anonymous query results tables don't support time travel.
    assert "SYSTEM_TIME" not in sql

    # Need fully-qualified table name.
    assert "my-test-project" in sql


@pytest.mark.parametrize(
    ("index_cols", "primary_keys", "values_distinct", "expected"),
    (
        (["col1", "col2"], ["col1", "col2", "col3"], False, False),
        (["col1", "col2", "col3"], ["col1", "col2", "col3"], True, True),
        (
            ["col2", "col3", "col1"],
            [
                "col3",
                "col2",
            ],
            True,
            True,
        ),
        (["col1", "col2"], [], False, False),
        ([], ["col1", "col2", "col3"], False, False),
        ([], [], False, False),
    ),
)
def test_are_index_cols_unique(index_cols, primary_keys, values_distinct, expected):
    """If a primary key is set on the table, we use that as the index column
    by default, no error should be raised in this case.

    See internal issue 335727141.
    """
    table = google.cloud.bigquery.Table.from_api_repr(
        {
            "tableReference": {
                "projectId": "my-project",
                "datasetId": "my_dataset",
                "tableId": "my_table",
            },
            "clustering": {
                "fields": ["col1", "col2"],
            },
        },
    )
    table.schema = (
        google.cloud.bigquery.SchemaField("col1", "INT64"),
        google.cloud.bigquery.SchemaField("col2", "INT64"),
        google.cloud.bigquery.SchemaField("col3", "INT64"),
        google.cloud.bigquery.SchemaField("col4", "INT64"),
    )

    # TODO(b/305264153): use setter for table_constraints in client library
    # when available.
    table._properties["tableConstraints"] = {
        "primaryKey": {
            "columns": primary_keys,
        },
    }
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.return_value = table

    bqclient.query_and_wait.return_value = (
        {"total_count": 3, "distinct_count": 3 if values_distinct else 2},
    )
    session = resources.create_bigquery_session(
        bqclient=bqclient, table_schema=table.schema
    )
    table._properties["location"] = session._location

    result = bf_read_gbq_table.are_index_cols_unique(bqclient, table, index_cols, "")

    assert result == expected
