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


def test_ai_forecast(monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    bf_df = mock.create_autospec(bpd.DataFrame)
    session.read_pandas.return_value = bf_df

    mock_forecast = mock.MagicMock()
    forecast_result_df = mock.create_autospec(bpd.DataFrame)
    mock_forecast.return_value = forecast_result_df
    expected_result = mock.create_autospec(pd.DataFrame)
    forecast_result_df.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "forecast", mock_forecast)

    df = pd.DataFrame({"date": ["2020-01-01"], "value": [1.0]})
    actual_result = df.bigquery.ai.forecast(
        timestamp_col="date",
        data_col="value",
        horizon=5,
        session=session,
    )

    session.read_pandas.assert_called_once()

    mock_forecast.assert_called_once_with(
        bf_df,
        timestamp_col="date",
        data_col="value",
        model="TimesFM 2.0",
        id_cols=None,
        horizon=5,
        confidence_level=0.95,
        context_window=None,
        output_historical_time_series=False,
    )
    forecast_result_df.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_forecast(scalar_types_df: bpd.DataFrame, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    forecast_result = mock.create_autospec(bpd.DataFrame)
    mock_forecast = mock.MagicMock()
    mock_forecast.return_value = forecast_result

    monkeypatch.setattr(bigframes.bigquery.ai, "forecast", mock_forecast)

    actual_result = scalar_types_df.bigquery.ai.forecast(
        timestamp_col="date",
        data_col="value",
        horizon=5,
        session=session,
    )

    session.read_pandas.assert_not_called()
    mock_forecast.assert_called_once()
    args, kwargs = mock_forecast.call_args
    assert args[0] is scalar_types_df
    assert kwargs == {
        "timestamp_col": "date",
        "data_col": "value",
        "model": "TimesFM 2.0",
        "id_cols": None,
        "horizon": 5,
        "confidence_level": 0.95,
        "context_window": None,
        "output_historical_time_series": False,
    }
    # BigFrames accessor returns the bf_df directly without calling to_pandas
    forecast_result.to_pandas.assert_not_called()
    assert actual_result is forecast_result


def test_ai_generate(monkeypatch):
    mock_generate = mock.MagicMock()
    result_series = mock.create_autospec(bpd.Series)
    mock_generate.return_value = result_series
    expected_result = mock.create_autospec(pd.Series)
    result_series.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "generate", mock_generate)

    prompt = mock.create_autospec(pd.Series)
    df = pd.DataFrame({"text_input": ["Is this a positive review?"]})
    actual_result = df.bigquery.ai.generate(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
        output_schema={"res": "STRING"},
    )

    mock_generate.assert_called_once_with(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
        output_schema={"res": "STRING"},
    )
    result_series.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate(scalar_types_df: bpd.DataFrame, monkeypatch):
    bf_series = mock.create_autospec(bpd.Series)
    result_series = mock.create_autospec(bpd.Series)

    mock_generate = mock.MagicMock()
    mock_generate.return_value = result_series

    monkeypatch.setattr(bigframes.bigquery.ai, "generate", mock_generate)

    actual_result = scalar_types_df.bigquery.ai.generate(
        bf_series,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
        output_schema={"res": "STRING"},
    )

    mock_generate.assert_called_once()
    args, kwargs = mock_generate.call_args
    assert args[0] is bf_series
    assert kwargs == {
        "connection_id": "conn",
        "endpoint": "endpoint",
        "request_type": "dedicated",
        "model_params": {"temp": 0.5},
        "output_schema": {"res": "STRING"},
    }
    result_series.to_pandas.assert_not_called()
    assert actual_result is result_series


