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


class _LazyProperty(object):
    """Descriptor for lazy loaded property.

    This follows the reify pattern: lazy evaluation and then replacement
    after evaluation.

    :type name: string
    :param name: The name of the attribute / property being evaluated.

    :type deferred_callable: callable that takes no arguments
    :param deferred_callable: The function / method used to evaluate the
                              property.
    """

    def __init__(self, name, deferred_callable):
        self._name = name
        self._deferred_callable = deferred_callable

    def __get__(self, obj, objtype):
        if obj is None:
            return self

        setattr(obj, self._name, self._deferred_callable())
        return getattr(obj, self._name)


def _lazy_property_deco(deferred_callable):
    """Decorator a method to create a :class:`_LazyProperty`.

    :type deferred_callable: callable that takes no arguments
    :param deferred_callable: The function / method used to evaluate the
                              property.

    :rtype: :class:`_LazyProperty`.
    :returns: A lazy property which defers the deferred_callable.
    """
    if isinstance(deferred_callable, staticmethod):
        # H/T: http://stackoverflow.com/a/9527450/1068170
        #      For Python2.7+ deferred_callable.__func__ would suffice.
        deferred_callable = deferred_callable.__get__(True)
    return _LazyProperty(deferred_callable.__name__, deferred_callable)


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


_PROJECT_ENV_VAR_NAME = 'GCLOUD_PROJECT'


def _get_production_project():
    """Gets the production project if it can be inferred."""
    return os.getenv(_PROJECT_ENV_VAR_NAME)


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


def set_default_project(project=None):
    """Set default project either explicitly or implicitly as fall-back.

    :type project: string
    :param project: Optional. The project name to use as default.

    :raises: :class:`EnvironmentError` if no project was found.
    """
    project = _determine_default_project(project=project)
    if project is not None:
        _DEFAULTS.project = project
    else:
        raise EnvironmentError('No project could be inferred.')


class _DefaultsContainer(object):
    """Container for defaults.

    :type project: string
    :param project: Persistent implied project from environment.

    :type implicit: boolean
    :param implicit: if False, assign the instance's ``project`` attribute
                     unconditionally;  otherwise, assign it only if the
                     value is not None.
    """

    @_lazy_property_deco
    @staticmethod
    def project():
        """Return the implicit default project."""
        return _determine_default_project()

    def __init__(self, project=None, implicit=False):
        if project is not None or not implicit:
            self.project = project


_DEFAULTS = _DefaultsContainer(implicit=True)
