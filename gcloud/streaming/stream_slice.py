# Copyright 2016 Google Inc. All rights reserved.
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

"""Small helper class to provide a small slice of a stream."""

from six.moves import http_client


class StreamSlice(object):
    """Provides a slice-like object for streams.

    :type stream:  readable file-like object
    :param stream:  the stream to be buffered

    :type max_bytes: integer
    :param max_bytes: maximum number of bytes to return in the slice
    """
    def __init__(self, stream, max_bytes):
        self._stream = stream
        self._remaining_bytes = max_bytes
        self._max_bytes = max_bytes

    def __repr__(self):
        return 'Slice of stream %s with %s/%s bytes not yet read' % (
            self._stream, self._remaining_bytes, self._max_bytes)

    def __len__(self):
        return self._max_bytes

    def __nonzero__(self):
        # For 32-bit python2.x, len() cannot exceed a 32-bit number; avoid
        # accidental len() calls from httplib in the form of "if this_object:".
        return bool(self._max_bytes)

    @property
    def length(self):
        """Maximum number of bytes to return in the slice.

        .. note::

           For 32-bit python2.x, len() cannot exceed a 32-bit number.

        :rtype: integer
        :returns: The max "length" of the stream.
        """
        return self._max_bytes

    def read(self, size=None):
        """Read bytes from the slice.

        Compared to other streams, there is one case where we may
        unexpectedly raise an exception on read: if the underlying stream
        is exhausted (i.e. returns no bytes on read), and the size of this
        slice indicates we should still be able to read more bytes, we
        raise :exc:`IncompleteRead`.

        :type size: integer or None
        :param size: If provided, read no more than size bytes from the stream.

        :rtype: bytes
        :returns: bytes read from this slice.

        :raises: :exc:`IncompleteRead`
        """
        if size is not None:
            read_size = min(size, self._remaining_bytes)
        else:
            read_size = self._remaining_bytes
        data = self._stream.read(read_size)
        if read_size > 0 and not data:
            raise http_client.IncompleteRead(
                self._max_bytes - self._remaining_bytes, self._max_bytes)
        self._remaining_bytes -= len(data)
        return data
