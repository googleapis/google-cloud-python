# Copyright 2024 Google LLC All rights reserved.
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
import unittest
from unittest import mock

from google.cloud.spanner_v1._async.database_sessions_manager import (
    DatabaseSessionsManager,
    TransactionType,
)


class TestSessionsManagerExtra(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.database = mock.Mock()
        self.database.logger = mock.Mock()
        self.pool = mock.Mock()

    async def test_use_multiplexed_unsupported(self):
        # coverage for line 213
        with self.assertRaises(ValueError):
            DatabaseSessionsManager._use_multiplexed("invalid")

    async def test_get_session_experimental_host(self):
        # coverage for line 87 (experimental host branch)
        self.database._experimental_host = "experimental"
        manager = DatabaseSessionsManager(self.database, self.pool)
        session = mock.Mock()
        session.is_multiplexed = True
        session.session_id = "sid"

        with mock.patch.object(
            manager, "_get_multiplexed_session", return_value=session
        ):
            res = await manager.get_session(TransactionType.READ_WRITE)
            self.assertEqual(res, session)

    async def test_maintenance_thread_sync_branch(self):
        # coverage for line 127 and 158
        manager = DatabaseSessionsManager(self.database, self.pool)
        session = mock.Mock()
        session.session_id = "sid"

        with mock.patch(
            "google.cloud.spanner_v1._async.database_sessions_manager.CrossSync.is_async",
            False,
        ):
            with mock.patch.object(
                manager, "_build_multiplexed_session", return_value=session
            ):
                with mock.patch(
                    "google.cloud.spanner_v1._async.database_sessions_manager.Thread"
                ) as mock_thread:
                    await manager._get_multiplexed_session()
                    self.assertTrue(mock_thread.called)

    async def test_maintain_multiplexed_session_terminate(self):
        # coverage for line 191-193
        manager = DatabaseSessionsManager(self.database, self.pool)
        manager._multiplexed_session_terminate_event = asyncio.Event()
        manager._multiplexed_session_terminate_event.set()

        from weakref import ref

        # Should return immediately
        await manager._maintain_multiplexed_session(ref(manager))

    async def test_maintain_multiplexed_session_manager_gone(self):
        # coverage for line 178
        from weakref import ref

        class Fake:
            pass

        fake = Fake()
        r = ref(fake)
        del fake
        await DatabaseSessionsManager._maintain_multiplexed_session(r)

    async def test_close_branches(self):
        # coverage for line 225-234
        manager = DatabaseSessionsManager(self.database, self.pool)

        # Branch where thread is None
        await manager.close()

        # Branch where thread is not None
        async def fake_coro():
            try:
                await asyncio.sleep(10)
            except asyncio.CancelledError:
                pass

        task = asyncio.create_task(fake_coro())
        manager._multiplexed_session_thread = task
        manager._multiplexed_session = mock.AsyncMock()

        with mock.patch(
            "google.cloud.spanner_v1._async.database_sessions_manager.CrossSync.is_async",
            True,
        ):
            await manager.close()
            # task is cancelled and awaited in close()
            self.assertTrue(task.done())

        # Sync branch of close
        manager._multiplexed_session_thread = mock.Mock()
        manager._multiplexed_session = mock.AsyncMock()
        with mock.patch(
            "google.cloud.spanner_v1._async.database_sessions_manager.CrossSync.is_async",
            False,
        ):
            await manager.close()
            self.assertTrue(manager._multiplexed_session_thread.join.called)

    async def test_maintain_multiplexed_session_refresh(self):
        # coverage for line 196-202
        manager = DatabaseSessionsManager(self.database, self.pool)
        manager._multiplexed_session_lock = asyncio.Lock()
        manager._multiplexed_session_terminate_event = asyncio.Event()
        manager._multiplexed_session = mock.AsyncMock()

        # We need to simulate time passing and then terminating
        refresh_interval = manager._MAINTENANCE_THREAD_REFRESH_INTERVAL.total_seconds()

        from time import time
        from weakref import ref

        start_time = time()

        # Mock time to skip forward
        # First call in while loop: manager._multiplexed_session_terminate_event.is_set() -> False
        # Second call in while loop: time() - session_created_time < refresh_interval -> False (after mock)
        # Inside the 'if' block:
        # We want it to run once then terminate

        call_count = 0

        def mock_time():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return start_time
            if call_count >= 2:
                # Trigger refresh
                return start_time + refresh_interval + 10
            return start_time

        with mock.patch("time.time", side_effect=mock_time):

            async def mock_build():
                manager._multiplexed_session_terminate_event.set()
                return mock.AsyncMock()

            with mock.patch.object(
                manager, "_build_multiplexed_session", side_effect=mock_build
            ):
                await manager._maintain_multiplexed_session(ref(manager))

        self.assertTrue(manager._multiplexed_session_terminate_event.is_set())

    async def test_maintain_multiplexed_session_manager_gone_in_loop(self):
        # coverage for line 191
        # Mock session_manager_ref() within the loop
        manager = DatabaseSessionsManager(self.database, self.pool)
        call_count = 0

        def mock_ref():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return manager
            return None

        with mock.patch("time.time", return_value=0):
            # Wait, it's a static method, so we pass the ref
            r = mock.Mock(side_effect=mock_ref)
            await DatabaseSessionsManager._maintain_multiplexed_session(r)
            self.assertEqual(call_count, 2)

    async def test_maintain_multiplexed_session_loop_sleep(self):
        # coverage for line 196
        manager = DatabaseSessionsManager(self.database, self.pool)
        manager._multiplexed_session_lock = asyncio.Lock()
        manager._multiplexed_session_terminate_event = asyncio.Event()
        call_count = 0

        def mock_time():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return 0  # start_time
            if call_count == 2:
                return 1  # within refresh interval
            # terminate
            manager._multiplexed_session_terminate_event.set()
            return 1000

        from weakref import ref

        with mock.patch("time.time", side_effect=mock_time):
            with mock.patch(
                "google.cloud.spanner_v1._async.database_sessions_manager.CrossSync.sleep",
                mock.AsyncMock(),
            ):
                await manager._maintain_multiplexed_session(ref(manager))
