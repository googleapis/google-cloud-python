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

import bigframes.dataframe
import bigframes.pandas.io.api as bf_io_api
import bigframes.session


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
