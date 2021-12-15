# coding=utf-8

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

import unittest
import io
import string

import mock

from google.api_core.exceptions import RequestRangeNotSatisfiable
from google.cloud.storage.retry import DEFAULT_RETRY

TEST_TEXT_DATA = string.ascii_lowercase + "\n" + string.ascii_uppercase + "\n"
TEST_BINARY_DATA = TEST_TEXT_DATA.encode("utf-8")
TEST_MULTIBYTE_TEXT_DATA = u"あいうえおかきくけこさしすせそたちつてと"
PLAIN_CONTENT_TYPE = "text/plain"
NUM_RETRIES = 2


class _BlobReaderBase:
    @staticmethod
    def _make_blob_reader(*args, **kwargs):
        from google.cloud.storage.fileio import BlobReader

        return BlobReader(*args, **kwargs)


class _BlobWriterBase:
    @staticmethod
    def _make_blob_writer(*args, **kwargs):
        from google.cloud.storage.fileio import BlobWriter

        return BlobWriter(*args, **kwargs)


class TestBlobReaderBinary(unittest.TestCase, _BlobReaderBase):
    def test_attributes(self):
        blob = mock.Mock()
        blob.chunk_size = 256
        reader = self._make_blob_reader(blob)
        self.assertTrue(reader.seekable())
        self.assertTrue(reader.readable())
        self.assertFalse(reader.writable())
        self.assertEqual(reader._chunk_size, 256)
        self.assertEqual(reader._retry, DEFAULT_RETRY)

    def test_attributes_explict(self):
        blob = mock.Mock()
        blob.chunk_size = 256
        reader = self._make_blob_reader(blob, chunk_size=1024, retry=None)
        self.assertEqual(reader._chunk_size, 1024)
        self.assertIsNone(reader._retry)

    def test_read(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_BINARY_DATA[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        download_kwargs = {"if_metageneration_match": 1}
        reader = self._make_blob_reader(blob, chunk_size=8, **download_kwargs)

        # Read and trigger the first download of chunk_size.
        self.assertEqual(reader.read(1), TEST_BINARY_DATA[0:1])
        blob.download_as_bytes.assert_called_once_with(
            start=0, end=8, checksum=None, retry=DEFAULT_RETRY, **download_kwargs
        )

        # Read from buffered data only.
        self.assertEqual(reader.read(3), TEST_BINARY_DATA[1:4])
        blob.download_as_bytes.assert_called_once()

        # Read remaining buffer plus an additional chunk read.
        self.assertEqual(reader.read(8), TEST_BINARY_DATA[4:12])
        self.assertEqual(reader._pos, 12)
        self.assertEqual(blob.download_as_bytes.call_count, 2)
        blob.download_as_bytes.assert_called_with(
            start=8, end=16, checksum=None, retry=DEFAULT_RETRY, **download_kwargs
        )

        # Read a larger amount, requiring a download larger than chunk_size.
        self.assertEqual(reader.read(16), TEST_BINARY_DATA[12:28])
        self.assertEqual(reader._pos, 28)
        self.assertEqual(blob.download_as_bytes.call_count, 3)
        blob.download_as_bytes.assert_called_with(
            start=16, end=28, checksum=None, retry=DEFAULT_RETRY, **download_kwargs
        )

        # Read all remaining data.
        self.assertEqual(reader.read(), TEST_BINARY_DATA[28:])
        self.assertEqual(blob.download_as_bytes.call_count, 4)
        blob.download_as_bytes.assert_called_with(
            start=28, end=None, checksum=None, retry=DEFAULT_RETRY, **download_kwargs
        )

        reader.close()

    def test_read_with_raw_download(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_BINARY_DATA[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        download_kwargs = {"raw_download": True}
        reader = self._make_blob_reader(blob, chunk_size=8, **download_kwargs)

        # Read and trigger the first download of chunk_size.
        self.assertEqual(reader.read(1), TEST_BINARY_DATA[0:1])
        blob.download_as_bytes.assert_called_once_with(
            start=0, end=8, checksum=None, retry=DEFAULT_RETRY, raw_download=True
        )

        reader.close()

    def test_retry_passed_through(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_BINARY_DATA[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        download_kwargs = {"if_metageneration_match": 1}
        reader = self._make_blob_reader(
            blob, chunk_size=8, retry=None, **download_kwargs
        )

        # Read and trigger the first download of chunk_size.
        self.assertEqual(reader.read(1), TEST_BINARY_DATA[0:1])
        blob.download_as_bytes.assert_called_once_with(
            start=0, end=8, checksum=None, retry=None, **download_kwargs
        )

        reader.close()

    def test_416_error_handled(self):
        blob = mock.Mock()
        blob.download_as_bytes = mock.Mock(
            side_effect=RequestRangeNotSatisfiable("message")
        )

        reader = self._make_blob_reader(blob)
        self.assertEqual(reader.read(), b"")

    def test_readline(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_BINARY_DATA[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        reader = self._make_blob_reader(blob, chunk_size=10)

        # Read a line. With chunk_size=10, expect three chunks downloaded.
        self.assertEqual(reader.readline(), TEST_BINARY_DATA[:27])
        blob.download_as_bytes.assert_called_with(
            start=20, end=30, checksum=None, retry=DEFAULT_RETRY
        )
        self.assertEqual(blob.download_as_bytes.call_count, 3)

        # Read another line.
        self.assertEqual(reader.readline(), TEST_BINARY_DATA[27:])
        blob.download_as_bytes.assert_called_with(
            start=50, end=60, checksum=None, retry=DEFAULT_RETRY
        )
        self.assertEqual(blob.download_as_bytes.call_count, 6)

        blob.size = len(TEST_BINARY_DATA)
        reader.seek(0)

        # Read all lines. The readlines algorithm will attempt to read past the end of the last line once to verify there is no more to read.
        self.assertEqual(b"".join(reader.readlines()), TEST_BINARY_DATA)
        blob.download_as_bytes.assert_called_with(
            start=len(TEST_BINARY_DATA),
            end=len(TEST_BINARY_DATA) + 10,
            checksum=None,
            retry=DEFAULT_RETRY,
        )
        self.assertEqual(blob.download_as_bytes.call_count, 13)

        reader.close()

    def test_seek(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_BINARY_DATA[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        blob.size = None
        download_kwargs = {"if_metageneration_match": 1}
        reader = self._make_blob_reader(blob, chunk_size=8, **download_kwargs)

        # Seek needs the blob size to work and should call reload() if the size
        # is not known. Set a mock to initialize the size if reload() is called.
        def initialize_size(**_):
            blob.size = len(TEST_BINARY_DATA)

        blob.reload = mock.Mock(side_effect=initialize_size)

        # Seek, forcing a blob reload in order to validate the seek doesn't
        # exceed the end of the blob.
        self.assertEqual(reader.seek(4), 4)
        blob.reload.assert_called_once_with(**download_kwargs)
        self.assertEqual(reader.read(4), TEST_BINARY_DATA[4:8])
        self.assertEqual(blob.download_as_bytes.call_count, 1)

        # Seek forward 2 bytes with whence=1. Position is still in buffer.
        self.assertEqual(reader.seek(2, 1), 10)
        self.assertEqual(reader.read(2), TEST_BINARY_DATA[10:12])
        self.assertEqual(blob.download_as_bytes.call_count, 1)

        # Attempt seek past end of file. Position should be at end of file.
        self.assertEqual(
            reader.seek(len(TEST_BINARY_DATA) + 100), len(TEST_BINARY_DATA)
        )

        # Seek to beginning. The next read will need to download data again.
        self.assertEqual(reader.seek(0), 0)
        self.assertEqual(reader.read(4), TEST_BINARY_DATA[0:4])
        self.assertEqual(blob.download_as_bytes.call_count, 2)

        # Seek relative to end with whence=2.
        self.assertEqual(reader.seek(-1, 2), len(TEST_BINARY_DATA) - 1)
        self.assertEqual(reader.read(), TEST_BINARY_DATA[-1:])
        self.assertEqual(blob.download_as_bytes.call_count, 3)

        with self.assertRaises(ValueError):
            reader.seek(1, 4)

        # tell() is an inherited method that uses seek().
        self.assertEqual(reader.tell(), reader._pos)

        reader.close()

    def test_close(self):
        blob = mock.Mock()
        reader = self._make_blob_reader(blob)

        reader.close()

        with self.assertRaises(ValueError):
            reader.read()

        with self.assertRaises(ValueError):
            reader.seek(0)

    def test_context_mgr(self):
        # Just very that the context manager form doesn't crash.
        blob = mock.Mock()
        with self._make_blob_reader(blob) as reader:
            reader.close()

    def test_rejects_invalid_kwargs(self):
        blob = mock.Mock()
        with self.assertRaises(ValueError):
            self._make_blob_reader(blob, invalid_kwarg=1)


class TestBlobWriterBinary(unittest.TestCase, _BlobWriterBase):
    def test_attributes(self):
        blob = mock.Mock()
        blob.chunk_size = 256 * 1024
        writer = self._make_blob_writer(blob)
        self.assertFalse(writer.seekable())
        self.assertFalse(writer.readable())
        self.assertTrue(writer.writable())
        self.assertEqual(writer._chunk_size, 256 * 1024)

    def test_attributes_explicit(self):
        blob = mock.Mock()
        blob.chunk_size = 256 * 1024
        writer = self._make_blob_writer(
            blob, chunk_size=512 * 1024, retry=DEFAULT_RETRY
        )
        self.assertEqual(writer._chunk_size, 512 * 1024)
        self.assertEqual(writer._retry, DEFAULT_RETRY)

    def test_deprecated_text_mode_attribute(self):
        blob = mock.Mock()
        blob.chunk_size = 256 * 1024
        writer = self._make_blob_writer(blob, text_mode=True)
        self.assertTrue(writer._ignore_flush)
        writer.flush()  # This should do nothing and not raise an error.

    def test_reject_wrong_chunk_size(self):
        blob = mock.Mock()
        blob.chunk_size = 123
        with self.assertRaises(ValueError):
            _ = self._make_blob_writer(blob)

    @mock.patch("warnings.warn")
    def test_write(self, mock_warn):
        from google.cloud.storage._helpers import _NUM_RETRIES_MESSAGE

        blob = mock.Mock()
        upload = mock.Mock()
        transport = mock.Mock()

        blob._initiate_resumable_upload.return_value = (upload, transport)

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer with (arbitrary) arguments so we can validate the
            # arguments are used.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            upload_kwargs = {"if_metageneration_match": 1}
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            writer = self._make_blob_writer(
                blob,
                chunk_size=chunk_size,
                num_retries=NUM_RETRIES,
                content_type=PLAIN_CONTENT_TYPE,
                **upload_kwargs
            )

        # The transmit_next_chunk method must actually consume bytes from the
        # sliding buffer for the flush() feature to work properly.
        upload.transmit_next_chunk.side_effect = lambda _: writer._buffer.read(
            chunk_size
        )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_BINARY_DATA[0:4])
        blob.initiate_resumable_upload.assert_not_called()

        # Write over chunk_size. This should result in upload initialization
        # and multiple chunks uploaded.
        writer.write(TEST_BINARY_DATA[4:32])
        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,
            NUM_RETRIES,
            chunk_size=chunk_size,
            retry=None,
            **upload_kwargs
        )
        upload.transmit_next_chunk.assert_called_with(transport)
        self.assertEqual(upload.transmit_next_chunk.call_count, 4)

        # Write another byte, finalize and close.
        writer.write(TEST_BINARY_DATA[32:33])
        self.assertEqual(writer.tell(), 33)
        writer.close()
        self.assertEqual(upload.transmit_next_chunk.call_count, 5)

        mock_warn.assert_called_once_with(
            _NUM_RETRIES_MESSAGE, DeprecationWarning, stacklevel=2,
        )

    def test_flush_fails(self):
        blob = mock.Mock(chunk_size=None)
        writer = self._make_blob_writer(blob)

        with self.assertRaises(io.UnsupportedOperation):
            writer.flush()

    def test_seek_fails(self):
        blob = mock.Mock(chunk_size=None)
        writer = self._make_blob_writer(blob)

        with self.assertRaises(io.UnsupportedOperation):
            writer.seek()

    def test_conditional_retry_failure(self):
        blob = mock.Mock()

        upload = mock.Mock()
        transport = mock.Mock()

        blob._initiate_resumable_upload.return_value = (upload, transport)

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            writer = self._make_blob_writer(
                blob, chunk_size=chunk_size, content_type=PLAIN_CONTENT_TYPE,
            )

        # The transmit_next_chunk method must actually consume bytes from the
        # sliding buffer for the flush() feature to work properly.
        upload.transmit_next_chunk.side_effect = lambda _: writer._buffer.read(
            chunk_size
        )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_BINARY_DATA[0:4])
        blob.initiate_resumable_upload.assert_not_called()

        # Write over chunk_size. This should result in upload initialization
        # and multiple chunks uploaded.
        # Due to the condition not being fulfilled, retry should be None.
        writer.write(TEST_BINARY_DATA[4:32])
        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,  # size
            None,  # num_retries
            chunk_size=chunk_size,
            retry=None,
        )
        upload.transmit_next_chunk.assert_called_with(transport)
        self.assertEqual(upload.transmit_next_chunk.call_count, 4)

        # Write another byte, finalize and close.
        writer.write(TEST_BINARY_DATA[32:33])
        writer.close()
        self.assertEqual(upload.transmit_next_chunk.call_count, 5)

    def test_conditional_retry_pass(self):
        blob = mock.Mock()

        upload = mock.Mock()
        transport = mock.Mock()

        blob._initiate_resumable_upload.return_value = (upload, transport)

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            writer = self._make_blob_writer(
                blob,
                chunk_size=chunk_size,
                content_type=PLAIN_CONTENT_TYPE,
                if_generation_match=123456,
            )

        # The transmit_next_chunk method must actually consume bytes from the
        # sliding buffer for the flush() feature to work properly.
        upload.transmit_next_chunk.side_effect = lambda _: writer._buffer.read(
            chunk_size
        )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_BINARY_DATA[0:4])
        blob.initiate_resumable_upload.assert_not_called()

        # Write over chunk_size. This should result in upload initialization
        # and multiple chunks uploaded.
        # Due to the condition being fulfilled, retry should be DEFAULT_RETRY.
        writer.write(TEST_BINARY_DATA[4:32])
        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,  # size
            None,  # num_retries
            chunk_size=chunk_size,
            retry=DEFAULT_RETRY,
            if_generation_match=123456,
        )
        upload.transmit_next_chunk.assert_called_with(transport)
        self.assertEqual(upload.transmit_next_chunk.call_count, 4)

        # Write another byte, finalize and close.
        writer.write(TEST_BINARY_DATA[32:33])
        writer.close()
        self.assertEqual(upload.transmit_next_chunk.call_count, 5)

    def test_forced_default_retry(self):
        blob = mock.Mock()

        upload = mock.Mock()
        transport = mock.Mock()

        blob._initiate_resumable_upload.return_value = (upload, transport)

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            writer = self._make_blob_writer(
                blob,
                chunk_size=chunk_size,
                content_type=PLAIN_CONTENT_TYPE,
                retry=DEFAULT_RETRY,
            )

        # The transmit_next_chunk method must actually consume bytes from the
        # sliding buffer for the flush() feature to work properly.
        upload.transmit_next_chunk.side_effect = lambda _: writer._buffer.read(
            chunk_size
        )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_BINARY_DATA[0:4])
        blob.initiate_resumable_upload.assert_not_called()

        # Write over chunk_size. This should result in upload initialization
        # and multiple chunks uploaded.
        writer.write(TEST_BINARY_DATA[4:32])
        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,  # size
            None,  # num_retries
            chunk_size=chunk_size,
            retry=DEFAULT_RETRY,
        )
        upload.transmit_next_chunk.assert_called_with(transport)
        self.assertEqual(upload.transmit_next_chunk.call_count, 4)

        # Write another byte, finalize and close.
        writer.write(TEST_BINARY_DATA[32:33])
        writer.close()
        self.assertEqual(upload.transmit_next_chunk.call_count, 5)

    @mock.patch("warnings.warn")
    def test_num_retries_and_retry_conflict(self, mock_warn):
        from google.cloud.storage._helpers import _NUM_RETRIES_MESSAGE

        blob = mock.Mock()

        blob._initiate_resumable_upload.side_effect = ValueError

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            writer = self._make_blob_writer(
                blob,
                chunk_size=chunk_size,
                content_type=PLAIN_CONTENT_TYPE,
                num_retries=2,
                retry=DEFAULT_RETRY,
            )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_BINARY_DATA[0:4])
        blob.initiate_resumable_upload.assert_not_called()

        # Write over chunk_size. The mock will raise a ValueError, simulating
        # actual behavior when num_retries and retry are both specified.
        with self.assertRaises(ValueError):
            writer.write(TEST_BINARY_DATA[4:32])

        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,  # size
            2,  # num_retries
            chunk_size=chunk_size,
            retry=DEFAULT_RETRY,
        )

        mock_warn.assert_called_once_with(
            _NUM_RETRIES_MESSAGE, DeprecationWarning, stacklevel=2,
        )

    @mock.patch("warnings.warn")
    def test_num_retries_only(self, mock_warn):
        from google.cloud.storage._helpers import _NUM_RETRIES_MESSAGE

        blob = mock.Mock()
        upload = mock.Mock()
        transport = mock.Mock()

        blob._initiate_resumable_upload.return_value = (upload, transport)

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            writer = self._make_blob_writer(
                blob,
                chunk_size=chunk_size,
                content_type=PLAIN_CONTENT_TYPE,
                num_retries=2,
            )

        # The transmit_next_chunk method must actually consume bytes from the
        # sliding buffer for the flush() feature to work properly.
        upload.transmit_next_chunk.side_effect = lambda _: writer._buffer.read(
            chunk_size
        )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_BINARY_DATA[0:4])
        blob.initiate_resumable_upload.assert_not_called()

        # Write over chunk_size. This should result in upload initialization
        # and multiple chunks uploaded.
        writer.write(TEST_BINARY_DATA[4:32])
        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,  # size
            2,  # num_retries
            chunk_size=chunk_size,
            retry=None,
        )
        upload.transmit_next_chunk.assert_called_with(transport)
        self.assertEqual(upload.transmit_next_chunk.call_count, 4)

        mock_warn.assert_called_once_with(
            _NUM_RETRIES_MESSAGE, DeprecationWarning, stacklevel=2
        )

        # Write another byte, finalize and close.
        writer.write(TEST_BINARY_DATA[32:33])
        writer.close()
        self.assertEqual(upload.transmit_next_chunk.call_count, 5)

    def test_rejects_invalid_kwargs(self):
        blob = mock.Mock()
        with self.assertRaises(ValueError):
            self._make_blob_writer(blob, invalid_kwarg=1)


