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

"""Small helper class to provide a small slice of a stream.

This class reads ahead to detect if we are at the end of the stream.
"""


class BufferedStream(object):
    """Buffers a stream, reading ahead to determine if we're at the end.

    :type stream:  readable file-like object
    :param stream:  the stream to be buffered

    :type start: integer
    :param start: the starting point in the stream

    :type size: integer
    :param size:  the size of the buffer
    """
    def __init__(self, stream, start, size):
        self._stream = stream
        self._start_pos = start
        self._buffer_pos = 0

        if not hasattr(self._stream, 'closed') or not self._stream.closed:
            self._buffered_data = self._stream.read(size)
        else:
            self._buffered_data = b''

        self._stream_at_end = len(self._buffered_data) < size
        self._end_pos = self._start_pos + len(self._buffered_data)

    def __repr__(self):
        return ('Buffered stream %s from position %s-%s with %s '
                'bytes remaining' % (self._stream, self._start_pos,
                                     self._end_pos, self._bytes_remaining))

    def __len__(self):
        return len(self._buffered_data)

    @property
    def stream_exhausted(self):
        """Does the stream have bytes remaining beyond the buffer

        :rtype: boolean
        :returns: Boolean indicating if the stream is exhausted.
        """
        return self._stream_at_end

    @property
    def stream_end_position(self):
        """Point to which stream was read into the buffer

        :rtype: integer
        :returns: The end-position of the stream.
        """
        return self._end_pos

    @property
    def _bytes_remaining(self):
        """Bytes remaining to be read from the buffer

        :rtype: integer
        :returns: The number of bytes remaining.
        """
        return len(self._buffered_data) - self._buffer_pos

    def read(self, size=None):
        """Read bytes from the buffer.

        :type size: integer or None
        :param size: How many bytes to read (defaults to all remaining bytes).

        :rtype: str
        :returns: The data read from the stream.
        """
        if size is None or size < 0:
            raise ValueError(
                'Illegal read of size %s requested on BufferedStream. '
                'Wrapped stream %s is at position %s-%s, '
                '%s bytes remaining.' %
                (size, self._stream, self._start_pos, self._end_pos,
                 self._bytes_remaining))

        if not self._bytes_remaining:
            return b''

        size = min(size, self._bytes_remaining)
        data = self._buffered_data[self._buffer_pos:self._buffer_pos + size]
        self._buffer_pos += size
        return data
