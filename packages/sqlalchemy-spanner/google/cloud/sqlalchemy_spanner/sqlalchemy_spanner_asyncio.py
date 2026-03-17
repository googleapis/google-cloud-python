# Copyright 2024 Google LLC
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
from .sqlalchemy_spanner import SpannerDialect
import sqlalchemy

from sqlalchemy.connectors.asyncio import (
    AsyncAdapt_dbapi_connection,
    AsyncAdapt_dbapi_cursor,
    AsyncAdapt_dbapi_module,
)
from sqlalchemy.util.concurrency import await_only


class AsyncIODBAPISpannerCursor:
    def __init__(self, sync_cursor):
        self._sync_cursor = sync_cursor

    @property
    def description(self):
        return self._sync_cursor.description

    @property
    def rowcount(self):
        return self._sync_cursor.rowcount

    @property
    def lastrowid(self):
        return self._sync_cursor.lastrowid

    @property
    def arraysize(self):
        return self._sync_cursor.arraysize

    @arraysize.setter
    def arraysize(self, value):
        self._sync_cursor.arraysize = value

    async def close(self):
        await asyncio.to_thread(self._sync_cursor.close)

    async def execute(self, operation, parameters=None):
        return await asyncio.to_thread(self._sync_cursor.execute, operation, parameters)

    async def executemany(self, operation, seq_of_parameters):
        return await asyncio.to_thread(
            self._sync_cursor.executemany, operation, seq_of_parameters
        )

    async def fetchone(self):
        return await asyncio.to_thread(self._sync_cursor.fetchone)

    async def fetchmany(self, size=None):
        if size is None:
            size = self.arraysize
        return await asyncio.to_thread(self._sync_cursor.fetchmany, size)

    async def fetchall(self):
        return await asyncio.to_thread(self._sync_cursor.fetchall)

    async def nextset(self):
        if hasattr(self._sync_cursor, "nextset"):
            return await asyncio.to_thread(self._sync_cursor.nextset)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class AsyncIODBAPISpannerConnection:
    def __init__(self, sync_conn):
        self._sync_conn = sync_conn

    async def commit(self):
        await asyncio.to_thread(self._sync_conn.commit)

    async def rollback(self):
        await asyncio.to_thread(self._sync_conn.rollback)

    async def close(self):
        await asyncio.to_thread(self._sync_conn.close)

    def cursor(self):
        return AsyncIODBAPISpannerCursor(self._sync_conn.cursor())

    def __getattr__(self, name):
        return getattr(self._sync_conn, name)


class AsyncAdapt_spanner_cursor(AsyncAdapt_dbapi_cursor):
    @property
    def connection(self):
        return self._adapt_connection


class AsyncAdapt_spanner_connection(AsyncAdapt_dbapi_connection):
    _cursor_cls = AsyncAdapt_spanner_cursor

    @property
    def connection(self):
        return self._connection._sync_conn

    def __getattr__(self, name):
        return getattr(self._connection, name)


class AsyncAdapt_spanner_dbapi(AsyncAdapt_dbapi_module):
    await_ = staticmethod(await_only)

    def __init__(self, spanner_dbapi):
        self.spanner_dbapi = spanner_dbapi
        for name in dir(spanner_dbapi):
            if not name.startswith("__") and name != "connect":
                setattr(self, name, getattr(spanner_dbapi, name))

    def connect(self, *arg, **kw):
        async_creator_fn = kw.pop("async_creator_fn", None)
        if async_creator_fn:
            connection = async_creator_fn(*arg, **kw)
        else:
            connection = self.spanner_dbapi.connect(*arg, **kw)

        return AsyncAdapt_spanner_connection(
            self, AsyncIODBAPISpannerConnection(connection)
        )


class SpannerDialect_asyncio(SpannerDialect):
    driver = "spanner_asyncio"
    is_async = True
    supports_statement_cache = True

    @classmethod
    def import_dbapi(cls):
        from google.cloud import spanner_dbapi

        return AsyncAdapt_spanner_dbapi(spanner_dbapi)

    @classmethod
    def dbapi(cls):
        return cls.import_dbapi()

    @classmethod
    def get_pool_class(cls, url):
        from sqlalchemy.pool import AsyncAdaptedQueuePool

        return AsyncAdaptedQueuePool

    def get_driver_connection(self, connection):
        return connection._connection
