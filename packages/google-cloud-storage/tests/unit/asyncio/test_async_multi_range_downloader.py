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

    def test_managed_stream_load(self):
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            _ManagedStream,
        )

        mock_stream = mock.MagicMock()
        mock_mux = mock.MagicMock()
        worker = _ManagedStream(mock_stream, mock_mux)

        # Initially zero load
        assert worker.calculate_load(target_io_depth=10, target_bytes=1000) == 0.0

        # Add 5 ranges and 500 bytes -> 5/10 = 0.5, 500/1000 = 0.5 -> load = 0.5*0.5 + 0.5*0.5 = 0.5
        worker.record_request(5, 500)
        assert worker.pending_ranges == 5
        assert worker.pending_bytes == 500
        assert worker.calculate_load(target_io_depth=10, target_bytes=1000) == 0.5

        # Release
        worker.record_completion(3, 300)
        assert worker.pending_ranges == 2
        assert worker.pending_bytes == 200
        assert worker.calculate_load(target_io_depth=10, target_bytes=1000) == 0.2

    @pytest.mark.asyncio
    async def test_stream_pool_scale_up_and_dispatch(self):
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            _ManagedStream,
            _StreamPool,
        )

        created_workers = []

        async def stream_factory():
            w = _ManagedStream(mock.MagicMock(), mock.MagicMock())
            created_workers.append(w)
            return w

        pool = _StreamPool(
            stream_factory=stream_factory,
            min_connections=1,
            max_connections=2,
            target_io_depth=2,
            target_bytes=100,
        )
        initial_worker = await stream_factory()
        await pool.add_worker(initial_worker)

        # 1. Acquire with small load (1 range, 10 bytes) -> load = 0.5*(1/2) + 0.5*(10/100) = 0.3 < 1.0
        w1 = await pool.acquire_stream(1, 10)
        assert w1 == initial_worker
        assert len(pool.workers) == 1

        # 2. Add enough load to exceed target load >= 1.0 (e.g. 3 ranges, 90 bytes)
        # Total on w1: 4 ranges (hits target and triggers background scale up)
        w1_again = await pool.acquire_stream(3, 90)
        assert w1_again == initial_worker

        # Scale-up task was scheduled; allow event loop to run background task
        await asyncio.sleep(0.01)
        assert len(pool.workers) == 2
        w2 = pool.workers[1]
        assert w2 != initial_worker

        # 3. Next acquire selects w2 because w2 has 0 load while w1 has high load
        w_next = await pool.acquire_stream(1, 10)
        assert w_next == w2

        # 4. Release worker capacity and close
        pool.release_stream(w1, 4, 100)
        pool.release_stream(w2, 1, 10)
        await pool.close()
        assert len(pool.workers) == 0

    @pytest.mark.asyncio
    async def test_stream_pool_proportional_scale_up(self):
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            _ManagedStream,
            _StreamPool,
        )

        created_workers = []

        async def stream_factory():
            w = _ManagedStream(mock.MagicMock(), mock.MagicMock())
            created_workers.append(w)
            return w

        pool = _StreamPool(
            stream_factory=stream_factory,
            min_connections=1,
            max_connections=5,
            target_io_depth=2,
            target_bytes=100,
        )
        initial_worker = await stream_factory()
        await pool.add_worker(initial_worker)

        # Huge burst: 6 ranges, 300 bytes -> load = 0.5*(6/2) + 0.5*(300/100) = 3.0
        # Desired connections = ceil(3.0) = 3.
        # Should launch 2 scale-ups concurrently in the background.
        w1 = await pool.acquire_stream(6, 300)
        assert w1 == initial_worker
        assert pool._pending_scale_ups == 2
        assert len(pool._background_tasks) == 2

        # Allow background scale-up tasks to finish
        await asyncio.sleep(0.01)
        assert len(pool.workers) == 3
        assert pool._pending_scale_ups == 0

        # Another huge burst exceeding max_connections (5):
        # 10 ranges, 500 bytes -> desired workers >= 5
        # Remaining headroom to max_connections is 5 - 3 = 2.
        await pool.acquire_stream(10, 500)
        assert pool._pending_scale_ups == 2

        await asyncio.sleep(0.01)
        assert len(pool.workers) == 5
        assert pool._pending_scale_ups == 0

        await pool.close()
        assert len(pool.workers) == 0

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_create_mrd_with_stream_config(self, mock_cls_stream):
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            MRDStreamConfig,
        )

        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        s1 = mock.MagicMock()
        s1.open = AsyncMock()
        s1.generation_number = 1
        s1.persisted_size = 100
        s1.read_handle = b"h1"
        s1.object_metadata = mock.Mock()

        s2 = mock.MagicMock()
        s2.open = AsyncMock()
        s2.generation_number = 1
        s2.persisted_size = 100
        s2.read_handle = b"h2"
        s2.object_metadata = mock.Mock()

        mock_cls_stream.side_effect = [s1, s2]

        config = MRDStreamConfig(
            min_connections=2,
            max_connections=4,
            target_io_depth=8,
            target_bytes=2 * 1024 * 1024,
        )

        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client, "b", "o", stream_config=config
        )

        assert mrd.stream_config.min_connections == 2
        assert mrd.stream_config.max_connections == 4
        assert mrd.stream_config.target_io_depth == 8
        assert mrd.stream_config.target_bytes == 2 * 1024 * 1024
        # Verified that 2 streams were opened initially for min_connections=2
        assert len(mrd._pool.workers) == 2
        await mrd.close()

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_mrd_download_ranges_triggers_pool_scaling(self, mock_cls_stream):
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            MRDStreamConfig,
        )

        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        s1 = mock.MagicMock()
        s1.open = AsyncMock()
        s1.generation_number = 1
        s1.persisted_size = 1000
        s1.read_handle = b"h1"
        s1.object_metadata = mock.Mock()

        s2 = mock.MagicMock()
        s2.open = AsyncMock()
        s2.generation_number = 1
        s2.persisted_size = 1000
        s2.read_handle = b"h2"
        s2.object_metadata = mock.Mock()

        mock_cls_stream.side_effect = [s1, s2]

        config = MRDStreamConfig(
            min_connections=1,
            max_connections=3,
            target_io_depth=1,
            target_bytes=50,
        )
        mrd = await AsyncMultiRangeDownloader.create_mrd(
            mock_client, "b", "o", stream_config=config
        )
        assert len(mrd._pool.workers) == 1

        with mock.patch.object(mrd, "_download_ranges_on_worker", new=AsyncMock()):
            # Download ranges with load > 1.0 (2 ranges, 100 bytes)
            await mrd.download_ranges([(0, 50, BytesIO()), (50, 50, BytesIO())])
            await asyncio.sleep(0.01)
            # Pool dynamically scaled up to 2 workers
            assert len(mrd._pool.workers) == 2

        await mrd.close()

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
    async def test_unfinalized_object_download(
        self,
        mock_cls_async_read_object_stream,
        mock_retry_manager_cls,
        mock_strategy_cls,
    ):
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        mock_stream = mock_cls_async_read_object_stream.return_value
        mock_stream.open = AsyncMock()
        mock_stream.generation_number = 123
        mock_stream.persisted_size = 50
        mock_stream.read_handle = b"handle"
        mock_stream.is_finalized = False
        mock_stream.full_obj_server_crc32c = None

        mrd = await AsyncMultiRangeDownloader.create_mrd(mock_client, "b", "o")
        assert mrd.is_finalized is False
        assert mrd.persisted_size == 50

        mock_retry_manager = mock_retry_manager_cls.return_value
        mock_retry_manager.execute = AsyncMock()

        # Download a range extending past initial persisted_size (offset 50, length 100 -> end 150)
        buf = BytesIO()
        await mrd.download_ranges([(50, 100, buf)])

        # Verify persisted_size is retained without error (no ratcheting)
        assert mrd.persisted_size == 50
        await mrd.close()

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_create_mrd_single_stream_bypass(self, mock_cls_stream):
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        s1 = mock.MagicMock()
        s1.open = AsyncMock()
        s1.generation_number = 1
        s1.persisted_size = 100
        s1.read_handle = b"h1"
        s1.object_metadata = mock.Mock()
        mock_cls_stream.return_value = s1

        # Default create_mrd without stream_config -> single-stream bypass
        mrd = await AsyncMultiRangeDownloader.create_mrd(mock_client, "b", "o")
        assert mrd.stream_config is None
        assert mrd._pool is None

        # download_ranges should use _primary_worker directly without pool
        with mock.patch.object(
            mrd, "_download_ranges_on_worker", new=AsyncMock()
        ) as mock_dl:
            await mrd.download_ranges([(0, 50, BytesIO())])
            assert mock_dl.call_count == 1
            assert mock_dl.call_args[0][0] == mrd._primary_worker

        await mrd.close()

    @pytest.mark.asyncio
    async def test_stream_pool_closed_and_cancellation(self):
        from google.cloud.storage.asyncio.async_multi_range_downloader import (
            _ManagedStream,
            _StreamPool,
        )

        scale_up_started = asyncio.Event()
        scale_up_finish = asyncio.Event()
        created_workers = []

        async def slow_factory():
            scale_up_started.set()
            await scale_up_finish.wait()
            mock_stream = mock.MagicMock()
            mock_stream.close = AsyncMock()
            mock_mux = mock.MagicMock()
            mock_mux.close = AsyncMock()
            w = _ManagedStream(mock_stream, mock_mux)
            created_workers.append(w)
            return w

        pool = _StreamPool(
            stream_factory=slow_factory,
            min_connections=1,
            max_connections=2,
            target_io_depth=1,
            target_bytes=10,
        )
        initial_w = _ManagedStream(mock.MagicMock(), mock.MagicMock())
        await pool.add_worker(initial_w)

        # Trigger scale up
        await pool.acquire_stream(2, 20)
        await scale_up_started.wait()
        assert len(pool._background_tasks) == 1

        # Close pool while scale up task is pending
        await pool.close()
        assert pool._closed is True
        assert len(pool.workers) == 0

        # Background task should be cancelled
        with pytest.raises(asyncio.CancelledError):
            await next(
                iter(pool._background_tasks)
            ) if pool._background_tasks else asyncio.sleep(0)

        # acquire_stream on closed pool must raise ValueError
        with pytest.raises(ValueError, match="Pool is closed"):
            await pool.acquire_stream(1, 10)

    @mock.patch(
        "google.cloud.storage.asyncio.async_multi_range_downloader._AsyncReadObjectStream"
    )
    @pytest.mark.asyncio
    async def test_routing_token_preservation_and_propagation(
        self, mock_cls_async_read_object_stream
    ):
        mock_client = mock.MagicMock()
        mock_client.grpc_client = mock.AsyncMock()

        s1 = mock.MagicMock()
        s1.open = AsyncMock()
        s1.generation_number = 100
        s1.read_handle = b"h1"
        s1.persisted_size = 1000
        s1.is_finalized = True
        s1.full_obj_server_crc32c = 12345
        mock_cls_async_read_object_stream.return_value = s1

        mrd = await AsyncMultiRangeDownloader.create_mrd(mock_client, "b", "o")
        # Simulate a redirect having set _routing_token
        mrd._routing_token = "token-abc"

        # Now when a new stream worker is opened via _create_new_stream_worker,
        # it should include routing_token in the metadata
        s2 = mock.MagicMock()
        s2.open = AsyncMock()
        s2.generation_number = 100
        s2.read_handle = b"h2"
        s2.persisted_size = 1000
        mock_cls_async_read_object_stream.return_value = s2

        w2 = await mrd._create_new_stream_worker()
        assert w2 is not None
        assert s2.open.call_count == 1
        call_kwargs = s2.open.call_args[1]
        assert ("x-goog-request-params", "routing_token=token-abc") in call_kwargs[
            "metadata"
        ]

        await mrd.close()
