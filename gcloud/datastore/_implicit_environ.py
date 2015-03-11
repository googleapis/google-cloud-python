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

"""Module to provide implicit behavior based on enviroment.

Allows the datastore package to infer the current dataset ID and
connection from the enviroment.
"""

import os
import socket

from six.moves.http_client import HTTPConnection  # pylint: disable=F0401

try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None

from gcloud import credentials
from gcloud.datastore.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/datastore',
         'https://www.googleapis.com/auth/userinfo.email')
"""The scopes required for authenticating as a Cloud Datastore consumer."""

_DATASET_ENV_VAR_NAME = 'GCLOUD_DATASET_ID'
_GCD_DATASET_ENV_VAR_NAME = 'DATASTORE_DATASET'


def app_engine_id():
    """Gets the App Engine application ID if it can be inferred.

    :rtype: string or ``NoneType``
    :returns: App Engine application ID if running in App Engine,
              else ``None``.
    """
    if app_identity is None:
        return None

    return app_identity.get_application_id()


def compute_engine_id():
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


def _get_production_dataset_id():
    """Gets the production application ID if it can be inferred."""
    return os.getenv(_DATASET_ENV_VAR_NAME)


def _get_gcd_dataset_id():
    """Gets the GCD application ID if it can be inferred."""
    return os.getenv(_GCD_DATASET_ENV_VAR_NAME)


def _determine_default_dataset_id(dataset_id=None):
    """Determine default dataset ID explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * GCLOUD_DATASET_ID environment variable
    * DATASTORE_DATASET environment variable (for ``gcd`` testing)
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.

    :rtype: string or ``NoneType``
    :returns: Default dataset ID if it can be determined.
    """
    if dataset_id is None:
        dataset_id = _get_production_dataset_id()

    if dataset_id is None:
        dataset_id = _get_gcd_dataset_id()

    if dataset_id is None:
        dataset_id = app_engine_id()

    if dataset_id is None:
        dataset_id = compute_engine_id()

    return dataset_id


def set_default_dataset_id(dataset_id=None):
    """Set default dataset ID either explicitly or implicitly as fall-back.

    In implicit case, supports four environments. In order of precedence, the
    implicit environments are:

    * GCLOUD_DATASET_ID environment variable
    * DATASTORE_DATASET environment variable (for ``gcd`` testing)
    * Google App Engine application ID
    * Google Compute Engine project ID (from metadata server)

    :type dataset_id: string
    :param dataset_id: Optional. The dataset ID to use as default.

    :raises: :class:`EnvironmentError` if no dataset ID was implied.
    """
    dataset_id = _determine_default_dataset_id(dataset_id=dataset_id)
    if dataset_id is not None:
        _DEFAULTS.dataset_id = dataset_id
    else:
        raise EnvironmentError('No dataset ID could be inferred.')


def get_default_dataset_id():
    """Get default dataset ID.

    :rtype: string or ``NoneType``
    :returns: The default dataset ID if one has been set.
    """
    return _DEFAULTS.dataset_id


def get_connection():
    """Shortcut method to establish a connection to the Cloud Datastore.

    Use this if you are going to access several datasets
    with the same set of credentials (unlikely):

    >>> from gcloud import datastore

    >>> connection = datastore.get_connection()
    >>> key1 = datastore.Key('Kind', 1234, dataset_id='dataset1')
    >>> key2 = datastore.Key('Kind', 1234, dataset_id='dataset2')
    >>> entity1 = datastore.get(key1, connection=connection)
    >>> entity2 = datastore.get(key2, connection=connection)

    :rtype: :class:`gcloud.datastore.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    implicit_credentials = credentials.get_credentials()
    scoped_credentials = implicit_credentials.create_scoped(SCOPE)
    return Connection(credentials=scoped_credentials)


def set_default_connection(connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    connection = connection or get_connection()
    _DEFAULTS.connection = connection


def get_default_connection():
    """Get default connection.

    :rtype: :class:`gcloud.datastore.connection.Connection` or ``NoneType``
    :returns: The default connection if one has been set.
    """
    return _DEFAULTS.connection


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
        if obj is None or objtype is not _DefaultsContainer:
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


class _DefaultsContainer(object):
    """Container for defaults.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: Persistent implied connection from environment.

    :type dataset_id: string
    :param dataset_id: Persistent implied dataset ID from environment.
    """

    @_lazy_property_deco
    @staticmethod
    def dataset_id():
        """Return the implicit default dataset ID."""
        return _determine_default_dataset_id()

    @_lazy_property_deco
    @staticmethod
    def connection():
        """Return the implicit default connection.."""
        return get_connection()

    def __init__(self, connection=None, dataset_id=None, implicit=False):
        if connection is not None or not implicit:
            self.connection = connection
        if dataset_id is not None or not implicit:
            self.dataset_id = dataset_id


_DEFAULTS = _DefaultsContainer(implicit=True)
