# Copyright 2014 Google Inc. All rights reserved.
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
"""Thread-local resource stack.

This module is not part of the public API surface of `gcloud`.
"""

import calendar
import datetime
import json
import os
import re
import socket
import sys
from threading import local as Local

from google.protobuf import timestamp_pb2
try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None
import six
from six.moves.http_client import HTTPConnection
from six.moves import configparser

from gcloud.environment_vars import PROJECT
from gcloud.environment_vars import CREDENTIALS


_NOW = datetime.datetime.utcnow  # To be replaced by tests.
_RFC3339_MICROS = '%Y-%m-%dT%H:%M:%S.%fZ'
_RFC3339_NO_FRACTION = '%Y-%m-%dT%H:%M:%S'
# datetime.strptime cannot handle nanosecond precision:  parse w/ regex
_RFC3339_NANOS = re.compile(r"""
    (?P<no_fraction>
        \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}  # YYYY-MM-DDTHH:MM:SS
    )
    \.                                       # decimal point
    (?P<nanos>\d{1,9})                       # nanoseconds, maybe truncated
    Z                                        # Zulu
""", re.VERBOSE)
DEFAULT_CONFIGURATION_PATH = '~/.config/gcloud/configurations/config_default'


class _LocalStack(Local):
    """Manage a thread-local LIFO stack of resources.

    Intended for use in :class:`gcloud.datastore.batch.Batch.__enter__`,
    :class:`gcloud.storage.batch.Batch.__enter__`, etc.
    """
    def __init__(self):
        super(_LocalStack, self).__init__()
        self._stack = []

    def __iter__(self):
        """Iterate the stack in LIFO order.
        """
        return iter(reversed(self._stack))

    def push(self, resource):
        """Push a resource onto our stack.
        """
        self._stack.append(resource)

    def pop(self):
        """Pop a resource from our stack.

        :rtype: object
        :returns: the top-most resource, after removing it.
        :raises IndexError: if the stack is empty.
        """
        return self._stack.pop()

    @property
    def top(self):
        """Get the top-most resource

        :rtype: object
        :returns: the top-most item, or None if the stack is empty.
        """
        if len(self._stack) > 0:
            return self._stack[-1]


