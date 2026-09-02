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
    # The `# noqa: F401` comment avoid flake8 "imported but not used" errors.
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

    interceptor: ClientInterceptor = otel_grpc.client_interceptor(
        tracer_provider=_get_tracer_provider(client_options)
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

    return otel_grpc.aio_client_interceptors(
        tracer_provider=_get_tracer_provider(client_options)
    )
