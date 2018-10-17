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

import collections
import json
import re

from google.protobuf.any_pb2 import Any
from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from google.cloud.logging.resource import Resource
from google.cloud._helpers import _name_from_project_path
from google.cloud._helpers import _rfc3339_nanos_to_datetime
from google.cloud._helpers import _datetime_to_rfc3339


_GLOBAL_RESOURCE = Resource(type='global', labels={})


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


def _int_or_none(value):
    """Helper: return an integer or ``None``."""
    if value is not None:
        value = int(value)
    return value


class _ApiReprMixin(object):
    """Mixin for the various log entry types."""
    received_timestamp = None

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

        :rtype: :class:`google.cloud.logging.entries.LogEntry`
        :returns: Log entry parsed from ``resource``.
        """
        if loggers is None:
            loggers = {}
        logger_fullname = resource['logName']
        logger = loggers.get(logger_fullname)
        if logger is None:
            logger_name = logger_name_from_path(logger_fullname)
            logger = loggers[logger_fullname] = client.logger(logger_name)
        if cls._PAYLOAD_KEY is not None:
            payload = resource[cls._PAYLOAD_KEY]
        else:
            payload = None
        insert_id = resource.get('insertId')
        timestamp = resource.get('timestamp')
        if timestamp is not None:
            timestamp = _rfc3339_nanos_to_datetime(timestamp)
        labels = resource.get('labels')
        severity = resource.get('severity')
        http_request = resource.get('httpRequest')
        trace = resource.get('trace')
        span_id = resource.get('spanId')
        trace_sampled = resource.get('traceSampled')
        source_location = resource.get('sourceLocation')
        if source_location is not None:
            line = source_location.pop('line', None)
            source_location['line'] = _int_or_none(line)
        operation = resource.get('operation')

        monitored_resource_dict = resource.get('resource')
        monitored_resource = None
        if monitored_resource_dict is not None:
            monitored_resource = Resource._from_dict(monitored_resource_dict)

        inst = cls(
            entry_type=cls._TYPE_NAME,
            log_name=logger_fullname,
            payload=payload,
            logger=logger,
            insert_id=insert_id,
            timestamp=timestamp,
            labels=labels,
            severity=severity,
            http_request=http_request,
            resource=monitored_resource,
            trace=trace,
            span_id=span_id,
            trace_sampled=trace_sampled,
            source_location=source_location,
            operation=operation
        )
        received = resource.get('receiveTimestamp')
        if received is not None:
            inst.received_timestamp = _rfc3339_nanos_to_datetime(received)
        return inst

    def to_api_repr(self):
        """API repr (JSON format) for entry.
        """
        if self.entry_type == 'text':
            info = {'textPayload': self.payload}
        elif self.entry_type == 'struct':
            info = {'jsonPayload': self.payload}
        elif self.entry_type == 'proto':
            # NOTE: If ``self`` contains an ``Any`` field with an
            #       unknown type, this will fail with a ``TypeError``.
            #       However, since ``self`` was provided by a user in
            #       ``Batch.log_proto``, the assumption is that any types
            #       needed for the protobuf->JSON conversion will be known
            #       from already imported ``pb2`` modules.
            info = {'protoPayload': MessageToDict(self.payload)}
        else:  # no payload
            info = {}
        if self.log_name is not None:
            info['logName'] = self.log_name
        if self.resource is not None:
            info['resource'] = self.resource._to_dict()
        if self.labels is not None:
            info['labels'] = self.labels
        if self.insert_id is not None:
            info['insertId'] = self.insert_id
        if self.severity is not None:
            info['severity'] = self.severity
        if self.http_request is not None:
            info['httpRequest'] = self.http_request
        if self.timestamp is not None:
            info['timestamp'] = _datetime_to_rfc3339(self.timestamp)
        if self.trace is not None:
            info['trace'] = self.trace
        if self.span_id is not None:
            info['spanId'] = self.span_id
        if self.trace_sampled is not None:
            info['traceSampled'] = self.trace_sampled
        if self.source_location is not None:
            source_location = self.source_location.copy()
            source_location['line'] = str(source_location.pop('line', 0))
            info['sourceLocation'] = source_location
        if self.operation is not None:
            info['operation'] = self.operation
        return info


_LOG_ENTRY_FIELDS = (  # (name, default)
    ('entry_type', None),
    ('log_name', None),
    ('payload', None),
    ('logger', None),
    ('labels', None),
    ('insert_id', None),
    ('severity', None),
    ('http_request', None),
    ('timestamp', None),
    ('resource', _GLOBAL_RESOURCE),
    ('trace', None),
    ('span_id', None),
    ('trace_sampled', None),
    ('source_location', None),
    ('operation', None),
)


_LogEntryTuple = collections.namedtuple(
        'LogEntry', (field for field, _ in _LOG_ENTRY_FIELDS))

_LogEntryTuple.__new__.__defaults__ = tuple(
    default for _, default in _LOG_ENTRY_FIELDS[1:])


_LOG_ENTRY_PARAM_DOCSTRING = """\

    :type logger: :class:`google.cloud.logging.logger.Logger`
    :param logger: the logger used to write the entry.

    :type log_name: str
    :param log_name: the name of the logger used to post the entry.

    :type labels: dict
    :param labels: (optional) mapping of labels for the entry

    :type insert_id: text
    :param insert_id: (optional) the ID used to identify an entry uniquely.

    :type severity: str
    :param severity: (optional) severity of event being logged.

    :type http_request: dict
    :param http_request: (optional) info about HTTP request associated with
                            the entry.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: (optional) timestamp for the entry

    :type resource: :class:`~google.cloud.logging.resource.Resource`
    :param resource: (Optional) Monitored resource of the entry

    :type trace: str
    :param trace: (optional) traceid to apply to the entry.

    :type span_id: str
    :param span_id: (optional) span_id within the trace for the log entry.
                    Specify the trace parameter if span_id is set.

    :type trace_sampled: bool
    :param trace_sampled: (optional) the sampling decision of the trace
                          associated with the log entry.

    :type source_location: dict
    :param source_location: (optional) location in source code from which
                            the entry was emitted.

    :type operation: dict
    :param operation: (optional) additional information about a potentially
                      long-running operation associated with the log entry.

    See:
    https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
