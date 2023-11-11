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
from unittest import mock

import google.api_core.exceptions
import google.auth
import google.auth.exceptions
import pytest

import bigframes.core.global_session
import bigframes.pandas as bpd


@pytest.fixture(autouse=True)
def reset_default_session_and_location():
    bpd.close_session()
    bpd.options.bigquery.location = None


@pytest.mark.parametrize(
    ("read_method", "query_prefix"),
    [
        (bpd.read_gbq, None),
        (bpd.read_gbq, "SELECT COUNT(1) FROM "),
        (bpd.read_gbq_table, None),
        (bpd.read_gbq_query, "SELECT COUNT(1) FROM "),
    ],
    ids=[
        "read_gbq-on-table-name",
        "read_gbq-on-sql",
        "read_gbq_table-on-table-name",
        "read_gbq_query-on-sql",
    ],
)
def test_read_gbq_start_sets_session_location(
    test_data_tables_tokyo,
    dataset_id_permanent_tokyo,
    tokyo_location,
    test_data_tables,
    dataset_id_permanent,
    read_method,
    query_prefix,
):
    # Form query as a table name or a SQL depending on the test scenario
    query_tokyo = test_data_tables_tokyo["scalars"]
    query = test_data_tables["scalars"]
    if query_prefix:
        query_tokyo = f"{query_prefix} {query_tokyo}"
        query = f"{query_prefix} {query}"

    # Initially there is no location set in the bigquery options
    assert not bpd.options.bigquery.location

    # Starting user journey with read_gbq* should work for a table in any
    # location, in this case tokyo
    df = read_method(query_tokyo)
    assert df is not None

    # Now bigquery options location should be set to tokyo
    assert bpd.options.bigquery.location == tokyo_location

    # Now read_gbq* from another location should fail
    with pytest.raises(
        (google.api_core.exceptions.NotFound, ValueError),
        match=dataset_id_permanent,
    ):
        read_method(query)

    # Close global session to start over
    bpd.close_session()

    # There should still be the previous location set in the bigquery options
    assert bpd.options.bigquery.location == tokyo_location

    # Reset the location to be able to query another location
    bpd.options.bigquery.location = None
    assert not bpd.options.bigquery.location

    # Starting over the user journey with read_gbq* should work for a table
    # in another location, in this case US
    df = read_method(query)
    assert df is not None

    # Now bigquery options location should be set to US
    assert bpd.options.bigquery.location == "US"

    # Now read_gbq* from another location should fail
    with pytest.raises(
        (google.api_core.exceptions.NotFound, ValueError),
        match=dataset_id_permanent_tokyo,
    ):
        read_method(query_tokyo)


@pytest.mark.parametrize(
    ("read_method", "query_prefix"),
    [
        (bpd.read_gbq, None),
        (bpd.read_gbq, "SELECT COUNT(1) FROM "),
        (bpd.read_gbq_table, None),
        (bpd.read_gbq_query, "SELECT COUNT(1) FROM "),
    ],
    ids=[
        "read_gbq-on-table-name",
        "read_gbq-on-sql",
        "read_gbq_table-on-table-name",
        "read_gbq_query-on-sql",
    ],
)
def test_read_gbq_after_session_start_must_comply_with_default_location(
    scalars_pandas_df_index,
    test_data_tables,
    test_data_tables_tokyo,
    dataset_id_permanent_tokyo,
    read_method,
    query_prefix,
):
    # Form query as a table name or a SQL depending on the test scenario
    query_tokyo = test_data_tables_tokyo["scalars"]
    query = test_data_tables["scalars"]
    if query_prefix:
        query_tokyo = f"{query_prefix} {query_tokyo}"
        query = f"{query_prefix} {query}"

    # Initially there is no location set in the bigquery options
    assert not bpd.options.bigquery.location

    # Starting user journey with anything other than read_gbq*, such as
    # read_pandas would bind the session to default location US
    df = bpd.read_pandas(scalars_pandas_df_index)
    assert df is not None

    # Doing read_gbq* from a table in another location should fail
    with pytest.raises(
        (google.api_core.exceptions.NotFound, ValueError),
        match=dataset_id_permanent_tokyo,
    ):
        read_method(query_tokyo)

    # read_gbq* from a table in the default location should work
    df = read_method(query)
    assert df is not None


