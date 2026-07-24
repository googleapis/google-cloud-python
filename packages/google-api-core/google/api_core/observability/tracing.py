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

"""OpenTelemetry Tracing Enrichment Interceptors."""

from typing import Any, Callable, Dict, Optional

import grpc
from opentelemetry import trace


class OtelUnaryClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    """A gRPC client interceptor that creates OpenTelemetry spans for outgoing requests.

    This interceptor explicitly creates a standard SpanKind.CLIENT span for each network attempt
    and enriches it with standard Google Cloud attributes.
    """

    def __init__(
        self,
        static_attributes: Optional[Dict[str, Any]] = None,
    ):
        """Initializes the OtelUnaryClientInterceptor.

        Args:
            static_attributes: Standard static attributes to attach to every span.
                E.g. {"gcp.client.repo": "googleapis/google-cloud-python"}
        """
        self._static_attributes = static_attributes or {}

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, Any], Any],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        from google.api_core._feature_gating_helpers import resolve_feature_flags

        # For now, we only check environment variables as we don't have access to ClientOptions here.
        # To support programmatic configuration, we would need to pass it during Client
        # initialization.
        # TODO: we need to refactor resolve_feature_flags to allows feature_key to be optional.
        enabled = resolve_feature_flags(
            env_var="GOOGLE_CLOUD_PYTHON_TRACING_ENABLED",
            feature_key="tracer_provider",
        )

        if not enabled:
            return continuation(client_call_details, request)

        tracer = trace.get_tracer(__name__)

        # Determine span name (e.g., from client_call_details.method)
        span_name = client_call_details.method

        with tracer.start_as_current_span(
            span_name, kind=trace.SpanKind.CLIENT
        ) as span:
            if span.is_recording():
                # Inject static attributes
                for key, val in self._static_attributes.items():
                    span.set_attribute(key, val)

                # Extract dynamic attributes from metadata
                for key, value in client_call_details.metadata:
                    if key == "x-goog-request-params":
                        try:
                            # x-goog-request-params is urlencoded string of key=value pairs separated by &
                            params = dict(
                                p.split("=") for p in value.split("&") if "=" in p
                            )

                            # Standard resource identifiers are usually in 'name' or 'parent'
                            resource_id = params.get("name") or params.get("parent")
                            if resource_id:
                                span.set_attribute(
                                    "gcp.resource.destination.id", resource_id
                                )
                        except Exception:
                            # Fail open if parsing fails to avoid breaking the request
                            pass

                span.set_attribute("rpc.system.name", "grpc")

            return continuation(client_call_details, request)
