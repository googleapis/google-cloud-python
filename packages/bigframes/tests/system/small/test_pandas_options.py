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
import re
from unittest import mock
import warnings

import google.api_core.exceptions
import pandas.testing
import pytest

import bigframes.exceptions
import bigframes.pandas as bpd


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
    reset_default_session_and_location,
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
    # location, in this case tokyo.
    with warnings.catch_warnings():
        # Since the query refers to a specific location, no warning should be
        # raised.
        warnings.simplefilter("error", bigframes.exceptions.DefaultLocationWarning)
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

    # Close the global session to start over.
    # Note: This is a thread-local operation because of the
    # reset_default_session_and_location fixture above.
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
    reset_default_session_and_location,
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
    with pytest.warns(
        bigframes.exceptions.DefaultLocationWarning,
        match=re.escape("using location US for the session"),
    ):
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
    reset_default_session_and_location,
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
    reset_default_session_and_location,
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


def test_credentials_need_reauthentication(
    monkeypatch, reset_default_session_and_location
):
    # Use a simple test query to verify that default session works to interact
    # with BQ.
    test_query = "SELECT 1"

    # Confirm that default session works as usual
    df = bpd.read_gbq(test_query)
    assert df is not None

    # Call get_global_session() *after* read_gbq so that our location detection
    # has a chance to work.
    session = bpd.get_global_session()
    assert session.bqclient._http.credentials.valid

    with monkeypatch.context() as m:
        # Simulate expired credentials to trigger the credential refresh flow
        m.setattr(
            session.bqclient._http.credentials, "expiry", datetime.datetime.utcnow()
        )
        assert not session.bqclient._http.credentials.valid

        # Simulate an exception during the credential refresh flow
        m.setattr(
            session.bqclient._http.credentials,
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

        # Now verify that closing the session works We look at the
        # thread-local session because of the
        # reset_default_session_and_location fixture and that this test mutates
        # state that might otherwise be used by tests running in parallel.
        assert (
            bigframes.core.global_session._global_session_state.thread_local_session
            is not None
        )

        with warnings.catch_warnings(record=True) as warned:
            bpd.close_session()  # CleanupFailedWarning: can't clean up

        assert len(warned) == 1
        assert warned[0].category == bigframes.exceptions.CleanupFailedWarning

        assert (
            bigframes.core.global_session._global_session_state.thread_local_session
            is None
        )

    # Now verify that use is able to start over
    df = bpd.read_gbq(test_query)
    assert df is not None


def test_max_rows_normal_execution_within_limit(
    scalars_df_index, scalars_pandas_df_index
):
    """Test queries execute normally when the number of rows is within the limit."""
    with bpd.option_context("compute.maximum_result_rows", 10):
        df = scalars_df_index.head(10)
        result = df.to_pandas()

    expected = scalars_pandas_df_index.head(10)
    pandas.testing.assert_frame_equal(result, expected)

    with bpd.option_context("compute.maximum_result_rows", 10), bpd.option_context(
        "display.repr_mode", "head"
    ):
        df = scalars_df_index.head(10)
        assert repr(df) is not None

    # We should be able to get away with only a single row for shape.
    with bpd.option_context("compute.maximum_result_rows", 1):
        shape = scalars_df_index.shape
        assert shape == scalars_pandas_df_index.shape

    # 0 is not recommended, as it would stop aggregations and many other
    # necessary operations, but we shouldn't need even 1 row for to_gbq().
    with bpd.option_context("compute.maximum_result_rows", 0):
        destination = scalars_df_index.to_gbq()
        assert destination is not None


def test_max_rows_exceeds_limit(scalars_df_index):
    """Test to_pandas() raises MaximumRowsDownloadedExceeded when the limit is exceeded."""
    with bpd.option_context("compute.maximum_result_rows", 5), pytest.raises(
        bigframes.exceptions.MaximumResultRowsExceeded, match="5"
    ):
        scalars_df_index.to_pandas()

    with bpd.option_context("compute.maximum_result_rows", 5), pytest.raises(
        bigframes.exceptions.MaximumResultRowsExceeded, match="5"
    ):
        next(iter(scalars_df_index.to_pandas_batches()))
