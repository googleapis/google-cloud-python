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

from typing import Dict, List, Optional
import unittest.mock as mock

import google.auth.credentials
import google.cloud.bigquery
import ibis
import pandas
import pytest

import bigframes
import bigframes.core as core
import bigframes.core.ordering
import bigframes.dataframe
import bigframes.session.clients

"""Utilities for creating test resources."""


def create_bigquery_session(
    bqclient: Optional[mock.Mock] = None,
    session_id: str = "abcxyz",
    anonymous_dataset: Optional[google.cloud.bigquery.DatasetReference] = None,
) -> bigframes.Session:
    credentials = mock.create_autospec(
        google.auth.credentials.Credentials, instance=True
    )

    if bqclient is None:
        bqclient = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
        bqclient.project = "test-project"

    if anonymous_dataset is None:
        anonymous_dataset = google.cloud.bigquery.DatasetReference(
            "test-project",
            "test_dataset",
        )

    query_job = mock.create_autospec(google.cloud.bigquery.QueryJob)
    type(query_job).destination = mock.PropertyMock(
        return_value=anonymous_dataset.table("test_table"),
    )
    type(query_job).session_info = google.cloud.bigquery.SessionInfo(
        {"sessionInfo": {"sessionId": session_id}},
    )
    bqclient.query.return_value = query_job

    clients_provider = mock.create_autospec(bigframes.session.clients.ClientsProvider)
    type(clients_provider).bqclient = mock.PropertyMock(return_value=bqclient)
    clients_provider._credentials = credentials

    bqoptions = bigframes.BigQueryOptions(
        credentials=credentials, location="test-region"
    )
    session = bigframes.Session(context=bqoptions, clients_provider=clients_provider)
    return session


def create_dataframe(
    monkeypatch: pytest.MonkeyPatch, session: Optional[bigframes.Session] = None
) -> bigframes.dataframe.DataFrame:
    if session is None:
        session = create_bigquery_session()

    # Since this may create a ReadLocalNode, the session we explicitly pass in
    # might not actually be used. Mock out the global session, too.
    monkeypatch.setattr(bigframes.core.global_session, "_global_session", session)
    bigframes.options.bigquery._session_started = True
    return bigframes.dataframe.DataFrame({}, session=session)


def create_pandas_session(tables: Dict[str, pandas.DataFrame]) -> bigframes.Session:
    # TODO(tswast): Refactor to make helper available for all tests. Consider
    # providing a proper "local Session" for use by downstream developers.
    session = mock.create_autospec(bigframes.Session, instance=True)
    ibis_client = ibis.pandas.connect(tables)
    type(session).ibis_client = mock.PropertyMock(return_value=ibis_client)
    return session


def create_arrayvalue(
    df: pandas.DataFrame, total_ordering_columns: List[str]
) -> core.ArrayValue:
    session = create_pandas_session({"test_table": df})
    ibis_table = session.ibis_client.table("test_table")
    columns = tuple(ibis_table[key] for key in ibis_table.columns)
    ordering = bigframes.core.ordering.ExpressionOrdering(
        tuple(
            [core.OrderingColumnReference(column) for column in total_ordering_columns]
        ),
        total_ordering_columns=frozenset(total_ordering_columns),
    )
    return core.ArrayValue.from_ibis(
        session=session,
        table=ibis_table,
        columns=columns,
        hidden_ordering_columns=(),
        ordering=ordering,
    )
