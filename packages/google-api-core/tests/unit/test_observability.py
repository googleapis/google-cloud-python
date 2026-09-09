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
import types
from unittest import mock

import pytest

from google.api_core import _observability
from google.api_core._feature_gating_helpers import FeatureGatingError
from google.api_core.client_options import ClientOptions


def test_is_otel_capabilities_enabled_disabled(monkeypatch):
    """Proves that is_otel_capabilities_enabled returns False when the tracing environment variable is disabled."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    assert not _observability.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_otel_missing(monkeypatch):
    """Proves that is_otel_capabilities_enabled returns False when tracing is enabled
    but OpenTelemetry gRPC instrumentation is not installed.
    """
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    # Simulate OTel not being installed by blocking imports
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)

    assert not _observability.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_otel_installed(monkeypatch):
    """Proves that is_otel_capabilities_enabled returns True when tracing is enabled
    and OpenTelemetry gRPC instrumentation is installed.
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

    assert _observability.is_otel_capabilities_enabled()


def test_is_otel_capabilities_enabled_experimental_requires_env_var(monkeypatch):
    """Proves that passing client_options with tracer_provider without the experimental
    env var set to 'true' raises FeatureGatingError (Fail Fast).
    """
    monkeypatch.delenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", raising=False)
    options = ClientOptions(tracer_provider=mock.Mock())

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

    options = ClientOptions(tracer_provider=mock.Mock())
    assert _observability.is_otel_capabilities_enabled(options)


def test_get_tracer_provider_default():
    """Proves that _get_tracer_provider returns None when no client_options are supplied."""
    assert _observability._get_tracer_provider() is None


def test_get_tracer_provider_config():
    """Proves that _get_tracer_provider extracts the tracer provider when supplied
    via a ClientOptions instance.
    """
    mock_tracer_provider = mock.Mock()
    options = ClientOptions(tracer_provider=mock_tracer_provider)
    assert _observability._get_tracer_provider(options) is mock_tracer_provider


def test_get_tracer_provider_dict_config():
    """Proves that _get_tracer_provider extracts the tracer provider when supplied
    via a dictionary configuration.
    """
    mock_tracer_provider = mock.Mock()
    options = {"tracer_provider": mock_tracer_provider}
    assert _observability._get_tracer_provider(options) is mock_tracer_provider


def test_get_otel_interceptor_disabled(monkeypatch):
    """Proves that get_otel_interceptor returns None when tracing is disabled."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    assert _observability.get_otel_interceptor() is None


def test_get_otel_interceptor_otel_missing(monkeypatch):
    """Proves that get_otel_interceptor returns None when OpenTelemetry gRPC
    instrumentation is not installed.
    """
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)
    assert _observability.get_otel_interceptor() is None


def test_get_otel_interceptor_enabled(monkeypatch):
    """Proves that get_otel_interceptor creates a synchronous OpenTelemetry client
    interceptor with the resolved tracer provider and returns a channel-intercepting callable.
    """
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    mock_tracer_provider = mock.Mock()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_raw_channel = mock.Mock(name="raw_channel")
    mock_wrapped_channel = mock.Mock(name="wrapped_channel")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock(name="otel_interceptor")

    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.return_value = mock_wrapped_channel

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    interceptor = _observability.get_otel_interceptor(client_options=options)
    assert callable(interceptor)

    mock_otel_grpc.client_interceptor.assert_called_once_with(
        tracer_provider=mock_tracer_provider,
        request_hook=_observability._client_request_hook,
        response_hook=_observability._client_response_hook,
    )

    result = interceptor(mock_raw_channel)
    assert result is mock_wrapped_channel
    mock_otel_grpc.intercept_channel.assert_called_once_with(
        mock_raw_channel, mock_interceptor
    )


def test_get_otel_interceptor_with_apply_channel_interceptors(monkeypatch):
    """Proves that get_otel_interceptor integrates seamlessly into apply_channel_interceptors."""
    pytest.importorskip("grpc")
    from google.api_core import grpc_helpers

    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    mock_tracer_provider = mock.Mock()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_raw_channel = mock.Mock(name="raw_channel")
    mock_wrapped_channel = mock.Mock(name="wrapped_channel")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_interceptor = mock.Mock(name="otel_interceptor")

    mock_otel_grpc.client_interceptor.return_value = mock_interceptor
    mock_otel_grpc.intercept_channel.return_value = mock_wrapped_channel

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    otel_interceptor = _observability.get_otel_interceptor(client_options=options)
    assert callable(otel_interceptor)

    result = grpc_helpers.apply_channel_interceptors(
        mock_raw_channel, interceptors=[otel_interceptor]
    )
    assert result is mock_wrapped_channel
    mock_otel_grpc.intercept_channel.assert_called_once_with(
        mock_raw_channel, mock_interceptor
    )


def test_get_otel_async_interceptor_disabled(monkeypatch):
    """Proves that get_otel_async_interceptor returns None when tracing is disabled."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "false")
    assert _observability.get_otel_async_interceptor() is None


