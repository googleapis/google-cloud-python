# Copyright 2014 Google Inc.
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

"""Create / interact with Google Cloud Storage blobs."""

import base64
import copy
import hashlib
from io import BytesIO
from io import UnsupportedOperation
import json
import mimetypes
import os
import time

import httplib2
import six
from six.moves.urllib.parse import quote

from google.cloud._helpers import _rfc3339_to_datetime
from google.cloud._helpers import _to_bytes
from google.cloud._helpers import _bytes_to_unicode
from google.cloud.credentials import generate_signed_url
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import make_exception
from google.cloud.storage._helpers import _PropertyMixin
from google.cloud.storage._helpers import _scalar_property
from google.cloud.storage.acl import ObjectACL
from google.cloud.streaming.http_wrapper import Request
from google.cloud.streaming.http_wrapper import make_api_request
from google.cloud.streaming.transfer import Download
from google.cloud.streaming.transfer import RESUMABLE_UPLOAD
from google.cloud.streaming.transfer import Upload


_API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'


class Blob(_PropertyMixin):
    """A wrapper around Cloud Storage's concept of an ``Object``.

    :type name: str
    :param name: The name of the blob.  This corresponds to the
                 unique path of the object in the bucket.

    :type bucket: :class:`google.cloud.storage.bucket.Bucket`
    :param bucket: The bucket to which this blob belongs.

    :type chunk_size: int
    :param chunk_size: The size of a chunk of data whenever iterating (1 MB).
                       This must be a multiple of 256 KB per the API
                       specification.

    :type encryption_key: bytes
    :param encryption_key:
        Optional 32 byte encryption key for customer-supplied encryption.
        See https://cloud.google.com/storage/docs/encryption#customer-supplied
    """

    _chunk_size = None  # Default value for each instance.

    _CHUNK_SIZE_MULTIPLE = 256 * 1024
    """Number (256 KB, in bytes) that must divide the chunk size."""

    _STORAGE_CLASSES = (
        'NEARLINE',
        'MULTI_REGIONAL',
        'REGIONAL',
        'COLDLINE',
        'STANDARD',  # alias for MULTI_REGIONAL/REGIONAL, based on location
    )
    """Allowed values for :attr:`storage_class`.

    See:
    https://cloud.google.com/storage/docs/json_api/v1/objects#storageClass
    https://cloud.google.com/storage/docs/per-object-storage-class

    .. note::
       This list does not include 'DURABLE_REDUCED_AVAILABILITY', which
       is only documented for buckets (and deprectated.

    .. note::
       The documentation does *not* mention 'STANDARD', but it is the value
       assigned by the back-end for objects created in buckets with 'STANDARD'
       set as their 'storage_class'.
    """

    def __init__(self, name, bucket, chunk_size=None, encryption_key=None):
        super(Blob, self).__init__(name=name)

        self.chunk_size = chunk_size  # Check that setter accepts value.
        self.bucket = bucket
        self._acl = ObjectACL(self)
        self._encryption_key = encryption_key

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
        if value is not None and value % self._CHUNK_SIZE_MULTIPLE != 0:
            raise ValueError('Chunk size must be a multiple of %d.' % (
                self._CHUNK_SIZE_MULTIPLE,))
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
        return bucket_path + '/o/' + quote(blob_name, safe='')

    @property
    def acl(self):
        """Create our ACL on demand."""
        return self._acl

    def __repr__(self):
        if self.bucket:
            bucket_name = self.bucket.name
        else:
            bucket_name = None

        return '<Blob: %s, %s>' % (bucket_name, self.name)

    @property
    def path(self):
        """Getter property for the URL path to this Blob.

        :rtype: str
        :returns: The URL path to this Blob.
        """
        if not self.name:
            raise ValueError('Cannot determine path without a blob name.')

        return self.path_helper(self.bucket.path, self.name)

    @property
    def client(self):
        """The client bound to this blob."""
        return self.bucket.client

    @property
    def public_url(self):
        """The public URL for this blob's object.

        :rtype: `string`
        :returns: The public URL for this blob.
        """
        return '{storage_base_url}/{bucket_name}/{quoted_name}'.format(
            storage_base_url='https://storage.googleapis.com',
            bucket_name=self.bucket.name,
            quoted_name=quote(self.name, safe=''))

    def generate_signed_url(self, expiration, method='GET',
                            content_type=None,
                            generation=None, response_disposition=None,
                            response_type=None, client=None, credentials=None):
        """Generates a signed URL for this blob.

        .. note::

            If you are on Google Compute Engine, you can't generate a signed
            URL. Follow `Issue 922`_ for updates on this. If you'd like to
            be able to generate a signed URL from GCE, you can use a standard
            service account from a JSON file rather than a GCE service account.

        .. _Issue 922: https://github.com/GoogleCloudPlatform/\
                       google-cloud-python/issues/922

        If you have a blob that you want to allow access to for a set
        amount of time, you can use this method to generate a URL that
        is only valid within a certain time period.

        This is particularly useful if you don't want publicly
        accessible blobs, but don't want to require users to explicitly
        log in.

        :type expiration: int, long, datetime.datetime, datetime.timedelta
        :param expiration: When the signed URL should expire.

        :type method: str
        :param method: The HTTP verb that will be used when requesting the URL.

        :type content_type: str
        :param content_type: (Optional) The content type of the object
                             referenced by ``resource``.

        :type generation: str
        :param generation: (Optional) A value that indicates which generation
                           of the resource to fetch.

        :type response_disposition: str
        :param response_disposition: (Optional) Content disposition of
                                     responses to requests for the signed URL.
                                     For example, to enable the signed URL
                                     to initiate a file of ``blog.png``, use
                                     the value
                                     ``'attachment; filename=blob.png'``.

        :type response_type: str
        :param response_type: (Optional) Content type of responses to requests
                              for the signed URL. Used to over-ride the content
                              type of the underlying blob/object.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: (Optional) The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.


        :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                           :class:`NoneType`
        :param credentials: (Optional) The OAuth2 credentials to use to sign
                            the URL. Defaults to the credentials stored on the
                            client used.

        :rtype: str
        :returns: A signed URL you can use to access the resource
                  until expiration.
        """
        resource = '/{bucket_name}/{quoted_name}'.format(
            bucket_name=self.bucket.name,
            quoted_name=quote(self.name, safe=''))

        if credentials is None:
            client = self._require_client(client)
            credentials = client._base_connection.credentials

        return generate_signed_url(
            credentials, resource=resource,
            api_access_endpoint=_API_ACCESS_ENDPOINT,
            expiration=expiration, method=method,
            content_type=content_type,
            response_type=response_type,
            response_disposition=response_disposition,
            generation=generation)

    def exists(self, client=None):
        """Determines whether or not this blob exists.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :rtype: bool
        :returns: True if the blob exists in Cloud Storage.
        """
        client = self._require_client(client)
        try:
            # We only need the status code (200 or not) so we seek to
            # minimize the returned payload.
            query_params = {'fields': 'name'}
            # We intentionally pass `_target_object=None` since fields=name
            # would limit the local properties.
            client._connection.api_request(
                method='GET', path=self.path,
                query_params=query_params, _target_object=None)
            # NOTE: This will not fail immediately in a batch. However, when
            #       Batch.finish() is called, the resulting `NotFound` will be
            #       raised.
            return True
        except NotFound:
            return False

    def delete(self, client=None):
        """Deletes a blob from Cloud Storage.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :rtype: :class:`Blob`
        :returns: The blob that was just deleted.
        :raises: :class:`google.cloud.exceptions.NotFound`
                 (propagated from
                 :meth:`google.cloud.storage.bucket.Bucket.delete_blob`).
        """
        return self.bucket.delete_blob(self.name, client=client)

    def download_to_file(self, file_obj, client=None):
        """Download the contents of this blob into a file-like object.

        .. note::

           If the server-set property, :attr:`media_link`, is not yet
           initialized, makes an additional API request to load it.

         Downloading a file that has been encrypted with a `customer-supplied`_
         encryption key:

         .. literalinclude:: storage_snippets.py
            :start-after: [START download_to_file]
            :end-before: [END download_to_file]

        The ``encryption_key`` should be a str or bytes with a length of at
        least 32.

        .. _customer-supplied: https://cloud.google.com/storage/docs/\
                               encryption#customer-supplied

        :type file_obj: file
        :param file_obj: A file handle to which to write the blob's data.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        client = self._require_client(client)
        if self.media_link is None:  # not yet loaded
            self.reload()

        download_url = self.media_link

        # Use apitools 'Download' facility.
        download = Download.from_stream(file_obj)

        if self.chunk_size is not None:
            download.chunksize = self.chunk_size

        headers = _get_encryption_headers(self._encryption_key)

        request = Request(download_url, 'GET', headers)

        # Use ``_base_connection`` rather ``_connection`` since the current
        # connection may be a batch. A batch wraps a client's connection,
        # but does not store the ``http`` object. The rest (API_BASE_URL and
        # build_api_url) are also defined on the Batch class, but we just
        # use the wrapped connection since it has all three (http,
        # API_BASE_URL and build_api_url).
        download.initialize_download(request, client._base_connection.http)

    def download_to_filename(self, filename, client=None):
        """Download the contents of this blob into a named file.

        :type filename: str
        :param filename: A filename to be passed to ``open``.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        with open(filename, 'wb') as file_obj:
            self.download_to_file(file_obj, client=client)

        mtime = time.mktime(self.updated.timetuple())
        os.utime(file_obj.name, (mtime, mtime))

    def download_as_string(self, client=None):
        """Download the contents of this blob as a string.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :rtype: bytes
        :returns: The data stored in this blob.
        :raises: :class:`google.cloud.exceptions.NotFound`
        """
        string_buffer = BytesIO()
        self.download_to_file(string_buffer, client=client)
        return string_buffer.getvalue()

    def _create_upload(
            self, client, file_obj=None, size=None, content_type=None,
            chunk_size=None, strategy=None, extra_headers=None):
        """Helper for upload methods.

        Creates a :class:`google.cloud.core.streaming.Upload` object to handle
        the details of uploading a file to Cloud Storage.

        :type client: :class:`~google.cloud.storage.client.Client` or
            ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
            to the ``client`` stored on the blob's bucket.

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type size: int
        :param size: The size of the upload, in bytes.

        :type content_type: str
        :param content_type: Optional type of content being uploaded.

        :type chunk_size: int
        :param chunk_size: The size of each chunk when doing resumable and
            media uploads.

        :type strategy: str
        :param strategy: Either
            :attr:`google.cloud.core.streaming.transfer.SIMPLE_UPLOAD` or
            :attr:`google.cloud.core.streaming.transfer.RESUMABLE_UPLOAD`.

        :type extra_headers: dict
        :param extra_headers: Additional headers to be sent with the upload
            initiation request.

        :rtype: Tuple[google.cloud.core.streaming.Upload,
                      google.cloud.core.streaming.Request,
                      google.cloud.core.streaming.Response]
        :returns: The Upload object, the upload HTTP request, and the upload
                  initiation response.
        """

        client = self._require_client(client)

        # Use ``_base_connection`` rather ``_connection`` since the current
        # connection may be a batch. A batch wraps a client's connection,
        # but does not store the ``http`` object. The rest (API_BASE_URL and
        # build_api_url) are also defined on the Batch class, but we just
        # use the wrapped connection since it has all three (http,
        # API_BASE_URL and build_api_url).
        connection = client._base_connection

        content_type = (content_type or self._properties.get('contentType') or
                        'application/octet-stream')

        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': connection.USER_AGENT,
        }

        if extra_headers:
            headers.update(extra_headers)

        headers.update(_get_encryption_headers(self._encryption_key))

        # Use apitools' Upload functionality
        upload = Upload(
            file_obj, content_type, total_size=size, auto_transfer=False)

        if chunk_size is not None:
            upload.chunksize = chunk_size

        if strategy is not None:
            upload.strategy = RESUMABLE_UPLOAD

        url_builder = _UrlBuilder(
            bucket_name=self.bucket.name,
            object_name=self.name)
        upload_config = _UploadConfig()

        # Temporary URL until strategy is determined.
        base_url = connection.API_BASE_URL + '/upload'
        upload_url = connection.build_api_url(
            api_base_url=base_url,
            path=self.bucket.path + '/o')

        # Configure the upload request parameters.
        request = Request(upload_url, 'POST', headers)
        upload.configure_request(upload_config, request, url_builder)

        # Configure final URL
        query_params = url_builder.query_params
        base_url = connection.API_BASE_URL + '/upload'
        request.url = connection.build_api_url(
            api_base_url=base_url,
            path=self.bucket.path + '/o',
            query_params=query_params)

        # Start the upload session
        response = upload.initialize_upload(request, connection.http)

        return upload, request, response

    @staticmethod
    def _check_response_error(request, http_response):
        """Helper for :meth:`upload_from_file`."""
        info = http_response.info
        status = int(info['status'])
        if not 200 <= status < 300:
            faux_response = httplib2.Response({'status': status})
            raise make_exception(faux_response, http_response.content,
                                 error_info=request.url)

    def upload_from_file(self, file_obj, rewind=False, size=None,
                         content_type=None, num_retries=6, client=None):
        """Upload the contents of this blob from a file-like object.

        The content type of the upload will either be
        - The value passed in to the function (if any)
        - The value stored on the current blob
        - The default value of 'application/octet-stream'

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        Uploading a file with a `customer-supplied`_ encryption key:

        .. literalinclude:: storage_snippets.py
            :start-after: [START upload_from_file]
            :end-before: [END upload_from_file]

        The ``encryption_key`` should be a str or bytes with a length of at
        least 32.

        .. _customer-supplied: https://cloud.google.com/storage/docs/\
                               encryption#customer-supplied

        :type file_obj: file
        :param file_obj: A file handle open for reading.

        :type rewind: bool
        :param rewind: If True, seek to the beginning of the file handle before
                       writing the file to Cloud Storage.

        :type size: int
        :param size: The number of bytes to read from the file handle.
                     If not provided, we'll try to guess the size using
                     :func:`os.fstat`. (If the file handle is not from the
                     filesystem this won't be possible.)

        :type content_type: str
        :param content_type: Optional type of content being uploaded.

        :type num_retries: int
        :param num_retries: Number of upload retries. Defaults to 6.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :raises: :class:`ValueError` if size is not passed in and can not be
                 determined; :class:`google.cloud.exceptions.GoogleCloudError`
                 if the upload response returns an error status.
        """
        client = self._require_client(client)
        # Use ``_base_connection`` rather ``_connection`` since the current
        # connection may be a batch. A batch wraps a client's connection,
        # but does not store the ``http`` object. The rest (API_BASE_URL and
        # build_api_url) are also defined on the Batch class, but we just
        # use the wrapped connection since it has all three (http,
        # API_BASE_URL and build_api_url).
        connection = client._base_connection

        # Rewind the file if desired.
        if rewind:
            file_obj.seek(0, os.SEEK_SET)

        # Get the basic stats about the file.
        total_bytes = size
        if total_bytes is None:
            if hasattr(file_obj, 'fileno'):
                try:
                    total_bytes = os.fstat(file_obj.fileno()).st_size
                except (OSError, UnsupportedOperation):
                    pass  # Assuming fd is not an actual file (maybe socket).

        chunk_size = None
        strategy = None
        if self.chunk_size is not None:
            chunk_size = self.chunk_size

            if total_bytes is None:
                strategy = RESUMABLE_UPLOAD
        elif total_bytes is None:
            raise ValueError('total bytes could not be determined. Please '
                             'pass an explicit size, or supply a chunk size '
                             'for a streaming transfer.')

        upload, request, _ = self._create_upload(
            client, file_obj=file_obj, size=total_bytes,
            content_type=content_type, chunk_size=chunk_size,
            strategy=strategy)

        if upload.strategy == RESUMABLE_UPLOAD:
            http_response = upload.stream_file(use_chunks=True)
        else:
            http_response = make_api_request(
                connection.http, request, retries=num_retries)

        self._check_response_error(request, http_response)
        response_content = http_response.content

        if not isinstance(response_content,
                          six.string_types):  # pragma: NO COVER  Python3
            response_content = response_content.decode('utf-8')
        self._set_properties(json.loads(response_content))

    def upload_from_filename(self, filename, content_type=None, client=None):
        """Upload this blob's contents from the content of a named file.

        The content type of the upload will either be
        - The value passed in to the function (if any)
        - The value stored on the current blob
        - The value given by mimetypes.guess_type

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        :type filename: str
        :param filename: The path to the file.

        :type content_type: str
        :param content_type: Optional type of content being uploaded.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        """
        content_type = content_type or self._properties.get('contentType')
        if content_type is None:
            content_type, _ = mimetypes.guess_type(filename)

        with open(filename, 'rb') as file_obj:
            self.upload_from_file(
                file_obj, content_type=content_type, client=client)

    def upload_from_string(self, data, content_type='text/plain', client=None):
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
        """
        if isinstance(data, six.text_type):
            data = data.encode('utf-8')
        string_buffer = BytesIO()
        string_buffer.write(data)
        self.upload_from_file(
            file_obj=string_buffer, rewind=True, size=len(data),
            content_type=content_type, client=client)

    def create_resumable_upload_session(
            self,
            content_type=None,
            size=None,
            origin=None,
            client=None):
        """Create a resumable upload session.

        Resumable upload sessions allow you to start an upload session from
        one client and complete the session in another. This method is called
        by the initiator to set the metadata and limits. The initiator then
        passes the session URL to the client that will upload the binary data.
        The client performs a PUT request on the session URL to complete the
        upload. This process allows untrusted clients to upload to an
        access-controlled bucket. For more details, see the
        `documentation on signed URLs`_.

        .. _documentation on signed URLs: https://cloud.google.com/storage\
                /docs/access-control/signed-urls#signing-resumable

        The content type of the upload will either be
        - The value passed in to the function (if any)
        - The value stored on the current blob
        - The default value of 'application/octet-stream'

        .. note::
           The effect of uploading to an existing blob depends on the
           "versioning" and "lifecycle" policies defined on the blob's
           bucket.  In the absence of those policies, upload will
           overwrite any existing contents.

           See the `object versioning
           <https://cloud.google.com/storage/docs/object-versioning>`_ and
           `lifecycle <https://cloud.google.com/storage/docs/lifecycle>`_
           API documents for details.

        If :attr:`encryption_key` is set, the blob will be `encrypted`_.

        .. _encrypted: https://cloud.google.com/storage/docs/\
                               encryption#customer-supplied

        :type size: int
        :param size: Optional, the maximum number of bytes that can be
            uploaded using this session. If the size is not known when creating
            the session, this should be left blank.

        :type content_type: str
        :param content_type: Optional type of content being uploaded. This can
            be used to restrict the allowed file type that can be uploaded
            to the size.

        :type origin: str
        :param origin: Optional origin. If set, the upload can only be
            completed by a user-agent that uploads from the given origin. This
            can be useful when passing the session to a web client.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :rtype: str
        :returns: The resumable upload session URL. The upload can be
            completed by making an HTTP PUT request with the file's contents.

        :raises: :class:`google.cloud.exceptions.GoogleCloudError`
                 if the session creation response returns an error status.
        """

        extra_headers = {}

        if origin is not None:
            # This header is specifically for client-side uploads, it
            # determines the origins allowed for CORS.
            extra_headers['Origin'] = origin

        _, _, start_response = self._create_upload(
            client,
            size=size,
            content_type=content_type,
            strategy=RESUMABLE_UPLOAD,
            extra_headers=extra_headers)

        # The location header contains the session URL. This can be used
        # to continue the upload.
        resumable_upload_session_url = start_response.info['location']

        return resumable_upload_session_url

    def make_public(self, client=None):
        """Make this blob public giving all users read access.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        """
        self.acl.all().grant_read()
        self.acl.save(client=client)

    def compose(self, sources, client=None):
        """Concatenate source blobs into this one.

        :type sources: list of :class:`Blob`
        :param sources: blobs whose contents will be composed into this blob.

        :type client: :class:`~google.cloud.storage.client.Client` or
                      ``NoneType``
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.

        :raises: :exc:`ValueError` if this blob does not have its
                 :attr:`content_type` set.
        """
        if self.content_type is None:
            raise ValueError("Destination 'content_type' not set.")
        client = self._require_client(client)
        request = {
            'sourceObjects': [{'name': source.name} for source in sources],
            'destination': self._properties.copy(),
        }
        api_response = client._connection.api_request(
            method='POST', path=self.path + '/compose', data=request,
            _target_object=self)
        self._set_properties(api_response)

    def rewrite(self, source, token=None, client=None):
        """Rewrite source blob into this one.

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

        :rtype: tuple
        :returns: ``(token, bytes_rewritten, total_bytes)``, where ``token``
                  is a rewrite token (``None`` if the rewrite is complete),
                  ``bytes_rewritten`` is the number of bytes rewritten so far,
                  and ``total_bytes`` is the total number of bytes to be
                  rewritten.
        """
        client = self._require_client(client)
        headers = _get_encryption_headers(self._encryption_key)
        headers.update(_get_encryption_headers(
            source._encryption_key, source=True))

        if token:
            query_params = {'rewriteToken': token}
        else:
            query_params = {}

        api_response = client._connection.api_request(
            method='POST', path=source.path + '/rewriteTo' + self.path,
            query_params=query_params, data=self._properties, headers=headers,
            _target_object=self)
        rewritten = int(api_response['totalBytesRewritten'])
        size = int(api_response['objectSize'])

        # The resource key is set if and only if the API response is
        # completely done. Additionally, there is no rewrite token to return
        # in this case.
        if api_response['done']:
            self._set_properties(api_response['resource'])
            return None, rewritten, size

        return api_response['rewriteToken'], rewritten, size

    def update_storage_class(self, new_class, client=None):
        """Update blob's storage class via a rewrite-in-place.

        See:
        https://cloud.google.com/storage/docs/per-object-storage-class

        :type new_class: str
        :param new_class: new storage class for the object

        :type client: :class:`~google.cloud.storage.client.Client`
        :param client: Optional. The client to use.  If not passed, falls back
                       to the ``client`` stored on the blob's bucket.
        """
        if new_class not in self._STORAGE_CLASSES:
            raise ValueError("Invalid storage class: %s" % (new_class,))

        client = self._require_client(client)
        headers = _get_encryption_headers(self._encryption_key)
        headers.update(_get_encryption_headers(
            self._encryption_key, source=True))

        api_response = client._connection.api_request(
            method='POST', path=self.path + '/rewriteTo' + self.path,
            data={'storageClass': new_class}, headers=headers,
            _target_object=self)
        self._set_properties(api_response['resource'])

    cache_control = _scalar_property('cacheControl')
    """HTTP 'Cache-Control' header for this object.

    See: https://tools.ietf.org/html/rfc7234#section-5.2 and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    content_disposition = _scalar_property('contentDisposition')
    """HTTP 'Content-Disposition' header for this object.

    See: https://tools.ietf.org/html/rfc6266 and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    content_encoding = _scalar_property('contentEncoding')
    """HTTP 'Content-Encoding' header for this object.

    See: https://tools.ietf.org/html/rfc7231#section-3.1.2.2 and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    content_language = _scalar_property('contentLanguage')
    """HTTP 'Content-Language' header for this object.

    See: https://tools.ietf.org/html/bcp47 and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    content_type = _scalar_property('contentType')
    """HTTP 'Content-Type' header for this object.

    See: https://tools.ietf.org/html/rfc2616#section-14.17 and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    crc32c = _scalar_property('crc32c')
    """CRC32C checksum for this object.

    See: https://tools.ietf.org/html/rfc4960#appendix-B and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    @property
    def component_count(self):
        """Number of underlying components that make up this object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The component count (in case of a composed object) or
                  ``None`` if the property is not set locally. This property
                  will not be set on objects not created via ``compose``.
        """
        component_count = self._properties.get('componentCount')
        if component_count is not None:
            return int(component_count)

    @property
    def etag(self):
        """Retrieve the ETag for the object.

        See: https://tools.ietf.org/html/rfc2616#section-3.11 and
             https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: str or ``NoneType``
        :returns: The blob etag or ``None`` if the property is not set locally.
        """
        return self._properties.get('etag')

    @property
    def generation(self):
        """Retrieve the generation for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The generation of the blob or ``None`` if the property
                  is not set locally.
        """
        generation = self._properties.get('generation')
        if generation is not None:
            return int(generation)

    @property
    def id(self):
        """Retrieve the ID for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: str or ``NoneType``
        :returns: The ID of the blob or ``None`` if the property is not
                  set locally.
        """
        return self._properties.get('id')

    md5_hash = _scalar_property('md5Hash')
    """MD5 hash for this object.

    See: https://tools.ietf.org/html/rfc4960#appendix-B and
         https://cloud.google.com/storage/docs/json_api/v1/objects

    If the property is not set locally, returns ``None``.

    :rtype: str or ``NoneType``
    """

    @property
    def media_link(self):
        """Retrieve the media download URI for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: str or ``NoneType``
        :returns: The media link for the blob or ``None`` if the property is
                  not set locally.
        """
        return self._properties.get('mediaLink')

    @property
    def metadata(self):
        """Retrieve arbitrary/application specific metadata for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: dict or ``NoneType``
        :returns: The metadata associated with the blob or ``None`` if the
                  property is not set locally.
        """
        return copy.deepcopy(self._properties.get('metadata'))

    @metadata.setter
    def metadata(self, value):
        """Update arbitrary/application specific metadata for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :type value: dict
        :param value: (Optional) The blob metadata to set.
        """
        self._patch_property('metadata', value)

    @property
    def metageneration(self):
        """Retrieve the metageneration for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The metageneration of the blob or ``None`` if the property
                  is not set locally.
        """
        metageneration = self._properties.get('metageneration')
        if metageneration is not None:
            return int(metageneration)

    @property
    def owner(self):
        """Retrieve info about the owner of the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: dict or ``NoneType``
        :returns: Mapping of owner's role/ID. If the property is not set
                  locally, returns ``None``.
        """
        return copy.deepcopy(self._properties.get('owner'))

    @property
    def self_link(self):
        """Retrieve the URI for the object.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: str or ``NoneType``
        :returns: The self link for the blob or ``None`` if the property is
                  not set locally.
        """
        return self._properties.get('selfLink')

    @property
    def size(self):
        """Size of the object, in bytes.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: int or ``NoneType``
        :returns: The size of the blob or ``None`` if the property
                  is not set locally.
        """
        size = self._properties.get('size')
        if size is not None:
            return int(size)

    @property
    def storage_class(self):
        """Retrieve the storage class for the object.

        See: https://cloud.google.com/storage/docs/storage-classes

        :rtype: str or ``NoneType``
        :returns: If set, one of "MULTI_REGIONAL", "REGIONAL",
                  "NEARLINE", "COLDLINE", "STANDARD", or
                  "DURABLE_REDUCED_AVAILABILITY", else ``None``.
        """
        return self._properties.get('storageClass')

    @property
    def time_deleted(self):
        """Retrieve the timestamp at which the object was deleted.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the property is not set locally. If the blob has
                  not been deleted, this will never be set.
        """
        value = self._properties.get('timeDeleted')
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def time_created(self):
        """Retrieve the timestamp at which the object was created.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the property is not set locally.
        """
        value = self._properties.get('timeCreated')
        if value is not None:
            return _rfc3339_to_datetime(value)

    @property
    def updated(self):
        """Retrieve the timestamp at which the object was updated.

        See: https://cloud.google.com/storage/docs/json_api/v1/objects

        :rtype: :class:`datetime.datetime` or ``NoneType``
        :returns: Datetime object parsed from RFC3339 valid timestamp, or
                  ``None`` if the property is not set locally.
        """
        value = self._properties.get('updated')
        if value is not None:
            return _rfc3339_to_datetime(value)


class _UploadConfig(object):
    """Faux message FBO apitools' 'configure_request'.

    Values extracted from apitools
    'samples/storage_sample/storage/storage_v1_client.py'
    """
    accept = ['*/*']
    max_size = None
    resumable_multipart = True
    resumable_path = u'/resumable/upload/storage/v1/b/{bucket}/o'
    simple_multipart = True
    simple_path = u'/upload/storage/v1/b/{bucket}/o'


class _UrlBuilder(object):
    """Faux builder FBO apitools' 'configure_request'"""
    def __init__(self, bucket_name, object_name):
        self.query_params = {'name': object_name}
        self._bucket_name = bucket_name
        self._relative_path = ''


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
    key_hash = base64.b64encode(key_hash).rstrip()
    key = base64.b64encode(key).rstrip()

    if source:
        prefix = 'X-Goog-Copy-Source-Encryption-'
    else:
        prefix = 'X-Goog-Encryption-'

    return {
        prefix + 'Algorithm': 'AES256',
        prefix + 'Key': _bytes_to_unicode(key),
        prefix + 'Key-Sha256': _bytes_to_unicode(key_hash),
    }
