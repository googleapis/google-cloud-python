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

import contextlib
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
        parsed = None
        hostname = None
        port = None
        try:
            parsed = urllib.parse.urlsplit(target)
            hostname = parsed.hostname
            port = parsed.port
        except ValueError:
            pass

        if hostname:
            attrs["server.address"] = hostname
        if port and parsed:
            scheme = parsed.scheme.lower()
            is_default_port = (port == 443 and scheme in ("https", "")) or (
                port == 80 and scheme == "http"
            )
            if not is_default_port:
                attrs["server.port"] = port
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

        # Upstream opentelemetry-instrumentation-grpc may format span names with a
        # leading slash (e.g. "/package.Service/Method"). Normalize the span name
        # and ensure rpc.method is always captured as the clean, fully-qualified name.
        span_name = getattr(span, "name", None)
        if isinstance(span_name, str) and span_name:
            clean_method_name = span_name.lstrip("/")
            if span_name.startswith("/") and hasattr(span, "update_name"):
                span.update_name(clean_method_name)
            span.set_attribute("rpc.method", clean_method_name)

        attrs: dict[str, Any] = {
            "rpc.system.name": "grpc",
        }
        if static_attrs:
            attrs.update(static_attrs)
        for key, value in attrs.items():
            span.set_attribute(key, value)

    return client_request_hook


_grpc_client_request_hook = _make_grpc_client_request_hook()


def _grpc_client_response_hook(span: Any, response: Any) -> None:
    """OpenTelemetry gRPC client response hook to record successful response status.

    Upstream ``opentelemetry-instrumentation-grpc`` sets the integer status code
    ``rpc.grpc.status_code`` (e.g. 0), but does not record the modern string status
    ``rpc.response.status_code`` (e.g. "OK") required by Cloud Trace and current
    OpenTelemetry semantic conventions (v1.27.0+).

    This hook enriches successful RPC attempt spans with ``rpc.response.status_code = "OK"``.
    Errors and non-OK statuses are handled at the Tier 3 method span layer or upstream.

    Upstream handles synchronous and asynchronous invocations differently:
    - **Synchronous gRPC**: Upstream only invokes the response hook when an RPC call
      succeeds. On failure, the hook is bypassed entirely.
    - **Asynchronous gRPC**: Upstream invokes the response hook unconditionally for
      both successes and failures (passing exception details on error). However, it
      always marks ``span.status`` with an error status before calling the hook.

    Because of this disparity, this hook checks ``span.status`` to guard against
    async failure callbacks while allowing synchronous and successful asynchronous
    calls to be marked "OK".

    Note:
        If upstream ``opentelemetry-instrumentation-grpc`` adds native support for
        modern ``rpc.response.status_code`` in future releases, this hook can be retired.

    Args:
        span: The OpenTelemetry span.
        response: The gRPC response object or details.
    """
    if span is None or not getattr(span, "is_recording", lambda: False)():
        return

    # Guard against upstream async calls that invoke this hook on failures.
    status = getattr(span, "status", None)
    status_code = getattr(status, "status_code", None)
    if (
        getattr(status_code, "name", None) == "ERROR"
        or getattr(status_code, "value", None) == 2
    ):
        return

    span.set_attribute("rpc.response.status_code", "OK")


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
        response_hook=_grpc_client_response_hook,
    )

    def otel_interceptor(channel: grpc.Channel) -> grpc.Channel:
        return otel_grpc.intercept_channel(channel, interceptor)

    otel_interceptor._is_otel_interceptor = True  # type: ignore[attr-defined]
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
        response_hook=_grpc_client_response_hook,
    )


