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

"""gcloud storage client for interacting with API."""


from gcloud.client import JSONClient
from gcloud.exceptions import NotFound
from gcloud.iterator import Iterator
from gcloud.storage.bucket import Bucket
from gcloud.storage.connection import Connection


class Client(JSONClient):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def get_bucket(self, bucket_name):
        """Get a bucket by name.

        If the bucket isn't found, this will raise a
        :class:`gcloud.storage.exceptions.NotFound`.

        For example::

          >>> try:
          >>>   bucket = client.get_bucket('my-bucket')
          >>> except gcloud.exceptions.NotFound:
          >>>   print 'Sorry, that bucket does not exist!'

        This implements "storage.buckets.get".

        :type bucket_name: string
        :param bucket_name: The name of the bucket to get.

        :rtype: :class:`gcloud.storage.bucket.Bucket`
        :returns: The bucket matching the name provided.
        :raises: :class:`gcloud.exceptions.NotFound`
        """
        bucket = Bucket(self, name=bucket_name)
        bucket.reload(client=self)
        return bucket

    def lookup_bucket(self, bucket_name):
        """Get a bucket by name, returning None if not found.

        You can use this if you would rather check for a None value
        than catching an exception::

          >>> bucket = client.lookup_bucket('doesnt-exist')
          >>> print bucket
          None
          >>> bucket = client.lookup_bucket('my-bucket')
          >>> print bucket
          <Bucket: my-bucket>

        :type bucket_name: string
        :param bucket_name: The name of the bucket to get.

        :rtype: :class:`gcloud.storage.bucket.Bucket`
        :returns: The bucket matching the name provided or None if not found.
        """
        try:
            return self.get_bucket(bucket_name)
        except NotFound:
            return None

    def create_bucket(self, bucket_name):
        """Create a new bucket.

        For example::

          >>> bucket = client.create_bucket('my-bucket')
          >>> print bucket
          <Bucket: my-bucket>

        This implements "storage.buckets.insert".

        If the bucket already exists, will raise
        :class:`gcloud.exceptions.Conflict`.

        :type bucket_name: string
        :param bucket_name: The bucket name to create.

        :rtype: :class:`gcloud.storage.bucket.Bucket`
        :returns: The newly created bucket.
        """
        bucket = Bucket(self, name=bucket_name)
        bucket.create(self.project, client=self)
        return bucket

    def list_buckets(self, max_results=None, page_token=None, prefix=None,
                     projection='noAcl', fields=None):
        """Get all buckets in the project associated to the client.

        This will not populate the list of blobs available in each
        bucket.

          >>> for bucket in client.list_buckets():
          >>>   print bucket

        This implements "storage.buckets.list".

        :type max_results: integer or ``NoneType``
        :param max_results: Optional. Maximum number of buckets to return.

        :type page_token: string or ``NoneType``
        :param page_token: Optional. Opaque marker for the next "page" of
                           buckets. If not passed, will return the first page
                           of buckets.

        :type prefix: string or ``NoneType``
        :param prefix: Optional. Filter results to buckets whose names begin
                       with this prefix.

        :type projection: string or ``NoneType``
        :param projection: If used, must be 'full' or 'noAcl'. Defaults to
                           'noAcl'. Specifies the set of properties to return.

        :type fields: string or ``NoneType``
        :param fields: Selector specifying which fields to include in a
                       partial response. Must be a list of fields. For example
                       to get a partial response with just the next page token
                       and the language of each bucket returned:
                       'items/id,nextPageToken'

        :rtype: iterable of :class:`gcloud.storage.bucket.Bucket` objects.
        :returns: All buckets belonging to this project.
        """
        extra_params = {'project': self.project}

        if max_results is not None:
            extra_params['maxResults'] = max_results

        if prefix is not None:
            extra_params['prefix'] = prefix

        extra_params['projection'] = projection

        if fields is not None:
            extra_params['fields'] = fields

        result = _BucketIterator(connection=self.connection,
                                 extra_params=extra_params)
        # Page token must be handled specially since the base `Iterator`
        # class has it as a reserved property.
        if page_token is not None:
            result.next_page_token = page_token
        return result


class _BucketIterator(Iterator):
    """An iterator listing all buckets.

    You shouldn't have to use this directly, but instead should use the
    helper methods on :class:`gcloud.storage.connection.Connection`
    objects.

    :type connection: :class:`gcloud.storage.connection.Connection`
    :param connection: The connection to use for querying the list of buckets.

    :type extra_params: dict or ``NoneType``
    :param extra_params: Extra query string parameters for the API call.
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
            bucket = Bucket(None, name)
            bucket._set_properties(item)
            yield bucket
