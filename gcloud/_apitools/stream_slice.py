#!/usr/bin/env python
"""Small helper class to provide a small slice of a stream."""

from apitools.base.py import exceptions


class StreamSlice(object):

    """Provides a slice-like object for streams."""

    def __init__(self, stream, max_bytes):
        self.__stream = stream
        self.__remaining_bytes = max_bytes
        self.__max_bytes = max_bytes

    def __str__(self):
        return 'Slice of stream %s with %s/%s bytes not yet read' % (
            self.__stream, self.__remaining_bytes, self.__max_bytes)

    def __len__(self):
        return self.__max_bytes

    def __nonzero__(self):
        # For 32-bit python2.x, len() cannot exceed a 32-bit number; avoid
        # accidental len() calls from httplib in the form of "if this_object:".
        return bool(self.__max_bytes)

    @property
    def length(self):
        # For 32-bit python2.x, len() cannot exceed a 32-bit number.
        return self.__max_bytes

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
            read_size = min(size, self.__remaining_bytes)
        else:
            read_size = self.__remaining_bytes
        data = self.__stream.read(read_size)
        if read_size > 0 and not data:
            raise exceptions.StreamExhausted(
                'Not enough bytes in stream; expected %d, exhausted '
                'after %d' % (
                    self.__max_bytes,
                    self.__max_bytes - self.__remaining_bytes))
        self.__remaining_bytes -= len(data)
        return data
