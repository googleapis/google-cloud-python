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

import functools
from typing import TYPE_CHECKING, Any, Callable

from google.api_core import _feature_gating_helpers
from google.api_core.client_options import ClientOptions

if TYPE_CHECKING:
    from google.api_core.grpc_helpers import ChannelWrapperCallable
else:
    ChannelWrapperCallable = Callable[[Any], Any]

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


def _get_otel_interceptor(
    client_options: ClientOptions | dict[str, Any] | None = None,
    is_async: bool = False,
) -> Any:
    """Instantiates a sync or async OpenTelemetry gRPC client interceptor.

    Args:
        client_options: The client options object or dictionary.
        is_async: If True, returns an async interceptor (`aio_client_interceptor`),
            otherwise returns a sync interceptor (`client_interceptor`).

    Returns:
        Any: The instantiated OpenTelemetry client interceptor.
    """
    import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found]

    tracer_provider = None
    if isinstance(client_options, dict):
        tracer_provider = client_options.get(_TRACER_PROVIDER)
    elif client_options is not None:
        tracer_provider = getattr(client_options, _TRACER_PROVIDER, None)

    if is_async:
        return otel_grpc.aio_client_interceptor(tracer_provider=tracer_provider)
    return otel_grpc.client_interceptor(tracer_provider=tracer_provider)


def get_otel_channel_wrapper(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> ChannelWrapperCallable | None:
    """Returns a channel wrapper callable that wraps a sync gRPC channel with OpenTelemetry tracing.

    Args:
        client_options: The client options object or dictionary used for feature gating
            and extracting the tracer provider.

    Returns:
        Optional[ChannelWrapperCallable]: A channel-wrapping callable if OpenTelemetry
            tracing is enabled and installed, None otherwise.
    """
    if not is_otel_capabilities_enabled(client_options):
        return None

    import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found]

    interceptor = _get_otel_interceptor(client_options, is_async=False)
    return functools.partial(otel_grpc.intercept_channel, interceptor=interceptor)


def get_otel_async_interceptor(
    client_options: ClientOptions | dict[str, Any] | None = None,
) -> Any | None:
    """Returns an async gRPC client interceptor for OpenTelemetry tracing.

    Args:
        client_options: The client options object or dictionary used for feature gating
            and extracting the tracer provider.

    Returns:
        Optional[Any]: An instantiated OpenTelemetry async client interceptor
            if tracing is enabled and installed, None otherwise.
    """
    if not is_otel_capabilities_enabled(client_options):
        return None

    return _get_otel_interceptor(client_options, is_async=True)