def test_get_otel_async_interceptor_otel_missing(monkeypatch):
    """Proves that get_otel_async_interceptor returns None when OpenTelemetry gRPC
    instrumentation is not installed.
    """
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    monkeypatch.setitem(sys.modules, "opentelemetry.instrumentation.grpc", None)
    assert _observability.get_otel_async_interceptor() is None


def test_get_otel_async_interceptor_enabled(monkeypatch):
    """Proves that get_otel_async_interceptor instantiates and returns asynchronous
    OpenTelemetry client interceptors with the resolved tracer provider.
    """
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    mock_tracer_provider = mock.Mock()
    options = ClientOptions(tracer_provider=mock_tracer_provider)

    mock_async_interceptors = [mock.Mock(name="otel_async_interceptor")]

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    mock_otel_grpc.aio_client_interceptors.return_value = mock_async_interceptors

    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability.get_otel_async_interceptor(client_options=options)
    assert result is mock_async_interceptors
    mock_otel_grpc.aio_client_interceptors.assert_called_once_with(
        tracer_provider=mock_tracer_provider,
        request_hook=_observability._client_request_hook,
        response_hook=_observability._client_response_hook,
    )


def test_extract_endpoint_attributes():
    """Proves that _extract_endpoint_attributes correctly parses server.address and server.port."""
    # None or empty options
    assert _observability._extract_endpoint_attributes(None) == {}
    assert _observability._extract_endpoint_attributes({}) == {}
    assert (
        _observability._extract_endpoint_attributes(ClientOptions(api_endpoint=None))
        == {}
    )

    # Dict options with standard endpoint
    dict_opts = {"api_endpoint": "secretmanager.googleapis.com"}
    attrs = _observability._extract_endpoint_attributes(dict_opts)
    assert attrs["server.address"] == "secretmanager.googleapis.com"
    assert attrs["server.port"] == 443

    # ClientOptions with custom port
    custom_opts = ClientOptions(api_endpoint="https://my-custom-host.com:8443/")
    attrs = _observability._extract_endpoint_attributes(custom_opts)
    assert attrs["server.address"] == "my-custom-host.com"
    assert attrs["server.port"] == 8443

    # Invalid port string falls back to 443
    invalid_port_opts = ClientOptions(api_endpoint="my-custom-host.com:invalid_port")
    attrs = _observability._extract_endpoint_attributes(invalid_port_opts)
    assert attrs["server.address"] == "my-custom-host.com"
    assert attrs["server.port"] == 443


@pytest.mark.parametrize(
    "req,expected_attrs",
    [
        (None, {"rpc.system.name": "grpc"}),
        (types.SimpleNamespace(), {"rpc.system.name": "grpc"}),
        (
            types.SimpleNamespace(name="projects/p1/secrets/s1"),
            {
                "rpc.system.name": "grpc",
                "gcp.resource.destination.id": "projects/p1/secrets/s1",
            },
        ),
        (
            types.SimpleNamespace(parent="projects/parent-p1"),
            {
                "rpc.system.name": "grpc",
                "gcp.resource.destination.id": "projects/parent-p1",
            },
        ),
        (
            types.SimpleNamespace(
                name="projects/p1/secrets/s1", parent="projects/parent-p1"
            ),
            {
                "rpc.system.name": "grpc",
                "gcp.resource.destination.id": "projects/p1/secrets/s1",
            },
        ),
        (
            types.SimpleNamespace(name="projects/p1/secrets/s1", resend_count=2),
            {
                "rpc.system.name": "grpc",
                "gcp.resource.destination.id": "projects/p1/secrets/s1",
                "gcp.grpc.resend_count": 2,
            },
        ),
        (
            types.SimpleNamespace(resend_count=0),
            {"rpc.system.name": "grpc"},
        ),
    ],
)
def test_extract_t4_attributes(req, expected_attrs):
    """Proves that _extract_t4_attributes extracts all T4 gRPC attributes."""
    assert _observability._extract_t4_attributes(req) == expected_attrs


