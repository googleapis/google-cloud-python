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

"""Virtual bases classes for uploading media via Google APIs.

Supported here are:

* simple (media) uploads
* multipart uploads that contain both metadata and a small file as payload
* resumable uploads (with metadata as well)
"""


import json
import os
import random
import sys

import six
from six.moves import http_client

from google.resumable_media import _helpers


_CONTENT_TYPE_HEADER = u'content-type'
_BOUNDARY_WIDTH = len(repr(sys.maxsize - 1))
_BOUNDARY_FORMAT = u'==============={{:0{:d}d}}=='.format(_BOUNDARY_WIDTH)
_MULTIPART_SEP = b'--'
_CRLF = b'\r\n'
_MULTIPART_BEGIN = (
    b'\r\ncontent-type: application/json; charset=UTF-8\r\n\r\n')
_RELATED_HEADER = b'multipart/related; boundary="'


class UploadBase(object):
    """Base class for upload helpers.

    Defines core shared behavior across different upload types.

    Args:
        upload_url (str): The URL where the content will be uploaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.

    Attributes:
        upload_url (str): The URL where the content will be uploaded.
    """

    def __init__(self, upload_url, headers=None):
        self.upload_url = upload_url
        if headers is None:
            headers = {}
        self._headers = headers
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the upload has completed."""
        return self._finished

    def _process_response(self, response):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            response (object): The HTTP response object.

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the status
                code is not 200.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        # Tombstone the current upload so it cannot be used again (in either
        # failure or success).
        self._finished = True
        _helpers.require_status_code(
            response, (http_client.OK,), self._get_status_code)

    @staticmethod
    def _get_status_code(response):
        """Access the status code from an HTTP response.

        Args:
            response (object): The HTTP response object.

        Raises:
            NotImplementedError: Always, since virtual.
        """
        raise NotImplementedError(u'This implementation is virtual.')


class SimpleUpload(UploadBase):
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

    def _prepare_request(self, content_type):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        .. note:

            This method will be used only once, so ``headers`` will be
            mutated by having a new key added to it.

        Args:
            content_type (str): The content type for the request.

        Returns:
            dict: The headers for the request.

        Raises:
            ValueError: If the current upload has already finished.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'An upload can only be used once.')

        self._headers[_CONTENT_TYPE_HEADER] = content_type
        return self._headers

    def transmit(self, transport, data, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (object): An object which can make authenticated
                requests.
            data (bytes): The resource content to be uploaded.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Raises:
            NotImplementedError: Always, since virtual.
        """
        raise NotImplementedError(u'This implementation is virtual.')


class MultipartUpload(UploadBase):
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

    def _prepare_request(self, data, metadata, content_type):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        .. note:

            This method will be used only once, so ``headers`` will be
            mutated by having a new key added to it.

        Args:
            data (bytes): The resource content to be uploaded.
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            Tuple[bytes, dict]: The payload and headers for the request.

        Raises:
            ValueError: If the current upload has already finished.
            TypeError: If ``data`` isn't bytes.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'An upload can only be used once.')

        if not isinstance(data, six.binary_type):
            raise TypeError(u'`data` must be bytes, received', type(data))
        content, multipart_boundary = construct_multipart_request(
            data, metadata, content_type)
        multipart_content_type = _RELATED_HEADER + multipart_boundary + b'"'
        self._headers[_CONTENT_TYPE_HEADER] = multipart_content_type
        return content, self._headers

    def transmit(self, transport, data, metadata, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (object): An object which can make authenticated
                requests.
            data (bytes): The resource content to be uploaded.
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Raises:
            NotImplementedError: Always, since virtual.
        """
        raise NotImplementedError(u'This implementation is virtual.')


def get_boundary():
    """Get a random boundary for a multipart request.

    Returns:
        bytes: The boundary used to separate parts of a multipart request.
    """
    random_int = random.randrange(sys.maxsize)
    boundary = _BOUNDARY_FORMAT.format(random_int)
    # NOTE: Neither % formatting nor .format() are available for byte strings
    #       in Python 3.4, so we must use unicode strings as templates.
    return boundary.encode(u'utf-8')


def construct_multipart_request(data, metadata, content_type):
    """Construct a multipart request body.

    Args:
        data (bytes): The resource content (UTF-8 encoded as bytes)
            to be uploaded.
        metadata (Mapping[str, str]): The resource metadata, such as an
            ACL list.
        content_type (str): The content type of the resource, e.g. a JPEG
            image has content type ``image/jpeg``.

    Returns:
        Tuple[bytes, bytes]: The multipart request body and the boundary used
        between each part.
    """
    multipart_boundary = get_boundary()
    json_bytes = json.dumps(metadata).encode(u'utf-8')
    content_type = content_type.encode(u'utf-8')
    # Combine the two parts into a multipart payload.
    # NOTE: We'd prefer a bytes template but are restricted by Python 3.4.
    boundary_sep = _MULTIPART_SEP + multipart_boundary
    content = (
        boundary_sep +
        _MULTIPART_BEGIN +
        json_bytes + _CRLF +
        boundary_sep + _CRLF +
        b'content-type: ' + content_type + _CRLF +
        _CRLF +  # Empty line between headers and body.
        data + _CRLF +
        boundary_sep + _MULTIPART_SEP)

    return content, multipart_boundary


def get_total_bytes(stream):
    """Determine the total number of bytes in a stream.

    Args:
       stream (IO[bytes]): The stream (i.e. file-like object).

    Returns:
        int: The number of bytes.
    """
    current_position = stream.tell()
    # NOTE: ``.seek()`` **should** return the same value that ``.tell()``
    #       returns, but in Python 2, ``file`` objects do not.
    stream.seek(0, os.SEEK_END)
    end_position = stream.tell()
    # Go back to the initial position.
    stream.seek(current_position)

    return end_position


def get_next_chunk(stream, chunk_size):
    """Get a chunk from an I/O stream.

    The ``stream`` may have fewer bytes remaining than ``chunk_size``
    so it may not always be the case that
    ``end_byte == start_byte + chunk_size - 1``.

    Args:
       stream (IO[bytes]): The stream (i.e. file-like object).

    Returns:
        Tuple[int, int, bytes]: Triple of the start byte index, the end byte
        index and the content in between those bytes.

    Raises:
        ValueError: If there is no data left to consume. This corresponds
            exactly to the case ``end_byte < start_byte``, which can only
            occur if ``end_byte == start_byte - 1``.
    """
    start_byte = stream.tell()
    payload = stream.read(chunk_size)
    end_byte = stream.tell() - 1
    if end_byte < start_byte:
        raise ValueError(
            u'Stream is already exhausted. There is no content remaining.')
    return start_byte, end_byte, payload
