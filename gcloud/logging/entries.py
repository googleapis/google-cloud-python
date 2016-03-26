# Copyright 2016 Google Inc. All rights reserved.
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

"""Log entries within the Google Cloud Logging API."""

import json

from google.protobuf.json_format import Parse

from gcloud._helpers import _rfc3339_nanos_to_datetime
from gcloud.logging._helpers import logger_name_from_path


class _BaseEntry(object):
    """Base class for TextEntry, StructEntry.

    :type payload: text or dict
    :param payload: The payload passed as ``textPayload``, ``jsonPayload``,
                    or ``protoPayload``.

    :type logger: :class:`gcloud.logging.logger.Logger`
    :param logger: the logger used to write the entry.

    :type insert_id: text, or :class:`NoneType`
    :param insert_id: (optional) the ID used to identify an entry uniquely.

    :type timestamp: :class:`datetime.datetime`, or :class:`NoneType`
    :param timestamp: (optional) timestamp for the entry
    """
    def __init__(self, payload, logger, insert_id=None, timestamp=None):
        self.payload = payload
        self.logger = logger
        self.insert_id = insert_id
        self.timestamp = timestamp

    @classmethod
    def from_api_repr(cls, resource, client, loggers=None):
        """Factory:  construct an entry given its API representation

        :type resource: dict
        :param resource: text entry resource representation returned from
                         the API

        :type client: :class:`gcloud.logging.client.Client`
        :param client: Client which holds credentials and project
                       configuration.

        :type loggers: dict or None
        :param loggers: A mapping of logger fullnames -> loggers.  If not
                        passed, the entry will have a newly-created logger.

        :rtype: :class:`gcloud.logging.entries.TextEntry`
        :returns: Text entry parsed from ``resource``.
        """
        if loggers is None:
            loggers = {}
        logger_fullname = resource['logName']
        logger = loggers.get(logger_fullname)
        if logger is None:
            logger_name = logger_name_from_path(
                logger_fullname, client.project)
            logger = loggers[logger_fullname] = client.logger(logger_name)
        payload = resource[cls._PAYLOAD_KEY]
        insert_id = resource.get('insertId')
        timestamp = resource.get('timestamp')
        if timestamp is not None:
            timestamp = _rfc3339_nanos_to_datetime(timestamp)
        return cls(payload, logger, insert_id, timestamp)


class TextEntry(_BaseEntry):
    """Entry created with ``textPayload``.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/LogEntry
    """
    _PAYLOAD_KEY = 'textPayload'


class StructEntry(_BaseEntry):
    """Entry created with ``jsonPayload``.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/LogEntry
    """
    _PAYLOAD_KEY = 'jsonPayload'


class ProtobufEntry(_BaseEntry):
    """Entry created with ``protoPayload``.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/LogEntry
    """
    _PAYLOAD_KEY = 'protoPayload'

    def parse_message(self, message):
        """Parse payload into a protobuf message.

        Mutates the passed-in ``message`` in place.

        :type message: Protobuf message
        :param message: the message to be logged
        """
        Parse(json.dumps(self.payload), message)
