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
import collections
import json
import logging.handlers

from google.cloud.logging_v2.handlers.handlers import CloudLoggingFilter
from google.cloud.logging_v2.handlers.handlers import _format_and_parse_message

GCP_FORMAT = (
    "{%(_payload_str)s"
    '"severity": "%(levelname)s", '
    '"logging.googleapis.com/labels": %(_labels_str)s, '
    '"logging.googleapis.com/trace": "%(_trace_str)s", '
    '"logging.googleapis.com/spanId": "%(_span_id_str)s", '
    '"logging.googleapis.com/trace_sampled": %(_trace_sampled_str)s, '
    '"logging.googleapis.com/sourceLocation": %(_source_location_str)s, '
    '"httpRequest": %(_http_request_str)s '
    "}"
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
        self._gcp_formatter = logging.Formatter(GCP_FORMAT)

    def format(self, record):
        """Format the message into structured log JSON.
        Args:
            record (logging.LogRecord): The log record.
        Returns:
            str: A JSON string formatted for GCP structured logging.
        """
        payload = None
        message = _format_and_parse_message(record, super(StructuredLogHandler, self))

        if isinstance(message, collections.abc.Mapping):
            # if input is a dictionary, encode it as a json string
            encoded_msg = json.dumps(message, ensure_ascii=False)
            # strip out open and close parentheses
            payload = encoded_msg.lstrip("{").rstrip("}") + ","
        elif message:
            # properly break any formatting in string to make it json safe
            encoded_message = json.dumps(message, ensure_ascii=False)
            payload = '"message": {},'.format(encoded_message)

        record._payload_str = payload or ""
        # remove exception info to avoid duplicating it
        # https://github.com/googleapis/python-logging/issues/382
        record.exc_info = None
        record.exc_text = None
        # convert to GCP structred logging format
        gcp_payload = self._gcp_formatter.format(record)
        return gcp_payload
