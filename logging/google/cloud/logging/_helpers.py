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

"""Common logging helpers."""

import logging

import requests

from google.cloud.logging.entries import LogEntry
from google.cloud.logging.entries import ProtobufEntry
from google.cloud.logging.entries import StructEntry
from google.cloud.logging.entries import TextEntry

try:
    from google.cloud.logging_v2.gapic.enums import LogSeverity
except ImportError:  # pragma: NO COVER

    class LogSeverity(object):
        """Map severities for non-GAPIC usage."""

        DEFAULT = 0
        DEBUG = 100
        INFO = 200
        NOTICE = 300
        WARNING = 400
        ERROR = 500
        CRITICAL = 600
        ALERT = 700
        EMERGENCY = 800


_NORMALIZED_SEVERITIES = {
    logging.CRITICAL: LogSeverity.CRITICAL,
    logging.ERROR: LogSeverity.ERROR,
    logging.WARNING: LogSeverity.WARNING,
    logging.INFO: LogSeverity.INFO,
    logging.DEBUG: LogSeverity.DEBUG,
    logging.NOTSET: LogSeverity.DEFAULT,
}

METADATA_URL = "http://metadata.google.internal./computeMetadata/v1/"
METADATA_HEADERS = {"Metadata-Flavor": "Google"}


def entry_from_resource(resource, client, loggers):
    """Detect correct entry type from resource and instantiate.

    :type resource: dict
    :param resource: One entry resource from API response.

    :type client: :class:`~google.cloud.logging.client.Client`
    :param client: Client that owns the log entry.

    :type loggers: dict
    :param loggers:
        A mapping of logger fullnames -> loggers.  If the logger
        that owns the entry is not in ``loggers``, the entry
        will have a newly-created logger.

    :rtype: :class:`~google.cloud.logging.entries._BaseEntry`
    :returns: The entry instance, constructed via the resource
    """
    if "textPayload" in resource:
        return TextEntry.from_api_repr(resource, client, loggers)

    if "jsonPayload" in resource:
        return StructEntry.from_api_repr(resource, client, loggers)

    if "protoPayload" in resource:
        return ProtobufEntry.from_api_repr(resource, client, loggers)

    return LogEntry.from_api_repr(resource, client, loggers)


def retrieve_metadata_server(metadata_key):
    """Retrieve the metadata key in the metadata server.

    See: https://cloud.google.com/compute/docs/storing-retrieving-metadata

    :type metadata_key: str
    :param metadata_key: Key of the metadata which will form the url. You can
                         also supply query parameters after the metadata key.
                         e.g. "tags?alt=json"

    :rtype: str
    :returns: The value of the metadata key returned by the metadata server.
    """
    url = METADATA_URL + metadata_key

    try:
        response = requests.get(url, headers=METADATA_HEADERS)

        if response.status_code == requests.codes.ok:
            return response.text

    except requests.exceptions.RequestException:
        # Ignore the exception, connection failed means the attribute does not
        # exist in the metadata server.
        pass

    return None


def _normalize_severity(stdlib_level):
    """Normalize a Python stdlib severity to LogSeverity enum.

    :type stdlib_level: int
    :param stdlib_level: 'levelno' from a :class:`logging.LogRecord`

    :rtype: int
    :returns: Corresponding Stackdriver severity.
    """
    return _NORMALIZED_SEVERITIES.get(stdlib_level, stdlib_level)
