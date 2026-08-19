# Copyright 2026 Google LLC
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

import pytest
from google.cloud import bigquery

import bigframes.session
from bigframes.ml import llm


def test_gemini_text_generator_default_model():
    mock_session = mock.create_autospec(spec=bigframes.session.Session)
    mock_session._create_bq_connection.return_value = (
        "projects/test-project/locations/us-central1/connections/test-conn"
    )
    mock_session._anonymous_dataset = bigquery.DatasetReference(
        "test-project", "test_dataset"
    )
    mock_job = mock.MagicMock()
    mock_job.destination.project = "test-project"
    mock_job.destination.dataset_id = "test_dataset"
    mock_job.destination.table_id = "test_model"
    mock_session._start_query_ml_ddl.return_value = (None, mock_job)
    mock_session.bqclient.get_model.return_value = mock.MagicMock(spec=bigquery.Model)

    with pytest.warns(
        FutureWarning, match="default model will be removed in BigFrames 3.0"
    ):
        model = llm.GeminiTextGenerator(
            session=mock_session,
            connection_name="test-conn",
        )

    assert model.model_name == "gemini-2.5-flash"
    mock_session._start_query_ml_ddl.assert_called_once()
    generated_sql = mock_session._start_query_ml_ddl.call_args[0][0]
    assert "gemini-2.5-flash" in generated_sql
