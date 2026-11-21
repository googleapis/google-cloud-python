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

from google.cloud.spanner_v1 import (
    BatchCreateSessionsRequest,
    BurstyPool,
    CreateSessionRequest,
    FixedSizePool,
    PingingPool,
)
from google.cloud.spanner_v1._async.pool import BurstyPool as AsyncBurstyPool
from google.cloud.spanner_v1._async.pool import FixedSizePool as AsyncFixedSizePool
from google.cloud.spanner_v1._async.pool import PingingPool as AsyncPingingPool
from tests.mockserver_tests.mock_server_test_base import (
    AsyncMockServerTestBase,
    MockServerTestBase,
)


class _PoolBindingAssertionsMixin:
    """Shared synchronous assertions for pool binding and role propagation."""

    def _assert_pool_bound(self, database, expected_pool_role: str):
        self.assertEqual(database._pool.database_role, expected_pool_role)
        self.assertIs(database._pool._database, database)

    def _assert_batch_create_role(self, expected_role: str):
        batch_create_requests = [
            request
            for request in self.spanner_service.requests
            if isinstance(request, BatchCreateSessionsRequest)
        ]
        self.assertEqual(len(batch_create_requests), 1)
        self.assertEqual(
            batch_create_requests[0].session_template.creator_role, expected_role
        )

    def _assert_session_role(self, session, expected_role: str):
        self.assertEqual(session.database_role, expected_role)
        self.assertIn(session.name, self.spanner_service.sessions)
        server_session = self.spanner_service.sessions[session.name]
        self.assertEqual(server_session.creator_role, expected_role)

    def _assert_create_session_role(self, expected_role: str):
        create_session_requests = [
            request
            for request in self.spanner_service.requests
            if isinstance(request, CreateSessionRequest)
        ]
        self.assertEqual(len(create_session_requests), 1)
        self.assertEqual(create_session_requests[0].session.creator_role, expected_role)


class TestPoolBinding(_PoolBindingAssertionsMixin, MockServerTestBase):
    def test_database_binding_of_fixed_size_pool(self):
        pool = FixedSizePool(
            size=1,
            default_timeout=500,
            database_role="parent",
        )
        database = self.instance.database("fixed_size_db", pool=pool)
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            pool.put(session)

    def test_database_binding_of_pinging_pool(self):
        pool = PingingPool(
            size=1,
            default_timeout=500,
            ping_interval=100,
            database_role="parent",
        )
        database = self.instance.database("binding_db", pool=pool)
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            pool.put(session)

    def test_database_binding_of_bursty_pool(self):
        pool = BurstyPool(
            target_size=1,
            database_role="parent",
        )
        database = self.instance.database("bursty_db", pool=pool)
        self._assert_pool_bound(database, "parent")

    def test_database_binding_with_database_role_on_database(self):
        pool = FixedSizePool(
            size=1,
            default_timeout=500,
        )
        database = self.instance.database(
            "db_role_on_database", pool=pool, database_role="parent"
        )
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            pool.put(session)

    def test_database_binding_pinging_pool_inherits_database_role(self):
        pool = PingingPool(
            size=1,
            default_timeout=500,
            ping_interval=100,
        )
        database = self.instance.database(
            "pinging_inherits_db", pool=pool, database_role="parent"
        )
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            pool.put(session)

    def test_database_binding_bursty_pool_inherits_database_role(self):
        pool = BurstyPool(
            target_size=1,
        )
        database = self.instance.database(
            "bursty_inherits_db", pool=pool, database_role="parent"
        )
        self._assert_pool_bound(database, "parent")

        session = pool.get()
        try:
            self._assert_session_role(session, "parent")
            self._assert_create_session_role("parent")
        finally:
            pool.put(session)

    def test_database_binding_pool_role_precedence(self):
        pool = FixedSizePool(
            size=1,
            default_timeout=500,
            database_role="pool-role",
        )
        database = self.instance.database(
            "role_precedence_db", pool=pool, database_role="database-role"
        )
        self.assertEqual(database.database_role, "database-role")
        self._assert_pool_bound(database, "pool-role")
        self._assert_batch_create_role("pool-role")

        session = pool.get()
        try:
            self._assert_session_role(session, "pool-role")
        finally:
            pool.put(session)


class TestPoolBindingAsync(_PoolBindingAssertionsMixin, AsyncMockServerTestBase):
    async def test_async_database_binding_of_fixed_size_pool(self):
        pool = AsyncFixedSizePool(
            size=1,
            default_timeout=500,
            database_role="parent",
        )
        database = await self.create_database("fixed_size_db", pool=pool)
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = await pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            await pool.put(session)

    async def test_async_database_binding_of_pinging_pool(self):
        pool = AsyncPingingPool(
            size=1,
            default_timeout=500,
            ping_interval=100,
            database_role="parent",
        )
        database = await self.create_database("binding_db", pool=pool)
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = await pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            await pool.put(session)

    async def test_async_database_binding_of_bursty_pool(self):
        pool = AsyncBurstyPool(
            target_size=1,
            database_role="parent",
        )
        database = await self.create_database("bursty_db", pool=pool)
        self._assert_pool_bound(database, "parent")

    async def test_async_database_binding_with_database_role_on_database(self):
        pool = AsyncFixedSizePool(
            size=1,
            default_timeout=500,
        )
        database = await self.create_database(
            "db_role_on_database", pool=pool, database_role="parent"
        )
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = await pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            await pool.put(session)

    async def test_async_database_binding_pinging_pool_inherits_database_role(self):
        pool = AsyncPingingPool(
            size=1,
            default_timeout=500,
            ping_interval=100,
        )
        database = await self.create_database(
            "pinging_inherits_db", pool=pool, database_role="parent"
        )
        self._assert_pool_bound(database, "parent")
        self._assert_batch_create_role("parent")

        session = await pool.get()
        try:
            self._assert_session_role(session, "parent")
        finally:
            await pool.put(session)

    async def test_async_database_binding_bursty_pool_inherits_database_role(self):
        pool = AsyncBurstyPool(
            target_size=1,
        )
        database = await self.create_database(
            "bursty_inherits_db", pool=pool, database_role="parent"
        )
        self._assert_pool_bound(database, "parent")

        session = await pool.get()
        try:
            self._assert_session_role(session, "parent")
            self._assert_create_session_role("parent")
        finally:
            await pool.put(session)

    async def test_async_database_binding_pool_role_precedence(self):
        pool = AsyncFixedSizePool(
            size=1,
            default_timeout=500,
            database_role="pool-role",
        )
        database = await self.create_database(
            "role_precedence_db", pool=pool, database_role="database-role"
        )
        self.assertEqual(database.database_role, "database-role")
        self._assert_pool_bound(database, "pool-role")
        self._assert_batch_create_role("pool-role")

        session = await pool.get()
        try:
            self._assert_session_role(session, "pool-role")
        finally:
            await pool.put(session)
