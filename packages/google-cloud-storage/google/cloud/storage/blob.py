# Copyright 2014 Google LLC
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

# pylint: disable=too-many-lines

"""Create / interact with Google Cloud Storage blobs.

.. _API reference docs: https://cloud.google.com/storage/docs/\
                        json_api/v1/objects
.. _customer-supplied: https://cloud.google.com/storage/docs/\
                       encryption#customer-supplied
.. _google-resumable-media: https://googleapis.github.io/\
                            google-resumable-media-python/latest/\
                            google.resumable_media.requests.html
"""

import base64
import copy
import hashlib
from io import BytesIO
import mimetypes
import os
import time
import warnings

from six.moves.urllib.parse import parse_qsl
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import urlencode
from six.moves.urllib.parse import urlsplit
from six.moves.urllib.parse import urlunsplit

from google import resumable_media
from google.resumable_media.requests import ChunkedDownload
from google.resumable_media.requests import Download
from google.resumable_media.requests import RawDownload
from google.resumable_media.requests import RawChunkedDownload
from google.resumable_media.requests import MultipartUpload
from google.resumable_media.requests import ResumableUpload

from google.api_core.iam import Policy
from google.cloud import exceptions
from google.cloud._helpers import _bytes_to_unicode
from google.cloud._helpers import _rfc3339_to_datetime
from google.cloud._helpers import _to_bytes
from google.cloud.exceptions import NotFound
from google.cloud.storage._helpers import _get_storage_host
from google.cloud.storage._helpers import _PropertyMixin
from google.cloud.storage._helpers import _scalar_property
from google.cloud.storage._signing import generate_signed_url_v2
from google.cloud.storage._signing import generate_signed_url_v4
from google.cloud.storage.acl import ACL
from google.cloud.storage.acl import ObjectACL
from google.cloud.storage.constants import _DEFAULT_TIMEOUT
from google.cloud.storage.constants import ARCHIVE_STORAGE_CLASS
from google.cloud.storage.constants import COLDLINE_STORAGE_CLASS
from google.cloud.storage.constants import MULTI_REGIONAL_LEGACY_STORAGE_CLASS
from google.cloud.storage.constants import NEARLINE_STORAGE_CLASS
from google.cloud.storage.constants import REGIONAL_LEGACY_STORAGE_CLASS
from google.cloud.storage.constants import STANDARD_STORAGE_CLASS

_STORAGE_HOST = _get_storage_host()

_API_ACCESS_ENDPOINT = "https://storage.googleapis.com"
_DEFAULT_CONTENT_TYPE = u"application/octet-stream"
_DOWNLOAD_URL_TEMPLATE = _STORAGE_HOST + u"/download/storage/v1{path}?alt=media"
_BASE_UPLOAD_TEMPLATE = _STORAGE_HOST + u"/upload/storage/v1{bucket_path}/o?uploadType="
_MULTIPART_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u"multipart"
_RESUMABLE_URL_TEMPLATE = _BASE_UPLOAD_TEMPLATE + u"resumable"
# NOTE: "acl" is also writeable but we defer ACL management to
#       the classes in the google.cloud.storage.acl module.
_CONTENT_TYPE_FIELD = "contentType"
_WRITABLE_FIELDS = (
    "cacheControl",
    "contentDisposition",
    "contentEncoding",
    "contentLanguage",
    _CONTENT_TYPE_FIELD,
    "crc32c",
    "md5Hash",
    "metadata",
    "name",
    "storageClass",
)
_NUM_RETRIES_MESSAGE = (
    "`num_retries` has been deprecated and will be removed in a future "
    "release. The default behavior (when `num_retries` is not specified) when "
    "a transient error (e.g. 429 Too Many Requests or 500 Internal Server "
    "Error) occurs will be as follows: upload requests will be automatically "
    "retried. Subsequent retries will be sent after waiting 1, 2, 4, 8, etc. "
    "seconds (exponential backoff) until 10 minutes of wait time have "
    "elapsed. At that point, there will be no more attempts to retry."
)
_READ_LESS_THAN_SIZE = (
    "Size {:d} was specified but the file-like object only had " "{:d} bytes remaining."
)

_DEFAULT_CHUNKSIZE = 104857600  # 1024 * 1024 B * 100 = 100 MB
_MAX_MULTIPART_SIZE = 8388608  # 8 MB


