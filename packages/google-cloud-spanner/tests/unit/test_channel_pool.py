# Copyright 2026 Google LLC All rights reserved.
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

import gc
import time
import unittest
from unittest import mock

import grpc
from google.api_core.exceptions import FailedPrecondition, ServiceUnavailable

from google.cloud.spanner_v1.channel_pool import (
    AffinityKind,
    ChannelEntry,
    ChannelLease,
    ChannelPool,
    ChannelPoolOptions,
    ChannelState,
    TransactionAffinity,
    _SyncStreamWrapper,
    _SyncUnaryStreamMultiCallable,
    _SyncUnaryUnaryMultiCallable,
    is_channel_pool_enabled,
    pick_channel_p2c,
)
from google.cloud.spanner_v1.request_id_header import (
    X_GOOG_SPANNER_REQUEST_ID_SPAN_ATTR,
)


class MockSyncGrpcChannel:
    """Mock sync gRPC channel simulating unary and streaming calls."""

    def __init__(self, name="mock-sync-channel"):
        self.name = name
        self.closed = False
        self.close_call_count = 0

    def close(self):
        self.closed = True
        self.close_call_count += 1

    def unary_unary(self, method, request_serializer=None, response_deserializer=None):
        def invoker(
            request,
            timeout=None,
            metadata=None,
            credentials=None,
            wait_for_ready=None,
            compression=None,
        ):
            return {
                "method": method,
                "request": request,
                "metadata": metadata,
                "channel": self.name,
            }

        return invoker

    def unary_stream(self, method, request_serializer=None, response_deserializer=None):
        def invoker(
            request,
            timeout=None,
            metadata=None,
            credentials=None,
            wait_for_ready=None,
            compression=None,
        ):
            class MockSyncStream:
                def __init__(self, items):
                    self.items = items
                    self.closed = False
                    self.fail_on_next = False
                    self.fail_on_cancel = False

                def __iter__(self):
                    return self

                def __next__(self):
                    if self.fail_on_next:
                        raise RuntimeError("stream next error")
                    if not self.items:
                        raise StopIteration
                    return self.items.pop(0)

                def cancel(self):
                    if self.fail_on_cancel:
                        raise RuntimeError("cancel failure")
                    self.closed = True

            return MockSyncStream(["row_1", "row_2"])

        return invoker


class TestSyncChannelPoolOptions(unittest.TestCase):
    def test_default_options(self):
        options = ChannelPoolOptions()
        self.assertEqual(options.min_channels, 4)
        self.assertEqual(options.max_channels, 10)
        self.assertEqual(options.initial_channels, 4)
        self.assertEqual(options.max_rpc_per_channel, 25)
        self.assertEqual(options.min_rpc_per_channel, 10)
        self.assertEqual(options.scale_up_step_factor, 0.30)
        self.assertEqual(options.min_scale_up_step, 2)
        self.assertEqual(options.scale_down_period_seconds, 60.0)

    def test_validation_success(self):
        options = ChannelPoolOptions(
            min_channels=2, max_channels=10, initial_channels=4
        )
        options.validate()
        self.assertEqual(options.min_channels, 2)
        self.assertEqual(options.max_channels, 10)
        self.assertEqual(options.initial_channels, 4)

    def test_validation_min_channels_zero(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_channels=0)

    def test_validation_min_greater_than_max(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_channels=10, max_channels=5)

    def test_validation_initial_channels_out_of_bounds(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_channels=4, max_channels=10, initial_channels=2)

        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_channels=4, max_channels=10, initial_channels=12)

    def test_validation_max_rpc_per_channel_invalid(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_rpc_per_channel=20, max_rpc_per_channel=10)

    def test_validation_scale_up_step_factor_invalid(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_up_step_factor=-0.1)
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_up_step_factor=1.5)

    def test_validation_scale_down_period_invalid(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_down_period_seconds=0)

    def test_from_dict(self):
        config_dict = {
            "min_channels": 2,
            "max_channels": 6,
            "max_rpc_per_channel": 40,
        }
        options = ChannelPoolOptions.from_dict(config_dict)
        self.assertEqual(options.min_channels, 2)
        self.assertEqual(options.max_channels, 6)
        self.assertEqual(options.max_rpc_per_channel, 40)

    def test_target_rpc_per_channel(self):
        options = ChannelPoolOptions(min_rpc_per_channel=10, max_rpc_per_channel=25)
        self.assertEqual(options.target_rpc_per_channel(), 17)

    def test_desired_channel_count(self):
        options = ChannelPoolOptions(
            min_channels=2,
            max_channels=10,
            min_rpc_per_channel=10,
            max_rpc_per_channel=30,
        )
        # target = (10 + 30) // 2 = 20
        self.assertEqual(options.desired_channel_count(0), 2)
        self.assertEqual(options.desired_channel_count(20), 2)
        self.assertEqual(options.desired_channel_count(60), 3)
        self.assertEqual(options.desired_channel_count(100), 5)
        self.assertEqual(options.desired_channel_count(500), 10)

    def test_validation_min_scale_up_step_invalid(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_scale_up_step=0).validate()

    def test_validation_additional_invalid_parameters(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_rpc_per_channel=-1).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(
                min_rpc_per_channel=20, max_rpc_per_channel=10
            ).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(max_scale_up_percent=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(max_scale_up_percent=150).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(max_remove_channels=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_down_interval_secs=0.0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_up_cooldown_seconds=-1.0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_down_consecutive_checks=0).validate()


class TestSyncChannelEntry(unittest.TestCase):
    def test_channel_entry_counters(self):
        mock_channel = MockSyncGrpcChannel("ch-1")
        entry = ChannelEntry(entry_id=1, logical_channel_id=1, channel=mock_channel)

        self.assertEqual(entry.entry_id, 1)
        self.assertEqual(entry.logical_channel_id, 1)
        self.assertEqual(entry.state, ChannelState.ACTIVE)
        self.assertEqual(entry.in_flight_rpcs, 0)
        self.assertEqual(entry.active_rw_transactions, 0)

        entry.increment_in_flight()
        self.assertEqual(entry.in_flight_rpcs, 1)
        entry.decrement_in_flight()
        self.assertEqual(entry.in_flight_rpcs, 0)

        entry.increment_rw_transaction()
        self.assertEqual(entry.active_rw_transactions, 1)
        entry.decrement_rw_transaction()
        self.assertEqual(entry.active_rw_transactions, 0)

        entry.set_state(ChannelState.DRAINING)
        self.assertEqual(entry.state, ChannelState.DRAINING)

    def test_channel_entry_additional_branches(self):
        mock_channel = MockSyncGrpcChannel("ch-1")
        entry = ChannelEntry(entry_id=1, logical_channel_id=1, channel=mock_channel)
        self.assertEqual(entry.decrement_active_rw(), 0)

        entry.touch_activity()
        self.assertGreaterEqual(entry.elapsed_since_activity(), 0.0)

        def sentinel_call(*args, **kwargs):
            return "cached"

        count = 0

        class SimulatedRaceDict(dict):
            def get(self, key, default=None):
                nonlocal count
                count += 1
                if count == 1:
                    return None
                return sentinel_call

        entry._unary_unary_cache = SimulatedRaceDict()
        self.assertIs(entry.get_unary_unary("/test/method"), sentinel_call)

        stream_count = 0

        class SimulatedStreamRaceDict(dict):
            def get(self, key, default=None):
                nonlocal stream_count
                stream_count += 1
                if stream_count == 1:
                    return None
                return sentinel_call

        entry._unary_stream_cache = SimulatedStreamRaceDict()
        self.assertIs(entry.get_unary_stream("/test/method"), sentinel_call)


class TestSyncP2CSelection(unittest.TestCase):
    def test_p2c_picks_less_loaded_channel(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        entry1 = ChannelEntry(1, 1, c1)
        entry2 = ChannelEntry(2, 2, c2)

        entry1.increment_in_flight()
        entry1.increment_in_flight()
        entry2.increment_in_flight()

        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            chosen = pick_channel_p2c([entry1, entry2])
            self.assertEqual(chosen, entry2)

    def test_p2c_tie_breaker_active_rw_transactions(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        entry1 = ChannelEntry(1, 1, c1)
        entry2 = ChannelEntry(2, 2, c2)

        entry1.increment_in_flight()
        entry2.increment_in_flight()
        entry1.increment_rw_transaction()

        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            chosen = pick_channel_p2c([entry1, entry2])
            self.assertEqual(chosen, entry2)

    def test_p2c_tie_breaker_random_when_load_equal(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        entry1 = ChannelEntry(1, 1, c1)
        entry2 = ChannelEntry(2, 2, c2)

        # Same in-flight (0) and same RW (0): first-drawn entry wins
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry1, entry2]), entry1)
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[1, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry1, entry2]), entry2)

    def test_p2c_single_candidate(self):
        c1 = MockSyncGrpcChannel("c1")
        entry1 = ChannelEntry(1, 1, c1)
        self.assertEqual(pick_channel_p2c([entry1]), entry1)
        self.assertIsNone(pick_channel_p2c([]))

    def test_p2c_random_tie_breaker(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        entry1 = ChannelEntry(1, 1, c1)
        entry2 = ChannelEntry(2, 2, c2)
        entry1.last_activity = 100.0
        entry2.last_activity = 100.0

        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry1, entry2]), entry1)
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[1, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry1, entry2]), entry2)

    def test_p2c_all_load_and_tie_branches(self):
        entry_1 = ChannelEntry(1, 1, MockSyncGrpcChannel("ch-1"))
        entry_2 = ChannelEntry(2, 2, MockSyncGrpcChannel("ch-2"))

        # 1. load1 < load2 -> returns entry_1
        entry_1._in_flight_rpcs = 1
        entry_2._in_flight_rpcs = 2
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry_1, entry_2]), entry_1)

        # 2. load2 < load1 -> returns entry_2
        entry_1._in_flight_rpcs = 2
        entry_2._in_flight_rpcs = 1
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry_1, entry_2]), entry_2)

        # 3. load1 == load2, active_rw_1 < active_rw_2 -> returns entry_1
        entry_1._in_flight_rpcs = 0
        entry_2._in_flight_rpcs = 0
        entry_1._active_rw_transactions = 0
        entry_2._active_rw_transactions = 1
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry_1, entry_2]), entry_1)

        # 4. load1 == load2, active_rw_2 < active_rw_1 -> returns entry_2
        entry_1._active_rw_transactions = 1
        entry_2._active_rw_transactions = 0
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.random.randrange",
            side_effect=[0, 0],
        ):
            self.assertEqual(pick_channel_p2c([entry_1, entry_2]), entry_2)


