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
>>> key = bucket.get_key('/remote/path/to/file.txt')
>>> print key.get_contents_as_string()
>>> key.set_contents_from_string('New contents!')
>>> bucket.upload_file('/local/path.txt', '/remote/path/storage.txt')

The main concepts with this API are:

- :class:`gcloud.storage.connection.Connection` which represents a
  connection between your machine and the Cloud Storage API.

- :class:`gcloud.storage.bucket.Bucket` which represents a particular
  bucket (akin to a mounted disk on a computer).

- :class:`gcloud.storage.key.Key` which represents a pointer to a
  particular entity in Cloud Storage (akin to a file path on a remote
  machine).
"""

from gcloud import credentials
from gcloud.storage.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/devstorage.full_control',
         'https://www.googleapis.com/auth/devstorage.read_only',
         'https://www.googleapis.com/auth/devstorage.read_write')


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