def test_client_request_hook():
    """Proves that _client_request_hook attaches extracted T4 attributes to recording spans."""
    # Non-recording span should not set attributes
    mock_span_non_rec = mock.Mock()
    mock_span_non_rec.is_recording.return_value = False
    _observability._client_request_hook(mock_span_non_rec, mock.Mock())
    mock_span_non_rec.set_attribute.assert_not_called()

    # None span should safely return
    _observability._client_request_hook(None, mock.Mock())

    # Recording span with default hook
    mock_span_rec = mock.Mock()
    mock_span_rec.is_recording.return_value = True
    req = types.SimpleNamespace(name="projects/my-proj/secrets/s1", resend_count=1)
    _observability._client_request_hook(mock_span_rec, req)
    mock_span_rec.set_attribute.assert_any_call("rpc.system.name", "grpc")
    mock_span_rec.set_attribute.assert_any_call(
        "gcp.resource.destination.id", "projects/my-proj/secrets/s1"
    )
    mock_span_rec.set_attribute.assert_any_call("gcp.grpc.resend_count", 1)

    # Custom hook with endpoint attributes
    endpoint_hook = _observability._make_client_request_hook(
        {"server.address": "custom.api.com", "server.port": 443}
    )
    mock_span_custom = mock.Mock()
    mock_span_custom.is_recording.return_value = True
    endpoint_hook(mock_span_custom, req)
    mock_span_custom.set_attribute.assert_any_call("server.address", "custom.api.com")
    mock_span_custom.set_attribute.assert_any_call("server.port", 443)


def test_client_response_hook():
    """Proves that _client_response_hook sets rpc.response.status_code, error.type, and status.message."""
    # Non-recording span should not set attributes
    mock_span_non_rec = mock.Mock()
    mock_span_non_rec.is_recording.return_value = False
    _observability._client_response_hook(mock_span_non_rec, mock.Mock())
    mock_span_non_rec.set_attribute.assert_not_called()

    # None span should safely return
    _observability._client_response_hook(None, mock.Mock())

    # Response with no code method defaults to OK
    mock_span_ok = mock.Mock()
    mock_span_ok.is_recording.return_value = True
    _observability._client_response_hook(mock_span_ok, mock.Mock(spec=[]))
    mock_span_ok.set_attribute.assert_called_once_with("rpc.response.status_code", "OK")

    # Response with StatusCode object having name (e.g. OK)
    mock_span_code_obj = mock.Mock()
    mock_span_code_obj.is_recording.return_value = True
    mock_resp_ok = mock.Mock()
    mock_code_ok = mock.Mock()
    mock_code_ok.name = "OK"
    mock_resp_ok.code.return_value = mock_code_ok
    _observability._client_response_hook(mock_span_code_obj, mock_resp_ok)
    mock_span_code_obj.set_attribute.assert_called_once_with(
        "rpc.response.status_code", "OK"
    )

    # Response with error status (e.g. integer 14 -> UNAVAILABLE) and details
    mock_span_err = mock.Mock()
    mock_span_err.is_recording.return_value = True
    mock_resp_err = mock.Mock()
    mock_resp_err.code.return_value = 14
    mock_resp_err.details.return_value = "Service temporarily unavailable"
    _observability._client_response_hook(mock_span_err, mock_resp_err)
    mock_span_err.set_attribute.assert_any_call(
        "rpc.response.status_code", "UNAVAILABLE"
    )
    mock_span_err.set_attribute.assert_any_call("error.type", "UNAVAILABLE")
    mock_span_err.set_attribute.assert_any_call(
        "status.message", "Service temporarily unavailable"
    )

    # Response where code() raises an exception is handled gracefully
    mock_span_exc = mock.Mock()
    mock_span_exc.is_recording.return_value = True
    mock_resp_exc = mock.Mock()
    mock_resp_exc.code.side_effect = RuntimeError("Broken call")
    _observability._client_response_hook(mock_span_exc, mock_resp_exc)
    mock_span_exc.set_attribute.assert_called_once_with(
        "rpc.response.status_code", "OK"
    )

    # Response with error status but no details method
    mock_span_no_det = mock.Mock()
    mock_span_no_det.is_recording.return_value = True
    mock_resp_no_det = mock.Mock(spec=["code"])
    mock_resp_no_det.code.return_value = 14
    _observability._client_response_hook(mock_span_no_det, mock_resp_no_det)
    mock_span_no_det.set_attribute.assert_any_call(
        "rpc.response.status_code", "UNAVAILABLE"
    )
    mock_span_no_det.set_attribute.assert_any_call("error.type", "UNAVAILABLE")

    # Response with error status where details() returns empty/None
    mock_span_empty_det = mock.Mock()
    mock_span_empty_det.is_recording.return_value = True
    mock_resp_empty_det = mock.Mock()
    mock_resp_empty_det.code.return_value = 14
    mock_resp_empty_det.details.return_value = ""
    _observability._client_response_hook(mock_span_empty_det, mock_resp_empty_det)
    mock_span_empty_det.set_attribute.assert_any_call(
        "rpc.response.status_code", "UNAVAILABLE"
    )

    # Response with error status where details() raises an exception
    mock_span_exc_det = mock.Mock()
    mock_span_exc_det.is_recording.return_value = True
    mock_resp_exc_det = mock.Mock()
    mock_resp_exc_det.code.return_value = 14
    mock_resp_exc_det.details.side_effect = RuntimeError("Details broken")
    _observability._client_response_hook(mock_span_exc_det, mock_resp_exc_det)
    mock_span_exc_det.set_attribute.assert_any_call(
        "rpc.response.status_code", "UNAVAILABLE"
    )


