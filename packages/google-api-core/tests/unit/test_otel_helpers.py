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

import sys
from unittest import mock

from google.api_core import _otel_helpers
from google.api_core.client_options import ClientOptions


def test_is_otel_capabilities_enabled_disabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "false")
    assert not _otel_helpers.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_otel_missing(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")
    # Simulate OTel not being installed by blocking imports
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    assert not _otel_helpers.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_otel_installed(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    assert _otel_helpers.is_otel_capabilities_enabled()


def test_apply_otel_capabilities_to_channel_disabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "false")
    mock_channel = mock.Mock()

    result = _otel_helpers.apply_otel_capabilities_to_channel(mock_channel)
    assert result is mock_channel


def test_apply_otel_capabilities_to_channel_enabled_otel_missing(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")
    # Simulate OTel not being installed by blocking imports
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    mock_channel = mock.Mock()
    result = _otel_helpers.apply_otel_capabilities_to_channel(mock_channel)
    assert result is mock_channel


def test_apply_otel_capabilities_to_channel_enabled_otel_installed(monkeypatch):
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_channel = mock.Mock()
    mock_intercepted_channel = mock.Mock()

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()

    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.return_value = mock_intercepted_channel

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _otel_helpers.apply_otel_capabilities_to_channel(mock_channel)

    assert result is mock_intercepted_channel
    mock_otel_grpc.client_interceptor.assert_called_once_with(tracer_provider=None)
    mock_otel_grpc.intercept_channel.assert_called_once_with(mock_channel, mock_interceptor)


def test_apply_otel_capabilities_to_channel_enabled_via_config(monkeypatch):
    # Tracing enabled via config (tracer_provider is set)
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_channel = mock.Mock()
    mock_intercepted_channel = mock.Mock()

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()

    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.return_value = mock_intercepted_channel

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _otel_helpers.apply_otel_capabilities_to_channel(mock_channel, client_options=options)

    assert result is mock_intercepted_channel
    mock_otel_grpc.client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )
    mock_otel_grpc.intercept_channel.assert_called_once_with(mock_channel, mock_interceptor)
