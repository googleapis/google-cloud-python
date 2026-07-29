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

from typing import cast
from unittest import mock

import bigframes.core.tools.datetimes
import bigframes.dtypes
import bigframes.pandas
import bigframes.testing.mocks


def test_to_datetime_with_series_and_format_doesnt_cache(monkeypatch):
    df = bigframes.testing.mocks.create_dataframe(monkeypatch)
    series = mock.Mock(spec=bigframes.pandas.Series, wraps=df["col"])
    dt_series = cast(
        bigframes.pandas.Series,
        bigframes.core.tools.datetimes.to_datetime(series, format="%Y%m%d"),
    )
    series._cached.assert_not_called()
    assert dt_series.dtype == bigframes.dtypes.DATETIME_DTYPE


def test_to_datetime_with_series_and_format_utc_doesnt_cache(monkeypatch):
    df = bigframes.testing.mocks.create_dataframe(monkeypatch)
    series = mock.Mock(spec=bigframes.pandas.Series, wraps=df["col"])
    dt_series = cast(
        bigframes.pandas.Series,
        bigframes.core.tools.datetimes.to_datetime(series, format="%Y%m%d", utc=True),
    )
    series._cached.assert_not_called()
    assert dt_series.dtype == bigframes.dtypes.TIMESTAMP_DTYPE
