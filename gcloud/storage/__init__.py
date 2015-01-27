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

>>> import gcloud.storage
>>> bucket = gcloud.storage.get_bucket('bucket-id-here', 'project-id')
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
from gcloud.storage import _implicit_environ
from gcloud.storage.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/devstorage.full_control',
         'https://www.googleapis.com/auth/devstorage.read_only',
         'https://www.googleapis.com/auth/devstorage.read_write')

_BUCKET_ENV_VAR_NAME = 'GCLOUD_BUCKET_NAME'
_PROJECT_ENV_VAR_NAME = 'GCLOUD_PROJECT'


def set_default_bucket_name(bucket_name=None):
    """Set default bucket name either explicitly or implicitly as fall-back.

    In implicit case, currently only supports enviroment variable but will
    support App Engine, Compute Engine and other environments in the future.

    Local environment variable used is:
    - GCLOUD_BUCKET_NAME

    :type bucket_name: string
    :param bucket_name: Optional. The bucket name to use as default.
    """
    if bucket_name is None:
        bucket_name = os.getenv(_BUCKET_ENV_VAR_NAME)

    if bucket_name is not None:
        _implicit_environ.BUCKET_NAME = bucket_name


def set_default_project(project=None):
    """Set default bucket name either explicitly or implicitly as fall-back.

    In implicit case, currently only supports enviroment variable but will
    support App Engine, Compute Engine and other environments in the future.

    Local environment variable used is:
    - GCLOUD_PROJECT

    :type project: string
    :param project: Optional. The project name to use as default.
    """
    if project is None:
        project = os.getenv(_PROJECT_ENV_VAR_NAME)

    if project is not None:
        _implicit_environ.PROJECT = project


def set_default_connection(project=None, connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type project: string
    :param project: Optional. The name of the project to connect to.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    if project is None:
        project = _implicit_environ.PROJECT

    connection = connection or get_connection(project)
    _implicit_environ.CONNECTION = connection


def set_defaults(bucket_name=None, project=None, connection=None):
    """Set defaults either explicitly or implicitly as fall-back.

    Uses the arguments to call the individual default methods.

    :type bucket_name: string
    :param bucket_name: Optional. The bucket name to use as default.

    :type project: string
    :param project: Optional. The name of the project to connect to.

    :type connection: :class:`gcloud.datastore.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    set_default_bucket_name(bucket_name=bucket_name)
    # NOTE: `set_default_project` is called before `set_default_connection`
    #       since `set_default_connection` falls back to implicit project.
    set_default_project(project=project)
    set_default_connection(project=project, connection=connection)


def get_connection(project):
    """Shortcut method to establish a connection to Cloud Storage.

    Use this if you are going to access several buckets with the same
    set of credentials:

    >>> from gcloud import storage
    >>> connection = storage.get_connection(project)
    >>> bucket1 = connection.get_bucket('bucket1')
    >>> bucket2 = connection.get_bucket('bucket2')

    :type project: string
    :param project: The name of the project to connect to.

    :rtype: :class:`gcloud.storage.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    implicit_credentials = credentials.get_credentials()
    scoped_credentials = implicit_credentials.create_scoped(SCOPE)
    return Connection(project=project, credentials=scoped_credentials)


def get_bucket(bucket_name, project):
    """Shortcut method to establish a connection to a particular bucket.

    You'll generally use this as the first call to working with the API:

    >>> from gcloud import storage
    >>> bucket = storage.get_bucket(project, bucket_name)
    >>> # Now you can do things with the bucket.
    >>> bucket.exists('/path/to/file.txt')
    False

    :type bucket_name: string
    :param bucket_name: The id of the bucket you want to use.
                      This is akin to a disk name on a file system.

    :type project: string
    :param project: The name of the project to connect to.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: A bucket with a connection using the provided credentials.
    """
    connection = get_connection(project)
    return connection.get_bucket(bucket_name)
