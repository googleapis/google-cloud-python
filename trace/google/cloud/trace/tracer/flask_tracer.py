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

"""The FlaskTracer maintains the trace spans for a trace in flask application.
It has a stack of TraceSpan that are currently open allowing you to know the
current context at any moment.
"""

try:
    import flask
except ImportError:  # pragma: NO COVER
    flask = None

from google.cloud.trace.propagation.google_cloud_format import from_header
from google.cloud.trace.span_context import _TRACE_HEADER_KEY
from google.cloud.trace.tracer.context_tracer import ContextTracer


class FlaskTracer(ContextTracer):
    """The flask implementation of the ContextTracer Interface.

    :type client: :class:`~google.cloud.trace.client.Client`
    :param client: The client that owns this API object.

    :type span_context: :class:`~google.cloud.trace.span_context.SpanContext`
    :param span_context: The current span context.
    """
    def __init__(self, client, span_context=None):
        if span_context is None:
            header = get_flask_header()
            span_context = from_header(header)

        super(FlaskTracer, self).__init__(
            client=client,
            span_context=span_context)


def get_flask_header():
    """Get trace context header from flask request headers.

    :rtype: str
    :returns: Trace context header in HTTP request headers.
    """
    if flask is None or not flask.request:
        return None

    header = flask.request.headers.get(_TRACE_HEADER_KEY)

    return header