class Blob(_PropertyMixin):
    """A wrapper around Cloud Storage's concept of an ``Object``.

    :type name: str
    :param name: The name of the blob.  This corresponds to the unique path of
                 the object in the bucket. If bytes, will be converted to a
                 unicode object. Blob / object names can contain any sequence
                 of valid unicode characters, of length 1-1024 bytes when
                 UTF-8 encoded.

    :type bucket: :class:`google.cloud.storage.bucket.Bucket`
    :param bucket: The bucket to which this blob belongs.

    :type chunk_size: int

    :param chunk_size: The size of a chunk of data whenever iterating (in
                       bytes). This must be a multiple of 256 KB per the API
                       specification.

    :type encryption_key: bytes
    :param encryption_key:
        Optional 32 byte encryption key for customer-supplied encryption.
        See https://cloud.google.com/storage/docs/encryption#customer-supplied.

    :type kms_key_name: str
    :param kms_key_name:
        Optional resource name of Cloud KMS key used to encrypt the blob's
        contents.
    """

    _chunk_size = None  # Default value for each instance.
    _CHUNK_SIZE_MULTIPLE = 256 * 1024
    """Number (256 KB, in bytes) that must divide the chunk size."""

    STORAGE_CLASSES = (
        STANDARD_STORAGE_CLASS,
        NEARLINE_STORAGE_CLASS,
        COLDLINE_STORAGE_CLASS,
        ARCHIVE_STORAGE_CLASS,
        MULTI_REGIONAL_LEGACY_STORAGE_CLASS,
        REGIONAL_LEGACY_STORAGE_CLASS,
    )
    """Allowed values for :attr:`storage_class`.

    See
    https://cloud.google.com/storage/docs/json_api/v1/objects#storageClass
    https://cloud.google.com/storage/docs/per-object-storage-class

    .. note::
       This list does not include 'DURABLE_REDUCED_AVAILABILITY', which
       is only documented for buckets (and deprecated).
    """

    def __init__(
        self,
        name,
        bucket,
        chunk_size=None,
        encryption_key=None,
        kms_key_name=None,
        generation=None,
    ):
        name = _bytes_to_unicode(name)
        super(Blob, self).__init__(name=name)

        self.chunk_size = chunk_size  # Check that setter accepts value.
        self._bucket = bucket
        self._acl = ObjectACL(self)
        if encryption_key is not None and kms_key_name is not None:
            raise ValueError(
                "Pass at most one of 'encryption_key' " "and 'kms_key_name'"
            )

        self._encryption_key = encryption_key

        if kms_key_name is not None:
            self._properties["kmsKeyName"] = kms_key_name

        if generation is not None:
            self._properties["generation"] = generation

    @property
    def bucket(self):
        """Bucket which contains the object.

        :rtype: :class:`~google.cloud.storage.bucket.Bucket`
        :returns: The object's bucket.
        """
        return self._bucket

    @property
    def chunk_size(self):
        """Get the blob's default chunk size.

        :rtype: int or ``NoneType``
        :returns: The current blob's chunk size, if it is set.
        """
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        """Set the blob's default chunk size.

        :type value: int
        :param value: (Optional) The current blob's chunk size, if it is set.

        :raises: :class:`ValueError` if ``value`` is not ``None`` and is not a
                 multiple of 256 KB.
        """
        if value is not None and value > 0 and value % self._CHUNK_SIZE_MULTIPLE != 0:
            raise ValueError(
                "Chunk size must be a multiple of %d." % (self._CHUNK_SIZE_MULTIPLE,)
            )
        self._chunk_size = value

    @staticmethod
    def path_helper(bucket_path, blob_name):
        """Relative URL path for a blob.

        :type bucket_path: str
        :param bucket_path: The URL path for a bucket.

        :type blob_name: str
        :param blob_name: The name of the blob.

        :rtype: str
        :returns: The relative URL path for ``blob_name``.
        """
        return bucket_path + "/o/" + _quote(blob_name)

    @property
    def acl(self):
        """Create our ACL on demand."""
        return self._acl

    def __repr__(self):
        if self.bucket:
            bucket_name = self.bucket.name
        else:
            bucket_name = None

        return "<Blob: %s, %s, %s>" % (bucket_name, self.name, self.generation)

    @property
    def path(self):
        """Getter property for the URL path to this Blob.

        :rtype: str
        :returns: The URL path to this Blob.
        """
        if not self.name:
            raise ValueError("Cannot determine path without a blob name.")

        return self.path_helper(self.bucket.path, self.name)

    @property
    def client(self):
        """The client bound to this blob."""
        return self.bucket.client

    @property
    def user_project(self):
        """Project ID billed for API requests made via this blob.

        Derived from bucket's value.

        :rtype: str
        """
        return self.bucket.user_project

    def _encryption_headers(self):
        """Return any encryption headers needed to fetch the object.

        :rtype: List(Tuple(str, str))
        :returns: a list of tuples to be passed as headers.
        """
        return _get_encryption_headers(self._encryption_key)

    @property
    def _query_params(self):
        """Default query parameters."""
        params = {}
        if self.generation is not None:
            params["generation"] = self.generation
        if self.user_project is not None:
            params["userProject"] = self.user_project
        return params

    @property
    def public_url(self):
        """The public URL for this blob.

        Use :meth:`make_public` to enable anonymous access via the returned
        URL.

        :rtype: `string`
        :returns: The public URL for this blob.
        """
        return "{storage_base_url}/{bucket_name}/{quoted_name}".format(
            storage_base_url=_API_ACCESS_ENDPOINT,
            bucket_name=self.bucket.name,
            quoted_name=_quote(self.name, safe=b"/~"),
        )

    @classmethod
    def from_string(cls, uri, client=None):
        """Get a constructor for blob object by URI.

         :type uri: str
         :param uri: The blob uri pass to get blob object.

         :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
         :param client: Optional. The client to use.

         :rtype: :class:`google.cloud.storage.blob.Blob`
         :returns: The blob object created.

         Example:
            Get a constructor for blob object by URI..

            >>> from google.cloud import storage
            >>> from google.cloud.storage.blob import Blob
            >>> client = storage.Client()
            >>> blob = Blob.from_string("gs://bucket/object")
         """
        from google.cloud.storage.bucket import Bucket

        scheme, netloc, path, query, frag = urlsplit(uri)
        if scheme != "gs":
            raise ValueError("URI scheme must be gs")

        bucket = Bucket(client, name=netloc)
        return cls(path[1:], bucket)

    def generate_signed_url(
        self,
        expiration=None,
        api_access_endpoint=_API_ACCESS_ENDPOINT,
        method="GET",
        content_md5=None,
        content_type=None,
        response_disposition=None,
        response_type=None,
        generation=None,
        headers=None,
        query_parameters=None,
        client=None,
        credentials=None,
        version=None,
        service_account_email=None,
        access_token=None,
    ):
        """Generates a signed URL for this blob.

        .. note::

            If you are on Google Compute Engine, you can't generate a signed
            URL using GCE service account. Follow `Issue 50`_ for updates on
            this. If you'd like to be able to generate a signed URL from GCE,
            you can use a standard service account from a JSON file rather
            than a GCE service account.

        .. _Issue 50: https://github.com/GoogleCloudPlatform/\
                      google-auth-library-python/issues/50

        If you have a blob that you want to allow access to for a set
        amount of time, you can use this method to generate a URL that
        is only valid within a certain time period.

        This is particularly useful if you don't want publicly
        accessible blobs, but don't want to require users to explicitly
        log in.

        :type expiration: Union[Integer, datetime.datetime, datetime.timedelta]
        :param expiration: Point in time when the signed URL should expire.

        :type api_access_endpoint: str
        :param api_access_endpoint: Optional URI base.

        :type method: str
        :param method: The HTTP verb that will be used when requesting the URL.

        :type content_md5: str
        :param content_md5: (Optional) The MD5 hash of the object referenced by
                            ``resource``.

        :type content_type: str
        :param content_type: (Optional) The content type of the object
                             referenced by ``resource``.

        :type response_disposition: str
        :param response_disposition: (Optional) Content disposition of
                                     responses to requests for the signed URL.
                                     For example, to enable the signed URL
                                     to initiate a file of ``blog.png``, use
                                     the value
                                     ``'attachment; filename=blob.png'``.

        :type response_type: str
        :param response_type: (Optional) Content type of responses to requests
                              for the signed URL. Ignored if content_type is
                              set on object/blob metadata.

        :type generation: str
        :param generation: (Optional) A value that indicates which generation
                           of the resource to fetch.

        :type headers: dict
        :param headers:
            (Optional) Additional HTTP headers to be included as part of the
            signed URLs.  See:
            https://cloud.google.com/storage/docs/xml-api/reference-headers
            Requests using the signed URL *must* pass the specified header
            (name and value) with each request for the URL.

        :type query_parameters: dict
        :param query_parameters:
            (Optional) Additional query paramtersto be included as part of the
            signed URLs.  See:
            https://cloud.google.com/storage/docs/xml-api/reference-headers#query

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.


        :type credentials: :class:`google.auth.credentials.Credentials` or
                           :class:`NoneType`
        :param credentials: The authorization credentials to attach to requests.
                            These credentials identify this application to the service.
                            If none are specified, the client will attempt to ascertain
                            the credentials from the environment.

        :type version: str
        :param version: (Optional) The version of signed credential to create.
                        Must be one of 'v2' | 'v4'.

        :type service_account_email: str
        :param service_account_email: (Optional) E-mail address of the service account.

        :type access_token: str
        :param access_token: (Optional) Access token for a service account.

        :raises: :exc:`ValueError` when version is invalid.
        :raises: :exc:`TypeError` when expiration is not a valid type.
        :raises: :exc:`AttributeError` if credentials is not an instance
                of :class:`google.auth.credentials.Signing`.

        :rtype: str
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """
        if version is None:
            version = "v2"
        elif version not in ("v2", "v4"):
            raise ValueError("'version' must be either 'v2' or 'v4'")

        quoted_name = _quote(self.name, safe=b"/~")
        resource = "/{bucket_name}/{quoted_name}".format(
            bucket_name=self.bucket.name, quoted_name=quoted_name
        )

        if credentials is None:
            client = self._require_client(client)
            credentials = client._credentials

        if version == "v2":
            helper = generate_signed_url_v2
        else:
            helper = generate_signed_url_v4

        if self._encryption_key is not None:
            encryption_headers = _get_encryption_headers(self._encryption_key)
            if headers is None:
                headers = {}
            if version == "v2":
                # See: https://cloud.google.com/storage/docs/access-control/signed-urls-v2#about-canonical-extension-headers
                v2_copy_only = "X-Goog-Encryption-Algorithm"
                headers[v2_copy_only] = encryption_headers[v2_copy_only]
            else:
                headers.update(encryption_headers)

        return helper(
            credentials,
            resource=resource,
            expiration=expiration,
            api_access_endpoint=api_access_endpoint,
            method=method.upper(),
            content_md5=content_md5,
            content_type=content_type,
            response_type=response_type,
            response_disposition=response_disposition,
            generation=generation,
            headers=headers,
            query_parameters=query_parameters,
            service_account_email=service_account_email,
            access_token=access_token,
        )

    def exists(self, client=None, timeout=_DEFAULT_TIMEOUT):
        """Determines whether or not this blob exists.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: bool
        :returns: True if the blob exists in Cloud Storage.
        """
        client = self._require_client(client)
        # We only need the status code (200 or not) so we seek to
        # minimize the returned payload.
        query_params = self._query_params
        query_params["fields"] = "name"

        try:
            # We intentionally pass `_target_object=None` since fields=name
            # would limit the local properties.
            client._connection.api_request(
                method="GET",
                path=self.path,
                query_params=query_params,
                _target_object=None,
                timeout=timeout,
            )
            # NOTE: This will not fail immediately in a batch. However, when
            #       Batch.finish() is called, the resulting `NotFound` will be
            #       raised.
            return True
        except NotFound:
            return False

    def delete(self, client=None, timeout=_DEFAULT_TIMEOUT):
        """Deletes a blob from Cloud Storage.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :raises: :class:`google.cloud.exceptions.NotFound`
                 (propagated from
                 :meth:`google.cloud.storage.bucket.Bucket.delete_blob`).
        """
        self.bucket.delete_blob(
            self.name, client=client, generation=self.generation, timeout=timeout
        )

    def _get_transport(self, client):
        """Return the client's transport.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :rtype transport:
            :class:`~google.auth.transport.requests.AuthorizedSession`
        :returns: The transport (with credentials) that will
                  make authenticated requests.
        """
        client = self._require_client(client)
        return client._http

    def _get_download_url(self):
        """Get the download URL for the current blob.

        If the ``media_link`` has been loaded, it will be used, otherwise
        the URL will be constructed from the current blob's path (and possibly
        generation) to avoid a round trip.

        :rtype: str
        :returns: The download URL for the current blob.
        """
        name_value_pairs = []
        if self.media_link is None:
            base_url = _DOWNLOAD_URL_TEMPLATE.format(path=self.path)
            if self.generation is not None:
                name_value_pairs.append(("generation", "{:d}".format(self.generation)))
        else:
            base_url = self.media_link

        if self.user_project is not None:
            name_value_pairs.append(("userProject", self.user_project))

        return _add_query_parameters(base_url, name_value_pairs)

    def _do_download(
        self,
        transport,
        file_obj,
        download_url,
        headers,
        start=None,
        end=None,
        raw_download=False,
    ):
        """Perform a download without any error handling.

        This is intended to be called by :meth:`download_to_file` so it can
        be wrapped with error handling / remapping.

        :type transport:
            :class:`~google.auth.transport.requests.AuthorizedSession`
        :param transport: The transport (with credentials) that will
                          make authenticated requests.

        :type file_obj: file
        :param file_obj: A file handle to which to write the blob's data.

        :type download_url: str
        :param download_url: The URL where the media can be accessed.

        :type headers: dict
        :param headers: Optional headers to be sent with the request(s).

        :type start: int
        :param start: Optional, the first byte in a range to be downloaded.

        :type end: int
        :param end: Optional, The last byte in a range to be downloaded.

        :type raw_download: bool
        :param raw_download:
            Optional, If true, download the object without any expansion.
        """
        if self.chunk_size is None:
            if raw_download:
                klass = RawDownload
            else:
                klass = Download

            download = klass(
                download_url, stream=file_obj, headers=headers, start=start, end=end
            )
            download.consume(transport)

        else:

            if raw_download:
                klass = RawChunkedDownload
            else:
                klass = ChunkedDownload

            download = klass(
                download_url,
                self.chunk_size,
                file_obj,
                headers=headers,
                start=start if start else 0,
                end=end,
            )

            while not download.finished:
                download.consume_next_chunk(transport)

    def download_to_file(
        self, file_obj, client=None, start=None, end=None, raw_download=False
    ):
        """Download the contents of this blob into a file-like object.

        .. note::

           If the server-set property, :attr:`media_link`, is not yet
           initialized, makes an additional API request to load it.

        Downloading a file that has been encrypted with a `customer-supplied`_
        encryption key:

         .. literalinclude:: snippets.py
            :start-after: [START download_to_file]
            :end-before: [END download_to_file]
            :dedent: 4

        The ``encryption_key`` should be a str or bytes with a length of at
        least 32.

        For more fine-grained control over the download process, check out
        `google-resumable-media`_. For example, this library allows
        downloading **parts** of a blob rather than the whole thing.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type file_obj: file
        :param file_obj: A file handle to which to write the blob's data.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type start: int
        :param start: Optional, the first byte in a range to be downloaded.

        :type end: int
        :param end: Optional, The last byte in a range to be downloaded.

        :type raw_download: bool
        :param raw_download:
            Optional, If true, download the object without any expansion.

        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        download_url = self._get_download_url()
        headers = _get_encryption_headers(self._encryption_key)
        headers["accept-encoding"] = "gzip"

        transport = self._get_transport(client)
        try:
            self._do_download(
                transport, file_obj, download_url, headers, start, end, raw_download
            )
        except resumable_media.InvalidResponse as exc:
            _raise_from_invalid_response(exc)

    def download_to_filename(
        self, filename, client=None, start=None, end=None, raw_download=False
    ):
        """Download the contents of this blob into a named file.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type filename: str
        :param filename: A filename to be passed to ``open``.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type start: int
        :param start: Optional, the first byte in a range to be downloaded.

        :type end: int
        :param end: Optional, The last byte in a range to be downloaded.

        :type raw_download: bool
        :param raw_download:
            Optional, If true, download the object without any expansion.

        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        try:
            with open(filename, "wb") as file_obj:
                self.download_to_file(
                    file_obj,
                    client=client,
                    start=start,
                    end=end,
                    raw_download=raw_download,
                )
        except resumable_media.DataCorruption:
            # Delete the corrupt downloaded file.
            os.remove(filename)
            raise

        updated = self.updated
        if updated is not None:
            mtime = time.mktime(updated.timetuple())
            os.utime(file_obj.name, (mtime, mtime))

    def download_as_string(self, client=None, start=None, end=None, raw_download=False):
        """Download the contents of this blob as a bytes object.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type start: int
        :param start: Optional, the first byte in a range to be downloaded.

        :type end: int
        :param end: Optional, The last byte in a range to be downloaded.

        :type raw_download: bool
        :param raw_download:
            Optional, If true, download the object without any expansion.

        :rtype: bytes
        :returns: The data stored in this blob.
        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        string_buffer = BytesIO()
        self.download_to_file(
            string_buffer,
            client=client,
            start=start,
            end=end,
            raw_download=raw_download,
        )
        return string_buffer.getvalue()

    def _get_content_type(self, content_type, filename=None):
        """Determine the content type from the current object.

        The return value will be determined in order of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        :type content_type: str
        :param content_type: (Optional) type of content.

        :type filename: str
        :param filename: (Optional) The name of the file where the content
                         is stored.

        :rtype: str
        :returns: Type of content gathered from the object.
        """
        if content_type is None:
            content_type = self.content_type

        if content_type is None and filename is not None:
            content_type, _ = mimetypes.guess_type(filename)

        if content_type is None:
            content_type = _DEFAULT_CONTENT_TYPE

        return content_type

    def _get_writable_metadata(self):
        """Get the object / blob metadata which is writable.

        This is intended to be used when creating a new object / blob.

        See the `API reference docs`_ for more information, the fields
        marked as writable are:

        * ``acl``
        * ``cacheControl``
        * ``contentDisposition``
        * ``contentEncoding``
        * ``contentLanguage``
        * ``contentType``
        * ``crc32c``
        * ``md5Hash``
        * ``metadata``
        * ``name``
        * ``storageClass``

        For now, we don't support ``acl``, access control lists should be
        managed directly through :class:`ObjectACL` methods.
        """
        # NOTE: This assumes `self.name` is unicode.
        object_metadata = {"name": self.name}
        for key in self._changes:
            if key in _WRITABLE_FIELDS:
                object_metadata[key] = self._properties[key]

        return object_metadata

    def _get_upload_arguments(self, content_type):
        """Get required arguments for performing an upload.

        The content type returned will be determined in order of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        :type content_type: str
        :param content_type: Type of content being uploaded (or :data:`None`).

        :rtype: tuple
        :returns: A triple of

                  * A header dictionary
                  * An object metadata dictionary
                  * The ``content_type`` as a string (according to precedence)
        """
        headers = _get_encryption_headers(self._encryption_key)
        object_metadata = self._get_writable_metadata()
        content_type = self._get_content_type(content_type)
        return headers, object_metadata, content_type

    def _do_multipart_upload(
        self, client, stream, content_type, size, num_retries, predefined_acl
    ):
        """Perform a multipart upload.

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type content_type: str
        :param content_type: Type of content being uploaded (or :data:`None`).

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list

        :rtype: :class:`~requests.Response`
        :returns: The "200 OK" response object returned after the multipart
                  upload request.
        :raises: :exc:`ValueError` if ``size`` is not :data:`None` but the
                 ``stream`` has fewer than ``size`` bytes remaining.
        """
        if size is None:
            data = stream.read()
        else:
            data = stream.read(size)
            if len(data) < size:
                msg = _READ_LESS_THAN_SIZE.format(size, len(data))
                raise ValueError(msg)

        transport = self._get_transport(client)
        info = self._get_upload_arguments(content_type)
        headers, object_metadata, content_type = info

        base_url = _MULTIPART_URL_TEMPLATE.format(bucket_path=self.bucket.path)
        name_value_pairs = []

        if self.user_project is not None:
            name_value_pairs.append(("userProject", self.user_project))

        if self.kms_key_name is not None:
            name_value_pairs.append(("kmsKeyName", self.kms_key_name))

        if predefined_acl is not None:
            name_value_pairs.append(("predefinedAcl", predefined_acl))

        upload_url = _add_query_parameters(base_url, name_value_pairs)
        upload = MultipartUpload(upload_url, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries
            )

        response = upload.transmit(transport, data, object_metadata, content_type)

        return response

    def _initiate_resumable_upload(
        self,
        client,
        stream,
        content_type,
        size,
        num_retries,
        predefined_acl=None,
        extra_headers=None,
        chunk_size=None,
    ):
        """Initiate a resumable upload.

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type content_type: str
        :param content_type: Type of content being uploaded (or :data:`None`).

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :type extra_headers: dict
        :param extra_headers: (Optional) Extra headers to add to standard
                              headers.

        :type chunk_size: int
        :param chunk_size:
            (Optional) Chunk size to use when creating a
            :class:`~google.resumable_media.requests.ResumableUpload`.
            If not passed, will fall back to the chunk size on the
            current blob.

        :rtype: tuple
        :returns:
            Pair of

            * The :class:`~google.resumable_media.requests.ResumableUpload`
              that was created
            * The ``transport`` used to initiate the upload.
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
            if chunk_size is None:
                chunk_size = _DEFAULT_CHUNKSIZE

        transport = self._get_transport(client)
        info = self._get_upload_arguments(content_type)
        headers, object_metadata, content_type = info
        if extra_headers is not None:
            headers.update(extra_headers)

        base_url = _RESUMABLE_URL_TEMPLATE.format(bucket_path=self.bucket.path)
        name_value_pairs = []

        if self.user_project is not None:
            name_value_pairs.append(("userProject", self.user_project))

        if self.kms_key_name is not None:
            name_value_pairs.append(("kmsKeyName", self.kms_key_name))

        if predefined_acl is not None:
            name_value_pairs.append(("predefinedAcl", predefined_acl))

        upload_url = _add_query_parameters(base_url, name_value_pairs)
        upload = ResumableUpload(upload_url, chunk_size, headers=headers)

        if num_retries is not None:
            upload._retry_strategy = resumable_media.RetryStrategy(
                max_retries=num_retries
            )

        upload.initiate(
            transport,
            stream,
            object_metadata,
            content_type,
            total_bytes=size,
            stream_final=False,
        )

        return upload, transport

    def _do_resumable_upload(
        self, client, stream, content_type, size, num_retries, predefined_acl
    ):
        """Perform a resumable upload.

        Assumes ``chunk_size`` is not :data:`None` on the current blob.

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type content_type: str
        :param content_type: Type of content being uploaded (or :data:`None`).

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list

        :rtype: :class:`~requests.Response`
        :returns: The "200 OK" response object returned after the final chunk
                  is uploaded.
        """
        upload, transport = self._initiate_resumable_upload(
            client,
            stream,
            content_type,
            size,
            num_retries,
            predefined_acl=predefined_acl,
        )

        while not upload.finished:
            response = upload.transmit_next_chunk(transport)

        return response

    def _do_upload(
        self, client, stream, content_type, size, num_retries, predefined_acl
    ):
        """Determine an upload strategy and then perform the upload.

        If the size of the data to be uploaded exceeds 5 MB a resumable media
        request will be used, otherwise the content and the metadata will be
        uploaded in a single multipart upload request.

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type stream: IO[bytes]
        :param stream: A bytes IO object open for reading.

        :type content_type: str
        :param content_type: Type of content being uploaded (or :data:`None`).

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``stream``). If not provided, the upload will be
                     concluded once ``stream`` is exhausted (or :data:`None`).

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list

        :rtype: dict
        :returns: The parsed JSON from the "200 OK" response. This will be the
                  **only** response in the multipart case and it will be the
                  **final** response in the resumable case.
        """
        if size is not None and size <= _MAX_MULTIPART_SIZE:
            response = self._do_multipart_upload(
                client, stream, content_type, size, num_retries, predefined_acl
            )
        else:
            response = self._do_resumable_upload(
                client, stream, content_type, size, num_retries, predefined_acl
            )

        return response.json()

    def upload_from_file(
        self,
        file_obj,
        rewind=False,
        size=None,
        content_type=None,
        num_retries=None,
        client=None,
        predefined_acl=None,
    ):
        """Upload the contents of this blob from a file-like object.

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning`_ and `lifecycle`_ API documents
           for details.

        Uploading a file with a `customer-supplied`_ encryption key:

        .. literalinclude:: snippets.py
            :start-after: [START upload_from_file]
            :end-before: [END upload_from_file]
            :dedent: 4

        The ``encryption_key`` should be a str or bytes with a length of at
        least 32.

        For more fine-grained over the upload process, check out
        `google-resumable-media`_.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       writing the file to Cloud Storage.

        :type size: int
        :param size: The number of bytes to be uploaded (which will be read
                     from ``file_obj``). If not provided, the upload will be
                     concluded once ``file_obj`` is exhausted.

        :type content_type: str
        :param content_type: Optional type of content being uploaded.

        :type num_retries: int
        :param num_retries: Number of upload retries. (Deprecated: This
                            argument will be removed in a future release.)

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list

        :raises: :class:`~google.cloud.exceptions.GoogleCloudError`
                 if the upload response returns an error status.

        .. _object versioning: https://cloud.google.com/storage/\
                               docs/object-versioning
        .. _lifecycle: https://cloud.google.com/storage/docs/lifecycle
        """
        if num_retries is not None:
            warnings.warn(_NUM_RETRIES_MESSAGE, DeprecationWarning, stacklevel=2)

        _maybe_rewind(file_obj, rewind=rewind)
        predefined_acl = ACL.validate_predefined(predefined_acl)

        try:
            created_json = self._do_upload(
                client, file_obj, content_type, size, num_retries, predefined_acl
            )
            self._set_properties(created_json)
        except resumable_media.InvalidResponse as exc:
            _raise_from_invalid_response(exc)

    def upload_from_filename(
        self, filename, content_type=None, client=None, predefined_acl=None
    ):
        """Upload this blob's contents from the content of a named file.

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The value given by ``mimetypes.guess_type``
        - The default value ('application/octet-stream')

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type filename: str
        :param filename: The path to the file.

        :type content_type: str
        :param content_type: Optional type of content being uploaded.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list
        """
        content_type = self._get_content_type(content_type, filename=filename)

        with open(filename, "rb") as file_obj:
            total_bytes = os.fstat(file_obj.fileno()).st_size
            self.upload_from_file(
                file_obj,
                content_type=content_type,
                client=client,
                size=total_bytes,
                predefined_acl=predefined_acl,
            )

    def upload_from_string(
        self, data, content_type="text/plain", client=None, predefined_acl=None
    ):
        """Upload contents of this blob from the provided string.

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type data: bytes or str
        :param data: The data to store in this blob.  If the value is
                     text, it will be encoded as UTF-8.

        :type content_type: str
        :param content_type: Optional type of content being uploaded. Defaults
                             to ``'text/plain'``.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type predefined_acl: str
        :param predefined_acl: (Optional) predefined access control list
        """
        data = _to_bytes(data, encoding="utf-8")
        string_buffer = BytesIO(data)
        self.upload_from_file(
            file_obj=string_buffer,
            size=len(data),
            content_type=content_type,
            client=client,
            predefined_acl=predefined_acl,
        )

    def create_resumable_upload_session(
        self, content_type=None, size=None, origin=None, client=None
    ):
        """Create a resumable upload session.

        Resumable upload sessions allow you to start an upload session from
        one client and complete the session in another. This method is called
        by the initiator to set the metadata and limits. The initiator then
        passes the session URL to the client that will upload the binary data.
        The client performs a PUT request on the session URL to complete the
        upload. This process allows untrusted clients to upload to an
        access-controlled bucket. For more details, see the
        `documentation on signed URLs`_.

        .. _documentation on signed URLs:
            https://cloud.google.com/storage/\
            docs/access-control/signed-urls#signing-resumable

        The content type of the upload will be determined in order
        of precedence:

        - The value passed in to this method (if not :data:`None`)
        - The value stored on the current blob
        - The default value ('application/octet-stream')

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        If :attr:`encryption_key` is set, the blob will be encrypted with
        a `customer-supplied`_ encryption key.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type size: int
        :param size: (Optional). The maximum number of bytes that can be
                     uploaded using this session. If the size is not known
                     when creating the session, this should be left blank.

        :type content_type: str
        :param content_type: (Optional) Type of content being uploaded.

        :type origin: str
        :param origin: (Optional) If set, the upload can only be completed
                       by a user-agent that uploads from the given origin. This
                       can be useful when passing the session to a web client.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :rtype: str
        :returns: The resumable upload session URL. The upload can be
                  completed by making an HTTP PUT request with the
                  file's contents.

        :raises: :class:`google.cloud.exceptions.GoogleCloudError`
                 if the session creation response returns an error status.
        """
        extra_headers = {}
        if origin is not None:
            # This header is specifically for client-side uploads, it
            # determines the origins allowed for CORS.
            extra_headers["Origin"] = origin

        try:
            dummy_stream = BytesIO(b"")
            # Send a fake the chunk size which we **know** will be acceptable
            # to the `ResumableUpload` constructor. The chunk size only
            # matters when **sending** bytes to an upload.
            upload, _ = self._initiate_resumable_upload(
                client,
                dummy_stream,
                content_type,
                size,
                None,
                predefined_acl=None,
                extra_headers=extra_headers,
                chunk_size=self._CHUNK_SIZE_MULTIPLE,
            )

            return upload.resumable_url
        except resumable_media.InvalidResponse as exc:
            _raise_from_invalid_response(exc)

    def get_iam_policy(
        self, client=None, requested_policy_version=None, timeout=_DEFAULT_TIMEOUT
    ):
        """Retrieve the IAM policy for the object.

        .. note:

           Blob- / object-level IAM support does not yet exist and methods
           currently call an internal ACL backend not providing any utility
           beyond the blob's :attr:`acl` at this time. The API may be enhanced
           in the future and is currently undocumented. Use :attr:`acl` for
           managing object access control.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current object's bucket.

        :type requested_policy_version: int or ``NoneType``
        :param requested_policy_version: Optional. The version of IAM policies to request.
                                         If a policy with a condition is requested without
                                         setting this, the server will return an error.
                                         This must be set to a value of 3 to retrieve IAM
                                         policies containing conditions. This is to prevent
                                         client code that isn't aware of IAM conditions from
                                         interpreting and modifying policies incorrectly.
                                         The service might return a policy with version lower
                                         than the one that was requested, based on the
                                         feature syntax in the policy fetched.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`google.api_core.iam.Policy`
        :returns: the policy instance, based on the resource returned from
                  the ``getIamPolicy`` API request.
        """
        client = self._require_client(client)

        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        if requested_policy_version is not None:
            query_params["optionsRequestedPolicyVersion"] = requested_policy_version

        info = client._connection.api_request(
            method="GET",
            path="%s/iam" % (self.path,),
            query_params=query_params,
            _target_object=None,
            timeout=timeout,
        )
        return Policy.from_api_repr(info)

    def set_iam_policy(self, policy, client=None, timeout=_DEFAULT_TIMEOUT):
        """Update the IAM policy for the bucket.

        .. note:

           Blob- / object-level IAM support does not yet exist and methods
           currently call an internal ACL backend not providing any utility
           beyond the blob's :attr:`acl` at this time. The API may be enhanced
           in the future and is currently undocumented. Use :attr:`acl` for
           managing object access control.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type policy: :class:`google.api_core.iam.Policy`
        :param policy: policy instance used to update bucket's IAM policy.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: :class:`google.api_core.iam.Policy`
        :returns: the policy instance, based on the resource returned from
                  the ``setIamPolicy`` API request.
        """
        client = self._require_client(client)

        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        resource = policy.to_api_repr()
        resource["resourceId"] = self.path
        info = client._connection.api_request(
            method="PUT",
            path="%s/iam" % (self.path,),
            query_params=query_params,
            data=resource,
            _target_object=None,
            timeout=timeout,
        )
        return Policy.from_api_repr(info)

    def test_iam_permissions(self, permissions, client=None, timeout=_DEFAULT_TIMEOUT):
        """API call:  test permissions

        .. note:

           Blob- / object-level IAM support does not yet exist and methods
           currently call an internal ACL backend not providing any utility
           beyond the blob's :attr:`acl` at this time. The API may be enhanced
           in the future and is currently undocumented. Use :attr:`acl` for
           managing object access control.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type permissions: list of string
        :param permissions: the permissions to check

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the current bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: list of string
        :returns: the permissions returned by the ``testIamPermissions`` API
                  request.
        """
        client = self._require_client(client)
        query_params = {"permissions": permissions}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        path = "%s/iam/testPermissions" % (self.path,)
        resp = client._connection.api_request(
            method="GET", path=path, query_params=query_params, timeout=timeout
        )

        return resp.get("permissions", [])

    def make_public(self, client=None):
        """Update blob's ACL, granting read access to anonymous users.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        """
        self.acl.all().grant_read()
        self.acl.save(client=client)

    def make_private(self, client=None):
        """Update blob's ACL, revoking read access for anonymous users.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        """
        self.acl.all().revoke_read()
        self.acl.save(client=client)

    def compose(self, sources, client=None, timeout=_DEFAULT_TIMEOUT):
        """Concatenate source blobs into this one.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type sources: list of :class:`Blob`
        :param sources: blobs whose contents will be composed into this blob.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.
        """
        client = self._require_client(client)
        query_params = {}

        if self.user_project is not None:
            query_params["userProject"] = self.user_project

        request = {
            "sourceObjects": [{"name": source.name} for source in sources],
            "destination": self._properties.copy(),
        }
        api_response = client._connection.api_request(
            method="POST",
            path=self.path + "/compose",
            query_params=query_params,
            data=request,
            _target_object=self,
            timeout=timeout,
        )
        self._set_properties(api_response)

    def rewrite(self, source, token=None, client=None, timeout=_DEFAULT_TIMEOUT):
        """Rewrite source blob into this one.

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type source: :class:`Blob`
        :param source: blob whose contents will be rewritten into this blob.

        :type token: str
        :param token: Optional. Token returned from an earlier, not-completed
                       call to rewrite the same source blob.  If passed,
                       result will include updated status, total bytes written.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :type timeout: float or tuple
        :param timeout: (optional) The amount of time, in seconds, to wait
            for the server response.

            Can also be passed as a tuple (connect_timeout, read_timeout).
            See :meth:`requests.Session.request` documentation for details.

        :rtype: tuple
        :returns: ``(token, bytes_rewritten, total_bytes)``, where ``token``
                  is a rewrite token (``None`` if the rewrite is complete),
                  ``bytes_rewritten`` is the number of bytes rewritten so far,
                  and ``total_bytes`` is the total number of bytes to be
                  rewritten.
        """
        client = self._require_client(client)
        headers = _get_encryption_headers(self._encryption_key)
        headers.update(_get_encryption_headers(source._encryption_key, source=True))

        query_params = self._query_params
        if "generation" in query_params:
            del query_params["generation"]

        if token:
            query_params["rewriteToken"] = token

        if source.generation:
            query_params["sourceGeneration"] = source.generation

        if self.kms_key_name is not None:
            query_params["destinationKmsKeyName"] = self.kms_key_name

        api_response = client._connection.api_request(
            method="POST",
            path=source.path + "/rewriteTo" + self.path,
            query_params=query_params,
            data=self._properties,
            headers=headers,
            _target_object=self,
            timeout=timeout,
        )
        rewritten = int(api_response["totalBytesRewritten"])
        size = int(api_response["objectSize"])

        # The resource key is set if and only if the API response is
        # completely done. Additionally, there is no rewrite token to return
        # in this case.
        if api_response["done"]:
            self._set_properties(api_response["resource"])
            return None, rewritten, size

        return api_response["rewriteToken"], rewritten, size

    def update_storage_class(self, new_class, client=None):
        """Update blob's storage class via a rewrite-in-place. This helper will
        wait for the rewrite to complete before returning, so it may take some
        time for large files.

        See
        https://cloud.google.com/storage/docs/per-object-storage-class

        If :attr:`user_project` is set on the bucket, bills the API request
        to that project.

        :type new_class: str
        :param new_class:
            new storage class for the object.   One of:
            :attr:`~google.cloud.storage.constants.NEARLINE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.COLDLINE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.ARCHIVE_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.STANDARD_STORAGE_CLASS`,
            :attr:`~google.cloud.storage.constants.MULTI_REGIONAL_LEGACY_STORAGE_CLASS`,
            or
            :attr:`~google.cloud.storage.constants.REGIONAL_LEGACY_STORAGE_CLASS`.

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        """
        if new_class not in self.STORAGE_CLASSES:
            raise ValueError("Invalid storage class: %s" % (new_class,))

        # Update current blob's storage class prior to rewrite
        self._patch_property("storageClass", new_class)

        # Execute consecutive rewrite operations until operation is done
        token, _, _ = self.rewrite(self)
        while token is not None:
            token, _, _ = self.rewrite(self, token=token)

    cache_control = _scalar_property("cacheControl")
    """HTTP 'Cache-Control' header for this object.

    See `RFC 7234`_ and `API reference docs`_.

    :rtype: str or ``NoneType``

    .. _RFC 7234: https://tools.ietf.org/html/rfc7234#section-5.2
    """

    content_disposition = _scalar_property("contentDisposition")
    """HTTP 'Content-Disposition' header for this object.

    See `RFC 6266`_ and `API reference docs`_.

    :rtype: str or ``NoneType``

    .. _RFC 6266: https://tools.ietf.org/html/rfc7234#section-5.2
    """

    content_encoding = _scalar_property("contentEncoding")
    """HTTP 'Content-Encoding' header for this object.

    See `RFC 7231`_ and `API reference docs`_.

    :rtype: str or ``NoneType``

    .. _RFC 7231: https://tools.ietf.org/html/rfc7231#section-3.1.2.2
    """

    content_language = _scalar_property("contentLanguage")
    """HTTP 'Content-Language' header for this object.

    See `BCP47`_ and `API reference docs`_.

    :rtype: str or ``NoneType``

    .. _BCP47: https://tools.ietf.org/html/bcp47
    """

    content_type = _scalar_property(_CONTENT_TYPE_FIELD)
    """HTTP 'Content-Type' header for this object.

    See `RFC 2616`_ and `API reference docs`_.

    :rtype: str or ``NoneType``

    .. _RFC 2616: https://tools.ietf.org/html/rfc2616#section-14.17
    """

    crc32c = _scalar_property("crc32c")
    """CRC32C checksum for this object.

    See `RFC 4960`_ and `API reference docs`_.

    If not set before upload, the server will compute the hash.

    :rtype: str or ``NoneType``

    .. _RFC 4960: https://tools.ietf.org/html/rfc4960#appendix-B
    """

    @property
    def component_count(self):
        """Number of underlying components that make up this object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The component count (in case of a composed object) or
                  ``None`` if the blob's resource has not been loaded from
                  the server.  This property will not be set on objects
                  not created via ``compose``.
        """
        component_count = self._properties.get("componentCount")
        if component_count is not None:
            return int(component_count)

    @property
    def etag(self):
        """Retrieve the ETag for the object.

        See `RFC 2616 (etags)`_ and `API reference docs`_.

        :rtype: str or ``NoneType``
        :returns: The blob etag or ``None`` if the blob's resource has not
                  been loaded from the server.

        .. _RFC 2616 (etags): https://tools.ietf.org/html/rfc2616#section-3.11
        """
        return self._properties.get("etag")

    event_based_hold = _scalar_property("eventBasedHold")
    """Is an event-based hold active on the object?

    See `API reference docs`_.

    If the property is not set locally, returns :data:`None`.

    :rtype: bool or ``NoneType``
    """

    @property
    def generation(self):
        """Retrieve the generation for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The generation of the blob or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        generation = self._properties.get("generation")
        if generation is not None:
            return int(generation)

    @property
    def id(self):
        """Retrieve the ID for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        The ID consists of the bucket name, object name, and generation number.

        :rtype: str or ``NoneType``
        :returns: The ID of the blob or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        return self._properties.get("id")

    md5_hash = _scalar_property("md5Hash")
    """MD5 hash for this object.

    See `RFC 1321`_ and `API reference docs`_.

    If not set before upload, the server will compute the hash.

    :rtype: str or ``NoneType``

    .. _RFC 1321: https://tools.ietf.org/html/rfc1321
    """

    @property
    def media_link(self):
        """Retrieve the media download URI for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: str or ``NoneType``
        :returns: The media link for the blob or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        return self._properties.get("mediaLink")

    @property
    def metadata(self):
        """Retrieve arbitrary/application specific metadata for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :setter: Update arbitrary/application specific metadata for the
                 object.
        :getter: Retrieve arbitrary/application specific metadata for
                 the object.

        :rtype: dict or ``NoneType``
        :returns: The metadata associated with the blob or ``None`` if the
                  property is not set.
        """
        return copy.deepcopy(self._properties.get("metadata"))

    @metadata.setter
    def metadata(self, value):
        """Update arbitrary/application specific metadata for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :type value: dict
        :param value: (Optional) The blob metadata to set.
        """
        value = {k: str(v) for k, v in value.items()}
        self._patch_property("metadata", value)

    @property
    def metageneration(self):
        """Retrieve the metageneration for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The metageneration of the blob or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        metageneration = self._properties.get("metageneration")
        if metageneration is not None:
            return int(metageneration)

    @property
    def owner(self):
        """Retrieve info about the owner of the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: dict or ``NoneType``
        :returns: Mapping of owner's role/ID, or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        return copy.deepcopy(self._properties.get("owner"))

    @property
    def retention_expiration_time(self):
        """Retrieve timestamp at which the object's retention period expires.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the property is not set locally.
        """
        value = self._properties.get("retentionExpirationTime")
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def self_link(self):
        """Retrieve the URI for the object.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: str or ``NoneType``
        :returns: The self link for the blob or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        return self._properties.get("selfLink")

    @property
    def size(self):
        """Size of the object, in bytes.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The size of the blob or ``None`` if the blob's
                  resource has not been loaded from the server.
        """
        size = self._properties.get("size")
        if size is not None:
            return int(size)

    @property
    def kms_key_name(self):
        """Resource name of Cloud KMS key used to encrypt the blob's contents.

        :rtype: str or ``NoneType``
        :returns:
            The resource name or ``None`` if no Cloud KMS key was used,
            or the blob's resource has not been loaded from the server.
        """
        return self._properties.get("kmsKeyName")

    storage_class = _scalar_property("storageClass")
    """Retrieve the storage class for the object.

    This can only be set at blob / object **creation** time. If you'd
    like to change the storage class **after** the blob / object already
    exists in a bucket, call :meth:`update_storage_class` (which uses
    :meth:`rewrite`).

    See https://cloud.google.com/storage/docs/storage-classes

    :rtype: str or ``NoneType``
    :returns:
        If set, one of
        :attr:`~google.cloud.storage.constants.STANDARD_STORAGE_CLASS`,
        :attr:`~google.cloud.storage.constants.NEARLINE_STORAGE_CLASS`,
        :attr:`~google.cloud.storage.constants.COLDLINE_STORAGE_CLASS`,
        :attr:`~google.cloud.storage.constants.ARCHIVE_STORAGE_CLASS`,
        :attr:`~google.cloud.storage.constants.MULTI_REGIONAL_LEGACY_STORAGE_CLASS`,
        :attr:`~google.cloud.storage.constants.REGIONAL_LEGACY_STORAGE_CLASS`,
        :attr:`~google.cloud.storage.constants.DURABLE_REDUCED_AVAILABILITY_STORAGE_CLASS`,
        else ``None``.
    """

    temporary_hold = _scalar_property("temporaryHold")
    """Is a temporary hold active on the object?

    See `API reference docs`_.

    If the property is not set locally, returns :data:`None`.

    :rtype: bool or ``NoneType``
    """

    @property
    def time_deleted(self):
        """Retrieve the timestamp at which the object was deleted.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the blob's resource has not been loaded from
                  the server (see :meth:`reload`). If the blob has
                  not been deleted, this will never be set.
        """
        value = self._properties.get("timeDeleted")
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def time_created(self):
        """Retrieve the timestamp at which the object was created.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the blob's resource has not been loaded from
                  the server (see :meth:`reload`).
        """
        value = self._properties.get("timeCreated")
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def updated(self):
        """Retrieve the timestamp at which the object was updated.

        See https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the blob's resource has not been loaded from
                  the server (see :meth:`reload`).
        """
        value = self._properties.get("updated")
        if value is not None:
            return _rfc3339_to_datetime(value)


