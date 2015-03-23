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


_DEFAULTS = _DefaultsContainer()
