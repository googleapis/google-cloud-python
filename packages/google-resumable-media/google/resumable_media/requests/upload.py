# Copyright 2017 Google Inc.
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

"""Support for resumable uploads.

Also supported here are simple (media) uploads and multipart
uploads that contain both metadata and a small file as payload.
"""


import json
import re

from six.moves import http_client

import google.resumable_media._helpers as _base_helpers
from google.resumable_media import _upload
from google.resumable_media import exceptions
from google.resumable_media.requests import _helpers


_CONTENT_RANGE_TEMPLATE = u'bytes {:d}-{:d}/{:d}'
_BYTES_RANGE_RE = re.compile(
    r'bytes=0-(?P<end_byte>\d+)', flags=re.IGNORECASE)
_STREAM_ERROR_TEMPLATE = (
    u'Bytes stream is in unexpected state. '
    u'The local stream has had {:d} bytes read from it while '
    u'{:d} bytes have already been updated (they should match).')

UPLOAD_CHUNK_SIZE = 262144  # 256 * 1024
"""int: Chunks in a resumable upload must come in multiples of 256 KB."""
PERMANENT_REDIRECT = 308
"""int: Permanent redirect status code.

It is used by Google services to indicate some (but not all) of
a resumable upload has been completed.

``http.client.PERMANENT_REDIRECT`` was added in Python 3.5, so
can't be used in a "general" code base.

For more information, see `RFC 7238`_.

.. _RFC 7238: https://tools.ietf.org/html/rfc7238
"""


