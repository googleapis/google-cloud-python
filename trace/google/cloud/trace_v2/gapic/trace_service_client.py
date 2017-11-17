# Copyright 2017, Google LLC All rights reserved.
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
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/devtools/cloudtrace/v2/tracing.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.devtools.cloudtrace.v2 TraceService API."""

import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.path_template

from google.cloud.trace_v2.gapic import enums
from google.cloud.trace_v2.gapic import trace_service_client_config
from google.cloud.trace_v2.proto import trace_pb2
from google.cloud.trace_v2.proto import tracing_pb2
from google.protobuf import timestamp_pb2
from google.protobuf import wrappers_pb2
from google.rpc import status_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-trace', ).version


class TraceServiceClient(object):
    """
    This file describes an API for collecting and viewing traces and spans
    within a trace.  A Trace is a collection of spans corresponding to a single
    operation or set of operations for an application. A span is an individual
    timed event which forms a node of the trace tree. A single trace may
    contain span(s) from multiple services.
    """

    SERVICE_ADDRESS = 'cloudtrace.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/trace.append', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.devtools.cloudtrace.v2.TraceService')

    @classmethod
    def project_path(cls, project):
        """Returns a fully-qualified project resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}',
            project=project, )

    @classmethod
    def span_path(cls, project, trace, span):
        """Returns a fully-qualified span resource name string."""
        return google.api_core.path_template.expand(
            'projects/{project}/traces/{trace}/spans/{span}',
            project=project,
            trace=trace,
            span=span, )

    def __init__(self,
                 channel=None,
                 credentials=None,
                 client_config=trace_service_client_config.config,
                 client_info=None):
        """Constructor.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. If specified, then the ``credentials``
                argument is ignored.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            client_config (dict):
                A dictionary of call options for each method. If not specified
                the default configuration is used. Generally, you only need
                to set this if you're developing your own client library.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        if channel is not None and credentials is not None:
            raise ValueError(
                'channel and credentials arguments to {} are mutually '
                'exclusive.'.format(self.__class__.__name__))

        if channel is None:
            channel = google.api_core.grpc_helpers.create_channel(
                self.SERVICE_ADDRESS,
                credentials=credentials,
                scopes=self._DEFAULT_SCOPES)

        self.trace_service_stub = (tracing_pb2.TraceServiceStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._batch_write_spans = google.api_core.gapic_v1.method.wrap_method(
            self.trace_service_stub.BatchWriteSpans,
            default_retry=method_configs['BatchWriteSpans'].retry,
            default_timeout=method_configs['BatchWriteSpans'].timeout,
            client_info=client_info)
        self._create_span = google.api_core.gapic_v1.method.wrap_method(
            self.trace_service_stub.CreateSpan,
            default_retry=method_configs['CreateSpan'].retry,
            default_timeout=method_configs['CreateSpan'].timeout,
            client_info=client_info)

    # Service calls
    def batch_write_spans(self,
                          name,
                          spans,
                          retry=google.api_core.gapic_v1.method.DEFAULT,
                          timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sends new spans to Stackdriver Trace or updates existing traces. If the
        name of a trace that you send matches that of an existing trace, new spans
        are added to the existing trace. Attempt to update existing spans results
        undefined behavior. If the name does not match, a new trace is created
        with given set of spans.

        Example:
            >>> from google.cloud import trace_v2
            >>>
            >>> client = trace_v2.TraceServiceClient()
            >>>
            >>> name = client.project_path('[PROJECT]')
            >>> spans = []
            >>>
            >>> client.batch_write_spans(name, spans)

        Args:
            name (str): Required. Name of the project where the spans belong. The format is
                ``projects/PROJECT_ID``.
            spans (list[Union[dict, ~google.cloud.trace_v2.types.Span]]): A collection of spans.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Span`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = tracing_pb2.BatchWriteSpansRequest(name=name, spans=spans)
        self._batch_write_spans(request, retry=retry, timeout=timeout)

    def create_span(self,
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
                    timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Creates a new Span.

        Example:
            >>> from google.cloud import trace_v2
            >>>
            >>> client = trace_v2.TraceServiceClient()
            >>>
            >>> name = client.span_path('[PROJECT]', '[TRACE]', '[SPAN]')
            >>> span_id = ''
            >>> display_name = {}
            >>> start_time = {}
            >>> end_time = {}
            >>>
            >>> response = client.create_span(name, span_id, display_name, start_time, end_time)

        Args:
            name (str): The resource name of the span in the following format:

                ::

                    projects/[PROJECT_ID]/traces/[TRACE_ID]/spans/[SPAN_ID]

                [TRACE_ID] is a unique identifier for a trace within a project.
                [SPAN_ID] is a unique identifier for a span within a trace,
                assigned when the span is created.
            span_id (str): The [SPAN_ID] portion of the span's resource name.
                The ID is a 16-character hexadecimal encoding of an 8-byte array.
            display_name (Union[dict, ~google.cloud.trace_v2.types.TruncatableString]): A description of the span's operation (up to 128 bytes).
                Stackdriver Trace displays the description in the
                {% dynamic print site_values.console_name %}.
                For example, the display name can be a qualified method name or a file name
                and a line number where the operation is called. A best practice is to use
                the same display name within an application and at the same call point.
                This makes it easier to correlate spans in different traces.
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
            parent_span_id (str): The [SPAN_ID] of this span's parent span. If this is a root span,
                then this field must be empty.
            attributes (Union[dict, ~google.cloud.trace_v2.types.Attributes]): A set of attributes on the span. There is a limit of 32 attributes per
                span.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Attributes`
            stack_trace (Union[dict, ~google.cloud.trace_v2.types.StackTrace]): Stack trace captured at the start of the span.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.StackTrace`
            time_events (Union[dict, ~google.cloud.trace_v2.types.TimeEvents]): The included time events. There can be up to 32 annotations and 128 message
                events per span.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.TimeEvents`
            links (Union[dict, ~google.cloud.trace_v2.types.Links]): A maximum of 128 links are allowed per Span.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Links`
            status (Union[dict, ~google.cloud.trace_v2.types.Status]): An optional final status for this span.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v2.types.Status`
            same_process_as_parent_span (Union[dict, ~google.cloud.trace_v2.types.BoolValue]): A highly recommended but not required flag that identifies when a trace
                crosses a process boundary. True when the parent_span belongs to the
                same process as the current span.
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

        Returns:
            A :class:`~google.cloud.trace_v2.types.Span` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
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
            child_span_count=child_span_count)
        return self._create_span(request, retry=retry, timeout=timeout)
