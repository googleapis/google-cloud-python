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

"""Shortcut methods for getting set up with Google Cloud Storage.

You'll typically use these to get started with the API:

>>> from gcloud import storage
>>> storage.set_defaults()
>>> bucket = storage.get_bucket('bucket-id-here')
>>> # Then do other things...
>>> blob = bucket.get_blob('/remote/path/to/file.txt')
>>> print blob.download_as_string()
>>> blob.upload_from_string('New contents!')
>>> bucket.upload_file('/remote/path/storage.txt', '/local/path.txt')

The main concepts with this API are:

- :class:`gcloud.storage.connection.Connection` which represents a
  connection between your machine and the Cloud Storage API.

- :class:`gcloud.storage.bucket.Bucket` which represents a particular
  bucket (akin to a mounted disk on a computer).

- :class:`gcloud.storage.blob.Blob` which represents a pointer to a
  particular entity in Cloud Storage (akin to a file path on a remote
  machine).
"""

import os

from gcloud import credentials
from gcloud._helpers import get_default_project
from gcloud._helpers import set_default_project
from gcloud.storage import _implicit_environ
from gcloud.storage._implicit_environ import get_default_bucket
from gcloud.storage._implicit_environ import get_default_connection
from gcloud.storage.api import create_bucket
from gcloud.storage.api import get_all_buckets
from gcloud.storage.api import get_bucket
from gcloud.storage.api import lookup_bucket
from gcloud.storage.blob import Blob
from gcloud.storage.bucket import Bucket
from gcloud.storage.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/devstorage.full_control',
         'https://www.googleapis.com/auth/devstorage.read_only',
         'https://www.googleapis.com/auth/devstorage.read_write')

_BUCKET_ENV_VAR_NAME = 'GCLOUD_BUCKET_NAME'


def set_default_bucket(bucket=None):
    """Set default bucket either explicitly or implicitly as fall-back.

    In implicit case, currently only supports enviroment variable but will
    support App Engine, Compute Engine and other environments in the future.

    In the implicit case, relies on an implicit connection in addition to the
    implicit bucket name.

    Local environment variable used is:
    - GCLOUD_BUCKET_NAME

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: Optional. The bucket to use as default.
    """
    if bucket is None:
        bucket_name = os.getenv(_BUCKET_ENV_VAR_NAME)
        connection = get_default_connection()

        if bucket_name is not None and connection is not None:
            bucket = Bucket(bucket_name, connection=connection)

    if bucket is not None:
        _implicit_environ._DEFAULTS.bucket = bucket


def set_default_connection(connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    connection = connection or get_connection()
    _implicit_environ._DEFAULTS.connection = connection


def set_defaults(bucket=None, project=None, connection=None):
    """Set defaults either explicitly or implicitly as fall-back.

    Uses the arguments to call the individual default methods.

    :type bucket: :class:`gcloud.storage.bucket.Bucket`
    :param bucket: Optional. The bucket to use as default.

    :type project: string
    :param project: Optional. The name of the project to connect to.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: Optional. A connection provided to be the default.
    """
    set_default_project(project=project)
    set_default_connection(connection=connection)
    # NOTE: `set_default_bucket` is called after `set_default_connection`
    #       since `set_default_bucket` falls back to implicit connection.
    set_default_bucket(bucket=bucket)


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
    implicit_credentials = credentials.get_credentials()
    scoped_credentials = implicit_credentials.create_scoped(SCOPE)
    return Connection(credentials=scoped_credentials)
