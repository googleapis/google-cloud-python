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

"""TraceContext encapsulates the current context within the request's trace."""

from google.cloud.trace.trace import generate_trace_id

import re
import logging

_TRACE_CONTEXT_HEADER_FORMAT = '([0-9a-f]{32})(\/(\d+))?(;o=(\d+))?'


class TraceContext(object):
    """TraceContext includes 3 fields: traceId, spanId, and an enabled flag 
    which indicateswhether or not the request is being traced.
    
    :type trace_id: str
    :param trace_id: (Optional) Trace_id is a 32 digits uuid for the trace.
                     If not given, will generate one automatically.

    :type span_id: int
    :param span_id: (Optional) Identifier for the span, unique within a trace.

    :type enabled: bool
    :param enabled: (Optional) Indicates whether the request is traced or not.
    
    :type from_header: bool
    :param from_header: (Optional) Indicates whether the trace context is
                        generated from request header.
    """
    def __init__(
            self,
            trace_id=None,
            span_id=None,
            enabled=True,
            from_header=False):
        if trace_id is None:
            trace_id = generate_trace_id()

        self.trace_id = trace_id
        self.span_id = self.check_span_id(span_id)
        self.enabled = enabled
        self.from_header = from_header

    def check_span_id(self, span_id):
        """Check the type of span_id to ensure it is int. If it is not int,
        first try to convert it to int, if failed to convert, then log a
        warning message and set the span_id to None.

        :type span_id: int
        :param span_id: Identifier for the span, unique within a trace.

        :rtype: int
        :returns: Span_id for the current span.
        """
        if not isinstance(span_id, int):
            try:
                span_id = int(span_id)
            except ValueError:
                logging.warning(
                    'The type of span_id should be int, got {}.'.format(
                        span_id.__class__.__name__))
                span_id = None

        return span_id

    def convert_to_string(self):
        """Returns a string form of the TraceContext. This is the format of 
        the Trace Context Header and should be forwarded to downstream
        requests as the X-Cloud-Trace-Context header.

        :rtype: str
        :returns: String form of the TraceContext.
        """
        header = '{}/{};o={}'.format(
            self.trace_id,
            self.span_id,
            self.enabled)
        return header


def generate_context_from_header(header):
    """Parse a request header and generate a TraceContext object.

    :type header: 
    :param header: Request header from web application.

    :rtype: :class:`~google.cloud.trace.trace_context.TraceContext`
    :returns: A TraceContext object.
    """
    pattern = re.compile(_TRACE_CONTEXT_HEADER_FORMAT)
    match = re.search(pattern, header)

    if match:
        trace_id = match.group(1)
        span_id = match.group(3)
        enabled = match.group(5)

        if enabled is None:
            enabled = 1

        trace_context = TraceContext(
            trace_id=trace_id,
            span_id=span_id,
            enabled=enabled,
            from_header=True)
        return trace_context
    else:
        return TraceContext()