class TestSyncTransactionAffinity(unittest.TestCase):
    def test_read_write_affinity_increments_and_decrements_rw_count(self):
        entry = ChannelEntry(1, 1, MockSyncGrpcChannel("ch-1"))
        affinity = TransactionAffinity.new_read_write()

        self.assertIsNone(affinity.entry_id)
        self.assertEqual(affinity.kind, AffinityKind.READ_WRITE)

        affinity.ensure_rw_guard(entry)
        self.assertEqual(affinity.entry_id, 1)
        self.assertEqual(entry.active_rw_transactions, 1)

        # Idempotent guard call
        affinity.ensure_rw_guard(entry)
        self.assertEqual(entry.active_rw_transactions, 1)

        affinity.reset()
        self.assertIsNone(affinity.entry_id)
        self.assertEqual(entry.active_rw_transactions, 0)

    def test_read_only_affinity_does_not_increment_rw_count(self):
        entry = ChannelEntry(1, 1, MockSyncGrpcChannel("ch-1"))
        affinity = TransactionAffinity.new_read_only()

        self.assertEqual(affinity.kind, AffinityKind.READ_ONLY)
        affinity.set_entry_id(1)
        self.assertEqual(affinity.entry_id, 1)
        affinity.ensure_rw_guard(entry)
        self.assertEqual(entry.active_rw_transactions, 0)

        affinity.reset()
        self.assertIsNone(affinity.entry_id)

    def test_pin_if_unpinned(self):
        affinity = TransactionAffinity.new_read_write()
        entry1 = ChannelEntry(1, 1, MockSyncGrpcChannel("ch-1"))
        entry2 = ChannelEntry(2, 2, MockSyncGrpcChannel("ch-2"))
        pinned = affinity.pin_if_unpinned(entry1)
        self.assertIs(pinned, entry1)
        self.assertEqual(affinity.entry_id, 1)
        self.assertEqual(entry1.active_rw_transactions, 1)

        # Second attempt to pin a different entry returns original and does not modify pin
        second_pinned = affinity.pin_if_unpinned(entry2)
        self.assertIs(second_pinned, entry1)
        self.assertEqual(affinity.entry_id, 1)
        self.assertEqual(entry1.active_rw_transactions, 1)
        self.assertEqual(entry2.active_rw_transactions, 0)

    def test_transaction_del_resets_affinity(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry = pool._active_entries[0]

        affinity = TransactionAffinity.new_read_write()
        affinity.ensure_rw_guard(entry)
        self.assertEqual(entry.active_rw_transactions, 1)

        class MockTransactionHolder:
            def __init__(self, aff):
                self._affinity = aff

            def __del__(self):
                if getattr(self, "_affinity", None) is not None:
                    self._affinity.reset()

        transaction = MockTransactionHolder(affinity)
        del transaction
        gc.collect()

        self.assertEqual(entry.active_rw_transactions, 0)
        self.assertIsNone(affinity.pinned_entry_id)

    def test_snapshot_del_resets_affinity(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry = pool._active_entries[0]

        affinity = TransactionAffinity.new_read_only()
        affinity.set_entry_id(entry.id)
        self.assertEqual(affinity.pinned_entry_id, entry.id)

        class MockSnapshot:
            def __init__(self, aff):
                self._affinity = aff

            def close(self):
                if self._affinity is not None:
                    self._affinity.reset()

            def __del__(self):
                self.close()

        snap = MockSnapshot(affinity)
        del snap
        gc.collect()

        self.assertIsNone(affinity.pinned_entry_id)


class TestSyncChannelPoolLifecycle(unittest.TestCase):
    def test_static_channel_pool_from_channels(self):
        channels = [MockSyncGrpcChannel("c1"), MockSyncGrpcChannel("c2")]
        pool = ChannelPool.from_channels(channels)

        self.assertFalse(pool.is_dynamic)
        self.assertEqual(pool.active_channels_count, 2)
        self.assertEqual(pool.draining_channels_count, 0)

        caller = pool.unary_unary("/test.Service/TestMethod")
        result = caller("ping", metadata=[("header-key", "header-val")])
        self.assertEqual(result["request"], "ping")
        self.assertEqual(result["method"], "/test.Service/TestMethod")

        pool.close()
        self.assertTrue(channels[0].closed)
        self.assertTrue(channels[1].closed)

    def test_request_id_formatting(self):
        channels = [MockSyncGrpcChannel("c1")]
        pool = ChannelPool.from_channels(channels)

        original_request_id = "2.rand123.client456.999.req789.attempt1"
        metadata = [("x-goog-spanner-request-id", original_request_id)]

        mock_span = mock.MagicMock()
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.get_current_span",
            return_value=mock_span,
        ):
            caller = pool.unary_unary("/test.Service/TestMethod")
            result = caller("test_req", metadata=metadata)

        out_metadata = result["metadata"]
        req_id_headers = [
            v for k, v in out_metadata if k == "x-goog-spanner-request-id"
        ]
        self.assertEqual(len(req_id_headers), 1)
        self.assertEqual(req_id_headers[0], "2.rand123.client456.1.req789.attempt1")
        mock_span.set_attribute.assert_called_once_with(
            X_GOOG_SPANNER_REQUEST_ID_SPAN_ATTR,
            "2.rand123.client456.1.req789.attempt1",
        )

        pool.close()
        self.assertTrue(channels[0].closed)

    def test_dynamic_pool_start_and_ensure_background_tasks(self):
        created = []

        def factory():
            ch = MockSyncGrpcChannel(f"dyn-{len(created)}")
            created.append(ch)
            return ch

        options = ChannelPoolOptions(
            min_channels=1,
            max_channels=3,
            max_rpc_per_channel=2,
            min_rpc_per_channel=1,
        )
        pool = ChannelPool(channel_factory=factory, options=options)
        self.assertTrue(pool.is_dynamic)
        self.assertEqual(pool.active_channels_count, 1)
        self.assertEqual(pool.draining_channels_count, 0)

        # Simulate load exceeding max_rpc_per_channel to trigger _signal_scale_up in _make_lease
        entry = pool._active_entries[0]
        entry.increment_in_flight()
        entry.increment_in_flight()

        lease = pool.acquire()
        self.assertTrue(pool._scale_up_event.is_set())
        lease.release()

        # Channel close exception handled gracefully
        failing_channel = MockSyncGrpcChannel("failing")

        def failing_close():
            raise RuntimeError("close error")

        failing_channel.close = failing_close
        pool._active_entries = pool._active_entries + (
            ChannelEntry(2, 2, failing_channel),
        )

        pool.close()

    def test_streaming_rpc_lifetime_holds_lease(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])

        entry = pool._active_entries[0]
        self.assertEqual(entry.in_flight_rpcs, 0)

        stream_caller = pool.unary_stream("/test.Service/StreamMethod")
        stream = stream_caller("stream_req")

        # In-flight incremented while iterating
        self.assertEqual(entry.in_flight_rpcs, 1)
        items = list(stream)
        self.assertEqual(items, ["row_1", "row_2"])
        # In-flight decremented after stream completes
        self.assertEqual(entry.in_flight_rpcs, 0)

        pool.close()

    def test_transaction_affinity_pinning_read_write(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2])

        affinity = TransactionAffinity.new_read_write()
        caller = pool.unary_unary("/test.Service/Method")
        result1 = caller("q1", metadata=[("x-goog-spanner-affinity", affinity)])
        first_channel = result1["channel"]

        result2 = caller("q2", metadata=[("x-goog-spanner-affinity", affinity)])
        self.assertEqual(result2["channel"], first_channel)

        affinity.reset()
        pool.close()

    def test_scale_down_debouncing_and_draining_cleanup(self):
        channels = [
            MockSyncGrpcChannel("c1"),
            MockSyncGrpcChannel("c2"),
            MockSyncGrpcChannel("c3"),
            MockSyncGrpcChannel("c4"),
        ]
        options = ChannelPoolOptions(
            min_channels=2,
            max_channels=5,
            initial_channels=4,
            max_rpc_per_channel=25,
            scale_down_period_seconds=1.0,
            drain_idle_grace_seconds=0.0,
        )
        pool = ChannelPool.from_channels(channels, options=options)

        # 3 debounced cycles
        pool._execute_scale_down_check()
        self.assertEqual(pool.active_channels_count, 4)
        pool._execute_scale_down_check()
        self.assertEqual(pool.active_channels_count, 4)
        pool._execute_scale_down_check()
        self.assertEqual(pool.active_channels_count, 2)
        self.assertEqual(pool.draining_channels_count, 2)

        pool._sweep_draining_channels()
        self.assertEqual(pool.draining_channels_count, 0)
        self.assertTrue(channels[2].closed)
        self.assertTrue(channels[3].closed)

        pool.close()

    def test_scale_down_no_visibility_gap(self):
        channels = [
            MockSyncGrpcChannel("c1"),
            MockSyncGrpcChannel("c2"),
            MockSyncGrpcChannel("c3"),
            MockSyncGrpcChannel("c4"),
        ]
        options = ChannelPoolOptions(
            min_channels=2,
            max_channels=5,
            initial_channels=4,
            max_rpc_per_channel=25,
            scale_down_period_seconds=1.0,
            drain_idle_grace_seconds=10.0,
        )
        pool = ChannelPool.from_channels(channels, options=options)

        pool._consecutive_low_load_checks = 2
        pool._execute_scale_down_check()

        self.assertEqual(pool.active_channels_count, 2)
        self.assertEqual(pool.draining_channels_count, 2)

        for entry in pool._draining_entries:
            affinity = TransactionAffinity.new_read_write()
            affinity._attached_entry = entry
            affinity._pinned_entry_id = entry.id
            resolved = pool.resolve_affinity(affinity)
            self.assertIs(resolved.entry, entry)

        pool.close()

    def test_soft_affinity_re_pins_when_draining(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2])

        entry_1 = pool._active_entries[0]
        affinity = TransactionAffinity.new_read_only()
        affinity.set_entry_id(entry_1.entry_id)

        # Mark entry 1 as draining
        entry_1.set_state(ChannelState.DRAINING)
        pool._draining_entries = (entry_1,)
        pool._active_entries = tuple(e for e in pool._active_entries if e != entry_1)

        # Acquire with soft affinity should detect draining and re-pin to an active channel
        lease = pool.acquire(affinity)
        self.assertEqual(lease.channel, c2)
        self.assertEqual(affinity.entry_id, pool._active_entries[0].entry_id)
        lease.release()

        affinity.reset()
        pool.close()

    def test_hard_affinity_sticks_when_draining(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2])

        entry_1 = pool._active_entries[0]
        affinity = TransactionAffinity.new_read_write()
        affinity.ensure_rw_guard(entry_1)

        # Mark entry 1 as draining
        entry_1.set_state(ChannelState.DRAINING)
        pool._draining_entries = (entry_1,)
        pool._active_entries = tuple(e for e in pool._active_entries if e != entry_1)

        # Acquire with hard affinity sticks to the draining channel so the transaction can commit
        lease = pool.acquire(affinity)
        self.assertEqual(lease.channel, c1)
        self.assertEqual(affinity.entry_id, entry_1.entry_id)
        lease.release()

        affinity.reset()
        pool.close()

    def test_dict_metadata_request_id_and_affinity_stripping(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])

        affinity = TransactionAffinity.new_read_write()
        metadata = {
            "x-goog-spanner-request-id": "2.rand123.client456.0.req789.attempt1",
            "x-goog-spanner-affinity": affinity,
            "custom-header": "test-val",
        }

        mock_span = mock.MagicMock()
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.get_current_span",
            return_value=mock_span,
        ):
            caller = pool.unary_unary("/test.Service/TestMethod")
            result = caller("test_req", metadata=metadata)

        out_metadata = result["metadata"]
        self.assertIsInstance(out_metadata, dict)
        self.assertNotIn("x-goog-spanner-affinity", out_metadata)
        self.assertEqual(out_metadata["custom-header"], "test-val")
        self.assertEqual(
            out_metadata["x-goog-spanner-request-id"],
            "2.rand123.client456.1.req789.attempt1",
        )
        mock_span.set_attribute.assert_called_once_with(
            X_GOOG_SPANNER_REQUEST_ID_SPAN_ATTR,
            "2.rand123.client456.1.req789.attempt1",
        )
        pool.close()

    def test_stream_wrapper_stop_iteration_does_not_cancel(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])

        stream_caller = pool.unary_stream("/test.Service/StreamingMethod")
        stream = stream_caller("stream_query")

        entry = pool._active_entries[0]
        self.assertEqual(entry.in_flight_rpcs, 1)

        items = list(stream)

        self.assertEqual(items, ["row_1", "row_2"])
        self.assertEqual(entry.in_flight_rpcs, 0)
        self.assertFalse(stream._stream.closed)

        pool.close()

    def test_stream_wrapper_del_reclaims_lease(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry = pool._active_entries[0]

        stream_caller = pool.unary_stream("/test.Service/StreamingMethod")
        stream = stream_caller("stream_query")
        self.assertEqual(entry.in_flight_rpcs, 1)

        del stream
        gc.collect()

        self.assertEqual(entry.in_flight_rpcs, 0)
        pool.close()

    def test_stream_wrapper_last_chunk_finishes_lease(self):
        class MockChunk:
            def __init__(self, last=False):
                self.last = last

        chunk1 = MockChunk(last=False)
        chunk2 = MockChunk(last=True)

        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry = pool._active_entries[0]

        stream_caller = pool.unary_stream("/test.Service/StreamingMethod")
        stream = stream_caller("stream_query")
        stream._stream.items = [chunk1, chunk2]

        self.assertEqual(entry.in_flight_rpcs, 1)
        res1 = next(stream)
        self.assertIs(res1, chunk1)
        self.assertEqual(entry.in_flight_rpcs, 1)
        self.assertFalse(stream._closed)

        res2 = next(stream)
        self.assertIs(res2, chunk2)
        self.assertEqual(entry.in_flight_rpcs, 0)
        self.assertTrue(stream._closed)

        self.assertFalse(stream._stream.closed)
        del stream
        gc.collect()
        self.assertEqual(entry.in_flight_rpcs, 0)

        pool.close()

    def test_interceptor_sharing(self):
        c1 = MockSyncGrpcChannel("c1")
        c1._unary_unary_interceptors = []
        pool = ChannelPool.from_channels([c1])

        pool._unary_unary_interceptors.append("mock_interceptor")
        self.assertIn("mock_interceptor", c1._unary_unary_interceptors)
        pool.close()

    def test_stream_wrapper_read_and_cancel_and_getattr(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])

        stream_caller = pool.unary_stream("/test.Service/StreamingMethod")
        stream = stream_caller("stream_query")
        stream._stream.custom_property = "val"
        self.assertEqual(stream.custom_property, "val")

        # Test cancel() on active stream
        stream_to_cancel = stream_caller("stream_query_cancel")
        stream_to_cancel.cancel()
        self.assertTrue(stream_to_cancel._stream.closed)

        # Test exception during __next__()
        stream3 = stream_caller("stream_query3")
        stream3._stream.fail_on_next = True
        with self.assertRaises(RuntimeError):
            next(stream3)

        # Test exception in stream.cancel() is swallowed
        stream4 = stream_caller("stream_query4")
        stream4._stream.fail_on_cancel = True
        stream4.close()  # should not raise

        pool.close()

    def test_resolve_affinity_unpinned_pins_channel(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2])

        affinity = TransactionAffinity.new_read_write()
        self.assertIsNone(affinity.entry_id)

        lease = pool.resolve_affinity(affinity)
        self.assertIsNotNone(lease)
        self.assertIsNotNone(affinity.entry_id)
        self.assertEqual(affinity.entry_id, lease.entry.id)
        self.assertEqual(lease.entry.active_rw_transactions, 1)

        # Subsequent call uses the same pinned channel
        second_lease = pool.resolve_affinity(affinity)
        self.assertEqual(second_lease.entry.id, lease.entry.id)

        lease.release()
        second_lease.release()
        affinity.reset()
        pool.close()

    def test_acquire_empty_pool_raises_runtime_error(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        pool._active_entries = ()
        with self.assertRaises(ServiceUnavailable):
            pool.acquire()
        pool.close()

    def test_pool_unsupported_streaming_and_stubs(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])

        with self.assertRaises(NotImplementedError):
            pool.stream_unary("/test/Method")
        with self.assertRaises(NotImplementedError):
            pool.stream_stream("/test/Method")

        # Stubs for grpc.Channel interface
        pool.subscribe(lambda state: None)
        pool.unsubscribe(lambda state: None)
        pool.get_state()
        pool.wait_for_state_change(None)
        pool.channel_ready()

        # Context manager
        with pool as p:
            self.assertIs(p, pool)
        pool.close()

    def test_interceptor_sharing_all_four_types(self):
        c1 = MockSyncGrpcChannel("c1")
        c1._unary_unary_interceptors = []
        c1._unary_stream_interceptors = []
        c1._stream_unary_interceptors = []
        c1._stream_stream_interceptors = []
        pool = ChannelPool.from_channels([c1])
        pool._unary_unary_interceptors.append("i1")
        pool._unary_stream_interceptors.append("i2")
        pool._stream_unary_interceptors.append("i3")
        pool._stream_stream_interceptors.append("i4")
        self.assertIn("i1", c1._unary_unary_interceptors)
        self.assertIn("i2", c1._unary_stream_interceptors)
        self.assertIn("i3", c1._stream_unary_interceptors)
        self.assertIn("i4", c1._stream_stream_interceptors)
        pool.close()

    def test_multicallable_error_handling_releases_lease(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry = pool._active_entries[0]

        def failing_stream(*args, **kwargs):
            raise RuntimeError("stream creation fail")

        c1.unary_stream = failing_stream
        stream_caller = pool.unary_stream("/test.Method")
        with self.assertRaises(RuntimeError):
            stream_caller("req")
        self.assertEqual(entry.in_flight_rpcs, 0)

        def failing_call(*args, **kwargs):
            raise RuntimeError("call fail")

        c1.unary_unary = failing_call
        unary_caller = pool.unary_unary("/test.Method")
        with self.assertRaises(RuntimeError):
            unary_caller("req")
        self.assertEqual(entry.in_flight_rpcs, 0)
        pool.close()

    def test_metadata_and_affinity_edge_cases(self):
        pool = ChannelPool(auto_start_background_tasks=False)
        self.assertEqual(
            pool._resolve_caller_affinity({"x-goog-spanner-affinity": "aff1"}),
            "aff1",
        )
        self.assertEqual(
            pool._resolve_caller_affinity([("x-goog-spanner-affinity", "aff2")]),
            "aff2",
        )
        self.assertIsNone(pool._resolve_caller_affinity("not-dict-or-list"))

        self.assertEqual(
            pool._format_request_metadata("raw-scalar", 1), ("raw-scalar", None)
        )
        formatted, req_id = pool._format_request_metadata(
            {"x-goog-spanner-request-id": "1.2.3"}, 1
        )
        self.assertEqual(formatted, {"x-goog-spanner-request-id": "1.2.3"})
        self.assertEqual(req_id, "1.2.3")

        formatted, req_id = pool._format_request_metadata(
            [("x-goog-spanner-request-id", "1.2.3")], 1
        )
        self.assertEqual(formatted, [("x-goog-spanner-request-id", "1.2.3")])
        self.assertEqual(req_id, "1.2.3")

        self.assertEqual(
            pool._format_request_metadata(["not-a-tuple"], 1), (["not-a-tuple"], None)
        )
        mock_span = mock.Mock()
        mock_span.is_recording.return_value = False
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.get_current_span",
            return_value=mock_span,
        ):
            pool._format_request_metadata({"x-goog-spanner-request-id": "1.2.3.4"}, 2)
            mock_span.set_attribute.assert_not_called()

    def test_resolve_affinity_all_edge_branches(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry1 = pool._active_entries[0]

        # 1. resolve_affinity when active_entries is empty
        pool._active_entries = ()
        aff = TransactionAffinity.new_read_write()
        self.assertIsNone(pool.resolve_affinity(aff))

        # 2. resolve_affinity when pick_channel_p2c returns None
        pool._active_entries = (entry1,)
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.pick_channel_p2c",
            return_value=None,
        ):
            self.assertIsNone(pool.resolve_affinity(aff))

        # 3. acquire(aff) when resolve_affinity returns None falls back to pick_channel
        with mock.patch.object(pool, "resolve_affinity", return_value=None):
            lease = pool.acquire(aff)
            self.assertIsNotNone(lease)
            lease.release()

        pool.close()


