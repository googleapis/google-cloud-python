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
# https://github.com/google/googleapis/blob/master/google/devtools/cloudtrace/v1/trace.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.devtools.cloudtrace.v1 TraceService API."""

import functools
import pkg_resources

import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.grpc_helpers
import google.api_core.page_iterator

from google.cloud.trace_v1.gapic import enums
from google.cloud.trace_v1.gapic import trace_service_client_config
from google.cloud.trace_v1.proto import trace_pb2
from google.protobuf import timestamp_pb2

_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution(
    'google-cloud-trace', ).version


class TraceServiceClient(object):
    """
    This file describes an API for collecting and viewing traces and spans
    within a trace.  A Trace is a collection of spans corresponding to a single
    operation or set of operations for an application. A span is an individual
    timed event which forms a node of the trace tree. Spans for a single trace
    may span multiple services.
    """

    SERVICE_ADDRESS = 'cloudtrace.googleapis.com:443'
    """The default address of the service."""

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/trace.append',
        'https://www.googleapis.com/auth/trace.readonly', )

    # The name of the interface for this client. This is the key used to find
    # method configuration in the client_config dictionary
    _INTERFACE_NAME = ('google.devtools.cloudtrace.v1.TraceService')

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

        self.trace_service_stub = (trace_pb2.TraceServiceStub(channel))

        if client_info is None:
            client_info = (
                google.api_core.gapic_v1.client_info.DEFAULT_CLIENT_INFO)

        client_info.gapic_version = _GAPIC_LIBRARY_VERSION

        interface_config = client_config['interfaces'][self._INTERFACE_NAME]
        method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            interface_config)

        self._patch_traces = google.api_core.gapic_v1.method.wrap_method(
            self.trace_service_stub.PatchTraces,
            default_retry=method_configs['PatchTraces'].retry,
            default_timeout=method_configs['PatchTraces'].timeout,
            client_info=client_info)
        self._get_trace = google.api_core.gapic_v1.method.wrap_method(
            self.trace_service_stub.GetTrace,
            default_retry=method_configs['GetTrace'].retry,
            default_timeout=method_configs['GetTrace'].timeout,
            client_info=client_info)
        self._list_traces = google.api_core.gapic_v1.method.wrap_method(
            self.trace_service_stub.ListTraces,
            default_retry=method_configs['ListTraces'].retry,
            default_timeout=method_configs['ListTraces'].timeout,
            client_info=client_info)

    # Service calls
    def patch_traces(self,
                     project_id,
                     traces,
                     retry=google.api_core.gapic_v1.method.DEFAULT,
                     timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Sends new traces to Stackdriver Trace or updates existing traces. If the ID
        of a trace that you send matches that of an existing trace, any fields
        in the existing trace and its spans are overwritten by the provided values,
        and any new fields provided are merged with the existing trace data. If the
        ID does not match, a new trace is created.

        Example:
            >>> from google.cloud import trace_v1
            >>>
            >>> client = trace_v1.TraceServiceClient()
            >>>
            >>> project_id = ''
            >>> traces = {}
            >>>
            >>> client.patch_traces(project_id, traces)

        Args:
            project_id (str): ID of the Cloud project where the trace data is stored.
            traces (Union[dict, ~google.cloud.trace_v1.types.Traces]): The body of the message.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v1.types.Traces`
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
        request = trace_pb2.PatchTracesRequest(
            project_id=project_id, traces=traces)
        self._patch_traces(request, retry=retry, timeout=timeout)

    def get_trace(self,
                  project_id,
                  trace_id,
                  retry=google.api_core.gapic_v1.method.DEFAULT,
                  timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Gets a single trace by its ID.

        Example:
            >>> from google.cloud import trace_v1
            >>>
            >>> client = trace_v1.TraceServiceClient()
            >>>
            >>> project_id = ''
            >>> trace_id = ''
            >>>
            >>> response = client.get_trace(project_id, trace_id)

        Args:
            project_id (str): ID of the Cloud project where the trace data is stored.
            trace_id (str): ID of the trace to return.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.cloud.trace_v1.types.Trace` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = trace_pb2.GetTraceRequest(
            project_id=project_id, trace_id=trace_id)
        return self._get_trace(request, retry=retry, timeout=timeout)

    def list_traces(self,
                    project_id,
                    view=None,
                    page_size=None,
                    start_time=None,
                    end_time=None,
                    filter_=None,
                    order_by=None,
                    retry=google.api_core.gapic_v1.method.DEFAULT,
                    timeout=google.api_core.gapic_v1.method.DEFAULT):
        """
        Returns of a list of traces that match the specified filter conditions.

        Example:
            >>> from google.cloud import trace_v1
            >>>
            >>> client = trace_v1.TraceServiceClient()
            >>>
            >>> project_id = ''
            >>>
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_traces(project_id):
            ...     # process element
            ...     pass
            >>>
            >>> # Or iterate over results one page at a time
            >>> for page in client.list_traces(project_id, options=CallOptions(page_token=INITIAL_PAGE)):
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            project_id (str): ID of the Cloud project where the trace data is stored.
            view (~google.cloud.trace_v1.types.ViewType): Type of data returned for traces in the list. Optional. Default is
                ``MINIMAL``.
            page_size (int): Maximum number of traces to return. If not specified or <= 0, the
                implementation selects a reasonable value.  The implementation may
                return fewer traces than the requested page size. Optional.
            start_time (Union[dict, ~google.cloud.trace_v1.types.Timestamp]): Start of the time interval (inclusive) during which the trace data was
                collected from the application.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v1.types.Timestamp`
            end_time (Union[dict, ~google.cloud.trace_v1.types.Timestamp]): End of the time interval (inclusive) during which the trace data was
                collected from the application.
                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.trace_v1.types.Timestamp`
            filter_ (str): An optional filter against labels for the request.

                By default, searches use prefix matching. To specify exact match, prepend
                a plus symbol (``+``) to the search term.
                Multiple terms are ANDed. Syntax:

                *   ``root:NAME_PREFIX`` or ``NAME_PREFIX``: Return traces where any root
                ::

                    span starts with `NAME_PREFIX`.
                *   ``+root:NAME`` or ``+NAME``: Return traces where any root span's name is
                ::

                    exactly `NAME`.
                *   ``span:NAME_PREFIX``: Return traces where any span starts with
                ::

                    `NAME_PREFIX`.
                *   ``+span:NAME``: Return traces where any span's name is exactly
                ::

                    `NAME`.
                *   ``latency:DURATION``: Return traces whose overall latency is
                ::

                    greater or equal to than `DURATION`. Accepted units are nanoseconds
                    (`ns`), milliseconds (`ms`), and seconds (`s`). Default is `ms`. For
                    example, `latency:24ms` returns traces whose overall latency
                    is greater than or equal to 24 milliseconds.
                *   ``label:LABEL_KEY``: Return all traces containing the specified
                ::

                    label key (exact match, case-sensitive) regardless of the key:value
                    pair's value (including empty values).
                *   ``LABEL_KEY:VALUE_PREFIX``: Return all traces containing the specified
                ::

                    label key (exact match, case-sensitive) whose value starts with
                    `VALUE_PREFIX`. Both a key and a value must be specified.
                *   ``+LABEL_KEY:VALUE``: Return all traces containing a key:value pair
                ::

                    exactly matching the specified text. Both a key and a value must be
                    specified.
                *   ``method:VALUE``: Equivalent to ``/http/method:VALUE``.
                *   ``url:VALUE``: Equivalent to ``/http/url:VALUE``.
            order_by (str): Field used to sort the returned traces. Optional.
                Can be one of the following:

                *   ``trace_id``
                *   ``name`` (``name`` field of root span in the trace)
                *   ``duration`` (difference between ``end_time`` and ``start_time`` fields of
                ::

                     the root span)
                *   ``start`` (``start_time`` field of the root span)

                Descending order can be specified by appending ``desc`` to the sort field
                (for example, ``name desc``).

                Only one sort field is permitted.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will not
                be retried.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.

        Returns:
            A :class:`~google.gax.PageIterator` instance. By default, this
            is an iterable of :class:`~google.cloud.trace_v1.types.Trace` instances.
            This object can also be configured to iterate over the pages
            of the response through the `options` parameter.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        request = trace_pb2.ListTracesRequest(
            project_id=project_id,
            view=view,
            page_size=page_size,
            start_time=start_time,
            end_time=end_time,
            filter=filter_,
            order_by=order_by)
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._list_traces, retry=retry, timeout=timeout),
            request=request,
            items_field='traces',
            request_token_field='page_token',
            response_token_field='next_page_token')
        return iterator
