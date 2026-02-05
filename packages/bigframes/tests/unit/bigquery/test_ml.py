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
from __future__ import annotations

from unittest import mock

import pandas as pd
import pytest

import bigframes.bigquery._operations.ml as ml_ops
import bigframes.session


@pytest.fixture
def mock_session():
    return mock.create_autospec(spec=bigframes.session.Session)


MODEL_SERIES = pd.Series(
    {
        "modelReference": {
            "projectId": "test-project",
            "datasetId": "test-dataset",
            "modelId": "test-model",
        }
    }
)

MODEL_NAME = "test-project.test-dataset.test-model"


@mock.patch("bigframes.bigquery._operations.ml._get_model_metadata")
@mock.patch("bigframes.pandas.read_pandas")
def test_create_model_with_pandas_dataframe(
    read_pandas_mock, _get_model_metadata_mock, mock_session
):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.create_model("model_name", training_data=df, session=mock_session)
    read_pandas_mock.assert_called_once()
    mock_session.read_gbq_query.assert_called_once()
    generated_sql = mock_session.read_gbq_query.call_args[0][0]
    assert "CREATE MODEL `model_name`" in generated_sql
    assert "AS SELECT * FROM `pandas_df`" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
@mock.patch("bigframes.pandas.read_pandas")
def test_evaluate_with_pandas_dataframe(read_pandas_mock, read_gbq_query_mock):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.evaluate(MODEL_SERIES, input_=df)
    read_pandas_mock.assert_called_once()
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.EVALUATE" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql
    assert "(SELECT * FROM `pandas_df`)" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
@mock.patch("bigframes.pandas.read_pandas")
def test_predict_with_pandas_dataframe(read_pandas_mock, read_gbq_query_mock):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.predict(MODEL_SERIES, input_=df)
    read_pandas_mock.assert_called_once()
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.PREDICT" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql
    assert "(SELECT * FROM `pandas_df`)" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
@mock.patch("bigframes.pandas.read_pandas")
def test_explain_predict_with_pandas_dataframe(read_pandas_mock, read_gbq_query_mock):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.explain_predict(MODEL_SERIES, input_=df)
    read_pandas_mock.assert_called_once()
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.EXPLAIN_PREDICT" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql
    assert "(SELECT * FROM `pandas_df`)" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
def test_global_explain_with_pandas_series_model(read_gbq_query_mock):
    ml_ops.global_explain(MODEL_SERIES)
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.GLOBAL_EXPLAIN" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
@mock.patch("bigframes.pandas.read_pandas")
def test_transform_with_pandas_dataframe(read_pandas_mock, read_gbq_query_mock):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.transform(MODEL_SERIES, input_=df)
    read_pandas_mock.assert_called_once()
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.TRANSFORM" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql
    assert "(SELECT * FROM `pandas_df`)" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
@mock.patch("bigframes.pandas.read_pandas")
def test_generate_text_with_pandas_dataframe(read_pandas_mock, read_gbq_query_mock):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.generate_text(
        MODEL_SERIES,
        input_=df,
        temperature=0.5,
        max_output_tokens=128,
        top_k=20,
        top_p=0.9,
        flatten_json_output=True,
        stop_sequences=["a", "b"],
        ground_with_google_search=True,
        request_type="TYPE",
    )
    read_pandas_mock.assert_called_once()
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.GENERATE_TEXT" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql
    assert "(SELECT * FROM `pandas_df`)" in generated_sql
    assert "STRUCT(0.5 AS temperature" in generated_sql
    assert "128 AS max_output_tokens" in generated_sql
    assert "20 AS top_k" in generated_sql
    assert "0.9 AS top_p" in generated_sql
    assert "true AS flatten_json_output" in generated_sql
    assert "['a', 'b'] AS stop_sequences" in generated_sql
    assert "true AS ground_with_google_search" in generated_sql
    assert "'TYPE' AS request_type" in generated_sql


@mock.patch("bigframes.pandas.read_gbq_query")
@mock.patch("bigframes.pandas.read_pandas")
def test_generate_embedding_with_pandas_dataframe(
    read_pandas_mock, read_gbq_query_mock
):
    df = pd.DataFrame({"col1": [1, 2, 3]})
    read_pandas_mock.return_value._to_sql_query.return_value = (
        "SELECT * FROM `pandas_df`",
        [],
        [],
    )
    ml_ops.generate_embedding(
        MODEL_SERIES,
        input_=df,
        flatten_json_output=True,
        task_type="RETRIEVAL_DOCUMENT",
        output_dimensionality=256,
    )
    read_pandas_mock.assert_called_once()
    read_gbq_query_mock.assert_called_once()
    generated_sql = read_gbq_query_mock.call_args[0][0]
    assert "ML.GENERATE_EMBEDDING" in generated_sql
    assert f"MODEL `{MODEL_NAME}`" in generated_sql
    assert "(SELECT * FROM `pandas_df`)" in generated_sql
    assert "true AS flatten_json_output" in generated_sql
    assert "'RETRIEVAL_DOCUMENT' AS task_type" in generated_sql
    assert "256 AS output_dimensionality" in generated_sql