def test_ai_generate_bool(monkeypatch):
    mock_generate_bool = mock.MagicMock()
    result_series = mock.create_autospec(bpd.Series)
    mock_generate_bool.return_value = result_series
    expected_result = mock.create_autospec(pd.Series)
    result_series.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_bool", mock_generate_bool)

    prompt = mock.create_autospec(pd.Series)
    df = pd.DataFrame({"text_input": ["Is this a positive review?"]})
    actual_result = df.bigquery.ai.generate_bool(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )

    mock_generate_bool.assert_called_once_with(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )
    result_series.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate_bool(scalar_types_df: bpd.DataFrame, monkeypatch):
    bf_series = mock.create_autospec(bpd.Series)
    result_series = mock.create_autospec(bpd.Series)

    mock_generate_bool = mock.MagicMock()
    mock_generate_bool.return_value = result_series

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_bool", mock_generate_bool)

    actual_result = scalar_types_df.bigquery.ai.generate_bool(
        bf_series,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )

    mock_generate_bool.assert_called_once()
    args, kwargs = mock_generate_bool.call_args
    assert args[0] is bf_series
    assert kwargs == {
        "connection_id": "conn",
        "endpoint": "endpoint",
        "request_type": "dedicated",
        "model_params": {"temp": 0.5},
    }
    result_series.to_pandas.assert_not_called()
    assert actual_result is result_series


def test_ai_generate_int(monkeypatch):
    mock_generate_int = mock.MagicMock()
    result_series = mock.create_autospec(bpd.Series)
    mock_generate_int.return_value = result_series
    expected_result = mock.create_autospec(pd.Series)
    result_series.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_int", mock_generate_int)

    prompt = mock.create_autospec(pd.Series)
    df = pd.DataFrame({"text_input": ["How many legs?"]})
    actual_result = df.bigquery.ai.generate_int(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )

    mock_generate_int.assert_called_once_with(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )
    result_series.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate_int(scalar_types_df: bpd.DataFrame, monkeypatch):
    bf_series = mock.create_autospec(bpd.Series)
    result_series = mock.create_autospec(bpd.Series)

    mock_generate_int = mock.MagicMock()
    mock_generate_int.return_value = result_series

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_int", mock_generate_int)

    actual_result = scalar_types_df.bigquery.ai.generate_int(
        bf_series,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )

    mock_generate_int.assert_called_once()
    args, kwargs = mock_generate_int.call_args
    assert args[0] is bf_series
    assert kwargs == {
        "connection_id": "conn",
        "endpoint": "endpoint",
        "request_type": "dedicated",
        "model_params": {"temp": 0.5},
    }
    result_series.to_pandas.assert_not_called()
    assert actual_result is result_series


def test_ai_generate_double(monkeypatch):
    mock_generate_double = mock.MagicMock()
    result_series = mock.create_autospec(bpd.Series)
    mock_generate_double.return_value = result_series
    expected_result = mock.create_autospec(pd.Series)
    result_series.to_pandas.return_value = expected_result

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_double", mock_generate_double)

    prompt = mock.create_autospec(pd.Series)
    df = pd.DataFrame({"text_input": ["How tall?"]})
    actual_result = df.bigquery.ai.generate_double(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )

    mock_generate_double.assert_called_once_with(
        prompt,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )
    result_series.to_pandas.assert_called_once()
    assert actual_result is expected_result


def test_bigframes_ai_generate_double(scalar_types_df: bpd.DataFrame, monkeypatch):
    bf_series = mock.create_autospec(bpd.Series)
    result_series = mock.create_autospec(bpd.Series)

    mock_generate_double = mock.MagicMock()
    mock_generate_double.return_value = result_series

    monkeypatch.setattr(bigframes.bigquery.ai, "generate_double", mock_generate_double)

    actual_result = scalar_types_df.bigquery.ai.generate_double(
        bf_series,
        connection_id="conn",
        endpoint="endpoint",
        request_type="dedicated",
        model_params={"temp": 0.5},
    )

    mock_generate_double.assert_called_once()
    args, kwargs = mock_generate_double.call_args
    assert args[0] is bf_series
    assert kwargs == {
        "connection_id": "conn",
        "endpoint": "endpoint",
        "request_type": "dedicated",
        "model_params": {"temp": 0.5},
    }
    result_series.to_pandas.assert_not_called()
    assert actual_result is result_series
