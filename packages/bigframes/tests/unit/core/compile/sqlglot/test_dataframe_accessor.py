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
