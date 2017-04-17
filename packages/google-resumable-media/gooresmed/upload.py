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
import os
import random
import sys

import six


_CONTENT_TYPE_HEADER = u'content-type'
_BOUNDARY_WIDTH = len(repr(sys.maxsize - 1))
_BOUNDARY_FORMAT = u'==============={{:0{:d}d}}=='.format(_BOUNDARY_WIDTH)
_MULTIPART_SEP = b'--'
_CRLF = b'\r\n'
_MULTIPART_BEGIN = (
    b'\r\ncontent-type: application/json; charset=UTF-8\r\n\r\n')
_RELATED_HEADER = b'multipart/related; boundary="'

UPLOAD_CHUNK_SIZE = 262144  # 256 * 1024
"""int: Chunks in a resumable upload must come in multiples of 256 KB."""


class _UploadBase(object):
    """Base class for upload helpers.

    Defines core shared behavior across different upload types.

    Args:
       upload_url (str): The URL where the content will be uploaded.
    """

    def __init__(self, upload_url):
        self.upload_url = upload_url
        """str: The URL where the content will be uploaded."""
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the upload has completed."""
        return self._finished

    def _process_response(self):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        # Tombstone the current Upload so it cannot be used again.
        self._finished = True


class SimpleUpload(_UploadBase):
    """Upload a resource to a Google API.

    A **simple** media upload sends no metadata and completes the upload
    in a single request.

    Args:
       upload_url (str): The URL where the content will be uploaded.
    """

    def _prepare_request(self, content_type):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

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

        headers = {_CONTENT_TYPE_HEADER: content_type}
        return headers

    def transmit(self, transport, data, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (object): An object which can make authenticated
                requests via a ``post()`` method which accepts an
                upload URL, a ``data`` keyword argument and a
                ``headers`` keyword argument.
            data (bytes): The resource content to be uploaded.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            object: The return value of ``transport.post()``.
        """
        headers = self._prepare_request(content_type)
        result = transport.post(self.upload_url, data=data, headers=headers)
        self._process_response()
        return result


class MultipartUpload(_UploadBase):
    """Upload a resource with metadata to a Google API.

    A **multipart** upload sends both metadata and the resource in a single
    (multipart) request.

    Args:
       upload_url (str): The URL where the content will be uploaded.
    """

    def _prepare_request(self, data, metadata, content_type):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            data (bytes): The resource content to be uploaded.
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            Tuple[str, dict]: The payload and headers for the request.

        Raises:
            ValueError: If the current upload has already finished.
            TypeError: If ``data`` isn't bytes.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'An upload can only be used once.')

        if not isinstance(data, six.binary_type):
            raise TypeError(u'`data` must be bytes, received', type(data))
        content, multipart_boundary = _construct_multipart_request(
            data, metadata, content_type)
        multipart_content_type = _RELATED_HEADER + multipart_boundary + b'"'
        headers = {_CONTENT_TYPE_HEADER: multipart_content_type}
        return content, headers

    def transmit(self, transport, data, metadata, content_type):
        """Transmit the resource to be uploaded.

        Args:
            transport (object): An object which can make authenticated
                requests via a ``post()`` method which accepts an
                upload URL, a ``data`` keyword argument and a
                ``headers`` keyword argument.
            data (bytes): The resource content to be uploaded.
            metadata (Mapping[str, str]): The resource metadata, such as an
                ACL list.
            content_type (str): The content type of the resource, e.g. a JPEG
                image has content type ``image/jpeg``.

        Returns:
            object: The return value of ``transport.post()``.
        """
        payload, headers = self._prepare_request(data, metadata, content_type)
        result = transport.post(self.upload_url, data=payload, headers=headers)
        self._process_response()
        return result


class ResumableUpload(_UploadBase):
    """Initiate and fulfill a resumable upload to a Google API.

    A **resumable** upload sends an initial request with the resource metadata
    and then gets assigned an upload ID / upload URL to send bytes to.
    Using the upload URL, the upload is then done in chunks (determined by
    the user) until all bytes have been uploaded.

    Args:
       upload_url (str): The URL where the resumable upload will be initiated.
       chunk_size (int): The size of each chunk used to upload the resource.

    Raises:
        ValueError: If ``chunk_size`` is not a multiple of
            :data:`UPLOAD_CHUNK_SIZE`.
    """

    def __init__(self, upload_url, chunk_size):
        super(ResumableUpload, self).__init__(upload_url)
        if chunk_size % UPLOAD_CHUNK_SIZE != 0:
            raise ValueError(u'256 KB must divide chunk size')
        self._chunk_size = chunk_size
        self._stream = None
        self._total_bytes = None
        self._upload_id = None

    @property
    def chunk_size(self):
        """int: The size of each chunk used to upload the resource."""
        return self._chunk_size

    @property
    def upload_id(self):
        """Optional[str]: The upload ID of the in-progress resumable upload."""
        return self._upload_id


def _get_boundary():
    """Get a random boundary for a multipart request.

    Returns:
        bytes: The boundary used to separate parts of a multipart request.
    """
    random_int = random.randrange(sys.maxsize)
    boundary = _BOUNDARY_FORMAT.format(random_int)
    # NOTE: Neither % formatting nor .format() are available for byte strings
    #       in Python 3.4, so we must use unicode strings as templates.
    return boundary.encode(u'utf-8')


def _construct_multipart_request(data, metadata, content_type):
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
    multipart_boundary = _get_boundary()
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


def _get_total_bytes(stream):
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
