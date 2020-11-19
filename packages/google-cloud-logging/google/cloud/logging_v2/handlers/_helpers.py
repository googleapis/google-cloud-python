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

from google.cloud.logging_v2.handlers.middleware.request import _get_django_request

_DJANGO_TRACE_HEADER = "HTTP_X_CLOUD_TRACE_CONTEXT"
_FLASK_TRACE_HEADER = "X_CLOUD_TRACE_CONTEXT"


def format_stackdriver_json(record, message):
    """Helper to format a LogRecord in in Stackdriver fluentd format.

    Returns:
        str: JSON str to be written to the log file.
    """
    subsecond, second = math.modf(record.created)

    payload = {
        "message": message,
        "timestamp": {"seconds": int(second), "nanos": int(subsecond * 1e9)},
        "thread": record.thread,
        "severity": record.levelname,
    }

    return json.dumps(payload)


def get_trace_id_from_flask():
    """Get trace_id from flask request headers.

    Returns:
        str: TraceID in HTTP request headers.
    """
    if flask is None or not flask.request:
        return None

    header = flask.request.headers.get(_FLASK_TRACE_HEADER)

    if header is None:
        return None

    trace_id = header.split("/", 1)[0]

    return trace_id


def get_trace_id_from_django():
    """Get trace_id from django request headers.

    Returns:
        str: TraceID in HTTP request headers.
    """
    request = _get_django_request()

    if request is None:
        return None

    header = request.META.get(_DJANGO_TRACE_HEADER)
    if header is None:
        return None

    trace_id = header.split("/", 1)[0]

    return trace_id


def get_trace_id():
    """Helper to get trace_id from web application request header.

    Returns:
        str: TraceID in HTTP request headers.
    """
    checkers = (
        get_trace_id_from_django,
        get_trace_id_from_flask,
    )

    for checker in checkers:
        trace_id = checker()
        if trace_id is not None:
            return trace_id

    return None
