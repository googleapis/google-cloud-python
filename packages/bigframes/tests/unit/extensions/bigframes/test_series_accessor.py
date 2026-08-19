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

from typing import cast
from unittest.mock import MagicMock, patch

import pytest

import bigframes.series as series
from bigframes.testing import mocks


def test_bigframes_series_has_accessor(monkeypatch: pytest.MonkeyPatch):
    # Arrange
    from bigframes.extensions.bigframes.series_accessor import (
        BigframesBigQuerySeriesAccessor,
    )

    bf_df = mocks.create_dataframe(monkeypatch, data={"col": [1, 2]})
    bf_series = cast(series.Series, bf_df["col"])

    # Act
    has_bq = hasattr(bf_series, "bigquery")
    bq_obj = bf_series.bigquery

    # Assert
    assert has_bq
    assert isinstance(bq_obj, BigframesBigQuerySeriesAccessor)


@patch("bigframes.operations.googlesql.global_namespace.array.array_length")
def test_bigframes_series_accessor_global_routing(
    mock_array_length, monkeypatch: pytest.MonkeyPatch
):
    # Arrange
    bf_df = mocks.create_dataframe(monkeypatch, data={"col": [[1, 2], [3, 4, 5]]})
    bf_series = cast(series.Series, bf_df["col"])
    mock_result_series = MagicMock()
    mock_array_length.return_value = mock_result_series

    # Act
    result = bf_series.bigquery.array_length()

    # Assert
    mock_array_length.assert_called_once_with(bf_series)
    assert result is mock_result_series


@patch("bigframes.operations.googlesql.aead.encrypt")
def test_bigframes_series_accessor_namespaced_routing(
    mock_encrypt, monkeypatch: pytest.MonkeyPatch
):
    # Arrange
    bf_df = mocks.create_dataframe(monkeypatch, data={"keyset": [b"key1", b"key2"]})
    keyset_series = cast(series.Series, bf_df["keyset"])
    mock_result_series = MagicMock()
    mock_encrypt.return_value = mock_result_series

    plaintext = "my secret"
    additional_data = "context"

    # Act
    result = keyset_series.bigquery.aead.encrypt(plaintext, additional_data)

    # Assert
    mock_encrypt.assert_called_once_with(keyset_series, plaintext, additional_data)
    assert result is mock_result_series