def _get_encryption_headers(key, source=False):
    """Builds customer encryption key headers

    :type key: bytes
    :param key: 32 byte key to build request key and hash.

    :type source: bool
    :param source: If true, return headers for the "source" blob; otherwise,
                   return headers for the "destination" blob.

    :rtype: dict
    :returns: dict of HTTP headers being sent in request.
    """
    if key is None:
        return {}

    key = _to_bytes(key)
    key_hash = hashlib.sha256(key).digest()
    key_hash = base64.b64encode(key_hash)
    key = base64.b64encode(key)

    if source:
        prefix = "X-Goog-Copy-Source-Encryption-"
    else:
        prefix = "X-Goog-Encryption-"

    return {
        prefix + "Algorithm": "AES256",
        prefix + "Key": _bytes_to_unicode(key),
        prefix + "Key-Sha256": _bytes_to_unicode(key_hash),
    }


def _quote(value, safe=b"~"):
    """URL-quote a string.

    If the value is unicode, this method first UTF-8 encodes it as bytes and
    then quotes the bytes. (In Python 3, ``urllib.parse.quote`` does this
    encoding automatically, but in Python 2, non-ASCII characters cannot be
    quoted.)

    :type value: str or bytes
    :param value: The value to be URL-quoted.

    :type safe: bytes
    :param safe: Bytes *not* to be quoted.  By default, includes only ``b'~'``.

    :rtype: str
    :returns: The encoded value (bytes in Python 2, unicode in Python 3).
    """
    value = _to_bytes(value, encoding="utf-8")
    return quote(value, safe=safe)


