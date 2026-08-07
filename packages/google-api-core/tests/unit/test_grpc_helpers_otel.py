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

"""Tests for OpenTelemetry gRPC interceptor integration in google-api-core."""

import sys
from unittest import mock

import pytest

try:
    from google.api_core import grpc_helpers

    HAS_GRPC_HELPERS = True
except ImportError:
    HAS_GRPC_HELPERS = False


# Removed clean_sys_modules fixture as it causes issues in no-grpc environments
# when tests are collected.


@pytest.mark.skipif(not HAS_GRPC_HELPERS, reason="Requires google-api-core[grpc]")
def test_create_channel_otel_installed_and_enabled(monkeypatch):
    """Verify that create_channel wraps the channel with OTel interceptor when installed and enabled."""

    # Build a hierarchy of mocks to simulate the nested OpenTelemetry modules.
    # This allows us to test code that imports these modules without needing them installed.
    mock_otel = mock.Mock()
    mock_otel_instrumentation = mock.Mock()
    mock_otel_grpc = mock.Mock()
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.side_effect = lambda ch, inc: f"wrapped_{ch}"

    # Link the mocks together to match the package structure (opentelemetry.instrumentation.grpc)
    mock_otel.instrumentation = mock_otel_instrumentation
    mock_otel_instrumentation.grpc = mock_otel_grpc

    # Inject the mocks into sys.modules so Python's import system uses them.
    # monkeypatch ensures these changes are reverted after the test finishes.
    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel_instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    # Enable tracing
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    # Mock grpc.secure_channel
    mock_channel = "raw_channel"
    with mock.patch(
        "grpc.secure_channel", return_value=mock_channel
    ) as mock_secure_channel:
        # We need to mock credentials setup to avoid external calls
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            channel = grpc_helpers.create_channel("localhost:1234")

            # Verify raw channel was created
            mock_secure_channel.assert_called_once()

            # Verify OTel interceptor was fetched and channel was wrapped
            mock_otel_grpc.client_interceptor.assert_called_once()
            mock_otel_grpc.intercept_channel.assert_called_once_with(
                mock_channel, mock_interceptor
            )

            # Verify returned channel is the wrapped one
            assert channel == f"wrapped_{mock_channel}"


@pytest.mark.skipif(not HAS_GRPC_HELPERS, reason="Requires google-api-core[grpc]")
def test_create_channel_otel_installed_but_disabled(monkeypatch):
    """Verify that create_channel does NOT wrap the channel if tracing is disabled."""

    mock_otel_grpc = mock.Mock()
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    # Disable tracing (or leave unset, default should be false/disabled)
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "false")

    mock_channel = "raw_channel"
    with mock.patch(
        "grpc.secure_channel", return_value=mock_channel
    ) as mock_secure_channel:
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            channel = grpc_helpers.create_channel("localhost:1234")

            # Verify raw channel was created
            mock_secure_channel.assert_called_once()

            # Verify OTel was NOT used
            mock_otel_grpc.intercept_channel.assert_not_called()

            # Verify returned channel is the raw one
            assert channel == mock_channel


@pytest.mark.skipif(not HAS_GRPC_HELPERS, reason="Requires google-api-core[grpc]")
def test_create_channel_otel_not_installed_fails_open(monkeypatch):
    """Verify that create_channel fails open if OTel is not installed, even if enabled."""

    # Simulate missing module
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    # Enable tracing
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_channel = "raw_channel"
    with mock.patch(
        "grpc.secure_channel", return_value=mock_channel
    ) as mock_secure_channel:
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            # This should NOT raise ImportError
            channel = grpc_helpers.create_channel("localhost:1234")

            # Verify raw channel was created
            mock_secure_channel.assert_called_once()

            # Verify returned channel is the raw one
            assert channel == mock_channel
