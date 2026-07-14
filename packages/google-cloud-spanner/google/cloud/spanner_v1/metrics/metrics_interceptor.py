# Copyright 2025 Google LLC
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

"""Interceptor for collecting Cloud Spanner metrics."""

import inspect
import logging
import re
from typing import Any, Dict

import grpc
from grpc_interceptor import ClientInterceptor

from .constants import GOOGLE_CLOUD_RESOURCE_KEY, SPANNER_METHOD_PREFIX
from .spanner_metrics_tracer_factory import SpannerMetricsTracerFactory

logger = logging.getLogger(__name__)


class MetricsInterceptor(ClientInterceptor):
    """Interceptor that collects metrics for Cloud Spanner operations."""

    @staticmethod
    def _parse_resource_path(path: str) -> dict:
        """Parse the resource path to extract project, instance and database.

        Args:
            path (str): The resource path from the request

        Returns:
            dict: Extracted resource components
        """
        # Match paths like:
        # projects/{project}/instances/{instance}/databases/{database}/sessions/{session}
        # projects/{project}/instances/{instance}/databases/{database}
        # projects/{project}/instances/{instance}
        pattern = r"^projects/(?P<project>[^/]+)(/instances/(?P<instance>[^/]+))?(/databases/(?P<database>[^/]+))?(/sessions/(?P<session>[^/]+))?.*$"
        match = re.match(pattern, path)
        if match:
            return {k: v for k, v in match.groupdict().items() if v is not None}
        return {}

    @staticmethod
    def _extract_resource_from_path(metadata: Dict[str, str]) -> Dict[str, str]:
        """
        Extracts resource information from the metadata based on the path.

        This method iterates through the metadata dictionary to find the first tuple containing the key 'google-cloud-resource-prefix'. It then extracts the path from this tuple and parses it to extract project, instance, and database information using the _parse_resource_path method.

        Args:
            metadata (Dict[str, str]): A dictionary containing metadata information.

        Returns:
            Dict[str, str]: A dictionary containing extracted project, instance, and database information.
        """
        # Extract resource info from the first metadata tuple containing :path
        path = next(
            (value for key, value in metadata if key == GOOGLE_CLOUD_RESOURCE_KEY), ""
        )

        resources = MetricsInterceptor._parse_resource_path(path)
        return resources

    @staticmethod
    def _set_metrics_tracer_attributes(resources: Dict[str, str]) -> None:
        """
        Sets the metric tracer attributes based on the provided resources.

        This method updates the current metric tracer's attributes with the project, instance, and database information extracted from the resources dictionary. If the current metric tracer is not set, the method does nothing.

        Args:
            resources (Dict[str, str]): A dictionary containing project, instance, and database information.
        """
        tracer = SpannerMetricsTracerFactory.get_current_tracer()
        if tracer is None:
            return

        if resources:
            if "project" in resources:
                tracer.set_project(resources["project"])
            if "instance" in resources:
                tracer.set_instance(resources["instance"])
            if "database" in resources:
                tracer.set_database(resources["database"])

    def intercept(self, invoked_method, request_or_iterator, call_details):
        """Intercept gRPC calls to collect metrics.

        Args:
            invoked_method: The RPC method
            request_or_iterator: The RPC request
            call_details: Details about the RPC call

        Returns:
            The RPC response
        """
        factory = SpannerMetricsTracerFactory()
        tracer = SpannerMetricsTracerFactory.get_current_tracer()
        if tracer is None or not factory.enabled:
            return invoked_method(request_or_iterator, call_details)

        # Setup Metric Tracer attributes from call details
        ## Extract Project / Instance / Database from header information if not already set
        if not (
            tracer.client_attributes.get("project_id")
            and tracer.client_attributes.get("instance_id")
            and tracer.client_attributes.get("database")
        ):
            resources = self._extract_resource_from_path(call_details.metadata)
            self._set_metrics_tracer_attributes(resources)

        ## Format method to be be spanner.<method name>
        method_str = call_details.method
        if isinstance(method_str, bytes):
            method_str = method_str.decode("utf-8")
        method_name = method_str.removeprefix(SPANNER_METHOD_PREFIX).replace("/", ".")

        tracer.set_method(method_name)
        tracer.record_attempt_start()
        response = invoked_method(request_or_iterator, call_details)

        return _wrap_response(response, tracer)


def _wrap_response(response: Any, tracer: Any) -> Any:
    """Wraps the response if it is streaming, or records metrics immediately if unary."""
    if hasattr(response, "__next__"):
        return _StreamingResponseWrapper(response, tracer)
    else:
        # Unary call: execute completion and record metrics immediately
        try:
            tracer.record_attempt_completion()
            metadata = []
            if hasattr(response, "initial_metadata"):
                try:
                    metadata.extend(response.initial_metadata() or [])
                except Exception as e:
                    logger.warning(f"Failed to retrieve initial metadata: {e}")
            tracer.record_gfe_metrics(metadata)
            tracer.record_afe_metrics(metadata)
        except Exception as e:
            logger.warning(f"Failed to record metrics: {e}")
        return response


