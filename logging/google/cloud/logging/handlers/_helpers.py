# Copyright 2016 Google Inc. All Rights Reserved.
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
import os


def format_stackdriver_json(record, message):
    """Helper to format a LogRecord in in Stackdriver fluentd format.

        :rtype: str
        :returns: JSON str to be written to the log file.
    """
    subsecond, second = math.modf(record.created)

    # Assemble a dictionary with the log string as the message.
    payload = {
        'message': message,
        'timestamp': {
            'seconds': int(second),
            'nanos': int(subsecond * 1e9),
        },
        'thread': record.thread,
        'severity': record.levelname,
    }

    # Make a best effort to add the trace id.
    # First try to extract the trace_id from HTTP header, only support flask framework for now.
    trace_id = parse_flask_request_header()

    # If that didn't work, try to get the trace_id from the 'extras' of the record.
    if not trace_id:
        trace_id = getattr(record, 'trace_id', None)

    # If still cannot get the trace_id, try to get it from environment.
    if not trace_id:
        trace_id = os.getenv('HTTP_X_CLOUD_TRACE_CONTEXT', '').split('/')[0]

    # Add trace_id to payload if it was found.
    if trace_id:
        payload['traceId'] = trace_id

    return json.dumps(payload)


def parse_flask_request_header():
    """Parse flask request header to get trace_id.
    
        :rtype: str
        :return: trace_id get from flask header
    """
    # Import the web framework to parse HTTP header.
    try:
        import flask
    except ImportError:
        flask = None

    # Extract the trace_id
    if flask:
        try:
            trace_id = flask.request.headers['X-Cloud-Trace-Context'].split('/')[0]
        except KeyError:
            trace_id = None
    else:
        trace_id = None

    return trace_id