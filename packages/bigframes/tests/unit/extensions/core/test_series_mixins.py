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

import unittest.mock as mock

import pandas as pd

import bigframes.bigquery.ai
import bigframes.pandas as bpd
import bigframes.session


def test_ai_generate_embedding(monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    bf_series = mock.create_autospec(bpd.Series)
    session.read_pandas.return_value = bf_series

    mock_generate_embedding = mock.MagicMock()
    result_df = mock.create_autospec(bpd.DataFrame)
    mock_generate_embedding.return_value = result_df
    expected_result = mock.create_autospec(pd.DataFrame)
    result_df.to_pandas.return_value = expected_result

    monkeypatch.setattr(
        bigframes.bigquery.ai, "generate_embedding", mock_generate_embedding
    )

    series = pd.Series(["apple"], name="content")
    actual_result = series.bigquery.ai.generate_embedding(  # type: ignore
        model="my_model",
        output_dimensionality=256,
        task_type="retrieval_document",
        start_second=1.0,
        end_second=2.0,
        interval_seconds=3.0,
        trial_id=4,
        session=session,
    )

    session.read_pandas.assert_called_once()
    mock_generate_embedding.assert_called_once_with(
        "my_model",
        bf_series,
        output_dimensionality=256,
        task_type="retrieval_document",
        start_second=1.0,
        end_second=2.0,
        interval_seconds=3.0,
        trial_id=4,
    )
    result_df.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate_embedding(scalar_types_df: bpd.DataFrame, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    result_df = mock.create_autospec(bpd.DataFrame)

    mock_generate_embedding = mock.MagicMock()
    mock_generate_embedding.return_value = result_df

    monkeypatch.setattr(
        bigframes.bigquery.ai, "generate_embedding", mock_generate_embedding
    )

    scalar_types_series = scalar_types_df["string_col"]
    actual_result = scalar_types_series.bigquery.ai.generate_embedding(
        model="my_model",
        output_dimensionality=256,
        session=session,
    )

    session.read_pandas.assert_not_called()
    mock_generate_embedding.assert_called_once()
    args, kwargs = mock_generate_embedding.call_args
    assert args[0] == "my_model"
    assert args[1] is scalar_types_series
    assert kwargs == {
        "output_dimensionality": 256,
        "task_type": None,
        "start_second": None,
        "end_second": None,
        "interval_seconds": None,
        "trial_id": None,
    }
    result_df.to_pandas.assert_not_called()
    assert actual_result is result_df


def test_ai_generate_text(monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    bf_series = mock.create_autospec(bpd.Series)
    session.read_pandas.return_value = bf_series

    mock_generate_text = mock.MagicMock()
    result_df = mock.create_autospec(bpd.DataFrame)
    mock_generate_text.return_value = result_df
    expected_result = mock.create_autospec(pd.DataFrame)
    result_df.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_text", mock_generate_text)

    series = pd.Series(["write a poem"], name="prompt")
    actual_result = series.bigquery.ai.generate_text(  # type: ignore
        model="my_model",
        temperature=0.7,
        max_output_tokens=100,
        top_k=50,
        top_p=0.9,
        stop_sequences=["\n"],
        ground_with_google_search=True,
        request_type="dedicated",
        session=session,
    )

    session.read_pandas.assert_called_once()
    mock_generate_text.assert_called_once_with(
        "my_model",
        bf_series,
        temperature=0.7,
        max_output_tokens=100,
        top_k=50,
        top_p=0.9,
        stop_sequences=["\n"],
        ground_with_google_search=True,
        request_type="dedicated",
    )
    result_df.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate_text(scalar_types_df: bpd.DataFrame, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    result_df = mock.create_autospec(bpd.DataFrame)

    mock_generate_text = mock.MagicMock()
    mock_generate_text.return_value = result_df

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_text", mock_generate_text)

    scalar_types_series = scalar_types_df["string_col"]
    actual_result = scalar_types_series.bigquery.ai.generate_text(
        model="my_model",
        temperature=0.7,
        session=session,
    )

    session.read_pandas.assert_not_called()
    mock_generate_text.assert_called_once()
    args, kwargs = mock_generate_text.call_args
    assert args[0] == "my_model"
    assert args[1] is scalar_types_series
    assert kwargs == {
        "temperature": 0.7,
        "max_output_tokens": None,
        "top_k": None,
        "top_p": None,
        "stop_sequences": None,
        "ground_with_google_search": None,
        "request_type": None,
    }
    result_df.to_pandas.assert_not_called()
    assert actual_result is result_df


def test_ai_generate_table(monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    bf_series = mock.create_autospec(bpd.Series)
    session.read_pandas.return_value = bf_series

    mock_generate_table = mock.MagicMock()
    result_df = mock.create_autospec(bpd.DataFrame)
    mock_generate_table.return_value = result_df
    expected_result = mock.create_autospec(pd.DataFrame)
    result_df.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_table", mock_generate_table)

    series = pd.Series(["generate something"], name="prompt")
    actual_result = series.bigquery.ai.generate_table(  # type: ignore
        model="my_model",
        output_schema="category STRING",
        temperature=0.7,
        top_p=0.9,
        max_output_tokens=100,
        stop_sequences=["\n"],
        request_type="dedicated",
        session=session,
    )

    session.read_pandas.assert_called_once()
    mock_generate_table.assert_called_once_with(
        "my_model",
        bf_series,
        output_schema="category STRING",
        temperature=0.7,
        top_p=0.9,
        max_output_tokens=100,
        stop_sequences=["\n"],
        request_type="dedicated",
    )
    result_df.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate_table(scalar_types_df: bpd.DataFrame, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    result_df = mock.create_autospec(bpd.DataFrame)

    mock_generate_table = mock.MagicMock()
    mock_generate_table.return_value = result_df

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_table", mock_generate_table)

    scalar_types_series = scalar_types_df["string_col"]
    actual_result = scalar_types_series.bigquery.ai.generate_table(
        model="my_model",
        output_schema="category STRING",
        temperature=0.7,
        session=session,
    )

    session.read_pandas.assert_not_called()
    mock_generate_table.assert_called_once()
    args, kwargs = mock_generate_table.call_args
    assert args[0] == "my_model"
    assert args[1] is scalar_types_series
    assert kwargs == {
        "output_schema": "category STRING",
        "temperature": 0.7,
        "top_p": None,
        "max_output_tokens": None,
        "stop_sequences": None,
        "request_type": None,
    }
    result_df.to_pandas.assert_not_called()
    assert actual_result is result_df


def test_ai_embed(monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    bf_series = mock.create_autospec(bpd.Series)
    session.read_pandas.return_value = bf_series

    mock_embed = mock.MagicMock()
    result_series = mock.create_autospec(bpd.Series)
    mock_embed.return_value = result_series
    expected_result = mock.create_autospec(pd.Series)
    result_series.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "embed", mock_embed)

    series = pd.Series(["hello world"], name="content")
    actual_result = series.bigquery.ai.embed(  # type: ignore
        endpoint="my_endpoint",
        model="my_model",
        task_type="retrieval_query",
        title="my_title",
        model_params={"key": "val"},
        connection_id="my_connection",
        session=session,
    )

    session.read_pandas.assert_called_once()
    mock_embed.assert_called_once_with(
        bf_series,
        endpoint="my_endpoint",
        model="my_model",
        task_type="retrieval_query",
        title="my_title",
        model_params={"key": "val"},
        connection_id="my_connection",
    )
    result_series.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_embed(scalar_types_df: bpd.DataFrame, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    result_series = mock.create_autospec(bpd.Series)

    mock_embed = mock.MagicMock()
    mock_embed.return_value = result_series

    monkeypatch.setattr(bigframes.bigquery.ai, "embed", mock_embed)

    scalar_types_series = scalar_types_df["string_col"]
    actual_result = scalar_types_series.bigquery.ai.embed(
        endpoint="my_endpoint",
        session=session,
    )

    session.read_pandas.assert_not_called()
    mock_embed.assert_called_once()
    args, kwargs = mock_embed.call_args
    assert args[0] is scalar_types_series
    assert kwargs == {
        "endpoint": "my_endpoint",
        "model": None,
        "task_type": None,
        "title": None,
        "model_params": None,
        "connection_id": None,
    }
    result_series.to_pandas.assert_not_called()
    assert actual_result is result_series


def test_ai_similarity(monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    bf_series = mock.create_autospec(bpd.Series)
    session.read_pandas.return_value = bf_series

    mock_similarity = mock.MagicMock()
    result_series = mock.create_autospec(bpd.Series)
    mock_similarity.return_value = result_series
    expected_result = mock.create_autospec(pd.Series)
    result_series.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "similarity", mock_similarity)

    series = pd.Series(["apple"], name="content")
    actual_result = series.bigquery.ai.similarity(  # type: ignore
        "banana",
        endpoint="my_endpoint",
        model="my_model",
        model_params={"key": "val"},
        connection_id="my_connection",
        session=session,
    )

    session.read_pandas.assert_called_once()
    mock_similarity.assert_called_once_with(
        bf_series,
        "banana",
        endpoint="my_endpoint",
        model="my_model",
        model_params={"key": "val"},
        connection_id="my_connection",
    )
    result_series.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_similarity(scalar_types_df: bpd.DataFrame, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    result_series = mock.create_autospec(bpd.Series)

    mock_similarity = mock.MagicMock()
    mock_similarity.return_value = result_series

    monkeypatch.setattr(bigframes.bigquery.ai, "similarity", mock_similarity)

    scalar_types_series = scalar_types_df["string_col"]
    actual_result = scalar_types_series.bigquery.ai.similarity(
        "other_text",
        endpoint="my_endpoint",
        session=session,
    )

    session.read_pandas.assert_not_called()
    mock_similarity.assert_called_once()
    args, kwargs = mock_similarity.call_args
    assert args[0] is scalar_types_series
    assert args[1] == "other_text"
    assert kwargs == {
        "endpoint": "my_endpoint",
        "model": None,
        "model_params": None,
        "connection_id": None,
    }
    result_series.to_pandas.assert_not_called()
    assert actual_result is result_series
