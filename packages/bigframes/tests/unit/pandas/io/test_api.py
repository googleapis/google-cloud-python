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

from unittest import mock

import google.cloud.bigquery
import pytest

import bigframes.dataframe
import bigframes.pandas
import bigframes.pandas.io.api as bf_io_api
import bigframes.session
import bigframes.session.clients

# _read_gbq_colab requires the polars engine.
pytest.importorskip("polars")


@mock.patch(
    "bigframes.pandas.io.api._set_default_session_location_if_possible_deferred_query"
)
@mock.patch("bigframes.core.global_session.with_default_session")
def test_read_gbq_colab_dry_run_doesnt_call_set_location(
    mock_with_default_session, mock_set_location
):
    """
    Ensure that we don't bind to a location too early. If it's a dry run, the
    user might not be done typing.
    """
    mock_df = mock.create_autospec(bigframes.dataframe.DataFrame)
    mock_with_default_session.return_value = mock_df

    query_or_table = "SELECT {param1} AS param1"
    sample_pyformat_args = {"param1": "value1"}
    bf_io_api._read_gbq_colab(
        query_or_table, pyformat_args=sample_pyformat_args, dry_run=True
    )

    mock_set_location.assert_not_called()


@mock.patch("bigframes._config.auth.get_default_credentials_with_project")
@mock.patch("bigframes.core.global_session.with_default_session")
def test_read_gbq_colab_dry_run_doesnt_authenticate_multiple_times(
    mock_with_default_session, mock_get_credentials, monkeypatch
):
    """
    Ensure that we authenticate too often, which is an expensive operation,
    performance-wise (2+ seconds).
    """
    bigframes.pandas.close_session()

    mock_get_credentials.return_value = (mock.Mock(), "unit-test-project")
    mock_create_bq_client = mock.Mock()
    mock_bq_client = mock.create_autospec(google.cloud.bigquery.Client, instance=True)
    mock_create_bq_client.return_value = mock_bq_client
    mock_query_job = mock.create_autospec(google.cloud.bigquery.QueryJob, instance=True)
    type(mock_query_job).schema = mock.PropertyMock(return_value=[])
    mock_query_job._properties = {}
    mock_bq_client.query.return_value = mock_query_job
    monkeypatch.setattr(
        bigframes.session.clients.ClientsProvider,
        "_create_bigquery_client",
        mock_create_bq_client,
    )
    mock_df = mock.create_autospec(bigframes.dataframe.DataFrame)
    mock_with_default_session.return_value = mock_df

    query_or_table = "SELECT {param1} AS param1"
    sample_pyformat_args = {"param1": "value1"}
    bf_io_api._read_gbq_colab(
        query_or_table, pyformat_args=sample_pyformat_args, dry_run=True
    )

    mock_with_default_session.assert_not_called()
    mock_get_credentials.reset_mock()

    # Repeat the operation so that the credentials would have have been cached.
    bf_io_api._read_gbq_colab(
        query_or_table, pyformat_args=sample_pyformat_args, dry_run=True
    )
    mock_get_credentials.assert_not_called()


@mock.patch(
    "bigframes.pandas.io.api._set_default_session_location_if_possible_deferred_query"
)
@mock.patch("bigframes.core.global_session.with_default_session")
def test_read_gbq_colab_calls_set_location(
    mock_with_default_session, mock_set_location
):
    # Configure the mock for with_default_session to return a DataFrame mock
    mock_df = mock.create_autospec(bigframes.dataframe.DataFrame)
    mock_with_default_session.return_value = mock_df

    query_or_table = "SELECT {param1} AS param1"
    sample_pyformat_args = {"param1": "value1"}
    result = bf_io_api._read_gbq_colab(
        query_or_table, pyformat_args=sample_pyformat_args, dry_run=False
    )

    # Make sure that we format the SQL first to prevent syntax errors.
    formatted_query = "SELECT 'value1' AS param1"
    mock_set_location.assert_called_once()
    args, _ = mock_set_location.call_args
    assert formatted_query == args[0]()
    mock_with_default_session.assert_called_once()

    # Check the actual arguments passed to with_default_session
    args, kwargs = mock_with_default_session.call_args
    assert args[0] == bigframes.session.Session._read_gbq_colab
    assert args[1] == query_or_table
    assert kwargs["pyformat_args"] == sample_pyformat_args
    assert not kwargs["dry_run"]
    assert isinstance(result, bigframes.dataframe.DataFrame)
