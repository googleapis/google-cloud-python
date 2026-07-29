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

import google.cloud.bigquery as bigquery
import google.cloud.exceptions
import pytest

import bigframes
from bigframes.session.proxy_executor import DualCompilerProxyExecutor


@pytest.fixture
def mock_executor():
    bqclient = mock.create_autospec(bigquery.Client)
    bqclient.project = "test-project"
    storage_manager = mock.Mock()
    bqstoragereadclient = mock.Mock()
    loader = mock.Mock()
    publisher = mock.Mock()
    function_manager = mock.Mock()
    return DualCompilerProxyExecutor(
        bqclient,
        storage_manager,
        bqstoragereadclient,
        loader,
        publisher=publisher,
        function_manager=function_manager,
    )


def test_execute_legacy_routes_to_ibis(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    execution_spec = mock.Mock(spec=bigframes.session.execution_spec.ExecutionSpec)

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "legacy")
    mock_executor.execute(array_value, execution_spec)

    mock_executor._ibis_executor.execute.assert_called_once_with(
        array_value, execution_spec
    )
    mock_executor._sqlglot_executor.execute.assert_not_called()


def test_execute_experimental_routes_to_sqlglot(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    execution_spec = mock.Mock(spec=bigframes.session.execution_spec.ExecutionSpec)
    execution_spec.with_bq_labels.return_value = execution_spec

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "experimental")
    mock_executor.execute(array_value, execution_spec)

    execution_spec.with_bq_labels.assert_called_once_with(
        {"bigframes-compiler": "sqlglot"}
    )
    mock_executor._sqlglot_executor.execute.assert_called_once_with(
        array_value, execution_spec
    )
    mock_executor._ibis_executor.execute.assert_not_called()


def test_execute_stable_routes_to_sqlglot_success(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    execution_spec = mock.Mock(spec=bigframes.session.execution_spec.ExecutionSpec)
    execution_spec.with_bq_labels.return_value = execution_spec

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "stable")
    with mock.patch("uuid.uuid1") as mock_uuid:
        mock_uuid.return_value.hex = "1234567890123456"
        mock_executor.execute(array_value, execution_spec)

    execution_spec.with_bq_labels.assert_called_once_with(
        {"bigframes-compiler": "sqlglot-123456789012"}
    )
    mock_executor._sqlglot_executor.execute.assert_called_once_with(
        array_value, execution_spec
    )
    mock_executor._ibis_executor.execute.assert_not_called()


def test_execute_stable_routes_to_sqlglot_fallback_to_ibis(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    execution_spec = mock.Mock(spec=bigframes.session.execution_spec.ExecutionSpec)

    spec_sqlglot = mock.Mock(spec=bigframes.session.execution_spec.ExecutionSpec)
    spec_ibis = mock.Mock(spec=bigframes.session.execution_spec.ExecutionSpec)
    execution_spec.with_bq_labels.side_effect = [spec_sqlglot, spec_ibis]

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    mock_executor._sqlglot_executor.execute.side_effect = (
        google.cloud.exceptions.BadRequest("test error")
    )

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "stable")
    with mock.patch("uuid.uuid1") as mock_uuid:
        mock_uuid.return_value.hex = "1234567890123456"
        with pytest.warns(
            UserWarning, match="Compiler ID 123456789012: Exception on sqlglot"
        ):
            mock_executor.execute(array_value, execution_spec)

    execution_spec.with_bq_labels.assert_has_calls(
        [
            mock.call({"bigframes-compiler": "sqlglot-123456789012"}),
            mock.call({"bigframes-compiler": "ibis-123456789012"}),
        ]
    )

    mock_executor._sqlglot_executor.execute.assert_called_once_with(
        array_value, spec_sqlglot
    )
    mock_executor._ibis_executor.execute.assert_called_once_with(array_value, spec_ibis)


def test_cached_legacy_routes_to_ibis(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    config = mock.Mock()

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "legacy")
    mock_executor.cached(array_value, config=config)

    mock_executor._ibis_executor.cached.assert_called_once_with(
        array_value, config=config
    )
    mock_executor._sqlglot_executor.cached.assert_not_called()


def test_cached_experimental_routes_to_sqlglot(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    config = mock.Mock()

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "experimental")
    mock_executor.cached(array_value, config=config)

    mock_executor._sqlglot_executor.cached.assert_called_once_with(
        array_value, config=config
    )
    mock_executor._ibis_executor.cached.assert_not_called()


def test_cached_stable_routes_to_sqlglot_fallback_to_ibis(mock_executor, monkeypatch):
    array_value = mock.Mock(spec=bigframes.core.ArrayValue)
    config = mock.Mock()

    mock_executor._ibis_executor = mock.Mock()
    mock_executor._sqlglot_executor = mock.Mock()

    mock_executor._sqlglot_executor.cached.side_effect = (
        google.cloud.exceptions.BadRequest("test error")
    )

    monkeypatch.setattr(bigframes.options.experiments, "sql_compiler", "stable")
    with mock.patch("uuid.uuid1") as mock_uuid:
        mock_uuid.return_value.hex = "1234567890123456"
        with pytest.warns(
            UserWarning, match="Compiler ID 123456789012: Exception on sqlglot"
        ):
            mock_executor.cached(array_value, config=config)

    mock_executor._sqlglot_executor.cached.assert_called_once_with(
        array_value, config=config
    )
    mock_executor._ibis_executor.cached.assert_called_once_with(
        array_value, config=config
    )
