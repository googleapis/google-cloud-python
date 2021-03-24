# Copyright 2021 Google LLC
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

import io

# Resumable uploads require a chunk size of precisely a multiple of 256 KiB.
CHUNK_SIZE_MULTIPLE = 256 * 1024  # 256 KiB
DEFAULT_CHUNK_SIZE = 40 * 1024 * 1024  # 40 MiB

# Valid keyword arguments for download methods, and blob.reload() if needed.
# Note: Changes here need to be reflected in the blob.open() docstring.
VALID_DOWNLOAD_KWARGS = {
    "if_generation_match",
    "if_generation_not_match",
    "if_metageneration_match",
    "if_metageneration_not_match",
    "timeout",
}

# Valid keyword arguments for upload methods.
# Note: Changes here need to be reflected in the blob.open() docstring.
VALID_UPLOAD_KWARGS = {
    "content_type",
    "num_retries",
    "predefined_acl",
    "if_generation_match",
    "if_generation_not_match",
    "if_metageneration_match",
    "if_metageneration_not_match",
    "timeout",
    "checksum",
}


class BlobReader(io.BufferedIOBase):
    """A file-like object that reads from a blob.

    :type blob: 'google.cloud.storage.blob.Blob'
    :param blob:
        The blob to download.

    :type chunk_size: long
    :param chunk_size:
        (Optional) The minimum number of bytes to read at a time. If fewer
        bytes than the chunk_size are requested, the remainder is buffered.
        The default is the chunk_size of the blob, or 40MiB.

    :param download_kwargs: Keyword arguments to pass to the underlying API
        calls. The following arguments are supported: "if_generation_match",
        "if_generation_not_match", "if_metageneration_match",
        "if_metageneration_not_match", "timeout".
    """

    def __init__(self, blob, chunk_size=None, **download_kwargs):
        """docstring note that download_kwargs also used for reload()"""
        for kwarg in download_kwargs:
            if kwarg not in VALID_DOWNLOAD_KWARGS:
                raise ValueError(
                    "BlobReader does not support keyword argument {}.".format(kwarg)
                )

        self._blob = blob
        self._pos = 0
        self._buffer = io.BytesIO()
        self._chunk_size = chunk_size or blob.chunk_size or DEFAULT_CHUNK_SIZE
        self._download_kwargs = download_kwargs

    def read(self, size=-1):
        self._checkClosed()  # Raises ValueError if closed.

        result = self._buffer.read(size)
        # If the read request demands more bytes than are buffered, fetch more.
        remaining_size = size - len(result)
        if remaining_size > 0 or size < 0:
            self._buffer.seek(0)
            self._buffer.truncate(0)  # Clear the buffer to make way for new data.
            fetch_start = self._pos + len(result)
            if size > 0:
                # Fetch the larger of self._chunk_size or the remaining_size.
                fetch_end = fetch_start + max(remaining_size, self._chunk_size)
            else:
                fetch_end = None

            # Download the blob.
            result += self._blob.download_as_bytes(
                start=fetch_start, end=fetch_end, **self._download_kwargs
            )

            # If more bytes were read than is immediately needed, buffer the
            # remainder and then trim the result.
            if size > 0 and len(result) > size:
                self._buffer.write(result[size:])
                self._buffer.seek(0)
                result = result[:size]

        self._pos += len(result)

        return result

    def read1(self, size=-1):
        return self.read(size)

    def seek(self, pos, whence=0):
        """Seek within the blob.

        This implementation of seek() uses knowledge of the blob size to
        validate that the reported position does not exceed the blob last byte.
        If the blob size is not already known it will call blob.reload().
        """
        self._checkClosed()  # Raises ValueError if closed.

        if self._blob.size is None:
            self._blob.reload(**self._download_kwargs)

        initial_pos = self._pos

        if whence == 0:
            self._pos = pos
        elif whence == 1:
            self._pos += pos
        elif whence == 2:
            self._pos = self._blob.size + pos
        if whence not in {0, 1, 2}:
            raise ValueError("invalid whence value")

        if self._pos > self._blob.size:
            self._pos = self._blob.size

        # Seek or invalidate buffer as needed.
        difference = self._pos - initial_pos
        new_buffer_pos = self._buffer.seek(difference, 1)
        if new_buffer_pos != difference:  # Buffer does not contain new pos.
            # Invalidate buffer.
            self._buffer.seek(0)
            self._buffer.truncate(0)

        return self._pos

    def close(self):
        self._buffer.close()

    def _checkClosed(self):
        if self._buffer.closed:
            raise ValueError("I/O operation on closed file.")

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return True


