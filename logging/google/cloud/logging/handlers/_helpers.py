# Copyright 2016 Google LLC All Rights Reserved.
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

"""Helper functions for logging handlers."""

import math
import json

try:
    import flask
except ImportError:  # pragma: NO COVER
    flask = None

try:
    import webapp2
except (ImportError, SyntaxError):  # pragma: NO COVER
    # If you try to import webapp2 under python3, you'll get a syntax
    # error (since it hasn't been ported yet).  We just pretend it
    # doesn't exist.  This is unlikely to hit in real life but does
    # in the tests.
    webapp2 = None

from google.cloud.logging.handlers.middleware.request import (
    _get_django_request)

_DJANGO_TRACE_HEADER = 'HTTP_X_CLOUD_TRACE_CONTEXT'
_FLASK_TRACE_HEADER = 'X_CLOUD_TRACE_CONTEXT'
_WEBAPP2_TRACE_HEADER = 'X-CLOUD-TRACE-CONTEXT'


def format_stackdriver_json(record, message):
    """Helper to format a LogRecord in in Stackdriver fluentd format.

        :rtype: str
        :returns: JSON str to be written to the log file.
    """
    subsecond, second = math.modf(record.created)

    payload = {
        'message': message,
        'timestamp': {
            'seconds': int(second),
            'nanos': int(subsecond * 1e9),
        },
        'thread': record.thread,
        'severity': record.levelname,
    }

    return json.dumps(payload)


def get_trace_id_from_flask():
    """Get trace_id from flask request headers.

    :rtype: str
    :returns: TraceID in HTTP request headers.
    """
    if flask is None or not flask.request:
        return None

    header = flask.request.headers.get(_FLASK_TRACE_HEADER)

    if header is None:
        return None

    trace_id = header.split('/', 1)[0]

    return trace_id


def get_trace_id_from_webapp2():
    """Get trace_id from webapp2 request headers.

    :rtype: str
    :returns: TraceID in HTTP request headers.
    """
    if webapp2 is None:
        return None

    try:
        # get_request() succeeds if we're in the middle of a webapp2
        # request, or raises an assertion error otherwise:
        # "Request global variable is not set".
        req = webapp2.get_request()
    except AssertionError:
        return None

    header = req.headers.get(_WEBAPP2_TRACE_HEADER)

    if header is None:
        return None

    trace_id = header.split('/', 1)[0]

    return trace_id


def get_trace_id_from_django():
    """Get trace_id from django request headers.

    :rtype: str
    :returns: TraceID in HTTP request headers.
    """
    request = _get_django_request()

    if request is None:
        return None

    header = request.META.get(_DJANGO_TRACE_HEADER)
    if header is None:
        return None

    trace_id = header.split('/', 1)[0]

    return trace_id


def get_trace_id():
    """Helper to get trace_id from web application request header.

    :rtype: str
    :returns: TraceID in HTTP request headers.
    """
    checkers = (get_trace_id_from_django,
                get_trace_id_from_flask,
                get_trace_id_from_webapp2)

    for checker in checkers:
        trace_id = checker()
        if trace_id is not None:
            return trace_id

    return None
