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

import unittest.mock as mock
import warnings

import google.cloud.bigquery
import pytest

from bigframes.core import bq_data
import bigframes.enums
import bigframes.exceptions
import bigframes.session._io.bigquery.read_gbq_table as bf_read_gbq_table
from bigframes.testing import mocks


@pytest.mark.parametrize(
    ("index_cols", "primary_keys", "expected"),
    (
        (["col1", "col2"], ["col1", "col2", "col3"], ("col1", "col2", "col3")),
        (
            ["col1", "col2", "col3"],
            ["col1", "col2", "col3"],
            ("col1", "col2", "col3"),
        ),
        (
            ["col2", "col3", "col1"],
            [
                "col3",
                "col2",
            ],
            ("col2", "col3"),
        ),
        (["col1", "col2"], [], ()),
        ([], ["col1", "col2", "col3"], ("col1", "col2", "col3")),
        ([], [], ()),
    ),
)
def test_infer_unique_columns(index_cols, primary_keys, expected):
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

    result = bf_read_gbq_table.infer_unique_columns(
        bq_data.GbqNativeTable.from_table(table), index_cols
    )

    assert result == expected


@pytest.mark.parametrize(
    ("index_cols", "values_distinct", "expected"),
    (
        (
            ["col1", "col2", "col3"],
            True,
            ("col1", "col2", "col3"),
        ),
        (
            ["col2", "col3", "col1"],
            True,
            ("col2", "col3", "col1"),
        ),
        (["col1", "col2"], False, ()),
        ([], False, ()),
    ),
)
def test_check_if_index_columns_are_unique(index_cols, values_distinct, expected):
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

    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    session = mocks.create_bigquery_session(
        bqclient=bqclient, table_schema=table.schema
    )

    # Mock bqclient _after_ creating session to override its mocks.
    bqclient.get_table.return_value = table
    bqclient._query_and_wait_bigframes.side_effect = None
    bqclient._query_and_wait_bigframes.return_value = (
        {"total_count": 3, "distinct_count": 3 if values_distinct else 2},
    )

    table._properties["location"] = session._location

    result = bf_read_gbq_table.check_if_index_columns_are_unique(
        bqclient=bqclient,
        table=bq_data.GbqNativeTable.from_table(table),
        index_cols=index_cols,
        publisher=session._publisher,
    )

    assert result == expected


def test_get_index_cols_warns_if_clustered_but_sequential_index():
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

    with pytest.warns(bigframes.exceptions.DefaultIndexWarning, match="is clustered"):
        bf_read_gbq_table.get_index_cols(
            bq_data.GbqNativeTable.from_table(table),
            index_col=(),
            default_index_type=bigframes.enums.DefaultIndexKind.SEQUENTIAL_INT64,
        )

    # Ensure that we don't raise if using a NULL index by default, such as in
    # partial ordering mode. See: internal issue b/356872356.
    with warnings.catch_warnings():
        warnings.simplefilter(
            "error", category=bigframes.exceptions.DefaultIndexWarning
        )
        bf_read_gbq_table.get_index_cols(
            bq_data.GbqNativeTable.from_table(table),
            index_col=(),
            default_index_type=bigframes.enums.DefaultIndexKind.NULL,
        )
