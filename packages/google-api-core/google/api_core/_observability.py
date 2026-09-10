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

import urllib.parse
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


def _extract_endpoint_attributes(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Extracts server.address, server.port (if non-default), and url.domain from client options if present.

    Args:
        client_options: The client options object or dictionary.

    Returns:
        dict[str, Any]: A dictionary containing url.domain and, if an api_endpoint is configured,
            server.address and non-default server.port.
    """
    attrs: dict[str, Any] = {}
    endpoint = None
    universe_domain = None

    if isinstance(client_options, dict):
        endpoint = client_options.get("api_endpoint")
        universe_domain = client_options.get("universe_domain")
    elif client_options is not None:
        endpoint = getattr(client_options, "api_endpoint", None)
        universe_domain = getattr(client_options, "universe_domain", None)

    attrs["url.domain"] = universe_domain or "googleapis.com"

    if endpoint and isinstance(endpoint, str):
        target = endpoint if "//" in endpoint else f"//{endpoint}"
        parsed = urllib.parse.urlsplit(target)
        if parsed.hostname:
            attrs["server.address"] = parsed.hostname
        if parsed.port:
            scheme = parsed.scheme.lower()
            is_default_port = (parsed.port == 443 and scheme in ("https", "")) or (
                parsed.port == 80 and scheme == "http"
            )
            if not is_default_port:
                attrs["server.port"] = parsed.port
    return attrs


def _extract_grpc_request_attributes(request: Any) -> dict[str, Any]:
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

    return attrs


def _extract_error_attributes(exc: Any) -> dict[str, Any]:
    """Extracts gcp.errors.domain, gcp.errors.metadata.*, and error.type from an exception or ErrorInfo.

    Args:
        exc: An exception (such as GoogleAPICallError or grpc.RpcError) or ErrorInfo object.

    Returns:
        dict[str, Any]: Extracted error attributes.
    """
    attrs: dict[str, Any] = {}
    if exc is None:
        return attrs

    error_info = getattr(exc, "error_info", None)
    if error_info is None and hasattr(exc, "trailing_metadata"):
        try:
            from google.api_core import exceptions

            _, error_info = exceptions._parse_grpc_error_details(exc)
        except Exception:
            pass

    if error_info is not None:
        domain = getattr(error_info, "domain", None)
        if domain and isinstance(domain, str):
            attrs["gcp.errors.domain"] = domain
        reason = getattr(error_info, "reason", None)
        if reason and isinstance(reason, str):
            attrs["error.type"] = reason
        metadata = getattr(error_info, "metadata", None)
        if metadata and hasattr(metadata, "items"):
            for k, v in metadata.items():
                attrs[f"gcp.errors.metadata.{k}"] = str(v)

    return attrs


def _make_grpc_client_request_hook(
    endpoint_attrs: dict[str, Any] | None = None,
) -> Callable[[Any, Any], None]:
    """Creates an OpenTelemetry gRPC client request hook with optional endpoint attributes.

    Args:
        endpoint_attrs: Optional static endpoint attributes to attach to every span.

    Returns:
        Callable[[Any, Any], None]: The request hook callback.
    """
    static_attrs = dict(endpoint_attrs) if endpoint_attrs else {}

    def client_request_hook(span: Any, request: Any) -> None:
        if span is None or not getattr(span, "is_recording", lambda: True)():
            return

        # Upstream opentelemetry-instrumentation-grpc names spans with a leading slash
        # (e.g. "/package.Service/Method") and sets only the short name on rpc.method.
        # Normalize span.name and rpc.method to the fully-qualified name without leading slash.
        span_name = getattr(span, "name", None)
        clean_method_name = None
        if isinstance(span_name, str) and span_name.startswith("/"):
            clean_method_name = span_name.lstrip("/")
            if hasattr(span, "update_name"):
                span.update_name(clean_method_name)

        # Remove duplicate legacy rpc.system attribute set by stock instrumentation
        # in favor of modern rpc.system.name ("grpc") per PRD changelog.
        span_attributes = getattr(span, "_attributes", None)
        if hasattr(span_attributes, "pop"):
            span_attributes.pop("rpc.system", None)

        attrs = _extract_grpc_request_attributes(request)
        if clean_method_name:
            attrs["rpc.method"] = clean_method_name
        if static_attrs:
            attrs.update(static_attrs)
        for key, value in attrs.items():
            span.set_attribute(key, value)

    return client_request_hook


_grpc_client_request_hook = _make_grpc_client_request_hook()


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
    request_hook = _make_grpc_client_request_hook(endpoint_attrs)

    interceptor: ClientInterceptor = otel_grpc.client_interceptor(
        tracer_provider=_get_tracer_provider(client_options),
        request_hook=request_hook,
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
    request_hook = _make_grpc_client_request_hook(endpoint_attrs)

    return otel_grpc.aio_client_interceptors(
        tracer_provider=_get_tracer_provider(client_options),
        request_hook=request_hook,
    )
