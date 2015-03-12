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

"""Methods for interacting with Google Cloud Storage.

Allows interacting with Cloud Storage via user-friendly objects
rather than via Connection.
"""

from gcloud.exceptions import NotFound
from gcloud.storage._implicit_environ import get_default_connection


def lookup_bucket(bucket_name, connection=None):
    """Get a bucket by name, returning None if not found.

    You can use this if you would rather checking for a None value
    than catching an exception::

      >>> from gcloud import storage
      >>> storage.set_defaults()
      >>> bucket = storage.lookup_bucket('doesnt-exist')
      >>> print bucket
      None
      >>> bucket = storage.lookup_bucket('my-bucket')
      >>> print bucket
      <Bucket: my-bucket>

    :type bucket_name: string
    :param bucket_name: The name of the bucket to get.

    :type connection: :class:`gcloud.storage.connection.Connection` or
                      ``NoneType``
    :param connection: Optional. The connection to use when sending requests.
                       If not provided, falls back to default.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: The bucket matching the name provided or None if not found.
    """
    if connection is None:
        connection = get_default_connection()

    try:
        return connection.get_bucket(bucket_name)
    except NotFound:
        return None
