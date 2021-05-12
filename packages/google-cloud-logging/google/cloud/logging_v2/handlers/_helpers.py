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
import re

try:
    import flask
except ImportError:  # pragma: NO COVER
    flask = None

from google.cloud.logging_v2.handlers.middleware.request import _get_django_request

_DJANGO_CONTENT_LENGTH = "CONTENT_LENGTH"
_DJANGO_TRACE_HEADER = "HTTP_X_CLOUD_TRACE_CONTEXT"
_DJANGO_USERAGENT_HEADER = "HTTP_USER_AGENT"
_DJANGO_REMOTE_ADDR_HEADER = "REMOTE_ADDR"
_DJANGO_REFERER_HEADER = "HTTP_REFERER"
_FLASK_TRACE_HEADER = "X_CLOUD_TRACE_CONTEXT"
_PROTOCOL_HEADER = "SERVER_PROTOCOL"


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

    return json.dumps(payload, ensure_ascii=False)


def get_request_data_from_flask():
    """Get http_request and trace data from flask request headers.

    Returns:
        Tuple[Optional[dict], Optional[str], Optional[str]]:
            Data related to the current http request, trace_id, and span_id for
            the request. All fields will be None if a django request isn't
            found.
    """
    if flask is None or not flask.request:
        return None, None, None

    # build http_request
    http_request = {
        "requestMethod": flask.request.method,
        "requestUrl": flask.request.url,
        "requestSize": flask.request.content_length,
        "userAgent": flask.request.user_agent.string,
        "remoteIp": flask.request.remote_addr,
        "referer": flask.request.referrer,
        "protocol": flask.request.environ.get(_PROTOCOL_HEADER),
    }

    # find trace id and span id
    header = flask.request.headers.get(_FLASK_TRACE_HEADER)
    trace_id, span_id = _parse_trace_span(header)

    return http_request, trace_id, span_id


def get_request_data_from_django():
    """Get http_request and trace data from django request headers.

    Returns:
        Tuple[Optional[dict], Optional[str], Optional[str]]:
            Data related to the current http request, trace_id, and span_id for
            the request. All fields will be None if a django request isn't
            found.
    """
    request = _get_django_request()

    if request is None:
        return None, None, None

    # convert content_length to int if it exists
    content_length = None
    try:
        content_length = int(request.META.get(_DJANGO_CONTENT_LENGTH))
    except (ValueError, TypeError):
        content_length = None

    # build http_request
    http_request = {
        "requestMethod": request.method,
        "requestUrl": request.build_absolute_uri(),
        "requestSize": content_length,
        "userAgent": request.META.get(_DJANGO_USERAGENT_HEADER),
        "remoteIp": request.META.get(_DJANGO_REMOTE_ADDR_HEADER),
        "referer": request.META.get(_DJANGO_REFERER_HEADER),
        "protocol": request.META.get(_PROTOCOL_HEADER),
    }

    # find trace id and span id
    header = request.META.get(_DJANGO_TRACE_HEADER)
    trace_id, span_id = _parse_trace_span(header)

    return http_request, trace_id, span_id


def _parse_trace_span(header):
    """Given an X_CLOUD_TRACE header, extract the trace and span ids.

    Args:
        header (str): the string extracted from the X_CLOUD_TRACE header
    Returns:
        Tuple[Optional[dict], Optional[str]]:
            The trace_id and span_id extracted from the header
            Each field will be None if not found.
    """
    trace_id = None
    span_id = None
    if header:
        try:
            split_header = header.split("/", 1)
            trace_id = split_header[0]
            header_suffix = split_header[1]
            # the span is the set of alphanumeric characters after the /
            span_id = re.findall(r"^\w+", header_suffix)[0]
        except IndexError:
            pass
    return trace_id, span_id


def get_request_data():
    """Helper to get http_request and trace data from supported web
    frameworks (currently supported: Flask and Django).

    Returns:
        Tuple[Optional[dict], Optional[str], Optional[str]]:
            Data related to the current http request, trace_id, and span_id for
            the request. All fields will be None if a django request isn't
            found.
    """
    checkers = (
        get_request_data_from_django,
        get_request_data_from_flask,
    )

    for checker in checkers:
        http_request, trace_id, span_id = checker()
        if http_request is not None:
            return http_request, trace_id, span_id

    return None, None, None
