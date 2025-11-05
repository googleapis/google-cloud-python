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

import io
import unittest
import pytest
from google.cloud.storage.exceptions import DataCorruption
from google.api_core import exceptions

from google.cloud import _storage_v2 as storage_v2
from google.cloud.storage._experimental.asyncio.retry.reads_resumption_strategy import (
    _DownloadState,
    _ReadResumptionStrategy,
)
from google.cloud._storage_v2.types.storage import BidiReadObjectRedirectedError

_READ_ID = 1


class TestDownloadState(unittest.TestCase):
    def test_initialization(self):
        """Test that _DownloadState initializes correctly."""
        initial_offset = 10
        initial_length = 100
        user_buffer = io.BytesIO()
        state = _DownloadState(initial_offset, initial_length, user_buffer)

        self.assertEqual(state.initial_offset, initial_offset)
        self.assertEqual(state.initial_length, initial_length)
        self.assertEqual(state.user_buffer, user_buffer)
        self.assertEqual(state.bytes_written, 0)
        self.assertEqual(state.next_expected_offset, initial_offset)
        self.assertFalse(state.is_complete)


class TestReadResumptionStrategy(unittest.TestCase):
    def test_generate_requests_single_incomplete(self):
        """Test generating a request for a single incomplete download."""
        read_state = _DownloadState(0, 100, io.BytesIO())
        read_state.bytes_written = 20
        state = {_READ_ID: read_state}

        read_strategy = _ReadResumptionStrategy()
        requests = read_strategy.generate_requests(state)

        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].read_offset, 20)
        self.assertEqual(requests[0].read_length, 80)
        self.assertEqual(requests[0].read_id, _READ_ID)

    def test_generate_requests_multiple_incomplete(self):
        """Test generating requests for multiple incomplete downloads."""
        read_id2 = 2
        read_state1 = _DownloadState(0, 100, io.BytesIO())
        read_state1.bytes_written = 50
        read_state2 = _DownloadState(200, 100, io.BytesIO())
        state = {_READ_ID: read_state1, read_id2: read_state2}

        read_strategy = _ReadResumptionStrategy()
        requests = read_strategy.generate_requests(state)

        self.assertEqual(len(requests), 2)
        req1 = next(request for request in requests if request.read_id == _READ_ID)
        req2 = next(request for request in requests if request.read_id == read_id2)

        self.assertEqual(req1.read_offset, 50)
        self.assertEqual(req1.read_length, 50)
        self.assertEqual(req2.read_offset, 200)
        self.assertEqual(req2.read_length, 100)

    def test_generate_requests_with_complete(self):
        """Test that no request is generated for a completed download."""
        read_state = _DownloadState(0, 100, io.BytesIO())
        read_state.is_complete = True
        state = {_READ_ID: read_state}

        read_strategy = _ReadResumptionStrategy()
        requests = read_strategy.generate_requests(state)

        self.assertEqual(len(requests), 0)

    def test_generate_requests_empty_state(self):
        """Test generating requests with an empty state."""
        read_strategy = _ReadResumptionStrategy()
        requests = read_strategy.generate_requests({})
        self.assertEqual(len(requests), 0)

    def test_update_state_processes_single_chunk_successfully(self):
        """Test updating state from a successful response."""
        buffer = io.BytesIO()
        read_state = _DownloadState(0, 100, buffer)
        state = {_READ_ID: read_state}
        data = b"test_data"
        read_strategy = _ReadResumptionStrategy()

        response = storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                storage_v2.types.ObjectRangeData(
                    read_range=storage_v2.ReadRange(
                        read_id=_READ_ID, read_offset=0, read_length=len(data)
                    ),
                    checksummed_data=storage_v2.ChecksummedData(content=data),
                )
            ]
        )

        read_strategy.update_state_from_response(response, state)

        self.assertEqual(read_state.bytes_written, len(data))
        self.assertEqual(read_state.next_expected_offset, len(data))
        self.assertFalse(read_state.is_complete)
        self.assertEqual(buffer.getvalue(), data)

    def test_update_state_from_response_offset_mismatch(self):
        """Test that an offset mismatch raises DataCorruption."""
        read_state = _DownloadState(0, 100, io.BytesIO())
        read_state.next_expected_offset = 10
        state = {_READ_ID: read_state}
        read_strategy = _ReadResumptionStrategy()

        response = storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                storage_v2.types.ObjectRangeData(
                    read_range=storage_v2.ReadRange(
                        read_id=_READ_ID, read_offset=0, read_length=4
                    ),
                    checksummed_data=storage_v2.ChecksummedData(content=b"data"),
                )
            ]
        )

        with pytest.raises(DataCorruption) as exc_info:
            read_strategy.update_state_from_response(response, state)
        assert "Offset mismatch" in str(exc_info.value)

    def test_update_state_from_response_final_byte_count_mismatch(self):
        """Test that a final byte count mismatch raises DataCorruption."""
        read_state = _DownloadState(0, 100, io.BytesIO())
        state = {_READ_ID: read_state}
        read_strategy = _ReadResumptionStrategy()

        response = storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                storage_v2.types.ObjectRangeData(
                    read_range=storage_v2.ReadRange(
                        read_id=_READ_ID, read_offset=0, read_length=4
                    ),
                    checksummed_data=storage_v2.ChecksummedData(content=b"data"),
                    range_end=True,
                )
            ]
        )

        with pytest.raises(DataCorruption) as exc_info:
            read_strategy.update_state_from_response(response, state)
        assert "Byte count mismatch" in str(exc_info.value)

    def test_update_state_from_response_completes_download(self):
        """Test that the download is marked complete on range_end."""
        buffer = io.BytesIO()
        data = b"test_data"
        read_state = _DownloadState(0, len(data), buffer)
        state = {_READ_ID: read_state}
        read_strategy = _ReadResumptionStrategy()

        response = storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                storage_v2.types.ObjectRangeData(
                    read_range=storage_v2.ReadRange(
                        read_id=_READ_ID, read_offset=0, read_length=len(data)
                    ),
                    checksummed_data=storage_v2.ChecksummedData(content=data),
                    range_end=True,
                )
            ]
        )

        read_strategy.update_state_from_response(response, state)

        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.bytes_written, len(data))
        self.assertEqual(buffer.getvalue(), data)

    def test_update_state_from_response_completes_download_zero_length(self):
        """Test completion for a download with initial_length of 0."""
        buffer = io.BytesIO()
        data = b"test_data"
        read_state = _DownloadState(0, 0, buffer)
        state = {_READ_ID: read_state}
        read_strategy = _ReadResumptionStrategy()

        response = storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                storage_v2.types.ObjectRangeData(
                    read_range=storage_v2.ReadRange(
                        read_id=_READ_ID, read_offset=0, read_length=len(data)
                    ),
                    checksummed_data=storage_v2.ChecksummedData(content=data),
                    range_end=True,
                )
            ]
        )

        read_strategy.update_state_from_response(response, state)

        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.bytes_written, len(data))

    async def test_recover_state_on_failure_handles_redirect(self):
        """Verify recover_state_on_failure correctly extracts routing_token."""
        strategy = _ReadResumptionStrategy()

        state = {}
        self.assertIsNone(state.get("routing_token"))

        dummy_token = "dummy-routing-token"
        redirect_error = BidiReadObjectRedirectedError(routing_token=dummy_token)

        final_error = exceptions.RetryError("Retry failed", cause=redirect_error)

        await strategy.recover_state_on_failure(final_error, state)

        self.assertEqual(state.get("routing_token"), dummy_token)