class BlobWriter(io.BufferedIOBase):
    """A file-like object that writes to a blob.

    :type blob: 'google.cloud.storage.blob.Blob'
    :param blob:
        The blob to which to write.

    :type chunk_size: long
    :param chunk_size:
        (Optional) The maximum number of bytes to buffer before sending data
        to the server, and the size of each request when data is sent.
        Writes are implemented as a "resumable upload", so chunk_size for
        writes must be exactly a multiple of 256KiB as with other resumable
        uploads. The default is the chunk_size of the blob, or 40 MiB.

    :type text_mode: boolean
    :param text_mode:
        Whether this class is wrapped in 'io.TextIOWrapper'. Toggling this
        changes the behavior of flush() to conform to TextIOWrapper's
        expectations.

    :param upload_kwargs: Keyword arguments to pass to the underlying API
        calls. The following arguments are supported: "if_generation_match",
        "if_generation_not_match", "if_metageneration_match",
        "if_metageneration_not_match", "timeout", "content_type",
        "num_retries", "predefined_acl", "checksum".
    """

    def __init__(self, blob, chunk_size=None, text_mode=False, **upload_kwargs):
        for kwarg in upload_kwargs:
            if kwarg not in VALID_UPLOAD_KWARGS:
                raise ValueError(
                    "BlobWriter does not support keyword argument {}.".format(kwarg)
                )
        self._blob = blob
        self._buffer = SlidingBuffer()
        self._upload_and_transport = None
        # Resumable uploads require a chunk size of a multiple of 256KiB.
        # self._chunk_size must not be changed after the upload is initiated.
        self._chunk_size = chunk_size or blob.chunk_size or DEFAULT_CHUNK_SIZE
        # In text mode this class will be wrapped and TextIOWrapper requires a
        # different behavior of flush().
        self._text_mode = text_mode
        self._upload_kwargs = upload_kwargs

    @property
    def _chunk_size(self):
        """Get the blob's default chunk size.

        :rtype: int or ``NoneType``
        :returns: The current blob's chunk size, if it is set.
        """
        return self.__chunk_size

    @_chunk_size.setter
    def _chunk_size(self, value):
        """Set the blob's default chunk size.

        :type value: int
        :param value: (Optional) The current blob's chunk size, if it is set.

        :raises: :class:`ValueError` if ``value`` is not ``None`` and is not a
                 multiple of 256 KiB.
        """
        if value is not None and value > 0 and value % CHUNK_SIZE_MULTIPLE != 0:
            raise ValueError(
                "Chunk size must be a multiple of %d." % CHUNK_SIZE_MULTIPLE
            )
        self.__chunk_size = value

    def write(self, b):
        self._checkClosed()  # Raises ValueError if closed.

        pos = self._buffer.write(b)

        # If there is enough content, upload chunks.
        num_chunks = len(self._buffer) // self._chunk_size
        if num_chunks:
            self._upload_chunks_from_buffer(num_chunks)

        return pos

    def _initiate_upload(self):
        num_retries = self._upload_kwargs.pop("num_retries", None)
        content_type = self._upload_kwargs.pop("content_type", None)

        if (
            self._upload_kwargs.get("if_metageneration_match") is None
            and num_retries is None
        ):
            # Uploads are only idempotent (safe to retry) if
            # if_metageneration_match is set. If it is not set, the default
            # num_retries should be 0. Note: Because retry logic for uploads is
            # provided by the google-resumable-media-python package, it doesn't
            # use the ConditionalRetryStrategy class used in other API calls in
            # this library to solve this problem.
            num_retries = 0

        self._upload_and_transport = self._blob._initiate_resumable_upload(
            self._blob.bucket.client,
            self._buffer,
            content_type,
            None,
            num_retries,
            chunk_size=self._chunk_size,
            **self._upload_kwargs
        )

    def _upload_chunks_from_buffer(self, num_chunks):
        """Upload a specified number of chunks."""

        # Initialize the upload if necessary.
        if not self._upload_and_transport:
            self._initiate_upload()

        upload, transport = self._upload_and_transport

        # Upload chunks. The SlidingBuffer class will manage seek position.
        for _ in range(num_chunks):
            upload.transmit_next_chunk(transport)

        # Wipe the buffer of chunks uploaded, preserving any remaining data.
        self._buffer.flush()

    def tell(self):
        return self._buffer.tell() + len(self._buffer)

    def flush(self):
        if self._text_mode:
            # TextIOWrapper expects this method to succeed before calling close().
            return

        raise io.UnsupportedOperation(
            "Cannot flush without finalizing upload. Use close() instead."
        )

    def close(self):
        self._checkClosed()  # Raises ValueError if closed.

        self._upload_chunks_from_buffer(1)
        self._buffer.close()

    def _checkClosed(self):
        if self._buffer.closed:
            raise ValueError("I/O operation on closed file.")

    def readable(self):
        return False

    def writable(self):
        return True

    def seekable(self):
        return False


