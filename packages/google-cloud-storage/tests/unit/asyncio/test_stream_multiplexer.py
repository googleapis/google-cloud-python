# Copyright 2026 Google LLC
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
from unittest.mock import AsyncMock

import pytest

from google.cloud import _storage_v2
from google.cloud.storage.asyncio._stream_multiplexer import (
    _DEFAULT_QUEUE_MAX_SIZE,
    _StreamEnd,
    _StreamError,
    _StreamMultiplexer,
)


class TestSentinelTypes:
    def test_stream_error_stores_exception_and_generation(self):
        exc = ValueError("test")
        error = _StreamError(exc, generation=3)
        assert error.exception is exc
        assert error.generation == 3

    def test_stream_end_is_instantiable(self):
        sentinel = _StreamEnd()
        assert isinstance(sentinel, _StreamEnd)


class TestStreamMultiplexerInit:
    def test_init_sets_stream_and_defaults(self):
        mock_stream = AsyncMock()
        mux = _StreamMultiplexer(mock_stream)
        assert mux._stream is mock_stream
        assert mux.stream_generation == 0
        assert mux._queues == {}
        assert mux._recv_task is None
        assert mux._queue_max_size == _DEFAULT_QUEUE_MAX_SIZE

    def test_init_custom_queue_size(self):
        mock_stream = AsyncMock()
        mux = _StreamMultiplexer(mock_stream, queue_max_size=50)
        assert mux._queue_max_size == 50


def _make_response(read_id, data=b"data", range_end=False):
    return _storage_v2.BidiReadObjectResponse(
        object_data_ranges=[
            _storage_v2.ObjectRangeData(
                checksummed_data=_storage_v2.ChecksummedData(content=data),
                read_range=_storage_v2.ReadRange(
                    read_id=read_id, read_offset=0, read_length=len(data)
                ),
                range_end=range_end,
            )
        ]
    )


def _make_multi_range_response(read_ids, data=b"data"):
    ranges = []
    for rid in read_ids:
        ranges.append(
            _storage_v2.ObjectRangeData(
                checksummed_data=_storage_v2.ChecksummedData(content=data),
                read_range=_storage_v2.ReadRange(
                    read_id=rid, read_offset=0, read_length=len(data)
                ),
            )
        )
    return _storage_v2.BidiReadObjectResponse(object_data_ranges=ranges)


