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
from gcloud._helpers import get_default_project
from gcloud.storage._helpers import _require_connection
from gcloud.storage.bucket import Bucket
from gcloud.storage.iterator import Iterator


def lookup_bucket(bucket_name, connection=None):
    """Get a bucket by name, returning None if not found.

    You can use this if you would rather checking for a None value
    than catching an exception::

      >>> from gcloud import storage
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
    connection = _require_connection(connection)
    try:
        return get_bucket(bucket_name, connection=connection)
    except NotFound:
        return None


def list_buckets(project=None, max_results=None, page_token=None, prefix=None,
                 projection='noAcl', fields=None, connection=None):
    """Get all buckets in the project.

    This will not populate the list of blobs available in each
    bucket.

      >>> from gcloud import storage
      >>> for bucket in storage.list_buckets():
      >>>   print bucket

    This implements "storage.buckets.list".

    :type project: string or ``NoneType``
    :param project: Optional. The project to use when listing all buckets.
                    If not provided, falls back to default.

    :type max_results: integer or ``NoneType``
    :param max_results: Optional. Maximum number of buckets to return.

    :type page_token: string or ``NoneType``
    :param page_token: Optional. Opaque marker for the next "page" of buckets.
                       If not passed, will return the first page of buckets.

    :type prefix: string or ``NoneType``
    :param prefix: Optional. Filter results to buckets whose names begin with
                   this prefix.

    :type projection: string or ``NoneType``
    :param projection: If used, must be 'full' or 'noAcl'. Defaults to
                       'noAcl'. Specifies the set of properties to return.

    :type fields: string or ``NoneType``
    :param fields: Selector specifying which fields to include in a
                   partial response. Must be a list of fields. For example
                   to get a partial response with just the next page token
                   and the language of each bucket returned:
                   'items/id,nextPageToken'

    :type connection: :class:`gcloud.storage.connection.Connection` or
                      ``NoneType``
    :param connection: Optional. The connection to use when sending requests.
                       If not provided, falls back to default.

    :rtype: iterable of :class:`gcloud.storage.bucket.Bucket` objects.
    :returns: All buckets belonging to this project.
    """
    connection = _require_connection(connection)
    if project is None:
        project = get_default_project()
    extra_params = {'project': project}

    if max_results is not None:
        extra_params['maxResults'] = max_results

    if prefix is not None:
        extra_params['prefix'] = prefix

    extra_params['projection'] = projection

    if fields is not None:
        extra_params['fields'] = fields

    result = _BucketIterator(connection=connection,
                             extra_params=extra_params)
    # Page token must be handled specially since the base `Iterator`
    # class has it as a reserved property.
    if page_token is not None:
        result.next_page_token = page_token
    return iter(result)


def get_bucket(bucket_name, connection=None):
    """Get a bucket by name.

    If the bucket isn't found, this will raise a
    :class:`gcloud.storage.exceptions.NotFound`.

    For example::

      >>> from gcloud import storage
      >>> from gcloud.exceptions import NotFound
      >>> try:
      >>>   bucket = storage.get_bucket('my-bucket')
      >>> except NotFound:
      >>>   print 'Sorry, that bucket does not exist!'

    This implements "storage.buckets.get".

    :type bucket_name: string
    :param bucket_name: The name of the bucket to get.

    :type connection: :class:`gcloud.storage.connection.Connection` or
                      ``NoneType``
    :param connection: Optional. The connection to use when sending requests.
                       If not provided, falls back to default.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: The bucket matching the name provided.
    :raises: :class:`gcloud.exceptions.NotFound`
    """
    connection = _require_connection(connection)
    bucket = Bucket(bucket_name, connection=connection)
    bucket.reload()
    return bucket


def create_bucket(bucket_name, project=None, connection=None):
    """Create a new bucket.

    For example::

      >>> from gcloud import storage
      >>> bucket = storage.create_bucket('my-bucket')
      >>> print bucket
      <Bucket: my-bucket>

    This implements "storage.buckets.insert".

    If the bucket already exists, will raise
    :class:`gcloud.exceptions.Conflict`.

    :type project: string
    :param project: Optional. The project to use when creating bucket.
                    If not provided, falls back to default.

    :type bucket_name: string
    :param bucket_name: The bucket name to create.

    :type connection: :class:`gcloud.storage.connection.Connection` or
                      ``NoneType``
    :param connection: Optional. The connection to use when sending requests.
                       If not provided, falls back to default.

    :rtype: :class:`gcloud.storage.bucket.Bucket`
    :returns: The newly created bucket.
    """
    connection = _require_connection(connection)
    bucket = Bucket(bucket_name, connection=connection)
    bucket.create(project)
    return bucket


class _BucketIterator(Iterator):
    """An iterator listing all buckets.

    You shouldn't have to use this directly, but instead should use the
    helper methods on :class:`gcloud.storage.connection.Connection`
    objects.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use for querying the list of buckets.
    """

    def __init__(self, connection, extra_params=None):
        super(_BucketIterator, self).__init__(connection=connection, path='/b',
                                              extra_params=extra_params)

    def get_items_from_response(self, response):
        """Factory method which yields :class:`.Bucket` items from a response.

        :type response: dict
        :param response: The JSON API response for a page of buckets.
        """
        for item in response.get('items', []):
            name = item.get('name')
            bucket = Bucket(name, connection=self.connection)
            bucket._set_properties(item)
            yield bucket
