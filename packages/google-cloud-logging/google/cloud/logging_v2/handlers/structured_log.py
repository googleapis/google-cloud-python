# Copyright 2021 Google LLC All Rights Reserved.
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

"""Logging handler for printing formatted structured logs to standard output.
"""

import logging.handlers

from google.cloud.logging_v2.handlers.handlers import CloudLoggingFilter

GCP_FORMAT = (
    '{"message": "%(message)s", '
    '"severity": "%(levelname)s", '
    '"logging.googleapis.com/labels": { %(total_labels_str)s }, '
    '"logging.googleapis.com/trace": "%(trace)s", '
    '"logging.googleapis.com/spanId": "%(span_id)s", '
    '"logging.googleapis.com/sourceLocation": { "file": "%(file)s", "line": "%(line)d", "function": "%(function)s"}, '
    '"httpRequest": {"requestMethod": "%(request_method)s", "requestUrl": "%(request_url)s", "userAgent": "%(user_agent)s", "protocol": "%(protocol)s"} }'
)


class StructuredLogHandler(logging.StreamHandler):
    """Handler to format logs into the Cloud Logging structured log format,
    and write them to standard output
    """

    def __init__(self, *, labels=None, stream=None, project_id=None):
        """
        Args:
            labels (Optional[dict]): Additional labels to attach to logs.
            stream (Optional[IO]): Stream to be used by the handler.
            project (Optional[str]): Project Id associated with the logs.
        """
        super(StructuredLogHandler, self).__init__(stream=stream)
        self.project_id = project_id

        # add extra keys to log record
        log_filter = CloudLoggingFilter(project=project_id, default_labels=labels)
        self.addFilter(log_filter)

        # make logs appear in GCP structured logging format
        self.formatter = logging.Formatter(GCP_FORMAT)

    def format(self, record):
        """Format the message into structured log JSON.
        Args:
            record (logging.LogRecord): The log record.
        Returns:
            str: A JSON string formatted for GKE fluentd.
        """

        payload = self.formatter.format(record)
        return payload
