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


def _add_bytes_range(start, end, headers):
    """Add a bytes range to a header dictionary.

    Some possible inputs and the corresponding bytes ranges::

       >>> headers = {}
       >>> _add_bytes_range(None, None, headers)
       >>> headers
       {}
       >>> _add_bytes_range(500, 999, headers)
       >>> headers['Range']
       'bytes=500-999'
       >>> _add_bytes_range(None, 499, headers)
       >>> headers['Range']
       'bytes=0-499'
       >>> _add_bytes_range(-500, None, headers)
       >>> headers['Range']
       'bytes=-500'
       >>> _add_bytes_range(9500, None, headers)
       >>> headers['Range']
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
            bytes_range = '0-{:d}'.format(end)
    else:
        if end is None:
            if start < 0:
                bytes_range = str(start)
            else:
                bytes_range = '{:d}-'.format(start)
        else:
            bytes_range = '{:d}-{:d}'.format(start, end)

    headers['Range'] = 'bytes=' + bytes_range


class Download(object):
    """Helper to manage downloading some or all of a resource.

    Basic support will

    * download directly to a file on the host OS
    * download into a stream or file-like object
    * download and return content directly as a string or bytes

    In addition, "slices" of the resource can be retrieved by
    specifying a range with ``start`` and / or ``end``. However, in
    typical usage, neither ``start`` nor ``end`` is expected to be
    provided.

    Args:
       media_url (str): The URL containing the media to be downloaded.
       start (int): The first byte in a range to be downloaded. If not
           provided, but ``end`` is provided, will download from the
           beginning to ``end`` of the media.
       end (int): The last byte in a range to be downloaded. If not
           provided, but ``start`` is provided, will download from the
           ``start`` to the end of the media.
    """

    def __init__(self, media_url, start=None, end=None):
        self.media_url = media_url
        """str: The URL containing the media to be downloaded."""
        self.start = start
        """Optional[int]: The first byte in a range to be downloaded."""
        self.end = end
        """Optional[int]: The last byte in a range to be downloaded."""
        self._finished = False

        self._headers = {}
        _add_bytes_range(start, end, self._headers)

    @property
    def finished(self):
        """bool: Flag indicating if the download has completed."""
        return self._finished

    def consume(self):
        """Consume the resource to be downloaded."""
        raise NotImplementedError
