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

"""Client for interacting with the Stackdriver Trace API."""

from google.cloud.trace._gapic import make_trace_api
from google.cloud.client import ClientWithProject


class Client(ClientWithProject):
    """
    Client to bundle configuration needed for API requests.

    Args:
        project (str): The project which the client acts on behalf of.
            If not passed, falls back to the default inferred from
            the environment.
        credentials (Optional[:class:`~google.auth.credentials.Credentials`]):
            The OAuth2 Credentials to use for this client. If not passed,
            falls back to the default inferred from the environment.
    """

    SCOPE = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/trace.append",
    )
    """The scopes required for authenticating as a Trace consumer."""

    _trace_api = None

    def __init__(self, project=None, credentials=None):
        super(Client, self).__init__(project=project, credentials=credentials)

    @property
    def trace_api(self):
        """
        Helper for trace-related API calls.

        See
        https://cloud.google.com/trace/docs/reference/v2/rpc/google.devtools.
        cloudtrace.v2
        """
        self._trace_api = make_trace_api(self)
        return self._trace_api

    def batch_write_spans(self, name, spans, retry=None, timeout=None):
        """
        Sends new spans to Stackdriver Trace or updates existing traces. If the
        name of a trace that you send matches that of an existing trace, new
        spans are added to the existing trace. Attempt to update existing spans
        results undefined behavior. If the name does not match, a new trace is
        created with given set of spans.

        Example:
            >>> from google.cloud import trace_v2
            >>>
            >>> client = trace_v2.Client()
            >>>
            >>> name = 'projects/[PROJECT_ID]'
            >>> spans = {'spans': [{'endTime': '2017-11-21T23:50:58.890768Z',
                                    'spanId': [SPAN_ID],
                                    'startTime': '2017-11-21T23:50:58.890763Z',
                                    'name': 'projects/[PROJECT_ID]/traces/
                                            [TRACE_ID]/spans/[SPAN_ID]',
                                    'displayName': {'value': 'sample span'}}]}
            >>>
            >>> client.batch_write_spans(name, spans)

        Args:
            name (str): Optional. Name of the project where the spans belong.
                The format is ``projects/PROJECT_ID``.
            spans (dict): A collection of spans.
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
        self.trace_api.batch_write_spans(
            name=name, spans=spans, retry=retry, timeout=timeout
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
        retry=None,
        timeout=None,
    ):
        """
        Creates a new Span.

        Example:
            >>> from google.cloud import trace_v2
            >>>
            >>> client = trace_v2.Client()
            >>>
            >>> name = 'projects/{project}/traces/{trace_id}/spans/{span_id}'.
                       format('[PROJECT]', '[TRACE_ID]', '[SPAN_ID]')
            >>> span_id = '[SPAN_ID]'
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
        return self.trace_api.create_span(
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
