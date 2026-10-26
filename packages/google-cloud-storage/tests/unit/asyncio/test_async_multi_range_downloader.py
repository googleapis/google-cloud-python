# Copyright 2025 Google LLC
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

import asyncio
from io import BytesIO
from unittest import mock
from unittest.mock import AsyncMock

import google_crc32c
import pytest
from google.api_core import exceptions
from google.rpc import error_details_pb2, status_pb2

from google.cloud import _storage_v2
from google.cloud.storage.asyncio import async_read_object_stream
from google.cloud.storage.asyncio.async_multi_range_downloader import (
    AsyncMultiRangeDownloader,
)
from google.cloud.storage.exceptions import DataCorruption

_TEST_BUCKET_NAME = "test-bucket"
_TEST_OBJECT_NAME = "test-object"
_TEST_OBJECT_SIZE = 1024 * 1024  # 1 MiB
_TEST_GENERATION_NUMBER = 123456789
_TEST_READ_HANDLE = b"test-handle"


class TestAsyncMultiRangeDownloader:
    def create_read_ranges(self, num_ranges):
        ranges = []
        for i in range(num_ranges):
            ranges.append((i, 1, BytesIO()))
        return ranges

    # helper method
    @pytest.mark.asyncio
    async def _make_mock_mrd(
        self,
        mock_cls_async_read_object_stream,
        bucket_name=_TEST_BUCKET_NAME,
        object_name=_TEST_OBJECT_NAME,
        generation=_TEST_GENERATION_NUMBER,
        read_handle=_TEST_READ_HANDLE,
    ):
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()
        mock_stream.generation_number = _TEST_GENERATION_NUMBER
        mock_stream.persisted_size = _TEST_OBJECT_SIZE
        mock_stream.read_handle = _TEST_READ_HANDLE
        mock_stream.object_metadata = mock.Mock()

        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client, bucket_name, object_name, generation, read_handle
        )

        return mrd, mock_client

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_create_mrd(self, mock_cls_async_read_object_stream):
        # Arrange & Act
        mrd, mock_client = await self._make_mock_mrd(mock_cls_async_read_object_stream)

        # Assert
        mock_cls_async_read_object_stream.assert_called_once_with(
            client=mock_client.grpc_client,
            bucket_name=_TEST_BUCKET_NAME,
            object_name=_TEST_OBJECT_NAME,
            generation_number=_TEST_GENERATION_NUMBER,
            read_handle=_TEST_READ_HANDLE,
        )

        mrd.read_obj_str.open.assert_called_once()

        assert mrd.client == mock_client
        assert mrd.bucket_name == _TEST_BUCKET_NAME
        assert mrd.object_name == _TEST_OBJECT_NAME
        assert mrd.generation == _TEST_GENERATION_NUMBER
        assert mrd.read_handle == _TEST_READ_HANDLE
        assert mrd.persisted_size == _TEST_OBJECT_SIZE
        assert mrd.is_stream_open
        assert mrd.object_metadata == mrd.read_obj_str.object_metadata
        assert mrd._open_retries == 0

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_download_ranges_via_async_gather(
        self, mock_cls_async_read_object_stream, mock_random_int
    ):
        data = b"these_are_18_chars"
        crc32c_int = google_crc32c.value(data)
        crc32c_checksum_for_data_slice = google_crc32c.value(data[10:16])

        mock_mrd, _ = await self._make_mock_mrd(mock_cls_async_read_object_stream)
        mock_random_int.side_effect = [456, 91011]

        send_count = 0
        both_sent = asyncio.Event()

        async def counting_send(request):
            nonlocal send_count
            send_count += 1
            if send_count >= 2:
                both_sent.set()

        mock_mrd.read_obj_str.send = AsyncMock(side_effect=counting_send)

        recv_call_count = 0

        async def controlled_recv():
            nonlocal recv_call_count
            recv_call_count += 1
            if recv_call_count == 1:
                await both_sent.wait()
                return _storage_v2.BidiReadObjectResponse(
                    object_data_ranges=[
                        _storage_v2.ObjectRangeData(
                            checksummed_data=_storage_v2.ChecksummedData(
                                content=data, crc32c=crc32c_int
                            ),
                            range_end=True,
                            read_range=_storage_v2.ReadRange(
                                read_offset=0, read_length=18, read_id=456
                            ),
                        )
                    ]
                )
            elif recv_call_count == 2:
                return _storage_v2.BidiReadObjectResponse(
                    object_data_ranges=[
                        _storage_v2.ObjectRangeData(
                            checksummed_data=_storage_v2.ChecksummedData(
                                content=data[10:16],
                                crc32c=crc32c_checksum_for_data_slice,
                            ),
                            range_end=True,
                            read_range=_storage_v2.ReadRange(
                                read_offset=10, read_length=6, read_id=91011
                            ),
                        )
                    ],
                )
            return None

        mock_mrd.read_obj_str.recv = AsyncMock(side_effect=controlled_recv)

        buffer = BytesIO()
        second_buffer = BytesIO()

        task1 = asyncio.create_task(mock_mrd.download_ranges([(0, 18, buffer)]))
        task2 = asyncio.create_task(mock_mrd.download_ranges([(10, 6, second_buffer)]))
        await asyncio.gather(task1, task2)

        assert buffer.getvalue() == data
        assert second_buffer.getvalue() == data[10:16]

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_download_ranges(
        self, mock_cls_async_read_object_stream, mock_random_int
    ):
        # Arrange
        data = b"these_are_18_chars"
        crc32c_int = google_crc32c.value(data)

        mock_mrd, _ = await self._make_mock_mrd(mock_cls_async_read_object_stream)
        mock_random_int.side_effect = [456]

        mock_mrd.read_obj_str.send = AsyncMock()
        mock_mrd.read_obj_str.recv = AsyncMock()
        mock_mrd.read_obj_str.recv.side_effect = [
            _storage_v2.BidiReadObjectResponse(
                object_data_ranges=[
                    _storage_v2.ObjectRangeData(
                        checksummed_data=_storage_v2.ChecksummedData(
                            content=data, crc32c=crc32c_int
                        ),
                        range_end=True,
                        read_range=_storage_v2.ReadRange(
                            read_offset=0, read_length=18, read_id=456
                        ),
                    )
                ],
            ),
            None,
        ]
        # Act
        buffer = BytesIO()

        await mock_mrd.download_ranges([(0, 18, buffer)])

        # Assert
        mock_mrd.read_obj_str.send.assert_called_once_with(
            _storage_v2.BidiReadObjectRequest(
                read_ranges=[
                    _storage_v2.ReadRange(read_offset=0, read_length=18, read_id=456)
                ]
            )
        )
        assert buffer.getvalue() == data

    @pytest.mark.asyncio
    async def test_downloading_ranges_with_more_than_1000_should_throw_error(self):
        # Arrange
        mock_client = mock.MagicMock()
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.download_ranges(self.create_read_ranges(1001))

        # Assert
        assert (
            str(exc.value)
            == "Invalid input - length of read_ranges cannot be more than 1000"
        )

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_opening_mrd_more_than_once_should_throw_error(
        self, mock_cls_async_read_object_stream
    ):
        # Arrange
        mrd, _ = await self._make_mock_mrd(
            mock_cls_async_read_object_stream
        )  # mock mrd is already opened

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.open()

        # Assert
        assert str(exc.value) == "Underlying bidi-gRPC stream is already open"

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_close_mrd(self, mock_cls_async_read_object_stream):
        # Arrange
        mrd, _ = await self._make_mock_mrd(
            mock_cls_async_read_object_stream
        )  # mock mrd is already opened
        mrd.read_obj_str.close = AsyncMock()

        # Act
        await mrd.close()

        # Assert
        assert not mrd.is_stream_open
        assert mrd.object_metadata is None

    @pytest.mark.asyncio
    async def test_close_mrd_not_opened_should_throw_error(self):
        # Arrange
        mock_client = mock.MagicMock()
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.close()

        # Assert
        assert str(exc.value) == "Underlying bidi-gRPC stream is not open"
        assert not mrd.is_stream_open

    @pytest.mark.asyncio
    async def test_downloading_without_opening_should_throw_error(self):
        # Arrange
        mock_client = mock.MagicMock()
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )

        # Act + Assert
        with pytest.raises(ValueError) as exc:
            await mrd.download_ranges([(0, 18, BytesIO())])

        # Assert
        assert str(exc.value) == "Underlying bidi-gRPC stream is not open"
        assert not mrd.is_stream_open

    @mock.patch("google.cloud.storage.asyncio._utils.google_crc32c")
    @pytest.mark.asyncio
    async def test_download_ranges_raises_if_crc32c_c_extension_is_missing(
        self, mock_google_crc32c
    ):
        mock_google_crc32c.implementation = "python"
        mock_client = mock.MagicMock()
        mrd = AsyncMultiRangeDownloader(mock_client, "bucket", "object")

        with pytest.raises(exceptions.FailedPrecondition) as exc_info:
            await mrd.download_ranges([(0, 10, BytesIO())])

        assert "The google-crc32c package is not installed with C support" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    @mock.patch(
        "google.cloud.storage.asyncio.retry.reads_resumption_strategy.google_crc32c.value"
    )
    async def test_download_ranges_raises_on_checksum_mismatch(self, mock_crc32c_value):
        from google.cloud.storage.asyncio._stream_multiplexer import _StreamMultiplexer
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            AsyncMultiRangeDownloader,
        )

        mock_client = mock.MagicMock()
        mock_stream = mock.AsyncMock(
            spec=async_read_object_stream._AsyncReadObjectStream
        )

        test_data = b"some-data"
        server_checksum = 12345
        mock_crc32c_value.return_value = 54321

        mock_response = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=test_data, crc32c=server_checksum
                    ),
                    read_range=_storage_v2.ReadRange(
                        read_id=0, read_offset=0, read_length=len(test_data)
                    ),
                    range_end=True,
                )
            ]
        )

        mock_stream.recv.side_effect = [mock_response, None]

        mrd = AsyncMultiRangeDownloader(mock_client, "bucket", "object")
        mrd.read_obj_str = mock_stream
        mrd._is_stream_open = True
        mrd._multiplexer = _StreamMultiplexer(mock_stream)

        with pytest.raises(DataCorruption) as exc_info:
            with mock.patch(
                "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer",
                return_value=0,
            ):
                await mrd.download_ranges([(0, len(test_data), BytesIO())])

        assert "Checksum mismatch" in str(exc_info.value)
        mock_crc32c_value.assert_called_once_with(test_data)

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.AsyncMultiRangeDownloader.open",
        new_callable=AsyncMock,
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.AsyncMultiRangeDownloader.close",
        new_callable=AsyncMock,
    )
    @pytest.mark.asyncio
    async def test_async_context_manager_calls_open_and_close(
        self, mock_close, mock_open
    ):
        # Arrange
        mock_client = mock.MagicMock()
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )

        # To simulate the behavior of open and close changing the stream state
        async def open_side_effect():
            mrd._is_stream_open = True

        async def close_side_effect():
            mrd._is_stream_open = False

        mock_open.side_effect = open_side_effect
        mock_close.side_effect = close_side_effect
        mrd._is_stream_open = False

        # Act
        async with mrd as downloader:
            # Assert
            mock_open.assert_called_once()
            assert downloader == mrd
            assert mrd.is_stream_open

        mock_close.assert_called_once()
        assert not mrd.is_stream_open

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_create_mrd_with_generation_number(
        self, mock_cls_async_read_object_stream, caplog
    ):
        # Arrange
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()
        mock_stream.generation_number = _TEST_GENERATION_NUMBER
        mock_stream.persisted_size = _TEST_OBJECT_SIZE
        mock_stream.read_handle = _TEST_READ_HANDLE

        # Act
        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client,
            _TEST_BUCKET_NAME,
            _TEST_OBJECT_NAME,
            generation_number=_TEST_GENERATION_NUMBER,
            read_handle=_TEST_READ_HANDLE,
        )

        # Assert
        assert mrd.generation == _TEST_GENERATION_NUMBER
        assert mrd.read_handle == _TEST_READ_HANDLE
        assert mrd.persisted_size == _TEST_OBJECT_SIZE
        assert "'generation_number' is deprecated" in caplog.text

    @pytest.mark.asyncio
    async def test_create_mrd_with_both_generation_and_generation_number(self):
        # Arrange
        mock_client = mock.MagicMock()

        # Act & Assert
        with pytest.raises(TypeError):
            await AsyncMultiRangeDownloader.create_mrd(
                mock_client,
                _TEST_BUCKET_NAME,
                _TEST_OBJECT_NAME,
                generation=_TEST_GENERATION_NUMBER,
                generation_number=_TEST_GENERATION_NUMBER,
            )

    @mock.patch("google.cloud.storage.asyncio.async_multi_range_downloader.AsyncRetry")
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_open_retries_increment(
        self, mock_cls_async_read_object_stream, mock_async_retry
    ):
        # Arrange
        # Configure AsyncRetry mock to return a pass-through decorator so we can await the result
        mock_policy = mock.MagicMock()
        mock_policy.side_effect = lambda f: f
        mock_async_retry.return_value = mock_policy

        mrd, _ = await self._make_mock_mrd(mock_cls_async_read_object_stream)
        # _make_mock_mrd calls create_mrd -> open.
        # We need to test logic where retry happens.

        # Create fresh MRD
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        # Mock stream
        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()

        # Action: We want to capture the on_error passed to AsyncRetry
        await mrd.open()

        # Assert
        # Check that AsyncRetry was initialized with a wrapper
        call_args = mock_async_retry.call_args
        assert call_args is not None
        _, kwargs = call_args
        on_error = kwargs.get("on_error")
        assert on_error is not None

        # Simulate error to trigger increment
        assert mrd._open_retries == 0
        on_error(ValueError("test"))
        assert mrd._open_retries == 1

    @mock.patch("google.cloud.storage.asyncio.async_multi_range_downloader.AsyncRetry")
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_open_uses_redirect_aware_retry_predicate(
        self, mock_cls_async_read_object_stream, mock_async_retry
    ):
        mock_policy = mock.MagicMock()
        mock_policy.side_effect = lambda f: f
        mock_async_retry.return_value = mock_policy

        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()
        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()

        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        await mrd.open()

        predicate = mock_async_retry.call_args.kwargs["predicate"]
        redirect = _storage_v2.BidiReadObjectRedirectedError(
            routing_token="redirect-token"
        )
        status = status_pb2.Status()
        detail = status.details.add()
        detail.type_url = (
            "type.googleapis.com/google.storage.v2.BidiReadObjectRedirectedError"
        )
        detail.value = _storage_v2.BidiReadObjectRedirectedError.serialize(redirect)
        grpc_error = mock.MagicMock()
        grpc_error.trailing_metadata.return_value = [
            ("grpc-status-details-bin", status.SerializeToString())
        ]

        assert predicate(exceptions.ServiceUnavailable("unavailable")) is True
        assert predicate(exceptions.Aborted("redirect", errors=[grpc_error])) is True
        assert predicate(exceptions.Aborted("bare aborted")) is False
        assert predicate(ConnectionResetError("connection reset")) is False

    @mock.patch("google.cloud.storage.asyncio.async_multi_range_downloader.logger")
    @pytest.mark.asyncio
    async def test_on_open_error_logs_warning(self, mock_logger):
        # Arrange
        mock_client = mock.MagicMock()
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        exc = ValueError("test error")

        # Act
        mrd._on_open_error(exc)

        # Assert
        mock_logger.warning.assert_called_once_with(
            f"Error occurred while opening MRD: {exc}"
        )

    @mock.patch("google.cloud.storage.asyncio.async_multi_range_downloader.logger")
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_download_ranges_resumption_logging(
        self, mock_cls_async_read_object_stream, mock_random_int, mock_logger
    ):
        # Arrange
        mock_mrd, _ = await self._make_mock_mrd(mock_cls_async_read_object_stream)

        from google.api_core import exceptions as core_exceptions

        retryable_exc = core_exceptions.ServiceUnavailable("Retry me")

        mock_mrd.read_obj_str.send = AsyncMock(
            side_effect=[
                retryable_exc,
                None,
            ]
        )

        recv_call_count = 0

        async def staged_recv():
            nonlocal recv_call_count
            recv_call_count += 1
            if recv_call_count == 1:
                return _storage_v2.BidiReadObjectResponse(
                    object_data_ranges=[
                        _storage_v2.ObjectRangeData(
                            checksummed_data=_storage_v2.ChecksummedData(
                                content=b"data", crc32c=123
                            ),
                            range_end=True,
                            read_range=_storage_v2.ReadRange(
                                read_offset=0, read_length=4, read_id=123
                            ),
                        )
                    ]
                )
            return None

        mock_mrd.read_obj_str.recv = AsyncMock(side_effect=staged_recv)

        mock_random_int.return_value = 123

        # Act
        buffer = BytesIO()

        # Patch google_crc32c.value where it is used in reads_resumption_strategy
        with mock.patch(
            "google.cloud.storage.asyncio.retry.reads_resumption_strategy.google_crc32c.value"
        ) as mock_crc_value:
            mock_crc_value.return_value = 123
            await mock_mrd.download_ranges([(0, 4, buffer)])

        # Assert
        mock_logger.info.assert_any_call("Resuming download (attempt 2) for 1 ranges.")

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_open_populates_checksum_properties(
        self, mock_cls_async_read_object_stream
    ):
        # Arrange
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()
        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()
        mock_stream.generation_number = 123
        mock_stream.persisted_size = 100
        mock_stream.read_handle = b"h"
        mock_stream.is_finalized = True
        mock_stream.full_obj_server_crc32c = 999

        mrd = AsyncMultiRangeDownloader(mock_client, "bucket", "object")
        assert mrd.is_finalized is False
        assert mrd.full_obj_server_crc32c is None

        # Act
        await mrd.open()

        # Assert
        assert mrd.is_finalized is True
        assert mrd.full_obj_server_crc32c == 999

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._ReadResumptionStrategy"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._BidiStreamRetryManager"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_download_ranges_configures_full_object_read_state(
        self,
        mock_cls_async_read_object_stream,
        mock_retry_manager_cls,
        mock_strategy_cls,
    ):
        # Arrange
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()
        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()
        mock_stream.persisted_size = 100
        mock_stream.is_finalized = True
        mock_stream.full_obj_server_crc32c = 999

        mrd = await AsyncMultiRangeDownloader.create_mrd(mock_client, "b", "o")

        mock_retry_manager = mock_retry_manager_cls.return_value
        mock_retry_manager.execute = AsyncMock()

        # Act
        # Implicit full read (0, 0) and explicit full read (0, persisted_size=100)
        ranges = [(0, 0, BytesIO()), (0, 100, BytesIO()), (10, 20, BytesIO())]
        await mrd.download_ranges(ranges, enable_checksum=True)

        # Assert
        mock_retry_manager.execute.assert_called_once()
        initial_state = mock_retry_manager.execute.call_args[0][0]

        download_states = initial_state["download_states"]
        assert len(download_states) == 3

        states_list = list(download_states.values())
        # First state: (0, 0) -> is_full_object_read is True
        assert states_list[0].is_full_object_read is True
        assert states_list[0].rolling_checksum is not None

        # Second state: (0, 100) -> is_full_object_read is True
        assert states_list[1].is_full_object_read is True
        assert states_list[1].rolling_checksum is not None

        # Third state: (10, 20) -> is_full_object_read is False
        assert states_list[2].is_full_object_read is False
        assert states_list[2].rolling_checksum is None

        # State values for enable_checksum and crc32c
        assert initial_state["enable_checksum"] is True
        assert initial_state["full_obj_server_crc32c"] == 999

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._ReadResumptionStrategy"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._BidiStreamRetryManager"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_download_ranges_closes_on_datacorruption(
        self,
        mock_cls_async_read_object_stream,
        mock_retry_manager_cls,
        mock_strategy_cls,
    ):
        # Arrange
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()
        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()

        mrd = await AsyncMultiRangeDownloader.create_mrd(mock_client, "b", "o")
        mrd.close = AsyncMock()

        mock_retry_manager = mock_retry_manager_cls.return_value
        mock_retry_manager.execute = AsyncMock(
            side_effect=DataCorruption(None, "corrupted")
        )

        # Act & Assert
        with pytest.raises(DataCorruption):
            await mrd.download_ranges([(0, 0, BytesIO())])

        mrd.close.assert_called_once()

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_download_ranges_retries_on_aborted_idle_stream_from_recv(
        self, mock_cls_async_read_object_stream, mock_random_int
    ):
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        initial_stream = mock.MagicMock()
        initial_stream.open = AsyncMock()
        initial_stream.close = AsyncMock()
        initial_stream.send = AsyncMock()
        initial_stream.generation_number = _TEST_GENERATION_NUMBER
        initial_stream.persisted_size = _TEST_OBJECT_SIZE
        initial_stream.read_handle = _TEST_READ_HANDLE
        initial_stream.is_finalized = True
        initial_stream.full_obj_server_crc32c = None
        initial_stream.is_stream_open = True

        replacement_stream = mock.MagicMock()
        replacement_stream.open = AsyncMock()
        replacement_stream.close = AsyncMock()
        replacement_stream.send = AsyncMock()
        replacement_stream.generation_number = _TEST_GENERATION_NUMBER
        replacement_stream.persisted_size = _TEST_OBJECT_SIZE
        replacement_stream.read_handle = _TEST_READ_HANDLE
        replacement_stream.is_finalized = True
        replacement_stream.full_obj_server_crc32c = None
        replacement_stream.is_stream_open = True

        mock_cls_async_read_object_stream.side_effect = [
            initial_stream,
            replacement_stream,
        ]

        error_info = error_details_pb2.ErrorInfo(
            reason="GRPC_REQUEST_TIMEOUT",
            domain="storage.googleapis.com",
        )
        initial_stream.recv = AsyncMock(
            side_effect=exceptions.Aborted(
                "Idle stream has been closed.",
                details=[error_info],
                error_info=error_info,
            )
        )

        response = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=b"data", crc32c=google_crc32c.value(b"data")
                    ),
                    range_end=True,
                    read_range=_storage_v2.ReadRange(
                        read_offset=0, read_length=4, read_id=123
                    ),
                )
            ]
        )
        replacement_stream.recv = AsyncMock(side_effect=[response])
        mock_random_int.return_value = 123

        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client,
            _TEST_BUCKET_NAME,
            _TEST_OBJECT_NAME,
            _TEST_GENERATION_NUMBER,
            _TEST_READ_HANDLE,
        )

        buffer = BytesIO()
        await mrd.download_ranges([(0, 4, buffer)])

        assert buffer.getvalue() == b"data"
        assert mock_cls_async_read_object_stream.call_count == 2
        initial_stream.close.assert_awaited_once()
        replacement_stream.open.assert_awaited_once()
        replacement_stream.send.assert_awaited_once_with(
            _storage_v2.BidiReadObjectRequest(
                read_ranges=[
                    _storage_v2.ReadRange(read_offset=0, read_length=4, read_id=123)
                ]
            )
        )

    def test_is_read_retryable_predicate(self):
        """Tests that _is_read_retryable correctly classifies retryable read errors."""
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            _is_read_retryable,
        )

        # Retryable exceptions
        assert _is_read_retryable(exceptions.Aborted("Idle stream closed")) is True
        assert _is_read_retryable(exceptions.ServiceUnavailable("unavailable")) is True
        assert _is_read_retryable(exceptions.InternalServerError("internal")) is True
        assert _is_read_retryable(exceptions.DeadlineExceeded("timeout")) is True
        assert _is_read_retryable(exceptions.TooManyRequests("quota")) is True
        assert _is_read_retryable(ConnectionResetError("connection reset")) is False
        assert _is_read_retryable(BrokenPipeError("broken pipe")) is False

        # Non-retryable exceptions
        assert _is_read_retryable(ValueError("invalid")) is False
        assert _is_read_retryable(exceptions.NotFound("not found")) is False
        assert _is_read_retryable(exceptions.PermissionDenied("denied")) is False
        assert _is_read_retryable(exceptions.InvalidArgument("invalid")) is False

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_mrd_metrics_recording(
        self, mock_cls_async_read_object_stream, mock_random_int
    ):
        mock_recorder = mock.MagicMock()
        mock_recorder.standard_enabled = True
        mock_client = mock.MagicMock()
        mock_client._metrics_recorder = mock_recorder
        mock_client.grpc_client = mock.AsyncMock()

        stream = mock.MagicMock()
        stream.open = AsyncMock()
        stream.close = AsyncMock()
        stream.send = AsyncMock()
        stream._mark_closing_cleanly = mock.MagicMock()
        stream.generation_number = _TEST_GENERATION_NUMBER
        stream.persisted_size = _TEST_OBJECT_SIZE
        stream.read_handle = _TEST_READ_HANDLE
        stream.is_finalized = True
        stream.full_obj_server_crc32c = None
        stream.is_stream_open = True
        mock_cls_async_read_object_stream.return_value = stream

        response = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=b"data", crc32c=google_crc32c.value(b"data")
                    ),
                    range_end=True,
                    read_range=_storage_v2.ReadRange(
                        read_offset=0, read_length=4, read_id=123
                    ),
                )
            ]
        )
        stream.recv = AsyncMock(side_effect=[response])
        mock_random_int.return_value = 123

        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client,
            _TEST_BUCKET_NAME,
            _TEST_OBJECT_NAME,
        )
        # create_mrd suppresses nested open() so only 1 logical operation is recorded
        mock_recorder.record_logical_operation.assert_called_once()
        assert (
            mock_recorder.record_logical_operation.call_args.kwargs["client_method"]
            == "storage.asyncio.AsyncMultiRangeDownloader.create_mrd"
        )

        mock_recorder.record_logical_operation.reset_mock()
        buf = BytesIO()
        await mrd.download_ranges([(0, 4, buf)])
        mock_recorder.record_response_body_size.assert_called_once_with(
            4, operation="ReadObject"
        )
        mock_recorder.record_logical_operation.assert_called_once()
        assert (
            mock_recorder.record_logical_operation.call_args.kwargs["client_method"]
            == "storage.asyncio.AsyncMultiRangeDownloader.download_ranges"
        )
        assert (
            mock_recorder.record_logical_operation.call_args.kwargs["operation"]
            == "ReadObject"
        )
        assert (
            mock_recorder.record_logical_operation.call_args.kwargs["rpc_method"]
            == "google.storage.v2.Storage/BidiReadObject"
        )

        # Verify download_ranges with custom metadata marks stream clean before reopen
        chunk1 = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=b"ab", crc32c=google_crc32c.value(b"ab")
                    ),
                    range_end=False,
                    read_range=_storage_v2.ReadRange(
                        read_offset=0, read_length=2, read_id=123
                    ),
                )
            ]
        )
        chunk2 = _storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                _storage_v2.ObjectRangeData(
                    checksummed_data=_storage_v2.ChecksummedData(
                        content=b"cd", crc32c=google_crc32c.value(b"cd")
                    ),
                    range_end=True,
                    read_range=_storage_v2.ReadRange(
                        read_offset=2, read_length=2, read_id=123
                    ),
                )
            ]
        )
        stream.recv = AsyncMock(side_effect=[chunk1, chunk2])
        mock_recorder.record_response_body_size.reset_mock()
        stream._mark_closing_cleanly.reset_mock()
        buf2 = BytesIO()
        await mrd.download_ranges([(0, 4, buf2)], metadata=[("x-custom", "val")])
        stream._mark_closing_cleanly.assert_called()
        mock_recorder.record_response_body_size.assert_called_once_with(
            4, operation="ReadObject"
        )

        await mrd.close()
        stream._mark_closing_cleanly.assert_called()

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_mrd_retry_metrics_accounting(
        self, mock_cls_async_read_object_stream, mock_random_int, monkeypatch
    ):
        from google.api_core.retry_async import AsyncRetry

        from google.cloud.storage import _opentelemetry_metrics

        monkeypatch.setattr(_opentelemetry_metrics, "HAS_OPENTELEMETRY_METRICS", True)
        monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
        mock_metrics = mock.Mock()
        mock_meter = mock.Mock()
        mock_meter.create_histogram.side_effect = lambda *a, **kw: mock.Mock()
        mock_meter.create_counter.side_effect = lambda *a, **kw: mock.Mock()
        mock_metrics.get_meter.return_value = mock_meter
        monkeypatch.setattr(
            _opentelemetry_metrics, "metrics", mock_metrics, raising=False
        )

        recorder = _opentelemetry_metrics._MetricsRecorder(
            enable_metrics=True, rpc_system="grpc"
        )
        mock_client = mock.MagicMock()
        mock_client._metrics_recorder = recorder
        mock_client.grpc_client = mock.AsyncMock()

        # 1. MRD.open() retry (attempt 1 fails with 503, attempt 2 succeeds)
        failed_open_stream = mock.MagicMock()
        failed_open_stream.open = AsyncMock(
            side_effect=exceptions.ServiceUnavailable("503 open failed")
        )
        failed_open_stream.is_stream_open = False

        open_stream = mock.MagicMock()
        open_stream.open = AsyncMock()
        open_stream.close = AsyncMock()
        open_stream.send = AsyncMock()
        open_stream.generation_number = _TEST_GENERATION_NUMBER
        open_stream.persisted_size = _TEST_OBJECT_SIZE
        open_stream.read_handle = _TEST_READ_HANDLE
        open_stream.is_finalized = True
        open_stream.full_obj_server_crc32c = None
        open_stream.is_stream_open = True

        # 2. MRD.download_ranges() mid-stream retry (attempt 1 Aborted, attempt 2 succeeds)
        open_stream.recv = AsyncMock(
            side_effect=exceptions.Aborted("Idle stream closed")
        )
        recovered_stream = mock.MagicMock()
        recovered_stream.open = AsyncMock()
        recovered_stream.close = AsyncMock()
        recovered_stream.send = AsyncMock()
        recovered_stream.generation_number = _TEST_GENERATION_NUMBER
        recovered_stream.persisted_size = _TEST_OBJECT_SIZE
        recovered_stream.read_handle = _TEST_READ_HANDLE
        recovered_stream.is_finalized = True
        recovered_stream.full_obj_server_crc32c = None
        recovered_stream.is_stream_open = True
        recovered_stream.recv = AsyncMock(
            side_effect=[
                _storage_v2.BidiReadObjectResponse(
                    object_data_ranges=[
                        _storage_v2.ObjectRangeData(
                            checksummed_data=_storage_v2.ChecksummedData(
                                content=b"data", crc32c=google_crc32c.value(b"data")
                            ),
                            range_end=True,
                            read_range=_storage_v2.ReadRange(
                                read_offset=0, read_length=4, read_id=123
                            ),
                        )
                    ]
                )
            ]
        )

        mock_cls_async_read_object_stream.side_effect = [
            failed_open_stream,
            open_stream,
            recovered_stream,
        ]
        mock_random_int.return_value = 123

        user_on_error = mock.Mock()
        fast_retry = AsyncRetry(initial=0.001, maximum=0.001, on_error=user_on_error)
        mrd = AsyncMultiRangeDownloader(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        await mrd.open(retry_policy=fast_retry)

        user_on_error.assert_called_once()
        recorder.retries_counter.add.assert_called_once()
        _, open_retry_kw = recorder.retries_counter.add.call_args
        assert open_retry_kw["attributes"]["gcp.storage.operation"] == "ReadObject"
        assert open_retry_kw["attributes"]["error.type"] == "UNAVAILABLE"

        recorder.retries_counter.add.reset_mock()
        buf = BytesIO()
        await mrd.download_ranges(
            [(0, 4, buf)],
            retry_policy=AsyncRetry(
                predicate=lambda e: True, initial=0.001, maximum=0.001
            ),
        )
        assert buf.getvalue() == b"data"
        recorder.retries_counter.add.assert_called_once()
        _, dl_retry_kw = recorder.retries_counter.add.call_args
        assert dl_retry_kw["attributes"]["gcp.storage.operation"] == "ReadObject"
        assert dl_retry_kw["attributes"]["error.type"] == "ABORTED"

        # 3. MRD.open() failure when metrics are disabled (recorder is None)
        disabled_client = mock.MagicMock()
        disabled_client._metrics_recorder = None
        disabled_client.grpc_client = mock.AsyncMock()
        fail_stream = mock.MagicMock()
        fail_stream.open = AsyncMock(side_effect=exceptions.NotFound("404"))
        mock_cls_async_read_object_stream.side_effect = [fail_stream]
        mrd_disabled = AsyncMultiRangeDownloader(
            disabled_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        with pytest.raises(exceptions.NotFound):
            await mrd_disabled.open()

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader.generate_random_56_bit_integer"
    )
    @pytest.mark.asyncio
    async def test_mrd_bidi_stream_interceptor_ttfb_duration_and_reopen_metrics(
        self, mock_random_int, monkeypatch
    ):
        import grpc
        from google.api_core.retry_async import AsyncRetry

        from google.cloud.storage import _opentelemetry_metrics
        from google.cloud.storage.asyncio import async_grpc_client

        monkeypatch.setattr(_opentelemetry_metrics, "HAS_OPENTELEMETRY_METRICS", True)
        monkeypatch.setattr(_opentelemetry_metrics, "_ENABLE_METRICS_DEV_GATE", True)
        mock_metrics = mock.Mock()
        mock_meter = mock.Mock()
        mock_meter.create_histogram.side_effect = lambda *a, **kw: mock.Mock()
        mock_meter.create_counter.side_effect = lambda *a, **kw: mock.Mock()
        mock_metrics.get_meter.return_value = mock_meter
        monkeypatch.setattr(
            _opentelemetry_metrics, "metrics", mock_metrics, raising=False
        )

        recorder = _opentelemetry_metrics._MetricsRecorder(
            enable_metrics=True, rpc_system="grpc"
        )
        _, _, _, s_s = async_grpc_client._create_metrics_interceptors(
            recorder, direct_path_attempted=False
        )
        details = mock.MagicMock(method="/google.storage.v2.Storage/BidiReadObject")

        class _FakeBidiCall:
            def __init__(self):
                self._queue = asyncio.Queue()
                self._done = False
                self._pump_task = None

            def done(self):
                return self._done

            def add_done_callback(self, callback):
                pass

            def cancel(self):
                self._done = True
                self._pump_task.cancel()
                self._queue.put_nowait(grpc.aio.EOF)
                return True

            async def write(self, request):
                if request.read_object_spec.bucket:
                    self._queue.put_nowait(
                        _storage_v2.BidiReadObjectResponse(
                            metadata=_storage_v2.Object(
                                generation=_TEST_GENERATION_NUMBER,
                                size=_TEST_OBJECT_SIZE,
                            ),
                            read_handle=_storage_v2.BidiReadHandle(
                                handle=_TEST_READ_HANDLE
                            ),
                        )
                    )
                if request.read_ranges:
                    for r in request.read_ranges:
                        self._queue.put_nowait(
                            _storage_v2.BidiReadObjectResponse(
                                object_data_ranges=[
                                    _storage_v2.ObjectRangeData(
                                        checksummed_data=_storage_v2.ChecksummedData(
                                            content=b"data",
                                            crc32c=google_crc32c.value(b"data"),
                                        ),
                                        range_end=True,
                                        read_range=_storage_v2.ReadRange(
                                            read_offset=r.read_offset,
                                            read_length=4,
                                            read_id=r.read_id,
                                        ),
                                    )
                                ]
                            )
                        )

            async def done_writing(self):
                self._queue.put_nowait(grpc.aio.EOF)

            async def read(self):
                return await self._queue.get()

        created_tracked_calls = []
        raw_calls = [
            _FakeBidiCall(),
            _FakeBidiCall(),
            _FakeBidiCall(),
        ]

        async def start_bidi_rpc(request_iterator=None, metadata=None):
            raw = raw_calls.pop(0)
            tracked = await s_s.intercept_stream_stream(
                mock.AsyncMock(return_value=raw), details, request_iterator
            )

            async def _pump_requests():
                async for req in request_iterator:
                    await tracked.write(req)
                await tracked.done_writing()

            raw._pump_task = asyncio.create_task(_pump_requests())
            created_tracked_calls.append(tracked)
            return tracked

        mock_client = mock.MagicMock()
        mock_client._metrics_recorder = recorder
        bidi_key = object()
        mock_client.grpc_client._client._transport.bidi_read_object = bidi_key
        mock_client.grpc_client._client._transport._wrapped_methods = {
            bidi_key: start_bidi_rpc
        }
        mock_random_int.side_effect = [101, 102, 201, 202]

        # Scenario A: Healthy MRD lifecycle across 2 download_ranges() calls + close()
        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        created_tracked_calls[0]._start_time -= 50.0
        assert recorder.ttfb.record.call_count == 1

        b1, b2 = BytesIO(), BytesIO()
        await mrd.download_ranges([(0, 4, b1)])
        await mrd.download_ranges([(0, 4, b2)])
        # Same physical stream: TTFB is still recorded only once
        assert recorder.ttfb.record.call_count == 1
        assert b1.getvalue() == b"data"
        assert b2.getvalue() == b"data"

        await mrd.close()
        assert recorder.attempts_counter.add.call_count == 1
        assert (
            recorder.attempts_counter.add.call_args.kwargs["attributes"]["error.type"]
            == "OK"
        )
        assert recorder.rpc_call_duration.record.call_args.args[0] >= 50.0

        # Scenario B: Broken stream during download_ranges() triggers reopen_stream()
        recorder.ttfb.record.reset_mock()
        recorder.attempts_counter.add.reset_mock()
        recorder.retries_counter.add.reset_mock()
        recorder.rpc_call_duration.record.reset_mock()

        mrd2 = await AsyncMultiRangeDownloader.create_mrd(
            mock_client, _TEST_BUCKET_NAME, _TEST_OBJECT_NAME
        )
        assert recorder.ttfb.record.call_count == 1
        mrd2.read_obj_str.send = AsyncMock(
            side_effect=exceptions.ServiceUnavailable("send broke")
        )

        b3 = BytesIO()
        await mrd2.download_ranges(
            [(0, 4, b3)],
            retry_policy=AsyncRetry(
                predicate=lambda e: True, initial=0.001, maximum=0.001
            ),
        )
        assert b3.getvalue() == b"data"
        # Stream 1 + reopened Stream 2 => 2 TTFB points and 1 retry
        assert recorder.ttfb.record.call_count == 2
        assert recorder.retries_counter.add.call_count == 1
        # Broken stream 1 was NOT falsely marked OK by reopen_stream()
        stream1_err = recorder.attempts_counter.add.call_args_list[0].kwargs[
            "attributes"
        ]["error.type"]
        assert stream1_err == "CANCELLED"

        await mrd2.close()
        assert recorder.attempts_counter.add.call_count == 2
        stream2_err = recorder.attempts_counter.add.call_args_list[1].kwargs[
            "attributes"
        ]["error.type"]
        assert stream2_err == "OK"
