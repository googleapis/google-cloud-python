# Copyright 2021 The sqlalchemy-bigquery Authors
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from unittest import mock

import google.api_core.exceptions
from google.cloud import bigquery
from google.cloud.bigquery.dataset import DatasetListItem
from google.cloud.bigquery.table import TableListItem
import pytest
import sqlalchemy


@pytest.fixture
def mock_bigquery_client():
    return mock.create_autospec(bigquery.Client, instance=True)


@pytest.fixture
def mock_connection(monkeypatch, mock_bigquery_client):
    import sqlalchemy_bigquery

    def mock_connect_args(*args, **kwargs):
        return ([mock_bigquery_client], {})

    monkeypatch.setattr(
        sqlalchemy_bigquery.BigQueryDialect, "create_connect_args", mock_connect_args
    )


@pytest.fixture
def engine_under_test(mock_connection):
    return sqlalchemy.create_engine("bigquery://")


@pytest.fixture
def inspector_under_test(engine_under_test):
    from sqlalchemy.engine.reflection import Inspector

    return Inspector.from_engine(engine_under_test)


def dataset_item(dataset_id):
    return DatasetListItem(
        {"datasetReference": {"projectId": "some-project-id", "datasetId": dataset_id}}
    )


def table_item(dataset_id, table_id, type_="TABLE"):
    return TableListItem(
        {
            "type": type_,
            "tableReference": {
                "projectId": "some-project-id",
                "datasetId": dataset_id,
                "tableId": table_id,
            },
        }
    )


@pytest.mark.parametrize(
    ["datasets_list", "tables_lists", "expected"],
    [
        ([], [], []),
        ([dataset_item("dataset_1")], [[]], []),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_2")],
            [
                [table_item("dataset_1", "d1t1"), table_item("dataset_1", "d1t2")],
                [
                    table_item("dataset_2", "d2t1"),
                    table_item("dataset_2", "d2view", type_="VIEW"),
                ],
            ],
            ["dataset_1.d1t1", "dataset_1.d1t2", "dataset_2.d2t1"],
        ),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_deleted")],
            [
                [table_item("dataset_1", "d1t1")],
                google.api_core.exceptions.NotFound("dataset_deleted"),
            ],
            ["dataset_1.d1t1"],
        ),
    ],
)
def test_get_table_names(
    engine_under_test, mock_bigquery_client, datasets_list, tables_lists, expected
):
    mock_bigquery_client.list_datasets.return_value = datasets_list
    mock_bigquery_client.list_tables.side_effect = tables_lists
    table_names = engine_under_test.table_names()
    mock_bigquery_client.list_datasets.assert_called_once()
    assert mock_bigquery_client.list_tables.call_count == len(datasets_list)
    assert list(sorted(table_names)) == list(sorted(expected))


@pytest.mark.parametrize(
    ["datasets_list", "tables_lists", "expected"],
    [
        ([], [], []),
        ([dataset_item("dataset_1")], [[]], []),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_2")],
            [
                [
                    table_item("dataset_1", "d1t1"),
                    table_item("dataset_1", "d1view", type_="VIEW"),
                ],
                [
                    table_item("dataset_2", "d2t1"),
                    table_item("dataset_2", "d2view", type_="VIEW"),
                ],
            ],
            ["dataset_1.d1view", "dataset_2.d2view"],
        ),
        (
            [dataset_item("dataset_1"), dataset_item("dataset_deleted")],
            [
                [table_item("dataset_1", "d1view", type_="VIEW")],
                google.api_core.exceptions.NotFound("dataset_deleted"),
            ],
            ["dataset_1.d1view"],
        ),
    ],
)
def test_get_view_names(
    inspector_under_test, mock_bigquery_client, datasets_list, tables_lists, expected
):
    mock_bigquery_client.list_datasets.return_value = datasets_list
    mock_bigquery_client.list_tables.side_effect = tables_lists
    view_names = inspector_under_test.get_view_names()
    mock_bigquery_client.list_datasets.assert_called_once()
    assert mock_bigquery_client.list_tables.call_count == len(datasets_list)
    assert list(sorted(view_names)) == list(sorted(expected))


@pytest.mark.parametrize(
    "inp, outp",
    [
        ("(NULL IN UNNEST([ NULL) AND (1 != 1 ]))", "(NULL IN(NULL) AND (1 != 1))"),
        (
            "(NULL IN UNNEST([ NULL) AND (1 != 1:INT64 ]))",
            "(NULL IN(NULL) AND (1 != 1))",
        ),
        (
            "(NULL IN UNNEST([ (NULL, NULL)) AND (1 != 1:INT64 ]))",
            "(NULL IN((NULL, NULL)) AND (1 != 1))",
        ),
    ],
)
def test__remove_type_from_empty_in(inp, outp):
    from sqlalchemy_bigquery.base import BigQueryExecutionContext

    r = BigQueryExecutionContext._BigQueryExecutionContext__remove_type_from_empty_in
    assert r(None, inp) == outp
