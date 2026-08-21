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
import types
from unittest import mock

import pytest

try:
    from google.api_core import grpc_helpers

    HAS_GRPC_HELPERS = True
except ImportError:
    HAS_GRPC_HELPERS = False


@pytest.fixture
def mock_otel_grpc(monkeypatch):
    """Fixture to mock OpenTelemetry gRPC hierarchy."""
    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock()
    mock_otel_grpc.client_interceptor.return_value = mock_interceptor

    modules = {
        "opentelemetry": mock_otel,
        "opentelemetry.instrumentation": mock_otel.instrumentation,
        "opentelemetry.instrumentation.grpc": mock_otel_grpc,
    }

    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)

    return mock_otel_grpc


@pytest.mark.parametrize(
    "is_otel_installed, tracing_env_var_value, expect_otel_interceptor",
    [
        pytest.param(True, "true", True, id="installed_and_enabled"),
        pytest.param(True, "false", False, id="installed_but_disabled"),
        pytest.param(False, "true", False, id="not_installed_fails_open"),
    ],
)
@pytest.mark.skipif(not HAS_GRPC_HELPERS, reason="Requires google-api-core[grpc]")
def test_create_channel_otel_combos(
    monkeypatch,
    mock_otel_grpc,
    is_otel_installed,
    tracing_env_var_value,
    expect_otel_interceptor,
):
    """Verify create_channel behavior with various OTel installation and enablement states."""

    monkeypatch.setenv("GOOGLE_CLOUD_PYTHON_TRACING_ENABLED", tracing_env_var_value)

    if not is_otel_installed:
        monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    mock_channel = "raw_channel"
    mock_otel_grpc.intercept_channel.side_effect = lambda ch, inc: f"wrapped_{ch}"

    with (
        mock.patch(
            "grpc.secure_channel", return_value=mock_channel
        ) as mock_secure_channel,
    ):
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            channel = grpc_helpers.create_channel("localhost:1234")

            # Always expect raw channel creation
            mock_secure_channel.assert_called_once()

            if expect_otel_interceptor:
                mock_otel_grpc.client_interceptor.assert_called_once()
                mock_otel_grpc.intercept_channel.assert_called_once_with(
                    mock_channel, mock_otel_grpc.client_interceptor.return_value
                )
                assert channel == f"wrapped_{mock_channel}"
            else:
                # OTel should NOT have been called
                mock_otel_grpc.intercept_channel.assert_not_called()
                assert channel == mock_channel


@pytest.mark.parametrize(
    "config_factory",
    [
        lambda tp: {"tracer_provider": tp},
        lambda tp: types.SimpleNamespace(tracer_provider=tp),
    ],
    ids=["dict", "object"],
)
@pytest.mark.skipif(not HAS_GRPC_HELPERS, reason="Requires google-api-core[grpc]")
def test_create_channel_with_custom_tracer_provider(
    monkeypatch, mock_otel_grpc, config_factory
):
    """Verify that create_channel passes custom tracer_provider to OTel interceptor."""

    mock_tracer_provider = mock.Mock()
    config = config_factory(mock_tracer_provider)

    mock_channel = "raw_channel"
    with (
        mock.patch("grpc.secure_channel", return_value=mock_channel),
    ):
        with mock.patch(
            "google.api_core.grpc_helpers._create_composite_credentials",
            return_value=mock.Mock(),
        ):
            grpc_helpers.create_channel("localhost:1234", configuration=config)

            mock_otel_grpc.client_interceptor.assert_called_once_with(
                tracer_provider=mock_tracer_provider
            )