class AsyncMetricsInterceptor(
    grpc.aio.UnaryUnaryClientInterceptor,
    grpc.aio.UnaryStreamClientInterceptor,
    grpc.aio.StreamUnaryClientInterceptor,
    grpc.aio.StreamStreamClientInterceptor,
):
    """Async Interceptor that collects metrics for Cloud Spanner operations."""

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        return await self._async_intercept(continuation, client_call_details, request)

    async def intercept_unary_stream(self, continuation, client_call_details, request):
        return await self._async_intercept(continuation, client_call_details, request)

    async def intercept_stream_unary(
        self, continuation, client_call_details, request_iterator
    ):
        return await self._async_intercept(
            continuation, client_call_details, request_iterator
        )

    async def intercept_stream_stream(
        self, continuation, client_call_details, request_iterator
    ):
        return await self._async_intercept(
            continuation, client_call_details, request_iterator
        )

    async def _async_intercept(
        self,
        continuation: Any,
        call_details: grpc.ClientCallDetails,
        request_or_iterator: Any,
    ) -> Any:
        # Implementation for async interceptor
        factory = SpannerMetricsTracerFactory()
        tracer = SpannerMetricsTracerFactory.get_current_tracer()
        if tracer is None or not factory.enabled:
            return await continuation(call_details, request_or_iterator)

        if not (
            tracer.client_attributes.get("project_id")
            and tracer.client_attributes.get("instance_id")
            and tracer.client_attributes.get("database")
        ):
            resources = MetricsInterceptor._extract_resource_from_path(
                call_details.metadata
            )
            MetricsInterceptor._set_metrics_tracer_attributes(resources)

        method_str = call_details.method
        if isinstance(method_str, bytes):
            method_str = method_str.decode("utf-8")
        method_name = method_str.removeprefix(SPANNER_METHOD_PREFIX).replace("/", ".")

        tracer.set_method(method_name)
        tracer.record_attempt_start()
        response = await continuation(call_details, request_or_iterator)

        if hasattr(response, "__anext__"):
            return _AsyncStreamingResponseWrapper(response, tracer)
        else:
            return _AsyncUnaryResponseWrapper(response, tracer)


class _StreamingResponseWrapper:
    """Wrapper for streaming RPC response iterators to defer metrics recording."""

    def __init__(self, response, tracer):
        self._response = response
        self._tracer = tracer
        self._metrics_recorded = False
        self._iterator = None

    def __iter__(self):
        self._iterator = iter(self._response)
        return self

    def __next__(self):
        if self._iterator is None:
            self._iterator = iter(self._response)
        try:
            return next(self._iterator)
        except StopIteration:
            self._record_metrics()
            raise
        except Exception:
            self._record_metrics()
            raise

    def _record_metrics(self):
        if self._metrics_recorded:
            return
        self._metrics_recorded = True
        try:
            self._tracer.record_attempt_completion()
            metadata = []
            if hasattr(self._response, "initial_metadata"):
                try:
                    metadata.extend(self._response.initial_metadata() or [])
                except Exception as e:
                    logger.warning(f"Failed to retrieve initial metadata: {e}")
            self._tracer.record_gfe_metrics(metadata)
            self._tracer.record_afe_metrics(metadata)
        except Exception as e:
            logger.warning(f"Failed to record metrics: {e}")

    def __del__(self):
        try:
            self._record_metrics()
        except Exception:
            pass

    def __getattr__(self, name):
        return getattr(self._response, name)