class _UTC(datetime.tzinfo):
    """Basic UTC implementation.

    Implementing a small surface area to avoid depending on ``pytz``.
    """

    _dst = datetime.timedelta(0)
    _tzname = 'UTC'
    _utcoffset = _dst

    def dst(self, dt):  # pylint: disable=unused-argument
        """Daylight savings time offset."""
        return self._dst

    def fromutc(self, dt):
        """Convert a timestamp from (naive) UTC to this timezone."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=self)
        return super(_UTC, self).fromutc(dt)

    def tzname(self, dt):  # pylint: disable=unused-argument
        """Get the name of this timezone."""
        return self._tzname

    def utcoffset(self, dt):  # pylint: disable=unused-argument
        """UTC offset of this timezone."""
        return self._utcoffset

    def __repr__(self):
        return '<%s>' % (self._tzname,)

    def __str__(self):
        return self._tzname


def _ensure_tuple_or_list(arg_name, tuple_or_list):
    """Ensures an input is a tuple or list.

    This effectively reduces the iterable types allowed to a very short
    whitelist: list and tuple.

    :type arg_name: str
    :param arg_name: Name of argument to use in error message.

    :type tuple_or_list: sequence of str
    :param tuple_or_list: Sequence to be verified.

    :rtype: list of str
    :returns: The ``tuple_or_list`` passed in cast to a ``list``.
    :raises TypeError: if the ``tuple_or_list`` is not a tuple or list.
    """
    if not isinstance(tuple_or_list, (tuple, list)):
        raise TypeError('Expected %s to be a tuple or list. '
                        'Received %r' % (arg_name, tuple_or_list))
    return list(tuple_or_list)


def _app_engine_id():
    """Gets the App Engine application ID if it can be inferred.

    :rtype: str or ``NoneType``
    :returns: App Engine application ID if running in App Engine,
              else ``None``.
    """
    if app_identity is None:
        return None

    return app_identity.get_application_id()


def _file_project_id():
    """Gets the project id from the credentials file if one is available.

    :rtype: str or ``NoneType``
    :returns: Project-ID from JSON credentials file if value exists,
              else ``None``.
    """
    credentials_file_path = os.getenv(CREDENTIALS)
    if credentials_file_path:
        with open(credentials_file_path, 'rb') as credentials_file:
            credentials_json = credentials_file.read()
            credentials = json.loads(credentials_json.decode('utf-8'))
            return credentials.get('project_id')


def _default_service_project_id():
    """Retrieves the project ID from the gcloud command line tool.

    Files that cannot be opened with configparser are silently ignored; this is
    designed so that you can specify a list of potential configuration file
    locations.

    :rtype: str or ``NoneType``
    :returns: Project-ID from default configuration file else ``None``
    """
    search_paths = []
    # Workaround for GAE not supporting pwd which is used by expanduser.
    try:
        search_paths.append(os.path.expanduser(DEFAULT_CONFIGURATION_PATH))
    except ImportError:
        pass

    windows_config_path = os.path.join(os.getenv('APPDATA', ''),
                                       'gcloud', 'configurations',
                                       'config_default')
    search_paths.append(windows_config_path)
    config = configparser.RawConfigParser()
    config.read(search_paths)

    if config.has_section('core'):
        return config.get('core', 'project')


def _compute_engine_id():
    """Gets the Compute Engine project ID if it can be inferred.

    Uses 169.254.169.254 for the metadata server to avoid request
    latency from DNS lookup.

    See https://cloud.google.com/compute/docs/metadata#metadataserver
    for information about this IP address. (This IP is also used for
    Amazon EC2 instances, so the metadata flavor is crucial.)

    See https://github.com/google/oauth2client/issues/93 for context about
    DNS latency.

    :rtype: str or ``NoneType``
    :returns: Compute Engine project ID if the metadata service is available,
              else ``None``.
    """
    host = '169.254.169.254'
    uri_path = '/computeMetadata/v1/project/project-id'
    headers = {'Metadata-Flavor': 'Google'}
    connection = HTTPConnection(host, timeout=0.1)

    try:
        connection.request('GET', uri_path, headers=headers)
        response = connection.getresponse()
        if response.status == 200:
            return response.read()
    except socket.error:  # socket.timeout or socket.error(64, 'Host is down')
        pass
    finally:
        connection.close()


def _get_production_project():
    """Gets the production project if it can be inferred."""
    return os.getenv(PROJECT)


def _determine_default_project(project=None):
    """Determine default project ID explicitly or implicitly as fall-back.

    In implicit case, supports three environments. In order of precedence, the
    implicit environments are:

    * GCLOUD_PROJECT environment variable
    * GOOGLE_APPLICATION_CREDENTIALS JSON file
    * Get default service project from
      ``$ gcloud beta auth application-default login``
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type project: str
    :param project: Optional. The project name to use as default.

    :rtype: str or ``NoneType``
    :returns: Default project if it can be determined.
    """
    if project is None:
        project = _get_production_project()

    if project is None:
        project = _file_project_id()

    if project is None:
        project = _default_service_project_id()

    if project is None:
        project = _app_engine_id()

    if project is None:
        project = _compute_engine_id()

    return project


def _millis(when):
    """Convert a zone-aware datetime to integer milliseconds.

    :type when: :class:`datetime.datetime`
    :param when: the datetime to convert

    :rtype: int
    :returns: milliseconds since epoch for ``when``
    """
    micros = _microseconds_from_datetime(when)
    return micros // 1000


def _datetime_from_microseconds(value):
    """Convert timestamp to datetime, assuming UTC.

    :type value: float
    :param value: The timestamp to convert

    :rtype: :class:`datetime.datetime`
    :returns: The datetime object created from the value.
    """
    return _EPOCH + datetime.timedelta(microseconds=value)


def _microseconds_from_datetime(value):
    """Convert non-none datetime to microseconds.

    :type value: :class:`datetime.datetime`
    :param value: The timestamp to convert.

    :rtype: int
    :returns: The timestamp, in microseconds.
    """
    if not value.tzinfo:
        value = value.replace(tzinfo=UTC)
    # Regardless of what timezone is on the value, convert it to UTC.
    value = value.astimezone(UTC)
    # Convert the datetime to a microsecond timestamp.
    return int(calendar.timegm(value.timetuple()) * 1e6) + value.microsecond


def _millis_from_datetime(value):
    """Convert non-none datetime to timestamp, assuming UTC.

    :type value: :class:`datetime.datetime`, or None
    :param value: the timestamp

    :rtype: int, or ``NoneType``
    :returns: the timestamp, in milliseconds, or None
    """
    if value is not None:
        return _millis(value)


def _total_seconds_backport(offset):
    """Backport of timedelta.total_seconds() from python 2.7+.

    :type offset: :class:`datetime.timedelta`
    :param offset: A timedelta object.

    :rtype: int
    :returns: The total seconds (including microseconds) in the
              duration.
    """
    seconds = offset.days * 24 * 60 * 60 + offset.seconds
    return seconds + offset.microseconds * 1e-6


def _total_seconds(offset):
    """Version independent total seconds for a time delta.

    :type offset: :class:`datetime.timedelta`
    :param offset: A timedelta object.

    :rtype: int
    :returns: The total seconds (including microseconds) in the
              duration.
    """
    if sys.version_info[:2] < (2, 7):  # pragma: NO COVER Python 2.6
        return _total_seconds_backport(offset)
    else:
        return offset.total_seconds()


def _rfc3339_to_datetime(dt_str):
    """Convert a microsecond-precision timetamp to a native datetime.

    :type dt_str: str
    :param dt_str: The string to convert.

    :rtype: :class:`datetime.datetime`
    :returns: The datetime object created from the string.
    """
    return datetime.datetime.strptime(
        dt_str, _RFC3339_MICROS).replace(tzinfo=UTC)


def _rfc3339_nanos_to_datetime(dt_str):
    """Convert a nanosecond-precision timestamp to a native datetime.

    .. note::

       Python datetimes do not support nanosecond precision;  this function
       therefore truncates such values to microseconds.

    :type dt_str: str
    :param dt_str: The string to convert.

    :rtype: :class:`datetime.datetime`
    :returns: The datetime object created from the string.
    :raises ValueError: If the timestamp does not match the RFC 3339
                        regular expression.
    """
    with_nanos = _RFC3339_NANOS.match(dt_str)
    if with_nanos is None:
        raise ValueError(
            'Timestamp: %r, does not match pattern: %r' % (
                dt_str, _RFC3339_NANOS.pattern))
    bare_seconds = datetime.datetime.strptime(
        with_nanos.group('no_fraction'), _RFC3339_NO_FRACTION)
    fraction = with_nanos.group('nanos')
    scale = 9 - len(fraction)
    nanos = int(fraction) * (10 ** scale)
    micros = nanos // 1000
    return bare_seconds.replace(microsecond=micros, tzinfo=UTC)


def _datetime_to_rfc3339(value, ignore_zone=True):
    """Convert a timestamp to a string.

    :type value: :class:`datetime.datetime`
    :param value: The datetime object to be converted to a string.

    :type ignore_zone: boolean
    :param ignore_zone: If True, then the timezone (if any) of the datetime
                        object is ignored.

    :rtype: str
    :returns: The string representing the datetime stamp.
    """
    if not ignore_zone and value.tzinfo is not None:
        # Convert to UTC and remove the time zone info.
        value = value.replace(tzinfo=None) - value.utcoffset()

    return value.strftime(_RFC3339_MICROS)


def _to_bytes(value, encoding='ascii'):
    """Converts a string value to bytes, if necessary.

    Unfortunately, ``six.b`` is insufficient for this task since in
    Python2 it does not modify ``unicode`` objects.

    :type value: str / bytes or unicode
    :param value: The string/bytes value to be converted.

    :type encoding: str
    :param encoding: The encoding to use to convert unicode to bytes. Defaults
                     to "ascii", which will not allow any characters from
                     ordinals larger than 127. Other useful values are
                     "latin-1", which which will only allows byte ordinals
                     (up to 255) and "utf-8", which will encode any unicode
                     that needs to be.

    :rtype: str / bytes
    :returns: The original value converted to bytes (if unicode) or as passed
              in if it started out as bytes.
    :raises TypeError: if the value could not be converted to bytes.
    """
    result = (value.encode(encoding)
              if isinstance(value, six.text_type) else value)
    if isinstance(result, six.binary_type):
        return result
    else:
        raise TypeError('%r could not be converted to bytes' % (value,))


def _bytes_to_unicode(value):
    """Converts bytes to a unicode value, if necessary.

    :type value: bytes
    :param value: bytes value to attempt string conversion on.

    :rtype: str
    :returns: The original value converted to unicode (if bytes) or as passed
              in if it started out as unicode.

    :raises ValueError: if the value could not be converted to unicode.
    """
    result = (value.decode('utf-8')
              if isinstance(value, six.binary_type) else value)
    if isinstance(result, six.text_type):
        return result
    else:
        raise ValueError('%r could not be converted to unicode' % (value,))


def _pb_timestamp_to_datetime(timestamp):
    """Convert a Timestamp protobuf to a datetime object.

    :type timestamp: :class:`google.protobuf.timestamp_pb2.Timestamp`
    :param timestamp: A Google returned timestamp protobuf.

    :rtype: :class:`datetime.datetime`
    :returns: A UTC datetime object converted from a protobuf timestamp.
    """
    return (
        _EPOCH +
        datetime.timedelta(
            seconds=timestamp.seconds,
            microseconds=(timestamp.nanos / 1000.0),
        )
    )


def _datetime_to_pb_timestamp(when):
    """Convert a datetime object to a Timestamp protobuf.

    :type when: :class:`datetime.datetime`
    :param when: the datetime to convert

    :rtype: :class:`google.protobuf.timestamp_pb2.Timestamp`
    :returns: A timestamp protobuf corresponding to the object.
    """
    ms_value = _microseconds_from_datetime(when)
    seconds, micros = divmod(ms_value, 10**6)
    nanos = micros * 10**3
    return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)


def _name_from_project_path(path, project, template):
    """Validate a URI path and get the leaf object's name.

    :type path: str
    :param path: URI path containing the name.

    :type project: str or NoneType
    :param project: The project associated with the request. It is
                    included for validation purposes.  If passed as None,
                    disables validation.

    :type template: str
    :param template: Template regex describing the expected form of the path.
                     The regex must have two named groups, 'project' and
                     'name'.

    :rtype: str
    :returns: Name parsed from ``path``.
    :raises ValueError: if the ``path`` is ill-formed or if the project from
                        the ``path`` does not agree with the ``project``
                        passed in.
    """
    if isinstance(template, str):
        template = re.compile(template)

    match = template.match(path)

    if not match:
        raise ValueError('path "%s" did not match expected pattern "%s"' % (
            path, template.pattern,))

    if project is not None:
        found_project = match.group('project')
        if found_project != project:
            raise ValueError(
                'Project from client (%s) should agree with '
                'project from resource(%s).' % (project, found_project))

    return match.group('name')


try:
    from pytz import UTC  # pylint: disable=unused-import,wrong-import-order
except ImportError:
    UTC = _UTC()  # Singleton instance to be used throughout.

# Need to define _EPOCH at the end of module since it relies on UTC.
_EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=UTC)
