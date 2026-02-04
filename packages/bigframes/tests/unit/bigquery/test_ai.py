# Copyright 2025 Google LLC
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

import pandas as pd
import pytest

import bigframes.bigquery as bbq
import bigframes.dataframe
import bigframes.series
import bigframes.session


@pytest.fixture
def mock_session():
    return mock.create_autospec(spec=bigframes.session.Session)


@pytest.fixture
def mock_dataframe(mock_session):
    df = mock.create_autospec(spec=bigframes.dataframe.DataFrame)
    df._session = mock_session
    df.sql = "SELECT * FROM my_table"
    return df


@pytest.fixture
def mock_series(mock_session):
    series = mock.create_autospec(spec=bigframes.series.Series)
    series._session = mock_session
    # Mock to_frame to return a mock dataframe
    df = mock.create_autospec(spec=bigframes.dataframe.DataFrame)
    df._session = mock_session
    df.sql = "SELECT my_col AS content FROM my_table"
    series.copy.return_value = series
    series.to_frame.return_value = df
    return series


def test_generate_embedding_with_dataframe(mock_dataframe, mock_session):
    model_name = "project.dataset.model"

    bbq.ai.generate_embedding(
        model_name,
        mock_dataframe,
        output_dimensionality=256,
    )

    mock_session.read_gbq.assert_called_once()
    query = mock_session.read_gbq.call_args[0][0]

    # Normalize whitespace for comparison
    query = " ".join(query.split())

    expected_part_1 = "SELECT * FROM AI.GENERATE_EMBEDDING("
    expected_part_2 = f"MODEL `{model_name}`,"
    expected_part_3 = "(SELECT * FROM my_table),"
    expected_part_4 = "STRUCT(256 AS OUTPUT_DIMENSIONALITY)"

    assert expected_part_1 in query
    assert expected_part_2 in query
    assert expected_part_3 in query
    assert expected_part_4 in query


def test_generate_embedding_with_series(mock_series, mock_session):
    model_name = "project.dataset.model"

    bbq.ai.generate_embedding(
        model_name, mock_series, start_second=0.0, end_second=10.0, interval_seconds=5.0
    )

    mock_session.read_gbq.assert_called_once()
    query = mock_session.read_gbq.call_args[0][0]
    query = " ".join(query.split())

    assert f"MODEL `{model_name}`" in query
    assert "(SELECT my_col AS content FROM my_table)" in query
    assert (
        "STRUCT(0.0 AS START_SECOND, 10.0 AS END_SECOND, 5.0 AS INTERVAL_SECONDS)"
        in query
    )


def test_generate_embedding_defaults(mock_dataframe, mock_session):
    model_name = "project.dataset.model"

    bbq.ai.generate_embedding(
        model_name,
        mock_dataframe,
    )

    mock_session.read_gbq.assert_called_once()
    query = mock_session.read_gbq.call_args[0][0]
    query = " ".join(query.split())

    assert f"MODEL `{model_name}`" in query
    assert "STRUCT()" in query


@mock.patch("bigframes.pandas.read_pandas")
def test_generate_embedding_with_pandas_dataframe(
    read_pandas_mock, mock_dataframe, mock_session
):
    # This tests that pandas input path works and calls read_pandas
    model_name = "project.dataset.model"

    # Mock return value of read_pandas to be a BigFrames DataFrame
    read_pandas_mock.return_value = mock_dataframe

    pandas_df = pd.DataFrame({"content": ["test"]})

    bbq.ai.generate_embedding(
        model_name,
        pandas_df,
    )

    read_pandas_mock.assert_called_once()
    # Check that read_pandas was called with something (the pandas df)
    assert read_pandas_mock.call_args[0][0] is pandas_df

    mock_session.read_gbq.assert_called_once()