def test_extract_endpoint_attributes_empty_clean():
    """Proves that endpoint consisting only of slashes/protocol results in empty attrs."""
    assert (
        _observability._extract_endpoint_attributes(
            ClientOptions(api_endpoint="http:///")
        )
        == {}
    )


def test_get_otel_interceptor_with_api_endpoint(monkeypatch):
    """Proves that get_otel_interceptor injects server.address and server.port when api_endpoint is set."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    options = ClientOptions(api_endpoint="secretmanager.googleapis.com:443")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    interceptor = _observability.get_otel_interceptor(client_options=options)
    assert callable(interceptor)

    # Verify custom request hook was passed
    args, kwargs = mock_otel_grpc.client_interceptor.call_args
    req_hook = kwargs["request_hook"]
    assert req_hook is not _observability._client_request_hook

    # Test invoking the custom hook
    mock_span = mock.Mock()
    mock_span.is_recording.return_value = True
    req_hook(mock_span, None)
    mock_span.set_attribute.assert_any_call(
        "server.address", "secretmanager.googleapis.com"
    )
    mock_span.set_attribute.assert_any_call("server.port", 443)


def test_get_otel_async_interceptor_with_api_endpoint(monkeypatch):
    """Proves that get_otel_async_interceptor injects server.address and server.port when api_endpoint is set."""
    monkeypatch.setenv("GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED", "true")
    options = ClientOptions(api_endpoint="secretmanager.googleapis.com:8443")

    mock_otel = mock.Mock()
    mock_otel_grpc = mock_otel.instrumentation.grpc
    monkeypatch.setitem(sys.modules, "opentelemetry", mock_otel)
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation", mock_otel.instrumentation
    )
    monkeypatch.setitem(
        sys.modules, "opentelemetry.instrumentation.grpc", mock_otel_grpc
    )

    result = _observability.get_otel_async_interceptor(client_options=options)
    assert result is not None

    args, kwargs = mock_otel_grpc.aio_client_interceptors.call_args
    req_hook = kwargs["request_hook"]
    assert req_hook is not _observability._client_request_hook

    mock_span = mock.Mock()
    mock_span.is_recording.return_value = True
    req_hook(mock_span, None)
    mock_span.set_attribute.assert_any_call(
        "server.address", "secretmanager.googleapis.com"
    )
    mock_span.set_attribute.assert_any_call("server.port", 8443)
