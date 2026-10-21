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

import uuid

import pytest
from google.api_core import exceptions as core_exceptions

from google.cloud.bigtable.data._accelerator import _daemon
from google.cloud.bigtable.data._cross_sync import CrossSync
from google.cloud.bigtable.data.mutations import DeleteAllFromRow, SetCell

from . import _harness

if CrossSync.is_async:
    from ._base_async import AcceleratorTestBaseAsync as AcceleratorTestBase
else:
    from ._base_autogen import AcceleratorTestBase

__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator.test_error_handling_autogen"


@CrossSync.convert_class(sync_name="TestErrorHandling")
class TestErrorHandlingAsync(AcceleratorTestBase):
    @CrossSync.convert
    async def _assert_round_trip(self, table):
        key = f"errtest-{uuid.uuid4().hex}".encode()
        ts = 1000 * _harness.MS
        await table.mutate_row(
            key, SetCell(_harness.TEST_FAMILY, b"q", b"ok", timestamp_micros=ts)
        )
        row = await table.read_row(key)
        assert row is not None and row.cells[0].value == b"ok"
        return key

    @CrossSync.pytest
    async def test_start_failure_falls_back_to_native(
        self, tmp_bin_dir, instance_id, table_id, monkeypatch
    ):
        path = _harness.immediately_exiting_binary(tmp_bin_dir, monkeypatch=monkeypatch)
        monkeypatch.setenv(_harness.BIN_ENV_VAR, path)
        monkeypatch.setattr(_daemon, "_resolve_binary_path", lambda: path)

        async with self._make_client(use_accelerator=True) as explicit_client:
            with pytest.raises(RuntimeError, match="exited during startup"):
                explicit_client.get_table(instance_id, table_id)

        async with self._make_client() as client:
            with pytest.warns(RuntimeWarning, match="Failed to start"):
                table = client.get_table(instance_id, table_id)
            async with table:
                assert table._accelerator_client is None
                assert table._accelerator_daemon is None
                key = await self._assert_round_trip(table)
                await table.mutate_row(key, DeleteAllFromRow())

    @CrossSync.pytest
    async def test_daemon_killed_midflight_falls_back_to_native(
        self, instance_id, table_id, native_table
    ):
        async with self._make_client(use_accelerator=True) as client:
            async with client.get_table(instance_id, table_id) as table:
                self.assert_accelerator_active(table)
                key = await self._assert_round_trip(table)
                assert not table._accelerator_breaker.bypass()

                pid = _harness.daemon_pid(table)
                assert pid is not None and _harness.pid_alive(pid)
                _harness.force_kill_daemon(table._accelerator_daemon)
                assert not table._accelerator_daemon.is_running

                row = await table.read_row(key, operation_timeout=30)
                assert row is not None and row.cells[0].value == b"ok"

                assert table._accelerator_breaker.bypass()
                assert table._accelerator_client is not None
                assert table._use_accelerator("read_row") is False
                assert table._use_accelerator("mutate_row") is False

                after_ts = 2000 * _harness.MS
                cell = SetCell(_harness.TEST_FAMILY, b"q", b"after", after_ts)
                await table.mutate_row(key, cell, operation_timeout=30)
                roundtrip = await table.read_row(key)
                assert any(c.value == b"after" for c in roundtrip.cells)

        assert (await native_table.read_row(key)) is not None
        await native_table.mutate_row(key, DeleteAllFromRow())

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
        bad = SetCell("no-such-family", b"q", b"v", timestamp_micros=1000 * _harness.MS)
        with pytest.raises(Exception) as accel_ei:
            await accel_table.mutate_row(key, bad)
        with pytest.raises(Exception) as native_ei:
            await native_table.mutate_row(key, bad)
        assert type(accel_ei.value) is type(native_ei.value)