# The `start_http_span` context manager deliberately supports two distinct invocation styles:
# 1. Bundled Request Object: `start_http_span(request, ...)`
#    Used when callers already possess an HTTP request instance (such as
#    requests.PreparedRequest or urllib.request.Request) with `.method`, `.url`, etc.
# 2. Unpacked Keyword Arguments: `start_http_span(method=..., url=..., headers=..., body=...)`
#    Used by generated GAPIC REST transports (_shared_macros.j2). In GAPIC templates,
#    requests are assembled from local strings and dictionaries before hitting the session.
#    Supporting keyword arguments avoids the CPU and memory overhead of instantiating
#    a throwaway dummy request object on every single RPC execution.
@contextlib.contextmanager
def start_http_span(
    request: Any = None,
    *,
    method: str | None = None,
    url: str | None = None,
    url_template: str | None = None,
    headers: dict[str, Any] | None = None,
    body: Any = None,
    client_options: ClientOptions | dict[str, Any] | None = None,
):
    """Context manager for tracing an HTTP wire request with OpenTelemetry.

    Supports two calling conventions:
    - Pass a single `request` object (such as `requests.PreparedRequest`).
    - Pass explicit keyword arguments (`method`, `url`, `headers`, `body`, `client_options`).

    Injects W3C traceparent headers into request headers and attaches standard
    semantic attributes. If tracing is disabled or OpenTelemetry is not installed,
    yields None.

    Args:
        request: Optional HTTP request object with .method, .url, .headers, and .body.
        method: HTTP request method (e.g. 'GET', 'POST').
        url: Full request URL.
        url_template: Low-cardinality URL path template (e.g. '/v1/{name}:echo').
        headers: Outgoing HTTP headers dictionary for traceparent injection.
        body: HTTP request body payload.
        client_options: Client options used for feature gating and tracer extraction.

    Yields:
        Optional[Span]: The active OpenTelemetry span or None.
    """
    # Defensively handle case where client_options was passed as the first positional argument
    if (
        isinstance(request, (ClientOptions, dict))
        and client_options is None
        and method is not None
    ):
        client_options = request
        request = None

    if not is_otel_capabilities_enabled(client_options):
        yield None
        return

    try:
        from opentelemetry import trace
        from opentelemetry.trace.propagation.tracecontext import (  # type: ignore[import-not-found]
            TraceContextTextMapPropagator,
        )

        tracer_provider = _get_tracer_provider(client_options)
        if tracer_provider is not None:
            tracer = tracer_provider.get_tracer("google.api_core")
        else:
            tracer = trace.get_tracer("google.api_core")

        # Resolve request attributes from either bundled object or explicit keyword arguments
        if request is not None:
            resolved_method = getattr(request, "method", "HTTP") or "HTTP"
            resolved_url = getattr(request, "url", "") or ""
            resolved_headers = getattr(request, "headers", None)
            resolved_body = getattr(request, "body", None)
        else:
            resolved_method = method or "HTTP"
            resolved_url = url or ""
            resolved_headers = headers
            resolved_body = body

        resolved_method = resolved_method.upper()
        endpoint_attrs = _extract_endpoint_attributes(client_options)

        server_address = endpoint_attrs.get("server.address")
        server_port = endpoint_attrs.get("server.port")
        if not server_address and resolved_url:
            try:
                parsed = urllib.parse.urlsplit(resolved_url)
                server_address = parsed.hostname
                if not server_port and parsed.port:
                    server_port = parsed.port
            except Exception:
                pass

        span_name = resolved_method
        span_attributes: dict[str, Any] = {
            "http.request.method": resolved_method,
            "server.address": server_address or "",
            "server.port": server_port or 443,
            "url.domain": endpoint_attrs.get("url.domain", "googleapis.com"),
        }
        if url_template:
            span_attributes["url.template"] = url_template
        if resolved_url:
            span_attributes["url.full"] = resolved_url

        if resolved_body is not None and isinstance(resolved_body, (bytes, str)):
            span_attributes["http.request.body.size"] = len(resolved_body)

        with tracer.start_as_current_span(
            span_name,
            kind=trace.SpanKind.CLIENT,
            attributes=span_attributes,
        ) as span:
            if resolved_headers is not None and hasattr(
                resolved_headers, "__setitem__"
            ):
                try:
                    TraceContextTextMapPropagator().inject(resolved_headers)
                except Exception:
                    pass

            yield span
    except Exception:
        yield None


def record_http_response(span: Any, response: Any) -> None:
    """Record HTTP response attributes on the wire span.

    Args:
        span: The active OpenTelemetry span.
        response: The HTTP response object (e.g. requests.Response).
    """
    if span is None or not hasattr(span, "set_attribute"):
        return

    try:
        from opentelemetry.trace.status import (  # type: ignore[import-not-found]
            Status,
            StatusCode,
        )

        status_code = getattr(response, "status_code", None)
        if status_code is not None:
            span.set_attribute("http.response.status_code", int(status_code))
            if int(status_code) >= 400:
                span.set_status(Status(StatusCode.ERROR))
            else:
                span.set_status(Status(StatusCode.OK))

        headers = getattr(response, "headers", None)
        if headers and "Content-Length" in headers:
            try:
                span.set_attribute(
                    "http.response.body.size", int(headers["Content-Length"])
                )
            except (ValueError, TypeError):
                pass
        elif hasattr(response, "_content") and response._content is not None:
            try:
                span.set_attribute("http.response.body.size", len(response._content))
            except Exception:
                pass
    except Exception:
        pass


def record_http_error(span: Any, exc: BaseException) -> None:
    """Record an HTTP error/exception on the wire span.

    Args:
        span: The active OpenTelemetry span.
        exc: The exception raised during dispatch.
    """
    if span is None:
        return

    try:
        from opentelemetry.trace.status import (  # type: ignore[import-not-found]
            Status,
            StatusCode,
        )

        if hasattr(span, "record_exception"):
            span.record_exception(exc)
        if hasattr(span, "set_status"):
            span.set_status(Status(StatusCode.ERROR))
        if hasattr(span, "set_attribute"):
            status_code = getattr(exc, "code", None) or getattr(
                exc, "status_code", None
            )
            if status_code:
                span.set_attribute("error.type", str(status_code))
            else:
                span.set_attribute("error.type", exc.__class__.__name__)
            msg = str(exc)
            if msg:
                span.set_attribute("status.message", msg)
    except Exception:
        pass
