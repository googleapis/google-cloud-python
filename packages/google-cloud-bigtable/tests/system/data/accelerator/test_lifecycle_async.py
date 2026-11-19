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

import multiprocessing
import os
import queue
import shutil
import time
import uuid

from google.cloud.bigtable.data._accelerator import _daemon
from google.cloud.bigtable.data._cross_sync import CrossSync
from google.cloud.bigtable.data.mutations import DeleteAllFromRow, SetCell

from . import _harness

if CrossSync.is_async:
    from ._base_async import AcceleratorTestBaseAsync as AcceleratorTestBase
else:
    from ._base_autogen import AcceleratorTestBase

__CROSS_SYNC_OUTPUT__ = "tests.system.data.accelerator.test_lifecycle_autogen"


def _daemon_owner_process(project, instance_id, table_id, app_profile_id, result_queue):
    """Start a daemon, report ("ok", (pid, tempdir)) or ("error", repr), then block."""
    from google.cloud.bigtable.data import BigtableDataClient

    try:
        override = _harness.SETTINGS.accelerator_bin
        if override:
            _daemon._resolve_binary_path = lambda: override
        with BigtableDataClient(project=project, use_accelerator=True) as client:
            table_kwargs = {"app_profile_id": app_profile_id} if app_profile_id else {}
            with client.get_table(instance_id, table_id, **table_kwargs) as table:
                key = f"crash-{uuid.uuid4().hex}".encode()
                ts = _harness.ms_ts(1000)
                table.mutate_row(
                    key, SetCell(_harness.TEST_FAMILY, b"q", b"v", timestamp_micros=ts)
                )
                table.mutate_row(key, DeleteAllFromRow())
                result_queue.put(
                    (
                        "ok",
                        (
                            _harness.daemon_pid(table),
                            table._accelerator_daemon._tempdir,
                        ),
                    )
                )
                while True:
                    time.sleep(3600)
    except Exception as exc:
        result_queue.put(("error", repr(exc)))
        raise


@CrossSync.convert_class(sync_name="TestLifecycle")
class TestLifecycleAsync(AcceleratorTestBase):
    LIFECYCLE_ITERATIONS = 8
    # Below the iteration count, so leaking one fd per lifecycle fails.
    LIFECYCLE_FD_SLACK = 4
    # The daemon documents exiting within ~500ms of its parent dying.
    ORPHAN_EXIT_TIMEOUT = 5.0

    @CrossSync.convert
    async def _one_lifecycle(self, instance_id, table_id):
        async with self._make_client(use_accelerator=True) as client:
            async with client.get_table(instance_id, table_id) as table:
                self.assert_accelerator_active(table)
                key = f"life-{uuid.uuid4().hex}".encode()
                await table.mutate_row(
                    key,
                    SetCell(
                        _harness.TEST_FAMILY,
                        b"q",
                        b"v",
                        timestamp_micros=_harness.ms_ts(1000),
                    ),
                )
                assert (await table.read_row(key)) is not None
                await table.mutate_row(key, DeleteAllFromRow())

    @CrossSync.pytest
    async def test_close_reaps_daemon_and_tempdir(self, instance_id, table_id):
        async with self._make_client(use_accelerator=True) as client:
            async with client.get_table(instance_id, table_id) as table:
                self.assert_accelerator_active(table)
                pid = _harness.daemon_pid(table)
                tempdir = table._accelerator_daemon._tempdir
                assert pid is not None and _harness.pid_alive(pid)
                assert tempdir is not None and os.path.exists(tempdir)
        assert not _harness.pid_alive(pid), "daemon still alive after client close"
        assert not _harness.pid_exists(pid), "daemon exited but was not reaped"
        assert not os.path.exists(tempdir), "UDS tempdir not cleaned up"

    @CrossSync.pytest
    async def test_no_leaks_over_repeated_lifecycles(self, instance_id, table_id):
        introspector = _harness.ProcessIntrospector()
        await self._one_lifecycle(instance_id, table_id)
        before = introspector.snapshot()
        for _ in range(self.LIFECYCLE_ITERATIONS):
            await self._one_lifecycle(instance_id, table_id)
        introspector.assert_no_leaks(
            before,
            fd_slack=self.LIFECYCLE_FD_SLACK,
            label=f"{self.LIFECYCLE_ITERATIONS}x accelerator lifecycle",
        )

    @CrossSync.pytest
    async def test_close_reclaims_resources_after_daemon_crash(
        self, instance_id, table_id
    ):
        introspector = _harness.ProcessIntrospector()
        # Warm up so fds opened on first client use are in the baseline.
        await self._one_lifecycle(instance_id, table_id)
        before = introspector.snapshot()
        async with self._make_client(use_accelerator=True) as client:
            async with client.get_table(instance_id, table_id) as table:
                self.assert_accelerator_active(table)
                pid = _harness.daemon_pid(table)
                tempdir = table._accelerator_daemon._tempdir
                assert pid is not None and _harness.pid_alive(pid)
                assert tempdir is not None and os.path.exists(tempdir)
                _harness.force_kill_daemon(table._accelerator_daemon)
                assert not _harness.pid_alive(pid), "daemon did not die after kill"
        assert not os.path.exists(tempdir), "client.close() did not reclaim tempdir"
        introspector.assert_no_leaks(before, label="daemon-crash teardown")

    @CrossSync.pytest
    async def test_no_daemon_leak_when_owner_process_is_killed(
        self, instance_id, table_id
    ):
        project = self._project_id()
        app_profile_id = _harness.SETTINGS.app_profile_id
        ctx = multiprocessing.get_context("spawn")
        result_queue = ctx.Queue()
        owner = ctx.Process(
            target=_daemon_owner_process,
            args=(project, instance_id, table_id, app_profile_id, result_queue),
        )
        owner.start()
        tempdir = None
        try:
            report = None
            deadline = time.monotonic() + 60.0
            while report is None and time.monotonic() < deadline:
                try:
                    report = result_queue.get_nowait()
                except queue.Empty:
                    if owner.is_alive():
                        await CrossSync.sleep(0.2)
                        continue
                    # The owner may have queued its failure just before exiting.
                    try:
                        report = result_queue.get(timeout=1.0)
                    except queue.Empty:
                        break
            assert report is not None, (
                "owner process exited or timed out before reporting a daemon"
            )
            status, payload = report
            assert status == "ok", f"owner process failed to start a daemon: {payload}"
            daemon_pid, tempdir = payload
            assert daemon_pid is not None, "owner process has no accelerator daemon"
            assert _harness.pid_alive(daemon_pid), "daemon not alive after owner start"
            owner.kill()
            deadline = time.monotonic() + 10.0
            while owner.is_alive() and time.monotonic() < deadline:
                await CrossSync.sleep(0.05)
            assert not owner.is_alive(), "owner process still alive after kill"
            deadline = time.monotonic() + self.ORPHAN_EXIT_TIMEOUT
            while _harness.pid_alive(daemon_pid) and time.monotonic() < deadline:
                await CrossSync.sleep(0.1)
            assert not _harness.pid_alive(daemon_pid), (
                f"orphaned daemon {daemon_pid} still alive "
                f"{self.ORPHAN_EXIT_TIMEOUT:g}s after its owner died"
            )
            socket_path = os.path.join(tempdir, _daemon._SOCKET_FILENAME)
            assert not os.path.exists(socket_path), "orphaned daemon left its socket"
        finally:
            if owner.is_alive():
                owner.kill()
                owner.join()
            if tempdir and os.path.isdir(tempdir):
                shutil.rmtree(tempdir, ignore_errors=True)
