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
"""Differential read/write correctness tests for the Cloud Bigtable accelerator."""

import concurrent.futures
import functools
import uuid

import pytest

from google.cloud.bigtable.data._cross_sync import CrossSync
from google.cloud.bigtable.data.mutations import DeleteRangeFromColumn
from google.cloud.bigtable.data.row_filters import CellsRowLimitFilter

from . import _harness

if CrossSync.is_async:
    from ._base_async import AcceleratorTestBaseAsync as AcceleratorTestBase
else:
    from ._base_autogen import AcceleratorTestBase

__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator.test_fuzz_correctness_autogen"


@CrossSync.convert_class(sync_name="TestFuzzCorrectness")
class TestFuzzCorrectnessAsync(AcceleratorTestBase):
    CONCURRENCY = 8
    OPS_PER_WORKER = 64
    MULTITABLE_OPS_PER_WORKER = 50

    @pytest.fixture(scope="session")
    @classmethod
    def second_table_id(
        cls,
        admin_client,
        project_id,
        instance_id,
        column_family_config,
        column_split_config,
    ):
        from google.api_core import exceptions, retry

        second_id = f"test-table-2-{uuid.uuid4().hex[:12]}"
        assert len(second_id) <= 50
        retry_fn = retry.Retry(
            predicate=retry.if_exception_type(exceptions.FailedPrecondition)
        )
        parent_path = f"projects/{project_id}/instances/{instance_id}"
        admin_client.table_admin_client.create_table(
            request={
                "parent": parent_path,
                "table_id": second_id,
                "table": {"column_families": column_family_config},
                "initial_splits": [{"key": key} for key in column_split_config],
            },
            retry=retry_fn,
        )
        try:
            yield second_id
        finally:
            try:
                admin_client.table_admin_client.delete_table(
                    name=f"{parent_path}/tables/{second_id}"
                )
            except Exception as exc:
                print(f"Failed to delete table {second_id}: {exc}")

    @CrossSync.convert
    async def _verify_key(self, accel_table, native_table, expected_state, key):
        accel_row = await accel_table.read_row(key)
        native_row = await native_table.read_row(key)
        expected = expected_state.expected_cells(key)
        accel_cells = _harness.normalize_row(accel_row)
        native_cells = _harness.normalize_row(native_row)
        _harness.assert_rows_equivalent(
            "accelerator", accel_cells, "expected", expected
        )
        _harness.assert_rows_equivalent(
            "accelerator", accel_cells, "native", native_cells
        )

    @CrossSync.convert
    async def _fuzz_worker(
        self, accel_table, native_table, janitor, seed, worker_id, run_id
    ):
        prefix = f"fuzz-{seed}-{run_id}-w{worker_id}-".encode()
        ops = _harness.RandomOps(
            seed * 100 + worker_id,
            key_prefix=prefix,
            include_aggregate=True,
            include_deletes=False,
        )
        expected_state = _harness.ExpectedState()
        touched: set[bytes] = set()

        for i in range(self.OPS_PER_WORKER):
            key, mutation = ops.build_mutation(expected_state)
            janitor.track(key)
            await accel_table.mutate_row(key, mutation)
            touched.add(key)
            if touched and i % 8 == 7:
                vkey = ops._rand.choice(sorted(touched))
                await self._verify_key(accel_table, native_table, expected_state, vkey)

        for key in sorted(touched):
            await self._verify_key(accel_table, native_table, expected_state, key)
        return sorted(touched)

    @pytest.mark.parametrize("seed", [0, 1])
    @CrossSync.pytest
    async def test_random_mutations_match_model_and_native(
        self, accel_table, native_table, janitor, seed
    ):
        run_id = uuid.uuid4().hex[:8]
        executor = (
            concurrent.futures.ThreadPoolExecutor(max_workers=self.CONCURRENCY)
            if not CrossSync.is_async
            else None
        )
        try:
            partials = [
                functools.partial(
                    self._fuzz_worker,
                    accel_table,
                    native_table,
                    janitor,
                    seed,
                    w,
                    run_id,
                )
                for w in range(self.CONCURRENCY)
            ]
            results = await CrossSync.gather_partials(
                partials, return_exceptions=True, sync_executor=executor
            )
        finally:
            if executor is not None:
                executor.shutdown(wait=True)

        for w, result in enumerate(results):
            assert not isinstance(result, BaseException), (
                f"fuzz worker {w} failed: {result!r}"
            )

    @CrossSync.pytest
    async def test_multiple_versions_range_delete_and_row_filter(
        self, accel_table, native_table, janitor
    ):
        key = janitor.track(f"versions-{uuid.uuid4().hex}".encode())
        family = _harness.TEST_FAMILY
        qualifier = b"q0"
        expected_state = _harness.ExpectedState()

        for ts_ms, value in [(1000, b"v1"), (2000, b"v2"), (3000, b"v3")]:
            ts = ts_ms * _harness.MS
            await accel_table.mutate_row(
                key, expected_state.set_cell(key, family, qualifier, value, ts)
            )
        await self._verify_key(accel_table, native_table, expected_state, key)

        # Verify row_filter parity (latest cell only).
        row_filter = CellsRowLimitFilter(1)
        accel_filtered = await accel_table.read_row(key, row_filter=row_filter)
        native_filtered = await native_table.read_row(key, row_filter=row_filter)
        _harness.assert_rows_equivalent(
            "accel-filtered",
            _harness.normalize_row(accel_filtered),
            "native-filtered",
            _harness.normalize_row(native_filtered),
        )
        assert len(accel_filtered.cells) == 1
        assert accel_filtered.cells[0].value == b"v3"

        # Delete middle version [2000ms, 3000ms).
        expected_state.delete_range_from_column(
            key, family, qualifier, 2000 * _harness.MS, 3000 * _harness.MS
        )
        await accel_table.mutate_row(
            key,
            DeleteRangeFromColumn(
                family, qualifier, 2000 * _harness.MS, 3000 * _harness.MS
            ),
        )
        await self._verify_key(accel_table, native_table, expected_state, key)

    @CrossSync.convert
    async def _multitable_worker(self, table, worker_id, key_prefix, janitor=None):
        ops = _harness.RandomOps(
            worker_id, key_prefix=key_prefix, include_deletes=False
        )
        expected_state = _harness.ExpectedState()
        touched = set()
        for _ in range(self.MULTITABLE_OPS_PER_WORKER):
            key, mutation = ops.build_mutation(expected_state)
            if janitor is not None:
                janitor.track(key)
            await table.mutate_row(key, mutation)
            touched.add(key)
        for key in sorted(touched):
            row = await table.read_row(key)
            _harness.assert_rows_equivalent(
                f"worker-{worker_id}",
                _harness.normalize_row(row),
                "model",
                expected_state.expected_cells(key),
            )
        return sorted(touched)

    @CrossSync.pytest
    async def test_shared_daemon_across_multiple_tables(
        self, instance_id, table_id, second_table_id, janitor
    ):
        async with CrossSync.DataClient(
            project=self._project_id(), use_accelerator=True
        ) as client:
            async with (
                client.get_table(instance_id, table_id) as table_a,
                client.get_table(instance_id, second_table_id) as table_b,
            ):
                self.assert_accelerator_active(table_a)
                self.assert_accelerator_active(table_b)
                daemon_pid_a = _harness.daemon_pid(table_a)
                assert _harness.daemon_pid(table_b) == daemon_pid_a

                run_id = uuid.uuid4().hex[:8]
                tables = (table_a, table_b)
                executor = (
                    concurrent.futures.ThreadPoolExecutor(max_workers=self.CONCURRENCY)
                    if not CrossSync.is_async
                    else None
                )
                try:
                    partials = [
                        functools.partial(
                            self._multitable_worker,
                            tables[w % 2],
                            w,
                            f"conc-mt-{run_id}-p{w // 2}-".encode(),
                            janitor if w % 2 == 0 else None,
                        )
                        for w in range(self.CONCURRENCY)
                    ]
                    results = await CrossSync.gather_partials(
                        partials, return_exceptions=True, sync_executor=executor
                    )
                finally:
                    if executor is not None:
                        executor.shutdown(wait=True)

                for w, result in enumerate(results):
                    assert not isinstance(result, BaseException), (
                        f"worker {w} failed: {result!r}"
                    )

                # Closing table_b must leave table_a and the shared daemon active.
                await table_b.close()
                assert _harness.daemon_pid(table_a) == daemon_pid_a
                verify_ops = _harness.RandomOps(
                    999,
                    key_prefix=f"conc-mt-after-close-{run_id}-".encode(),
                    include_deletes=False,
                )
                verify_state = _harness.ExpectedState()
                verify_keys = set()
                for _ in range(5):
                    vkey, vmut = verify_ops.build_mutation(verify_state)
                    janitor.track(vkey)
                    await table_a.mutate_row(vkey, vmut)
                    verify_keys.add(vkey)
                for vkey in sorted(verify_keys):
                    vrow = await table_a.read_row(vkey)
                    _harness.assert_rows_equivalent(
                        "table_a-after-close",
                        _harness.normalize_row(vrow),
                        "model",
                        verify_state.expected_cells(vkey),
                    )