class Test_SlidingBuffer(unittest.TestCase):
    @staticmethod
    def _make_sliding_buffer(*args, **kwargs):
        from google.cloud.storage.fileio import SlidingBuffer

        return SlidingBuffer(*args, **kwargs)

    def test_write_and_read(self):
        buff = self._make_sliding_buffer()

        # Write and verify tell() still reports 0 and len is correct.
        buff.write(TEST_BINARY_DATA)
        self.assertEqual(buff.tell(), 0)
        self.assertEqual(len(buff), len(TEST_BINARY_DATA))

        # Read and verify tell() reports end.
        self.assertEqual(buff.read(), TEST_BINARY_DATA)
        self.assertEqual(buff.tell(), len(TEST_BINARY_DATA))
        self.assertEqual(len(buff), len(TEST_BINARY_DATA))

    def test_flush(self):
        buff = self._make_sliding_buffer()

        # Write and verify tell() still reports 0 and len is correct.
        buff.write(TEST_BINARY_DATA)
        self.assertEqual(buff.tell(), 0)
        self.assertEqual(len(buff), len(TEST_BINARY_DATA))

        # Read 8 bytes and verify tell reports correctly.
        self.assertEqual(buff.read(8), TEST_BINARY_DATA[:8])
        self.assertEqual(buff.tell(), 8)
        self.assertEqual(len(buff), len(TEST_BINARY_DATA))

        # Flush buffer and verify tell doesn't change but len does.
        buff.flush()
        self.assertEqual(buff.tell(), 8)
        self.assertEqual(len(buff), len(TEST_BINARY_DATA) - 8)

        # Read remainder.
        self.assertEqual(buff.read(), TEST_BINARY_DATA[8:])
        self.assertEqual(buff.tell(), len(TEST_BINARY_DATA))
        self.assertEqual(len(buff), len(TEST_BINARY_DATA[8:]))

    def test_seek(self):
        buff = self._make_sliding_buffer()
        buff.write(TEST_BINARY_DATA)

        # Try to seek forward. Verify the tell() doesn't change.
        with self.assertRaises(ValueError):
            pos = buff.tell()
            buff.seek(len(TEST_BINARY_DATA) + 1)
        self.assertEqual(pos, buff.tell())

        # Read 8 bytes, test seek backwards, read again, and flush.
        self.assertEqual(buff.read(8), TEST_BINARY_DATA[:8])
        buff.seek(0)
        self.assertEqual(buff.read(8), TEST_BINARY_DATA[:8])
        buff.flush()
        self.assertEqual(buff.tell(), 8)

        # Try to seek to a byte that has already been flushed.
        with self.assertRaises(ValueError):
            pos = buff.tell()
            buff.seek(0)
        self.assertEqual(pos, buff.tell())

    def test_close(self):
        buff = self._make_sliding_buffer()
        buff.close()
        with self.assertRaises(ValueError):
            buff.read()