class SlidingBuffer(object):
    """A non-rewindable buffer that frees memory of chunks already consumed.

    This class is necessary because `google-resumable-media-python` expects
    `tell()` to work relative to the start of the file, not relative to a place
    in an intermediate buffer. Using this class, we present an external
    interface with consistent seek and tell behavior without having to actually
    store bytes already sent.

    Behavior of this class differs from an ordinary BytesIO buffer. `write()`
    will always append to the end of the file only and not change the seek
    position otherwise. `flush()` will delete all data already read (data to the
    left of the seek position). `tell()` will report the seek position of the
    buffer including all deleted data. Additionally the class implements
    __len__() which will report the size of the actual underlying buffer.

    This class does not attempt to implement the entire Python I/O interface.
    """

    def __init__(self):
        self._buffer = io.BytesIO()
        self._cursor = 0

    def write(self, b):
        """Append to the end of the buffer without changing the position."""
        self._checkClosed()  # Raises ValueError if closed.

        bookmark = self._buffer.tell()
        self._buffer.seek(0, io.SEEK_END)
        pos = self._buffer.write(b)
        self._buffer.seek(bookmark)
        return self._cursor + pos

    def read(self, size=-1):
        """Read and move the cursor."""
        self._checkClosed()  # Raises ValueError if closed.

        data = self._buffer.read(size)
        self._cursor += len(data)
        return data

    def flush(self):
        """Delete already-read data (all data to the left of the position)."""
        self._checkClosed()  # Raises ValueError if closed.

        # BytesIO can't be deleted from the left, so save any leftover, unread
        # data and truncate at 0, then readd leftover data.
        leftover = self._buffer.read()
        self._buffer.seek(0)
        self._buffer.truncate(0)
        self._buffer.write(leftover)
        self._buffer.seek(0)

    def tell(self):
        """Report how many bytes have been read from the buffer in total."""
        return self._cursor

    def seek(self, pos):
        """Seek to a position (backwards only) within the internal buffer.

        This implementation of seek() verifies that the seek destination is
        contained in _buffer. It will raise ValueError if the destination byte
        has already been purged from the buffer.

        The "whence" argument is not supported in this implementation.
        """
        self._checkClosed()  # Raises ValueError if closed.

        buffer_initial_pos = self._buffer.tell()
        difference = pos - self._cursor
        buffer_seek_result = self._buffer.seek(difference, io.SEEK_CUR)
        if (
            not buffer_seek_result - buffer_initial_pos == difference
            or pos > self._cursor
        ):
            # The seek did not arrive at the expected byte because the internal
            # buffer does not (or no longer) contains the byte. Reset and raise.
            self._buffer.seek(buffer_initial_pos)
            raise ValueError("Cannot seek() to that value.")

        self._cursor = pos
        return self._cursor

    def __len__(self):
        """Determine the size of the buffer by seeking to the end."""
        bookmark = self._buffer.tell()
        length = self._buffer.seek(0, io.SEEK_END)
        self._buffer.seek(bookmark)
        return length

    def close(self):
        return self._buffer.close()

    def _checkClosed(self):
        return self._buffer._checkClosed()

    @property
    def closed(self):
        return self._buffer.closed