class TestSyncChannelPoolScaling(unittest.TestCase):
    def test_scale_up_trigger_and_priming(self):
        created_channels = []

        def factory():
            ch = MockSyncGrpcChannel(f"dyn-sync-ch-{len(created_channels) + 1}")
            created_channels.append(ch)
            return ch

        options = ChannelPoolOptions(
            min_channels=1,
            max_channels=5,
            initial_channels=1,
            max_rpc_per_channel=2,
            min_rpc_per_channel=1,
            min_scale_up_step=2,
            scale_up_step_factor=0.5,
        )

        pool = ChannelPool(channel_factory=factory, options=options)
        self.assertEqual(pool.active_channels_count, 1)

        pool.set_prime_session("projects/p/instances/i/databases/d/sessions/s123")

        entry = pool._active_entries[0]
        entry.increment_in_flight()
        entry.increment_in_flight()
        entry.increment_in_flight()

        # Run scale-up directly in sync mode (verifies ThreadPoolExecutor execution!)
        pool._execute_scale_up()

        self.assertEqual(pool.active_channels_count, 3)
        pool.close()

    def test_priming_sends_gfe_headers_and_uses_prime_timeout(self):
        recorded_calls = []

        class PrimingCapturingSyncChannel(MockSyncGrpcChannel):
            def unary_unary(
                self, method, request_serializer=None, response_deserializer=None
            ):
                def invoker(request, timeout=None, metadata=None, **kwargs):
                    recorded_calls.append(
                        {
                            "method": method,
                            "request": request,
                            "timeout": timeout,
                            "metadata": metadata,
                        }
                    )
                    return mock.MagicMock()

                return invoker

        channel = PrimingCapturingSyncChannel("priming-sync-ch")
        options = ChannelPoolOptions(
            min_channels=1,
            max_channels=2,
            prime_timeout_seconds=7.5,
        )
        pool = ChannelPool(options=options)
        pool.set_prime_session(
            "projects/test-proj/instances/test-inst/databases/test-db/sessions/sess-123"
        )

        primed = pool._prime_channel(channel)
        self.assertTrue(primed)
        self.assertEqual(len(recorded_calls), 1)
        call = recorded_calls[0]
        self.assertEqual(call["timeout"], 7.5)
        expected_db = "projects/test-proj/instances/test-inst/databases/test-db"
        self.assertEqual(
            call["metadata"],
            [
                ("google-cloud-resource-prefix", expected_db),
                ("x-goog-request-params", f"database={expected_db}"),
            ],
        )
        pool.close()

    def test_draining_channel_idle_timeout_for_abandoned_transaction(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(
                min_channels=1, max_channels=2, drain_idle_grace_seconds=5.0
            ),
        )

        entry = pool._active_entries[0]
        entry.increment_rw_transaction()
        entry.set_state(ChannelState.DRAINING)
        pool._draining_entries = (entry,)
        pool._active_entries = ()

        # Simulate old activity older than timeout (10s + 5s = 15s)
        entry.last_activity = 100.0

        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.time.monotonic",
            return_value=120.0,
        ):
            pool._sweep_draining_channels()

        self.assertEqual(pool.draining_channels_count, 0)
        self.assertTrue(c1.closed)

        pool.close()

    def test_scale_up_cooldown_waits_for_cooldown(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(scale_up_cooldown_seconds=10.0),
            auto_start_background_tasks=False,
        )
        pool._last_scale_up_time = 100.0

        waited_timeouts = []

        def fake_wait(event, timeout=None):
            waited_timeouts.append(timeout)
            if event is pool._shutdown_event:
                pool._shutdown_event.set()

        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.time.monotonic",
            return_value=102.0,
        ):
            with mock.patch(
                "google.cloud.aio._cross_sync.CrossSync._Sync_Impl.event_wait",
                side_effect=fake_wait,
            ):
                pool._scale_up_event.set()
                pool._scale_up_worker_loop()

        self.assertIn(8.0, waited_timeouts)
        pool.close()

    def test_scale_up_edge_cases(self):
        c1 = MockSyncGrpcChannel("c1")
        options = ChannelPoolOptions(min_channels=1, max_channels=2)
        pool = ChannelPool.from_channels([c1], options=options)

        # 1. No prime session -> execute_scale_up returns early
        pool._execute_scale_up()

        # 2. Set prime session, but active entries >= max_channels -> returns early
        pool.set_prime_session("projects/p/instances/i/databases/d/sessions/s1")
        c2 = MockSyncGrpcChannel("c2")
        pool._active_entries = pool._active_entries + (ChannelEntry(2, 2, c2),)
        pool._execute_scale_up()

        # 3. desired <= current -> returns early
        pool._active_entries = pool._active_entries[:-1]
        pool._execute_scale_up()

        # 4. _dial_prime_and_publish_one handles channel_factory exception
        def failing_factory():
            raise RuntimeError("dial failure")

        pool._channel_factory = failing_factory
        pool._dial_prime_and_publish_one()

        # 5. _publish_primed_channel when at max channels closes channel
        pool._active_entries = pool._active_entries + (ChannelEntry(2, 2, c2),)
        c3 = MockSyncGrpcChannel("c3")
        published = pool._publish_primed_channel(c3)
        self.assertFalse(published)
        self.assertTrue(c3.closed)

        # 6. _publish_primed_channel accounts for draining channels in slot allocation
        pool._active_entries = (ChannelEntry(1, 1, c1),)
        entry_draining = ChannelEntry(2, 2, c2)
        entry_draining.set_state(ChannelState.DRAINING)
        pool._draining_entries = (entry_draining,)

        c4 = MockSyncGrpcChannel("c4")
        published = pool._publish_primed_channel(c4)
        self.assertTrue(published)
        new_entry = pool._active_entries[-1]
        self.assertEqual(new_entry.logical_channel_id, 3)

        pool.close()

    def test_scale_down_edge_cases(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        options = ChannelPoolOptions(
            min_channels=2, max_channels=5, min_rpc_per_channel=10
        )
        pool = ChannelPool.from_channels([c1, c2], options=options)

        # 1. len <= min_channels -> returns early
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 0)

        # 2. Add channels, but load >= min_rpc_per_channel -> returns early and resets counter
        c3 = MockSyncGrpcChannel("c3")
        entry3 = ChannelEntry(3, 3, c3)
        for _ in range(35):
            entry3.increment_in_flight()
        pool._active_entries = pool._active_entries + (entry3,)
        pool._consecutive_low_load_checks = 2
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 0)

        # 3. Consecutive checks < 3 -> increments and returns without draining
        for _ in range(35):
            entry3.decrement_in_flight()
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 1)

        pool.close()

    def test_lazy_init_affinity_bypass_prevention(self):
        from unittest.mock import MagicMock

        from google.cloud.spanner_v1.snapshot import Snapshot
        from google.cloud.spanner_v1.transaction import Transaction

        mock_db = MagicMock()
        mock_db.channel_pool = None
        mock_db._channel_pool_options = ChannelPoolOptions(
            min_channels=2, max_channels=4
        )

        mock_session = MagicMock()
        mock_session._database = mock_db

        # Snapshot with multi_use=True should have affinity even when channel_pool is None
        snapshot = Snapshot(mock_session, multi_use=True)
        self.assertIsNotNone(snapshot._affinity)
        self.assertTrue(snapshot._affinity.is_read_only())

        # Single-use snapshot should not have affinity
        single_snapshot = Snapshot(mock_session, multi_use=False)
        self.assertIsNone(single_snapshot._affinity)

        # Transaction should have read-write affinity
        transaction = Transaction(mock_session)
        self.assertIsNotNone(transaction._affinity)
        self.assertTrue(transaction._affinity.is_read_write())

    def test_aborted_retry_preserves_affinity(self):
        from unittest.mock import MagicMock

        from google.api_core.exceptions import Aborted

        from google.cloud.spanner_v1.session import Session
        from google.cloud.spanner_v1.transaction import Transaction

        mock_db = MagicMock()
        mock_db._channel_pool_options = ChannelPoolOptions(
            min_channels=2, max_channels=4
        )
        mock_db.channel_pool = None
        mock_db.log_commit_stats = False
        mock_db.observability_options = None
        mock_db._instance._client.project = "proj"
        mock_db._instance.instance_id = "inst"
        mock_db.database_id = "db"

        session = Session(mock_db)
        session._session_id = "sess-1"

        captured_affinities = []
        attempt_count = 0

        def work(transaction):
            nonlocal attempt_count
            attempt_count += 1
            captured_affinities.append(transaction._affinity)
            if attempt_count == 1:
                # First attempt aborts
                err = MagicMock()
                err.retry_delay.seconds = 0
                err.retry_delay.nanos = 0
                aborted_exc = Aborted("Transaction aborted", errors=[err])
                raise aborted_exc
            # Second attempt succeeds
            return "success"

        with mock.patch("google.cloud.spanner_v1.session._delay_until_retry"):
            with mock.patch.object(Transaction, "commit"):
                result = session.run_in_transaction(work)

        self.assertEqual(result, "success")
        self.assertEqual(len(captured_affinities), 2)
        # Both attempts must share the exact same TransactionAffinity instance
        self.assertIs(captured_affinities[0], captured_affinities[1])
        self.assertIsNotNone(captured_affinities[0])

    def test_multicallable_caching(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(1, 1, c1)

        call1 = entry.get_unary_unary("/test/Method")
        call2 = entry.get_unary_unary("/test/Method")
        self.assertIs(call1, call2)

        stream1 = entry.get_unary_stream("/test/StreamMethod")
        stream2 = entry.get_unary_stream("/test/StreamMethod")
        self.assertIs(stream1, stream2)

        entry.set_state(ChannelState.CLOSED)
        self.assertEqual(len(entry._unary_unary_cache), 0)
        self.assertEqual(len(entry._unary_stream_cache), 0)

    def test_draining_safe_closure_conditions(self):
        c1 = MockSyncGrpcChannel("c1")
        options = ChannelPoolOptions(min_channels=1, max_channels=2)
        pool = ChannelPool.from_channels([c1], options=options)

        entry = pool._active_entries[0]
        entry.set_state(ChannelState.DRAINING)
        pool._draining_entries = (entry,)

        # 1. in_flight == 0 and active_rw == 0 -> closes immediately
        pool._sweep_draining_channels()
        self.assertTrue(entry.is_closed())
        self.assertTrue(c1.closed)
        self.assertEqual(len(pool._draining_entries), 0)

        # 2. active_rw > 0 and elapsed < 15.0 -> remains draining
        c2 = MockSyncGrpcChannel("c2")
        entry2 = ChannelEntry(2, 2, c2)
        entry2.set_state(ChannelState.DRAINING)
        entry2.increment_rw_transaction()
        pool._draining_entries = (entry2,)

        pool._sweep_draining_channels()
        self.assertFalse(entry2.is_closed())
        self.assertEqual(len(pool._draining_entries), 1)

        # 3. active_rw > 0 but elapsed >= 15.0 -> reclaimed abandoned transaction
        entry2.last_activity = time.monotonic() - 16.0
        pool._sweep_draining_channels()
        self.assertTrue(entry2.is_closed())
        self.assertEqual(len(pool._draining_entries), 0)

        pool.close()

    def test_scale_down_custom_consecutive_checks(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        c3 = MockSyncGrpcChannel("c3")
        options = ChannelPoolOptions(
            min_channels=1,
            max_channels=3,
            initial_channels=3,
            min_rpc_per_channel=10,
            scale_down_consecutive_checks=2,
            drain_idle_grace_seconds=0.0,
        )
        pool = ChannelPool.from_channels([c1, c2, c3], options=options)
        self.assertEqual(pool.active_channels_count, 3)

        # Check 1: increments counter to 1
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 1)
        self.assertEqual(pool.active_channels_count, 3)

        # Check 2: reaches configured limit 2 -> scales down
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 0)
        self.assertEqual(pool.active_channels_count, 1)
        self.assertEqual(pool.draining_channels_count, 2)
        pool.close()

    def test_database_channel_pool_property_and_close(self):
        from google.cloud.spanner_v1.client import Client

        client = Client(project="test-project")
        instance = client.instance("test-instance")
        options = ChannelPoolOptions(min_channels=2, max_channels=4)
        database = instance.database("test-db", channel_pool_options=options)
        self.assertIs(database.channel_pool_options, options)

        # Close when uninitialized is a safe no-op
        database.close()

        # Connect a channel pool
        mock_pool = ChannelPool.from_channels([MockSyncGrpcChannel("c1")])
        database._channel_pool = mock_pool
        self.assertIs(database.channel_pool, mock_pool)
        database.close()
        self.assertTrue(mock_pool._shutdown_event.is_set())

    def test_channel_pool_duck_typing_stubs(self):
        pool = ChannelPool.from_channels([MockSyncGrpcChannel("c1")])
        callback = mock.Mock()
        pool.subscribe(callback)
        pool.unsubscribe(callback)

        state = pool.get_state()
        self.assertIsNotNone(state)
        pool.channel_ready()
        pool.wait_for_state_change(state)
        pool.close()

    def test_channel_pool_options_validation_edges(self):
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_channels=4, initial_channels=2).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(
                min_channels=2, max_channels=4, initial_channels=6
            ).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_rpc_per_channel=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(min_rpc_per_channel=10, max_rpc_per_channel=5).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(max_scale_up_percent=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(max_scale_up_percent=150).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(max_remove_channels=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_down_interval_secs=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_up_cooldown_seconds=-1).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(drain_idle_grace_seconds=-1).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(prime_timeout_seconds=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(prime_max_attempts=0).validate()
        with self.assertRaises(ValueError):
            ChannelPoolOptions(scale_down_consecutive_checks=0).validate()

        opts = ChannelPoolOptions(scale_up_cooldown=5.0, drain_idle_grace=20.0)
        self.assertEqual(opts.scale_up_cooldown_seconds, 5.0)
        self.assertEqual(opts.drain_idle_grace_seconds, 20.0)
        self.assertEqual(opts.target_rpc_per_channel(), 17)

        opts_no_max = ChannelPoolOptions(min_channels=2, max_channels=None)
        self.assertEqual(opts_no_max.desired_channel_count(100), 6)

    def test_channel_lease_context_managers_and_properties(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(id=1, logical_channel_id=2, channel=c1)
        on_release = mock.Mock()
        lease = ChannelLease(entry, on_release=on_release)

        self.assertEqual(lease.id, 1)
        self.assertEqual(lease.logical_channel_id, 2)
        self.assertIs(lease.channel, c1)

        entry.increment_in_flight()
        with lease:
            pass
        self.assertEqual(entry.in_flight_rpcs, 0)
        on_release.assert_called_once_with(lease)

        lease.release()
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_channel_entry_methods(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(id=1, logical_channel_id=1, channel=c1)
        entry.touch_activity()
        self.assertGreaterEqual(entry.elapsed_since_activity(), 0.0)

        entry.set_state(ChannelState.CLOSED)
        load = entry.try_increment_in_flight()
        self.assertEqual(load, 0)

        entry.set_state(ChannelState.ACTIVE)
        call1 = entry.get_unary_unary("method_a")
        call2 = entry.get_unary_unary("method_a")
        self.assertIs(call1, call2)

        stream1 = entry.get_unary_stream("method_stream")
        stream2 = entry.get_unary_stream("method_stream")
        self.assertIs(stream1, stream2)

    def test_prime_channel_failure_scenarios(self):
        pool = ChannelPool(auto_start_background_tasks=False)
        c1 = MockSyncGrpcChannel("c1")

        self.assertFalse(pool._prime_channel(c1))

        pool._prime_session = "projects/p/instances/i/databases/d/sessions/s1"

        def failing_unary(*args, **kwargs):
            raise RuntimeError("Prime network error")

        c1.unary_unary = failing_unary
        pool.options.prime_max_attempts = 2
        self.assertFalse(pool._prime_channel(c1))

        pool._shutdown_event.set()
        self.assertFalse(pool._prime_channel(c1))

    def test_publish_primed_channel_overflow_and_shutdown(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=1),
            initial_channels=[c1],
            auto_start_background_tasks=False,
        )
        c2 = MockSyncGrpcChannel("c2")
        self.assertFalse(pool._publish_primed_channel(c2))
        self.assertTrue(c2.closed)

        c3 = MockSyncGrpcChannel("c3")
        pool._shutdown_event.set()
        self.assertFalse(pool._publish_primed_channel(c3))
        self.assertTrue(c3.closed)

    def test_sweep_draining_channels_with_active_in_flight(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            initial_channels=[c1, c2],
            auto_start_background_tasks=False,
        )
        entry2 = pool._active_entries[1]
        entry2.increment_in_flight()
        entry2.set_state(ChannelState.DRAINING)
        pool._active_entries = (pool._active_entries[0],)
        pool._draining_entries = (entry2,)

        pool._sweep_draining_channels()
        self.assertEqual(len(pool._draining_entries), 1)

        entry2.decrement_in_flight()

        def bad_close():
            raise RuntimeError("close failure")

        c2.close = bad_close
        pool._sweep_draining_channels()
        self.assertEqual(len(pool._draining_entries), 0)

    def test_format_request_metadata_edge_cases(self):
        pool = ChannelPool(auto_start_background_tasks=False)
        self.assertEqual(pool._format_request_metadata(None, 1), (None, None))

        metadata = [
            ("x-goog-spanner-request-id", "req.uuid.1.9"),
            ("x-goog-spanner-affinity", "skip-this"),
            ("custom-header", "value"),
            ("x-short-req", "req.uuid"),
        ]
        formatted, req_id = pool._format_request_metadata(metadata, 3)
        self.assertEqual(req_id, "req.uuid.1.3")
        self.assertIn(("x-goog-spanner-request-id", "req.uuid.1.3"), formatted)
        self.assertNotIn(("x-goog-spanner-affinity", "skip-this"), formatted)
        self.assertIn(("custom-header", "value"), formatted)

        short_metadata = [("x-goog-spanner-request-id", "short.id")]
        formatted_short, short_req_id = pool._format_request_metadata(short_metadata, 3)
        self.assertEqual(short_req_id, "short.id")
        self.assertEqual(formatted_short[0][1], "short.id")

        mock_span = mock.Mock()
        mock_span.is_recording.return_value = True
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.get_current_span",
            return_value=mock_span,
        ):
            pool._format_request_metadata({"x-goog-spanner-request-id": "1.2.3.4"}, 5)
            mock_span.set_attribute.assert_called_once_with(
                X_GOOG_SPANNER_REQUEST_ID_SPAN_ATTR, "1.2.3.5"
            )

    def test_stream_wrapper_sync_edge_cases(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(id=1, logical_channel_id=1, channel=c1)
        lease = ChannelLease(entry)

        mock_stream = mock.MagicMock()
        mock_stream.__next__.return_value = "row1"
        mock_stream.extra_attr = "stream_prop"

        wrapper = _SyncStreamWrapper(mock_stream, lease)
        self.assertIs(iter(wrapper), wrapper)
        self.assertEqual(wrapper.extra_attr, "stream_prop")
        self.assertEqual(next(wrapper), "row1")

        lease2 = ChannelLease(entry)
        mock_stream2 = iter(["rowA"])
        wrapper2 = _SyncStreamWrapper(mock_stream2, lease2)
        self.assertEqual(next(wrapper2), "rowA")
        with self.assertRaises(StopIteration):
            next(wrapper2)
        self.assertTrue(lease2._released)

        lease3 = ChannelLease(entry)
        mock_stream3 = mock.Mock()
        mock_stream3.__next__ = mock.Mock(side_effect=RuntimeError("sync err"))
        wrapper3 = _SyncStreamWrapper(mock_stream3, lease3)
        with self.assertRaises(RuntimeError):
            next(wrapper3)
        self.assertTrue(lease3._released)

        lease4 = ChannelLease(entry)
        mock_stream4 = mock.Mock()
        mock_stream4.cancel = mock.Mock()
        wrapper4 = _SyncStreamWrapper(mock_stream4, lease4)
        wrapper4.cancel()
        mock_stream4.cancel.assert_called_once()
        self.assertTrue(lease4._released)

        lease5 = ChannelLease(entry)
        wrapper5 = _SyncStreamWrapper(mock_stream4, lease5)
        wrapper5.__del__()
        self.assertTrue(lease5._released)

    def test_destructor_and_empty_pool(self):
        pool = ChannelPool(auto_start_background_tasks=False)
        pool.__del__()
        self.assertTrue(pool._shutdown_event.is_set())

        with self.assertRaises(FailedPrecondition):
            pool.acquire()

    def test_default_options_validate(self):
        options = ChannelPoolOptions()
        options.validate()
        self.assertEqual(options.initial_channels, options.min_channels)
        options.initial_channels = None
        options.validate()

    def test_stream_wrapper_edge_branches(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(1, 1, c1)
        lease = ChannelLease(entry)
        mock_stream = mock.MagicMock()
        wrapper = _SyncStreamWrapper(mock_stream, lease)
        wrapper._finish()
        wrapper._finish()  # second finish is no-op

        mock_stream_no_cancel = mock.MagicMock(spec=[])
        wrapper_no_cancel = _SyncStreamWrapper(
            mock_stream_no_cancel, ChannelLease(entry)
        )
        wrapper_no_cancel.close()

        mock_stream_bad_cancel = mock.MagicMock()
        mock_stream_bad_cancel.cancel.side_effect = RuntimeError("cancel fail")
        wrapper_bad_cancel = _SyncStreamWrapper(
            mock_stream_bad_cancel, ChannelLease(entry)
        )
        wrapper_bad_cancel.close()

    def test_make_lease_and_pick_channel_none(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        closed_entry = pool._active_entries[0]
        closed_entry.set_state(ChannelState.CLOSED)
        self.assertIsNone(pool._make_lease(closed_entry))

        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.pick_channel_p2c",
            return_value=None,
        ):
            self.assertIsNone(pool.pick_channel())

        c2 = MockSyncGrpcChannel("c2")
        pool2 = ChannelPool.from_channels([c1, c2])
        entry_closed = pool2._active_entries[0]
        entry_closed.set_state(ChannelState.CLOSED)
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.pick_channel_p2c",
            return_value=entry_closed,
        ):
            fallback_lease = pool2.pick_channel()
            self.assertIsNotNone(fallback_lease)
            self.assertEqual(fallback_lease.entry.id, pool2._active_entries[1].id)
            fallback_lease.release()

        pool2._active_entries[1].set_state(ChannelState.CLOSED)
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.pick_channel_p2c",
            return_value=entry_closed,
        ):
            self.assertIsNone(pool2.pick_channel())
        pool2.close()
        pool.close()

    def test_resolve_affinity_read_only_pinned(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1])
        entry1 = pool._active_entries[0]
        ro_affinity = TransactionAffinity.new_read_only()
        ro_affinity.set_entry_id(entry1.id)
        lease = pool.resolve_affinity(ro_affinity)
        self.assertIsNotNone(lease)
        self.assertEqual(lease.id, entry1.id)
        self.assertEqual(entry1.active_rw_transactions, 0)
        lease.release()
        pool.close()

    def test_resolve_affinity_make_lease_none(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2])
        ro_affinity = TransactionAffinity.new_read_only()
        ro_affinity.set_entry_id(pool._active_entries[0].id)

        with mock.patch.object(pool, "_make_lease", return_value=None):
            self.assertIsNone(pool.resolve_affinity(ro_affinity))
        pool.close()

    def test_resolve_affinity_read_only_repins_when_channel_draining(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2])
        entry1 = pool._active_entries[0]
        entry2 = pool._active_entries[1]

        ro_affinity = TransactionAffinity.new_read_only()
        # 1. Initial pin
        lease1 = pool.resolve_affinity(ro_affinity)
        self.assertIsNotNone(lease1)
        draining_entry = lease1.entry
        other_entry = entry2 if draining_entry.id == entry1.id else entry1
        lease1.release()

        # 2. Initially pinned channel transitions to DRAINING
        draining_entry.set_state(ChannelState.DRAINING)
        pool._draining_entries = (draining_entry,)
        pool._active_entries = (other_entry,)

        # 3. Next read should seamlessly re-pin to other_entry (the active channel)
        lease2 = pool.resolve_affinity(ro_affinity)
        self.assertIsNotNone(lease2)
        self.assertEqual(lease2.entry.id, other_entry.id)
        self.assertEqual(ro_affinity.pinned_entry_id, other_entry.id)
        lease2.release()
        pool.close()

    def test_repin_if_stale_concurrent_winner(self):
        affinity = TransactionAffinity.new_read_only()
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        c3 = MockSyncGrpcChannel("c3")
        entry1 = ChannelEntry(1, 1, c1)
        entry2 = ChannelEntry(2, 2, c2)
        entry3 = ChannelEntry(3, 3, c3)

        # Initial pin
        pinned = affinity.repin_if_stale(None, entry1)
        self.assertEqual(pinned.id, 1)

        # Thread A re-pins from entry1 to entry2
        pinned_a = affinity.repin_if_stale(1, entry2)
        self.assertEqual(pinned_a.id, 2)

        # Thread B tries to re-pin from entry1 to entry3, but affinity was already updated to 2
        pinned_b = affinity.repin_if_stale(1, entry3)
        self.assertEqual(pinned_b.id, 2)  # Adopts winning entry2!

    def test_scale_up_cooldown_branches(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(
                min_channels=1, max_channels=2, scale_up_cooldown_seconds=0.01
            ),
            auto_start_background_tasks=False,
        )
        pool._last_scale_up_time = time.monotonic() - 100.0
        pool._scale_up_event.set()

        orig_execute = pool._execute_scale_up

        def stop():
            pool._shutdown_event.set()
            orig_execute()

        pool._execute_scale_up = stop
        pool._scale_up_worker_loop()
        pool.close()

    def test_dial_prime_and_publish_one_priming_failure(self):
        c = MockSyncGrpcChannel("c_fail")
        c.close = mock.Mock()
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            channel_factory=lambda: c,
            auto_start_background_tasks=False,
        )
        pool._prime_session = "projects/p/instances/i/databases/d/sessions/s1"
        with mock.patch.object(pool, "_prime_channel", return_value=False):
            pool._dial_prime_and_publish_one()
            c.close.assert_called_once()
        pool.close()

    def test_publish_primed_channel_occupied_slots_and_error(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=3),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        draining_closed = ChannelEntry(10, 5, MockSyncGrpcChannel("d1"))
        draining_closed.set_state(ChannelState.CLOSED)
        pool._draining_entries = (draining_closed,)

        c_new = MockSyncGrpcChannel("c_new")
        self.assertTrue(pool._publish_primed_channel(c_new))

        pool._shutdown_event.set()
        c_bad = MockSyncGrpcChannel("c_bad")
        c_bad.close = mock.Mock(side_effect=RuntimeError("close fail"))
        self.assertFalse(pool._publish_primed_channel(c_bad))
        pool.close()

    def test_evaluate_scale_down_zero_channels_to_remove(self):
        options = ChannelPoolOptions(
            min_channels=2,
            max_channels=5,
            min_rpc_per_channel=10,
            scale_down_consecutive_checks=1,
        )
        pool = ChannelPool.from_channels(
            [
                MockSyncGrpcChannel("c1"),
                MockSyncGrpcChannel("c2"),
                MockSyncGrpcChannel("c3"),
            ],
            options=options,
            auto_start_background_tasks=False,
        )
        pool._active_entries[0]._in_flight_rpcs = 8
        pool._active_entries[1]._in_flight_rpcs = 8
        pool._active_entries[2]._in_flight_rpcs = 9
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 0)
        pool.close()

    def test_scale_up_execution_early_exits(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            channel_factory=lambda: MockSyncGrpcChannel("c2"),
        )
        pool._prime_session = "projects/p/instances/i/databases/d/sessions/s1"
        c2 = MockSyncGrpcChannel("c2")
        pool._active_entries = pool._active_entries + (ChannelEntry(2, 2, c2),)
        pool._execute_scale_up()
        self.assertIsNotNone(pool._last_scale_up_time)

        pool._active_entries = (pool._active_entries[0],)
        pool._execute_scale_up()

        pool._channel_factory = None
        pool._dial_prime_and_publish_one()

        def error_factory():
            raise RuntimeError("Factory failed")

        pool._channel_factory = error_factory
        pool._dial_prime_and_publish_one()

        pool._active_entries = (
            ChannelEntry(1, 1, MockSyncGrpcChannel("c1")),
            ChannelEntry(2, 2, MockSyncGrpcChannel("c2")),
        )
        pool.options.min_channels = 2
        pool._evaluate_scale_down()
        self.assertEqual(pool._consecutive_low_load_checks, 0)
        pool.close()

    def test_scale_up_worker_and_monitor_single_step(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(
                min_channels=1, max_channels=2, scale_down_interval_secs=0.01
            ),
            auto_start_background_tasks=False,
        )
        pool._prime_session = "projects/p/instances/i/databases/d/sessions/s1"
        pool._scale_up_event.set()

        orig_execute = pool._execute_scale_up

        def stop_on_scale_up():
            pool._shutdown_event.set()
            orig_execute()

        pool._execute_scale_up = stop_on_scale_up
        pool._scale_up_worker_loop()

        pool._shutdown_event.clear()
        orig_check = pool._execute_scale_down_check

        def stop_on_check():
            pool._shutdown_event.set()
            orig_check()

        pool._execute_scale_down_check = stop_on_check

        with mock.patch(
            "google.cloud.aio._cross_sync.CrossSync._Sync_Impl.event_wait",
            return_value=None,
        ):
            pool._scale_down_monitor_loop()
        pool.close()

    def test_ensure_background_tasks_branches(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool(
            channel_factory=lambda: c1,
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            auto_start_background_tasks=False,
        )
        self.assertIsNone(pool._scale_up_task)
        self.assertIsNone(pool._scale_down_task)
        pool._ensure_background_tasks()
        self.assertIsNotNone(pool._scale_up_task)
        self.assertIsNotNone(pool._scale_down_task)

        task1 = pool._scale_up_task
        pool._ensure_background_tasks()
        self.assertIs(pool._scale_up_task, task1)

        pool._scale_up_task = mock.Mock(is_alive=mock.Mock(return_value=False))
        pool._scale_down_task = mock.Mock(is_alive=mock.Mock(return_value=False))
        pool._ensure_background_tasks()
        self.assertIsNot(pool._scale_up_task, task1)
        pool.close()

    def test_stream_wrapper_context_manager(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(1, 1, c1)
        entry.increment_in_flight()
        lease = ChannelLease(entry)
        mock_stream = mock.Mock()
        mock_stream.__enter__ = mock.Mock(return_value=mock_stream)
        mock_stream.__exit__ = mock.Mock(return_value=None)
        wrapper = _SyncStreamWrapper(mock_stream, lease)
        self.assertEqual(entry.in_flight_rpcs, 1)
        with wrapper as stream:
            self.assertIs(stream, wrapper)
        mock_stream.__enter__.assert_called_once()
        mock_stream.__exit__.assert_called_once()
        self.assertEqual(entry.in_flight_rpcs, 0)

        # Context manager with exception inside body
        entry.increment_in_flight()
        lease2 = ChannelLease(entry)
        wrapper2 = _SyncStreamWrapper(mock_stream, lease2)
        self.assertEqual(entry.in_flight_rpcs, 1)
        with self.assertRaises(ValueError):
            with wrapper2:
                raise ValueError("error in stream")
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_ensure_rw_guard_updates_pinned_entry_id(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        entry1 = ChannelEntry(1, 1, c1)
        entry2 = ChannelEntry(2, 2, c2)
        affinity = TransactionAffinity.new_read_write()
        affinity.ensure_rw_guard(entry1)
        self.assertEqual(affinity.pinned_entry_id, 1)
        self.assertEqual(entry1.active_rw_transactions, 1)
        # Switch guard to entry2
        affinity.ensure_rw_guard(entry2)
        self.assertEqual(affinity.pinned_entry_id, 2)
        self.assertEqual(entry1.active_rw_transactions, 0)
        self.assertEqual(entry2.active_rw_transactions, 1)

    def test_dial_prime_and_publish_close_exception(self):
        c_bad = MockSyncGrpcChannel("c_bad")
        c_bad.close = mock.Mock(side_effect=RuntimeError("close failed"))
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            channel_factory=lambda: c_bad,
            auto_start_background_tasks=False,
        )
        with mock.patch.object(pool, "_prime_channel", return_value=False):
            pool._dial_prime_and_publish_one()
        pool.close()

    def test_publish_primed_channel_at_max_channels(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(min_channels=1, max_channels=1),
            auto_start_background_tasks=False,
        )
        c2 = MockSyncGrpcChannel("c2")
        result = pool._publish_primed_channel(c2)
        self.assertFalse(result)
        self.assertTrue(c2.closed)
        self.assertEqual(c2.close_call_count, 1)
        pool.close()

    def test_is_channel_pool_enabled_helper(self):
        self.assertFalse(is_channel_pool_enabled(None))

        mock_db = mock.Mock()
        mock_db.channel_pool_enabled = True
        self.assertTrue(is_channel_pool_enabled(mock_db))

        mock_db.channel_pool_enabled = False
        self.assertFalse(is_channel_pool_enabled(mock_db))

        mock_db_opts = mock.Mock(spec=[])
        mock_db_opts._channel_pool_options = ChannelPoolOptions()
        self.assertTrue(is_channel_pool_enabled(mock_db_opts))

        mock_db_pool = mock.Mock(spec=[])
        c = MockSyncGrpcChannel("c")
        mock_db_pool.channel_pool = ChannelPool.from_channels([c])
        self.assertTrue(is_channel_pool_enabled(mock_db_pool))

        plain_mock = mock.Mock()
        self.assertFalse(is_channel_pool_enabled(plain_mock))

    def test_transaction_affinity_del(self):
        affinity = TransactionAffinity.new_read_write()
        c = MockSyncGrpcChannel("c")
        entry = ChannelEntry(1, 1, c)
        affinity.ensure_rw_guard(entry)
        self.assertEqual(entry.active_rw_transactions, 1)
        affinity.__del__()
        self.assertEqual(entry.active_rw_transactions, 0)

    def test_scale_up_worker_shutdown_on_wake(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        pool_ref = mock.MagicMock()
        pool_ref.side_effect = [pool, None]
        pool._scale_up_event.set()
        pool._run_scale_up_worker(pool_ref)

    def test_scale_up_worker_shutdown_during_cooldown(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(
                min_channels=1, max_channels=2, scale_up_cooldown_seconds=0.01
            ),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        pool._last_scale_up_time = time.monotonic()
        pool._scale_up_event.set()
        pool_ref = mock.MagicMock()
        shutdown_pool = mock.MagicMock()
        shutdown_pool._shutdown_event.is_set.return_value = True
        pool_ref.side_effect = [pool, pool, shutdown_pool]
        pool._run_scale_up_worker(pool_ref)

    def test_pick_channel_retries_on_inactive_candidate(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels(
            [c1, c2],
            auto_start_background_tasks=False,
        )
        pool._active_entries[0].set_state(ChannelState.DRAINING)
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool.pick_channel_p2c",
            side_effect=[pool._active_entries[0], pool._active_entries[1]],
        ):
            lease = pool.pick_channel()
            self.assertIsNotNone(lease)
            self.assertEqual(lease.entry.id, 2)
            lease.release()

    def test_channel_entry_is_draining(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(1, 1, c1)
        self.assertFalse(entry.is_draining())
        entry.set_state(ChannelState.DRAINING)
        self.assertTrue(entry.is_draining())

    def test_resolve_caller_affinity_dict_metadata(self):
        pool = ChannelPool.from_channels(
            [MockSyncGrpcChannel("c1")], auto_start_background_tasks=False
        )
        affinity = TransactionAffinity.new_read_write()
        resolved = pool._resolve_caller_affinity({"x-goog-spanner-affinity": affinity})
        self.assertIs(resolved, affinity)

    def test_publish_primed_channel_at_max_channels_closes_channel(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=1),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        extra_channel = MockSyncGrpcChannel("extra")
        success = pool._publish_primed_channel(extra_channel)
        self.assertFalse(success)
        self.assertTrue(extra_channel.closed)

    def test_stream_wrapper_cancel_returns_bool(self):
        mock_call = mock.MagicMock()
        mock_call.cancel.return_value = True
        entry = ChannelEntry(1, 1, MockSyncGrpcChannel("c1"))
        lease = ChannelLease(entry)
        wrapper = _SyncStreamWrapper(mock_call, lease)
        result = wrapper.cancel()
        self.assertIs(result, True)

    def test_pick_channel_fallback_none_when_all_draining(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            auto_start_background_tasks=False,
        )
        pool._active_entries[0].set_state(ChannelState.DRAINING)
        lease = pool.pick_channel()
        self.assertIsNone(lease)

    def test_channel_lease_entry_id(self):
        entry = ChannelEntry(1, 1, MockSyncGrpcChannel("c1"))
        lease = ChannelLease(entry)
        self.assertEqual(lease.entry_id, 1)

    def test_pin_entry_repin(self):
        affinity = TransactionAffinity.new_read_write()
        entry1 = ChannelEntry(1, 1, MockSyncGrpcChannel("c1"))
        entry2 = ChannelEntry(2, 2, MockSyncGrpcChannel("c2"))
        affinity.pin_entry(entry1)
        self.assertEqual(entry1.active_rw_transactions, 1)
        # Re-pin to entry2
        affinity.pin_entry(entry2)
        self.assertEqual(entry1.active_rw_transactions, 0)
        self.assertEqual(entry2.active_rw_transactions, 1)

    def test_stream_wrapper_enter_exit_delegation(self):
        class MockSyncStreamWithContext:
            def __init__(self):
                self.entered = False
                self.exited = False

            def __enter__(self):
                self.entered = True
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.exited = True

        mock_stream = MockSyncStreamWithContext()
        entry = ChannelEntry(1, 1, MockSyncGrpcChannel("c1"))
        lease = ChannelLease(entry)
        wrapper = _SyncStreamWrapper(mock_stream, lease)
        with wrapper as entered:
            self.assertIs(entered, wrapper)
            self.assertTrue(mock_stream.entered)
        self.assertTrue(mock_stream.exited)

    def test_resolve_affinity_draining_make_lease_none_falls_through(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        draining_entry = ChannelEntry(2, 2, c2)
        draining_entry.set_state(ChannelState.DRAINING)
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        pool._draining_entries = (draining_entry,)
        affinity = TransactionAffinity.new_read_write()
        affinity.set_entry_id(2)

        original_make_lease = pool._make_lease

        def failing_make_lease(entry, require_active=True):
            if entry.id == 2:
                return None
            return original_make_lease(entry, require_active=require_active)

        with mock.patch.object(pool, "_make_lease", side_effect=failing_make_lease):
            lease = pool.resolve_affinity(affinity)
            self.assertIsNotNone(lease)
            self.assertEqual(lease.entry.id, 1)

    def test_channel_entry_try_close_draining(self):
        c1 = MockSyncGrpcChannel("c1")
        entry = ChannelEntry(1, 1, c1)
        entry.set_state(ChannelState.DRAINING)

        # 1. In-flight busy -> False
        entry.increment_in_flight()
        self.assertFalse(entry.try_close_draining(15.0))
        entry.decrement_in_flight()

        # 2. Active RW transactions present and not expired -> False
        entry.increment_active_rw()
        entry.touch_activity()
        self.assertFalse(entry.try_close_draining(15.0))

        # 3. Active RW present but elapsed >= idle_grace -> True
        entry.last_activity = time.monotonic() - 20.0
        self.assertTrue(entry.try_close_draining(15.0))
        self.assertTrue(entry.is_closed())

        # 4. Clean close: active_rw == 0 -> True
        entry2 = ChannelEntry(2, 2, MockSyncGrpcChannel("c2"))
        entry2.set_state(ChannelState.DRAINING)
        self.assertTrue(entry2.try_close_draining(15.0))
        self.assertTrue(entry2.is_closed())

    def test_dynamic_channel_pool_max_channels_none(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=None),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        self.assertTrue(pool.is_dynamic)

    def test_pin_entry_same_entry(self):
        affinity = TransactionAffinity.new_read_write()
        entry1 = ChannelEntry(1, 1, MockSyncGrpcChannel("c1"))
        affinity.pin_entry(entry1)
        # Re-pin to same entry (exercises _attached_entry.id == entry.id)
        affinity.pin_entry(entry1)
        self.assertEqual(entry1.active_rw_transactions, 1)

    def test_concurrent_resolve_affinity_pins_same_channel(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels([c1, c2], auto_start_background_tasks=False)
        affinity = TransactionAffinity.new_read_write()

        lease1 = pool.resolve_affinity(affinity)
        lease2 = pool.resolve_affinity(affinity)

        self.assertIsNotNone(lease1)
        self.assertIsNotNone(lease2)
        self.assertEqual(lease1.entry.id, lease2.entry.id)
        self.assertEqual(affinity.entry_id, lease1.entry.id)
        self.assertEqual(lease1.entry.active_rw_transactions, 1)
        lease1.release()
        lease2.release()

    def test_resolve_affinity_read_write_draining_not_found(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        affinity = TransactionAffinity.new_read_write()
        affinity.set_entry_id(999)  # ID not in active and not in draining
        lease = pool.resolve_affinity(affinity)
        self.assertIsNotNone(lease)
        self.assertEqual(lease.entry.id, 1)

    def test_publish_primed_channel_shutdown_while_priming(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(min_channels=1, max_channels=2),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        pool._shutdown_event.set()
        extra_channel = MockSyncGrpcChannel("extra")
        success = pool._publish_primed_channel(extra_channel)
        self.assertFalse(success)
        self.assertTrue(extra_channel.closed)


class TestChannelPoolGrpcInterfaceAndGapicIntegration(unittest.TestCase):
    """Tests verifying channel pool compliance with gRPC MultiCallable interfaces and GAPIC clients."""

    def test_unary_unary_is_multicallable_instance(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        callable_obj = pool.unary_unary("/google.spanner.v1.Spanner/Commit")
        self.assertIsInstance(callable_obj, grpc.UnaryUnaryMultiCallable)
        self.assertIsInstance(callable_obj, _SyncUnaryUnaryMultiCallable)

    def test_unary_stream_is_multicallable_instance(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        callable_obj = pool.unary_stream(
            "/google.spanner.v1.Spanner/ExecuteStreamingSql"
        )
        self.assertIsInstance(callable_obj, grpc.UnaryStreamMultiCallable)
        self.assertIsInstance(callable_obj, _SyncUnaryStreamMultiCallable)

    def test_unary_unary_with_call_support_and_lease_release(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        callable_obj = pool.unary_unary("/google.spanner.v1.Spanner/Commit")
        entry = pool._active_entries[0]
        self.assertEqual(entry.in_flight_rpcs, 0)

        response, call = callable_obj.with_call({"request": "data"})
        self.assertEqual(response["request"], {"request": "data"})
        self.assertIsInstance(call, grpc.Call)
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_unary_unary_future_not_supported_raises_and_releases_lease(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        callable_obj = pool.unary_unary("/google.spanner.v1.Spanner/Commit")
        entry = pool._active_entries[0]
        self.assertEqual(entry.in_flight_rpcs, 0)

        with self.assertRaises(NotImplementedError):
            callable_obj.future({"request": "data"})
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_unary_unary_future_support_and_lease_release(self):
        from concurrent.futures import Future

        class ChannelWithFuture:
            def unary_unary(
                self, method, request_serializer=None, response_deserializer=None
            ):
                class MultiCallable(grpc.UnaryUnaryMultiCallable):
                    def __call__(self, *args, **kwargs):
                        return "called"

                    def with_call(self, *args, **kwargs):
                        return "called", grpc.Call()

                    def future(self, request, *args, **kwargs):
                        fut = Future()
                        fut.set_result({"request": request})
                        return fut

                return MultiCallable()

            def close(self):
                pass

        pool = ChannelPool.from_channels(
            [ChannelWithFuture()], auto_start_background_tasks=False
        )
        callable_obj = pool.unary_unary("/test")
        entry = pool._active_entries[0]
        self.assertEqual(entry.in_flight_rpcs, 0)

        fut = callable_obj.future({"request": "data"})
        self.assertEqual(fut.result(), {"request": {"request": "data"}})
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_unary_unary_with_call_underlying_has_with_call(self):
        class ChannelWithWithCall:
            def unary_unary(
                self, method, request_serializer=None, response_deserializer=None
            ):
                class MultiCallable(grpc.UnaryUnaryMultiCallable):
                    def __call__(self, request, *args, **kwargs):
                        return "called"

                    def with_call(self, request, *args, **kwargs):
                        class CustomCall(grpc.Call):
                            def initial_metadata(self):
                                return (("key", "val"),)

                            def trailing_metadata(self):
                                return ()

                            def code(self):
                                return grpc.StatusCode.OK

                            def details(self):
                                return ""

                            def is_active(self):
                                return False

                            def time_remaining(self):
                                return None

                            def cancel(self):
                                return False

                            def add_callback(self, cb):
                                return False

                        return "with_called", CustomCall()

                    def future(self, request, *args, **kwargs):
                        raise NotImplementedError()

                return MultiCallable()

            def close(self):
                pass

        pool = ChannelPool.from_channels(
            [ChannelWithWithCall()], auto_start_background_tasks=False
        )
        callable_obj = pool.unary_unary("/test")
        resp, call = callable_obj.with_call("test-req")
        self.assertEqual(resp, "with_called")
        self.assertEqual(call.initial_metadata(), (("key", "val"),))

    def test_unary_unary_with_call_error_releases_lease_and_attaches_request_id(
        self,
    ):
        class FailingChannel:
            def unary_unary(
                self, method, request_serializer=None, response_deserializer=None
            ):
                def invoker(*args, **kwargs):
                    raise RuntimeError("RPC error")

                return invoker

            def close(self):
                pass

        pool = ChannelPool.from_channels(
            [FailingChannel()], auto_start_background_tasks=False
        )
        callable_obj = pool.unary_unary("/test")
        entry = pool._active_entries[0]
        with self.assertRaises(RuntimeError) as ctx:
            callable_obj.with_call(
                "req", metadata=(("x-goog-spanner-request-id", "req-123"),)
            )
        self.assertEqual(entry.in_flight_rpcs, 0)
        self.assertEqual(getattr(ctx.exception, "_spanner_request_id", None), "req-123")

    def test_unary_stream_call_is_grpc_call_and_iterates(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        stream_callable = pool.unary_stream(
            "/google.spanner.v1.Spanner/ExecuteStreamingSql"
        )
        entry = pool._active_entries[0]
        stream = stream_callable({"query": "SELECT 1"})
        self.assertIsInstance(stream, grpc.Call)
        self.assertIsInstance(stream, _SyncStreamWrapper)
        self.assertEqual(entry.in_flight_rpcs, 1)

        results = list(stream)
        self.assertEqual(results, ["row_1", "row_2"])
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_unary_stream_early_cancel_releases_lease(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        stream_callable = pool.unary_stream(
            "/google.spanner.v1.Spanner/ExecuteStreamingSql"
        )
        entry = pool._active_entries[0]
        stream = stream_callable({"query": "SELECT 1"})
        self.assertEqual(entry.in_flight_rpcs, 1)
        stream.cancel()
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_unary_stream_context_manager_releases_lease(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        stream_callable = pool.unary_stream(
            "/google.spanner.v1.Spanner/ExecuteStreamingSql"
        )
        entry = pool._active_entries[0]
        with stream_callable({"query": "SELECT 1"}) as stream:
            self.assertEqual(entry.in_flight_rpcs, 1)
            first_item = next(stream)
            self.assertEqual(first_item, "row_1")
        self.assertEqual(entry.in_flight_rpcs, 0)

    def test_spanner_grpc_transport_and_client_end_to_end(self):
        from google.cloud.spanner_v1.services.spanner import SpannerClient
        from google.cloud.spanner_v1.services.spanner.transports.grpc import (
            SpannerGrpcTransport,
        )
        from google.cloud.spanner_v1.types import (
            BatchCreateSessionsResponse,
            CommitResponse,
            PartialResultSet,
        )

        class MockGapicChannel:
            def unary_unary(
                self, method, request_serializer=None, response_deserializer=None
            ):
                def invoker(
                    request,
                    timeout=None,
                    metadata=None,
                    credentials=None,
                    wait_for_ready=None,
                    compression=None,
                    **kwargs,
                ):
                    if "Commit" in method:
                        return CommitResponse()
                    if "BatchCreateSessions" in method:
                        return BatchCreateSessionsResponse()
                    return mock.MagicMock()

                def with_call(request, *args, **kwargs):
                    class MockCall(grpc.Call):
                        def initial_metadata(self):
                            return ()

                        def trailing_metadata(self):
                            return ()

                        def code(self):
                            return grpc.StatusCode.OK

                        def details(self):
                            return ""

                        def is_active(self):
                            return False

                        def time_remaining(self):
                            return None

                        def cancel(self):
                            return False

                        def add_callback(self, cb):
                            return False

                    return invoker(request, *args, **kwargs), MockCall()

                invoker.with_call = with_call
                return invoker

            def unary_stream(
                self, method, request_serializer=None, response_deserializer=None
            ):
                def invoker(request, *args, **kwargs):
                    class MockStream(grpc.Call):
                        def __init__(self):
                            self.items = [PartialResultSet()]

                        def __iter__(self):
                            return self

                        def __next__(self):
                            if not self.items:
                                raise StopIteration
                            return self.items.pop(0)

                        def cancel(self):
                            return True

                        def initial_metadata(self):
                            return ()

                        def trailing_metadata(self):
                            return ()

                        def code(self):
                            return grpc.StatusCode.OK

                        def details(self):
                            return ""

                        def is_active(self):
                            return False

                        def time_remaining(self):
                            return None

                        def add_callback(self, cb):
                            return False

                    return MockStream()

                return invoker

            def close(self):
                pass

        mock_channel = MockGapicChannel()
        pool = ChannelPool.from_channels(
            [mock_channel], auto_start_background_tasks=False
        )
        transport = SpannerGrpcTransport(channel=pool)
        client = SpannerClient(transport=transport)

        # 1. Unary call through GAPIC client (exercises interceptor -> .with_call)
        commit_resp = client.commit(
            request={"session": "projects/p/instances/i/databases/d/sessions/s"}
        )
        self.assertIsInstance(commit_resp, CommitResponse)
        self.assertEqual(pool._active_entries[0].in_flight_rpcs, 0)

        # 2. Another unary call (batch_create_sessions)
        batch_resp = client.batch_create_sessions(
            request={
                "database": "projects/p/instances/i/databases/d",
                "session_count": 5,
            }
        )
        self.assertIsInstance(batch_resp, BatchCreateSessionsResponse)
        self.assertEqual(pool._active_entries[0].in_flight_rpcs, 0)

        # 3. Streaming call through GAPIC client
        stream = client.execute_streaming_sql(
            request={
                "session": "projects/p/instances/i/databases/d/sessions/s",
                "sql": "SELECT 1",
            }
        )
        results = list(stream)
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], PartialResultSet)
        self.assertEqual(pool._active_entries[0].in_flight_rpcs, 0)

    def test_scale_up_worker_respects_min_scale_up_step(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(
                min_channels=1,
                max_channels=10,
                min_scale_up_step=3,
                max_scale_up_percent=10,
            ),
            initial_channels=[MockSyncGrpcChannel("c1")],
            auto_start_background_tasks=False,
        )
        pool._channel_factory = mock.Mock(
            side_effect=[
                MockSyncGrpcChannel("c2"),
                MockSyncGrpcChannel("c3"),
                MockSyncGrpcChannel("c4"),
            ]
        )
        pool._channel_primer = mock.Mock()
        pool._active_entries[0]._in_flight_rpcs = 100
        pool._scale_up_event.set()
        pool_ref = mock.MagicMock()
        shutdown_pool = mock.MagicMock()
        shutdown_pool._shutdown_event.is_set.return_value = True
        pool_ref.side_effect = [pool, pool, shutdown_pool]
        pool._run_scale_up_worker(pool_ref)
        self.assertEqual(len(pool._active_entries), 4)

    def test_stream_wrapper_releases_on_last_chunk(self):
        class MockChunk:
            def __init__(self, last=False):
                self.last = last

        chunk1 = MockChunk(last=False)
        chunk2 = MockChunk(last=True)

        stream_calls = []

        class MockSyncDrainStream:
            def __init__(self, items):
                self.items = list(items)

            def __iter__(self):
                return self

            def __next__(self):
                stream_calls.append("__next__")
                if not self.items:
                    raise StopIteration
                return self.items.pop(0)

        mock_stream = MockSyncDrainStream([chunk1, chunk2])
        mock_channel = mock.Mock()
        mock_channel.unary_stream.return_value = mock.Mock(return_value=mock_stream)

        pool = ChannelPool.from_channels(
            [mock_channel], auto_start_background_tasks=False
        )
        stream_caller = pool.unary_stream("/test")
        entry = pool._active_entries[0]

        stream = stream_caller("req")
        self.assertEqual(entry.in_flight_rpcs, 1)

        res1 = next(stream)
        self.assertIs(res1, chunk1)
        self.assertEqual(stream_calls, ["__next__"])

        res2 = next(stream)
        self.assertIs(res2, chunk2)
        self.assertEqual(stream_calls, ["__next__", "__next__"])
        self.assertEqual(entry.in_flight_rpcs, 0)
        self.assertTrue(stream._closed)

    def test_rlock_reentrant_lease_release(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels([c1], auto_start_background_tasks=False)
        lease = pool.acquire()
        entry = lease.entry
        # Simulate finalizer running while entry._lock is already held on this thread
        with entry._lock:
            lease.release()
        self.assertEqual(entry.in_flight_rpcs, 0)
        self.assertTrue(lease._released)

    def test_channel_pool_options_unknown_kwargs_raises_type_error(self):
        with self.assertRaises(TypeError) as ctx:
            ChannelPoolOptions(invalid_option_key="foo")
        self.assertIn("unexpected keyword argument", str(ctx.exception))

    def test_scale_up_promotes_draining_channels_before_dialing(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        pool = ChannelPool.from_channels(
            [c1, c2],
            options=ChannelPoolOptions(
                min_channels=1,
                max_channels=4,
                min_rpc_per_channel=2,
                max_rpc_per_channel=5,
            ),
            auto_start_background_tasks=False,
        )
        # Move c2 to draining
        draining_entry = pool._active_entries[1]
        draining_entry.set_state(ChannelState.DRAINING)
        pool._active_entries = (pool._active_entries[0],)
        pool._draining_entries = (draining_entry,)

        # Induce high load on active channel c1
        for _ in range(6):
            pool._active_entries[0].increment_in_flight()

        # Run scale-up. Since draining channels exist, c2 should be promoted back to active
        pool._execute_scale_up()
        self.assertIn(draining_entry, pool._active_entries)
        self.assertEqual(draining_entry.state, ChannelState.ACTIVE)
        self.assertEqual(len(pool._draining_entries), 0)
        pool.close()

    def test_scale_up_triggered_by_max_entry_load_hotspot(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        c3 = MockSyncGrpcChannel("c3")
        c4 = MockSyncGrpcChannel("c4")
        mock_factory = mock.Mock(side_effect=lambda: MockSyncGrpcChannel("c_new"))
        pool = ChannelPool.from_channels(
            [c1, c2, c3, c4],
            options=ChannelPoolOptions(
                min_channels=4,
                max_channels=8,
                max_rpc_per_channel=25,
            ),
            channel_factory=mock_factory,
            auto_start_background_tasks=False,
        )
        # Total load is 26 across 4 channels -> average is 6.5 < 25 (aggregate would not scale up)
        # But c1 alone has 26 load -> max_entry_load > 25
        for _ in range(26):
            c1_entry = pool._active_entries[0]
            c1_entry.increment_in_flight()

        pool._execute_scale_up()
        # Pool should have scaled up by min_scale_up_step (2 channels)
        self.assertEqual(len(pool._active_entries), 6)
        pool.close()

    def test_format_request_metadata_tuple_and_fast_path_edge_cases(self):
        pool = ChannelPool(auto_start_background_tasks=False)

        # 1. Tuple metadata with affinity and request-id: should strip affinity and rewrite channel slot to 3
        metadata_tuple = (
            ("x-goog-spanner-affinity", "test-affinity"),
            ("x-goog-spanner-request-id", "1.uuid.1.9"),
            ("custom-header", "custom-value"),
        )
        formatted, found_request_id = pool._format_request_metadata(metadata_tuple, 3)
        self.assertIsInstance(formatted, tuple)
        self.assertEqual(found_request_id, "1.uuid.1.3")
        self.assertEqual(
            formatted,
            (
                ("x-goog-spanner-request-id", "1.uuid.1.3"),
                ("custom-header", "custom-value"),
            ),
        )

        # 2. Tuple metadata that is already matching and has no affinity: should return same tuple object
        clean_tuple = (
            ("x-goog-spanner-request-id", "1.uuid.1.3"),
            ("custom-header", "custom-value"),
        )
        formatted_clean, found_clean_id = pool._format_request_metadata(clean_tuple, 3)
        self.assertIs(formatted_clean, clean_tuple)
        self.assertEqual(found_clean_id, "1.uuid.1.3")

        # 3. Dict metadata with non-string request-id: returns (metadata, None)
        dict_with_non_string = {
            "x-goog-spanner-request-id": 12345,
            "custom-header": "custom-value",
        }
        formatted_dict, found_dict_id = pool._format_request_metadata(
            dict_with_non_string, 3
        )
        self.assertIs(formatted_dict, dict_with_non_string)
        self.assertIsNone(found_dict_id)

        # 4. Dict metadata without request-id: returns (metadata, None)
        dict_without_req_id = {"custom-header": "custom-value"}
        formatted_no_req, found_no_req = pool._format_request_metadata(
            dict_without_req_id, 3
        )
        self.assertIs(formatted_no_req, dict_without_req_id)
        self.assertIsNone(found_no_req)

    def test_scale_up_partial_promotion_of_draining_entries(self):
        c1 = MockSyncGrpcChannel("c1")
        c2 = MockSyncGrpcChannel("c2")
        c3 = MockSyncGrpcChannel("c3")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(
                min_channels=1,
                max_channels=2,
                max_rpc_per_channel=25,
            ),
            auto_start_background_tasks=False,
        )
        entry2 = ChannelEntry(id=2, logical_channel_id=2, channel=c2)
        entry2.set_state(ChannelState.DRAINING)
        entry2.last_activity = 2000.0
        entry3 = ChannelEntry(id=3, logical_channel_id=3, channel=c3)
        entry3.set_state(ChannelState.DRAINING)
        entry3.last_activity = 1000.0
        pool._draining_entries = (entry2, entry3)
        pool._consecutive_low_load_checks = 2

        # Induce load on c1: 30 in-flight RPCs -> desired = 2 channels -> channels_to_add = 1
        for _ in range(30):
            pool._active_entries[0].increment_in_flight()

        pool._execute_scale_up()

        # Exactly one draining entry was promoted, the other remains draining
        self.assertEqual(len(pool._active_entries), 2)
        self.assertEqual(len(pool._draining_entries), 1)
        self.assertIn(entry2, pool._active_entries)
        self.assertIn(entry3, pool._draining_entries)
        self.assertEqual(entry2.state, ChannelState.ACTIVE)
        self.assertEqual(entry3.state, ChannelState.DRAINING)
        # Consecutive low load checks reset to 0
        self.assertEqual(pool._consecutive_low_load_checks, 0)
        pool.close()

    def test_dial_prime_and_publish_failure_and_shutdown_paths(self):
        c1 = MockSyncGrpcChannel("c1")
        pool = ChannelPool.from_channels(
            [c1],
            options=ChannelPoolOptions(min_channels=1, max_channels=4),
            auto_start_background_tasks=False,
        )

        # 1. When warming fails, channel is closed and not published
        failing_channel = MockSyncGrpcChannel("failing")
        failing_channel.close = mock.Mock()
        pool._channel_factory = mock.Mock(return_value=failing_channel)
        with mock.patch.object(pool, "_warm_channel", return_value=False):
            pool._dial_prime_and_publish_one()
            failing_channel.close.assert_called_once()
            self.assertEqual(len(pool._active_entries), 1)

        # 2. When priming fails, channel is closed and not published
        failing_prime_channel = MockSyncGrpcChannel("failing_prime")
        failing_prime_channel.close = mock.Mock()
        pool._channel_factory = mock.Mock(return_value=failing_prime_channel)
        pool._prime_session = "projects/p/instances/i/databases/d/sessions/s1"
        with mock.patch.object(pool, "_prime_channel", return_value=False):
            pool._dial_prime_and_publish_one()
            failing_prime_channel.close.assert_called_once()
            self.assertEqual(len(pool._active_entries), 1)

        # 3. When shutdown is set during dial, channel is closed and not published
        shutdown_channel = MockSyncGrpcChannel("shutdown_ch")
        shutdown_channel.close = mock.Mock()

        def dial_and_shutdown():
            pool._shutdown_event.set()
            return shutdown_channel

        pool._channel_factory = mock.Mock(side_effect=dial_and_shutdown)
        with mock.patch.object(pool, "_warm_channel", return_value=True):
            pool._dial_prime_and_publish_one()
            shutdown_channel.close.assert_called_once()
            self.assertEqual(len(pool._active_entries), 1)
        pool.close()

    def test_warm_channel_direct_coverage(self):
        pool = ChannelPool(
            options=ChannelPoolOptions(prime_timeout_seconds=0.1),
            auto_start_background_tasks=False,
        )

        # 1. Success with subscribe and channel_ready_future
        mock_channel = mock.Mock()
        mock_channel.subscribe = mock.Mock()
        mock_future = mock.Mock()
        mock_future.result = mock.Mock(return_value=None)
        with mock.patch("grpc.channel_ready_future", return_value=mock_future):
            self.assertTrue(pool._warm_channel(mock_channel))
            mock_future.result.assert_called_once_with(timeout=0.1)

        # 2. Timeout/failure with subscribe and channel_ready_future cancels future and logs
        mock_failing_channel = mock.Mock()
        mock_failing_channel.subscribe = mock.Mock()
        mock_failing_future = mock.Mock()
        mock_failing_future.result = mock.Mock(
            side_effect=grpc.FutureTimeoutError("timeout")
        )
        mock_failing_future.cancel = mock.Mock()
        with (
            mock.patch("grpc.channel_ready_future", return_value=mock_failing_future),
            mock.patch(
                "google.cloud.spanner_v1.channel_pool._LOGGER.debug"
            ) as mock_debug,
        ):
            self.assertFalse(pool._warm_channel(mock_failing_channel))
            mock_failing_future.cancel.assert_called_once()
            mock_debug.assert_called_once()

        # 3. Fallback to get_state
        mock_get_state_channel = mock.Mock(spec=["get_state"])
        mock_get_state_channel.get_state = mock.Mock(
            return_value=grpc.ChannelConnectivity.READY
        )
        self.assertTrue(pool._warm_channel(mock_get_state_channel))
        mock_get_state_channel.get_state.assert_called_once_with(try_to_connect=True)

        # 4. Fallback get_state raises exception
        mock_failing_get_state = mock.Mock(spec=["get_state"])
        mock_failing_get_state.get_state = mock.Mock(
            side_effect=RuntimeError("connection error")
        )
        with mock.patch(
            "google.cloud.spanner_v1.channel_pool._LOGGER.debug"
        ) as mock_debug:
            self.assertFalse(pool._warm_channel(mock_failing_get_state))
            mock_debug.assert_called_once()
        pool.close()
