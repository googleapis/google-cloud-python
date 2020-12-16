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
from google.logging.type.http_request_pb2 import HttpRequest

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

    return json.dumps(payload)


def get_request_data_from_flask():
    """Get http_request and trace data from flask request headers.

    Returns:
        Tuple[Optional[google.logging.type.http_request_pb2.HttpRequest], Optional[str]]:
            Data related to the current http request and the trace_id for the
            request. Both fields will be None if a flask request isn't found.
    """
    if flask is None or not flask.request:
        return None, None

    # build http_request
    http_request = HttpRequest(
        request_method=flask.request.method,
        request_url=flask.request.url,
        request_size=flask.request.content_length,
        user_agent=flask.request.user_agent.string,
        remote_ip=flask.request.remote_addr,
        referer=flask.request.referrer,
        protocol=flask.request.environ.get(_PROTOCOL_HEADER),
    )

    # find trace id
    trace_id = None
    header = flask.request.headers.get(_FLASK_TRACE_HEADER)
    if header:
        trace_id = header.split("/", 1)[0]

    return http_request, trace_id


def get_request_data_from_django():
    """Get http_request and trace data from django request headers.

    Returns:
        Tuple[Optional[google.logging.type.http_request_pb2.HttpRequest], Optional[str]]:
            Data related to the current http request and the trace_id for the
            request. Both fields will be None if a django request isn't found.
    """
    request = _get_django_request()

    if request is None:
        return None, None
    # build http_request
    http_request = HttpRequest(
        request_method=request.method,
        request_url=request.build_absolute_uri(),
        request_size=len(request.body),
        user_agent=request.META.get(_DJANGO_USERAGENT_HEADER),
        remote_ip=request.META.get(_DJANGO_REMOTE_ADDR_HEADER),
        referer=request.META.get(_DJANGO_REFERER_HEADER),
        protocol=request.META.get(_PROTOCOL_HEADER),
    )

    # find trace id
    trace_id = None
    header = request.META.get(_DJANGO_TRACE_HEADER)
    if header:
        trace_id = header.split("/", 1)[0]

    return http_request, trace_id


def get_request_data():
    """Helper to get http_request and trace data from supported web
    frameworks (currently supported: Flask and Django).

    Returns:
        Tuple[Optional[google.logging.type.http_request_pb2.HttpRequest], Optional[str]]:
            Data related to the current http request and the trace_id for the
            request. Both fields will be None if a supported web request isn't found.
    """
    checkers = (
        get_request_data_from_django,
        get_request_data_from_flask,
    )

    for checker in checkers:
        http_request, trace_id = checker()
        if http_request is not None:
            return http_request, trace_id

    return None, None
