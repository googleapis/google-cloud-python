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

import pytest

from google.api_core import _observability
from google.api_core._feature_gating_helpers import FeatureGatingError
from google.api_core.client_options import ClientOptions


def test_is_otel_capabilities_enabled_disabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    assert not _observability.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_otel_missing(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    # Simulate OTel not being installed by blocking imports
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    assert not _observability.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_otel_installed(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    assert _observability.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_experimental_requires_env_var(monkeypatch):
    """Proves that passing client_options with tracer_provider without the experimental
    env var set to 'true' raises FeatureGatingError (Fail Fast).
    """
    monkeypatch.delenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", raising=False)
    options = ClientOptions(tracer_provider=object())

    with pytest.raises(
        FeatureGatingError,
        match="requires GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED",
    ):
        _observability.is_otel_capabilities_enabled(options)


def test_is_otel_capabilities_enabled_experimental_enabled_with_config(monkeypatch):
    """Proves that when GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED=true and tracer_provider
    is supplied via client_options, is_otel_capabilities_enabled returns True.
    """
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    options = ClientOptions(tracer_provider=object())
    assert _observability.is_otel_capabilities_enabled(options)


def test_get_otel_interceptor_sync_default(monkeypatch):
    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability._get_otel_interceptor()
    assert result is mock_interceptor
    mock_otel_grpc.client_interceptor.assert_called_once_with(tracer_provider=None)


def test_get_otel_interceptor_sync_config(monkeypatch):
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability._get_otel_interceptor(client_options=options)
    assert result is mock_interceptor
    mock_otel_grpc.client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )


def test_get_otel_interceptor_sync_dict_config(monkeypatch):
    mock_tracer_provider = object()
    options = {"tracer_provider": mock_tracer_provider}

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability._get_otel_interceptor(client_options=options)
    assert result is mock_interceptor
    mock_otel_grpc.client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )


def test_get_otel_interceptor_async(monkeypatch):
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_async_interceptor = mock.Mock()
    mock_otel_grpc.aio_client_interceptor.return_value = mock_async_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability._get_otel_interceptor(client_options=options, is_async=True)
    assert result is mock_async_interceptor
    mock_otel_grpc.aio_client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )


def test_create_channel_with_otel_disabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    mock_raw_channel = mock.Mock(name="raw_channel")
    mock_channel_factory = mock.Mock(return_value=mock_raw_channel)

    result = _observability.create_channel_with_otel(
        mock_channel_factory,
        target="example.com:443",
        credentials="mock_creds",
    )

    assert result is mock_raw_channel
    mock_channel_factory.assert_called_once_with(
        target="example.com:443", credentials="mock_creds"
    )


def test_create_channel_with_otel_enabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_raw_channel = mock.Mock(name="raw_channel")
    mock_wrapped_channel = mock.Mock(name="wrapped_channel")
    mock_channel_factory = mock.Mock(return_value=mock_raw_channel)

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()

    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.return_value = mock_wrapped_channel

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability.create_channel_with_otel(
        mock_channel_factory,
        client_options=options,
        target="example.com:443",
        credentials="mock_creds",
    )

    assert result is mock_wrapped_channel
    mock_channel_factory.assert_called_once_with(
        target="example.com:443", credentials="mock_creds"
    )
    mock_otel_grpc.client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )
    mock_otel_grpc.intercept_channel.assert_called_once_with(
        mock_raw_channel, mock_interceptor
    )


def test_create_async_channel_with_otel_disabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    mock_async_channel = mock.Mock(name="async_channel")
    mock_channel_factory = mock.Mock(return_value=mock_async_channel)
    user_interceptor = mock.Mock(name="user_interceptor")

    result = _observability.create_async_channel_with_otel(
        mock_channel_factory,
        target="example.com:443",
        interceptors=[user_interceptor],
    )

    assert result is mock_async_channel
    mock_channel_factory.assert_called_once_with(
        target="example.com:443",
        interceptors=[user_interceptor],
    )


def test_create_async_channel_with_otel_enabled(monkeypatch):
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_async_channel = mock.Mock(name="async_channel")
    mock_channel_factory = mock.Mock(return_value=mock_async_channel)
    user_interceptor = mock.Mock(name="user_interceptor")
    mock_async_interceptor = mock.Mock(name="otel_async_interceptor")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_otel_grpc.aio_client_interceptor.return_value = mock_async_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability.create_async_channel_with_otel(
        mock_channel_factory,
        client_options=options,
        target="example.com:443",
        interceptors=[user_interceptor],
    )

    assert result is mock_async_channel
    mock_otel_grpc.aio_client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )
    mock_channel_factory.assert_called_once_with(
        target="example.com:443",
        interceptors=[user_interceptor, mock_async_interceptor],
    )


def test_create_async_channel_with_otel_none_interceptors(monkeypatch):
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_async_channel = mock.Mock(name="async_channel")
    mock_channel_factory = mock.Mock(return_value=mock_async_channel)
    mock_async_interceptor = mock.Mock(name="otel_async_interceptor")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_otel_grpc.aio_client_interceptor.return_value = mock_async_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability.create_async_channel_with_otel(
        mock_channel_factory,
        client_options=options,
        target="example.com:443",
        interceptors=None,
    )

    assert result is mock_async_channel
    mock_otel_grpc.aio_client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )
    mock_channel_factory.assert_called_once_with(
        target="example.com:443",
        interceptors=[mock_async_interceptor],
    )


def test_create_async_channel_with_otel_omitted_interceptors(monkeypatch):
    mock_tracer_provider = object()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_async_channel = mock.Mock(name="async_channel")
    mock_channel_factory = mock.Mock(return_value=mock_async_channel)
    mock_async_interceptor = mock.Mock(name="otel_async_interceptor")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_otel_grpc.aio_client_interceptor.return_value = mock_async_interceptor

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability.create_async_channel_with_otel(
        mock_channel_factory,
        client_options=options,
        target="example.com:443",
    )

    assert result is mock_async_channel
    mock_otel_grpc.aio_client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider
    )
    mock_channel_factory.assert_called_once_with(
        target="example.com:443",
        interceptors=[mock_async_interceptor],
    )
