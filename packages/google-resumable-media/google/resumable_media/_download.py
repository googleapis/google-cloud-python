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

"""Virtual bases classes for downloading media from Google APIs."""


import re

from six.moves import http_client

from google.resumable_media import _helpers
from google.resumable_media import exceptions


_CONTENT_RANGE_RE = re.compile(
    r'bytes (?P<start_byte>\d+)-(?P<end_byte>\d+)/(?P<total_bytes>\d+)',
    flags=re.IGNORECASE)
ACCEPTABLE_STATUS_CODES = (http_client.OK, http_client.PARTIAL_CONTENT)


class DownloadBase(object):
    """Base class for download helpers.

    Defines core shared behavior across different download types.

    Args:
        media_url (str): The URL containing the media to be downloaded.
        start (int): The first byte in a range to be downloaded.
        end (int): The last byte in a range to be downloaded.
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.
    """

    def __init__(self, media_url, start=None, end=None, headers=None):
        self.media_url = media_url
        """str: The URL containing the media to be downloaded."""
        self.start = start
        """Optional[int]: The first byte in a range to be downloaded."""
        self.end = end
        """Optional[int]: The last byte in a range to be downloaded."""
        if headers is None:
            headers = {}
        self._headers = headers
        self._finished = False

    @property
    def finished(self):
        """bool: Flag indicating if the download has completed."""
        return self._finished


class Download(DownloadBase):
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
        headers (Optional[Mapping[str, str]]): Extra headers that should
            be sent with the request, e.g. headers for encrypted data.
    """

    def _prepare_request(self):
        """Prepare the contents of an HTTP request.

        This is everything that must be done before a request that doesn't
        require network I/O (or other I/O). This is based on the `sans-I/O`_
        philosophy.

        Returns:
            Mapping[str, str]: The headers for the request.

        Raises:
            ValueError: If the current :class:`Download` has already
                finished.

        .. _sans-I/O: https://sans-io.readthedocs.io/
        """
        if self.finished:
            raise ValueError(u'A download can only be used once.')

        add_bytes_range(self.start, self.end, self._headers)
        return self._headers

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
        _helpers.require_status_code(response, ACCEPTABLE_STATUS_CODES)

    def consume(self, transport):
        """Consume the resource to be downloaded.

        Args:
            transport (object): An object which can make authenticated
                requests.

        Returns:
            object: The HTTP response returned by ``transport``.

        Raises:
            NotImplementedError: Always, since virtual.
        """
        raise NotImplementedError(u'This implementation is virtual.')


def add_bytes_range(start, end, headers):
    """Add a bytes range to a header dictionary.

    Some possible inputs and the corresponding bytes ranges::

       >>> headers = {}
       >>> add_bytes_range(None, None, headers)
       >>> headers
       {}
       >>> add_bytes_range(500, 999, headers)
       >>> headers['range']
       'bytes=500-999'
       >>> add_bytes_range(None, 499, headers)
       >>> headers['range']
       'bytes=0-499'
       >>> add_bytes_range(-500, None, headers)
       >>> headers['range']
       'bytes=-500'
       >>> add_bytes_range(9500, None, headers)
       >>> headers['range']
       'bytes=9500-'

    Args:
        start (Optional[int]): The first byte in a range. Can be zero,
            positive, negative or :data:`None`.
        end (Optional[int]): The last byte in a range. Assumed to be
            positive.
        headers (Mapping[str, str]): A headers mapping which can have the
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

    headers[_helpers.RANGE_HEADER] = u'bytes=' + bytes_range


def get_range_info(response, callback=_helpers.do_nothing):
    """Get the start, end and total bytes from a content range header.

    Args:
        response (object): An HTTP response object.
        callback (Optional[Callable]): A callback that takes no arguments,
            to be executed when an exception is being raised.

    Returns:
        Tuple[int, int, int]: The start byte, end byte and total bytes.

    Raises:
        ~google.resumable_media.exceptions.InvalidResponse: If the
            ``Content-Range`` header is not of the form
            ``bytes {start}-{end}/{total}``.
    """
    content_range = _helpers.header_required(
        response, _helpers.CONTENT_RANGE_HEADER)
    match = _CONTENT_RANGE_RE.match(content_range)
    if match is None:
        callback()
        raise exceptions.InvalidResponse(
            response, u'Unexpected content-range header', content_range,
            u'Expected to be of the form "bytes {start}-{end}/{total}"')

    return (
        int(match.group(u'start_byte')),
        int(match.group(u'end_byte')),
        int(match.group(u'total_bytes'))
    )
