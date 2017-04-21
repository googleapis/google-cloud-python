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

"""Support for downloading media from Google APIs."""


import re

from six.moves import http_client

from google.resumable_media import _helpers
from google.resumable_media import exceptions


_CONTENT_RANGE_RE = re.compile(
    r'bytes (?P<start_byte>\d+)-(?P<end_byte>\d+)/(?P<total_bytes>\d+)',
    flags=re.IGNORECASE)
_ACCEPTABLE_STATUS_CODES = (http_client.OK, http_client.PARTIAL_CONTENT)


class _DownloadBase(object):
    """Base class for download helpers.

    Defines core shared behavior across different download types.

    Args:
       media_url (str): The URL containing the media to be downloaded.
       start (int): The first byte in a range to be downloaded.
       end (int): The last byte in a range to be downloaded.
    """

    def __init__(self, media_url, start=None, end=None):
        self.media_url = media_url
        """str: The URL containing the media to be downloaded."""
        self.start = start
        """Optional[int]: The first byte in a range to be downloaded."""
        self.end = end
        """Optional[int]: The last byte in a range to be downloaded."""
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the download has completed."""
        return self._finished


class Download(_DownloadBase):
    """Helper to manage downloading a resource from a Google API.

    "Slices" of the resource can be retrieved by specifying a range
    with ``start`` and / or ``end``. However, in typical usage, neither
    ``start`` nor ``end`` is expected to be provided.

    Args:
       media_url (str): The URL containing the media to be downloaded.
       start (int): The first byte in a range to be downloaded. If not
           provided, but ``end`` is provided, will download from the
           beginning to ``end`` of the media.
       end (int): The last byte in a range to be downloaded. If not
           provided, but ``start`` is provided, will download from the
           ``start`` to the end of the media.
    """

    def _prepare_request(self):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Returns:
            dict: The headers for the request.

        Raises:
            ValueError: If the current :class:`Download` has already
                finished.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'A download can only be used once.')

        headers = {}
        _add_bytes_range(self.start, self.end, headers)
        return headers

    def _process_response(self, response):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Args:
            response (object): The HTTP response object.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        # Tombstone the current Download so it cannot be used again.
        self._finished = True
        _helpers.require_status_code(response, _ACCEPTABLE_STATUS_CODES)

    def consume(self, transport):
        """Consume the resource to be downloaded.

        Args:
            transport (object): An object which can make authenticated
                requests.

        Returns:
            object: The HTTP response returned by ``transport``.

        Raises:
            ValueError: If the current :class:`Download` has already
                finished.
        """
        headers = self._prepare_request()
        result = _helpers.http_request(
            transport, u'GET', self.media_url, headers=headers)
        self._process_response(result)
        return result


class ChunkedDownload(_DownloadBase):
    """Download a resource in chunks from a Google API.

    Args:
       media_url (str): The URL containing the media to be downloaded.
       chunk_size (int): The number of bytes to be retrieved in each
           request.
       stream (IO[bytes]): A write-able stream (i.e. file-like object) that
           will be used to concatenate chunks of the resource as they are
           downloaded.
       start (int): The first byte in a range to be downloaded. If not
           provided, defaults to ``0``.
       end (int): The last byte in a range to be downloaded. If not
           provided, will download to the end of the media.

    Raises:
        ValueError: If ``start`` is negative.
    """

    def __init__(self, media_url, chunk_size, stream, start=0, end=None):
        if start < 0:
            raise ValueError(
                u'On a chunked download the starting '
                u'value cannot be negative.')
        super(ChunkedDownload, self).__init__(
            media_url, start=start, end=end)
        self.chunk_size = chunk_size
        """int: The number of bytes to be retrieved in each request."""
        self._stream = stream
        self._bytes_downloaded = 0
        self._total_bytes = None

    @property
    def bytes_downloaded(self):
        """int: Number of bytes that have been downloaded."""
        return self._bytes_downloaded

    @property
    def total_bytes(self):
        """Optional[int]: The total number of bytes to be downloaded."""
        return self._total_bytes

    def _get_byte_range(self):
        """Determines the byte range for the next request.

        Returns:
            Tuple[int, int]: The pair of begin and end byte for the next
            chunked request.
        """
        curr_start = self.start + self.bytes_downloaded
        curr_end = curr_start + self.chunk_size - 1
        # Make sure ``curr_end`` does not exceed ``end``.
        if self.end is not None:
            curr_end = min(curr_end, self.end)
        # Make sure ``curr_end`` does not exceed ``total_bytes - 1``.
        if self.total_bytes is not None:
            curr_end = min(curr_end, self.total_bytes - 1)
        return curr_start, curr_end

    def _prepare_request(self):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Returns:
            dict: The headers for the request.

        Raises:
            ValueError: If the current download has finished.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'Download has finished.')

        curr_start, curr_end = self._get_byte_range()
        headers = {}
        _add_bytes_range(curr_start, curr_end, headers)
        return headers

    def _process_response(self, response):
        """Process the response from an HTTP request.

        This is everything that must be done after a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Updates the current state after consuming a chunk. First,
        increments ``bytes_downloaded`` by the number of bytes in the
        ``Content-Length`` header.

        If ``total_bytes`` is already set, this assumes (but does not check)
        that we already have the correct value and doesn't bother to check
        that it agrees with the headers.

        We expect the **total** length to be in the ``Content-Range`` header,
        but this header is only present on requests which sent the ``Range``
        header. This response header should be of the form
        ``bytes {start}-{end}/{total}`` and ``{end} - {start} + 1``
        should be the same as the ``Content-Length``.

        Args:
            response (object): The HTTP response object (need headers).

        Raises:
            ~google.resumable_media.exceptions.InvalidResponse: If the number
                of bytes in the body doesn't match the content length header.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        # Verify the response before updating the current instance.
        _helpers.require_status_code(response, _ACCEPTABLE_STATUS_CODES)
        content_length = _helpers.header_required(response, u'content-length')
        num_bytes = int(content_length)
        _, end_byte, total_bytes = _get_range_info(response)
        response_body = _helpers.get_body(response)
        if len(response_body) != num_bytes:
            raise exceptions.InvalidResponse(
                response, u'Response is different size than content-length',
                u'Expected', num_bytes, u'Received', len(response_body))

        # First update ``bytes_downloaded``.
        self._bytes_downloaded += num_bytes
        # If the end byte is past ``end`` or ``total_bytes - 1`` we are done.
        if self.end is not None and end_byte >= self.end:
            self._finished = True
        elif end_byte >= total_bytes - 1:
            self._finished = True
        # NOTE: We only use ``total_bytes`` if not already known.
        if self.total_bytes is None:
            self._total_bytes = total_bytes
        # Write the response body to the stream.
        self._stream.write(response_body)

    def consume_next_chunk(self, transport):
        """Consume the next chunk of the resource to be downloaded.

        Args:
            transport (object): An object which can make authenticated
                requests.

        Returns:
            object: The HTTP response returned by ``transport``.

        Raises:
            ValueError: If the current download has finished.
        """
        headers = self._prepare_request()
        result = _helpers.http_request(
            transport, u'GET', self.media_url, headers=headers)
        self._process_response(result)
        return result


