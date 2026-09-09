# -*- coding: utf-8 -*-
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
#

"""OpenTelemetry helpers for resolving and instantiating interceptors."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Sequence

from google.api_core import _feature_gating_helpers
from google.api_core.client_options import ClientOptions

if TYPE_CHECKING:
    # flake8: grpc, trace, and ClientInterceptor are imported only for static analysis and type annotations
    # The 'noqa: F401' comment avoids flake8 "imported but not used" errors.
    import grpc  # noqa: F401
    import opentelemetry.trace  # noqa: F401

    from google.api_core.grpc_helpers import ClientInterceptor  # noqa: F401

_TRACER_PROVIDER = "tracer_provider"


def is_otel_capabilities_enabled(
    client_options: ClientOptions | dict[str, Any] | None = None,
    env_var: str = "GOOGLE_SDK_EXPERIMENTAL_PYTHON_TRACING_ENABLED",
) -> bool:
    """Checks if OTel capabilities are enabled and installed.

    Args:
        client_options: The client options object or dictionary.
        env_var: The environment variable to check for enablement.

    Returns:
        bool: True if enabled and installed, False otherwise.
    """
    is_tracing_enabled = _feature_gating_helpers.resolve_feature_flags(
        env_var=env_var,
        feature_key=_TRACER_PROVIDER,
        configuration=client_options,
    )

    if is_tracing_enabled:
        try:
            import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found] # noqa: F401

            return True
        except ImportError:
            pass

    return False


_STATUS_CODE_NAMES = {
    0: "OK",
    1: "CANCELLED",
    2: "UNKNOWN",
    3: "INVALID_ARGUMENT",
    4: "DEADLINE_EXCEEDED",
    5: "NOT_FOUND",
    6: "ALREADY_EXISTS",
    7: "PERMISSION_DENIED",
    8: "RESOURCE_EXHAUSTED",
    9: "FAILED_PRECONDITION",
    10: "ABORTED",
    11: "OUT_OF_RANGE",
    12: "UNIMPLEMENTED",
    13: "INTERNAL",
    14: "UNAVAILABLE",
    15: "DATA_LOSS",
    16: "UNAUTHENTICATED",
}


def _extract_endpoint_attributes(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Extracts server.address and server.port from client options if present."""
    attrs: dict[str, Any] = {}
    endpoint = None
    if isinstance(client_options, dict):
        endpoint = client_options.get("api_endpoint")
    elif client_options is not None:
        endpoint = getattr(client_options, "api_endpoint", None)

    if endpoint and isinstance(endpoint, str):
        clean = endpoint.replace("http://", "").replace("https://", "").strip("/")
        if clean:
            if ":" in clean:
                host, port_str = clean.split(":", 1)
                attrs["server.address"] = host
                try:
                    attrs["server.port"] = int(port_str)
                except ValueError:
                    attrs["server.port"] = 443
            else:
                attrs["server.address"] = clean
                attrs["server.port"] = 443
    return attrs


def _extract_t4_attributes(request: Any) -> dict[str, Any]:
    """Extracts Google Cloud T4 semantic and resource attributes from a gRPC request object.

    Args:
        request: The gRPC request object.

    Returns:
        dict[str, Any]: A dictionary of semantic attributes.
    """
    attrs: dict[str, Any] = {
        "rpc.system.name": "grpc",
    }
    if request is None:
        return attrs

    resend_count = getattr(request, "resend_count", None)
    if isinstance(resend_count, int) and resend_count > 0:
        attrs["gcp.grpc.resend_count"] = resend_count

    name = getattr(request, "name", None)
    if isinstance(name, str) and name:
        attrs["gcp.resource.destination.id"] = name
    else:
        parent = getattr(request, "parent", None)
        if isinstance(parent, str) and parent:
            attrs["gcp.resource.destination.id"] = parent

    return attrs


