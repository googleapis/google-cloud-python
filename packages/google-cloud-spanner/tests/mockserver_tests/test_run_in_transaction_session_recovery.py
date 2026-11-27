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

import asyncio
import os
import queue
import threading
from unittest import mock

from google.api_core.exceptions import DeadlineExceeded

from google.cloud.spanner_v1 import (
    CommitRequest,
    CreateSessionRequest,
    ExecuteSqlRequest,
    FixedSizePool,
    PingingPool,
)
from google.cloud.spanner_v1._async.pool import (
    FixedSizePool as AsyncFixedSizePool,
)
from google.cloud.spanner_v1._async.pool import (
    PingingPool as AsyncPingingPool,
)
from google.cloud.spanner_v1.testing.mock_spanner import SpannerServicer
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
    aborted_status,
    add_error,
    add_select1_result,
    deadline_exceeded_status,
)

_SYNC_WAIT_TIMEOUT_SECONDS = 5.0


class TestRunInTransactionSessionRecovery(MockServerTestBase):
    def test_multiplexed_session_deadline_exceeded_then_recovers(self):
        add_select1_result()
        add_error(
            SpannerServicer.CreateSession.__name__,
            deadline_exceeded_status(),
        )

        with mock.patch.dict(
            os.environ,
            {"GOOGLE_CLOUD_SPANNER_MULTIPLEXED_SESSIONS_FOR_RW": "true"},
        ):
            database = self.instance.database(
                "mux-deadline-db",
                pool=FixedSizePool(size=1),
                enable_interceptors_in_tests=True,
                logger=self.logger,
            )
            try:
                callback_calls = 0

                def unit_of_work(transaction):
                    nonlocal callback_calls
                    callback_calls += 1
                    result_set = transaction.execute_sql("select 1")
                    return [row[0] for row in result_set]

                with self.assertRaisesRegex(DeadlineExceeded, "Deadline exceeded."):
                    database.run_in_transaction(unit_of_work)

                self.assertEqual(callback_calls, 0)
                self.assertFalse(database._local.transaction_running)
                self.assertIsNone(database._sessions_manager._multiplexed_session)

                rows = database.run_in_transaction(unit_of_work)

                self.assertEqual(rows, [1])
                self.assertEqual(callback_calls, 1)
                self.assertFalse(database._local.transaction_running)
                self.assertIsNotNone(database._sessions_manager._multiplexed_session)

                requests = self.spanner_service.requests
                create_session_requests = [
                    request
                    for request in requests
                    if isinstance(request, CreateSessionRequest)
                ]
                execute_sql_requests = [
                    request
                    for request in requests
                    if isinstance(request, ExecuteSqlRequest)
                ]
                commit_requests = [
                    request
                    for request in requests
                    if isinstance(request, CommitRequest)
                ]
                self.assertEqual(len(create_session_requests), 2)
                self.assertTrue(
                    all(
                        request.session.multiplexed
                        for request in create_session_requests
                    )
                )
                self.assertEqual(len(execute_sql_requests), 1)
                self.assertEqual(len(commit_requests), 1)
            finally:
                database.close()

    def test_regular_session_pool_exhausted_then_recovers(self):
        add_select1_result()

        with mock.patch.dict(
            os.environ,
            {"GOOGLE_CLOUD_SPANNER_MULTIPLEXED_SESSIONS_FOR_RW": "false"},
        ):
            database = self.instance.database(
                "regular-pool-exhausted-db",
                pool=PingingPool(size=1, default_timeout=0),
                enable_interceptors_in_tests=True,
                logger=self.logger,
            )
            acquired_event = threading.Event()
            release_event = threading.Event()
            worker_errors = []

            def hold_session(transaction):
                acquired_event.set()
                if not release_event.wait(timeout=_SYNC_WAIT_TIMEOUT_SECONDS):
                    raise TimeoutError(
                        "Timed out waiting to release held session (DEADLOCK)!"
                    )
                result_set = transaction.execute_sql("select 1")
                return [row[0] for row in result_set]

            def run_holder():
                try:
                    database.run_in_transaction(hold_session)
                except BaseException as exc:  # pragma: no cover - defensive
                    worker_errors.append(exc)

            worker_thread = threading.Thread(target=run_holder)
            worker_thread.start()
            try:
                if not acquired_event.wait(timeout=_SYNC_WAIT_TIMEOUT_SECONDS):
                    self.fail(
                        "Timed out waiting for worker thread to check out session (DEADLOCK)!"
                    )

                callback_calls = 0

                def unit_of_work(transaction):
                    nonlocal callback_calls
                    callback_calls += 1
                    result_set = transaction.execute_sql("select 1")
                    return [row[0] for row in result_set]

                with self.assertRaises(queue.Empty) as raised:
                    database.run_in_transaction(unit_of_work)
                self.assertEqual(str(raised.exception), "")

                self.assertEqual(callback_calls, 0)
                self.assertFalse(database._local.transaction_running)
            finally:
                release_event.set()
                worker_thread.join(timeout=_SYNC_WAIT_TIMEOUT_SECONDS)

            self.assertFalse(
                worker_thread.is_alive(),
                "Worker thread did not finish within timeout (DEADLOCK)!",
            )
            self.assertEqual(worker_errors, [])

            # Clear requests from the background worker and force an Aborted retry
            # on the recovered call to verify the same regular session is reused
            # across retry attempts.
            self.spanner_service.clear_requests()
            add_error(SpannerServicer.Commit.__name__, aborted_status())

            try:
                rows = database.run_in_transaction(unit_of_work)

                self.assertEqual(rows, [1])
                self.assertEqual(callback_calls, 2)
                self.assertFalse(database._local.transaction_running)

                requests = self.spanner_service.requests
                execute_sql_requests = [
                    request
                    for request in requests
                    if isinstance(request, ExecuteSqlRequest)
                ]
                commit_requests = [
                    request
                    for request in requests
                    if isinstance(request, CommitRequest)
                ]
                self.assertEqual(len(execute_sql_requests), 2)
                self.assertEqual(len(commit_requests), 2)
                session_names = {
                    request.session
                    for request in execute_sql_requests + commit_requests
                }
                self.assertEqual(len(session_names), 1)
            finally:
                database.close()


