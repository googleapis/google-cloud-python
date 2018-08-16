# Copyright 2015 Google LLC
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

"""Client for interacting with the Google Cloud Storage API."""


from google.auth.credentials import AnonymousCredentials

from google.api_core import page_iterator
from google.cloud._helpers import _LocalStack
from google.cloud.client import ClientWithProject
from google.cloud.exceptions import NotFound
from google.cloud.storage._http import Connection
from google.cloud.storage.batch import Batch
from google.cloud.storage.bucket import Bucket


_marker = object()


class Client(ClientWithProject):
    """Client to bundle configuration needed for API requests.

    :type project: str or None
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`~google.auth.credentials.Credentials`
    :param credentials: (Optional) The OAuth2 Credentials to use for this
                        client. If not passed (and if no ``_http`` object is
                        passed), falls back to the default inferred from the
                        environment.

    :type _http: :class:`~requests.Session`
    :param _http: (Optional) HTTP object to make requests. Can be any object
                  that defines ``request()`` with the same interface as
                  :meth:`requests.Session.request`. If not passed, an
                  ``_http`` object is created that is bound to the
                  ``credentials`` for the current object.
                  This parameter should be considered private, and could
                  change in the future.
    """

    SCOPE = ('https://www.googleapis.com/auth/devstorage.full_control',
             'https://www.googleapis.com/auth/devstorage.read_only',
             'https://www.googleapis.com/auth/devstorage.read_write')
    """The scopes required for authenticating as a Cloud Storage consumer."""

    def __init__(self, project=_marker, credentials=None, _http=None):
        self._base_connection = None
        if project is None:
            no_project = True
            project = '<none>'
        else:
            no_project = False
        if project is _marker:
            project = None
        super(Client, self).__init__(project=project, credentials=credentials,
                                     _http=_http)
        if no_project:
            self.project = None
        self._connection = Connection(self)
        self._batch_stack = _LocalStack()

    @classmethod
    def create_anonymous_client(cls):
        """Factory: return client with anonymous credentials.

        .. note::

           Such a client has only limited access to "public" buckets:
           listing their contents and downloading their blobs.

        :rtype: :class:`google.cloud.storage.client.Client`
        :returns: Instance w/ anonymous credentials and no project.
        """
        client = cls(project='<none>', credentials=AnonymousCredentials())
        client.project = None
        return client

    @property
    def _connection(self):
        """Get connection or batch on the client.

        :rtype: :class:`google.cloud.storage._http.Connection`
        :returns: The connection set on the client, or the batch
                  if one is set.
        """
        if self.current_batch is not None:
            return self.current_batch
        else:
            return self._base_connection

    @_connection.setter
    def _connection(self, value):
        """Set connection on the client.

        Intended to be used by constructor (since the base class calls)
            self._connection = connection
        Will raise if the connection is set more than once.

        :type value: :class:`google.cloud.storage._http.Connection`
        :param value: The connection set on the client.

        :raises: :class:`ValueError` if connection has already been set.
        """
        if self._base_connection is not None:
            raise ValueError('Connection already set on client')
        self._base_connection = value

    def _push_batch(self, batch):
        """Push a batch onto our stack.

        "Protected", intended for use by batch context mgrs.

        :type batch: :class:`google.cloud.storage.batch.Batch`
        :param batch: newly-active batch
        """
        self._batch_stack.push(batch)

    def _pop_batch(self):
        """Pop a batch from our stack.

        "Protected", intended for use by batch context mgrs.

        :raises: IndexError if the stack is empty.
        :rtype: :class:`google.cloud.storage.batch.Batch`
        :returns: the top-most batch/transaction, after removing it.
        """
        return self._batch_stack.pop()

    @property
    def current_batch(self):
        """Currently-active batch.

        :rtype: :class:`google.cloud.storage.batch.Batch` or ``NoneType`` (if
                no batch is active).
        :returns: The batch at the top of the batch stack.
        """
        return self._batch_stack.top

    def get_service_account_email(self, project=None):
        """Get the email address of the project's GCS service account

        :type project: str
        :param project:
            (Optional) Project ID to use for retreiving GCS service account
            email address.  Defaults to the client's project.

        :rtype: str
        :returns: service account email address
        """
        if project is None:
            project = self.project
        path = '/projects/%s/serviceAccount' % (project,)
        api_response = self._base_connection.api_request(
            method='GET', path=path)
        return api_response['email_address']

    def bucket(self, bucket_name, user_project=None):
        """Factory constructor for bucket object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a bucket object owned by this client.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to be instantiated.

        :type user_project: str
        :param user_project: (Optional) the project ID to be billed for API
                             requests made via the bucket.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The bucket object created.
        """
        return Bucket(client=self, name=bucket_name, user_project=user_project)

    def batch(self):
        """Factory constructor for batch object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a batch object owned by this client.

        :rtype: :class:`google.cloud.storage.batch.Batch`
        :returns: The batch object created.
        """
        return Batch(client=self)

    def get_bucket(self, bucket_name):
        """Get a bucket by name.

        If the bucket isn't found, this will raise a
        :class:`google.cloud.exceptions.NotFound`.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START get_bucket]
            :end-before: [END get_bucket]

        This implements "storage.buckets.get".

        :type bucket_name: str
        :param bucket_name: The name of the bucket to get.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The bucket matching the name provided.
        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        bucket = Bucket(self, name=bucket_name)
        bucket.reload(client=self)
        return bucket

    def lookup_bucket(self, bucket_name):
        """Get a bucket by name, returning None if not found.

        You can use this if you would rather check for a None value
        than catching an exception:

        .. literalinclude:: snippets.py
            :start-after: [START lookup_bucket]
            :end-before: [END lookup_bucket]

        :type bucket_name: str
        :param bucket_name: The name of the bucket to get.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The bucket matching the name provided or None if not found.
        """
        try:
            return self.get_bucket(bucket_name)
        except NotFound:
            return None

    def create_bucket(self, bucket_name, requester_pays=None, project=None):
        """Create a new bucket.

        For example:

        .. literalinclude:: snippets.py
            :start-after: [START create_bucket]
            :end-before: [END create_bucket]

        This implements "storage.buckets.insert".

        If the bucket already exists, will raise
        :class:`google.cloud.exceptions.Conflict`.

        To set additional properties when creating a bucket, such as the
        bucket location, use :meth:`~.Bucket.create`.

        :type bucket_name: str
        :param bucket_name: The bucket name to create.

        :type requester_pays: bool
        :param requester_pays:
            (Optional) Whether requester pays for API requests for this
            bucket and its blobs.

        :type project: str
        :param project: (Optional) the project under which the  bucket is to
                        be created.  If not passed, uses the project set on
                        the client.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The newly created bucket.
        """
        bucket = Bucket(self, name=bucket_name)
        if requester_pays is not None:
            bucket.requester_pays = requester_pays
        bucket.create(client=self, project=project)
        return bucket

    def list_buckets(self, max_results=None, page_token=None, prefix=None,
                     projection='noAcl', fields=None, project=None):
        """Get all buckets in the project associated to the client.

        This will not populate the list of blobs available in each
        bucket.

        .. literalinclude:: snippets.py
            :start-after: [START list_buckets]
            :end-before: [END list_buckets]

        This implements "storage.buckets.list".

        :type max_results: int
        :param max_results: Optional. Maximum number of buckets to return.

        :type page_token: str
        :param page_token: Optional. Opaque marker for the next "page" of
                           buckets. If not passed, will return the first page
                           of buckets.

        :type prefix: str
        :param prefix: Optional. Filter results to buckets whose names begin
                       with this prefix.

        :type projection: str
        :param projection:
            (Optional) Specifies the set of properties to return. If used, must
            be 'full' or 'noAcl'. Defaults to 'noAcl'.

        :type fields: str
        :param fields:
            (Optional) Selector specifying which fields to include in a partial
            response. Must be a list of fields. For example to get a partial
            response with just the next page token and the language of each
            bucket returned: 'items/id,nextPageToken'

        :type project: str
        :param project: (Optional) the project whose buckets are to be listed.
                        If not passed, uses the project set on the client.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :raises ValueError: if both ``project`` is ``None`` and the client's
                            project is also ``None``.
        :returns: Iterator of all :class:`~google.cloud.storage.bucket.Bucket`
                  belonging to this project.
        """
        if project is None:
            project = self.project

        if project is None:
            raise ValueError(
                "Client project not set:  pass an explicit project.")

        extra_params = {'project': project}

        if prefix is not None:
            extra_params['prefix'] = prefix

        extra_params['projection'] = projection

        if fields is not None:
            extra_params['fields'] = fields

        return page_iterator.HTTPIterator(
            client=self,
            api_request=self._connection.api_request,
            path='/b',
            item_to_value=_item_to_bucket,
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params)


def _item_to_bucket(iterator, item):
    """Convert a JSON bucket to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type item: dict
    :param item: An item to be converted to a bucket.

    :rtype: :class:`.Bucket`
    :returns: The next bucket in the page.
    """
    name = item.get('name')
    bucket = Bucket(iterator.client, name)
    bucket._set_properties(item)
    return bucket
