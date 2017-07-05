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

from google.cloud.trace.trace import Trace
from google.cloud.trace.trace_span import TraceSpan


class ContextTracer(object):
    """The interface for tracing a request context.

    :type client: :class:`~google.cloud.trace.client.Client`
    :param client: The client that owns this API object.
    
    :rtype: :class:`~google.cloud.trace.trace_context.TraceContext`
    :returns: A TraceContext object.
    """
    _span_stack = []

    def __init__(self, client, trace_context):
        self.client = client
        self.trace_context = trace_context
        self.trace_id = trace_context.trace_id
        self.trace = self.trace()

    def trace(self):
        """Create a trace using the context information.

        :rtype: :class:`~google.cloud.trace.trace.Trace`
        :returns: The Trace object.
        """
        return Trace(client=self.client, trace_id=self.trace_id)

    def start_trace(self):
        """Start a trace."""
        self.trace.start()

    def end_trace(self):
        """End a trace."""
        self.trace.finish()

    def span(self, name='span'):
        """Create a new span with the trace using the context information.
        
        :type name: str
        :param name: The name of the span.
        
        :rtype: :class:`~google.cloud.trace.trace_span.TraceSpan`
        :returns: The TraceSpan object.
        """
        parent_span_id = self.trace_context.span_id
        span = TraceSpan(name, parent_span_id=parent_span_id)
        self.trace.spans.append(span)
        self._span_stack.append(span)
        self.trace_context.span_id = span.span_id
        return span

    def start_span(self, name='span'):
        """Start a span."""
        span = self.span(name=name)
        span.start()

    def end_span(self):
        """End a span. Remove the span from the span stack, and update the
        span_id in TraceContext as the current span_id which is the peek
        element in the span stack.
        """
        try:
            cur_span = self._span_stack.pop()
        except IndexError:
            raise

        cur_span.finish()

        if not self._span_stack:
            self.trace_context.span_id = None
        else:
            self.trace_context.span_id = self._span_stack[-1]