class SimpleUpload(_helpers.RequestsMixin, _upload.SimpleUpload):
    """Upload a resource to a Google API.

    A **simple** media upload sends no metadata and completes the upload
    in a single request.

    Args:
        upload_url (str): The URL where the content will be uploaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.
    """

    def transmit(self, transport, data, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            data (bytes): The resource content to be uploaded.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.
        """
        headers = self._prepare_request(content_type)
        result = _helpers.http_request(
            transport, u'POST', self.upload_url, data=data, headers=headers)
        self._process_response(result)
        return result


class MultipartUpload(_helpers.RequestsMixin, _upload.MultipartUpload):
    """Upload a resource with metadata to a Google API.

    A **multipart** upload sends both metadata and the resource in a single
    (multipart) request.

    Args:
        upload_url (str): The URL where the content will be uploaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.
    """

    def transmit(self, transport, data, metadata, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (~requests.Session): A ``requests`` object which can
                make authenticated requests.
            data (bytes): The resource content to be uploaded.
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            ~requests.Response: The HTTP response returned by ``transport``.
        """
        payload, headers = self._prepare_request(data, metadata, content_type)
        result = _helpers.http_request(
            transport, u'POST', self.upload_url, data=payload, headers=headers)
        self._process_response(result)
        return result


class ResumableUpload(_helpers.RequestsMixin, _upload.UploadBase):
    """Initiate and fulfill a resumable upload to a Google API.

    A **resumable** upload sends an initial request with the resource metadata
    and then gets assigned an upload ID / upload URL to send bytes to.
    Using the upload URL, the upload is then done in chunks (determined by
    the user) until all bytes have been uploaded.

    Args:
        upload_url (str): The URL where the resumable upload will be initiated.
        chunk_size (int): The size of each chunk used to upload the resource.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the :meth:`initiate` request, e.g. headers for
            encrypted data. These **will not** be sent with
            :meth:`transmit_next_chunk` or :meth:`recover` requests.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.

    Raises:
        ValueError: If ``chunk_size`` is not a multiple of
            :data:`UPLOAD_CHUNK_SIZE`.
    """

    def __init__(self, upload_url, chunk_size, headers=None):
        super(ResumableUpload, self).__init__(upload_url, headers=headers)
        if chunk_size % UPLOAD_CHUNK_SIZE != 0:
            raise ValueError(u'256 KB must divide chunk size')
        self._chunk_size = chunk_size
        self._stream = None
        self._content_type = None
        self._bytes_uploaded = 0
        self._total_bytes = None
        self._resumable_url = None
        self._invalid = False

    @property
    def invalid(self):
        """bool: Indicates if the upload is in an invalid state.

        This will occur if a call to :meth:`transmit_next_chunk` fails.
        To recover from such a failure, call :meth:`recover`.
        """
        return self._invalid

    @property
    def chunk_size(self):
        """int: The size of each chunk used to upload the resource."""
        return self._chunk_size

    @property
    def resumable_url(self):
        """Optional[str]: The URL of the in-progress resumable upload."""
        return self._resumable_url

    @property
    def bytes_uploaded(self):
        """int: Number of bytes that have been uploaded."""
        return self._bytes_uploaded

    @property
    def total_bytes(self):
        """Optional[int]: The total number of bytes to be uploaded."""
        return self._total_bytes

    def _prepare_initiate_request(self, stream, metadata, content_type):
        """Prepare the contents of HTTP request to initiate upload.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            stream (IO[bytes]): The stream (i.e. file-like object) that will
                be uploaded. The stream **must** be at the beginning (i.e.
                ``stream.tell() == 0``).
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            Tuple[bytes, dict]: The payload and headers for the request.

        Raises:
            ValueError: If the current upload has already been initiated.
            ValueError: If ``stream`` is not at the beginning.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.resumable_url is not None:
            raise ValueError(u'This upload has already been initiated.')
        if stream.tell() != 0:
            raise ValueError(u'Stream must be at beginning.')

        self._stream = stream
        self._content_type = content_type
        self._total_bytes = _upload.get_total_bytes(stream)
        headers = {
            _upload._CONTENT_TYPE_HEADER: u'application/json; charset=UTF-8',
            u'x-upload-content-type': content_type,
            u'x-upload-content-length': u'{:d}'.format(self._total_bytes),
        }
        headers.update(self._headers)
        payload = json.dumps(metadata).encode(u'utf-8')
        return payload, headers

    def _process_initiate_response(self, response):
        """Process the response from an HTTP request that initiated upload.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        This method takes the URL from the ``Location`` header and stores it
        for future use. Within that URL, we assume the ``upload_id`` query
        parameter has been included, but we do not check.

        Args:
            response (object): The HTTP response object (need headers).

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        self._resumable_url = _base_helpers.header_required(
            response, u'location', self._get_headers)

    def initiate(self, transport, stream, metadata, content_type):
        """Initiate a resumable upload.

        Args:
            transport (object): An object which can make authenticated
                requests.
            stream (IO[bytes]): The stream (i.e. file-like object) that will
                be uploaded. The stream **must** be at the beginning (i.e.
                ``stream.tell() == 0``).
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            object: The HTTP response returned by ``transport``.
        """
        payload, headers = self._prepare_initiate_request(
            stream, metadata, content_type)
        result = _helpers.http_request(
            transport, u'POST', self.upload_url, data=payload, headers=headers)
        self._process_initiate_response(result)
        return result

    def _prepare_request(self):
        """Prepare the contents of HTTP request to upload a chunk.

        This is everything that must be done before a request that doesn't
        require network I/O. This is based on the `sans-I/O`_ philosophy.

        For the time being, this **does require** some form of I/O to read
        a chunk from ``stream`` (via :func:`get_next_chunk`). However, this
        will (almost) certainly not be network I/O.

        Returns:
            Tuple[bytes, dict]: The payload and headers for the request. The
            headers **do not** incorporate the ``_headers`` on the
            current instance.

        Raises:
            ValueError: If the current upload has finished.
            ValueError: If the current upload is in an invalid state.
            ValueError: If the current upload has not been initiated.
            ValueError: If the location in the stream (i.e. ``stream.tell()``)
                does not agree with ``bytes_uploaded``.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'Upload has finished.')
        if self.invalid:
            raise ValueError(
                u'Upload is in an invalid state. To recover call `recover()`.')
        if self.resumable_url is None:
            raise ValueError(
                u'This upload has not been initiated. Please call '
                u'initiate() before beginning to transmit chunks.')

        start_byte, end_byte, payload = _upload.get_next_chunk(
            self._stream, self._chunk_size)
        if start_byte != self.bytes_uploaded:
            msg = _STREAM_ERROR_TEMPLATE.format(
                start_byte, self.bytes_uploaded)
            raise ValueError(msg)

        content_range = _CONTENT_RANGE_TEMPLATE.format(
            start_byte, end_byte, self._total_bytes)
        headers = {
            _upload._CONTENT_TYPE_HEADER: self._content_type,
            _base_helpers.CONTENT_RANGE_HEADER: content_range,
        }
        return payload, headers

    def _make_invalid(self):
        """Simple setter for ``invalid``.

        This is intended to be passed along as a callback to helpers that
        raise an exception so they can mark this instance as invalid before
        raising.
        """
        self._invalid = True

    def _process_response(self, response):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            response (object): The HTTP response object.

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is 308 and the ``range`` header is not of the form
                ``bytes 0-{end}``.
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is not 200 or 308.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        status_code = _base_helpers.require_status_code(
            response, (http_client.OK, PERMANENT_REDIRECT),
            self._get_status_code, callback=self._make_invalid)
        if status_code == http_client.OK:
            self._bytes_uploaded = self._total_bytes
            # Tombstone the current upload so it cannot be used again.
            self._finished = True
        else:
            bytes_range = _base_helpers.header_required(
                response, _base_helpers.RANGE_HEADER,
                self._get_headers, callback=self._make_invalid)
            match = _BYTES_RANGE_RE.match(bytes_range)
            if match is None:
                self._make_invalid()
                raise exceptions.InvalidResponse(
                    response, u'Unexpected "range" header', bytes_range,
                    u'Expected to be of the form "bytes=0-{end}"')
            self._bytes_uploaded = int(match.group(u'end_byte')) + 1

    def transmit_next_chunk(self, transport):
        """Transmit the next chunk of the resource to be uploaded.

        In the case of failure, an exception is thrown that preserves the
        failed response:

        .. testsetup:: bad-response

           import io

           import mock
           import requests
           from six.moves import http_client

           from google import resumable_media
           import google.resumable_media.requests.upload as upload_mod

           transport = mock.Mock(spec=[u'request'])
           fake_response = requests.Response()
           fake_response.status_code = int(http_client.BAD_REQUEST)
           transport.request.return_value = fake_response

           upload_url = u'http://test.invalid'
           upload = upload_mod.ResumableUpload(
               upload_url, upload_mod.UPLOAD_CHUNK_SIZE)
           # Fake that the upload has been initiate()-d
           data = b'data is here'
           upload._stream = io.BytesIO(data)
           upload._total_bytes = len(data)
           upload._resumable_url = u'http://test.invalid?upload_id=nope'

        .. doctest:: bad-response
           :options: +NORMALIZE_WHITESPACE

           >>> error = None
           >>> try:
           ...     upload.transmit_next_chunk(transport)
           ... except resumable_media.InvalidResponse as caught_exc:
           ...     error = caught_exc
           ...
           >>> error
           InvalidResponse('Request failed with status code', 400,
                           'Expected one of', <HTTPStatus.OK: 200>, 308)
           >>> error.response
           <Response [400]>

        Args:
            transport (object): An object which can make authenticated
                requests.

        Returns:
            object: The HTTP response returned by ``transport``.

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is not 200 or 308.
        """
        payload, headers = self._prepare_request()
        result = _helpers.http_request(
            transport, u'PUT', self.resumable_url,
            data=payload, headers=headers)
        self._process_response(result)
        return result

    def _prepare_recover_request(self):
        """Prepare the contents of HTTP request to recover from failure.

        This is everything that must be done before a request that doesn't
        require network I/O. This is based on the `sans-I/O`_ philosophy.

        We assume that the :attr:`resumable_url` is set (i.e. the only way
        the upload can end up :attr:`invalid` is if it has been initiated.

        Returns:
            dict: The headers for the request (they **do not** incorporate the
            ``_headers`` on the current instance).

        Raises:
            ValueError: If the current upload is not in an invalid state.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if not self.invalid:
            raise ValueError(
                u'Upload is not in invalid state, no need to recover.')

        headers = {_base_helpers.CONTENT_RANGE_HEADER: u'bytes */*'}
        return headers

    def _process_recover_response(self, response):
        """Process the response from an HTTP request to recover from failure.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            response (object): The HTTP response object.

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is not 308.
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is 308 and the ``range`` header is not of the form
                ``bytes 0-{end}``.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        _base_helpers.require_status_code(
            response, (PERMANENT_REDIRECT,), self._get_status_code)
        headers = _helpers.RequestsMixin._get_headers(response)
        if _base_helpers.RANGE_HEADER in headers:
            bytes_range = headers[_base_helpers.RANGE_HEADER]
            match = _BYTES_RANGE_RE.match(bytes_range)
            if match is None:
                raise exceptions.InvalidResponse(
                    response, u'Unexpected "range" header', bytes_range,
                    u'Expected to be of the form "bytes=0-{end}"')
            self._bytes_uploaded = int(match.group(u'end_byte')) + 1
        else:
            # In this case, the upload has not "begun".
            self._bytes_uploaded = 0

        self._stream.seek(self._bytes_uploaded)
        self._invalid = False

    def recover(self, transport):
        """Recover from a failure.

        This method should be used when a :class:`ResumableUpload` is in an
        :attr:`~ResumableUpload.invalid` state due to a request failure.

        This will verify the progress with the server and make sure the
        current upload is in a valid state before :meth:`transmit_next_chunk`
        can be used again.

        Args:
            transport (object): An object which can make authenticated
                requests.

        Returns:
            object: The HTTP response returned by ``transport``.
        """
        headers = self._prepare_recover_request()
        result = _helpers.http_request(
            transport, u'PUT', self.resumable_url, headers=headers)
        self._process_recover_response(result)
        return result
