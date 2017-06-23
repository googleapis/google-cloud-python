# Copyright 2017 Google Inc.
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

"""TraceSpan for sending traces to the Stackdriver Trace API."""

from datetime import datetime
from google.cloud.gapic.trace.v1.enums import TraceSpan as Enum

import random


class TraceSpan(object):
    """A span is an individual timed event which forms a node of the trace
    tree. Each span has its name, span id and parent id. The parent id
    indicates the causal relationships between the individual spans in a
    single distributed trace. Span that does not have a parent id is called
    root span. All spans associated with a specific trace also share a common
    trace id. Spans do not need to be continuous, there can be gaps between
    two spans.

    See
    https://cloud.google.com/trace/docs/reference/v1/rpc/google.devtools.
    cloudtrace.v1#google.devtools.cloudtrace.v1.TraceSpan

    :type name: str
    :param name: The name of the span.

    :type kind: :class:`~google.cloud.trace.span.SpanKind`
    :param kind: Distinguishes between spans generated in a particular context.
                 For example, two spans with the same name may be
                 distinguished using RPC_CLIENT and RPC_SERVER to identify
                 queueing latency associated with the span.

    :type parent_span_id: str
    :param parent_span_id: ID of the parent span. Optional.

    :type labels: dict
    :param labels: Collection of labels associated with the span.
                   Label keys must be less than 128 bytes.
                   Label values must be less than 16 kilobytes.

    :type start_time: str
    :param start_time: (Optional) Start of the time interval (inclusive)
                       during which the trace data was collected from the
                       application.

    :type end_time: str
    :param end_time: (Optional) End of the time interval (inclusive) during
                     which the trace data was collected from the application.

    :type span_id: str
    :param span_id: Identifier for the span, unique within a trace.
    """

    def __init__(
            self,
            name,
            kind=Enum.SpanKind.SPAN_KIND_UNSPECIFIED,
            parent_span_id=None,
            labels=None,
            start_time=None,
            end_time=None,
            span_id=None):
        self.name = name
        self.kind = kind
        self.parent_span_id = parent_span_id
        self.labels = labels
        self.start_time = start_time
        self.end_time = end_time

        if span_id is None:
            span_id = generate_span_id()

        self.span_id = span_id

        self.child_spans = []

    def span(self, name='child_span'):
        """Create a child span for the current span and append it to the child
        spans list.

        :type name: str
        :param name: (Optional) The name of the child span.

        :rtype: :class: `~google.cloud.trace.trace_span.TraceSpan`
        :returns: A child TraceSpan to be added to the current span.
        """
        child_span = TraceSpan(name, parent_span_id=self.span_id)
        self.child_spans.append(child_span)
        return child_span

    def set_start_time(self):
        """Set the start time for a span."""
        self.start_time = datetime.utcnow().isoformat() + 'Z'

    def set_end_time(self):
        """Set the end time for a span."""
        self.end_time = datetime.utcnow().isoformat() + 'Z'

    def __enter__(self):
        self.set_start_time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.set_end_time()


def generate_span_id():
    """Return the random generated span ID for a span.

    :rtype: int
    :returns: Identifier for the span. Must be a 64-bit integer other
                than 0 and unique within a trace. Converted to string.
    """
    span_id = str(random.getrandbits(64))
    return int(span_id)


def format_span_json(span):
    """Helper to format a TraceSpan in JSON format.

    :type span: :class:`~google.cloud.trace.trace_span.TraceSpan`
    :param span: A TraceSpan to be transferred to JSON format.

    :rtype: dict
    :returns: Formatted TraceSpan.
    """
    span_json = {
        'name': span.name,
        'kind': span.kind,
        'spanId': span.span_id,
        'startTime': span.start_time,
        'endTime': span.end_time,
    }

    if span.parent_span_id is not None:
        span_json['parentSpanId'] = span.parent_span_id

    if span.labels is not None:
        span_json['labels'] = span.labels

    return span_json