def _make_client_request_hook(
    endpoint_attrs: dict[str, Any] | None = None,
) -> Callable[[Any, Any], None]:
    """Creates an OpenTelemetry client request hook with optional endpoint attributes."""

    def client_request_hook(span: Any, request: Any) -> None:
        if span is None or not getattr(span, "is_recording", lambda: True)():
            return
        attrs = _extract_t4_attributes(request)
        if endpoint_attrs:
            attrs.update(endpoint_attrs)
        for key, value in attrs.items():
            span.set_attribute(key, value)

    return client_request_hook


_client_request_hook = _make_client_request_hook()


def _client_response_hook(span: Any, response: Any) -> None:
    """OpenTelemetry client response hook to inject gRPC response status attributes into the span."""
    if span is None or not getattr(span, "is_recording", lambda: True)():
        return

    status_str = "OK"
    code_fn = getattr(response, "code", None)
    if callable(code_fn):
        try:
            code_val = code_fn()
            status_str = getattr(code_val, "name", None) or _STATUS_CODE_NAMES.get(
                code_val, str(code_val)
            )
        except Exception:
            pass

    span.set_attribute("rpc.response.status_code", status_str)
    if status_str != "OK":
        span.set_attribute("error.type", status_str)
        details_fn = getattr(response, "details", None)
        if callable(details_fn):
            try:
                details = details_fn()
                if details:
                    span.set_attribute("status.message", str(details))
            except Exception:
                pass


def _get_tracer_provider(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> opentelemetry.trace.TracerProvider | None:
    """Extracts the OpenTelemetry tracer provider from client options if present.

    Args:
        client_options: The client options object or dictionary.

    Returns:
        opentelemetry.trace.TracerProvider | None: The tracer provider if present,
            None otherwise.
    """
    if isinstance(client_options, dict):
        return client_options.get(_TRACER_PROVIDER)
    elif client_options is not None:
        return getattr(client_options, _TRACER_PROVIDER, None)
    return None


def get_otel_interceptor(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> Callable[[grpc.Channel], grpc.Channel] | None:
    """Returns an interceptor callable that wraps a sync gRPC channel with OpenTelemetry tracing.

    Args:
        client_options: The client options object or dictionary used for feature gating
            and extracting the tracer provider.

    Returns:
        Callable[[grpc.Channel], grpc.Channel] | None: An interceptor callable if OpenTelemetry
            tracing is enabled and installed, None otherwise.
    """
    if not is_otel_capabilities_enabled(client_options):
        return None

    import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found]

    endpoint_attrs = _extract_endpoint_attributes(client_options)
    request_hook = (
        _make_client_request_hook(endpoint_attrs)
        if endpoint_attrs
        else _client_request_hook
    )

    interceptor: ClientInterceptor = otel_grpc.client_interceptor(
        tracer_provider=_get_tracer_provider(client_options),
        request_hook=request_hook,
        response_hook=_client_response_hook,
    )

    def otel_interceptor(channel: grpc.Channel) -> grpc.Channel:
        return otel_grpc.intercept_channel(channel, interceptor)

    return otel_interceptor


def get_otel_async_interceptor(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> Sequence[grpc.aio.ClientInterceptor] | None:
    """Returns async gRPC client interceptors for OpenTelemetry tracing.

    Args:
        client_options: The client options object or dictionary used for feature gating
            and extracting the tracer provider.

    Returns:
        Sequence[grpc.aio.ClientInterceptor] | None: Instantiated OpenTelemetry async
            client interceptors if tracing is enabled and installed, None otherwise.
    """
    if not is_otel_capabilities_enabled(client_options):
        return None

    # Ignored by mypy: Optional dependency only loaded if early-return is skipped
    import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found]

    endpoint_attrs = _extract_endpoint_attributes(client_options)
    request_hook = (
        _make_client_request_hook(endpoint_attrs)
        if endpoint_attrs
        else _client_request_hook
    )

    return otel_grpc.aio_client_interceptors(
        tracer_provider=_get_tracer_provider(client_options),
        request_hook=request_hook,
        response_hook=_client_response_hook,
    )
