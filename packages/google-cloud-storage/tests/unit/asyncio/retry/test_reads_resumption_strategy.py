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
import concurrent.futures
import io
import os
import signal
import unittest
import warnings
from unittest import mock

import google_crc32c
from google.api_core import exceptions

from google.cloud import _storage_v2 as storage_v2
from google.cloud._storage_v2.types.storage import BidiReadObjectRedirectedError
from google.cloud.storage.asyncio import _zero_copy_bidi_read
from google.cloud.storage.asyncio.retry import reads_resumption_strategy
from google.cloud.storage.asyncio.retry.reads_resumption_strategy import (
    _DownloadState,
    _ReadResumptionStrategy,
)
from google.cloud.storage.exceptions import DataCorruption

_READ_ID = 1
LOGGER_NAME = "google.cloud.storage.asyncio.retry.reads_resumption_strategy"
_OFFLOAD_ENV_VAR = "GCS_PYTHON_CLIENT_CRC32C_OFFLOAD"


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
        self.assertFalse(state.is_full_object_read)
        self.assertIsNone(state.rolling_checksum)

    def test_initialization_with_full_object_read(self):
        """Test that _DownloadState initializes correctly when is_full_object_read is True."""
        initial_offset = 10
        initial_length = 100
        user_buffer = io.BytesIO()
        state_full = _DownloadState(
            initial_offset, initial_length, user_buffer, is_full_object_read=True
        )

        self.assertEqual(state_full.initial_offset, initial_offset)
        self.assertEqual(state_full.initial_length, initial_length)
        self.assertEqual(state_full.user_buffer, user_buffer)
        self.assertEqual(state_full.bytes_written, 0)
        self.assertEqual(state_full.next_expected_offset, initial_offset)
        self.assertFalse(state_full.is_complete)
        self.assertTrue(state_full.is_full_object_read)
        self.assertIsNotNone(state_full.rolling_checksum)

    def test_initialization_with_full_object_read_and_checksum_disabled(self):
        """Test that _DownloadState does not initialize rolling_checksum when enable_checksum is False."""
        initial_offset = 10
        initial_length = 100
        user_buffer = io.BytesIO()
        state_full = _DownloadState(
            initial_offset,
            initial_length,
            user_buffer,
            is_full_object_read=True,
            enable_checksum=False,
        )

        self.assertEqual(state_full.initial_offset, initial_offset)
        self.assertEqual(state_full.initial_length, initial_length)
        self.assertEqual(state_full.user_buffer, user_buffer)
        self.assertEqual(state_full.bytes_written, 0)
        self.assertEqual(state_full.next_expected_offset, initial_offset)
        self.assertFalse(state_full.is_complete)
        self.assertTrue(state_full.is_full_object_read)
        self.assertIsNone(state_full.rolling_checksum)


class TestReadResumptionStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = _ReadResumptionStrategy()

        self.state = {"download_states": {}, "read_handle": None, "routing_token": None}

    def _add_download(
        self,
        read_id,
        offset=0,
        length=100,
        buffer=None,
        is_full_object_read=False,
        enable_checksum=True,
        receives_views=False,
    ):
        """Helper to inject a download state into the correct nested location."""
        if buffer is None:
            buffer = io.BytesIO()
        state = _DownloadState(
            initial_offset=offset,
            initial_length=length,
            user_buffer=buffer,
            is_full_object_read=is_full_object_read,
            enable_checksum=enable_checksum,
            receives_views=receives_views,
        )
        self.state["download_states"][read_id] = state
        return state

    def _create_response(
        self,
        content,
        read_id,
        offset,
        crc=None,
        range_end=False,
        handle=None,
        has_read_range=True,
    ):
        """Helper to create a response object."""
        checksummed_data = None
        if content is not None:
            if crc is None:
                crc = google_crc32c.value(content)
            checksummed_data = storage_v2.ChecksummedData(content=content, crc32c=crc)

        read_range = None
        if has_read_range:
            read_range = storage_v2.ReadRange(read_id=read_id, read_offset=offset)

        read_handle_message = None
        if handle:
            read_handle_message = storage_v2.BidiReadHandle(handle=handle)
            self.state["read_handle"] = handle

        return storage_v2.BidiReadObjectResponse(
            object_data_ranges=[
                storage_v2.ObjectRangeData(
                    checksummed_data=checksummed_data,
                    read_range=read_range,
                    range_end=range_end,
                )
            ],
            read_handle=read_handle_message,
        )

    # --- Request Generation Tests ---

    def test_generate_requests_single_incomplete(self):
        """Test generating a request for a single incomplete download."""
        read_state = self._add_download(_READ_ID, offset=0, length=100)
        read_state.bytes_written = 20

        requests = self.strategy.generate_requests(self.state)

        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].read_offset, 20)
        self.assertEqual(requests[0].read_length, 80)
        self.assertEqual(requests[0].read_id, _READ_ID)

    def test_generate_requests_multiple_incomplete(self):
        """Test generating requests for multiple incomplete downloads."""
        read_id2 = 2
        rs1 = self._add_download(_READ_ID, offset=0, length=100)
        rs1.bytes_written = 50

        self._add_download(read_id2, offset=200, length=100)

        requests = self.strategy.generate_requests(self.state)

        self.assertEqual(len(requests), 2)
        requests.sort(key=lambda r: r.read_id)

        req1 = requests[0]
        req2 = requests[1]

        self.assertEqual(req1.read_id, _READ_ID)
        self.assertEqual(req1.read_offset, 50)
        self.assertEqual(req1.read_length, 50)

        self.assertEqual(req2.read_id, read_id2)
        self.assertEqual(req2.read_offset, 200)
        self.assertEqual(req2.read_length, 100)

    def test_generate_requests_read_to_end_resumption(self):
        """Test resumption for 'read to end' (length=0) requests."""
        read_state = self._add_download(_READ_ID, offset=0, length=0)
        read_state.bytes_written = 500

        requests = self.strategy.generate_requests(self.state)

        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].read_offset, 500)
        self.assertEqual(requests[0].read_length, 0)

    def test_generate_requests_with_complete(self):
        """Test that no request is generated for a completed download."""
        read_state = self._add_download(_READ_ID)
        read_state.is_complete = True

        requests = self.strategy.generate_requests(self.state)
        self.assertEqual(len(requests), 0)

    def test_generate_requests_multiple_mixed_states(self):
        """Test generating requests with mixed complete, partial, and fresh states."""
        s1 = self._add_download(1, length=100)
        s1.is_complete = True

        s2 = self._add_download(2, offset=0, length=100)
        s2.bytes_written = 50

        s3 = self._add_download(3, offset=200, length=100)
        s3.bytes_written = 0

        requests = self.strategy.generate_requests(self.state)

        self.assertEqual(len(requests), 2)
        requests.sort(key=lambda r: r.read_id)

        self.assertEqual(requests[0].read_id, 2)
        self.assertEqual(requests[1].read_id, 3)

    def test_generate_requests_empty_state(self):
        """Test generating requests with an empty state."""
        requests = self.strategy.generate_requests(self.state)
        self.assertEqual(len(requests), 0)

    # --- Update State and response processing Tests ---

    def test_update_state_processes_single_chunk_successfully(self):
        """Test updating state from a successful response."""
        read_state = self._add_download(_READ_ID, offset=0, length=100)
        data = b"test_data"

        response = self._create_response(data, _READ_ID, offset=0)

        self.strategy.update_state_from_response(response, self.state)

        self.assertEqual(read_state.bytes_written, len(data))
        self.assertEqual(read_state.next_expected_offset, len(data))
        self.assertFalse(read_state.is_complete)
        self.assertEqual(read_state.user_buffer.getvalue(), data)

    def test_update_state_accumulates_chunks(self):
        """Verify that state updates correctly over multiple chunks."""
        read_state = self._add_download(_READ_ID, offset=0, length=8)

        resp1 = self._create_response(b"test", _READ_ID, offset=0)
        self.strategy.update_state_from_response(resp1, self.state)

        self.assertEqual(read_state.bytes_written, 4)
        self.assertEqual(read_state.user_buffer.getvalue(), b"test")

        resp2 = self._create_response(b"data", _READ_ID, offset=4, range_end=True)
        self.strategy.update_state_from_response(resp2, self.state)

        self.assertEqual(read_state.bytes_written, 8)
        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.user_buffer.getvalue(), b"testdata")

    def test_update_state_captures_read_handle(self):
        """Verify read_handle is extracted from the response."""
        self._add_download(_READ_ID)

        new_handle = b"optimized_handle"
        response = self._create_response(b"data", _READ_ID, 0, handle=new_handle)

        self.strategy.update_state_from_response(response, self.state)
        self.assertEqual(self.state["read_handle"].handle, new_handle)

    def test_update_state_unknown_id(self):
        """Verify we ignore data for IDs not in our tracking state."""
        self._add_download(_READ_ID)
        response = self._create_response(b"ghost", read_id=999, offset=0)

        self.strategy.update_state_from_response(response, self.state)
        self.assertEqual(self.state["download_states"][_READ_ID].bytes_written, 0)

    def test_update_state_missing_read_range(self):
        """Verify we ignore ranges without read_range metadata."""
        response = self._create_response(b"data", _READ_ID, 0, has_read_range=False)
        self.strategy.update_state_from_response(response, self.state)

    def test_update_state_offset_mismatch(self):
        """Test that an offset mismatch raises DataCorruption."""
        read_state = self._add_download(_READ_ID, offset=0)
        read_state.next_expected_offset = 10

        response = self._create_response(b"data", _READ_ID, offset=0)

        with self.assertRaisesRegex(DataCorruption, "Offset mismatch"):
            self.strategy.update_state_from_response(response, self.state)

    def test_update_state_checksum_mismatch(self):
        """Test that a CRC32C mismatch raises DataCorruption."""
        self._add_download(_READ_ID)
        response = self._create_response(b"data", _READ_ID, offset=0, crc=999999)

        with self.assertRaisesRegex(DataCorruption, "Checksum mismatch"):
            self.strategy.update_state_from_response(response, self.state)

    def test_update_state_failed_write_leaves_read_resumable(self):
        buffer = mock.Mock(spec=io.BytesIO)
        buffer.write.side_effect = [OSError("disk full"), None]
        read_state = self._add_download(_READ_ID, length=8, buffer=buffer)
        response = self._create_response(b"data", _READ_ID, offset=0)

        with self.assertRaises(OSError):
            self.strategy.update_state_from_response(response, self.state)

        self.assertEqual(read_state.bytes_written, 0)
        self.assertEqual(read_state.next_expected_offset, 0)
        self.strategy.update_state_from_response(response, self.state)
        self.assertEqual(read_state.bytes_written, 4)

    # --- Offloaded Checksum Tests ---

    def _large_chunk(self):
        return b"x" * reads_resumption_strategy._CRC32C_OFFLOAD_MIN_BYTES

    def _enable_offload(self):
        patcher = mock.patch.dict(os.environ, {_OFFLOAD_ENV_VAR: "1"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def _offload_to(self, futures):
        """Make the strategy hand large chunks to ``futures`` instead of a pool."""
        self._enable_offload()
        executor = mock.Mock()
        executor.submit.side_effect = list(futures)
        patcher = mock.patch.object(
            reads_resumption_strategy, "_crc32c_executor", executor
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_update_state_verifies_large_chunk_inline_by_default(self):
        """Unless the flag is on, a 1 MiB ``bytes`` chunk is hashed and written
        as it arrives."""
        content = b"x" * (1024 * 1024)
        envs = (
            {},
            {"GCS_PYTHON_CLIENT_ZERO_COPY_BIDI_READ": "1"},
            {_OFFLOAD_ENV_VAR: "0"},
            {_OFFLOAD_ENV_VAR: "false"},
            {_OFFLOAD_ENV_VAR: ""},
            {_OFFLOAD_ENV_VAR: "enabled"},
        )
        for read_id, env in enumerate(envs):
            with self.subTest(env=env), mock.patch.dict(os.environ, env, clear=True):
                read_state = self._add_download(read_id, length=len(content))
                response = self._create_response(
                    content, read_id, offset=0, range_end=True
                )

                self.strategy.update_state_from_response(response, self.state)

                self.assertEqual(read_state.user_buffer.getvalue(), content)
                self.assertTrue(read_state.is_complete)
                self.assertNotIn("pending_checksums", self.state)

    def test_update_state_offloads_large_chunk_when_enabled(self):
        """GCS_PYTHON_CLIENT_CRC32C_OFFLOAD offloads even a ``bytes`` chunk; it
        is held until its worker-side checksum verifies."""
        content = b"x" * (1024 * 1024)
        for read_id, value in enumerate(("1", "true", "TRUE", " yes ", "on")):
            with (
                self.subTest(value=value),
                mock.patch.dict(os.environ, {_OFFLOAD_ENV_VAR: value}),
            ):
                read_state = self._add_download(read_id, length=len(content))
                response = self._create_response(
                    content, read_id, offset=0, range_end=True
                )

                self.strategy.update_state_from_response(response, self.state)

                self.assertEqual(read_state.bytes_written, 0)
                self.assertEqual(len(self.state["pending_checksums"]), 1)
                asyncio.run(self.strategy.verify_pending_checksums(self.state))
                self.assertEqual(read_state.user_buffer.getvalue(), content)
                self.assertTrue(read_state.is_complete)

    def _accept_memoryview_in_crc32c(self):
        """Let google_crc32c hash views even if it predates memoryview support."""
        value, update = google_crc32c.value, google_crc32c.Checksum.update
        for patcher in (
            mock.patch.object(google_crc32c, "value", lambda data: value(bytes(data))),
            mock.patch.object(
                google_crc32c.Checksum,
                "update",
                lambda self, data: update(self, bytes(data)),
            ),
            mock.patch.object(_zero_copy_bidi_read, "_memoryview_supported", None),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def _create_view_response(self, content, read_id, offset, range_end=False):
        """A response as the zero-copy parser yields it, with memoryview chunks.

        Call _accept_memoryview_in_crc32c() once in the test first.
        """
        response = _zero_copy_bidi_read.deserialize(
            storage_v2.BidiReadObjectResponse.serialize(
                self._create_response(content, read_id, offset, range_end=range_end)
            )
        )
        self.assertIsInstance(
            response.object_data_ranges[0].checksummed_data.content, memoryview
        )
        return response

    def test_update_state_offloads_view_chunk_by_default(self):
        """With the flag unset, a 1 MiB chunk that reaches its destination as a
        memoryview is hashed on the worker pool and held until it verifies."""
        self._accept_memoryview_in_crc32c()
        content = self._large_chunk()
        read_state = self._add_download(
            _READ_ID, length=len(content), receives_views=True
        )
        response = self._create_view_response(
            content, _READ_ID, offset=0, range_end=True
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            self.strategy.update_state_from_response(response, self.state)

        self.assertEqual(read_state.bytes_written, 0)
        self.assertEqual(len(self.state["pending_checksums"]), 1)
        asyncio.run(self.strategy.verify_pending_checksums(self.state))
        self.assertEqual(read_state.user_buffer.getvalue(), content)
        self.assertTrue(read_state.is_complete)

    def test_update_state_hashes_inline_by_default_unless_views_reach_destination(
        self,
    ):
        """With the flag unset, a chunk is hashed inline when it is ``bytes``
        (the generated parser, or a google-crc32c without memoryview support)
        or when the SDK copies it to ``bytes`` for its destination."""
        self._accept_memoryview_in_crc32c()
        content = self._large_chunk()
        cases = (
            ("view chunk, bytes destination", True, False),
            ("bytes chunk, view destination", False, True),
        )
        for read_id, (name, view_chunk, receives_views) in enumerate(cases):
            with self.subTest(name), mock.patch.dict(os.environ, {}, clear=True):
                read_state = self._add_download(
                    read_id, length=len(content), receives_views=receives_views
                )
                create = (
                    self._create_view_response if view_chunk else self._create_response
                )
                response = create(content, read_id, offset=0, range_end=True)

                self.strategy.update_state_from_response(response, self.state)

                self.assertEqual(read_state.user_buffer.getvalue(), content)
                self.assertTrue(read_state.is_complete)
                self.assertNotIn("pending_checksums", self.state)

    def test_update_state_offload_flag_overrides_default_for_view_chunks(self):
        """A set GCS_PYTHON_CLIENT_CRC32C_OFFLOAD wins over the default: any
        value other than 1/true/yes/on keeps view chunks inline, and an empty
        value counts as unset."""
        self._accept_memoryview_in_crc32c()
        content = self._large_chunk()
        cases = (
            ("0", False),
            ("false", False),
            ("off", False),
            ("enabled", False),
            ("", True),
            ("1", True),
        )
        for read_id, (value, offloaded) in enumerate(cases):
            with (
                self.subTest(value=value),
                mock.patch.dict(os.environ, {_OFFLOAD_ENV_VAR: value}),
            ):
                read_state = self._add_download(
                    read_id, length=len(content), receives_views=True
                )
                response = self._create_view_response(
                    content, read_id, offset=0, range_end=True
                )

                self.strategy.update_state_from_response(response, self.state)

                held = self.state.get("pending_checksums") or ()
                self.assertEqual(len(held), 1 if offloaded else 0)
                asyncio.run(self.strategy.verify_pending_checksums(self.state))
                self.assertEqual(read_state.user_buffer.getvalue(), content)
                self.assertTrue(read_state.is_complete)

    def test_update_state_hashes_chunk_below_1_mib_inline_when_enabled(self):
        """google_crc32c holds the GIL below 1 MiB, so smaller chunks stay inline."""
        content = b"x" * (1024 * 1024 - 1)
        self._enable_offload()
        read_state = self._add_download(_READ_ID, length=len(content))
        response = self._create_response(content, _READ_ID, offset=0, range_end=True)

        self.strategy.update_state_from_response(response, self.state)

        self.assertEqual(read_state.user_buffer.getvalue(), content)
        self.assertNotIn("pending_checksums", self.state)

    def test_update_state_holds_large_chunk_until_verified(self):
        """Large chunks are written only once their offloaded checksum matches."""
        content = self._large_chunk()
        future = concurrent.futures.Future()
        self._offload_to([future])
        read_state = self._add_download(_READ_ID, length=len(content))
        response = self._create_response(content, _READ_ID, offset=0, range_end=True)

        self.strategy.update_state_from_response(response, self.state)

        self.assertEqual(read_state.user_buffer.getvalue(), b"")
        self.assertEqual(read_state.bytes_written, 0)
        self.assertFalse(read_state.is_complete)
        self.assertEqual(read_state.next_expected_offset, len(content))
        self.assertEqual(len(self.state["pending_checksums"]), 1)
        self.assertIs(self.state["pending_checksums"][0].checksum_future, future)

        future.set_result(google_crc32c.value(content))
        asyncio.run(self.strategy.verify_pending_checksums(self.state))

        self.assertEqual(read_state.user_buffer.getvalue(), content)
        self.assertEqual(read_state.bytes_written, len(content))
        self.assertTrue(read_state.is_complete)
        self.assertEqual(len(self.state["pending_checksums"]), 0)

    def test_verify_pending_checksums_mismatch_rewinds_to_corrupt_chunk(self):
        """Nothing from the corrupt chunk on is written; a retry resumes there."""
        content = self._large_chunk()
        size = len(content)
        futures = [concurrent.futures.Future() for _ in range(3)]
        for future, crc in zip(futures, (google_crc32c.value(content), 999999, 0)):
            future.set_result(crc)
        self._offload_to(futures)
        read_state = self._add_download(_READ_ID, offset=10, length=3 * size)
        for i in range(3):
            response = self._create_response(content, _READ_ID, offset=10 + i * size)
            self.strategy.update_state_from_response(response, self.state)

        with self.assertRaisesRegex(DataCorruption, "Checksum mismatch"):
            asyncio.run(self.strategy.verify_pending_checksums(self.state))

        self.assertEqual(read_state.user_buffer.getvalue(), content)
        self.assertEqual(read_state.bytes_written, size)
        self.assertEqual(read_state.next_expected_offset, 10 + size)
        self.assertEqual(len(self.state["pending_checksums"]), 0)
        (request,) = self.strategy.generate_requests(self.state)
        self.assertEqual(request.read_offset, 10 + size)
        self.assertEqual(request.read_length, 2 * size)

    def test_update_state_holds_small_chunk_behind_pending_one(self):
        """Chunks are written in arrival order, even if verified out of order."""
        large, small = self._large_chunk(), b"tail"
        future = concurrent.futures.Future()
        self._offload_to([future])
        read_state = self._add_download(_READ_ID, length=len(large) + len(small))
        responses = [
            self._create_response(large, _READ_ID, offset=0),
            self._create_response(small, _READ_ID, offset=len(large), range_end=True),
        ]
        for response in responses:
            self.strategy.update_state_from_response(response, self.state)

        self.assertEqual(read_state.user_buffer.getvalue(), b"")
        self.assertEqual(len(self.state["pending_checksums"]), 2)

        future.set_result(google_crc32c.value(large))
        asyncio.run(self.strategy.verify_pending_checksums(self.state))

        self.assertEqual(read_state.user_buffer.getvalue(), large + small)
        self.assertTrue(read_state.is_complete)

    def test_verify_pending_checksums_honors_max_pending(self):
        """Finished chunks are written at once; unfinished ones only block
        while more than max_pending are held."""
        content = self._large_chunk()
        futures = [concurrent.futures.Future() for _ in range(3)]
        futures[0].set_result(google_crc32c.value(content))
        self._offload_to(futures)
        read_state = self._add_download(_READ_ID, length=3 * len(content))
        for i in range(3):
            response = self._create_response(content, _READ_ID, offset=i * len(content))
            self.strategy.update_state_from_response(response, self.state)
        self.assertEqual(len(self.state["pending_checksums"]), 3)

        asyncio.run(self.strategy.verify_pending_checksums(self.state, max_pending=2))
        self.assertEqual(len(self.state["pending_checksums"]), 2)
        self.assertEqual(read_state.bytes_written, len(content))

        for future in futures[1:]:
            future.set_result(google_crc32c.value(content))
        asyncio.run(self.strategy.verify_pending_checksums(self.state))
        self.assertEqual(len(self.state["pending_checksums"]), 0)
        self.assertEqual(read_state.user_buffer.getvalue(), content * 3)

    def test_verify_pending_checksums_without_pending_is_noop(self):
        asyncio.run(self.strategy.verify_pending_checksums(self.state))
        self.assertNotIn("pending_checksums", self.state)

    def test_verify_pending_checksums_awaits_unfinished_future(self):
        content = self._large_chunk()
        future = concurrent.futures.Future()
        self._offload_to([future])
        self._add_download(_READ_ID, length=len(content))
        response = self._create_response(content, _READ_ID, offset=0)
        self.strategy.update_state_from_response(response, self.state)

        async def run():
            loop = asyncio.get_running_loop()
            loop.call_later(0.01, future.set_result, google_crc32c.value(content))
            await self.strategy.verify_pending_checksums(self.state)

        asyncio.run(run())
        self.assertEqual(len(self.state["pending_checksums"]), 0)

    def test_verify_pending_checksums_cancels_queued_futures_on_mismatch(self):
        """Work queued behind a corrupt chunk is dropped from the shared pool."""
        content = self._large_chunk()
        corrupt, queued = concurrent.futures.Future(), concurrent.futures.Future()
        corrupt.set_result(999999)
        self._offload_to([corrupt, queued])
        self._add_download(_READ_ID, length=2 * len(content))
        for i in range(2):
            response = self._create_response(content, _READ_ID, offset=i * len(content))
            self.strategy.update_state_from_response(response, self.state)

        with self.assertRaisesRegex(DataCorruption, "Checksum mismatch"):
            asyncio.run(self.strategy.verify_pending_checksums(self.state))

        self.assertTrue(queued.cancelled())
        self.assertEqual(len(self.state["pending_checksums"]), 0)

    def test_verify_pending_checksums_discards_queue_when_worker_raises(self):
        content = self._large_chunk()
        failed, queued = concurrent.futures.Future(), concurrent.futures.Future()
        failed.set_exception(TypeError("worker failed"))
        self._offload_to([failed, queued])
        read_state = self._add_download(_READ_ID, length=2 * len(content))
        for i in range(2):
            response = self._create_response(content, _READ_ID, offset=i * len(content))
            self.strategy.update_state_from_response(response, self.state)

        with self.assertRaisesRegex(TypeError, "worker failed"):
            asyncio.run(self.strategy.verify_pending_checksums(self.state))

        self.assertTrue(queued.cancelled())
        self.assertEqual(len(self.state["pending_checksums"]), 0)
        self.assertEqual(read_state.next_expected_offset, 0)

    def test_discard_pending_checksums_cancels_and_rewinds(self):
        content = self._large_chunk()
        future = concurrent.futures.Future()
        self._offload_to([future])
        read_state = self._add_download(_READ_ID, offset=5, length=len(content) + 4)
        responses = [
            self._create_response(content, _READ_ID, offset=5),
            self._create_response(b"tail", _READ_ID, offset=5 + len(content)),
        ]
        for response in responses:
            self.strategy.update_state_from_response(response, self.state)

        self.strategy.discard_pending_checksums(self.state)

        self.assertTrue(future.cancelled())
        self.assertEqual(len(self.state["pending_checksums"]), 0)
        self.assertEqual(read_state.next_expected_offset, 5)
        self.assertEqual(read_state.user_buffer.getvalue(), b"")

    def test_discard_pending_checksums_without_pending_is_noop(self):
        self.strategy.discard_pending_checksums(self.state)
        self.assertNotIn("pending_checksums", self.state)

    def test_verify_pending_checksums_checks_byte_count_of_held_chunk(self):
        content = self._large_chunk()
        self._enable_offload()
        self._add_download(_READ_ID, length=len(content) - 1)
        response = self._create_response(content, _READ_ID, offset=0, range_end=True)
        self.strategy.update_state_from_response(response, self.state)

        with self.assertRaisesRegex(DataCorruption, "Byte count mismatch"):
            asyncio.run(self.strategy.verify_pending_checksums(self.state))

    def test_update_state_hashes_inline_when_pool_rejects_work(self):
        """After interpreter shutdown begins, submit() raises RuntimeError."""
        content = self._large_chunk()
        self._enable_offload()
        executor = mock.Mock()
        executor.submit.side_effect = RuntimeError(
            "cannot schedule new futures after interpreter shutdown"
        )
        patcher = mock.patch.object(
            reads_resumption_strategy, "_crc32c_executor", executor
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        read_state = self._add_download(_READ_ID, length=2 * len(content))

        response = self._create_response(content, _READ_ID, offset=0)
        self.strategy.update_state_from_response(response, self.state)
        self.assertEqual(read_state.user_buffer.getvalue(), content)
        self.assertNotIn("pending_checksums", self.state)

        response = self._create_response(
            content, _READ_ID, offset=len(content), crc=999999
        )
        with self.assertRaisesRegex(DataCorruption, "Checksum mismatch"):
            self.strategy.update_state_from_response(response, self.state)
        self.assertEqual(read_state.bytes_written, len(content))

    def test_update_state_large_chunk_not_deferred_when_checksum_disabled(self):
        content = self._large_chunk()
        self._enable_offload()
        self.state["enable_checksum"] = False
        self._add_download(_READ_ID, length=len(content))
        response = self._create_response(content, _READ_ID, offset=0, crc=999999)

        self.strategy.update_state_from_response(response, self.state)

        self.assertNotIn("pending_checksums", self.state)

    def test_update_state_full_object_read_hashes_large_chunk_inline(self):
        """Full-object reads already hash every chunk into the rolling checksum
        on the calling thread, so a worker-side hash would only be overhead."""
        content = self._large_chunk()
        self._enable_offload()
        read_state = self._add_download(
            _READ_ID, length=len(content), is_full_object_read=True
        )
        response = self._create_response(content, _READ_ID, offset=0)

        self.strategy.update_state_from_response(response, self.state)

        self.assertNotIn("pending_checksums", self.state)
        self.assertEqual(read_state.rolling_checksum._crc, google_crc32c.value(content))

    def test_update_state_full_object_read_large_chunk_mismatch_raises_inline(self):
        content = self._large_chunk()
        self._enable_offload()
        self._add_download(_READ_ID, length=len(content), is_full_object_read=True)
        response = self._create_response(content, _READ_ID, offset=0, crc=999999)

        with self.assertRaisesRegex(DataCorruption, "Checksum mismatch"):
            self.strategy.update_state_from_response(response, self.state)

    def test_update_state_final_byte_count_mismatch(self):
        """Test mismatch between expected length and actual bytes written on completion."""
        self._add_download(_READ_ID, length=100)

        data = b"data" * 30
        response = self._create_response(data, _READ_ID, offset=0, range_end=True)

        with self.assertRaisesRegex(DataCorruption, "Byte count mismatch"):
            self.strategy.update_state_from_response(response, self.state)

    def test_update_state_completes_download(self):
        """Test that the download is marked complete on range_end."""
        data = b"test_data"
        read_state = self._add_download(_READ_ID, length=len(data))

        response = self._create_response(data, _READ_ID, offset=0, range_end=True)

        self.strategy.update_state_from_response(response, self.state)

        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.bytes_written, len(data))

    def test_update_state_completes_download_zero_length(self):
        """Test completion for a download with initial_length of 0."""
        read_state = self._add_download(_READ_ID, length=0)
        data = b"test_data"

        response = self._create_response(data, _READ_ID, offset=0, range_end=True)

        self.strategy.update_state_from_response(response, self.state)

        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.bytes_written, len(data))

    def test_update_state_zero_byte_file(self):
        """Test downloading a completely empty file."""
        read_state = self._add_download(_READ_ID, length=0)

        response = self._create_response(b"", _READ_ID, offset=0, range_end=True)

        self.strategy.update_state_from_response(response, self.state)

        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.bytes_written, 0)
        self.assertEqual(read_state.user_buffer.getvalue(), b"")

    def test_update_state_missing_read_range_logs_warning(self):
        """Verify we log a warning and continue when read_range is missing."""
        response = self._create_response(b"data", _READ_ID, 0, has_read_range=False)

        # assertLogs captures logs for the given logger name and minimum level
        with self.assertLogs(LOGGER_NAME, level="WARNING") as cm:
            self.strategy.update_state_from_response(response, self.state)

        self.assertTrue(
            any("missing read_range field" in output for output in cm.output)
        )

    def test_update_state_unknown_id_logs_warning(self):
        """Verify we log a warning and continue when read_id is unknown."""
        unknown_id = 999
        self._add_download(_READ_ID)
        response = self._create_response(b"ghost", read_id=unknown_id, offset=0)

        with self.assertLogs(LOGGER_NAME, level="WARNING") as cm:
            self.strategy.update_state_from_response(response, self.state)

        self.assertTrue(
            any(
                f"unknown or stale read_id {unknown_id}" in output
                for output in cm.output
            )
        )

    # --- Recovery Tests ---

    def test_recover_state_on_failure_handles_redirect(self):
        """Verify recover_state_on_failure correctly extracts routing_token."""
        token = "dummy-routing-token"
        redirect_error = BidiReadObjectRedirectedError(routing_token=token)
        final_error = exceptions.Aborted("Retry failed", errors=[redirect_error])

        async def run():
            await self.strategy.recover_state_on_failure(final_error, self.state)

        asyncio.new_event_loop().run_until_complete(run())

        self.assertEqual(self.state["routing_token"], token)

    def test_recover_state_ignores_standard_errors(self):
        """Verify that non-redirect errors do not corrupt the routing token."""
        self.state["routing_token"] = "existing-token"

        std_error = exceptions.ServiceUnavailable("Maintenance")
        final_error = exceptions.RetryError("Retry failed", cause=std_error)

        async def run():
            await self.strategy.recover_state_on_failure(final_error, self.state)

        asyncio.new_event_loop().run_until_complete(run())

        # Token should remain unchanged
        self.assertEqual(self.state["routing_token"], "existing-token")

    def test_recover_state_on_failure_raises_for_corrupt_pending_chunk(self):
        """A corrupt chunk received before a stream error aborts instead of retrying,
        without writing it; the redirect is still recorded."""
        content = self._large_chunk()
        self._enable_offload()
        read_state = self._add_download(_READ_ID, length=len(content))
        response = self._create_response(content, _READ_ID, offset=0, crc=999999)
        self.strategy.update_state_from_response(response, self.state)
        token = "dummy-routing-token"
        final_error = exceptions.Aborted(
            "Retry failed", errors=[BidiReadObjectRedirectedError(routing_token=token)]
        )

        with self.assertRaisesRegex(DataCorruption, "Checksum mismatch"):
            asyncio.run(self.strategy.recover_state_on_failure(final_error, self.state))

        self.assertEqual(self.state["routing_token"], token)
        self.assertEqual(read_state.user_buffer.getvalue(), b"")
        (request,) = self.strategy.generate_requests(self.state)
        self.assertEqual(request.read_offset, 0)

    def test_recover_state_on_failure_drains_pending_checksums(self):
        """Verified chunks are written before the retry computes its offsets."""
        content = self._large_chunk()
        future = concurrent.futures.Future()
        self._offload_to([future])
        read_state = self._add_download(_READ_ID, length=2 * len(content))
        response = self._create_response(content, _READ_ID, offset=0)
        self.strategy.update_state_from_response(response, self.state)
        token = "dummy-routing-token"
        final_error = exceptions.Aborted(
            "Retry failed", errors=[BidiReadObjectRedirectedError(routing_token=token)]
        )

        async def run():
            asyncio.get_running_loop().call_later(
                0.01, future.set_result, google_crc32c.value(content)
            )
            await self.strategy.recover_state_on_failure(final_error, self.state)

        asyncio.run(run())

        self.assertEqual(len(self.state["pending_checksums"]), 0)
        self.assertEqual(self.state["routing_token"], token)
        self.assertEqual(read_state.user_buffer.getvalue(), content)
        (request,) = self.strategy.generate_requests(self.state)
        self.assertEqual(request.read_offset, len(content))

    def test_update_state_full_object_checksum_success(self):
        """Test that full object checksum verification succeeds on range_end."""
        read_state = self._add_download(
            _READ_ID, offset=0, length=9, is_full_object_read=True
        )
        self.state["enable_checksum"] = True
        self.state["full_obj_server_crc32c"] = google_crc32c.value(b"testdata1")

        resp1 = self._create_response(b"test", _READ_ID, offset=0)
        self.strategy.update_state_from_response(resp1, self.state)

        resp2 = self._create_response(b"data1", _READ_ID, offset=4, range_end=True)
        self.strategy.update_state_from_response(resp2, self.state)

        self.assertTrue(read_state.is_complete)
        self.assertEqual(read_state.bytes_written, 9)

    def test_update_state_full_object_checksum_failure(self):
        """Test that full object checksum verification raises DataCorruption on mismatch at range_end."""
        self._add_download(_READ_ID, offset=0, length=9, is_full_object_read=True)
        self.state["enable_checksum"] = True
        self.state["full_obj_server_crc32c"] = 111111  # Wrong server checksum!

        resp1 = self._create_response(b"test", _READ_ID, offset=0)
        self.strategy.update_state_from_response(resp1, self.state)

        resp2 = self._create_response(b"data1", _READ_ID, offset=4, range_end=True)
        with self.assertRaisesRegex(DataCorruption, "Full object checksum mismatch"):
            self.strategy.update_state_from_response(resp2, self.state)

    def test_update_state_checksum_mismatch_ignored_when_disabled(self):
        """Test that a CRC32C mismatch is ignored when enable_checksum is False."""
        self._add_download(_READ_ID)
        self.state["enable_checksum"] = False
        response = self._create_response(b"data", _READ_ID, offset=0, crc=999999)

        # Should NOT raise DataCorruption!
        self.strategy.update_state_from_response(response, self.state)

    def test_update_state_full_object_checksum_mismatch_ignored_when_disabled(self):
        """Test that a full-object CRC32C mismatch is ignored when enable_checksum is False."""
        self._add_download(
            _READ_ID,
            offset=0,
            length=9,
            is_full_object_read=True,
            enable_checksum=False,
        )
        self.state["enable_checksum"] = False
        self.state["full_obj_server_crc32c"] = 111111  # Wrong server checksum!

        resp1 = self._create_response(b"test", _READ_ID, offset=0)
        self.strategy.update_state_from_response(resp1, self.state)

        resp2 = self._create_response(b"data1", _READ_ID, offset=4, range_end=True)
        # Should NOT raise DataCorruption!
        self.strategy.update_state_from_response(resp2, self.state)


class TestCrc32cExecutor(unittest.TestCase):
    def test_reset_replaces_the_pool(self):
        pool = reads_resumption_strategy._crc32c_executor
        self.addCleanup(setattr, reads_resumption_strategy, "_crc32c_executor", pool)

        reads_resumption_strategy._reset_crc32c_executor()

        new_pool = reads_resumption_strategy._crc32c_executor
        self.addCleanup(new_pool.shutdown)
        self.assertIsNot(new_pool, pool)
        self.assertEqual(new_pool.submit(int, "7").result(), 7)

    @unittest.skipUnless(hasattr(os, "fork"), "requires os.fork")
    def test_forked_child_gets_a_working_pool(self):
        """The parent's pool has no threads in a forked child; work sent to it
        would never run."""
        pool = reads_resumption_strategy._crc32c_executor
        self.assertEqual(pool.submit(int, "7").result(), 7)
        with warnings.catch_warnings():
            # Python 3.12+ warns about forking a process that has threads.
            warnings.simplefilter("ignore", DeprecationWarning)
            pid = os.fork()
        if pid == 0:  # pragma: NO COVER - the child exits without saving coverage
            ok = False
            try:
                signal.alarm(30)  # never leave the parent waiting on a hung child
                child_pool = reads_resumption_strategy._crc32c_executor
                ok = child_pool is not pool and (
                    child_pool.submit(int, "7").result(timeout=10) == 7
                )
            finally:
                os._exit(0 if ok else 1)
        _, status = os.waitpid(pid, 0)
        self.assertEqual(os.waitstatus_to_exitcode(status), 0)
