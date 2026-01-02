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
import unittest.mock as mock
from datetime import datetime

import pytest
import google_crc32c

from google.cloud._storage_v2.types import storage as storage_type
from google.cloud.storage._experimental.asyncio.retry.writes_resumption_strategy import (
    _WriteState,
    _WriteResumptionStrategy,
)
from google.cloud._storage_v2.types.storage import BidiWriteObjectRedirectedError


class TestWriteResumptionStrategy(unittest.TestCase):
    def _get_target_class(self):
        return _WriteResumptionStrategy

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_ctor(self):
        strategy = self._make_one()
        self.assertIsInstance(strategy, self._get_target_class())

    def test_generate_requests_initial_new_object(self):
        """
        Verify the initial request sequence for a new upload (WriteObjectSpec).
        """
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"0123456789")
        # Use WriteObjectSpec for new objects
        mock_spec = storage_type.WriteObjectSpec(
            resource=storage_type.Object(name="test-object")
        )
        state = {
            "write_state": _WriteState(
                mock_spec, chunk_size=4, user_buffer=mock_buffer
            ),
        }

        requests = list(strategy.generate_requests(state))

        # Check first request (Spec)
        self.assertEqual(requests[0].write_object_spec, mock_spec)
        self.assertFalse(requests[0].state_lookup)

        # Check data chunks
        self.assertEqual(requests[1].write_offset, 0)
        self.assertEqual(requests[1].checksummed_data.content, b"0123")
        self.assertEqual(requests[2].write_offset, 4)
        self.assertEqual(requests[2].checksummed_data.content, b"4567")
        self.assertEqual(requests[3].write_offset, 8)
        self.assertEqual(requests[3].checksummed_data.content, b"89")

        # Total requests: 1 Spec + 3 Chunks
        self.assertEqual(len(requests), 4)

    def test_generate_requests_initial_existing_object(self):
        """
        Verify the initial request sequence for appending to an existing object (AppendObjectSpec).
        """
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"0123")
        # Use AppendObjectSpec for existing objects
        mock_spec = storage_type.AppendObjectSpec(
            object_="test-object", bucket="test-bucket"
        )
        state = {
            "write_state": _WriteState(
                mock_spec, chunk_size=4, user_buffer=mock_buffer
            ),
        }

        requests = list(strategy.generate_requests(state))

        # Check first request (Spec)
        self.assertEqual(requests[0].append_object_spec, mock_spec)
        self.assertFalse(requests[0].state_lookup)

        # Check data chunk
        self.assertEqual(requests[1].write_offset, 0)
        self.assertEqual(requests[1].checksummed_data.content, b"0123")

    def test_generate_requests_empty_file(self):
        """
        Verify request sequence for an empty file. Should just be the Spec.
        """
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"")
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")
        state = {
            "write_state": _WriteState(
                mock_spec, chunk_size=4, user_buffer=mock_buffer
            ),
        }

        requests = list(strategy.generate_requests(state))

        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].append_object_spec, mock_spec)

    def test_generate_requests_resumption(self):
        """
        Verify request sequence when resuming an upload.
        """
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"0123456789")
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")

        write_state = _WriteState(mock_spec, chunk_size=4, user_buffer=mock_buffer)
        write_state.persisted_size = 4
        write_state.bytes_sent = 4
        write_state.write_handle = storage_type.BidiWriteHandle(handle=b"test-handle")
        mock_buffer.seek(4)

        state = {"write_state": write_state}

        requests = list(strategy.generate_requests(state))

        # Check first request has handle and lookup
        self.assertEqual(
            requests[0].append_object_spec.write_handle.handle, b"test-handle"
        )

        # Check data starts from offset 4
        self.assertEqual(requests[1].write_offset, 4)
        self.assertEqual(requests[1].checksummed_data.content, b"4567")
        self.assertEqual(requests[2].write_offset, 8)
        self.assertEqual(requests[2].checksummed_data.content, b"89")

    @pytest.mark.asyncio
    async def test_generate_requests_after_failure_and_recovery(self):
        """
        Verify recovery and resumption flow.
        """
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"0123456789abcdef")
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")
        state = {
            "write_state": _WriteState(mock_spec, chunk_size=4, user_buffer=mock_buffer)
        }
        write_state = state["write_state"]

        write_state.bytes_sent = 8
        mock_buffer.seek(8)

        strategy.update_state_from_response(
            storage_type.BidiWriteObjectResponse(
                persisted_size=4,
                write_handle=storage_type.BidiWriteHandle(handle=b"handle-1"),
            ),
            state,
        )

        await strategy.recover_state_on_failure(Exception("network error"), state)

        self.assertEqual(mock_buffer.tell(), 4)
        self.assertEqual(write_state.bytes_sent, 4)

        requests = list(strategy.generate_requests(state))

        self.assertTrue(requests[0].state_lookup)
        self.assertEqual(
            requests[0].append_object_spec.write_handle.handle, b"handle-1"
        )

        self.assertEqual(requests[1].write_offset, 4)
        self.assertEqual(requests[1].checksummed_data.content, b"4567")

    def test_update_state_from_response(self):
        """Verify state updates from server responses."""
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"0123456789")
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")
        state = {
            "write_state": _WriteState(
                mock_spec, chunk_size=4, user_buffer=mock_buffer
            ),
        }
        write_state = state["write_state"]

        response1 = storage_type.BidiWriteObjectResponse(
            write_handle=storage_type.BidiWriteHandle(handle=b"handle-1")
        )
        strategy.update_state_from_response(response1, state)
        self.assertEqual(write_state.write_handle.handle, b"handle-1")

        response2 = storage_type.BidiWriteObjectResponse(persisted_size=1024)
        strategy.update_state_from_response(response2, state)
        self.assertEqual(write_state.persisted_size, 1024)

        final_resource = storage_type.Object(name="test-object", bucket="b", size=2048, finalize_time=datetime.now())
        response3 = storage_type.BidiWriteObjectResponse(resource=final_resource)
        strategy.update_state_from_response(response3, state)
        self.assertEqual(write_state.persisted_size, 2048)
        self.assertTrue(write_state.is_finalized)

    @pytest.mark.asyncio
    async def test_recover_state_on_failure_handles_redirect(self):
        """
        Verify redirection error handling.
        """
        strategy = self._make_one()
        mock_buffer = mock.MagicMock(spec=io.BytesIO)
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")

        write_state = _WriteState(mock_spec, chunk_size=4, user_buffer=mock_buffer)
        state = {"write_state": write_state}

        redirect_error = BidiWriteObjectRedirectedError(routing_token="new-token-123")
        wrapped_error = Exception("RPC error")
        wrapped_error.cause = redirect_error

        await strategy.recover_state_on_failure(wrapped_error, state)

        self.assertEqual(write_state.routing_token, "new-token-123")
        mock_buffer.seek.assert_called_with(0)

    @pytest.mark.asyncio
    async def test_recover_state_on_failure_handles_redirect_with_handle(self):
        """Verify redirection that includes a write handle."""
        strategy = self._make_one()
        mock_buffer = mock.MagicMock(spec=io.BytesIO)
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")

        write_state = _WriteState(mock_spec, chunk_size=4, user_buffer=mock_buffer)
        state = {"write_state": write_state}

        redirect_error = BidiWriteObjectRedirectedError(
            routing_token="new-token-456", write_handle=b"redirect-handle"
        )
        wrapped_error = Exception("RPC error")
        wrapped_error.cause = redirect_error

        await strategy.recover_state_on_failure(wrapped_error, state)

        self.assertEqual(write_state.routing_token, "new-token-456")
        self.assertEqual(write_state.write_handle, b"redirect-handle")

        mock_buffer.seek.assert_called_with(0)

    def test_generate_requests_sends_crc32c_checksum(self):
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"0123")
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")
        state = {
            "write_state": _WriteState(
                mock_spec, chunk_size=4, user_buffer=mock_buffer
            ),
        }

        requests = list(strategy.generate_requests(state))

        expected_crc = google_crc32c.Checksum(b"0123")
        expected_crc_int = int.from_bytes(expected_crc.digest(), "big")
        self.assertEqual(requests[1].checksummed_data.crc32c, expected_crc_int)

    def test_generate_requests_with_routing_token(self):
        strategy = self._make_one()
        mock_buffer = io.BytesIO(b"")
        mock_spec = storage_type.AppendObjectSpec(object_="test-object")

        write_state = _WriteState(mock_spec, chunk_size=4, user_buffer=mock_buffer)
        write_state.routing_token = "redirected-token"
        state = {"write_state": write_state}

        requests = list(strategy.generate_requests(state))

        self.assertEqual(
            requests[0].append_object_spec.routing_token, "redirected-token"
        )
