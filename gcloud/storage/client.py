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
        bucket = Bucket(bucket_name)
        bucket.reload(connection=self.connection)
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
        bucket = Bucket(bucket_name)
        bucket.create(self.project, connection=self.connection)
        return bucket
