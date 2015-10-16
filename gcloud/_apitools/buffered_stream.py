# pylint: skip-file
"""Small helper class to provide a small slice of a stream.

This class reads ahead to detect if we are at the end of the stream.
"""

from gcloud._apitools import exceptions


# TODO(user): Consider replacing this with a StringIO.
class BufferedStream(object):

    """Buffers a stream, reading ahead to determine if we're at the end."""

    def __init__(self, stream, start, size):
        self._stream = stream
        self._start_pos = start
        self._buffer_pos = 0
        self._buffered_data = self._stream.read(size)
        self._stream_at_end = len(self._buffered_data) < size
        self._end_pos = self._start_pos + len(self._buffered_data)

    def __str__(self):  # pragma: NO COVER
        return ('Buffered stream %s from position %s-%s with %s '
                'bytes remaining' % (self._stream, self._start_pos,
                                     self._end_pos, self._bytes_remaining))

    def __len__(self):
        return len(self._buffered_data)

    @property
    def stream_exhausted(self):
        return self._stream_at_end

    @property
    def stream_end_position(self):
        return self._end_pos

    @property
    def _bytes_remaining(self):
        return len(self._buffered_data) - self._buffer_pos

    def read(self, size=None):  # pylint: disable=invalid-name
        """Reads from the buffer."""
        if size is None or size < 0:
            raise exceptions.NotYetImplementedError(
                'Illegal read of size %s requested on BufferedStream. '
                'Wrapped stream %s is at position %s-%s, '
                '%s bytes remaining.' %
                (size, self._stream, self._start_pos, self._end_pos,
                 self._bytes_remaining))

        data = b''
        if self._bytes_remaining:
            size = min(size, self._bytes_remaining)
            data = self._buffered_data[
                self._buffer_pos:self._buffer_pos + size]
            self._buffer_pos += size
        return data