def _add_bytes_range(start, end, headers):
    """Add a bytes range to a header dictionary.

    Some possible inputs and the corresponding bytes ranges::

       >>> headers = {}
       >>> _add_bytes_range(None, None, headers)
       >>> headers
       {}
       >>> _add_bytes_range(500, 999, headers)
       >>> headers['range']
       'bytes=500-999'
       >>> _add_bytes_range(None, 499, headers)
       >>> headers['range']
       'bytes=0-499'
       >>> _add_bytes_range(-500, None, headers)
       >>> headers['range']
       'bytes=-500'
       >>> _add_bytes_range(9500, None, headers)
       >>> headers['range']
       'bytes=9500-'

    Args:
        start (Optional[int]): The first byte in a range. Can be zero,
            positive, negative or :data:`None`.
        end (Optional[int]): The last byte in a range. Assumed to be
            positive.
        headers (dict): A headers dictionary which can have the
            bytes range added if at least one of ``start`` or ``end``
            is not :data:`None`.
    """
    if start is None:
        if end is None:
            # No range to add.
            return
        else:
            # NOTE: This assumes ``end`` is non-negative.
            bytes_range = u'0-{:d}'.format(end)
    else:
        if end is None:
            if start < 0:
                bytes_range = u'{:d}'.format(start)
            else:
                bytes_range = u'{:d}-'.format(start)
        else:
            # NOTE: This is invalid if ``start < 0``.
            bytes_range = u'{:d}-{:d}'.format(start, end)

    headers[u'range'] = u'bytes=' + bytes_range


def _get_range_info(response):
    """Get the start, end and total bytes from a content range header.

    Args:
        response (object): An HTTP response object.

    Returns:
        Tuple[int, int, int]: The start byte, end byte and total bytes.

    Raises:
        ~google.resumable_media.exceptions.InvalidResponse: If the
            ``Content-Range`` header is not of the form
            ``bytes {start}-{end}/{total}``.
    """
    content_range = _helpers.header_required(response, u'content-range')
    match = _CONTENT_RANGE_RE.match(content_range)
    if match is None:
        raise exceptions.InvalidResponse(
            response, u'Unexpected content-range header', content_range,
            u'Expected to be of the form "bytes {start}-{end}/{total}"')

    return (
        int(match.group(u'start_byte')),
        int(match.group(u'end_byte')),
        int(match.group(u'total_bytes'))
    )