class TestRegisterUnregister:
    def _make_multiplexer(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        return _StreamMultiplexer(mock_stream), mock_stream

    @pytest.mark.asyncio
    async def test_register_returns_bounded_queue(self):
        mux, _ = self._make_multiplexer()
        queue = mux.register({1, 2, 3})
        assert isinstance(queue, asyncio.Queue)
        assert queue.maxsize == _DEFAULT_QUEUE_MAX_SIZE
        mux.unregister({1, 2, 3})

    @pytest.mark.asyncio
    async def test_register_maps_read_ids_to_same_queue(self):
        mux, _ = self._make_multiplexer()
        queue = mux.register({10, 20})
        assert mux._queues[10] is queue
        assert mux._queues[20] is queue
        mux.unregister({10, 20})

    @pytest.mark.asyncio
    async def test_register_does_not_start_recv_loop(self):
        mux, _ = self._make_multiplexer()
        assert mux._recv_task is None
        mux.register({1})
        assert mux._recv_task is None
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_two_registers_get_separate_queues(self):
        mux, _ = self._make_multiplexer()
        q1 = mux.register({1})
        q2 = mux.register({2})
        assert q1 is not q2
        assert mux._queues[1] is q1
        assert mux._queues[2] is q2
        mux.unregister({1, 2})

    @pytest.mark.asyncio
    async def test_unregister_removes_read_ids(self):
        mux, _ = self._make_multiplexer()
        mux.register({1, 2})
        mux.unregister({1})
        assert 1 not in mux._queues
        assert 2 in mux._queues
        mux.unregister({2})

    @pytest.mark.asyncio
    async def test_unregister_all_does_not_stop_recv_loop(self):
        mux, _ = self._make_multiplexer()
        mux.register({1})
        mux._ensure_recv_loop()
        recv_task = mux._recv_task
        assert recv_task is not None
        mux.unregister({1})
        await asyncio.sleep(0)
        assert not recv_task.cancelled()

    @pytest.mark.asyncio
    async def test_unregister_nonexistent_is_noop(self):
        mux, _ = self._make_multiplexer()
        mux.register({1})
        mux.unregister({999})
        assert 1 in mux._queues
        mux.unregister({1})


class TestRecvLoop:
    @pytest.mark.asyncio
    async def test_routes_response_by_read_id(self):
        mock_stream = AsyncMock()
        resp1 = _make_response(read_id=10, data=b"hello")
        resp2 = _make_response(read_id=20, data=b"world")
        mock_stream.recv = AsyncMock(side_effect=[resp1, resp2, None])

        mux = _StreamMultiplexer(mock_stream)
        q1 = mux.register({10})
        q2 = mux.register({20})
        mux._ensure_recv_loop()

        item1 = await asyncio.wait_for(q1.get(), timeout=1)
        item2 = await asyncio.wait_for(q2.get(), timeout=1)

        assert item1 is resp1
        assert item2 is resp2
        end1 = await asyncio.wait_for(q1.get(), timeout=1)
        end2 = await asyncio.wait_for(q2.get(), timeout=1)
        assert isinstance(end1, _StreamEnd)
        assert isinstance(end2, _StreamEnd)
        mux.unregister({10, 20})

    @pytest.mark.asyncio
    async def test_deduplicates_when_multiple_read_ids_map_to_same_queue(self):
        mock_stream = AsyncMock()
        resp = _make_multi_range_response([10, 11])
        mock_stream.recv = AsyncMock(side_effect=[resp, None])

        mux = _StreamMultiplexer(mock_stream)
        queue = mux.register({10, 11})
        mux._ensure_recv_loop()

        item = await asyncio.wait_for(queue.get(), timeout=1)
        assert item is resp
        end = await asyncio.wait_for(queue.get(), timeout=1)
        assert isinstance(end, _StreamEnd)
        mux.unregister({10, 11})

    @pytest.mark.asyncio
    async def test_metadata_only_response_broadcast_to_all(self):
        mock_stream = AsyncMock()
        metadata_resp = _storage_v2.BidiReadObjectResponse(
            read_handle=_storage_v2.BidiReadHandle(handle=b"handle")
        )
        mock_stream.recv = AsyncMock(side_effect=[metadata_resp, None])

        mux = _StreamMultiplexer(mock_stream)
        q1 = mux.register({10})
        q2 = mux.register({20})
        mux._ensure_recv_loop()

        item1 = await asyncio.wait_for(q1.get(), timeout=1)
        item2 = await asyncio.wait_for(q2.get(), timeout=1)
        assert item1 is metadata_resp
        assert item2 is metadata_resp
        mux.unregister({10, 20})

    @pytest.mark.asyncio
    async def test_stream_end_sends_sentinel_to_all_queues(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(return_value=None)

        mux = _StreamMultiplexer(mock_stream)
        q1 = mux.register({10})
        q2 = mux.register({20})
        mux._ensure_recv_loop()

        end1 = await asyncio.wait_for(q1.get(), timeout=1)
        end2 = await asyncio.wait_for(q2.get(), timeout=1)
        assert isinstance(end1, _StreamEnd)
        assert isinstance(end2, _StreamEnd)
        mux.unregister({10, 20})

    @pytest.mark.asyncio
    async def test_error_broadcasts_stream_error_to_all_queues(self):
        mock_stream = AsyncMock()
        exc = RuntimeError("stream broke")
        mock_stream.recv = AsyncMock(side_effect=exc)

        mux = _StreamMultiplexer(mock_stream)
        q1 = mux.register({10})
        q2 = mux.register({20})
        mux._ensure_recv_loop()

        await asyncio.sleep(0.05)

        err1 = q1.get_nowait()
        err2 = q2.get_nowait()
        assert isinstance(err1, _StreamError)
        assert err1.exception is exc
        assert err1.generation == 0
        assert isinstance(err2, _StreamError)
        assert err2.exception is exc
        mux.unregister({10, 20})

    @pytest.mark.asyncio
    async def test_error_uses_put_nowait(self):
        mock_stream = AsyncMock()
        exc = RuntimeError("broke")
        mock_stream.recv = AsyncMock(side_effect=exc)

        mux = _StreamMultiplexer(mock_stream, queue_max_size=1)
        queue = mux.register({10})
        queue.put_nowait("filler")
        mux._ensure_recv_loop()

        await asyncio.sleep(0.05)

        # Queue is full (maxsize=1), but _put_error_nowait pops existing items
        # to ensure the error gets recorded.
        assert queue.qsize() == 1
        err = queue.get_nowait()
        assert isinstance(err, _StreamError)
        assert err.exception is exc
        mux.unregister({10})

    @pytest.mark.asyncio
    async def test_unknown_read_id_is_dropped(self):
        mock_stream = AsyncMock()
        resp = _make_response(read_id=999)
        mock_stream.recv = AsyncMock(side_effect=[resp, None])

        mux = _StreamMultiplexer(mock_stream)
        queue = mux.register({10})
        mux._ensure_recv_loop()

        end = await asyncio.wait_for(queue.get(), timeout=1)
        assert isinstance(end, _StreamEnd)
        mux.unregister({10})


class TestSend:
    @pytest.mark.asyncio
    async def test_send_forwards_to_stream(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(mock_stream)

        request = _storage_v2.BidiReadObjectRequest(
            read_ranges=[
                _storage_v2.ReadRange(read_id=1, read_offset=0, read_length=10)
            ]
        )
        gen = await mux.send(request)
        mock_stream.send.assert_called_once_with(request)
        assert gen == 0

    @pytest.mark.asyncio
    async def test_send_returns_current_generation(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(mock_stream)
        mux._stream_generation = 5

        request = _storage_v2.BidiReadObjectRequest()
        gen = await mux.send(request)
        assert gen == 5

    @pytest.mark.asyncio
    async def test_send_propagates_exception(self):
        mock_stream = AsyncMock()
        mock_stream.send = AsyncMock(side_effect=RuntimeError("send failed"))
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(mock_stream)

        with pytest.raises(RuntimeError, match="send failed"):
            await mux.send(_storage_v2.BidiReadObjectRequest())


class TestReopenStream:
    @pytest.mark.asyncio
    async def test_reopen_bumps_generation_and_replaces_stream(self):
        old_stream = AsyncMock()
        old_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(old_stream)
        mux.register({1})
        assert mux.stream_generation == 0

        new_stream = AsyncMock()
        new_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        factory = AsyncMock(return_value=new_stream)

        await mux.reopen_stream(0, factory)

        assert mux.stream_generation == 1
        assert mux._stream is new_stream
        factory.assert_called_once()
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_reopen_skips_if_generation_mismatch(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(mock_stream)
        mux._stream_generation = 5
        mux.register({1})

        factory = AsyncMock()
        await mux.reopen_stream(3, factory)

        assert mux.stream_generation == 5
        factory.assert_not_called()
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_reopen_broadcasts_error_before_bump(self):
        old_stream = AsyncMock()
        old_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(old_stream)
        queue = mux.register({1})

        new_stream = AsyncMock()
        new_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        factory = AsyncMock(return_value=new_stream)

        await mux.reopen_stream(0, factory)

        err = queue.get_nowait()
        assert isinstance(err, _StreamError)
        assert err.generation == 0
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_reopen_starts_new_recv_loop(self):
        old_stream = AsyncMock()
        old_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(old_stream)
        mux.register({1})
        old_recv_task = mux._recv_task

        new_stream = AsyncMock()
        new_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        factory = AsyncMock(return_value=new_stream)

        await mux.reopen_stream(0, factory)

        assert mux._recv_task is not old_recv_task
        assert not mux._recv_task.done()
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_reopen_closes_old_stream_best_effort(self):
        old_stream = AsyncMock()
        old_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        old_stream.close = AsyncMock(side_effect=RuntimeError("close failed"))
        mux = _StreamMultiplexer(old_stream)
        mux.register({1})

        new_stream = AsyncMock()
        new_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        factory = AsyncMock(return_value=new_stream)

        await mux.reopen_stream(0, factory)
        assert mux.stream_generation == 1
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_concurrent_reopen_only_one_wins(self):
        old_stream = AsyncMock()
        old_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(old_stream)
        mux.register({1})

        call_count = 0

        async def counting_factory():
            nonlocal call_count
            call_count += 1
            new_stream = AsyncMock()
            new_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
            return new_stream

        await asyncio.gather(
            mux.reopen_stream(0, counting_factory),
            mux.reopen_stream(0, counting_factory),
        )

        assert call_count == 1
        assert mux.stream_generation == 1
        mux.unregister({1})

    @pytest.mark.asyncio
    async def test_reopen_factory_failure_leaves_generation_unchanged(self):
        """If stream_factory raises, generation is not bumped and recv loop
        is not restarted. The caller's retry manager will re-attempt reopen
        with the same generation, which will succeed because the generation
        check still matches."""
        old_stream = AsyncMock()
        old_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(old_stream)
        mux.register({1})

        failing_factory = AsyncMock(side_effect=RuntimeError("open failed"))

        with pytest.raises(RuntimeError, match="open failed"):
            await mux.reopen_stream(0, failing_factory)

        # Generation was NOT bumped
        assert mux.stream_generation == 0
        # Recv loop was stopped and not restarted
        assert mux._recv_task is None or mux._recv_task.done()

        # A subsequent reopen with the same generation succeeds
        new_stream = AsyncMock()
        new_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        ok_factory = AsyncMock(return_value=new_stream)

        await mux.reopen_stream(0, ok_factory)

        assert mux.stream_generation == 1
        assert mux._stream is new_stream
        assert mux._recv_task is not None and not mux._recv_task.done()
        mux.unregister({1})


class TestClose:
    @pytest.mark.asyncio
    async def test_close_cancels_recv_loop(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(mock_stream)
        mux.register({1})
        mux._ensure_recv_loop()
        recv_task = mux._recv_task

        await mux.close()
        assert recv_task.cancelled()

    @pytest.mark.asyncio
    async def test_close_broadcasts_terminal_error(self):
        mock_stream = AsyncMock()
        mock_stream.recv = AsyncMock(side_effect=asyncio.Event().wait)
        mux = _StreamMultiplexer(mock_stream)
        q1 = mux.register({1})
        q2 = mux.register({2})

        await mux.close()

        err1 = q1.get_nowait()
        err2 = q2.get_nowait()
        assert isinstance(err1, _StreamError)
        assert isinstance(err2, _StreamError)

    @pytest.mark.asyncio
    async def test_close_with_no_tasks_is_noop(self):
        mock_stream = AsyncMock()
        mux = _StreamMultiplexer(mock_stream)
        await mux.close()  # should not raise
