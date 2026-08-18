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


def get_otel_grpc_interceptor(
    client_options: Optional[ClientOptions] = None,
    env_var: str = "GOOGLE_CLOUD_PYTHON_TRACING_ENABLED",
) -> Optional[Any]:
    """Checks feature flags, attempts to import OTel, and returns the interceptor.

    This helper centralizes the logic for checking environment variables,
    programmatic configuration (via ClientOptions), and soft-importing
    the `opentelemetry-instrumentation-grpc` package.

    Args:
        client_options: The client options object, potentially holding a tracer_provider.
        env_var: The environment variable to check for enablement.

    Returns:
        Optional[Any]: An OpenTelemetry gRPC client interceptor instance if enabled
            and installed, otherwise None.
    """
    is_tracing_enabled = _feature_gating_helpers.resolve_feature_flags(
        env_var=env_var,
        feature_key="tracer_provider",
        configuration=client_options,
    )

    if is_tracing_enabled:
        try:
            import opentelemetry.instrumentation.grpc as otel_grpc  # type: ignore[import-not-found]

            tracer_provider = getattr(client_options, "tracer_provider", None)
            return otel_grpc.client_interceptor(tracer_provider=tracer_provider)
        except ImportError:
            # Failed open if OTel is not installed but feature was requested.
            # We might want to warn here, but for now we follow the "silent fail open" pattern
            # or let the user handle it if they care.
            pass

    return None