class TestBlobReaderText(unittest.TestCase, _BlobReaderBase):
    def test_attributes(self):
        blob = mock.Mock()
        reader = io.TextIOWrapper(self._make_blob_reader(blob))
        self.assertTrue(reader.seekable())
        self.assertTrue(reader.readable())
        self.assertFalse(reader.writable())

    def test_read(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_TEXT_DATA.encode("utf-8")[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        blob.chunk_size = None
        blob.size = len(TEST_TEXT_DATA.encode("utf-8"))
        download_kwargs = {"if_metageneration_match": 1}
        reader = io.TextIOWrapper(self._make_blob_reader(blob, **download_kwargs))

        # The TextIOWrapper class has an internally defined chunk size which
        # will override ours. The wrapper class is not under test.
        # Read and trigger the first download of chunk_size.
        self.assertEqual(reader.read(1), TEST_TEXT_DATA[0:1])
        blob.download_as_bytes.assert_called_once()

        # Read from buffered data only.
        self.assertEqual(reader.read(3), TEST_TEXT_DATA[1:4])
        blob.download_as_bytes.assert_called_once()

        # Read all remaining data.
        self.assertEqual(reader.read(), TEST_TEXT_DATA[4:])

        # Seek to 0 and read all remaining data again.
        reader.seek(0)
        self.assertEqual(reader.read(), TEST_TEXT_DATA)

        reader.close()

    def test_multibyte_read(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_MULTIBYTE_TEXT_DATA.encode("utf-8")[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        blob.chunk_size = None
        blob.size = len(TEST_MULTIBYTE_TEXT_DATA.encode("utf-8"))
        download_kwargs = {"if_metageneration_match": 1}
        reader = io.TextIOWrapper(self._make_blob_reader(blob, **download_kwargs))

        # The TextIOWrapper class has an internally defined chunk size which
        # will override ours. The wrapper class is not under test.
        # Read and trigger the first download of chunk_size.
        self.assertEqual(reader.read(1), TEST_MULTIBYTE_TEXT_DATA[0:1])
        blob.download_as_bytes.assert_called_once()

        # Read from buffered data only.
        self.assertEqual(reader.read(3), TEST_MULTIBYTE_TEXT_DATA[1:4])
        blob.download_as_bytes.assert_called_once()

        # Read all remaining data.
        self.assertEqual(reader.read(), TEST_MULTIBYTE_TEXT_DATA[4:])

        # Seek to 0 and read all remaining data again.
        reader.seek(0)
        self.assertEqual(reader.read(), TEST_MULTIBYTE_TEXT_DATA)

        reader.close()

    def test_seek(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_TEXT_DATA.encode("utf-8")[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        blob.size = None
        blob.chunk_size = None
        download_kwargs = {"if_metageneration_match": 1}
        reader = io.TextIOWrapper(self._make_blob_reader(blob, **download_kwargs))

        # Seek needs the blob size to work and should call reload() if the size
        # is not known. Set a mock to initialize the size if reload() is called.
        def initialize_size(**_):
            blob.size = len(TEST_TEXT_DATA.encode("utf-8"))

        blob.reload = mock.Mock(side_effect=initialize_size)

        # Seek, forcing a blob reload in order to validate the seek doesn't
        # exceed the end of the blob.
        self.assertEqual(reader.seek(4), 4)
        blob.reload.assert_called_once_with(**download_kwargs)
        self.assertEqual(reader.read(4), TEST_TEXT_DATA[4:8])
        self.assertEqual(blob.download_as_bytes.call_count, 1)

        # Seek to beginning. The next read will need to download data again.
        self.assertEqual(reader.seek(0), 0)
        self.assertEqual(reader.read(), TEST_TEXT_DATA)
        self.assertEqual(blob.download_as_bytes.call_count, 2)

        reader.close()

    def test_multibyte_seek(self):
        blob = mock.Mock()

        def read_from_fake_data(start=0, end=None, **_):
            return TEST_MULTIBYTE_TEXT_DATA.encode("utf-8")[start:end]

        blob.download_as_bytes = mock.Mock(side_effect=read_from_fake_data)
        blob.size = None
        blob.chunk_size = None
        download_kwargs = {"if_metageneration_match": 1}
        reader = io.TextIOWrapper(self._make_blob_reader(blob, **download_kwargs))

        # Seek needs the blob size to work and should call reload() if the size
        # is not known. Set a mock to initialize the size if reload() is called.
        def initialize_size(**_):
            blob.size = len(TEST_MULTIBYTE_TEXT_DATA.encode("utf-8"))

        blob.reload = mock.Mock(side_effect=initialize_size)

        # Seek, forcing a blob reload in order to validate the seek doesn't
        # exceed the end of the blob.
        self.assertEqual(reader.seek(4), 4)
        blob.reload.assert_called_once_with(**download_kwargs)

        # Seek to beginning.
        self.assertEqual(reader.seek(0), 0)
        self.assertEqual(reader.read(), TEST_MULTIBYTE_TEXT_DATA)
        self.assertEqual(blob.download_as_bytes.call_count, 1)

        # tell() is an inherited method that uses seek().
        self.assertEqual(reader.tell(), len(TEST_MULTIBYTE_TEXT_DATA.encode("utf-8")))

        reader.close()

    def test_close(self):
        blob = mock.Mock()
        reader = self._make_blob_reader(blob)

        reader.close()

        with self.assertRaises(ValueError):
            reader.read()

        with self.assertRaises(ValueError):
            reader.seek(0)


class TestBlobWriterText(unittest.TestCase, _BlobWriterBase):
    @mock.patch("warnings.warn")
    def test_write(self, mock_warn):
        from google.cloud.storage._helpers import _NUM_RETRIES_MESSAGE

        blob = mock.Mock()
        upload = mock.Mock()
        transport = mock.Mock()

        blob._initiate_resumable_upload.return_value = (upload, transport)

        with mock.patch("google.cloud.storage.fileio.CHUNK_SIZE_MULTIPLE", 1):
            # Create a writer in text mode.
            # It would be normal to use a context manager here, but not doing so
            # gives us more control over close() for test purposes.
            chunk_size = 8  # Note: Real upload requires a multiple of 256KiB.
            unwrapped_writer = self._make_blob_writer(
                blob,
                chunk_size=chunk_size,
                ignore_flush=True,
                num_retries=NUM_RETRIES,
                content_type=PLAIN_CONTENT_TYPE,
            )

        writer = io.TextIOWrapper(unwrapped_writer)

        # The transmit_next_chunk method must actually consume bytes from the
        # sliding buffer for the flush() feature to work properly.
        upload.transmit_next_chunk.side_effect = lambda _: unwrapped_writer._buffer.read(
            chunk_size
        )

        # Write under chunk_size. This should be buffered and the upload not
        # initiated.
        writer.write(TEST_MULTIBYTE_TEXT_DATA[0:2])
        blob.initiate_resumable_upload.assert_not_called()

        # Write all data and close.
        writer.write(TEST_MULTIBYTE_TEXT_DATA[2:])
        writer.close()

        blob._initiate_resumable_upload.assert_called_once_with(
            blob.bucket.client,
            unwrapped_writer._buffer,
            PLAIN_CONTENT_TYPE,
            None,
            NUM_RETRIES,
            chunk_size=chunk_size,
            retry=None,
        )
        upload.transmit_next_chunk.assert_called_with(transport)

        mock_warn.assert_called_once_with(
            _NUM_RETRIES_MESSAGE, DeprecationWarning, stacklevel=2,
        )
