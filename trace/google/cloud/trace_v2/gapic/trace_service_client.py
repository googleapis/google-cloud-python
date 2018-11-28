# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Accesses the google.devtools.cloudtrace.v2 TraceService API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.trace_v2.gapic import enums
from google.cloud.trace_v2.gapic import trace_service_client_config
from google.cloud.trace_v2.gapic.transports import trace_service_grpc_transport
from google.cloud.trace_v2.proto import trace_pb2
from google.cloud.trace_v2.proto import tracing_pb2
from google.cloud.trace_v2.proto import tracing_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import timestamp_pb2
from google.protobuf import wrappers_pb2
from google.rpc import status_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-trace").version


class TraceServiceClient(object):
    """
    This file describes an API for collecting and viewing traces and spans
    within a trace.  A Trace is a collection of spans corresponding to a single
    operation or set of operations for an application. A span is an individual
    timed event which forms a node of the trace tree. A single trace may
    contain span(s) from multiple services.
    """

    SERVICE_ADDRESS = "cloudtrace.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.devtools.cloudtrace.v2.TraceService"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            TraceServiceClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project
        )

    @classmethod
    def span_path(cls, project, trace, span):
        """Return a fully-qualified span string."""
        return google.api_core.path_template.expand(
            "projects/{project}/traces/{trace}/spans/{span}",
            project=project,
            trace=trace,
            span=span,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.TraceServiceGrpcTransport,
                    Callable[[~.Credentials, type], ~.TraceServiceGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = trace_service_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=trace_service_grpc_transport.TraceServiceGrpcTransport,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = trace_service_grpc_transport.TraceServiceGrpcTransport(
                address=self.SERVICE_ADDRESS, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def batch_write_spans(
        self,
        name,
        spans,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Sends new spans to new or existing traces. You cannot update
        existing spans.

        Example:
            >>> from google.cloud import trace_v2
            >>>
            >>> client = trace_v2.TraceServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>>
            >>> # TODO: Initialize `spans`:
            >>> spans = []
            >>>
            >>> client.batch_write_spans(name, spans)

        Args:
            name (str): Required. The name of the project where the spans belong. The format is
                ``projects/[PROJECT_ID]``.
            spans (list[Union[dict, ~google.cloud.trace_v2.types.Span]]): A list of new spans. The span names must not match existing
                spans, or the results are undefined.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Span`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "batch_write_spans" not in self._inner_api_calls:
            self._inner_api_calls[
                "batch_write_spans"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.batch_write_spans,
                default_retry=self._method_configs["BatchWriteSpans"].retry,
                default_timeout=self._method_configs["BatchWriteSpans"].timeout,
                client_info=self._client_info,
            )

        request = tracing_pb2.BatchWriteSpansRequest(name=name, spans=spans)
        self._inner_api_calls["batch_write_spans"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def create_span(
        self,
        name,
        span_id,
        display_name,
        start_time,
        end_time,
        parent_span_id=None,
        attributes=None,
        stack_trace=None,
        time_events=None,
        links=None,
        status=None,
        same_process_as_parent_span=None,
        child_span_count=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Creates a new span.

        Example:
            >>> from google.cloud import trace_v2
            >>>
            >>> client = trace_v2.TraceServiceClient()
            >>>
            >>> name = client.span_path('[PROJECT]', '[TRACE]', '[SPAN]')
            >>>
            >>> # TODO: Initialize `span_id`:
            >>> span_id = ''
            >>>
            >>> # TODO: Initialize `display_name`:
            >>> display_name = {}
            >>>
            >>> # TODO: Initialize `start_time`:
            >>> start_time = {}
            >>>
            >>> # TODO: Initialize `end_time`:
            >>> end_time = {}
            >>>
            >>> response = client.create_span(name, span_id, display_name, start_time, end_time)

        Args:
            name (str): The resource name of the span in the following format:

                ::

                     projects/[PROJECT_ID]/traces/[TRACE_ID]/spans/[SPAN_ID]

                [TRACE\_ID] is a unique identifier for a trace within a project; it is a
                32-character hexadecimal encoding of a 16-byte array.

                [SPAN\_ID] is a unique identifier for a span within a trace; it is a
                16-character hexadecimal encoding of an 8-byte array.
            span_id (str): The [SPAN\_ID] portion of the span's resource name.
            display_name (Union[dict, ~google.cloud.trace_v2.types.TruncatableString]): A description of the span's operation (up to 128 bytes). Stackdriver
                Trace displays the description in the {% dynamic print
                site\_values.console\_name %}. For example, the display name can be a
                qualified method name or a file name and a line number where the
                operation is called. A best practice is to use the same display name
                within an application and at the same call point. This makes it easier
                to correlate spans in different traces.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.TruncatableString`
            start_time (Union[dict, ~google.cloud.trace_v2.types.Timestamp]): The start time of the span. On the client side, this is the time kept by
                the local machine where the span execution starts. On the server side, this
                is the time when the server's application handler starts running.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Timestamp`
            end_time (Union[dict, ~google.cloud.trace_v2.types.Timestamp]): The end time of the span. On the client side, this is the time kept by
                the local machine where the span execution ends. On the server side, this
                is the time when the server application handler stops running.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Timestamp`
            parent_span_id (str): The [SPAN\_ID] of this span's parent span. If this is a root span, then
                this field must be empty.
            attributes (Union[dict, ~google.cloud.trace_v2.types.Attributes]): A set of attributes on the span. You can have up to 32 attributes per
                span.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Attributes`
            stack_trace (Union[dict, ~google.cloud.trace_v2.types.StackTrace]): Stack trace captured at the start of the span.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.StackTrace`
            time_events (Union[dict, ~google.cloud.trace_v2.types.TimeEvents]): A set of time events. You can have up to 32 annotations and 128 message
                events per span.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.TimeEvents`
            links (Union[dict, ~google.cloud.trace_v2.types.Links]): Links associated with the span. You can have up to 128 links per Span.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Links`
            status (Union[dict, ~google.cloud.trace_v2.types.Status]): An optional final status for this span.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Status`
            same_process_as_parent_span (Union[dict, ~google.cloud.trace_v2.types.BoolValue]): (Optional) Set this parameter to indicate whether this span is in
                the same process as its parent. If you do not set this parameter,
                Stackdriver Trace is unable to take advantage of this helpful
                information.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.BoolValue`
            child_span_count (Union[dict, ~google.cloud.trace_v2.types.Int32Value]): An optional number of child spans that were generated while this span
                was active. If set, allows implementation to detect missing child spans.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Int32Value`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.trace_v2.types.Span` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "create_span" not in self._inner_api_calls:
            self._inner_api_calls[
                "create_span"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.create_span,
                default_retry=self._method_configs["CreateSpan"].retry,
                default_timeout=self._method_configs["CreateSpan"].timeout,
                client_info=self._client_info,
            )

        request = trace_pb2.Span(
            name=name,
            span_id=span_id,
            display_name=display_name,
            start_time=start_time,
            end_time=end_time,
            parent_span_id=parent_span_id,
            attributes=attributes,
            stack_trace=stack_trace,
            time_events=time_events,
            links=links,
            status=status,
            same_process_as_parent_span=same_process_as_parent_span,
            child_span_count=child_span_count,
        )
        return self._inner_api_calls["create_span"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )
