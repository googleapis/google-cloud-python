# Copyright 2017 Google LLC
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

"""Wrapper for interacting with the Stackdriver Trace API."""

from google.api_core.gapic_v1 import client_info
from google.api_core.gapic_v1 import method
from google.cloud._helpers import _datetime_to_pb_timestamp
from google.cloud.trace import __version__
from google.cloud.trace_v2.gapic import trace_service_client
from google.cloud.trace_v2.proto import trace_pb2
from google.protobuf.json_format import ParseDict
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


_CLIENT_INFO = client_info.ClientInfo(client_library_version=__version__)


class _TraceAPI(object):
    """
    Wrapper to help mapping trace-related APIs.

    See
    https://cloud.google.com/trace/docs/reference/v2/rpc/google.devtools.
    cloudtrace.v2

    Args:
        gapic (~google.cloud.trace_v2.gapic.trace_service_client.
            TraceServiceClient): Required. API object used to make RPCs.

        client (~google.cloud.trace_v2.client.Client): Required. The
            client that owns this API object.
    """

    def __init__(self, gapic_api, client):
        self._gapic_api = gapic_api
        self.client = client

    def batch_write_spans(
        self, name, spans, retry=method.DEFAULT, timeout=method.DEFAULT
    ):
        """
        Sends new spans to Stackdriver Trace or updates existing traces. If the
        name of a trace that you send matches that of an existing trace, new
        spans are added to the existing trace. Attempt to update existing spans
        results undefined behavior. If the name does not match, a new trace is
        created with given set of spans.

        Args:
            name (str): Required. Name of the project where the spans belong.
                The format is ``projects/PROJECT_ID``.
            spans (list[Union[dict, ~google.cloud.trace_v2.types.Span]]): A
                collection of spans. If a dict is provided, it must be of the
                same form as the protobuf message
                :class:`~google.cloud.trace_v2.types.Span`
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
        spans_pb_list = []

        for span_mapping in spans["spans"]:
            span_pb = _dict_mapping_to_pb(span_mapping, "Span")
            spans_pb_list.append(span_pb)

        self._gapic_api.batch_write_spans(
            name=name, spans=spans_pb_list, retry=retry, timeout=timeout
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
        retry=method.DEFAULT,
        timeout=method.DEFAULT,
    ):
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
            >>> response = client.create_span(name, span_id, display_name,
                                              start_time, end_time)

        Args:
            name (str): The resource name of the span in the following format:

                ::

                    projects/[PROJECT_ID]/traces/[TRACE_ID]/spans/[SPAN_ID]

                [TRACE_ID] is a unique identifier for a trace within a project.
                [SPAN_ID] is a unique identifier for a span within a trace,
                assigned when the span is created.
            span_id (str): The [SPAN_ID] portion of the span's resource name.
                The ID is a 16-character hexadecimal encoding of an 8-byte
                array.
            display_name (dict): A description of the span's operation
                (up to 128 bytes). Stackdriver Trace displays the description
                in the {% dynamic print site_values.console_name %}.
                For example, the display name can be a qualified method name
                or a file name and a line number where the operation is called.
                A best practice is to use the same display name within an
                application and at the same call point. This makes it easier to
                correlate spans in different traces.
                Contains two fields, value is the truncated name,
                truncatedByteCount is the number of bytes removed from the
                original string. If 0, then the string was not shortened.
            start_time (:class:`~datetime.datetime`):
                The start time of the span. On the client side, this is the
                time kept by the local machine where the span execution starts.
                On the server side, this is the time when the server's
                application handler starts running.
            end_time (:class:`~datetime.datetime`):
                The end time of the span. On the client side, this is the time
                kept by the local machine where the span execution ends. On the
                server side, this is the time when the server application
                handler stops running.
            parent_span_id (str): The [SPAN_ID] of this span's parent span.
                If this is a root span, then this field must be empty.
            attributes (dict): A set of attributes on the span. There is a
                limit of 32 attributes per span.
            stack_trace (dict):
                Stack trace captured at the start of the span.
                Contains two fields, stackFrames is a list of stack frames in
                this call stack, a maximum of 128 frames are allowed per
                StackFrame; stackTraceHashId is used to conserve network
                bandwidth for duplicate stack traces within a single trace.
            time_events (dict):
                The included time events. There can be up to 32 annotations
                and 128 message events per span.
            links (dict): A maximum of 128 links are allowed per Span.
            status (dict): An optional final status for this span.
            same_process_as_parent_span (bool): A highly recommended but not
                required flag that identifies when a trace crosses a process
                boundary. True when the parent_span belongs to the same process
                as the current span.
            child_span_count (int): An optional number of child spans that were
                generated while this span was active. If set, allows
                implementation to detect missing child spans.
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
        # Convert the dict type parameters to protobuf
        display_name = _dict_mapping_to_pb(display_name, "TruncatableString")
        start_time = _datetime_to_pb_timestamp(start_time)
        end_time = _datetime_to_pb_timestamp(end_time)

        if attributes is not None:
            attributes = _span_attrs_to_pb(attributes, "Attributes")

        if stack_trace is not None:
            stack_trace = _dict_mapping_to_pb(stack_trace, "StackTrace")

        if time_events is not None:
            time_events = _span_attrs_to_pb(time_events, "TimeEvents")

        if links is not None:
            links = _span_attrs_to_pb(links, "Links")

        if status is not None:
            status = _status_mapping_to_pb(status)

        if same_process_as_parent_span is not None:
            same_process_as_parent_span = _value_to_pb(
                same_process_as_parent_span, "BoolValue"
            )

        if child_span_count is not None:
            child_span_count = _value_to_pb(child_span_count, "Int32Value")

        return self._gapic_api.create_span(
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


def _dict_mapping_to_pb(mapping, proto_type):
    """
    Convert a dict to protobuf.

    Args:
        mapping (dict): A dict that needs to be converted to protobuf.
        proto_type (str): The type of the Protobuf.

    Returns:
        An instance of the specified protobuf.
    """
    converted_pb = getattr(trace_pb2, proto_type)()
    ParseDict(mapping, converted_pb)
    return converted_pb


def _span_attrs_to_pb(span_attr, proto_type):
    """
    Convert a span attribute dict to protobuf, including Links, Attributes,
    TimeEvents.

    Args:
        span_attr (dict): A dict that needs to be converted to protobuf.
        proto_type (str): The type of the Protobuf.

    Returns:
        An instance of the specified protobuf.
    """
    attr_pb = getattr(trace_pb2.Span, proto_type)()
    ParseDict(span_attr, attr_pb)
    return attr_pb


def _status_mapping_to_pb(status):
    """
    Convert a status dict to protobuf.

    Args:
        status (dict): A status that needs to be converted to protobuf.

    Returns:
        An instance of the specified protobuf.
    """
    status_pb = google_dot_rpc_dot_status__pb2.Status()
    ParseDict(status, status_pb)
    return status_pb


def _value_to_pb(value, proto_type):
    """
    Convert a value to protobuf. e.g. BoolValue, Int32Value.

    Args:
        value (dict): A dict that needs to be converted to protobuf.
        proto_type (str): The type of the Protobuf.

    Returns:
        An instance of the specified protobuf.
    """
    data_type_pb = getattr(google_dot_protobuf_dot_wrappers__pb2, proto_type)()
    ParseDict(value, data_type_pb)
    return data_type_pb


def make_trace_api(client):
    """
    Create an instance of the gapic Trace API.

    Args:
        client (:class:`~google.cloud.trace_v2.client.Client`): The client
            that holds configuration details.

    Returns:
        A :class:`~google.cloud.trace_v2._gapic._TraceAPI` instance with the
        proper configurations.
    """
    generated = trace_service_client.TraceServiceClient(
        credentials=client._credentials, client_info=_CLIENT_INFO
    )
    return _TraceAPI(generated, client)