"""


class LogEntry(_LogEntryTuple, _ApiReprMixin):
    __doc__ = """
    Log entry.

    :type entry_type: str
    :param entry_type: one of 'empty', 'text', 'struct', or 'proto'. Indicates
                       how the payload field is handled.

    :type payload: None, str | unicode, dict, protobuf message
    :param payload: payload for the message, based on :attr:`entry_type`
    """ + _LOG_ENTRY_PARAM_DOCSTRING


_EmptyEntryTuple = collections.namedtuple(
        'EmptyEntry', (field for field, _ in _LOG_ENTRY_FIELDS))
_EmptyEntryTuple.__new__.__defaults__ = (
    ('empty',) + tuple(default for _, default in _LOG_ENTRY_FIELDS[1:]))


class EmptyEntry(_EmptyEntryTuple, _ApiReprMixin):
    __doc__ = """
    Log entry without payload.

    """ + _LOG_ENTRY_PARAM_DOCSTRING
    _PAYLOAD_KEY = None
    _TYPE_NAME = 'empty'


_TextEntryTuple = collections.namedtuple(
        'TextEntry', (field for field, _ in _LOG_ENTRY_FIELDS))
_TextEntryTuple.__new__.__defaults__ = (
    ('text',) + tuple(default for _, default in _LOG_ENTRY_FIELDS[1:]))


class TextEntry(_TextEntryTuple, _ApiReprMixin):
    __doc__ = """
    Log entry with text payload.

    :type payload: str | unicode
    :param payload: payload for the log entry.
    """ + _LOG_ENTRY_PARAM_DOCSTRING
    _PAYLOAD_KEY = 'textPayload'
    _TYPE_NAME = 'text'


_StructEntryTuple = collections.namedtuple(
        'StructEntry', (field for field, _ in _LOG_ENTRY_FIELDS))
_StructEntryTuple.__new__.__defaults__ = (
    ('struct',) + tuple(default for _, default in _LOG_ENTRY_FIELDS[1:]))


class StructEntry(_StructEntryTuple, _ApiReprMixin):
    __doc__ = """
    Log entry with JSON payload.

    :type payload: dict
    :param payload: payload for the log entry.
    """ + _LOG_ENTRY_PARAM_DOCSTRING
    _PAYLOAD_KEY = 'jsonPayload'
    _TYPE_NAME = 'struct'


_ProtobufEntryTuple = collections.namedtuple(
        'ProtobufEntry', (field for field, _ in _LOG_ENTRY_FIELDS))
_ProtobufEntryTuple.__new__.__defaults__ = (
    ('proto',) + tuple(default for _, default in _LOG_ENTRY_FIELDS[1:]))


class ProtobufEntry(_ProtobufEntryTuple, _ApiReprMixin):
    __doc__ = """
    Log entry with protobuf message payload.

    :type payload: protobuf message
    :param payload: payload for the log entry.
    """ + _LOG_ENTRY_PARAM_DOCSTRING
    _PAYLOAD_KEY = 'protoPayload'
    _TYPE_NAME = 'proto'

    @property
    def payload_pb(self):
        if isinstance(self.payload, Any):
            return self.payload

    @property
    def payload_json(self):
        if not isinstance(self.payload, Any):
            return self.payload

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
