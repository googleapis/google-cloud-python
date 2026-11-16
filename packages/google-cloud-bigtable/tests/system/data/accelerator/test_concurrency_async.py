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

import concurrent.futures
import functools
import uuid

import pytest

from google.cloud.bigtable.data._cross_sync import CrossSync

from . import _harness

if CrossSync.is_async:
    from ._base_async import AcceleratorTestBaseAsync as AcceleratorTestBase
else:
    from ._base_autogen import AcceleratorTestBase

__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator.test_concurrency_autogen"


@CrossSync.convert_class(sync_name="TestConcurrency")
class TestConcurrencyAsync(AcceleratorTestBase):
    CONCURRENCY = 8
    OPS_PER_WORKER = 50

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
    async def _worker(self, table, worker_id, key_prefix, janitor=None):
        ops = _harness.RandomOps(
            worker_id, key_prefix=key_prefix, include_deletes=False
        )
        expected_state = _harness.ExpectedState()
        touched = set()
        for _ in range(self.OPS_PER_WORKER):
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
    async def test_concurrent_multitable_workers_stay_consistent(
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
                            self._worker,
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
