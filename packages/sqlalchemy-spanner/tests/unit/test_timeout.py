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

from unittest import mock

from sqlalchemy.testing import eq_
from sqlalchemy.testing.plugin.plugin_base import fixtures

from google.cloud import spanner_dbapi
from google.cloud.sqlalchemy_spanner.sqlalchemy_spanner import (
    _UNSET,
    SpannerDialect,
    SpannerExecutionContext,
    reset_connection,
)


class SqlAlchemyTimeoutTest(fixtures.TestBase):
    def test_reset_connection_clears_timeout(self):
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = 30.0
        dbapi_conn.inside_transaction = False

        reset_connection(dbapi_conn, None)

        eq_(dbapi_conn.timeout, None)

    def test_pre_exec_sets_timeout(self):
        context = SpannerExecutionContext()
        context.execution_options = {"timeout": 45.0}

        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = None
        context._dbapi_connection = mock.MagicMock()
        context._dbapi_connection.connection = dbapi_conn

        context.pre_exec()

        eq_(dbapi_conn.timeout, 45.0)

    def test_query_without_timeout_does_not_alter_connection_timeout(self):
        dialect = SpannerDialect()
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = 25.0

        context = SpannerExecutionContext()
        context.dialect = dialect
        context.execution_options = {}
        context._dbapi_connection = mock.MagicMock()
        context._dbapi_connection.connection = dbapi_conn

        context.pre_exec()
        eq_(dbapi_conn.timeout, 25.0)

        context.post_exec()
        eq_(dbapi_conn.timeout, 25.0)

    def test_statement_level_timeout_restores_previous_timeout_in_post_exec(self):
        dialect = SpannerDialect()
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = 25.0

        context = SpannerExecutionContext()
        context.dialect = dialect
        context.execution_options = {"timeout": 5.0}
        context._dbapi_connection = mock.MagicMock()
        context._dbapi_connection.connection = dbapi_conn

        context.pre_exec()
        eq_(dbapi_conn.timeout, 5.0)

        context.post_exec()
        eq_(dbapi_conn.timeout, 25.0)

    def test_statement_level_timeout_restores_previous_timeout_on_dbapi_exception(self):
        dialect = SpannerDialect()
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = 25.0

        context = SpannerExecutionContext()
        context.dialect = dialect
        context.execution_options = {"timeout": 5.0}
        context._dbapi_connection = mock.MagicMock()
        context._dbapi_connection.connection = dbapi_conn

        context.pre_exec()
        eq_(dbapi_conn.timeout, 5.0)

        context.handle_dbapi_exception(Exception("Statement timeout/error"))
        eq_(dbapi_conn.timeout, 25.0)

    def test_statement_level_timeout_none_overrides_and_restores(self):
        dialect = SpannerDialect()
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = 25.0

        context = SpannerExecutionContext()
        context.dialect = dialect
        context.execution_options = {"timeout": None}
        context._dbapi_connection = mock.MagicMock()
        context._dbapi_connection.connection = dbapi_conn

        context.pre_exec()
        eq_(dbapi_conn.timeout, None)

        context.post_exec()
        eq_(dbapi_conn.timeout, 25.0)

    def test_statement_level_timeout_swallows_exception_on_broken_conn(self):
        dialect = SpannerDialect()
        dbapi_conn = mock.MagicMock(spec=spanner_dbapi.Connection)
        dbapi_conn.timeout = 25.0

        context = SpannerExecutionContext()
        context.dialect = dialect
        context.execution_options = {"timeout": 5.0}
        context._dbapi_connection = mock.MagicMock()
        context._dbapi_connection.connection = dbapi_conn

        context.pre_exec()
        eq_(dbapi_conn.timeout, 5.0)

        # Simulate broken connection raising on timeout assignment
        type(dbapi_conn).timeout = mock.PropertyMock(
            side_effect=Exception("Connection broken")
        )

        # Should not raise exception
        context.handle_dbapi_exception(Exception("Original DBAPI error"))
        eq_(context._previous_timeout, _UNSET)
