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
"""Crash correctness, fallback, and error parity tests for the accelerator."""

import copy
import threading
import time
import uuid

import pytest
from google.api_core import exceptions as core_exceptions

from google.cloud.bigtable.data._cross_sync import CrossSync
from google.cloud.bigtable.data.mutations import AddToCell, SetCell

from . import _harness

if CrossSync.is_async:
    from ._base_async import AcceleratorTestBaseAsync as AcceleratorTestBase
else:
    from ._base_autogen import AcceleratorTestBase

__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator.test_error_handling_autogen"


@CrossSync.convert_class(sync_name="TestErrorHandling")
class TestErrorHandlingAsync(AcceleratorTestBase):
    # Number of times to repeat the single-worker mid-flight daemon crash test.
    CRASH_ITERATIONS = 8
    # Number of mutations issued by the single worker per crash iteration.
    OPS_PER_CRASH_RUN = 20
    # Read back and verify every 4th mutated row during the workload.
    SPOT_CHECK_INTERVAL = 4

    @CrossSync.convert
    async def _run_crash_workload(self, table, native_table, janitor, iteration):
        prefix = f"crash-iter{iteration}-{uuid.uuid4().hex[:8]}-".encode()
        ops = _harness.RandomOps(
            seed=100 + iteration,
            key_prefix=prefix,
            include_aggregate=False,
            include_deletes=False,
        )
        expected_state = _harness.ExpectedState()
        touched = set()
        kill_at_op = self.OPS_PER_CRASH_RUN // 3
        kill_trigger = threading.Event()

        def _kill_daemon_from_background():
            if kill_trigger.wait(timeout=30.0):
                time.sleep(0.002 * (iteration % 4))
                _harness.force_kill_daemon(table._accelerator_daemon)

        killer_thread = threading.Thread(
            target=_kill_daemon_from_background, daemon=True
        )
        killer_thread.start()
        try:
            for i in range(self.OPS_PER_CRASH_RUN):
                if i == kill_at_op:
                    kill_trigger.set()
                prev_rows = copy.deepcopy(expected_state._rows)
                key, mutation = ops.build_mutation(expected_state)
                janitor.track(key)
                try:
                    await table.mutate_row(key, mutation, operation_timeout=30)
                    touched.add(key)
                except core_exceptions.GoogleAPICallError:
                    # Both throwing a mutation error and succeeding are acceptable
                    # when the daemon is killed mid-flight from another thread.
                    # Reconcile expected_state with whether the in-flight mutation
                    # reached Bigtable before SIGKILL.
                    actual = _harness.normalize_row(
                        await native_table.read_row(key, operation_timeout=30)
                    )
                    if actual != expected_state.expected_cells(key):
                        expected_state._rows = prev_rows
                    touched.add(key)
                    continue
                # Spot-check every 4th mutation to verify reads across the mid-flight
                # daemon kill and fallback transition without reading on every op.
                if i % self.SPOT_CHECK_INTERVAL == self.SPOT_CHECK_INTERVAL - 1:
                    try:
                        row = await table.read_row(key, operation_timeout=30)
                    except core_exceptions.GoogleAPICallError:
                        row = await table.read_row(key, operation_timeout=30)
                    _harness.assert_rows_equivalent(
                        label_a=f"crash-iter-{iteration}-op-{i}",
                        cells_a=_harness.normalize_row(row),
                        label_b="model",
                        cells_b=expected_state.expected_cells(key),
                    )
        finally:
            kill_trigger.set()
            killer_thread.join(timeout=5.0)
        return sorted(touched), expected_state

    @CrossSync.pytest
    async def test_daemon_killed_during_active_idempotent_workload_preserves_correctness(
        self, instance_id, table_id, native_table, janitor
    ):
        """Killing the Go daemon from a background thread during an active
        idempotent workload must trip the breaker, fall back to native, and keep
        all rows consistent with ExpectedState and native reads across repeated runs."""
        for iteration in range(self.CRASH_ITERATIONS):
            async with self._make_client(use_accelerator=True) as client:
                async with client.get_table(instance_id, table_id) as table:
                    self.assert_accelerator_active(table)
                    assert not table._accelerator_breaker.bypass()

                    keys, expected_state = await self._run_crash_workload(
                        table, native_table, janitor, iteration
                    )

                    assert not table._accelerator_daemon.is_running
                    for key in keys:
                        accel_row = await table.read_row(key)
                        native_row = await native_table.read_row(key)
                        expected = expected_state.expected_cells(key)
                        _harness.assert_rows_equivalent(
                            label_a="fallback-table",
                            cells_a=_harness.normalize_row(accel_row),
                            label_b="expected",
                            cells_b=expected,
                        )
                        _harness.assert_rows_equivalent(
                            label_a="native-table",
                            cells_a=_harness.normalize_row(native_row),
                            label_b="expected",
                            cells_b=expected,
                        )
                    assert table._accelerator_breaker.bypass()
                    assert table._use_accelerator("read_row") is False
                    assert table._use_accelerator("mutate_row") is False

    @CrossSync.pytest
    async def test_non_idempotent_mutate_row_on_daemon_crash_does_not_double_apply(
        self, instance_id, table_id, native_table, janitor
    ):
        """When the daemon crashes on a non-idempotent AddToCell or server-timestamp
        SetCell, the call must raise rather than retrying on native, trip the
        breaker, and route subsequent increments through native with exact totals."""
        agg_key = janitor.track(f"crash-agg-{uuid.uuid4().hex}".encode())
        srv_key = janitor.track(f"crash-srv-{uuid.uuid4().hex}".encode())
        ts = _harness.ms_ts(1000)
        expected_state = _harness.ExpectedState()

        async with self._make_client(use_accelerator=True) as client:
            async with client.get_table(instance_id, table_id) as table:
                self.assert_accelerator_active(table)

                # 1. Apply an initial increment (+10) through the live accelerator.
                await table.mutate_row(
                    agg_key, expected_state.add_to_cell(agg_key, b"counter", 10, ts)
                )
                row = await table.read_row(agg_key)
                _harness.assert_rows_equivalent(
                    label_a="initial-agg",
                    cells_a=_harness.normalize_row(row),
                    label_b="expected",
                    cells_b=expected_state.expected_cells(agg_key),
                )

                # 2. Kill the daemon before a non-idempotent AddToCell (+100).
                # It must raise and trip the breaker rather than falling back to
                # native (which on a true mid-flight crash could double-increment).
                _harness.force_kill_daemon(table._accelerator_daemon)
                assert not table._accelerator_daemon.is_running

                with pytest.raises(core_exceptions.GoogleAPICallError):
                    await table.mutate_row(
                        agg_key,
                        AddToCell(
                            _harness.TEST_AGGREGATE_FAMILY,
                            b"counter",
                            100,
                            timestamp_micros=ts,
                        ),
                    )
                assert table._accelerator_breaker.is_tripped
                assert table._use_accelerator("mutate_row") is False

                # 3. Subsequent AddToCell (+25) routes directly to native and
                # produces the exact expected total (10 + 25 = 35, never 135).
                await table.mutate_row(
                    agg_key, expected_state.add_to_cell(agg_key, b"counter", 25, ts)
                )
                final_row = await native_table.read_row(agg_key)
                _harness.assert_rows_equivalent(
                    label_a="final-agg",
                    cells_a=_harness.normalize_row(final_row),
                    label_b="expected",
                    cells_b=expected_state.expected_cells(agg_key),
                )

        # Also verify server-assigned timestamp SetCell (timestamp_micros=-1)
        # raises on daemon death rather than falling back.
        async with self._make_client(use_accelerator=True) as client2:
            async with client2.get_table(instance_id, table_id) as table2:
                self.assert_accelerator_active(table2)
                _harness.force_kill_daemon(table2._accelerator_daemon)
                with pytest.raises(core_exceptions.GoogleAPICallError):
                    await table2.mutate_row(
                        srv_key,
                        SetCell(
                            _harness.TEST_FAMILY,
                            b"q",
                            b"server-ts",
                            timestamp_micros=-1,
                        ),
                    )
                assert table2._accelerator_breaker.is_tripped
                assert (await native_table.read_row(srv_key)) is None

    @CrossSync.pytest
    async def test_shared_daemon_crash_falls_back_across_all_client_tables(
        self, instance_id, table_id, second_table_id, native_table, janitor
    ):
        async with self._make_client(use_accelerator=True) as client:
            async with (
                client.get_table(instance_id, table_id) as table_a,
                client.get_table(instance_id, second_table_id) as table_b,
            ):
                self.assert_accelerator_active(table_a)
                self.assert_accelerator_active(table_b)
                key_a = janitor.track(f"multi-a-{uuid.uuid4().hex}".encode())
                key_b = f"multi-b-{uuid.uuid4().hex}".encode()
                ts = _harness.ms_ts(1000)

                await table_a.mutate_row(
                    key_a,
                    SetCell(_harness.TEST_FAMILY, b"q", b"a1", timestamp_micros=ts),
                )
                _harness.force_kill_daemon(client._accelerator_daemon)

                # First call on table_a trips the shared client breaker and falls back;
                # table_b immediately sees the tripped breaker and also uses native.
                row_a = await table_a.read_row(key_a, operation_timeout=30)
                assert row_a is not None and row_a.cells[0].value == b"a1"
                assert table_a._use_accelerator("read_row") is False
                assert table_b._use_accelerator("mutate_row") is False

                await table_b.mutate_row(
                    key_b,
                    SetCell(_harness.TEST_FAMILY, b"q", b"b1", timestamp_micros=ts),
                )
                row_b = await table_b.read_row(key_b)
                assert row_b is not None and row_b.cells[0].value == b"b1"

    @CrossSync.pytest
    async def test_operation_timeout_enforced_as_deadline(
        self, accel_table, native_table
    ):
        key = f"errtest-{uuid.uuid4().hex}".encode()
        with pytest.raises(core_exceptions.DeadlineExceeded):
            await accel_table.read_row(key, operation_timeout=0.001)
        with pytest.raises(core_exceptions.DeadlineExceeded):
            await native_table.read_row(key, operation_timeout=0.001)
        assert not accel_table._accelerator_breaker.bypass()
        assert accel_table._accelerator_client is not None

    @CrossSync.pytest
    async def test_backend_error_type_matches_native(self, accel_table, native_table):
        key = f"errtest-{uuid.uuid4().hex}".encode()
        bad = SetCell(
            "no-such-family", b"q", b"v", timestamp_micros=_harness.ms_ts(1000)
        )
        with pytest.raises(Exception) as accel_ei:
            await accel_table.mutate_row(key, bad)
        with pytest.raises(Exception) as native_ei:
            await native_table.mutate_row(key, bad)
        assert type(accel_ei.value) is type(native_ei.value)