class TestAsyncRunInTransactionSessionRecovery(AsyncMockServerTestBase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        if AsyncMockServerTestBase.spanner_service:
            AsyncMockServerTestBase.spanner_service.clear_results()

    async def asyncTearDown(self):
        await super().asyncTearDown()
        if AsyncMockServerTestBase.spanner_service:
            AsyncMockServerTestBase.spanner_service.clear_results()

    async def test_multiplexed_session_deadline_exceeded_then_recovers(self):
        add_select1_result()
        add_error(
            SpannerServicer.CreateSession.__name__,
            deadline_exceeded_status(),
        )

        with mock.patch.dict(
            os.environ,
            {"GOOGLE_CLOUD_SPANNER_MULTIPLEXED_SESSIONS_FOR_RW": "true"},
        ):
            database = await self.instance.database(
                "async-mux-deadline-db",
                pool=AsyncFixedSizePool(size=1),
                enable_interceptors_in_tests=False,
                logger=self.logger,
            )
            try:
                callback_calls = 0

                async def unit_of_work(transaction):
                    nonlocal callback_calls
                    callback_calls += 1
                    result_set = await transaction.execute_sql("select 1")
                    return [row[0] async for row in result_set]

                with self.assertRaisesRegex(DeadlineExceeded, "Deadline exceeded."):
                    await database.run_in_transaction(unit_of_work)

                self.assertEqual(callback_calls, 0)
                self.assertFalse(database._local.transaction_running)
                self.assertIsNone(database._sessions_manager._multiplexed_session)

                rows = await database.run_in_transaction(unit_of_work)

                self.assertEqual(rows, [1])
                self.assertEqual(callback_calls, 1)
                self.assertFalse(database._local.transaction_running)
                self.assertIsNotNone(database._sessions_manager._multiplexed_session)

                requests = self.spanner_service.requests
                create_session_requests = [
                    request
                    for request in requests
                    if isinstance(request, CreateSessionRequest)
                ]
                execute_sql_requests = [
                    request
                    for request in requests
                    if isinstance(request, ExecuteSqlRequest)
                ]
                commit_requests = [
                    request
                    for request in requests
                    if isinstance(request, CommitRequest)
                ]
                self.assertEqual(len(create_session_requests), 2)
                self.assertTrue(
                    all(
                        request.session.multiplexed
                        for request in create_session_requests
                    )
                )
                self.assertEqual(len(execute_sql_requests), 1)
                self.assertEqual(len(commit_requests), 1)
            finally:
                await database.close()

    async def test_regular_session_pool_exhausted_then_recovers(self):
        add_select1_result()

        # TODO(https://github.com/googleapis/google-cloud-python/issues/19107):
        # Replace with AsyncPingingPool(size=1, default_timeout=0) once
        # CrossSync.queue_get handles timeout <= 0 on non-empty queues.
        class _NonBlockingAsyncPingingPool(AsyncPingingPool):
            """Test pool that raises QueueEmpty immediately when empty."""

            async def get(self, timeout=None):
                if self._sessions.empty():
                    raise asyncio.QueueEmpty()
                return await super().get(timeout=timeout)

        with mock.patch.dict(
            os.environ,
            {"GOOGLE_CLOUD_SPANNER_MULTIPLEXED_SESSIONS_FOR_RW": "false"},
        ):
            database = await self.instance.database(
                "async-regular-pool-exhausted-db",
                pool=_NonBlockingAsyncPingingPool(size=1, default_timeout=None),
                enable_interceptors_in_tests=False,
                logger=self.logger,
            )
            acquired_event = asyncio.Event()
            release_event = asyncio.Event()

            async def hold_session(transaction):
                acquired_event.set()
                try:
                    await asyncio.wait_for(
                        release_event.wait(), timeout=_SYNC_WAIT_TIMEOUT_SECONDS
                    )
                except asyncio.TimeoutError:
                    self.fail(
                        "Timed out waiting to release held async session (DEADLOCK)!"
                    )
                result_set = await transaction.execute_sql("select 1")
                return [row[0] async for row in result_set]

            worker_task = asyncio.create_task(database.run_in_transaction(hold_session))
            try:
                try:
                    await asyncio.wait_for(
                        acquired_event.wait(), timeout=_SYNC_WAIT_TIMEOUT_SECONDS
                    )
                except asyncio.TimeoutError:
                    self.fail(
                        "Timed out waiting for worker task to check out session (DEADLOCK)!"
                    )

                callback_calls = 0

                async def unit_of_work(transaction):
                    nonlocal callback_calls
                    callback_calls += 1
                    result_set = await transaction.execute_sql("select 1")
                    return [row[0] async for row in result_set]

                with self.assertRaises(asyncio.QueueEmpty) as raised:
                    await database.run_in_transaction(unit_of_work)
                self.assertEqual(str(raised.exception), "")

                self.assertEqual(callback_calls, 0)
                self.assertFalse(database._local.transaction_running)
            finally:
                release_event.set()
                try:
                    await asyncio.wait_for(
                        worker_task, timeout=_SYNC_WAIT_TIMEOUT_SECONDS
                    )
                except asyncio.TimeoutError:
                    self.fail("Worker task did not finish within timeout (DEADLOCK)!")

            self.spanner_service.clear_requests()
            add_error(SpannerServicer.Commit.__name__, aborted_status())

            try:
                rows = await database.run_in_transaction(unit_of_work)

                self.assertEqual(rows, [1])
                self.assertEqual(callback_calls, 2)
                self.assertFalse(database._local.transaction_running)

                requests = self.spanner_service.requests
                execute_sql_requests = [
                    request
                    for request in requests
                    if isinstance(request, ExecuteSqlRequest)
                ]
                commit_requests = [
                    request
                    for request in requests
                    if isinstance(request, CommitRequest)
                ]
                self.assertEqual(len(execute_sql_requests), 2)
                self.assertEqual(len(commit_requests), 2)
                session_names = {
                    request.session
                    for request in execute_sql_requests + commit_requests
                }
                self.assertEqual(len(session_names), 1)
            finally:
                await database.close()