def _maybe_rewind(stream, rewind=False):
    """Rewind the stream if desired.

    :type stream: IO[bytes]
    :param stream: A bytes IO object open for reading.

    :type rewind: bool
    :param rewind: Indicates if we should seek to the beginning of the stream.
    """
    if rewind:
        stream.seek(0, os.SEEK_SET)


def _raise_from_invalid_response(error):
    """Re-wrap and raise an ``InvalidResponse`` exception.

    :type error: :exc:`google.resumable_media.InvalidResponse`
    :param error: A caught exception from the ``google-resumable-media``
                  library.

    :raises: :class:`~google.cloud.exceptions.GoogleCloudError` corresponding
             to the failed status code
    """
    response = error.response
    error_message = str(error)

    message = u"{method} {url}: {error}".format(
        method=response.request.method, url=response.request.url, error=error_message
    )

    raise exceptions.from_http_status(response.status_code, message, response=response)


def _add_query_parameters(base_url, name_value_pairs):
    """Add one query parameter to a base URL.

    :type base_url: string
    :param base_url: Base URL (may already contain query parameters)

    :type name_value_pairs: list of (string, string) tuples.
    :param name_value_pairs: Names and values of the query parameters to add

    :rtype: string
    :returns: URL with additional query strings appended.
    """
    if len(name_value_pairs) == 0:
        return base_url

    scheme, netloc, path, query, frag = urlsplit(base_url)
    query = parse_qsl(query)
    query.extend(name_value_pairs)
    return urlunsplit((scheme, netloc, path, urlencode(query), frag))
