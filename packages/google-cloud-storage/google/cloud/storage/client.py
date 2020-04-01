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

import base64
import binascii
import collections
import datetime
import functools
import json
import warnings
import google.api_core.client_options

from google.auth.credentials import AnonymousCredentials

from google.api_core import page_iterator
from google.cloud._helpers import _LocalStack, _NOW
from google.cloud.client import ClientWithProject
from google.cloud.exceptions import NotFound
from google.cloud.storage._helpers import _get_storage_host
from google.cloud.storage._http import Connection
from google.cloud.storage._signing import (
    get_expiration_seconds_v4,
    get_v4_now_dtstamps,
    ensure_signed_credentials,
    _sign_message,
)
from google.cloud.storage.batch import Batch
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.blob import Blob
from google.cloud.storage.hmac_key import HMACKeyMetadata
from google.cloud.storage.acl import BucketACL
from google.cloud.storage.acl import DefaultObjectACL
from google.cloud.storage.constants import _DEFAULT_TIMEOUT


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

    :type client_info: :class:`~google.api_core.client_info.ClientInfo`
    :param client_info:
        The client info used to send a user-agent string along with API
        requests. If ``None``, then default info will be used. Generally,
        you only need to set this if you're developing your own library
        or partner tool.
    :type client_options: :class:`~google.api_core.client_options.ClientOptions` or :class:`dict`
    :param client_options: (Optional) Client options used to set user options on the client.
        API Endpoint should be set through client_options.
    """

    SCOPE = (
        "https://www.googleapis.com/auth/devstorage.full_control",
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/devstorage.read_write",
    )
    """The scopes required for authenticating as a Cloud Storage consumer."""

    def __init__(
        self,
        project=_marker,
        credentials=None,
        _http=None,
        client_info=None,
        client_options=None,
    ):
        self._base_connection = None
        if project is None:
            no_project = True
            project = "<none>"
        else:
            no_project = False
        if project is _marker:
            project = None
        super(Client, self).__init__(
            project=project, credentials=credentials, _http=_http
        )

        kw_args = {"client_info": client_info}

        kw_args["api_endpoint"] = _get_storage_host()

        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint
                kw_args["api_endpoint"] = api_endpoint

        if no_project:
            self.project = None
        self._connection = Connection(self, **kw_args)
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
        client = cls(project="<none>", credentials=AnonymousCredentials())
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
            raise ValueError("Connection already set on client")
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

    def _bucket_arg_to_bucket(self, bucket_or_name):
        """Helper to return given bucket or create new by name.

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

        Returns:
            google.cloud.storage.bucket.Bucket
                The newly created bucket or the given one.
        """
        if isinstance(bucket_or_name, Bucket):
            bucket = bucket_or_name
        else:
            bucket = Bucket(self, name=bucket_or_name)
        return bucket

    @property
    def current_batch(self):
        """Currently-active batch.

        :rtype: :class:`google.cloud.storage.batch.Batch` or ``NoneType`` (if
                no batch is active).
        :returns: The batch at the top of the batch stack.
        """
        return self._batch_stack.top

    def get_service_account_email(self, project=None, timeout=_DEFAULT_TIMEOUT):
        """Get the email address of the project's GCS service account

        :type project: str
        :param project:
            (Optional) Project ID to use for retreiving GCS service account
            email address.  Defaults to the client's project.
        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: str
        :returns: service account email address
        """
        if project is None:
            project = self.project
        path = "/projects/%s/serviceAccount" % (project,)
        api_response = self._base_connection.api_request(
            method="GET", path=path, timeout=timeout
        )
        return api_response["email_address"]

    def bucket(self, bucket_name, user_project=None):
        """Factory constructor for bucket object.

        .. note::
          This will not make an HTTP request; it simply instantiates
          a bucket object owned by this client.

        :type bucket_name: str
        :param bucket_name: The name of the bucket to be instantiated.

        :type user_project: str
        :param user_project: (Optional) The project ID to be billed for API
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

    def get_bucket(self, bucket_or_name, timeout=_DEFAULT_TIMEOUT):
        """API call: retrieve a bucket via a GET request.

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets/get

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time, in seconds, to wait for the server response.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            google.cloud.storage.bucket.Bucket
                The bucket matching the name provided.

        Raises:
            google.cloud.exceptions.NotFound
                If the bucket is not found.

        Examples:
            Retrieve a bucket using a string.

            .. literalinclude:: snippets.py
                :start-after: [START get_bucket]
                :end-before: [END get_bucket]

            Get a bucket using a resource.

            >>> from google.cloud import storage
            >>> client = storage.Client()

            >>> # Set properties on a plain resource object.
            >>> bucket = client.get_bucket("my-bucket-name")

            >>> # Time passes. Another program may have modified the bucket
            ... # in the meantime, so you want to get the latest state.
            >>> bucket = client.get_bucket(bucket)  # API request.

        """
        bucket = self._bucket_arg_to_bucket(bucket_or_name)

        bucket.reload(client=self, timeout=timeout)
        return bucket

    def lookup_bucket(self, bucket_name, timeout=_DEFAULT_TIMEOUT):
        """Get a bucket by name, returning None if not found.

        You can use this if you would rather check for a None value
        than catching an exception:

        .. literalinclude:: snippets.py
            :start-after: [START lookup_bucket]
            :end-before: [END lookup_bucket]

        :type bucket_name: str
        :param bucket_name: The name of the bucket to get.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`google.cloud.storage.bucket.Bucket`
        :returns: The bucket matching the name provided or None if not found.
        """
        try:
            return self.get_bucket(bucket_name, timeout=timeout)
        except NotFound:
            return None

    def create_bucket(
        self,
        bucket_or_name,
        requester_pays=None,
        project=None,
        user_project=None,
        location=None,
        predefined_acl=None,
        predefined_default_object_acl=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """API call: create a new bucket via a POST request.

        See
        https://cloud.google.com/storage/docs/json_api/v1/buckets/insert

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.
            requester_pays (bool):
                DEPRECATED. Use Bucket().requester_pays instead.
                (Optional) Whether requester pays for API requests for
                this bucket and its blobs.
            project (str):
                (Optional) The project under which the bucket is to be created.
                If not passed, uses the project set on the client.
            user_project (str):
                (Optional) The project ID to be billed for API requests
                made via created bucket.
            location (str):
                (Optional) The location of the bucket. If not passed,
                the default location, US, will be used. See
                https://cloud.google.com/storage/docs/bucket-locations
            predefined_acl (str):
                (Optional) Name of predefined ACL to apply to bucket. See:
                https://cloud.google.com/storage/docs/access-control/lists#predefined-acl
            predefined_default_object_acl (str):
                (Optional) Name of predefined ACL to apply to bucket's objects. See:
                https://cloud.google.com/storage/docs/access-control/lists#predefined-acl
            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time, in seconds, to wait for the server response.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            google.cloud.storage.bucket.Bucket
                The newly created bucket.

        Raises:
            google.cloud.exceptions.Conflict
                If the bucket already exists.

        Examples:
            Create a bucket using a string.

            .. literalinclude:: snippets.py
                :start-after: [START create_bucket]
                :end-before: [END create_bucket]

            Create a bucket using a resource.

            >>> from google.cloud import storage
            >>> client = storage.Client()

            >>> # Set properties on a plain resource object.
            >>> bucket = storage.Bucket("my-bucket-name")
            >>> bucket.location = "europe-west6"
            >>> bucket.storage_class = "COLDLINE"

            >>> # Pass that resource object to the client.
            >>> bucket = client.create_bucket(bucket)  # API request.

        """
        bucket = self._bucket_arg_to_bucket(bucket_or_name)

        if project is None:
            project = self.project

        if project is None:
            raise ValueError("Client project not set:  pass an explicit project.")

        if requester_pays is not None:
            warnings.warn(
                "requester_pays arg is deprecated. Use Bucket().requester_pays instead.",
                PendingDeprecationWarning,
                stacklevel=1,
            )
            bucket.requester_pays = requester_pays

        query_params = {"project": project}

        if predefined_acl is not None:
            predefined_acl = BucketACL.validate_predefined(predefined_acl)
            query_params["predefinedAcl"] = predefined_acl

        if predefined_default_object_acl is not None:
            predefined_default_object_acl = DefaultObjectACL.validate_predefined(
                predefined_default_object_acl
            )
            query_params["predefinedDefaultObjectAcl"] = predefined_default_object_acl

        if user_project is not None:
            query_params["userProject"] = user_project

        properties = {key: bucket._properties[key] for key in bucket._changes}
        properties["name"] = bucket.name

        if location is not None:
            properties["location"] = location

        api_response = self._connection.api_request(
            method="POST",
            path="/b",
            query_params=query_params,
            data=properties,
            _target_object=bucket,
            timeout=timeout,
        )

        bucket._set_properties(api_response)
        return bucket

    def download_blob_to_file(self, blob_or_uri, file_obj, start=None, end=None):
        """Download the contents of a blob object or blob URI into a file-like object.

        Args:
            blob_or_uri (Union[ \
            :class:`~google.cloud.storage.blob.Blob`, \
             str, \
            ]):
                The blob resource to pass or URI to download.
            file_obj (file):
                A file handle to which to write the blob's data.
            start (int):
                (Optional) The first byte in a range to be downloaded.
            end (int):
                (Optional) The last byte in a range to be downloaded.

        Examples:
            Download a blob using using a blob resource.

            >>> from google.cloud import storage
            >>> client = storage.Client()

            >>> bucket = client.get_bucket('my-bucket-name')
            >>> blob = storage.Blob('path/to/blob', bucket)

            >>> with open('file-to-download-to') as file_obj:
            >>>     client.download_blob_to_file(blob, file_obj)  # API request.


            Download a blob using a URI.

            >>> from google.cloud import storage
            >>> client = storage.Client()

            >>> with open('file-to-download-to') as file_obj:
            >>>     client.download_blob_to_file(
            >>>         'gs://bucket_name/path/to/blob', file_obj)


        """
        try:
            blob_or_uri.download_to_file(file_obj, client=self, start=start, end=end)
        except AttributeError:
            blob = Blob.from_string(blob_or_uri)
            blob.download_to_file(file_obj, client=self, start=start, end=end)

    def list_blobs(
        self,
        bucket_or_name,
        max_results=None,
        page_token=None,
        prefix=None,
        delimiter=None,
        versions=None,
        projection="noAcl",
        fields=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """Return an iterator used to find blobs in the bucket.

        If :attr:`user_project` is set, bills the API request to that project.

        Args:
            bucket_or_name (Union[ \
                :class:`~google.cloud.storage.bucket.Bucket`, \
                 str, \
            ]):
                The bucket resource to pass or name to create.

            max_results (int):
                (Optional) The maximum number of blobs to return.

            page_token (str):
                (Optional) If present, return the next batch of blobs, using the
                value, which must correspond to the ``nextPageToken`` value
                returned in the previous response.  Deprecated: use the ``pages``
                property of the returned iterator instead of manually passing the
                token.

            prefix (str):
                (Optional) Prefix used to filter blobs.

            delimiter (str):
                (Optional) Delimiter, used with ``prefix`` to
                emulate hierarchy.

            versions (bool):
                (Optional) Whether object versions should be returned
                as separate blobs.

            projection (str):
                (Optional) If used, must be 'full' or 'noAcl'.
                Defaults to ``'noAcl'``. Specifies the set of
                properties to return.

            fields (str):
                (Optional) Selector specifying which fields to include
                in a partial response. Must be a list of fields. For
                example to get a partial response with just the next
                page token and the name and language of each blob returned:
                ``'items(name,contentLanguage),nextPageToken'``.
                See: https://cloud.google.com/storage/docs/json_api/v1/parameters#fields

            timeout (Optional[Union[float, Tuple[float, float]]]):
                The amount of time, in seconds, to wait for the server response.

                Can also be passed as a tuple (connect_timeout, read_timeout).
                See :meth:`requests.Session.request` documentation for details.

        Returns:
            Iterator of all :class:`~google.cloud.storage.blob.Blob`
            in this bucket matching the arguments.
        """
        bucket = self._bucket_arg_to_bucket(bucket_or_name)
        return bucket.list_blobs(
            max_results=max_results,
            page_token=page_token,
            prefix=prefix,
            delimiter=delimiter,
            versions=versions,
            projection=projection,
            fields=fields,
            client=self,
            timeout=timeout,
        )

    def list_buckets(
        self,
        max_results=None,
        page_token=None,
        prefix=None,
        projection="noAcl",
        fields=None,
        project=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """Get all buckets in the project associated to the client.

        This will not populate the list of blobs available in each
        bucket.

        .. literalinclude:: snippets.py
            :start-after: [START list_buckets]
            :end-before: [END list_buckets]

        This implements "storage.buckets.list".

        :type max_results: int
        :param max_results: (Optional) The maximum number of buckets to return.

        :type page_token: str
        :param page_token:
            (Optional) If present, return the next batch of buckets, using the
            value, which must correspond to the ``nextPageToken`` value
            returned in the previous response.  Deprecated: use the ``pages``
            property of the returned iterator instead of manually passing the
            token.

        :type prefix: str
        :param prefix: (Optional) Filter results to buckets whose names begin
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
        :param project: (Optional) The project whose buckets are to be listed.
                        If not passed, uses the project set on the client.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`~google.api_core.page_iterator.Iterator`
        :raises ValueError: if both ``project`` is ``None`` and the client's
                            project is also ``None``.
        :returns: Iterator of all :class:`~google.cloud.storage.bucket.Bucket`
                  belonging to this project.
        """
        if project is None:
            project = self.project

        if project is None:
            raise ValueError("Client project not set:  pass an explicit project.")

        extra_params = {"project": project}

        if prefix is not None:
            extra_params["prefix"] = prefix

        extra_params["projection"] = projection

        if fields is not None:
            extra_params["fields"] = fields

        api_request = functools.partial(self._connection.api_request, timeout=timeout)

        return page_iterator.HTTPIterator(
            client=self,
            api_request=api_request,
            path="/b",
            item_to_value=_item_to_bucket,
            page_token=page_token,
            max_results=max_results,
            extra_params=extra_params,
        )

    def create_hmac_key(
        self,
        service_account_email,
        project_id=None,
        user_project=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """Create an HMAC key for a service account.

        :type service_account_email: str
        :param service_account_email: e-mail address of the service account

        :type project_id: str
        :param project_id: (Optional) Explicit project ID for the key.
            Defaults to the client's project.

        :type user_project: str
        :param user_project: (Optional) This parameter is currently ignored.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype:
            Tuple[:class:`~google.cloud.storage.hmac_key.HMACKeyMetadata`, str]
        :returns: metadata for the created key, plus the bytes of the key's secret, which is an 40-character base64-encoded string.
        """
        if project_id is None:
            project_id = self.project

        path = "/projects/{}/hmacKeys".format(project_id)
        qs_params = {"serviceAccountEmail": service_account_email}

        if user_project is not None:
            qs_params["userProject"] = user_project

        api_response = self._connection.api_request(
            method="POST", path=path, query_params=qs_params, timeout=timeout
        )
        metadata = HMACKeyMetadata(self)
        metadata._properties = api_response["metadata"]
        secret = api_response["secret"]
        return metadata, secret

    def list_hmac_keys(
        self,
        max_results=None,
        service_account_email=None,
        show_deleted_keys=None,
        project_id=None,
        user_project=None,
        timeout=_DEFAULT_TIMEOUT,
    ):
        """List HMAC keys for a project.

        :type max_results: int
        :param max_results:
            (Optional) Max number of keys to return in a given page.

        :type service_account_email: str
        :param service_account_email:
            (Optional) Limit keys to those created by the given service account.

        :type show_deleted_keys: bool
        :param show_deleted_keys:
            (Optional) Included deleted keys in the list. Default is to
            exclude them.

        :type project_id: str
        :param project_id: (Optional) Explicit project ID for the key.
            Defaults to the client's project.

        :type user_project: str
        :param user_project: (Optional) This parameter is currently ignored.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype:
            Tuple[:class:`~google.cloud.storage.hmac_key.HMACKeyMetadata`, str]
        :returns: metadata for the created key, plus the bytes of the key's secret, which is an 40-character base64-encoded string.
        """
        if project_id is None:
            project_id = self.project

        path = "/projects/{}/hmacKeys".format(project_id)
        extra_params = {}

        if service_account_email is not None:
            extra_params["serviceAccountEmail"] = service_account_email

        if show_deleted_keys is not None:
            extra_params["showDeletedKeys"] = show_deleted_keys

        if user_project is not None:
            extra_params["userProject"] = user_project

        api_request = functools.partial(self._connection.api_request, timeout=timeout)

        return page_iterator.HTTPIterator(
            client=self,
            api_request=api_request,
            path=path,
            item_to_value=_item_to_hmac_key_metadata,
            max_results=max_results,
            extra_params=extra_params,
        )

    def get_hmac_key_metadata(
        self, access_id, project_id=None, user_project=None, timeout=_DEFAULT_TIMEOUT
    ):
        """Return a metadata instance for the given HMAC key.

        :type access_id: str
        :param access_id: Unique ID of an existing key.

        :type project_id: str
        :param project_id: (Optional) Project ID of an existing key.
            Defaults to client's project.

        :type timeout: float or tuple
        :param timeout: (Optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :type user_project: str
        :param user_project: (Optional) This parameter is currently ignored.
        """
        metadata = HMACKeyMetadata(self, access_id, project_id, user_project)
        metadata.reload(timeout=timeout)  # raises NotFound for missing key
        return metadata

    def generate_signed_post_policy_v4(
        self,
        bucket_name,
        blob_name,
        expiration,
        conditions=None,
        fields=None,
        credentials=None,
        virtual_hosted_style=False,
        bucket_bound_hostname=None,
        scheme=None,
        service_account_email=None,
        access_token=None,
    ):
        """Generate a V4 signed policy object.

        .. note::

            Assumes ``credentials`` implements the
            :class:`google.auth.credentials.Signing` interface. Also assumes
            ``credentials`` has a ``service_account_email`` property which
            identifies the credentials.

        Generated policy object allows user to upload objects with a POST request.

        :type bucket_name: str
        :param bucket_name: Bucket name.

        :type blob_name: str
        :param blob_name: Object name.

        :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
        :param expiration: Policy expiration time.

        :type conditions: list
        :param conditions: (Optional) List of POST policy conditions, which are
                           used to restrict what is allowed in the request.

        :type fields: dict
        :param fields: (Optional) Additional elements to include into request.

        :type credentials: :class:`google.auth.credentials.Signing`
        :param credentials: (Optional) Credentials object with an associated private
                            key to sign text.

        :type virtual_hosted_style: bool
        :param virtual_hosted_style: (Optional) If True, construct the URL relative to the bucket
                                     virtual hostname, e.g., '<bucket-name>.storage.googleapis.com'.

        :type bucket_bound_hostname: str
        :param bucket_bound_hostname:
            (Optional) If passed, construct the URL relative to the bucket-bound hostname.
            Value can be bare or with a scheme, e.g., 'example.com' or 'http://example.com'.
            See: https://cloud.google.com/storage/docs/request-endpoints#cname

        :type scheme: str
        :param scheme:
            (Optional) If ``bucket_bound_hostname`` is passed as a bare hostname, use
            this value as a scheme. ``https`` will work only when using a CDN.
            Defaults to ``"http"``.

        :type service_account_email: str
        :param service_account_email: (Optional) E-mail address of the service account.

        :type access_token: str
        :param access_token: (Optional) Access token for a service account.

        :rtype: dict
        :returns: Signed POST policy.

        Example:
            Generate signed POST policy and upload a file.

            >>> from google.cloud import storage
            >>> client = storage.Client()
            >>> policy = client.generate_signed_post_policy_v4(
                "bucket-name",
                "blob-name",
                expiration=datetime.datetime(2020, 3, 17),
                conditions=[
                    ["content-length-range", 0, 255]
                ],
                fields=[
                    "x-goog-meta-hello" => "world"
                ],
            )
            >>> with open("bucket-name", "rb") as f:
                files = {"file": ("bucket-name", f)}
                requests.post(policy["url"], data=policy["fields"], files=files)
        """
        credentials = self._credentials if credentials is None else credentials
        ensure_signed_credentials(credentials)

        # prepare policy conditions and fields
        timestamp, datestamp = get_v4_now_dtstamps()

        x_goog_credential = "{email}/{datestamp}/auto/storage/goog4_request".format(
            email=credentials.signer_email, datestamp=datestamp
        )
        required_conditions = [
            {"key": blob_name},
            {"x-goog-date": timestamp},
            {"x-goog-credential": x_goog_credential},
            {"x-goog-algorithm": "GOOG4-RSA-SHA256"},
        ]

        conditions = conditions or []
        policy_fields = {}
        for key, value in sorted((fields or {}).items()):
            if not key.startswith("x-ignore-"):
                policy_fields[key] = value
                conditions.append({key: value})

        conditions += required_conditions

        # calculate policy expiration time
        now = _NOW()
        if expiration is None:
            expiration = now + datetime.timedelta(hours=1)

        policy_expires = now + datetime.timedelta(
            seconds=get_expiration_seconds_v4(expiration)
        )

        # encode policy for signing
        policy = json.dumps(
            collections.OrderedDict(
                sorted(
                    {
                        "conditions": conditions,
                        "expiration": policy_expires.isoformat() + "Z",
                    }.items()
                )
            ),
            separators=(",", ":"),
        )
        str_to_sign = base64.b64encode(policy.encode("utf-8"))

        # sign the policy and get its cryptographic signature
        if access_token and service_account_email:
            signature = _sign_message(str_to_sign, access_token, service_account_email)
            signature_bytes = base64.b64decode(signature)
        else:
            signature_bytes = credentials.sign_bytes(str_to_sign)

        # get hexadecimal representation of the signature
        signature = binascii.hexlify(signature_bytes).decode("utf-8")

        policy_fields.update(
            {
                "key": blob_name,
                "x-goog-algorithm": "GOOG4-RSA-SHA256",
                "x-goog-credential": x_goog_credential,
                "x-goog-date": timestamp,
                "x-goog-signature": signature,
                "policy": str_to_sign,
            }
        )
        # designate URL
        if virtual_hosted_style:
            url = "https://{}.storage.googleapis.com/".format(bucket_name)

        elif bucket_bound_hostname:
            if ":" in bucket_bound_hostname:  # URL includes scheme
                url = bucket_bound_hostname

            else:  # scheme is given separately
                url = "{scheme}://{host}/".format(
                    scheme=scheme, host=bucket_bound_hostname
                )
        else:
            url = "https://storage.googleapis.com/{}/".format(bucket_name)

        return {"url": url, "fields": policy_fields}


def _item_to_bucket(iterator, item):
    """Convert a JSON bucket to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type item: dict
    :param item: An item to be converted to a bucket.

    :rtype: :class:`.Bucket`
    :returns: The next bucket in the page.
    """
    name = item.get("name")
    bucket = Bucket(iterator.client, name)
    bucket._set_properties(item)
    return bucket


def _item_to_hmac_key_metadata(iterator, item):
    """Convert a JSON key metadata resource to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that has retrieved the item.

    :type item: dict
    :param item: An item to be converted to a key metadata instance.

    :rtype: :class:`~google.cloud.storage.hmac_key.HMACKeyMetadata`
    :returns: The next key metadata instance in the page.
    """
    metadata = HMACKeyMetadata(iterator.client)
    metadata._properties = item
    return metadata