@pytest.mark.parametrize(
    ("read_method", "query_prefix"),
    [
        (bpd.read_gbq, None),
        (bpd.read_gbq, "SELECT COUNT(1) FROM "),
        (bpd.read_gbq_table, None),
        (bpd.read_gbq_query, "SELECT COUNT(1) FROM "),
    ],
    ids=[
        "read_gbq-on-table-name",
        "read_gbq-on-sql",
        "read_gbq_table-on-table-name",
        "read_gbq_query-on-sql",
    ],
)
def test_read_gbq_must_comply_with_set_location_US(
    test_data_tables,
    test_data_tables_tokyo,
    dataset_id_permanent_tokyo,
    read_method,
    query_prefix,
):
    # Form query as a table name or a SQL depending on the test scenario
    query_tokyo = test_data_tables_tokyo["scalars"]
    query = test_data_tables["scalars"]
    if query_prefix:
        query_tokyo = f"{query_prefix} {query_tokyo}"
        query = f"{query_prefix} {query}"

    # Initially there is no location set in the bigquery options
    assert not bpd.options.bigquery.location

    # Explicitly set location
    bpd.options.bigquery.location = "US"
    assert bpd.options.bigquery.location == "US"

    # Starting user journey with read_gbq* from another location should fail
    with pytest.raises(
        (google.api_core.exceptions.NotFound, ValueError),
        match=dataset_id_permanent_tokyo,
    ):
        read_method(query_tokyo)

    # Starting user journey with read_gbq* should work for a table in the same
    # location, in this case tokyo
    df = read_method(query)
    assert df is not None


@pytest.mark.parametrize(
    ("read_method", "query_prefix"),
    [
        (bpd.read_gbq, None),
        (bpd.read_gbq, "SELECT COUNT(1) FROM "),
        (bpd.read_gbq_table, None),
        (bpd.read_gbq_query, "SELECT COUNT(1) FROM "),
    ],
    ids=[
        "read_gbq-on-table-name",
        "read_gbq-on-sql",
        "read_gbq_table-on-table-name",
        "read_gbq_query-on-sql",
    ],
)
def test_read_gbq_must_comply_with_set_location_non_US(
    tokyo_location,
    test_data_tables,
    test_data_tables_tokyo,
    dataset_id_permanent,
    read_method,
    query_prefix,
):
    # Form query as a table name or a SQL depending on the test scenario
    query_tokyo = test_data_tables_tokyo["scalars"]
    query = test_data_tables["scalars"]
    if query_prefix:
        query_tokyo = f"{query_prefix} {query_tokyo}"
        query = f"{query_prefix} {query}"

    # Initially there is no location set in the bigquery options
    assert not bpd.options.bigquery.location

    # Explicitly set location
    bpd.options.bigquery.location = tokyo_location
    assert bpd.options.bigquery.location == tokyo_location

    # Starting user journey with read_gbq* from another location should fail
    with pytest.raises(
        (google.api_core.exceptions.NotFound, ValueError),
        match=dataset_id_permanent,
    ):
        read_method(query)

    # Starting user journey with read_gbq* should work for a table in the same
    # location, in this case tokyo
    df = read_method(query_tokyo)
    assert df is not None


def test_close_session_after_credentials_need_reauthentication(monkeypatch):
    # Use a simple test query to verify that default session works to interact
    # with BQ
    test_query = "SELECT 1"

    # Confirm that default session has BQ client with valid credentials
    session = bpd.get_global_session()
    assert session.bqclient._credentials.valid

    # Confirm that default session works as usual
    df = bpd.read_gbq(test_query)
    assert df is not None

    with monkeypatch.context() as m:
        # Simulate expired credentials to trigger the credential refresh flow
        m.setattr(session.bqclient._credentials, "expiry", datetime.datetime.utcnow())
        assert not session.bqclient._credentials.valid

        # Simulate an exception during the credential refresh flow
        m.setattr(
            session.bqclient._credentials,
            "refresh",
            mock.Mock(side_effect=google.auth.exceptions.RefreshError()),
        )

        # Confirm that session is unusable to run any jobs
        with pytest.raises(google.auth.exceptions.RefreshError):
            query_job = session.bqclient.query(test_query)
            query_job.result()  # blocks until finished

        # Confirm that as a result bigframes.pandas interface is unusable
        with pytest.raises(google.auth.exceptions.RefreshError):
            bpd.read_gbq(test_query)

        # Now verify that closing the session works
        bpd.close_session()
        assert bigframes.core.global_session._global_session is None

    # Now verify that use is able to start over
    df = bpd.read_gbq(test_query)
    assert df is not None
