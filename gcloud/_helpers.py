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
import os
import socket

try:
    from threading import local as Local
except ImportError:     # pragma: NO COVER (who doesn't have it?)
    class Local(object):
        """Placeholder for non-threaded applications."""

from six.moves.http_client import HTTPConnection  # pylint: disable=F0401

try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None

from gcloud.environment_vars import PROJECT


_NOW = datetime.datetime.utcnow  # To be replaced by tests.
_RFC3339_MICROS = '%Y-%m-%dT%H:%M:%S.%fZ'


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

        :raises: IndexError if the stack is empty.
        :returns: the top-most resource, after removing it.
        """
        return self._stack.pop()

    @property
    def top(self):
        """Get the top-most resource

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

    :type arg_name: string
    :param arg_name: Name of argument to use in error message.

    :type tuple_or_list: sequence of string
    :param tuple_or_list: Sequence to be verified.

    :rtype: list of string
    :returns: The ``tuple_or_list`` passed in cast to a ``list``.
    :raises: class:`TypeError` if the ``tuple_or_list`` is not a tuple or
             list.
    """
    if not isinstance(tuple_or_list, (tuple, list)):
        raise TypeError('Expected %s to be a tuple or list. '
                        'Received %r' % (arg_name, tuple_or_list))
    return list(tuple_or_list)


def _app_engine_id():
    """Gets the App Engine application ID if it can be inferred.

    :rtype: string or ``NoneType``
    :returns: App Engine application ID if running in App Engine,
              else ``None``.
    """
    if app_identity is None:
        return None

    return app_identity.get_application_id()


def _compute_engine_id():
    """Gets the Compute Engine project ID if it can be inferred.

    Uses 169.254.169.254 for the metadata server to avoid request
    latency from DNS lookup.

    See https://cloud.google.com/compute/docs/metadata#metadataserver
    for information about this IP address. (This IP is also used for
    Amazon EC2 instances, so the metadata flavor is crucial.)

    See https://github.com/google/oauth2client/issues/93 for context about
    DNS latency.

    :rtype: string or ``NoneType``
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

    In implicit case, currently only supports enviroment variable but will
    support App Engine, Compute Engine and other environments in the future.

    Local environment variable used is:
    - GCLOUD_PROJECT

    :type project: string
    :param project: Optional. The project name to use as default.

    :rtype: string or ``NoneType``
    :returns: Default project if it can be determined.
    """
    if project is None:
        project = _get_production_project()

    return project


def _millis(when):
    """Convert a zone-aware datetime to integer milliseconds.

    :type when: :class:`datetime.datetime`
    :param when: the datetime to convert

    :rtype: integer
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

    :rtype: integer
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

    :rtype: integer, or ``NoneType``
    :returns: the timestamp, in milliseconds, or None
    """
    if value is not None:
        return _millis(value)


try:
    from pytz import UTC  # pylint: disable=unused-import
except ImportError:
    UTC = _UTC()  # Singleton instance to be used throughout.

# Need to define _EPOCH at the end of module since it relies on UTC.
_EPOCH = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=UTC)
