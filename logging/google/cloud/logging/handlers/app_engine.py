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

"""Logging handler for App Engine Flexible

Logs to the well-known file that the fluentd sidecar container on App Engine
Flexible is configured to read from and send to Stackdriver Logging.

See the fluentd configuration here:

https://github.com/GoogleCloudPlatform/appengine-sidecars-docker/tree/master/fluentd_logger
"""

# This file is largely copied from:
#  https://github.com/GoogleCloudPlatform/python-compat-runtime/blob/master
# /appengine-vmruntime/vmruntime/cloud_logging.py

import logging.handlers
import os

from google.cloud.logging.handlers._helpers import format_stackdriver_json

_LOG_PATH_TEMPLATE = '/var/log/app_engine/app.{pid}.json'
_MAX_LOG_BYTES = 128 * 1024 * 1024
_LOG_FILE_COUNT = 3


class AppEngineHandler(logging.handlers.RotatingFileHandler):
    """A handler that writes to the App Engine fluentd Stackdriver log file.

    Writes to the file that the fluentd agent on App Engine Flexible is
    configured to discover logs and send them to  Stackdriver Logging.
    Log entries are wrapped in JSON and with appropriate metadata. The
    process of converting the user's formatted logs into a JSON payload for
    Stackdriver Logging consumption is implemented as part of the handler
    itself, and not as a formatting step, so as not to interfere with
    user-defined logging formats.
    """

    def __init__(self):
        """Construct the handler

        Large log entries will get mangled if multiple workers write to the
        same file simultaneously, so we'll use the worker's PID to pick a log
        filename.
        """
        self.filename = _LOG_PATH_TEMPLATE.format(pid=os.getpid())
        super(AppEngineHandler, self).__init__(self.filename,
                                               maxBytes=_MAX_LOG_BYTES,
                                               backupCount=_LOG_FILE_COUNT)

    def format(self, record):
        """Format the specified record into the expected JSON structure.

        :type record: :class:`~logging.LogRecord`
        :param record: the log record

        :rtype: str
        :returns: JSON str to be written to the log file
        """
        message = super(AppEngineHandler, self).format(record)
        return format_stackdriver_json(record, message)
