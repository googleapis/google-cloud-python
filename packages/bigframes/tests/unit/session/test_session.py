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
import os
import re
from unittest import mock

import google.api_core.exceptions
import google.cloud.bigquery
import pytest

import bigframes

from .. import resources


@pytest.mark.parametrize("missing_parts_table_id", [(""), ("table")])
def test_read_gbq_missing_parts(missing_parts_table_id):
    session = resources.create_bigquery_session()

    with pytest.raises(ValueError):
        session.read_gbq(missing_parts_table_id)


def test_read_gbq_cached_table():
    session = resources.create_bigquery_session()
    table_ref = google.cloud.bigquery.TableReference(
        google.cloud.bigquery.DatasetReference("my-project", "my_dataset"),
        "my_table",
    )
    session._df_snapshot[table_ref] = datetime.datetime(
        1999, 1, 2, 3, 4, 5, 678901, tzinfo=datetime.timezone.utc
    )

    with pytest.warns(UserWarning, match=re.escape("use_cache=False")):
        df = session.read_gbq("my-project.my_dataset.my_table")

    assert "1999-01-02T03:04:05.678901" in df.sql


@pytest.mark.parametrize(
    "not_found_table_id",
    [("unknown.dataset.table"), ("project.unknown.table"), ("project.dataset.unknown")],
)
def test_read_gbq_not_found_tables(not_found_table_id):
    bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    bqclient.project = "test-project"
    bqclient.get_table.side_effect = google.api_core.exceptions.NotFound(
        "table not found"
    )
    session = resources.create_bigquery_session(bqclient=bqclient)

    with pytest.raises(google.api_core.exceptions.NotFound):
        session.read_gbq(not_found_table_id)


@pytest.mark.parametrize(
    ("api_name", "query_or_table"),
    [
        ("read_gbq", "project.dataset.table"),
        ("read_gbq_table", "project.dataset.table"),
        ("read_gbq", "SELECT * FROM project.dataset.table"),
        ("read_gbq_query", "SELECT * FROM project.dataset.table"),
    ],
    ids=[
        "read_gbq_on_table",
        "read_gbq_table",
        "read_gbq_on_query",
        "read_gbq_query",
    ],
)
def test_read_gbq_external_table_no_drive_access(api_name, query_or_table):
    session = resources.create_bigquery_session()
    session_query_mock = session.bqclient.query

    def query_mock(query, *args, **kwargs):
        if query.lstrip().startswith("SELECT *"):
            raise google.api_core.exceptions.Forbidden(
                "Access Denied: BigQuery BigQuery: Permission denied while getting Drive credentials."
            )

        return session_query_mock(query, *args, **kwargs)

    session.bqclient.query = query_mock

    def get_table_mock(dataset_ref):
        dataset = google.cloud.bigquery.Dataset(dataset_ref)
        dataset.location = session._location
        return dataset

    session.bqclient.get_table = get_table_mock

    api = getattr(session, api_name)
    with pytest.raises(
        google.api_core.exceptions.Forbidden,
        match="Check https://cloud.google.com/bigquery/docs/query-drive-data#Google_Drive_permissions.",
    ):
        api(query_or_table)


@mock.patch.dict(os.environ, {}, clear=True)
def test_session_init_fails_with_no_project():
    with pytest.raises(
        ValueError, match="Project must be set to initialize BigQuery client."
    ):
        bigframes.Session(
            bigframes.BigQueryOptions(
                credentials=mock.Mock(spec=google.auth.credentials.Credentials)
            )
        )


@pytest.mark.parametrize(
    ("query_or_table", "columns", "filters", "expected_output"),
    [
        pytest.param(
            """SELECT
                rowindex,
                string_col,
            FROM `test_table` AS t
            """,
            [],
            [("rowindex", "<", 4), ("string_col", "==", "Hello, World!")],
            """SELECT * FROM (SELECT
                rowindex,
                string_col,
            FROM `test_table` AS t
            ) AS sub WHERE `rowindex` < 4 AND `string_col` = 'Hello, World!'""",
            id="query_input",
        ),
        pytest.param(
            "test_table",
            [],
            [("date_col", ">", "2022-10-20")],
            "SELECT * FROM `test_table` AS sub WHERE `date_col` > '2022-10-20'",
            id="table_input",
        ),
        pytest.param(
            "test_table",
            ["row_index", "string_col"],
            [
                (("rowindex", "not in", [0, 6]),),
                (("string_col", "in", ["Hello, World!", "こんにちは"]),),
            ],
            (
                "SELECT `row_index`, `string_col` FROM `test_table` AS sub WHERE "
                "`rowindex` NOT IN (0, 6) OR `string_col` IN ('Hello, World!', "
                "'こんにちは')"
            ),
            id="or_operation",
        ),
        pytest.param(
            "test_table",
            [],
            ["date_col", ">", "2022-10-20"],
            None,
            marks=pytest.mark.xfail(
                raises=ValueError,
            ),
            id="raise_error",
        ),
    ],
)
def test_read_gbq_with_filters(query_or_table, columns, filters, expected_output):
    session = resources.create_bigquery_session()
    query = session._to_query(query_or_table, columns, filters)
    assert query == expected_output


@pytest.mark.parametrize(
    ("query_or_table", "columns", "filters", "expected_output"),
    [
        pytest.param(
            "test_table*",
            [],
            [],
            "SELECT * FROM `test_table*` AS sub",
            id="wildcard_table_input",
        ),
        pytest.param(
            "test_table*",
            [],
            [("_TABLE_SUFFIX", ">", "2022-10-20")],
            "SELECT * FROM `test_table*` AS sub WHERE `_TABLE_SUFFIX` > '2022-10-20'",
            id="wildcard_table_input_with_filter",
        ),
    ],
)
def test_read_gbq_wildcard(query_or_table, columns, filters, expected_output):
    session = resources.create_bigquery_session()
    query = session._to_query(query_or_table, columns, filters)
    assert query == expected_output