class _AsyncUnaryResponseWrapper(grpc.aio.UnaryUnaryCall):
    """Wrapper for async unary RPC response to defer metrics recording until awaited."""

    def __init__(self, response, tracer):
        self._response = response
        self._tracer = tracer
        self._metrics_recorded = False

    def add_done_callback(self, *args, **kwargs):
        return getattr(self._response, "add_done_callback")(*args, **kwargs)

    def cancel(self, *args, **kwargs):
        return getattr(self._response, "cancel")(*args, **kwargs)

    def cancelled(self, *args, **kwargs):
        return getattr(self._response, "cancelled")(*args, **kwargs)

    def code(self, *args, **kwargs):
        return getattr(self._response, "code")(*args, **kwargs)

    def details(self, *args, **kwargs):
        return getattr(self._response, "details")(*args, **kwargs)

    def done(self, *args, **kwargs):
        return getattr(self._response, "done")(*args, **kwargs)

    def initial_metadata(self, *args, **kwargs):
        return getattr(self._response, "initial_metadata")(*args, **kwargs)

    def time_remaining(self, *args, **kwargs):
        return getattr(self._response, "time_remaining")(*args, **kwargs)

    def trailing_metadata(self, *args, **kwargs):
        return getattr(self._response, "trailing_metadata")(*args, **kwargs)

    def wait_for_connection(self, *args, **kwargs):
        return getattr(self._response, "wait_for_connection")(*args, **kwargs)

    def __await__(self):
        async def _wait():
            try:
                return await self._response
            finally:
                await self._record_metrics()

        return _wait().__await__()

    async def _record_metrics(self):
        if self._metrics_recorded:
            return
        self._metrics_recorded = True
        try:
            self._tracer.record_attempt_completion()
            metadata = []
            if hasattr(self._response, "initial_metadata"):
                try:
                    res = self._response.initial_metadata()
                    if inspect.isawaitable(res):
                        res = await res
                    metadata.extend(res or [])
                except Exception as e:
                    logger.warning(f"Failed to retrieve initial metadata: {e}")
            self._tracer.record_gfe_metrics(metadata)
            self._tracer.record_afe_metrics(metadata)
        except Exception as e:
            logger.warning(f"Failed to record metrics: {e}")

    def __del__(self):
        if not self._metrics_recorded:
            self._metrics_recorded = True
            try:
                self._tracer.record_attempt_completion()
            except Exception:
                pass

    def __getattr__(self, name):
        return getattr(self._response, name)


class _AsyncStreamingResponseWrapper(
    grpc.aio.UnaryStreamCall,
    grpc.aio.StreamUnaryCall,
    grpc.aio.StreamStreamCall,
):
    """Wrapper for async streaming RPC response iterators to defer metrics recording."""

    def __init__(self, response, tracer):
        self._response = response
        self._tracer = tracer
        self._metrics_recorded = False
        self._iterator = None

    def add_done_callback(self, *args, **kwargs):
        return getattr(self._response, "add_done_callback")(*args, **kwargs)

    def cancel(self, *args, **kwargs):
        return getattr(self._response, "cancel")(*args, **kwargs)

    def cancelled(self, *args, **kwargs):
        return getattr(self._response, "cancelled")(*args, **kwargs)

    def code(self, *args, **kwargs):
        return getattr(self._response, "code")(*args, **kwargs)

    def details(self, *args, **kwargs):
        return getattr(self._response, "details")(*args, **kwargs)

    def done(self, *args, **kwargs):
        return getattr(self._response, "done")(*args, **kwargs)

    def initial_metadata(self, *args, **kwargs):
        return getattr(self._response, "initial_metadata")(*args, **kwargs)

    def time_remaining(self, *args, **kwargs):
        return getattr(self._response, "time_remaining")(*args, **kwargs)

    def trailing_metadata(self, *args, **kwargs):
        return getattr(self._response, "trailing_metadata")(*args, **kwargs)

    def wait_for_connection(self, *args, **kwargs):
        return getattr(self._response, "wait_for_connection")(*args, **kwargs)

    def read(self, *args, **kwargs):
        return getattr(self._response, "read")(*args, **kwargs)

    def write(self, *args, **kwargs):
        return getattr(self._response, "write")(*args, **kwargs)

    def done_writing(self, *args, **kwargs):
        return getattr(self._response, "done_writing")(*args, **kwargs)

    def __aiter__(self):
        if hasattr(self._response, "__aiter__"):
            self._iterator = self._response.__aiter__()
        else:
            self._iterator = self._response
        return self

    async def __anext__(self):
        if self._iterator is None:
            if hasattr(self._response, "__aiter__"):
                self._iterator = self._response.__aiter__()
            else:
                self._iterator = self._response
        try:
            return await self._iterator.__anext__()
        except StopAsyncIteration:
            await self._record_metrics()
            raise
        except Exception:
            await self._record_metrics()
            raise

    async def _record_metrics(self):
        if self._metrics_recorded:
            return
        self._metrics_recorded = True
        try:
            self._tracer.record_attempt_completion()
            metadata = []
            if hasattr(self._response, "initial_metadata"):
                try:
                    res = self._response.initial_metadata()
                    if inspect.isawaitable(res):
                        res = await res
                    metadata.extend(res or [])
                except Exception as e:
                    logger.warning(f"Failed to retrieve initial metadata: {e}")
            self._tracer.record_gfe_metrics(metadata)
            self._tracer.record_afe_metrics(metadata)
        except Exception as e:
            logger.warning(f"Failed to record metrics: {e}")

    def __del__(self):
        if not self._metrics_recorded:
            self._metrics_recorded = True
            try:
                self._tracer.record_attempt_completion()
            except Exception:
                pass

    def __getattr__(self, name):
        return getattr(self._response, name)
