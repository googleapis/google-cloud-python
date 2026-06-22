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


class OtelSpanEnricher(grpc.UnaryUnaryClientInterceptor):
    """A gRPC client interceptor that enriches the active OpenTelemetry span.

    This interceptor relies on the standard OpenTelemetry gRPC instrumentor
    to create the baseline span. It runs in the interceptor chain to inject
    additional Google Cloud specific domain attributes.
    """

    def __init__(
        self,
        static_attributes: Optional[Dict[str, Any]] = None,
        attribute_extractor: Optional[
            Callable[[Any, grpc.ClientCallDetails], Dict[str, Any]]
        ] = None,
    ):
        """Initializes the OtelSpanEnricher.

        Args:
            static_attributes: Standard static attributes to attach to every span.
                E.g. {"gcp.client.repo": "googleapis/google-cloud-python"}
            attribute_extractor: A callable that extracts dynamic attributes from
                the request and client call details.
        """
        self._static_attributes = static_attributes or {}
        self._attribute_extractor = attribute_extractor

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, Any], Any],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Any:
        span = trace.get_current_span()

        if span.is_recording():
            # Inject static attributes
            for key, val in self._static_attributes.items():
                span.set_attribute(key, val)

            # Extract and inject dynamic attributes
            if self._attribute_extractor:
                try:
                    dynamic_attrs = self._attribute_extractor(
                        request, client_call_details
                    )
                    for key, val in dynamic_attrs.items():
                        if val is not None:
                            span.set_attribute(key, val)
                except Exception:
                    # Prevent custom extractor exceptions from failing the RPC
                    pass

        return continuation(client_call_details, request)
