# pylint: skip-file
"""Small helper class to provide a small slice of a stream."""

from gcloud._apitools import exceptions


class StreamSlice(object):

    """Provides a slice-like object for streams."""

    def __init__(self, stream, max_bytes):
        self._stream = stream
        self._remaining_bytes = max_bytes
        self._max_bytes = max_bytes

    def __str__(self):  # pragma: NO COVER
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
        # For 32-bit python2.x, len() cannot exceed a 32-bit number.
        return self._max_bytes

    def read(self, size=None):  # pylint: disable=missing-docstring
        """Read at most size bytes from this slice.

        Compared to other streams, there is one case where we may
        unexpectedly raise an exception on read: if the underlying stream
        is exhausted (i.e. returns no bytes on read), and the size of this
        slice indicates we should still be able to read more bytes, we
        raise exceptions.StreamExhausted.

        Args:
          size: If provided, read no more than size bytes from the stream.

        Returns:
          The bytes read from this slice.

        Raises:
          exceptions.StreamExhausted

        """
        if size is not None:
            read_size = min(size, self._remaining_bytes)
        else:
            read_size = self._remaining_bytes
        data = self._stream.read(read_size)
        if read_size > 0 and not data:
            raise exceptions.StreamExhausted(
                'Not enough bytes in stream; expected %d, exhausted '
                'after %d' % (
                    self._max_bytes,
                    self._max_bytes - self._remaining_bytes))
        self._remaining_bytes -= len(data)
        return data
