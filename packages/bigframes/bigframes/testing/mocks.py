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

import copy
import datetime
from typing import Any, Dict, Literal, Optional, Sequence
import unittest.mock as mock

from bigframes_vendored.google_cloud_bigquery import _pandas_helpers
import google.auth.credentials
import google.cloud.bigquery
import google.cloud.bigquery.table
import pyarrow
import pytest

import bigframes
import bigframes.clients
import bigframes.core.global_session
import bigframes.dataframe
import bigframes.session.clients

"""Utilities for creating test resources."""


TEST_SCHEMA = (google.cloud.bigquery.SchemaField("col", "INTEGER"),)


def create_bigquery_session(
    *,
    bqclient: Optional[mock.Mock] = None,
    session_id: str = "abcxyz",
    table_schema: Sequence[google.cloud.bigquery.SchemaField] = TEST_SCHEMA,
    table_name: str = "test_table",
    anonymous_dataset: Optional[google.cloud.bigquery.DatasetReference] = None,
    location: str = "test-region",
    ordering_mode: Literal["strict", "partial"] = "partial",
) -> bigframes.Session:
    """[Experimental] Create a mock BigQuery DataFrames session that avoids making Google Cloud API calls.

    Intended for unit test environments that don't have access to the network.
    """
    credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    bq_time = datetime.datetime.now()
    table_time = bq_time + datetime.timedelta(minutes=1)

    if anonymous_dataset is None:
        anonymous_dataset = google.cloud.bigquery.DatasetReference(
            "test-project",
            "test_dataset",
        )

    if bqclient is None:
        bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
        bqclient.project = anonymous_dataset.project
        bqclient.location = location

        # Mock the location.
        table = mock.create_autospec(google.cloud.bigquery.Table, instance=True)
        table._properties = {}
        # TODO(tswast): support tables created before and after the session started.
        type(table).created = mock.PropertyMock(return_value=table_time)
        type(table).location = mock.PropertyMock(return_value=location)
        type(table).schema = mock.PropertyMock(return_value=table_schema)
        type(table).project = anonymous_dataset.project
        type(table).dataset_id = anonymous_dataset.dataset_id
        type(table).table_id = table_name
        type(table).num_rows = mock.PropertyMock(return_value=1000000000)
        bqclient.get_table.return_value = table

    queries = []
    job_configs = []

    def query_mock(
        query,
        *args,
        job_config: Optional[google.cloud.bigquery.QueryJobConfig] = None,
        **kwargs,
    ):
        queries.append(query)
        job_configs.append(copy.deepcopy(job_config))
        query_job = mock.create_autospec(google.cloud.bigquery.QueryJob, instance=True)
        query_job._properties = {}
        type(query_job).destination = mock.PropertyMock(
            return_value=anonymous_dataset.table(table_name),
        )
        type(query_job).statement_type = mock.PropertyMock(return_value="SELECT")

        if job_config is not None and job_config.create_session:
            type(query_job).session_info = google.cloud.bigquery.SessionInfo(
                {"sessionId": session_id},
            )

        if query.startswith("SELECT CURRENT_TIMESTAMP()"):
            query_job.result = mock.MagicMock(return_value=[[bq_time]])
        elif "CREATE TEMP TABLE".casefold() in query.casefold():
            type(query_job).destination = mock.PropertyMock(
                return_value=anonymous_dataset.table("temp_table_from_session"),
            )
        else:
            type(query_job).schema = mock.PropertyMock(return_value=table_schema)

        return query_job

    def query_and_wait_mock(query, *args, job_config=None, **kwargs):
        queries.append(query)
        job_configs.append(copy.deepcopy(job_config))

        if query.startswith("SELECT CURRENT_TIMESTAMP()"):
            return iter([[datetime.datetime.now()]])

        rows = mock.create_autospec(
            google.cloud.bigquery.table.RowIterator, instance=True
        )
        row = mock.create_autospec(google.cloud.bigquery.table.Row, instance=True)
        rows.__iter__.return_value = [row]
        type(rows).schema = mock.PropertyMock(return_value=table_schema)
        rows.to_arrow.return_value = pyarrow.Table.from_pydict(
            {field.name: [None] for field in table_schema},
            schema=pyarrow.schema(
                _pandas_helpers.bq_to_arrow_field(field) for field in table_schema
            ),
        )

        if job_config is not None and job_config.destination is None:
            # Assume that the query finishes fast enough for jobless mode.
            type(rows).job_id = mock.PropertyMock(return_value=None)

        return rows

    bqclient.query.side_effect = query_mock
    bqclient.query_and_wait.side_effect = query_and_wait_mock

    clients_provider = mock.create_autospec(bigframes.session.clients.ClientsProvider)
    type(clients_provider).bqclient = mock.PropertyMock(return_value=bqclient)
    clients_provider._credentials = credentials

    bqoptions = bigframes.BigQueryOptions(
        credentials=credentials,
        location=location,
        ordering_mode=ordering_mode,
    )
    session = bigframes.Session(context=bqoptions, clients_provider=clients_provider)
    session._bq_connection_manager = mock.create_autospec(
        bigframes.clients.BqConnectionManager, instance=True
    )
    session._queries = queries  # type: ignore
    session._job_configs = job_configs  # type: ignore
    return session


def create_dataframe(
    monkeypatch: pytest.MonkeyPatch,
    *,
    session: Optional[bigframes.Session] = None,
    data: Optional[Dict[str, Sequence[Any]]] = None,
) -> bigframes.dataframe.DataFrame:
    """[Experimental] Create a mock DataFrame that avoids making Google Cloud API calls.

    Intended for unit test environments that don't have access to the network.
    """
    if session is None:
        session = create_bigquery_session()

    if data is None:
        data = {"col": []}

    # Since this may create a ReadLocalNode, the session we explicitly pass in
    # might not actually be used. Mock out the global session, too.
    monkeypatch.setattr(bigframes.core.global_session, "_global_session", session)
    bigframes.options.bigquery._session_started = True
    return bigframes.dataframe.DataFrame(data, session=session)
