# Copyright 2016 Google LLC
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

"""Log entries within the Google Stackdriver Logging API."""

import json
import re

from google.protobuf import any_pb2
from google.protobuf.json_format import Parse

from google.cloud.logging.resource import Resource
from google.cloud._helpers import _name_from_project_path
from google.cloud._helpers import _rfc3339_nanos_to_datetime


_LOGGER_TEMPLATE = re.compile(r"""
    projects/            # static prefix
    (?P<project>[^/]+)   # initial letter, wordchars + hyphen
    /logs/               # static midfix
    (?P<name>[^/]+)      # initial letter, wordchars + allowed punc
""", re.VERBOSE)


def logger_name_from_path(path):
    """Validate a logger URI path and get the logger name.

    :type path: str
    :param path: URI path for a logger API request.

    :rtype: str
    :returns: Logger name parsed from ``path``.
    :raises: :class:`ValueError` if the ``path`` is ill-formed or if
             the project from the ``path`` does not agree with the
             ``project`` passed in.
    """
    return _name_from_project_path(path, None, _LOGGER_TEMPLATE)


class _BaseEntry(object):
    """Base class for TextEntry, StructEntry, ProtobufEntry.

    :type payload: text or dict
    :param payload: The payload passed as ``textPayload``, ``jsonPayload``,
                    or ``protoPayload``.

    :type logger: :class:`google.cloud.logging.logger.Logger`
    :param logger: the logger used to write the entry.

    :type insert_id: text
    :param insert_id: (optional) the ID used to identify an entry uniquely.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: (optional) timestamp for the entry

    :type labels: dict
    :param labels: (optional) mapping of labels for the entry

    :type severity: str
    :param severity: (optional) severity of event being logged.

    :type http_request: dict
    :param http_request: (optional) info about HTTP request associated with
                         the entry.

    :type resource: :class:`~google.cloud.logging.resource.Resource`
    :param resource: (Optional) Monitored resource of the entry
    """
    def __init__(self, payload, logger, insert_id=None, timestamp=None,
                 labels=None, severity=None, http_request=None, resource=None):
        self.payload = payload
        self.logger = logger
        self.insert_id = insert_id
        self.timestamp = timestamp
        self.labels = labels
        self.severity = severity
        self.http_request = http_request
        self.resource = resource

    @classmethod
    def from_api_repr(cls, resource, client, loggers=None):
        """Factory:  construct an entry given its API representation

        :type resource: dict
        :param resource: text entry resource representation returned from
                         the API

        :type client: :class:`google.cloud.logging.client.Client`
        :param client: Client which holds credentials and project
                       configuration.

        :type loggers: dict
        :param loggers:
            (Optional) A mapping of logger fullnames -> loggers.  If not
            passed, the entry will have a newly-created logger.

        :rtype: :class:`google.cloud.logging.entries._BaseEntry`
        :returns: Text entry parsed from ``resource``.
        """
        if loggers is None:
            loggers = {}
        logger_fullname = resource['logName']
        logger = loggers.get(logger_fullname)
        if logger is None:
            logger_name = logger_name_from_path(logger_fullname)
            logger = loggers[logger_fullname] = client.logger(logger_name)
        payload = resource[cls._PAYLOAD_KEY]
        insert_id = resource.get('insertId')
        timestamp = resource.get('timestamp')
        if timestamp is not None:
            timestamp = _rfc3339_nanos_to_datetime(timestamp)
        labels = resource.get('labels')
        severity = resource.get('severity')
        http_request = resource.get('httpRequest')

        monitored_resource_dict = resource.get('resource')
        monitored_resource = None
        if monitored_resource_dict is not None:
            monitored_resource = Resource._from_dict(monitored_resource_dict)

        return cls(payload, logger, insert_id=insert_id, timestamp=timestamp,
                   labels=labels, severity=severity, http_request=http_request,
                   resource=monitored_resource)


class TextEntry(_BaseEntry):
    """Entry created with ``textPayload``.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
    """
    _PAYLOAD_KEY = 'textPayload'


class StructEntry(_BaseEntry):
    """Entry created with ``jsonPayload``.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
    """
    _PAYLOAD_KEY = 'jsonPayload'


class ProtobufEntry(_BaseEntry):
    """Entry created with ``protoPayload``.

    See
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry

    :type payload: str, dict or any_pb2.Any
    :param payload: The payload passed as ``textPayload``, ``jsonPayload``,
                    or ``protoPayload``. This also may be passed as a raw
                    :class:`.any_pb2.Any` if the ``protoPayload`` could
                    not be deserialized.

    :type logger: :class:`~google.cloud.logging.logger.Logger`
    :param logger: the logger used to write the entry.

    :type insert_id: str
    :param insert_id: (optional) the ID used to identify an entry uniquely.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: (optional) timestamp for the entry

    :type labels: dict
    :param labels: (optional) mapping of labels for the entry

    :type severity: str
    :param severity: (optional) severity of event being logged.

    :type http_request: dict
    :param http_request: (optional) info about HTTP request associated with
                         the entry

    :type resource: :class:`~google.cloud.logging.resource.Resource`
    :param resource: (Optional) Monitored resource of the entry
    """
    _PAYLOAD_KEY = 'protoPayload'

    def __init__(self, payload, logger, insert_id=None, timestamp=None,
                 labels=None, severity=None, http_request=None, resource=None):
        super(ProtobufEntry, self).__init__(
            payload, logger, insert_id=insert_id, timestamp=timestamp,
            labels=labels, severity=severity, http_request=http_request,
            resource=resource)
        if isinstance(self.payload, any_pb2.Any):
            self.payload_pb = self.payload
            self.payload = None
        else:
            self.payload_pb = None

    def parse_message(self, message):
        """Parse payload into a protobuf message.

        Mutates the passed-in ``message`` in place.

        :type message: Protobuf message
        :param message: the message to be logged
        """
        # NOTE: This assumes that ``payload`` is already a deserialized
        #       ``Any`` field and ``message`` has come from an imported
        #       ``pb2`` module with the relevant protobuf message type.
        Parse(json.dumps(self.payload), message)
