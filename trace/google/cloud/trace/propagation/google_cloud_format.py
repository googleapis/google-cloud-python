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

"""This file is for converting the trace header in google cloud format and
generate a SpanContext, or converting a SpanContext to a google cloud format
header. Later we will add implementation for supporting other format like
binary format and zipkin, opencensus format.
"""

import logging
import re

from google.cloud.trace.span_context import SpanContext

_TRACE_CONTEXT_HEADER_FORMAT = '([0-9a-f]{32})(\/(\d+))?(;o=(\d+))?'
_TRACE_ID_DELIMETER = '/'
_SPAN_ID_DELIMETER = ';'


def from_header(header):
    """Generate a SpanContext object using the trace context header.
    The value of enabled parsed from header is int. Need to convert to bool.

    :type header: str
    :param header: Trace context header which was extracted from the HTTP
                   request headers.

    :rtype: :class:`~google.cloud.trace.span_context.SpanContext`
    :returns: SpanContext generated from the trace context header.
    """
    pattern = re.compile(_TRACE_CONTEXT_HEADER_FORMAT)

    try:
        match = re.search(pattern, header)
    except TypeError:
        logging.warning(
            'Header should be str, got {}. Cannot parse the header, '
            'generate a new context instead.'.format(
                header.__class__.__name__))
        return SpanContext()

    if match:
        trace_id = match.group(1)
        span_id = match.group(3)
        enabled = match.group(5)

        if enabled is None:
            enabled = True

        trace_context = SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            enabled=bool(enabled),
            from_header=True)
        return trace_context
    else:
        logging.warning(
            'Cannot parse the header {}, generate a new context instead.'
            .format(header))
        return SpanContext()


def to_header(span_context):
    """Convert a SpanContext object to header string.

    :type span_context:
        :class:`~google.cloud.trace.span_context.SpanContext`
    :param span_context: SpanContext object.

    :rtype: str
    :returns: A trace context header string in google cloud format.
    """
    trace_id = span_context.trace_id
    span_id = span_context.span_id
    enabled = span_context.enabled

    header = '{}/{};o={}'.format(
        trace_id,
        span_id,
        enabled)
    return header
