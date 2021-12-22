# Copyright (c) 2017 pandas-gbq Authors All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# -*- coding: utf-8 -*-

from unittest import mock

import pytest


@pytest.fixture(autouse=True, scope="function")
def reset_context():
    import pandas_gbq

    pandas_gbq.context.credentials = None
    pandas_gbq.context.project = None


@pytest.fixture(autouse=True)
def mock_bigquery_client(monkeypatch):
    import google.cloud.bigquery
    import google.cloud.bigquery.table

    mock_client = mock.create_autospec(google.cloud.bigquery.Client)
    # Constructor returns the mock itself, so this mock can be treated as the
    # constructor or the instance.
    mock_client.return_value = mock_client

    mock_query = mock.create_autospec(google.cloud.bigquery.QueryJob)
    mock_query.job_id = "some-random-id"
    mock_query.state = "DONE"
    mock_rows = mock.create_autospec(google.cloud.bigquery.table.RowIterator)
    mock_rows.total_rows = 1

    mock_rows.__iter__.return_value = [(1,)]
    mock_query.result.return_value = mock_rows
    mock_client.list_rows.return_value = mock_rows
    mock_client.query.return_value = mock_query
    # Mock table creation.
    monkeypatch.setattr(google.cloud.bigquery, "Client", mock_client)
    mock_client.reset_mock()

    # Mock out SELECT 1 query results.
    def generate_schema():
        query = mock_client.query.call_args[0][0] if mock_client.query.call_args else ""
        if query == "SELECT 1 AS int_col":
            return [google.cloud.bigquery.SchemaField("int_col", "INTEGER")]
        else:
            return [google.cloud.bigquery.SchemaField("_f0", "INTEGER")]

    type(mock_rows).schema = mock.PropertyMock(side_effect=generate_schema)

    # Mock out get_table.
    def get_table(table_ref_or_id, **kwargs):
        return google.cloud.bigquery.Table(table_ref_or_id)

    mock_client.get_table.side_effect = get_table

    return mock_client
