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

from unittest.mock import MagicMock, patch

import pandas as pd

import bigframes  # noqa: F401 registers pandas extensions
import bigframes.series as series


def test_pandas_series_registers_accessor():
    # Arrange
    from bigframes.extensions.pandas.series_accessor import (
        PandasBigQuerySeriesAccessor,
    )

    s = pd.Series([1, 2])

    # Act
    has_bq = hasattr(s, "bigquery")
    bq_obj = s.bigquery

    # Assert
    assert has_bq
    assert isinstance(bq_obj, PandasBigQuerySeriesAccessor)


@patch("bigframes.operations.googlesql.global_namespace.array.array_length")
def test_pandas_series_accessor_global_routing(mock_array_length):
    # Arrange
    mock_bf_series = MagicMock()
    mock_bf_series.to_pandas.return_value = pd.Series([2, 3])
    mock_array_length.return_value = mock_bf_series
    mock_session = MagicMock()
    mock_bf_self = MagicMock()
    mock_session.read_pandas.return_value = mock_bf_self

    s = pd.Series([[1, 2], [3, 4, 5]])

    # Act
    result = s.bigquery.array_length(session=mock_session)

    # Assert
    mock_session.read_pandas.assert_called_once_with(s)
    mock_array_length.assert_called_once_with(mock_bf_self)
    mock_bf_series.to_pandas.assert_called_once_with(ordered=True)
    pd.testing.assert_series_equal(result, pd.Series([2, 3]))


@patch("bigframes.operations.googlesql.aead.encrypt")
def test_pandas_series_accessor_namespaced_routing(mock_encrypt):
    # Arrange
    mock_bf_series = MagicMock()
    mock_bf_series.to_pandas.return_value = pd.Series([b"encrypted1", b"encrypted2"])
    mock_encrypt.return_value = mock_bf_series
    mock_session = MagicMock()
    mock_bf_self = MagicMock()
    mock_session.read_pandas.return_value = mock_bf_self

    keyset_series = pd.Series([b"key1", b"key2"])
    plaintext = "my secret"
    additional_data = "context"

    # Act
    result = keyset_series.bigquery.aead.encrypt(  # type: ignore
        plaintext, additional_data, session=mock_session
    )

    # Assert
    mock_session.read_pandas.assert_called_once_with(keyset_series)
    mock_encrypt.assert_called_once_with(mock_bf_self, plaintext, additional_data)
    mock_bf_series.to_pandas.assert_called_once_with(ordered=True)
    pd.testing.assert_series_equal(result, pd.Series([b"encrypted1", b"encrypted2"]))


@patch("bigframes.operations.googlesql.global_namespace.array.array_concat")
def test_pandas_series_accessor_global_routing_uses_series_session(mock_array_concat):
    # Arrange
    mock_bf_series = MagicMock()
    mock_bf_series.to_pandas.return_value = pd.Series([[1, 2, 3, 4]])
    mock_array_concat.return_value = mock_bf_series
    mock_session = MagicMock()
    mock_bf_other = MagicMock(spec=series.Series)
    mock_bf_other._session = mock_session
    mock_bf_self = MagicMock()
    mock_session.read_pandas.return_value = mock_bf_self
    s = pd.Series([[1, 2]])

    # Act
    result = s.bigquery.array_concat(mock_bf_other)

    # Assert
    assert result is not None
    mock_session.read_pandas.assert_called_once_with(s)
    mock_array_concat.assert_called_once_with(mock_bf_self, mock_bf_other)


@patch("bigframes.operations.googlesql.aead.encrypt")
def test_pandas_series_accessor_namespaced_routing_uses_series_session(
    mock_encrypt,
):
    # Arrange
    mock_bf_series = MagicMock()
    mock_bf_series.to_pandas.return_value = pd.Series([b"encrypted1", b"encrypted2"])
    mock_encrypt.return_value = mock_bf_series
    mock_session = MagicMock()
    mock_bf_plaintext = MagicMock(spec=series.Series)
    mock_bf_plaintext._session = mock_session
    mock_bf_self = MagicMock()
    mock_session.read_pandas.return_value = mock_bf_self
    keyset_series = pd.Series([b"key1", b"key2"])
    additional_data = "context"

    # Act
    result = keyset_series.bigquery.aead.encrypt(  # type: ignore
        mock_bf_plaintext, additional_data
    )

    # Assert
    assert result is not None
    mock_session.read_pandas.assert_called_once_with(keyset_series)
    mock_encrypt.assert_called_once_with(
        mock_bf_self, mock_bf_plaintext, additional_data
    )
