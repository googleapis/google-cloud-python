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

import grpc
import pytest
from google.api_core import grpc_helpers


@pytest.fixture
def clean_sys_modules():
    """Fixture to ensure opentelemetry modules are unloaded before and after tests."""
    modules_to_remove = [
        "opentelemetry.instrumentation.grpc",
        "opentelemetry.instrumentation",
        "opentelemetry",
    ]
    for mod in modules_to_remove:
        if mod in sys.modules:
            del sys.modules[mod]
    yield
    for mod in modules_to_remove:
        if mod in sys.modules:
            del sys.modules[mod]


def test_create_channel_otel_installed_and_enabled(monkeypatch, clean_sys_modules):
    """Verify that create_channel wraps the channel with OTel interceptor when installed and enabled."""

    # Mock opentelemetry.instrumentation.grpc
    mock_otel_grpc = mock.Mock()
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.side_effect = lambda ch, inc: f"wrapped_{ch}"

    sys.modules["opentelemetry.instrumentation.grpc"] = mock_otel_grpc

    # Enable tracing
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    # Mock grpc.secure_channel
    mock_channel = "raw_channel"
    with mock.patch("grpc.secure_channel", return_value=mock_channel) as mock_secure_channel:
        # We need to mock credentials setup to avoid external calls
        with mock.patch("google.api_core.grpc_helpers._create_composite_credentials", return_value=mock.Mock()):
            channel = grpc_helpers.create_channel("localhost:1234")

            # Verify raw channel was created
            mock_secure_channel.assert_called_once()

            # Verify OTel interceptor was fetched and channel was wrapped
            mock_otel_grpc.client_interceptor.assert_called_once()
            mock_otel_grpc.intercept_channel.assert_called_once_with(mock_channel, mock_interceptor)

            # Verify returned channel is the wrapped one
            assert channel == f"wrapped_{mock_channel}"


def test_create_channel_otel_installed_but_disabled(monkeypatch, clean_sys_modules):
    """Verify that create_channel does NOT wrap the channel if tracing is disabled."""

    mock_otel_grpc = mock.Mock()
    sys.modules["opentelemetry.instrumentation.grpc"] = mock_otel_grpc

    # Disable tracing (or leave unset, default should be false/disabled)
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "false")

    mock_channel = "raw_channel"
    with mock.patch("grpc.secure_channel", return_value=mock_channel) as mock_secure_channel:
        with mock.patch("google.api_core.grpc_helpers._create_composite_credentials", return_value=mock.Mock()):
            channel = grpc_helpers.create_channel("localhost:1234")

            # Verify raw channel was created
            mock_secure_channel.assert_called_once()

            # Verify OTel was NOT used
            mock_otel_grpc.intercept_channel.assert_not_called()

            # Verify returned channel is the raw one
            assert channel == mock_channel


def test_create_channel_otel_not_installed_fails_open(monkeypatch, clean_sys_modules):
    """Verify that create_channel fails open if OTel is not installed, even if enabled."""

    # Ensure it's not in sys.modules
    if "opentelemetry.instrumentation.grpc" in sys.modules:
        del sys.modules["opentelemetry.instrumentation.grpc"]

    # Enable tracing
    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", "true")

    mock_channel = "raw_channel"
    with mock.patch("grpc.secure_channel", return_value=mock_channel) as mock_secure_channel:
        with mock.patch("google.api_core.grpc_helpers._create_composite_credentials", return_value=mock.Mock()):
            # This should NOT raise ImportError
            channel = grpc_helpers.create_channel("localhost:1234")

            # Verify raw channel was created
            mock_secure_channel.assert_called_once()

            # Verify returned channel is the raw one
            assert channel == mock_channel
