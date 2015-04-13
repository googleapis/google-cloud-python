# Copyright 2015 Google Inc. All rights reserved.
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

Allows the storage package to infer the default bucket and connection
from the enviroment.
"""


from gcloud.connection import get_scoped_connection
from gcloud.storage.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/devstorage.full_control',
         'https://www.googleapis.com/auth/devstorage.read_only',
         'https://www.googleapis.com/auth/devstorage.read_write')


class _DefaultsContainer(object):
    """Container for defaults.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: Persistent implied default bucket from environment.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: Persistent implied connection from environment.
    """

    def __init__(self, bucket=None, connection=None):
        self.bucket = bucket
        self.connection = connection


def get_default_bucket():
    """Get default bucket.

    :rtype: :class:`gcloud.storage.bucket.Bucket` or ``NoneType``
    :returns: The default bucket if one has been set.
    """
    return _DEFAULTS.bucket


def get_default_connection():
    """Get default connection.

    :rtype: :class:`gcloud.storage.connection.Connection` or ``NoneType``
    :returns: The default connection if one has been set.
    """
    return _DEFAULTS.connection


def get_connection():
    """Shortcut method to establish a connection to Cloud Storage.

    Use this if you are going to access several buckets with the same
    set of credentials:

    >>> from gcloud import storage
    >>> connection = storage.get_connection()
    >>> bucket1 = storage.get_bucket('bucket1', connection=connection)
    >>> bucket2 = storage.get_bucket('bucket2', connection=connection)

    :rtype: :class:`gcloud.storage.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    return get_scoped_connection(Connection, SCOPE)


def set_default_connection(connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    connection = connection or get_connection()
    _DEFAULTS.connection = connection


_DEFAULTS = _DefaultsContainer()
