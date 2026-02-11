# Copyright 2025 Google LLC All rights reserved.
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
"""
This module provides functionality for capturing metrics in Cloud Spanner operations.

It includes a context manager class, MetricsCapture, which automatically handles the
start and completion of metrics tracing for a given operation. This ensures that metrics
are consistently recorded for Cloud Spanner operations, facilitating observability and
performance monitoring.
"""

from contextvars import Token

from .spanner_metrics_tracer_factory import SpannerMetricsTracerFactory


class MetricsCapture:
    """Context manager for capturing metrics in Cloud Spanner operations.

    This class provides a context manager interface to automatically handle
    the start and completion of metrics tracing for a given operation.
    """

    _token: Token
    """Token to reset the context variable after the operation completes."""

    def __enter__(self):
        """Enter the runtime context related to this object.

        This method initializes a new metrics tracer for the operation and
        records the start of the operation.

        Returns:
            MetricsCapture: The instance of the context manager.
        """
        # Short circuit out if metrics are disabled
        factory = SpannerMetricsTracerFactory()
        if not factory.enabled:
            return self

        # Define a new metrics tracer for the new operation
        # Set the context var and keep the token for reset
        tracer = factory.create_metrics_tracer()
        self._token = SpannerMetricsTracerFactory.set_current_tracer(tracer)
        if tracer:
            tracer.record_operation_start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object.

        This method records the completion of the operation. If an exception
        occurred, it will be propagated after the metrics are recorded.

        Args:
            exc_type (Type[BaseException]): The exception type.
            exc_value (BaseException): The exception value.
            traceback (TracebackType): The traceback object.

        Returns:
            bool: False to propagate the exception if any occurred.
        """
        # Short circuit out if metrics are disable
        if not SpannerMetricsTracerFactory().enabled:
            return False

        tracer = SpannerMetricsTracerFactory.get_current_tracer()
        if tracer:
            tracer.record_operation_completion()

        # Reset the context var using the token
        if getattr(self, "_token", None):
            SpannerMetricsTracerFactory.reset_current_tracer(self._token)
        return False  # Propagate the exception if any
