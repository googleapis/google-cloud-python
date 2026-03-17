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
import pytest

import bigframes.pandas as bpd
import bigframes.session

pytest.importorskip("pytest_snapshot")


def test_sql_scalar(scalar_types_df: bpd.DataFrame, snapshot, monkeypatch):
    session = mock.create_autospec(bigframes.session.Session)
    session.read_pandas.return_value = scalar_types_df

    def to_pandas(series, *, ordered):
        assert ordered is True
        sql, _, _ = series.to_frame()._to_sql_query(include_index=True)
        return sql

    monkeypatch.setattr(bpd.Series, "to_pandas", to_pandas)

    df = pd.DataFrame({"int64_col": [1, 2], "int64_too": [3, 4]})
    result = df.bigquery.sql_scalar(
        "ROUND({int64_col} + {int64_too})",
        output_dtype=pd.Int64Dtype(),
        session=session,
    )

    session.read_pandas.assert_called_once()
    snapshot.assert_match(result, "out.sql")


def test_ai_forecast(snapshot, monkeypatch):
    import bigframes.bigquery.ai
    import bigframes.session

    session = mock.create_autospec(bigframes.session.Session)
    bf_df = mock.create_autospec(bpd.DataFrame)
    session.read_pandas.return_value = bf_df

    def mock_ai_forecast(df, **kwargs):
        assert df is bf_df
        result_df = mock.create_autospec(bpd.DataFrame)
        result_df.to_pandas.return_value = kwargs
        return result_df

    import bigframes.bigquery.ai

    monkeypatch.setattr(bigframes.bigquery.ai, "forecast", mock_ai_forecast)

    df = pd.DataFrame({"date": ["2020-01-01"], "value": [1.0]})
    result = df.bigquery.ai.forecast(
        timestamp_col="date",
        data_col="value",
        horizon=5,
        session=session,
    )

    session.read_pandas.assert_called_once()
    assert result == {
        "timestamp_col": "date",
        "data_col": "value",
        "model": "TimesFM 2.0",
        "id_cols": None,
        "horizon": 5,
        "confidence_level": 0.95,
        "context_window": None,
        "output_historical_time_series": False,
    }
