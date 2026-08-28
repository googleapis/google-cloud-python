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

from typing import Any, Optional

from google.api_core import _feature_gating_helpers
from google.api_core.client_options import ClientOptions

_TRACER_PROVIDER = "tracer_provider"


def is_otel_capabilities_enabled(
    client_options: Optional[ClientOptions | dict[str, Any]] = None,
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


def apply_otel_capabilities_to_channel(
    channel: Any,
    client_options: Optional[ClientOptions | dict[str, Any]] = None,
) -> Any:
    """Applies OTel capabilities (like tracing) to the channel.

    Precondition: This function assumes `is_otel_capabilities_enabled` has already
    been called and returned `True`, i.e. in the Client. At this time
    this function is not intended to be standalone.

    Args:
        channel: The raw gRPC channel to wrap.
        client_options: The client options object or dictionary.

    Returns:
        Any: The intercepted channel.

    Raises:
        ImportError: If OpenTelemetry packages are not installed and this function
            is called directly (bypassing the precondition).
    """
    import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found]

    tracer_provider = None
    if isinstance(client_options, dict):
        tracer_provider = client_options.get(_TRACER_PROVIDER)
    elif client_options is not None:
        tracer_provider = getattr(client_options, _TRACER_PROVIDER, None)

    interceptor = otel_grpc.client_interceptor(tracer_provider=tracer_provider)

    # We use OTel's own compatible applier to avoid standard gRPC TypeError.
    return otel_grpc.intercept_channel(channel, interceptor)
